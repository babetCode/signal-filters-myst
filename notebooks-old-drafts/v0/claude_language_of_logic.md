Developing precise language is vital for communicating a precise understanding of any topic. As we introduce new language over the coming chapters, it is important to keep in mind that we will be switching back and forth between three different layers of language:

- **Metalanguage:** This is plain language we use to talk *about* the formal mathematical language we are developing. For example, most of the writing between the lines of math in this book is plain English, and not rigorously defined. While we try our best to be articulate and specific, metalanguage is not formal.
- **Syntax:** This refers to the raw symbols (or strings of symbols) we use in our formal mathematical language, *before* any meaning is interpreted. So far in this book, our syntax has consisted of the roman alphabet, greek alphabet, numbers, algebraic symbols, and some combinations of letters with symbols (such as "$\hat x _k^-$"). However, we are about to introduce some new symbols.
- **Semantics:** This is the list of rules and conventions which dictate how the symbols (or strings of symbols) in our syntax are interpreted. For example, the convention in this book is to interpret "$\hat x _k^-$" as "the prediction at time $k$ prior to the measurement at time $k$".

# Syntax

In this section we describe the symbols of our formal language and the rules for combining them into formulas. At this stage they are only symbols. We say what they mean in the Semantics section below.

## Symbols

The symbols of our formal language are:

- **Variables:** $x, y, z, \ldots$ We assume we have as many variables as we need, using subscripts ($x_1, x_2, \ldots$) if we run out of letters.
- **Relation symbols:** $\in$ (read "is in") and $=$ (read "equals").
- **Negation:** $\neg$ (read "not").
- **Conjunction:** $\land$ (read "and").
- **Existential quantifier:** $\exists$ (read "there exists").
- **Parentheses:** $($ and $)$.

Other symbols familiar from logic, such as $\lor$, $\rightarrow$, $\leftrightarrow$, and $\forall$, are not on this list. We introduce them below as abbreviations.

## Formulas

A *formula* is a finite string of the symbols above, built according to the following recursive rules. (The letters $\varphi$ and $\psi$ are metalanguage placeholders for arbitrary formulas, and $u$, $v$, and $x$ are metalanguage placeholders for arbitrary variables. They are not themselves symbols of the formal language.)

1. **Atomic:** If $u$ and $v$ are variables (not necessarily distinct), then $u \in v$ and $u = v$ are formulas.
2. **Negation:** If $\varphi$ is a formula, so is $\neg \varphi$.
3. **Conjunction:** If $\varphi$ and $\psi$ are formulas, so is $(\varphi \land \psi)$.
4. **Quantifier:** If $\varphi$ is a formula and $x$ is a variable, then $\exists x\,\varphi$ is a formula.
5. **Closure:** Nothing else is a formula.

For example, $\exists x\,(x \in y \land \neg\, x = y)$ is a formula. It is built in stages: first the atomic formulas $x \in y$ and $x = y$, then $\neg\, x = y$, then the conjunction $(x \in y \land \neg\, x = y)$, and finally the quantified formula.

## Abbreviations

### The Symbol $:=$

When we want to introduce a new notation as shorthand for something we've already written, we write

$$\text{new notation} := \text{old notation}$$

to mean "the left side is defined to stand for the right side." Unlike "$=$", the symbol "$:=$" is not part of our formal language. It belongs to the metalanguage and simply tells the reader that we are introducing shorthand. Anything written using such shorthand can, in principle, be rewritten without it by unpacking the definition.

Later we will also use "$:=$" to give names to particular sets. A name for a set is not itself a formula, but any formula containing the name can again be rewritten without it. We will say how when we first do this.

### Derived Connectives and $\forall$

We use this notation to introduce the remaining connectives and the universal quantifier:

| Notation | Abbreviates |
| :--- | :--- |
| $(\varphi \lor \psi)$ | $\neg(\neg\varphi \land \neg\psi)$ |
| $(\varphi \rightarrow \psi)$ | $(\neg\varphi \lor \psi)$ |
| $(\varphi \leftrightarrow \psi)$ | $((\varphi \rightarrow \psi) \land (\psi \rightarrow \varphi))$ |
| $\forall x\, \varphi$ | $\neg\exists x\, \neg\varphi$ |

Since these are abbreviations for formulas, they may be used anywhere a formula is allowed. In practice we also omit outer parentheses, and sometimes use square brackets in place of parentheses to make long formulas easier to read.

## Free and Bound Variables

Each occurrence of a variable in a formula is either *free* or *bound*, according to the following recursive rules:

