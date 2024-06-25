import shutil
import os
import markdown as md

def build_project(project_name):
    os.chdir(project_name)
    copy_raw_project_dir(project_name)
    render_markdown()
    os.chdir('..')

def copy_raw_project_dir(project_name):
    """
    Copies project's content into dist
    """
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    shutil.copytree('.', 'dist')


def render_markdown():
    for root, dirs, files in os.walk('dist/md'):
        for file in files:
            filename = os.path.join(root, file)
            with open(filename) as input_md:
                with open(filename.split('.')[0] + '.html', "w") as output:
                    output.write(md.markdown(input_md.read()))
            os.remove(filename)



