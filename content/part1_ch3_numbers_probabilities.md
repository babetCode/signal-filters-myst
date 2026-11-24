---
title: Probabilities
# marimo-version: 0.25.1
# css_file: notebook-styles.css
subtitle: "To Infinity and Beyond"
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

plt.style.use('default')
schemdraw.use("svg")
mo.latex(dedent(
    r"""\newcommand{\existsin}[2]{\exists #1 \!\!\in\!\! #2\,}
    \newcommand{\forallin}[2]{\forall #1 \!\!\in\!\! #2\,}
    \newcommand{\existssubseteq}[2]{\exists #1 \!\!\subseteq\!\! #2\,}
    \newcommand{\forallsubseteq}[2]{\forall #1 \!\!\subseteq\!\! #2\,}"""
))
mo.output.clear()
```

In mathematical terms, the notion of probability depends on sigma algebra
  
### Sigma Algebra

A $\sigma$-algebra $F$ of a set $\Omega$ (called the ambient set) is a subset of $\mathcal P (\Omega)$ which satisfy three criteria:

1. **Contains the sample space:**
   $$\Omega \in F.$$
2. **Closed under complementation:**
   $$S \in F \rightarrow S^c \in F,$$
   where $S^c$ is the complement of $S$: $\{x \in \Omega: x \notin S\}$.
3. **Closed under countable unions:**
    $$S_1, S_2, S_3, \ldots \in F \rightarrow \bigcup_{i=1}^\infty S_i \in F,$$
   where $\bigcup_{i=1}^\infty$ is shorthand for $S_1 \cup S_2 \cup \cdots$.
  
Now, we can define a **probability space**:
  
:::{div}
:class: h-0 overflow-hidden opacity-0 m-0 p-0 pointer-events-none

### Probability Space
:::

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Probability Space
: a triple $(\Omega, F, P)$, where:
  - $\Omega$ is a set (the sample space),
  - $F$ is a $\sigma$-algebra of subsets of $\Omega$ (the “events”),
  - $P$ is a function from $F$ to $[0,1]$ satisfying: $P(\Omega) = 1$, and countable additivity (for pairwise disjoint events $A_1, A_2, ..., P(\bigcup A_i) = ΣP(Aᵢ))$.
:::
::::
  
### Coin Toss

Whenever we talk about the probablility of something happening, we are refering to the value of some $P(A)$, where $P$ is a probability function in some probability space $(\Omega, F, P)$, and $A$ is some event in a $\sigma$-algebra $F$. For example, let's define a probability space for a coin flip that might produce heads or tails:

**Defining $\Omega$:** Since we only have two possible samples (heads or tails), $\Omega$ will only have two elements in this case:

$$\Omega = \{H, T\}.$$

**Defining $F$:** Since $\mathcal P(\Omega) = \{\{H, T\}, \{H\}, \{T\}, \emptyset\}$, we only have a couple options here which are closed under complementation and countable unions:

1. $F = \{\{H, T\}, \emptyset\}$. This is the simplest, but the only events are "something happening" (equal to $\Omega$, with $P(\Omega) = 1$), and "nothing happening" (where $P(\emptyset)$ is always zero to satisfy additivity). The rules allow it, but it's not very interesting.
2. $F = \mathcal P(\Omega)$. This also works as a $\sigma$-algebra and is much more interesting because it includes $\{H\}$ and $\{T\}$ as events. Let's use this one.

**Defining $P$:** We must have $P(\Omega) = 1$ and $P(\emptyset) = 0$, but we are free to pick any $P(\{H\})$ and $P(\{T\})$ that satisfy

$$P(\{H\}) + P(\{T\}) = P(\{H\} \cup \{T\}) = P(\{H, T\}) = P(\Omega) = 1.$$

The natural choice is $P(\{H\}) = P(\{T\}) = 0.5$, but we're free to model an unfair coin if we wish.
  
### Random Rational

Now, let's model picking a random number from $\mathbb Q \cap [0, 1]$. This example is more subtle than the coin toss, because the sample space is infinite and the natural-sounding choice ("every rational is equally likely") turns out to be impossible.

**Defining $\Omega$:** We take the sample space to be the set of rationals in the unit interval:

$$\Omega = \mathbb Q \cap [0, 1] = \{x \in \mathbb Q : 0 \le x \le 1\}.$$

This set is infinite, but it is *countable*, meaning we can list all of its elements in a sequence $q_1, q_2, q_3, \ldots$ in which every element appears exactly once. For example, we can list them by increasing denominator:

$$0,\; 1,\; \tfrac12,\; \tfrac13,\; \tfrac23,\; \tfrac14,\; \tfrac34,\; \tfrac15,\; \tfrac25,\; \tfrac35,\; \tfrac45,\; \ldots$$

(skipping any fraction that is not in lowest terms, so that no number is listed twice). Fix this enumeration for the rest of the section.

**Defining $F$:** Just as in the coin toss, we can take $F = \mathcal P(\Omega)$. The power set always satisfies the three $\sigma$-algebra criteria: it contains $\Omega$, since $\Omega \subseteq \Omega$; it is closed under complementation, since $S^c \subseteq \Omega$ whenever $S \subseteq \Omega$; and it is closed under countable unions, since a union of subsets of $\Omega$ is again a subset of $\Omega$. In particular, every singleton $\{q\}$ is an event.

**Defining $P$:** The natural guess is to make every rational equally likely, say $P(\{q\}) = c$ for every $q \in \Omega$. But the singletons $\{q_1\}, \{q_2\}, \ldots$ are pairwise disjoint and their union is $\Omega$, so countable additivity would require

$$1 = P(\Omega) = \sum_{n=1}^\infty P(\{q_n\}) = \sum_{n=1}^\infty c.$$

If $c = 0$ the sum is $0$, and if $c > 0$ the sum diverges to $\infty$. Neither equals $1$, so **no uniform probability function exists on a countably infinite set.**

We can still build a valid $P$ by giving up on "equally likely". Using our enumeration, assign

$$P(\{q_n\}) = 2^{-n},$$

and for a general event $A \in F$, add up the probabilities of the points it contains:

$$P(A) = \sum_{n \,:\, q_n \in A} 2^{-n}.$$

This satisfies the requirements:

- $P(\Omega) = \sum_{n=1}^\infty 2^{-n} = 1$.
- $P(A) \in [0, 1]$ for every event, since $P(A) \le P(\Omega) = 1$ (all terms are nonnegative).
- If $A_1, A_2, \ldots$ are pairwise disjoint, each index $n$ belongs to at most one $A_i$, so the sum over $\bigcup A_i$ splits into the sums over each $A_i$ (this rearrangement is allowed because all terms are nonnegative). Hence $P(\bigcup A_i) = \sum P(A_i)$.

Note that this $P$ depends entirely on our arbitrary choice of enumeration. Reordering the list would give the same rational a different probability. There is no canonical way to pick a "random rational", and this is the price of working in a countable set.

*Note:* If we want a truly uniform random number, we have to move to $\Omega = [0,1]$ (the real numbers) and use the Lebesgue measure, where $P([a,b]) = b - a$. There, $F$ cannot be the full power set, and must be a smaller $\sigma$-algebra (the Borel sets). In that model, every single point has probability $0$, and since $\mathbb Q \cap [0,1]$ is countable, countable additivity gives $P(\mathbb Q \cap [0,1]) = 0$. In other words, a uniformly random real number in $[0,1]$ is irrational with probability $1$.
  
### Random Number

Now, let's model picking a random number from $[0, 1]$. This is the example the previous section was pointing toward: we want every number to be "equally likely," and now it will turn out that we can get something close to that, provided we are careful about which sets we call events.

**Defining $\Omega$:** We take the sample space to be the closed unit interval of real numbers:

$$\Omega = [0, 1] = \{x \in \mathbb R : 0 \le x \le 1\}.$$

Unlike $\mathbb Q \cap [0,1]$, this set is *uncountable*, meaning there is no way to list all of its elements in a sequence $x_1, x_2, x_3, \ldots$ (this is Cantor's diagonal argument). This is exactly what lets us escape the problem from the last section: countable additivity only lets us add up countably many probabilities, so it no longer forces the probability of $\Omega$ to be a sum of single-point probabilities.

**Defining $F$:** Our first instinct is to copy the previous examples and take $F = \mathcal P(\Omega)$. This is a valid $\sigma$-algebra, but it turns out to be *too big*: it can be proven (using the Axiom of Choice) that no function $P$ on all of $\mathcal P([0,1])$ can satisfy countable additivity, $P(\Omega) = 1$, and also assign every interval $[a, b]$ the probability $b - a$ (the Vitali set is the classic counterexample). So we must settle for a smaller $\sigma$-algebra.

We want $F$ to contain every interval, since "the number lands between $a$ and $b$" is surely an event we care about. Rather than listing the members of $F$ by hand, we define it as the *smallest* $\sigma$-algebra containing all of those intervals. This is well defined because the intersection of any collection of $\sigma$-algebras on $\Omega$ is again a $\sigma$-algebra, so we can take

$$F = \bigcap \{G : G \text{ is a } \sigma\text{-algebra on } \Omega \text{ and } [a,b] \in G \text{ for all } 0 \le a \le b \le 1\}.$$

This is called the **Borel $\sigma$-algebra** on $[0,1]$ and its members are called **Borel sets**. By closure under complements and countable unions, it automatically contains many more sets than just intervals, such as open intervals, single points, and every countable set (including $\mathbb Q \cap [0,1]$). In practice, every set you are likely to write down is a Borel set, so we lose very little by excluding the others.

**Defining $P$:** We want the probability of landing in an interval to equal its length:

$$P([a, b]) = b - a.$$

A major theorem of measure theory (the existence of the **Lebesgue measure**, usually proven with Carathéodory's extension theorem) guarantees that there is exactly one function $P : F \to [0,1]$ which satisfies this and also countable additivity. We will take this for granted here, since constructing it takes more machinery than we have built so far. This $P$ is called the **uniform distribution** on $[0, 1]$.

Several consequences follow directly from the axioms:

- **Every single point has probability zero.** For any $x \in \Omega$, $P(\{x\}) = P([x, x]) = x - x = 0$. So unlike the discrete examples, we can no longer find the probability of an event by adding up the probabilities of its individual outcomes.
- **Countable sets have probability zero.** Any countable set $\{x_1, x_2, \ldots\}$ is a countable disjoint union of singletons, so countable additivity gives $P(\{x_1, x_2, \ldots\}) = \sum_i 0 = 0$. In particular, $P(\mathbb Q \cap [0,1]) = 0$, so a uniformly random real number is irrational with probability $1$.
- **Zero probability does not mean impossible.** The outcome $x = 0.5$ is a member of $\Omega$ and could happen, even though $P(\{0.5\}) = 0$. Similarly, probability $1$ does not mean certain. Events like these are described as holding *almost surely*, and this subtlety is unavoidable once $\Omega$ is uncountable.
- **Endpoints don't matter.** Since single points have probability zero, $P([a,b]) = P((a,b)) = P([a,b)) = P((a,b]) = b - a$.

Going forward, this is the model we will use whenever we talk about a quantity (like the noise in a measurement) taking a value from a continuous range. In that setting, we will rarely ask for the probability of a single value, and will instead ask for the probability of landing in some interval.
  
### Conditional Probability

If $A$ and $B$ are events in a probability space, then the conditional probability $P(A|B)$ (read as "probability of A given B") is defined as

$$P(A|B) := \frac{P(A \cap B)}{P(B)}$$
  
### Bayes Theorem

Since $A \cap B = B\cap A$, we have

$$\begin{align*}
P(A|B) &= \frac{P(A \cap B)}{P(B)} \\
&= \frac{P(A)\left(\frac{P(B \cap A}{P(A)}\right)}{P(B)} \\
&= \frac{P(A)P(B|A)}{P(B)}
\end{align*}$$
  
## Discrete probabilties.
  
Discrete probablity distributions are the typical type of probablity we encounter in a "50/50" coin toss or "hitting the red" in roulette. There are a finite nubmer of possible outcomes, exactly one of which will actually be true. Since we don't know which one, we assign some probabilty to each, and since *something* must be true, the sum of all probabilities is 1.
  
## Modeling Noise
  
As previously discussed, it is impossible to measure anything with 100% precision. Because measurements are unpredicatble, we say that the measurement {term}`signal` is {term}`stochastic`. Therefore, we model measurements as being sampled from a **probability density function** (PDF).
  
## Brainstorm
  
modeling the measurement as the sum of the true value with a noise value, which we can write as
$$z = x + \eta$$
combining our knowlege and measurements to increase the
  
The mean of a PDF is defined as
  
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

```{marimo} python
# TODO figure out if there's a difference between the mean vs the expected value of a PDF, does the term "expected value" even apply to a PDF or only to a sample taken from it?

# TODO explain convolutions
```