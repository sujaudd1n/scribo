import json
import os
import re
from collections import deque


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

    remove_path(root)  # remove prefix "pages"
    sort_toc(root)  # sort based on order

    return root


def remove_path(root):
    """Remove "pages" from path of node and its children in place"""
    root["path"] = "/".join(root["path"].split(os.sep)[1:])
    for child in root["children"]:
        remove_path(child)


def sort_toc(toc):
    """sort node based on "order"."""
    # print(json.dumps(toc, indent=4))
    toc["children"].sort(key=lambda x: x["order"])
    for child in toc["children"]:
        sort_toc(child)


def get_order(filepath):
    """
    Return order found in index.md. if not found return 999.
    """
    with open(filepath) as markdown_file:
        file_string = markdown_file.read()
        matches = re.search(r"order:\s+(\d+)", file_string, re.IGNORECASE)
        if matches:
            order = matches.groups()[0]
            return int(order)
        else:
            return 999
