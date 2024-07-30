import shutil
import os
from .copy_and_minimize import copy_and_minimize_static_files
from .render import render

DIST_DIR = "dist"


def build_project(project_root):
    """
    project_root: Directory containing the project.
    """
    os.chdir(project_root)
    create_dist_dir(DIST_DIR)
    copy_and_minimize_static_files()
    render()


def create_dist_dir(dir_name):
    """
    Create dist dir.
    If it exists, it gets deleted and a new dir is created.
    """
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.mkdir(dir_name)
