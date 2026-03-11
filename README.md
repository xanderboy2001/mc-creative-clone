<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPL-3.0-or-later][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<h3 align="center">Minecraft Creative Backup</h3>

  <p align="center">
    A command-line tool that copies a Minecraft world save, patches it into creative mode with cheats enabled, and launches it through PrismLauncher — all in one command.
    <br />
    <a href="https://github.com/xanderboy2001/mc-creative-clone"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/xanderboy2001/mc-creative-clone">View Demo</a>
    &middot;
    <a href="https://github.com/xanderboy2001/mc-creative-clone/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/xanderboy2001/mc-creative-clone/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#options">Options></a></li>
        <li><a href="#examples"><Examples></a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Minecraft Creative Backup is a Python CLI tool that automates the process of creating creative mode backups of Minecraft worlds managed by PrismLauncher.

When building or experimenting in Minecraft, it's useful to have a creative mode copy of a survival world - but doing it manually means copying the folder, opening the world, changing the game mode, and enabling cheats. This tool automates all of that in a single command.

### What it does

- Copies a Minecraft world save folder
- Patches the world's `level.dat` to enable creative mode and cheats
- Renames the backup with the current date for easy identification
- Launches the instance directly through PrismLauncher
<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python-badge]][Python-url]
* [![Rich][Rich-badge]][Rich-url]
* [![questionary][questionary-badge]][questionary-url]
* [![nbtlib][nbtlib-badge]][nbtlib-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

- Python 3.14 or higher
- [PrismLauncher](https://prismlauncher.org/) installed and configured with at least one instance and world.
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Installation

1. Clone the repository
```sh
   git clone https://github.com/xanderboy2001/mc-creative-clone.git
   cd mc-creative-clone
```

2. Install the package
```sh
   uv tool install .
```

   Or with pip:
```sh
   pip install .
```

3. Verify the installation
```sh
   mc-creative-clone --help
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Run the tool interactively - you will be prompted to select an instance and world:
```sh
mc-creative-clone
```

Or specify options directly to skip the interactive prompts
```sh
mc-creative-clone --instance "My instance" --world "My world"
```

### Options

| **Option** | **Short** | **Description** |
| --- | --- | --- |
| `--prism-path PATH` | `-p` | Path to PrismLauncher data directory. Defaults to the standard OS path. |
| `--instance INSTANCE` | `-i` | Name of the PrismLauncher instance to use. |
| `--world WORLD` | `-w` | Name of the world to copy. |
| `--force` | `-f` | Overwrite the destination world if it already exists without prompting. |
| `--dry-run` | | Preview actions without making any changes to the filesystem. |
| `--verbose` | `-v` | Enable verbose debug logging output. |

### Examples

Preview what would happen without making any changes:
```sh
mc-creative-clone --dry-run --instance "Survival" --world "My World"
```


Force overwrite an existing backup:
```sh
mc-creative-clone --force --instance "Survival" --world "My World"
```


Use a custom PrismLauncher data directory:
```sh
mc-creative-clone --prism-path "/path/to/prismlauncher"
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/xanderboy2001/mc-creative-clone/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=xanderboy2001/mc-creative-clone" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the GPL-3.0-or-later. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Alexander Christian - alexanderechristian@gmail.com

Project Link: [https://github.com/xanderboy2001/mc-creative-clone](https://github.com/xanderboy2001/mc-creative-clone)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/xanderboy2001/mc-creative-clone.svg?style=for-the-badge
[contributors-url]: https://github.com/xanderboy2001/mc-creative-clone/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/xanderboy2001/mc-creative-clone.svg?style=for-the-badge
[forks-url]: https://github.com/xanderboy2001/mc-creative-clone/network/members
[stars-shield]: https://img.shields.io/github/stars/xanderboy2001/mc-creative-clone.svg?style=for-the-badge
[stars-url]: https://github.com/xanderboy2001/mc-creative-clone/stargazers
[issues-shield]: https://img.shields.io/github/issues/xanderboy2001/mc-creative-clone.svg?style=for-the-badge
[issues-url]: https://github.com/xanderboy2001/mc-creative-clone/issues
[license-shield]: https://img.shields.io/github/license/xanderboy2001/mc-creative-clone.svg?style=for-the-badge
[license-url]: https://github.com/xanderboy2001/mc-creative-clone/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/alexander-e-christian
[product-screenshot]: images/screenshot.png
<!-- Shields.io badges. You can a comprehensive list with many more badges at: https://github.com/inttter/md-badges -->
[Python-badge]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org
[Rich-badge]: https://img.shields.io/badge/Rich-FAD000?style=for-the-badge&logo=python&logoColor=black
[Rich-url]: https://github.com/Textualize/rich
[questionary-badge]: https://img.shields.io/badge/questionary-4a4a55?style=for-the-badge&logo=python&logoColor=white
[questionary-url]: https://github.com/tmbo/questionary
[nbtlib-badge]: https://img.shields.io/badge/nbtlib-4a4a55?style=for-the-badge&logo=python&logoColor=white
[nbtlib-url]: https://github.com/vberlier/nbtlib
