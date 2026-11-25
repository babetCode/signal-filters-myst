---
title: 3. Sets for Probability
# marimo-version: 0.25.1
# css_file: notebook-styles.css
subtitle: "Complements, Preimages, and Infinity"
abbreviations:
  iff: if and only if
  diff: null
numbering:
  equations: false
math:
  '\existsin': '\exists #1 \!\!\in\!\! #2\,'
  '\forallin': '\forall #1 \!\!\in\!\! #2\,'
  '\existssubseteq': '\exists #1 \!\!\subseteq\!\! #2\,'
  '\forallsubseteq': '\forall #1 \!\!\subseteq\!\! #2\,'
---

```{marimo-config}
---
pyproject: |-
  dependencies = [
      "marimo>=0.25.1",
      "matplotlib==3.11.2",
      "numpy==2.5.3",
  ]
---
```

```{marimo} python
:name: imports
:include: false

import marimo as mo
import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction
from textwrap import dedent
```

```{marimo} python
:name: display_settings
:include: false

plt.style.use("default")

def graphic(x):
    return mo.Html(dedent(f'''\
        <div class="graphic">
            {mo.as_html(x)}
        </div>
        '''))
```

```{marimo} python
:name: latex_macros
:include: false

mo.latex(dedent(
    r"""\newcommand{\existsin}[2]{\exists #1 \!\!\in\!\! #2\,}
    \newcommand{\forallin}[2]{\forall #1 \!\!\in\!\! #2\,}
    \newcommand{\existssubseteq}[2]{\exists #1 \!\!\subseteq\!\! #2\,}
    \newcommand{\forallsubseteq}[2]{\forall #1 \!\!\subseteq\!\! #2\,}"""
))
mo.output.clear()
```

:::{seealso icon=false} 🔗 **Prerequisites**
- [Chapter 1](ch1_language_of_logic_v2.md): connectives, quantifiers and their negations, and the proof techniques (contrapositive, contradiction, cases).
- [Chapter 2](ch2_axioms_of_set_theory_v2.md): the axioms of set theory (especially Separation, Replacement, Union, Power Set, Regularity, and Choice), ordered pairs, Cartesian products, functions, the natural numbers, induction, and the Recursion Theorem.
- [Appendix B: Arithmetic on the Natural Numbers](appendix_b_number_systems_v2.md) (optional): proofs of the facts about $+$, $\cdot$, and $<$ on $\mathbb N$ listed below, including well-ordering.
- [Appendix B: The Integers](appendix_b_number_systems_v2.md), [The Rational Numbers](appendix_b_number_systems_v2.md), [The Real Numbers](appendix_b_number_systems_v2.md), and [Uniqueness of the Real Numbers](appendix_b_number_systems_v2.md) (optional): the constructions of $\mathbb Z$, $\mathbb Q$, and $\mathbb R$, whose results this chapter uses.
- **Before [Chapter 4](ch4_probability_spaces_v2.md):** read [Appendix C: Sequences and Limits](appendix_c_calculus_v2.md) and [Appendix C: Series](appendix_c_calculus_v2.md). They are built on the real numbers of this chapter, and Chapter 4 uses their limits.
:::
  
Probability theory assigns numbers to *sets* of outcomes.[^informal-probability] The question "does the scale read above 156 lb?" is not a number. It is the set of all situations in which the reading exceeds 156 lb, and its probability is a number attached to that set. Before [Chapter 4](ch4_probability_spaces_v2.md) can define probability, we need four tools from set theory:

1. **Complements, and unions and intersections of infinitely many sets.** These are "not", "or", and "and" for questions, including questions with infinitely many conditions, such as "every future reading is within 1 lb of the truth".
2. **Preimages.** They translate a condition on a measured number into the set of situations that produce it.
3. **Countable versus uncountable infinity.** Probabilities add up over a *list* of disjoint events, but the possible values of a noisy reading cannot be listed. This mismatch is why Chapter 4 cannot give every set a probability.
4. **The real numbers and the extended real numbers $[0, \infty]$**, where measurements, probabilities, and infinite sums live.

[^informal-probability]: "Probability", "outcome", and "event" are used informally in this chapter. They are defined precisely in [Chapter 4](ch4_probability_spaces_v2.md).
  
:::{attention icon=false} 🗝️ **Key Idea**
Every question about a noisy measurement is a set of outcomes. Set operations are the logic of those questions, and whether a set can be listed (is countable) decides how probabilities can be added up.
:::
  
## Complements and De Morgan's Laws

In probability, every set we care about is a subset of one fixed set: the set $\Omega$ (capital omega) of all possible outcomes. "Not $A$" then means "in $\Omega$ but not in $A$". Chapter 2's {term}`set difference` $\Omega \setminus A$ already expresses this. Because we will use it constantly, it gets a shorter name.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Complement
: Let $\Omega$ be a set, called the *ambient set*, and let $A \subseteq \Omega$. The complement of $A$ (relative to $\Omega$) is
  $$A^c := \Omega \setminus A = \{x \in \Omega : x \notin A\}.$$
:::
::::

The notation $A^c$ hides $\Omega$, so we always say which ambient set is meant. For a die, $\Omega = \{1, 2, 3, 4, 5, 6\}$ and $A = \{2, 4, 6\}$ give $A^c = \{1, 3, 5\}$. With $\Omega = \mathbb N$, the same $A$ has complement $\{0, 1, 3, 5, 7, 8, 9, \ldots\}$. There is no complement without an ambient set, because $\{x : x \notin A\}$ is not a set.[^no-absolute-complement]

[^no-absolute-complement]: If $C = \{x : x \notin A\}$ were a set, then $C \cup A$ would contain every set, contradicting the No Set of All Sets theorem of [Chapter 2](ch2_axioms_of_set_theory_v2.md).
  
:::{important icon=false} 📐 **Lemma (Rules for Complements)**
Let $A, B \subseteq \Omega$, with complements taken relative to $\Omega$. Then:

1. $(A^c)^c = A$;
2. $\Omega^c = \emptyset$ and $\emptyset^c = \Omega$;
3. $A \cap A^c = \emptyset$ and $A \cup A^c = \Omega$;
4. $A \subseteq B$ if and only if $B^c \subseteq A^c$;
5. $A \setminus B = A \cap B^c$.
:::

:::{admonition icon=false} ✍️ **Proof**
Every set in these statements is a subset of $\Omega$. So by Extensionality it suffices to show, for each $x \in \Omega$, that $x$ belongs to the left side if and only if it belongs to the right side.

1. $x \in (A^c)^c \iff \neg(x \in A^c) \iff \neg\neg(x \in A) \iff x \in A$, by double negation.
2. No $x \in \Omega$ satisfies $x \notin \Omega$, and every $x \in \Omega$ satisfies $x \notin \emptyset$.
3. $x \in A \land x \notin A$ is a contradiction, and $x \in A \lor x \notin A$ is a tautology.
4. Since $A \subseteq \Omega$, the statement $A \subseteq B$ says $\forallin{x}{\Omega} (x \in A \rightarrow x \in B)$. This is logically equivalent to its contrapositive $\forallin{x}{\Omega} (x \notin B \rightarrow x \notin A)$, which says $B^c \subseteq A^c$.
5. $x \in A \setminus B \iff (x \in A \land x \notin B) \iff (x \in A \land x \in B^c)$. $\blacksquare$
:::
  
