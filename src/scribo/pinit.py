import os
import shutil
import sys

PROJECT_TEMPLATE = os.path.join(os.path.dirname(__file__), "sample")


def initialize(project_name):
    """Initialize the project."""
    create_project_dir(project_name)


def create_project_dir(project_name):
    """
    Create project directory by copying PROJECT_TEMPLATE
    as project_name.
    """

    if os.path.exists(project_name):
        sys.exit(f"Project: {project_name} already exists!")
    shutil.copytree(PROJECT_TEMPLATE, project_name)
