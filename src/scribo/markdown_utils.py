import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from markdown.extensions.toc import TocExtension

markdown_extensions = [
    ExtraExtension(),
    CodeHiliteExtension(linenums=True),
    TocExtension(),
    "admonition",
    "meta",
]
markdown_converter = markdown.Markdown(extensions=markdown_extensions)


def markdown_to_html_with_metadata(markdown_file_path):
    """Render markdown and returns html, toc, and meta"""
    with open(markdown_file_path) as markdown_file:
        html = markdown_converter.convert(markdown_file.read())
        toc = markdown_converter.toc
        meta = markdown_converter.Meta
        markdown_converter.Meta = {}
        return html, toc, meta
