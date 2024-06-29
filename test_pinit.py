import pytest
import os
import shutil

from pinit import create_project_dirs
from pinit import write_to_project_files


def test_create_project_dirs():
    PROJECT_NAME = "myproject"
    if os.path.exists(PROJECT_NAME):
        shutil.rmtree(PROJECT_NAME)

    create_project_dirs(PROJECT_NAME)

    assert os.path.exists(PROJECT_NAME)
    assert os.path.exists(os.path.join(PROJECT_NAME, "md/getting-started"))
    assert os.path.exists(os.path.join(PROJECT_NAME, "script"))
    assert os.path.exists(os.path.join(PROJECT_NAME, "style"))


def test_write_to_project_files():
    project_name = "myproject"
    write_to_project_files(project_name)

    def compare_source_to_dest(source, dest):
        with open(dest) as dest:
            with open(source) as source:
                return dest.read() == source.read()

    assert compare_source_to_dest(
        "templates/index.html", f"{project_name}/index.html"
    )
    assert compare_source_to_dest(
        "templates/style.css", f"{project_name}/style/style.css"
    )
    assert compare_source_to_dest(
        "templates/script.js", f"{project_name}/script/script.js"
    )
    assert compare_source_to_dest(
        "templates/meta.json", f"{project_name}/meta.json"
    )
    assert compare_source_to_dest(
        "templates/index.md", f"{project_name}/md/getting-stated/index.md"
    )
