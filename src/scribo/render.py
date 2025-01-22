"""
Module to convert markdown into HTML
"""

import os

from .helper import *

DIST_DIR = "dist"
TEMPLATES_DIR = "assets/templates"

project_metadata = get_project_metadata()


def render():
    """Run all steps for rendering html from markdown"""
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
    """Render markdown to html in proper directory in DIST_DIR"""
    html, page_toc, page_metadata = render_markdown(markdown_path)

    root_dir = "/".join(markdown_path.split(os.sep)[:-1])
    if root_dir == ".":
        root_dir = "pages"

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
        "pages": get_filtered_toc("pages", 1),
        "page_metadata": page_metadata,
        "page_toc": page_toc,
        "html": html,
        "contents": get_filtered_toc(root_dir, 2),
    }
    render_template_and_save(
        "index.html.jinja", data, os.path.join(TEMPLATES_DIR, "index.html.tmp")
    )

    data = {**project_metadata, "contents": get_filtered_toc(root_dir, 1)}
    render_template_and_save("index.html.tmp", data, output_html_path)

    os.remove(os.path.join(TEMPLATES_DIR, "index.html.tmp"))


def render_template_and_save(
    template_name,
    data,
    output_path,
):
    """Render template_name with data and save html in output_path"""
    rendered_template = get_rendered_template(template_name, data)
    save_html(output_path, rendered_template)


def render_pages():
    """Render all markdown in pages dir"""
    PAGES_DIR = "pages"
    ALL_PAGES = [
        page
        for page in os.listdir(PAGES_DIR)
        if os.path.isdir(os.path.join(PAGES_DIR, page))
    ]
    for page in ALL_PAGES:
        render_page(os.path.join("pages", page))


def render_page(directory):
    """Helper function of render_pages"""
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
            **project_metadata,
            "pages": get_filtered_toc("pages", 1),
            "contents": get_filtered_toc("pages"),
        },
        path + "/index.html",
    )
