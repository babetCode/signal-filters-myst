---
title: Probability Spaces
# marimo-version: 0.25.1
# css_file: notebook-styles.css
subtitle: "Measuring Uncertainty"
abbreviations:
  iff: if and only if
  diff: null
numbering:
  equations: false
---

```{marimo-config}
---
pyproject: |-
  dependencies = [
      "marimo>=0.25.1",
      "matplotlib==3.11.2",
      "numpy==2.5.3",
  ]
---
```

```{marimo} python
:name: imports
:include: false

import marimo as mo
import numpy as np
import matplotlib.pyplot as plt
from textwrap import dedent
```

```{marimo} python
:name: display_settings
:include: false

plt.style.use("default")

def graphic(x):
    return mo.Html(dedent(f'''\
        <div class="graphic">
            {mo.as_html(x)}
        </div>
        '''))
```

:::{seealso icon=false} 🔗 **Prerequisites**
- [Chapter 2](ch2_axioms_of_set_theory_v2.md): power sets, the intersection $\bigcap F$ of a nonempty set of sets, sets of functions $Y^X$, and the Axiom of Choice (used once, for the Vitali set).
- [Chapter 3](ch3_sets_for_probability_v2.md): {term}`complements <complement>` and De Morgan's laws, {term}`indexed families <indexed family>` and the Disjointification lemma, {term}`partitions <partition>`, {term}`countable` and {term}`uncountable` sets (including the Listing theorem and the countability of $\mathbb Q$), the Archimedean property, {term}`intervals <interval>`, and the {term}`extended real numbers`.
- [Appendix C: Sequences and Limits](appendix_c_calculus_v2.md): limits, the limit laws, and Monotone Convergence (for the continuity of probability).
- [Appendix C: Series](appendix_c_calculus_v2.md): series of nonnegative terms, their value in $[0, \infty]$, and the theorem that such sums may be reordered and regrouped (Nonnegative Sums in Any Order).
:::
  
The Introduction claimed that averaging noisy measurements makes the noise "cancel out". To turn that claim into theorems ([Chapter 6](ch6_expectation_and_variance_v2.md)) and use them to choose $\alpha$ ([Chapter 7](ch7_optimal_alpha_v2.md)), we need a precise model of uncertainty. This chapter builds it. A **probability space** $(\Omega, \mathcal F, \mathbb P)$ consists of a set $\Omega$ of possible outcomes, a collection $\mathcal F$ of *events* (the sets of outcomes we are allowed to ask about), and a function $\mathbb P$ that assigns each event its probability. Every later statement, such as "the measurement noise has variance $R$" or "the estimate is unbiased", is a statement about a probability space.

We write $\mathbb P$ (blackboard-bold P) for probabilities because $P_k$ will denote the Kalman filter's error variance.

:::{attention icon=false} 🗝️ **Key Idea**
Probabilities are assigned to *sets* of outcomes, called events, not to individual outcomes. For a continuous quantity such as scale noise, every single outcome has probability $0$, and only sets such as intervals carry probability.
:::
  
## Motivation: A Scale Reading to 0.1 lb

Our scale computes its weight estimate as a real number but displays it rounded to $0.1$ lb. Suppose the true weight is $155$ lb, and write a single reading as $155 + \omega$, where $\omega$ is the noise in pounds.[^noise-informal] Questions about the display are questions about $\omega$:

- "The display shows $155.0$" happens exactly when $154.95 \le 155 + \omega < 155.05$, that is, when $\omega \in [-0.05, 0.05)$.
- "The display does not show $155.0$" is the complement $\mathbb R \setminus [-0.05, 0.05)$.
- "The display shows $155.0$ or $155.1$" is the union $[-0.05, 0.05) \cup [0.05, 0.15) = [-0.05, 0.15)$.
- "Every one of infinitely many readings displays $155.0$" combines infinitely many conditions, one per reading, with "and".

So the questions we want probabilities for are *sets* of possible noise values, combined with complements, unions, and intersections, sometimes of infinitely many sets. The question "what is the probability that $\omega$ is exactly $0.03$?" will turn out to have the answer $0$ in every reasonable continuous model, even though some value of $\omega$ certainly occurs. A probability model therefore assigns probabilities to sets, and it must say which sets.

[^noise-informal]: For now $\omega$ is just an unknown real number. [Chapter 5](ch5_random_variables_v2.md) makes noise precise as a random variable.
  
## Sample Spaces, Outcomes, and Events

We model an experiment whose result is uncertain, such as tossing a coin, rolling a die, or taking a scale reading, by first fixing the set of everything that could happen.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Sample space
: A nonempty set, usually written $\Omega$, whose elements represent the possible results of an experiment, chosen so that each run of the experiment produces exactly one element of $\Omega$.
:::
::::

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Outcome
: An element $\omega$ of a {term}`sample space` $\Omega$.
:::
::::

Mathematically, any nonempty set can serve as a sample space; the interpretation is part of the model. Examples:

- a coin toss: $\Omega = \{H, T\}$, where $H$ and $T$ are two distinct symbols for heads and tails;
- a die: $\Omega = \{1, 2, 3, 4, 5, 6\}$;
- two dice: $\Omega = \{1, \ldots, 6\} \times \{1, \ldots, 6\}$, as in Chapter 3's preimage explorer;
- the noise in one scale reading: $\Omega = \mathbb R$;
- a number chosen "uniformly at random" between $0$ and $1$: $\Omega = [0, 1]$.

The sample space must be detailed enough to describe every result we want to ask about. To ask about the first die as well as the sum of two dice, we need $\Omega = \{1, \ldots, 6\}^2$, not $\Omega = \{2, \ldots, 12\}$.

A statement about the result of the experiment corresponds to the set of outcomes for which it is true. "The die shows an even number" corresponds to $\{2, 4, 6\}$. Logical operations on statements become operations on sets, with complements taken relative to $\Omega$:

| Statement | Set of outcomes |
|---|---|
| $A$ happens | the outcome $\omega$ lies in $A$ |
| $A$ does not happen | $A^c = \Omega \setminus A$ |
| $A$ or $B$ happens | $A \cup B$ |
| $A$ and $B$ both happen | $A \cap B$ |
| $A$ and $B$ cannot both happen | $A \cap B = \emptyset$ ({term}`disjoint`) |
| if $A$ happens, then $B$ happens | $A \subseteq B$ |
| something happens / nothing happens | $\Omega$ / $\emptyset$ |
| at least one of $A_1, A_2, \ldots$ happens | $\bigcup_{n=1}^\infty A_n$ |
| all of $A_1, A_2, \ldots$ happen | $\bigcap_{n=1}^\infty A_n$ |

Which subsets of $\Omega$ should be given probabilities? For a die, all of them. For the scale noise, this chapter shows that we *cannot* sensibly give a probability to every subset of $\mathbb R$. So a model must specify its collection of events, and that collection must be closed under the operations in the table.
  
## σ-Algebras

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Sigma-algebra
: A σ-algebra on a set $\Omega$ is a set $\mathcal F \subseteq \mathcal P(\Omega)$ such that:

  1. $\Omega \in \mathcal F$;
  2. if $A \in \mathcal F$, then $A^c \in \mathcal F$ (complement relative to $\Omega$);
  3. if $(A_n)_{n=1}^\infty$ is a sequence of elements of $\mathcal F$, then $\bigcup_{n=1}^\infty A_n \in \mathcal F$.
:::
::::

The σ ("sigma", for *sum*) refers to the countable unions in condition 3. The pair $(\Omega, \mathcal F)$ is called a *measurable space*.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Event
: Given a {term}`sample space` $\Omega$ and a {term}`σ-algebra <sigma-algebra>` $\mathcal F$ on $\Omega$, an event is an element of $\mathcal F$.
:::
::::

So every event is a set of outcomes, but a set of outcomes is an event only if it belongs to the chosen $\mathcal F$. The definition asks only for $\Omega$, complements, and countable unions; everything else in the table above follows.

:::{important icon=false} 📐 **Lemma (Closure Properties)**
Let $\mathcal F$ be a σ-algebra on $\Omega$. Then:

1. $\emptyset \in \mathcal F$;
2. if $A_1, \ldots, A_n \in \mathcal F$ with $n \ge 1$, then $\bigcup_{k=1}^n A_k \in \mathcal F$ and $\bigcap_{k=1}^n A_k \in \mathcal F$;
3. if $(A_n)_{n=1}^\infty$ is a sequence in $\mathcal F$, then $\bigcap_{n=1}^\infty A_n \in \mathcal F$;
4. if $A, B \in \mathcal F$, then $A \setminus B \in \mathcal F$.
:::

:::{admonition icon=false} ✍️ **Proof**
1. $\emptyset = \Omega^c$.
3. By De Morgan's laws for families ([Chapter 3](ch3_sets_for_probability_v2.md)), $\bigcap_n A_n = \big(\bigcup_n A_n^c\big)^c$. Each $A_n^c \in \mathcal F$, so the union is in $\mathcal F$, and so is its complement.
2. Extend $A_1, \ldots, A_n$ to a sequence by $A_k := \emptyset$ for $k > n$; its union is $\bigcup_{k=1}^n A_k$, which is therefore in $\mathcal F$. Extending by $A_k := \Omega$ instead, the intersection of the sequence is $\bigcap_{k=1}^n A_k$, which is in $\mathcal F$ by part 3.
4. $A \setminus B = A \cap B^c$ ([Chapter 3](ch3_sets_for_probability_v2.md), Rules for Complements), which is in $\mathcal F$ by part 2. $\blacksquare$
:::

**Examples.**

