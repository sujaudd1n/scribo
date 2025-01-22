"""
Module for building site.
"""

import os
import shutil

from .copy_and_minimize import copy_and_minimize_static_files

DIST_DIR = "dist"


def build_project(project_root):
    """Execute all the steps to build the project."""
    os.chdir(project_root)
    from .render import render

    create_dist_dir(DIST_DIR)
    copy_and_minimize_static_files()
    render()


def create_dist_dir(dir_name):
    """
    Create dist directory named dir_name.
    If it exists, it gets deleted and a new directory is created.
    """
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.mkdir(dir_name)
