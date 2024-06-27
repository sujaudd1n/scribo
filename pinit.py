import os
import pathlib

def create_project_structure(project_name):
    create_project_dirs(project_name)
    write_to_project_files(project_name)

def create_project_dirs(project_name):
    os.mkdir(project_name)
    os.chdir(project_name)
    os.makedirs("md/getting-started")
    os.makedirs("style")
    os.makedirs("script")
    os.chdir('..')


def write_to_project_files(project_name):
    def write_from_source_to_dest(source, dest):
        with open(dest, "w") as dest:
            with open(source) as source:
                dest.write(source.read())

    write_from_source_to_dest("templates/index.html", f"{project_name}/index.html")
    write_from_source_to_dest("templates/style.css", f"{project_name}/style/style.css")
    write_from_source_to_dest("templates/script.js", f"{project_name}/script/script.js")
    write_from_source_to_dest("templates/meta.json", f"{project_name}/meta.json")
    write_from_source_to_dest("templates/index.md", f"{project_name}/md/getting-started/index.md")