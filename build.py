import shutil
import os
import json
import markdown as md
from jinja2 import Environment, select_autoescape, FileSystemLoader

DIST_DIR = "dist"


def build_project(project_root):
    os.chdir(project_root)
    create_dist_dir(DIST_DIR)
    copy_and_minimize_static_files()
    render()


def create_dist_dir(dir_name):
    """
    Create dist dir.
    It it exists, it gets deleted and a new dir is
    created.
    """
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.mkdir(dir_name)

def copy_and_minimize_static_files():
    copy_static_files()
    minimize_static_files()

def copy_static_files():
    shutil.copytree('styles', 'dist/styles')
    shutil.copytree('scripts', 'dist/scripts')

def minimize_static_files():
    pass

def render():
    render_index_html()
    render_blogs()


def render_index_html():
    env = Environment(loader=FileSystemLoader([".", "templates"]), autoescape=select_autoescape)
    index_html = env.get_template("index.html")

    with open("meta.json") as metafile:
        meta = json.load(metafile)

    rendered_index_html = index_html.render(
        **meta
    )

    OUTPUT_FILE = os.path.join(DIST_DIR, "index.html")
    with open(OUTPUT_FILE, "w") as out:
        out.write(rendered_index_html)


def render_blogs():
    BLOGS_DIR = "blogs"
    for root, dirs, files in os.walk(BLOGS_DIR):
        for file in files:
            filepath = os.path.join(root, file)
            out_file_dir = os.path.join(DIST_DIR, BLOGS_DIR, filepath.split(os.sep)[1])
            os.makedirs(out_file_dir)
            with open(filepath) as input_md:
                with open(
                    os.path.join(out_file_dir, file.split('.')[0] + '.html'),
                    "w",
                ) as output:
                    output.write(md.markdown(input_md.read()))
