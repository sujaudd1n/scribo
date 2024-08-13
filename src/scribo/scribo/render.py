import shutil
import os
import json
import re

from .helper import get_project_metadata, get_toc

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
    complete_markdown_render("index.md", "index.html")
    return
    render_pages()
    render_sitemap()


def complete_markdown_render(
    markdown_path,
    output_html_path,
    template_name="index.html.jinja",
    root_dir="pages",
):
    html, page_toc, page_metadata = render_markdown(markdown_path)

    data = {
        **get_project_metadata(),
        "pages": get_toc(root_dir, 1),
        "contents": get_toc(root_dir, 1),
        "page_metadata": page_metadata,
        "page_toc": page_toc,
        "html": html,
    }
    render_template_and_save(
        "index.html.jinja",
        data,
        os.path.join(TEMPLATES_DIR, "index.html.tmp")
    )

    data = {
        "contents": get_toc(root_dir)
        }
    render_template_and_save("index.html.tmp", data, DIST_DIR + "/index.html")

    os.remove(os.path.join(TEMPLATES_DIR, "index.html.tmp"))


def render_template_and_save(
    template_name,
    data,
    output_path,
):
    rendered_template = get_rendered_template(template_name, data)
    save_html(output_path, rendered_template)



def save_html(filepath, rendered_template):
    with open(filepath, "w") as output_file:
        output_file.write(rendered_template)


def second_html_render(template_name, root_dir):
    second_rendered_template = get_rendered_template(
        "index.html.tmp", {**get_project_metadata()}
    )

    save_html(os.path.join(DIST_DIR, "index.html"), second_rendered_template)


def render_markdown(markdown_file_path):
    with open(markdown_file_path) as markdown_file:
        html = markdown_converter.convert(markdown_file.read())
        toc = markdown_converter.toc
        meta = markdown_converter.Meta
        return html, toc, meta


def get_rendered_template(template_name, data):
    template = jinja_environment.get_template(template_name)
    return template.render(**data)


def render_pages():
    PAGES_DIR = "pages"
    ALL_PAGES = [
        page
        for page in os.listdir(PAGES_DIR)
        if os.path.isdir(os.path.join(PAGES_DIR, page))
    ]
    for page in ALL_PAGES:
        render_page(os.path.join("pages", page))


def render_page(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)

            if not filepath.endswith(".md"):
                continue

            html, toc, meta = render_markdown(filepath)

            out_file_dir = os.path.join(DIST_DIR, *filepath.split(os.sep)[:-1])
            os.makedirs(out_file_dir, exist_ok=True)

            tmp_page = get_rendered_template(
                "article.html.jinja",
                {
                    "pages": get_toc("pages", 1),
                    "html": html,
                    "toc": toc,
                    **get_project_metadata(),
                    **meta,
                },
            )
            tmp_path = "assets/templates/article.html.tmp"

            save_html(tmp_path, tmp_page)

            rendered_page = get_rendered_template(
                "article.html.tmp",
                {
                    "pages": get_toc("pages", 1),
                    "html": html,
                    "toc": toc,
                    **get_project_metadata(),
                },
            )

            output_filename = os.path.join(out_file_dir, file.split(".")[0] + ".html")

            save_html(output_filename, rendered_page)

            os.remove(tmp_path)


def render_sitemap():
    path = "dist/sitemap"
    os.makedirs(path, exist_ok=True)
    render_template_and_save("sitemap.html.jinja", {
        **get_project_metadata(),
        "pages": get_toc("pages", 1),
        "contents": get_toc("pages")
    },
    path + "/index.html"

    )
