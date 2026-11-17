# /// script
# dependencies = [
#     "marimo>=0.25.1",
#     "matplotlib==3.11.2",
#     "numpy==2.5.3",
#     "pandas==3.0.6",
#     "schemdraw==0.23",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="Set Theory", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
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
    -->
    """)
    return


@app.cell
def imports():
    # jb: include=false
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib
    import schemdraw
    from schemdraw import flow
    from textwrap import dedent
    import matplotlib.pyplot as plt

    return dedent, mo, plt, schemdraw


@app.cell
def display_format(dedent, mo, plt, schemdraw):
    # jb: include=false
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

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The goal of this chapter is to define set theory and the necessary tools for defining probability spaces (which we will then do in the next chapter).

    Set theory is a foundation for nearly all of mathematics, including number theory, functions, topology, algebra, and probability[^other-math-foundations]. Here, we will build the axioms of Zermelo-Frankel set theory, along with the axiom of choice.

    There are many equivalent ways to formulate the ZFC axioms. We will include all 10 for the purpose of explanation. However, the Axiom of the Null Set is often omitted since it is easily proven by applying the Axiom Schema of Separation to filter out elements which are equal to themselves. Additionally, the Axiom Schema of Separation is sometimes omitted since it can be proven using the Axiom Schema of Replacement.

    [^other-math-foundations]: This is because almost every mathematical object can be defined inside set theory, and almost every theorem can be derived from its axioms. However, alternative foundational theories also exist, such as [Category Theory](https://en.wikipedia.org/wiki/Category_theory), which is common in geometry, and [Type Theory](https://en.wikipedia.org/wiki/Type_theory), which is used in theoretical computer science, as well as the theorem prover programming languages [Lean](https://lean-lang.org) and [Rocq](https://rocq-prover.org).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Axiom of Extensionality

    Two sets are equal iff they contain the exact same members:

    $$\forall x\forall y\,[\forall z\,(z\in x\leftrightarrow z\in y)\rightarrow x=y].$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Axiom of the Null Set

    There exists a set $x$ such that for all $y$, $y$ is not an element of $x$:

    $$\exists x \forall y (y \notin x).$$

    By Extensionality, this set is unique. It is called the "null set" or "empty set" and is denoted "$\emptyset$".
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Axiom of Pairing

    For any two sets $x$ and $y$, there exists a set $z$ that contains $x$ and $y$ as its only members:

    $$\forall x \, \forall y \, \exists z \, \forall w \, (w \in z \leftrightarrow w = x \lor w = y).$$

    By extensionality, this set $z$ is unique and may be referred to as the pairing set $\{x, y\}$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Singleton Sets

    By letting $y=x$, the Axiom of Pairing tells us that

    $$\forall x\, \exists z\, \forall w\, (w \in z \leftrightarrow w = x).$$

    This set $z$ is called a singleton set because it contains exactly one element, and is denoted $\{x\}$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ordered Pairs

    Given two sets $a$ and $b$, the axiom of pairing guarantees the existence of the singleton $\{a\}$ and the pairing set $\{a, b\}$. Paring again guarantees the existence of $\{\{a\},\{a,b\}\}$. We call this the "ordered pair" of $a$ and $b$ and use the shorthand

    $$(a, b) := \{\{a\},\{a,b\}\},$$

    where $a$ and $b$ are called the "coordinates".

    By extensionality, two ordered pairs are equal iff their corresponding coordinates are equal:

    $$(a, b) = (c, d) \leftrightarrow a = c \land b = d.$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Functions

    A set $f$ is a function iff:

    - Every element of $f$ is an ordered pair:
      $$\forallin x f \, \exists a\, \exists b\, [x = (a, b)]$$
    - Each first coordinate has at most one partner:
      $$\forall a\, \forall b\, \forall c\; ([(a, b) \in f \land (a, c) \in f] \rightarrow b = c)$$

    If $f$ is a function and $(a, b) \in f$, then we write $f(a) = b$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Axiom of Power Set

    For any set $x$, there exists a set $y$ containing precisely all the subsets of $x$:

    $$\forall x\,\exists y\,\forall z\, (z\in y \leftrightarrow z \subseteq x).$$

    This set $y$ is known as the power set of $x$ and is denoted $\mathcal{P}(x)$. By Extensionality, it is unique.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Axiom of Union

    For any set of sets $X$, there exists a set $U$ whose elements are precisely the elements that belong to at least one of the sets contained in $X$:

    $$\forall X\,\exists U\,\forall y\, [y\in U\leftrightarrow \existsin z X (y\in z)].$$

    By Extensionality, this union set $U$ is unique. It is sometimes denoted as $\bigcup X$ or $\bigcup_{w \in X} w$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Union Operator

    The union operator is denoted $\cup$. When placed between two sets $x$ and $y$, it is a shorthand to reference the union of the set containing $x$ and $y$ (whose existence is guaranteed by the axiom of pairing):

    $$x \cup y := \bigcup \{x, y\}.$$

    Since the pairing set is unordered, this operation is commutative and we have

    $$x \cup y = y \cup x.$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Axiom Schema of Separation

    For every formula $\varphi(x, A, p_1, \dots, p_n)$ where $A, p_1, \dots, p_n$ are sets, the following is an axiom:

    For any sets $A, p_1, \dots, p_n$, there exists a set $B$ distinct from $x, A, p_1, \dots, p_n$ (so $B$ is not free in $\varphi$) whose elements are exactly those elements $x$ of $A$ that satisfy $\varphi$:

    $$\forall p_1 \cdots \forall p_n\, \forall A\, \exists B\, \forall x\, [x \in B \leftrightarrow (x \in A \land \varphi)].$$

    In other words, every property definable by a formula carves out a subset of any given set. This is called an axiom schema, rather than a single axiom, because we want Separation to hold for all formulas $\varphi$, so we make an axiom for every $\varphi$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Separation Set-Builder Notation

    We use the following notation to refer to a set whose existence is guaranteed by the axiom schema of separation:

    $$\{x \in A: \varphi\}.$$

    By extensionality, this set is unique.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Intersection Operator

    The intersection operator is denoted $\cap$. When placed between two sets, such as:

    $$A \cap B,$$

    it acts as a shorthand for $\{x \in A: x \in B\}$. Since we are treating $A$ and $B$ symmetrically here, intersection is commutative[^intersection-commutativity]:

    $$A \cap B = B \cap A.$$

    [^intersection-commutativity]:
        $$\begin{align*}
        C = A \cap B &\leftrightarrow C = \{x \in A: x \in B\} \\
        &\leftrightarrow \forall x\, [x \in C \leftrightarrow x \in A \land x \in B] \\
        &\leftrightarrow \forall x\, [x \in C \leftrightarrow x \in B \land x \in A] \\
        &\leftrightarrow C = \{x \in B: x \in A\} \\
        &\leftrightarrow C = B \cap A \\
        \end{align*}$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Axiom Schema of Replacement

    For every formula $\varphi(x, y, A, p_1, \dots, p_n)$ where $A, p_1, \dots, p_n$ are sets, the following is an axiom:

    For any sets $A, p_1, \dots, p_n$, if for every $x \in A$ there is exactly one $y$ satisfying $\varphi$, then there exists a set $B$ distinct from $x, y, A, p_1, \dots, p_n$ (so $B$ is not free in $\varphi$) whose elements are exactly those $y$ such that $\varphi$ holds for some $x \in A$:

    $$\forall p_1 \cdots \forall p_n\, \forall A\,[\forallin x A\, \exists! y\, \varphi \rightarrow \exists B\, \forall y\, (y \in B \leftrightarrow \existsin x A\, \varphi)].$$

    In other words, if a formula $\varphi$ assigns to each $x \in A$ exactly one $y$, then the collection of all outputs is also a set. Like Separation, this is a schema because we want it to hold for every formula $\varphi$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Replacement Set-Builder Notation

    Suppose $\varphi$ assigns to each $x \in A$ exactly one $y$. We use the following notation to refer to the set whose existence is guaranteed by the axiom schema of replacement:

    $$\{y : \existsin x A\, \varphi\},$$

    which is read as "the set of all $y$ such that $\varphi$ holds for some $x \in A$." By extensionality, this set is unique. We only use this notation when $\varphi$ is functional on $A$, since otherwise Replacement does not guarantee that such a set exists.

    ### Combining Set-Builder Notations

    Note that while Separation set-builder notation ranges over $A$ and filters elements out, Replacement set-builder notation ranges over $A$ and transforms each element. However, we can combine the two into a single notation. Suppose $\psi$ is a formula and $\varphi$ is functional on $\{x \in A : \psi\}$. We use the notation

    $$\{y : \existsin x A\, (\psi \land \varphi)\},$$

    which is interpreted as

    $$\{y : \existsin x {\{x \in A : \psi\}}\, \varphi\}.$$[^combined-set-builder]

    Note that $\varphi$ need only be functional on the filtered subset $\{x \in A : \psi\}$, not on all of $A$.

    [^combined-set-builder]:
        $$\begin{align*}
        B = \{y : \existsin x {\{x \in A : \psi\}}\, \varphi\} &\leftrightarrow \forall y\, [y \in B \leftrightarrow \exists x\, (x \in \{x \in A : \psi\} \land \varphi)] \\
        &\leftrightarrow \forall y\, [y \in B \leftrightarrow \exists x\, ((x \in A \land \psi) \land \varphi)] \\
        &\leftrightarrow \forall y\, [y \in B \leftrightarrow \exists x\, (x \in A \land (\psi \land \varphi))] \\
        &\leftrightarrow B = \{y : \existsin x A\, (\psi \land \varphi)\} \\
        \end{align*}$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Replacement Set-Builder Notation

    Similarly to our Separation set-builder notation, we often refer to a set whose existence is guaranteed by the Axiom Schema of Replacement as:

    $$\{F(x): x \in A\},$$

    where $F(x)$ is interpereted as "the unique $y$ such that "
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Replacement Set-Builder Notation

    Replacement also gives a set-builder notation. Suppose $\varphi(x, y)$ is functional on $A$, so that for every $x \in A$ there is exactly one $y$ with $\varphi(x, y)$. It is common to write this unique $y$ as a term $F(x)$, where $F(x)$ is shorthand for "the unique $y$ such that $\varphi(x, y)$." The set $B$ guaranteed by Replacement is then referred to with the notation

    $$\{F(x) : x \in A\}.$$

    Unwinding the shorthand, this is the set $B$ satisfying

    $$y \in \{F(x) : x \in A\} \leftrightarrow \exists x \in A\, \varphi(x, y),$$

    or equivalently, $y \in B$ iff $y = F(x)$ for some $x \in A$. By Extensionality, this set is unique.

    Note the difference in form between the two notations. In $\{x \in A : \varphi\}$ the variable ranges over $A$ and the formula *filters* the elements, so the result is a subset of $A$. In $\{F(x) : x \in A\}$ the variable ranges over $A$ and the formula *transforms* each element, so the result generally contains new objects that need not be elements of $A$ at all.

    #### Examples

    Given a set $A$, the set of singletons of its elements is

    $$\{\{x\} : x \in A\},$$

    and if $A$ is a set of sets, the set of all unions of pairs with a fixed set $S$ is

    $$\{x \cup S : x \in A\}.$$

    #### Combining Both Set-Builder Notations

    The two notations are often combined to apply a transformation to only some elements of $A$. Writing $\{F(x) : x \in A \land \psi(x)\}$ means

    $$\{F(x) : x \in \{x \in A : \psi(x)\}\},$$

    where Separation first produces the subset $\{x \in A : \psi(x)\}$ and Replacement then maps over it. For example, if $A$ is a set of sets,

    $$\{\bigcup x : x \in A \land x \neq \varnothing\}$$

    collects the unions of the nonempty members of $A$.

    Note: Replacement is strictly stronger than the transformation notation might suggest. Because $F(x)$ can be any definable operation, the image of a set under any definable function is guaranteed to be a set, even when the outputs have much higher rank than the inputs. Separation alone cannot provide this.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Axiom of Infinity

    At least one infinite set $I$ exists. The empty set $\emptyset$ is an element of $I$, and whenever a set $x$ is an element of $I$, so is its successor $x \cup \{x\}$:

    $$\exists I\, [\emptyset \in I \land \forall x\, (x \in I \rightarrow x \cup \{x\} \in I)].$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Successor

    $x \cup \{x\}$ is called the successor of $x$, and is often denoted $S(x)$, or $x^+$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Axiom of Regularity

    Every nonempty set $A$ has a member $x$ that shares no members with $A$:

    $$\forall A\,[\exists x\,(x \in A) \rightarrow \existsin x A\, \neg\exists z\,(z \in x \land z \in A)].$$

    Using the abbreviations above, the last part says $x \cap A = \emptyset$. This is also called the Axiom of Foundation. It rules out sets that are “circular” in their membership. This has two consequences:

    1. No set is a member of itself. If $A \in A$, then the singleton $\{A\}$ is nonempty, so by Regularity it has a member disjoint from it. The only member is $A$, so $A \cap \{A\} = \emptyset$. But $A \in A$ and $A \in \{A\}$, so $A$ is in both, a contradiction.
    2. There are no infinite descending chains $\cdots \in x_3 \in x_2 \in x_1 \in x_0$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Axiom of Choice

    For any set $X$ whose members are nonempty, pairwise disjoint sets, there exists a set $C$ that contains exactly one element from each member of $X$:

    $$\forall X\,\big[\big(\forall A \in X\,\exists y\,(y \in A) \;\land\; \forall A \in X\,\forall B \in X\,(\neg(A = B) \rightarrow \neg\exists z\,(z \in A \land z \in B))\big) \rightarrow \exists C\,\forall A \in X\,\exists! z\,(z \in A \land z \in C)\big].$$

    The set $C$ is called a choice set or selector for $X$. Unlike the other axioms, Choice asserts that a set exists without giving any rule for constructing it. Informally, it lets us make infinitely many arbitrary selections at once. It is equivalent to several other well-known statements, such as the Well-Ordering Theorem, Zorn’s Lemma, and “every product of nonempty sets is nonempty.”

    Note: The version above (disjoint sets) is one of many equivalent formulations. Another common one says that for every collection of nonempty sets there exists a function that picks an element from each. Once we define functions in terms of sets, this is easy to state, but the disjoint-sets form can be written directly in the language of $\in$ and $=$.
    """)
    return


if __name__ == "__main__":
    app.run()
