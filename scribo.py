import os
import shutil
import pathlib
import sys
import argparse


def main():
    cl_args = parse_command_line_args()

    if cl_args.init:
        project_name = cl_args.init
        if os.path.exists(project_name):
            sys.exit(f"Project: {project_name} already exists!")
        else:
            create_project_structure(project_name)


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init", help="Initialize project structure")
    return parser.parse_args()


def create_project_structure(project_name):
    create_project_dirs(project_name)
    write_to_project_files()


def create_project_dirs(project_name):
    os.mkdir(project_name)
    os.chdir(project_name)
    pathlib.Path("index.html").touch()
    os.makedirs("md/getting-started")
    pathlib.Path("md/getting-started/index.md").touch()
    os.makedirs("style")
    pathlib.Path("style/style.css").touch()
    os.makedirs("script")
    pathlib.Path("script/script.js").touch()
    os.chdir("..")


def write_to_project_files(project_name):
    def write_from_source_to_dest(source, dest):
        with open(f"{project_name}/index.html", "w") as dest:
            with open("templates/index.html") as source:
                dest.write(source.read())

    write_from_source_to_dest("templates/index.html", f"{project_name}/index.html")
    write_from_source_to_dest("templates/style.css", f"{project_name}/style/style.css")
    write_from_source_to_dest("templates/script.js", f"{project_name}/style/style.js")


if __name__ == "__main__":
    main()
