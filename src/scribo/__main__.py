"""Functions to run from CLI and for argument parsing."""
import argparse

from .build import build_project
from .pinit import initialize
from .__about__ import __version__
from .__init__ import __doc__

epilog_text = "Thank you for using scribo.\n"\
              "To contribute please visit https://github.com/sujaudd1n/scribo."

def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.init:
        project_name = args.init
        initialize(project_name)
    elif args.build:
        project_root = args.build
        build_project(project_root)
    else:
        parser.print_usage()
        print("\n" + epilog_text)


def get_parser():
    parser = argparse.ArgumentParser(
        prog="scribo",
        description="Scribo is a static site generator.",
        epilog=epilog_text,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-i", "--init", metavar="project-name", help="Initialize project")
    parser.add_argument("-b", "--build", metavar="project-name", help="Build site for production")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


if __name__ == "__main__":
    main()
