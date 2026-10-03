---
abbreviations:
  iff: if and only if
  diff: null
  PDF: probability density function
numbering:
  equations: false
---

# Optimal Filterings
<!---->

```{marimo} python
:hide-code: true
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
:hide-code: true
:name: display_format
:include: false
plt.style.use('default')
schemdraw.use("svg")
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

Our goal when designing a signal filter is to algorithmically combine multiple measurements to increase the probability that the noise "cancels out". In the last two sections, we've seen different examples of using an $\alpha$ value to take a weighed average of a prior estimate and a measurement. In this section, we will address the problem of choosing a value of $\alpha$ given different expected {term}`noise` components from our estimate and measurement.
<!---->
## Modeling Noise
<!---->
As previously discussed, it is impossible to measure anything with 100% precision. Because measurements are unpredicatble, we say that the measurement {term}`signal` is {term}`stochastic`. Therefore, we model measurements as being sampled from a **probability density function** (PDF).
<!---->
::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Probability Density Function
: A {term}`function` which represents the probability density of some unkown value. Specifically, for any PDF $P$, the probability of its represented value falling between constants $a$ and $b$ (where $a<b$) is defined by the {term}`integral`:
  $$\int_a^b P(x)\, dx.$$
  By definition, all PDFs must satisfy
  $$\int_{-\infty}^\infty P(x)\, dx = 1.$$
:::
::::
<!---->
## brainstorm
<!---->
The mean of a PDF is defined as
<!---->
::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Mean
: 1. (Of a sample of data $n$ values) The sum of the values divided by n:
  $$\bar x := \sum_{x=1}^n x_i$$

  2. (Of a continuous function $f(x)$ over $[a,b]$) The integral of $f(x)x$ over $[a,b]$:
  $$\mu_{[a,b]} := \int_a^b f(x)x\, dx.$$
  If no interval is specified, it is assumed to be over the reals:
  $$\mu := \int_{-\infty}^\infty f(x)x\, dx.$$
:::
::::

```{marimo} python
# TODO figure out if there's a difference between the mean vs the expected value of a PDF, does the term "expected value" even apply to a PDF or only to a sample taken from it?
```
