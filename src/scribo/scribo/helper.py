import os
import json


def get_metadata():
    with open("meta.json") as metafile:
        return json.load(metafile)


def get_toc(directory):
    result = []

    root = {"name": directory, "path": directory, "order": -1, "children": []}
    q = [root]

    while q:
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

    # print(json.dumps(root, indent=4))

    # return root
    sort_toc(root)
    return root


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
    try:
        with open(os.path.join(path, "index.md")) as markdown_file:
            file_string = markdown_file.read()
            matches = re.search(r"order:\s+(\d)\n", file_string, re.IGNORECASE)
            if matches:
                order = matches.groups()[0]
                return int(order)
    except:
        return 999
