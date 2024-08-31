# Code

Code highlighting in enabled by default.

``` { .python }
def get_order(filepath):
    """
    Return order found in index.md. if not found return 2**32 - 1.
    """
    with open(filepath) as markdown_file:
        file_string = markdown_file.read()
        matches = re.findall(r"order:\s+(\d+)", file_string, re.IGNORECASE)
        if matches:
            order = matches[-1]
            return int(order)
        else:
            return 2**32 - 1 
```

Syntax:

&#96;&#96;&#96;python
<pre>
def get_order(filepath):
    """
    Return order found in index.md. if not found return 2**32 - 1.
    """
    with open(filepath) as markdown_file:
        file_string = markdown_file.read()
        matches = re.findall(r"order:\s+(\d+)", file_string, re.IGNORECASE)
        if matches:
            order = matches[-1]
            return int(order)
        else:
            return 2**32 - 1
</pre>
&#96;&#96;&#96;