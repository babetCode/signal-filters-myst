---
title: "Optimal Filtering"
numbering:
  equations: false
---

```{marimo-config}
:pyproject:
    requires-python = ">=3.13"
    dependencies = [
        "matplotlib==3.11.1",
        "numpy==2.5.2",
        "pandas==3.0.5",
        "schemdraw[matplotlib,svgmath]==0.23",
    ]
```

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

# Calculus Definitions
<!---->
**Left-Hand Limit:** $\lim_{x \rightarrow a^-} f(x) = b$ iff for every $\epsilon > 0$, there exists some $\delta > 0$ such that for all $x$, if $a - \delta < x < a$, then $\vert{}f(x) - b\vert{} < \epsilon$.

**Right-Hand Limit:** $\lim_{x \rightarrow a^+} f(x) = b$ iff for every $\epsilon > 0$, there exists some $\delta > 0$ such that for all $x$, if $a < x < a + \delta$, then $\vert{}f(x) - b\vert{} < \epsilon$.

**Two-Sided Limit:**

$$\lim_{x \rightarrow a} f(x) = b \iff \lim_{x \rightarrow a^-} f(x) = b \quad \text{and} \quad \lim_{x \rightarrow a^+} f(x) = b.$$

**Continuity on $(a, b)$:** $f$ is continuous on $(a, b)$ iff for every $c \in (a, b)$, $\lim_{x \to c^-} f(x) = \lim_{x \to c^+} f(x) = f(c)$.

**Derivative:** The derivative of a function $f$ at some $x$ in its domain is

$$f'(x) = \lim_{h\rightarrow0}\frac{f(x + h) - f(x)}{h}$$

profided this limit exists.
<!---->
# Probability density function (PDF)
<!---->
A probability density function (PDF) is a function which represents the probability density of some unkown value. Specifically, any probability density function $P$ represents a

$$\int_a^b P(x)dx$$

probability of being between constants $a$ and $b$ for all constants $a<b$. By definition, all PDFs must satisfy

$$\int_{-\infty}^\infty P(x)dx = 1.$$

$\lim_{x\rightarrow\infty}$
<!---->
Assuming \(x\) and \(y\) are sampled **independently**, write

$$z_\alpha=x+\alpha(y-x)=(1-\alpha)x+\alpha y.$$

Since \(x\sim N(0,a^2)\) and \(y\sim N(0,b^2)\), we have

$$z_\alpha\sim N\!\left(0,\,(1-\alpha)^2a^2+\alpha^2b^2\right).$$

To make \(z_\alpha\) as close to \(0\) as possible, we should minimize its variance:

$$f(\alpha)=(1-\alpha)^2a^2+\alpha^2b^2.$$

Differentiate:

$$f'(\alpha)=-2a^2(1-\alpha)+2b^2\alpha.$$

Set this equal to zero:

$$-a^2+a^2\alpha+b^2\alpha=0$$

so

$$\alpha=\frac{a^2}{a^2+b^2}.$$

This is the same answer whether “closest to 0” means minimizing expected squared distance \(E[z_\alpha^2]\) or expected absolute distance \(E|z_\alpha|\), since both are increasing functions of the standard deviation of this zero-mean normal.

So the noisier variable gets **less weight**: the coefficient on \(y\) is larger when \(a\) is larger, because \(x\) is then the less reliable estimate of \(0\).
<!---->
$\int_{x}^{x}$
