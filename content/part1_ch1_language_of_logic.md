---
title: Language of Logic
# marimo-version: 0.25.1
# css_file: notebook-styles.css
subtitle: "From Symbols to Sentences"
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
mo.latex(dedent(
    r"""
    \newcommand{\existsin}[2]{\exists #1 \!\!\in\!\! #2\,}
    \newcommand{\forallin}[2]{\forall #1 \!\!\in\!\! #2\,}
    \newcommand{\existssubseteq}[2]{\exists #1 \!\!\subseteq\!\! #2\,}
    \newcommand{\forallsubseteq}[2]{\forall #1 \!\!\subseteq\!\! #2\,}
    """
))
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

Developing precise language is vital for communicating a precise understanding of any topic. As we introduce new language over the coming chapters, it is important to keep in mind that we will be switching back and forth between three different layers of language:
- **Metalanguage:** This is plain language we use to talk *about* the formal mathematical language we are developing.  For example, most of the writing between the lines of math in this book is plain english, and not rigorously defined. While we try our best to be articulate and specific, metalanguage is not formal.
- **Syntax:** This refers to the raw symbols (or strings of symbols) we use in our formal mathematical language, *before* any meaning is interpreted. So far in this book, our syntax has consisted of the roman alphabet, greek alphabet, numbers, algebraic symbols, and some combinations of letters with symbols (such as "$\hat x _k^-$"). However, we are about to introduce some new symbols.
- **Semantics:** This the list of rules and conventions which dictate how the symbols (or strings of symbols) in our syntax are interpreted. For example the convention is this book is to interpret "$\hat x _k^-$" as "the prediction at time $k$ prior to the measurement at time $k$".
  
## Connectives

Logical connectives combine one or more statements into a new statement whose truth value depends only on the truth values of the parts.
  
### Negation

The negation operator is denoted $\neg$ (read as "not"). When placed to the left of a statement $A$ such as:

$$\neg A$$

it creates a new statement which has the opposite truth value from $A$.

Letting $T$ represent a placeholder for some true statement, and $F$ represent a placeholder for some false statement, we say that "$\neg T$" is false and "$\neg F$" is true. This is often represented in the form of a truth table:

$$\begin{array}{r | c}
\neg & \\
\hline
\mathbf{T} & \text{F} \\
\mathbf{F} & \text{T} \\
\end{array}$$
  
### Conjunction

The conjunction operator is denoted $\land$ (read as "and"). When placed between two statements $A$ and $B$, such as:

$$A \land B$$

it creates a new statement which is true iff $A$ and $B$ are both true.

Conjunction is represented by the following truth table:

$$\begin{array}{r | cc}
\land & \mathbf{T} & \mathbf{F} \\
\hline
\mathbf{T} & \text{T} & \text{F} \\
\mathbf{F} & \text{F} & \text{F} \\
\end{array}$$
  
### Disjunction

The disjunction operator is denoted $\lor$ (read "or"). When placed between two statements $A$ and $B$, such as:

$$A \lor B$$

it acts as a shorthand for $\neg(\neg A \land \neg B)$, which is false iff both statements are false[^de-morgan].

Disjunction is represented by the following truth table:

$$\begin{array}{r | cc}
\lor & \mathbf{T} & \mathbf{F} \\
\hline
\mathbf{T} & \text{T} & \text{T} \\
\mathbf{F} & \text{T} & \text{F} \\
\end{array}$$

