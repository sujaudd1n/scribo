"""
Various helper functions.
"""

import copy
import json
import os
import re
import urllib.parse
from collections import deque

from jinja2 import Environment, FileSystemLoader, select_autoescape

DIST_DIR = "dist"
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "html_templates")

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


from pathlib import Path


def modify_path(path: str) -> str:
    """
    Remove "pages" from the path of a node and its children.

    Args:
        path (str): The input path as a string.

    Returns:
        str: The modified path with "pages" removed and URL-encoded.
    """
    # Convert the input path to a Path object
    path_obj = Path(path)

    # Remove the first part of the path (e.g., "pages")
    page_removed_path = (
        path_obj.relative_to("pages") if "pages" in path_obj.parts else path_obj
    )

    # Convert the Path object back to a string and URL-encode it
    encoded_url = urllib.parse.quote(str(page_removed_path))

    return encoded_url


def sort_toc(children):
    """sort node based on "order"."""
    return sorted(children, key=lambda x: x["order"])


def capitalize_name(name):
    name = str(name)
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


def save(filepath, text):
    """Save rendered_template in output_path"""
    with open(filepath, "w") as output:
        output.write(text)


def get_rendered_template(template_name, data):
    """Render template_name with data and returns it"""
    template = jinja_environment.get_template(template_name)
    return template.render(**data)


def colorize(text, color):
    """
    Print text with a specified color.

    Args:
        text (str): The text to be printed.
        color (str): The color to apply to the text. Valid options are "red" and "green".

    Returns:
        str: The text wrapped in the appropriate ANSI color codes.

    Raises:
        ValueError: If an invalid color is provided.
    """
    color = color.lower()

    color_codes = {
        "red": "\x1b[31m",
        "green": "\x1b[32m",
    }

    if color not in color_codes:
        raise ValueError(
            f"Invalid color '{color}'. Valid options are: {', '.join(color_codes.keys())}"
        )

    return f"{color_codes[color]}{text}\x1b[0m"
