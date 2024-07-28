import shutil
import os
import json
import re
import markdown as md
import minify_html as minify
from jinja2 import Environment, select_autoescape, FileSystemLoader

from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.toc import TocExtension
from markdown.extensions.extra import ExtraExtension

md_extensions = [
    # FencedCodeExtension(lang_prefix="lang"),
    ExtraExtension(),
    CodeHiliteExtension(
        linenums=True,
    ),
    TocExtension(),
    "admonition",
    "meta"
]

DIST_DIR = "dist"


def build_project(project_root):
    os.chdir(project_root)
    create_dist_dir(DIST_DIR)
    copy_and_minimize_static_files()
    render()


def create_dist_dir(dir_name):
    """
    Create dist dir.
    If it exists, it gets deleted and a new dir is
    created.
    """
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.mkdir(dir_name)


def copy_and_minimize_static_files():
    copy_static_dirs()
    # minimize_static_files()


def copy_static_dirs():
    STATIC_DIRS = [
        "styles",
        "scripts",
        "fonts",
        "static"
    ]
    for static_dir in STATIC_DIRS:
        shutil.copytree(static_dir, os.path.join(DIST_DIR, static_dir))


def minimize_static_files():
    DIRS = ["dist/styles", "dist/scripts"]

    for diren in DIRS:
        print(diren)
        for file in os.listdir(diren):
            with open(os.path.join(diren, file), "r+") as source:
                source_text = source.read()
                source.seek(0)
                source.write(
                    minify.minify(
                        source_text,
                        minify_js=True,
                        minify_css=True,
                        remove_processing_instructions=True,
                    )
                )


def render():
    render_index_html()
    render_blogs()


TEMPLATES_DIR = "templates"
env = Environment(
    loader=FileSystemLoader([".", TEMPLATES_DIR]), autoescape=select_autoescape
)


def render_index_html():
    index_template = env.get_template("index.html")
    rendered_index_template = index_template.render(**get_metadata(), contents=get_toc())

    OUTPUT_FILE = os.path.join(DIST_DIR, "index.html")
    with open(OUTPUT_FILE, "w") as out:
        out.write(rendered_index_template)


def get_metadata():
    with open("meta.json") as metafile:
        return json.load(metafile)


def get_toc():
    BLOGS_DIR = "blogs"
    result = []

    root = {"name": BLOGS_DIR, "path": BLOGS_DIR, "order": -1,  "children": []}
    q = [root]

    while q:
        parent = q.pop()
        for child in os.listdir(parent["path"]):
            child_path = os.path.join(parent["path"], child)
            if not os.path.isdir(child_path):
                continue

            child_node = {
                "name": child,
                "path": os.path.join(parent["path"], child),
                "order": get_order(child_path),
                "children": [],
            }

            parent["children"].append(child_node)
            q.append(child_node)
    
    # print(json.dumps(root, indent=4))

    # return root
    sort_toc(root)
    return root


def get_order(path):
    """
    Return order found in index.md
    if not found return 999
    """
    with open(os.path.join(path, "index.md")) as markdown_file:
        file_string = markdown_file.read()
        matches = re.search(r"order:\s+(\d)\n", file_string, re.IGNORECASE)
        if matches:
            order = matches.groups()[0]
            return int(order)
        return 999

def sort_toc(toc):
    # print(json.dumps(toc, indent=4))
    toc['children'].sort(key=lambda x: x['order'])
    for child in toc['children']:
        sort_toc(child)



def render_blogs():
    BLOGS_DIR = "blogs"

    for root, dirs, files in os.walk(BLOGS_DIR):
        for file in files:
            filepath = os.path.join(root, file)
            if not filepath.endswith(".md"):
                continue
            with open(filepath) as f:
                mdc = md.Markdown(extensions=md_extensions)
                html = mdc.convert(f.read())

            out_file_dir = os.path.join(
                DIST_DIR, BLOGS_DIR, *filepath.split(os.sep)[1:-1]
            )
            os.makedirs(out_file_dir, exist_ok=True)

            base_template = env.get_template("blog.html")
            rendered_blog = base_template.render(**get_metadata(), html=html, toc=mdc.toc)

            output_filename = os.path.join(out_file_dir, file.split(".")[0] + ".html")
            with open(output_filename, "w") as f:
                f.write(rendered_blog)
