---
title: 'Appendix B: Constructing the Number Systems'
# marimo-version: 0.25.1
# css_file: notebook-styles.css
subtitle: "From Natural Numbers to Real Numbers"
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
---

```{marimo-config}
---
pyproject: |-
  dependencies = [
      "marimo>=0.25.1",
      "matplotlib==3.11.2",
  ]
---
```

```{marimo} python
:name: imports
:include: false

import marimo as mo
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

:::{seealso icon=false} 🔗 **Prerequisites**
- [Chapter 2](ch2_axioms_of_set_theory_v2.md): all of it, especially induction, the Recursion Theorem, Equality of Functions, and the recursive definitions of $+$, $\cdot$, and $<$ on $\mathbb N$.
- [Chapter 3](ch3_sets_for_probability_v2.md) (optional): the definitions of a {term}`field`, an {term}`ordered field`, an {term}`upper bound`, a {term}`supremum`, a {term}`complete ordered field`, and a {term}`bijective` function. Each is restated here where it is first needed, so this appendix can be read directly after Chapter 2.
:::
  
[Chapter 3](ch3_sets_for_probability_v2.md) works with the real numbers as a *complete ordered field*: a number system with the familiar arithmetic and order in which every nonempty set with an upper bound has a least upper bound. Every later chapter depends on that property. Limits, infinite sums, and integrals are all defined through least upper bounds ([Appendix C](appendix_c_calculus_v2.md)), and with them the probabilities, expectations, and variances that filters are built from.

This appendix shows that the property is not an extra assumption. Inside ZFC, starting from the natural numbers of [Chapter 2](ch2_axioms_of_set_theory_v2.md), we construct the integers $\mathbb Z$, the rational numbers $\mathbb Q$, and the real numbers $\mathbb R$, and prove that $\mathbb R$ is a complete ordered field. Along the way we see exactly what is missing from $\mathbb Q$: the rationals have a hole where $\sqrt 2$ should be.

:::{attention icon=false} 🗝️ **Key Idea**
Each number system is built from the previous one by a set-theoretic construction that repairs one defect. Integers are classes of pairs of natural numbers (adding subtraction), rational numbers are classes of pairs of integers (adding division), and real numbers are sets of rational numbers called Dedekind cuts (adding least upper bounds).
:::
  
## Arithmetic on the Natural Numbers

Chapter 2 defined, for all $m, n \in \mathbb N$,

$$m + 0 = m, \qquad m + (n + 1) = (m + n) + 1, \qquad m \cdot 0 = 0, \qquad m \cdot (n + 1) = m \cdot n + m,$$

where $n + 1 = \operatorname{succ}(n)$, together with $m < n :\Longleftrightarrow m \in n$ and $m \le n :\Longleftrightarrow (m < n \lor m = n)$. This section proves the Theorem (Arithmetic and Order on ℕ) stated there. Every proof is an induction on the variable that the recursion runs over. We write $mn$ for $m \cdot n$, and we use two facts from Chapter 2: the successor is injective on $\mathbb N$ (Peano axiom 4), and every natural number is $0$ or $n + 1$ for some $n \in \mathbb N$ (Zero or Successor).

:::{important icon=false} 📐 **Theorem (Addition on ℕ)**
For all $a, b, c \in \mathbb N$:

1. $0 + a = a$.
2. $(a + 1) + b = (a + b) + 1$.
3. $(a + b) + c = a + (b + c)$.
4. $a + b = b + a$.
5. If $a + c = b + c$, then $a = b$.
:::

:::{admonition icon=false} ✍️ **Proof**
1. Induction on $a$. $0 + 0 = 0$ by definition. If $0 + a = a$, then $0 + (a + 1) = (0 + a) + 1 = a + 1$.
2. Induction on $b$. For $b = 0$: $(a + 1) + 0 = a + 1 = (a + 0) + 1$. If the claim holds for $b$, then $(a + 1) + (b + 1) = \big((a + 1) + b\big) + 1 = \big((a + b) + 1\big) + 1 = \big(a + (b + 1)\big) + 1$.
3. Induction on $c$. For $c = 0$: $(a + b) + 0 = a + b = a + (b + 0)$. If the claim holds for $c$, then $(a + b) + (c + 1) = \big((a + b) + c\big) + 1 = \big(a + (b + c)\big) + 1 = a + \big((b + c) + 1\big) = a + \big(b + (c + 1)\big)$.
4. Induction on $b$. For $b = 0$: $a + 0 = a = 0 + a$ by part 1. If $a + b = b + a$, then $a + (b + 1) = (a + b) + 1 = (b + a) + 1 = (b + 1) + a$ by part 2.
5. Induction on $c$. For $c = 0$ there is nothing to prove. Suppose the claim holds for $c$, and $a + (c + 1) = b + (c + 1)$. Then $(a + c) + 1 = (b + c) + 1$, so $a + c = b + c$ because the successor is injective, so $a = b$ by the induction hypothesis. $\blacksquare$
:::

:::{important icon=false} 📐 **Theorem (Multiplication on ℕ)**
For all $a, b, c \in \mathbb N$:

1. $0 \cdot a = 0$ and $a \cdot 1 = a$.
2. $(a + 1)\,b = ab + b$.
3. $ab = ba$.
4. $a(b + c) = ab + ac$.
5. $(ab)c = a(bc)$.
:::

:::{admonition icon=false} ✍️ **Proof**
We use the laws of addition freely.

1. Induction on $a$: $0 \cdot 0 = 0$, and if $0 \cdot a = 0$, then $0 \cdot (a + 1) = 0 \cdot a + 0 = 0$. Also $a \cdot 1 = a \cdot (0 + 1) = a \cdot 0 + a = 0 + a = a$.
2. Induction on $b$. For $b = 0$ both sides are $0$. If the claim holds for $b$, then $(a + 1)(b + 1) = (a + 1)b + (a + 1) = (ab + b) + (a + 1) = (ab + a) + (b + 1) = a(b + 1) + (b + 1)$.
3. Induction on $b$. For $b = 0$: $a \cdot 0 = 0 = 0 \cdot a$ by part 1. If $ab = ba$, then $a(b + 1) = ab + a = ba + a = (b + 1)a$ by part 2.
4. Induction on $c$. For $c = 0$: $a(b + 0) = ab = ab + a \cdot 0$. If the claim holds for $c$, then $a\big(b + (c + 1)\big) = a\big((b + c) + 1\big) = a(b + c) + a = (ab + ac) + a = ab + a(c + 1)$.
5. Induction on $c$. For $c = 0$ both sides are $0$. If the claim holds for $c$, then $(ab)(c + 1) = (ab)c + ab = a(bc) + ab = a(bc + b) = a\big(b(c + 1)\big)$, using part 4. $\blacksquare$
:::
  
:::{important icon=false} 📐 **Theorem (Order on ℕ)**
For all $a, b, c \in \mathbb N$:

1. $a < b + 1 \leftrightarrow a \le b$, and $0 \le a$.
2. If $a < b$ and $b < c$, then $a < c$.
3. (Trichotomy) Exactly one of $a < b$, $a = b$, $b < a$ holds.
4. $a \le b$ iff $a + k = b$ for some $k \in \mathbb N$; this $k$ is then unique.
5. $a < b \leftrightarrow a + c < b + c$, and $a \le b \leftrightarrow a + c \le b + c$.
6. If $c \neq 0$: $a < b \leftrightarrow ac < bc$, and $ac = bc$ implies $a = b$.
7. If $ab = 0$, then $a = 0$ or $b = 0$.
8. (Well-ordering) Every nonempty $X \subseteq \mathbb N$ has a least element: some $m \in X$ with $m \le x$ for every $x \in X$.
:::

:::{admonition icon=false} ✍️ **Proof**
1. $a \in b \cup \{b\}$ iff $a \in b$ or $a = b$. Then $0 \le a$ by induction on $a$: $0 \le 0$, and if $0 \le a$, then $0 < a + 1$ by the first part.
2. $c$ is transitive (Chapter 2, Transitivity Lemma), so $b \in c$ gives $b \subseteq c$, and $a \in b$ gives $a \in c$.
3. *At most one holds:* $a < a$ is impossible because no set is an element of itself, and $a < b$ together with $b < a$ would give $a < a$ by part 2. *At least one holds:* first we show that $a < b$ implies $a + 1 \le b$, by induction on $b$. For $b = 0$ there is nothing to prove, since nothing is an element of $0$. If it holds for $b$ and $a < b + 1$, then either $a = b$, so $a + 1 = b + 1$, or $a < b$, so $a + 1 \le b < b + 1$ by the induction hypothesis; either way $a + 1 \le b + 1$. Now we prove "$a < b$ or $a = b$ or $b < a$ for every $b$" by induction on $a$. For $a = 0$ it holds because $0 \le b$. Suppose it holds for $a$, and let $b \in \mathbb N$. If $b < a$ or $b = a$, then $b < a + 1$ by part 1. If $a < b$, then $a + 1 \le b$ by the claim just shown. In every case the statement holds for $a + 1$.
4. ($\leftarrow$) $a \le a + k$, by induction on $k$: $a \le a + 0$, and if $a \le a + k$, then $a \le a + k < (a + k) + 1 = a + (k + 1)$. ($\rightarrow$) Induction on $b$. If $a \le 0$, then $a = 0$ (nothing is an element of $0$), and $a + 0 = 0$. If the claim holds for $b$ and $a \le b + 1$, then either $a = b + 1 = a + 0$, or $a < b + 1$, so $a \le b$ by part 1 and $a + k = b$ for some $k$, giving $a + (k + 1) = b + 1$. *Uniqueness:* if $a + k = a + k'$, then $k = k'$ by commutativity and cancellation.
5. ($\rightarrow$) By part 4, $b = a + k$, and $k \neq 0$ since $a \neq b$; so $k = j + 1$ for some $j$. Then $b + c = (a + c) + (j + 1) = \big((a + c) + j\big) + 1$, and $a + c \le (a + c) + j < \big((a + c) + j\big) + 1$, so $a + c < b + c$. ($\leftarrow$) If $a < b$ fails, then $b \le a$ by trichotomy, so $b + c \le a + c$ by ($\rightarrow$), which together with $a + c < b + c$ contradicts trichotomy. The statement for $\le$ follows by combining this with cancellation.
6. ($\rightarrow$) As in part 5, $b = a + k$ with $k \neq 0$. Write $k = j + 1$ and $c = i + 1$. Then $kc = ki + k = (ki + j) + 1$, so $bc = ac + kc = \big(ac + (ki + j)\big) + 1$, and $ac \le ac + (ki + j) < bc$ by parts 4 and 1. ($\leftarrow$) If $ac < bc$ but $a < b$ fails, then $b \le a$, so $bc \le ac$ by ($\rightarrow$), contradicting trichotomy. *Cancellation:* if $a \neq b$, then $a < b$ or $b < a$, so $ac < bc$ or $bc < ac$; either way $ac \neq bc$.
7. If $a \neq 0$ and $b \neq 0$, then $0 < a$ by part 1, so $0 = 0 \cdot b < ab$ by part 6, and $ab \neq 0$.
8. Suppose $X \subseteq \mathbb N$ has no least element; we show $X = \emptyset$. Let $T := \{n \in \mathbb N : n \cap X = \emptyset\}$, the set of $n$ with no element of $X$ below $n$. Then $0 \in T$. Let $n \in T$. If $(n + 1) \cap X$ had an element $y$, then $y \in n$ or $y = n$; the first contradicts $n \cap X = \emptyset$, so $n \in X$. But then $n$ would be a least element of $X$: for $x \in X$, $x \notin n$ (as $n \cap X = \emptyset$), so $n \le x$ by trichotomy. This contradicts the assumption, so $n + 1 \in T$. By induction, $T = \mathbb N$. Finally, if $x \in X$, then $x \in (x + 1) \cap X$, contradicting $x + 1 \in T$. So $X = \emptyset$. $\blacksquare$
:::

These three theorems together prove every item of Chapter 2's Theorem (Arithmetic and Order on ℕ). Part 4 also justifies subtraction where it makes sense: for $m \le n$ we write $n - m$ for the unique $k \in \mathbb N$ with $m + k = n$. For $m > n$ no such $k$ exists in $\mathbb N$; repairing that is the job of the integers.
  
## Equivalence Relations and Quotients

In $\mathbb N$, the expression $2 - 5$ has no value. The fix is to *represent* each missing number by the data that would produce it, for instance the pair $(2, 5)$ for "$2 - 5$", and to declare two representations equal when they ought to name the same number: $(2, 5)$ and $(0, 3)$ both stand for "$-3$". Equivalence relations make "ought to name the same number" precise, and quotient sets turn it into actual equality.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Equivalence relation
: A relation $\sim$ on a set $X$ is an equivalence relation iff it is reflexive, symmetric, and transitive:
  $$\forallin{x}{X}\,(x \sim x), \qquad \forallin{x}{X}\,\forallin{y}{X}\,(x \sim y \rightarrow y \sim x),$$
  $$\forallin{x}{X}\,\forallin{y}{X}\,\forallin{z}{X}\,\big((x \sim y \land y \sim z) \rightarrow x \sim z\big).$$
:::
::::

Equality on any set is an equivalence relation. For intuition[^display-informal]: a scale that displays weight to the nearest 0.1 lb treats two true weights as equivalent when they produce the same display. The order $<$ on $\mathbb N$ is transitive but neither reflexive nor symmetric, so it is not an equivalence relation.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Equivalence class
: For an equivalence relation $\sim$ on $X$ and $x \in X$, the equivalence class of $x$ is
  $$[x] := \{y \in X : y \sim x\},$$
  written $[x]_\sim$ when the relation must be named. Any element of a class is called a representative of it.
:::
::::

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Quotient set
: For an equivalence relation $\sim$ on $X$, the quotient set is the set of all equivalence classes,
  $$X/{\sim} := \{[x] : x \in X\},$$
  which is a set by Replacement.
:::
::::

In the scale example, each class is the set of true weights that produce one display value, and the quotient set corresponds to the set of possible displays.

:::{important icon=false} 📐 **Lemma (Equivalence Classes)**
Let $\sim$ be an equivalence relation on $X$. For all $x, y \in X$:

1. $x \in [x]$;
2. $[x] = [y] \leftrightarrow x \sim y$;
3. if $[x] \cap [y] \neq \emptyset$, then $[x] = [y]$.
:::

:::{admonition icon=false} ✍️ **Proof**
1. Reflexivity.
2. ($\leftarrow$) Suppose $x \sim y$. If $z \in [x]$, then $z \sim x$ and $x \sim y$, so $z \sim y$, that is, $z \in [y]$. If $z \in [y]$, then $z \sim y$ and $y \sim x$ (symmetry), so $z \in [x]$. By Extensionality, $[x] = [y]$. ($\rightarrow$) By part 1, $x \in [x] = [y]$, so $x \sim y$.
3. If $z \in [x] \cap [y]$, then $z \sim x$ and $z \sim y$, so $x \sim z$ and $z \sim y$, so $x \sim y$, and $[x] = [y]$ by part 2. $\blacksquare$
:::

So every element of $X$ lies in a class, and two classes are either equal or have no element in common: the classes form a {term}`partition` of $X$. Part 2 is the point of the construction. It converts the equivalence $x \sim y$ into the equality $[x] = [y]$.

[^display-informal]: This example uses real numbers informally; it is for intuition only.
  
To compute with classes we compute with representatives: for example, add two pairs and take the class of the result. This works only if the class of the result does not depend on which representatives we picked.

:::{important icon=false} 📐 **Lemma (Well-Definedness)**
Let $\sim$ be an equivalence relation on $X$.

1. Let $\star : X \times X \to X$ be *compatible* with $\sim$, meaning that $x \sim x'$ and $y \sim y'$ imply $x \star y \sim x' \star y'$. Then there is exactly one function $\circledast : (X/{\sim}) \times (X/{\sim}) \to X/{\sim}$ with $[x] \circledast [y] = [x \star y]$ for all $x, y \in X$.
2. Let $u : X \to X$ be compatible with $\sim$, meaning that $x \sim x'$ implies $u(x) \sim u(x')$. Then there is exactly one function $\bar u : X/{\sim} \to X/{\sim}$ with $\bar u([x]) = [u(x)]$ for all $x \in X$.
3. Let $\rho$ be a relation on $X$ compatible with $\sim$, meaning that $x \sim x'$, $y \sim y'$, and $x \mathrel{\rho} y$ imply $x' \mathrel{\rho} y'$. Then there is exactly one relation $\bar\rho$ on $X/{\sim}$ with $[x] \mathrel{\bar\rho} [y] \leftrightarrow x \mathrel{\rho} y$ for all $x, y \in X$.
:::

:::{admonition icon=false} ✍️ **Proof**
1. *Existence.* Let $\circledast := \{(([x], [y]), [x \star y]) : (x, y) \in X \times X\}$, a set by Replacement. Every element of $(X/{\sim}) \times (X/{\sim})$ has the form $([x], [y])$, so it is a first coordinate of some element of $\circledast$. Suppose two elements of $\circledast$ have the same first coordinate, $([x], [y]) = ([x'], [y'])$. Then $[x] = [x']$ and $[y] = [y']$ (Characteristic Property of Ordered Pairs), so $x \sim x'$ and $y \sim y'$ (Equivalence Classes, part 2), so $x \star y \sim x' \star y'$ (compatibility), so $[x \star y] = [x' \star y']$. Hence $\circledast$ is a function with the required property. *Uniqueness.* Any function with the property has the same domain as $\circledast$ and the same value at every $([x], [y])$, so it equals $\circledast$ by Equality of Functions.
2. The same argument with one argument instead of two.
3. Let $\bar\rho := \{([x], [y]) : (x, y) \in X \times X \land x \mathrel{\rho} y\}$. If $x \mathrel{\rho} y$, then $[x] \mathrel{\bar\rho} [y]$ by construction. Conversely, if $[x] \mathrel{\bar\rho} [y]$, then $([x], [y]) = ([x'], [y'])$ for some $x', y'$ with $x' \mathrel{\rho} y'$; then $x' \sim x$ and $y' \sim y$, and compatibility gives $x \mathrel{\rho} y$. Two relations on $X/{\sim}$ with the stated property contain exactly the same pairs, so $\bar\rho$ is unique. $\blacksquare$
:::

In each construction below, $x \star y = y \star x$ holds literally for representatives. Then compatibility needs checking in one argument only: if $x \sim x'$ always implies $x \star y \sim x' \star y$, then $x \star y \sim x' \star y = y \star x' \sim y' \star x' = x' \star y'$.

:::{caution icon=false} ⚠️ **Assumptions and Failure Modes**
Compatibility is essential. On pairs of natural numbers with nonzero second entry, read informally as fractions, let $(a, b) \approx (c, d) :\Longleftrightarrow ad = bc$. This is an equivalence relation: reflexivity and symmetry follow from commutativity, and if $ad = bc$ and $cf = de$, then $(af)d = (ad)f = (bc)f = b(cf) = b(de) = (be)d$, so $af = be$ by cancellation ($d \neq 0$; Order on ℕ, part 6). The rule "numerator plus denominator", $(a, b) \mapsto a + b$, is not compatible: $(1, 2) \approx (2, 4)$, but $1 + 2 = 3$ while $2 + 4 = 6$. So "the numerator plus the denominator of a fraction" is not a function of the fraction; the set built in the proof above would be a relation in which one class has two partners.
:::
  
## The Integers

We represent the integer "$a - b$" by the pair $(a, b) \in \mathbb N \times \mathbb N$. This reading is only a guide, since subtraction is not yet defined. Two pairs should represent the same integer when $a - b = c - d$, which can be said without subtraction as $a + d = b + c$.

:::{important icon=false} 📐 **Lemma**
The relation on $\mathbb N \times \mathbb N$ given by $(a, b) \sim (c, d) :\Longleftrightarrow a + d = b + c$ is an equivalence relation.
:::

:::{admonition icon=false} ✍️ **Proof**
Reflexivity ($a + b = b + a$) and symmetry follow from commutativity. For transitivity, suppose $a + d = b + c$ and $c + f = d + e$. Then, rearranging with the associative and commutative laws,
$$(a + f) + (c + d) = (a + d) + (c + f) = (b + c) + (d + e) = (b + e) + (c + d),$$
and cancellation gives $a + f = b + e$, that is, $(a, b) \sim (e, f)$. $\blacksquare$
:::

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Integers
: The set of integers is the quotient set
  $$\mathbb Z := (\mathbb N \times \mathbb N)/{\sim}, \qquad\text{where } (a, b) \sim (c, d) :\Longleftrightarrow a + d = b + c.$$
  Its elements are called integers; the class $[(a, b)]$ represents $a - b$.
:::
::::

Guided by $(a - b) + (c - d) = (a + c) - (b + d)$, $(a - b)(c - d) = (ac + bd) - (ad + bc)$, and $-(a - b) = b - a$, define on representatives

$$(a, b) \oplus (c, d) := (a + c,\ b + d), \qquad (a, b) \odot (c, d) := (ac + bd,\ ad + bc), \qquad \ominus(a, b) := (b, a),$$

$$(a, b) \prec (c, d) \;:\Longleftrightarrow\; a + d < b + c.$$

:::{important icon=false} 📐 **Lemma (Compatibility for ℤ)**
The functions $\oplus$, $\odot$, $\ominus$ and the relation $\prec$ are compatible with $\sim$.
:::

:::{admonition icon=false} ✍️ **Proof**
Suppose $(a, b) \sim (a', b')$, that is, $a + b' = b + a'$. Since $\oplus$ and $\odot$ are commutative on representatives (by the laws of $\mathbb N$), it suffices to vary the first argument.

- $\oplus$: $(a + c) + (b' + d) = (a + b') + (c + d) = (b + a') + (c + d) = (b + d) + (a' + c)$, which says $(a + c, b + d) \sim (a' + c, b' + d)$.
- $\odot$: let $s := a + b' = b + a'$. Then
  $$(ac + bd) + (a'd + b'c) = c(a + b') + d(b + a') = cs + ds = d(a + b') + c(b + a') = (ad + bc) + (a'c + b'd),$$
  which says $(ac + bd,\ ad + bc) \sim (a'c + b'd,\ a'd + b'c)$.
- $\ominus$: $b + a' = a + b'$ says $(b, a) \sim (b', a')$.
- $\prec$: suppose also $(c, d) \sim (c', d')$, that is, $c + d' = d + c'$, and $a + d < b + c$. Adding $b' + d'$ to both sides (Order on ℕ, part 5) and substituting gives $(b + d) + (a' + d') < (b + d) + (b' + c')$, and cancelling $b + d$ (part 5 again) gives $a' + d' < b' + c'$. $\blacksquare$
:::

By the Well-Definedness Lemma we obtain operations $+$, $\cdot$, $-$ and a relation $<$ on $\mathbb Z$ with

$$[(a, b)] + [(c, d)] = [(a + c,\ b + d)], \quad [(a, b)] \cdot [(c, d)] = [(ac + bd,\ ad + bc)], \quad -[(a, b)] = [(b, a)],$$

and $[(a, b)] < [(c, d)] \leftrightarrow a + d < b + c$. Let $0 := [(0, 0)]$ and $1 := [(1, 0)]$, write $x - y := x + (-y)$ and $x \le y :\Longleftrightarrow (x < y \lor x = y)$, and define $\iota : \mathbb N \to \mathbb Z$ by $\iota(n) := [(n, 0)]$.

:::{important icon=false} 📐 **Theorem (Properties of ℤ)**
1. For all $x, y, z \in \mathbb Z$: $(x + y) + z = x + (y + z)$, $x + y = y + x$, $x + 0 = x$, $x + (-x) = 0$, $(xy)z = x(yz)$, $xy = yx$, $x \cdot 1 = x$, and $x(y + z) = xy + xz$.
2. $0 \neq 1$, and if $xy = 0$, then $x = 0$ or $y = 0$.
3. For all $x, y, z \in \mathbb Z$: exactly one of $x < y$, $x = y$, $y < x$ holds; if $x < y$ and $y < z$, then $x < z$; if $x < y$, then $x + z < y + z$; and if $0 < x$ and $0 < y$, then $0 < xy$.
4. $\iota$ is injective, $\iota(m + n) = \iota(m) + \iota(n)$, $\iota(mn) = \iota(m)\iota(n)$, and $m < n \leftrightarrow \iota(m) < \iota(n)$. Every integer equals $\iota(n)$ or $-\iota(n)$ for some $n \in \mathbb N$; the integers $x$ with $0 \le x$ are exactly the $\iota(n)$, and those with $0 < x$ are the $\iota(n)$ with $n \neq 0$.
:::

:::{admonition icon=false} ✍️ **Proof**
Write $x = [(a, b)]$, $y = [(c, d)]$, $z = [(e, f)]$. We prove part 4 before part 3, which uses it.

- *Part 1.* Every identity except $x + (-x) = 0$ holds already for representatives, as an equality of pairs, by the laws of $\mathbb N$. For example, for associativity of multiplication both $\big((a, b) \odot (c, d)\big) \odot (e, f)$ and $(a, b) \odot \big((c, d) \odot (e, f)\big)$ equal $(ace + adf + bcf + bde,\ acf + ade + bce + bdf)$, and $(a, b) \odot (1, 0) = (a, b)$. For the additive inverse, $(a, b) \oplus (b, a) = (a + b, b + a) \sim (0, 0)$, because $(a + b) + 0 = (b + a) + 0$.
- *Part 4.* $[(m, 0)] = [(n, 0)]$ iff $m + 0 = 0 + n$ iff $m = n$. Also $(m, 0) \oplus (n, 0) = (m + n, 0)$, $(m, 0) \odot (n, 0) = (mn, 0)$, and $(m, 0) \prec (n, 0)$ iff $m < n$. For $x = [(a, b)]$, trichotomy in $\mathbb N$ gives $b \le a$ or $a \le b$. If $b \le a$, then $a = b + k$ for some $k$ (Order on ℕ, part 4), so $(a, b) \sim (k, 0)$ and $x = \iota(k)$. If $a \le b$, then $b = a + k$, so $(a, b) \sim (0, k)$ and $x = -\iota(k)$. Finally, $0 < \iota(k)$ iff $0 < k$, while $0 < -\iota(k) = [(0, k)]$ would mean $k < 0$, which is impossible; so the integers $> 0$ are the $\iota(n)$ with $n \neq 0$, and those $\ge 0$ are the $\iota(n)$.
- *Part 3.* *Trichotomy:* $x < y$, $x = y$, $y < x$ mean $a + d < b + c$, $a + d = b + c$, $b + c < a + d$, and exactly one of these holds in $\mathbb N$. *Transitivity:* from $a + d < b + c$ and $c + f < d + e$, applying Order on ℕ, part 5, twice gives $(a + d) + (c + f) < (b + c) + (d + e)$, that is, $(a + f) + (c + d) < (b + e) + (c + d)$, and cancelling $c + d$ (part 5) gives $a + f < b + e$. *Addition:* $(a + e) + (d + f) < (b + f) + (c + e)$ iff $a + d < b + c$, by part 5. *Multiplication:* by part 4, $0 < x$ and $0 < y$ give $x = \iota(m)$ and $y = \iota(n)$ with $m, n \neq 0$, so $xy = \iota(mn)$ with $mn \neq 0$ (Order on ℕ, part 7), and $0 < xy$.
- *Part 2.* $(0, 0) \sim (1, 0)$ would mean $0 + 0 = 0 + 1$, which is false. Now suppose $x \neq 0$ and $xy = 0$. Then $a \neq b$. If $b < a$, write $a = b + k$ with $k \neq 0$; the equation $xy = 0$ says $ac + bd = ad + bc$, that is, $(b + k)c + bd = (b + k)d + bc$, so $kc = kd$ after cancelling $bc + bd$, and $c = d$ by Order on ℕ, part 6. So $y = [(c, c)] = 0$. The case $a < b$ is symmetric. $\blacksquare$
:::

With $x - y := x + (-y)$ we get $[(a, b)] = \iota(a) - \iota(b)$, because $[(a, 0)] + [(0, b)] = [(a, b)]$; so the class of $(a, b)$ really is "$a - b$".
  
:::{tip icon=false} **Identifying ℕ ⊆ ℤ ⊆ ℚ ⊆ ℝ**
Strictly speaking, $\mathbb N$ is not a subset of $\mathbb Z$: the integer $\iota(n) = [(n, 0)]$ is a set of ordered pairs, not the von Neumann numeral $n$. But $\iota$ is injective and preserves $+$, $\cdot$, and $<$, so every statement about natural numbers translates into the same statement about their images. We therefore *identify* each $n \in \mathbb N$ with $\iota(n)$ and write $\mathbb N \subseteq \mathbb Z$. (If one insists on a literal inclusion, one can replace $\mathbb Z$ by an isomorphic copy that contains $\mathbb N$ itself; nothing in the theory changes.) The same remark applies to the embeddings $\mathbb Z \to \mathbb Q$ and $\mathbb Q \to \mathbb R$ below. With these identifications, $\mathbb N \subseteq \mathbb Z \subseteq \mathbb Q \subseteq \mathbb R$, every integer is $m - n$ for some $m, n \in \mathbb N$, and the positive integers are the elements of $\mathbb N \setminus \{0\}$.
:::
  
## The Rational Numbers

**The goal.** We now repeat the construction with multiplication in place of addition, aiming for an ordered field. We use the standard axioms, as in [Chapter 3](ch3_sets_for_probability_v2.md). A {term}`field` is a set $F$ with two functions $+, \cdot : F \times F \to F$ and two elements $0 \neq 1$ of $F$ such that, for all $x, y, z \in F$:

| | addition | multiplication |
|---|---|---|
| associativity | $(x + y) + z = x + (y + z)$ | $(xy)z = x(yz)$ |
| commutativity | $x + y = y + x$ | $xy = yx$ |
| identity | $x + 0 = x$ | $x \cdot 1 = x$ |
| inverses | some $-x \in F$ has $x + (-x) = 0$ | if $x \neq 0$, some $x^{-1} \in F$ has $x x^{-1} = 1$ |
| distributivity | $x(y + z) = xy + xz$ | |

An {term}`ordered field` is a field with a relation $<$ such that, for all $x, y, z$: exactly one of $x < y$, $x = y$, $y < x$ holds (trichotomy); $x < y$ and $y < z$ imply $x < z$ (transitivity); $x < y$ implies $x + z < y + z$ (addition); and $0 < x$ and $0 < y$ imply $0 < xy$ (multiplication). We write $x \le y$ for "$x < y$ or $x = y$", and $x - y := x + (-y)$. By the Theorem (Properties of ℤ), $\mathbb Z$ satisfies all of these axioms except the existence of multiplicative inverses.

The usual rules for inequalities follow from these axioms. We need them both in $\mathbb Z$ and in ordered fields.

:::{important icon=false} 📐 **Lemma (Inequality Rules)**
Let $R$ be $\mathbb Z$ or an ordered field. For all $x, y, z \in R$:

1. $x < y \leftrightarrow 0 < y - x$.
2. If $0 < z$, then $x < y \leftrightarrow xz < yz$ and $x \le y \leftrightarrow xz \le yz$.
3. If $x \neq 0$, then $0 < x^2$; in particular $0 < 1$.
4. If $R$ is an ordered field and $0 < x$, then $0 < x^{-1}$.
5. If $0 \le x < y$, then $x^2 < y^2$; and if $0 \le x$, $0 \le y$, and $x^2 < y^2$, then $x < y$.
:::

:::{admonition icon=false} ✍️ **Proof**
The ring laws give $x \cdot 0 = 0$ (from $x \cdot 0 = x(0 + 0) = x \cdot 0 + x \cdot 0$), $(-x)y = -(xy)$ (since $(-x)y + xy = (-x + x)y = 0$), and hence $(-x)(-y) = xy$.

1. Add $-x$ to both sides of $x < y$ (addition axiom); for the converse, add $x$.
2. If $x < y$, then $0 < y - x$ by part 1, so $0 < (y - x)z = yz - xz$ by the multiplication axiom, and $xz < yz$ by part 1. Conversely, if $xz < yz$ but $x < y$ fails, then $y \le x$ by trichotomy, so $yz \le xz$, which contradicts trichotomy. The statement for $\le$ follows, because $x = y$ implies $xz = yz$, and $xz = yz$ implies $x = y$ (otherwise $x < y$ or $y < x$ would give $xz \neq yz$).
3. If $0 < x$, then $0 < x \cdot x$ by the multiplication axiom. If $x < 0$, then $0 < -x$ by part 1, and $x^2 = (-x)(-x) > 0$. In particular $0 < 1 \cdot 1 = 1$.
4. $x^{-1} \neq 0$, since $x x^{-1} = 1 \neq 0 = x \cdot 0$. If $x^{-1} < 0$, then part 2 with $z = x$ gives $1 = x^{-1}x < 0 \cdot x = 0$, contradicting part 3.
5. If $0 \le x < y$, then $0 < y$, so $x \cdot x \le x \cdot y$ (by part 2 if $0 < x$, and trivially if $x = 0$) and $x \cdot y < y \cdot y$ (part 2); hence $x^2 < y^2$. For the second claim: if $y \le x$, then $y^2 \le x^2$ by the first claim (or equality), contradicting $x^2 < y^2$. $\blacksquare$
:::
  
**The construction.** Represent the fraction "$a / b$" by a pair $(a, b)$ of integers with $b \neq 0$, and declare $(a, b)$ and $(c, d)$ equivalent when $a/b = c/d$, which can be said without division as $ad = bc$. Let $\mathbb Z^* := \mathbb Z \setminus \{0\}$.

:::{important icon=false} 📐 **Lemma**
The relation on $\mathbb Z \times \mathbb Z^*$ given by $(a, b) \approx (c, d) :\Longleftrightarrow ad = bc$ is an equivalence relation.
:::

:::{admonition icon=false} ✍️ **Proof**
Reflexivity and symmetry follow from commutativity. For transitivity, suppose $ad = bc$ and $cf = de$. Then $(af)d = (ad)f = (bc)f = b(cf) = b(de) = (be)d$, so $(af - be)d = 0$. Since $d \neq 0$ and $\mathbb Z$ has no zero divisors, $af = be$. $\blacksquare$
:::

This is exactly where the construction needs $\mathbb Z$ to have no zero divisors.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Rational numbers
: The set of rational numbers is the quotient set
  $$\mathbb Q := (\mathbb Z \times \mathbb Z^*)/{\approx}, \qquad\text{where } \mathbb Z^* := \mathbb Z \setminus \{0\} \text{ and } (a, b) \approx (c, d) :\Longleftrightarrow ad = bc.$$
  Its elements are called rational numbers, and we write $a/b := [(a, b)]$, so that $a/b = c/d \leftrightarrow ad = bc$.
:::
::::

Define on representatives (the denominators $bd$ are nonzero because $\mathbb Z$ has no zero divisors)

$$\frac ab + \frac cd := \frac{ad + bc}{bd}, \qquad \frac ab \cdot \frac cd := \frac{ac}{bd}, \qquad -\frac ab := \frac{-a}{b}, \qquad \Big(\frac ab\Big)^{-1} := \frac ba \quad (a \neq 0).$$

Each is compatible with $\approx$; as before, it suffices to vary the first argument. Suppose $ab' = a'b$. For addition, $(ad + bc)\,b'd = (ab')d^2 + bb'cd = (a'b)d^2 + bb'cd = bd\,(a'd + b'c)$. For multiplication, $(ac)(b'd) = (ab')(cd) = (a'b)(cd) = (bd)(a'c)$. For the negative, $(-a)b' = -(a'b) = b(-a')$. For the inverse, $a/b = 0/1$ iff $a = 0$, so we apply the Well-Definedness Lemma on $\mathbb Z^* \times \mathbb Z^*$: if $a, a' \neq 0$ and $ab' = a'b$, then $ba' = ab'$, which says $b/a = b'/a'$.

**Order.** Every rational has a representative with a positive denominator, because $(a, b) \approx (-a, -b)$. For positive denominators we want $a/b < c/d \leftrightarrow ad < bc$. To define a relation on *all* representatives, multiply both sides by $bd$:

$$(a, b) \prec (c, d) \;:\Longleftrightarrow\; (ad)(bd) < (bc)(bd).$$

Both sides are unchanged when $(a, b)$ is replaced by $(-a, -b)$ or $(c, d)$ by $(-c, -d)$, and when $b, d > 0$ the condition is equivalent to $ad < bc$ (Inequality Rules, part 2, with $z = bd > 0$). So compatibility only needs checking for positive denominators: if $b, b', d, d' > 0$, $ab' = a'b$, $cd' = c'd$, and $ad < bc$, then multiplying by $b'd' > 0$ gives $(ab')(dd') < (cd')(bb')$, that is, $(a'd')(bd) < (b'c')(bd)$, and cancelling $bd > 0$ (part 2) gives $a'd' < b'c'$.

:::{important icon=false} 📐 **Theorem (Properties of ℚ)**
1. $\mathbb Q$, with the operations above, $0 := 0/1$, $1 := 1/1$, and $<$, is an ordered field.
2. $\iota : \mathbb Z \to \mathbb Q$, $\iota(a) := a/1$, is injective and preserves $+$, $\cdot$, and $<$.
3. (Density) If $p < q$ in $\mathbb Q$, then $p < \tfrac{p + q}{2} < q$, where $2 := 1 + 1$ and $\tfrac{x}{2} := x \cdot 2^{-1}$.
:::

:::{admonition icon=false} ✍️ **Proof**
1. Each field axiom reduces to the laws of $\mathbb Z$. Some hold already for representatives: for instance, both $(a/b + c/d) + e/f$ and $a/b + (c/d + e/f)$ have the representative $(adf + bcf + bde,\ bdf)$. The others hold up to $\approx$, using $(bu)/(bv) = u/v$ for $b \neq 0$ (because $(bu)v = (bv)u$). For example, $a/b + (-a)/b = 0/b^2 = 0/1$; $(a/b)(b/a) = (ab)/(ba) = 1/1$; and both sides of the distributive law reduce to $(acf + ade)/(bdf)$. Also $0/1 \neq 1/1$ because $0 \cdot 1 \neq 1 \cdot 1$. For the order axioms, take positive denominators $b, d, f$. *Trichotomy* comes from trichotomy in $\mathbb Z$, since $a/b = c/d$ iff $ad = bc$. *Transitivity:* from $ad < bc$ and $cf < de$, multiplying by $f$ and by $b$ gives $adf < bcf < bde$, so $(af)d < (be)d$, and cancelling $d$ gives $af < be$. *Addition:* $a/b + e/f < c/d + e/f$ means $(af + be)(df) < (cf + de)(bf)$, that is, $adf^2 < bcf^2$, which holds iff $ad < bc$ because $f^2 > 0$. *Multiplication:* $0 < a/b$ iff $0 < a$, so $0 < a/b$ and $0 < c/d$ give $0 < ac$, that is, $0 < (ac)/(bd)$.
2. $a/1 = c/1$ iff $a = c$; $a/1 + c/1 = (a + c)/1$; $(a/1)(c/1) = (ac)/1$; and $a/1 < c/1$ iff $a < c$.
3. From $p < q$, the addition axiom gives $p + p < p + q$, that is, $2p < p + q$. Also $0 < 1$ gives $1 < 2$, so $0 < 2$ and $0 < 2^{-1}$ (Inequality Rules, parts 3 and 4). Multiplying by $2^{-1}$ gives $p < \tfrac{p + q}{2}$. Likewise $p + q < 2q$ gives $\tfrac{p + q}{2} < q$. $\blacksquare$
:::

As with $\mathbb Z$, we identify $a \in \mathbb Z$ with $a/1$, so $\mathbb Z \subseteq \mathbb Q$. Then $a/b = a \cdot b^{-1}$, every rational number equals $a/b$ for some $a \in \mathbb Z$ and some positive integer $b$, and a rational $a/b$ with $b > 0$ is positive iff $a > 0$.
  
## Incompleteness of the Rationals

$\mathbb Q$ is dense (between any two rationals lies a third), yet it has holes. To say this precisely we need the following notions, restated from [Chapter 3](ch3_sets_for_probability_v2.md), for a subset $S$ of an ordered field $F$ (they use only the order, so they make sense for any set with a relation $<$ satisfying trichotomy and transitivity):

- $u \in F$ is an {term}`upper bound` of $S$ iff $s \le u$ for every $s \in S$, and $S$ is *bounded above* iff it has an upper bound in $F$;
- $\sigma \in F$ is a {term}`supremum` (least upper bound) of $S$ iff $\sigma$ is an upper bound of $S$ and $\sigma \le u$ for every upper bound $u$ of $S$.

A set has at most one supremum, since two suprema are each $\le$ the other.

:::{important icon=false} 📐 **Lemma (No Rational Square Root of 2)**
No $q \in \mathbb Q$ satisfies $q^2 = 2$.
:::

:::{admonition icon=false} ✍️ **Proof**
Suppose $q^2 = 2$ and write $q = a/b$ with $b > 0$. Then $a \neq 0$ (since $0^2 \neq 2$), and replacing $q$ by $-q$ if necessary, $a > 0$. Now $a^2/b^2 = 2/1$ means $a^2 = 2b^2$ in $\mathbb Z$. So the set
$$B := \{b \in \mathbb N : b > 0 \land \existsin{a}{\mathbb N}\,(a > 0 \land a^2 = 2b^2)\}$$
is nonempty, and by well-ordering it has a least element $b$; fix $a > 0$ with $a^2 = 2b^2$. Since $b^2 > 0$, we have $b^2 < 2b^2 = a^2 < 4b^2 = (2b)^2$, so $b < a < 2b$ by Inequality Rules, part 5. Let $a' := 2b - a$ and $b' := a - b$. Both are positive, and $b' < b$ because $a < 2b$. Using $a^2 = 2b^2$ twice,
$$a'^2 = 4b^2 - 4ab + a^2 = 3a^2 - 4ab, \qquad 2b'^2 = 2a^2 - 4ab + 2b^2 = 3a^2 - 4ab.$$
So $a'^2 = 2b'^2$ with $0 < b' < b$, that is, $b' \in B$, contradicting the minimality of $b$. $\blacksquare$
:::

The proof of the next theorem uses one explicit map. For a rational $p > 0$, let

$$\varphi(p) := \frac{2p + 2}{p + 2}, \qquad\text{so that}\qquad \varphi(p) - p = \frac{2 - p^2}{p + 2} \quad\text{and}\quad \varphi(p)^2 - 2 = \frac{2(p^2 - 2)}{(p + 2)^2}.$$

Both identities are direct computations. Since $p + 2 > 0$, they show: if $p^2 < 2$, then $\varphi(p) > p$ and $\varphi(p)^2 < 2$; if $p^2 > 2$, then $0 < \varphi(p) < p$ and $\varphi(p)^2 > 2$. In words, $\varphi$ moves any positive rational strictly closer to the hole while staying on the same side of it.

:::{important icon=false} 📐 **Theorem (Incompleteness of ℚ)**
The set $S := \{q \in \mathbb Q : q < 0 \lor q^2 < 2\}$ is nonempty and bounded above in $\mathbb Q$, but it has no supremum in $\mathbb Q$.
:::

:::{admonition icon=false} ✍️ **Proof**
*Nonempty:* $0 \in S$. *Bounded above by 2:* if $q \in S$ and $2 < q$, then $q > 0$, and $4 < q^2$ by Inequality Rules, part 5, so $q \notin S$, a contradiction. Hence $q \le 2$ for every $q \in S$.

*No supremum.* Suppose $\sigma \in \mathbb Q$ is a supremum of $S$. Since $1 \in S$, $\sigma \ge 1 > 0$. By the Lemma, $\sigma^2 \neq 2$, so there are two cases.

- If $\sigma^2 < 2$, then $\varphi(\sigma) \in S$ and $\varphi(\sigma) > \sigma$, so $\sigma$ is not an upper bound of $S$.
- If $\sigma^2 > 2$, then $\varphi(\sigma) < \sigma$, and $\varphi(\sigma)$ is an upper bound of $S$: if some $q \in S$ had $q > \varphi(\sigma) > 0$, then $q^2 > \varphi(\sigma)^2 > 2$ and $q > 0$, so $q \notin S$. So $\sigma$ is not the *least* upper bound.

Both cases contradict the assumption. $\blacksquare$
:::

In $\mathbb Q$, then, a bounded set can fail to have a least upper bound. For filtering this would be fatal: square roots (such as a standard deviation), limits, and infinite sums all rely on least upper bounds existing.

The explorer below lists every rational between 1 and 2 whose denominator (in lowest terms) is at most $N$, split by membership in $S$. As $N$ grows, the largest element of $S$ shown and the smallest upper bound shown close in on $\sqrt 2 \approx 1.41421$, yet $\varphi$ always produces a larger element of $S$ and a smaller upper bound: $S$ has no largest element, and there is no least rational upper bound.

```{marimo} python
:hide-code: true

