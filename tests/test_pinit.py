import os

DIST_DIR = "dist"
project_name = "testproject"

from scribo.pinit import *

os.chdir("tests")

def test_initialize():
    initialize(project_name)
    assert os.path.exists(project_name)