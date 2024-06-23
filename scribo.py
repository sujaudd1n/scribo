import os
import shutil
import pathlib
import sys
import argparse

def main():
    cl_args = parse_command_line_args()
    if cl_args.init:
        create_project_structure(cl_args.init)


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init", help="Initialize project structure")
    return parser.parse_args()

def create_project_structure(project_name):
    os.mkdir(project_name)
    os.chdir(project_name)
    os.makedirs("md/getting-started", exist_ok=True)
    pathlib.Path("md/getting-started/index.md").touch()
    os.makedirs("style")
    os.makedirs("script")
    pathlib.Path("index.html").touch()
    os.chdir('..')

if __name__ == '__main__':
    main()