[^de-morgan]: Similarly, had we taken $\lor$ as primitive, then $\land$ could be defined as an abbreviation, where $A \land B$ would be shorthand for $\neg(\neg A \lor \neg B)$. This ability to express conjunctions and disjunctions in terms of each other using negation is known as a "dual" in [De Morgan's laws](https://en.wikipedia.org/wiki/De_Morgan%27s_laws).
  
### Conditional

The conditional operator is denoted $\rightarrow$ (read "implies", or "if ... then ..."). When placed between two statements, such as:

$$A \rightarrow B$$

it acts as shorthand for "$\neg A \lor B$", which is false iff $A$ is true and $B$ is false.

The conditional is represented by the following truth table:

$$\begin{array}{r | cc}
\rightarrow & \mathbf{T} & \mathbf{F} \\
\hline
\mathbf{T} & \text{T} & \text{F} \\
\mathbf{F} & \text{T} & \text{T} \\
\end{array}$$
  
### Biconditional

The biconditional operator is denoted $\leftrightarrow$ (read "if and only if"). When placed between two statements, such as:

$$A \leftrightarrow B$$

it acts as shorthand for "$(A \rightarrow B) \land (B \rightarrow A)$", which is true iff $A$ and $B$ have the same truth value.

The biconditional is represented by the following truth table:

$$\begin{array}{r | cc}
\leftrightarrow & \mathbf{T} & \mathbf{F} \\
\hline
\mathbf{T} & \text{T} & \text{F} \\
\mathbf{F} & \text{F} & \text{T} \\
\end{array}$$
  
## Quantifiers

Logical quantifiers allow us to make statements about collections of objects by stating how many objects in a given domain satisfy some property.
  
### Existential

The existential quantifier is denoted $\exists$ (read as "there exists"). When placed to the left of a variable, followed by some statement, such as:

$$\exists x\, A$$

it creates a new statement interpreted as "There exists at least one value of $x$ for which $A$ is true".
  
### Universal

The universal quantifier is denoted $\forall$ (read as "for all"). When placed to the left of a variable, followed by some statement, such as:

$$\forall x\, A$$

it acts as a shorthand for "$\neg \exists x\, (\neg A)$", which is true iff for all values of $x$, $A$ is true.
  
## Relational Operators

Relational operators compare two objects and produce a true or false statement.
  
### Equality

The equality operator (aka equals sign) is denoted "$=$". When placed between two objects, such as:

$$x = y$$

it creates a new statement which is true iff $x$ and $y$ have the same value.
  
### Membership

The membership symbol is denoted $\in$ (read as "is in", or "in").

This symbol is specific to Set Theory. A "set" is an object in math which can roughly thought of as "any unordered collection of unique objects." The objects in the collection are called the set's "members" or "elements". However, no precise definition or "set" exists because sets are a "primitive concept", meaning they are a foundational block on which other concepts are defined (a [bottom turtle](https://en.wikipedia.org/wiki/Turtles_all_the_way_down), so to speak, since we cannot have infinite regress of definitions). As such, sets are only described by how the [Set Theory axioms](https://en.wikipedia.org/wiki/Zermelo%E2%80%93Fraenkel_set_theory) allow them to behave. More on that in the next section.

When placed between an object and a set, such as:

$$x \in y$$

it creates a new statement which is true iff $x$ is an element of $y$.
  
## Formulas

Now that we have the ability to connect statements, make quantitative statements about collections of objects, and state relations between objects, we want some way to combine all of these abilities together. Formulas combine connectives, quantifiers, and relational operators to specify properties of objects. Formulas are defined recursively according to the following 5 rules:

1. **Atomic:** If $u$ and $v$ are variables (not necessarily distinct), then $u \in v$ and $u = v$ are formulas.
2. **Negation:** If $\varphi$ is a formula, so is $\neg \varphi$.

3. **Conjunction:** If $\varphi$ and $\psi$ are formulas, so is $(\varphi \land \psi)$.

4. **Quantifiers:** If $\varphi$ is a formula and $x$ is a variable, then $\exists x\,\varphi$ is a formula.

5. **Closure:** Nothing else is a formula.

Note that since $\lor$, $\rightarrow$, $\leftrightarrow$, $\forall$, are abbreviations using $\neg$, $\land$, $\exists$, they are allowed in formulas as well.
  
### Free Variable Notation

Any variable in a formula which is directly to the right of a quantifier (such as $x$ in the formula $\exists x\, \varphi$) is called a *bound variable*. This is because it acts as a place holder value for the collection of objects being quantified, rather than a value which we can freely assign. By contrast, any other variable in a formula which we can freely assign a value to (such as $x$ in the formula $x = y$) is called a *free variable*.

When we want to specify the free variables of some unspecified formula $\varphi$, we write

$$\varphi(p_1,\ldots,p_n)$$

to indicate that the free variables of $\varphi$ are among $p_1,\ldots,p_n$. We might not know how many $p_i$ there are, or even if the $p_i$ necessarily occur as free variables in $\varphi$, but this notation ensures that if a variable is not one of $p_1,\ldots,p_n$, then it does not occur as a free variable in $\varphi(p_1,\ldots,p_n)$.
  
### Formula Substitution

We use the notation

$$\varphi[x/y]$$

to reference the result of replacing every *free* occurrence of $x$ in $\varphi$ by $y$. We only use this when $y$ is a variable that does not occur in $\varphi$, so there are no capture issues.
  
### Sentences

A sentence is a formula with no free variables; every variable occurring in it is bound by a quantifier. While a formula with free variables doesn't have a truth value until we assign values to the variables, sentences are simply true or false in a given structure. In order to build a mathematical structure, we must choose some sentences as starting points which we define as true in our structure. We call these starting point sentences **axioms**.
  
## More Definitions

When we want to introduce a new notation for an object we've already described, we write

$$\text{new notation} := \text{description}$$

to mean "the left side is defined to stand for the right side." Unlike "$=$", the symbol "$:=$" is not part of our formal language. It belongs to the metalanguage and simply tells the reader that we are introducing shorthand. Any formula written using such shorthand can be rewritten by substituting in the definition.

Before we move on to building the foundational axioms of mathematics, let's define a few more notations that will make our writing easier:

| Definition | Read as |
| :--- | :--- |
| $x \notin y := \neg(x \in y)$ | "$x$ is **not in** $y$" |
| $x \subseteq y := \forall z(z \in x \rightarrow z \in y)$ | "$x$ is a **subset** of $y$" |
| $\exists! x\, \varphi := \exists x\, (\varphi \land \forall y\, (\varphi[x/y] \leftrightarrow y = x))$ | "There **exists unique** $x$ such that $\varphi$" |
| $\existsin{x}{y} \varphi := \exists x\, (x \in y \land \varphi)$ | "There **exists** $x$ **in** $y$ such that $\varphi$" |
| $\forallin{x}{y} \varphi := \forall x\, (x \in y \rightarrow \varphi)$ | "**For all** $x$ **in** $y$, $\varphi$" |
| $\existssubseteq{x}{y} \varphi := \exists x\, (x \subseteq y \land \varphi)$ | "There **exists** $x$ which is a **subset** of $y$ such that $\varphi$" |
| $\forallsubseteq{x}{y} \varphi := \forall x\, (x \subseteq y \rightarrow \varphi)$ | "**For all** $x$ which are **subsets** of $y$, $\varphi$" |