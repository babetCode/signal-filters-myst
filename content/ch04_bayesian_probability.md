---
title: Chapter 4
# marimo-version: 0.25.1
# css_file: notebook-styles.css
subtitle: "Bayesian Porbability: Building on the foundations"
abbreviations:
  iff: if and only if
  diff: null
  PDF: probability density function
numbering:
  equations: false
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

Our goal when designing a signal filter is to algorithmically remove noise from a measurement signal. As we saw in the past two sections, this is usually done by combining our knowlege and measurements in a way that increases the probability that the noise cancels out. To understand what that means, it is helpful to develop a more rigorous notion of probability. Since probability is built on set theory, we will first address sets and their notation.
  
## Sets
  
While the term "set" is not rigorously defined in mathematics[^primitive-terms], we can think of it as "any unordered collection of unique objects" for now. For a more precise understanding, see the [set theory](/extra-set-theory) section.

[^primitive-terms]: This is because the term set is a "primitive term", meaning it is a foundational block on which other terms are defined; its meaning in strictly derived from the axioms which describe how it *behaves*, rather than what it *is*.
  
## What is probability
  
In mathematical terms, the notion of probability depends on a **probability space**
  
::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Probability Space
: a triple $(\Omega, F, P)$, where:
  - $\Omega$ is a set (the sample space),
  - $F$ is a $\sigma$-algebra of subsets of $\Omega$ (the “events”),
  - $P$ is a function from $F$ to $[0,1]$ satisfying: $P(\Omega) = 1$, and countable additivity (for pairwise disjoint events $A_1, A_2, ..., P(\bigcup A_i) = ΣP(Aᵢ))$.
:::
::::
  
## Discrete probabilties.
  
Discrete probablity distributions are the typical type of probablity we encounter in a "50/50" coin toss or "hitting the red" in roulette. There are a finite nubmer of possible outcomes, exactly one of which will actually be true. Since we don't know which one, we assign some probabilty to each, and since *something* must be true, the sum of all probabilities is 1.
  
## Intersections
  
The conditional probability $A$ given $B$ is defined
$$P(A|B) := \frac{P(A\cap B)}{P(B)}$$
  
## Modeling Noise
  
As previously discussed, it is impossible to measure anything with 100% precision. Because measurements are unpredicatble, we say that the measurement {term}`signal` is {term}`stochastic`. Therefore, we model measurements as being sampled from a **probability density function** (PDF).
  
:::{admonition icon=false} 📖 **Definition**
<u>**Probability Density Function**</u>
A&nbsp;function&nbsp;which represents the probability density of some unkown value. Specifically, for any PDF $P$, the probability of its represented value falling between constants $a$ and $b$ (where $a<b$) is defined by the &nbsp;integral&nbsp;:
$$\int_a^b P(x)\, dx.$$
By definition, all PDFs must satisfy
$$\int_{-\infty}^\infty P(x)\, dx = 1.$$
:::
  
## Brainstorm
  
modeling the measurement as the sum of the true value with a noise value, which we can write as
$$z = x + \eta$$
combining our knowlege and measurements to increase the
  
The mean of a PDF is defined as
  
:::{admonition icon=false} 📖 **Definition**
<u>**Mean**</u>
1. (Of a sample of $n$ values) The sum of the values divided by n:
$$\bar x := \sum_{x=1}^n x_i$$

2. (Of a continuous function $f(x)$ over $[a,b]$) The integral of $f(x)x$ over $[a,b]$:
$$\mu_{[a,b]} := \int_a^b f(x)x\, dx.$$
If no interval is specified, it is assumed to be over the reals:
$$\mu := \int_{-\infty}^\infty f(x)x\, dx.$$
:::
  
###
  
### Bayesian statistics
  
Consider a game of three card monte, where we must guess which one of three shuffled cards is the queen. If we guess perfectly at random we would have a $\frac13$ chance of guessing correctly. Put differently, if we had no information about the cards (other than exactly one of them being the queen), then the most reasonable probability distribution to assign would be:

$$\begin{align*}
\text{card 1: } & 1/3 \\
\text{card 2: } & 1/3 \\
\text{card 3: } & 1/3 \\
\end{align*}$$

Now consider how card 1's probability would change if card 3 was reavealed to *not* be the queen. According the the Bayesian formula, this is calculated as

