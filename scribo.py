import os
import shutil
import pathlib
import sys
import argparse

from pinit import create_project_structure

def main():
    cl_args = parse_command_line_args()

    if cl_args.init:
        project_name = cl_args.init
        if os.path.exists(project_name):
            sys.exit(f"Project: {project_name} already exists!")
        else:
            create_project_structure(project_name)
    elif cl_args.build:
        project_name = cl_args.build
        build_project(project_name)


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init", help="Initialize project structure")
    parser.add_argument("-b", "--build", help="Build static site for production")
    return parser.parse_args()

if __name__ == '__main__':
    main()