- In an atomic formula $u \in v$ or $u = v$, every occurrence of a variable is free.
- The free occurrences in $\neg\varphi$ are those in $\varphi$.
- The free occurrences in $(\varphi \land \psi)$ are those in $\varphi$ together with those in $\psi$.
- In $\exists x\, \varphi$, the $x$ right after $\exists$ is bound, every occurrence of $x$ in $\varphi$ is bound, and every occurrence of another variable is free exactly when it is free in $\varphi$.

A bound occurrence acts as a placeholder for the collection of objects being quantified over, rather than a value which we can freely assign. A variable is a *free variable* of a formula if at least one of its occurrences is free. Note that a variable can be both free and bound in the same formula. In

$$(x = y) \land \exists x\,(x \in y),$$

the first $x$ is free and the second is bound, while $y$ is free in both places. The free variables of this formula are $x$ and $y$.

When we want to specify the free variables of some unspecified formula $\varphi$, we write

$$\varphi(p_1,\ldots,p_n)$$

to indicate that the free variables of $\varphi$ are among $p_1,\ldots,p_n$. We might not know how many $p_i$ there are, or even if the $p_i$ necessarily occur as free variables in $\varphi$, but this notation ensures that if a variable is not one of $p_1,\ldots,p_n$, then it does not occur as a free variable in $\varphi(p_1,\ldots,p_n)$.

### Formula Substitution

We use the notation

$$\varphi[x/y]$$

to reference the result of replacing every *free* occurrence of $x$ in $\varphi$ by $y$. We only use this when $y$ is a variable that does not occur in $\varphi$ at all (whether free or bound), so there are no capture issues.

## Sentences

A *sentence* is a formula with no free variables. Equivalently, every occurrence of every variable in it is bound by a quantifier. We say what it means for a sentence to be true in the Semantics section.

# Semantics

So far we have only manipulated symbols. In this section we say what the symbols mean.

## Structures and the Domain of Discourse

To say what a formula means, we must say what the variables stand for and what the symbol $\in$ expresses. A *structure* consists of:

- a collection of objects, called the *domain of discourse*, which the variables stand for, and
- a specification of which objects in the domain are members of which other objects.

In other words, a structure is an interpretation of the symbols. In set theory, the only kind of object we talk about is a set, so every variable stands for a set. Our intended structure is the collection of all sets, with $\in$ meaning ordinary set membership.

Formulas are not in the domain of discourse. They are strings of symbols that we describe using the metalanguage, rather than values a variable can take. So the placeholders $\varphi$ and $\psi$ stand for formulas, and they are different in kind from variables like $x$ and $y$, which stand for sets. A quantifier such as $\exists$ refers to the objects in the domain: it makes a claim about the sets, not about formulas.

## Meaning of $=$ and $\in$

The equality symbol (aka equals sign) is placed between two variables, such as:

$$x = y$$

and expresses that $x$ and $y$ stand for the same set.

The membership symbol is placed between two variables, such as:

$$x \in y$$

and expresses that the set $x$ is an element of the set $y$.

The membership symbol is specific to set theory. A "set" is an object in math which can be roughly thought of as "any unordered collection of unique objects." The objects in the collection are called the set's "members" or "elements". However, no precise definition of "set" exists, because sets are a "primitive concept", meaning they are a foundational block on which other concepts are defined (a [bottom turtle](https://en.wikipedia.org/wiki/Turtles_all_the_way_down), so to speak, since we cannot have an infinite regress of definitions). As such, sets are only described by how the [Set Theory axioms](https://en.wikipedia.org/wiki/Zermelo%E2%80%93Fraenkel_set_theory) allow them to behave. More on that in the next section.

## Truth

Fix a structure, and suppose each variable has been assigned an object from the domain, that is, a set. Then every formula is either true or false, according to the following clauses, one for each rule for building formulas:

1. $u \in v$ is true iff the set assigned to $u$ is a member of the set assigned to $v$.
2. $u = v$ is true iff $u$ and $v$ are assigned the same set.
3. $\neg\varphi$ is true iff $\varphi$ is not true.
4. $(\varphi \land \psi)$ is true iff both $\varphi$ and $\psi$ are true.
5. $\exists x\,\varphi$ is true iff $\varphi$ is true for at least one choice of set for $x$, keeping the sets assigned to all other variables the same.

Only the sets assigned to the free variables of a formula affect whether it is true. In particular, a sentence needs no assignment at all: it is simply true or false in a given structure.

### Truth Tables

The clauses for $\neg$ and $\land$ depend only on whether the parts are true or false, so they can be displayed as truth tables. Writing $\mathbf{T}$ for "true" and $\mathbf{F}$ for "false":

**Negation.** $\neg\varphi$ has the opposite truth value from $\varphi$.

$$\begin{array}{r | c}
\neg & \\
\hline
\mathbf{T} & \text{F} \\
\mathbf{F} & \text{T} \\
\end{array}$$

**Conjunction.** $(\varphi \land \psi)$ is true iff $\varphi$ and $\psi$ are both true.

