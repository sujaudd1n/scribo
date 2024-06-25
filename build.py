import shutil
import os

def copy_raw_project_dir(project_name):
    """
    Copies project's content into dist
    """
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    shutil.copytree(project_name, 'dist')