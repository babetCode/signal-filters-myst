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


@app.cell(hide_code=True)
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


@app.cell(hide_code=True)
def imports():
    # jb: include=false
    import marimo as mo
    from textwrap import dedent

    return dedent, mo


@app.cell(hide_code=True)
def display_format(dedent, mo):
    # jb: include=false
    mo.latex(dedent(
        r"""\newcommand{\existsin}[2]{\exists #1 \!\!\in\!\! #2\,}
        \newcommand{\forallin}[2]{\forall #1 \!\!\in\!\! #2\,}
        \newcommand{\existssubseteq}[2]{\exists #1 \!\!\subseteq\!\! #2\,}
        \newcommand{\forallsubseteq}[2]{\forall #1 \!\!\subseteq\!\! #2\,}"""
    ))
    mo.output.clear()
    return


@app.cell(hide_code=True)
def _(mo):
    # jb: include=false
    _foo = False
    mo.md(r"""
    $\LaTeX$ commands:
    ```md
    $$\newcommand{\existsin}[2]{\exists #1 \!\!\in\!\! #2\,}
    \newcommand{\forallin}[2]{\forall #1 \!\!\in\!\! #2\,}
    \newcommand{\existssubseteq}[2]{\exists #1 \!\!\subseteq\!\! #2\,}
    \newcommand{\forallsubseteq}[2]{\forall #1 \!\!\subseteq\!\! #2\,}$$
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The goal of this chapter is to define the axioms of set theory and and the notational shorthands they permit (which will be neccesary for defining probability spaces in the next chapter).

    Set theory is a foundation for nearly all of mathematics, including number theory, functions, topology, algebra, and probability[^other-math-foundations]. Set theory rests on axioms. We use the Zermelo-Frankel axioms along with the axiom of choice, by convention.

    There are many equivalent ways to formulate the ZFC {term}`axioms <axiom>`. We include all 10 for the purpose of explanation. However, the axiom of the null det is often omitted since it is easily proven by applying the axiom schema of separation to filter out elements which are equal to themselves. Additionally, the axiom schema of separation is sometimes omitted since it can be proven using the axiom schema of replacement.

    [^other-math-foundations]: This is because almost every mathematical object can be defined inside set theory, and almost every theorem can be derived from its axioms. However, alternative foundational theories also exist, such as [Category Theory](https://en.wikipedia.org/wiki/Category_theory), which is common in geometry, and [Type Theory](https://en.wikipedia.org/wiki/Type_theory), which is used in theoretical computer science, as well as the theorem prover programming languages [Lean](https://lean-lang.org) and [Rocq](https://rocq-prover.org).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Axiom of **Extensionality**

    If two sets contain the exact same members, then they are equal:

    $$\forall x\forall y\,[\forall z\,(z\in x\leftrightarrow z\in y)\rightarrow x=y].$$

    This axiom supplies uniqueness: if we can show that all sets satisfying some property contain exactly the same members, then by extensionality we know there exists a unique set which satisfies the property.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Axiom of the **Null Set**

    There exists a set $x$ such that for all $y$, $y$ is not an element of $x$:

    $$\exists x \forall y (y \notin x).$$

    By extensionality, there exists a unique $x$ which satisfies this. We call that set the "null set", "empty set", or just use the symbol "$\emptyset$". This is our first example of a *defined term*.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Defined Terms

    In our formal language, the only way to refer to a set is with a variable. However, we're about to write things like $\emptyset \in I$, where $\emptyset$ is a specific set, rather than a variable representing an unknown set. While at first glance this does not seem to meet last chapter's definition of a formula, it's important to explain why this is still legitimate shorthand.

    A *term* is notation that names a set (as opposed to a formula, which makes a claim that is true or false). So far our only term have been variables. However, we can add new terms one *operation* at a time, each justified by a proof that the operation always produces exactly one set.

    **Operations:** Let $\delta(x_1, \dots, x_n, y)$ be a formula. If we have proven

    $$\forall x_1 \cdots \forall x_n\, \exists! y\, \delta(x_1, \dots, x_n, y),$$

    then we may introduce a new notation $F(x_1, \dots, x_n)$, called an *operation*, which stands for "the unique $y$ such that $\delta(x_1, \dots, x_n, y)$." We call $\delta$ the *defining formula* of $F$. When $n = 0$ (such as with $\emptyset$), this is simply a name for one particular set.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Operation**</u>
    If we have proven

    $$\forall x_1 \cdots \forall x_n\, \exists! y\, \delta(x_1, \dots, x_n, y),$$

    for some formula $\delta(x_1, \dots, x_n, y)$, then $F(x_1, \dots, x_n)$ is an operation which stands for "the unique $y$ such that $\delta(x_1, \dots, x_n, y)$" and $\delta$ is called the defining formula of $F$.
    ///

    Just as the axiom of the null set introduces $\emptyset$, each axiom below that asserts the existence of a set introduces its own operation (with extensionality supplying uniqueness of the asserted set):

    - Null set introdues $\emptyset$.
    - Pairing introduces $\{x, y\}$ and $\{x\}$.
    - Power introduces $\mathcal{P}(x)$.
    - Union introduces $\bigcup X$.
    - Separation introduces $\{x \in A: \varphi\}$.
    - Replacement introduces $\{y: \existsin x A\, \varphi\}$.

    *Note:* Infinity and choice also assert the existence of sets, but not of a unique set, so they introduce no operations.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Terms:** *Terms* are built by the following recursive rules:

    1. **Variable:** Every variable is a term.
    2. **Operation:** If $F$ is an operation with $n$ arguments and $t_1, \dots, t_n$ are terms, then $F(t_1, \dots, t_n)$ is a term.
    3. **Closure:** Nothing else is a term.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Term**</u>
    A variable or an operation applied to a term, which represents a set.
    ///

    Since every variable term represents a set, and every operation term is a shorthand for the unique set which satisfies its defining formula, then every term names a single set. This fact is what justifies using $:=$ for sets.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We allow terms on either side of $\in$ and $=$, but a string like $\emptyset \in I$ is then not literally a formula of the formal language. It is shorthand for one, obtained by *unpacking*: if an atomic formula $\alpha$ contains $F(v_1, \dots, v_n)$ where each $v_i$ is a variable, then $\alpha$ abbreviates

    $$\exists z\,\big(\delta_F(v_1, \dots, v_n, z) \land \alpha'\big),$$

    where $z$ is a variable not occurring in $\alpha$, and $\alpha'$ is $\alpha$ with that occurrence of $F(v_1, \dots, v_n)$ replaced by $z$ (renaming bound variables of $\delta_F$ if necessary to avoid clashes). Repeating this, innermost operation first, removes every operation. For example, $\emptyset \in I$ abbreviates $\exists z\,(\forall w\,(w \notin z) \land z \in I)$. When $\alpha$ is $y = F(v_1, \dots, v_n)$ for a variable $y$, the result is equivalent to the simpler $\delta_F(v_1, \dots, v_n, y)$, and we use that instead. Because unique existence has been proven, it would make no difference to use $\forall z\,(\delta_F \rightarrow \alpha')$ in place of the $\exists$ form. So, as with our other abbreviations, anything written with terms can be rewritten without them[^definitional-extension].

    [^definitional-extension]: In logic this device is called an *extension by definitions*. It is *conservative*: anything expressible without the new notation that can be proven with it can also be proven without it. So the notation adds convenience but no new content.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Provisos:** Some notation names a set only under a condition. Function application is the main example: $f(a)$ names a set only when $f$ is a function and $a$ is a first coordinate of some element of $f$ (this is covered in the Axiom of Pairing section). The Replacement set-builder notation below is another, where the condition is the hypothesis of the schema. For such notation we give a *proviso* $D(x_1, \dots, x_n)$ and prove only $\forall x_1 \cdots \forall x_n\,(D \rightarrow \exists! y\, \delta)$. Unpacking then adds $D$ as an extra conjunct (so every atomic formula still unpacks to an honest formula), and we follow the convention of using the notation only where its proviso is known to hold. For terms using such notation, our guarantee that "every term names a single set" only holds at values of the variables where the provisos hold.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Axiom of **Pairing**

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

    where $a$ and $b$ are called the "coordinates"[^kuratowski].

    By extensionality, two ordered pairs are equal iff their corresponding coordinates are equal:

    $$(a, b) = (c, d) \leftrightarrow a = c \land b = d.$$

    [^kuratowski]: There are many ways to define ordered pairs, but we use this one by convetion (called the Kuratowski construction).
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
    ## Axiom of **Union**

    For any set of sets $X$, there exists a set $U$ whose elements are precisely the elements that belong to at least one of the sets contained in $X$:

    $$\forall X\,\exists U\,\forall y\, [y\in U\leftrightarrow \existsin z X (y\in z)].$$

    By Extensionality, this union set $U$ is unique. It is sometimes denoted as $\bigcup X$ or $\bigcup_{w \in X} w$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Union Operator

    The union operator is denoted $\cup$. When placed between two sets $x$ and $y$, it is a shorthand to reference the union of the set containing $x$ and $y$ (whose existence is guaranteed by pairing):

    $$x \cup y := \bigcup \{x, y\}.$$

    Since the pairing set is unordered, this operation is commutative and we have

    $$x \cup y = y \cup x.$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Axiom of **Separation**

    For every formula $\varphi(x, A, p_1, \dots, p_n)$ where $A, p_1, \dots, p_n$ are sets, the following is an axiom:

    For any sets $A, p_1, \dots, p_n$, there exists a set $B$ distinct from $x, A, p_1, \dots, p_n$ (so $B$ is not free in $\varphi$) whose elements are exactly those elements $x$ of $A$ that satisfy $\varphi$:

    $$\forall p_1 \cdots \forall p_n\, \forall A\, \exists B\, \forall x\, [x \in B \leftrightarrow (x \in A \land \varphi)].$$

    In other words, every property definable by a formula carves out a subset of any given set. This is called an axiom schema, rather than a single axiom, because we want Separation to hold for all formulas $\varphi$, so we make an axiom for every $\varphi$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Separation Set-Builder

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
    Additionally, we can take the intersection of a set of sets. Similar to the union, if a set $A$ contains $a_1, a_2, \ldots, a_n$, then we have[^intersection]:

    $$\bigcap A := \{x \in a_1: x \in a_2 \land \cdots \land x \in a_n\}.$$

    [^intersection]: Since intersection is commutative, we could equivalently define:
        $$\bigcap A := a_1 \cup \cdots \cup a_n.$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Axiom of **Replacement**

    For every formula $\varphi(x, y, A, p_1, \dots, p_n)$ where $A, p_1, \dots, p_n$ are sets, the following is an axiom:

    For any sets $A, p_1, \dots, p_n$, if for every $x \in A$ there is exactly one $y$ satisfying $\varphi$, then there exists a set $B$ distinct from $x, y, A, p_1, \dots, p_n$ (so $B$ is not free in $\varphi$) whose elements are exactly those $y$ such that $\varphi$ holds for some $x \in A$:

    $$\forall p_1 \cdots \forall p_n\, \forall A\,[\forallin x A\, \exists! y\, \varphi \rightarrow \exists B\, \forall y\, (y \in B \leftrightarrow \existsin x A\, \varphi)].$$

    In other words, if a formula $\varphi$ assigns to each $x \in A$ exactly one $y$, then the collection of all outputs is also a set. Like Separation, this is a schema because we want it to hold for every formula $\varphi$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Replacement Set-Builder

    We use the following notation to refer to a set whose existence is guaranteed by the axiom schema of replacement:

    $$\{y: \existsin x A\, \varphi\}.$$

    This is only meaningful when the hypothesis of the schema holds, namely $\forallin x A\, \exists! y\, \varphi$. By extensionality, this set is unique.

    Where Separation notation selects elements *of* $A$, this notation collects *outputs*: $y$ is in the set iff $\varphi$ relates it to some $x \in A$. The elements of the resulting set need not be elements of $A$, and different $x$'s may share the same $y$, so the new set can be smaller than $A$.

    Most often, $\varphi$ simply says that $y = t$ for some expression $t$ built from $x$ using notations we have already introduced, such as $\{x\}$, $(x, c)$, or $x \cup \{x\}$. We then write

    $$\{t: x \in A\} := \{y: \existsin x A\, (y = t)\},$$

    where $y$ is a variable that does not occur in $t$. Because each of these expressions exists and is unique for every $x$, the hypothesis $\forallin x A\, \exists! y\, (y = t)$ holds automatically.

    For example, if $A = \{\emptyset, \{\emptyset\}\}$, then

    $$\{\{x\}: x \in A\} = \{\{\emptyset\}, \{\{\emptyset\}\}\}.$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Combined Set-Builder

    Often we want to transform only *some* of the elements of a set. We cannot simply add a filter to $\varphi$, because Replacement requires that *every* $x \in A$ has an output. Instead, we first use Separation to select the elements we want, and then use Replacement on the result. For a formula $\psi$, we write

    $$\{y: \existsin x A\, (\psi \land \varphi)\} := \{y: \existsin x {A'}\, \varphi\}, \quad \text{where } A' = \{x \in A: \psi\}.$$

    The hypothesis of Replacement for $A'$ is equivalent to $\forallin x A\, (\psi \rightarrow \exists! y\, \varphi)$: only the $x$'s satisfying $\psi$ need an output. Unpacking the definitions, $y$ is in this set iff there is some $x \in A$ such that both $\psi$ and $\varphi$ hold.

    As before, when $\varphi$ is $y = t$ for some expression $t$ built from $x$, we abbreviate

    $$\{t: x \in A \land \psi\} := \{y: \existsin x A\, (\psi \land y = t)\}.$$

    This generalizes both earlier notations:

    - If $t$ is $x$ itself, we get $\{x: x \in A \land \psi\}$, which is just $\{x \in A: \psi\}$ from Separation.
    - If $\psi$ is trivially true (such as $x = x$), then $A' = A$ by extensionality, and we recover $\{t: x \in A\}$ from Replacement.

    For example, let $A = \{\emptyset, \{\emptyset\}, \{\{\emptyset\}\}\}$. Separation first gives $A' = \{x \in A: \neg(x = \emptyset)\} = \{\{\emptyset\}, \{\{\emptyset\}\}\}$, and then Replacement wraps each remaining element in braces:

    $$\{\{x\}: x \in A \land \neg(x = \emptyset)\} = \{\{\{\emptyset\}\}, \{\{\{\emptyset\}\}\}\}.$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Axiom of **Power Set**

    For any set $x$, there exists a set $y$ containing precisely all the subsets of $x$:

    $$\forall x\,\exists y\,\forall z\, (z\in y \leftrightarrow z \subseteq x).$$

    This set $y$ is known as the power set of $x$ and is denoted $\mathcal{P}(x)$. By Extensionality, it is unique.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cartesian Product

    For sets $X$ and $Y$, we want to define $X \times Y$ as the set of all ordered pairs $(a, b)$ such that $a \in X \land B \in Y$. To show this is a set, we need a set big enough to contain all such pairs and then use separation to select those we want.

    - If both $a$ and $b$ are in $X \cup Y$, then $\{a\}$ and $\{a, b\}$ are subsets of $X \cup Y$, so they belong to $\mathcal P(X \cup Y)$.

    - Therefore, $\{\{a\}, \{a, b\}\}$ is a subset of $\mathcal P(\mathcal P(X \cup Y))$.

    So we define:

    $$X \times Y := \{z \in \mathcal P(\mathcal P(X \cup Y)): \existsin a X \existsin b Y z = (a, b)\}.$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Relations and Function Sets

    A *relation from $X$ to $Y$* is a subset $R \subseteq X \times Y$. A relation *on* $X$ is a subset of $X \times X$. We write $x \mathrel{R} y$ for $(x, y) \in R$.

    We say $f$ is a *function from $X$ to $Y$*, written $f: X \to Y$, if $f$ is a function (as defined above), $f \subseteq X \times Y$, and every $a \in X$ is a first coordinate of some element of $f$. By power set and separation, the collection of all such functions is a set:


    $$Y^X := \{f \in \mathcal P(X \times Y): f \text{ is a function} \land \forallin a X\, \exists b\, ((a, b) \in f)\}.$$

    For a function $f: X \times X \to Y$ we write $f(a, b)$ for $f((a, b))$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Axiom of **Infinity**

    At least one infinite set $I$ exists. The empty set $\emptyset$ is an element of $I$, and whenever a set $x$ is an element of $I$, so is $x \cup \{x\}$:

    $$\exists I\, [\emptyset \in I \land \forall x\, (x \in I \rightarrow x \cup \{x\} \in I)].$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Natural Numbers

    We call $x \cup \{x\}$ the *successor* of $x$, and we use the notation:

    $$\text{succ}(x) := x \cup \{x\}.$$

    We call a set $I$ *inductive* if it satisfies the formula

    $$\emptyset \in I \land \forall x\, (x \in I \rightarrow \text{succ}(I) \in I).$$

    The axiom of infinity guarantees that at least one such set exists.

    For convenience, we use the notation:

    $$\text{inductive}(I) := \emptyset \in I \land \forall x\, (x \in I \rightarrow \text{succ}(x) \in I).$$

    Let $J$ be an inductive set (so that it satisfies $\text{inductive}(J)$). We define the natural numbers as:

    $$\mathbb N := \{x \in J: \forall I(\text{inductive}(I) \rightarrow x \in I)\}.$$

    This guarantees that $\mathbb N$ contains exactly:

    $$\begin{align*}
    0 &:= \emptyset \\
    1 &:= \{\emptyset\} \\
    2 &:= \{\emptyset, \{\emptyset\}\} \\
    3 &:= \{\emptyset, \{\emptyset\}, \{\emptyset, \{\emptyset\}\}\} \\
    &\ \ \ \vdots
    \end{align*}$$

    Where each successive number is obtained by the successor operation and is defined as the set containing all smaller numbers.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Peano Arithmetic

    From here, we can recover the axioms of Peano Arithmetic:

    - Existence of zero and closure under succession:
      $$0 \in \mathbb N \land x \in \mathbb N \rightarrow \text{succ}(x) \in \mathbb N.$$
    - Injectivity of succession:
      $$\text{succ}(x) = \text{succ}(y) \rightarrow x = y.$$
    - Zero not a successor:
      $$\neg \exists x \text{succ}(x) = 0.$$
    - Induction:
      $$\text{inductive}(x) \rightarrow \mathbb N \subseteq x.$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Recursion on the Natural Numbers

    The Peano axioms tell us what $\mathbb N$ looks like, but not how to define functions out of it. For that we need recursion.

    ::::{admonition icon=false} 📖 **Theorem (Recursion)**
    Let $A$ be a set, $a \in A$, and $g: A \to A$. Then there is exactly one function $h: \mathbb N \to A$ with $h(0) = a$ and $h(\text{succ}(n)) = g(h(n))$ for all $n \in \mathbb N$.
    ::::

    *Proof.* Call $p \subseteq \mathbb N \times A$ *closed* if $(0, a) \in p$ and $(n, x) \in p \rightarrow (\text{succ}(n), g(x)) \in p$. Closed sets exist ($\mathbb N \times A$ is one), so let

    $$h := \{z \in \mathbb N \times A: \forall p \in \mathcal P(\mathbb N \times A)\, (p \text{ closed} \rightarrow z \in p)\}$$

    be the intersection of all of them. Then $h$ is itself closed, and it is contained in every closed set. We show that for every $n$ there is exactly one $x$ with $(n, x) \in h$, by induction on $n$ (that is, we show $\{n \in \mathbb N : \exists! x\, (n, x) \in h\}$ is inductive).

    - *Base.* $(0, a) \in h$. If also $(0, x) \in h$ with $x \neq a$, then $h \setminus \{(0, x)\}$ is closed (no $(\text{succ}(n), g(y))$ has first coordinate $0$), contradicting minimality of $h$.
    - *Step.* Suppose $(n, y)$ is the unique pair in $h$ with first coordinate $n$. Then $(\text{succ}(n), g(y)) \in h$. If also $(\text{succ}(n), z) \in h$ with $z \neq g(y)$, then $h \setminus \{(\text{succ}(n), z)\}$ is closed: if $(m, w)$ remains and $(\text{succ}(m), g(w)) = (\text{succ}(n), z)$, injectivity of succ gives $m = n$, uniqueness at $n$ gives $w = y$, so $z = g(y)$, a contradiction. Again this contradicts minimality.

    So $h$ is a function $\mathbb N \to A$ satisfying the recursion. If $h'$ is another, it is closed, so $h \subseteq h'$, and two functions with the same domain, one contained in the other, are equal. $\square$

    ### Arithmetic and Order on $\mathbb N$

    For each $m \in \mathbb N$, recursion with $A = \mathbb N$, $a = m$, $g = \text{succ}$ gives a unique $h_m$, and we define

    $$m + n := h_m(n), \quad\text{so}\quad m + 0 = m, \quad m + \text{succ}(n) = \text{succ}(m + n).$$

    Likewise recursion with $a = 0$ and $g(x) = x + m$ gives

    $$m \cdot 0 = 0, \qquad m \cdot \text{succ}(n) = m \cdot n + m.$$

    By replacement these assemble into functions $+, \cdot: \mathbb N \times \mathbb N \to \mathbb N$. These are notations with proviso $m, n \in \mathbb N$, in the sense of the Provisos section. Finally, $m < n$ means $m \in n$, and $m \le n$ means $m \in n \lor m = n$.

    ::::{admonition icon=false} 📖 **Proposition**
    For all $a, b, c \in \mathbb N$:

    1. $+$ and $\cdot$ are associative and commutative; $a + 0 = a$ and $a \cdot 1 = a$.
    2. $a \cdot (b + c) = a \cdot b + a \cdot c$.
    3. (Cancellation) $a + c = b + c \rightarrow a = b$.
    4. (No zero divisors) $a \cdot b = 0 \rightarrow a = 0 \lor b = 0$.
    5. $<$ is a strict total order: exactly one of $a < b$, $a = b$, $b < a$ holds.
    6. $a < b \rightarrow a + c < b + c$, and $a < b \land 0 < c \rightarrow a c < b c$.
    7. (Well-ordering) Every nonempty subset of $\mathbb N$ has a least element.
    ::::

    Each is a routine proof by induction, which we omit[^arithmetic-proofs].

    [^arithmetic-proofs]: See Enderton, *Elements of Set Theory*, Chapter 4, or Landau, *Foundations of Analysis*.

    ### Equivalence Relations and Quotients

    ::::{admonition icon=false} 📖 **Definition**
    :::{glossary}
    Equivalence relation
    : A relation $\sim$ on a set $X$ that is reflexive ($x \sim x$), symmetric ($x \sim y \rightarrow y \sim x$), and transitive ($x \sim y \land y \sim z \rightarrow x \sim z$).
    :::
    ::::

    For an equivalence relation $\sim$ on $X$, the *equivalence class* of $x$ is $[x] := \{y \in X : y \sim x\}$ and the *quotient* is

    $$X/{\sim} := \{[x]: x \in X\},$$

    which is a set by replacement. Then $[x] = [y] \leftrightarrow x \sim y$. (If $x \sim y$, then $z \sim x \leftrightarrow z \sim y$ by symmetry and transitivity, so the classes are equal by extensionality. Conversely $x \in [x]$ by reflexivity, so $[x] = [y]$ gives $x \in [y]$.)

    To define an operation on classes by choosing representatives, we must check that the answer doesn't depend on the choice.

    ::::{admonition icon=false} 📖 **Lemma (Well-definedness)**
    Let $*: X \times X \to X$ be *compatible* with $\sim$, meaning $x \sim x' \land y \sim y' \rightarrow x * y \sim x' * y'$. Then there is a unique function $\oplus: (X/{\sim}) \times (X/{\sim}) \to X/{\sim}$ with $[x] \oplus [y] = [x * y]$. Similarly, a relation $\preceq$ on $X$ with $x \sim x' \land y \sim y' \land x \preceq y \rightarrow x' \preceq y'$ induces a relation on $X/{\sim}$ by $[x] \le [y] :\leftrightarrow x \preceq y$.
    ::::

    *Proof.* Take $\oplus := \{(([x], [y]), [x * y]): (x, y) \in X \times X\}$ (a set by replacement). It is a function because if $[x] = [x']$ and $[y] = [y']$ then $x \sim x'$ and $y \sim y'$, so $[x * y] = [x' * y']$ by compatibility. It is defined on every pair of classes by construction. The statement for relations is similar. $\square$

    ### Integers

    We want a set of integers, but so far we have no subtraction. Instead we use ordered pairs $(a, b) \in \mathbb N \times \mathbb N$, thought of informally as the difference $a - b$ (a conceptual aid only; nothing is defined yet). Two pairs should represent the same difference when

    $$(a, b) \sim (c, d) :\leftrightarrow a + d = b + c.$$

    ::::{admonition icon=false} 📖 **Proposition**
    $\sim$ is an equivalence relation on $\mathbb N \times \mathbb N$.
    ::::

    *Proof.* Reflexivity and symmetry follow from commutativity of $+$. For transitivity, suppose $a + d = b + c$ and $c + f = d + e$. Adding gives $(a + f) + (c + d) = (b + e) + (c + d)$, and cancellation gives $a + f = b + e$. $\square$

    Define $\mathbb Z := (\mathbb N \times \mathbb N)/{\sim}$, so $[x] = \{y \in \mathbb N \times \mathbb N: y \sim x\}$ as before. Guided by $a - b$, define on representatives

    $$(a, b) + (c, d) := (a + c,\, b + d), \qquad (a, b) \cdot (c, d) := (ac + bd,\, ad + bc),$$
    $$-(a, b) := (b, a), \qquad (a, b) \preceq (c, d) :\leftrightarrow a + d \le b + c.$$

    Each is compatible with $\sim$, so by the Well-definedness Lemma they induce operations and an order on $\mathbb Z$. For example, for multiplication it suffices to vary one argument at a time. If $(a, b) \sim (a', b')$, let $s := a + b' = b + a'$. Then

    $$(ac + bd) + (a'd + b'c) = c(a + b') + d(b + a') = (c + d)s = d(a + b') + c(b + a') = (ad + bc) + (a'c + b'd),$$

    which says $(ac + bd,\, ad + bc) \sim (a'c + b'd,\, a'd + b'c)$. The other checks are similar.

    Let $0 := [(0, 0)]$, $1 := [(1, 0)]$, and $\iota(n) := [(n, 0)]$.

    ::::{admonition icon=false} 📖 **Proposition**
    1. $\mathbb Z$ is a commutative ring with identity: $+$ and $\cdot$ are associative and commutative, $\cdot$ distributes over $+$, $x + 0 = x$, $x \cdot 1 = x$, and $x + (-x) = 0$.
    2. $\mathbb Z$ has no zero divisors: $xy = 0 \rightarrow x = 0 \lor y = 0$.
    3. $\le$ is a total order compatible with $+$, and with $\cdot$ by positive elements.
    4. $\iota: \mathbb N \to \mathbb Z$ is injective, preserves $+$, $\cdot$ and $\le$, and every integer is $\iota(n)$ or $-\iota(n)$ for some $n \in \mathbb N$.
    ::::

    Each statement reduces to the corresponding fact about $\mathbb N$. Since $\iota$ is an order- and arithmetic-preserving injection, we *identify* $n$ with $\iota(n)$ and regard $\mathbb N \subseteq \mathbb Z$[^identification]. With $x - y := x + (-y)$, we then have $[(a, b)] = a - b$, which justifies the original intuition.

    [^identification]: Strictly speaking $\mathbb N \not\subseteq \mathbb Z$, since $\iota(n)$ is an equivalence class of pairs, not $n$. Identifying $n$ with $\iota(n)$ is harmless, because everything we say about $\mathbb N$ transfers along $\iota$. Alternatively, one can replace $\mathbb Z$ by an isomorphic copy in which $\mathbb N$ literally is a subset. The same remark applies to the inclusions $\mathbb Z \subseteq \mathbb Q \subseteq \mathbb R$ below.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Integers

    We want to build the set of all integers $\mathbb I$, but so far we don't have a notion of subtraction. To get around this, we use odered pairs $(a, b)$, where, informaly, we think of them as the difference $a - b$ (note that this is soley a conceptual aid for now and doesn't actually mean anything yet, since we haven't defined subtraction). We define the equivalence operation between ordered pairs:

    $$(a, b) \sim (c, d) := a + d = b + c.$$

    We define the notation:

    $$[x] := \{y \in \mathbb N \times \mathbb N : y \sim x\}.$$

    Then, we define:

    $$\mathbb Z := \{[x]: x \in \mathbb N \times \mathbb N\}.$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Rational Numbers

    The idea is the same, with division in place of subtraction. We think of a pair $(a, b)$ as the fraction $a / b$, which requires $b \neq 0$. Let $\mathbb Z^* := \{x \in \mathbb Z: \neg(x = 0)\}$ and define a relation on $\mathbb Z \times \mathbb Z^*$ by

    $$(a, b) \approx (c, d) :\leftrightarrow a d = b c.$$

    ::::{admonition icon=false} 📖 **Proposition**
    $\approx$ is an equivalence relation on $\mathbb Z \times \mathbb Z^*$.
    ::::

    *Proof.* Reflexivity and symmetry follow from commutativity. For transitivity, suppose $ad = bc$ and $cf = de$. Then $d(af) = (ad)f = (bc)f = b(cf) = b(de) = d(be)$. Since $d \neq 0$ and $\mathbb Z$ has no zero divisors, $af = be$. $\square$

    (This is exactly where we need $\mathbb Z$ to have no zero divisors.)

    Define $\mathbb Q := (\mathbb Z \times \mathbb Z^*)/{\approx}$ and write $a/b := [(a, b)]$, so that $a/b = c/d \leftrightarrow ad = bc$. Define on representatives

    $$\frac ab + \frac cd := \frac{ad + bc}{bd}, \qquad \frac ab \cdot \frac cd := \frac{ac}{bd}, \qquad -\frac ab := \frac{-a}{b}, \qquad \Big(\frac ab\Big)^{-1} := \frac ba \ \ (a \neq 0).$$

    These make sense because $b, d \neq 0$ implies $bd \neq 0$. Compatibility with $\approx$ is a direct check. For addition, if $ab' = a'b$ then

    $$(ad + bc)\,b'd = ab'd^2 + bb'cd = a'bd^2 + bb'cd = bd\,(a'd + b'c).$$

    For order, note every class has a representative with positive denominator, since $(a, b) \approx (-a, -b)$. For such representatives define $a/b \le c/d :\leftrightarrow ad \le bc$, which is again compatible.

    ::::{admonition icon=false} 📖 **Proposition**
    1. $\mathbb Q$ is a *field*: a commutative ring with identity $1 = 1/1$ in which every $x \neq 0$ has a multiplicative inverse.
    2. $\le$ is a total order compatible with $+$ and with $\cdot$ by positive elements.
    3. $\iota: \mathbb Z \to \mathbb Q$, $\iota(a) := a/1$, is injective and preserves $+$, $\cdot$ and $\le$.
    4. (Density) If $p < q$ in $\mathbb Q$, then $p < \frac{p + q}{1 + 1} < q$.
    ::::

    As before, we identify $a$ with $a/1$ and regard $\mathbb Z \subseteq \mathbb Q$.

    ### Incompleteness of $\mathbb Q$

    $\mathbb Q$ has no gaps in the sense of density, but it does have holes.

    ::::{admonition icon=false} 📖 **Proposition**
    There is no $q \in \mathbb Q$ with $q \cdot q = 2$.
    ::::

    *Proof.* Suppose $q = a/b$ with $a, b \in \mathbb N$ and $b > 0$ (we may replace $q$ by $-q$) and $a^2 = 2b^2$. By well-ordering, choose such a pair with $b$ least. Since the square of an odd number is odd, $a$ is even, say $a = 2k$. Then $4k^2 = 2b^2$, so $b^2 = 2k^2$, so $b$ is even, say $b = 2c$, and $k^2 = 2c^2$ with $0 < c < b$, contradicting minimality of $b$. $\square$

    So the set $\{q \in \mathbb Q: q < 0 \lor q \cdot q < 2\}$ has no least upper bound in $\mathbb Q$. The real numbers are built to fill such holes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Real Numbers

    We construct $\mathbb R$ using *Dedekind cuts*[^cauchy]. The idea is to identify a real number $x$ with the set of rationals below it, $\{q \in \mathbb Q: q < x\}$, and then take that set to *be* the number.

    ::::{admonition icon=false} 📖 **Definition**
    :::{glossary}
    Dedekind cut
    : A set $\alpha \subseteq \mathbb Q$ such that (1) $\alpha \neq \emptyset$ and $\alpha \neq \mathbb Q$; (2) $\alpha$ is *downward closed*: $p \in \alpha \land q < p \rightarrow q \in \alpha$; and (3) $\alpha$ has no greatest element: $p \in \alpha \rightarrow \existsin q \alpha\, (p < q)$.
    :::
    ::::

    We define

    $$\mathbb R := \{\alpha \in \mathcal P(\mathbb Q): \alpha \text{ is a Dedekind cut}\},$$

    which is a set by power set and separation. For $r \in \mathbb Q$, let $r^* := \{q \in \mathbb Q: q < r\}$. This is a cut: it contains $r - 1$, omits $r$, is downward closed, and has no greatest element since $q < \frac{q + r}{1 + 1} < r$. The cut $\{q \in \mathbb Q: q < 0 \lor q \cdot q < 2\}$ is a real number ($\sqrt 2$) that, by the proposition above, is not of the form $r^*$.

    **Order.** For cuts, define $\alpha \le \beta :\leftrightarrow \alpha \subseteq \beta$.

    ::::{admonition icon=false} 📖 **Proposition**
    $\le$ is a total order on $\mathbb R$.
    ::::

    *Proof.* Reflexivity and transitivity are clear, and antisymmetry is extensionality. For totality, suppose $\alpha \not\subseteq \beta$ and pick $p \in \alpha \setminus \beta$. If $q \in \beta$ and $q \ge p$, downward closure would put $p \in \beta$; so every $q \in \beta$ satisfies $q < p$, hence $q \in \alpha$ since $p \in \alpha$. So $\beta \subseteq \alpha$. $\square$

    **Completeness.** This is the property $\mathbb Q$ lacks.

    ::::{admonition icon=false} 📖 **Theorem (Least upper bound property)**
    Every nonempty $S \subseteq \mathbb R$ that is bounded above has a least upper bound, namely $\sigma := \bigcup S$.
    ::::

    *Proof.* Let $\beta$ be an upper bound of $S$. The set $\sigma$ exists by the axiom of union. It is a cut: it is nonempty because $S$ has a member and every cut is nonempty; $\sigma \subseteq \beta \neq \mathbb Q$ gives $\sigma \neq \mathbb Q$; if $p \in \alpha \in S$ and $q < p$ then $q \in \alpha \subseteq \sigma$; and if $p \in \alpha \in S$, there is $q \in \alpha \subseteq \sigma$ with $q > p$. Clearly $\alpha \subseteq \sigma$ for every $\alpha \in S$, so $\sigma$ is an upper bound. If $\gamma$ is any upper bound, then every $\alpha \in S$ satisfies $\alpha \subseteq \gamma$, so $\sigma \subseteq \gamma$. $\square$

    **Arithmetic.** Define

    $$\alpha + \beta := \{p + q: (p, q) \in \alpha \times \beta\} \quad\text{(by replacement)}, \qquad 0^* = \{q \in \mathbb Q : q < 0\},$$
    $$-\alpha := \{p \in \mathbb Q: \existsin r {\mathbb Q}\,(r > 0 \land -p - r \notin \alpha)\}.$$

    For example, $\alpha + \beta$ is a cut: it is nonempty; if $r \notin \alpha$ and $s \notin \beta$ then $r + s \notin \alpha + \beta$, because downward closure forces every $p \in \alpha$ to satisfy $p < r$ and every $q \in \beta$ to satisfy $q < s$; it is downward closed because $t < p + q$ gives $t = (t - q) + q$ with $t - q \in \alpha$; and it has no greatest element because $\alpha$ and $\beta$ do not.

    For multiplication, first take $\alpha, \beta > 0^*$ and set

    $$\alpha \cdot \beta := \{p \in \mathbb Q: \existsin r \alpha \existsin s \beta\,(r > 0 \land s > 0 \land p \le rs)\}.$$

    Then put $\alpha \cdot 0^* = 0^* \cdot \alpha := 0^*$, and extend to other signs by the rules $\alpha \cdot \beta := -(\alpha \cdot (-\beta))$ if $\alpha > 0^* > \beta$, similarly with the roles swapped, and $\alpha \cdot \beta := (-\alpha)(-\beta)$ if both are negative. For $\alpha > 0^*$ the inverse is

    $$\alpha^{-1} := \{p \in \mathbb Q: p \le 0 \lor (p > 0 \land \existsin r {\mathbb Q}\,(r > 1 \land (pr)^{-1} \notin \alpha))\},$$

    with the sign rule for negative $\alpha$.

    ::::{admonition icon=false} 📖 **Theorem**
    $(\mathbb R, +, \cdot, 0^*, 1^*, \le)$ is a totally ordered field with the least upper bound property, and $\iota: \mathbb Q \to \mathbb R$, $\iota(r) := r^*$, is injective and preserves $+$, $\cdot$ and $\le$.
    ::::

    The verifications are long but elementary, and each follows from the corresponding fact for $\mathbb Q$[^rudin]. As before, we identify $r$ with $r^*$, so that

    $$\mathbb N \subseteq \mathbb Z \subseteq \mathbb Q \subseteq \mathbb R.$$

    [^cauchy]: The other standard construction takes equivalence classes of Cauchy sequences $\mathbb N \to \mathbb Q$ under the relation "the difference tends to $0$". It uses the quotient lemma again, and it generalizes to completing arbitrary metric spaces. Dedekind cuts need no functions or sequences and make order and suprema immediate.

    [^rudin]: See Rudin, *Principles of Mathematical Analysis*, Chapter 1 (Appendix), or Enderton, *Elements of Set Theory*, Chapter 5.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Axiom of **Regularity**

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
    ## Axiom of **Choice**

    For any set $X$ whose members are nonempty, pairwise disjoint sets, there exists a set $C$ that contains exactly one element from each member of $X$:

    $$\forall X\,\big[\big(\forall A \in X\,\exists y\,(y \in A) \;\land\; \forall A \in X\,\forall B \in X\,(\neg(A = B) \rightarrow \neg\exists z\,(z \in A \land z \in B))\big) \rightarrow \exists C\,\forall A \in X\,\exists! z\,(z \in A \land z \in C)\big].$$

    The set $C$ is called a choice set or selector for $X$. Unlike the other axioms, Choice asserts that a set exists without giving any rule for constructing it. Informally, it lets us make infinitely many arbitrary selections at once. It is equivalent to several other well-known statements, such as the Well-Ordering Theorem, Zorn’s Lemma, and “every product of nonempty sets is nonempty.”

    Note: The version above (disjoint sets) is one of many equivalent formulations. Another common one says that for every collection of nonempty sets there exists a function that picks an element from each. Once we define functions in terms of sets, this is easy to state, but the disjoint-sets form can be written directly in the language of $\in$ and $=$.
    """)
    return


if __name__ == "__main__":
    app.run()
