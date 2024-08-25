# Code

Code highlighting in enabled by default.

``` { .python }
def get_toc():
    BLOGS_DIR = "blogs"
    result = []

    root = {"name": BLOGS_DIR, "path": BLOGS_DIR, "children": []}
    q = [root]
    while q:
        parent = q.pop()
        for child in [
            subdir
            for subdir in os.listdir(parent["path"])
            if os.path.isdir(os.path.join(parent["path"], subdir))
        ]:
            child_node = {
                "name": child,
                "path": os.path.join(parent["path"], child),
                "children": [],
            }
            parent["children"].append(child_node)
            q.append(child_node)

    print(json.dumps(root, indent=4))

    return root

```