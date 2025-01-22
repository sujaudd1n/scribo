"""
Module to minify code.
"""

import os
import shutil

DIST_DIR = "dist"


def copy_and_minimize_static_files():
    static_parent = ["assets"]
    static_dirs = ["dist/assets/styles", "dist/assets/scripts"]
    copy_static_dirs(static_parent, DIST_DIR)
    # minimize_static_files(static_dirs)


def copy_static_dirs(static_dirs, dist_dir):
    """Copies all dirs in STATIC_DIRS into dist dir"""
    for static_dir in static_dirs:
        shutil.copytree(static_dir, os.path.join(dist_dir, static_dir))


def minimize_static_files(static_dirs):
    """
    Minimized all files that starts with css or js in
    all static_dirs
    """
    for diren in static_dirs:
        for file in os.listdir(diren):
            if not file.endswith(".css") or not file.endswith(".js"):
                continue
            with open(os.path.join(diren, file), "r+") as source:
                source_text = source.read()
                source.seek(0)
                source.write(
                    minify.minify(
                        source_text,
                        minify_js=True,
                        minify_css=True,
                        remove_processing_instructions=True,
                    )
                )
