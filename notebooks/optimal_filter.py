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

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Drafts
    """)
    return


@app.cell(hide_code=True)
def imports():
    # jb: include=false
    import marimo as mo
    import schemdraw
    from schemdraw import flow
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from textwrap import dedent

    return dedent, mo, np


@app.cell(hide_code=True)
def admonition(mo):
    # jb: include=false
    def admonition(
        value: str,
        title: str = "<b>Key Idea</b>",
        color: str = "GoldenRod",
        icon_str='<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="color-mix(in srgb, GoldenRod 70%, currentColor 30%)" d="M8.308 13.308q.538-.539.538-1.308t-.538-1.308T7 10.154t-1.308.538T5.154 12t.538 1.308T7 13.846t1.308-.538M7 16.73q-2 0-3.366-1.366Q2.27 14 2.27 12t1.366-3.366T7 7.27q1.698 0 2.941.958t1.593 2.273h9.049l1.494 1.494l-2.48 2.635l-1.828-1.379l-1.827 1.442l-1.557-1.192h-2.85q-.356 1.339-1.608 2.285T7 16.73"></path></svg>',
    ):
        # Parse LaTeX & Markdown first into a rendered Marimo HTML element
        content = mo.md(value) if isinstance(value, str) else value
        title_content = mo.md(title) if isinstance(title, str) and title else None

        title_html = ""
        if title_content:
            title_html = f"""
            <div style="
                display: flex;
                align-items: center;
                font-weight: bold;
                margin-bottom: 8px;
            ">
                <div style="
                    flex-shrink: 0;
                    margin-right: 8px;
                    font-size: 1.5em;
                    display: flex;
                ">
                    {icon_str}
                </div>
                <div style="color:color-mix(in srgb, {color} 70%, currentColor 30%)">{title_content.text}</div>
            </div>
            """

        # Build body HTML using content.text (already parsed by KaTeX)
        body_html = f"""
        <div style="display: flex; align-items: flex-start;">
            {f"" if title else f'<div style="flex-shrink: 0; margin-right: 12px; font-size: 1.5em; display: flex; padding-top: 2px;">{icon_str}</div>'}
            <div style="flex-grow: 1; overflow-wrap: anywhere;">
                {content.text}
            </div>
        </div>
        """

        return mo.Html(f"""
        <div style="
            display: flex;
            flex-direction: column;
            padding: 16px;
            margin: 16px 0;
            border-left: 4px solid {color};
            background-color: color-mix(in srgb, {color} 10%, transparent);
            border-radius: 0 6px 6px 0;
        ">
            {title_html}
            {body_html}
        </div>
        """)

    return (admonition,)


@app.cell(hide_code=True)
def _(admonition):
    # jb: include=false
    def key_idea(
        value: str,
        title="<b>Key Idea</b>",
        color="GoldenRod",
    ):
        icon_str = '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="color-mix(in srgb, GoldenRod 70%, currentColor 30%)" d="M8.308 13.308q.538-.539.538-1.308t-.538-1.308T7 10.154t-1.308.538T5.154 12t.538 1.308T7 13.846t1.308-.538M7 16.73q-2 0-3.366-1.366Q2.27 14 2.27 12t1.366-3.366T7 7.27q1.698 0 2.941.958t1.593 2.273h9.049l1.494 1.494l-2.48 2.635l-1.828-1.379l-1.827 1.442l-1.557-1.192h-2.85q-.356 1.339-1.608 2.285T7 16.73"></path></svg>'
        return admonition(value=value, title=title, color=color, icon_str=icon_str)

    return


@app.cell(hide_code=True)
def _(admonition):
    # jb: include=false
    def glossary_def(
        value: str,
        title="<b>Definition</b>",
        color="cornflowerblue",
    ):
        icon_str = '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="color-mix(in srgb, cornflowerblue 70%, currentColor 30%)" d="M4.385 14.09h.779l.555-1.534h2.87l.561 1.535h.792l-2.31-6.143h-.957zm1.62-2.267l1.124-3.06h.05l1.123 3.06zm7.88-2.23v-.931q.805-.408 1.725-.612t1.89-.204q.554 0 1.064.071q.509.072 1.052.202v.908q-.524-.167-1.02-.232q-.498-.064-1.096-.064q-.97 0-1.892.218q-.924.218-1.724.643m0 5.462v-.97q.768-.407 1.717-.611t1.899-.204q.554 0 1.064.072q.509.07 1.052.201v.908q-.524-.167-1.02-.232q-.498-.064-1.096-.064q-.97 0-1.892.235q-.924.234-1.724.665m0-2.712v-.969q.806-.408 1.726-.611t1.89-.204q.554 0 1.063.07q.51.072 1.052.203v.908q-.523-.168-1.02-.232q-.497-.065-1.095-.065q-.97 0-1.892.238q-.924.237-1.724.662M12.5 17.32q1.216-.678 2.453-.98t2.547-.3q.9 0 1.618.111t1.267.296q.23.096.423-.029t.192-.394V7.008q0-.173-.096-.308q-.096-.134-.327-.23q-.825-.293-1.501-.4T17.5 5.961q-1.31 0-2.613.386q-1.304.387-2.387 1.16zm-.5 1.45q-1.22-.834-2.62-1.282T6.5 17.04q-.78 0-1.534.13q-.753.131-1.466.42q-.544.217-1.022-.131T2 16.496V6.831q0-.371.195-.689t.547-.442q.881-.388 1.833-.563T6.5 4.962q1.47 0 2.866.423q1.398.423 2.634 1.23q1.237-.807 2.634-1.23t2.866-.423q.973 0 1.925.175t1.833.563q.352.125.547.442t.195.689v9.665q0 .614-.516.943q-.517.328-1.1.111q-.693-.27-1.418-.39q-.724-.121-1.466-.121q-1.48 0-2.88.448T12 18.769"></path></svg>'
        return admonition(
            value=value, title=title, color=color, icon_str=icon_str
        )

    return


@app.cell(hide_code=True)
def _(dedent, mo):
    # jb: include=false
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
def _(np):
    # jb: include=false
    def gaussian_noise(
        mean=0.,
        std_dev=1.,
        Hz=1.,
        duration_sec=10.,
        seed=1,
    ):
        rng = np.random.default_rng(seed=seed)

        n = int(Hz * duration_sec)
        measurements = rng.normal(
            loc=mean,
            scale=std_dev,
            size=n,
        )
        return measurements

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Calculus Definitions
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Left-Hand Limit:** $\lim_{x \rightarrow a^-} f(x) = b$ iff for every $\epsilon > 0$, there exists some $\delta > 0$ such that for all $x$, if $a - \delta < x < a$, then $\vert{}f(x) - b\vert{} < \epsilon$.

    **Right-Hand Limit:** $\lim_{x \rightarrow a^+} f(x) = b$ iff for every $\epsilon > 0$, there exists some $\delta > 0$ such that for all $x$, if $a < x < a + \delta$, then $\vert{}f(x) - b\vert{} < \epsilon$.

    **Two-Sided Limit:**

    $$\lim_{x \rightarrow a} f(x) = b \iff \lim_{x \rightarrow a^-} f(x) = b \quad \text{and} \quad \lim_{x \rightarrow a^+} f(x) = b.$$

    **Continuity on $(a, b)$:** $f$ is continuous on $(a, b)$ iff for every $c \in (a, b)$, $\lim_{x \to c^-} f(x) = \lim_{x \to c^+} f(x) = f(c)$.

    **Derivative:** The derivative of a function $f$ at some $x$ in its domain is

    $$f'(x) = \lim_{h\rightarrow0}\frac{f(x + h) - f(x)}{h}$$

    profided this limit exists.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Probability density function (PDF)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A probability density function (PDF) is a function which represents the probability density of some unkown value. Specifically, any probability density function $P$ represents a

    $$\int_a^b P(x)dx$$

    probability of being between constants $a$ and $b$ for all constants $a<b$. By definition, all PDFs must satisfy

    $$\int_{-\infty}^\infty P(x)dx = 1.$$

    $\lim_{x\rightarrow\infty}$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Assuming \(x\) and \(y\) are sampled **independently**, write

    $$
    z_\alpha=x+\alpha(y-x)=(1-\alpha)x+\alpha y.
    $$

    Since \(x\sim N(0,a^2)\) and \(y\sim N(0,b^2)\), we have

    $$
    z_\alpha\sim N\!\left(0,\,(1-\alpha)^2a^2+\alpha^2b^2\right).
    $$

    To make \(z_\alpha\) as close to \(0\) as possible, we should minimize its variance:

    $$
    f(\alpha)=(1-\alpha)^2a^2+\alpha^2b^2.
    $$

    Differentiate:

    $$
    f'(\alpha)=-2a^2(1-\alpha)+2b^2\alpha.
    $$

    Set this equal to zero:

    $$
    -a^2+a^2\alpha+b^2\alpha=0
    $$

    so

    $$
    \boxed{\alpha=\frac{a^2}{a^2+b^2}}.
    $$

    This is the same answer whether “closest to 0” means minimizing expected squared distance \(E[z_\alpha^2]\) or expected absolute distance \(E|z_\alpha|\), since both are increasing functions of the standard deviation of this zero-mean normal.

    So the noisier variable gets **less weight**: the coefficient on \(y\) is larger when \(a\) is larger, because \(x\) is then the less reliable estimate of \(0\).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\int_{x}^{x}$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    {term}`Signal`
    """)
    return


if __name__ == "__main__":
    app.run()
