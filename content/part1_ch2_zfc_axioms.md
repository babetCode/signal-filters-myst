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
:hide-code: true
:name: imports
:include: false

import marimo as mo
from textwrap import dedent
```

```{marimo} python
:hide-code: true
:name: display_format
:include: false

mo.latex(dedent(
    r"""\newcommand{\existsin}[2]{\exists #1 \!\!\in\!\! #2\,}
    \newcommand{\forallin}[2]{\forall #1 \!\!\in\!\! #2\,}
    \newcommand{\existssubseteq}[2]{\exists #1 \!\!\subseteq\!\! #2\,}
    \newcommand{\forallsubseteq}[2]{\forall #1 \!\!\subseteq\!\! #2\,}"""
))
mo.output.clear()
```

The goal of this chapter is to define the axioms of set theory and and the notational shorthands they permit (which well be neccesary for defining probability spaces in the next chapter).

Set theory is a foundation for nearly all of mathematics, including number theory, functions, topology, algebra, and probability[^other-math-foundations]. Set theory rests on axioms. We use the Zermelo-Frankel axioms along with the axiom of choice, by convention.

There are many equivalent ways to formulate the ZFC {term}`axioms <axiom>`. We include all 10 for the purpose of explanation. However, the axiom of the null det is often omitted since it is easily proven by applying the axiom schema of separation to filter out elements which are equal to themselves. Additionally, the axiom schema of separation is sometimes omitted since it can be proven using the axiom schema of replacement.

[^other-math-foundations]: This is because almost every mathematical object can be defined inside set theory, and almost every theorem can be derived from its axioms. However, alternative foundational theories also exist, such as [Category Theory](https://en.wikipedia.org/wiki/Category_theory), which is common in geometry, and [Type Theory](https://en.wikipedia.org/wiki/Type_theory), which is used in theoretical computer science, as well as the theorem prover programming languages [Lean](https://lean-lang.org) and [Rocq](https://rocq-prover.org).
  
## Axiom of Extensionality

If two sets contain the exact same members, then they are equal:

$$\forall x\forall y\,[\forall z\,(z\in x\leftrightarrow z\in y)\rightarrow x=y].$$

This axiom supplies uniqueness: if we can show that all sets satisfying some property contain exactly the same members, then by extensionality we know there exists a unique set which satisfies the property.
  
## Axiom of the Null Set

There exists a set $x$ such that for all $y$, $y$ is not an element of $x$:

$$\exists x \forall y (y \notin x).$$

By extensionality, there exists a unique $x$ which satisfies this. We call that set the "null set", "empty set", or just use the symbol "$\emptyset$". This is our first example of a *defined term*.
  
### Defined Terms

In our formal language, the only way to refer to a set is with a variable. However, we are about to write things like $\emptyset \in I$, which are not formulas as defined in the previous chapter. Therefore, we must explain why such notation is legitimate shorthand.

A *term* is notation that names a set (as opposed to a formula, which makes a claim that is true or false). So far the only terms are variables. We add new terms one *operation* at a time, each justified by a proof that the operation always produces exactly one set.
  
#### Operations

Let $\delta(x_1, \dots, x_n, y)$ be a formula. If we have proven

$$\forall x_1 \cdots \forall x_n\, \exists! y\, \delta(x_1, \dots, x_n, y),$$

then we may introduce a new notation $F(x_1, \dots, x_n)$, called an *operation*, which stands for "the unique $y$ such that $\delta(x_1, \dots, x_n, y)$." We call $\delta$ the *defining formula* of $F$. When $n = 0$ (such as with $\emptyset$), this is simply a name for one particular set.

Just as the axiom of the null set introduces $\emptyset$, each axiom below that asserts the existence of a set introduces its own operation (with extensionality supplying uniqueness of the asserted set):

- Pairing introduces $\{x, y\}$ and $\{x\}$.
- Power introduces $\mathcal{P}(x)$.
- Union introduces $\bigcup X$.
- Separation introduces $\{x \in A: \varphi\}$.
- Replacement introduces $\{y: \existsin x A\, \varphi\}$.

*Note:* Infinity and choice also assert the existence of sets, but not of a unique set, so they introduce no operations.
  
$\{y: \existsin x A\, \varphi\}$
  
#### Terms and Unpacking

*Terms* are built by the following recursive rules:

1. **Variable:** Every variable is a term.
2. **Operation:** If $F$ is an operation with $n$ arguments and $t_1, \dots, t_n$ are terms, then $F(t_1, \dots, t_n)$ is a term.
3. **Closure:** Nothing else is a term.

Since every variable term represents a set, and every operation term is a shorthand for the unique set which satisfies its defining formula, then every term names a single set. This fact is what justifies using $:=$ for sets.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Term
: A variable or an operation applied to a term, which represents a set.
:::
::::
  
We allow terms on either side of $\in$ and $=$, but a string like $\emptyset \in I$ is then not literally a formula of the formal language. It is shorthand for one, obtained by *unpacking*: if an atomic formula $\alpha$ contains $F(v_1, \dots, v_n)$ where each $v_i$ is a variable, then $\alpha$ abbreviates

$$\exists z\,\big(\delta_F(v_1, \dots, v_n, z) \land \alpha'\big),$$

where $z$ is a variable not occurring in $\alpha$, and $\alpha'$ is $\alpha$ with that occurrence of $F(v_1, \dots, v_n)$ replaced by $z$ (renaming bound variables of $\delta_F$ if necessary to avoid clashes). Repeating this, innermost operation first, removes every operation. For example, $\emptyset \in I$ abbreviates $\exists z\,(\forall w\,(w \notin z) \land z \in I)$. When $\alpha$ is $y = F(v_1, \dots, v_n)$ for a variable $y$, the result is equivalent to the simpler $\delta_F(v_1, \dots, v_n, y)$, and we use that instead. Because unique existence has been proven, it would make no difference to use $\forall z\,(\delta_F \rightarrow \alpha')$ in place of the $\exists$ form. So, as with our other abbreviations, anything written with terms can be rewritten without them[^definitional-extension].

[^definitional-extension]: In logic this device is called an *extension by definitions*. It is *conservative*: anything expressible without the new notation that can be proven with it can also be proven without it. So the notation adds convenience but no new content.
  
#### Provisos

Some notation names a set only under a condition. Function application is the main example: $f(a)$ names a set only when $f$ is a function and $a$ is a first coordinate of some element of $f$ (this is covered in the Axiom of Pairing section). The Replacement set-builder notation below is another, where the condition is the hypothesis of the schema. For such notation we give a *proviso* $D(x_1, \dots, x_n)$ and prove only $\forall x_1 \cdots \forall x_n\,(D \rightarrow \exists! y\, \delta)$. Unpacking then adds $D$ as an extra conjunct (so every atomic formula still unpacks to an honest formula), and we follow the convention of using the notation only where its proviso is known to hold. For terms using such notation, our guarantee that "every term names a single set" only holds at values of the variables where the provisos hold.
  
## Axiom of Pairing

For any two sets $x$ and $y$, there exists a set $z$ that contains $x$ and $y$ as its only members:

$$\forall x \, \forall y \, \exists z \, \forall w \, (w \in z \leftrightarrow w = x \lor w = y).$$

By extensionality, this set $z$ is unique and may be referred to as the pairing set $\{x, y\}$.
  
### Singleton Sets

By letting $y=x$, the Axiom of Pairing tells us that

$$\forall x\, \exists z\, \forall w\, (w \in z \leftrightarrow w = x).$$

This set $z$ is called a singleton set because it contains exactly one element, and is denoted $\{x\}$.
  
### Ordered Pairs

Given two sets $a$ and $b$, the axiom of pairing guarantees the existence of the singleton $\{a\}$ and the pairing set $\{a, b\}$. Paring again guarantees the existence of $\{\{a\},\{a,b\}\}$. We call this the "ordered pair" of $a$ and $b$ and use the shorthand

$$(a, b) := \{\{a\},\{a,b\}\},$$

where $a$ and $b$ are called the "coordinates".

By extensionality, two ordered pairs are equal iff their corresponding coordinates are equal:

$$(a, b) = (c, d) \leftrightarrow a = c \land b = d.$$
  
### Functions

A set $f$ is a function iff:

- Every element of $f$ is an ordered pair:
  $$\forallin x f \, \exists a\, \exists b\, [x = (a, b)]$$
- Each first coordinate has at most one partner:
  $$\forall a\, \forall b\, \forall c\; ([(a, b) \in f \land (a, c) \in f] \rightarrow b = c)$$

If $f$ is a function and $(a, b) \in f$, then we write $f(a) = b$.
  
## Axiom of Union

For any set of sets $X$, there exists a set $U$ whose elements are precisely the elements that belong to at least one of the sets contained in $X$:

$$\forall X\,\exists U\,\forall y\, [y\in U\leftrightarrow \existsin z X (y\in z)].$$

By Extensionality, this union set $U$ is unique. It is sometimes denoted as $\bigcup X$ or $\bigcup_{w \in X} w$.
  
### Union Operator

The union operator is denoted $\cup$. When placed between two sets $x$ and $y$, it is a shorthand to reference the union of the set containing $x$ and $y$ (whose existence is guaranteed by pairing):

$$x \cup y := \bigcup \{x, y\}.$$

Since the pairing set is unordered, this operation is commutative and we have

$$x \cup y = y \cup x.$$
  
## Axiom Schema of Separation

For every formula $\varphi(x, A, p_1, \dots, p_n)$ where $A, p_1, \dots, p_n$ are sets, the following is an axiom:

For any sets $A, p_1, \dots, p_n$, there exists a set $B$ distinct from $x, A, p_1, \dots, p_n$ (so $B$ is not free in $\varphi$) whose elements are exactly those elements $x$ of $A$ that satisfy $\varphi$:

$$\forall p_1 \cdots \forall p_n\, \forall A\, \exists B\, \forall x\, [x \in B \leftrightarrow (x \in A \land \varphi)].$$

In other words, every property definable by a formula carves out a subset of any given set. This is called an axiom schema, rather than a single axiom, because we want Separation to hold for all formulas $\varphi$, so we make an axiom for every $\varphi$.
  
### Separation Set-Builder Notation

We use the following notation to refer to a set whose existence is guaranteed by the axiom schema of separation:

$$\{x \in A: \varphi\}.$$

By extensionality, this set is unique.
  
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
  
Additionally, we can take the intersection of a set of sets. Similar to the union, if a set $A$ contains $a_1, a_2, \ldots, a_n$, then we have:

$$\bigcap A := \{x \in a_1: x \in a_2 \land \cdots \land x \in a_n\}.$$
  
## Axiom Schema of Replacement

For every formula $\varphi(x, y, A, p_1, \dots, p_n)$ where $A, p_1, \dots, p_n$ are sets, the following is an axiom:

For any sets $A, p_1, \dots, p_n$, if for every $x \in A$ there is exactly one $y$ satisfying $\varphi$, then there exists a set $B$ distinct from $x, y, A, p_1, \dots, p_n$ (so $B$ is not free in $\varphi$) whose elements are exactly those $y$ such that $\varphi$ holds for some $x \in A$:

$$\forall p_1 \cdots \forall p_n\, \forall A\,[\forallin x A\, \exists! y\, \varphi \rightarrow \exists B\, \forall y\, (y \in B \leftrightarrow \existsin x A\, \varphi)].$$

In other words, if a formula $\varphi$ assigns to each $x \in A$ exactly one $y$, then the collection of all outputs is also a set. Like Separation, this is a schema because we want it to hold for every formula $\varphi$.
  
### Replacement Set-Builder Notation

We use the following notation to refer to a set whose existence is guaranteed by the axiom schema of replacement:

$$\{y: \existsin x A\, \varphi\}.$$

This is only meaningful when the hypothesis of the schema holds, namely $\forallin x A\, \exists! y\, \varphi$. By extensionality, this set is unique.

Where Separation notation selects elements *of* $A$, this notation collects *outputs*: $y$ is in the set iff $\varphi$ relates it to some $x \in A$. The elements of the resulting set need not be elements of $A$, and different $x$'s may share the same $y$, so the new set can be smaller than $A$.

Most often, $\varphi$ simply says that $y = t$ for some expression $t$ built from $x$ using notations we have already introduced, such as $\{x\}$, $(x, c)$, or $x \cup \{x\}$. We then write

$$\{t: x \in A\} := \{y: \existsin x A\, (y = t)\},$$

where $y$ is a variable that does not occur in $t$. Because each of these expressions exists and is unique for every $x$, the hypothesis $\forallin x A\, \exists! y\, (y = t)$ holds automatically.

For example, if $A = \{\emptyset, \{\emptyset\}\}$, then

$$\{\{x\}: x \in A\} = \{\{\emptyset\}, \{\{\emptyset\}\}\}.$$
  
### Combining Set-Builder Notations

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
  
## Axiom of Infinity

At least one infinite set $I$ exists. The empty set $\emptyset$ is an element of $I$, and whenever a set $x$ is an element of $I$, so is $x \cup \{x\}$:

$$\exists I\, [\emptyset \in I \land \forall x\, (x \in I \rightarrow x \cup \{x\} \in I)].$$

We call a set $I$ *inductive* if it satisfies the formula $[\emptyset \in I \land \forall x\, (x \in I \rightarrow x \cup \{x\} \in I)]$. The axiom of infinity guarantees that at least one such set exists.
  
### Natural Numbers

For convenience, we introduce the notation:

$$\text{inductive}(I) := \emptyset \in I \land \forall x\, (x \in I \rightarrow x \cup \{x\} \in I).$$

Let $J$ be an inductive set (so that it satisfies $\text{inductive}(J)$). We define the natural numbers as:

$$\mathbb N := \{x \in J: \forall I(\text{inductive}(I) \rightarrow x \in I)\}.$$
  
## Axiom of Power Set

For any set $x$, there exists a set $y$ containing precisely all the subsets of $x$:

$$\forall x\,\exists y\,\forall z\, (z\in y \leftrightarrow z \subseteq x).$$

This set $y$ is known as the power set of $x$ and is denoted $\mathcal{P}(x)$. By Extensionality, it is unique.
  
## Axiom of Regularity

Every nonempty set $A$ has a member $x$ that shares no members with $A$:

$$\forall A\,[\exists x\,(x \in A) \rightarrow \existsin x A\, \neg\exists z\,(z \in x \land z \in A)].$$

Using the abbreviations above, the last part says $x \cap A = \emptyset$. This is also called the Axiom of Foundation. It rules out sets that are “circular” in their membership. This has two consequences:

1. No set is a member of itself. If $A \in A$, then the singleton $\{A\}$ is nonempty, so by Regularity it has a member disjoint from it. The only member is $A$, so $A \cap \{A\} = \emptyset$. But $A \in A$ and $A \in \{A\}$, so $A$ is in both, a contradiction.
2. There are no infinite descending chains $\cdots \in x_3 \in x_2 \in x_1 \in x_0$.
  
## Axiom of Choice

For any set $X$ whose members are nonempty, pairwise disjoint sets, there exists a set $C$ that contains exactly one element from each member of $X$:

$$\forall X\,\big[\big(\forall A \in X\,\exists y\,(y \in A) \;\land\; \forall A \in X\,\forall B \in X\,(\neg(A = B) \rightarrow \neg\exists z\,(z \in A \land z \in B))\big) \rightarrow \exists C\,\forall A \in X\,\exists! z\,(z \in A \land z \in C)\big].$$

The set $C$ is called a choice set or selector for $X$. Unlike the other axioms, Choice asserts that a set exists without giving any rule for constructing it. Informally, it lets us make infinitely many arbitrary selections at once. It is equivalent to several other well-known statements, such as the Well-Ordering Theorem, Zorn’s Lemma, and “every product of nonempty sets is nonempty.”

Note: The version above (disjoint sets) is one of many equivalent formulations. Another common one says that for every collection of nonempty sets there exists a function that picks an element from each. Once we define functions in terms of sets, this is easy to state, but the disjoint-sets form can be written directly in the language of $\in$ and $=$.