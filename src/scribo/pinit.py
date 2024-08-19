import os
import shutil

PROJECT_TEMPLATE = os.path.join(os.path.dirname(__file__), "sample")


def initialize(project_name):
    """Initialize the project."""
    create_project_dir(project_name)


def create_project_dir(project_name):
    """
    Create project directory by copying PROJECT_TEMPLATE
    as project_name.
    """
    shutil.copytree(PROJECT_TEMPLATE, project_name)