$$\begin{align*}
P(\text{card 1} | \neg \text{card 3}) &= \frac{P^-(\text{card 1})P(\neg\text{card 3}|\text{card 1})}{P(\neg\text{card 3})} \\
&= \frac{(1/3)(1)}{(2/3)} = \boxed{\frac12}.
\end{align*}$$
  
Now, consider a hypothetical game of darts where the horizontal position of the dart is normally distributed. In other words, the probability that the dart's horizontal position lands $x$ to the right of the the bullseye is
$$x \sim \mathcal N(0, \sigma^2).$$
Imagine that a dart is thrown while you are not watching, and then you are only told that dart fell to the right of the bullseye. Given only this information, how should you update your distribution for $x$?
  
Now, consider the following thought experiement: you are driving a car on "x-axis ave." in mythical math world. an infinitely long, perfectly straight road. Your are completely lost, but have a GPS to locate your position on the road—the GPS has some Gaussian noise in the reading. In other words, given some position reading by the GPS, the probability distribution of your position can be represented as a normal curve centered at the reading.
  
Bayes theorem gives

$$p(X|Z) = \frac{p(Z|X)p(X)}{p(Z)},$$
where:
- $p(X)$ is the prior density.
- $p(Z|X)$ is the likelihood.
- $p(X|Z)$ is the posterior density.
- $p(Z)$ is the evidence, or marginal likelihood.
  
:::{admonition icon=false} 📖 **Definition**
<u>**Convolution**</u>
The convolution of functions $f$ and $g$ is defined as
$$(f * g)(x) = \int_{-\infty}^\infty f(x-t)g(t)\, dt.$$
:::

```{marimo} python
# TODO figure out if there's a difference between the mean vs the expected value of a PDF, does the term "expected value" even apply to a PDF or only to a sample taken from it?

# TODO explain convolutions
```

Edit `sync_notebooks.py` to convert
```md
:::{admonition icon=false} 📖 **Definition**
<u>**Term**</u>
Definition of the term.
$$x = \text{equation on a new line}$$
Another line of text
:::
```
into
```md
::::{admonition icon=false} 📖 **Definition**
:::{glossary}
term
: Definition of the term with all new lines being indented by two spaces.
  $$x = \text{equation on a new line}$$
  Another line of text
:::
::::
```
  
| Symbol / Abbreviation | LaTeX Command | English Reading / Meaning |
| :--- | :--- | :--- |
| $\wedge$ | `\wedge` or `\land` | **"and"** (Conjunction) |
| $\vee$ | `\vee` or `\lor` | **"or"** (Disjunction) |
| $\neg$ | `\neg` or `\lnot` | **"not"** (Negation) |
| $\rightarrow$ | `\rightarrow` or `\to` | **"implies"** / **"if... then..."** |
| $\leftrightarrow$ | `\leftrightarrow` or `\iff` | **"if and only if"** (Biconditional) |
| $\oplus$ | `\oplus` | **"exclusive or"** (XOR) |
| $\forall$ | `\forall` | **"for all"** / **"for every"** |
| $\exists$ | `\exists` | **"there exists"** |
| $\exists!$ | `\exists!` | **"there exists a unique"** |
| $\therefore$ | `\therefore` | **"therefore"** |
| $\because$ | `\because` | **"because"** |
| $\in$ | `\in` | **"is an element of"** / **"is in"** |
| $\notin$ | `\notin` | **"is not an element of"** |
| $\subseteq$ | `\subseteq` | **"is a subset of"** (Inclusive) |
| $\subset$ | `\subset` or `\subsetneq` | **"is a proper subset of"** (Strict) |
| $\cap$ | `\cap` | **"intersection"** (Elements in both) |
| $\cup$ | `\cup` | **"union"** (Elements in either or both) |
| $\setminus$ | `\setminus` | **"set difference"** / **"minus"** |
| $\times$ | `\times` | **"Cartesian product of"** |
| $\mathcal{P}$ | `\mathcal{P}` or `\wp` | **"power set of"** |
| $\emptyset$ | `\emptyset` or `\varnothing` | **"the empty set"** |
| s.t. / $\mid$ | `:` or `\mid` | **"such that"** |
| WLOG | *N/A* | **"Without loss of generality"** |
| Q.E.D. / $\blacksquare$ | `\blacksquare` | **"Which was to be demonstrated"** (End of proof) |
| iff | *N/A* | **"if and only if"** |