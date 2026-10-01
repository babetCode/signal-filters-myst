---
title: "Optimal Filtering"
numbering:
  equations: false
---

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
As previously discussed, it is impossible to measure anything with 100% precision. Because measurements are unpredicatble, we say that the measurement {term}`signal` is {term}`stochastic`. Therefore, we model measurements as being sampled from a **probability density function**.
<!---->
::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Probability Density Function
: A {term}`function` which represents the probability density of some unkown value. Specifically, for any PDF $P$, the probability of its represented value falling between constants $a$ and $b$ (where $a<b$) is defined by the {term}`integral`: $$\int_a^b P(x)dx.$$ By definition, all PDFs must satisfy $$\int_{-\infty}^\infty P(x)dx = 1.$$
:::
::::
<!---->
## Brainstorm
<!---->
The **Reimman sum** is something like:

if we break the area under a curve $f(x)$ between points $a$ and $b$ (where $a<b$) into partitions with maximum width $k$, and we let $p_i$ be the $x$ value at the start of the $i$-th partition, then area of the $i$-th partition under the curve has the left-hand approximation

$$f(p_i)p_i,$$

so the area under the whole curve has the left-hand approximation

$$\sum f(p_i)p_i*.$$

and the definite integral of $f(x)$ from $a$ to $b$ is

$$\int_a^b f(x)dx = \lim_{k\rightarrow0}\left(\sum f(p_i)p_i*\right).$$

```{marimo} python
# TODO figure out if there's a difference between the mean vs the expected value of a PDF, does the term "expected value" even apply to a PDF or only to a sample taken from it?
```
