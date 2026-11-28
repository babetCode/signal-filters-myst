# /// script
# dependencies = [
#     "marimo>=0.25.1",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="Appendix A: Formal Logic", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "Syntax, Semantics, and Proof"
    description: "An optional, exact account of the formulas, structures, and formal proofs behind the informal logic of Chapter 1."
    label: appa
    -->
    """)
    return


@app.cell
def imports():
    # jb: include=false
    import marimo as mo
    from textwrap import dedent

    return dedent, mo


@app.cell
def display_settings(dedent, mo):
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
    - [Chapter 1](#ch1): [connectives, truth tables](#ch1-sec-connectives-and-truth-tables), {term}`quantifiers <quantifier>`, and [informal proofs](#ch1-sec-proof-techniques).
    - [Chapter 2](#ch2) (optional): [the ZFC axioms](#ch2-sec-the-axioms-of-zfc) used as examples here.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Chapter 1](#ch1) treated logic as a working tool: statements, their meanings, and rules for proving them, all described in English. This appendix makes each of those notions exact, for the language of set theory used in [Chapter 2](#ch2). It is optional: nothing on the main path depends on it. It answers two questions the main path takes on trust: what exactly counts as a statement of set theory, and why the informal proofs of the book establish what they claim.

    /// attention | 🗝️ **Key Idea**
    A formal language has three layers. **Syntax** says which strings of symbols are formulas and which sequences of formulas are proofs, without reference to meaning. **Semantics** says what a formula means in a given structure. The **Soundness and Completeness Theorem** says the two agree: a sentence is provable from a theory iff it is true in every structure in which the theory's axioms are true.
    ///

    Throughout, we reason *about* the formal language in English and informal mathematics, the **metalanguage**. Symbols such as $\varphi$, $\psi$, $\mathfrak A$, $\models$, and $\vdash$ belong to the metalanguage: they name formulas, structures, and relations between them, and are not symbols of the formal language itself. The last section, The Metatheory, discusses what this informal background assumes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: appa-sec-formal-syntax -->
    ## Formal Syntax

    In this section the symbols are only marks on paper. We say what they mean in Formal Semantics below.

    <!-- label: appa-sec-symbols -->
    ### Symbols

    The symbols of the language of set theory are:

    - **Variables:** $x, y, z, u, v, w, \ldots$, with subscripts ($x_1, x_2, \ldots$) so that there are infinitely many.
    - **Relation symbols:** $\in$ (read "is in") and $=$ (read "equals").
    - **Negation** $\lnot$, **conjunction** $\land$, and the **existential quantifier** $\exists$.
    - **Parentheses** $($ and $)$.

    The other symbols of [Chapter 1](#ch1) ($\lor$, $\rightarrow$, $\leftrightarrow$, $\forall$, and more) are introduced below as abbreviations. Using few primitive symbols keeps every definition and proof by cases in this appendix short. A general first-order language may also have constant symbols, function symbols, and other relation symbols; the language of set theory needs none of them, and Extension by Definitions shows how defined ones are added.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: appa-sec-formulas -->
    ### Formulas

    In the rules below, $\varphi$ and $\psi$ stand for arbitrary formulas and $u$, $v$, $x$ for arbitrary variables. These letters belong to the metalanguage.

    /// note | 📖 **Definition**
    <u>**Formula**</u>

    A finite string of symbols obtained by finitely many applications of these rules:

    1. **Atomic:** if $u$ and $v$ are variables (not necessarily distinct), then $u \in v$ and $u = v$ are formulas.
    2. **Negation:** if $\varphi$ is a formula, then $\lnot\varphi$ is a formula.
    3. **Conjunction:** if $\varphi$ and $\psi$ are formulas, then $(\varphi \land \psi)$ is a formula.
    4. **Quantifier:** if $\varphi$ is a formula and $x$ is a variable, then $\exists x\,\varphi$ is a formula.
    ///

    For example, $\exists x\,(x \in y \land \lnot\, x = y)$ is a formula. It is built in stages: the atomic formulas $x \in y$ and $x = y$, then $\lnot\, x = y$, then $(x \in y \land \lnot\, x = y)$, then the quantified formula. Since every formula is built in finitely many steps, a property can be proved for all formulas by *induction on formulas*: prove it for atomic formulas, and prove that rules 2–4 preserve it. (Formally, this is induction on the number of symbols.)

    The parentheses in rule 3 make the construction of each formula unambiguous, which is what lets later definitions proceed "by cases on the last rule used".

    /// admonition | 📐 **Lemma (Unique Readability)**
        attrs: {class: lemma, id: appa-lem-unique-readability}
    1. No formula is a proper initial segment of another formula.
    2. Every formula is either atomic, or equal to exactly one of $\lnot\varphi$, $(\varphi \land \psi)$, $\exists x\,\varphi$, and in that case $\varphi$, $\psi$, $x$ are uniquely determined.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    1. Suppose $\chi'$ is a formula that is a proper initial segment of a formula $\chi$; we derive a contradiction by induction on the length of $\chi$. The two share their first symbol. If it is a variable, both are atomic, hence both have exactly three symbols, so they are equal. If it is $\lnot$, then $\chi = \lnot\alpha$ and $\chi' = \lnot\alpha'$ with $\alpha'$ a proper initial segment of $\alpha$, contradicting the induction hypothesis. The case $\exists$ is the same, since the variable after $\exists$ is also shared. If it is $($, then $\chi = (\alpha \land \beta)$ and $\chi' = (\alpha' \land \beta')$. One of $\alpha$, $\alpha'$ is an initial segment of the other, so by the induction hypothesis $\alpha = \alpha'$. Then one of $\beta$, $\beta'$ is an initial segment of the other, so $\beta = \beta'$, and $\chi' = \chi$, contradicting properness.
    2. The first symbol determines the form: a variable (atomic), $\lnot$, $($, or $\exists$. For $\lnot\varphi$ and $\exists x\,\varphi$, the parts are what follows the first one or two symbols. For $(\varphi \land \psi)$, if also $(\varphi \land \psi) = (\varphi' \land \psi')$, then one of $\varphi$, $\varphi'$ is an initial segment of the other, so $\varphi = \varphi'$ by part 1, and then $\psi = \psi'$. $\blacksquare$
    ///

    Besides formulas, a first-order language has *terms*, expressions that name objects rather than make claims. In the language of set theory the only terms are variables. Defined terms such as $\emptyset$ and $\{x, y\}$ are added in Extension by Definitions below.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: appa-sec-free-and-bound-variables -->
    ### Free and Bound Variables

    Each occurrence of a variable in a formula is *free* or *bound*, according to these rules:

    - In an atomic formula $u \in v$ or $u = v$, every occurrence of a variable is free.
    - The free occurrences in $\lnot\varphi$ are those in $\varphi$.
    - The free occurrences in $(\varphi \land \psi)$ are those in $\varphi$ together with those in $\psi$.
    - In $\exists x\,\varphi$, the occurrence of $x$ right after $\exists$ and every occurrence of $x$ in $\varphi$ are bound; an occurrence of any other variable is free exactly when it is free in $\varphi$.

    An occurrence that is not free is bound. A bound occurrence is a placeholder for "some object", not a slot for a particular value.

    /// note | 📖 **Definition**
    <u>**Free variable**</u>

    A variable $x$ is a free variable of a formula $\varphi$ iff at least one occurrence of $x$ in $\varphi$ is free.
    ///

    /// note | 📖 **Definition**
    <u>**Bound variable**</u>

    A variable $x$ is a bound variable of a formula $\varphi$ iff at least one occurrence of $x$ in $\varphi$ is bound.
    ///

    A variable can be both free and bound in the same formula. In

    $$(x = y \land \exists x\,(x \in y)),$$

    the first $x$ is free and the other two are bound, so the values of the two $x$'s have nothing to do with each other: the bound one could be renamed $z$ without changing the meaning. Both occurrences of $y$ are free, so both must stand for the same object. The free variables of this formula are $x$ and $y$, and its only bound variable is $x$.

    We write $\varphi(p_1, \ldots, p_n)$ to indicate that the free variables of $\varphi$ are *among* $p_1, \ldots, p_n$: a variable not in the list does not occur free in $\varphi$, but a listed variable need not occur free.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: appa-sec-sentences -->
    ### Sentences

    /// note | 📖 **Definition**
    <u>**Sentence**</u>

    A {term}`formula` with no {term}`free variables <free variable>`.
    ///

    For example, $\exists x\,\lnot\exists y\,(y \in x)$ is a sentence, while $\exists y\,(y \in x)$ is not, because $x$ is free in it. A formula with free variables makes a claim only once its free variables are given values; a sentence makes a claim outright. Formal Semantics below makes this precise, and the axioms of a theory are always sentences.

    <!-- label: appa-sec-substitution -->
    ### Substitution

    For a formula $\varphi$ and variables $x$, $y$, let $\varphi[x/y]$ be the result of replacing every *free* occurrence of $x$ in $\varphi$ by $y$. We say $y$ is *substitutable for* $x$ in $\varphi$ iff no free occurrence of $x$ in $\varphi$ lies inside a part of $\varphi$ of the form $\exists y\,\psi$. Then each new occurrence of $y$ is free, and $\varphi[x/y]$ says about $y$ exactly what $\varphi$ says about $x$. Otherwise the new $y$ would be *captured*: if $\varphi$ is $\exists y\,(y \in x)$ ("$x$ has an element"), then $\varphi[x/y]$ is $\exists y\,(y \in y)$ ("something is an element of itself"), a different claim. A variable that does not occur in $\varphi$ at all is always substitutable. When $\varphi$ is written $\varphi(x)$, we write $\varphi(y)$ for $\varphi[x/y]$, and only when $y$ is substitutable for $x$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: appa-sec-abbreviations -->
    ### Abbreviations

    The notation $\text{new} := \text{old}$ says that the left side is shorthand for the right side. Like $\varphi$, the symbol $:=$ belongs to the metalanguage. Anything written with these abbreviations can be rewritten without them by unpacking, so they add no expressive power.

    | Notation $:=$ Definition | Read as |
    |:---|:---|
    | $(\varphi \lor \psi) := \lnot(\lnot\varphi \land \lnot\psi)$ | "$\varphi$ **or** $\psi$" (disjunction) |
    | $(\varphi \rightarrow \psi) := (\lnot\varphi \lor \psi)$ | "**if** $\varphi$ **then** $\psi$" (conditional) |
    | $(\varphi \leftrightarrow \psi) := ((\varphi \rightarrow \psi) \land (\psi \rightarrow \varphi))$ | "$\varphi$ **if and only if** $\psi$" (biconditional) |
    | $\forall x\,\varphi := \lnot\exists x\,\lnot\varphi$ | "**for all** $x$, $\varphi$" (universal quantifier) |
    | $u \notin v := \lnot\, u \in v$ | "$u$ is **not in** $v$" |
    | $u \neq v := \lnot\, u = v$ | "$u$ is **not equal to** $v$" |
    | $u \subseteq v := \forall z\,(z \in u \rightarrow z \in v)$ | "$u$ is a {term}`subset` of $v$" |
    | $\exists! x\,\varphi := \exists x\,(\varphi \land \forall y\,(\varphi[x/y] \rightarrow y = x))$ | "there **exists exactly one** $x$ such that $\varphi$" |
    | $\existsin{x}{v} \varphi := \exists x\,(x \in v \land \varphi)$ | "there **exists** $x$ **in** $v$ such that $\varphi$" |
    | $\forallin{x}{v} \varphi := \forall x\,(x \in v \rightarrow \varphi)$ | "**for all** $x$ **in** $v$, $\varphi$" |
    | $\existssubseteq{x}{v} \varphi := \exists x\,(x \subseteq v \land \varphi)$ | "there **exists** a **subset** $x$ of $v$ such that $\varphi$" |
    | $\forallsubseteq{x}{v} \varphi := \forall x\,(x \subseteq v \rightarrow \varphi)$ | "**for all subsets** $x$ of $v$, $\varphi$" |

    In each row, the variables shown are distinct, $z$ is not $u$ or $v$, $x$ is not $v$, and in the row for $\exists!$ the variable $y$ does not occur in $\varphi$ (so it is substitutable for $x$). We also drop outer parentheses and use the precedence conventions of [Chapter 1](#ch1-sec-connectives-and-truth-tables).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: appa-sec-formal-semantics -->
    ## Formal Semantics

    So far we have only manipulated strings. Now we say what they mean.

    <!-- label: appa-sec-structures -->
    ### Structures

    To give a formula a meaning, we must say which objects the variables stand for and which of those objects count as "members" of which.

    /// note | 📖 **Definition**
    <u>**Structure**</u>

    A pair $\mathfrak A = (A, E)$ consisting of a nonempty collection $A$ of objects, called the *domain of discourse*, and a specification $E$ that says, for each ordered choice of objects $a, b \in A$, whether $a$ counts as a member of $b$ (written $a \mathrel{E} b$) or not.
    ///

    The symbol $\in$ is interpreted by $E$, and $=$ is always interpreted as identity (being the same object). A structure is an *interpretation* of the language: it fixes what the variables range over and what $\in$ means. The structure need not consist of sets, and $E$ need not resemble membership. For example, $\mathfrak N = (\mathbb N, <)$, the natural numbers with "$a \mathrel{E} b$ iff $a < b$", is a structure. The structure the main path has in mind is the *intended structure*, whose domain consists of all sets and whose $E$ is actual membership. That domain is not itself a set, a subtlety discussed in The Metatheory.

    Formulas are not objects in the domain of discourse. They are strings of symbols, described in the metalanguage. That is why the placeholders $\varphi$, $\psi$ for formulas differ in kind from variables like $x$ and $y$, which stand for objects in the domain. A quantifier $\exists x$ ranges over the domain: it makes a claim about objects, never about formulas.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: appa-sec-satisfaction -->
    ### Satisfaction

    Fix a structure $\mathfrak A = (A, E)$. An *assignment* is a rule $s$ that gives each variable $x$ a value $s(x) \in A$. For an assignment $s$, a variable $x$, and $a \in A$, let $s(x \mid a)$ be the assignment that gives $x$ the value $a$ and agrees with $s$ on every other variable.

    We define "$\mathfrak A$ *satisfies* $\varphi$ with $s$", written $\mathfrak A \models \varphi[s]$, by induction on formulas, one clause per formation rule:

    1. $\mathfrak A \models (u \in v)[s]$ iff $s(u) \mathrel{E} s(v)$.
    2. $\mathfrak A \models (u = v)[s]$ iff $s(u)$ and $s(v)$ are the same object.
    3. $\mathfrak A \models \lnot\varphi[s]$ iff not $\mathfrak A \models \varphi[s]$.
    4. $\mathfrak A \models (\varphi \land \psi)[s]$ iff $\mathfrak A \models \varphi[s]$ and $\mathfrak A \models \psi[s]$.
    5. $\mathfrak A \models \exists x\,\varphi[s]$ iff there is some $a \in A$ with $\mathfrak A \models \varphi[s(x \mid a)]$.

    By Unique Readability, exactly one clause applies to each formula, so this defines satisfaction for every formula. We also say $\varphi$ is *true* in $\mathfrak A$ under $s$.

    /// admonition | 📐 **Lemma (Coincidence)**
        attrs: {class: lemma, id: appa-lem-coincidence}
    If assignments $s$ and $s'$ agree on every free variable of $\varphi$, then $\mathfrak A \models \varphi[s]$ iff $\mathfrak A \models \varphi[s']$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    By induction on formulas. For atomic $\varphi$, every variable in $\varphi$ is free, so $s$ and $s'$ give them the same values and clauses 1–2 agree. For $\lnot\varphi$ and $\varphi \land \psi$, the free variables of the parts are free in the whole, so the induction hypothesis applies to the parts and clauses 3–4 agree. For $\exists x\,\varphi$: its free variables are those of $\varphi$ other than $x$. For each $a \in A$, the assignments $s(x \mid a)$ and $s'(x \mid a)$ agree on $x$ (both give $a$) and on every other free variable of $\varphi$, so by the induction hypothesis $\mathfrak A \models \varphi[s(x \mid a)]$ iff $\mathfrak A \models \varphi[s'(x \mid a)]$. Hence the two sides of clause 5 agree. $\blacksquare$
    ///

    A sentence has no free variables, so by the [Coincidence lemma](#appa-lem-coincidence) it is satisfied by all assignments or by none. (At least one assignment exists because $A$ is nonempty.) We say a sentence $\sigma$ is *true in* $\mathfrak A$, written $\mathfrak A \models \sigma$, if it is satisfied by every assignment, and *false in* $\mathfrak A$ otherwise. For example, $\exists x\,\lnot\exists y\,(y \in x)$ is true in $(\mathbb N, <)$, because nothing is less than $0$, while $\forall x\,\exists y\,(y \in x)$ is false there.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: appa-sec-derived-symbols -->
    ### Derived Symbols

    Unpacking the abbreviations and applying clauses 3–5 recovers exactly the truth tables and quantifier meanings of [Chapter 1](#ch1). Fix $\mathfrak A$ and $s$, and say "$\varphi$ is true" for $\mathfrak A \models \varphi[s]$.

    - $\varphi \lor \psi$ is $\lnot(\lnot\varphi \land \lnot\psi)$, which is false iff $\lnot\varphi$ and $\lnot\psi$ are both true, that is, iff $\varphi$ and $\psi$ are both false.
    - $\varphi \rightarrow \psi$ is $\lnot\varphi \lor \psi$, which is false iff $\lnot\varphi$ and $\psi$ are both false, that is, iff $\varphi$ is true and $\psi$ is false.
    - $\varphi \leftrightarrow \psi$ is $(\varphi \rightarrow \psi) \land (\psi \rightarrow \varphi)$, which is true iff neither "$\varphi$ true and $\psi$ false" nor "$\psi$ true and $\varphi$ false" holds, that is, iff $\varphi$ and $\psi$ have the same truth value.
    - $\forall x\,\varphi$ is $\lnot\exists x\,\lnot\varphi$, which is true iff no $a \in A$ makes $\lnot\varphi$ true under $s(x \mid a)$, that is, iff every $a \in A$ makes $\varphi$ true under $s(x \mid a)$.

    Two formulas $\varphi$ and $\psi$ are *logically equivalent* if $\mathfrak A \models \varphi[s]$ iff $\mathfrak A \models \psi[s]$ for every structure $\mathfrak A$ and every assignment $s$. This extends {term}`logical equivalence <logically equivalent>` of statement forms from Chapter 1 to formulas with quantifiers; for example, $\lnot\forall x\,\varphi$ and $\exists x\,\lnot\varphi$ are logically equivalent, by the last bullet and double negation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: appa-sec-models -->
    ### Models

    /// note | 📖 **Definition**
    <u>**Model**</u>

    A structure $\mathfrak A$ is a model of a collection $\Gamma$ of sentences, written $\mathfrak A \models \Gamma$, iff every sentence in $\Gamma$ is true in $\mathfrak A$.
    ///

    For example, $(\mathbb N, <)$ is a model of $\{\exists x\,\lnot\exists y\,(y \in x)\}$ but not of $\{\forall x\,\exists y\,(y \in x)\}$. The checker at the end of the next section lets you build small structures and test which sentences they are models of.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: appa-sec-theories-and-logical-consequence -->
    ## Theories and Logical Consequence

    /// note | 📖 **Definition**
    <u>**Theory**</u>

    A collection of {term}`sentences <sentence>`, called the axioms of the theory.
    ///

    ZFC is a theory with infinitely many axioms, because Separation and Replacement are *schemas*: one axiom for each formula. (Some texts reserve "theory" for a collection of sentences closed under logical consequence; we do not.)

    Being an {term}`axiom` and being true are different kinds of property. A sentence is an axiom *of a theory*: a matter of which sentences were chosen. A sentence is true or false *in a structure*: a matter of what the symbols are interpreted to mean. The two meet in the notion of {term}`model`: $\mathfrak A$ is a model of a theory $T$ iff every axiom of $T$ is true in $\mathfrak A$. The axioms of ZFC are intended to be true in the intended structure of all sets, but nothing in the definitions forces that: $(\mathbb N, <)$ is a perfectly good structure in which some ZFC axioms are true and others false.

    /// note | 📖 **Definition**
    <u>**Logical consequence**</u>

    A formula $\varphi$ is a logical consequence of a collection $\Gamma$ of formulas, written $\Gamma \models \varphi$, iff for every structure $\mathfrak A$ and every assignment $s$ such that $\mathfrak A$ satisfies every member of $\Gamma$ with $s$, also $\mathfrak A \models \varphi[s]$.
    ///

    When $\Gamma$ is a theory and $\varphi$ a sentence, this says: $\varphi$ is true in every model of $\Gamma$. A formula with $\varnothing \models \varphi$ (written $\models \varphi$) is *logically valid*: true in every structure under every assignment. Logically valid formulas generalize the {term}`tautologies <tautology>` of Chapter 1. The symbol $\models$ is used in two ways, $\mathfrak A \models \varphi[s]$ (satisfaction) and $\Gamma \models \varphi$ (consequence); the left side always shows which is meant.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To show $\Gamma \models \varphi$, reason about an arbitrary model. To show $\Gamma \not\models \varphi$, exhibit one *counter-model*: a model of $\Gamma$ in which $\varphi$ is false. This is the semantic version of a {term}`counterexample`.

    /// admonition | 📐 **Theorem (Asymmetry Implies Irreflexivity)**
        attrs: {class: theorem, id: appa-thm-asymmetry-implies-irreflexivity}
    $\{\forall x\,\forall y\,(x \in y \rightarrow y \notin x)\} \models \forall z\,(z \notin z)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Let $\mathfrak A = (A, E)$ be a model of the hypothesis and let $c \in A$ be arbitrary. Taking $x$ and $y$ both to be $c$, the hypothesis gives: if $c \mathrel{E} c$ then not $c \mathrel{E} c$. If $c \mathrel{E} c$ held, we would get both $c \mathrel{E} c$ and not $c \mathrel{E} c$; so not $c \mathrel{E} c$. Since $c$ was arbitrary, $\forall z\,(z \notin z)$ is true in $\mathfrak A$. $\blacksquare$
    ///

    /// admonition | 📐 **Theorem (Extensionality Does Not Imply Empty Set)**
        attrs: {class: theorem, id: appa-thm-extensionality-does-not-imply-empty-set}
    Let $\text{Ext}$ be $\forall x\,\forall y\,(\forall z\,(z \in x \leftrightarrow z \in y) \rightarrow x = y)$ and $\text{Emp}$ be $\exists x\,\forall y\,(y \notin x)$. Then $\{\text{Ext}\} \not\models \text{Emp}$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Let $\mathfrak A$ have a single object $a$, with $a \mathrel{E} a$. $\text{Ext}$ is true in $\mathfrak A$: any two choices of $x$ and $y$ are both $a$, so the conclusion $x = y$ is true. $\text{Emp}$ is false in $\mathfrak A$: the only candidate for $x$ is $a$, and $y = a$ satisfies $y \mathrel{E} x$. So $\mathfrak A$ is a counter-model. $\blacksquare$
    ///

    This is how logicians show that an axiom does not follow from the others: they build a model of the others in which it fails. The same method shows that the Axiom of Choice does not follow from the other ZFC axioms, though the models needed are far from finite.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: appa-sec-try-it-a-structure-checker -->
    ### Try It: A Structure Checker

    Build a structure with up to four objects $a, b, c, d$ by choosing which objects are "members" of which (a check at "$a$ E $b$" means $a \mathrel{E} b$). The checker evaluates each sentence below with the satisfaction clauses, by brute force over all assignments, and reports whether the structure is a model of it. For a false sentence that begins with $\forall$, it shows a counterexample for the leading universal variables; for a true sentence that begins with $\exists$, it shows a witness. Start from a preset, then edit the checkboxes. The preset "One self-member" with 1 object is the counter-model from the [Extensionality Does Not Imply Empty Set theorem](#appa-thm-extensionality-does-not-imply-empty-set). Can you find a counter-model with more objects? You will not find a structure satisfying both Pairing and Regularity: no finite one exists[^finite-pairing], a first hint that models of set theory must be infinite.

    [^finite-pairing]: Suppose a structure has $n$ objects and satisfies Pairing. For each of the $n(n+1)/2$ ways to choose two objects or one object, Pairing requires an object whose members are exactly those chosen, and objects with different members are different objects. So $n \ge n(n+1)/2$, which forces $n = 1$. With a single object $a$, Pairing (with $x = y = a$) requires $a \mathrel{E} a$, and then Regularity fails for $x = a$, because the only member of $a$ is $a$ itself, which shares the member $a$ with $a$.
    """)
    return


