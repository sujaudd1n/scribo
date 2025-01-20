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
    parser = argparse.ArgumentParser(
        prog="scribo",
        description="Scribo is a static site generator.",
        epilog="Thank you for using scribo.\n"
        "To contribute please visit https://github.com/sujaudd1n/scribo.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subcommand_help_text = "Enter subcommand\nhi"\
    "Valid subcommands are:\n"\
    "* init - Initialize a project"
    parser.add_argument("subcommand", choices=["init", "build"], help=subcommand_help_text)
    # parser.add_argument("-i", "--init", help="Initialize project")
    # parser.add_argument("-b", "--build", help="Build site for production")
    return parser.parse_args()


if __name__ == "__main__":
    main()