1. The power set $\mathcal P(\Omega)$ is a σ-algebra on $\Omega$, the largest one: all three conditions concern subsets of $\Omega$, and $\mathcal P(\Omega)$ contains them all.
2. $\{\emptyset, \Omega\}$ is a σ-algebra, the smallest one, since every σ-algebra contains $\Omega$ and $\emptyset$.
3. *A finite example.* For a die, $\mathcal F = \{\emptyset, \{1, 3, 5\}, \{2, 4, 6\}, \Omega\}$ is a σ-algebra. It contains $\Omega$, and the complement of each member is a member. For a sequence of members, the union is $\Omega$ if $\Omega$ occurs or both $\{1, 3, 5\}$ and $\{2, 4, 6\}$ occur; otherwise it is $\{1, 3, 5\}$ or $\{2, 4, 6\}$ if that set occurs; and otherwise every member of the sequence is $\emptyset$ and so is the union.

The third example describes **partial information**. If you are told only whether the die shows an even number, you can decide every event in $\mathcal F$ (did "odd" happen?) but not, say, $\{6\}$. In filtering, the information available at a given time is described in exactly this way.
  
### Generated σ-Algebras

We rarely list a σ-algebra member by member. Instead we name a few sets that must be events and take the smallest σ-algebra containing them. That this exists rests on the following lemma.

:::{important icon=false} 📐 **Lemma (Intersections of σ-Algebras)**
If $\mathfrak S$ is a nonempty set of σ-algebras on $\Omega$, then $\bigcap \mathfrak S$ is a σ-algebra on $\Omega$.
:::

:::{admonition icon=false} ✍️ **Proof**
Every member of $\bigcap \mathfrak S$ belongs to some $\mathcal F \in \mathfrak S$ and is therefore a subset of $\Omega$, so $\bigcap \mathfrak S \subseteq \mathcal P(\Omega)$. Each condition holds in every $\mathcal F \in \mathfrak S$, hence in the intersection: $\Omega \in \mathcal F$ for every $\mathcal F$; if $A$ lies in every $\mathcal F$, so does $A^c$; and if every $A_n$ lies in every $\mathcal F$, so does $\bigcup_n A_n$. $\blacksquare$
:::

Unions do not work: on $\Omega = \{1, 2, 3\}$, both $\{\emptyset, \{1\}, \{2, 3\}, \Omega\}$ and $\{\emptyset, \{2\}, \{1, 3\}, \Omega\}$ are σ-algebras, but their union contains $\{1\}$ and $\{2\}$ and not $\{1, 2\}$.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Generated sigma-algebra
: For a set $\Omega$ and a set $\mathcal G \subseteq \mathcal P(\Omega)$, the σ-algebra generated by $\mathcal G$ is
  $$\sigma(\mathcal G) := \bigcap \{\mathcal F \in \mathcal P(\mathcal P(\Omega)) : \mathcal F \text{ is a σ-algebra on } \Omega \text{ and } \mathcal G \subseteq \mathcal F\}.$$
:::
::::

:::{important icon=false} 📐 **Theorem (The Generated σ-Algebra Is the Smallest)**
$\sigma(\mathcal G)$ is a σ-algebra on $\Omega$, it contains $\mathcal G$, and $\sigma(\mathcal G) \subseteq \mathcal F$ for every σ-algebra $\mathcal F$ on $\Omega$ with $\mathcal G \subseteq \mathcal F$.
:::

:::{admonition icon=false} ✍️ **Proof**
Let $\mathfrak S$ be the set of σ-algebras on $\Omega$ that contain $\mathcal G$; it is a set by Separation. It is nonempty because $\mathcal P(\Omega) \in \mathfrak S$, so $\sigma(\mathcal G) = \bigcap \mathfrak S$ is defined (this is Chapter 2's proviso for $\bigcap$) and is a σ-algebra by the lemma. Each $G \in \mathcal G$ lies in every member of $\mathfrak S$, hence in $\bigcap \mathfrak S$. If $\mathcal F$ is a σ-algebra containing $\mathcal G$, then $\mathcal F \in \mathfrak S$, so $\bigcap \mathfrak S \subseteq \mathcal F$. $\blacksquare$
:::

The theorem gives a standard proof technique, sometimes called the **good-sets principle**: to show that every set in $\sigma(\mathcal G)$ has some property, show that the sets with the property form a σ-algebra containing $\mathcal G$. By the theorem, that σ-algebra contains $\sigma(\mathcal G)$.

**Example.** For a die and $\mathcal G = \{\{6\}\}$, we get $\sigma(\mathcal G) = \{\emptyset, \{6\}, \{1, 2, 3, 4, 5\}, \Omega\}$. This collection is a σ-algebra (as for the parity example) and contains $\{6\}$, and every σ-algebra containing $\{6\}$ contains its complement, $\emptyset$, and $\Omega$.

When $\Omega$ is countable and only finitely many generators are given, the generated σ-algebra can be described completely. Call two outcomes *indistinguishable by* $G_1, \ldots, G_m$ if each $G_i$ contains both or neither of them, and call the set of outcomes indistinguishable from $\omega$ the *atom* of $\omega$.

:::{important icon=false} 📐 **Theorem (Atoms)**
Let $\Omega$ be countable and $G_1, \ldots, G_m \subseteq \Omega$. The atoms form a {term}`partition` $\mathcal A$ of $\Omega$, and $\sigma(\{G_1, \ldots, G_m\})$ consists exactly of the unions $\bigcup \mathcal S$ of sets of atoms $\mathcal S \subseteq \mathcal A$.
:::

:::{admonition icon=false} ✍️ **Proof**
Write $\mathcal G := \{G_1, \ldots, G_m\}$ and let $a(\omega)$ be the atom of $\omega$.

*The atoms partition $\Omega$.* Indistinguishability is reflexive, symmetric, and transitive, because it says that $\omega$ and $\omega'$ have the same membership in every $G_i$. So $\omega \in a(\omega)$, and if $\omega'' \in a(\omega) \cap a(\omega')$, then $\omega$ and $\omega'$ are indistinguishable and $a(\omega) = a(\omega')$. Hence atoms are nonempty, cover $\Omega$, and distinct atoms are disjoint.

*Unions of atoms form a σ-algebra containing $\mathcal G$.* Let $\mathcal U := \{\bigcup \mathcal S : \mathcal S \subseteq \mathcal A\}$. It contains $\Omega = \bigcup \mathcal A$. Since every outcome lies in exactly one atom, $(\bigcup \mathcal S)^c = \bigcup (\mathcal A \setminus \mathcal S)$. A union of unions of atoms is the union of all the atoms involved. Each $G_i$ is the union of the atoms of its elements, because if $\omega \in G_i$ and $\omega'$ is indistinguishable from $\omega$, then $\omega' \in G_i$. So $\sigma(\mathcal G) \subseteq \mathcal U$.

*Unions of atoms lie in $\sigma(\mathcal G)$.* For each $i$ let $G_i^\omega := G_i$ if $\omega \in G_i$ and $G_i^\omega := G_i^c$ otherwise. Then $a(\omega) = \bigcap_{i=1}^m G_i^\omega$ (or $a(\omega) = \Omega$ if $m = 0$), a finite intersection of members of $\sigma(\mathcal G)$, so $a(\omega) \in \sigma(\mathcal G)$. The set $\mathcal A$ is the image of the countable set $\Omega$ under $\omega \mapsto a(\omega)$, so it is countable, and so is every $\mathcal S \subseteq \mathcal A$ ([Chapter 3](ch3_sets_for_probability_v2.md)). If $\mathcal S \neq \emptyset$, the Listing theorem writes $\mathcal S$ as the set of terms of a sequence, so $\bigcup \mathcal S$ is a countable union of members of $\sigma(\mathcal G)$; and $\bigcup \emptyset = \emptyset \in \sigma(\mathcal G)$. $\blacksquare$
:::

