"""
Module for building a static site.
"""

import os
import shutil
from typing import Optional

from .copy_and_minimize import copy_static, minimize

DIST_DIR = "dist"


def build_project(project_root: str) -> None:
    """
    Execute all the steps to build the project.

    Args:
        project_root (str): The root directory of the project.
    """
    try:
        from .render import render

        create_dist_dir(DIST_DIR)
        copy_static()
        render()
        # minimize(DIST_DIR)
    except Exception as e:
        print(f"Error during build process: {e}")
        raise


def create_dist_dir(dir_name: str) -> None:
    """
    Create a distribution directory named `dir_name`.
    If it exists, it gets deleted and a new directory is created.

    Args:
        dir_name (str): The name of the directory to create.
    """
    try:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        os.makedirs(dir_name)
    except OSError as e:
        print(f"Error creating directory {dir_name}: {e}")
        raise
