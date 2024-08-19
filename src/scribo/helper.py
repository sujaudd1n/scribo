import json
import os
import re


def get_project_metadata():

    with open("meta.json") as metafile:
        return json.load(metafile)


def get_toc(directory, depth=None):
    result = []

    root = {"name": directory, "path": directory, "order": -1, "children": []}
    q = [root]

    current_depth = 0

    while q:
        if depth != None and current_depth >= depth:
            break
        print(depth, current_depth)

        for _ in range(len(q)):
            parent = q.pop(0)
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

        current_depth += 1

    # print(json.dumps(root, indent=4))

    # return root
    remove_path(root)
    sort_toc(root)
    return root

def remove_path(root):
    root['path'] = '/'.join(root['path'].split(os.sep)[1:])
    for child in root['children']:
        remove_path(child)


def sort_toc(toc):
    # print(json.dumps(toc, indent=4))
    toc["children"].sort(key=lambda x: x["order"])
    for child in toc["children"]:
        sort_toc(child)


def get_order(path):
    """
    Return order found in index.md
    if not found return 999
    """
    with open(os.path.join(path, "index.md")) as markdown_file:
        file_string = markdown_file.read()
        matches = re.search(r"order:\s+(\d)", file_string, re.IGNORECASE)
        if matches:
            order = matches.groups()[0]
            return int(order)
        else:
            return 999