:::{important icon=false} 📐 **Theorem (De Morgan's Laws)**
For $A, B \subseteq \Omega$,
$$(A \cup B)^c = A^c \cap B^c \qquad\text{and}\qquad (A \cap B)^c = A^c \cup B^c.$$
:::

:::{admonition icon=false} ✍️ **Proof**
For $x \in \Omega$,
$$x \in (A \cup B)^c \iff \neg(x \in A \lor x \in B) \iff (x \notin A \land x \notin B) \iff x \in A^c \cap B^c.$$
The middle step is De Morgan's law of logic, $\neg(P \lor Q) \leftrightarrow (\neg P \land \neg Q)$ ([Chapter 1](ch1_language_of_logic_v2.md)). The second law follows in the same way from $\neg(P \land Q) \leftrightarrow (\neg P \lor \neg Q)$. $\blacksquare$
:::

In words: "not ($A$ or $B$)" means "not $A$ and not $B$", and "not both $A$ and $B$" means "not $A$ or not $B$". The same laws hold for infinitely many sets, once we have a way to index them.
  
## Indexed Families and Sequences

The Introduction's measurements $z_1, z_2, \ldots$ are not a set $\{z_1, z_2, \ldots\}$: two measurements can be equal, and their order matters. They are the values of a function of the time step $k$. A function used this way is called an indexed family.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Indexed family
: A {term}`function` $A$ whose {term}`domain` is a set $I$, called the *index set*. The value of $A$ at $i \in I$ is written $A_i$ rather than $A(i)$, and the family is written $(A_i)_{i \in I}$.
:::
::::

Every function is an indexed family. The word only signals the subscript notation, and that we care about the values $A_i$ rather than the set of ordered pairs. Values may repeat: the family $(A_i)_{i \in \{1, 2\}}$ with $A_1 = A_2 = \{0\}$ has two members that happen to be equal, while the set $\{A_1, A_2\} = \{\{0\}\}$ has one element.

We write $\mathbb N^+ := \mathbb N \setminus \{0\} = \{1, 2, 3, \ldots\}$ and, for $n \in \mathbb N$,
$$\{1, \ldots, n\} := \{k \in \mathbb N^+ : k \le n\},$$
so in particular $\{1, \ldots, 0\} = \emptyset$.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Sequence
: An {term}`indexed family` whose index set is $\mathbb N$ or $\mathbb N^+$, written $(x_n)_{n \in \mathbb N}$ or $(x_n)_{n=1}^\infty$. A *finite sequence of length* $n \in \mathbb N$ is an indexed family whose index set is $\{1, \ldots, n\}$, written $(x_k)_{k=1}^n$ or $x_1, \ldots, x_n$.
:::
::::

The measurements $z_1, \ldots, z_k$ form a finite sequence, and a filter that runs forever produces a sequence of estimates $(\hat x_k)_{k=1}^\infty$. Chapter 2's Recursion Theorem is a machine for defining sequences: the filter recursion $\hat x_k = g(k, \hat x_{k-1})$ defines one. Re-indexing by $y_n := x_{n+1}$ turns a sequence indexed by $\mathbb N^+$ into one indexed by $\mathbb N$ and back, so a result proven for one convention holds for the other.
  
:::{tip icon=false} **Facts about $\mathbb N$ used in this chapter**
Chapter 2 defines $+$, $\cdot$, and $<$ on $\mathbb N$ by recursion, and [Appendix B: Arithmetic on the Natural Numbers](appendix_b_number_systems_v2.md) proves their familiar properties. We use the following:

- $+$ and $\cdot$ are associative and commutative, $\cdot$ distributes over $+$, and $n + 0 = n$, $n \cdot 1 = n$, $n \cdot 0 = 0$.
- $<$ is a strict total order: for all $m, n$, exactly one of $m < n$, $m = n$, $n < m$ holds. Moreover $m < n + 1$ if and only if $m \le n$, and $m < n$ implies $m + k < n + k$.
- If $m \le n$, there is exactly one $d \in \mathbb N$ with $m + d = n$; we write $d = n - m$.
- Every $n \neq 0$ is a successor: $n = m + 1$ for some $m \in \mathbb N$.
- **Well-ordering:** every nonempty subset of $\mathbb N$ has a least element.
:::
  
### Unions and Intersections of Families

Given a family of sets $(A_i)_{i \in I}$, Replacement gives the set $\{A_i : i \in I\}$ of its members, and Chapter 2's union and intersection of a set of sets apply to it:
$$\bigcup_{i \in I} A_i := \bigcup \{A_i : i \in I\}, \qquad \bigcap_{i \in I} A_i := \bigcap \{A_i : i \in I\} \quad (I \neq \emptyset).$$
Unpacking the definitions,
$$x \in \bigcup_{i \in I} A_i \iff \existsin{i}{I} (x \in A_i), \qquad x \in \bigcap_{i \in I} A_i \iff \forallin{i}{I} (x \in A_i).$$
The proviso $I \neq \emptyset$ is Chapter 2's proviso for $\bigcap$. If $I = \emptyset$, every set $x$ satisfies "$x \in A_i$ for every $i \in I$" vacuously, and there is no set of all sets. For sequences we write $\bigcup_{n=1}^\infty A_n$ and $\bigcap_{n=1}^\infty A_n$. For finite sequences we write $\bigcup_{k=1}^n A_k = A_1 \cup \cdots \cup A_n$, and $\bigcup_{k=1}^0 A_k = \bigcup \emptyset = \emptyset$.

**Example.** For $n \in \mathbb N^+$ let $A_n := \{m \in \mathbb N : m \ge n\}$. Every $A_n$ is nonempty and $A_1 \supseteq A_2 \supseteq \cdots$, yet
$$\bigcap_{n=1}^\infty A_n = \emptyset,$$
because each $m \in \mathbb N$ fails to be in $A_{m+1}$. Each condition "$m \ge n$" leaves plenty of numbers, but all of them together leave none. Chapter 4 meets this phenomenon again as *continuity of probability*.
  
:::{important icon=false} 📐 **Theorem (De Morgan's Laws for Families)**
Let $(A_i)_{i \in I}$ be a family of subsets of $\Omega$ with $I \neq \emptyset$. Then
$$\Big(\bigcup_{i \in I} A_i\Big)^c = \bigcap_{i \in I} A_i^c \qquad\text{and}\qquad \Big(\bigcap_{i \in I} A_i\Big)^c = \bigcup_{i \in I} A_i^c.$$
:::

:::{admonition icon=false} ✍️ **Proof**
Here $(A_i^c)_{i \in I}$ is the family $i \mapsto \Omega \setminus A_i$, which exists by Replacement. For $x \in \Omega$,
$$x \in \Big(\bigcup_{i \in I} A_i\Big)^c \iff \neg\existsin{i}{I} (x \in A_i) \iff \forallin{i}{I} (x \notin A_i) \iff \forallin{i}{I} (x \in A_i^c) \iff x \in \bigcap_{i \in I} A_i^c,$$
using the rule for negating a quantifier ([Chapter 1](ch1_language_of_logic_v2.md)) and $x \in \Omega$ in the third step. For the second law, apply the first to the family $(A_i^c)_{i \in I}$ and use $(B^c)^c = B$:
$$\Big(\bigcup_{i \in I} A_i^c\Big)^c = \bigcap_{i \in I} (A_i^c)^c = \bigcap_{i \in I} A_i.$$
Taking complements of both sides gives $\bigcup_{i \in I} A_i^c = \big(\bigcap_{i \in I} A_i\big)^c$. $\blacksquare$
:::

The two-set laws are the special case $I = \{1, 2\}$.

:::{important icon=false} 📐 **Lemma (Distributive Laws)**
For a set $B$ and a family of sets $(A_i)_{i \in I}$,
$$B \cap \bigcup_{i \in I} A_i = \bigcup_{i \in I} (B \cap A_i), \qquad\text{and, if } I \neq \emptyset, \qquad B \cup \bigcap_{i \in I} A_i = \bigcap_{i \in I} (B \cup A_i).$$
:::

:::{admonition icon=false} ✍️ **Proof**
$x \in B \land \existsin{i}{I} (x \in A_i)$ is equivalent to $\existsin{i}{I} (x \in B \land x \in A_i)$, because the condition $x \in B$ does not involve $i$. Similarly, $x \in B \lor \forallin{i}{I} (x \in A_i)$ is equivalent to $\forallin{i}{I} (x \in B \lor x \in A_i)$: if $x \notin B$, both say that $x \in A_i$ for every $i$, and if $x \in B$, both are true. $\blacksquare$
:::
  
## Disjoint Sets and Partitions

A die cannot show both an even and an odd number. Events that cannot happen together are modeled by sets with no common elements, and Chapter 4's probabilities add up exactly over such sets.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Disjoint
: Sets $A$ and $B$ are disjoint if $A \cap B = \emptyset$. A family $(A_i)_{i \in I}$ is *pairwise disjoint* if $A_i \cap A_j = \emptyset$ for all $i, j \in I$ with $i \neq j$. A set $\mathcal A$ of sets is *pairwise disjoint* if any two distinct members of $\mathcal A$ are disjoint.
:::
::::

The family and set versions differ when members repeat. The family $A_1 = A_2 = \{1\}$ is *not* pairwise disjoint, since $A_1 \cap A_2 = \{1\}$, while the set $\{A_1, A_2\} = \{\{1\}\}$ is pairwise disjoint, because it has no two distinct members. The family $A_1 = A_2 = \emptyset$ is pairwise disjoint. Chapter 4 adds probabilities over pairwise disjoint *sequences*, so the family version is the one that matters there.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Partition
: A partition of a set $\Omega$ is a pairwise {term}`disjoint` set $\mathcal P$ of nonempty subsets of $\Omega$ whose union is $\Omega$, that is, $\bigcup \mathcal P = \Omega$.
:::
::::

Equivalently, a set $\mathcal P$ of nonempty subsets of $\Omega$ is a partition if and only if every element of $\Omega$ lies in exactly one member of $\mathcal P$: "at least one" is $\bigcup \mathcal P = \Omega$, and "at most one" is pairwise disjointness. For example, $\{\{1, 3, 5\}, \{2, 4, 6\}\}$ partitions $\{1, \ldots, 6\}$ by parity. In Chapter 4 a partition describes partial information: being told which member contains the outcome, but nothing more.
  
Probabilities add up over disjoint sets, but the sets we meet are often not disjoint. The following construction replaces any sequence of sets by a disjoint one with the same unions.

:::{important icon=false} 📐 **Lemma (Disjointification)**
Let $(A_n)_{n=1}^\infty$ be a sequence of sets and define
$$D_n := A_n \setminus \bigcup_{k=1}^{n-1} A_k \qquad (n \in \mathbb N^+),$$
so that $D_1 = A_1$. Then:

1. $D_n \subseteq A_n$ for every $n$;
2. $(D_n)_{n=1}^\infty$ is pairwise disjoint;
3. $\bigcup_{k=1}^n D_k = \bigcup_{k=1}^n A_k$ for every $n \in \mathbb N$;
4. $\bigcup_{n=1}^\infty D_n = \bigcup_{n=1}^\infty A_n$.

If moreover $A_1 \subseteq A_2 \subseteq \cdots$, then $D_n = A_n \setminus A_{n-1}$ for $n \ge 2$.
:::

:::{admonition icon=false} ✍️ **Proof**
1. By definition of set difference.
2. Let $m < n$. Then $D_m \subseteq A_m \subseteq \bigcup_{k=1}^{n-1} A_k$, and $D_n$ contains no element of that union, so $D_m \cap D_n = \emptyset$.
3. and 4. The inclusions $\subseteq$ follow from 1. Conversely, let $x \in A_k$ for some index $k$ (with $k \le n$ in part 3). By well-ordering there is a least index $m$ with $x \in A_m$, and $m \le k$. Then $x \notin A_j$ for all $j < m$, so $x \in D_m$.

If $A_1 \subseteq A_2 \subseteq \cdots$, then $A_k \subseteq A_{n-1}$ for all $k \le n - 1$ (by induction on $n - 1 - k$), so $\bigcup_{k=1}^{n-1} A_k = A_{n-1}$ for $n \ge 2$. $\blacksquare$
:::

In words, $D_n$ is the part of $A_n$ that is *new*: not already covered by $A_1, \ldots, A_{n-1}$.
  
## Finite Sums and Products

The Introduction averaged measurements as $(z_1 + \cdots + z_k)/k$. The dots hide a recursion, which we now make explicit. Let $S$ be a set with an addition $+ : S \times S \to S$ that is associative and commutative and has an identity element $0$ (so $a + 0 = a$). Right now our only example is $S = \mathbb N$. Later in this chapter $S$ will also be $\mathbb R$ and $[0, \infty]$, and Appendix B supplies $\mathbb Z$ and $\mathbb Q$.

For a sequence $(a_k)_{k=1}^\infty$ in $S$, Chapter 2's Recursion Theorem, in its form $h(n + 1) = g(n, h(n))$ with $g(n, x) := x + a_{n+1}$, gives exactly one sequence $(s_n)_{n \in \mathbb N}$ with
$$s_0 = 0, \qquad s_{n+1} = s_n + a_{n+1}.$$
We write $\sum_{k=1}^n a_k := s_n$, so that
$$\sum_{k=1}^0 a_k = 0 \qquad\text{and}\qquad \sum_{k=1}^{n+1} a_k = \sum_{k=1}^n a_k + a_{n+1}.$$
By induction on $n$, $s_n$ depends only on $a_1, \ldots, a_n$. So the sum of a finite sequence $a_1, \ldots, a_N$ is defined by extending it with $a_k := 0$ for $k > N$, and the extension does not affect $\sum_{k=1}^n a_k$ for $n \le N$. Sums over other index ranges, such as $\sum_{k=0}^n a_k$, are defined by shifting the index. If $S$ also has an associative, commutative multiplication with identity $1$, products are defined in the same way:
$$\prod_{k=1}^0 a_k := 1, \qquad \prod_{k=1}^{n+1} a_k := \Big(\prod_{k=1}^n a_k\Big) \cdot a_{n+1}, \qquad a^n := \prod_{k=1}^n a.$$

:::{important icon=false} 📐 **Lemma (Rules for Finite Sums)**
Let $(a_k)$ and $(b_k)$ be sequences in $S$ and $n \in \mathbb N$.

1. $\sum_{k=1}^n (a_k + b_k) = \sum_{k=1}^n a_k + \sum_{k=1}^n b_k$.
2. If $S$ has a multiplication that distributes over $+$ and satisfies $c \cdot 0 = 0$, then $c \sum_{k=1}^n a_k = \sum_{k=1}^n c\, a_k$.
3. If $S$ has an order $\le$ such that $a \le b$ implies $a + c \le b + c$, and $a_k \le b_k$ for $k = 1, \ldots, n$, then $\sum_{k=1}^n a_k \le \sum_{k=1}^n b_k$.
4. For a doubly indexed family $(a_{jk})_{j, k \in \mathbb N^+}$ in $S$ and $m \in \mathbb N$, $\;\sum_{j=1}^m \sum_{k=1}^n a_{jk} = \sum_{k=1}^n \sum_{j=1}^m a_{jk}$.
:::

:::{admonition icon=false} ✍️ **Proof**
Parts 1–3 are by induction on $n$; each holds for $n = 0$ because both sides are $0$ (using $c \cdot 0 = 0$ in part 2, and $0 \le 0$ in part 3).

1. $\sum_{k=1}^{n+1} (a_k + b_k) = \Big(\sum_{k=1}^n a_k + \sum_{k=1}^n b_k\Big) + (a_{n+1} + b_{n+1}) = \Big(\sum_{k=1}^n a_k + a_{n+1}\Big) + \Big(\sum_{k=1}^n b_k + b_{n+1}\Big)$, by the induction hypothesis, then associativity and commutativity.
2. $c\Big(\sum_{k=1}^n a_k + a_{n+1}\Big) = c\sum_{k=1}^n a_k + c\, a_{n+1} = \sum_{k=1}^n c\, a_k + c\, a_{n+1}$.
3. $\sum_{k=1}^n a_k + a_{n+1} \le \sum_{k=1}^n b_k + a_{n+1} \le \sum_{k=1}^n b_k + b_{n+1}$, applying the hypothesis on $\le$ twice (with commutativity) and transitivity.
4. Induction on $m$. For $m = 0$, the left side is $0$ and the right side is a sum of zeros, which is $0$ (induction on $n$). For the step,
$$\sum_{j=1}^{m+1} \sum_{k=1}^n a_{jk} = \sum_{k=1}^n \sum_{j=1}^m a_{jk} + \sum_{k=1}^n a_{m+1, k} = \sum_{k=1}^n \Big(\sum_{j=1}^m a_{jk} + a_{m+1, k}\Big) = \sum_{k=1}^n \sum_{j=1}^{m+1} a_{jk},$$
by the induction hypothesis and part 1. $\blacksquare$
:::

**Example (triangular numbers).** Let $T(n) := \sum_{k=1}^n k$ in $\mathbb N$, so $T(0) = 0$ and $T(n + 1) = T(n) + n + 1$. The first values are $0, 1, 3, 6, 10, 15$. By induction, $2\,T(n) = n(n + 1)$: the step is $2\,T(n+1) = n(n+1) + 2(n+1) = (n+1)(n+2)$. We use $T$ below to list the pairs of natural numbers.
  
## Images and Preimages

A function can transport sets in two directions. Forward, it carries a set of inputs to the set of their outputs. Backward, it pulls a set of outputs back to the set of all inputs that land in it. Probability uses the backward direction.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Image
: Let $f: X \to Y$ be a {term}`function` and $A \subseteq X$. The image of $A$ under $f$ is the set of outputs of elements of $A$,
  $$f[A] := \{f(a) : a \in A\} \subseteq Y.$$
:::
::::

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Preimage
: Let $f: X \to Y$ be a {term}`function` and $B \subseteq Y$. The preimage of $B$ under $f$ is the set of inputs whose output lies in $B$,
  $$f^{-1}[B] := \{x \in X : f(x) \in B\} \subseteq X.$$
:::
::::

The image exists by Replacement and the preimage by Separation. Square brackets distinguish the set $f[A]$ from the single output $f(a)$. The image $f[X]$ of the whole domain is the {term}`range` of $f$. The notation $f^{-1}[B]$ makes sense for *every* function: $f$ does not need an inverse function (defined below).

**Example (two dice).** Let $D := \{1, \ldots, 6\}$ and $\Omega := D \times D$, the possible results $(d_1, d_2)$ of rolling two dice. Let $s : \Omega \to \{2, \ldots, 12\}$ be the sum, $s(d_1, d_2) := d_1 + d_2$. Then
$$s^{-1}[\{7\}] = \{(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)\}$$
is the set of results that produce a sum of $7$, and $s[\{(1, 1), (2, 2)\}] = \{2, 4\}$.
  
:::{important icon=false} 📐 **Lemma (Preimages Preserve Set Operations)**
Let $f: X \to Y$, let $B, B' \subseteq Y$, and let $(B_i)_{i \in I}$ be a family of subsets of $Y$. Then:

1. $f^{-1}\big[\bigcup_{i \in I} B_i\big] = \bigcup_{i \in I} f^{-1}[B_i]$;
2. $f^{-1}\big[\bigcap_{i \in I} B_i\big] = \bigcap_{i \in I} f^{-1}[B_i]$ if $I \neq \emptyset$;
3. $f^{-1}[Y \setminus B] = X \setminus f^{-1}[B]$, that is, $f^{-1}[B^c] = \big(f^{-1}[B]\big)^c$ with complements relative to $Y$ and $X$;
4. $f^{-1}[Y] = X$ and $f^{-1}[\emptyset] = \emptyset$;
5. if $B \subseteq B'$ then $f^{-1}[B] \subseteq f^{-1}[B']$.
:::

:::{admonition icon=false} ✍️ **Proof**
All sets involved are subsets of $X$. For $x \in X$:

1. $x \in f^{-1}\big[\bigcup_i B_i\big] \iff f(x) \in \bigcup_i B_i \iff \existsin{i}{I} \big(f(x) \in B_i\big) \iff \existsin{i}{I} \big(x \in f^{-1}[B_i]\big) \iff x \in \bigcup_i f^{-1}[B_i]$.
2. The same chain with $\forallin{i}{I}$ in place of $\existsin{i}{I}$.
3. $x \in f^{-1}[Y \setminus B] \iff (f(x) \in Y \land f(x) \notin B) \iff f(x) \notin B \iff x \notin f^{-1}[B]$, because $f(x) \in Y$ always holds.
4. Every $f(x)$ is in $Y$, and no $f(x)$ is in $\emptyset$.
5. If $f(x) \in B$ then $f(x) \in B'$. $\blacksquare$
:::

Images behave well with unions but not with intersections or complements.

:::{important icon=false} 📐 **Lemma (Images)**
Let $f: X \to Y$, $A, A' \subseteq X$, and let $(A_i)_{i \in I}$ be a family of subsets of $X$. Then $f\big[\bigcup_{i \in I} A_i\big] = \bigcup_{i \in I} f[A_i]$ and $f[A \cap A'] \subseteq f[A] \cap f[A']$.
:::

:::{admonition icon=false} ✍️ **Proof**
$y \in f\big[\bigcup_i A_i\big]$ iff $y = f(x)$ for some $x$ in some $A_i$, iff $y \in f[A_i]$ for some $i$. If $y = f(x)$ with $x \in A \cap A'$, then $y \in f[A]$ and $y \in f[A']$. $\blacksquare$
:::

