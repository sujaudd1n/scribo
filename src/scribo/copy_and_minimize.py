import os
import shutil

DIST_DIR = "dist"


def copy_and_minimize_static_files():
    static_dirs = ["assets"]
    copy_static_dirs(static_dirs, DIST_DIR)
    # minimize_static_files()


def copy_static_dirs(static_dirs, dist_dir):
    """Copies all dirs in STATIC_DIRS into dist dir"""
    for static_dir in static_dirs:
        shutil.copytree(static_dir, os.path.join(dist_dir, static_dir))


def minimize_static_files():
    DIRS = ["dist/styles", "dist/scripts"]

    for diren in DIRS:
        print(diren)
        for file in os.listdir(diren):
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
