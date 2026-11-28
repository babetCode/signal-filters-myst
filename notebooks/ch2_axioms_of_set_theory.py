# /// script
# dependencies = [
#     "marimo>=0.25.1",
#     "matplotlib==3.11.2",
#     "numpy==2.5.3",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="2. Axioms of Set Theory", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "From Axioms to Natural Numbers"
    abbreviations:
      iff: if and only if
      diff: null
      ZFC: Zermelo–Fraenkel set theory with the Axiom of Choice
      EMA: exponential moving average
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
    import matplotlib.pyplot as plt
    from textwrap import dedent

    return dedent, mo, np, plt


@app.cell
def display_settings(dedent, mo, plt):
    # jb: include=false
    plt.style.use("default")

    def graphic(x):
        return mo.Html(dedent(f'''\
            <div class="graphic">
                {mo.as_html(x)}
            </div>
            '''))

    return (graphic,)


@app.cell
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
    mo.md(r"""
    /// important | 🔗 **Prerequisites**
        attrs: {class: no-icon}
    - [Chapter 1](ch1_language_of_logic.md): statements and predicates; the connectives $\neg, \land, \lor, \rightarrow, \leftrightarrow$; the quantifiers $\forall$, $\exists$, $\exists!$ and the bounded forms $\forallin{x}{A}$, $\existsin{x}{A}$; the notations $:=$ (defining an object) and $:\Longleftrightarrow$ (defining a property); and the proof techniques (direct proof, contradiction, cases, proving $\leftrightarrow$ in two directions).
    - [Appendix A](appendix_a_formal_logic.md) (optional): the formal language behind the notation of this chapter.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Every filter in this book is a *recursion*: it computes the {term}`estimate` $\hat x_k$ from the previous estimate $\hat x_{k-1}$ and the newest measurement $z_k$, for $k = 1, 2, 3, \ldots$ The Introduction's cumulative average is one example:

    $$\hat x_k = \hat x_{k-1} + \tfrac1k\,(z_k - \hat x_{k-1}).$$

    Writing "and so on" is easy. Proving that such a rule defines exactly one estimate for *every* step $k$ is not, because it needs precise notions of the steps $k$ (the natural numbers), of "a value for every step" (a function), and of the pairs $(k, \hat x_k)$ that make up such a function. This chapter builds all three from the axioms of Zermelo–Fraenkel set theory with the Axiom of Choice (ZFC). It ends with the Recursion Theorem: an initial value and an update rule determine exactly one sequence[^sequence-informal] of estimates. Everything later in the book rests on the same foundation; for example, the probabilities of [Chapter 4](ch4_probability_spaces.md) are functions whose inputs are sets.

    [^sequence-informal]: Used informally here; *sequence* is defined precisely in [Chapter 3](ch3_sets_for_probability.md).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    Every object in this book (numbers, pairs, functions, signals, probabilities) is a set, built by a small number of axioms. The payoff comes at the end of the chapter: the Recursion Theorem proves that an update rule $\hat x_k = G(k, \hat x_{k-1})$ and an initial value $\hat x_0$ define exactly one estimate for every step $k$.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Sets and Membership

    Informally, a *set* is a collection of objects, called its *elements* (or *members*). We write $x \in A$ for "$x$ is an element of $A$" and $x \notin A$ for $\neg(x \in A)$.

    Neither "set" nor "is an element of" gets a glossary entry. A {term}`definition` is a necessary-and-sufficient test stated in words that were defined earlier, and these are the first words of the theory: there are no earlier words to define them with. They are *primitive notions*. We never say what a set *is*; the axioms below say only how sets behave, and every other term in the book is defined, directly or indirectly, from $\in$ and $=$ using the logic of [Chapter 1](ch1_language_of_logic.md).

    Two conventions follow. First, everything is a set: numbers, ordered pairs, functions, and signals will all be particular sets, and every variable in this chapter stands for a set. Second, $a = b$ means that $a$ and $b$ are the same set, so equal sets have exactly the same properties. That is a law of logic, not an axiom.

    The first defined notion compares two sets by their elements.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Subset**</u>

    A set $A$ is a subset of a set $B$, written $A \subseteq B$, iff every element of $A$ is an element of $B$:
    $$A \subseteq B \;:\Longleftrightarrow\; \forallin{x}{A}\,(x \in B).$$
    ///

    For example, $A \subseteq A$ for every set $A$; and if $A \subseteq B$ and $B \subseteq C$, then $A \subseteq C$ (if $x \in A$, then $x \in B$, so $x \in C$). Being a subset ($\subseteq$) and being an element ($\in$) are different relations; examples follow once we can build sets.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Axioms of ZFC

    Why axioms at all? The naive rule "every property defines a set" is contradictory, as we prove under Separation below. Zermelo–Fraenkel set theory replaces that rule with ten specific set-building {term}`axioms <axiom>`[^zfc-variants], each a sentence about $\in$ and $=$, which mathematicians assume to be free of contradictions[^zfc-consistency]. For each axiom we give it in words, then in symbols, and then define the notation it justifies, immediately, so that nothing is used before it is introduced.

    | # | Axiom | What it provides |
    |---|---|---|
    | 1 | Extensionality | sets with the same elements are equal, so names are unambiguous |
    | 2 | Empty Set | $\emptyset$ |
    | 3 | Pairing | $\{a, b\}$ and $\{a\}$ |
    | 4 | Union | $\bigcup F$ and $A \cup B$ |
    | 5 | Separation | $\{x \in A : \varphi(x)\}$, $A \cap B$, $\bigcap F$, $A \setminus B$ |
    | 6 | Power Set | $\mathcal P(A)$ |
    | 7 | Replacement | $\{t(x) : x \in A\}$ |
    | 8 | Infinity | an inductive set, and from it the natural numbers $\mathbb N$ |
    | 9 | Regularity | no set is an element of itself |
    | 10 | Choice | a choice set for any family of nonempty sets that share no elements |

    [^zfc-variants]: Formulations of ZFC differ slightly. Empty Set is often omitted because it follows from Separation applied to any set (for example, the one provided by Infinity) with the predicate $x \neq x$, and Separation is sometimes omitted because it follows from Replacement and Empty Set. We list all ten because each one justifies notation. Set theory is also not the only possible foundation: [category theory](https://en.wikipedia.org/wiki/Category_theory) and [type theory](https://en.wikipedia.org/wiki/Type_theory) are alternatives, and type theory underlies proof assistants such as [Lean](https://lean-lang.org) and [Rocq](https://rocq-prover.org).

    [^zfc-consistency]: By Gödel's second incompleteness theorem, ZFC cannot prove its own consistency unless it is inconsistent, so this is an assumption, shared by nearly all of mathematics. See [Appendix A: The Metatheory](appendix_a_formal_logic.md).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1. Extensionality

    **In words.** Two sets with the same elements are equal.

    **In symbols.**

    $$\forall A\,\forall B\,\big[\forall x\,(x \in A \leftrightarrow x \in B) \rightarrow A = B\big].$$

    The converse (equal sets have the same elements) is a law of logic. So a set is completely determined by its elements; the order and repetition in a listing play no role.

    **What it builds.** Extensionality creates no sets, but it makes names unambiguous.

    /// important | 📐 **Lemma (Uniqueness)**
        attrs: {class: no-icon}
    Let $\psi(x)$ be a predicate (it may mention other sets as parameters). There is at most one set $A$ whose elements are exactly the sets satisfying $\psi$, that is, with $\forall x\,\big(x \in A \leftrightarrow \psi(x)\big)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Suppose $A$ and $A'$ both have this property. Then for every $x$, $x \in A \leftrightarrow \psi(x) \leftrightarrow x \in A'$, so $A = A'$ by Extensionality. $\blacksquare$
    ///

    Every axiom below that creates a set says "there is a set $A$ with $\forall x\,(x \in A \leftrightarrow \psi(x))$" for some predicate $\psi$. By the Uniqueness Lemma that set is unique, so we may give it a name, such as $\emptyset$ or $\{a, b\}$, introduced with $:=$. A name introduced this way is pure shorthand: every statement that uses it can be rewritten as a statement about $\in$ and $=$ alone, and the name makes no new theorems provable. In logic this is called an *extension by definitions*. [Appendix A: Extension by Definitions](appendix_a_formal_logic.md) gives the precise rules, including the rules for notation that names a set only under a stated condition (a *proviso*), such as the function value $f(a)$ defined later in this chapter.

    The most common way to use Extensionality is the following.

    /// important | 📐 **Lemma (Double Inclusion)**
        attrs: {class: no-icon}
    For all sets $A$ and $B$: $A = B \leftrightarrow (A \subseteq B \land B \subseteq A)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    ($\rightarrow$) Every set is a subset of itself. ($\leftarrow$) If $A \subseteq B$ and $B \subseteq A$, then for every $x$ both $x \in A \rightarrow x \in B$ and $x \in B \rightarrow x \in A$ hold, that is, $x \in A \leftrightarrow x \in B$. By Extensionality, $A = B$. $\blacksquare$
    ///

    To prove that two sets are equal, then, we show either that they have the same elements or that each is a subset of the other.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2. Empty Set

    **In words.** There is a set with no elements.

    **In symbols.**

    $$\exists A\,\forall x\,(x \notin A).$$

    **What it builds.** A set with no elements is a set $A$ with $\forall x\,(x \in A \leftrightarrow x \neq x)$, since $x \neq x$ is never true. By the Uniqueness Lemma there is exactly one such set.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Empty set**</u>

    The empty set $\emptyset$ is the unique set with no elements:
    $$\forall x\,(x \notin \emptyset).$$
    ///

    The empty set is a subset of every set: $\emptyset \subseteq A$ says $\forallin{x}{\emptyset}\,(x \in A)$, which is vacuously true because there is no $x \in \emptyset$ (recall the conditional in [Chapter 1](ch1_language_of_logic.md)). A set $A$ is *nonempty* iff $A \neq \emptyset$. By Extensionality, this holds iff $A$ has at least one element: a set with no elements has the same elements as $\emptyset$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3. Pairing

    **In words.** For any sets $a$ and $b$, there is a set whose elements are exactly $a$ and $b$.

    **In symbols.**

    $$\forall a\,\forall b\,\exists P\,\forall x\,\big(x \in P \leftrightarrow (x = a \lor x = b)\big).$$

    **What it builds.** By the Uniqueness Lemma the set $P$ is unique. We name it $\{a, b\}$, and we define the *singleton* $\{a\} := \{a, a\}$. Thus

    $$x \in \{a, b\} \leftrightarrow (x = a \lor x = b), \qquad x \in \{a\} \leftrightarrow x = a.$$

    Since $x = a \lor x = b$ and $x = b \lor x = a$ are logically equivalent, $\{a, b\}$ and $\{b, a\}$ have the same elements, so $\{a, b\} = \{b, a\}$: sets built by Pairing are *unordered*. Ordered pairs are built from them under Building Blocks below.

    Starting from $\emptyset$ alone, Pairing already produces new sets. For example, $\emptyset \neq \{\emptyset\}$, because $\emptyset \in \{\emptyset\}$ but $\emptyset \notin \emptyset$. These sets also show that $\in$ and $\subseteq$ differ: $\{\emptyset\} \in \{\{\emptyset\}\}$, but $\{\emptyset\} \not\subseteq \{\{\emptyset\}\}$, because the element $\emptyset$ of $\{\emptyset\}$ is not an element of $\{\{\emptyset\}\}$ (its only element is $\{\emptyset\} \neq \emptyset$).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4. Union

    **In words.** For any set $F$, there is a set whose elements are exactly the elements of the elements of $F$.

    **In symbols.**

    $$\forall F\,\exists U\,\forall x\,\big(x \in U \leftrightarrow \existsin{A}{F}\,(x \in A)\big).$$

    **What it builds.** By the Uniqueness Lemma the set $U$ is unique.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Union**</u>

    The union of a set $F$ is the unique set $\bigcup F$ whose elements are the elements of the elements of $F$:
    $$x \in \bigcup F \;\leftrightarrow\; \existsin{A}{F}\,(x \in A).$$
    The union of two sets $A$ and $B$ is $A \cup B := \bigcup \{A, B\}$.
    ///

    /// important | 📐 **Lemma (Binary Union)**
        attrs: {class: no-icon}
    For all sets $A$, $B$, and $x$: $x \in A \cup B \leftrightarrow (x \in A \lor x \in B)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    By definition, $x \in \bigcup\{A, B\}$ iff $x \in C$ for some $C \in \{A, B\}$, that is, for some $C$ with $C = A$ or $C = B$. This holds iff $x \in A$ or $x \in B$. $\blacksquare$
    ///

    Because $\lor$ is commutative and associative, so is $\cup$: $A \cup B = B \cup A$ and $(A \cup B) \cup C = A \cup (B \cup C)$, since in each case both sides have the same elements. For any sets $a$, $b$, $c$, the set $\bigcup\{\{a, b\}, \{b, c\}\} = \{a, b\} \cup \{b, c\}$ has exactly the elements $a$, $b$, $c$. At the other extreme, $\bigcup \emptyset = \emptyset$, because no $A \in \emptyset$ contributes elements.

    **Roster notation.** Pairing and Union together let us list sets explicitly: $\{a, b, c\} := \{a, b\} \cup \{c\}$, then $\{a, b, c, d\} := \{a, b, c\} \cup \{d\}$, and so on for any list written out in full. By the Lemma, $x \in \{a, b, c\} \leftrightarrow (x = a \lor x = b \lor x = c)$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 5. Separation

    **In words.** For any set $A$ and any predicate $\varphi(x)$, the elements of $A$ that satisfy $\varphi$ form a set.

    **In symbols.** For each {term}`predicate` $\varphi(x, p_1, \ldots, p_n)$ in which the letter $B$ does not occur (formally, each {term}`formula`; see [Appendix A: Formal Syntax](appendix_a_formal_logic.md)), the following is an axiom:

    $$\forall p_1 \cdots \forall p_n\,\forall A\,\exists B\,\forall x\,\big(x \in B \leftrightarrow (x \in A \land \varphi(x, p_1, \ldots, p_n))\big).$$

    The sets $p_1, \ldots, p_n$ are *parameters*: they let $\varphi$ refer to other sets. Separation is an *axiom schema*, one axiom for each predicate, because "for every predicate $\varphi$" is not a statement about sets and cannot be written inside the logic of Chapter 1.

    **What it builds.** By the Uniqueness Lemma the set $B$ is unique. We write it as

    $$\{x \in A : \varphi(x)\},$$

    read "the set of $x$ in $A$ such that $\varphi(x)$." So $y \in \{x \in A : \varphi(x)\} \leftrightarrow (y \in A \land \varphi(y))$. The letter $x$ is only a placeholder: $\{y \in A : \varphi(y)\}$ is the same set.

    Separation only carves a subset out of a set $A$ that already exists. That restriction is essential.

    /// important | 📐 **Theorem (No Set of All Sets)**
        attrs: {class: no-icon}
    There is no set $V$ such that $\forall x\,(x \in V)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Suppose, for contradiction, that such a set $V$ exists. By Separation, $R := \{x \in V : x \notin x\}$ is a set, and $R \in V$ because every set is in $V$. By the definition of $R$,
    $$R \in R \;\leftrightarrow\; (R \in V \land R \notin R) \;\leftrightarrow\; R \notin R,$$
    where the second step uses $R \in V$. A statement equivalent to its own negation is a contradiction. $\blacksquare$
    ///

    The same argument is [Russell's paradox](https://en.wikipedia.org/wiki/Russell%27s_paradox) (1901). It shows that the naive rule "for every predicate $\varphi$, the collection $\{x : \varphi(x)\}$ is a set" is contradictory: applied to $\varphi(x) := x \notin x$, it produces a set $R$ with $R \in R \leftrightarrow R \notin R$. ZFC avoids the paradox by building new sets only from sets already known to exist[^proper-class].

    [^proper-class]: Collections such as "all sets" can still be discussed in the metalanguage, where they are called *proper classes*; they are just not sets. See [Appendix A: The Metatheory](appendix_a_formal_logic.md).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Separation gives the remaining basic operations on sets.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Intersection**</u>

    The intersection of sets $A$ and $B$ is $A \cap B := \{x \in A : x \in B\}$, so that
    $$x \in A \cap B \;\leftrightarrow\; (x \in A \land x \in B).$$
    The intersection of a nonempty set $F$ is
    $$\bigcap F := \Big\{x \in \bigcup F : \forallin{A}{F}\,(x \in A)\Big\},$$
    so that $x \in \bigcap F \leftrightarrow \forallin{A}{F}\,(x \in A)$. The notation $\bigcap F$ is not used when $F = \emptyset$.
    ///

    Although the definition of $A \cap B$ treats $A$ and $B$ differently, $A \cap B = B \cap A$: both sides have the same elements because $\land$ is commutative. The characterization of $\bigcap F$ needs a proof, because that is where the proviso $F \neq \emptyset$ matters.

    /// important | 📐 **Lemma (General Intersection)**
        attrs: {class: no-icon}
    If $F \neq \emptyset$, then for every $x$: $x \in \bigcap F \leftrightarrow \forallin{A}{F}\,(x \in A)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    ($\rightarrow$) This is part of the defining condition of $\bigcap F$. ($\leftarrow$) Suppose $x \in A$ for every $A \in F$. Since $F \neq \emptyset$, it has some element $A_0$, and $x \in A_0$, so $x \in \bigcup F$. Together with the assumption, this is exactly the condition for $x \in \bigcap F$. $\blacksquare$
    ///

    Why the proviso? When $F = \emptyset$, the condition $\forallin{A}{\emptyset}\,(x \in A)$ is vacuously true for *every* set $x$, so a set with the characterization above would contain every set, and the No Set of All Sets theorem says no such set exists. The formula in the definition would still produce a set when $F = \emptyset$ (namely $\emptyset$, the only subset of $\bigcup \emptyset = \emptyset$), but that set lacks the property that makes it an intersection, so we never write $\bigcap F$ unless $F \neq \emptyset$. Any element of $F$ could replace $\bigcup F$ as the set we separate from; using $\bigcup F$ avoids having to pick one. For two sets the definitions agree: $\bigcap\{A, B\} = A \cap B$, since both have as elements exactly the $x$ with $x \in A \land x \in B$.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Set difference**</u>

    The set difference of sets $A$ and $B$ is $A \setminus B := \{x \in A : x \notin B\}$, so that
    $$x \in A \setminus B \;\leftrightarrow\; (x \in A \land x \notin B).$$
    ///

    For example, if $a$, $b$, $c$ are distinct sets, then $\{a, b\} \cap \{b, c\} = \{b\}$ and $\{a, b, c\} \setminus \{b\} = \{a, c\}$. Unlike $\cup$ and $\cap$, set difference is not symmetric: $\{a, b\} \setminus \{b\} = \{a\}$, but $\{b\} \setminus \{a, b\} = \emptyset$. The complement of a set relative to an ambient set, $A^c := \Omega \setminus A$, is introduced in [Chapter 3](ch3_sets_for_probability.md).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6. Power Set

    **In words.** For any set $A$, there is a set whose elements are exactly the subsets of $A$.

    **In symbols.**

    $$\forall A\,\exists P\,\forall x\,(x \in P \leftrightarrow x \subseteq A).$$

    **What it builds.** By the Uniqueness Lemma the set $P$ is unique.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Power set**</u>

    The power set of a set $A$ is the unique set $\mathcal P(A)$ whose elements are the subsets of $A$:
    $$x \in \mathcal P(A) \;\leftrightarrow\; x \subseteq A.$$
    ///

    For example, $\mathcal P(\emptyset) = \{\emptyset\}$, and if $a \neq b$, then $\mathcal P(\{a, b\}) = \{\emptyset, \{a\}, \{b\}, \{a, b\}\}$. For every set $A$, both $\emptyset \in \mathcal P(A)$ and $A \in \mathcal P(A)$.

    Separation only shrinks sets, and Pairing and Union enlarge them modestly; Power Set is the axiom that produces genuinely larger sets ([Chapter 3](ch3_sets_for_probability.md) proves Cantor's theorem, which makes "larger" precise). Below, it supplies the room needed for Cartesian products and sets of functions. In [Chapter 4](ch4_probability_spaces.md), the events of a probability space are elements of $\mathcal P(\Omega)$, where $\Omega$ is the set of possible outcomes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 7. Replacement

    **In words.** If a predicate assigns to each element $x$ of a set $A$ exactly one set $y$, then the assigned sets form a set.

    **In symbols.** For each predicate $\varphi(x, y, p_1, \ldots, p_n)$ in which $B$ does not occur, the following is an axiom (we suppress the parameters $p_1, \ldots, p_n$ inside $\varphi$ for readability):

    $$\forall p_1 \cdots \forall p_n\,\forall A\,\Big[\forallin{x}{A}\,\exists! y\,\varphi(x, y) \;\rightarrow\; \exists B\,\forall y\,\big(y \in B \leftrightarrow \existsin{x}{A}\,\varphi(x, y)\big)\Big].$$

    **What it builds.** When the hypothesis $\forallin{x}{A}\,\exists! y\,\varphi(x, y)$ holds, the set $B$ is unique, and we write $\{y : \existsin{x}{A}\,\varphi(x, y)\}$ for it. This notation has a proviso: it names a set only when the hypothesis holds, and we use it only then.

    In practice, $\varphi(x, y)$ almost always says $y = t(x)$, where $t(x)$ is an expression built from $x$ with notation already defined, such as $\{x\}$ or $x \cup \{x\}$. Such an expression names exactly one set for each $x$, so the hypothesis holds automatically, and we write

    $$\{t(x) : x \in A\} := \big\{y : \existsin{x}{A}\,\big(y = t(x)\big)\big\}, \qquad\text{so}\qquad y \in \{t(x) : x \in A\} \leftrightarrow \existsin{x}{A}\,\big(y = t(x)\big).$$

    To transform only the elements that satisfy a predicate $\psi$, first separate, then replace:

    $$\{t(x) : x \in A \land \psi(x)\} := \{t(x) : x \in A'\}, \qquad\text{where } A' := \{x \in A : \psi(x)\}.$$

    Then $y$ is an element iff $y = t(x)$ for some $x \in A$ with $\psi(x)$. Taking $t(x) := x$ gives back Separation's $\{x \in A : \psi(x)\}$.

    For example, if $A = \{\emptyset, \{\emptyset\}\}$, then

    $$\{\{x\} : x \in A\} = \{\{\emptyset\}, \{\{\emptyset\}\}\} \qquad\text{and}\qquad \{\{x\} : x \in A \land x \neq \emptyset\} = \{\{\{\emptyset\}\}\}.$$

    The outputs need not be elements of $A$, and different inputs may give the same output; the set collects each output once.

    Separation can only collect elements of a set we already have; Replacement needs no such ambient set. In this book it is mostly a convenience that makes notation such as $\{t(x) : x \in A\}$ legitimate without first finding a set that contains all the outputs[^replacement-strength].

    [^replacement-strength]: Replacement is nevertheless strictly stronger than Separation: without it one cannot prove that $\{\mathbb N, \mathcal P(\mathbb N), \mathcal P(\mathcal P(\mathbb N)), \ldots\}$ is a set, where $\mathbb N$ is the set of natural numbers defined below. See [Zermelo set theory](https://en.wikipedia.org/wiki/Zermelo_set_theory).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 8. Infinity

    Pairing and Union let us form, from any set $x$, a set that contains everything in $x$ and also $x$ itself.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Successor**</u>

    The successor of a set $x$ is $\operatorname{succ}(x) := x \cup \{x\}$, so that
    $$y \in \operatorname{succ}(x) \;\leftrightarrow\; (y \in x \lor y = x).$$
    ///

    Starting from $\emptyset$ and taking successors repeatedly gives

    $$\operatorname{succ}(\emptyset) = \{\emptyset\}, \quad \operatorname{succ}(\{\emptyset\}) = \{\emptyset, \{\emptyset\}\}, \quad \operatorname{succ}(\{\emptyset, \{\emptyset\}\}) = \{\emptyset, \{\emptyset\}, \{\emptyset, \{\emptyset\}\}\}, \quad \ldots$$

    These will be the natural numbers $1, 2, 3, \ldots$, with $0 := \emptyset$. Each step is justified by the axioms so far, but none of them provides a single set containing all of these sets. The Axiom of Infinity does.

    **In words.** There is a set that contains $\emptyset$ and contains the successor of each of its elements.

    **In symbols.**

    $$\exists I\,\big(\emptyset \in I \land \forallin{x}{I}\,(\operatorname{succ}(x) \in I)\big).$$

    **What it builds.** The property in parentheses gets a name.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Inductive set**</u>

    A set $I$ is inductive iff it contains $\emptyset$ and the successor of each of its elements:
    $$I \text{ is inductive} \;:\Longleftrightarrow\; \emptyset \in I \land \forallin{x}{I}\,\big(\operatorname{succ}(x) \in I\big).$$
    ///

    So the Axiom of Infinity says that an inductive set exists. Such a set contains $\emptyset$, $\operatorname{succ}(\emptyset)$, $\operatorname{succ}(\operatorname{succ}(\emptyset))$, and so on; each of these is an element of all later ones, and no set is an element of itself (Regularity, below), so no two of them are equal, and an inductive set is infinite[^infinite-informal]. The other axioms cannot prove that any inductive set exists[^hereditarily-finite]. Every infinite object in this book, from the time index $k$ to the real line, rests on this axiom. The natural numbers are defined from it under Natural Numbers below.

    [^infinite-informal]: Used informally here; *finite* and *infinite* are defined precisely in [Chapter 3](ch3_sets_for_probability.md).

    [^hereditarily-finite]: The [hereditarily finite sets](https://en.wikipedia.org/wiki/Hereditarily_finite_set) satisfy all the other axioms but contain no inductive set, so Infinity cannot be derived from the others (provided they are consistent).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 9. Regularity

    **In words.** Every nonempty set $A$ has an element $x$ that has no element in common with $A$.

    **In symbols.**

    $$\forall A\,\big(A \neq \emptyset \rightarrow \existsin{x}{A}\,(x \cap A = \emptyset)\big).$$

    **What it builds.** Nothing. Regularity (also called Foundation) forbids membership loops: there is no set with $x \in x$ (proved next), and no sets with $x \in y$ and $y \in x$ (apply Regularity to $\{x, y\}$: its element $x$ has $y$ in common with it, and its element $y$ has $x$ in common with it). More generally, it forbids [infinite descending membership chains](https://en.wikipedia.org/wiki/Axiom_of_regularity), so every set is built up in stages from $\emptyset$. Ordinary mathematics rarely needs it. We use it once, through the next theorem, to prove that different natural numbers have different successors.

    /// important | 📐 **Theorem (No Set Is an Element of Itself)**
        attrs: {class: no-icon}
    For every set $x$, $x \notin x$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Suppose, for contradiction, that $x \in x$. The singleton $\{x\}$ is nonempty, so by Regularity it has an element $y$ with $y \cap \{x\} = \emptyset$. The only element of $\{x\}$ is $x$, so $y = x$ and $x \cap \{x\} = \emptyset$. But $x \in x$ and $x \in \{x\}$, so $x \in x \cap \{x\}$, a contradiction. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 10. Choice

    **In words.** For any set $F$ of nonempty sets, no two of which have an element in common, there is a set $C$ that contains exactly one element of each member of $F$.

    **In symbols.**

    $$\forall F\,\Big[\Big(\forallin{A}{F}\,(A \neq \emptyset) \land \forallin{A}{F}\,\forallin{B}{F}\,\big(A \neq B \rightarrow A \cap B = \emptyset\big)\Big) \rightarrow \exists C\,\forallin{A}{F}\,\exists! x\,(x \in A \cap C)\Big].$$

    Such a set $C$ is called a *choice set* for $F$. Unlike the other set-building axioms, Choice does not determine its set: it asserts that a selection exists without giving a rule for making it, and a choice set is generally not unique, so Choice introduces no notation.

    **Why it is needed.** Finitely many choices need no axiom: from "$A_1$ is nonempty" a proof may say "let $x_1 \in A_1$," and a proof can contain finitely many such steps. For infinitely many sets with no rule for picking an element, the other axioms are not enough: Choice can be neither proved nor disproved from them [@godel1938; @cohen1963]; see [Axiom of choice](https://en.wikipedia.org/wiki/Axiom_of_choice). Most of mathematics, including this book, accepts it. [Chapter 3](ch3_sets_for_probability.md) uses it to show that a countable union of countable sets is countable, and [Chapter 4](ch4_probability_spaces.md) uses it to construct the Vitali set, a set of numbers in $[0, 1)$ to which no probability can be assigned consistently. That example is why probabilities are assigned only to a chosen collection of *events* rather than to every subset of the outcomes. An equivalent form of Choice that uses functions appears under Functions below.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Building Blocks

    The axioms give us sets. Mathematics also needs ordered pairs, relations, and functions; each of these is a particular kind of set.

    ### Ordered Pairs

    A measurement taken at step $k$ is naturally the pair "step $k$, value $z_k$", and the order matters: step 2 with value 5 is not step 5 with value 2. Sets built by Pairing are unordered ($\{a, b\} = \{b, a\}$), so we need a set that also records which element comes first. The standard choice is due to [Kuratowski](https://en.wikipedia.org/wiki/Ordered_pair) (1921).

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Ordered pair**</u>

    The ordered pair of sets $a$ and $b$ is
    $$(a, b) := \{\{a\}, \{a, b\}\},$$
    with first coordinate $a$ and second coordinate $b$. A set $p$ is an ordered pair iff $p = (a, b)$ for some sets $a$ and $b$.
    ///

    The set $(a, b)$ exists by three applications of Pairing. The particular set $\{\{a\}, \{a, b\}\}$ is only a device[^other-pairs]; everything we ever use about ordered pairs is the following property, which says that an ordered pair determines its coordinates and their order.

    /// important | 📐 **Theorem (Characteristic Property of Ordered Pairs)**
        attrs: {class: no-icon}
    For all sets $a$, $b$, $c$, $d$:
    $$(a, b) = (c, d) \;\leftrightarrow\; (a = c \land b = d).$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    ($\leftarrow$) If $a = c$ and $b = d$, then $(a, b)$ and $(c, d)$ are built from the same sets in the same way, so they are equal.

    ($\rightarrow$) Suppose $\{\{a\}, \{a, b\}\} = \{\{c\}, \{c, d\}\}$.

    *Step 1: $a = c$.* Since $\{a\} \in (a, b) = (c, d)$, either $\{a\} = \{c\}$ or $\{a\} = \{c, d\}$. In the first case $a \in \{c\}$, so $a = c$. In the second case $c \in \{c, d\} = \{a\}$, so $c = a$.

    *Step 2: $b = d$.* We consider two cases.

    - *Case $a = b$.* Then $\{a, b\} = \{a\}$, so $(a, b) = \{\{a\}\}$. Since $\{c, d\} \in (c, d) = \{\{a\}\}$, we get $\{c, d\} = \{a\}$; hence $d \in \{a\}$, and $d = a = b$.
    - *Case $a \neq b$.* Since $\{a, b\} \in (c, d)$, either $\{a, b\} = \{c\}$ or $\{a, b\} = \{c, d\}$. The first is impossible, because it would give $a = c$ and $b = c$, hence $a = b$. So $\{a, b\} = \{c, d\}$, and therefore $b \in \{c, d\}$, that is, $b = c$ or $b = d$. If $b = c$, then $b = c = a$ by Step 1, contradicting $a \neq b$. Therefore $b = d$. $\blacksquare$
    ///

    [^other-pairs]: Any definition with the characteristic property would serve equally well. Kuratowski's is standard because it needs only Pairing.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cartesian Products

    Given sets $X$ and $Y$, we want the set of all ordered pairs $(a, b)$ with $a \in X$ and $b \in Y$. Separation can only select from a set that already exists, so we first find a set that contains every such pair.

    /// important | 📐 **Lemma (Pairs Lie in a Power Set)**
        attrs: {class: no-icon}
    If $a \in X$ and $b \in Y$, then $(a, b) \in \mathcal P(\mathcal P(X \cup Y))$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Since $a$ and $b$ are elements of $X \cup Y$, the sets $\{a\}$ and $\{a, b\}$ are *subsets* of $X \cup Y$, that is, *elements* of $\mathcal P(X \cup Y)$. Therefore $(a, b) = \{\{a\}, \{a, b\}\}$ is a *subset* of $\mathcal P(X \cup Y)$, that is, an *element* of $\mathcal P(\mathcal P(X \cup Y))$. $\blacksquare$
    ///

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Cartesian product**</u>

    The Cartesian product of sets $X$ and $Y$ is the set of all ordered pairs whose first coordinate is in $X$ and whose second coordinate is in $Y$:
    $$X \times Y := \Big\{p \in \mathcal P\big(\mathcal P(X \cup Y)\big) : \existsin{a}{X}\,\existsin{b}{Y}\,\big(p = (a, b)\big)\Big\}.$$
    ///

    By the Lemma, separating from $\mathcal P(\mathcal P(X \cup Y))$ loses no pairs: $p \in X \times Y \leftrightarrow \existsin{a}{X}\,\existsin{b}{Y}\,\big(p = (a, b)\big)$. Combined with the Characteristic Property, $(a, b) \in X \times Y \leftrightarrow (a \in X \land b \in Y)$. For example, $\{a, b\} \times \{c\} = \{(a, c), (b, c)\}$ for any sets $a$, $b$, $c$, and $X \times \emptyset = \emptyset$ for every $X$. In general $X \times Y \neq Y \times X$.

    ### Relations

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Relation**</u>

    A relation is a set $R$ whose elements are all ordered pairs. For a relation $R$, we write $a \mathrel{R} b$ for $(a, b) \in R$. A relation from $X$ to $Y$ is a relation $R \subseteq X \times Y$, and a relation on $X$ is a relation $R \subseteq X \times X$.
    ///

    A relation is identified with the collection of pairs it relates. We often build one by Separation from a Cartesian product, using the shorthand

    $$\{(x, y) \in X \times Y : \varphi(x, y)\} := \big\{p \in X \times Y : \exists x\,\exists y\,\big(p = (x, y) \land \varphi(x, y)\big)\big\}.$$

    For example, on $A := \{\emptyset, \{\emptyset\}\}$ the membership relation $\{(x, y) \in A \times A : x \in y\}$ equals $\{(\emptyset, \{\emptyset\})\}$. The order $<$ on the natural numbers below is a relation, and so are the equivalence relations of [Appendix B](appendix_b_number_systems.md).

    Every relation has a set of first coordinates and a set of second coordinates. To build them with Separation we need a set that contains every coordinate.

    /// important | 📐 **Lemma (Coordinates)**
        attrs: {class: no-icon}
    If $(a, b) \in R$, then $a \in \bigcup\bigcup R$ and $b \in \bigcup\bigcup R$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    We have $\{a, b\} \in (a, b)$ and $(a, b) \in R$, so $\{a, b\} \in \bigcup R$. Then $a \in \{a, b\}$ and $\{a, b\} \in \bigcup R$ give $a \in \bigcup\bigcup R$, and likewise for $b$. $\blacksquare$
    ///

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Domain**</u>

    The domain of a relation $R$ is the set of first coordinates of its elements,
    $$\operatorname{dom} R := \Big\{a \in \bigcup\bigcup R : \exists b\,\big((a, b) \in R\big)\Big\},$$
    so that, by the Coordinates Lemma, $a \in \operatorname{dom} R \leftrightarrow \exists b\,\big((a, b) \in R\big)$.
    ///

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Range**</u>

    The range of a relation $R$ is the set of second coordinates of its elements,
    $$\operatorname{ran} R := \Big\{b \in \bigcup\bigcup R : \exists a\,\big((a, b) \in R\big)\Big\},$$
    so that, by the Coordinates Lemma, $b \in \operatorname{ran} R \leftrightarrow \exists a\,\big((a, b) \in R\big)$.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Functions

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Function**</u>

    A function is a relation $f$ in which no first coordinate has two different partners:
    $$\forall a\,\forall b\,\forall c\,\Big(\big((a, b) \in f \land (a, c) \in f\big) \rightarrow b = c\Big).$$
    For $a \in \operatorname{dom} f$, the value of $f$ at $a$, written $f(a)$, is the unique $b$ with $(a, b) \in f$.
    ///

    So a function *is* its graph: the set of its input–output pairs. The notation $f(a)$ has a proviso: it names a set only when $f$ is a function and $a \in \operatorname{dom} f$, and we write it only then (see [Appendix A: Extension by Definitions](appendix_a_formal_logic.md)). For example, if $a$, $b$, $c$ are distinct sets, then $f := \{(a, c), (b, c)\}$ is a function with $\operatorname{dom} f = \{a, b\}$, $\operatorname{ran} f = \{c\}$, and $f(a) = f(b) = c$. The relation $\{(a, b), (a, c)\}$ is not a function, because $a$ has the two partners $b \neq c$.

    The domain and range of a function are determined by its pairs. A target set for the values is not, so it is declared separately.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Codomain**</u>

    A set $Y$ is a codomain of a function $f$ iff $\operatorname{ran} f \subseteq Y$. We write
    $$f : X \to Y \;:\Longleftrightarrow\; f \text{ is a function} \land \operatorname{dom} f = X \land \operatorname{ran} f \subseteq Y,$$
    read "$f$ is a function from $X$ to $Y$," and in that context call $Y$ *the* codomain of $f$.
    ///

    For instance, the function $f = \{(a, c), (b, c)\}$ above satisfies both $f : \{a, b\} \to \{c\}$ and $f : \{a, b\} \to \{a, b, c\}$; a codomain is always stated alongside the function. A {term}`signal` is a function whose domain is a set of times. For example, the scale readings of the Introduction form a function from the set of sample indices to the real numbers[^reals-informal].

    [^reals-informal]: Used informally here; the real numbers are constructed in [Appendix B](appendix_b_number_systems.md) and characterized in [Chapter 3](ch3_sets_for_probability.md).

    /// important | 📐 **Lemma (Equality of Functions)**
        attrs: {class: no-icon}
    Functions $f$ and $g$ are equal iff $\operatorname{dom} f = \operatorname{dom} g$ and $f(a) = g(a)$ for every $a \in \operatorname{dom} f$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    ($\rightarrow$) Equal sets have the same domains and the same values. ($\leftarrow$) We show $f \subseteq g$. Every element of $f$ is a pair $(a, b)$ with $a \in \operatorname{dom} f$ and $b = f(a)$. Then $a \in \operatorname{dom} g$ and $b = f(a) = g(a)$, so $(a, b) = (a, g(a)) \in g$. Exchanging the roles of $f$ and $g$ gives $g \subseteq f$, so $f = g$ by Double Inclusion. $\blacksquare$
    ///

    **Functions given by a rule.** If $t(x)$ is an expression that names a set for each $x \in X$, Replacement gives the set

    $$(x \mapsto t(x)) := \{(x, t(x)) : x \in X\}.$$

    It is a function with domain $X$ and value $t(a)$ at each $a \in X$. Indeed, each of its elements is a pair $(x, t(x))$ with $x \in X$, so its domain is $X$; and if $(a, b)$ is an element, then $(a, b) = (x, t(x))$ for some $x \in X$, so $a = x$ and $b = t(a)$ by the Characteristic Property, which means $a$ has only the partner $t(a)$. If moreover $t(x) \in Y$ for every $x \in X$, then $(x \mapsto t(x)) : X \to Y$.

    **Sets of functions.** If $f : X \to Y$, then $f \subseteq X \times Y$, because each element of $f$ is a pair $(a, b)$ with $a \in \operatorname{dom} f = X$ and $b \in \operatorname{ran} f \subseteq Y$. So $f \in \mathcal P(X \times Y)$, and Separation gives the set of all functions from $X$ to $Y$:

    $$Y^X := \{f \in \mathcal P(X \times Y) : f \text{ is a function} \land \operatorname{dom} f = X\}.$$

    Then $f \in Y^X \leftrightarrow f : X \to Y$ (for "$\rightarrow$", note that $f \subseteq X \times Y$ forces $\operatorname{ran} f \subseteq Y$). For a function $f$ whose domain is a Cartesian product, we write $f(a, b)$ for $f((a, b))$.

    **Choice, restated.** With functions available, the Axiom of Choice takes a more familiar form.

    /// important | 📐 **Theorem (Choice Functions)**
        attrs: {class: no-icon}
    For every set $F$ of nonempty sets, there is a function $c : F \to \bigcup F$ with $c(A) \in A$ for every $A \in F$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    The members of $F$ may share elements, so we first make disjoint copies of them by tagging each element with the set it came from. For $A \in F$, let $A' := \{A\} \times A$, the set of pairs $(A, x)$ with $x \in A$, and let $F' := \{A' : A \in F\}$ (Replacement).

    - Each $A'$ is nonempty: $A$ has an element $x$, and $(A, x) \in A'$.
    - Different members of $F'$ have no element in common: if $p \in A' \cap B'$, then $p = (A, x) = (B, y)$ for some $x$ and $y$, so $A = B$ by the Characteristic Property, and hence $A' = B'$.

    By the Axiom of Choice, $F'$ has a choice set $C$. Let $c := C \cap \bigcup F'$. Every element of $c$ lies in some $A'$, so it is a pair $(A, x)$ with $A \in F$ and $x \in A$; in particular, $c$ is a relation. For each $A \in F$, the elements of $c$ with first coordinate $A$ are exactly the elements of $A' \cap C$ (an element $(A, x)$ of $c$ lies in some $B'$, and the Characteristic Property forces $B = A$), and $A' \cap C$ has exactly one element. Hence $c$ is a function with $\operatorname{dom} c = F$ and $c(A) \in A$ for every $A \in F$, so $\operatorname{ran} c \subseteq \bigcup F$. $\blacksquare$
    ///

    Such a $c$ is called a *choice function* for $F$. Conversely, if no two members of $F$ share an element and $c$ is a choice function for $F$, then $\operatorname{ran} c$ is a choice set for $F$: it contains $c(A) \in A$, and any $x \in A \cap \operatorname{ran} c$ equals $c(B)$ for some $B \in F$ with $x \in A \cap B$, which forces $B = A$ and $x = c(A)$. So the theorem is equivalent to the Axiom of Choice.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Natural Numbers

    ### The Smallest Inductive Set

    The Axiom of Infinity provides an inductive set, but possibly one with extra elements. The natural numbers are the sets that belong to *every* inductive set. Fix an inductive set $I_0$ (one exists by Infinity) and define

    $$\mathbb N := \{n \in I_0 : \forall I\,(I \text{ is inductive} \rightarrow n \in I)\}.$$

    A set that belongs to every inductive set belongs in particular to $I_0$, so the condition $n \in I_0$ excludes nothing:

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Natural numbers**</u>

    The set $\mathbb N$ of natural numbers is the set whose elements are exactly the sets that belong to every inductive set:
    $$n \in \mathbb N \;\leftrightarrow\; \forall I\,(I \text{ is inductive} \rightarrow n \in I).$$
    Its elements are called natural numbers.
    ///

    This characterization does not mention $I_0$, so by the Uniqueness Lemma $\mathbb N$ does not depend on which inductive set we fixed.

    /// important | 📐 **Theorem (Smallest Inductive Set)**
        attrs: {class: no-icon}
    $\mathbb N$ is inductive, and $\mathbb N \subseteq I$ for every inductive set $I$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Every inductive set contains $\emptyset$, so $\emptyset \in \mathbb N$. If $n \in \mathbb N$ and $I$ is inductive, then $n \in I$, so $\operatorname{succ}(n) \in I$; since this holds for every inductive $I$, $\operatorname{succ}(n) \in \mathbb N$. So $\mathbb N$ is inductive. The inclusion $\mathbb N \subseteq I$ is the definition of $\mathbb N$. $\blacksquare$
    ///

    We name the first few natural numbers:

    $$0 := \emptyset, \qquad 1 := \operatorname{succ}(0) = \{0\}, \qquad 2 := \operatorname{succ}(1) = \{0, 1\}, \qquad 3 := \operatorname{succ}(2) = \{0, 1, 2\}, \qquad \ldots$$

    Each natural number is the set of the natural numbers before it (proved under Arithmetic and Order below). These are the [von Neumann numerals](https://en.wikipedia.org/wiki/Set-theoretic_definition_of_natural_numbers). As in the rest of the book, $\mathbb N = \{0, 1, 2, \ldots\}$ starts at $0$; the time index $k = 0$ is the initial condition, and measurements start at $k = 1$.

    Explore the numerals below: the slider picks $n$, and the panel writes $n$ using only braces and $\emptyset$, lists its elements, and checks two facts: $n$ is transitive (proved under Induction below) and $n \notin n$ (proved under Regularity).
    """)
    return


