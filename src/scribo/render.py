"""
Module to convert markdown into HTML.
"""

import os
from pathlib import Path
from typing import Dict, Any

from scribo.helper import *
from scribo.markdown_utils import markdown_to_html_with_metadata

DIST_DIR = "dist"
CONTENT_DIR = "pages"
TEMPLATES_DIR = Path(__file__).parent / "html_templates"

project_metadata = get_project_metadata()


def render() -> None:
    """Run all steps for rendering HTML from markdown."""
    render_pages(Path(CONTENT_DIR))
    render_sitemap()

def render_pages(PAGES_DIR) -> None:
    """Render all markdown files in the CONTENT_DIR directory."""
    for page in PAGES_DIR.iterdir():
        if not page.is_dir():
            render_page(page)
        else:
            render_pages(page)


def render_page(filepath: Path) -> None:
    """Render all markdown files in a given directory."""
    dist_path = Path(DIST_DIR) / filepath.relative_to("pages").with_suffix(".html")
    dist_path.parent.mkdir(parents=True, exist_ok=True)
    complete_markdown_render(filepath, dist_path)

def complete_markdown_render(
    markdown_path: Path,
    output_html_path: Path,
    template_name: str = "index.html.jinja",
) -> None:
    """Render markdown to HTML and save it in the proper directory in DIST_DIR."""
    html, page_toc, page_metadata = markdown_to_html_with_metadata(markdown_path)


    page_metadata = update_page_metadata(page_metadata)
    root_dir = markdown_path.parent if markdown_path.parent != '.' else Path(CONTENT_DIR)

    data = {
        **project_metadata,
        "page_metadata": page_metadata,
        "page_toc": page_toc,
        "html": html,
        "contents": get_filtered_toc(root_dir, depth=2),
        # "pages": get_filtered_toc("pages", depth=1),
    }
    render_template_and_save(template_name, data, TEMPLATES_DIR / "index.html.tmp")
    data = {**project_metadata, "contents": get_filtered_toc(root_dir, depth=1)}
    render_template_and_save("index.html.tmp", data, output_html_path)

    (TEMPLATES_DIR / "index.html.tmp").unlink()


def update_page_metadata(page_metadata):
    page_title = page_metadata.get("title", "")
    if page_title:
        page_title = f"{page_title[-1]} - "

    page_description = page_metadata.get("description", project_metadata["description"])
    page_metadata.update({"title": page_title, "description": page_description})
    return page_metadata


def render_template_and_save(
    template_name: str,
    data: Dict[str, Any],
    output_path: Path,
) -> None:
    """Render a template with data and save the resulting HTML to the output path."""
    rendered_template = get_rendered_template(template_name, data)
    save(output_path, rendered_template)


def render_sitemap() -> None:
    """Render the sitemap HTML file."""
    sitemap_path = Path(DIST_DIR) / "sitemap"
    sitemap_path.mkdir(exist_ok=True)
    render_template_and_save(
        "sitemap.html.jinja",
        {
            **project_metadata,
            "pages": get_filtered_toc("pages", depth=1),
            "contents": get_filtered_toc("pages"),
        },
        sitemap_path / "index.html",
    )
