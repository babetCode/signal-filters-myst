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
app = marimo.App(app_title="Foundations", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "The Basis of Everything"
    abbreviations:
      iff: if and only if
      diff: null
      ZFC: Zermelo-Frankel set theory with Axiom of Choice
    numbering:
      equations: false
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
    Our goal when designing a signal filter is to algorithmically remove noise from a measurement signal. As we saw in the past two sections, this is usually done by combining our knowlege and measurements in a way that increases the probability that the noise cancels out. In terms of the equations we've been working with:

    $$\hat{x}_k = \hat x_k^- + \alpha (z_k - \hat x_k^-).$$

    :::{div}
    :class: h-0 overflow-hidden opacity-0 m-0 p-0 pointer-events-none

    ## Key Question
    :::

    Now we lay the groundwork for answering the question:

    >"Given some amounts of noise in our prior ($\hat x_k^-$) and measurement ($z_k$), what value of $\alpha$ should we pick?"

    Since modeling noise relies on probabilities, probabilities are built on set theory, and set theory is built on logic, we will briefly introduce these topics along the way.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Language of Logic
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Developing precise language is vital for communicating a precise understanding of any topic. As we introduce new language over the coming chapters, it is important to keep in mind that we will be switching back and fourth between three different layers of language:
    - **Metalanguage:** This is plain language we use to talk *about* the formal mathematical language we are developing.  For example, most of the writing between the lines of math in this book is plain english, and not rigourously defined. While we try our best to be articulate and specific, metalanguage is not formal.
    - **Syntax:** This refers to the raw symbols (or strings of symbols) we use in our formal mathematical language, *before* any meaning is interpereted. So far in this book, our syntax has consisted of the roman alphabet, greek alphabet, numbers, algebraic symbols, and some combinations of letters with symbols (such as "$\hat x _k^-$"). However, we are about to introduce some new symbols.
    - **Semantics:** This the list of rules and convetions which dictate how the symbols (or strings of symbols) in our syntax are interpereted. For example the convention is this book is to interperet "$\hat x _k^-$" as "the prediction at time $k$ prior to the measurement at time $k$".
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Statement**</u>
    Any finite string of symbols (most statements are meaningless, such as $a \forall)6!$").
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A **Boolean variable**[^george-boole] represents a truth value: either **True** or **False**. In the lingo, we say that if $A$ is a boolean variable, then it **evaluates** to $T$ (true) or $F$ (false). We can create **boolean expressions** by combining boolean variables with the following **connective operators**[^connectives]:

    [^george-boole]: Named after British mathematician George Boole.

    [^connectives]: This is not an exhaustive list of all connectives, but it includes the most common ones which are useful for building our notion of set theory.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Logical Connectives
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Negation

    The negation operator is denoted $\neg$ (read as "not"). When placed to the left of an expression, it evaluates to the opposite of the original expression[^expression]:

    $$\begin{array}{r | c}
    \neg & \\
    \hline
    \mathbf{T} & \text{F} \\
    \mathbf{F} & \text{T} \\
    \end{array}$$

    For example, "$\neg T$" evaluates to $F$.

    [^expression]: The $\neg$ operator may also be placed to left of a boolean variable or a bare truth value, since these count as expressions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Conjunction

    The conjunction operator is denoted $\land$ (read as "and"). When placed between two expressions, it evaluates to $T$ if and only if both expressions evaluate to $T$, otherwise it evaluates to $F$:

    $$\begin{array}{r | cc}
    \land & \mathbf{T} & \mathbf{F} \\
    \hline
    \mathbf{T} & \text{T} & \text{F} \\
    \mathbf{F} & \text{F} & \text{F} \\
    \end{array}$$

    For example, "$T \land F$" evaluates to $F$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Disjunction

    The disjunction operator is denoted $\lor$ (read "or"). When placed between two expressions, it evaluates to $F$ if and only if both expressions evaluate to $F$, otherwise it evaluates to $T$:

    $$\begin{array}{r | cc}
    \lor & \mathbf{T} & \mathbf{F} \\
    \hline
    \mathbf{T} & \text{T} & \text{T} \\
    \mathbf{F} & \text{T} & \text{F} \\
    \end{array}$$

    For example, "$T \lor F$" evaluates to $T$[^de-morgan].

    [^de-morgan]: The disjunction operator may also be defined in terms of conjunction, where  $A \lor B$ is just shorthand for $\neg(\neg A \land \neg B)$. Similarly, had we taken $\lor$ as primitive, then $\land$ could be defined as an abbreviation, where $A \land B$ would be shorthand for $\neg(\neg A \lor \neg B)$. This ability to express conjunctions and disjunctions in terms of each other using negation is known as a **dual** in [De Morgan's laws](https://en.wikipedia.org/wiki/De_Morgan%27s_laws).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Conditional

    The conditional operator is denoted $\rightarrow$ (read "implies", or "if ... then ..."). When placed between two expressions, such as $A \rightarrow B$, it acts as shorthand for

    $$\neg A \lor B.$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Bionditional

    The biconditional operator is denoted $\leftrightarrow$ (read "if and only if"). When placed between two expressions, such as $A \leftrightarrow B$, it acts as shorthand for

    $$(A \rightarrow B) \land (B \rightarrow A).$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Logical Quantifiers
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Unlike connectives, which
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### For All

    The quantifier $\forall$ (read as "for all"),
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### There Exists

    The quantifier $\exists$ (read as "there exists")
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Relation Operators
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Equality
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The equals sign "$=$" is placed between expressions which evaluate identically.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Membership

    The membership symbol $\in$ (read as "is in", or "in") represents membership in a set and is placed between the member (to the left) and the set (to the right), such as $x \in S$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Formulas
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The **formulas** of set theory are defined recursively according to the following 4 rules:

    1. **(Atomic)** If $u$ and $v$ are variables (not necessarily distinct), then
       $u \in v$ and $u = v$ are formulas.
    2. **(Connectives)** If $\psi$ and $\chi$ are formulas, then so are
       $\neg\psi$, $(\psi \land \chi)$, $(\psi \lor \chi)$,
       $(\psi \to \chi)$, and $(\psi \leftrightarrow \chi)$.
    3. **(Quantifiers)** If $\psi$ is a formula and $u$ is a variable, then
       $\forall u\,\psi$ and $\exists u\,\psi$ are formulas.
    4. **(Closure)** Nothing else is a formula.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ZFC Axioms
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Set theory is a foundation for nearly all of mathematics, including number theory, functions, topology, algebra, and probability[^other-math-foundations]. In this section we will introduce the notion, theory, and some of its implications.

    [^other-math-foundations]: This is because almost every mathematical object can be defined inside set theory, and almost every theorem can be derived from its axioms (usually ZFC). However, alternative foundational theories also exist, such as [Category Theory](https://en.wikipedia.org/wiki/Category_theory), which is common in geometry, and [Type Theory](https://en.wikipedia.org/wiki/Type_theory), which is used in theoretical computer science, as well as the theorem prover programming languages [Lean](https://lean-lang.org) and [Rocq](https://rocq-prover.org).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A "set" in math can be approximately thought of as "any unordered collection of unique objects." However, no single, precise definition exists, because sets considered are a "primitive concept"—meaning they are a foundational block on which other terms are defined (a [bottom turtle](https://en.wikipedia.org/wiki/Turtles_all_the_way_down), so to speak, since we cannot have infinite regress of definitions). As such, the concept of sets derives meaning from the [ZFC](https://en.wikipedia.org/wiki/Zermelo%E2%80%93Fraenkel_set_theory) axioms[^zfc-axioms]:

    [^zfc-axioms]: There are many equivalent ways to formulate the ZFC axioms. The list shown here from [quanta magazine](https://www.quantamagazine.org/why-maths-final-axiom-proved-so-controversial-20260429/) includes all 10 for pedagogical/historical reasons. However, the Null Set axiom is often omitted since it is easily proven by applying the axiom of Separation to filter out elements which are equal to themselves. Additionall, the axiom of Separation is sometimes omitted since it can be proven using the axiom of Replacement.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/zfc_axioms.svg" class="graphic" alt="Scale Diagram" height="700" style="max-height: 50em" />
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The objects in a set are called "elements", and we denote that an element $x$ is in a set $S$ as

    $$x \in S,$$

    where "$\in$" is read as "is in". Additionally, the following symbols are useful when discussing sets:

    | Symbol | Read as | TeX command |
    | :--- | :--- | :--- |
    | $\in$ | **"is an element of"** / **"is in"** | `\in` |
    | $\forall$ | **"for all"** / **"for every"** | `\forall` |
    | $\exists$ | **"there exists"** | `\exists` |
    | $\exists!$ | **"there exists a unique"** | `\exists!` |
    | $\land$ | **"and"** (Conjunction) | `\wedge` or `\land` |
    | $\lor$ | **"or"** (Disjunction) | `\vee` or `\lor` |
    | $\neg$ | **"not"** (Negation) | `\neg` or `\lnot` |
    | $\rightarrow$ | **"implies"** / **"if... then..."** | `\rightarrow` or `\to` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As well as the following abbreviations:

    | Symbol | Read as | Abbreviation for | TeX command |
    | :--- | :--- | :--- | :--- |
    | $x \notin S$ | "$x$ is **not in** $S$" | $\neg(x \in S)$ | `\notin` |
    | $S_1 \subseteq S_2$ | "$S_1$ is a **subset** of $S_2$" | $\forall x(x \in S_1 \rightarrow x \in S_2)$ | `\subseteq` |
    | $a \leftrightarrow b$ | "$a$ **if and only if** $b$" (Biconditional) | $(a \rightarrow b) \land (b \rightarrow a)$ | `\leftrightarrow` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    | Axiom | Statement |
    | :-----: | :---------: |
    | Null Set | $\exists S[\forall x(x \notin S)]$ |
    | Extensionality | $[(S_1 \subseteq S_2) \land (S_2 \subseteq S_1)] \rightarrow (S_1 = S_2)$ |
    | Pairs | $\forall S_1 \forall S_2(\exists S_3[(S_1 \in S_3) \land (S_2 \in S_3)])$ |
    | Power Set | $\forall S_1 \exists S_2[\forall x(x \subseteq S_1 \rightarrow x \in S_2)]$ |
    | Union | $\forall S_1 \exists S_2[\forall S_3 \forall x([S_3 \in S_1 \land x \in S_3] \rightarrow x \in S_2)]$ |
    | Infinity | $\exists S_1[(\emptyset \in S_1) \land \forall x(x \in S_1 \rightarrow \exists S_2[(x \in S_2) \land (S_2 \in S_1)])]$ |
    | Separation | I don't know |
    | Replacement | I don't know |
    | Regularity | $\forall S(S \notin S)$ |
    | Choice | I don't know |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    | Axiom | Statement |
    | :-----: | :---------: |
    | Null Set | *Write here* |
    | Extensionality | *Write here* |
    | Pairs | *Write here* |
    | Power Set | *Write here* |
    | Union | *Write here* |
    | Infinity | *Write here* |
    | Separation | *Write here* |
    | Replacement | *Write here* |
    | Regularity | *Write here* |
    | Choice | *Write here* |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Using these symbols, we can write our axioms as:

    - **Null Set:** $\exists S[\forall x(x \notin S)]$ (This set is called the "null set" and is denoted $\emptyset$).
    - **Extensionality:** $[(S_1 \subseteq S_2) \land (S_2 \subseteq S_1)] \rightarrow (S_1 = S_2)$.
    - **Pairs:** $\forall S_1 \forall S_2(\exists S_3[(S_1 \in S_3) \land (S_2 \in S_3)])$.
    - **Power Set:** $\forall S_1 \exists S_2[\forall x(x \subseteq S_1 \rightarrow x \in S_2)]$.
    - **Union:** $\forall S_1 \exists S_2[\forall S_3 \forall x([S_3 \in S_1 \land x \in S_3] \rightarrow x \in S_2)]$.
    - **Infinity:** $\exists S_1[(\emptyset \in S_1) \land ]$.
    - **Null Set:** $$.
    - **Null Set:** $$.
    - **Null Set:** $$.
    - **Null Set:** $$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What is probability
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In mathematical terms, the notion of probability depends on a **probability space**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    :::{div}
    :class: h-0 overflow-hidden opacity-0 m-0 p-0 pointer-events-none

    ### Probability Space
    :::

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Probability Space**</u>
    a triple $(\Omega, F, P)$, where:
    - $\Omega$ is a set (the sample space),
    - $F$ is a $\sigma$-algebra of subsets of $\Omega$ (the “events”),
    - $P$ is a function from $F$ to $[0,1]$ satisfying: $P(\Omega) = 1$, and countable additivity (for pairwise disjoint events $A_1, A_2, ..., P(\bigcup A_i) = ΣP(Aᵢ))$.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Sigma Algebra

    A $\sigma$-algebra $F$ og a set $\Omega$ (called the ambient set) is a set of subsets of $\Omega$ which satisfy three criteria:

    1. $\Omega \in F$
    2. $S \in F \rightarrow S^c = \{x \in \Omega: x \notin S\} \in F$
    3. $S_1, S_2, S_3, \ldots \in F \rightarrow \bigcup_{i=1}^\infty S_i \in F$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Discrete probabilties.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Discrete probablity distributions are the typical type of probablity we encounter in a "50/50" coin toss or "hitting the red" in roulette. There are a finite nubmer of possible outcomes, exactly one of which will actually be true. Since we don't know which one, we assign some probabilty to each, and since *something* must be true, the sum of all probabilities is 1.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Intersections
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The conditional probability $A$ given $B$ is defined
    $$P(A|B) := \frac{P(A\cap B)}{P(B)}$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Modeling Noise
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As previously discussed, it is impossible to measure anything with 100% precision. Because measurements are unpredicatble, we say that the measurement {term}`signal` is {term}`stochastic`. Therefore, we model measurements as being sampled from a **probability density function** (PDF).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Brainstorm
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    modeling the measurement as the sum of the true value with a noise value, which we can write as
    $$z = x + \eta$$
    combining our knowlege and measurements to increase the
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The mean of a PDF is defined as
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ###
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Bayesian statistics
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
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
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, consider a hypothetical game of darts where the horizontal position of the dart is normally distributed. In other words, the probability that the dart's horizontal position lands $x$ to the right of the the bullseye is
    $$x \sim \mathcal N(0, \sigma^2).$$
    Imagine that a dart is thrown while you are not watching, and then you are only told that dart fell to the right of the bullseye. Given only this information, how should you update your distribution for $x$?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, consider the following thought experiement: you are driving a car on "x-axis ave." in mythical math world. an infinitely long, perfectly straight road. Your are completely lost, but have a GPS to locate your position on the road—the GPS has some Gaussian noise in the reading. In other words, given some position reading by the GPS, the probability distribution of your position can be represented as a normal curve centered at the reading.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Bayes theorem gives

    $$p(X|Z) = \frac{p(Z|X)p(X)}{p(Z)},$$
    where:
    - $p(X)$ is the prior density.
    - $p(Z|X)$ is the likelihood.
    - $p(X|Z)$ is the posterior density.
    - $p(Z)$ is the evidence, or marginal likelihood.
    """)
    return


@app.cell
def _():
    # TODO figure out if there's a difference between the mean vs the expected value of a PDF, does the term "expected value" even apply to a PDF or only to a sample taken from it?

    # TODO explain convolutions
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
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
    """)
    return


if __name__ == "__main__":
    app.run()