@app.cell
def checker_engine():
    # jb: include=false
    from itertools import product as _product

    CK_NAMES = ("a", "b", "c", "d")

    CK_PRESETS = {
        "Von Neumann numerals (a = 0, b = 1, c = 2, d = 3)": {(i, j) for i in range(4) for j in range(4) if i < j},
        "Nothing is a member of anything": set(),
        "One self-member (a E a)": {(0, 0)},
        "A membership cycle (a E b, b E a)": {(0, 1), (1, 0)},
    }

    def _in(x, y): return ("in", x, y)
    def _eq(x, y): return ("eq", x, y)
    def _not(p): return ("not", p)
    def _and(p, q): return ("and", p, q)
    def _or(p, q): return ("or", p, q)
    def _imp(p, q): return ("imp", p, q)
    def _iff(p, q): return ("iff", p, q)
    def _ex(x, p): return ("exists", x, p)
    def _all(x, p): return ("forall", x, p)

    CK_SENTENCES = [
        ("Extensionality (Ext)",
         r"\forall x\,\forall y\,(\forall z\,(z \in x \leftrightarrow z \in y) \rightarrow x = y)",
         _all("x", _all("y", _imp(_all("z", _iff(_in("z", "x"), _in("z", "y"))), _eq("x", "y"))))),
        ("Empty Set (Emp)",
         r"\exists x\,\forall y\,(y \notin x)",
         _ex("x", _all("y", _not(_in("y", "x"))))),
        ("Pairing",
         r"\forall x\,\forall y\,\exists z\,\forall w\,(w \in z \leftrightarrow w = x \lor w = y)",
         _all("x", _all("y", _ex("z", _all("w", _iff(_in("w", "z"), _or(_eq("w", "x"), _eq("w", "y")))))))),
        ("Union",
         r"\forall x\,\exists u\,\forall y\,(y \in u \leftrightarrow \exists z\,(z \in x \land y \in z))",
         _all("x", _ex("u", _all("y", _iff(_in("y", "u"), _ex("z", _and(_in("z", "x"), _in("y", "z")))))))),
        ("Power Set",
         r"\forall x\,\exists p\,\forall z\,(z \in p \leftrightarrow \forall w\,(w \in z \rightarrow w \in x))",
         _all("x", _ex("p", _all("z", _iff(_in("z", "p"), _all("w", _imp(_in("w", "z"), _in("w", "x")))))))),
        ("Regularity",
         r"\forall x\,(\exists y\,(y \in x) \rightarrow \exists y\,(y \in x \land \lnot\exists z\,(z \in y \land z \in x)))",
         _all("x", _imp(_ex("y", _in("y", "x")),
                        _ex("y", _and(_in("y", "x"), _not(_ex("z", _and(_in("z", "y"), _in("z", "x"))))))))),
        ("Asymmetry",
         r"\forall x\,\forall y\,(x \in y \rightarrow y \notin x)",
         _all("x", _all("y", _imp(_in("x", "y"), _not(_in("y", "x")))))),
        ("Irreflexivity",
         r"\forall z\,(z \notin z)",
         _all("z", _not(_in("z", "z")))),
    ]

    def ck_holds(node, member, n, s):
        """Satisfaction clauses: member is a set of index pairs (i, j) meaning i E j,
        n is the number of objects, s maps variable names to indices."""
        kind = node[0]
        if kind == "in":
            return (s[node[1]], s[node[2]]) in member
        if kind == "eq":
            return s[node[1]] == s[node[2]]
        if kind == "not":
            return not ck_holds(node[1], member, n, s)
        if kind in ("exists", "forall"):
            results = (ck_holds(node[2], member, n, {**s, node[1]: a}) for a in range(n))
            return any(results) if kind == "exists" else all(results)
        p, q = ck_holds(node[1], member, n, s), ck_holds(node[2], member, n, s)
        return {"and": p and q, "or": p or q, "imp": (not p) or q, "iff": p == q}[kind]

    def _leading_block(node):
        kind, variables = node[0], []
        while node[0] == kind and kind in ("exists", "forall"):
            variables.append(node[1])
            node = node[2]
        return kind, variables, node

    def ck_report(member, n):
        objs = CK_NAMES[:n]
        lines = ["| Sentence | Formula | In this structure | Why |", "| :--- | :--- | :-: | :--- |"]
        model_of = []
        for name, tex, sentence in CK_SENTENCES:
            truth = ck_holds(sentence, member, n, {})
            kind, variables, body = _leading_block(sentence)
            why = ""
            if (kind == "forall" and not truth) or (kind == "exists" and truth):
                want = kind == "exists"
                for values in _product(range(n), repeat=len(variables)):
                    if ck_holds(body, member, n, dict(zip(variables, values))) == want:
                        pairs = ", ".join(f"{v} = {objs[i]}" for v, i in zip(variables, values))
                        why = ("witness: " if want else "counterexample: ") + pairs
                        break
            elif kind == "forall":
                why = "no counterexample"
            elif kind == "exists":
                why = "no witness"
            if truth:
                model_of.append(name.split(" (")[0])
            lines.append(f"| {name} | ${tex}$ | {'true' if truth else 'false'} | {why} |")
        members = "; ".join(
            f"{objs[j]}: " + (", ".join(objs[i] for i in range(n) if (i, j) in member) or "none")
            for j in range(n)
        )
        summary = (
            f"Members of each object: {members}.\n\n"
            + ("This structure is a model of: " + ", ".join(model_of) + "." if model_of
               else "This structure is a model of none of these sentences.")
        )
        return summary + "\n\n" + "\n".join(lines)

    return CK_NAMES, CK_PRESETS, ck_report


