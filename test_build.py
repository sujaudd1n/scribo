import pytest
import filecmp
import os

from build import create_dist_dir

DIST_DIR = 'dist'
project_name = 'myproject'

'''
def test_copy_raw_project_dir():
    os.chdir(project_name)
    copy_raw_project_dir(project_name)
    for root, dirs, files in os.walk(project_name):
        for file in files:
            file1 = os.path.join(root, file)
            file2 = os.path.join('dist', os.path.relpath(file1, project_name))
            print(file1, file2)
            assert filecmp.cmp(file1, file2)
    os.chdir('..')
'''

def test_create_dist_dir():
    create_dist_dir()
    assert os.path.exists(DIST_DIR)