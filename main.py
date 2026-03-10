import argparse
from datetime import date
import logging
from os import scandir
from pathlib import Path
import re
from shutil import copytree, move, rmtree
from sys import platform

import nbtlib
import questionary
from rich.console import Console
from rich.logging import RichHandler

logging.basicConfig(
    level="WARNING",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger("mc-creative-clone")
console = Console()


def get_prism_path() -> Path:
    """Detects the OS and returns the PrismLauncher data directory.

    Returns:
        Path: The path to the PrismLauncher data directory.

    Raises:
        ValueError: If the current platform is not supported.
        FileNotFoundError: If the PrismLauncher data directory does not exist.
    """
    # Detect OS
    if platform == "linux" or platform == "linux2":
        # OS is Linux
        prism_path = Path("~/.local/share/PrismLauncher").expanduser()
    elif platform == "darwin":
        # OS is MacOS
        prism_path = Path("~/Library/Application Support/PrismLauncher").expanduser()
    elif platform == "win32":
        # OS is Windows
        prism_path = Path("~\\AppData\\Roaming\\PrismLauncher").expanduser()
    else:
        raise ValueError(f"{platform} is invalid")

    if prism_path.exists():
        return prism_path
    raise FileNotFoundError(f"{prism_path} does not exist")


def get_prism_instance(prism_path: Path, instance_name: str | None = None) -> Path:
    """Finds and returns the path of a PrismLauncher instance.

    If multiple instances are found, the user is prompted to select one.

    Args:
        prism_path: The path to the PrismLauncher data directory.
        instance_name: The name of the instance to select. If None, prompts interactively.

    Returns:
        Path: The path to the selected PrismLauncher instance.

    Raises:
        FileNotFoundError: If the instances directory or no instances are found.
    """
    instances_path = prism_path / "instances"

    if not instances_path.is_dir():
        raise FileNotFoundError(f"{instances_path} is not a valid directory")

    instances_list = [entry for entry in scandir(instances_path) if entry.is_dir()]

    if instance_name is not None:
        match = next((i for i in instances_list if i.name == instance_name), None)
        if match is None:
            raise FileNotFoundError(f"Could not find instance '{instance_name}'.")
        return Path(match.path)

    if len(instances_list) == 0:
        raise FileNotFoundError("Could not find any instances.")

    if len(instances_list) == 1:
        return Path(instances_list[0].path)
    choices = [
        questionary.Choice(title=instance.name, value=instance.path)
        for instance in instances_list
    ]
    return Path(questionary.select("Choose an instance", choices=choices).ask())


def parse_args() -> argparse.Namespace:
    """Parses and returns command line arguments.

    Returns:
        argparse.Namespace: The parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        prog="mc-creative-clone",
        description="Copies a minecraft world and converts it to a creative mode world.",
        epilog="If no options are provided, the script will run interactively.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--prism-path",
        "-p",
        default=None,
        metavar="PATH",
        help="Path to the PrismLauncher data directory. "
        "Defaults to the standard OS path if not specified.",
    )
    parser.add_argument(
        "--instance",
        "-i",
        default=None,
        metavar="INSTANCE",
        help="Name of the PrismLauncher instance to use."
        "Promped interactively if not specified.",
    )
    parser.add_argument(
        "--world",
        "-w",
        default=None,
        metavar="WORLD",
        help="Name of the world to copy. Prompted interactively if not specified.",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Overwrite the destination world if it already exists, without prompting.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose (debug) logging output.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview actions without making any changes to the filesystem.",
    )

    args = parser.parse_args()

    if args.prism_path is None:
        args.prism_path = get_prism_path()

    return args


def get_minecraft_folder(instance_path: Path) -> Path:
    """Finds and returns the .minecraft directory for a given instance.

    Args:
        instance_path: The path of the PrismLauncher instance.

    Returns:
        Path: The path to the .minecraft directory.

    Raises:
        FileNotFoundError: If the .minecraft directory cannot be found.
    """
    instance_minecraft_dir = instance_path / "minecraft"
    if not instance_minecraft_dir.is_dir():
        instance_minecraft_dir = instance_path / ".minecraft"
    if not instance_minecraft_dir.is_dir():
        raise FileNotFoundError(
            f"Could not find minecraft directory in {instance_path}"
        )
    return instance_minecraft_dir


def get_save_folder(minecraft_folder_path: Path, world_name: str | None = None) -> Path:
    """Finds and returns the path of a Minecraft world save folder.

    If multiple worlds are found, the user is prompted to select one.

    Args:
        minecraft_folder_path: The path of the PrismLauncher instance .minecraft folder.
        world_name: The name of the world to select. If None, prompts interactively.

    Returns:
        Path: The path to the selected world save folder.

    Raises:
        FileNotFoundError: If the saves directory or no save folders are found.
    """
    instance_save_path = minecraft_folder_path / "saves"
    if not instance_save_path.is_dir():
        raise FileNotFoundError(f"Could not find saves path in {minecraft_folder_path}")

    save_folders = [entry for entry in scandir(instance_save_path) if entry.is_dir()]

    if world_name is not None:
        match = next((w for w in save_folders if w.name == world_name), None)
        if match is None:
            raise FileNotFoundError(f"Could not find world '{world_name}'.")
        return Path(match.path)

    if len(save_folders) == 0:
        raise FileNotFoundError(
            f"Could not find any save folders in {instance_save_path}."
        )

    if len(save_folders) == 1:
        return Path(save_folders[0].path)
    choices = [
        questionary.Choice(title=world.name, value=world.path) for world in save_folders
    ]
    return Path(questionary.select("Choose a world to copy", choices=choices).ask())


def get_level_dat(world_path: Path) -> Path:
    """Finds and returns the path of a world's level.dat file.

    Args:
        world_path: The path to the world save folder.

    Returns:
        Path: The path to the level.dat file.

    Raises:
        FileNotFoundError: If the level.dat file does not exist.
    """
    level_dat_path = world_path / "level.dat"

    if not level_dat_path.is_file():
        raise FileNotFoundError(f"{level_dat_path} is not a valid filepath.")

    return level_dat_path


def get_creative_world_path(world_path: Path) -> Path:
    """Generates the path for the creative backup world.

    Appends '_creative' and the current date to the original world path.

    Args:
        world_path: The path to the original world save folder.

    Returns:
        Path: The path to the creative backup world.
    """
    return Path(str(world_path) + f"_creative_{date.today()}")


def copy_world(world_path: Path, force: bool = False) -> Path:
    """Copies a world folder and returns the path of the new copy.

    The world folder is named with the original name suffixed by
    '_creative' and the current date.

    Args:
        world_path: The path to the world save folder to copy.
        force: If True, overwrites the destination without prompting.

    Returns:
        Path: The path to the newly created world copy.
    """
    new_path = get_creative_world_path(world_path)

    if new_path.exists():
        if force:
            log.debug(f"Removing {new_path}...")
            rmtree(new_path)
        else:
            log.warning(f"{new_path} already exists")
            overwrite = questionary.confirm(
                f"{new_path} already exists. Overwrite?"
            ).ask()
            if overwrite:
                log.debug(f"Removing {new_path}...")
                rmtree(new_path)
            else:
                numbers = [
                    int(m.group(1))
                    for path in scandir(new_path.parent)
                    if path.is_dir()
                    and (
                        m := re.search(
                            rf"{re.escape(new_path.name)}_old_(\d+)$",
                            path.name,
                        )
                    )
                ]

                next_number = max(numbers, default=0) + 1

                backup_path = new_path.parent / f"{new_path.name}_old_{next_number}"
                log.debug(f"Renaming {new_path} to {backup_path}...")
                move(new_path, backup_path)
                log.debug(f"Renamed {new_path} to {backup_path}")

    log.debug(f"Copying {world_path} to {new_path}...")
    copytree(world_path, new_path)
    log.debug(f"Copied {world_path} to {new_path}")
    return new_path


def patch_level_dat(level_dat_path: Path) -> None:
    """Patches a level.dat file to enable creative mode and cheats.

    Sets GameType to Creative, enables cheats, and updates the world
    and player game modes.

    Args:
        level_dat_path: The path to the level.dat file to patch.
    """
    nbt_file = nbtlib.load(level_dat_path)
    nbt_data = nbt_file["Data"]

    level_name = nbt_data["LevelName"]

    nbt_data["allowCommands"] = nbtlib.Byte(1)
    nbt_data["GameType"] = nbtlib.Int(1)
    nbt_data["LevelName"] = nbtlib.String(level_name + "_creative")
    nbt_data["Player"]["playerGameType"] = nbtlib.Int(1)

    nbt_file.save()


def launch_prism() -> None:
    """Launches PrismLauncher with the specified instance and world."""
    return


def main() -> None:
    """Main entry point for mc-creative-clone."""
    args = parse_args()
    log.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    log.info("Hello from mc-creative-clone!")

    instance = get_prism_instance(args.prism_path, args.instance)
    log.debug(f"Instance path: {instance}")

    minecraft_folder = get_minecraft_folder(instance)
    log.debug(f"Minecraft folder: {minecraft_folder}")

    world = get_save_folder(minecraft_folder, args.world)
    log.debug(f"World path: {world}")

    new_world = get_creative_world_path(world)
    if args.dry_run:
        log.info(f"[DRY RUN] Would make a copy of {world.name}")
        log.info(f"[DRY RUN] Would patch level.dat at {new_world / 'level.dat'}")
    else:
        log.info(f"Making a copy of {world.name}...")
        new_world = copy_world(world, args.force)
        log.info(f"Copied {world.name}")

        new_level_dat = get_level_dat(new_world)
        log.debug(f"Level.dat path: {new_level_dat}")
        log.debug(f"Patching {new_level_dat}...")
        patch_level_dat(new_level_dat)
        log.debug(f"Patched {new_level_dat}")

    log.info("Done!")


if __name__ == "__main__":
    main()
