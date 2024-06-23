import pytest
import os

from scribo import create_project_structure


def test_create_project_structure():
    PROJECT_NAME = 'myproject'
    create_project_structure(PROJECT_NAME)
    assert(os.path.exists(PROJECT_NAME))
    assert(os.path.exists(os.path.join(PROJECT_NAME, "md/getting-started")))
    assert(os.path.exists(os.path.join(PROJECT_NAME, "script")))
    assert(os.path.exists(os.path.join(PROJECT_NAME, "style")))
    assert(os.path.exists(os.path.join(PROJECT_NAME, "index.html")))
