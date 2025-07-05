#   LIBS
from loguru import logger
import sys
import subprocess
from pathlib import Path
from typing import List

#   FUN
def logging_setup():
    logger.remove()
    logger.add(
        sys.stderr,
        format='<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<blue>{function}</blue>:<blue>{line}</blue> - <level>{message}</level>',
        level="INFO"
    )
    logger.add(
        "autovenv.log",
        rotation='1 MB',
        retention='10 days',
        level="DEBUG",
        enqueue=True
    )

def create_dir(dir_path: Path):
    if dir_path.exists():
        logger.warning(f"Directory already exists: {dir_path}")
        return

    logger.info(f"Creating directory: {dir_path}")
    try:
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.success(f"Directory created: {dir_path}")
    except OSError as e:
        logger.error(f"Failed to create directory {dir_path}: {e}")
        raise

def create_venv(venv_path: Path):
    if venv_path.exists():
        logger.warning(f"Virtual environment already exists: {venv_path}")
        return

    logger.info(f"Creating virtual environment at {venv_path}")
    try:
        subprocess.run(
            [sys.executable, '-m', 'venv', str(venv_path)],
            check=True,
            capture_output=True
        )
        logger.success(f"Virtual environment created at {venv_path}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error creating venv: {e.stderr.decode().strip()}")
        raise

def get_venv_python(venv_path: Path) -> Path:
    if sys.platform == "win32": # for win
        return venv_path / "Scripts" / "python.exe"
    else:                       # linux/mac
        return venv_path / "bin" / "python"

def install_packages(venv_path: Path, packages: List[str
    if not packages:
        logger.info("No packages requested for installation.")
        return

    python_exe = get_venv_python(venv_path)
    if not python_exe.exists():
        logger.error(f"Could not find python executable in venv: {python_exe}")
        raise FileNotFoundError("Virtual environment's Python interpreter not found.")

    logger.info(f"Installing packages: {', '.join(packages)}")
    try:
        command = [str(python_exe), '-m', 'pip', 'install'] + packages
        subprocess.run(command, check=True, capture_output=True, text=True)
        logger.success("All packages installed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install packages. Pip output:\n{e.stderr}")
        raise

def main():
    logging_setup()
    logger.info("Script started")

    base_dir = Path.home() / "Documents"    # change bade directory if needed

    if not base_dir.exists():
        logger.warning(f"Base directory '{base_dir}' does not exist. Creating it now.")
        create_dir(base_dir)

    new_dir_name = input(f"Enter new project name (will be created in '{base_dir}'): ").strip()

    if not new_dir_name:
        logger.error("Project name cannot be empty.")
        sys.exit(1)

    project_path = base_dir / new_dir_name
    venv_path = project_path / 'venv'

    try:
        create_dir(project_path)

        create_venv(venv_path)

      
        libs_to_install_str = input("Enter libraries to install (space-separated, e.g., 'requests pandas loguru'), or press Enter to skip: ").strip()
        
        if libs_to_install_str:
            package_list = libs_to_install_str.split()
            install_packages(venv_path, package_list)

        logger.info("-" * 60)
        logger.success(f"Setup complete! Project is ready at: {project_path}")
        logger.info(f"To activate the virtual environment (Windows), run:\n{venv_path / 'Scripts' / 'activate'}")
        logger.info(f"To activate the virtual environment (Linux/macOS), run:\n. {venv_path / 'bin' / 'activate'}")
        logger.info("-" * 60)

    except Exception as e:
        logger.critical(f"Script failed: {e}")
        sys.exit(1)

    logger.success("Script completed successfully.")


if __name__ == "__main__":
    main()