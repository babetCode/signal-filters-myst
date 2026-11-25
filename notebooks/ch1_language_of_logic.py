# /// script
# dependencies = [
#     "marimo>=0.25.1",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="1. Language of Logic", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "From Statements to Proofs"
    abbreviations:
      iff: if and only if
      diff: null
      ZFC: Zermelo–Fraenkel set theory with the Axiom of Choice
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
    from textwrap import dedent

    return dedent, mo


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
    /// seealso | 🔗 **Prerequisites**
        attrs: {class: no-icon}
    - [Introduction](introduction.md): the notation $z_k$, $\hat x_k$, $\hat x_k^-$ and the update $\hat x_k = \hat x_{k-1} + \alpha(z_k - \hat x_{k-1})$ (used only in examples).
    - [Appendix A: Formal Logic](appendix_a_formal_logic.md) (optional; the formal grammar, semantics, and deductive system behind this chapter).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A filter turns measurements $z_1, \ldots, z_k$ into estimates $\hat x_1, \ldots, \hat x_k$, and we want to know things about those estimates for certain: that an estimate never overshoots the measurement, that its error variance is as small as possible, that it settles down as data accumulates. "For certain" means *proved*. A proof is only as reliable as the statements it connects, so this chapter builds the language for writing statements with exactly one meaning, and the rules for proving them. Every later chapter is written in this language.

    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    A mathematical statement has exactly one meaning, and a proof is a chain of steps, each justified by a rule that never leads from true statements to a false one.
    ///

    We discuss mathematics in English, which plays the role of a *metalanguage*: the informal language we use to talk *about* mathematical statements. This chapter treats logic as a working tool: what the logical symbols mean, and how proofs are built. The fully formal version (a precise grammar of formulas, a precise definition of truth, and a mechanical notion of proof) is in [Appendix A](appendix_a_formal_logic.md). Nothing on the main path depends on it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Statements

    Consider four lines of text[^informal-numbers]:

    1. $2 + 2 = 4$.
    2. $155 < 150$.
    3. Is the scale turned on?
    4. $z > 150$.

    The first is true and the second is false. The third is a question, so it is neither. The fourth is neither true nor false *as written*: it becomes true or false only once we know which number $z$ is. We return to this kind of expression in Predicates and Variables below.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Statement**</u>

    A declarative sentence that is either true or false, but not both.
    ///

    Whether a statement is true or false is its *truth value*, written $\text{T}$ or $\text{F}$. We do not need to know the truth value for a sentence to be a statement: "the $10^{100}$-th decimal digit of $\pi$ is $7$" is a statement, though nobody knows which truth value it has. We use the letters $P$, $Q$, $R$ (called *statement letters*) to stand for arbitrary statements.

    [^informal-numbers]: Numbers, arithmetic, and inequalities are used informally in this chapter's examples. [Chapter 2](ch2_axioms_of_set_theory.md) builds the natural numbers from sets, [Appendix B](appendix_b_number_systems.md) builds the integers, rationals, and reals, and [Chapter 3](ch3_sets_for_probability.md) lists the properties of the real numbers that we rely on.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Connectives and Truth Tables

    Statements combine into compound statements using *connectives*. A connective's meaning is fixed completely by saying what truth value the compound statement has for each combination of truth values of its parts.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Truth table**</u>

    A table with one row for each way of assigning a truth value ($\text{T}$ or $\text{F}$) to each of the statement letters $P, Q, \ldots$ in a compound statement, listing the truth value of the compound statement under that assignment.
    ///

    With $n$ statement letters there are $2^n$ assignments, so $2^n$ rows. The five connectives used in this book are defined by this truth table:

    $$\begin{array}{cc|ccccc}
    P & Q & \lnot P & P \land Q & P \lor Q & P \rightarrow Q & P \leftrightarrow Q \\
    \hline
    \text{T} & \text{T} & \text{F} & \text{T} & \text{T} & \text{T} & \text{T} \\
    \text{T} & \text{F} & \text{F} & \text{F} & \text{T} & \text{F} & \text{F} \\
    \text{F} & \text{T} & \text{T} & \text{F} & \text{T} & \text{T} & \text{F} \\
    \text{F} & \text{F} & \text{T} & \text{F} & \text{F} & \text{T} & \text{T} \\
    \end{array}$$

    - **Negation** $\lnot P$, read "not $P$": true exactly when $P$ is false.
    - **Conjunction** $P \land Q$, read "$P$ and $Q$": true exactly when both are true.
    - **Disjunction** $P \lor Q$, read "$P$ or $Q$": true exactly when at least one is true. This "or" is *inclusive*: it is true when both parts are true. "Either $P$ or $Q$ but not both" is written $(P \lor Q) \land \lnot(P \land Q)$.
    - **Conditional** $P \rightarrow Q$, read "if $P$ then $Q$" or "$P$ implies $Q$": false exactly when $P$ is true and $Q$ is false. $P$ is the *hypothesis* and $Q$ the *conclusion*. Other English forms of $P \rightarrow Q$: "$Q$ if $P$", "$P$ only if $Q$", "$Q$ whenever $P$".
    - **Biconditional** $P \leftrightarrow Q$, read "$P$ if and only if $Q$" (abbreviated "$P$ iff $Q$"): true exactly when $P$ and $Q$ have the same truth value.

    To save parentheses, $\lnot$ applies to the smallest statement after it, and the binary connectives bind in the order $\land$, $\lor$, $\rightarrow$, $\leftrightarrow$ (tightest first). So $\lnot P \land Q$ means $(\lnot P) \land Q$, and $P \land Q \rightarrow R$ means $(P \land Q) \rightarrow R$. When in doubt, we write the parentheses.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vacuous Truth

    The last two rows of the conditional surprise most readers: when $P$ is false, $P \rightarrow Q$ is true whatever $Q$ is. Think of $P \rightarrow Q$ as a promise: "If it rains tomorrow, I will bring an umbrella." The promise is broken in exactly one situation: it rains and I don't bring one. If it doesn't rain, I have kept my promise whether or not I bring an umbrella. A conditional whose hypothesis is false is called *vacuously true*.

    Vacuous truth is what makes general rules work. "For every reading, if the reading exceeds 300 lb then the scale displays an error" should be true of a correctly working scale, and that requires the conditional to be true for each reading below 300 lb, where its hypothesis is false.

    The conditional also asserts no cause and effect. "If $2 + 2 = 5$, then the Moon is made of cheese" is true, because its hypothesis is false. In mathematics, $P \rightarrow Q$ is a claim about truth values only.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Necessary and Sufficient Conditions

    When $P \rightarrow Q$ is true, knowing $P$ is enough to conclude $Q$, and $P$ cannot hold without $Q$ holding too. These two readings have names.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Sufficient condition**</u>

    $P$ is a sufficient condition for $Q$ iff $P \rightarrow Q$ is true: whenever $P$ is true, $Q$ is true.
    ///

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Necessary condition**</u>

    $Q$ is a necessary condition for $P$ iff $P \rightarrow Q$ is true: $P$ is never true while $Q$ is false.
    ///

    So "$P$ is sufficient for $Q$" and "$Q$ is necessary for $P$" are the same claim. $P$ is *necessary and sufficient* for $Q$ iff both $P \rightarrow Q$ and $Q \rightarrow P$ are true, which by the truth table happens exactly when $P \leftrightarrow Q$ is true.

    Usually the conditions are properties of an object rather than single statements. For an integer $n$, "$n$ is divisible by 4" is sufficient but not necessary for "$n$ is even" ($n = 2$ is even but not divisible by 4), and "$n$ is even" is necessary but not sufficient for "$n$ is divisible by 4". Here the conditional must hold for *every* $n$; Quantifiers below makes "for every" precise.

    This is exactly the standard the book's guiding principles set for a {term}`definition`: a list of requirements that are necessary and sufficient for belonging to the category a word names. "A square is a four-sided figure whose sides are all equal and whose angles are all right angles." Each requirement is necessary: a figure missing any one of them is not a square. Together they are sufficient: a figure meeting all of them is a square. A test that is only necessary ("a square has four sides") lets in non-squares; a test that is only sufficient ("a four-sided figure with all sides of length 1 and all angles right angles") shuts out squares of other sizes. That is why a definition is a biconditional, a form we give its own notation in Definitions below.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Tautologies and Logical Equivalence

    An expression built from statement letters with connectives, such as $\lnot(P \land Q)$, is a *statement form*. Replacing each letter by a statement turns it into a statement whose truth value depends only on the truth values substituted, so a truth table evaluates a statement form under every possible substitution at once. Some statement forms are true for reasons of form alone: $P \lor \lnot P$ is true whether $P$ is true or false.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Tautology**</u>

    A statement form that is true under every assignment of truth values to its statement letters.
    ///

    A statement form that is false under every assignment, such as $P \land \lnot P$, is called a *contradiction*.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Logically equivalent**</u>

    Two statement forms $A$ and $B$ are logically equivalent, written $A \equiv B$, iff they have the same truth value under every assignment of truth values to their statement letters. Equivalently, $A \leftrightarrow B$ is a {term}`tautology`.
    ///

    The two versions agree because $A \leftrightarrow B$ is true exactly when $A$ and $B$ have the same truth value. The symbol $\equiv$ is not a connective: like the English around it, it belongs to the metalanguage and makes a claim *about* two statement forms. Logical equivalence is useful for two reasons:

    - The truth value of a compound statement depends only on the truth values of its parts, so **replacing any part of a statement by a logically equivalent statement form never changes its truth value.**
    - A law below holds under every assignment of truth values to $P, Q, R$, so it continues to hold when $P, Q, R$ are replaced by any statement forms.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The Laws Used Most

    1. **Double negation:** $\lnot\lnot P \equiv P$.
    2. **De Morgan's laws:** $\lnot(P \land Q) \equiv \lnot P \lor \lnot Q$ and $\lnot(P \lor Q) \equiv \lnot P \land \lnot Q$.
    3. **Conditional as disjunction:** $P \rightarrow Q \equiv \lnot P \lor Q$, and its negation $\lnot(P \rightarrow Q) \equiv P \land \lnot Q$.
    4. **Contrapositive:** $P \rightarrow Q \equiv \lnot Q \rightarrow \lnot P$.
    5. **Biconditional as two conditionals:** $P \leftrightarrow Q \equiv (P \rightarrow Q) \land (Q \rightarrow P)$.
    6. **Distributive laws:** $P \land (Q \lor R) \equiv (P \land Q) \lor (P \land R)$ and $P \lor (Q \land R) \equiv (P \lor Q) \land (P \lor R)$.
    7. **Excluded middle:** $P \lor \lnot P$ is a tautology.

    Each law is proved by a truth table. For double negation: if $P$ is $\text{T}$, then $\lnot P$ is $\text{F}$ and $\lnot\lnot P$ is $\text{T}$; if $P$ is $\text{F}$, then $\lnot P$ is $\text{T}$ and $\lnot\lnot P$ is $\text{F}$. For excluded middle: exactly one of $P$ and $\lnot P$ is true, so their disjunction is true. For De Morgan's laws, compare the last two columns of each group:

    $$\begin{array}{cc|ccc|ccc}
    P & Q & P \land Q & \lnot(P \land Q) & \lnot P \lor \lnot Q & P \lor Q & \lnot(P \lor Q) & \lnot P \land \lnot Q \\
    \hline
    \text{T} & \text{T} & \text{T} & \text{F} & \text{F} & \text{T} & \text{F} & \text{F} \\
    \text{T} & \text{F} & \text{F} & \text{T} & \text{T} & \text{T} & \text{F} & \text{F} \\
    \text{F} & \text{T} & \text{F} & \text{T} & \text{T} & \text{T} & \text{F} & \text{F} \\
    \text{F} & \text{F} & \text{F} & \text{T} & \text{T} & \text{F} & \text{T} & \text{T} \\
    \end{array}$$

    Laws 3–5 are checked on one table. The columns $P \rightarrow Q$, $\lnot Q \rightarrow \lnot P$, and $\lnot P \lor Q$ agree; so do $\lnot(P \rightarrow Q)$ and $P \land \lnot Q$; and so do the last two:

    $$\begin{array}{cc|ccc|cc|c|cc}
    P & Q & P \rightarrow Q & \lnot Q \rightarrow \lnot P & \lnot P \lor Q & \lnot(P \rightarrow Q) & P \land \lnot Q & Q \rightarrow P & (P \rightarrow Q) \land (Q \rightarrow P) & P \leftrightarrow Q \\
    \hline
    \text{T} & \text{T} & \text{T} & \text{T} & \text{T} & \text{F} & \text{F} & \text{T} & \text{T} & \text{T} \\
    \text{T} & \text{F} & \text{F} & \text{F} & \text{F} & \text{T} & \text{T} & \text{T} & \text{F} & \text{F} \\
    \text{F} & \text{T} & \text{T} & \text{T} & \text{T} & \text{F} & \text{F} & \text{F} & \text{F} & \text{F} \\
    \text{F} & \text{F} & \text{T} & \text{T} & \text{T} & \text{F} & \text{F} & \text{T} & \text{T} & \text{T} \\
    \end{array}$$

    For the first distributive law, compare the fifth and last columns:

    $$\begin{array}{ccc|ccccc}
    P & Q & R & Q \lor R & P \land (Q \lor R) & P \land Q & P \land R & (P \land Q) \lor (P \land R) \\
    \hline
    \text{T} & \text{T} & \text{T} & \text{T} & \text{T} & \text{T} & \text{T} & \text{T} \\
    \text{T} & \text{T} & \text{F} & \text{T} & \text{T} & \text{T} & \text{F} & \text{T} \\
    \text{T} & \text{F} & \text{T} & \text{T} & \text{T} & \text{F} & \text{T} & \text{T} \\
    \text{T} & \text{F} & \text{F} & \text{F} & \text{F} & \text{F} & \text{F} & \text{F} \\
    \text{F} & \text{T} & \text{T} & \text{T} & \text{F} & \text{F} & \text{F} & \text{F} \\
    \text{F} & \text{T} & \text{F} & \text{T} & \text{F} & \text{F} & \text{F} & \text{F} \\
    \text{F} & \text{F} & \text{T} & \text{T} & \text{F} & \text{F} & \text{F} & \text{F} \\
    \text{F} & \text{F} & \text{F} & \text{F} & \text{F} & \text{F} & \text{F} & \text{F} \\
    \end{array}$$

    The second distributive law follows from the first without a new table. Apply double negation, then De Morgan's laws, then the first distributive law (with $\lnot P, \lnot Q, \lnot R$ in place of $P, Q, R$), then De Morgan's laws and double negation again:

    $$\begin{aligned}
    P \lor (Q \land R) &\equiv \lnot\big(\lnot P \land \lnot(Q \land R)\big) \equiv \lnot\big(\lnot P \land (\lnot Q \lor \lnot R)\big) \equiv \lnot\big((\lnot P \land \lnot Q) \lor (\lnot P \land \lnot R)\big) \\
    &\equiv \lnot(\lnot P \land \lnot Q) \land \lnot(\lnot P \land \lnot R) \equiv (P \lor Q) \land (P \lor R).
    \end{aligned}$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Contrapositive Versus Converse

    The *contrapositive* of $P \rightarrow Q$ is $\lnot Q \rightarrow \lnot P$, and law 4 says it is logically equivalent to the original. The *converse* of $P \rightarrow Q$ is $Q \rightarrow P$, and it is **not** equivalent: in the second table above, the columns $P \rightarrow Q$ and $Q \rightarrow P$ differ in the second and third rows. For example, "if $n$ is divisible by 4, then $n$ is even" is true for every integer $n$, but its converse "if $n$ is even, then $n$ is divisible by 4" is false for $n = 2$. Proving the converse of what was asked is one of the most common errors in mathematics.

    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    A conditional and its contrapositive always have the same truth value. A conditional and its converse need not.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try It: Truth-Table Generator

    Choose an example or type your own statement form in the letters $P$, $Q$, $R$. The generator builds the full truth table, one column per sub-form, and reports whether the form is a tautology, a contradiction, or neither. To test whether two forms $A$ and $B$ are logically equivalent, enter $A \leftrightarrow B$ and check whether it is a tautology. You can type the connectives as follows (spaces are optional):

    - $\lnot$: `~`, `!`, `¬`, or `not`
    - $\land$: `&`, `∧`, or `and`
    - $\lor$: `|`, `∨`, or `or`
    - $\rightarrow$: `->`, `=>`, `→`, or `implies`
    - $\leftrightarrow$: `<->`, `<=>`, `↔`, or `iff`

    Parentheses group as usual, and the precedence rules from Connectives and Truth Tables apply; a chain $P \rightarrow Q \rightarrow R$ is read $P \rightarrow (Q \rightarrow R)$. The input is read by a small parser that only understands these symbols; it never runs your text as code.
    """)
    return


@app.cell
def truth_table_engine():
    # jb: include=false
    from itertools import product

    TT_LETTERS = ("P", "Q", "R")
    _SYMBOLS = (
        ("<->", "iff"), ("<=>", "iff"), ("->", "imp"), ("=>", "imp"),
        ("¬", "not"), ("~", "not"), ("!", "not"),
        ("∧", "and"), ("&", "and"), ("∨", "or"), ("|", "or"),
        ("→", "imp"), ("↔", "iff"), ("(", "("), (")", ")"),
    )
    _WORDS = {"not": "not", "and": "and", "or": "or", "implies": "imp", "iff": "iff"}
    _SHOW = {"not": "¬", "and": "∧", "or": "∨", "imp": "→", "iff": "↔", "(": "(", ")": ")"}
    _TEX = {"and": r"\land", "or": r"\lor", "imp": r"\rightarrow", "iff": r"\leftrightarrow"}

    def tt_tokenize(text):
        """Split text into letters, connective names, and parentheses."""
        tokens = []
        i = 0
        while i < len(text):
            if text[i].isspace():
                i += 1
                continue
            for sym, tok in _SYMBOLS:
                if text.startswith(sym, i):
                    tokens.append(tok)
                    i += len(sym)
                    break
            else:
                if not text[i].isalpha():
                    raise ValueError(f"The symbol '{text[i]}' is not recognized.")
                j = i
                while j < len(text) and text[j].isalpha():
                    j += 1
                word = text[i:j]
                if word.upper() in TT_LETTERS:
                    tokens.append(word.upper())
                elif word.lower() in _WORDS:
                    tokens.append(_WORDS[word.lower()])
                else:
                    raise ValueError(
                        f"'{word}' is not a statement letter or connective. "
                        "Use the letters P, Q, R, separated by connectives."
                    )
                i = j
        return tokens

    def tt_parse(text):
        """Recursive-descent parser. Returns a nested tuple such as
        ('imp', ('var', 'P'), ('var', 'Q')). Precedence, tightest first:
        not, and, or, imp (right-associative), iff."""
        tokens = tt_tokenize(text)
        if not tokens:
            raise ValueError("Type a statement form, for example P -> Q.")
        pos = [0]

        def peek():
            return tokens[pos[0]] if pos[0] < len(tokens) else None

        def take():
            tok = peek()
            pos[0] += 1
            return tok

        def left_assoc(op, sub):
            node = sub()
            while peek() == op:
                take()
                node = (op, node, sub())
            return node

        def iff_level():
            return left_assoc("iff", imp_level)

        def imp_level():
            node = or_level()
            if peek() == "imp":
                take()
                return ("imp", node, imp_level())
            return node

        def or_level():
            return left_assoc("or", and_level)

        def and_level():
            return left_assoc("and", not_level)

        def not_level():
            if peek() == "not":
                take()
                return ("not", not_level())
            return atom()

        def atom():
            tok = take()
            if tok is None:
                raise ValueError("The statement form ends too early.")
            if tok in TT_LETTERS:
                return ("var", tok)
            if tok == "(":
                node = iff_level()
                if take() != ")":
                    raise ValueError("A '(' is never closed.")
                return node
            raise ValueError(f"Unexpected '{_SHOW[tok]}'.")

        tree = iff_level()
        if peek() is not None:
            raise ValueError(f"Unexpected '{_SHOW[peek()]}' after a complete statement form.")
        return tree

    def tt_value(node, values):
        kind = node[0]
        if kind == "var":
            return values[node[1]]
        if kind == "not":
            return not tt_value(node[1], values)
        a, b = tt_value(node[1], values), tt_value(node[2], values)
        if kind == "and":
            return a and b
        if kind == "or":
            return a or b
        if kind == "imp":
            return (not a) or b
        return a == b

    def tt_latex(node, top=True):
        kind = node[0]
        if kind == "var":
            return node[1]
        if kind == "not":
            return r"\lnot " + tt_latex(node[1], top=False)
        body = f"{tt_latex(node[1], False)} {_TEX[kind]} {tt_latex(node[2], False)}"
        return body if top else f"({body})"

    def tt_parts(node, out):
        """Compound sub-forms in the order they are built, without repeats."""
        if node[0] == "not":
            tt_parts(node[1], out)
        elif node[0] != "var":
            tt_parts(node[1], out)
            tt_parts(node[2], out)
        if node[0] != "var" and node not in out:
            out.append(node)
        return out

    def tt_letters(node):
        if node[0] == "var":
            return {node[1]}
        return set().union(*(tt_letters(child) for child in node[1:]))

    def truth_table_markdown(text):
        try:
            tree = tt_parse(text)
        except ValueError as err:
            return f"**Could not read the statement form.** {err}"
        used = [L for L in TT_LETTERS if L in tt_letters(tree)]
        parts = tt_parts(tree, [])
        header = [f"${L}$" for L in used] + [
            f"${tt_latex(p)}$" if p is not tree else f"$\\mathbf{{{tt_latex(p)}}}$"
            for p in parts
        ]
        lines = ["| " + " | ".join(header) + " |", "|" + ":-:|" * len(header)]
        results = []
        for row in product((True, False), repeat=len(used)):
            values = dict(zip(used, row))
            cells = ["T" if v else "F" for v in row]
            for p in parts:
                v = tt_value(p, values)
                cells.append(("**T**" if v else "**F**") if p is tree else ("T" if v else "F"))
            results.append(tt_value(tree, values))
            lines.append("| " + " | ".join(cells) + " |")
        n_true, n_rows = sum(results), len(results)
        if n_true == n_rows:
            verdict = f"True in all {n_rows} rows: a **tautology**."
            if tree[0] == "iff":
                verdict += " Since it is a biconditional, its two sides are **logically equivalent**."
        elif n_true == 0:
            verdict = f"False in all {n_rows} rows: a **contradiction**."
        else:
            verdict = (f"True in {n_true} of {n_rows} rows: neither a tautology nor a contradiction.")
            if tree[0] == "iff":
                verdict += " Its two sides are **not** logically equivalent."
        return "\n".join(lines) + "\n\n" + verdict

    return (truth_table_markdown,)


@app.cell(hide_code=True)
def _(mo):
    tt_preset = mo.ui.dropdown(
        options={
            "Conditional: P → Q": "P -> Q",
            "Contrapositive: (P → Q) ↔ (¬Q → ¬P)": "(P -> Q) <-> (~Q -> ~P)",
            "Converse: (P → Q) ↔ (Q → P)": "(P -> Q) <-> (Q -> P)",
            "De Morgan: ¬(P ∧ Q) ↔ (¬P ∨ ¬Q)": "~(P & Q) <-> (~P | ~Q)",
            "Distributive: P ∧ (Q ∨ R) ↔ (P ∧ Q) ∨ (P ∧ R)": "P & (Q | R) <-> (P & Q) | (P & R)",
            "Excluded middle: P ∨ ¬P": "P | ~P",
            "Contradiction: P ∧ ¬P": "P & ~P",
            "Proof by cases: ((P ∨ Q) ∧ (P → R) ∧ (Q → R)) → R": "((P | Q) & (P -> R) & (Q -> R)) -> R",
            "Proof by contradiction: (¬P → (Q ∧ ¬Q)) → P": "(~P -> (Q & ~Q)) -> P",
        },
        value="Contrapositive: (P → Q) ↔ (¬Q → ¬P)",
        label="Example",
    )
    return (tt_preset,)


@app.cell(hide_code=True)
def _(mo, tt_preset):
    tt_formula = mo.ui.text(value=tt_preset.value, label="Statement form", full_width=True)
    return (tt_formula,)


@app.cell(hide_code=True)
def _(mo, truth_table_markdown, tt_formula, tt_preset):
    mo.vstack([tt_preset, tt_formula, mo.md(truth_table_markdown(tt_formula.value))])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Predicates and Variables

    The expression "$z > 150$" from the start of the chapter is not a statement, because $z$ has no fixed value. Once a value is supplied it becomes one: with $z = 155.3$ it is true, with $z = 149$ it is false.

    A *variable* is a symbol, such as $x$, $z$, or $n$, that stands for an unspecified object. The objects a variable may stand for form the *domain of discourse*, which must be stated (or clear from context) before an expression involving variables has a meaning. (This is unrelated to the {term}`domain` of a function, defined in [Chapter 2](ch2_axioms_of_set_theory.md).)

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Predicate**</u>

    An expression containing one or more variables that becomes a {term}`statement` whenever each of its variables is replaced by a name of an object in the domain of discourse.
    ///

    We name predicates by their variables: if $P(z)$ is "$z > 150$" with the real numbers as domain of discourse, then $P(155.3)$ is a true statement and $P(149)$ is a false one. A predicate may have several variables: $L(x, y)$, "$x \le y$", becomes a statement once both $x$ and $y$ are given values. A predicate with one variable is often called a *property*.

    Connectives combine predicates just as they combine statements: $P(z) \land L(z, 160)$ is the predicate "$z > 150$ and $z \le 160$". In [Chapter 2](ch2_axioms_of_set_theory.md), set theory starts from a single undefined predicate, $x \in y$ ("$x$ is an element of $y$"). Every other predicate in this book is defined from it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Quantifiers

    There are two ways to turn a predicate into a statement without choosing values for its variables: claim that it holds for every object, or that it holds for at least one.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Quantifier**</u>

    Either of the symbols $\forall$ ("for all") and $\exists$ ("there exists"), which form statements from a {term}`predicate` $P(x)$ as follows:

    - $\forall x\, P(x)$ is true iff $P(a)$ is true for every object $a$ in the domain of discourse;
    - $\exists x\, P(x)$ is true iff $P(a)$ is true for at least one object $a$ in the domain of discourse.
    ///

    $\forall$ is the *universal* quantifier and $\exists$ the *existential* quantifier. The truth value depends on the domain of discourse: $\exists x\,(x \cdot x = 2)$ is false when $x$ ranges over the rational numbers and true when it ranges over the real numbers. The domain of discourse is always assumed to contain at least one object.

    In $\forall x\, P(x)$, the variable $x$ is *bound* by the quantifier: the statement is about the whole domain of discourse, not about some particular $x$. Renaming a bound variable to a letter not already in use does not change the meaning, so $\forall x\, P(x)$ and $\forall y\, P(y)$ say the same thing. A variable that is not bound is *free*, and a predicate's free variables are the ones still waiting for values. Precise definitions of {term}`free <free variable>` and {term}`bound variables <bound variable>` are in [Appendix A: Formal Syntax](appendix_a_formal_logic.md).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Order Matters

    Let the domain of discourse be the natural numbers $0, 1, 2, \ldots$, and compare

    $$\forall n\, \exists m\, (m > n) \qquad\text{and}\qquad \exists m\, \forall n\, (m > n).$$

    The first says every natural number has a larger one. It is true: for each $n$, take $m = n + 1$. The second says some single natural number is larger than every natural number, itself included. It is false: no $m$ satisfies $m > m$. The difference is what may depend on what. In $\forall n\, \exists m$, the $m$ may be chosen *after* $n$, so it may depend on $n$. In $\exists m\, \forall n$, one $m$ must work for every $n$. Quantifiers of the same kind do commute: $\forall x\, \forall y\, P(x, y)$ and $\forall y\, \forall x\, P(x, y)$ both say $P(a, b)$ holds for every pair of objects, and similarly for $\exists$.

    ### Negating Quantified Statements

    $\forall x\, P(x)$ is false iff $P(a)$ is false for at least one $a$, that is, iff $\exists x\, \lnot P(x)$ is true. Likewise, $\exists x\, P(x)$ is false iff $P(a)$ is false for every $a$, that is, iff $\forall x\, \lnot P(x)$ is true. So

    $$\lnot \forall x\, P(x) \equiv \exists x\, \lnot P(x), \qquad \lnot \exists x\, P(x) \equiv \forall x\, \lnot P(x),$$

    where $\equiv$ now means "has the same truth value for every domain of discourse and every predicate $P$" (made precise in [Appendix A: Formal Semantics](appendix_a_formal_logic.md)). Pushing $\lnot$ past a quantifier flips the quantifier. Applied repeatedly, this negates any statement mechanically:

    $$\lnot \forall n\, \exists m\, (m > n) \equiv \exists n\, \lnot \exists m\, (m > n) \equiv \exists n\, \forall m\, \lnot(m > n) \equiv \exists n\, \forall m\, (m \le n).$$

    The last step uses a fact about the order of numbers, not logic: $\lnot(m > n)$ iff $m \le n$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Bounded Quantifiers

    Most quantifiers in mathematics range over part of the domain of discourse: "every element of the set $A$"[^informal-sets], or "every $\varepsilon > 0$". These are abbreviations:

    $$\forallin{x}{A} P(x) := \forall x\, (x \in A \rightarrow P(x)), \qquad \existsin{x}{A} P(x) := \exists x\, (x \in A \land P(x)),$$

    read "for all $x$ in $A$, $P(x)$" and "there exists $x$ in $A$ such that $P(x)$". (The symbol $:=$ is explained in Definitions below.) The universal form uses $\rightarrow$ and the existential form uses $\land$, and swapping them gives the wrong meaning. $\forall x\,(x \in A \land P(x))$ would claim that *every* object is in $A$. $\exists x\,(x \in A \rightarrow P(x))$ is true as soon as any object lies outside $A$ (by vacuous truth), whatever $P$ is. Bounds written with an inequality work the same way: $\forall \varepsilon > 0\; P(\varepsilon)$ abbreviates $\forall \varepsilon\,(\varepsilon > 0 \rightarrow P(\varepsilon))$, and $\exists k \ge K\; P(k)$ abbreviates $\exists k\,(k \ge K \land P(k))$. Once {term}`subsets <subset>` are defined in [Chapter 2](ch2_axioms_of_set_theory.md), $\forallsubseteq{x}{A} P(x)$ and $\existssubseteq{x}{A} P(x)$ abbreviate $\forall x\,(x \subseteq A \rightarrow P(x))$ and $\exists x\,(x \subseteq A \land P(x))$.

    If $A$ has no elements, then $\forallin{x}{A} P(x)$ is true (vacuously, since every hypothesis $x \in A$ is false) and $\existsin{x}{A} P(x)$ is false, whatever $P$ is.

    Bounded quantifiers negate just like unbounded ones, keeping the bound:

    $$\lnot \forallin{x}{A} P(x) \equiv \existsin{x}{A} \lnot P(x), \qquad \lnot \existsin{x}{A} P(x) \equiv \forallin{x}{A} \lnot P(x).$$

    For the first, $\lnot \forall x\,(x \in A \rightarrow P(x)) \equiv \exists x\, \lnot(x \in A \rightarrow P(x)) \equiv \exists x\,(x \in A \land \lnot P(x))$, by the quantifier rule and then the negated conditional (law 3). For the second, $\lnot \exists x\,(x \in A \land P(x)) \equiv \forall x\, \lnot(x \in A \land P(x)) \equiv \forall x\,(\lnot\, x \in A \lor \lnot P(x)) \equiv \forall x\,(x \in A \rightarrow \lnot P(x))$, by the quantifier rule, De Morgan's law, and the conditional as a disjunction (law 3). Each step replaces the predicate inside the quantifier by one with the same truth value for every $x$, which leaves the quantified statement's truth value unchanged.

    [^informal-sets]: Used informally here: a set is a collection of objects, and $x \in A$ means $x$ is an element of $A$. [Chapter 2](ch2_axioms_of_set_theory.md) takes "set" and "$\in$" as undefined notions governed by axioms.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Example: Convergence of a Filter

    Suppose a filter estimates a constant true value $x$, producing estimates $\hat x_1, \hat x_2, \ldots$. With $\varepsilon$ ranging over real numbers and $K, k$ over step numbers, "the estimates converge to $x$" means

    $$\forall \varepsilon > 0\;\, \exists K\;\, \forall k \ge K\;\, (x - \varepsilon < \hat x_k < x + \varepsilon):$$

    for every tolerance $\varepsilon$, however small, there is a step $K$ after which every estimate is within $\varepsilon$ of $x$. The step $K$ may depend on $\varepsilon$; smaller tolerances may take longer to reach. ([Appendix C: Sequences and Limits](appendix_c_calculus.md) studies this definition.)

    *Swapping the quantifiers* gives $\exists K\;\, \forall \varepsilon > 0\;\, \forall k \ge K\;\, (x - \varepsilon < \hat x_k < x + \varepsilon)$: one step $K$ works for every tolerance. Then each $\hat x_k$ with $k \ge K$ is within *every* positive distance of $x$, so $\hat x_k = x$ exactly. That is a far stronger claim, which no filter fed noisy measurements can be expected to satisfy.

    *Negating* with the rules above (and $\lnot(a < b < c)$ iff $b \le a$ or $b \ge c$) gives what it means for the estimates **not** to converge to $x$:

    $$\exists \varepsilon > 0\;\, \forall K\;\, \exists k \ge K\;\, (\hat x_k \le x - \varepsilon \lor \hat x_k \ge x + \varepsilon):$$

    some tolerance is violated at arbitrarily late steps.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Unique Existence

    "There exists exactly one $x$ such that $P(x)$" is written $\exists! x\, P(x)$ and abbreviates

    $$\exists! x\, P(x) := \exists x\, \big(P(x) \land \forall y\, (P(y) \rightarrow y = x)\big),$$

    where $y$ is a variable that does not occur in $P(x)$, and $y = x$ means $y$ and $x$ are the same object. It combines *existence* (some $x$ has the property) and *uniqueness* (any $y$ with the property is that $x$), and a proof of $\exists!$ must establish both. Over the natural numbers, $\exists! n\,(n + 2 = 5)$ is true, while $\exists! n\,(n \cdot n = n)$ is false because both $0$ and $1$ satisfy it. [Chapter 2](ch2_axioms_of_set_theory.md) uses unique existence to justify giving sets names such as $\emptyset$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Definitions: $:=$ and $:\Longleftrightarrow$

    A definition introduces a new symbol or word as an abbreviation for something already meaningful. There are two kinds.

    - **Naming an object:** $a := b$, read "$a$ is defined to be $b$". The left side is new; the right side uses only notation defined earlier and names exactly one object. Example: the average of the first $k$ measurements, $\bar x_k := (z_1 + \cdots + z_k)/k$. The bounded quantifiers above were defined this way too, as abbreviations for longer expressions.
    - **Naming a property:** $P(x) :\Longleftrightarrow \varphi(x)$, read "$P(x)$ is defined to mean $\varphi(x)$", where $\varphi(x)$ is a predicate built from notation defined earlier. Example: for an integer $n$, "$n$ is even" $:\Longleftrightarrow \exists m\,(n = 2m)$ and "$n$ is odd" $:\Longleftrightarrow \exists m\,(n = 2m + 1)$, with $m$ ranging over the integers.

    Both $:=$ and $:\Longleftrightarrow$ belong to the metalanguage. The symbols $=$ and $\leftrightarrow$ appear *inside* statements and make claims; $:=$ and $:\Longleftrightarrow$ are announcements about notation and make no claim at all. A definition of a property is a biconditional, so it gives a condition that is necessary and sufficient for the property, exactly the test a {term}`definition` must pass. (Many texts write "if" in definitions where "iff" is meant; this book always means "iff".)

    Naming an object with $:=$ requires that the right side names exactly one object. When an object is *described* by a property ("the set with no elements"), the $\exists!$ statement must be proved before the name may be used; [Chapter 2](ch2_axioms_of_set_theory.md) does exactly this. Because every defined symbol can be replaced by its definition, definitions add convenience but no new assumptions. [Appendix A: Extension by Definitions](appendix_a_formal_logic.md) proves this.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Axioms, Theorems, and Proofs

    Mathematics sorts true statements by *how* they are known to be true. A few are assumed; everything else is proved from them.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Axiom**</u>

    A {term}`statement` assumed without proof as one of the starting points of a mathematical theory, where a *theory* is the subject determined by a chosen list of axioms.
    ///

    For example, set theory (ZFC) is determined by the axioms in [Chapter 2](ch2_axioms_of_set_theory.md), and the theory of complete ordered fields by the axioms in [Chapter 3](ch3_sets_for_probability.md). An axiom is not claimed to be "self-evident", only assumed. Whether it is actually true depends on what objects we interpret it to be about. For instance, the axioms of a complete ordered field are all true of the real numbers, but not all true of the rational numbers. A theorem of the theory is then guaranteed to be true of any objects of which all the axioms are true. [Appendix A: Theories and Logical Consequence](appendix_a_formal_logic.md) makes this precise.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Rules of Inference

    A *rule of inference* licenses writing down a conclusion once certain premises have been established. A rule is *valid* if it never leads from true premises to a false conclusion: in every situation in which all of its premises are true, its conclusion is true. The proofs in this book use these valid rules:

    1. **Modus ponens:** from $P$ and $P \rightarrow Q$, conclude $Q$. (Valid: the only row of the truth table in which $P$ and $P \rightarrow Q$ are both true has $Q$ true.)
    2. **Replacement by equivalents:** replace a statement, or any part of it, by a logically equivalent one. Any statement obtained from a tautology by replacing its letters with statements may be written down at any time.
    3. **Conditional proof:** to prove $P \rightarrow Q$, *assume* $P$, derive $Q$, and conclude $P \rightarrow Q$. The assumption $P$ is *in force* only until $P \rightarrow Q$ is concluded, and may not be used afterward. (Valid: if $P$ is false, $P \rightarrow Q$ is vacuously true; if $P$ is true, the derivation makes $Q$ true.)
    4. **Universal instantiation:** from $\forall x\, P(x)$, conclude $P(a)$ for any object $a$.
    5. **Universal generalization:** if $P(a)$ has been proved for an *arbitrary* $a$ (one about which nothing is assumed that is not assumed about every object), conclude $\forall x\, P(x)$. In prose: "Let $a$ be arbitrary."
    6. **Existential generalization:** from $P(a)$ for some particular object $a$, conclude $\exists x\, P(x)$.
    7. **Existential instantiation:** from $\exists x\, P(x)$, introduce a *new* name $c$ for an object with $P(c)$. The name $c$ must not already be in use, and the final conclusion must not mention $c$.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Proof**</u>

    A proof of a statement $S$ in a theory is a finite sequence of statements ending with $S$, in which every statement is an {term}`axiom` of the theory, a statement proved earlier, an instance of a definition, an assumption in force, or the conclusion of a valid rule of inference applied to earlier statements in the sequence.
    ///

    Proofs in this book are *rigorous informal arguments*: written in English and standard notation, with each step justified by a rule above, a definition, an axiom, or an earlier result, and with routine steps combined when the justification is clear. Each could be expanded into a fully formal proof, a sequence of formulas that a computer could check, in the deductive system of [Appendix A: Formal Proofs](appendix_a_formal_logic.md). The Soundness and Completeness Theorem stated there shows that formal proofs establish exactly the statements that are true in every situation where the axioms are true.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Theorems, Lemmas, and Corollaries

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Theorem**</u>

    A {term}`statement` that has a {term}`proof` from the axioms of the theory under consideration.
    ///

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Lemma**</u>

    A {term}`theorem` proved mainly in order to be used in proving other theorems.
    ///

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Corollary**</u>

    A {term}`theorem` that follows from a preceding theorem by a short additional argument.
    ///

    The laws of logic proved by truth tables earlier are theorems of logic alone, true in every theory. The labels Lemma and Corollary describe a theorem's role, not its importance. This book displays results and their proofs in boxes like these:

    /// important | 📐 **Theorem (Name)**
        attrs: {class: no-icon}
    The statement being proved.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    The argument, ending with the symbol $\blacksquare$, which marks the end of a proof. $\blacksquare$
    ///

    When a proof is not given, the proof box says so and links to one.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Proof Techniques

    Each technique below is a pattern of the rules of inference, justified by a tautology. The examples use the integers and real numbers informally, together with the definitions of even and odd from Definitions above. The last technique in common use, proof by induction, needs the natural numbers and appears in [Chapter 2](ch2_axioms_of_set_theory.md).

    ### Direct Proof

    To prove $\forall x\,(P(x) \rightarrow Q(x))$: let $x$ be arbitrary, assume $P(x)$, and derive $Q(x)$. This is conditional proof followed by universal generalization.

    /// important | 📐 **Theorem**
        attrs: {class: no-icon}
    For every integer $n$, if $n$ is even, then $n^2$ is even.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Let $n$ be an arbitrary integer, and assume $n$ is even. By the definition of even, there is an integer $m$ with $n = 2m$ (existential instantiation). Then $n^2 = 4m^2 = 2(2m^2)$, and $2m^2$ is an integer, so $n^2$ is even by the definition of even (existential generalization, with $2m^2$ as the witness). Since $n$ was arbitrary, the statement holds for every integer. $\blacksquare$
    ///

    ### Proof by Contrapositive

    Since $P \rightarrow Q \equiv \lnot Q \rightarrow \lnot P$, we may prove $\lnot Q \rightarrow \lnot P$ directly instead. This helps when $\lnot Q$ gives more to work with than $P$ does.

    /// important | 📐 **Theorem**
        attrs: {class: no-icon}
    For all real numbers $x$ and $y$, if $x + y \ge 2$, then $x \ge 1$ or $y \ge 1$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Let $x$ and $y$ be arbitrary real numbers. We prove the contrapositive. By De Morgan's law, the negation of "$x \ge 1$ or $y \ge 1$" is "$x < 1$ and $y < 1$". Assume this. Adding the two inequalities gives $x + y < 2$, which is the negation of $x + y \ge 2$. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Proof by Contradiction

    To prove $S$: assume $\lnot S$ and derive a contradiction, a statement of the form $Q \land \lnot Q$. This is justified by the tautology $\big(\lnot S \rightarrow (Q \land \lnot Q)\big) \rightarrow S$: conditional proof establishes $\lnot S \rightarrow (Q \land \lnot Q)$, and modus ponens then gives $S$. (If $S$ were false, the hypothesis $\lnot S$ would be true and the conclusion $Q \land \lnot Q$ false, so $\lnot S \rightarrow (Q \land \lnot Q)$ would be false.)

    /// important | 📐 **Theorem**
        attrs: {class: no-icon}
    There is no smallest positive real number: $\lnot\, \exists \varepsilon > 0\;\, \forall \delta > 0\;\, (\varepsilon \le \delta)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Suppose, for contradiction, that some $\varepsilon > 0$ satisfies $\varepsilon \le \delta$ for every $\delta > 0$. Since $\varepsilon > 0$, also $\varepsilon/2 > 0$, so taking $\delta = \varepsilon/2$ gives $\varepsilon \le \varepsilon/2$. Subtracting $\varepsilon/2$ from both sides gives $\varepsilon/2 \le 0$, so $\varepsilon \le 0$, contradicting $\varepsilon > 0$. $\blacksquare$
    ///

    This is why statements about accuracy, like the convergence example above, quantify over *every* tolerance $\varepsilon > 0$: there is no smallest one to check instead.

    ### Proof by Cases

    If $P \lor Q$ is known, and both $P \rightarrow R$ and $Q \rightarrow R$ are proved, then $R$ follows. The justifying tautology is $\big((P \lor Q) \land (P \rightarrow R) \land (Q \rightarrow R)\big) \rightarrow R$. The cases must be *exhaustive*: at least one of them must hold.

    /// important | 📐 **Theorem**
        attrs: {class: no-icon}
    For every real number $x$, $x^2 \ge 0$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Let $x$ be an arbitrary real number. Either $x \ge 0$ or $x < 0$.

    - *Case $x \ge 0$:* a product of two non-negative numbers is non-negative, so $x^2 = x \cdot x \ge 0$.
    - *Case $x < 0$:* then $-x > 0$, and $x^2 = (-x)(-x)$ is a product of two positive numbers, so $x^2 > 0$.

    In both cases $x^2 \ge 0$. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Proving Existence by Example

    To prove $\exists x\, P(x)$, exhibit one object $a$ and verify $P(a)$ (existential generalization).

    /// important | 📐 **Theorem**
        attrs: {class: no-icon}
    There is a natural number $n$ with $n^2 = n + 2$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Take $n = 2$: $n^2 = 4 = 2 + 2 = n + 2$. $\blacksquare$
    ///

    The reverse does not work: checking examples, however many, never proves a universal statement about infinitely many objects. The expression $n^2 + n + 41$ is prime for every $n = 0, 1, \ldots, 39$, yet at $n = 40$ it equals $1681 = 41^2$.

    ### Disproving a Universal Statement by Counterexample

    Since $\lnot \forall x\, P(x) \equiv \exists x\, \lnot P(x)$, a universal statement is disproved by exhibiting one object for which it fails.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Counterexample**</u>

    For a statement $\forall x\, P(x)$, an object $a$ in the domain of discourse such that $P(a)$ is false. (For a bounded statement $\forallin{x}{A} P(x)$, the object must also satisfy $a \in A$.)
    ///

    /// important | 📐 **Theorem**
        attrs: {class: no-icon}
    The statement "for all real numbers $a$ and $b$, $(a + b)^2 = a^2 + b^2$" is false.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    The pair $a = b = 1$ is a counterexample: $(1 + 1)^2 = 4$, but $1^2 + 1^2 = 2$. $\blacksquare$
    ///

    The value $n = 40$ above is a counterexample to "$n^2 + n + 41$ is prime for every natural number $n$".

    ### Proving a Biconditional in Two Directions

    Since $P \leftrightarrow Q \equiv (P \rightarrow Q) \land (Q \rightarrow P)$, prove each conditional separately. The two halves are labeled $(\Rightarrow)$ for $P \rightarrow Q$ and $(\Leftarrow)$ for $Q \rightarrow P$.

    /// important | 📐 **Theorem**
        attrs: {class: no-icon}
    For every integer $n$: $n$ is even iff $n + 1$ is odd.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Let $n$ be an arbitrary integer.

    - $(\Rightarrow)$ If $n$ is even, then $n = 2m$ for some integer $m$, so $n + 1 = 2m + 1$ is odd.
    - $(\Leftarrow)$ If $n + 1$ is odd, then $n + 1 = 2m + 1$ for some integer $m$, so $n = 2m$ is even. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A Filtering Proof

    The [Introduction](introduction.md) claimed that the update $\hat x_k = \hat x_{k-1} + \alpha(z_k - \hat x_{k-1})$ always chooses a value between the previous estimate $\hat x_{k-1}$ and the new measurement $z_k$. We can now state this precisely and prove it. For real numbers $a$ and $b$, let $\min(a, b)$ be $a$ if $a \le b$ and $b$ otherwise, and let $\max(a, b)$ be $b$ if $a \le b$ and $a$ otherwise. "$u$ lies between $a$ and $b$" means $\min(a, b) \le u \le \max(a, b)$.

    /// important | 📐 **Theorem (The Update Lies Between)**
        attrs: {class: no-icon}
    Let $\alpha$ be a real number with $0 \le \alpha \le 1$. For all real numbers $a$ and $z$, the number $u := a + \alpha(z - a)$ lies between $a$ and $z$.

    In particular, with $a = \hat x_{k-1}$ and $z = z_k$, the estimate $\hat x_k$ lies between $\hat x_{k-1}$ and $z_k$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Let $a$ and $z$ be arbitrary real numbers, and write $m := \min(a, z)$ and $M := \max(a, z)$. Then $m \le a \le M$ and $m \le z \le M$. (By cases: if $a \le z$, then $m = a$ and $M = z$; otherwise $z < a$, $m = z$, and $M = a$.)

    Rearranging, $u = (1 - \alpha)\,a + \alpha\, z$. Both weights are non-negative: $1 - \alpha \ge 0$ because $\alpha \le 1$, and $\alpha \ge 0$. Multiplying an inequality by a non-negative number preserves it, so $(1 - \alpha)\,a \ge (1 - \alpha)\,m$ and $\alpha z \ge \alpha m$. Adding these,

    $$u \ge (1 - \alpha)\,m + \alpha\, m = m.$$

    The same argument with $a \le M$ and $z \le M$ gives $u \le (1 - \alpha)M + \alpha M = M$. Hence $m \le u \le M$. $\blacksquare$
    ///

    The proof never used what $a$ means, so it applies equally to the alpha filter of the Introduction, which uses the prediction $\hat x_k^-$ in place of $\hat x_{k-1}$.

    /// important | 📐 **Corollary**
        attrs: {class: no-icon}
    If $0 \le \alpha \le 1$, the alpha-filter estimate $\hat x_k = \hat x_k^- + \alpha(z_k - \hat x_k^-)$ lies between the prediction $\hat x_k^-$ and the measurement $z_k$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Apply the theorem with $a = \hat x_k^-$ and $z = z_k$. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The theorem says $0 \le \alpha \le 1$ is *sufficient* for the update to stay between its inputs. It is also *necessary*:

    /// important | 📐 **Theorem (The Condition Is Necessary)**
        attrs: {class: no-icon}
    Let $\alpha$ be a real number. If $a + \alpha(z - a)$ lies between $a$ and $z$ for all real numbers $a$ and $z$, then $0 \le \alpha \le 1$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    We prove the contrapositive. Assume $\lnot(0 \le \alpha \le 1)$, which by De Morgan's law means $\alpha < 0$ or $\alpha > 1$. We exhibit a counterexample to the universal statement: take $a = 0$ and $z = 1$, so that $a + \alpha(z - a) = \alpha$, $\min(a, z) = 0$, and $\max(a, z) = 1$.

    - *Case $\alpha < 0$:* the update $\alpha$ is less than $0$, so it is not between $0$ and $1$.
    - *Case $\alpha > 1$:* the update $\alpha$ is greater than $1$, so it is not between $0$ and $1$.

    In both cases, the pair $(0, 1)$ is a counterexample, so the universal statement is false. $\blacksquare$
    ///

    Together the two theorems say: the update lies between its inputs for all inputs **iff** $0 \le \alpha \le 1$. The proofs used direct proof, cases, the contrapositive, and a counterexample.

    /// caution | ⚠️ **Assumptions and Failure Modes**
        attrs: {class: no-icon}
    - **$0 \le \alpha \le 1$.** This is necessary, not just convenient. With $\alpha > 1$ the estimate overshoots past the measurement; with $\alpha < 0$ it moves away from the measurement.
    - **"Between" is not "accurate".** The theorems say nothing about the true value $x_k$. If $z_k$ is an outlier, $\hat x_k$ is pulled a fraction $\alpha$ of the way toward it. How close estimates are to the truth is a question about noise, answered with probability in [Chapter 6](ch6_expectation_and_variance.md) and [Chapter 7](ch7_optimal_alpha.md).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - A {term}`statement` is either true or false. The connectives $\lnot, \land, \lor, \rightarrow, \leftrightarrow$ build compound statements whose truth values are given by {term}`truth tables <truth table>`. A conditional with a false hypothesis is vacuously true.
    - $P \rightarrow Q$ says $P$ is a {term}`sufficient condition` for $Q$ and $Q$ is a {term}`necessary condition` for $P$. A definition gives a condition that is both, so it is a biconditional.
    - {term}`Tautologies <tautology>` are true by form alone. {term}`Logically equivalent` forms can replace each other; the contrapositive is equivalent to the original conditional, but the converse is not.
    - A {term}`predicate` becomes a statement when its variables get values, or when they are bound by {term}`quantifiers <quantifier>`. Quantifier order matters, and negation flips each quantifier.
    - $:=$ names objects and $:\Longleftrightarrow$ names properties.
    - A {term}`proof` derives a {term}`theorem` from {term}`axioms <axiom>` by valid rules of inference. The techniques are direct proof, contrapositive, contradiction, cases, existence by example, disproof by {term}`counterexample`, and proving both directions of a biconditional.
    - The update $\hat x_{k-1} + \alpha(z_k - \hat x_{k-1})$ lies between $\hat x_{k-1}$ and $z_k$ for all inputs iff $0 \le \alpha \le 1$.

    ## What's Next

    We can now read and write precise statements, but we have nothing to make statements *about*. [Chapter 2](ch2_axioms_of_set_theory.md) supplies the objects: it states the axioms of ZFC set theory, uses unique existence to define the basic set operations, and builds the natural numbers, where proof by induction and definition by recursion (the logic behind every recursive filter) live.
    """)
    return


if __name__ == "__main__":
    app.run()
