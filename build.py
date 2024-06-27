import shutil
import os
import json
import markdown as md
from jinja2 import Environment, select_autoescape, FileSystemLoader

DIST_DIR = "dist"


def build_project(project_root):
    os.chdir(project_root)
    create_dist_dir()
    render()


def create_dist_dir():
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.mkdir(DIST_DIR)
    os.mkdir(os.path.join(DIST_DIR, "blogs"))


def render():
    render_index_html()
    render_markdown()


def render_index_html():
    env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape)
    template = env.get_template("index.html")

    with open("meta.json") as metafile:
        meta = json.load(metafile)

    rendered_template = template.render(
        title=meta["title"],
        description=meta["description"],
        author=meta["author"],
    )

    OUTPUT_FILE = os.path.join(DIST_DIR, "index.html")
    with open(OUTPUT_FILE, "w") as out:
        out.write(rendered_template)


def render_markdown():
    for root, dirs, files in os.walk("md"):
        for file in files:
            filepath = os.path.join(root, file)
            out_file_dir = os.path.join(DIST_DIR, "blogs", filepath.split(os.sep)[1])
            os.mkdir(out_file_dir)
            with open(filepath) as input_md:
                with open(
                    os.path.join(out_file_dir, file.split('.')[0] + '.html'),
                    "w",
                ) as output:
                    output.write(md.markdown(input_md.read()))
