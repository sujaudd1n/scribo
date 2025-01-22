from scribo.helper import (
    get_filtered_toc,
    get_order,
    get_toc,
    modify_path,
    sort_toc,
    capitalize_name,
    print_with_color,
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


def test_modify_path():
    path = "pages/hello/world/foo bar"
    modified_node = modify_path(path)
    assert modified_node == "hello/world/foo%20bar"


def test_sort_toc():
    children = [
        {"path": "pages/hello", "order": 2, "children": []},
        {"path": "pages/world", "order": 1, "children": []},
    ]
    m_children = [
        {"path": "pages/world", "order": 1, "children": []},
        {"path": "pages/hello", "order": 2, "children": []},
    ]

    modified_node = sort_toc(children)
    assert modified_node == m_children


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


def test_capitalize_name():
    name = "Getting started With scribo"
    capitalized_name = capitalize_name(name)
    assert capitalized_name == "Getting Started With Scribo"


def test_get_order():
    order = get_order("./markdown/order.md")
    assert order == 33
    order = get_order("./markdown/no-order.md")
    assert order == 2**32 - 1


def test_print_with_color():
    text = "example text"

    red_text = print_with_color(text, "Red")
    assert red_text == f"\x1b[31m{text}\x1b[0m"

    red_text = print_with_color(text, "red")
    assert red_text == f"\x1b[31m{text}\x1b[0m"

    green_text = print_with_color(text, "green")
    assert green_text == f"\x1b[32m{text}\x1b[0m"
