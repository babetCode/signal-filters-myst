---
title: Set Theory
# marimo-version: 0.25.1
# css_file: notebook-styles.css
subtitle: "Axiomatic Structure"
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

Set theory is a foundation for nearly all of mathematics, including number theory, functions, topology, algebra, and probability[^other-math-foundations]. There are many equivalent ways to formulate the ZFC axioms. Here, we will include all 10 for the purpose of explanation. However, the Axiom of the Null Set is often omitted since it is easily proven by applying the Axiom Schema of Separation to filter out elements which are equal to themselves. Additionally, the Axiom Schema of Separation is sometimes omitted since it can be proven using the Axiom Schema of Replacement.

[^other-math-foundations]: This is because almost every mathematical object can be defined inside set theory, and almost every theorem can be derived from its axioms. However, alternative foundational theories also exist, such as [Category Theory](https://en.wikipedia.org/wiki/Category_theory), which is common in geometry, and [Type Theory](https://en.wikipedia.org/wiki/Type_theory), which is used in theoretical computer science, as well as the theorem prover programming languages [Lean](https://lean-lang.org) and [Rocq](https://rocq-prover.org).
  
:::{div}
:class: h-0 overflow-hidden opacity-0 m-0 p-0 pointer-events-none

## Definition - Axiom
:::

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Axiom
: A {term}`sentence` that is a starting point in a mathematical structure, which can be used in a proof without justification.
:::
::::
  
## Axiom of Extensionality

Two sets are equal iff they contain the exact same members:

$$\forall x\forall y\,[\forall z\,(z\in x\leftrightarrow z\in y)\rightarrow x=y]$$
  
## Axiom of the Null Set

There exists a set $x$ such that for all $y$, $y$ is not an element of $x$:

$$\exists x \forall y (y \notin x)$$

By Extensionality, this set is unique. It is called the "null set" or "empty set" and is denoted "$\emptyset$".
  
## Axiom of Pairing

For any two sets $x$ and $y$, there exists a set $z$ that contains $x$ and $y$ as its only members:

$$\forall x \, \forall y \, \exists z \, \forall w \, (w \in z \leftrightarrow w = x \lor w = y).$$

By extensionality, this set $z$ is unique and may be referred to as $\{x, y\}$.
  
### Singleton Sets

By letting $y=x$, the Axiom of Pairing tells us that

$$\forall x\, \exists z\, \forall w\, (w \in z \leftrightarrow w = x).$$

This set $z$ is called a singleton set because it contains exactly one element, and is denoted $\{x\}$.
  
## Axiom of Power Set

For any set $x$, there exists a unique set $y$ containing precisely all the subsets of $x$:

$$\forall x\,\exists y\,\forall z\, (z\in y \leftrightarrow z \subseteq x)$$

This set $y$ is known as the power set of $x$ and is denoted $\mathcal{P}(x)$.
  
## Axiom of Union

For any set of sets $X$, there exists a set $U$ whose elements are precisely the elements that belong to at least one of the sets contained in $X$:

$$\forall X\,\exists U\,\forall y\, [y\in U\leftrightarrow \exists z\in X (y\in z)]$$

By Extensionality, this union set $U$ is unique. It is sometimes denoted as $\bigcup X$ or $\bigcup_{w \in X} w$.
  
### Union Operator

The union operator is denoted $\cup$. When placed between two sets $x$ and $y$, it is a shorthand to reference the union of the set containing $x$ and $y$ (whose existence is guaranteed by the axiom of pairng):

$$x \cup y := \bigcup \{x, y\}.$$

Since the paring set is unordered, this operation is commutative and we have

$$x \cup y = y \cup x.$$
  
## Axiom Schema of Separation

For every formula $\varphi(x, A, p_1, \dots, p_n)$ where $A, p_1, \dots, p_n$ are sets, the following is an axiom:

For any sets $A, p_1, \dots, p_n$, there exists a set $B$—distinct from $(x, A, p_1, \dots, p_n)$, so $B$ is not free in $\varphi$—whose elements are exactly those elements $x$ of $A$ that satisfy $\varphi$.:

$$\forall p_1 \cdots \forall p_n\, \forall A\, \exists B\, \forall x\, [x \in B \leftrightarrow (x \in A \land \varphi)].$$

In other words, every property definable by a formula carves out a subset of any given set. This is called an axiom schema, rather than a single axiom, because we want Separation to hold for all formulas $\varphi$, so we make an axiom for every such $\varphi$.
  
### Set-Builder Notation

When referencing sets, we often use curly braces as shorthand for any set $B$ whose existence is guaranteed by the axiom schema of separation:

$$\{x \in A: \varphi\}.$$

By extensionality, this set is unique.
  
### Intersection Operator

The intersection operator is denoted $\cap$. When placed between two sets, it references the set which contains all elements contained in both sets:

$$A \cap B = \{x \in A: x \in B\}.$$

Since this separation treats $A$ and $B$ symetrically, we have

$$A \cap B = B \cap A.$$
  
## Axiom Schema of Replacement

For every formula $\varphi(x, y, A, p_1, \dots, p_n)$ where $A, p_1, \dots, p_n$ are sets, the following is an axiom:

For any sets $A, p_1, \dots, p_n$, if for every $x \in A$ there is exactly one $y$ satisfying $\varphi$, then there exists a set $B$—distinct from $(x, y, A, p_1, \dots, p_n)$, so $B$ is not free in $\varphi$—whose elements are exactly those $y$ such that $\varphi$ holds for some $x \in A$:

$$\forall p_1 \cdots \forall p_n\, \forall A\,[\forallin x A\, \exists! y\, \varphi \rightarrow \exists B\, \forall y\, (y \in B \leftrightarrow \existsin x A\, \varphi)].$$

In other words, if a formula $\varphi$ is functional on a set $A$ (that is, it assigns to each $x \in A$ exactly one $y$), then the collection of all outputs is also a set (formally, $\varphi$ is not a function yet, since it is not a set of ordered pairs). Like Separation, this is a schema because we want it to hold for every formula $\varphi$.
  
## Axiom of Infinity

At least one infinite set $I$ exists. The empty set $\emptyset$ is an element of $I$, and whenever a set $x$ is an element of $I$, so is its successor $x \cup \{x\}$:

$$\exists I\, [\emptyset \in I \land \forall x\, (x \in I \rightarrow x \cup \{x\} \in I)].$$
  
### Successor Operator

$x \cup \{x\}$ is called the successor of $x$, and is often denoted $S(x)$, or $x^+$.
  
## Axiom of Regularity

Every nonempty set $A$ has a member $x$ that shares no members with $A$:

$$\forall A\,[\exists x\,(x \in A) \rightarrow \existsin x A\, \neg\exists z\,(z \in x \land z \in A)].$$

Using the abbreviations above, the last part says $x \cap A = \emptyset$. This is also called the Axiom of Foundation. It rules out sets that are “circular” in their membership. Two consequences:

No set is a member of itself. If $A \in A$, then the singleton $\{A\}$ is nonempty, so by Regularity it has a member disjoint from it. The only member is $A$, so $A \cap \{A\} = \emptyset$. But $A \in A$ and $A \in \{A\}$, so $A$ is in both, a contradiction.
There are no infinite descending chains $\cdots \in x_3 \in x_2 \in x_1 \in x_0$.
  
## Axiom of Choice

For any set $X$ whose members are nonempty, pairwise disjoint sets, there exists a set $C$ that contains exactly one element from each member of $X$:

$$\forall X\,\big[\big(\forall A \in X\,\exists y\,(y \in A) \;\land\; \forall A \in X\,\forall B \in X\,(\neg(A = B) \rightarrow \neg\exists z\,(z \in A \land z \in B))\big) \rightarrow \exists C\,\forall A \in X\,\exists! z\,(z \in A \land z \in C)\big].$$

The set $C$ is called a choice set or selector for $X$. Unlike the other axioms, Choice asserts that a set exists without giving any rule for constructing it. Informally, it lets us make infinitely many arbitrary selections at once. It is equivalent to several other well-known statements, such as the Well-Ordering Theorem, Zorn’s Lemma, and “every product of nonempty sets is nonempty.”

Note: The version above (disjoint sets) is one of many equivalent formulations. Another common one says that for every collection of nonempty sets there exists a function that picks an element from each. Once we define functions in terms of sets, this is easy to state, but the disjoint-sets form can be written directly in the language of $\in$ and $=$.