@app.cell
def _():
    # jb: include=false
    def von_neumann(n):
        """Return the von Neumann numerals 0, 1, ..., n as nested frozensets."""
        numerals = [frozenset()]
        for _ in range(n):
            numerals.append(numerals[-1] | {numerals[-1]})
        return numerals

    def braces(s):
        """Write a hereditarily finite set using only braces and the empty-set symbol."""
        if not s:
            return "∅"
        return "{" + ", ".join(braces(e) for e in sorted(s, key=len)) + "}"

    return braces, von_neumann


@app.cell(hide_code=True)
def _(mo):
    numeral_slider = mo.ui.slider(
        start=0, stop=6, step=1, value=3, show_value=True, label=r"numeral $n$"
    )
    return (numeral_slider,)


@app.cell(hide_code=True)
def _(braces, mo, numeral_slider, von_neumann):
    _n = numeral_slider.value
    _nums = von_neumann(_n + 1)
    _x, _succ = _nums[_n], _nums[_n + 1]
    _name = {s: str(i) for i, s in enumerate(_nums)}

    def _roster(s):
        if not s:
            return r"\emptyset"
        return r"\{" + ", ".join(_name[e] for e in sorted(s, key=len)) + r"\}"

    def _yes(b):
        return "yes" if b else "no"

    _brace_form = braces(_x)
    _rows = [
        (rf"${_n}$ written with braces and $\emptyset$ only", _brace_form),
        (rf"${_n}$ as a set of numerals", f"${_roster(_x)}$"),
        (rf"$\operatorname{{succ}}({_n}) = {_n} \cup \{{{_n}\}}$", f"${_roster(_succ)}$"),
        (rf"number of elements of ${_n}$", str(len(_x))),
        (r"number of $\emptyset$ symbols in the brace form", str(_brace_form.count("∅"))),
        (rf"every element of ${_n}$ is a subset of ${_n}$", _yes(all(e <= _x for e in _x))),
        (rf"${_n} \in {_n}$", _yes(_x in _x)),
    ]
    _table = "| | |\n|---|---|\n" + "\n".join(f"| {a} | {b} |" for a, b in _rows)
    mo.vstack([numeral_slider, mo.md(_table)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The brace form doubles in length at each step, because $\operatorname{succ}(n) = n \cup \{n\}$ contains a complete copy of $n$ as an element. Nobody computes with numerals this way; the point is that the natural numbers *exist as sets*, with nothing assumed beyond the axioms.

    ### Induction

    Because $\mathbb N$ is the *smallest* inductive set, any inductive subset of $\mathbb N$ is all of $\mathbb N$. This is the principle of induction.

    /// important | 📐 **Theorem (Induction)**
        attrs: {class: no-icon}
    Let $T \subseteq \mathbb N$. If $0 \in T$ and $\forallin{n}{T}\,\big(\operatorname{succ}(n) \in T\big)$, then $T = \mathbb N$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    The hypotheses say that $T$ is inductive, so $\mathbb N \subseteq T$ by the Smallest Inductive Set theorem. Together with $T \subseteq \mathbb N$, Double Inclusion gives $T = \mathbb N$. $\blacksquare$
    ///

    In practice we apply the theorem to $T := \{n \in \mathbb N : P(n)\}$ for a predicate $P$. To prove $\forallin{n}{\mathbb N}\,P(n)$ by induction, we prove

    1. the *base case* $P(0)$, and
    2. the *inductive step*: for every $n \in \mathbb N$, if $P(n)$ holds (the *induction hypothesis*), then $P(\operatorname{succ}(n))$ holds.

    Here are two first examples; both are used again later.

    /// important | 📐 **Lemma (Zero or Successor)**
        attrs: {class: no-icon}
    Every natural number is $0$ or the successor of a natural number: $\forallin{n}{\mathbb N}\,\big(n = 0 \lor \existsin{m}{\mathbb N}\,(n = \operatorname{succ}(m))\big)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    By induction on $n$. *Base case:* $0 = 0$. *Inductive step:* for any $n \in \mathbb N$, the number $\operatorname{succ}(n)$ is the successor of the natural number $n$ (this step does not even need the induction hypothesis). $\blacksquare$
    ///

    A set $A$ is *transitive* iff every element of $A$ is also a subset of $A$:

    $$A \text{ is transitive} \;:\Longleftrightarrow\; \forallin{x}{A}\,(x \subseteq A).$$

    Equivalently, $y \in x$ and $x \in A$ imply $y \in A$.

    /// important | 📐 **Lemma (Transitivity)**
        attrs: {class: no-icon}
    (a) Every natural number is transitive. (b) $\mathbb N$ is transitive: every element of a natural number is a natural number.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    (a) By induction on $n$. *Base case:* $0 = \emptyset$ is transitive, vacuously. *Inductive step:* suppose $n$ is transitive, and let $x \in \operatorname{succ}(n) = n \cup \{n\}$. If $x \in n$, then $x \subseteq n \subseteq \operatorname{succ}(n)$ by the induction hypothesis. If $x = n$, then $x = n \subseteq \operatorname{succ}(n)$. Either way $x \subseteq \operatorname{succ}(n)$, so $\operatorname{succ}(n)$ is transitive.

    (b) We prove $n \subseteq \mathbb N$ for every $n \in \mathbb N$, by induction. *Base case:* $\emptyset \subseteq \mathbb N$. *Inductive step:* if $n \subseteq \mathbb N$, then every element of $\operatorname{succ}(n) = n \cup \{n\}$ is either an element of $n \subseteq \mathbb N$ or equal to $n \in \mathbb N$, so $\operatorname{succ}(n) \subseteq \mathbb N$. $\blacksquare$
    ///

    /// caution | ⚠️ **Assumptions and Failure Modes**
        attrs: {class: no-icon}
    Induction needs both hypotheses, for every $n$.

    - **Without the base case, the inductive step proves nothing.** Let $P(n)$ be "$n = \operatorname{succ}(n)$". The inductive step holds: if $n = \operatorname{succ}(n)$, then $\operatorname{succ}(n) = \operatorname{succ}(\operatorname{succ}(n))$, since equal sets have equal successors. Yet $P(n)$ is false for every $n$, because $n \in \operatorname{succ}(n)$ while $n \notin n$.
    - **The inductive step must hold for every $n$, including the smallest ones.** The famous false proof that [all horses are the same color](https://en.wikipedia.org/wiki/All_horses_are_the_same_color) has a valid base case and an inductive step that works for every $n$ except the step from one horse to two.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The Peano Axioms

    In 1889, Giuseppe Peano characterized the natural numbers by five properties, now called the [Peano axioms](https://en.wikipedia.org/wiki/Peano_axioms). In ZFC they are not axioms but theorems about the set $\mathbb N$ we just constructed. Only the fourth needs real work.

    /// important | 📐 **Theorem (Peano Axioms)**
        attrs: {class: no-icon}
    1. $0 \in \mathbb N$.
    2. $\forallin{n}{\mathbb N}\,\big(\operatorname{succ}(n) \in \mathbb N\big)$.
    3. $\forallin{n}{\mathbb N}\,\big(\operatorname{succ}(n) \neq 0\big)$.
    4. $\forallin{m}{\mathbb N}\,\forallin{n}{\mathbb N}\,\big(\operatorname{succ}(m) = \operatorname{succ}(n) \rightarrow m = n\big)$.
    5. For every $T \subseteq \mathbb N$: $\big(0 \in T \land \forallin{n}{T}\,(\operatorname{succ}(n) \in T)\big) \rightarrow T = \mathbb N$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    (1) and (2) say that $\mathbb N$ is inductive (Smallest Inductive Set), and (5) is the Induction theorem. (3) holds because $n \in \operatorname{succ}(n)$, while $0 = \emptyset$ has no elements.

    (4) Suppose $\operatorname{succ}(m) = \operatorname{succ}(n)$ but $m \neq n$. Since $m \in \operatorname{succ}(m) = \operatorname{succ}(n) = n \cup \{n\}$ and $m \neq n$, we get $m \in n$. The same argument with $m$ and $n$ exchanged gives $n \in m$. Now $n$ is transitive (Transitivity Lemma), so $m \in n$ gives $m \subseteq n$, and then $n \in m$ gives $n \in n$. This contradicts the theorem that no set is an element of itself. $\blacksquare$
    ///

    Property 4 says that different natural numbers have different successors; in the language of [Chapter 3](ch3_sets_for_probability.md), the function $(n \mapsto \operatorname{succ}(n)) : \mathbb N \to \mathbb N$ is *injective*[^injective-informal].

    [^injective-informal]: Used informally here; injective functions are defined in [Chapter 3](ch3_sets_for_probability.md).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Recursion

    A recursive definition gives a starting value and a rule for computing each value from the previous one. It feels obvious that this defines a value for every $n$, but "and so on" is not a proof: the result is a function on all of $\mathbb N$, an infinite set of pairs, and we must show that exactly one such set exists. Not every self-referential rule succeeds. For example, every constant function satisfies $h(n) = h(\operatorname{succ}(n))$, so that "rule" determines nothing. The Recursion Theorem shows that a rule which refers only to the *previous* value always defines exactly one function.

    /// important | 📐 **Theorem (Recursion)**
        attrs: {class: no-icon}
    Let $A$ be a set, $a \in A$, and $g : A \to A$. There is exactly one function $h : \mathbb N \to A$ such that
    $$h(0) = a \qquad\text{and}\qquad h(\operatorname{succ}(n)) = g(h(n)) \ \text{ for every } n \in \mathbb N.$$
    ///

    The idea of the proof: take $h$ to be the smallest set of pairs that contains $(0, a)$ and is closed under the step $(n, x) \mapsto (\operatorname{succ}(n), g(x))$, and then show by induction that it contains exactly one pair for each $n$.

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    *Construction.* Call a set $R \subseteq \mathbb N \times A$ *closed* if $(0, a) \in R$ and, for all $n$ and $x$, $(n, x) \in R$ implies $(\operatorname{succ}(n), g(x)) \in R$. The set $\mathbb N \times A$ itself is closed, so the set
    $$\mathcal C := \{R \in \mathcal P(\mathbb N \times A) : R \text{ is closed}\}$$
    is nonempty, and we may define $h := \bigcap \mathcal C$. By the General Intersection Lemma, $h \subseteq R$ for every closed $R$. Moreover, $h$ is itself closed: $(0, a)$ lies in every closed $R$, hence in $h$; and if $(n, x) \in h$, then $(n, x)$ lies in every closed $R$, so $(\operatorname{succ}(n), g(x))$ lies in every closed $R$, hence in $h$. In particular, $h \subseteq \mathbb N \times A$.

    *Key observation.* If $(m, z) \in h$, then $h \setminus \{(m, z)\}$ is not closed: otherwise $h \subseteq h \setminus \{(m, z)\}$, which is false because $(m, z) \in h$.

    *Each $n$ has exactly one partner.* Let $T := \{n \in \mathbb N : \text{there is exactly one } x \text{ with } (n, x) \in h\}$. We show that $T$ is inductive.

    - *Base case.* $(0, a) \in h$. Suppose also $(0, x) \in h$ with $x \neq a$, and let $R := h \setminus \{(0, x)\}$. Then $(0, a) \in R$, because $(0, a) \neq (0, x)$ by the Characteristic Property. If $(n, y) \in R$, then $(\operatorname{succ}(n), g(y)) \in h$ because $h$ is closed, and $(\operatorname{succ}(n), g(y)) \neq (0, x)$ because $\operatorname{succ}(n) \neq 0$; so $(\operatorname{succ}(n), g(y)) \in R$. Thus $R$ is closed, contradicting the key observation. Hence $0 \in T$.
    - *Inductive step.* Let $n \in T$, and let $y$ be the unique set with $(n, y) \in h$. Then $(\operatorname{succ}(n), g(y)) \in h$. Suppose also $(\operatorname{succ}(n), z) \in h$ with $z \neq g(y)$, and let $R := h \setminus \{(\operatorname{succ}(n), z)\}$. Then $(0, a) \in R$, because $0 \neq \operatorname{succ}(n)$. If $(m, w) \in R$, then $(\operatorname{succ}(m), g(w)) \in h$. If this pair were $(\operatorname{succ}(n), z)$, then $\operatorname{succ}(m) = \operatorname{succ}(n)$, so $m = n$ (Peano 4), so $w = y$ (because $n \in T$), so $z = g(w) = g(y)$, a contradiction. Hence $(\operatorname{succ}(m), g(w)) \in R$, and $R$ is closed, contradicting the key observation. Hence $\operatorname{succ}(n) \in T$.

    By Induction, $T = \mathbb N$.

    *Existence.* Since $h \subseteq \mathbb N \times A$ and every $n \in \mathbb N$ has exactly one partner in $h$, $h$ is a function with $\operatorname{dom} h = \mathbb N$ and $\operatorname{ran} h \subseteq A$, that is, $h : \mathbb N \to A$. Because $h$ is closed, $(0, a) \in h$ gives $h(0) = a$, and $(n, h(n)) \in h$ gives $(\operatorname{succ}(n), g(h(n))) \in h$, that is, $h(\operatorname{succ}(n)) = g(h(n))$.

    *Uniqueness.* Let $h' : \mathbb N \to A$ also satisfy both equations, and let $E := \{n \in \mathbb N : h(n) = h'(n)\}$. Then $0 \in E$ because $h(0) = a = h'(0)$, and if $n \in E$, then $h(\operatorname{succ}(n)) = g(h(n)) = g(h'(n)) = h'(\operatorname{succ}(n))$. By Induction $E = \mathbb N$, so $h = h'$ by Equality of Functions. $\blacksquare$
    ///

    The rule of a filter also depends on the step number, through the gain and the measurement, so we need a version in which $g$ sees $n$ as well.

    /// important | 📐 **Theorem (Recursion with a Step Index)**
        attrs: {class: no-icon}
    Let $A$ be a set, $a \in A$, and $g : \mathbb N \times A \to A$. There is exactly one function $h : \mathbb N \to A$ such that
    $$h(0) = a \qquad\text{and}\qquad h(\operatorname{succ}(n)) = g(n, h(n)) \ \text{ for every } n \in \mathbb N.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    *Existence.* We recurse on pairs (step, value). Apply the Recursion Theorem to the set $\mathbb N \times A$, the starting value $(0, a)$, and the function $G : \mathbb N \times A \to \mathbb N \times A$ given by $G(n, x) := (\operatorname{succ}(n), g(n, x))$. This yields $H : \mathbb N \to \mathbb N \times A$ with $H(0) = (0, a)$ and $H(\operatorname{succ}(n)) = G(H(n))$. By induction, the first coordinate of $H(n)$ is $n$: this holds for $n = 0$, and if $H(n) = (n, x)$, then $H(\operatorname{succ}(n)) = G(n, x) = (\operatorname{succ}(n), g(n, x))$.

    Let $h := \operatorname{ran} H$. Its elements are the pairs $H(n)$, and $H(n)$ is the only one of them with first coordinate $n$, so $h$ is a function with $\operatorname{dom} h = \mathbb N$, $\operatorname{ran} h \subseteq A$, and $H(n) = (n, h(n))$. Then $H(0) = (0, a)$ gives $h(0) = a$, and $H(\operatorname{succ}(n)) = (\operatorname{succ}(n), g(n, h(n)))$ gives $h(\operatorname{succ}(n)) = g(n, h(n))$, by the Characteristic Property.

    *Uniqueness.* If $h'$ also satisfies both equations, let $E := \{n \in \mathbb N : h(n) = h'(n)\}$. Then $0 \in E$, and if $n \in E$, then $h(\operatorname{succ}(n)) = g(n, h(n)) = g(n, h'(n)) = h'(\operatorname{succ}(n))$. By Induction and Equality of Functions, $h = h'$. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    A filter is a recursion with a step index. Given an initial estimate $\hat x_0 \in A$ and an update rule $G$ that computes the estimate at each step $k \ge 1$ from $k$ and the previous estimate,
    $$\hat x_k = G(k, \hat x_{k-1}),$$
    the Recursion Theorem with a Step Index, applied to $g(n, x) := G(\operatorname{succ}(n), x)$, gives exactly one function $k \mapsto \hat x_k$ on all of $\mathbb N$.
    ///

    Here $A$ is the set of possible estimates (the real numbers, in Part I). The step index matters because the rule changes with $k$: for the cumulative average, $G(k, x) = x + \tfrac1k\,(z_k - x)$ depends on $k$ through the gain $\tfrac1k$ and through the measurement $z_k$, which is a fixed parameter of the rule[^measurements-fixed]. The theorem guarantees that the estimates exist and are unambiguous; it says nothing about whether they are *good*. That question occupies the rest of Part I.

    Below, the scale readings of the Introduction (true weight 155 lb, readings scattered by about 1 lb) are filtered by the rule $G(k, x) = x + \alpha_k\,(z_k - x)$ with two choices of gain: $\alpha_k = 1/k$ (the cumulative average) and the constant $\alpha_k = 0.2$ for $k \ge 2$ of an {term}`exponential moving average` (EMA). In both cases $\alpha_1 = 1$, which makes $\hat x_1 = z_1$ whatever the initial value $\hat x_0$ (first-measurement initialization). The code evaluates $\hat x_1, \hat x_2, \ldots$ in order, which computes exactly the function the theorem guarantees.

    [^measurements-fixed]: Treating the measurements as given makes $G$ a fixed function. In [Chapter 5](ch5_random_variables.md) the measurements become random variables, and the recursion is applied to each possible sequence of measurements.
    """)
    return


@app.cell
def _(np):
    # jb: include=false
    scale_z = np.round(155.0 + np.random.default_rng(1).normal(0.0, 1.0, 30), 2)
    return (scale_z,)


@app.cell(hide_code=True)
def _(mo):
    steps_slider = mo.ui.slider(
        start=1, stop=30, step=1, value=10, show_value=True, label=r"steps $k$"
    )
    gain_choice = mo.ui.dropdown(
        options={
            "cumulative average, α_k = 1/k": "average",
            "EMA, α_k = 0.2": "ema",
        },
        value="cumulative average, α_k = 1/k",
        label="update rule",
    )
    return gain_choice, steps_slider


@app.cell(hide_code=True)
def _(gain_choice, graphic, mo, np, plt, scale_z, steps_slider):
    _K = steps_slider.value
    _rule = gain_choice.value

    def _gain(k, rule):
        if k == 1:
            return 1.0
        return 1.0 / k if rule == "average" else 0.2

    _xhat = [0.0]  # h(0) = x̂_0; irrelevant because α_1 = 1
    for _k in range(1, _K + 1):
        _prev = _xhat[-1]
        _xhat.append(_prev + _gain(_k, _rule) * (scale_z[_k - 1] - _prev))

    _ks = np.arange(1, _K + 1)
    _fig, _ax = plt.subplots(figsize=(7, 3.6))
    _ax.axhline(155.0, color="black", linewidth=1, label="true weight")
    _ax.plot(_ks, scale_z[:_K], "o", mfc="none", mec="black", label=r"measurement $z_k$")
    _ax.plot(_ks, _xhat[1:], "-o", color="C1", markersize=4, label=r"estimate $\hat x_k$")
    _ax.set_xlim(0.5, 30.5)
    _ax.set_ylim(152.0, 158.0)
    _ax.set_xlabel("step $k$ (samples at 10 Hz)")
    _ax.set_ylabel("weight (lb)")
    _ax.set_title(r"Evaluating $\hat x_k = G(k, \hat x_{k-1})$ step by step", style="italic")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.legend(loc="upper right", fontsize=8)
    _fig.tight_layout()
    _plot = graphic(_fig)
    plt.close(_fig)

    _a = _gain(_K, _rule)
    _step_text = mo.md(
        rf"Last step: $\hat x_{{{_K}}} = \hat x_{{{_K - 1}}} + \alpha_{{{_K}}}\,(z_{{{_K}}} - \hat x_{{{_K - 1}}})"
        rf" = {_xhat[_K - 1]:.2f} + {_a:.3f}\,({scale_z[_K - 1]:.2f} - {_xhat[_K - 1]:.2f}) = {_xhat[_K]:.2f}$ lb."
    )
    mo.vstack([mo.hstack([steps_slider, gain_choice], justify="start", gap=2), _plot, _step_text])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
        attrs: {class: no-icon}
    - **The update must be defined for every value it can receive.** The theorem requires $g : A \to A$ (or $g : \mathbb N \times A \to A$): defined on all of $A$, with values in $A$. If a rule is undefined for some value the recursion can reach, the recursion stops there. For example, an update containing $1/(\hat x_{k-1} - c)$ is undefined as soon as some estimate equals $c$.
    - **The rule may use only the previous value and the step index.** Rules that refer to later values need not define anything, as the constant-function example above shows. Rules that use several earlier values, such as $h(n+2) = g(h(n), h(n+1))$, reduce to the theorem by recursing on pairs $(h(n), h(n+1))$, just as the Introduction's alpha-beta filter carries the pair (estimate, rate) from step to step.
    - **The theorem is about exact values.** A computer evaluates $h(1), h(2), \ldots$ in finite-precision arithmetic, so the computed values can drift from the exact ones over many steps. [Chapter 14](ch14_kalman_filters_in_practice.md) discusses this for the Kalman filter.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Arithmetic and Order

    Recursion defines the arithmetic of $\mathbb N$.

    **Addition.** Fix $m \in \mathbb N$. Since $\mathbb N$ is inductive, $\operatorname{succ}$ maps $\mathbb N$ into $\mathbb N$, so the Recursion Theorem (with $A := \mathbb N$, $a := m$, and $g := (n \mapsto \operatorname{succ}(n))$) gives exactly one $h_m : \mathbb N \to \mathbb N$ with $h_m(0) = m$ and $h_m(\operatorname{succ}(n)) = \operatorname{succ}(h_m(n))$. Because $h_m$ is uniquely determined by $m$, the expression $h_m(n)$ names one set for each pair $(m, n)$, and the rule notation gives a function $+ : \mathbb N \times \mathbb N \to \mathbb N$, $(m, n) \mapsto m + n := h_m(n)$. It satisfies

    $$m + 0 = m, \qquad m + \operatorname{succ}(n) = \operatorname{succ}(m + n).$$

    Since $1 = \operatorname{succ}(0)$, the second equation gives $m + 1 = \operatorname{succ}(m + 0) = \operatorname{succ}(m)$. From now on we write $n + 1$ for $\operatorname{succ}(n)$.

    **Multiplication.** For fixed $m$, recursion with $a := 0$ and $g := (x \mapsto x + m)$ gives

    $$m \cdot 0 = 0, \qquad m \cdot (n + 1) = m \cdot n + m.$$

    The same pattern defines powers, $m^0 := 1$ and $m^{n+1} := m^n \cdot m$, and later, with the real numbers in place of $\mathbb N$, powers such as the $(1 - \alpha)^k$ that appear in the EMA.

    **Order.** For $m, n \in \mathbb N$, define

    $$m < n \;:\Longleftrightarrow\; m \in n, \qquad m \le n \;:\Longleftrightarrow\; (m < n \lor m = n).$$

    Since $n + 1 = n \cup \{n\}$, we have $m < n + 1 \leftrightarrow m \le n$. Since every element of a natural number is a natural number (Transitivity Lemma),

    $$n = \{m \in \mathbb N : m < n\}.$$

    So $n = \{0, 1, \ldots, n - 1\}$: each natural number is the set of the natural numbers before it, as the explorer above showed. For a filter, the number $k$ is literally the set of time steps before step $k$. [Chapter 3](ch3_sets_for_probability.md) uses these sets to define what it means for a set to be finite.

    /// important | 📐 **Theorem (Arithmetic and Order on ℕ)**
        attrs: {class: no-icon}
    For all $a, b, c \in \mathbb N$:

    1. $(a + b) + c = a + (b + c)$ and $(a \cdot b) \cdot c = a \cdot (b \cdot c)$.
    2. $a + b = b + a$ and $a \cdot b = b \cdot a$.
    3. $a \cdot (b + c) = a \cdot b + a \cdot c$.
    4. $a + 0 = a$ and $a \cdot 1 = a$.
    5. If $a + c = b + c$, then $a = b$.
    6. Exactly one of $a < b$, $a = b$, $b < a$ holds.
    7. If $a < b$, then $a + c < b + c$; if moreover $c \neq 0$, then $a \cdot c < b \cdot c$.
    8. If $a \cdot b = 0$, then $a = 0$ or $b = 0$.
    9. Every nonempty subset $X \subseteq \mathbb N$ has a least element: some $m \in X$ with $m \le x$ for every $x \in X$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Each statement is proved by induction from the recursive equations above; the full proofs are in [Appendix B: Arithmetic on the Natural Numbers](appendix_b_number_systems.md). To see the pattern, here is $0 + n = n$, by induction on $n$: $0 + 0 = 0$ by the first equation for addition, and if $0 + n = n$, then $0 + (n + 1) = (0 + n) + 1 = n + 1$ by the second.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - **Sets and $\in$ are primitive.** Extensionality says a set is determined by its elements, so a set specified by a membership condition is unique and can be named.
    - **Each axiom justifies notation, defined right after it:** $\emptyset$ (Empty Set); $\{a, b\}$ and $\{a\}$ (Pairing); $\bigcup F$ and $A \cup B$ (Union); $\{x \in A : \varphi(x)\}$, $A \cap B$, $\bigcap F$ for $F \neq \emptyset$, and $A \setminus B$ (Separation); $\mathcal P(A)$ (Power Set); $\{t(x) : x \in A\}$ (Replacement).
    - **Separation builds only subsets of existing sets**, which avoids Russell's paradox; there is no set of all sets.
    - **Ordered pairs** $(a, b) := \{\{a\}, \{a, b\}\}$ satisfy $(a, b) = (c, d) \leftrightarrow (a = c \land b = d)$. From them we built Cartesian products, relations, and functions (with domain, range, codomain, and the set $Y^X$).
    - **Infinity, Regularity, Choice.** Infinity provides an inductive set; Regularity gives $x \notin x$; Choice provides choice sets and, equivalently, choice functions.
    - **Natural numbers.** $\mathbb N$ is the smallest inductive set, which gives induction; the Peano axioms are theorems.
    - **Recursion.** A starting value and an update rule define exactly one function on $\mathbb N$. With a step index, this is the filter recursion $\hat x_k = G(k, \hat x_{k-1})$.
    - **Arithmetic and order** on $\mathbb N$ are defined by recursion; their properties are proved in Appendix B.

    ## What's Next

    [Chapter 3](ch3_sets_for_probability.md) develops the set theory that probability needs: complements and De Morgan's laws, images and preimages (the tools behind the definition of a random variable), sizes of infinite sets, and the real numbers as a complete ordered field. To see the integers, rationals, and real numbers constructed from $\mathbb N$, read [Appendix B](appendix_b_number_systems.md) before or alongside Chapter 3.
    """)
    return


if __name__ == "__main__":
    app.run()
