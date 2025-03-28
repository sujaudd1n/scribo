"""Functions to run from CLI and for argument parsing."""

import argparse
import os

from .build import build_project
from .pinit import initialize
from .__about__ import __version__
from scribo.extensions.linkify.links_ext import create_links_dir

epilog_text = (
    "Thank you for using scribo.\n"
    "To contribute please visit https://github.com/sujaudd1n/scribo."
)


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.init:
        project_name = args.init
        initialize(project_name)
    elif args.build:
        project_root = args.build
        os.chdir(project_root)
        build_project(project_root)
    elif args.linkify:
        project_root = args.linkify
        cwd = os.getcwd()
        os.chdir(project_root)
        create_links_dir(project_root)
        # os.chdir(cwd)
        build_project(project_root)
    else:
        parser.print_help()


def get_parser():
    parser = argparse.ArgumentParser(
        prog="scribo",
        description="Scribo is a static site generator.",
        epilog=epilog_text,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-i", "--init", metavar="project_name", help="Initialize project"
    )
    parser.add_argument(
        "-b",
        "--build",
        metavar="project_dir",
        help="Build site for production",
    )
    parser.add_argument(
        "-l",
        "--linkify",
        metavar="project_dir",
        help="Build links pages from YAML files",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    return parser


if __name__ == "__main__":
    main()
