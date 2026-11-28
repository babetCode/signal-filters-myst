# To Do

This file contains ideas of things to do with this project. This includes edits, revisions, formatting changes, etc.... Not all ideas here are well formulated yet, some are more of a brainstorm of thing that may improve the quality of the project (or may not).

## Chapter Notes

Notes I've taken while reading through the chapter and finding places that potentially could be improved. I'm still working through them and have not proof-read all the chapters yet.

### Introduction

### Chapter 1

### Chapter 2

### Chapter 3

### Chapter 4

## Tooling

### marimo: inconsistent escaping of `"""` in markdown cells

Inspect this bug and decide whether it's worth reporting to marimo, or whether a newer version has already fixed it (found in marimo 0.25.1).

- The marimo editor saves `"""` typed inside a markdown cell as `"\"\"` in the `.py` file.
- `marimo check` compares markdown cells with `format_markdown` in `marimo/_ast/codegen.py`, which replaces every `""` with `"\"` and so expects `"\""`. As a result, every fenced code copy containing a docstring gets `warning[markdown-indentation]` (MF007), and `marimo check --fix` rewrites `"\"\"` to `"\""`.
- In an `r"""` string, the same replacement is wrong: `"\""` keeps its backslash and shows on the page.
- The workaround is documented in STYLEGUIDE §3 (format of a fenced copy) and §11 (MF007 exception). If marimo fixes this, remove the §11 exception.
