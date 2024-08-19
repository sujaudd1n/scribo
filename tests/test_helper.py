from scribo.helper import remove_path


def test_remove_path():
    node = {
        "path": "pages/hello/world",
        "children": [{"path": "pages/world/hello", "children": []}],
    }
    after_node = {
        "path": "hello/world",
        "children": [{"path": "world/hello", "children": []}],
    }
    remove_path(node)
    assert node == after_node
