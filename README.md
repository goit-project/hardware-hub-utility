# Hardware Hub Utility
This repository is part of [GoIT](https://wiki.goit-project.eu/index.php?title=Main_Page) project's open-source silicon hub/repository. It contains **Hardware Hub Utility**, which aims at improving productivity in developing and maintaining silicon IP.

## Installation
The project uses standard [pyproject.toml](https://pip.pypa.io/en/latest/reference/build-system/pyproject-toml/) specification. For example, the project can be built using the [PDM](https://pdm-project.org/en/latest/) manager by following these steps:

1. Clone this repository:
   ```
   git clone git@github.com:goit-project/hardware-hub-utility.git
   ```

2. Build and install

   2.1. Build and install project using PDM:
   ```
   pdm build
   pdm install .
   ```
   alternativelly, for development purposes, editable mode can be enabled:
   ```
   pdm add --dev --editable .
   pdm build
   pdm install .
   ```
   and check if tool is installed by running it
   ```
   pdm run goit --help
   ```
   
   2.2. Build and install project using PDM and [pipx](https://github.com/pypa/pipx):
   ```
   pdm build
   pipx install .
   ```
   or in editable mode:
   ```
   pdm build
   pipx install -editable .
   ```
   At this point, the utility should be available globally. Update environment or open new terminal and type:
   ```
   goit --help
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
