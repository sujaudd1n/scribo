import os

import markdown as md
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from markdown.extensions.toc import TocExtension

from .helper import *

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
    complete_markdown_render(
        os.path.join(".", "index.md"), os.path.join(DIST_DIR, "index.html")
    )
    render_pages()
    render_sitemap()


def complete_markdown_render(
    markdown_path,
    output_html_path,
    template_name="index.html.jinja",
):
    print(42, markdown_path)
    html, page_toc, page_metadata = render_markdown(markdown_path)

    root_dir = "/".join(markdown_path.split(os.sep)[:-1])
    if root_dir == ".":
        root_dir = "pages"

    project_metadata = get_project_metadata()

    p_title = page_metadata.get("title", "")
    if p_title is not None and p_title != "":
        p_title = p_title[-1] + " - "

    p_description = page_metadata.get("description")
    if p_description is not None and p_description != "":
        p_description = p_description[-1]
    else:
        p_description = project_metadata["description"]

    page_metadata["title"] = p_title
    page_metadata["description"] = p_description

    data = {
        **project_metadata,
        "pages": get_toc("pages", 1),
        "page_metadata": page_metadata,
        "page_toc": page_toc,
        "html": html,
    }
    render_template_and_save(
        "index.html.jinja", data, os.path.join(TEMPLATES_DIR, "index.html.tmp")
    )

    data = {"contents": get_toc(root_dir, 1)}
    render_template_and_save("index.html.tmp", data, output_html_path)

    os.remove(os.path.join(TEMPLATES_DIR, "index.html.tmp"))


def render_template_and_save(
    template_name,
    data,
    output_path,
):
    rendered_template = get_rendered_template(template_name, data)
    save_html(output_path, rendered_template)


def render_pages():
    PAGES_DIR = "pages"
    ALL_PAGES = [
        page
        for page in os.listdir(PAGES_DIR)
        if os.path.isdir(os.path.join(PAGES_DIR, page))
    ]
    for page in ALL_PAGES:
        print(page)
        render_page(os.path.join("pages", page))


def render_page(directory):
    for root, dirs, files in os.walk(directory):
        dist_root = "/".join(root.split(os.sep)[1:])
        for file in files:
            filepath = os.path.join(root, file)
            os.makedirs(os.path.join(DIST_DIR, dist_root), exist_ok=True)
            outputpath = os.path.join(DIST_DIR, dist_root, file.replace("md", "html"))

            if not filepath.endswith(".md"):
                continue
            complete_markdown_render(filepath, outputpath)


def render_sitemap():
    path = "dist/sitemap"
    os.makedirs(path, exist_ok=True)
    render_template_and_save(
        "sitemap.html.jinja",
        {
            **get_project_metadata(),
            "pages": get_toc("pages", 1),
            "contents": get_toc("pages"),
        },
        path + "/index.html",
    )


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
        markdown_converter.Meta = {}
        return html, toc, meta


def get_rendered_template(template_name, data):
    template = jinja_environment.get_template(template_name)
    return template.render(**data)