Distinct sets of atoms have distinct unions, because atoms are nonempty and disjoint. So if there are $k$ atoms, $\sigma(\mathcal G)$ has as many events as a $k$-element set has subsets, namely $2^k$ (see [Power set](https://en.wikipedia.org/wiki/Power_set)). The explorer below computes the atoms for a die and the events you choose to generate from. The atoms are exactly the pieces of information the generating events can reveal.

```{marimo} python
:hide-code: true

sigma_generators = {
    "even = {2, 4, 6}": frozenset({2, 4, 6}),
    "at most 3 = {1, 2, 3}": frozenset({1, 2, 3}),
    "prime = {2, 3, 5}": frozenset({2, 3, 5}),
    "six = {6}": frozenset({6}),
    "at least 5 = {5, 6}": frozenset({5, 6}),
}
sigma_select = mo.ui.multiselect(
    options=list(sigma_generators),
    value=["even = {2, 4, 6}"],
    label=r"Generating events $\mathcal G$",
)
```

```{marimo} python
:hide-code: true

_omega = [1, 2, 3, 4, 5, 6]
_gens = [sigma_generators[_name] for _name in sigma_select.value]
_atoms = []
for _w in _omega:
    _sig = tuple(_w in _g for _g in _gens)
    for _atom in _atoms:
        if tuple(_atom[0] in _g for _g in _gens) == _sig:
            _atom.append(_w)
            break
    else:
        _atoms.append([_w])
_k = len(_atoms)

_fig, _ax = plt.subplots(figsize=(7.5, 1.9))
for _i, _atom in enumerate(_atoms):
    for _w in _atom:
        _ax.add_patch(plt.Rectangle((_w - 0.45, -0.45), 0.9, 0.9, facecolor=f"C{_i}", alpha=0.85))
        _ax.text(_w, 0, str(_w), ha="center", va="center", fontsize=15, color="white", fontweight="bold")
_ax.set_xlim(0.4, 6.6)
_ax.set_ylim(-0.6, 0.6)
_ax.set_aspect("equal")
_ax.axis("off")
_ax.set_title(
    rf"Die faces colored by atom: {_k} atoms, so $\sigma(\mathcal{{G}})$ has $2^{{{_k}}} = {2 ** _k}$ events",
    style="italic",
)

def _set(_s):
    return r"\{" + ", ".join(str(_v) for _v in sorted(_s)) + r"\}" if _s else r"\emptyset"

_atom_text = ",\\ ".join(_set(_a) for _a in _atoms)
if _k <= 4:
    _events = []
    for _mask in range(2 ** _k):
        _events.append(sorted(_w for _j, _a in enumerate(_atoms) if _mask >> _j & 1 for _w in _a))
    _events.sort(key=lambda _e: (len(_e), _e))
    _event_text = "The events are $" + ",\\ ".join(_set(_e) for _e in _events) + "$."
else:
    _event_text = f"There are {2 ** _k} events, too many to list."
_summary = mo.md("Atoms: $" + _atom_text + "$. " + _event_text)
mo.vstack([sigma_select, graphic(_fig), _summary])
```

### The Borel σ-Algebra

For the scale noise, $\Omega = \mathbb R$, and the events we certainly want are the intervals, such as "the noise lies in $[-0.05, 0.05)$".

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Borel sigma-algebra
: The Borel σ-algebra on $\mathbb R$ is $\mathcal B(\mathbb R) := \sigma(\mathcal I)$, the {term}`σ-algebra generated by <generated sigma-algebra>` the set $\mathcal I$ of all {term}`intervals <interval>`. Its elements are called *Borel sets*. For a Borel set $\Omega_0 \subseteq \mathbb R$, the Borel σ-algebra on $\Omega_0$ is $\mathcal B(\Omega_0) := \{B \in \mathcal B(\mathbb R) : B \subseteq \Omega_0\}$.
:::
::::

The same σ-algebra is generated by the open subsets of $\mathbb R$, which is how many books define it ([Borel set](https://en.wikipedia.org/wiki/Borel_set)), and [Chapter 5](ch5_random_variables_v2.md) shows that the rays $(-\infty, b]$ alone already generate it.

:::{important icon=false} 📐 **Lemma (Borel Sets)**
1. Every interval, every singleton $\{x\}$, and every countable subset of $\mathbb R$ is a Borel set. In particular $\mathbb N$, $\mathbb Z$, $\mathbb Q$, and $\mathbb R \setminus \mathbb Q$ are Borel sets.
2. If $\Omega_0$ is a Borel set, then $\mathcal B(\Omega_0)$ is a σ-algebra on $\Omega_0$ containing every interval $I \subseteq \Omega_0$.
3. If $B$ is a Borel set and $t \in \mathbb R$, then $B + t := \{b + t : b \in B\}$ is a Borel set.
:::

:::{admonition icon=false} ✍️ **Proof**
1. Intervals lie in $\mathcal I \subseteq \mathcal B(\mathbb R)$, and $\{x\} = [x, x]$. A nonempty countable set $C$ is $\{c_n : n \in \mathbb N^+\}$ for some sequence (Listing theorem, [Chapter 3](ch3_sets_for_probability_v2.md)), so $C = \bigcup_{n=1}^\infty \{c_n\}$ is a countable union of Borel sets; and $\emptyset$ is in every σ-algebra. $\mathbb N$, $\mathbb Z$, and $\mathbb Q$ are countable, and $\mathbb R \setminus \mathbb Q$ is a complement.
2. $\Omega_0 \in \mathcal B(\Omega_0)$. If $B \in \mathcal B(\Omega_0)$, then $\Omega_0 \setminus B = \Omega_0 \cap (\mathbb R \setminus B)$ is a Borel set by the Closure Properties lemma, and it is a subset of $\Omega_0$. A countable union of members of $\mathcal B(\Omega_0)$ is a Borel subset of $\Omega_0$. Intervals contained in $\Omega_0$ are Borel sets by part 1.
3. We use the good-sets principle. Let $\mathcal A := \{B \subseteq \mathbb R : B + t \in \mathcal B(\mathbb R)\}$. Because $x \mapsto x + t$ is a bijection of $\mathbb R$ with inverse $x \mapsto x - t$, we have $\mathbb R + t = \mathbb R$, $(\mathbb R \setminus B) + t = \mathbb R \setminus (B + t)$, and $\big(\bigcup_n B_n\big) + t = \bigcup_n (B_n + t)$. So $\mathcal A$ is a σ-algebra. Translating an interval gives an interval of the same form, for example $[a, b] + t = [a + t, b + t]$, so $\mathcal I \subseteq \mathcal A$. Hence $\mathcal B(\mathbb R) = \sigma(\mathcal I) \subseteq \mathcal A$. $\blacksquare$
:::

Not every subset of $\mathbb R$ is a Borel set; we meet one below. But every set you are likely to write down is, so restricting events to Borel sets costs nothing in practice.
  
## Kolmogorov's Axioms

Kolmogorov proposed the following axioms in 1933, and they are the foundation of modern probability theory ([Probability axioms](https://en.wikipedia.org/wiki/Probability_axioms)).

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Probability measure
: Let $\mathcal F$ be a {term}`σ-algebra <sigma-algebra>` on a set $\Omega$. A probability measure on $(\Omega, \mathcal F)$ is a function $\mathbb P : \mathcal F \to \mathbb R$ satisfying *Kolmogorov's axioms*:

  1. *(nonnegativity)* $\mathbb P(A) \ge 0$ for every $A \in \mathcal F$;
  2. *(normalization)* $\mathbb P(\Omega) = 1$;
  3. *(countable additivity)* for every sequence $(A_n)_{n=1}^\infty$ of pairwise {term}`disjoint` events, $\mathbb P\big(\bigcup_{n=1}^\infty A_n\big) = \sum_{n=1}^\infty \mathbb P(A_n)$.
:::
::::

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Probability space
: A triple $(\Omega, \mathcal F, \mathbb P)$ in which $\Omega$ is a {term}`sample space`, $\mathcal F$ is a {term}`σ-algebra <sigma-algebra>` on $\Omega$, and $\mathbb P$ is a {term}`probability measure` on $(\Omega, \mathcal F)$. We read $\mathbb P(A)$ as "the probability of $A$".
:::
::::

Axiom 3 needs $\bigcup_n A_n$ to be an event, which is why events must be closed under countable unions. Its right side is the value in $[0, \infty]$ of a series of nonnegative terms ([Chapter 3](ch3_sets_for_probability_v2.md) and [Appendix C: Series](appendix_c_calculus_v2.md)); the axiom says in particular that this value is the real number $\mathbb P(\bigcup_n A_n)$.

The axioms say how probabilities combine, not what they mean. Whether $\mathbb P(A)$ is read as a long-run frequency or as a degree of belief, the same rules apply. The experiment at the end of this chapter compares probabilities with frequencies, and [Chapter 6](ch6_expectation_and_variance_v2.md) proves the connection.
  
## Discrete Probability Spaces

**Coin toss.** Let $\Omega = \{H, T\}$ and $\mathcal F = \mathcal P(\Omega) = \{\emptyset, \{H\}, \{T\}, \Omega\}$. Choose a number $p \in [0, 1]$, the probability of heads, and set
$$\mathbb P(\emptyset) = 0, \qquad \mathbb P(\{H\}) = p, \qquad \mathbb P(\{T\}) = 1 - p, \qquad \mathbb P(\Omega) = 1.$$
A fair coin has $p = \tfrac12$, but the axioms allow any $p$. Axioms 1 and 2 clearly hold. Checking axiom 3 by hand means considering every sequence of pairwise disjoint subsets of $\{H, T\}$; the next theorem does this once for all models of this kind. It uses the *indicator* of a set $A \subseteq \Omega$, the function $\mathbf 1_A : \Omega \to \{0, 1\}$ with $\mathbf 1_A(\omega) := 1$ if $\omega \in A$ and $\mathbf 1_A(\omega) := 0$ otherwise.

:::{important icon=false} 📐 **Theorem (Discrete Probability Measures)**
Let $\Omega$ be a nonempty set, $(\omega_n)_{n=1}^\infty$ a sequence in $\Omega$, and $(p_n)_{n=1}^\infty$ a sequence of nonnegative real numbers with $\sum_{n=1}^\infty p_n = 1$. Then
$$\mathbb P(A) := \sum_{n=1}^\infty p_n \mathbf 1_A(\omega_n) \qquad (A \subseteq \Omega)$$
defines a probability measure on $(\Omega, \mathcal P(\Omega))$.
:::

:::{admonition icon=false} ✍️ **Proof**
Since $0 \le p_n \mathbf 1_A(\omega_n) \le p_n$, comparison of nonnegative series gives $0 \le \mathbb P(A) \le \sum_n p_n = 1$, so $\mathbb P(A)$ is a real number, and $\mathbb P(\Omega) = \sum_n p_n = 1$. For countable additivity, let $(A_k)_{k=1}^\infty$ be pairwise disjoint with union $A$, and fix $n$. If $\omega_n \notin A$, every term of $\sum_k p_n \mathbf 1_{A_k}(\omega_n)$ is $0$. If $\omega_n \in A$, then $\omega_n$ lies in exactly one $A_k$, so exactly one term equals $p_n$ and the others are $0$. Either way $\sum_{k=1}^\infty p_n \mathbf 1_{A_k}(\omega_n) = p_n \mathbf 1_A(\omega_n)$. Therefore
$$\mathbb P(A) = \sum_{n=1}^\infty \sum_{k=1}^\infty p_n \mathbf 1_{A_k}(\omega_n) = \sum_{k=1}^\infty \sum_{n=1}^\infty p_n \mathbf 1_{A_k}(\omega_n) = \sum_{k=1}^\infty \mathbb P(A_k).$$
The order of summation may be exchanged because the terms are nonnegative: by Nonnegative Sums in Any Order ([Appendix C: Series](appendix_c_calculus_v2.md)), both iterated sums equal the sum of the family $\big(p_n \mathbf 1_{A_k}(\omega_n)\big)_{(n, k) \in \mathbb N^+ \times \mathbb N^+}$, grouped by $n$ in one case and by $k$ in the other. $\blacksquare$
:::

Think of $p_n$ as a mass placed at the outcome $\omega_n$; then $\mathbb P(A)$ is the total mass inside $A$. Repetitions in the sequence $(\omega_n)$ are allowed, and their masses add up.

- *Coin.* Take $\omega_1 := H$, $\omega_2 := T$, $p_1 := p$, $p_2 := 1 - p$, and $p_n := 0$, $\omega_n := H$ for $n \ge 3$. This gives exactly the four probabilities above.
- *Die.* Take $\omega_n := n$ and $p_n := \tfrac16$ for $n \le 6$, and $p_n := 0$, $\omega_n := 1$ for $n > 6$. Then $\mathbb P(A) = \sum_{n=1}^6 \tfrac16 \mathbf 1_A(n)$ is one sixth of the number of outcomes in $A$; for example $\mathbb P(\{2, 4, 6\}) = \tfrac12$.

Conversely, every probability measure on $(\Omega, \mathcal P(\Omega))$ with $\Omega$ countable arises this way. By Chapter 3, $\Omega$ is finite or countably infinite, so it can be listed without repetition as $\omega_1, \omega_2, \ldots$ (for a finite $\Omega$, pad the list with $p_n := 0$). Set $p_n := \mathbb P(\{\omega_n\})$. For $A \subseteq \Omega$, the sets $\{\omega_n\} \cap A$ (and $\emptyset$ beyond the end of a finite list) are pairwise disjoint with union $A$, so countable additivity gives $\mathbb P(A) = \sum_n p_n \mathbf 1_A(\omega_n)$. A probability space of this kind, with $\Omega$ countable and $\mathcal F = \mathcal P(\Omega)$, is called *discrete*.
  
### A Random Rational Number

Now let $\Omega := \mathbb Q \cap [0, 1]$. It is countable, as a subset of $\mathbb Q$, and infinite, since it contains the distinct numbers $1, \tfrac12, \tfrac13, \ldots$; so it is countably infinite ([Chapter 3](ch3_sets_for_probability_v2.md)). Can we choose a rational number in $[0, 1]$ with every rational equally likely?

:::{important icon=false} 📐 **Theorem (No Uniform Probability on a Countably Infinite Set)**
Let $\Omega$ be countably infinite and $\mathcal F$ a σ-algebra on $\Omega$ that contains every singleton. No probability measure on $(\Omega, \mathcal F)$ gives all singletons the same probability.
:::

:::{admonition icon=false} ✍️ **Proof**
Suppose $\mathbb P(\{\omega\}) = c$ for every $\omega \in \Omega$. Let $e : \mathbb N^+ \to \Omega$ be a bijection. The singletons $\{e(n)\}$ are pairwise disjoint because $e$ is injective, and their union is $\Omega$ because $e$ is surjective. By countable additivity,
$$1 = \mathbb P(\Omega) = \sum_{n=1}^\infty c.$$
If $c = 0$ the sum is $0$, and if $c > 0$ it is $\infty$ ([Chapter 3](ch3_sets_for_probability_v2.md), Extended Real Numbers). Neither equals $1$. $\blacksquare$
:::

In particular, there is no "uniformly random natural number". Countable additivity forbids spreading probability evenly over countably many points, and the same two-case argument will defeat the Vitali set below.

We can still choose a rational number at random if we give up "equally likely". List $\Omega$ by increasing denominator, in lowest terms:
$$q_1 = 0,\ q_2 = 1,\ q_3 = \tfrac12,\ q_4 = \tfrac13,\ q_5 = \tfrac23,\ q_6 = \tfrac14,\ q_7 = \tfrac34,\ \ldots$$
This lists every element of $\Omega$ exactly once. With $p_n := 2^{-n}$ and $\sum_{n=1}^\infty 2^{-n} = 1$ (geometric series, [Appendix C: Series](appendix_c_calculus_v2.md)), the Discrete Probability Measures theorem gives a probability measure with $\mathbb P(\{0\}) = \tfrac12$, $\mathbb P(\{1\}) = \tfrac14$, $\mathbb P(\{\tfrac12\}) = \tfrac18$, and so on. The model depends entirely on the chosen listing, so there is no canonical "random rational".
  
## Consequences of the Axioms

Everything below follows from Kolmogorov's three axioms. Throughout, $(\Omega, \mathcal F, \mathbb P)$ is a probability space and all sets are events.

:::{important icon=false} 📐 **Lemma (Probability of the Empty Set)**
$\mathbb P(\emptyset) = 0$.
:::

:::{admonition icon=false} ✍️ **Proof**
Let $c := \mathbb P(\emptyset)$, a real number $\ge 0$. The constant sequence $A_n := \emptyset$ is pairwise disjoint (as $\emptyset \cap \emptyset = \emptyset$) with union $\emptyset$, so countable additivity gives $c = \sum_{n=1}^\infty c$. If $c > 0$, the right side is $\infty$, which is not a real number. So $c = 0$. $\blacksquare$
:::

:::{important icon=false} 📐 **Theorem (Finite Additivity)**
If $A_1, \ldots, A_n$ are pairwise disjoint events, then $\mathbb P\big(\bigcup_{k=1}^n A_k\big) = \sum_{k=1}^n \mathbb P(A_k)$.
:::

:::{admonition icon=false} ✍️ **Proof**
Extend the list by $A_k := \emptyset$ for $k > n$. The sequence is still pairwise disjoint and has the same union, so $\mathbb P\big(\bigcup_{k=1}^n A_k\big) = \sum_{k=1}^\infty \mathbb P(A_k)$. The terms with $k > n$ are $0$, so the partial sums are constant from the $n$-th on, and the series equals $\sum_{k=1}^n \mathbb P(A_k)$. $\blacksquare$
:::

:::{important icon=false} 📐 **Corollary (Complement Rule)**
$\mathbb P(A^c) = 1 - \mathbb P(A)$.
:::

:::{admonition icon=false} ✍️ **Proof**
$A$ and $A^c$ are disjoint with union $\Omega$, so $\mathbb P(A) + \mathbb P(A^c) = \mathbb P(\Omega) = 1$. $\blacksquare$
:::

:::{important icon=false} 📐 **Theorem (Monotonicity)**
If $A \subseteq B$, then $\mathbb P(B \setminus A) = \mathbb P(B) - \mathbb P(A)$ and $\mathbb P(A) \le \mathbb P(B)$. In particular, $0 \le \mathbb P(A) \le 1$ for every event $A$, and $\mathbb P(A \setminus B) = \mathbb P(A) - \mathbb P(A \cap B)$ for all events $A, B$.
:::

:::{admonition icon=false} ✍️ **Proof**
If $A \subseteq B$, then $B$ is the disjoint union of $A$ and $B \setminus A$, so $\mathbb P(B) = \mathbb P(A) + \mathbb P(B \setminus A)$. Subtracting the real number $\mathbb P(A)$ gives the first formula, and $\mathbb P(B \setminus A) \ge 0$ gives $\mathbb P(A) \le \mathbb P(B)$. Taking $B = \Omega$ gives $\mathbb P(A) \le 1$. Finally, $A \setminus B = A \setminus (A \cap B)$ and $A \cap B \subseteq A$. $\blacksquare$
:::

:::{important icon=false} 📐 **Theorem (Inclusion–Exclusion for Two Events)**
$\mathbb P(A \cup B) = \mathbb P(A) + \mathbb P(B) - \mathbb P(A \cap B)$.
:::

:::{admonition icon=false} ✍️ **Proof**
$A \cup B$ is the disjoint union of $A$ and $B \setminus A$, and $B \setminus A = B \setminus (A \cap B)$. So $\mathbb P(A \cup B) = \mathbb P(A) + \mathbb P(B \setminus A) = \mathbb P(A) + \mathbb P(B) - \mathbb P(A \cap B)$ by Monotonicity. $\blacksquare$
:::

In words, adding $\mathbb P(A)$ and $\mathbb P(B)$ counts the overlap twice, so we subtract it once.
  
:::{important icon=false} 📐 **Theorem (Union Bound)**
For every sequence $(A_n)_{n=1}^\infty$ of events, $\mathbb P\big(\bigcup_{n=1}^\infty A_n\big) \le \sum_{n=1}^\infty \mathbb P(A_n)$. For finitely many events, $\mathbb P\big(\bigcup_{k=1}^n A_k\big) \le \sum_{k=1}^n \mathbb P(A_k)$.
:::

:::{admonition icon=false} ✍️ **Proof**
Let $D_n := A_n \setminus \bigcup_{k=1}^{n-1} A_k$. These are events (Closure Properties), and by the Disjointification lemma ([Chapter 3](ch3_sets_for_probability_v2.md)) they are pairwise disjoint, with $D_n \subseteq A_n$ and $\bigcup_n D_n = \bigcup_n A_n$. By countable additivity and Monotonicity,
$$\mathbb P\Big(\bigcup_{n=1}^\infty A_n\Big) = \sum_{n=1}^\infty \mathbb P(D_n) \le \sum_{n=1}^\infty \mathbb P(A_n),$$
where the inequality compares two series of nonnegative terms term by term. For finitely many events, extend the list by $\emptyset$. $\blacksquare$
:::

The union bound needs no assumptions about how the events are related. For example, if each of $30$ scale readings has probability $0.01$ of being an outlier, then the probability that at least one of them is an outlier is at most $0.3$, however the outliers depend on each other.

The next two theorems are where countable additivity earns its place. They connect probabilities with limits ([Appendix C: Sequences and Limits](appendix_c_calculus_v2.md)).

:::{important icon=false} 📐 **Theorem (Continuity from Below)**
If $A_1 \subseteq A_2 \subseteq \cdots$ are events, then $\mathbb P\big(\bigcup_{n=1}^\infty A_n\big) = \lim_{n \to \infty} \mathbb P(A_n)$.
:::

:::{admonition icon=false} ✍️ **Proof**
Let $A := \bigcup_n A_n$. By the Disjointification lemma, $D_1 := A_1$ and $D_n := A_n \setminus A_{n-1}$ for $n \ge 2$ are pairwise disjoint events with $\bigcup_{k=1}^N D_k = A_N$ and $\bigcup_n D_n = A$. By countable and finite additivity,
$$\mathbb P(A) = \sum_{k=1}^\infty \mathbb P(D_k), \qquad \sum_{k=1}^N \mathbb P(D_k) = \mathbb P(A_N).$$
So the numbers $\mathbb P(A_N)$ are the partial sums of a series of nonnegative terms whose value is $\mathbb P(A) \le 1$. They are nondecreasing and bounded, so by Monotone Convergence they converge to their supremum, which is the value of the series, $\mathbb P(A)$. $\blacksquare$
:::

:::{important icon=false} 📐 **Theorem (Continuity from Above)**
If $A_1 \supseteq A_2 \supseteq \cdots$ are events, then $\mathbb P\big(\bigcap_{n=1}^\infty A_n\big) = \lim_{n \to \infty} \mathbb P(A_n)$.
:::

:::{admonition icon=false} ✍️ **Proof**
The complements increase, $A_1^c \subseteq A_2^c \subseteq \cdots$ (Rules for Complements), and $\bigcap_n A_n = \big(\bigcup_n A_n^c\big)^c$ (De Morgan's laws). By the Complement Rule, Continuity from Below, and the limit laws,
$$\mathbb P\Big(\bigcap_{n=1}^\infty A_n\Big) = 1 - \mathbb P\Big(\bigcup_{n=1}^\infty A_n^c\Big) = 1 - \lim_{n \to \infty} \big(1 - \mathbb P(A_n)\big) = \lim_{n \to \infty} \mathbb P(A_n). \qquad \blacksquare$$
:::

Conversely, a function on $\mathcal F$ that is finitely additive and continuous from below is countably additive: for pairwise disjoint $A_n$, the events $B_N := \bigcup_{n=1}^N A_n$ increase to $\bigcup_n A_n$, so $\mathbb P\big(\bigcup_n A_n\big) = \lim_N \mathbb P(B_N) = \lim_N \sum_{n=1}^N \mathbb P(A_n) = \sum_{n=1}^\infty \mathbb P(A_n)$.

:::{attention icon=false} 🗝️ **Key Idea**
Countable additivity is exactly what makes probability compatible with limits: given finite additivity, it is equivalent to continuity from below. The limit arguments about probabilities in later chapters, starting with the properties of distribution functions in [Chapter 5](ch5_random_variables_v2.md), rest on it.
:::

:::{caution icon=false} ⚠️ **Assumptions and Failure Modes**
- **Finite values.** Monotonicity, inclusion–exclusion, and continuity from above subtract probabilities, which works because $\mathbb P$ takes real values. For the *length* of subsets of $\mathbb R$ (below), which can be $\infty$, continuity from above fails: the intervals $[n, \infty)$ decrease to $\emptyset$, yet each has infinite length.
- **Finite additivity is not enough.** The *natural density* of $A \subseteq \mathbb N^+$, $d(A) := \lim_{n \to \infty} |A \cap \{1, \ldots, n\}| / n$ when the limit exists ([Natural density](https://en.wikipedia.org/wiki/Natural_density)), treats all natural numbers alike: $d(\mathbb N^+) = 1$, the even numbers have density $\tfrac12$, and every finite set has density $0$. It is additive for two disjoint sets whose densities exist. But the finite sets $\{1, \ldots, n\}$ increase to $\mathbb N^+$ while their densities stay $0$, so it is not continuous from below and is not a probability measure. This is the closest one can get to a "uniformly random natural number".
:::
  
## Why Not Every Subset Can Be an Event

For a die, every subset of $\Omega$ is an event. For a number chosen "uniformly at random" from $[0, 1)$ we would like the same, together with two further wishes: an interval $[a, b)$ should have probability $b - a$, and moving a set around without changing its shape should not change its probability. This section shows that the first wish contradicts the last one, even without the second. The culprit is a set whose existence the Axiom of Choice guarantees.

**Rotations of $[0, 1)$.** For $x, r \in [0, 1)$ let
$$x \oplus r := \begin{cases} x + r & \text{if } x + r < 1, \\ x + r - 1 & \text{if } x + r \ge 1, \end{cases}$$
so that $x \oplus r \in [0, 1)$. If we bend $[0, 1)$ into a circle of circumference $1$, then $\oplus\, r$ rotates the circle by $r$. For $A \subseteq [0, 1)$ let $A \oplus r := \{a \oplus r : a \in A\}$. For instance, $[0.5, 0.9) \oplus 0.3 = [0.8, 1) \cup [0, 0.2)$, still of total length $0.4$. Given a σ-algebra $\mathcal F$ on $[0, 1)$, a probability measure $\mu$ on $([0, 1), \mathcal F)$ is *rotation invariant* if $A \oplus r \in \mathcal F$ and $\mu(A \oplus r) = \mu(A)$ for every $A \in \mathcal F$ and every rational $r \in [0, 1)$.

**Vitali sets.** For $x \in [0, 1)$ let $E_x := \{y \in [0, 1) : y - x \in \mathbb Q\}$, the numbers in $[0, 1)$ that differ from $x$ by a rational number.

:::{important icon=false} 📐 **Lemma (Rational Classes)**
$\{E_x : x \in [0, 1)\}$ is a {term}`partition` of $[0, 1)$.
:::

:::{admonition icon=false} ✍️ **Proof**
The set exists by Replacement. Since $x - x = 0 \in \mathbb Q$, we have $x \in E_x$, so the sets $E_x$ are nonempty and cover $[0, 1)$. Suppose $z \in E_x \cap E_y$. Then $z - x$ and $z - y$ are rational, hence so is $y - x = (z - x) - (z - y)$. For any $w \in E_y$, $w - x = (w - y) + (y - x)$ is rational, so $E_y \subseteq E_x$; by symmetry $E_x = E_y$. So two of the sets are either equal or disjoint. $\blacksquare$
:::

The sets $E_x$ are nonempty and pairwise disjoint, so the Axiom of Choice ([Chapter 2](ch2_axioms_of_set_theory_v2.md)) gives a set $C$ containing exactly one element of each $E_x$. Then $V := C \cap [0, 1)$ contains exactly one element of each $E_x$ and nothing else. Any such set is called a *Vitali set*, after Giuseppe Vitali, who introduced it in 1905 ([Vitali set](https://en.wikipedia.org/wiki/Vitali_set)). Choice asserts that $V$ exists but gives no rule for which element of each $E_x$ to take.

:::{important icon=false} 📐 **Theorem (Vitali)**
Let $\mathcal F$ be a σ-algebra on $[0, 1)$ and $\mu$ a rotation-invariant probability measure on $([0, 1), \mathcal F)$. Then no Vitali set belongs to $\mathcal F$. In particular, there is no rotation-invariant probability measure on $([0, 1), \mathcal P([0, 1)))$.
:::

:::{admonition icon=false} ✍️ **Proof**
Suppose a Vitali set $V$ belongs to $\mathcal F$. Let $R := \mathbb Q \cap [0, 1)$ and, for $r \in R$, let $V_r := V \oplus r$. By rotation invariance, $V_r \in \mathcal F$ and $\mu(V_r) = \mu(V) =: c$.

*Step 1: the sets $V_r$ ($r \in R$) are pairwise disjoint.* Let $z \in V_r \cap V_s$, so $z = v \oplus r = w \oplus s$ with $v, w \in V$. By the definition of $\oplus$, $z = v + r - i = w + s - j$ with $i, j \in \{0, 1\}$. Then $v - w = (s - r) + (i - j)$ is rational, so $v$ and $w$ lie in the same set $E_w$. Since $V$ contains only one element of $E_w$, $v = w$. Then $r - s = i - j$ is an integer, and $-1 < r - s < 1$ because $r, s \in [0, 1)$, so $r = s$.

*Step 2: $\bigcup_{r \in R} V_r = [0, 1)$.* Each $V_r \subseteq [0, 1)$. Conversely, let $x \in [0, 1)$. $V$ contains an element $v$ of $E_x$, so $q := x - v$ is rational, with $-1 < q < 1$. If $q \ge 0$, let $r := q$; then $v + r = x < 1$, so $v \oplus r = x$. If $q < 0$, let $r := q + 1 \in (0, 1)$; then $v + r = x + 1 \ge 1$, so $v \oplus r = x$. Either way $r \in R$ and $x \in V_r$.

*Step 3: contradiction.* If $c = 0$: $R$ is countable (a subset of $\mathbb Q$) and nonempty, so $R = \{r_n : n \in \mathbb N^+\}$ for some sequence (Listing theorem). By Step 2 and the Union Bound,
$$1 = \mu([0, 1)) \le \sum_{n=1}^\infty \mu(V_{r_n}) = \sum_{n=1}^\infty 0 = 0.$$
If $c > 0$: the numbers $s_n := \tfrac{1}{n+1}$ ($n \in \mathbb N^+$) are distinct elements of $R$, so by Step 1 the events $V_{s_n}$ are pairwise disjoint. By countable additivity and Monotonicity,
$$1 \ge \mu\Big(\bigcup_{n=1}^\infty V_{s_n}\Big) = \sum_{n=1}^\infty c = \infty.$$
Both cases are impossible, so $V \notin \mathcal F$. If $\mathcal F = \mathcal P([0, 1))$, then $V \in \mathcal F$, so no such $\mu$ exists. $\blacksquare$
:::

:::{caution icon=false} ⚠️ **Assumptions and Failure Modes**
Each hypothesis is needed; dropping any one removes the contradiction.

- **The Axiom of Choice** is used only to produce $V$. Without it the theorem cannot be proven: Solovay showed in 1970 that, if the existence of an inaccessible cardinal (a large-cardinal axiom) is consistent with the axioms of set theory, then so is the following: the other axioms, plus a weak form of Choice, plus "every subset of $\mathbb R$ is Lebesgue measurable", so that length extends to all subsets ([Solovay model](https://en.wikipedia.org/wiki/Solovay_model)). This book keeps Choice, as nearly all of mathematics does, and accepts the consequence.
- **Countable additivity** is used in both cases of Step 3, which add up infinitely many rotated copies of $V$. With finite additivity alone the argument fails, and rotation-invariant, finitely additive "probabilities" defined on *all* subsets of the circle do exist; this goes back to Banach's 1923 work on the measure problem (see [Banach–Tarski paradox](https://en.wikipedia.org/wiki/Banach%E2%80%93Tarski_paradox) for the context).
- **Rotation invariance** is what gives every $V_r$ the same probability. Without it, probabilities on all subsets are easy: the point mass $\mu(A) := \mathbf 1_A(0)$ is a probability measure on $\mathcal P([0, 1))$. It is just not "uniform".
- **All subsets.** The proof only needs $V \in \mathcal F$. Below, Lebesgue measure provides a rotation-invariant probability on the Borel sets, so by the theorem Vitali sets are not Borel sets.
:::

:::{attention icon=false} 🗝️ **Key Idea**
We cannot have all three of: every subset of $[0, 1)$ is an event, countable additivity, and rotation invariance. Probability theory keeps countable additivity and rotation invariance and gives up the first: the events form a σ-algebra smaller than $\mathcal P(\Omega)$.
:::
  
## Lebesgue Measure

Giving up the non-Borel sets is enough: on the Borel sets, length works. To state this for all of $\mathbb R$, which has infinite length, we need a slightly more general notion than a probability measure. A *measure* on a measurable space $(\Omega, \mathcal F)$ is a function $\mu : \mathcal F \to [0, \infty]$ with $\mu(\emptyset) = 0$ that is countably additive, $\mu\big(\bigcup_n A_n\big) = \sum_n \mu(A_n)$ for pairwise disjoint $A_n \in \mathcal F$. A probability measure is exactly a measure with $\mu(\Omega) = 1$: such a $\mu$ takes real values, because $\mu(A) + \mu(A^c) = 1$, and conversely a probability measure has $\mathbb P(\emptyset) = 0$. The proofs of Finite Additivity, of the inequality $\mathbb P(A) \le \mathbb P(B)$ for $A \subseteq B$ (from $\mathbb P(B) = \mathbb P(A) + \mathbb P(B \setminus A)$), and of the Union Bound never subtract, so they hold for every measure.

:::{important icon=false} 📐 **Theorem (Lebesgue Measure)**
There is exactly one measure $\lambda$ on $(\mathbb R, \mathcal B(\mathbb R))$ with $\lambda([a, b]) = b - a$ for all real $a \le b$, called *Lebesgue measure*. It is translation invariant: $\lambda(B + t) = \lambda(B)$ for every Borel set $B$ and every $t \in \mathbb R$.
:::

:::{admonition icon=false} ✍️ **Proof**
Existence and uniqueness are not proven here. Carathéodory's extension theorem extends the length of intervals to a measure on a σ-algebra that contains $\mathcal B(\mathbb R)$. Its uniqueness statement, which applies because $\mathbb R$ is a countable union of intervals $[-n, n]$ of finite length, shows that no other measure on $\mathcal B(\mathbb R)$ gives every interval $[a, b]$ the length $b - a$ ([Lebesgue measure](https://en.wikipedia.org/wiki/Lebesgue_measure); [Carathéodory's extension theorem](https://en.wikipedia.org/wiki/Carath%C3%A9odory%27s_extension_theorem)).

Translation invariance follows from uniqueness. Fix $t$ and let $\mu(B) := \lambda(B + t)$ for $B \in \mathcal B(\mathbb R)$, which is defined by the Borel Sets lemma. Then $\mu(\emptyset) = 0$, and $\mu$ is countably additive because translating pairwise disjoint sets gives pairwise disjoint sets and $\big(\bigcup_n B_n\big) + t = \bigcup_n (B_n + t)$. Also $\mu([a, b]) = \lambda([a + t, b + t]) = b - a$. By uniqueness, $\mu = \lambda$. $\blacksquare$
:::

Restricting $\lambda$ to the Borel subsets of $[0, 1]$ gives a probability measure on $([0, 1], \mathcal B([0, 1]))$: it is countably additive because $\lambda$ is, and $\lambda([0, 1]) = 1$. It is also called **Lebesgue measure on $[0, 1]$** and also written $\lambda$. The probability space $([0, 1], \mathcal B([0, 1]), \lambda)$ models a number chosen uniformly at random from $[0, 1]$: probabilities of intervals are their lengths. This is the uniform distribution of [Chapter 5](ch5_random_variables_v2.md).

:::{important icon=false} 📐 **Theorem (A Uniformly Random Number)**
In the probability space $([0, 1], \mathcal B([0, 1]), \lambda)$:

1. $\lambda(\{x\}) = 0$ for every $x \in [0, 1]$;
2. for $0 \le a \le b \le 1$, each of $[a, b]$, $[a, b)$, $(a, b]$, $(a, b)$ has probability $b - a$;
3. every countable $C \subseteq [0, 1]$ has $\lambda(C) = 0$. In particular $\lambda(\mathbb Q \cap [0, 1]) = 0$ and $\lambda([0, 1] \setminus \mathbb Q) = 1$.
:::

:::{admonition icon=false} ✍️ **Proof**
1. $\lambda(\{x\}) = \lambda([x, x]) = x - x = 0$.
2. For example $[a, b) = [a, b] \setminus \{b\}$, so by Monotonicity $\lambda([a, b)) = (b - a) - 0$. The other cases are the same.
3. If $C \neq \emptyset$, write $C = \{c_n : n \in \mathbb N^+\}$ (Listing theorem). By the Union Bound, $\lambda(C) \le \sum_n \lambda(\{c_n\}) = 0$. The last statement follows from the Complement Rule. $\blacksquare$
:::

Part 1 also follows from Continuity from Above: the intervals $[x, x + \tfrac1n] \cap [0, 1]$ decrease to $\{x\}$ (any $y > x$ is excluded once $\tfrac1n < y - x$, by the Archimedean property), and their probabilities are at most $\tfrac1n$, which tends to $0$.

Compare with the random rational. There, countable additivity forced unequal weights on the points. Here every point has probability $0$, yet $\lambda([0, 1]) = 1$. There is no contradiction, because $[0, 1]$ is uncountable ([Chapter 3](ch3_sets_for_probability_v2.md)): it is not the set of terms of any sequence, so countable additivity never adds up the zeros.

:::{important icon=false} 📐 **Corollary (Vitali Sets Are Not Borel Sets)**
No Vitali set is a Borel set. Consequently, Lebesgue measure on $[0, 1)$ cannot be extended to a rotation-invariant probability measure on all subsets of $[0, 1)$.
:::

:::{admonition icon=false} ✍️ **Proof**
Let $\mathcal F := \mathcal B([0, 1))$ and let $\mu$ be the restriction of $\lambda$ to $\mathcal F$, a probability measure because $\lambda([0, 1)) = \lambda([0, 1]) - \lambda(\{1\}) = 1$. We show that $\mu$ is rotation invariant. Let $A \in \mathcal F$ and $r \in [0, 1)$, and split $A$ into $A_1 := A \cap [0, 1 - r)$ and $A_2 := A \cap [1 - r, 1)$. Elements of $A_1$ satisfy $x \oplus r = x + r$, and elements of $A_2$ satisfy $x \oplus r = x + r - 1$, so
$$A \oplus r = (A_1 + r) \cup (A_2 + r - 1).$$
Both pieces are Borel sets (Borel Sets lemma), and they lie in $[r, 1)$ and $[0, r)$ respectively, so they are disjoint subsets of $[0, 1)$. Hence $A \oplus r \in \mathcal F$ and, by Finite Additivity and translation invariance,
$$\mu(A \oplus r) = \lambda(A_1 + r) + \lambda(A_2 + r - 1) = \lambda(A_1) + \lambda(A_2) = \mu(A).$$
By Vitali's theorem, no Vitali set $V$ is in $\mathcal B([0, 1))$, and since $V \subseteq [0, 1)$, $V$ is not a Borel set at all. The second statement is Vitali's theorem applied to such an extension. $\blacksquare$
:::

**Back to the scale.** As a toy model, suppose the noise $\omega$ of a reading is uniformly distributed on $[-0.5, 0.5]$: take $\Omega := [-0.5, 0.5]$, $\mathcal F := \mathcal B(\Omega)$, and $\mathbb P := \lambda$ restricted to $\mathcal F$, a probability measure because $\lambda(\Omega) = 1$. Then
$$\mathbb P(\text{display shows } 155.0) = \lambda([-0.05, 0.05)) = 0.1, \qquad \mathbb P(\text{noise is exactly } 0.03) = \lambda(\{0.03\}) = 0.$$
Real scale noise is closer to normal than to uniform. [Chapter 5](ch5_random_variables_v2.md) builds such models from densities, and also shows that the rounding error of a display is well modeled as uniform.
  
## Almost Surely

A uniformly random number in $[0, 1]$ is irrational with probability $1$. Yet the rational outcomes are in $\Omega$, and nothing in the model prevents them. Probability $1$ is not the same as certainty, and probability $0$ is not the same as impossibility.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Almost surely
: A statement about the outcomes of a {term}`probability space` $(\Omega, \mathcal F, \mathbb P)$ holds almost surely (abbreviated *a.s.*) if there is an {term}`event` $A$ with $\mathbb P(A) = 1$ such that the statement holds for every outcome $\omega \in A$.
:::
::::

An event of probability $0$ is called a *null event*. So a statement holds almost surely if and only if the outcomes where it fails are contained in a null event (take complements). If the set $S$ of outcomes where the statement holds is itself an event, "almost surely" simply means $\mathbb P(S) = 1$: if $A \subseteq S$ and $\mathbb P(A) = 1$, then $1 = \mathbb P(A) \le \mathbb P(S) \le 1$ by Monotonicity.

**Examples.** For a uniformly random number $\omega \in [0, 1]$, "$\omega$ is irrational" and "$\omega \neq \tfrac12$" hold almost surely, although $\omega = \tfrac12$ is a possible outcome. For a coin with $p = \tfrac12$, "the coin shows heads" does not hold almost surely.

:::{important icon=false} 📐 **Lemma (Countably Many Almost Sure Statements)**
If each statement in a sequence of statements holds almost surely, then almost surely all of them hold simultaneously.
:::

:::{admonition icon=false} ✍️ **Proof**
Let $A_n$ be an event with $\mathbb P(A_n) = 1$ on which the $n$-th statement holds. All statements hold on $\bigcap_n A_n$, and by De Morgan's laws, the Complement Rule, and the Union Bound,
$$\mathbb P\Big(\bigcap_{n=1}^\infty A_n\Big) = 1 - \mathbb P\Big(\bigcup_{n=1}^\infty A_n^c\Big) \ge 1 - \sum_{n=1}^\infty \mathbb P(A_n^c) = 1 - 0 = 1. \qquad \blacksquare$$
:::

The lemma fails for uncountably many statements: for a uniformly random $\omega$, each statement "$\omega \neq x$" ($x \in [0, 1]$) holds almost surely, but together they say that $\omega$ is no number at all. Convergence results about random quantities, including some about filters, are usually stated "almost surely": they may fail on a null event of outcomes.
  
## Conditional Probability

Suppose a fair die is rolled and we learn that the result is even. Outcomes outside $\{2, 4, 6\}$ are ruled out, and the remaining outcomes keep their relative weights, rescaled so that they add up to $1$: each of $2, 4, 6$ now has probability $\tfrac{1/6}{1/2} = \tfrac13$.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Conditional probability
: Let $(\Omega, \mathcal F, \mathbb P)$ be a {term}`probability space` and $B$ an {term}`event` with $\mathbb P(B) > 0$. The conditional probability of an event $A$ given $B$ is
  $$\mathbb P(A \mid B) := \frac{\mathbb P(A \cap B)}{\mathbb P(B)}.$$
:::
::::

:::{important icon=false} 📐 **Theorem (Conditioning Gives a Probability Measure)**
If $\mathbb P(B) > 0$, then $A \mapsto \mathbb P(A \mid B)$ is a probability measure on $(\Omega, \mathcal F)$, and $\mathbb P(B \mid B) = 1$.
:::

:::{admonition icon=false} ✍️ **Proof**
Nonnegativity is clear, and $\mathbb P(\Omega \mid B) = \mathbb P(B)/\mathbb P(B) = 1 = \mathbb P(B \mid B)$. If $(A_n)$ are pairwise disjoint, so are the events $A_n \cap B$, and their union is $\big(\bigcup_n A_n\big) \cap B$ by the Distributive Laws ([Chapter 3](ch3_sets_for_probability_v2.md)). By countable additivity, $\mathbb P\big(\big(\bigcup_n A_n\big) \cap B\big) = \sum_n \mathbb P(A_n \cap B)$. Dividing by $\mathbb P(B)$ is allowed termwise: the partial sums converge, and the limit laws let us divide each partial sum by $\mathbb P(B)$. $\blacksquare$
:::

So every rule proven above, such as the Complement Rule, also holds for conditional probabilities given a fixed $B$. Rearranging the definition gives the **multiplication rule**
$$\mathbb P(A \cap B) = \mathbb P(A \mid B)\, \mathbb P(B).$$

:::{important icon=false} 📐 **Theorem (Law of Total Probability)**
Let $(A_n)_{n=1}^\infty$ be pairwise disjoint events with $\bigcup_n A_n = \Omega$. Then for every event $B$,
$$\mathbb P(B) = \sum_{n=1}^\infty \mathbb P(B \cap A_n), \qquad\text{and if every } \mathbb P(A_n) > 0, \qquad \mathbb P(B) = \sum_{n=1}^\infty \mathbb P(B \mid A_n)\, \mathbb P(A_n).$$
The same holds for finitely many events $A_1, \ldots, A_m$ with sums up to $m$.
:::

:::{admonition icon=false} ✍️ **Proof**
By the Distributive Laws, $B = B \cap \Omega = \bigcup_n (B \cap A_n)$, a union of pairwise disjoint events, so countable additivity gives the first formula. The second follows from the multiplication rule. For finitely many events, extend the list by $A_n := \emptyset$, whose terms are $0$. $\blacksquare$
:::

:::{important icon=false} 📐 **Theorem (Bayes' Theorem for Events)**
If $\mathbb P(A) > 0$ and $\mathbb P(B) > 0$, then
$$\mathbb P(A \mid B) = \frac{\mathbb P(B \mid A)\, \mathbb P(A)}{\mathbb P(B)}.$$
If moreover $(A_n)$ is a sequence, or a finite list, of pairwise disjoint events with union $\Omega$ and every $\mathbb P(A_n) > 0$, then
$$\mathbb P(A_k \mid B) = \frac{\mathbb P(B \mid A_k)\, \mathbb P(A_k)}{\sum_n \mathbb P(B \mid A_n)\, \mathbb P(A_n)}.$$
:::

:::{admonition icon=false} ✍️ **Proof**
By the multiplication rule, used twice, $\mathbb P(A \mid B)\,\mathbb P(B) = \mathbb P(A \cap B) = \mathbb P(B \mid A)\,\mathbb P(A)$; divide by $\mathbb P(B)$. For the second formula, the denominator is $\mathbb P(B)$ by the Law of Total Probability. $\blacksquare$
:::

In filtering, the $A_n$ are hypotheses about the true state and $B$ is a measurement. Bayes' theorem turns "how likely is this measurement if hypothesis $A_k$ is true" into "how likely is hypothesis $A_k$ given this measurement". [Chapter 8](ch8_bayesian_view_v2.md) names the ingredients and develops this into the Bayes filter.
  
**Example (three-card monte).** Three cards lie face down, and one of them is the queen. You point at card 1. With no other information, model the queen's position by the discrete probability space $\Omega = \{1, 2, 3\}$ with $\mathbb P(\{k\}) = \tfrac13$, and let $A_k := \{k\}$ be the event "the queen is card $k$".

*Scenario 1: an accidental reveal.* A gust of wind flips card 3, and it is not the queen. The observation is $B := \{1, 2\}$. Here $\mathbb P(B \mid A_1) = \mathbb P(B \mid A_2) = 1$ and $\mathbb P(B \mid A_3) = 0$, so by Bayes' theorem
$$\mathbb P(A_1 \mid B) = \frac{1 \cdot \tfrac13}{1 \cdot \tfrac13 + 1 \cdot \tfrac13 + 0 \cdot \tfrac13} = \frac12.$$
The definition gives the same directly: $\mathbb P(\{1\})/\mathbb P(\{1, 2\}) = \tfrac12$.

*Scenario 2: the dealer reveals.* The dealer knows where the queen is and always turns over a card that is neither yours nor the queen, flipping a fair coin to choose between cards 2 and 3 when both qualify. The dealer turns over card 3. The outcome must now record the dealer's action as well: take
$$\Omega' := \{(1, 2), (1, 3), (2, 3), (3, 2)\},$$
where $(q, d)$ means "the queen is card $q$ and the dealer turns over card $d$", with probabilities $\tfrac16, \tfrac16, \tfrac13, \tfrac13$ (the queen is card 1 with probability $\tfrac13$, and then the dealer picks each card with probability $\tfrac12$). Let $A_k$ be the event "the queen is card $k$" and $D := \{(1, 3), (2, 3)\}$ the event "the dealer turns over card 3". Then $\mathbb P(D \mid A_1) = \tfrac12$, $\mathbb P(D \mid A_2) = 1$, $\mathbb P(D \mid A_3) = 0$, and
$$\mathbb P(A_1 \mid D) = \frac{\tfrac12 \cdot \tfrac13}{\tfrac12 \cdot \tfrac13 + 1 \cdot \tfrac13 + 0 \cdot \tfrac13} = \frac13, \qquad \mathbb P(A_2 \mid D) = \frac23.$$

Both scenarios reveal the same fact, that card 3 is not the queen, yet card 1's probability is $\tfrac12$ in one and $\tfrac13$ in the other. The difference lies in $\mathbb P(\text{observation} \mid \text{hypothesis})$: in Scenario 2, the dealer's choice carries information about where the queen is. For filtering, the lesson is that a measurement can only be interpreted through a model of how it was produced, not through its value alone. (Scenario 2 is the [Monty Hall problem](https://en.wikipedia.org/wiki/Monty_Hall_problem): switching to card 2 doubles your chance of winning.)

**Example (a faulty load cell).** Suppose a scale's load cell is faulty with probability $0.01$. A healthy cell gives a reading more than $2$ lb from the truth with probability $0.05$, and a faulty one with probability $0.9$. (A discrete probability space with four outcomes, healthy or faulty and off or not, realizes these numbers.) A reading comes out $2.5$ lb off. With $W$ the event "the cell is faulty" and $O$ the event "the reading is more than $2$ lb off",
$$\mathbb P(W \mid O) = \frac{\mathbb P(O \mid W)\,\mathbb P(W)}{\mathbb P(O \mid W)\,\mathbb P(W) + \mathbb P(O \mid W^c)\,\mathbb P(W^c)} = \frac{0.9 \cdot 0.01}{0.9 \cdot 0.01 + 0.05 \cdot 0.99} \approx 0.154.$$
Even after a reading that a healthy cell rarely produces, the cell is most likely healthy, because faults are rare to begin with. Confusing $\mathbb P(O \mid W) = 0.9$ with $\mathbb P(W \mid O) \approx 0.15$ is a common mistake. Deciding whether to discard such a reading as an outlier involves exactly this trade-off ([Chapter 14](ch14_kalman_filters_in_practice_v2.md)).

:::{caution icon=false} ⚠️ **Assumptions and Failure Modes**
- **$\mathbb P(B) > 0$ is required.** Conditioning on a null event, such as "the noise is exactly $0.03$", is undefined by this formula. [Chapter 8](ch8_bayesian_view_v2.md) conditions on exact values of continuous quantities using densities. Doing so naively leads to paradoxes ([Borel–Kolmogorov paradox](https://en.wikipedia.org/wiki/Borel%E2%80%93Kolmogorov_paradox)).
- **$\mathbb P(A \mid B) \neq \mathbb P(B \mid A)$ in general**, as the load-cell example shows.
- **The answer depends on the model of the observation**, not only on the fact observed, as the two card scenarios show.
:::
  
## Independence

Two events are independent when the probability that both happen factors into the product of their probabilities.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Independent events
: Events $A$ and $B$ of a {term}`probability space` are independent if $\mathbb P(A \cap B) = \mathbb P(A)\,\mathbb P(B)$. A family $(A_i)_{i \in I}$ of events is (*mutually*) independent if
  $$\mathbb P(A_{i_1} \cap \cdots \cap A_{i_k}) = \mathbb P(A_{i_1}) \cdots \mathbb P(A_{i_k})$$
  for every $k \ge 2$ and all distinct indices $i_1, \ldots, i_k \in I$. It is *pairwise independent* if $A_i$ and $A_j$ are independent whenever $i \neq j$.
:::
::::

If $\mathbb P(B) > 0$, then $A$ and $B$ are independent if and only if $\mathbb P(A \mid B) = \mathbb P(A)$: learning that $B$ happened does not change the probability of $A$. The product form is used as the definition because it is symmetric in $A$ and $B$ and also makes sense when $\mathbb P(B) = 0$.

**Example.** For a fair die, "even" $= \{2, 4, 6\}$ and "at most 2" $= \{1, 2\}$ are independent, since $\mathbb P(\{2\}) = \tfrac16 = \tfrac12 \cdot \tfrac13$. But "even" and "at most 3" $= \{1, 2, 3\}$ are not, since $\mathbb P(\{2\}) = \tfrac16 \neq \tfrac12 \cdot \tfrac12$.

:::{important icon=false} 📐 **Lemma (Complements of Independent Events)**
If $A$ and $B$ are independent, then so are $A$ and $B^c$, $A^c$ and $B$, and $A^c$ and $B^c$.
:::

:::{admonition icon=false} ✍️ **Proof**
$A \cap B^c = A \setminus B$, so by Monotonicity $\mathbb P(A \cap B^c) = \mathbb P(A) - \mathbb P(A)\,\mathbb P(B) = \mathbb P(A)\,\mathbb P(B^c)$. The other two cases follow by applying this to the pair $(B, A)$ and then to $(A^c, B)$. $\blacksquare$
:::

**Disjoint is not independent.** If $A \cap B = \emptyset$ with $\mathbb P(A) > 0$ and $\mathbb P(B) > 0$, then $\mathbb P(A \cap B) = 0 < \mathbb P(A)\,\mathbb P(B)$. Disjoint events with positive probability are always *dependent*: knowing that $A$ happened tells you that $B$ did not.

**Pairwise is not mutual.** Toss a fair coin twice: $\Omega = \{HH, HT, TH, TT\}$, each outcome with probability $\tfrac14$. Let $A := \{HH, HT\}$ (first toss heads), $B := \{HH, TH\}$ (second toss heads), and $C := \{HH, TT\}$ (the tosses agree). Each has probability $\tfrac12$, and each pairwise intersection is $\{HH\}$, with probability $\tfrac14 = \tfrac12 \cdot \tfrac12$. So $A, B, C$ are pairwise independent. But
$$\mathbb P(A \cap B \cap C) = \mathbb P(\{HH\}) = \tfrac14 \neq \tfrac18 = \mathbb P(A)\,\mathbb P(B)\,\mathbb P(C),$$
so they are not mutually independent: $A$ and $B$ together determine $C$. Later chapters assume that measurement noises are independent, and it matters that this means the mutual version.

**Many independent trials.** For $n$ tosses of a coin with probability $p$ of heads, take $\Omega := \{H, T\}^{\{1, \ldots, n\}}$, the set of sequences of $n$ results, with $\mathcal F := \mathcal P(\Omega)$, and give each outcome $\omega$ the weight $\prod_{i=1}^n q(\omega_i)$, where $q(H) := p$ and $q(T) := 1 - p$. Expanding $\prod_{i=1}^n \big(q(H) + q(T)\big) = 1$ shows that the weights add up to $1$, and the same factorization shows that the events "toss $i$ is heads" ($i = 1, \ldots, n$) are mutually independent, each with probability $p$ ([Product measure](https://en.wikipedia.org/wiki/Product_measure)). For infinitely many tosses, a probability space with the same property exists too, but its construction needs more measure theory ([Kolmogorov extension theorem](https://en.wikipedia.org/wiki/Kolmogorov_extension_theorem)).
  
## Experiment: Relative Frequencies

Independent repetitions give a concrete way to look at $\mathbb P(A)$: in $n$ trials, count how often $A$ happens and divide by $n$. The plot below simulates five independent runs with a pseudo-random number generator and shows the *relative frequency* of $A$ after each trial.

This is an **experiment, not a proof.** The plot suggests that the relative frequency settles near $\mathbb P(A)$ as $n$ grows. [Chapter 6](ch6_expectation_and_variance_v2.md) proves the weak law of large numbers, which states precisely in what sense this happens, using only the axioms of this chapter and independence. Things to try: with few trials the runs disagree wildly; with many they bunch around $\mathbb P(A)$. The spread shrinks roughly like $1/\sqrt n$, which Chapter 6 explains through the variance $\sigma^2/n$ of an average. The convergence relies on independent trials under identical conditions; if the coin's bias drifted, or each toss depended on the previous ones, the frequencies need not settle at $\mathbb P(A)$.

```{marimo} python
:hide-code: true

freq_event = mo.ui.dropdown(
    options={
        "Fair coin shows heads (probability 1/2)": "coin",
        "Fair die shows six (probability 1/6)": "die",
        "Biased coin shows heads (probability 0.3)": "biased",
    },
    value="Fair coin shows heads (probability 1/2)",
    label="Event $A$",
)
freq_n = mo.ui.slider(
    steps=[10, 30, 100, 300, 1000, 3000, 10000],
    value=1000,
    show_value=True,
    label="Number of trials $n$",
)
```

```{marimo} python
:hide-code: true

_kind = freq_event.value
_p = {"coin": 0.5, "die": 1 / 6, "biased": 0.3}[_kind]
_n = freq_n.value
_runs = 5
_rng = np.random.default_rng(4)
if _kind == "die":
    _hits = _rng.integers(1, 7, size=(_runs, 10000))[:, :_n] == 6
else:
    _hits = _rng.random((_runs, 10000))[:, :_n] < _p
_k = np.arange(1, _n + 1)
_freq = np.cumsum(_hits, axis=1) / _k

_fig, _ax = plt.subplots(figsize=(8, 4.2))
for _r in range(_runs):
    _ax.plot(_k, _freq[_r], color=f"C{_r}", linewidth=1, label=f"run {_r + 1}")
_ax.axhline(_p, color="black", linewidth=1.5, label=r"$\mathbb{P}(A)$")
_ax.set_xscale("log")
_ax.set_xlim(1, _n)
_ax.set_ylim(0, 1)
_ax.set_xlabel("number of trials $k$ (log scale)")
_ax.set_ylabel("relative frequency of $A$")
_ax.grid(visible=True, alpha=0.9, linewidth=0.4)
_ax.legend(loc="upper right", fontsize=8, ncol=2)
_ax.set_title(f"Relative frequency of A in five runs of {_n} trials", style="italic")
_fig.tight_layout()

_final = ", ".join(f"{_v:.3f}" for _v in _freq[:, -1])
_dev = float(np.max(np.abs(_freq[:, -1] - _p)))
_summary = mo.md(
    f"After {_n} trials the relative frequencies are {_final}, "
    + rf"compared with $\mathbb P(A) = {_p:.3f}$. "
    + f"The largest deviation is {_dev:.3f}."
)
mo.vstack([mo.hstack([freq_event, freq_n], justify="start"), graphic(_fig), _summary])
```

## Summary

- A **probability space** $(\Omega, \mathcal F, \mathbb P)$ consists of a **sample space** $\Omega$ of **outcomes**, a **σ-algebra** $\mathcal F$ of **events** (it contains $\Omega$ and is closed under complements and countable unions), and a **probability measure** $\mathbb P$ satisfying Kolmogorov's axioms: nonnegativity, $\mathbb P(\Omega) = 1$, and countable additivity.
- The **generated σ-algebra** $\sigma(\mathcal G)$ is the smallest σ-algebra containing $\mathcal G$. The **Borel σ-algebra** $\mathcal B(\mathbb R)$ is generated by the intervals and contains every interval and every countable set.
- The axioms imply $\mathbb P(\emptyset) = 0$, finite additivity, the complement rule, monotonicity, inclusion–exclusion for two events, the union bound, and continuity from below and above.
- Discrete probability spaces put masses $p_n$ on countably many outcomes. No probability treats all elements of a countably infinite set equally.
- Using the Axiom of Choice, the Vitali set shows that no rotation-invariant probability is defined on all subsets of $[0, 1)$. Lebesgue measure $\lambda$, which gives every interval its length, exists on the Borel sets. For a uniformly random number in $[0, 1]$, every single point and every countable set has probability $0$, so statements can hold **almost surely** without holding surely.
- **Conditional probability** $\mathbb P(A \mid B) = \mathbb P(A \cap B)/\mathbb P(B)$ is again a probability measure, and it gives the law of total probability and Bayes' theorem. Interpreting an observation requires a model of how it was produced.
- **Independent events** satisfy $\mathbb P(A \cap B) = \mathbb P(A)\,\mathbb P(B)$; pairwise independence does not imply mutual independence, and disjoint events with positive probability are never independent.
- In simulations, relative frequencies settle near probabilities; Chapter 6 proves why.

## What's Next

So far, events are sets of outcomes. Filters, however, work with *numbers*: readings, noise values, and estimates. [Chapter 5](ch5_random_variables_v2.md) introduces **random variables**, functions from $\Omega$ to $\mathbb R$ whose preimages of Borel sets are events. Chapter 3's lemma that preimages preserve set operations makes every question about a random variable's value an event, and the probabilities of those events form its **distribution**. That is the language in which we finally write the measurement model $z_k = x_k + v_k$ precisely.