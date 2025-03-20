import yaml
import os
import shutil
import json
from string import Template
from pathlib import Path

from scribo.config import LINKS_DIR_NAME, CONTENTS_DIR_NAME
from .dom import *

def create_links_dir(root):
    links_dir = Path(f"{root}/{LINKS_DIR_NAME}")
    contents_dir = Path(f"{root}/{CONTENTS_DIR_NAME}")

    for filepath in links_dir.iterdir():
        if filepath.is_file() and filepath.name.split(".")[-1].lower() in (
            "yml",
            "yaml",
        ):
            with open(filepath) as file:
                content = yaml.safe_load(file)

            filename = filepath.name
            target_dirname = filename.split(".")[0]
            target_dir = contents_dir / target_dirname
            if target_dir.exists():
                shutil.rmtree(target_dir)
            target_dir.mkdir()

            target_dir_index_file = target_dir / "index.md"
            with open(target_dir_index_file, "w") as f:
                dom_tree = build_dom(content, 2, 1, 15)
                f.write(dom_tree.innerHTML)
            print(f"Links page for {filename} created.")


def build_dom(json, tag_number, depth, idnt):
    if not json:
        return HTMLTextElement("")

    container = HTMLElement("div")

    for key, value in json.items():
        link_container = HTMLElement("div")

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

            link_container.children.append(title)
            link_container.children.append(
                build_dom(value, tag_number + 1, depth + 1, idnt + 15)
            )
        elif type(value) == str:
            a = HTMLAnchorElement(href=value, target="_blank", children=[HTMLTextElement(str(key))])
            p = HTMLParagraphElement(
                children=[a],
                style={
                    "margin-bottom": "5px",
                    "margin-left": f"{idnt}px",
                },
            )
            link_container.children.append(p)
        container.children.append(link_container)
    return container