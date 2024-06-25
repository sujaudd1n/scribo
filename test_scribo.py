import pytest
import os
import shutil

from scribo import create_project_structure


def list_files(dir):
    result = []
    for path, dirs, files in os.walk(dir):
        for file in files:
            result.append(os.path.join(path, file)) 
    return result


def test_create_project_structure():
    PROJECT_NAME = 'myproject'
    if os.path.exists(PROJECT_NAME):
        shutil.rmtree(PROJECT_NAME)

    create_project_structure(PROJECT_NAME)

    assert len(list_files(PROJECT_NAME)) == 4
    assert os.path.exists(PROJECT_NAME)
    assert os.path.exists(os.path.join(PROJECT_NAME, "md/getting-started"))
    assert os.path.exists(os.path.join(PROJECT_NAME, "script"))
    assert os.path.exists(os.path.join(PROJECT_NAME, "style"))
    assert os.path.exists(os.path.join(PROJECT_NAME, "style/style.css"))
    assert os.path.exists(os.path.join(PROJECT_NAME, "script/script.js"))
    assert os.path.exists(os.path.join(PROJECT_NAME, "index.html"))