The inclusion can be strict. In the dice example take $A = \{(1, 2)\}$ and $A' = \{(2, 1)\}$. Then $s[A] \cap s[A'] = \{3\}$, but $s[A \cap A'] = s[\emptyset] = \emptyset$. Complements fail too: $s[\Omega \setminus A]$ still contains $3 = s(2, 1)$, so it is not $\{2, \ldots, 12\} \setminus s[A]$. In both cases the culprit is two different inputs with the same output.
  
**Why random variables are defined with preimages.** In [Chapter 5](ch5_random_variables_v2.md) a {term}`random variable` will be a function $X$ from the set of outcomes $\Omega$ to $\mathbb R$; for the scale, it is the noise in a reading as a function of the outcome. A question about its value, "is $X$ in $B$?", is the set of outcomes $X^{-1}[B]$. The lemma says that "$X \in B$ or $X \in B'$" is the set $X^{-1}[B] \cup X^{-1}[B']$, that "not $X \in B$" is the complement $X^{-1}[B]^c$, and likewise for infinitely many conditions. So the logic of questions about the value of $X$ matches the logic of sets of outcomes exactly. Images have no such property, which is why Chapter 5 defines random variables through preimages.

:::{attention icon=false} 🗝️ **Key Idea**
Preimages commute with every set operation; images do not. A condition on a measured value becomes a set of outcomes through a preimage, and combining conditions with "not", "or", and "and" combines those sets in the same way.
:::

The explorer below shows preimages under the dice sum $s$. Choose two sets of sums $B_1$ and $B_2$ and an operation. The right panel shows $s^{-1}[B_1 \cup B_2]$ (or $\cap$, or $\setminus$), and by the lemma it always coincides with the same operation applied to the two left panels.

```{marimo} python
:hide-code: true

_sums = [str(_v) for _v in range(2, 13)]
preimage_b1 = mo.ui.multiselect(options=_sums, value=["7"], label=r"$B_1$")
preimage_b2 = mo.ui.multiselect(
    options=_sums, value=["2", "3", "4", "5", "6"], label=r"$B_2$"
)
preimage_op = mo.ui.dropdown(
    options={"union": "union", "intersection": "intersection", "difference": "difference"},
    value="union",
    label="Operation",
)
```

```{marimo} python
:hide-code: true

_faces = np.arange(1, 7)
_sum = np.add.outer(_faces, _faces)  # _sum[i, j] = (i + 1) + (j + 1)
_b1 = sorted(int(_v) for _v in preimage_b1.value)
_b2 = sorted(int(_v) for _v in preimage_b2.value)
_op = preimage_op.value
if _op == "union":
    _b3 = sorted(set(_b1) | set(_b2))
    _sym = r"\cup"
elif _op == "intersection":
    _b3 = sorted(set(_b1) & set(_b2))
    _sym = r"\cap"
else:
    _b3 = sorted(set(_b1) - set(_b2))
    _sym = r"\setminus"
_m1 = np.isin(_sum, _b1)
_m2 = np.isin(_sum, _b2)
_m3 = np.isin(_sum, _b3)
_combined = {"union": _m1 | _m2, "intersection": _m1 & _m2, "difference": _m1 & ~_m2}[_op]
_agree = bool(np.array_equal(_m3, _combined))

_fig, _axes = plt.subplots(1, 3, figsize=(11, 3.9))
_titles = [r"$s^{-1}[B_1]$", r"$s^{-1}[B_2]$", rf"$s^{{-1}}[B_1 {_sym} B_2]$"]
for _ax, _mask, _title in zip(_axes, [_m1, _m2, _m3], _titles):
    for _i in range(6):
        for _j in range(6):
            _ax.add_patch(plt.Rectangle(
                (_i + 0.5, _j + 0.5), 1, 1,
                facecolor="C1" if _mask[_i, _j] else "#eeeeee",
                edgecolor="white", linewidth=1.5,
            ))
            _ax.text(_i + 1, _j + 1, str(_sum[_i, _j]), ha="center", va="center", fontsize=8)
    _ax.set_xlim(0.5, 6.5)
    _ax.set_ylim(0.5, 6.5)
    _ax.set_aspect("equal")
    _ax.set_xticks(_faces)
    _ax.set_yticks(_faces)
    _ax.set_xlabel("first die $d_1$")
    _ax.set_title(_title, style="italic")
_axes[0].set_ylabel("second die $d_2$")
_fig.tight_layout()

def _fmt(_b):
    return r"\{" + ", ".join(str(_v) for _v in _b) + r"\}" if _b else r"\emptyset"

_summary = mo.md(
    rf"$B_1 {_sym} B_2 = {_fmt(_b3)}$, and its preimage contains "
    + f"{int(_m3.sum())} of the 36 outcomes. "
    + (
        rf"It equals $s^{{-1}}[B_1] {_sym} s^{{-1}}[B_2]$, as the lemma guarantees."
        if _agree
        else "It differs from the combined preimages (this should never happen)."
    )
)
mo.vstack([mo.hstack([preimage_b1, preimage_b2, preimage_op], justify="start"), graphic(_fig), _summary])
```

## Injections, Surjections, and Bijections

Whether a function loses information (two inputs, one output) or misses part of its codomain (an output that never occurs) is captured by three properties.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Injective
: A {term}`function` $f: X \to Y$ is injective (an *injection*) if different inputs have different outputs: for all $x, x' \in X$, $f(x) = f(x')$ implies $x = x'$.
:::
::::

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Surjective
: A {term}`function` $f: X \to Y$ is surjective (a *surjection*) if every element of the {term}`codomain` is an output: for every $y \in Y$ there is an $x \in X$ with $f(x) = y$. Equivalently, $f[X] = Y$.
:::
::::

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Bijective
: A {term}`function` $f: X \to Y$ is bijective (a *bijection*) if it is both {term}`injective` and {term}`surjective`; that is, every $y \in Y$ equals $f(x)$ for exactly one $x \in X$.
:::
::::

Surjectivity depends on the codomain, which the notation $f: X \to Y$ fixes. The dice sum $s: \Omega \to \{2, \ldots, 12\}$ is surjective but not injective. The successor function $\operatorname{succ}: \mathbb N \to \mathbb N$ is injective (Chapter 2) but not surjective, because $0$ is not a successor. For every set $X$, the identity $\operatorname{id}_X : X \to X$, $\operatorname{id}_X(x) := x$, is bijective.

The counterexample for images used two inputs with one output, and injectivity rules that out: if $f$ is injective, then $f[A \cap A'] = f[A] \cap f[A']$. Indeed, if $y = f(a) = f(a')$ with $a \in A$ and $a' \in A'$, then $a = a' \in A \cap A'$.
  
::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Composition
: For functions $f: X \to Y$ and $g: Y \to Z$, the composition of $g$ with $f$ is the function $g \circ f : X \to Z$ given by $(g \circ f)(x) := g(f(x))$. As a set, $g \circ f := \{(x, g(f(x))) : x \in X\}$.
:::
::::

:::{important icon=false} 📐 **Lemma (Compositions)**
Let $f: X \to Y$ and $g: Y \to Z$.

1. If $f$ and $g$ are injective, so is $g \circ f$.
2. If $f$ and $g$ are surjective, so is $g \circ f$.
3. If $f$ and $g$ are bijective, so is $g \circ f$.
4. $(g \circ f)^{-1}[C] = f^{-1}\big[g^{-1}[C]\big]$ for every $C \subseteq Z$.
:::

:::{admonition icon=false} ✍️ **Proof**
1. If $g(f(x)) = g(f(x'))$, then $f(x) = f(x')$ because $g$ is injective, and $x = x'$ because $f$ is injective.
2. Given $z \in Z$, there is $y \in Y$ with $g(y) = z$, and there is $x \in X$ with $f(x) = y$; then $(g \circ f)(x) = z$.
3. Combine 1 and 2.
4. $x \in (g \circ f)^{-1}[C] \iff g(f(x)) \in C \iff f(x) \in g^{-1}[C] \iff x \in f^{-1}\big[g^{-1}[C]\big]$. $\blacksquare$
:::

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Inverse function
: For a {term}`bijection <bijective>` $f: X \to Y$, the inverse function $f^{-1} : Y \to X$ sends each $y \in Y$ to the unique $x \in X$ with $f(x) = y$. As a set, $f^{-1} := \{(y, x) : (x, y) \in f\}$.
:::
::::

:::{important icon=false} 📐 **Lemma (Inverse Functions)**
Let $f: X \to Y$ be a bijection. Then $f^{-1}$ is a bijection from $Y$ to $X$, with $f^{-1}(f(x)) = x$ for all $x \in X$ and $f(f^{-1}(y)) = y$ for all $y \in Y$. For $B \subseteq Y$, the preimage $f^{-1}[B]$ equals the image of $B$ under the inverse function.
:::

:::{admonition icon=false} ✍️ **Proof**
The set $\{(y, x) : (x, y) \in f\}$ exists by Replacement and is a subset of $Y \times X$. Each $y \in Y$ is the second coordinate of at least one pair in $f$ (surjectivity) and of at most one (injectivity), so $f^{-1}$ is a function from $Y$ to $X$. Since $(x, f(x)) \in f$, we have $(f(x), x) \in f^{-1}$, that is, $f^{-1}(f(x)) = x$. Since $(f^{-1}(y), y) \in f$, we have $f(f^{-1}(y)) = y$. If $f^{-1}(y) = f^{-1}(y')$, applying $f$ gives $y = y'$, so $f^{-1}$ is injective; and every $x$ equals $f^{-1}(f(x))$, so $f^{-1}$ is surjective. Finally, $x \in f^{-1}[B] \iff f(x) \in B \iff x = f^{-1}(y)$ for some $y \in B$. $\blacksquare$
:::

The last statement means the notation $f^{-1}[B]$ is unambiguous: for a bijection, the preimage and the image under the inverse function are the same set. **Example:** $\operatorname{succ}: \mathbb N \to \mathbb N^+$ is a bijection, because it is injective and every $n \neq 0$ is a successor. Its inverse is $n \mapsto n - 1$. This is the re-indexing between sequences on $\mathbb N$ and on $\mathbb N^+$.
  
## Countable and Uncountable Sets

A fair die has six equally likely outcomes. Can a "random natural number" have all of its outcomes equally likely? Can a "uniformly random" real number in $[0, 1]$? [Chapter 4](ch4_probability_spaces_v2.md) shows that the answers are *no* and *yes, with care*, and the difference comes down to the kind of infinity involved. Here we make the size of a set precise without counting: two sets have the same size if their elements can be paired off exactly.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Equinumerous
: Sets $X$ and $Y$ are equinumerous, written $X \approx Y$, if there is a {term}`bijection <bijective>` $X \to Y$.
:::
::::

:::{important icon=false} 📐 **Lemma (Equinumerosity)**
For all sets $X$, $Y$, $Z$: $X \approx X$; if $X \approx Y$ then $Y \approx X$; and if $X \approx Y$ and $Y \approx Z$ then $X \approx Z$.
:::

:::{admonition icon=false} ✍️ **Proof**
The identity $\operatorname{id}_X$ is a bijection; the inverse of a bijection is a bijection (Inverse Functions lemma); and a composition of bijections is a bijection (Compositions lemma). $\blacksquare$
:::

The bijection $\operatorname{succ} : \mathbb N \to \mathbb N^+$ shows $\mathbb N \approx \mathbb N^+$: an infinite set can be equinumerous to a part of itself. For the sets $\{1, \ldots, n\}$ this is impossible, which is the content of the next lemma.

:::{important icon=false} 📐 **Lemma (Pigeonhole Principle)**
For every $n \in \mathbb N$, there is no injection $\{1, \ldots, n + 1\} \to \{1, \ldots, n\}$.
:::

:::{admonition icon=false} ✍️ **Proof**
Induction on $n$. For $n = 0$ there is no function at all from the nonempty set $\{1\}$ to $\emptyset$. Suppose the statement holds for $n$, and suppose $f : \{1, \ldots, n + 2\} \to \{1, \ldots, n + 1\}$ were injective.

- If no $k \le n + 1$ has $f(k) = n + 1$, then $f$ restricted to $\{1, \ldots, n + 1\}$ is an injection into $\{1, \ldots, n\}$, contradicting the induction hypothesis.
- Otherwise $f(j) = n + 1$ for some $j \le n + 1$, and $f(n + 2) \neq n + 1$ by injectivity. Define $g$ on $\{1, \ldots, n + 1\}$ by $g(j) := f(n + 2)$ and $g(k) := f(k)$ for $k \neq j$. The values of $g$ are the values $f(k)$ for $k \neq j$, which are distinct and different from $f(j) = n + 1$. So $g$ is an injection $\{1, \ldots, n + 1\} \to \{1, \ldots, n\}$, again a contradiction. $\blacksquare$
:::
  
::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Finite
: A set $X$ is finite if $X \approx \{1, \ldots, n\}$ for some $n \in \mathbb N$. A set that is not finite is *infinite*.
:::
::::

:::{important icon=false} 📐 **Corollary (Number of Elements)**
If $X \approx \{1, \ldots, m\}$ and $X \approx \{1, \ldots, n\}$, then $m = n$. This number is the *number of elements* of $X$, written $|X|$. Moreover, $\mathbb N$ is infinite.
:::

:::{admonition icon=false} ✍️ **Proof**
By the Equinumerosity lemma there is a bijection $h : \{1, \ldots, n\} \to \{1, \ldots, m\}$. If $m < n$, then $\{1, \ldots, m + 1\} \subseteq \{1, \ldots, n\}$, and $h$ restricted to $\{1, \ldots, m + 1\}$ is an injection into $\{1, \ldots, m\}$, contradicting the Pigeonhole Principle. By symmetry $n < m$ is impossible too, so $m = n$. Likewise, a bijection $h : \mathbb N \to \{1, \ldots, n\}$ would restrict to an injection $\{1, \ldots, n + 1\} \to \{1, \ldots, n\}$. $\blacksquare$
:::

**Sums over finite sets.** A finite set has no preferred order, so to add up a family $(a_i)_{i \in F}$ indexed by a finite set $F$ we list $F$ in some order and must check that the order does not matter.

:::{important icon=false} 📐 **Lemma (Splitting and Reordering Finite Sums)**
Let $(a_k)$ be a sequence in a set $S$ with addition as in Finite Sums and Products, and let $m, n \in \mathbb N$.

1. *(Splitting)* $\sum_{k=1}^{m+n} a_k = \sum_{k=1}^m a_k + \sum_{k=1}^n a_{m+k}$.
2. *(Reordering)* If $\sigma : \{1, \ldots, n\} \to \{1, \ldots, n\}$ is a bijection, then $\sum_{k=1}^n a_{\sigma(k)} = \sum_{k=1}^n a_k$.
:::

:::{admonition icon=false} ✍️ **Proof**
1. Induction on $n$. For $n = 0$ both sides are $\sum_{k=1}^m a_k$. For the step, $\sum_{k=1}^{m+n+1} a_k = \sum_{k=1}^m a_k + \sum_{k=1}^n a_{m+k} + a_{m+n+1} = \sum_{k=1}^m a_k + \sum_{k=1}^{n+1} a_{m+k}$.
2. Induction on $n$; the case $n = 0$ is trivial. Let $\sigma$ be a bijection of $\{1, \ldots, n + 1\}$ and $j := \sigma^{-1}(n + 1)$. Splitting the sum before and after position $j$ (part 1) and moving the term $a_{\sigma(j)} = a_{n+1}$ to the end (commutativity),
$$\sum_{k=1}^{n+1} a_{\sigma(k)} = \sum_{k=1}^n a_{\tau(k)} + a_{n+1}, \qquad \tau(k) := \begin{cases} \sigma(k), & k < j, \\ \sigma(k + 1), & j \le k \le n. \end{cases}$$
The function $\tau$ is a bijection from $\{1, \ldots, n\}$ onto $\{1, \ldots, n + 1\} \setminus \{n + 1\} = \{1, \ldots, n\}$, so by the induction hypothesis the right side equals $\sum_{k=1}^n a_k + a_{n+1} = \sum_{k=1}^{n+1} a_k$. $\blacksquare$
:::

For a finite set $F$ with $|F| = n$ and a family $(a_i)_{i \in F}$ in $S$, we define
$$\sum_{i \in F} a_i := \sum_{k=1}^n a_{e(k)}$$
for any bijection $e : \{1, \ldots, n\} \to F$. The value does not depend on $e$: if $e'$ is another such bijection, then $\sigma := e^{-1} \circ e'$ is a bijection of $\{1, \ldots, n\}$ and $a_{e'(k)} = a_{e(\sigma(k))}$, so part 2 applies. In particular $\sum_{i \in \emptyset} a_i = 0$. If $F$ and $G$ are disjoint finite sets, listing $F$ first and then $G$ is a bijection $\{1, \ldots, |F| + |G|\} \to F \cup G$, so part 1 gives $\sum_{i \in F \cup G} a_i = \sum_{i \in F} a_i + \sum_{i \in G} a_i$. Products $\prod_{i \in F} a_i$ are defined in the same way.
  
::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Countable
: A set $X$ is countable if there is an {term}`injection <injective>` $X \to \mathbb N$. It is *countably infinite* if $X \approx \mathbb N$.
:::
::::

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Uncountable
: A set is uncountable if it is not {term}`countable`.
:::
::::

Finite sets are countable: a bijection $X \to \{1, \ldots, n\}$ followed by the inclusion of $\{1, \ldots, n\}$ in $\mathbb N$ is an injection (Compositions lemma). Countably infinite sets are countable, and they are infinite: if $X \approx \mathbb N$ and $X \approx \{1, \ldots, n\}$, then $\mathbb N \approx \{1, \ldots, n\}$, which the corollary above rules out. Some books use "countable" to mean "countably infinite". In this book, finite sets are countable too.

:::{important icon=false} 📐 **Theorem (Listing Countable Sets)**
A nonempty set $X$ is countable if and only if there is a surjection $g : \mathbb N \to X$, that is, a sequence $(x_n)_{n \in \mathbb N}$ with $\{x_n : n \in \mathbb N\} = X$. The same holds with $\mathbb N^+$ in place of $\mathbb N$.
:::

:::{admonition icon=false} ✍️ **Proof**
($\Rightarrow$) Let $f : X \to \mathbb N$ be injective and fix $x_0 \in X$. Let
$$g := \{(n, x) \in \mathbb N \times X : f(x) = n \ \lor\ (n \notin f[X] \land x = x_0)\}.$$
For $n \in f[X]$ exactly one $x$ has $f(x) = n$, by injectivity, and for $n \notin f[X]$ the only partner is $x_0$. So $g$ is a function $\mathbb N \to X$, and it is surjective because $g(f(x)) = x$.

($\Leftarrow$) Let $g : \mathbb N \to X$ be surjective. For $x \in X$ the set $g^{-1}[\{x\}] \subseteq \mathbb N$ is nonempty, so it has a least element by well-ordering; let $f(x)$ be that element. Then $g(f(x)) = x$, so $f(x) = f(x')$ implies $x = g(f(x)) = g(f(x')) = x'$, and $f$ is injective.

For $\mathbb N^+$, compose with the bijection $\operatorname{succ}$ or its inverse. $\blacksquare$
:::

A listing may repeat elements. The direction ($\Leftarrow$) needs no Axiom of Choice: well-ordering supplies a definite choice, the least index.

:::{important icon=false} 📐 **Corollary (Subsets and Images)**
1. Every subset of a countable set is countable.
2. If $X$ is countable and $f : X \to Y$, then $f[X]$ is countable.
:::

:::{admonition icon=false} ✍️ **Proof**
1. Restrict the injection to the subset.
2. If $X = \emptyset$, then $f[X] = \emptyset$, which is countable because the empty function is an injection. Otherwise take a surjection $g : \mathbb N \to X$. Viewed as a function into $f[X]$, $f$ is surjective, so $f \circ g : \mathbb N \to f[X]$ is a surjection (Compositions lemma), and $f[X]$ is countable by the theorem. $\blacksquare$
:::

:::{important icon=false} 📐 **Theorem (Countable Sets Are Finite or Countably Infinite)**
A set is countable if and only if it is finite or countably infinite.
:::

:::{admonition icon=false} ✍️ **Proof**
Finite and countably infinite sets are countable, as shown above. Conversely, let $f : X \to \mathbb N$ be injective. Then $f$ is a bijection from $X$ onto $f[X]$, so by the Equinumerosity lemma it suffices to show that every $Y \subseteq \mathbb N$ is finite or countably infinite.

*Case 1: $Y$ is bounded,* that is, $Y \subseteq \{k \in \mathbb N : k < m\}$ for some $m$. We show by induction on $m$ that every subset of $\{k : k < m\}$ is finite. For $m = 0$ the only subset is $\emptyset = \{1, \ldots, 0\}$. If $Y \subseteq \{k : k < m + 1\}$, then $Y' := Y \setminus \{m\} \subseteq \{k : k < m\}$ is finite by the induction hypothesis, say via a bijection $h : Y' \to \{1, \ldots, j\}$. If $m \notin Y$, then $Y = Y'$. If $m \in Y$, then $h \cup \{(m, j + 1)\}$ is a bijection $Y \to \{1, \ldots, j + 1\}$.

*Case 2: $Y$ is unbounded,* that is, every $m \in \mathbb N$ has some $y \in Y$ with $y > m$. Let $\nu(m) := \min\{y \in Y : y > m\}$, which exists by well-ordering. By the Recursion Theorem there is a sequence $e : \mathbb N \to \mathbb N$ with $e(0) = \min Y$ and $e(k + 1) = \nu(e(k))$. Every $e(k)$ is in $Y$ and $e(k) < e(k + 1)$. By induction, $k < l$ implies $e(k) < e(l)$, so $e$ is injective, and $e(k) \ge k$ for every $k$. For surjectivity let $y \in Y$. The set $\{k : e(k) \ge y\}$ contains $y$, so it has a least element $k$. If $k = 0$, then $\min Y \le y \le e(0) = \min Y$. If $k = j + 1$, then $e(j) < y$, so $y$ belongs to $\{y' \in Y : y' > e(j)\}$, whose least element is $e(k)$; hence $e(k) \le y \le e(k)$. Either way $y = e(k)$. So $e : \mathbb N \to Y$ is a bijection. $\blacksquare$
:::
  
### Pairs, Integers, and Rationals

The pairs $(m, n)$ of natural numbers fill a quarter-plane, which looks "bigger" than $\mathbb N$. They can nevertheless be listed, diagonal by diagonal: first the pairs with $m + n = 0$, then those with $m + n = 1$, and so on. The triangular numbers $T(s) = \sum_{k=1}^s k$ count the pairs on the diagonals before diagonal $s$.

:::{important icon=false} 📐 **Theorem (Pairing)**
The function $\pi : \mathbb N \times \mathbb N \to \mathbb N$, $\pi(m, n) := T(m + n) + n$, is a bijection. Hence $\mathbb N \times \mathbb N$ is countably infinite.
:::

:::{admonition icon=false} ✍️ **Proof**
Since $T(t + 1) = T(t) + t + 1$, the function $T$ is strictly increasing, and by induction $T(t) \ge t$.

*Claim: for every $N \in \mathbb N$ there is exactly one $s \in \mathbb N$ with $T(s) \le N < T(s + 1)$.* For existence, $T(N + 1) \ge N + 1 > N$, so the set $\{t \in \mathbb N : N < T(t)\}$ is nonempty and has a least element $t_0$. Since $T(0) = 0 \le N$, $t_0 \neq 0$, so $t_0 = s + 1$ for some $s$, and $T(s) \le N$ by minimality. For uniqueness, if $s < s'$ then $T(s + 1) \le T(s')$, so $N < T(s + 1)$ and $T(s') \le N$ cannot both hold.

*Injective.* Let $\pi(m, n) = N$ and $s := m + n$. Then $T(s) \le T(s) + n = N \le T(s) + s < T(s + 1)$, so $s$ is the unique index of the claim for $N$. If also $\pi(m', n') = N$, then $m' + n' = s$ as well, so $n' = N - T(s) = n$ and $m' = s - n = m$.

*Surjective.* Given $N$, take $s$ from the claim and let $n := N - T(s)$. From $N < T(s) + s + 1$ we get $n \le s$, so $m := s - n \in \mathbb N$, and $\pi(m, n) = T(s) + n = N$. $\blacksquare$
:::

So $\pi(0, 0) = 0$, $\pi(1, 0) = 1$, $\pi(0, 1) = 2$, $\pi(2, 0) = 3$, $\pi(1, 1) = 4$, $\pi(0, 2) = 5$, and so on.

:::{important icon=false} 📐 **Corollary (Products of Countable Sets)**
If $X$ and $Y$ are countable, so is $X \times Y$.
:::

:::{admonition icon=false} ✍️ **Proof**
With injections $f : X \to \mathbb N$ and $g : Y \to \mathbb N$, the function $(x, y) \mapsto \pi(f(x), g(y))$ is injective, because $\pi$ is injective and two ordered pairs are equal only if their coordinates are equal. $\blacksquare$
:::

:::{tip icon=false} **Facts about $\mathbb Z$ and $\mathbb Q$ used in this chapter**
[Appendix B: The Integers](appendix_b_number_systems_v2.md) and [Appendix B: The Rational Numbers](appendix_b_number_systems_v2.md) construct the integers $\mathbb Z$ and the rational numbers $\mathbb Q$, and identify $\mathbb N \subseteq \mathbb Z \subseteq \mathbb Q$ so that $+$, $\cdot$, and $<$ extend those of $\mathbb N$. We use: every integer is $m - n$ for some $m, n \in \mathbb N$; every rational number is $a/b$ for some $a \in \mathbb Z$ and $b \in \mathbb N^+$, and every positive rational number is $a/b$ with $a, b \in \mathbb N^+$; $\mathbb Z$ is closed under $+$, $-$, and $\cdot$, and $\mathbb Q$ is in addition closed under division by nonzero elements.
:::

:::{important icon=false} 📐 **Theorem (The Integers and the Rationals Are Countable)**
$\mathbb Z$ and $\mathbb Q$ are countably infinite.
:::

:::{admonition icon=false} ✍️ **Proof**
The function $(m, n) \mapsto m - n$ maps $\mathbb N \times \mathbb N$ onto $\mathbb Z$, so $\mathbb Z$ is countable by the Pairing theorem and the Subsets and Images corollary. The function $(a, n) \mapsto a/(n + 1)$ maps $\mathbb Z \times \mathbb N$ onto $\mathbb Q$, and $\mathbb Z \times \mathbb N$ is countable by the previous corollary, so $\mathbb Q$ is countable. Both are infinite because they contain $\mathbb N$: an injection from either into $\{1, \ldots, n\}$ would restrict to an injection $\{1, \ldots, n + 1\} \to \{1, \ldots, n\}$. By the previous theorem both are countably infinite. $\blacksquare$
:::

The diagram below lists the positive rationals using the proof. The $k$-th term is $q_k := (m + 1)/(n + 1)$ where $(m, n) = \pi^{-1}(k)$, so the list runs along the diagonals of the grid of numerators and denominators. Every positive rational $a/b$ appears, at position $\pi(a - 1, b - 1)$. Fractions not in lowest terms, such as $2/2$, repeat an earlier value, which a listing is allowed to do.

```{marimo} python
:hide-code: true

zigzag_slider = mo.ui.slider(
    start=1, stop=45, step=1, value=10, show_value=True,
    label=r"Number of terms $N$",
)
```

```{marimo} python
:hide-code: true

_N = zigzag_slider.value
_pairs = []
_diag = 0
while len(_pairs) < _N:
    for _n in range(_diag + 1):
        _pairs.append((_diag - _n, _n))
    _diag += 1
_pairs = _pairs[:_N]
_num = np.array([_p[0] + 1 for _p in _pairs])
_den = np.array([_p[1] + 1 for _p in _pairs])
_new = np.gcd(_num, _den) == 1

_fig, _ax = plt.subplots(figsize=(6.4, 5.6))
_grid = np.arange(1, 10)
_gx, _gy = np.meshgrid(_grid, _grid)
_ax.scatter(_gx, _gy, s=10, color="lightgray", zorder=1)
_ax.plot(_num, _den, color="C0", linewidth=1, zorder=2)
_ax.scatter(_num[_new], _den[_new], s=70, color="C1", zorder=3, label="new value")
_ax.scatter(
    _num[~_new], _den[~_new], s=70, facecolors="white", edgecolors="gray",
    zorder=3, label="repeat of an earlier value",
)
for _k in range(_N):
    _ax.annotate(str(_k), (_num[_k], _den[_k]), textcoords="offset points", xytext=(6, 5), fontsize=8)
_ax.set_xticks(_grid)
_ax.set_yticks(_grid)
_ax.set_xlim(0.5, 9.5)
_ax.set_ylim(9.5, 0.5)
_ax.set_xlabel("numerator $m + 1$")
_ax.set_ylabel("denominator $n + 1$")
_ax.grid(visible=True, alpha=0.9, linewidth=0.4)
_ax.legend(loc="lower right", fontsize=8)
_ax.set_title("Listing the positive rationals along diagonals", style="italic")

def _frac(_a, _b):
    _t = str(_a) if _b == 1 else rf"\tfrac{{{_a}}}{{{_b}}}"
    return _t if np.gcd(_a, _b) == 1 else rf"\textcolor{{gray}}{{{_t}}}"

_sep = r",\ "
_terms = _sep.join(_frac(int(_a), int(_b)) for _a, _b in zip(_num, _den))
_listing = mo.md(rf"$q_0, \ldots, q_{{{_N - 1}}} = {_terms}$ (repeated values in gray)")
mo.vstack([zigzag_slider, graphic(_fig), _listing])
```

### Countable Unions

A countable union of countable sets is countable. The proof needs one injection into $\mathbb N$ for each of infinitely many sets, chosen all at once, so it uses Chapter 2's Axiom of Choice through the following consequence.

:::{important icon=false} 📐 **Lemma (Countable Choice)**
If $(S_n)_{n \in \mathbb N}$ is a sequence of nonempty sets, there is a sequence $(s_n)_{n \in \mathbb N}$ with $s_n \in S_n$ for every $n$.
:::

:::{admonition icon=false} ✍️ **Proof**
Let $F := \{\{n\} \times S_n : n \in \mathbb N\}$, a set by Replacement. Its members are nonempty, and two different members share no element, since elements of $\{n\} \times S_n$ have first coordinate $n$. By the Axiom of Choice there is a set $C$ containing exactly one element of each member of $F$. Then $c := C \cap \bigcup F$ contains, for each $n$, exactly one pair $(n, s)$, and that pair has $s \in S_n$. So $c$ is a function on $\mathbb N$ with $c(n) \in S_n$; let $s_n := c(n)$. (With the function form of Choice from Chapter 2, apply it to the set $\{S_n : n \in \mathbb N\}$ directly.) $\blacksquare$
:::

:::{important icon=false} 📐 **Theorem (Countable Unions of Countable Sets)**
If $(A_n)_{n \in \mathbb N}$ is a sequence of countable sets, then $\bigcup_{n \in \mathbb N} A_n$ is countable.
:::

:::{admonition icon=false} ✍️ **Proof**
Let $S_n$ be the set of injections $A_n \to \mathbb N$, a subset of $\mathbb N^{A_n}$ by Separation. Each $S_n$ is nonempty because $A_n$ is countable, so by Countable Choice there is a sequence $(f_n)$ with each $f_n : A_n \to \mathbb N$ injective. For $x \in U := \bigcup_n A_n$, let $n_x := \min\{n : x \in A_n\}$ (well-ordering) and define
$$F(x) := \pi\big(n_x,\ f_{n_x}(x)\big).$$
If $F(x) = F(y)$, then since $\pi$ is injective, $n_x = n_y =: n$ and $f_n(x) = f_n(y)$, so $x = y$ because $f_n$ is injective. Thus $F : U \to \mathbb N$ is an injection. $\blacksquare$
:::

:::{caution icon=false} ⚠️ **Assumptions and Failure Modes**
- **Choice is used.** Each $A_n$ has many injections into $\mathbb N$, and nothing singles one out, so choosing one for every $n$ at once needs the Axiom of Choice. Without it the theorem can fail: if the other axioms of set theory are consistent, they remain consistent when "$\mathbb R$ is a countable union of countable sets" is added (the Feferman–Lévy model; see [Axiom of countable choice](https://en.wikipedia.org/wiki/Axiom_of_countable_choice)). When the injections are given explicitly, as for $\mathbb Z$ and $\mathbb Q$ above, or when there are only finitely many sets, no choice is needed.
- **"Countably many" is essential.** An uncountable union of countable sets can be uncountable: $\mathbb R = \bigcup_{x \in \mathbb R} \{x\}$, and $\mathbb R$ is uncountable, as we prove below.
:::
  
### Uncountable Sets Exist

Not every infinite set can be listed. The proof is the first appearance of a *diagonal argument*: build an object that differs from every item on a proposed list.

:::{important icon=false} 📐 **Theorem (Cantor)**
For every set $X$, no function $f : X \to \mathcal P(X)$ is surjective.
:::

:::{admonition icon=false} ✍️ **Proof**
Let $f : X \to \mathcal P(X)$ and let $D := \{x \in X : x \notin f(x)\}$, a subset of $X$ by Separation. If $D = f(d)$ for some $d \in X$, then $d \in D \iff d \notin f(d) = D$, a contradiction. So $D$ is not an output of $f$. $\blacksquare$
:::

:::{important icon=false} 📐 **Corollary (The Power Set of $\mathbb N$ Is Uncountable)**
$\mathcal P(\mathbb N)$ is uncountable.
:::

:::{admonition icon=false} ✍️ **Proof**
$\mathcal P(\mathbb N)$ is nonempty. If it were countable, the Listing theorem would give a surjection $\mathbb N \to \mathcal P(\mathbb N)$, contradicting Cantor's theorem. $\blacksquare$
:::

Since $x \mapsto \{x\}$ is an injection $X \to \mathcal P(X)$ but there is no surjection back, $\mathcal P(X)$ is in this sense strictly larger than $X$, and the sequence $X$, $\mathcal P(X)$, $\mathcal P(\mathcal P(X))$, … never stops growing. The set of real numbers, which we define next, is also uncountable, by a second diagonal argument.
  
## The Real Numbers

Measurements, noise, and probabilities are real numbers. What matters about $\mathbb R$ in this book is not how it is built but which rules it obeys: those of a *complete ordered field*. We state the rules, then quote the theorem that exactly one structure obeys them.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Field
: A set $F$ together with two functions $+ : F \times F \to F$ and $\cdot : F \times F \to F$ and two elements $0 \neq 1$ of $F$, such that for all $a, b, c \in F$:

  1. (associativity) $(a + b) + c = a + (b + c)$ and $(a \cdot b) \cdot c = a \cdot (b \cdot c)$;
  2. (commutativity) $a + b = b + a$ and $a \cdot b = b \cdot a$;
  3. (identities) $a + 0 = a$ and $a \cdot 1 = a$;
  4. (additive inverses) there is $-a \in F$ with $a + (-a) = 0$;
  5. (multiplicative inverses) if $a \neq 0$, there is $a^{-1} \in F$ with $a \cdot a^{-1} = 1$;
  6. (distributivity) $a \cdot (b + c) = a \cdot b + a \cdot c$.
:::
::::

We write $ab$ for $a \cdot b$, $a - b := a + (-b)$, and $a / b := a b^{-1}$ for $b \neq 0$. Inverses are unique: if $a + b = 0$ and $a + b' = 0$, then $b = b + (a + b') = (b + a) + b' = b'$, and likewise for $a^{-1}$. So $-a$ and $a^{-1}$ name definite elements. (Formally, a field is the tuple $(F, +, \cdot, 0, 1)$.)

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Ordered field
: A {term}`field` $F$ together with a relation $<$ on $F$ such that for all $a, b, c \in F$:

  1. (trichotomy) exactly one of $a < b$, $a = b$, $b < a$ holds;
  2. (transitivity) if $a < b$ and $b < c$, then $a < c$;
  3. (addition) if $a < b$, then $a + c < b + c$;
  4. (multiplication) if $0 < a$ and $0 < b$, then $0 < ab$.
:::
::::

We write $a \le b$ for "$a < b$ or $a = b$" and $a > b$ for $b < a$, and call $a$ *positive* if $a > 0$ and *negative* if $a < 0$. The rational numbers form an ordered field ([Appendix B: The Rational Numbers](appendix_b_number_systems_v2.md)).
  
:::{important icon=false} 📐 **Lemma (Rules of Algebra)**
In an ordered field, for all $a, b, c, d$:

1. $a \cdot 0 = 0$, $(-a) b = -(ab)$, and $(-a)(-b) = ab$;
2. $a < b$ if and only if $-b < -a$; in particular, $a > 0$ if and only if $-a < 0$;
3. if $a \neq 0$ then $a^2 := a a > 0$; in particular $0 < 1$;
4. if $a < b$ and $c > 0$, then $a c < b c$;
5. if $a > 0$ then $a^{-1} > 0$, and if $0 < a < b$ then $b^{-1} < a^{-1}$;
6. if $a \le b$ and $c \le d$, then $a + c \le b + d$, with $<$ if either hypothesis is strict.
:::

:::{admonition icon=false} ✍️ **Proof**
1. $a \cdot 0 = a(0 + 0) = a \cdot 0 + a \cdot 0$; adding $-(a \cdot 0)$ to both sides gives $0 = a \cdot 0$. Then $ab + (-a)b = (a + (-a))b = 0$, so $(-a)b$ is the additive inverse of $ab$. Since $x$ is the additive inverse of $-x$, we have $-(-x) = x$, so $(-a)(-b) = -(a(-b)) = -(-(ab)) = ab$.
2. If $a < b$, adding $(-a) + (-b)$ to both sides (axiom 3) gives $-b < -a$. The converse is the same argument applied to $-b < -a$, using $-(-x) = x$. Taking $a = 0$ and using $-0 = 0$ gives the second statement.
3. If $a > 0$, then $aa > 0$ by axiom 4. If $a < 0$, then $-a > 0$ by 2, and $aa = (-a)(-a) > 0$ by 1 and axiom 4. Since $1 \neq 0$, $1 = 1 \cdot 1 > 0$.
4. $b - a > 0$ by axiom 3, so $(b - a)c > 0$ by axiom 4, that is, $bc - ac > 0$ by distributivity and 1. Add $ac$.
5. $a^{-1} \neq 0$, since otherwise $1 = a a^{-1} = 0$. If $a^{-1} < 0$, then 4 (multiplying by $a > 0$) gives $1 < 0$, contradicting 3. So $a^{-1} > 0$. If $0 < a < b$, multiply $a < b$ by $a^{-1} b^{-1} > 0$ to get $b^{-1} < a^{-1}$.
6. $a + c \le b + c \le b + d$ by axiom 3 applied twice (with commutativity), then transitivity. $\blacksquare$
:::

Every other familiar rule for equations and inequalities follows from the axioms in the same way. When this book needs one that is not listed here, it says so.
  
### Bounds and Completeness

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Upper bound
: Let $F$ be an {term}`ordered field` and $S \subseteq F$. An element $u \in F$ is an upper bound of $S$ if $s \le u$ for every $s \in S$. If $S$ has an upper bound, $S$ is *bounded above*. *Lower bounds* and *bounded below* are defined in the same way, with $\ge$ in place of $\le$.
:::
::::

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Supremum
: Let $S$ be a subset of an {term}`ordered field` $F$. An element $u \in F$ is a supremum (*least upper bound*) of $S$ if $u$ is an {term}`upper bound` of $S$ and $u \le v$ for every upper bound $v$ of $S$. It is written $\sup S$.
:::
::::

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Infimum
: Let $S$ be a subset of an {term}`ordered field` $F$. An element $l \in F$ is an infimum (*greatest lower bound*) of $S$ if $l$ is a lower bound of $S$ and $v \le l$ for every lower bound $v$ of $S$. It is written $\inf S$.
:::
::::

A set has at most one supremum: if $u$ and $u'$ are both suprema, then $u \le u'$ and $u' \le u$, so $u = u'$ by trichotomy. The same holds for infima, so the notations $\sup S$ and $\inf S$ are justified whenever these exist. A supremum need not belong to the set. In $\mathbb Q$, the set $S = \{q \in \mathbb Q : q < 0\}$ has supremum $0 \notin S$: $0$ is an upper bound, and no $u < 0$ is one, because $u < u/2 < 0$ with $u/2 \in S$.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Complete ordered field
: An {term}`ordered field` in which every nonempty subset that is bounded above has a {term}`supremum`. This requirement is called the *least-upper-bound property*.
:::
::::

:::{important icon=false} 📐 **Theorem (The Real Numbers)**
There exists a complete ordered field. If $F$ and $F'$ are complete ordered fields, there is exactly one bijection $\varphi : F \to F'$ with $\varphi(a + b) = \varphi(a) + \varphi(b)$, $\varphi(ab) = \varphi(a)\varphi(b)$, and $a < b \iff \varphi(a) < \varphi(b)$ for all $a, b \in F$.
:::

:::{admonition icon=false} ✍️ **Proof**
Not proven here. [Appendix B: The Real Numbers](appendix_b_number_systems_v2.md) constructs a complete ordered field from $\mathbb Q$ using Dedekind cuts, and [Appendix B: Uniqueness of the Real Numbers](appendix_b_number_systems_v2.md) states uniqueness precisely, sketches why it holds, and links to a full proof.
:::

We fix one complete ordered field, call its elements the *real numbers*, and denote it $\mathbb R$. By the theorem, any other choice differs only by renaming its elements, so nothing in this book depends on the choice. Appendix B builds $\mathbb R$ so that $\mathbb N \subseteq \mathbb Z \subseteq \mathbb Q \subseteq \mathbb R$, with the $+$, $\cdot$, and $<$ of $\mathbb R$ extending those of the smaller systems. In particular, the successor of $n \in \mathbb N$ is $n + 1$, and the facts about $\mathbb N$, $\mathbb Z$, and $\mathbb Q$ listed earlier hold inside $\mathbb R$.

Completeness is exactly what $\mathbb Q$ lacks. The set $\{q \in \mathbb Q : q < 0 \text{ or } q^2 < 2\}$ is nonempty and bounded above in $\mathbb Q$, but it has no supremum in $\mathbb Q$ ([Appendix B: Incompleteness of the Rationals](appendix_b_number_systems_v2.md)). Completeness is the one axiom that separates $\mathbb R$ from $\mathbb Q$, and every limit argument in this book rests on it.

:::{important icon=false} 📐 **Lemma (Infima)**
Every nonempty $S \subseteq \mathbb R$ that is bounded below has an infimum, namely $\inf S = -\sup(-S)$, where $-S := \{-s : s \in S\}$.
:::

:::{admonition icon=false} ✍️ **Proof**
By Rules of Algebra part 2, $l$ is a lower bound of $S$ if and only if $-l$ is an upper bound of $-S$. So $-S$ is nonempty and bounded above, and $u := \sup(-S)$ exists. Then $-u$ is a lower bound of $S$. If $v$ is any lower bound of $S$, then $-v$ is an upper bound of $-S$, so $u \le -v$, that is, $v \le -u$. $\blacksquare$
:::
  
### Consequences of Completeness

:::{important icon=false} 📐 **Theorem (Archimedean Property)**
For every $x \in \mathbb R$ there is $n \in \mathbb N$ with $n > x$. Consequently, for every $\varepsilon > 0$ there is $n \in \mathbb N^+$ with $1/n < \varepsilon$.
:::

:::{admonition icon=false} ✍️ **Proof**
Suppose not: then $x$ is an upper bound of $\mathbb N$, which is nonempty, so $s := \sup \mathbb N$ exists. Since $s - 1 < s$, the number $s - 1$ is not an upper bound, so some $n \in \mathbb N$ has $n > s - 1$. Then $n + 1 \in \mathbb N$ and $n + 1 > s$, contradicting that $s$ is an upper bound. For the second statement, choose $n \in \mathbb N$ with $n > 1/\varepsilon$. Then $n > 0$, so $n \in \mathbb N^+$, and $1/n < \varepsilon$ by Rules of Algebra part 5. $\blacksquare$
:::

Completeness is needed: there are ordered fields with elements larger than every natural number (see [Archimedean property](https://en.wikipedia.org/wiki/Archimedean_property)).

:::{important icon=false} 📐 **Theorem (Density of the Rationals)**
For all real $a < b$ there is $q \in \mathbb Q$ with $a < q < b$.
:::

:::{admonition icon=false} ✍️ **Proof**
By the Archimedean property choose $n \in \mathbb N^+$ with $1/n < b - a$, so that $1 < n(b - a)$, and choose $k \in \mathbb N$ with $k > -na$. The set $J := \{j \in \mathbb N : j - k > na\}$ is nonempty (Archimedean property again), so it has a least element $j_0$. Let $m := j_0 - k \in \mathbb Z$. Then $m > na$. Moreover $j_0 \neq 0$, since $-k < na$, so $j_0 - 1 \in \mathbb N \setminus J$, which means $m - 1 \le na$. Hence
$$na < m \le na + 1 < na + n(b - a) = nb,$$
and dividing by $n > 0$ (Rules of Algebra parts 4 and 5) gives $a < m/n < b$. $\blacksquare$
:::

So between any two real numbers, however close, there is a rational one. Yet the next section shows that the rationals are a negligible part of $\mathbb R$ in the sense of counting.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Absolute value
: For $x \in \mathbb R$, the absolute value of $x$ is $|x| := x$ if $x \ge 0$ and $|x| := -x$ if $x < 0$. The number $|x - y|$ is the *distance* between $x$ and $y$.
:::
::::

:::{important icon=false} 📐 **Lemma (Properties of Absolute Value)**
For $x, y \in \mathbb R$ and $c \ge 0$:

1. $|x| \ge 0$, and $|x| = 0$ if and only if $x = 0$;
2. $|-x| = |x|$ and $-|x| \le x \le |x|$;
3. $|x| \le c$ if and only if $-c \le x \le c$;
4. $|xy| = |x|\,|y|$;
5. *(triangle inequality)* $|x + y| \le |x| + |y|$.
:::

:::{admonition icon=false} ✍️ **Proof**
1. If $x \ge 0$ then $|x| = x \ge 0$; if $x < 0$ then $|x| = -x > 0$ by Rules of Algebra part 2. In both cases $|x| = 0$ forces $x = 0$.
2. Both $|x|$ and $|-x|$ equal whichever of $x, -x$ is nonnegative. If $x \ge 0$, then $-|x| = -x \le 0 \le x = |x|$; if $x < 0$, then $-|x| = x < 0 < -x = |x|$.
3. If $|x| \le c$, then $x \le |x| \le c$ and $-x \le |-x| = |x| \le c$, so $-c \le x$. Conversely, if $-c \le x \le c$, then both $x$ and $-x$ are at most $c$, and $|x|$ is one of them.
4. By Rules of Algebra part 1, both $|xy|$ and $|x||y|$ are equal to $xy$ or to $-xy$, and both are $\ge 0$. If $xy = 0$, both are $0$. Otherwise exactly one of $xy, -xy$ is positive, so the two agree.
5. Adding $-|x| \le x \le |x|$ and $-|y| \le y \le |y|$ (Rules of Algebra part 6) gives $-(|x| + |y|) \le x + y \le |x| + |y|$; apply 3 with $c = |x| + |y|$. $\blacksquare$
:::

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Interval
: A subset of $\mathbb R$ of one of the following forms, where $a, b \in \mathbb R$ with $a \le b$, and $x$ ranges over $\mathbb R$:

  - $[a, b] := \{x : a \le x \le b\}$, $(a, b) := \{x : a < x < b\}$, $[a, b) := \{x : a \le x < b\}$, $(a, b] := \{x : a < x \le b\}$;
  - $[a, \infty) := \{x : x \ge a\}$, $(a, \infty) := \{x : x > a\}$, $(-\infty, b] := \{x : x \le b\}$, $(-\infty, b) := \{x : x < b\}$, or $(-\infty, \infty) := \mathbb R$.
:::
::::

Here $\infty$ and $-\infty$ are only notation; they become elements of the extended real numbers at the end of this chapter. The definition allows degenerate cases: $[x, x] = \{x\}$ and $(a, a) = \emptyset$ are intervals.
  
## The Real Numbers Are Uncountable

A noisy reading can be any real number in a range. If the real numbers in $[0, 1]$ could be listed as $x_0, x_1, x_2, \ldots$, we could hope to add up probabilities point by point. They cannot. The proof is a second diagonal argument, and it uses completeness through the following lemma.

:::{important icon=false} 📐 **Lemma (Nested Intervals)**
If $a_n \le a_{n+1} \le b_{n+1} \le b_n$ for all $n \in \mathbb N$, then $\bigcap_{n \in \mathbb N} [a_n, b_n] \neq \emptyset$.
:::

:::{admonition icon=false} ✍️ **Proof**
By induction, $a_n \le a_m$ and $b_m \le b_n$ whenever $n \le m$. So for any $n, m$, with $k$ the larger of the two, $a_n \le a_k \le b_k \le b_m$. Thus $A := \{a_n : n \in \mathbb N\}$ is nonempty and every $b_m$ is an upper bound of $A$. Let $s := \sup A$. Then $a_n \le s$ for all $n$ because $s$ is an upper bound, and $s \le b_m$ for all $m$ because $s$ is the least one. So $s \in [a_n, b_n]$ for every $n$. $\blacksquare$
:::

:::{important icon=false} 📐 **Theorem (The Real Numbers Are Uncountable)**
For every sequence $(x_n)_{n \in \mathbb N}$ of real numbers and all real $a < b$, there is a $c \in [a, b]$ with $c \neq x_n$ for every $n$. Consequently every interval $[a, b]$ with $a < b$ is uncountable, and so is $\mathbb R$.
:::

:::{admonition icon=false} ✍️ **Proof**
For $u < v$ let $d := v - u > 0$, and consider the left third $L := [u, u + d/3]$ and the right third $R := [v - d/3, v]$ of $[u, v]$. They are disjoint, since $u + d/3 < u + 2d/3 = v - d/3$. Let $P := \{(u, v) \in \mathbb R \times \mathbb R : u < v\}$ and define $g : \mathbb N \times P \to P$ by
$$g\big(n, (u, v)\big) := \begin{cases} (u,\ u + d/3) & \text{if } x_n \notin L, \\ (v - d/3,\ v) & \text{if } x_n \in L. \end{cases}$$
By the Recursion Theorem there is a sequence $(a_n, b_n)_{n \in \mathbb N}$ in $P$ with $(a_0, b_0) = (a, b)$ and $(a_{n+1}, b_{n+1}) = g\big(n, (a_n, b_n)\big)$. If $x_n \notin L$ we keep $L$, which avoids $x_n$; if $x_n \in L$ then $x_n \notin R$, and we keep $R$. Either way $x_n \notin [a_{n+1}, b_{n+1}]$. Both thirds lie in $[u, v]$, so $a_n \le a_{n+1} < b_{n+1} \le b_n$. By the Nested Intervals lemma some $c$ lies in every $[a_n, b_n]$. Then $c \in [a_0, b_0] = [a, b]$, and $c \neq x_n$ because $c \in [a_{n+1}, b_{n+1}]$ while $x_n$ is not.

If $[a, b]$ were countable, it would be nonempty, so it would be the set of terms of some sequence (Listing theorem), and the point $c$ for that sequence would be missing from it. So $[a, b]$ is uncountable, and $\mathbb R \supseteq [a, b]$ is uncountable because subsets of countable sets are countable. $\blacksquare$
:::

:::{important icon=false} 📐 **Corollary (Irrational Numbers)**
For real $a < b$, the set $[a, b] \setminus \mathbb Q$ of irrational numbers in $[a, b]$ is uncountable.
:::

:::{admonition icon=false} ✍️ **Proof**
The union of two countable sets $A$ and $B$ is countable: with injections $f : A \to \mathbb N$ and $g : B \to \mathbb N$, the function sending $x \in A$ to $\pi(0, f(x))$ and $x \in B \setminus A$ to $\pi(1, g(x))$ is injective, because $\pi$ is. Now $[a, b] = ([a, b] \cap \mathbb Q) \cup ([a, b] \setminus \mathbb Q)$, and $[a, b] \cap \mathbb Q \subseteq \mathbb Q$ is countable. If $[a, b] \setminus \mathbb Q$ were countable too, $[a, b]$ would be countable. $\blacksquare$
:::
  
The construction in the proof can be run on an actual list. Below, the list is $\mathbb Q \cap [0, 1]$ ordered by increasing denominator, in lowest terms: $0, 1, \tfrac12, \tfrac13, \tfrac23, \tfrac14, \tfrac34, \ldots$, which contains every rational number in $[0, 1]$. Each row shows the interval $[a_k, b_k]$ and the listed number $x_k$ that the next interval must avoid. Since the point $c$ in every interval differs from every rational number in $[0, 1]$, it is irrational.

:::{caution icon=false} ⚠️ **Assumptions and Failure Modes**
- **Completeness is essential.** The proof uses completeness exactly once, in the Nested Intervals lemma. It must fail for $\mathbb Q$, which is countable. Indeed, running the construction inside $\mathbb Q$ on the listing below gives nested intervals $[a_n, b_n] \cap \mathbb Q$ that are all nonempty but have no rational number in common. In $\mathbb Q$, nested closed intervals can have empty intersection.
- **Countable does not mean sparse.** $\mathbb Q$ is countable, yet it meets every interval $(a, b)$ with $a < b$ (Density of the Rationals). Countable sets are small only in the sense of listing. [Chapter 4](ch4_probability_spaces_v2.md) shows that they are also small in the sense of length: a countable set has length $0$.
:::

```{marimo} python
:hide-code: true

nested_slider = mo.ui.slider(
    start=1, stop=8, step=1, value=4, show_value=True,
    label=r"Steps of the construction $n$",
)
```

```{marimo} python
:hide-code: true

_n = nested_slider.value
_xs = []
_den = 1
while len(_xs) < _n:
    for _num in range(_den + 1):
        if Fraction(_num, _den).denominator == _den:
            _xs.append(Fraction(_num, _den))
    _den += 1
_xs = _xs[:_n]
_ivals = [(Fraction(0), Fraction(1))]
_kept = []
for _x in _xs:
    _lo, _hi = _ivals[-1]
    _third = (_hi - _lo) / 3
    if _lo <= _x <= _lo + _third:
        _ivals.append((_hi - _third, _hi))
        _kept.append("right")
    else:
        _ivals.append((_lo, _lo + _third))
        _kept.append("left")

_fig, _ax = plt.subplots(figsize=(8, 0.55 * (_n + 1) + 1.5))
for _k, (_lo, _hi) in enumerate(_ivals):
    _ax.plot([0, 1], [_k, _k], color="lightgray", linewidth=1, zorder=1)
    _ax.plot([float(_lo), float(_hi)], [_k, _k], color="C1", linewidth=7, solid_capstyle="butt", zorder=2)
    _ax.plot(float(_lo + _hi) / 2, _k, marker="|", color="C1", markersize=14, zorder=2)
for _k, _x in enumerate(_xs):
    _ax.plot(float(_x), _k, marker="x", color="black", markersize=9, markeredgewidth=2, zorder=3)
_ax.plot([], [], color="C1", linewidth=7, label=r"interval $[a_k, b_k]$")
_ax.plot([], [], marker="x", color="black", linestyle="none", markeredgewidth=2, label=r"listed rational $x_k$ to avoid")
_ax.set_yticks(range(_n + 1))
_ax.set_yticklabels([f"k = {_k}" for _k in range(_n + 1)])
_ax.set_ylim(_n + 0.6, -0.6)
_ax.set_xlim(-0.02, 1.02)
_ax.set_xlabel("real number line")
_ax.grid(visible=True, alpha=0.9, linewidth=0.4)
_ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=2, fontsize=8)
_ax.set_title("Nested intervals that avoid the listed rationals", style="italic")
_fig.tight_layout()

def _tex(_q):
    return str(_q.numerator) if _q.denominator == 1 else rf"\tfrac{{{_q.numerator}}}{{{_q.denominator}}}"

_rows = ["| $k$ | $x_k$ | kept third | $[a_{k+1}, b_{k+1}]$ |", "|---|---|---|---|"]
for _k, (_x, _side) in enumerate(zip(_xs, _kept)):
    _lo, _hi = _ivals[_k + 1]
    _rows.append(f"| {_k} | ${_tex(_x)}$ | {_side} | $[{_tex(_lo)}, {_tex(_hi)}]$ |")
_table = mo.md("\n".join(_rows))
mo.vstack([nested_slider, graphic(_fig), _table])
```

## Extended Real Numbers

Probabilities are real numbers in $[0, 1]$. But [Chapter 4](ch4_probability_spaces_v2.md) also needs *lengths*, and $\mathbb R$ has infinite length; and a sum of infinitely many nonnegative numbers can be infinite. To state such facts without special cases, we add two new elements, $\infty$ and $-\infty$.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Extended real numbers
: The set $\overline{\mathbb R} := \mathbb R \cup \{-\infty, +\infty\}$, where $-\infty$ and $+\infty$ are two distinct objects that are not real numbers, ordered by the order of $\mathbb R$ together with $-\infty < x < +\infty$ for every $x \in \mathbb R$ (and $-\infty < +\infty$). We write $\infty$ for $+\infty$ and $[0, \infty] := \{x \in \overline{\mathbb R} : x \ge 0\}$.
:::
::::

Which two objects we use does not matter.[^infinity-objects] Interval notation such as $(0, \infty]$ is used in $\overline{\mathbb R}$ as in $\mathbb R$. Arithmetic on $[0, \infty]$ extends that of the nonnegative real numbers by the conventions

- $a + \infty = \infty + a = \infty$ for every $a \in [0, \infty]$;
- $a \cdot \infty = \infty \cdot a = \infty$ for every $a \in (0, \infty]$, and $0 \cdot \infty = \infty \cdot 0 = 0$.

Subtraction and division involving $\infty$, such as $\infty - \infty$ and $\infty / \infty$, are left undefined; differences $a - b$ are used only for real numbers. The convention $0 \cdot \infty = 0$ expresses that a set of length $0$, repeated infinitely often, still has length $0$; Chapter 4 relies on it.

[^infinity-objects]: For example, $+\infty := \mathbb R$ and $-\infty := \{\mathbb R\}$ work. Regularity gives $\mathbb R \notin \mathbb R$. If $\{\mathbb R\} \in \mathbb R$, then the set $\{\mathbb R, \{\mathbb R\}\}$ would have no element disjoint from it, since $\{\mathbb R\} \in \mathbb R$ and $\mathbb R \in \{\mathbb R\}$, contradicting Regularity. The two objects are distinct because $\mathbb R \in \{\mathbb R\}$ but $\mathbb R \notin \mathbb R$.

:::{important icon=false} 📐 **Lemma (Arithmetic in $[0, \infty]$)**
On $[0, \infty]$, addition and multiplication are associative and commutative, multiplication distributes over addition, $a + 0 = a$ and $a \cdot 1 = a$, and $a \le b$ implies $a + c \le b + c$ and $a c \le b c$.
:::

:::{admonition icon=false} ✍️ **Proof**
When none of the numbers involved is $\infty$, these are rules for nonnegative real numbers: field axioms, ordered-field axiom 3, and Rules of Algebra parts 1 and 4. Otherwise, note that a sum is $\infty$ exactly when some summand is $\infty$, and a product is $0$ exactly when some factor is $0$, and is otherwise $\infty$ exactly when some factor is $\infty$.

- *Sums.* If some summand is $\infty$, both sides of the associative and commutative laws are $\infty$. For $a \le b$: if $c = \infty$ or $b = \infty$, then $b + c = \infty$; and $a = \infty$ forces $b = \infty$.
- *Products.* If some factor is $0$, both sides of the associative and commutative laws are $0$; otherwise all factors are positive, and if one is $\infty$, both sides are $\infty$. Also $\infty \cdot 1 = \infty$.
- *Distributivity,* $a(b + c) = ab + ac$. If $a = 0$, both sides are $0$. If $0 < a < \infty$ and $b$ or $c$ is $\infty$, both sides are $\infty$. If $a = \infty$, both sides are $\infty$ when $b > 0$ or $c > 0$, and both are $0$ when $b = c = 0$.
- *Monotonicity of products,* $a \le b \Rightarrow ac \le bc$. If $c = 0$, both sides are $0$. If $c > 0$ and $b = \infty$, then $bc = \infty$. If $c = \infty$ and $b < \infty$: when $a > 0$, also $b > 0$ and both sides are $\infty$; when $a = 0$, the left side is $0$. $\blacksquare$
:::

:::{caution icon=false} ⚠️ **Assumptions and Failure Modes**
- **No cancellation.** $1 + \infty = 2 + \infty$ and $1 \cdot \infty = 2 \cdot \infty$, although $1 \neq 2$. From $a + c = b + c$ we may conclude $a = b$ only when $c < \infty$. This is why Chapter 4 requires probabilities to be real numbers: its proofs subtract them.
- **No subtraction.** $\infty - \infty$ has no sensible value: any $x \in [0, \infty]$ satisfies $x + \infty = \infty$.
- **$0 \cdot \infty = 0$ is a convention.** It is convenient for lengths and probabilities, but it makes multiplication jump: $\tfrac1n \cdot \infty = \infty$ for every $n \in \mathbb N^+$, while $0 \cdot \infty = 0$.
:::
  
The definitions of upper bound and supremum make sense for subsets of $\overline{\mathbb R}$ with its order. In $\overline{\mathbb R}$ the least-upper-bound property holds without any proviso.

:::{important icon=false} 📐 **Lemma (Suprema in the Extended Reals)**
Every subset $S \subseteq \overline{\mathbb R}$ has a supremum in $\overline{\mathbb R}$. If $S \subseteq [0, \infty]$ is nonempty, then $\sup S \in [0, \infty]$.
:::

:::{admonition icon=false} ✍️ **Proof**
- If $+\infty \in S$, or $S \cap \mathbb R$ has no upper bound in $\mathbb R$, then $+\infty$ is the only upper bound of $S$, so $\sup S = +\infty$.
- If $S \subseteq \{-\infty\}$ (including $S = \emptyset$), every element of $\overline{\mathbb R}$ is an upper bound, and the least one is $-\infty$.
- Otherwise $S \cap \mathbb R$ is nonempty and bounded above in $\mathbb R$, and $+\infty \notin S$. Then $s := \sup(S \cap \mathbb R)$ exists in $\mathbb R$ by completeness, and $s$ is an upper bound of $S$ (also of $-\infty$, if present). Every upper bound of $S$ is either $+\infty$ or a real upper bound of $S \cap \mathbb R$, and in both cases it is $\ge s$; it cannot be $-\infty$, because $S \cap \mathbb R \neq \emptyset$.

If $S \subseteq [0, \infty]$ is nonempty, then $\sup S \ge s$ for some $s \in S$, so $\sup S \ge 0$. $\blacksquare$
:::

**Infinite sums.** For a sequence $(a_n)_{n=1}^\infty$ in $[0, \infty]$, the partial sums $\sum_{n=1}^N a_n$ never decrease as $N$ grows (we only add terms $\ge 0$), and by the lemma they always have a supremum in $[0, \infty]$. [Appendix C: Series](appendix_c_calculus_v2.md) defines $\sum_{n=1}^\infty a_n$ as this supremum, shows that it is the limit of the partial sums when they are bounded, and proves that such sums may be reordered and regrouped freely. So a series of nonnegative terms always has a value in $[0, \infty]$. This is what lets Chapter 4 add up infinitely many probabilities without first checking convergence. Two examples we use there:

- $\sum_{n=1}^\infty 0 = 0$, because every partial sum is $0$;
- $\sum_{n=1}^\infty c = \infty$ for every $c \in (0, \infty]$. If $c = \infty$, the first partial sum is already $\infty$. If $c$ is real, the $N$-th partial sum is $Nc$ (induction and distributivity), and for every real $u$ the Archimedean property gives $N > u/c$, so $Nc > u$; hence no real number is an upper bound.
  
## Summary

- The **complement** $A^c = \Omega \setminus A$ is taken relative to an ambient set $\Omega$. **De Morgan's laws** say that the complement of a union is the intersection of the complements and vice versa, for two sets and for any nonempty family.
- An **indexed family** is a function written with subscripts; a **sequence** is a family indexed by $\mathbb N$ or $\mathbb N^+$. Unions and intersections of families exist by Replacement and Union, and **disjointification** turns any sequence of sets into a pairwise **disjoint** one with the same unions.
- **Finite sums and products** are defined by recursion; their order does not matter, so sums over finite sets make sense.
- **Preimages** preserve unions, intersections, and complements; **images** preserve only unions. This is why random variables will be defined with preimages.
- **Injective**, **surjective**, and **bijective** functions; **composition**; and the **inverse function** of a bijection.
- A set is **countable** if it injects into $\mathbb N$, equivalently if it is **finite** or can be listed as a sequence. $\mathbb N \times \mathbb N$, $\mathbb Z$, and $\mathbb Q$ are countable, and so is a countable union of countable sets (using the Axiom of Choice). $\mathcal P(\mathbb N)$ and every interval $[a, b]$ with $a < b$ are **uncountable**.
- $\mathbb R$ is the **complete ordered field**. Completeness gives the Archimedean property and the density of $\mathbb Q$; we also have **absolute value** with the triangle inequality, and **intervals**.
- The **extended real numbers** add $\pm\infty$. On $[0, \infty]$ every set has a supremum, the conventions $a + \infty = \infty$ and $0 \cdot \infty = 0$ hold, and every series of nonnegative terms has a value.

## What's Next

[Chapter 4](ch4_probability_spaces_v2.md) uses all of this to define probability. Events are subsets of a sample space $\Omega$, and the collection of events is closed under complements and countable unions, where De Morgan's laws and indexed unions do the work. A probability measure adds up over sequences of disjoint events, with values in $[0, 1] \subseteq [0, \infty]$. Countability returns in two impossibility results: no probability treats all natural numbers equally, and, using the Axiom of Choice and the countability of $\mathbb Q$, no probability treats all subsets of $[0, 1)$ "uniformly". Before Chapter 4, read [Appendix C: Sequences and Limits](appendix_c_calculus_v2.md) and [Appendix C: Series](appendix_c_calculus_v2.md).