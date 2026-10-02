# /// script
# dependencies = [
#     "marimo>=0.9.0",
#     "matplotlib==3.11.1",
#     "numpy==2.5.2",
#     "pandas==3.0.5",
#     "schemdraw[matplotlib,svgmath]==0.23",
# ]
# requires-python = ">=3.13"
# ///

import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Drafting
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    abbreviations:
      iff: if and only if
      diff: null
    numbering:
      equations: false
    -->
    """)
    return


@app.cell(hide_code=True)
def imports():
    # jb: include=false
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib
    import schemdraw
    from schemdraw import flow
    from textwrap import dedent
    import matplotlib.pyplot as plt

    return dedent, mo, plt


@app.cell(hide_code=True)
def display_format(dedent, mo, plt):
    # jb: include=false
    plt.style.use('default')
    def graphic(x):
        return mo.Html(
            dedent(f'''\
            <style>
                .dark .graphic {{ 
                    filter: invert(1) hue-rotate(180deg); 
                }}
            </style>
            <div class="graphic">
                {mo.as_html(x)}
            </div>
            ''')
        )

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    lorem ipsum dolor sit amet consectetuer adipiscing elit sed diam nonummy nib
    """)
    return


if __name__ == "__main__":
    app.run()
