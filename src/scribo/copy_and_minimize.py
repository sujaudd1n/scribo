"""
Module to minify code.
"""

import os
import shutil

DIST_DIR = "dist"
STATIC_DIR = "assets"

def copy_and_minimize_static_files():
    """
    Copies static files from the source directory to the distribution directory.
    Optionally, static files can be minimized (commented out for now).
    """
    static_dirs = [STATIC_DIR]
    copy_static_dirs(static_dirs, DIST_DIR)
    # minimize_static_files(static_dirs)  # Uncomment to enable minimization

def copy_static_dirs(static_dirs, dist_dir):
    """
    Copies all directories in `static_dirs` into the `dist_dir`.

    Args:
        static_dirs (list): List of directories to copy.
        dist_dir (str): Destination directory where files will be copied.
    """
    for static_dir in static_dirs:
        source = os.path.join(os.path.dirname(__file__), static_dir)
        destination = os.path.join(dist_dir, static_dir)

        if os.path.exists(destination):
            shutil.rmtree(destination) 
        shutil.copytree(source, destination)

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
