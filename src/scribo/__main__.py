r"""
Functions to run from CLI and for argument parsing.
"""
import argparse

from .build import build_project
from .pinit import initialize


def main():
    args = parse_command_line_args()

    if args.init:
        project_name = args.init
        initialize(project_name)
    elif args.build:
        project_root = args.build
        build_project(project_root)
    else:
        print("This is Scribo beta")


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init", help="Initialize project")
    parser.add_argument("-b", "--build", help="Build site for production")
    return parser.parse_args()


if __name__ == "__main__":
    main()
