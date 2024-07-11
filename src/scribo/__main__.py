import os
import shutil
import pathlib
import sys
import argparse

from .scribo.pinit import initialize
from .scribo.build import build_project


def main():
    args = parse_command_line_args()

    if args.init:
        project_name = args.init
        if os.path.exists(project_name):
            sys.exit(f"Project: {project_name} already exists!")
        else:
            initialize(project_name)
    elif args.build:
        project_root = args.build
        build_project(project_root)


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init", help="Initialize project structure")
    parser.add_argument("-b", "--build", help="Build static site for production")
    return parser.parse_args()


if __name__ == "__main__":
    main()
