# /// script
# dependencies = [
#     "marimo>=0.25.1",
#     "matplotlib==3.11.2",
#     "numpy==2.5.3",
#     "pandas==3.0.6",
#     "schemdraw==0.23",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(
    app_title="Part 1: Mathematical Foundations",
    css_file="notebook-styles.css",
)


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "From Primitives to Probabilities"
    abbreviations:
      iff: if and only if
      diff: null
      ZFC: Zermelo-Frankel set theory with Axiom of Choice
    numbering:
      equations: false
    -->
    """)
    return


@app.cell
def imports():
    # jb: include=false
    import marimo as mo
    from textwrap import dedent
    import schemdraw
    from schemdraw import flow

    return dedent, mo, schemdraw


@app.cell
def display_format(dedent, mo, schemdraw):
    # jb: include=false
    schemdraw.use("svg")

    def graphic(x):
        return mo.Html(
            dedent(f'''\
            <div class="graphic">
                {mo.as_html(x)}
            </div>
            ''')
        )

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Our goal when designing a signal filter is to algorithmically remove noise from a measurement signal. This is usually done by combining our knowlege and measurements in a way that increases the probability that the noise cancels out. In terms of the equations from the introduction:

    $$\hat{x}_k = \hat x_k^- + \alpha (z_k - \hat x_k^-).$$

    Here we lay the groundwork for answering the question:

    >"Given some amounts of noise in our prior ($\hat x_k^-$) and measurement ($z_k$), what value of $\alpha$ should we pick?"

    Since modeling noise relies on probabilities, probabilities are built on set theory, and set theory is built on logic, we will briefly introduce these topics along the way.
    """)
    return


if __name__ == "__main__":
    app.run()
