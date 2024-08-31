---
title: Getting Started
description: Getting started with Scribo
order: 1
---

# Getting Started

In this guide, you will learn how to install Scribo and build a
production ready site.

## Installation

Install with `pip`.

``` console
pip install scribo
```

## Quickstart

In this quickstart, we'll build a small site for a **Python** course
which will have pages like *assignments*, *resources* and
more.

### Initialize

Assume, the code of the course is **py101**. Now, let's initialize the
project.

```console
scribo --init py101
```

A directory structure of the following will be created.

```console
py101/
├── assets
├── index.md
├── meta.json
└── pages
```

- **assets** dir is for static files such as styles, scripts, templates
etc.
- **index.md** is the root for the project.
- **meta.json** is for config and metadate information.
- **pages** directory is for file-system based routing. 

## Configure

Let's change the meta.json file. After the change file file looks like
this.

```json
{
    "title": "PY101",
    "project_name": "Python Course 101",
    "description": "Learn Python",
    "author": "Teacher",
    "production_urls": [
        "http://localhost:8000",
        "http://localhost:8001"
    ],
    "base_url": "/",
    "quick_links": [
        {
            "name": "Home",
            "url": "/"
        },
        {
            "name": "Assignment",
            "url": "/assignment"
        },
        {
            "name": "Resources",
            "url": "/resources"
        }
    ],
    "_comment": "Docs for this meta file: <>"
}
```

## Write

Now, let's write content for site.

First, the index page. Edit the **index.md** at the root of the project,
with the following LLM generated content [index.md](#).

Now, let's write the assignment, resources page.

Inside `pages/` create two directory with index.md files.
index.md file is necessary. You may delete the other directories
if you don't need them.

- pages/assignment/index.md
- pages/resources/index.md

Now, same as before write content to the files using

- [assignment/index.md]()
- [resources/index.md]()


### Build

It's time to build the project.

```console
scribo --build py101 # if outside of project dir
scribo --build . # if inside for prject dir
```

A new directory will be created named **dist**.

You can deploy this to any static site hosting provider, you wish.

See live view of [py101](#).

## Next

Now that you know the basics, read the [docs](/docs) to learn more.