# AutoVenv

`autovenv.py` is a Python automation script that sets up a new project directory with a virtual environment and optionally installs specified Python packages.

## Features

* Creates a project directory inside the user's `Documents` folder. (feel free to change the base directory in the code, line 83)
* Creates a Python virtual environment within the project directory.
* Optionally installs Python packages specified by the user.
* Logs actions and errors to `autovenv.log`.

## Requirements

* Python 3.6+
* `loguru` Python library for logs

Install `loguru` if not already installed:

```bash
pip install loguru
```

## Usage

1. Run the script:

```bash
python autovenv.py
```

2. Follow the prompts:

* Enter the new project name.
* Optionally provide a space-separated list of libraries to install (e.g., `requests pandas`), or press Enter to skip.

## Output

* A new directory will be created in `~/Documents`.
* A virtual environment will be created inside that directory under `venv/`.
* If libraries were specified, they will be installed into the virtual environment.
* Logs will be saved in `autovenv.log`.

## Activating the Virtual Environment

**Windows:**

```cmd
<project_path>\venv\Scripts\activate
```

**Linux/macOS:**

```bash
source <project_path>/venv/bin/activate
```

## Notes

* The base directory for new projects is set to the user's `Documents` folder. This can be changed by modifying the `base_dir` variable in the script.
* Existing directories or environments will not be overwritten.
  