denominator_slider = mo.ui.slider(
    start=1, stop=40, step=1, value=6, show_value=True, label=r"largest denominator $N$"
)
```

```{marimo} python
:hide-code: true

_N = denominator_slider.value

def _in_S(r):
    return r < 0 or r * r < 2

def _phi(p):
    return (2 * p + 2) / (p + 2)

def _frac(r):
    return rf"\tfrac{{{r.numerator}}}{{{r.denominator}}}"

_rats = sorted({Fraction(p, q) for q in range(1, _N + 1) for p in range(q, 2 * q + 1)})
_inside = [r for r in _rats if _in_S(r)]
_outside = [r for r in _rats if not _in_S(r)]
_lo, _hi = max(_inside), min(_outside)
_lo_next, _hi_next = _phi(_lo), _phi(_hi)

_fig, _ax = plt.subplots(figsize=(7, 3.6))
_ax.plot([float(r) for r in _inside], [r.denominator for r in _inside], "o",
         color="C0", markersize=4, label=r"in $S$ ($q^2 < 2$)")
_ax.plot([float(r) for r in _outside], [r.denominator for r in _outside], "o",
         mfc="none", mec="C3", markersize=4, label=r"upper bound of $S$ ($q^2 > 2$)")
_ax.axvline(2 ** 0.5, color="black", linestyle=":", linewidth=1, label=r"$\sqrt{2}$ (not rational)")
_ax.set_xlim(0.98, 2.02)
_ax.set_ylim(0, 41)
_ax.set_xlabel("rational number $q$ (dimensionless)")
_ax.set_ylabel("denominator in lowest terms")
_ax.set_title(f"Rationals in [1, 2] with denominator at most {_N}", style="italic")
_ax.grid(visible=True, alpha=0.9, linewidth=0.4)
_ax.legend(loc="upper right", fontsize=8)
_fig.tight_layout()
_plot = graphic(_fig)
plt.close(_fig)

