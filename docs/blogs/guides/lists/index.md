# Lists

You can define the following kind of lists.

*[HTML]: HTML 

## Unordered List

- one
- two
- three
    - four
    - five
- six

NOTE: The marker of unordered list changes depending on nesting level.

### Syntax

``` { .md linenums=false }
- one
- two
- three
    - four
    - five
- six
```

## Ordered List

1. One
1. Two
    1. Three
    1. Four
1. Five

### Systax

``` { .md linenums=false }
1. One
1. Two
    1. Three
    1. Four
1. Five
```

NOTE: The numbers are all **1**, markdown will automatically figure out
the correct number. Later if you delete any list you don't have to
change all the numbers manually.

## Definition List

Rust
:    Rust is a memory safe programming language.

Python
:    Python is also memory safe but it's interpreted.

### Syntax 

``` {.md linenums=false }
Rust
:    Rust is a memory safe programming language.

Python
:    Python is also memory safe but it's interpreted.
```