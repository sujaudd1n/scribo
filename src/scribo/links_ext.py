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
        if filepath.is_file() and filepath.name.split(".")[-1].lower() in (
            "yml",
            "yaml",
        ):
            filename = filepath.name
            file = open(filepath)
            content = yaml.safe_load(file)
            file.close()

            target_dirname = filename.split(".")[0]
            target_dir = contents_dir / target_dirname
            if target_dir.exists():
                shutil.rmtree(target_dir)
            target_dir.mkdir()

            target_dir_index_file = target_dir / "index.md"
            with open(target_dir_index_file, "w") as f:
                f.write(build_dom(content))

            print(filename)


def render(json, tag_number, depth, idnt):
    container = HTMLElement("div")
    if not json:
        return container

    for key, value in json.items():
        if type(value) not in [str, int]:
            title = HTMLElement(
                f"h{tag_number}",
                children=[HTMLTextElement(key)],
                style={
                    "margin-bottom": "10px",
                    "margin-left": f"{idnt}px",
                    "margin-top": f"{(7 - tag_number) * 10}px",
                },
            )

            container.children.append(title)
            container.children.append(
                render(value, tag_number + 1, depth + 1, idnt + 15)
            )

        elif type(value) == str:
            a = HTMLAnchorElement(href=value, target="_blank", children=[HTMLTextElement(value)])
            p = HTMLParagraphElement(
                children=[a],
                style={
                    "margin-bottom": "5px",
                    "margin-left": f"{idnt}px",
                },
            )
            container.children.append(p)
    return container


def build_dom(content):
    root = HTMLElement("p", children=[
        HTMLAnchorElement(
            href="#",
            target="#",
            children=[HTMLTextElement("HI")]
        )
    ])
    root = render(content, 1, 1, 15)
    print(root.innerHTML)
    return root.innerHTML



class HTMLElement:
    def __init__(
        self, nodeName, children=None, style=None, classList=None, id=None, title=None
    ):
        self.nodeName = nodeName
        self.children = children if children is not None else []
        self.style = style if style is not None else {}

    def __str__(self):
        return self.nodeName

    @property
    def innerHTML(self):
        # childrensInnerHTML = [
            # child.innerHTML for child in self.children
        # ]

        childrensInnerHTML = []
        for child in self.children:
            childrensInnerHTML.append(child.innerHTML)

        mydom = f"""
<{self.nodeName}>
    {'\n'.join(childrensInnerHTML)}
</{self.nodeName}>
        """
        return mydom

class HTMLTextElement(HTMLElement):
    def __init__(self, textContent):
        self.textContent = textContent
    
    def __str__(self):
        return f"#text {self.textContent}"
    
    @property
    def innerHTML(self):
        return self.textContent

class HTMLAnchorElement(HTMLElement):
    def __init__(self, href, target, children, style={}):
        self.nodeName = "a"
        super().__init__(self.nodeName, children, style)
    


class HTMLParagraphElement(HTMLElement):
    def __init__(self, children, style={}):
        self.nodeName = "p"
        super().__init__(self.nodeName, children, style)