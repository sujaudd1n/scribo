---
order: 1
---
# Getting Started

## Installation

``` console
pip install <>
```

## Quickstart

### Initialize

```console
scribo --init <project_name>
```

A new directory with the project name will be created.  

Inside it, in the **blogs** directory, you will be writing your
blogs/articles.

Create a directory inside **blogs** and in it add a file named
**index.md**. The name of the directory inside blogs will be used
to access that blog.

For example:
If the directory structure looks like this `/blogs/a-guide-to-x/index.md`  
It will be accessed `you-site-name/blogs/a-guide-to-x/`

### Build

When you want to deploy the project simply execute the following 
command.

```console
scribo --build <project_name>
```

A new directory inside *project_name* will be created named **dist**.

You can deploy this to any static site hosting provider, you wish.