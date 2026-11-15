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
app = marimo.App(
    app_title="Mathematical Foundations",
    css_file="notebook-styles.css",
)


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
    ### Connectives

    Logical connectives combine one or more statements into a new statement whose truth value depends only on the truth values of the parts.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Negation

    The negation operator is denoted $\neg$ (read as "not"). When placed to the left of a statement, the new statement has the opposite truth value of the original statement. Letting $T$ represent a placeholder for some true statement, and $F$ represent a placeholder for some false statement, we say that "$\neg T$" evaluates to $F$ and "$\neg F$" evaluates to $T$. This is often represented in the form of a truth table:

    $$\begin{array}{r | c}
    \neg & \\
    \hline
    \mathbf{T} & \text{F} \\
    \mathbf{F} & \text{T} \\
    \end{array}$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Conjunction

    The conjunction operator is denoted $\land$ (read as "and"). When placed between two statements, it evaluates to $T$ if and only if both statements evaluate to $T$, otherwise it evaluates to $F$:

    $$\begin{array}{r | cc}
    \land & \mathbf{T} & \mathbf{F} \\
    \hline
    \mathbf{T} & \text{T} & \text{F} \\
    \mathbf{F} & \text{F} & \text{F} \\
    \end{array}$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Disjunction

    The disjunction operator is denoted $\lor$ (read "or"). When placed between two expressions, it evaluates to $F$ if and only if both expressions evaluate to $F$, otherwise it evaluates to $T$[^de-morgan]:

    $$\begin{array}{r | cc}
    \lor & \mathbf{T} & \mathbf{F} \\
    \hline
    \mathbf{T} & \text{T} & \text{T} \\
    \mathbf{F} & \text{T} & \text{F} \\
    \end{array}$$

    [^de-morgan]: The disjunction operator may also be defined in terms of conjunction, where  $A \lor B$ is just shorthand for $\neg(\neg A \land \neg B)$. Similarly, had we taken $\lor$ as primitive, then $\land$ could be defined as an abbreviation, where $A \land B$ would be shorthand for $\neg(\neg A \lor \neg B)$. This ability to express conjunctions and disjunctions in terms of each other using negation is known as a **dual** in [De Morgan's laws](https://en.wikipedia.org/wiki/De_Morgan%27s_laws).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Conditional

    The conditional operator is denoted $\rightarrow$ (read "implies", or "if ... then ..."). When placed between two expressions, such as:

    $$A \rightarrow B$$

    it acts as shorthand for "$\neg A \lor B$".
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Biconditional

    The biconditional operator is denoted $\leftrightarrow$ (read "if and only if"). When placed between two expressions, such as:

    $$A \leftrightarrow B$$

    it acts as shorthand for "$(A \rightarrow B) \land (B \rightarrow A)$".
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Quantifiers
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Logical quantifiers allow us to make claims about collections of objects by stating how many things in a given domain satisfy some property.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Existential

    The existential quantifier is denoted $\exists$ (read as "there exists"). When placed to the left of a variable, followed by some statement, we interperet the new statement as "There exists at least one value of the variable for which the statement is true":

    $$\exists x\, A$$

    is interpereted as the statement "there exists at least one value of $x$ such that the statement $A$ is true".
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Universal

    The universal quantifier is denoted $\forall$ (read as "for all"). When placed to the left of a variable, followed by some statement, we interperet the new statement as "for all values of the variable, the statement is true":

    $$\forall x\, A$$

    is a shorthand for "$\neg \exists x\, (\neg A)$".
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Relational Operators

    Relational operators compare two quantities or objects and produce a true or false statement (these are different from logical connectives in that they compare values, rather than combining statements).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Equality

    The equality operator (aka equals sign) is denoted "$=$". When placed between two quantities or objects, it produces a true statement iff they have identical values, such as:

    $$x = y.$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Membership

    The membership symbol is denoted $\in$ (read as "is in", or "in"). When placed between a quantity/object and a set, it produces a true statement iff the object on the left is a member of the set on the right, such as:

    $$x \in y.$$

    *Note:* A "set" object in math can be approximately thought of as "any unordered collection of unique objects." The objects in the set are called "members" or "elements" of the set. However, no precise definition exists because sets are a "primitive concept", meaning they are a foundational block on which other terms are defined (a [bottom turtle](https://en.wikipedia.org/wiki/Turtles_all_the_way_down), so to speak, since we cannot have infinite regress of definitions). As such, the concept of sets derives meaning from the [ZFC](https://en.wikipedia.org/wiki/Zermelo%E2%80%93Fraenkel_set_theory) axioms, discussed below.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Formulas

    Now that we have the ability to connect statements, quantify claims about collections of objects, and compare relations between objects, we want some way to combine all of these abilities together. Formulas combine connectives, quantifiers, and relational operators to specify properties of objects. Formulas are defined recursively according to the following 5 rules:

    1. **Atomic:** If $u$ and $v$ are variables (not necessarily distinct), then $u \in v$ and $u = v$ are formulas.
    2. **Negation:** If $\varphi$ is a formula, so is $\neg \varphi$.

    3. **Conjunction:** If $\varphi$ and $\psi$ are formulas, so is $(\varphi \land \psi)$.

    4. **Quantifiers:** If $\varphi$ is a formula and $x$ is a variable, then $\exists x\,\varphi$ is a formula.

    5. **Closure:** Nothing else is a formula.

    Note that since $\lor$, $\rightarrow$, $\leftrightarrow$, $\forall$, are abbreviations using $\neg$, $\land$, $\exists$, they are allowed in formulas as well.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Formula Substitution

    We use the metalanguage notation

    $$\varphi[x/y]$$

    to reference the result of replacing every *free* occurence of $x$ in $\varphi$ by $y$. We only use this when $y$ is a variable that does not occur in $\varphi$, so there are no capture issues.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Free Variable Notation

    Any variable in a formula which is directly to the right of a quantifier (such as $x$ in the formula $\exists x\, \varphi$) is called a *bound variables*. This is because it acts as a place holder value for the collection of objects being quantified, rather than a value which we can freely assign. By contrast, any other variable in a formula which we can freely assign a value to (such as $x$ in the formula $x = y$) is called a *free variable*.

    When we want to specify the free variables of some unspecified formula $\varphi$, we write

    $$\varphi(p_1,\ldots,p_n)$$

    to indicate that the free variables of $\varphi$ are among $p_1,\ldots,p_n$. We might not know how many $p_i$ there are, or even if the $p_i$ necessarily occur as free variables in $\varphi$, but this notation ensures that if a variable is not one of $p_1,\ldots,p_n$, then it does not occur as a free variable in $\varphi(p_1,\ldots,p_n)$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Sentences

    A sentence is a formula with no free variables; every variable occurring in it is bound by a quantifier. While a formula with free variables doesn't have a truth value until we assign values to the variables, sentences are simply true or false in a given structure. In order to build a mathematical system, we must choose some sentences as starting points, which we define as true in our mathematical structure. We call these starting point sentences **axioms**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    :::{div}
    :class: h-0 overflow-hidden opacity-0 m-0 p-0 pointer-events-none

    ### Axiom
    :::

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Axiom**</u>

    A {term}`sentence` that is a starting point in a mathematical structure, which can be used in a proof without justification.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### More Useful Abbreviations

    Before we put this all together to build the foundational axioms of mathematics, here are a few abbreviations that will make our writing easier:

    | Abbreviation | Read as | Abbreviation for |
    | :---: | :---: | :---: |
    | $x \notin y$ | "$x$ is **not in** $y$" | $\neg(x \in y)$ |
    | $x \subseteq y$ | "$x$ is a **subset** of $y$" | $\forall z(z \in x \rightarrow z \in y)$ |
    | $\exists! x\, \varphi$ | "There **exists unique** $x$ such that $\varphi$" | $\exists x\, (\varphi \land \forall y\, (\varphi[y/x] \leftrightarrow y = x))$ |
    | $\exists x \in S\, \varphi$ | "There exists $x$ in $S$ such that $\varphi$" | $\exists x\, (x \in S \land \varphi)$ |
    | $\forall x \in S\, \varphi$ | "For all $x$ in $S$, $\varphi$" | $\forall x\, (x \in S \rightarrow \varphi)$ |

    We take is as intuitive that anything written with these abbreviations could have been written without them.
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
    Set theory is a foundation for nearly all of mathematics[^other-math-foundations], including number theory, functions, topology, algebra, and probability. There are many equivalent ways to formulate the ZFC axioms. Here, we will include all 10 for the purpose of explanation. However, the Axiom of the Null Set is often omitted since it is easily proven by applying the Axiom of Separation to filter out elements which are equal to themselves. Additionally, the Axiom Schema of Separation is sometimes omitted since it can be proven using the Axiom Schema of Replacement.

    [^other-math-foundations]: This is because almost every mathematical object can be defined inside set theory, and almost every theorem can be derived from its axioms. However, alternative foundational theories also exist, such as [Category Theory](https://en.wikipedia.org/wiki/Category_theory), which is common in geometry, and [Type Theory](https://en.wikipedia.org/wiki/Type_theory), which is used in theoretical computer science, as well as the theorem prover programming languages [Lean](https://lean-lang.org) and [Rocq](https://rocq-prover.org).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1. Axiom of Extensionality

    Two sets are equal iff they contain the exact same members:

    $$\forall S_1\forall S_2\,[\forall z\,(z\in S_1\leftrightarrow z\in S_2)\rightarrow S_1=S_2]$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2. Axiom of the Null Set

    There exists a set $S$ such that for all $x$, $x$ is not an element of $S$:

    $$\exists S \forall x (x \notin S)$$

    By Extensionality, this set is unique. It is called the "null set" or "empty set" and is denoted "$\emptyset$".
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3. Axiom of Pairing

    Given any two sets (or objects) $S_1$ and $S_2$, there exists a set $S_3$ that contains $S_1$ and $S_2$ as its only members:

    $$\forall S_1 \, \forall S_2 \, \exists S_3 \, \forall x \, (x \in S_3 \leftrightarrow x = S_1 \lor x = S_2).$$

    By extensionality, this set $S_3$ is unique.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Singleton Sets

    By letting $S_1 = S_2$, the Axiom of Pairing tells us that

    $$\forall S_1\, \exists S_3\, \forall x\, (x \in S_3 \leftrightarrow x = S_1).$$

    This set $S_3$ is called a singleton set because it contains exactly one element, and is denoted $\{S_1\}$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4. Axiom of Power Set

    For any given set $S_1$, there exists a unique set $S_2$ containing precisely all the subsets of $S_1$:

    $$\forall S_1\,\exists S_2\,\forall x\, (x\in S_2 \leftrightarrow x \subseteq S_1)$$

    This set $S_2$ is known as the power set of $S_1$ and is denoted $\mathcal{P}(S_1)$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 5. Axiom of Union

    For any set of sets $X$, there exists a set $U$ whose elements are precisely the elements that belong to at least one of the sets contained in $X$:

    $$\forall X\,\exists U\,\forall y\, [y\in U\leftrightarrow \exists z(z\in X \land y\in z)]$$

    By Extensionality, this union set $U$ is unique. It is commonly denoted as $\bigcup X$ or $\bigcup_{w \in X} w$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Union Operator

    The union operator is denoted $\cup$. When placed between two sets $S_1$ and $S_2$, it is a shorthand to reference the union of the pairing set containing $S_1$ and $S_2$:

    $$S_1 \cup S_2.$$

    Since the paring set is unordered, this operation is commutative and we have

    $$S_1 \cup S_2 = S_2 \cup S_1.$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6. Axiom of Infinity

    At least one infinite set $I$ exists. The empty set $\emptyset$ is an element of $I$, and whenever a set $x$ is an element of $I$, so is its successor $x \cup \{x\}$:

    $$\exists I\, [\emptyset \in I \land \forall x\, (x \in I \rightarrow x \cup \{x\} \in I)].$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 7. Axiom Schema of Separation

    For every formula $\varphi(x, A, p_1, \dots, p_n)$, for any sets $A, p_1, \dots, p_n$, there exists a set $B$ distinct from $(x, A, p_1, \dots, p_n)$ (so $B$ is not free in $\varphi$) whose elements are exactly those elements $x$ of $A$ that satisfy $\varphi$. In other words, every property definable by a formula carves out a subset of any given set:

    $$\forall p_1 \cdots \forall p_n\, \forall A\, \exists B\, \forall x\, [x \in B \leftrightarrow (x \in A \land \varphi)].$$

    This is called an axiom schema, rather than a single axiom, because we want Separation to hold for all formulas $\varphi$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Set-Builder Notation

    When referencing sets, we often use curly braces as shorthand for any set $B$ whose existence is guaranteed by the axiom schema of separation:

    $$\{x \in A: \varphi\}.$$

    By extensionality, this set is unique.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Intersection Operator

    The intersection operator is denoted $\cap$. When placed between two sets, it references the set which contains all elements contained in both sets:

    $$A \cap B = \{x \in A: x \in B\}.$$

    Since this separation treats $A$ and $B$ symetrically, we have

    $$A \cap B = B \cap A.$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 8. Axiom Schema of Replacement

    For every formula $\varphi(x, y, A, p_1, \dots, p_n)$ in which $B$ is not free, if $\varphi$ assigns to each $x \in A$ exactly one $y$, then the collection of all those $y$ values forms a set $B$:

    $$\forall p_1 \cdots \forall p_n\, \forall A\,[\forall x \in A\, \exists! y\, \varphi \rightarrow \exists B\, \forall y\, (y \in B \leftrightarrow \exists x \in A\, \varphi)].$$

    Informally, $\varphi$ acts like a function defined on $A$ (though $\varphi$ is a formula, not a set, so it is not yet a function in the formal sense). Replacement says that the image of a set under such a “function” is again a set. Like Separation, this is a schema because we want it to hold for every formula $\varphi$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 9. Axiom of Regularity

    Every nonempty set $A$ has a member $x$ that shares no members with $A$:

    $$\forall A\,[\exists x\,(x \in A) \rightarrow \exists x \in A\,\neg\exists z\,(z \in x \land z \in A)].$$

    Using the abbreviations above, the last part says $x \cap A = \emptyset$. This is also called the Axiom of Foundation. It rules out sets that are “circular” in their membership. Two consequences:

    No set is a member of itself. If $A \in A$, then the singleton $\{A\}$ is nonempty, so by Regularity it has a member disjoint from it. The only member is $A$, so $A \cap \{A\} = \emptyset$. But $A \in A$ and $A \in \{A\}$, so $A$ is in both, a contradiction.
    There are no infinite descending chains $\cdots \in x_3 \in x_2 \in x_1 \in x_0$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 10. Axiom of Choice

    For any set $X$ whose members are nonempty, pairwise disjoint sets, there exists a set $C$ that contains exactly one element from each member of $X$:

    $$\forall X\,\big[\big(\forall A \in X\,\exists y\,(y \in A) \;\land\; \forall A \in X\,\forall B \in X\,(\neg(A = B) \rightarrow \neg\exists z\,(z \in A \land z \in B))\big) \rightarrow \exists C\,\forall A \in X\,\exists! z\,(z \in A \land z \in C)\big].$$

    The set $C$ is called a choice set or selector for $X$. Unlike the other axioms, Choice asserts that a set exists without giving any rule for constructing it. Informally, it lets us make infinitely many arbitrary selections at once. It is equivalent to several other well-known statements, such as the Well-Ordering Theorem, Zorn’s Lemma, and “every product of nonempty sets is nonempty.”

    Note: The version above (disjoint sets) is one of many equivalent formulations. Another common one says that for every collection of nonempty sets there exists a function that picks an element from each. Once we define functions in terms of sets, this is easy to state, but the disjoint-sets form can be written directly in the language of $\in$ and $=$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Probabilities
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In mathematical terms, the notion of probability depends on sigma algebra
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
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
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, we can define a **probability space**:
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
    ### Coin Toss

    Whenever we talk about the probablility of something happening, we are refering to the value of some $P(A)$, where $P$ is a probability function in some probability space $(\Omega, F, P)$, and $A$ is some event in $F$. For example, let's define a probability space for a coin flip that might produce heads or tails:

    **Defining $\Omega$:** Since we only have two possible samples (heads or tails), $\Omega$ will only have two elements in this case:

    $$\Omega = \{H, T\}.$$

    Note: this is a shorthand for $\exists \Omega\, (x \in \Omega \leftrightarrow x = H \lor x = T)$. More generally, we will sometimes use "$S = \{x_1, \ldots, x_n\}$" as a shorthand for $\exists S\, (y \in S \leftrightarrow y = x_1 \lor \cdots \lor y = x_n)$, or simply "$\{x_1, \ldots, x_n\}$" to refer to that set $S$.

    **Defining $F$:** Since $\mathcal P(\Omega) = \{\{H, T\}, \{H\}, \{T\}, \emptyset\}$, we only have a couple options here which are closed under complementation and countable unions:

    1. $F = \{\{H, T\}, \emptyset\}$. This is the simplest, but the only events are "something happening" (equal to $\Omega$, with $P(\Omega) = 1$), and "nothing happening" (where $P(\emptyset)$ is always zero to satisfy additivity). The rules allow it, but it's not very interesting.
    2. $F = \mathcal P(\Omega)$. This also works as a $\sigma$-algebra and is much more interesting because it includes $\{H\}$ and $\{T\}$ as events. Let's use this one.

    **Defining $P$:** We must have $P(\Omega) = 1$ and $P(\emptyset) = 0$, but we are free to pick any $P(\{H\})$ and $P(\{T\})$ that satisfy

    $$P(\{H\}) + P(\{T\}) = P(\{H\} \cup \{T\}) = P(\{H, T\}) = P(\Omega) = 1.$$

    The natural choice is $P(\{H\}) = P(\{T\}) = 0.5$, but we're free to model an unfair coin if we wish.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
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
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Random Number

    Now, let's model picking a random number from $[0, 1]$.

    **Defining $\Omega$:**

    **Defining $F$:**

    **Defining $P$:**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Conditional Probability

    If $A$ and $B$ are events in a probability space, then the conditional probability $P(A|B)$ (read as "probability of A given B") is defined as

    $$P(A|B) := \frac{P(A \cap B)}{P(B)}$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Bayes Theorem

    Since $A \cap B = B\cap A$, we have

    $$\begin{align*}
    P(A|B) &= \frac{P(A \cap B)}{P(B)} \\
    &= \frac{P(A)\left(\frac{P(B \cap A}{P(A)}\right)}{P(B)} \\
    &= \frac{P(A)P(B|A)}{P(B)}
    \end{align*}$$
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


if __name__ == "__main__":
    app.run()
