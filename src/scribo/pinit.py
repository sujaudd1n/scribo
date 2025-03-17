"""
Module to initialize project.
"""

import os
import shutil
import sys
from scribo.helper import colorize

PROJECT_TEMPLATE = os.path.join(os.path.dirname(__file__), "skeleton")


def initialize(project_name):
    """
    Initialize a new project by creating a directory and copying the template.

    Args:
        project_name (str): Name of the project to initialize.
    """
    try:
        initialize_project_dir(project_name)
        print(colorize(f"Project '{project_name}' has been initialized.\n", "green"))
        print(f"Run:\n$ cd {project_name}\nAnd start editing files.")
    except Exception as e:
        sys.exit(colorize(f"{e}", "red"))


def initialize_project_dir(project_name):
    """
    Create a project directory by copying the PROJECT_TEMPLATE.

    Args:
        project_name (str): Name of the project directory to create.

    Raises:
        SystemExit: If the project directory already exists.
    """
    if os.path.exists(project_name):
        raise FileExistsError(f"Project directory '{project_name}' already exists!")

    shutil.copytree(PROJECT_TEMPLATE, project_name)