_rows = [
    ("largest element of $S$ shown", _lo, _in_S(_lo)),
    (r"$\varphi$ of it: a larger element of $S$", _lo_next, _in_S(_lo_next)),
    ("smallest upper bound shown", _hi, _in_S(_hi)),
    (r"$\varphi$ of it: a smaller upper bound", _hi_next, _in_S(_hi_next)),
]
_table = "| | rational | decimal | in $S$? |\n|---|---|---|---|\n" + "\n".join(
    f"| {_label} | ${_frac(_r)}$ | {float(_r):.6f} | {'yes' if _ins else 'no'} |"
    for _label, _r, _ins in _rows
)
_gap = float(_hi - _lo)
mo.vstack([
    denominator_slider,
    _plot,
    mo.md(_table + f"\n\nGap between the smallest upper bound and the largest element shown: {_gap:.6f}."),
])
```

## The Real Numbers

The set $S$ above "points at" a number that $\mathbb Q$ lacks, and it is completely determined by that number: it consists of the rationals below it. [Dedekind](https://en.wikipedia.org/wiki/Dedekind_cut) (1872) turned this around: *define* a real number to be such a set of rationals[^cauchy].

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Dedekind cut
: A Dedekind cut is a set $\alpha \subseteq \mathbb Q$ that is neither $\emptyset$ nor $\mathbb Q$, is downward closed, $\forallin{p}{\alpha}\,\forallin{q}{\mathbb Q}\,(q < p \rightarrow q \in \alpha)$, and has no greatest element, $\forallin{p}{\alpha}\,\existsin{q}{\alpha}\,(p < q)$.
:::
::::

We define

$$\mathbb R := \{\alpha \in \mathcal P(\mathbb Q) : \alpha \text{ is a Dedekind cut}\},$$

a set by Power Set and Separation. In this section, lowercase Greek letters $\alpha, \beta, \gamma, \sigma$ denote cuts.

:::{important icon=false} 📐 **Lemma (Rational Cuts)**
For $r \in \mathbb Q$, the set $r^* := \{q \in \mathbb Q : q < r\}$ is a Dedekind cut, and $r^* = s^*$ implies $r = s$.
:::

:::{admonition icon=false} ✍️ **Proof**
$r - 1 \in r^*$ and $r \notin r^*$, so $r^*$ is neither $\emptyset$ nor $\mathbb Q$. It is downward closed because $q < p < r$ implies $q < r$. It has no greatest element: if $q < r$, then $q < \tfrac{q + r}{2} < r$ by density. Finally, if $r < s$, then $r \in s^* \setminus r^*$, so $r^* \neq s^*$; likewise if $s < r$. By trichotomy, $r^* = s^*$ forces $r = s$. $\blacksquare$
:::

:::{important icon=false} 📐 **Theorem (The Cut at √2)**
The set $S = \{q \in \mathbb Q : q < 0 \lor q^2 < 2\}$ is a Dedekind cut, and $S \neq r^*$ for every $r \in \mathbb Q$.
:::

:::{admonition icon=false} ✍️ **Proof**
$0 \in S$ and $2 \notin S$. *Downward closed:* let $p \in S$ and $q < p$. If $q < 0$, then $q \in S$. Otherwise $0 \le q < p$, so $p > 0$, hence $p^2 < 2$, and $q^2 < p^2 < 2$ (Inequality Rules, part 5), so $q \in S$. *No greatest element:* if $p < 0$, then $0 \in S$ is larger; if $p = 0$, then $1 \in S$ is larger; if $p > 0$, then $\varphi(p) \in S$ is larger. *Not rational:* $r$ is a supremum of $r^*$ in $\mathbb Q$. Indeed, $r$ is an upper bound of $r^*$, and if $u < r$, then $\tfrac{u + r}{2} \in r^*$ exceeds $u$, so $u$ is not an upper bound; hence every upper bound is $\ge r$. Since $S$ has no supremum in $\mathbb Q$, $S \neq r^*$. $\blacksquare$
:::

This cut is the real number $\sqrt 2$.

**Order.** For cuts, define $\alpha < \beta :\Longleftrightarrow (\alpha \subseteq \beta \land \alpha \neq \beta)$, so that $\alpha \le \beta$ iff $\alpha \subseteq \beta$.

:::{important icon=false} 📐 **Theorem (Order on ℝ)**
For all cuts $\alpha$, $\beta$, $\gamma$: exactly one of $\alpha < \beta$, $\alpha = \beta$, $\beta < \alpha$ holds, and $\alpha < \beta$ and $\beta < \gamma$ imply $\alpha < \gamma$. For all $r, s \in \mathbb Q$: $r < s \leftrightarrow r^* < s^*$.
:::

:::{admonition icon=false} ✍️ **Proof**
*Any two cuts are comparable under $\subseteq$:* suppose $\alpha \not\subseteq \beta$, and pick $p \in \alpha \setminus \beta$. Let $q \in \beta$. If $p \le q$, then $p \in \beta$ (by downward closure, or because $p = q$), which is false; so $q < p$, and $q \in \alpha$ by downward closure of $\alpha$. Hence $\beta \subseteq \alpha$. *Trichotomy:* by comparability, at least one of $\alpha \subsetneq \beta$, $\alpha = \beta$, $\beta \subsetneq \alpha$ holds; $\alpha \subsetneq \beta$ and $\beta \subsetneq \alpha$ cannot both hold by Double Inclusion, and neither is compatible with $\alpha = \beta$. *Transitivity:* $\alpha \subseteq \beta \subseteq \gamma$ gives $\alpha \subseteq \gamma$, and $\alpha = \gamma$ would give $\beta \subseteq \alpha$, hence $\alpha = \beta$, which is false. *Rationals:* if $r < s$, then $r^* \subseteq s^*$ (since $q < r$ implies $q < s$) and $r \in s^* \setminus r^*$, so $r^* < s^*$. The converse follows by trichotomy in $\mathbb Q$ and in $\mathbb R$. $\blacksquare$
:::

[^cauchy]: The other standard construction takes equivalence classes of Cauchy sequences of rationals ([Appendix C](appendix_c_calculus_v2.md)) under the relation "the difference tends to 0". It uses the quotient construction again and generalizes to completing other spaces. Dedekind cuts need no sequences and make order and suprema immediate. See [Construction of the real numbers](https://en.wikipedia.org/wiki/Construction_of_the_real_numbers).
  
**Completeness.** This is exactly the property that $\mathbb Q$ lacks.

:::{important icon=false} 📐 **Theorem (Least-Upper-Bound Property)**
Every nonempty set $\mathcal A \subseteq \mathbb R$ that is bounded above has a supremum in $\mathbb R$, namely $\bigcup \mathcal A$.
:::

:::{admonition icon=false} ✍️ **Proof**
Let $\beta$ be an upper bound of $\mathcal A$, and let $\sigma := \bigcup \mathcal A$, a set by the Axiom of Union. First, $\sigma$ is a cut:

- $\sigma \neq \emptyset$, because $\mathcal A$ has an element $\alpha$, and $\alpha \neq \emptyset$.
- $\sigma \neq \mathbb Q$, because every $\alpha \in \mathcal A$ satisfies $\alpha \subseteq \beta$, so $\sigma \subseteq \beta \neq \mathbb Q$.
- $\sigma$ is downward closed: if $p \in \sigma$, then $p \in \alpha$ for some $\alpha \in \mathcal A$, and $q < p$ gives $q \in \alpha \subseteq \sigma$.
- $\sigma$ has no greatest element: if $p \in \alpha \in \mathcal A$, some $q \in \alpha \subseteq \sigma$ has $q > p$.

Next, $\sigma$ is an upper bound of $\mathcal A$, because $\alpha \subseteq \bigcup \mathcal A$ for every $\alpha \in \mathcal A$. Finally, if $\gamma$ is any upper bound of $\mathcal A$, then $\alpha \subseteq \gamma$ for every $\alpha \in \mathcal A$, so $\sigma \subseteq \gamma$, that is, $\sigma \le \gamma$. $\blacksquare$
:::

:::{caution icon=false} ⚠️ **Assumptions and Failure Modes**
- **$\mathcal A$ must be nonempty.** For $\mathcal A = \emptyset$, the union $\bigcup \emptyset = \emptyset$ is not a cut.
- **$\mathcal A$ must be bounded above.** For $\mathcal A = \{r^* : r \in \mathbb Q\}$, every rational $q$ lies in $(q + 1)^*$, so $\bigcup \mathcal A = \mathbb Q$, which is not a cut; correspondingly, $\mathcal A$ has no upper bound in $\mathbb R$.
- **The property is about $\mathbb R$, not $\mathbb Q$.** The Incompleteness theorem shows that it fails in $\mathbb Q$. The difference is that a union of cuts is again a cut, while nothing in $\mathbb Q$ plays the role of the union.
:::

**Arithmetic.** For cuts $\alpha$ and $\beta$, define

$$\alpha + \beta := \{p + q : (p, q) \in \alpha \times \beta\}, \qquad -\alpha := \{p \in \mathbb Q : \existsin{r}{\mathbb Q}\,(0 < r \land -p - r \notin \alpha)\}.$$

The definition of $-\alpha$ says that $-p - r \notin \alpha$ for some $r > 0$, so $-p$ exceeds every element of $\alpha$ by more than $r$. The margin $r$ prevents $-\alpha$ from having a greatest element when $\alpha = s^*$ for a rational $s$.

:::{important icon=false} 📐 **Lemma (Addition of Cuts)**
For cuts $\alpha$, $\beta$ and rationals $r$, $s$:

1. $\alpha + \beta$ is a cut;
2. $\alpha + 0^* = \alpha$;
3. $(r + s)^* = r^* + s^*$.
:::

:::{admonition icon=false} ✍️ **Proof**
1. $\alpha + \beta \neq \emptyset$ because $\alpha$ and $\beta$ are nonempty. Choose $r \notin \alpha$ and $s \notin \beta$. Every $p \in \alpha$ satisfies $p < r$, since $r \le p$ would put $r$ in $\alpha$; likewise every $q \in \beta$ satisfies $q < s$. So every element of $\alpha + \beta$ is less than $r + s$, and $r + s \notin \alpha + \beta$. *Downward closed:* if $t < p + q$ with $p \in \alpha$ and $q \in \beta$, then $t - q < p$, so $t - q \in \alpha$, and $t = (t - q) + q \in \alpha + \beta$. *No greatest element:* given $p + q$, choose $p' \in \alpha$ with $p' > p$; then $p' + q \in \alpha + \beta$ is larger.
2. If $p \in \alpha$ and $q < 0$, then $p + q < p$, so $p + q \in \alpha$. Conversely, if $p \in \alpha$, choose $r \in \alpha$ with $r > p$; then $p = r + (p - r)$ with $p - r < 0$, so $p \in \alpha + 0^*$.
3. If $p < r$ and $q < s$, then $p + q < r + s$. Conversely, if $t < r + s$, let $h := \tfrac{(r + s) - t}{2} > 0$; then $t = (r - h) + (s - h)$ with $r - h \in r^*$ and $s - h \in s^*$. $\blacksquare$
:::

For multiplication, first take $\alpha, \beta > 0^*$ and define

$$\alpha\beta := \{p \in \mathbb Q : \existsin{r}{\alpha}\,\existsin{s}{\beta}\,(0 < r \land 0 < s \land p \le rs)\}.$$

Then set $\alpha 0^* = 0^* \alpha := 0^*$, and extend to other signs by $\alpha\beta := -\big((-\alpha)\beta\big)$ if $\alpha < 0^* < \beta$, $\alpha\beta := -\big(\alpha(-\beta)\big)$ if $\beta < 0^* < \alpha$, and $\alpha\beta := (-\alpha)(-\beta)$ if $\alpha, \beta < 0^*$. For $\alpha > 0^*$ the reciprocal is

$$\alpha^{-1} := \{p \in \mathbb Q : p \le 0 \lor \big(0 < p \land \existsin{r}{\mathbb Q}\,(1 < r \land (pr)^{-1} \notin \alpha)\big)\},$$

and $\alpha^{-1} := -\big((-\alpha)^{-1}\big)$ for $\alpha < 0^*$.

:::{important icon=false} 📐 **Theorem (ℝ Is a Complete Ordered Field)**
$(\mathbb R, +, \cdot, 0^*, 1^*, <)$ is a {term}`complete ordered field`: an ordered field in which every nonempty subset that is bounded above has a supremum. The map $\iota : \mathbb Q \to \mathbb R$, $\iota(r) := r^*$, is injective and preserves $+$, $\cdot$, and $<$.
:::

:::{admonition icon=false} ✍️ **Proof**
Proved above: $<$ satisfies trichotomy and transitivity, the least-upper-bound property holds, $\alpha + \beta$ is a cut, $0^*$ is an additive identity, and $\iota$ is injective and preserves $<$ and $+$. The remaining verifications (that $-\alpha$, $\alpha\beta$, and $\alpha^{-1}$ are cuts, and that the other field and order axioms hold) each reduce to the corresponding property of $\mathbb Q$, but they are long, and we do not repeat them. Complete proofs are in [Rudin (1976), *Principles of Mathematical Analysis*](https://en.wikipedia.org/wiki/Principles_of_Mathematical_Analysis), 3rd ed., appendix to Chapter 1, and in Enderton (1977), *Elements of Set Theory*, Chapter 5. The one step that needs more than the ordered-field axioms of $\mathbb Q$ is $\alpha + (-\alpha) = 0^*$, which uses the Archimedean property of $\mathbb Q$: for rationals $w > 0$ and $p$, some natural number $n$ has $nw > p$.
:::

Following the identification remark, we identify each $r \in \mathbb Q$ with $r^*$, so that $\mathbb N \subseteq \mathbb Z \subseteq \mathbb Q \subseteq \mathbb R$, and the cut $S$ is the real number $\sqrt 2$, which is not rational.
  
## Uniqueness of the Real Numbers

Dedekind cuts are one construction among several. The next theorem says the choice does not matter.

:::{important icon=false} 📐 **Theorem (Uniqueness of the Real Numbers)**
Let $F$ be any complete ordered field. There is exactly one {term}`bijective` function $\phi : \mathbb R \to F$ such that, for all $x, y \in \mathbb R$,
$$\phi(x + y) = \phi(x) + \phi(y), \qquad \phi(xy) = \phi(x)\,\phi(y), \qquad x < y \leftrightarrow \phi(x) < \phi(y).$$
:::

:::{admonition icon=false} ✍️ **Proof**
Not proved here; see Spivak, *Calculus*, Chapters 29–30, or [Real number: Axiomatic approach](https://en.wikipedia.org/wiki/Real_number). The idea: $\phi$ is forced on $\mathbb N$ by $\phi(1) = 1$ and additivity, then on $\mathbb Z$ by $\phi(-x) = -\phi(x)$, and on $\mathbb Q$ by $\phi(x^{-1}) = \phi(x)^{-1}$. For a general $x$, order preservation forces $\phi(x) = \sup\{\phi(q) : q \in \mathbb Q,\ q < x\}$, and completeness of $F$ guarantees that this supremum exists. One then checks that this $\phi$ is a bijection that preserves $+$, $\cdot$, and $<$.
:::

So, up to renaming elements by $\phi$, there is only one complete ordered field. Every construction (Dedekind cuts, Cauchy sequences, infinite decimals) produces "the same" $\mathbb R$, and any theorem proved from the complete-ordered-field axioms alone holds for all of them. This is why [Chapter 3](ch3_sets_for_probability_v2.md) and the rest of the book work from those axioms and never mention cuts again.

## Summary

- **Natural numbers:** the recursive definitions of $+$, $\cdot$, and $<$ from Chapter 2 yield, by induction, the associative, commutative, distributive, cancellation, and order laws, including trichotomy and well-ordering.
- **Equivalence relations and quotients:** an equivalence relation turns "represents the same thing" into equality of classes; operations defined on representatives pass to classes exactly when they are compatible.
- **Integers** are classes of pairs $(a, b) \in \mathbb N \times \mathbb N$ ("$a - b$"); they form a commutative ring with no zero divisors, ordered by a relation $<$ that satisfies the ordered-field axioms.
- **Rational numbers** are classes of pairs $(a, b) \in \mathbb Z \times \mathbb Z^*$ ("$a / b$"); they form an ordered field that is dense.
- **Incompleteness:** $\{q \in \mathbb Q : q < 0 \lor q^2 < 2\}$ is bounded above but has no rational supremum.
- **Real numbers** are Dedekind cuts. The supremum of a bounded nonempty set of cuts is its union, so $\mathbb R$ is a complete ordered field, and it is the only one up to isomorphism.

[Chapter 3](ch3_sets_for_probability_v2.md) takes it from here, working with $\mathbb R$ through the complete-ordered-field axioms: the Archimedean property, density of $\mathbb Q$ in $\mathbb R$, and the uncountability of $\mathbb R$ all follow from the least-upper-bound property proved in this appendix.