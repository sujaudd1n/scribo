from scribo.helper import remove_path, get_order, sort_toc

node = {
    "path": "pages/",
    "order": -1,
    "children": [
        {"path": "pages/hello", "order": 2, "children": []},
        {"path": "pages/world", "order": 1, "children": []},
    ],
}


def test_remove_path():
    node_after = {
        "path": "",
        "order": -1,
        "children": [
            {"path": "hello", "order": 2, "children": []},
            {"path": "world", "order": 1, "children": []},
        ],
    }
    modified_node = remove_path(node)
    assert modified_node == node_after


def test_sort_toc():
    node_after = {
        "path": "pages/",
        "order": -1,
        "children": [
            {"path": "pages/world", "order": 1, "children": []},
            {"path": "pages/hello", "order": 2, "children": []},
        ],
    }
    modified_node = sort_toc(node)
    assert modified_node == node_after


def test_get_order():
    order = get_order("./markdown/order.md")
    assert order == 33
    order = get_order("./markdown/no-order.md")
    assert order == 2**32 - 1
