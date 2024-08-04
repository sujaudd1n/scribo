import shutil
import os
import json
import re

from .helper import get_metadata, get_toc

import markdown as md
import minify_html as minify
from jinja2 import Environment, select_autoescape, FileSystemLoader, BaseLoader
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.toc import TocExtension
from markdown.extensions.extra import ExtraExtension


DIST_DIR = "dist"
TEMPLATES_DIR = "assets/templates"


markdown_extensions = [
    ExtraExtension(),
    CodeHiliteExtension(linenums=True),
    TocExtension(),
    "admonition",
    "meta",
]
markdown_converter = md.Markdown(extensions=markdown_extensions)

jinja_environment = Environment(
    loader=FileSystemLoader([".", TEMPLATES_DIR, "dist"]), autoescape=select_autoescape
)


def render():
    render_index_page()
    render_pages()


def render_index_page():
    index_template = jinja_environment.get_template("index.html.jinja")
    index_markdown_filename = "index.md"
    with open(index_markdown_filename) as index_markdown_file:
        index_html = markdown_converter.convert(index_markdown_file.read())
    rendered_index_template = index_template.render(pages=get_toc('pages', 1), **get_metadata(), html=index_html)

    output_filename = os.path.join(DIST_DIR, "index.html")
    with open(output_filename, "w") as output_file:
        output_file.write(rendered_index_template)

    index_template = jinja_environment.get_template("index.html")
    rendered_index_template = index_template.render(contents=get_toc('pages', 1))

    output_filename = os.path.join(DIST_DIR, "index.html")
    with open(output_filename, "w") as output_file:
        output_file.write(rendered_index_template)


def render_pages():
    PAGES_DIR = "pages"
    ALL_PAGES = [
        page for page in os.listdir(PAGES_DIR)
        if os.path.isdir(
            os.path.join(PAGES_DIR, page)
        )
    ]
    for page in ALL_PAGES:
        render_page(os.path.join("pages", page))

def render_page(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            if not filepath.endswith(".md"):
                continue
            with open(filepath) as f:
                html = markdown_converter.convert(f.read())

            out_file_dir = os.path.join(
                DIST_DIR, directory, *filepath.split(os.sep)[2:-1]
            )
            os.makedirs(out_file_dir, exist_ok=True)

            base_template = jinja_environment.get_template("article.html.jinja")
            rendered_blog = base_template.render(
                pages=get_toc('pages', 1),
                **get_metadata(), html=html, toc=markdown_converter.toc
            )

            output_filename = os.path.join(out_file_dir, file.split(".")[0] + ".html")
            with open(output_filename, "w") as f:
                f.write(rendered_blog)
