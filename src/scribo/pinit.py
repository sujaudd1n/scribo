"""
Module to initialize project.
"""

import os
import shutil
import sys
import json
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
        write_custom_meta(project_name)
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


def write_custom_meta(project_name):
    data = {
        "title": project_name,
        "project_name": project_name,
        "description": f"{project_name} - built with scribo",
        "author": project_name,
        "production_urls": [
            "http://localhost:8000",
        ],
        "base_url": "/",
        "quick_links": [
            {"name": "Home", "url": "/"},
        ],
        "nav_links": [{"name": "Github", "url": "https://github.com/sujaudd1n/scribo"}],
        "_comment": "Docs for this meta file: <>",
    }

    filename = "meta.json"
    with open(project_name + "/" + filename, "w") as json_file:
        json.dump(data, json_file, indent=4)
