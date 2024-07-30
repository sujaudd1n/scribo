import os
import shutil

DIST_DIR = "dist"

def copy_and_minimize_static_files():
    copy_static_dirs()
    # minimize_static_files()


def copy_static_dirs():
    STATIC_DIRS = ["assets"]
    for static_dir in STATIC_DIRS:
        shutil.copytree(static_dir, os.path.join(DIST_DIR, static_dir))


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


