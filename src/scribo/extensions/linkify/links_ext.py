import yaml
import os
import shutil
import json
from string import Template
from pathlib import Path
from .dom import *

from scribo.config import LINKS_DIR_NAME, CONTENTS_DIR_NAME, LINKS_OUTPUT_DIR_NAME


def create_links_dir(root):
    links_dir = Path(f"{LINKS_DIR_NAME}")
    linkify_output_dir = Path(f"{CONTENTS_DIR_NAME}/{LINKS_OUTPUT_DIR_NAME}")

    for filepath in links_dir.iterdir():
        if filepath.is_file() and filepath.name.split(".")[-1].lower() in (
            "yml",
            "yaml",
        ):
            with open(filepath) as file:
                content = yaml.safe_load(file)
            filename = filepath.name
            target_dirname = filename.split(".")[0]

            if target_dirname == "meta":
                print(json.dumps(content))
                with open(Path(CONTENTS_DIR_NAME) / "index.md", "w") as f:
                    s = []
                    for key, val in content.items():
                        s.append(f"{key}: {val}")
                    f.write('  \n'.join(s))
                continue

            target_dir = linkify_output_dir / target_dirname
            if target_dir.exists():
                shutil.rmtree(target_dir)
            target_dir.mkdir(parents=True)

            target_dir_index_file = target_dir / "index.md"
            with open(target_dir_index_file, "w") as f:
                # dom_tree = build_dom(content, 2, 1, 15)
                # f.write(dom_tree.innerHTML)
                f.write(build_markdown(content, 2))
            print(f"Links page for {filename} created.")
    with open(linkify_output_dir / "index.md", "w") as f:
        f.write("Links")


def build_markdown(json, tagno):
    if not json:
        return ""

    container = []

    for key, value in json.items():
        link_container = []

        if type(value) not in [str, int]:
            title = f"{'#' * tagno} {key}"
            link_container.append(title)
            link_container.append(build_markdown(value, min(tagno + 1, 6)))
        elif type(value) == str:
            a = f"[{key}]({value})  "
            a = f'<a href="{value}" target="_blank">{key}</a>  '
            link_container.append(a)
        container.append("\n\n".join(link_container))
    return "\n".join(container)


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
            a = HTMLAnchorElement(
                href=value, target="_blank", children=[HTMLTextElement(str(key))]
            )
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
