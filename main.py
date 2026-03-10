import argparse
from sys import platform
from os import path, scandir
import questionary
from rich.console import Console

import nbtlib
from datetime import date
from shutil import copytree
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger("mc-creative-clone")
console = Console()


def get_prism_path() -> str:
    # Detect OS
    if platform == "linux" or platform == "linux2":
        # OS is Linux
        prism_path = path.expanduser("~/.local/share/PrismLauncher")
    elif platform == "darwin":
        # OS is MacOS
        prism_path = path.expanduser("~/Library/Application Support/PrismLauncher")
    elif platform == "win32":
        # OS is Windows
        prism_path = path.expanduser("~\\AppData\\Roaming\\PrismLauncher")
    else:
        raise Exception(f"{platform} is invalid")

    if path.exists(prism_path):
        return prism_path
    else:
        raise Exception(f"{prism_path} does not exist")


def get_prism_instance(prism_path: str) -> str:

    instances_path = path.join(prism_path, "instances")

    if not path.isdir(instances_path):
        raise Exception(f"{instances_path} is not a valid directory")

    instances_list = [entry for entry in scandir(instances_path) if entry.is_dir()]

    if len(instances_list) == 0:
        raise Exception("Could not find any instances.")

    if len(instances_list) == 1:
        return instances_list[0].path
    else:
        choices = [
            questionary.Choice(title=instance.name, value=instance.path)
            for instance in instances_list
        ]
        return questionary.select("Choose an instance", choices=choices).ask()


def parse_args() -> argparse.Namespace:

    default_prism_path = get_prism_path()

    parser = argparse.ArgumentParser(
        prog="Minecraft Creative Copt",
        description="Copies a minecraft world as a creative world.",
    )

    parser.add_argument("--prism-path", default=default_prism_path)
    parser.add_argument("-v", "--verbose", action="store_true")

    return parser.parse_args()


def get_minecraft_folder(prism_path: str, instance_name: str):
    instance_path = path.join(prism_path, "instances", instance_name)

    instance_minecraft_dir = path.join(instance_path, "minecraft")
    if not path.isdir(instance_minecraft_dir):
        instance_minecraft_dir = path.join(instance_path, ".minecraft")
    if not path.isdir(instance_minecraft_dir):
        raise Exception(f"Could not find minecraft directory in {instance_path}")
    return instance_minecraft_dir


def get_save_folder(prism_path: str, instance_name: str) -> str:

    instance_minecraft_dir = get_minecraft_folder(prism_path, instance_name)

    instance_save_path = path.join(instance_minecraft_dir, "saves")
    if not path.isdir(instance_save_path):
        raise Exception(f"Could not find saves path in {instance_minecraft_dir}")

    save_folders = [entry for entry in scandir(instance_save_path) if entry.is_dir()]

    if len(save_folders) == 0:
        raise Exception(f"Could not find any save folders in {instance_save_path}.")

    if len(save_folders) == 1:
        return save_folders[0].path
    else:
        choices = [
            questionary.Choice(title=world.name, value=world.path)
            for world in save_folders
        ]
        return questionary.select("Choose a world to copy", choices=choices).ask()


def get_level_dat(world_path: str) -> str:
    level_dat_path = path.join(world_path, "level.dat")

    if not path.isfile(level_dat_path):
        raise Exception(f"{level_dat_path} is not a valid filepath.")

    return level_dat_path


def copy_world(world_path: str) -> str:
    new_path = world_path + f"_creative{date.today()}"

    copytree(world_path, new_path)
    return new_path


def patch_level_dat(level_dat_path: str):
    nbt_file = nbtlib.load(level_dat_path)
    nbt_data = nbt_file["Data"]

    level_name = nbt_data["LevelName"]

    nbt_data["allowCommands"] = nbtlib.Byte(1)
    nbt_data["GameType"] = nbtlib.Int(1)
    nbt_data["LevelName"] = nbtlib.String(level_name + "_creative")
    nbt_data["Player"]["playerGameType"] = nbtlib.Int(1)

    nbt_file.save()


def launch_prism():
    return


def main():
    args = parse_args()
    log.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    log.info("Hello from mc-creative-clone!")

    instance = get_prism_instance(args.prism_path)
    log.debug(f"Instance path: {instance}")

    world = get_save_folder(args.prism_path, instance)
    log.debug(f"World path: {world}")

    log.info(f"Making a copy of {path.basename(world)}...")
    new_world = copy_world(world)

    new_level_dat = get_level_dat(new_world)
    log.debug(f"Level.dat path: {new_level_dat}")

    log.info("Patching level.dat...")
    patch_level_dat(new_level_dat)

    log.info("Done!")


if __name__ == "__main__":
    main()
