import yaml
import os
import shutil
import json
from string import Template
from pathlib import Path

from scribo.config import LINKS_DIR_NAME, CONTENTS_DIR_NAME

def create_links_dir(root):
    links_dir = Path(f"{root}/{LINKS_DIR_NAME}")
    contents_dir = Path(f"{root}/{CONTENTS_DIR_NAME}")

    for filepath in links_dir.iterdir():
        if filepath.is_file() and filepath.name.split(".")[-1].lower() in ("yml", "yaml"):
            filename = filepath.name
            file = open(filepath)
            content = yaml.safe_load(file)
            file.close()

            target_dirname = filename.split(".")[0]
            target_dir = contents_dir / target_dirname
            if target_dir.exists():
                shutil.rmtree(target_dir)
            target_dir.mkdir()

            target_dir_index_file = target_dir / 'index.md'
            with open(target_dir_index_file, 'w') as f:
                f.write(build_dom(content))

            print(filename)

def gen_html(obj):
    con = {
        'name': 'div',
        'children': []
    }
    tag_number = 1
    depth = 0
    def render(json, tag_number, depth, idnt):
        if not json:
            return
        for key in json:
            if type(json[key]) not in [str, int]:
                item = json[key]
                title = {
                    'name': f"h{tag_number}",
                    'textContent': '',
                    'children': [],
                    'classList': [],
                    'style': {

                    }
                }
                title['style']['margin-bottom'] = "10px"
                title['style']['margin-left'] = f"{idnt}px"
                match tag_number:
                    case 1:
                        title['style']['margin-top'] = "60px"
                    case 2:
                        title['style']['margin-top'] = "50px"
                    case 3:
                        title['style']['margin-top'] = "40px"
                    case 4:
                        title['style']['margin-top'] = "30px"
                    case 5:
                        title['style']['margin-top'] = "20px"
                    case 6:
                        title['style']['margin-top'] = "10px"

                if depth == 0:
                    title['classList'].append("section-title")
                    title.textContent = key
                con['children'].append(title)

                render(item, tag_number + 1, depth + 1, idnt + 15);
            elif type(json[key]) == str:
                item = json[key]
                p = {
                    'name': 'p',
                    'style': {
                        'margin-bottom': '5px',
                        'margin-left': f"{idnt}px",
                    },
                    'children': []
                }
                a = {
                    'name': 'a',
                    'href': item,
                    'title': item,
                    'target': "_blank",
                    'textContent': item
                    }

                p['children'].append(a);
                con['children'].append(p);
    render(obj, 1, 1, 15)
    return con

def build_dom(content):
    root = gen_html(content)
    print(root)
    return r(root)
def r(root):
    element = single_dom(root)
    if not root.get("children"):
        return element
    children = []
    for child in root['children']:
        children.append(r(child))
    element = Template(element).substitute(children="\n".join(children))
    return element


def single_dom(element):
    element = f"""
<{element["name"]}>
  {element.get("textContent", '')}
  $children
</{element["name"]}>
    """
    return element

class Node:
    def __init__(self, nodeName, textContent):
        self.nodeName = nodeName
        self.textContent = textContent

class HTMLElement(Node):
    def __init__(self, nodeName, textContent, style, children=[], classList=[], id=None, title=None):
        super().__init__(nodeName, textContent)
        self.style = style # style will a dict

class HTMLAnchorElement(HTMLElement):
    def __init__(self, href, textContent, target, style):
        self.nodeName = 'a'
        super().__init__(self.nodeName, textContent, style)

