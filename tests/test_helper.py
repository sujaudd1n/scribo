from scribo.helper import (
    get_filtered_toc,
    get_order,
    get_toc,
    remove_path,
    sort_toc,
    capitalize_toc,
)

node = {
    "path": "pages",
    "order": -1,
    "children": [
        {"path": "pages/hello", "order": 2, "children": []},
        {"path": "pages/world", "order": 1, "children": []},
    ],
}


def test_get_toc():
    root = get_toc("markdown")
    expected = {
        "name": "markdown",
        "path": "markdown",
        "order": -1,
        "children": [
            {
                "name": "child",
                "path": "markdown/child",
                "order": 2**32 - 1,
                "children": [],
            }
        ],
    }
    assert root == expected


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
        "path": "pages",
        "order": -1,
        "children": [
            {"path": "pages/world", "order": 1, "children": []},
            {"path": "pages/hello", "order": 2, "children": []},
        ],
    }
    modified_node = sort_toc(node)
    assert modified_node == node_after


def test_get_filtered_toc():
    expected = {
        "name": "Markdown",
        "path": "",
        "order": -1,
        "children": [
            {
                "name": "Child",
                "path": "child",
                "order": 2**32 - 1,
                "children": [],
            }
        ],
    }
    filtered_toc = get_filtered_toc("markdown")
    assert expected == filtered_toc


def test_capitalize_toc():
    expected = {
        "name": "Markdown",
        "path": "",
        "order": -1,
        "children": [
            {
                "name": "Child",
                "path": "child",
                "order": 2**32 - 1,
                "children": [],
            }
        ],
    }
    filtered_toc = get_filtered_toc("markdown")
    assert expected == filtered_toc


def test_get_order():
    order = get_order("./markdown/order.md")
    assert order == 33
    order = get_order("./markdown/no-order.md")
    assert order == 2**32 - 1
