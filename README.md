# Hardware Hub Utility
This repository is part of [GoIT](https://wiki.goit-project.eu/index.php?title=Main_Page) project's open-source silicon hub/repository. It contains **Hardware Hub Utility**, which aims at improving productivity in developing and maintaining silicon IP.

## Table of Contents
* [Setup](#setup)
  + [Installation from sources](#installation-from-sources)
  + [Autocomplete](#autocomplete)
* [Contents](#contents)
* [Usage](#usage)

## Setup
### Installation from sources
The project uses standard [pyproject.toml](https://pip.pypa.io/en/latest/reference/build-system/pyproject-toml/) specification. For example, the project can be built using the [PDM](https://pdm-project.org/en/latest/) manager by following these steps:

1. Clone the repository:
   ```
   git clone git@github.com:goit-project/hardware-hub-utility.git
   ```

2. Build and install
   ```
   pdm build
   ```
   alternativelly, for development purposes, enable editable mode:
   ```
   pdm add --dev --editable .
   pdm build
   ```

3. Install
   ```
   pdm install .
   ```
   
4. The project incoroporates both - an application (utility) and package. Therefore, unless a global installation is performed, a virtual environment must be enabled
   ```
   eval $(pdm venv activate)
   ```
   
5. Test the tool:
   ```
   goit help
   ```
   
### Autocomplete
It is highly recommended to set up argument completion as it will save a lot of time. The utility achieves this with [argcomplete](https://pypi.org/project/argcomplete/) python package. There is a script which attempts to set up autocomplete on your system for BASH or ZSH. The application utilizes BASH completion, which, in the case of ZSH, must be explicitly enabled. The script attempts to do that.
```
chmod +x autocomplete.sh
./autocomplete.sh
```

## Contents

- `src/goit/subcommands/`: This directory contains...

- `src/goit/classes/`: This directory contains...

- `pyproject.toml`: This script is for performing...

## Usage

Here are some common tasks you can perform using this project:

- **Check**: Run the following command to check if the file meets the requirements. 
   ```
   goit check -i <vhdl_file_path>
   ```
