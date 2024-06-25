import os
import pathlib

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
    os.chdir('..')

def write_to_project_files(project_name):
    
    write_from_source_to_dest("templates/index.html", f"{project_name}/index.html")
    write_from_source_to_dest("templates/style.css", f"{project_name}/style/style.css")
    write_from_source_to_dest("templates/script.js", f"{project_name}/style/style.js")

def write_from_source_to_dest(source, dest):
    with open(dest, "w") as dest:
        with open(source) as source:
            dest.write(source.read())