@app.cell(hide_code=True)
def _(CK_PRESETS, mo):
    ck_preset = mo.ui.dropdown(
        options=list(CK_PRESETS),
        value="Von Neumann numerals (a = 0, b = 1, c = 2, d = 3)",
        label="Start from",
    )
    ck_size = mo.ui.slider(1, 4, value=4, step=1, label="Number of objects", show_value=True)
    return ck_preset, ck_size


@app.cell(hide_code=True)
def _(CK_NAMES, CK_PRESETS, ck_preset, ck_size, mo):
    ck_relation = mo.ui.array([
        mo.ui.checkbox(
            value=(i, j) in CK_PRESETS[ck_preset.value],
            label=f"{CK_NAMES[i]} E {CK_NAMES[j]}",
        )
        for i in range(ck_size.value)
        for j in range(ck_size.value)
    ])
    return (ck_relation,)


@app.cell(hide_code=True)
def _(ck_preset, ck_relation, ck_report, ck_size, mo):
    _n = ck_size.value
    _member = {(k // _n, k % _n) for k, checked in enumerate(ck_relation.value) if checked}
    _grid = mo.vstack([
        mo.hstack([ck_relation[i * _n + j] for j in range(_n)], justify="start", gap=1.5)
        for i in range(_n)
    ])
    mo.vstack([mo.hstack([ck_preset, ck_size], justify="start"), _grid, mo.md(ck_report(_member, _n))])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: appa-sec-formal-proofs -->
    ## Formal Proofs

    Logical consequence quantifies over *all* structures, of every size, so it cannot be checked directly. A deductive system replaces it with a finite, mechanical check: a list of logical axioms and rules of inference, with a proof being a sequence of formulas each of which is an axiom or follows from earlier ones by a rule. We use the system of @enderton2001 [§2.4], adapted to our primitive symbols.

    <!-- label: appa-sec-logical-axioms-and-modus-ponens -->
    ### Logical Axioms and Modus Ponens

    Call a formula *prime* if it is atomic or begins with $\exists$. Every formula is built from prime formulas by $\lnot$ and $\land$. A formula is a *tautology instance* if it is true under every assignment of truth values to its prime parts, computing $\lnot$ and $\land$ by their truth tables. For example, $(x \in y \land \exists z\,(z \in x)) \rightarrow x \in y$ is a tautology instance, because $(P \land Q) \rightarrow P$ is a {term}`tautology`.

    The **logical axioms** are all *generalizations* $\forall x_1 \cdots \forall x_n\,\theta$ ($n \ge 0$) of formulas $\theta$ of the following six forms, where $\varphi$, $\psi$ are any formulas and $x$, $y$ any variables:

    1. Tautology instances.
    2. $\forall x\,\varphi \rightarrow \varphi[x/y]$, where $y$ is substitutable for $x$ in $\varphi$ (in particular, $y$ may be $x$).
    3. $\forall x\,(\varphi \rightarrow \psi) \rightarrow (\forall x\,\varphi \rightarrow \forall x\,\psi)$.
    4. $\varphi \rightarrow \forall x\,\varphi$, where $x$ is not a free variable of $\varphi$.
    5. $x = x$.
    6. $x = y \rightarrow (\alpha \rightarrow \alpha')$, where $\alpha$ is atomic and $\alpha'$ is obtained from $\alpha$ by replacing $x$ by $y$ at zero or more places.

    The only **rule of inference** is *modus ponens*: from $\varphi$ and $\varphi \rightarrow \psi$, infer $\psi$.

    /// note | 📖 **Definition**
    <u>**Formal proof**</u>

    A formal proof (or *deduction*) of a formula $\varphi$ from a collection $\Gamma$ of formulas is a finite sequence of formulas $\varphi_1, \ldots, \varphi_n$ with $\varphi_n = \varphi$, in which each $\varphi_i$ is a logical axiom, a member of $\Gamma$, or follows by modus ponens from earlier formulas $\varphi_j$ and $\varphi_k = (\varphi_j \rightarrow \varphi_i)$, with $j, k < i$.
    ///

    We write $\Gamma \vdash \varphi$, read "$\varphi$ is provable from $\Gamma$", if such a sequence exists, and $\vdash \varphi$ when $\Gamma$ is empty. Whether a given sequence is a formal proof can be checked mechanically, symbol by symbol. Note that there is no separate "generalization" rule: generalization is built into the axioms (every generalization of an axiom is an axiom) and recovered as the Generalization Lemma below.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: appa-sec-two-worked-derivations -->
    ### Two Worked Derivations

    **A three-line proof.** $\vdash \forall x\,(x \in y \land x \neq y) \rightarrow \forall x\,(x \in y)$:

    | # | Formula | Justification |
    |:-:|:---|:---|
    | 1 | $\forall x\,\big((x \in y \land x \neq y) \rightarrow x \in y\big)$ | axiom group 1, generalized: $(P \land Q) \rightarrow P$ is a tautology |
    | 2 | $\forall x\,\big((x \in y \land x \neq y) \rightarrow x \in y\big) \rightarrow \big(\forall x\,(x \in y \land x \neq y) \rightarrow \forall x\,(x \in y)\big)$ | axiom group 3 |
    | 3 | $\forall x\,(x \in y \land x \neq y) \rightarrow \forall x\,(x \in y)$ | modus ponens, 1 and 2 |

    **The formal version of Asymmetry Implies Irreflexivity.** Let $\Gamma = \{\forall x\,\forall y\,(x \in y \rightarrow y \notin x)\}$. Then $\Gamma \vdash z \notin z$:

    | # | Formula | Justification |
    |:-:|:---|:---|
    | 1 | $\forall x\,\forall y\,(x \in y \rightarrow y \notin x)$ | member of $\Gamma$ |
    | 2 | $\forall x\,\forall y\,(x \in y \rightarrow y \notin x) \rightarrow \forall y\,(z \in y \rightarrow y \notin z)$ | axiom group 2 ($z$ is substitutable for $x$, since no quantifier on $z$ occurs) |
    | 3 | $\forall y\,(z \in y \rightarrow y \notin z)$ | modus ponens, 1 and 2 |
    | 4 | $\forall y\,(z \in y \rightarrow y \notin z) \rightarrow (z \in z \rightarrow z \notin z)$ | axiom group 2 ($z$ is substitutable for $y$, since no quantifier occurs) |
    | 5 | $z \in z \rightarrow z \notin z$ | modus ponens, 3 and 4 |
    | 6 | $(z \in z \rightarrow z \notin z) \rightarrow z \notin z$ | axiom group 1: $(P \rightarrow \lnot P) \rightarrow \lnot P$ is a tautology |
    | 7 | $z \notin z$ | modus ponens, 5 and 6 |

    Step 4 substitutes $z$ for $y$ in a formula that already contains $z$; this is allowed because substitutability only forbids capture by a quantifier, which is why Formal Syntax defined substitutability rather than requiring a fresh variable. Since $z$ is not free in the member of $\Gamma$, the Generalization Lemma below upgrades this to $\Gamma \vdash \forall z\,(z \notin z)$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: appa-sec-derived-rules -->
    ### Derived Rules

    The informal rules of inference in [Chapter 1](#ch1-sec-rules-of-inference) are shortcuts for patterns of formal steps. The two most important are proved here.

    /// admonition | 📐 **Lemma (Deduction)**
        attrs: {class: lemma, id: appa-lem-deduction}
    $\Gamma \cup \{\gamma\} \vdash \varphi$ iff $\Gamma \vdash \gamma \rightarrow \varphi$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    $(\Leftarrow)$ Append $\gamma$ and $\varphi$ to a deduction of $\gamma \rightarrow \varphi$ from $\Gamma$; the last step is modus ponens.

    $(\Rightarrow)$ Let $\varphi_1, \ldots, \varphi_n$ be a deduction from $\Gamma \cup \{\gamma\}$. We show $\Gamma \vdash \gamma \rightarrow \varphi_i$ for each $i$, by induction on $i$.

    - If $\varphi_i$ is a logical axiom or in $\Gamma$, then $\Gamma \vdash \varphi_i$, and $\varphi_i \rightarrow (\gamma \rightarrow \varphi_i)$ is a tautology instance (of $Q \rightarrow (P \rightarrow Q)$), so modus ponens gives $\Gamma \vdash \gamma \rightarrow \varphi_i$.
    - If $\varphi_i = \gamma$, then $\gamma \rightarrow \gamma$ is a tautology instance.
    - If $\varphi_i$ follows by modus ponens from $\varphi_j$ and $\varphi_j \rightarrow \varphi_i$ with $j < i$, the induction hypothesis gives $\Gamma \vdash \gamma \rightarrow \varphi_j$ and $\Gamma \vdash \gamma \rightarrow (\varphi_j \rightarrow \varphi_i)$. The formula $(\gamma \rightarrow \varphi_j) \rightarrow \big((\gamma \rightarrow (\varphi_j \rightarrow \varphi_i)) \rightarrow (\gamma \rightarrow \varphi_i)\big)$ is a tautology instance, so two applications of modus ponens give $\Gamma \vdash \gamma \rightarrow \varphi_i$. $\blacksquare$
    ///

    /// admonition | 📐 **Lemma (Generalization)**
        attrs: {class: lemma, id: appa-lem-generalization}
    If $\Gamma \vdash \varphi$ and $x$ is not a free variable of any formula in $\Gamma$, then $\Gamma \vdash \forall x\,\varphi$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Let $\varphi_1, \ldots, \varphi_n$ be a deduction of $\varphi$ from $\Gamma$. We show $\Gamma \vdash \forall x\,\varphi_i$ for each $i$, by induction on $i$.

    - If $\varphi_i$ is a logical axiom, so is its generalization $\forall x\,\varphi_i$.
    - If $\varphi_i \in \Gamma$, then $x$ is not free in $\varphi_i$, so $\varphi_i \rightarrow \forall x\,\varphi_i$ is in axiom group 4, and modus ponens gives $\forall x\,\varphi_i$.
    - If $\varphi_i$ follows by modus ponens from $\varphi_j$ and $\varphi_j \rightarrow \varphi_i$, the induction hypothesis gives $\Gamma \vdash \forall x\,\varphi_j$ and $\Gamma \vdash \forall x\,(\varphi_j \rightarrow \varphi_i)$. Axiom group 3 gives $\forall x\,(\varphi_j \rightarrow \varphi_i) \rightarrow (\forall x\,\varphi_j \rightarrow \forall x\,\varphi_i)$, and two applications of modus ponens give $\Gamma \vdash \forall x\,\varphi_i$. $\blacksquare$
    ///

    The Deduction Lemma is Chapter 1's *conditional proof* ("assume $\gamma$ ... therefore $\gamma \rightarrow \varphi$"), and the Generalization Lemma is *universal generalization* ("let $x$ be arbitrary"): the requirement that $x$ not be free in $\Gamma$ is the formal meaning of "nothing is assumed about $x$". Axiom group 2 is universal instantiation, and modus ponens is itself. Existential generalization and existential instantiation are also derived rules; see @enderton2001 [§2.4].
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: appa-sec-soundness-and-completeness -->
    ### Soundness and Completeness

    /// admonition | 📐 **Theorem (Soundness and Completeness)**
        attrs: {class: theorem, id: appa-thm-soundness-and-completeness}
    For every collection $\Gamma$ of formulas and every formula $\varphi$:

    $$\Gamma \vdash \varphi \quad\text{iff}\quad \Gamma \models \varphi.$$

    The direction $(\Rightarrow)$ is the *Soundness Theorem*; the direction $(\Leftarrow)$ is Gödel's *Completeness Theorem* (1929).
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Not given here. Soundness is proved by induction along a deduction: every logical axiom is logically valid, and modus ponens preserves satisfaction. Completeness is proved by Henkin's method, which builds a model out of the formulas themselves for any collection from which no contradiction is provable. Both proofs are in @enderton2001 [§2.5]; see also [Gödel's completeness theorem (Wikipedia)](https://en.wikipedia.org/wiki/G%C3%B6del%27s_completeness_theorem). $\blacksquare$
    ///

    So the mechanical notion $\vdash$ and the semantic notion $\models$ coincide. A collection $\Gamma$ of formulas is *consistent* if there is no formula $\varphi$ with both $\Gamma \vdash \varphi$ and $\Gamma \vdash \lnot\varphi$.

    /// admonition | 📐 **Corollary (Consistency and Models)**
        attrs: {class: corollary, id: appa-cor-consistency-and-models}
    A theory is consistent iff it has a model.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    $(\Leftarrow)$ If $\mathfrak A$ is a model of $T$ and $T \vdash \varphi$ and $T \vdash \lnot\varphi$ for some formula $\varphi$, then by soundness $\mathfrak A \models \varphi[s]$ and $\mathfrak A \models \lnot\varphi[s]$ for any assignment $s$, which clause 3 of satisfaction forbids. $(\Rightarrow)$ If $T$ has no model, then no structure and assignment satisfy every member of $T$, so $T \models \varphi$ and $T \models \lnot\varphi$ hold vacuously for any $\varphi$; by completeness both are provable, so $T$ is inconsistent. $\blacksquare$
    ///

    This is what justifies the main path's informal proofs. Each of them could be expanded into a formal deduction from the ZFC axioms, and by soundness, whatever is formally provable from ZFC is true in every model of ZFC.

    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **First-order logic only.** Quantifiers here range over objects of the domain. In *second-order* logic, which also quantifies over all subsets of the domain, no deductive system is both sound and complete for the standard semantics; see [Second-order logic (Wikipedia)](https://en.wikipedia.org/wiki/Second-order_logic).
    - **Checking is not finding.** A formal proof can be checked mechanically, but there is no algorithm that decides, for every formula, whether it is logically valid (Church and Turing, 1936; see [Entscheidungsproblem (Wikipedia)](https://en.wikipedia.org/wiki/Entscheidungsproblem)).
    - **All models, not one.** Completeness concerns truth in *every* model of $\Gamma$. A sentence that is true in the intended structure but false in some other model of $\Gamma$ is not provable from $\Gamma$. The Metatheory below returns to this.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: appa-sec-extension-by-definitions -->
    ## Extension by Definitions

    The only symbols of the language of set theory are $\in$ and $=$, yet [Chapter 2](#ch2) writes $\emptyset \in I$, $\{a, b\}$, and $A \subseteq B$. This section shows that such notation is legitimate shorthand: every statement using it can be rewritten in the original language, and it makes no new statements of the original language provable. Throughout, $T$ is a theory, such as ZFC.

    <!-- label: appa-sec-defined-relations -->
    ### Defined Relations

    A definition $P(x_1, \ldots, x_n) :\Longleftrightarrow \varphi(x_1, \ldots, x_n)$, where $\varphi$ is a formula, introduces a new relation symbol $P$. Each occurrence of $P(y_1, \ldots, y_n)$ abbreviates the formula obtained from $\varphi$ by substituting $y_i$ for $x_i$, after renaming the bound variables of $\varphi$ if necessary so that each $y_i$ is substitutable. The abbreviations $\subseteq$ and $\notin$ in Formal Syntax are of this kind. Defined relations need no proof before use.

    <!-- label: appa-sec-operations -->
    ### Operations

    Names for objects do need a proof first: a name must name exactly one object.

    /// note | 📖 **Definition**
    <u>**Operation**</u>

    An operation of a theory $T$ is a new symbol $F$ together with a formula $\delta(x_1, \ldots, x_n, y)$, its *defining formula*, such that $T \vdash \forall x_1 \cdots \forall x_n\, \exists! y\, \delta(x_1, \ldots, x_n, y)$. The expression $F(x_1, \ldots, x_n)$ stands for "the unique $y$ such that $\delta(x_1, \ldots, x_n, y)$". An operation with $n = 0$ is a *constant*: a name for one particular object.
    ///

    In ZFC, each axiom that asserts the existence of a set with prescribed elements yields an operation, with Extensionality supplying uniqueness (Chapter 2's Uniqueness Lemma):

    | Axiom | Operation | Defining formula |
    |:---|:---|:---|
    | Empty Set | $\emptyset$ (a constant) | $\forall w\,(w \notin y)$ |
    | Pairing | $\{x_1, x_2\}$ | $\forall w\,(w \in y \leftrightarrow w = x_1 \lor w = x_2)$ |
    | Union | $\bigcup x_1$ | $\forall w\,(w \in y \leftrightarrow \exists z\,(z \in x_1 \land w \in z))$ |
    | Power Set | $\mathcal P(x_1)$ | $\forall w\,(w \in y \leftrightarrow w \subseteq x_1)$ |
    | Separation | $\{w \in x_1 : \varphi\}$ | $\forall w\,(w \in y \leftrightarrow w \in x_1 \land \varphi)$, one operation for each formula $\varphi$, with $\varphi$'s other free variables as further arguments |

    Replacement also yields an operation, but one with a proviso (below). Infinity and Choice assert that a set exists without determining it uniquely, so they yield no operation directly. Operations may also be defined from earlier ones, such as $A \cup B := \bigcup\{A, B\}$.

    <!-- label: appa-sec-terms -->
    ### Terms

    /// note | 📖 **Definition**
    <u>**Term**</u>

    An expression obtained by finitely many applications of these rules: every variable is a term; and if $F$ is an {term}`operation` with $n$ arguments and $t_1, \ldots, t_n$ are terms, then $F(t_1, \ldots, t_n)$ is a term (for $n = 0$, the constant $F$ itself is a term).
    ///

    For example, $\{\emptyset, \{\emptyset\}\}$ is a term built from the constant $\emptyset$ and the pairing operation (with $\{t\} := \{t, t\}$). In any model of $T$, under any assignment, every term names exactly one object: a variable names its assigned value, and $F(t_1, \ldots, t_n)$ names the unique $y$ satisfying $\delta$ at the objects named by $t_1, \ldots, t_n$ (by induction on terms). This is what justifies introducing names with $:=$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: appa-sec-unpacking -->
    ### Unpacking

    In the extended language, the atomic formulas are $t_1 \in t_2$ and $t_1 = t_2$ for terms $t_1, t_2$. Such a formula is shorthand for a formula of the original language, obtained by *unpacking*. If an atomic formula $\alpha$ contains an occurrence of $F(v_1, \ldots, v_n)$ whose arguments $v_1, \ldots, v_n$ are variables, then $\alpha$ abbreviates

    $$\exists z\,\big(\delta_F(v_1, \ldots, v_n, z) \land \alpha'\big),$$

    where $\delta_F$ is the defining formula of $F$ (with its bound variables renamed if necessary to avoid clashes), $z$ is a variable not occurring in $\alpha$, and $\alpha'$ is $\alpha$ with that occurrence of $F(v_1, \ldots, v_n)$ replaced by $z$. Each step removes one operation symbol, so repeating it, innermost operations first, removes them all. For example, $\emptyset \in I$ unpacks to $\exists z\,\big(\forall w\,(w \notin z) \land z \in I\big)$. When $\alpha$ is $y = F(v_1, \ldots, v_n)$ for a variable $y$, the result is equivalent to the simpler $\delta_F(v_1, \ldots, v_n, y)$, which we use instead.

    /// admonition | 📐 **Lemma (The Two Unpackings Agree)**
        attrs: {class: lemma, id: appa-lem-the-two-unpackings-agree}
    If $T \vdash \forall v_1 \cdots \forall v_n\, \exists! z\, \delta(v_1, \ldots, v_n, z)$, then $T \vdash \exists z\,(\delta \land \alpha') \leftrightarrow \forall z\,(\delta \rightarrow \alpha')$ for every formula $\alpha'$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Let $\mathfrak A$ be a model of $T$ and $s$ an assignment. By hypothesis exactly one object $b$ satisfies $\delta$ when $z$ is assigned $b$ (and the other variables as in $s$). The left side is true iff $\alpha'$ is true when $z$ is assigned $b$, since $b$ is the only candidate. The right side is true iff $\alpha'$ is true whenever $z$ is assigned an object satisfying $\delta$, that is, iff $\alpha'$ is true when $z$ is assigned $b$. So the biconditional is true in every model of $T$ under every assignment, and by the Completeness Theorem $T$ proves it. $\blacksquare$
    ///

    So it makes no difference whether "the $F$ of $v$ has property $\alpha'$" is unpacked as "some object satisfying $\delta$ has property $\alpha'$" or "every object satisfying $\delta$ has property $\alpha'$".

    <!-- label: appa-sec-provisos -->
    ### Provisos

    Some notation names an object only under a condition. The main example is function application: in [Chapter 2](#ch2-sec-functions), $f(a)$ names a set only when $f$ is a function and $a$ is in its domain. Another is Replacement notation $\{y : \existsin{x}{A}\, \varphi\}$, which names a set only when $\forallin{x}{A}\, \exists! y\, \varphi$. For such notation we are given a *proviso* $D(x_1, \ldots, x_n)$ and a proof of only

    $$T \vdash \forall x_1 \cdots \forall x_n\, \big(D \rightarrow \exists! y\, \delta\big).$$

    This is turned into an operation by choosing a default value where the proviso fails. Take as defining formula

    $$\delta'(x_1, \ldots, x_n, y) := (D \land \delta) \lor (\lnot D \land y = \emptyset).$$

    Then $T \vdash \forall x_1 \cdots \forall x_n\, \exists! y\, \delta'$: where $D$ holds, $\delta'$ is equivalent to $\delta$; where it fails, $\delta'$ is equivalent to $y = \emptyset$. So $F$ is an operation, and everything in this section applies to it. The default value is never used, because we follow the convention of writing $F(x_1, \ldots, x_n)$ only where $D(x_1, \ldots, x_n)$ is known to hold. Accordingly, for terms containing such notation, the guarantee that a term names the intended object holds only at values where all of its provisos hold.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: appa-sec-conservative-extensions -->
    ### Conservative Extensions

    /// note | 📖 **Definition**
    <u>**Conservative extension**</u>

    Let $T$ be a theory, and let $T'$ be a theory whose language contains every symbol of $T$'s language (and possibly more). $T'$ is a conservative extension of $T$ iff for every formula $\varphi$ of $T$'s language, $T' \vdash \varphi$ iff $T \vdash \varphi$.
    ///

    Let $T'$ be $T$ together with a *defining axiom* for each new symbol: $\forall x_1 \cdots \forall x_n\,\big(P(x_1, \ldots, x_n) \leftrightarrow \varphi\big)$ for each defined relation $P$, and $\forall x_1 \cdots \forall x_n\, \forall y\,\big(y = F(x_1, \ldots, x_n) \leftrightarrow \delta\big)$ for each operation $F$. A structure for the extended language also interprets each new relation symbol by a relation on the domain and each operation symbol $F$ by a rule $F^{\mathfrak A}$ assigning an object to each $n$-tuple of objects. Terms are then evaluated recursively, and the satisfaction clauses are otherwise unchanged.

    /// admonition | 📐 **Theorem (Extension by Definitions)**
        attrs: {class: theorem, id: appa-thm-extension-by-definitions}
    1. $T'$ is a conservative extension of $T$.
    2. For every formula $\varphi'$ of the extended language, its unpacking $\varphi$ is a formula of $T$'s language with $T' \vdash \varphi' \leftrightarrow \varphi$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    1. If $T \vdash \varphi$, then $T' \vdash \varphi$, because every axiom of $T$ is an axiom of $T'$. Conversely, suppose $T' \vdash \varphi$, with $\varphi$ in $T$'s language. Let $\mathfrak A$ be any model of $T$. Expand it to a structure $\mathfrak A'$ for the extended language, interpreting the new symbols in the order they were defined: each $P$ by the tuples satisfying its defining formula, and each $F$ by $F^{\mathfrak A}(a_1, \ldots, a_n) :=$ the unique $b$ such that $\delta$ is satisfied when $x_1, \ldots, x_n, y$ are assigned $a_1, \ldots, a_n, b$. That $b$ exists and is unique because $\forall x_1 \cdots \forall x_n\, \exists! y\, \delta$ is provable in $T$, hence (by soundness) true in $\mathfrak A$. Then $\mathfrak A'$ is a model of $T'$, so by soundness $\varphi$ is true in $\mathfrak A'$ under every assignment. Since $\varphi$ mentions no new symbol, the satisfaction clauses evaluate it in $\mathfrak A'$ exactly as in $\mathfrak A$, so $\varphi$ is true in $\mathfrak A$ under every assignment. As $\mathfrak A$ was an arbitrary model of $T$, $T \models \varphi$, and by completeness $T \vdash \varphi$.
    2. In any model of $T'$, a defined relation $P(y_1, \ldots, y_n)$ is true exactly when its defining formula is (by its defining axiom). An atomic formula $\alpha$ containing $F(v_1, \ldots, v_n)$ is true exactly when $\alpha'$ is true with $z$ assigned the value of $F(v_1, \ldots, v_n)$, which, by the defining axiom of $F$, is exactly when $\exists z\,(\delta_F \land \alpha')$ is true. So each unpacking step replaces an atomic formula by one with the same truth value in every model of $T'$ under every assignment. Replacing a part of a formula by such an equivalent part preserves truth values (by induction on formulas, using the satisfaction clauses). Hence $\varphi'$ and $\varphi$ have the same truth value in every model of $T'$ under every assignment, and by completeness $T' \vdash \varphi' \leftrightarrow \varphi$. $\blacksquare$
    ///

    Part 2 says every statement written with defined notation means a statement in $\in$ and $=$ alone; part 1 says the notation lets us prove nothing new about $\in$ and $=$. Together they justify [Chapter 1](#ch1-sec-definitions-and-longleftrightarrow)'s remark that definitions add convenience but no new assumptions. See also [Extension by definitions (Wikipedia)](https://en.wikipedia.org/wiki/Extension_by_definitions) and [Conservative extension (Wikipedia)](https://en.wikipedia.org/wiki/Conservative_extension).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: appa-sec-the-metatheory -->
    ## The Metatheory

    Every lemma and theorem in this appendix (Unique Readability, Coincidence, Deduction, Soundness and Completeness) is a statement *about* formulas, structures, and deductions, proved in the metalanguage. The informal mathematics we reason in there is the *metatheory*. This section says what it assumes, and what the formal system cannot do.

    <!-- label: appa-sec-the-metatheory-is-informal -->
    ### The Metatheory Is Informal

    The metatheory is ordinary informal mathematics: naive reasoning about collections, together with induction on the length of finite strings and finite sequences. Syntax needs very little of it: formulas and deductions are finite strings of symbols, and facts about them need only finite combinatorics. Semantics needs more, because structures may have infinite domains.

    This can look circular: set theory is used to explain the language of set theory. The circle is not vicious. Nothing here claims to found the metatheory; it is the background mathematics that author and reader already share, and the formal system is a precise *model* of how that mathematics reasons. Alternatively, the metatheory can itself be carried out inside ZFC, with formulas coded as sets; the theorems of this appendix then become theorems of ZFC about those codes.

    <!-- label: appa-sec-the-intended-structure-is-not-a-set -->
    ### The Intended Structure Is Not a Set

    [Chapter 2](#ch2-thm-no-set-of-all-sets) proves, from Separation, that there is no set of all sets (the theorem No Set of All Sets, which is Russell's paradox). So the domain of the intended structure, the collection of all sets, is not a set. Collections like it, defined by a formula (here $x = x$) but too large to be sets, are called *proper classes*. Our definition of {term}`structure` says "collection" precisely so that it covers the intended structure informally.

    The cost is that "true in the intended structure" cannot be defined inside ZFC: no single formula $\text{True}(x)$ of the language of set theory satisfies $\text{True}(\ulcorner\sigma\urcorner) \leftrightarrow \sigma$ for the code $\ulcorner\sigma\urcorner$ of every sentence $\sigma$ (Tarski's undefinability theorem; see [Tarski's undefinability theorem (Wikipedia)](https://en.wikipedia.org/wiki/Tarski%27s_undefinability_theorem)). For this reason the main path never claims a result is "true" in an absolute sense: it claims that the result is *provable from ZFC*, and hence, by soundness, true in every model of ZFC.

    <!-- label: appa-sec-consistency-is-assumed -->
    ### Consistency Is Assumed

    If ZFC were inconsistent, it would prove every sentence: from $\varphi$ and $\lnot\varphi$, the tautology instance $\varphi \rightarrow (\lnot\varphi \rightarrow \psi)$ and modus ponens give any $\psi$. Its theorems would then be worthless. Can we prove that ZFC is consistent? Not in ZFC itself:

    /// admonition | 📐 **Theorem (Gödel's Incompleteness Theorems, 1931)**
        attrs: {class: theorem, id: appa-thm-godels-incompleteness-theorems-1931}
    Let $T$ be a consistent theory whose axioms can be listed by an algorithm and which proves the basic facts of arithmetic (as ZFC does). Then:

    1. There is a sentence $\sigma$ of $T$'s language such that neither $T \vdash \sigma$ nor $T \vdash \lnot\sigma$. (Gödel assumed slightly more than consistency; Rosser (1936) showed consistency suffices.)
    2. $T$ does not prove the sentence $\text{Con}(T)$ that expresses, via coding, "$T$ is consistent".
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Not given here; see [Gödel's incompleteness theorems (Wikipedia)](https://en.wikipedia.org/wiki/G%C3%B6del%27s_incompleteness_theorems) and the references there. $\blacksquare$
    ///

    So this book, like nearly all of mathematics, **assumes that ZFC is consistent**. By the Corollary to Soundness and Completeness, this is the same as assuming that ZFC has a model. The evidence is practical: a century of intensive use has produced no contradiction, and the consistency of ZFC can be proved in stronger theories (which merely shifts the assumption to them). The first incompleteness theorem has a concrete instance in set theory: the Continuum Hypothesis (that every infinite subset of $\mathbb R$ is {term}`equinumerous` with $\mathbb N$ or with $\mathbb R$) can be neither proved nor refuted from ZFC, if ZFC is consistent [@godel1940; @cohen1963]; see [Continuum hypothesis (Wikipedia)](https://en.wikipedia.org/wiki/Continuum_hypothesis). Nothing in this book depends on it.

    <!-- label: appa-sec-countable-models -->
    ### Countable Models

    By the Löwenheim–Skolem theorem, if ZFC has a model, it has one whose domain is {term}`countable` from the metatheory's point of view, even though ZFC proves that $\mathbb R$ is {term}`uncountable` ([Chapter 3](#ch3-thm-the-real-numbers-are-uncountable)). There is no contradiction: inside such a model, "uncountable" means that no bijection with $\mathbb N$ exists *among the objects of the model*, and the bijections the metatheory can see are not in the model. This is *Skolem's paradox*; see [Skolem's paradox (Wikipedia)](https://en.wikipedia.org/wiki/Skolem%27s_paradox). It is one more reason to read the main path's theorems as "provable from ZFC" rather than as facts about one fixed collection of sets.

    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **The book assumes ZFC is consistent.** This cannot be proved in ZFC (second incompleteness theorem). If it failed, every statement would be provable, including every theorem of this book and its negation.
    - **"Proved" means "provable from ZFC".** A sentence true in the intended structure but independent of ZFC (like the Continuum Hypothesis, if it is true there) is not a theorem.
    - **The metatheory is informal.** The theorems of this appendix are proved in ordinary mathematics; formalizing that mathematics leads back to a theory like ZFC, whose consistency is again assumed.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: appa-sec-summary -->
    ## Summary

    - **Syntax.** {term}`Formulas <formula>` are strings built from atomic formulas $u \in v$, $u = v$ by $\lnot$, $\land$, $\exists$; every formula is built in exactly one way. Occurrences of variables are {term}`free <free variable>` or {term}`bound <bound variable>`, and a {term}`sentence` has no free variables. Other connectives and quantifiers are abbreviations.
    - **Semantics.** A {term}`structure` interprets $\in$ on a nonempty domain; satisfaction $\mathfrak A \models \varphi[s]$ is defined clause by clause, and a sentence is simply true or false in a structure. A {term}`model` of a collection of sentences makes all of them true.
    - **Theories.** A {term}`theory` is a collection of sentences, its axioms. Being an axiom is relative to a theory; being true is relative to a structure. $\Gamma \models \varphi$ ({term}`logical consequence`) means $\varphi$ holds wherever $\Gamma$ does.
    - **Proofs.** A {term}`formal proof` uses the logical axioms and modus ponens. The Deduction and Generalization Lemmas recover Chapter 1's informal rules, and by Soundness and Completeness, $\Gamma \vdash \varphi$ iff $\Gamma \models \varphi$.
    - **Definitions.** Defined relations and {term}`operations <operation>` (built into {term}`terms <term>`) unpack into the original language, and adding them gives a {term}`conservative extension`.
    - **Metatheory.** The metatheory is informal; the collection of all sets is a proper class; ZFC's consistency is assumed, because ZFC cannot prove it.

    <!-- label: appa-sec-whats-next -->
    ## What's Next

    Return to the main path at [Chapter 2](#ch2-sec-the-axioms-of-zfc), where the axioms of ZFC are stated in the language of this appendix and the defined notation it justifies is put to work.
    """)
    return


if __name__ == "__main__":
    app.run()
