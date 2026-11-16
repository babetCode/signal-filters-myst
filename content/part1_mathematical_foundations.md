---
title: Mathematical Foundations
# marimo-version: 0.25.1
# css_file: notebook-styles.css
subtitle: "From Primitives to Probabilities"
abbreviations:
  iff: if and only if
  diff: null
  ZFC: Zermelo-Frankel set theory with Axiom of Choice
numbering:
  equations: false
math:
  '\existsin': '\exists #1 \!\!\in\!\! #2\,'
  '\forallin': '\forall #1 \!\!\in\!\! #2\,'
  '\existssubseteq': '\exists #1 \!\!\subseteq\!\! #2\,'
  '\forallsubseteq': '\forall #1 \!\!\subseteq\!\! #2\,'
---

```{marimo-config}
:eval: false
---
pyproject: |-
  dependencies = [
      "marimo>=0.25.1",
      "matplotlib==3.11.2",
      "numpy==2.5.3",
      "pandas==3.0.6",
      "schemdraw==0.23",
  ]
---
```

```{marimo} python
:name: imports
:include: false

import marimo as mo
import numpy as np
import pandas as pd
import matplotlib
import schemdraw
from schemdraw import flow
from textwrap import dedent
import matplotlib.pyplot as plt
```

```{marimo} python
:name: display_format
:include: false

plt.style.use('default')
schemdraw.use("svg")
mo.latex(r"""
\newcommand{\existsin}[2]{\exists #1 \!\!\in\!\! #2\,}
\newcommand{\forallin}[2]{\forall #1 \!\!\in\!\! #2\,}
\newcommand{\existssubseteq}[2]{\exists #1 \!\!\subseteq\!\! #2\,}
\newcommand{\forallsubseteq}[2]{\forall #1 \!\!\subseteq\!\! #2\,}
""")
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
```

Our goal when designing a signal filter is to algorithmically remove noise from a measurement signal. This is usually done by combining our knowlege and measurements in a way that increases the probability that the noise cancels out. In terms of the equations from the introduction:

$$\hat{x}_k = \hat x_k^- + \alpha (z_k - \hat x_k^-).$$

Here we lay the groundwork for answering the question:

>"Given some amounts of noise in our prior ($\hat x_k^-$) and measurement ($z_k$), what value of $\alpha$ should we pick?"

Since modeling noise relies on probabilities, probabilities are built on set theory, and set theory is built on logic, we will briefly introduce these topics along the way.