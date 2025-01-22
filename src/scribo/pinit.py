"""
Module to initialize project.
"""

import os
import shutil
import sys
from scribo.helper import print_with_color

PROJECT_TEMPLATE = os.path.join(os.path.dirname(__file__), "project_template")


def initialize(project_name):
    """Initialize the project."""
    initialize_project_dir(project_name)
    print_with_color(f"Project {project_name} has been initialized.\n", "green")
    print(f"Run\n$ cd {project_name}\nAnd start editing files.")


def initialize_project_dir(project_name):
    """
    Create a directory called <project_name> by copying PROJECT_TEMPLATE
    in current working directory.

    If <project_name> dir already exists, it prints a message and exits.
    """
    if os.path.exists(project_name):
        sys.exit(f"\x1b[31mproject {project_name} already exists!\x1b[0m")
    shutil.copytree(PROJECT_TEMPLATE, project_name)
