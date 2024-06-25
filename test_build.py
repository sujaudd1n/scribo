import pytest
import filecmp
import os

from build import copy_raw_project_dir

project_name = 'myproject'

def test_copy_raw_project_dir():
    copy_raw_project_dir(project_name)
    for root, dirs, files in os.walk(project_name):
        for file in files:
            file1 = os.path.join(root, file)
            file2 = os.path.join('dist', os.path.relpath(file1, project_name))
            print(file1, file2)
            assert filecmp.cmp(file1, file2)

