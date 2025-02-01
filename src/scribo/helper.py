"""
Various helper functions.
"""

import copy
import json
import os
import re
import urllib.parse
from collections import deque

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from markdown.extensions.toc import TocExtension

DIST_DIR = "dist"
TEMPLATES_DIR = "assets/templates"

markdown_extensions = [
    ExtraExtension(),
    CodeHiliteExtension(linenums=True),
    TocExtension(),
    "admonition",
    "meta",
]
markdown_converter = markdown.Markdown(extensions=markdown_extensions)

jinja_environment = Environment(
    loader=FileSystemLoader([".", TEMPLATES_DIR, "dist"]), autoescape=select_autoescape
)


def get_project_metadata():
    """
    Get project metadata from file called 'meta.json' in root
    directory and returns as dict.
    """
    with open("meta.json") as metafile:
        return json.load(metafile)


def get_toc(directory, depth=None):
    """
    Generate graph of directories starting from `directory` up to
    `depth` depth for creating routes.
    """
    root = {"name": directory, "path": directory, "order": -1, "children": []}
    q = deque([root])
    current_depth = 0

    while q:
        if depth != None and current_depth >= depth:
            break
        for _ in range(len(q)):
            parent = q.popleft()
            for child in os.listdir(parent["path"]):
                child_path = os.path.join(parent["path"], child)
                if not os.path.isdir(child_path):
                    continue
                child_node = {
                    "name": child,
                    "path": child_path,
                    "order": get_order(os.path.join(child_path, "index.md")),
                    "children": [],
                }
                parent["children"].append(child_node)
                q.append(child_node)
        current_depth += 1

    return root


def get_filtered_toc(root, depth=None):
    toc = get_toc(root, depth)
    # path_removed_toc = remove_path(toc)
    # sorted_toc = sort_toc(path_removed_toc)
    # capitalized_toc = capitalize_toc(sorted_toc)
    filtered_toc = apply_filter(toc)
    return filtered_toc


def apply_filter(root):
    root = copy.deepcopy(root)

    root["path"] = modify_path(root["path"])
    root["children"] = sort_toc(root["children"])
    root["name"] = capitalize_name(root["name"])

    for idx in range(len(root["children"])):
        child = root["children"][idx]
        root["children"][idx] = apply_filter(child)
    return root


def modify_path(path):
    """Remove "pages" from path of node and its children"""
    page_removed_path = "/".join(path.split(os.sep)[1:])
    encoded_url = urllib.parse.quote(page_removed_path)
    return encoded_url


def sort_toc(children):
    """sort node based on "order"."""
    return sorted(children, key=lambda x: x["order"])


def capitalize_name(name):
    """Capitalize each word in name"""
    return " ".join(map(str.capitalize, name.split()))


def get_order(filepath):
    """
    Return order found in index.md. if not found return 2**32 - 1.
    """
    with open(filepath) as markdown_file:
        file_string = markdown_file.read()
        matches = re.findall(r"order:\s+(\d+)", file_string, re.IGNORECASE)
        if matches:
            order = matches[-1]
            return int(order)
        else:
            return 2**32 - 1


def save_html(output_path, rendered_template):
    """Save rendered_template in output_path"""
    with open(output_path, "w") as output_file:
        output_file.write(rendered_template)


def render_markdown(markdown_file_path):
    """Render markdown and returns html, toc, and meta"""
    with open(markdown_file_path) as markdown_file:
        html = markdown_converter.convert(markdown_file.read())
        toc = markdown_converter.toc
        meta = markdown_converter.Meta
        markdown_converter.Meta = {}
        return html, toc, meta


def get_rendered_template(template_name, data):
    """Render template_name with data and returns it"""
    template = jinja_environment.get_template(template_name)
    return template.render(**data)


def print_with_color(text, color):
    """Print text with a color.

    Valid colors are:
        * Red
        * Green
    """
    color = color.lower()

    match color:
        case "red":
            text = f"\x1b[31m{text}\x1b[0m"
        case "green":
            text = f"\x1b[32m{text}\x1b[0m"

    print(text)
    return text
