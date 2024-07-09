import os
import shutil


SAMPLE_CODE_DIR = "sample"


def initialize(project_name):
    create_project_dir(project_name)


def create_project_dir(project_name):
    shutil.copytree(SAMPLE_CODE_DIR, project_name)
