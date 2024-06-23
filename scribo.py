import os
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
    pass

if __name__ == '__main__':
    main()