$$\begin{array}{r | cc}
\land & \mathbf{T} & \mathbf{F} \\
\hline
\mathbf{T} & \text{T} & \text{F} \\
\mathbf{F} & \text{F} & \text{F} \\
\end{array}$$

## Derived Connectives and $\forall$

The abbreviations introduced in the Syntax section get their meanings from the clauses above. We work them out one at a time.

### Disjunction

$(\varphi \lor \psi)$ abbreviates $\neg(\neg\varphi \land \neg\psi)$. By the clauses for $\neg$ and $\land$, this is false iff $\neg\varphi$ and $\neg\psi$ are both true, which happens iff $\varphi$ and $\psi$ are both false[^de-morgan].

$$\begin{array}{r | cc}
\lor & \mathbf{T} & \mathbf{F} \\
\hline
\mathbf{T} & \text{T} & \text{T} \\
\mathbf{F} & \text{T} & \text{F} \\
\end{array}$$

[^de-morgan]: Similarly, had we taken $\lor$ as primitive, then $\land$ could be defined as an abbreviation, where $(\varphi \land \psi)$ would be shorthand for $\neg(\neg\varphi \lor \neg\psi)$. This ability to express conjunction and disjunction in terms of each other using negation is captured by [De Morgan's laws](https://en.wikipedia.org/wiki/De_Morgan%27s_laws).

### Conditional

$(\varphi \rightarrow \psi)$ abbreviates $(\neg\varphi \lor \psi)$. This is false iff $\neg\varphi$ and $\psi$ are both false, which happens iff $\varphi$ is true and $\psi$ is false. The conditional is read "implies", or "if ... then ...".

$$\begin{array}{r | cc}
\rightarrow & \mathbf{T} & \mathbf{F} \\
\hline
\mathbf{T} & \text{T} & \text{F} \\
\mathbf{F} & \text{T} & \text{T} \\
\end{array}$$

### Biconditional

$(\varphi \leftrightarrow \psi)$ abbreviates $((\varphi \rightarrow \psi) \land (\psi \rightarrow \varphi))$. This is true iff both conditionals are true, which happens iff $\varphi$ and $\psi$ have the same truth value. The biconditional is read "if and only if".

$$\begin{array}{r | cc}
\leftrightarrow & \mathbf{T} & \mathbf{F} \\
\hline
\mathbf{T} & \text{T} & \text{F} \\
\mathbf{F} & \text{F} & \text{T} \\
\end{array}$$

### Universal Quantifier

$\forall x\,\varphi$ abbreviates $\neg\exists x\,\neg\varphi$. This is true iff it is not the case that some choice of set for $x$ makes $\neg\varphi$ true, which happens iff $\varphi$ is true for every choice of set for $x$. The universal quantifier is read "for all".

## Sentences and Axioms

While a formula with free variables doesn't have a truth value until we assign values to its free variables, a sentence is simply true or false in a given structure. We take certain sentences as starting points and agree to treat them as true of the sets we are talking about. We call these starting point sentences **axioms**. Everything else we prove will follow from them.

# Useful Notation

Before we move on to building the foundational axioms of mathematics, here are a few more abbreviations that will make our writing easier. As with the abbreviations above, anything written using them can, in principle, be rewritten using only the symbols of our formal language.

| Notation $:=$ Definition | Read as |
| :--- | :--- |
| $x \notin y := \neg(x \in y)$ | "$x$ is **not in** $y$" |
| $x \subseteq y := \forall z(z \in x \rightarrow z \in y)$ | "$x$ is a **subset** of $y$" |
| $\exists! x\, \varphi := \exists x\, (\varphi \land \forall y\, (\varphi[x/y] \leftrightarrow y = x))$ | "There **exists unique** $x$ such that $\varphi$" |
| $\existsin{x}{y} \varphi := \exists x\, (x \in y \land \varphi)$ | "There **exists** $x$ **in** $y$ such that $\varphi$" |
| $\forallin{x}{y} \varphi := \forall x\, (x \in y \rightarrow \varphi)$ | "**For all** $x$ **in** $y$, $\varphi$" |
| $\existssubseteq{x}{y} \varphi := \exists x\, (x \subseteq y \land \varphi)$ | "There **exists** $x$ which is a **subset** of $y$ such that $\varphi$" |
| $\forallsubseteq{x}{y} \varphi := \forall x\, (x \subseteq y \rightarrow \varphi)$ | "**For all** $x$ which are **subsets** of $y$, $\varphi$" |

In each entry, the variables $x$, $y$ (and $z$, in the entry for $\subseteq$) are distinct from one another. In the entry for $\exists!$, the variable $y$ must also not occur in $\varphi$, so that the substitution $\varphi[x/y]$ is allowed.