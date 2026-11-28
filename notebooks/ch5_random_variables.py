# /// script
# dependencies = [
#     "marimo>=0.25.1",
#     "matplotlib==3.11.2",
#     "numpy==2.5.3",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="5. Random Variables", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "From Outcomes to Numbers"
    description: "Random variables, their distributions, and their densities, used to model a measurement as a true value plus noise."
    label: ch5
    -->
    """)
    return


@app.cell
def imports():
    # jb: include=false
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import math
    from textwrap import dedent
    from pathlib import Path

    return Path, dedent, math, mo, np, plt


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
def _(Path):
    # jb: include=false
    IMAGES_DIR = Path(__file__).parent.parent / "notebooks" / "public"
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    return (IMAGES_DIR,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// important | 🔗 **Prerequisites**
    - [Introduction](#intro): [the bathroom-scale example](#intro-sec-measurements-and-definitions), [the notation](#intro-sec-measurements-and-definitions) $x_k$ (true value) and $z_k$ (measurement), and the definitions of {term}`signal` and {term}`noise`.
    - [Chapter 3](#ch3): {term}`preimages <preimage>` and the [Preimages Preserve Set Operations lemma](#ch3-lem-preimages-preserve-set-operations); {term}`countable` sets, including that $\mathbb Q$ and $\mathbb N \times \mathbb N$ are countable; the [Archimedean property](#ch3-thm-archimedean-property) and the [density of $\mathbb Q$ in $\mathbb R$](#ch3-thm-density-of-the-rationals); {term}`supremum` and {term}`infimum`; {term}`intervals <interval>`.
    - [Chapter 4](#ch4): {term}`probability spaces <probability space>`; the {term}`generated sigma-algebra` and the {term}`Borel sigma-algebra`; [monotonicity](#ch4-thm-monotonicity), [finite and countable additivity](#ch4-thm-finite-additivity), [the union bound](#ch4-thm-union-bound), and [continuity from below and above](#ch4-thm-continuity-from-below); [Lebesgue measure](#ch4-thm-lebesgue-measure) on $[0,1]$; {term}`independent events`; {term}`almost surely`.
    - [Appendix C: Sequences and Limits](#appc-sec-sequences-and-limits) and [Appendix C: Limits of Functions and Continuity](#appc-sec-limits-of-functions-and-continuity): limits, including one-sided limits.
    - [Appendix C: Series](#appc-sec-series): a series of nonnegative terms, or an absolutely convergent series, [may be summed in any order and grouped arbitrarily](#appc-thm-nonnegative-sums-in-any-order).
    - [Appendix C: The Riemann Integral](#appc-sec-the-riemann-integral), [Appendix C: The Fundamental Theorem of Calculus](#appc-sec-the-fundamental-theorem-of-calculus) (including substitution), [Appendix C: Exponential and Logarithm](#appc-sec-exponential-and-logarithm), and [Appendix C: Improper Integrals](#appc-sec-improper-integrals).
    - [Appendix C: Multiple Integrals](#appc-sec-multiple-integrals): [Fubini's theorem](#appc-thm-tonelli-and-fubini) and [the Gaussian integral](#appc-thm-gaussian-integral) $\int_{-\infty}^{\infty} e^{-z^2/2}\,dz = \sqrt{2\pi}$.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the Introduction we wrote each scale reading as the true weight plus some noise, and claimed that averaging many readings makes the noise smaller. To prove that claim (Chapter 6) and then use it to choose $\alpha$ (Chapter 7), we need a precise mathematical object for "a number whose value depends on chance." That object is a *random variable*: a function that assigns a number to every outcome of a random experiment.

    [Chapter 4](#ch4) assigned probabilities to *events*. Random variables let us ask questions about *numbers* instead ("what is the probability that the noise exceeds 1 lb?"), and they let us describe the answers to all such questions at once with a single object, the *distribution*. By the end of this chapter we can state the standard model behind almost every filter in this book: each measurement is the true value plus independent, normally distributed noise. We also see exactly where that model can fail.

    /// attention | 🗝️ **Key Idea**
    A random variable is a function from outcomes to real numbers such that "the value lies in $B$" is an event for every reasonable set $B$. Its distribution records how likely each range of values is; for any question about $X$ alone, that is all we need to know.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch5-sec-random-variables -->
    ## Random Variables

    <!-- label: ch5-sec-from-outcomes-to-numbers -->
    ### From Outcomes to Numbers

    Toss a fair coin twice. Take the sample space $\Omega = \{HH, HT, TH, TT\}$, the $\sigma$-algebra $\mathcal F = \mathcal P(\Omega)$, and $\mathbb P(\{\omega\}) = 1/4$ for each outcome $\omega$. Let $X(\omega)$ be the number of heads in $\omega$:

    $$X(HH) = 2, \qquad X(HT) = X(TH) = 1, \qquad X(TT) = 0.$$

    The question "what is the probability of exactly one head?" is a question about the set of outcomes on which $X$ equals $1$, which is the {term}`preimage` $X^{-1}[\{1\}] = \{HT, TH\}$. Its probability is $1/2$. In general, every question of the form "does $X$ land in the set $B$?" is a question about the preimage $X^{-1}[B]$.

    For $\mathbb P$ to answer such a question, the preimage must be an {term}`event`, that is, a member of $\mathcal F$. With $\mathcal F = \mathcal P(\Omega)$ every subset is an event, so this is automatic. But it can fail. Suppose an observer sees only the *first* toss. The events this observer can decide are those in

    $$\mathcal F_1 := \big\{\emptyset,\ \{HH, HT\},\ \{TH, TT\},\ \Omega\big\},$$

    which is a $\sigma$-algebra (it contains $\Omega$ and is closed under complements and unions). The number of heads is not determined by the first toss alone, and indeed $X^{-1}[\{2\}] = \{HH\} \notin \mathcal F_1$. By contrast, the function $Y$ that equals $1$ if the first toss is heads and $0$ otherwise has preimages $\emptyset$, $\{HH, HT\}$, $\{TH, TT\}$, and $\Omega$, all of which are in $\mathcal F_1$. Relative to $\mathcal F_1$, $Y$ is a legitimate random quantity and $X$ is not.

    The bathroom scale has the same structure. An outcome $\omega \in \Omega$ stands for everything that determines one reading: how the person shifted, the thermal noise in the load cell, and so on. We never need to list $\Omega$ explicitly. What we need is the function $V : \Omega \to \mathbb R$ giving the noise $V(\omega)$ in pounds, together with a guarantee that questions like "is the noise between $-1$ and $1$ lb?" (the set $V^{-1}\big[[-1, 1]\big]$) are events.

    Which sets $B \subseteq \mathbb R$ should we be allowed to ask about? At the very least, every {term}`interval`. Events are closed under complements and countable unions, so once every interval is allowed, so is every set in the $\sigma$-algebra generated by the intervals. That is the {term}`Borel sigma-algebra` of [Chapter 4](#ch4-sec-the-borel-sigma-algebra), which we write $\mathcal B(\mathbb R)$; its members are the *Borel sets*. The following lemma shows that a much smaller collection of intervals already generates it. Here $\sigma(\mathcal C)$ denotes the {term}`sigma-algebra generated by <generated sigma-algebra>` a collection $\mathcal C$ of subsets of $\mathbb R$, the smallest $\sigma$-algebra on $\mathbb R$ containing $\mathcal C$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// admonition | 📐 **Lemma (Rays Generate the Borel Sets)**
        attrs: {class: lemma, id: ch5-lem-rays-generate-the-borel-sets}
    $\mathcal B(\mathbb R) = \sigma\big(\{(-\infty, b] : b \in \mathbb R\}\big)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Let $\mathcal G := \sigma\big(\{(-\infty, b] : b \in \mathbb R\}\big)$.

    ($\mathcal G \subseteq \mathcal B(\mathbb R)$.) Every ray $(-\infty, b]$ is an interval, so it belongs to $\mathcal B(\mathbb R)$. Thus $\mathcal B(\mathbb R)$ is a $\sigma$-algebra containing all the rays, and $\mathcal G$ is the smallest such $\sigma$-algebra, so $\mathcal G \subseteq \mathcal B(\mathbb R)$.

    ($\mathcal B(\mathbb R) \subseteq \mathcal G$.) It suffices to show that every interval is in $\mathcal G$, because $\mathcal B(\mathbb R)$ is the smallest $\sigma$-algebra containing the intervals. Fix $a, b \in \mathbb R$.

    - $(-\infty, b] \in \mathcal G$ by definition.
    - $(-\infty, b) = \bigcup_{n=1}^{\infty} (-\infty, b - \tfrac1n]$. Each set on the right is contained in $(-\infty, b)$. Conversely, if $x < b$, the Archimedean property gives an $n$ with $\tfrac1n < b - x$, so $x \in (-\infty, b - \tfrac1n]$. A countable union of members of $\mathcal G$ is in $\mathcal G$.
    - $(a, \infty) = \mathbb R \setminus (-\infty, a]$ and $[a, \infty) = \mathbb R \setminus (-\infty, a)$ are complements of members of $\mathcal G$.
    - Every bounded interval is the intersection of one of the two left-unbounded rays above with one of the two right-unbounded rays; for example $(a, b] = (a, \infty) \cap (-\infty, b]$ and $[a, b) = [a, \infty) \cap (-\infty, b)$. A $\sigma$-algebra is closed under finite intersections, by De Morgan's laws.
    - $\mathbb R = \bigcup_{n=1}^\infty (-\infty, n]$ and $\emptyset = \mathbb R \setminus \mathbb R$.

    So every interval is in $\mathcal G$. $\blacksquare$
    ///

    Some books generate $\mathcal B(\mathbb R)$ from the open subsets of $\mathbb R$ instead of the intervals. This gives the same $\sigma$-algebra, because every open set is a countable union of open intervals with rational endpoints ([Wikipedia: Borel set](https://en.wikipedia.org/wiki/Borel_set)).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch5-sec-definition -->
    ### Definition

    /// note | 📖 **Definition**
    <u>**Random variable**</u>

    Let $(\Omega, \mathcal F, \mathbb P)$ be a {term}`probability space`. A random variable on it is a {term}`function` $X : \Omega \to \mathbb R$ such that $X^{-1}[B] \in \mathcal F$ for every Borel set $B \in \mathcal B(\mathbb R)$.
    ///

    A random variable is neither random nor a variable: it is a fixed function. The randomness lies in *which* outcome $\omega$ occurs, and $X(\omega)$ is the number we then observe.

    **Notation.** For $B \subseteq \mathbb R$ we write

    $$\{X \in B\} := X^{-1}[B] = \{\omega \in \Omega : X(\omega) \in B\}, \qquad \mathbb P(X \in B) := \mathbb P(\{X \in B\}),$$

    and similarly $\{X \le b\} := X^{-1}\big[(-\infty, b]\big]$, $\{X = b\}$, $\{a < X \le b\}$, and so on. A comma inside braces means intersection: $\{X \in A, Y \in B\} := \{X \in A\} \cap \{Y \in B\}$. Random variables are written in uppercase and the numbers they take in lowercase, so "$x$ is a possible value of $X$." In particular, the Introduction's $z_k$ is the number the scale actually displayed. From now on $Z_k$ denotes the random variable "the $k$-th reading," and $z_k = Z_k(\omega)$ is its value on the outcome that occurred.

    Checking the definition for every Borel set would be impractical. The [Measurability Test lemma](#ch5-lem-measurability-test) below reduces it to the rays.

    /// admonition | 📐 **Lemma (Measurability Test)**
        attrs: {class: lemma, id: ch5-lem-measurability-test}
    Let $(\Omega, \mathcal F, \mathbb P)$ be a probability space and $X : \Omega \to \mathbb R$ a function. Then $X$ is a random variable if and only if $\{X \le b\} \in \mathcal F$ for every $b \in \mathbb R$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    ($\Rightarrow$) Each ray $(-\infty, b]$ is a Borel set.

    ($\Leftarrow$) Let $\mathcal A := \{B \subseteq \mathbb R : X^{-1}[B] \in \mathcal F\}$, the collection of "good" sets. We show $\mathcal A$ is a $\sigma$-algebra on $\mathbb R$, using the lemma of [Chapter 3](#ch3-lem-preimages-preserve-set-operations) that preimages preserve complements and unions.

    - $\mathbb R \in \mathcal A$, since $X^{-1}[\mathbb R] = \Omega \in \mathcal F$.
    - If $B \in \mathcal A$, then $X^{-1}[\mathbb R \setminus B] = \Omega \setminus X^{-1}[B] \in \mathcal F$, so $\mathbb R \setminus B \in \mathcal A$.
    - If $B_1, B_2, \ldots \in \mathcal A$, then $X^{-1}\big[\bigcup_n B_n\big] = \bigcup_n X^{-1}[B_n] \in \mathcal F$, so $\bigcup_n B_n \in \mathcal A$.

    By hypothesis $\mathcal A$ contains every ray $(-\infty, b]$. Since $\mathcal A$ is a $\sigma$-algebra, it contains the $\sigma$-algebra they generate, which is $\mathcal B(\mathbb R)$ by the [Rays Generate the Borel Sets lemma](#ch5-lem-rays-generate-the-borel-sets). So $X^{-1}[B] \in \mathcal F$ for every Borel set $B$. $\blacksquare$
    ///

    The proof never used $\mathbb P$, only $\mathcal F$. The same argument works for any function between two sets each equipped with a $\sigma$-algebra, a fact we use again below.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Examples.**

    1. *Constants.* For $c \in \mathbb R$, the function $X(\omega) := c$ is a random variable, since $\{X \le b\}$ is $\Omega$ if $c \le b$ and $\emptyset$ otherwise.
    2. *Indicators.* For a set $A \subseteq \Omega$, the *indicator* of $A$ is the function $\mathbf 1_A : \Omega \to \mathbb R$ with $\mathbf 1_A(\omega) := 1$ if $\omega \in A$ and $\mathbf 1_A(\omega) := 0$ otherwise. If $A \in \mathcal F$, then $\{\mathbf 1_A \le b\}$ is $\emptyset$ for $b < 0$, $\Omega \setminus A$ for $0 \le b < 1$, and $\Omega$ for $b \ge 1$, so $\mathbf 1_A$ is a random variable. If $A \notin \mathcal F$, it is not, since $\mathbf 1_A^{-1}[\{1\}] = A$. The coin example's $Y$ is $\mathbf 1_{\{HH, HT\}}$.
    3. *A uniformly random number.* [Chapter 4](#ch4-thm-a-uniformly-random-number) built the probability space with $\Omega = [0, 1]$, $\mathcal F$ the Borel subsets of $[0,1]$, and $\mathbb P = \lambda$, Lebesgue measure, which gives every interval its length: $\lambda([a, b]) = b - a$. On it, $U(\omega) := \omega$ is a random variable, since $\{U \le b\}$ is $\emptyset$, $[0, b]$, or $[0, 1]$, and $\mathbb P(U \le b) = b$ for $0 \le b \le 1$. Below we show that this one random variable is enough to build a random variable with *any* distribution.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch5-sec-new-random-variables-from-old -->
    ### New Random Variables from Old

    Filters add, scale, and combine measurements, so we need to know that these operations produce random variables again. Call a function $g : \mathbb R \to \mathbb R$ *Borel* iff $g^{-1}[B] \in \mathcal B(\mathbb R)$ for every $B \in \mathcal B(\mathbb R)$. For a random variable $X$ we write $g(X)$ for the composition $g \circ X : \Omega \to \mathbb R$.

    /// admonition | 📐 **Theorem (Building Random Variables)**
        attrs: {class: theorem, id: ch5-thm-building-random-variables}
    Let $X$ and $Y$ be random variables on $(\Omega, \mathcal F, \mathbb P)$, let $a, b \in \mathbb R$, and let $g : \mathbb R \to \mathbb R$ be Borel. Then $aX + b$, $X + Y$, $X^2$, $XY$, and $g(X)$ are random variables. Every continuous $g$ is Borel.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    We use the measurability test throughout. Fix $c \in \mathbb R$.

    - $aX + b$: if $a > 0$, then $\{aX + b \le c\} = \{X \le \tfrac{c-b}{a}\} \in \mathcal F$. If $a < 0$, then $\{aX + b \le c\} = \{X \ge \tfrac{c-b}{a}\} = X^{-1}\big[[\tfrac{c-b}{a}, \infty)\big] \in \mathcal F$, since intervals are Borel. If $a = 0$, then $aX + b$ is constant.
    - $X + Y$: we claim
      $$\{X + Y < c\} = \bigcup_{q \in \mathbb Q} \big(\{X < q\} \cap \{Y < c - q\}\big).$$
      If $X(\omega) < q$ and $Y(\omega) < c - q$, adding gives $X(\omega) + Y(\omega) < c$. Conversely, if $X(\omega) + Y(\omega) < c$, then $X(\omega) < c - Y(\omega)$, and by the density of $\mathbb Q$ there is a rational $q$ with $X(\omega) < q < c - Y(\omega)$, so $Y(\omega) < c - q$. The right side is a countable union (since $\mathbb Q$ is countable) of events, so it is an event. Finally $\{X + Y \le c\} = \bigcap_{n=1}^\infty \{X + Y < c + \tfrac1n\}$ by the Archimedean property, and a countable intersection of events is an event.
    - $X^2$: $\{X^2 \le c\}$ is $\emptyset$ if $c < 0$, and $\{-\sqrt c \le X \le \sqrt c\} = X^{-1}\big[[-\sqrt c, \sqrt c]\big]$ if $c \ge 0$.
    - $XY = \tfrac14\big((X+Y)^2 - (X-Y)^2\big)$, which is built from the previous three cases.
    - $g(X)$: $(g \circ X)^{-1}[B] = X^{-1}\big[g^{-1}[B]\big]$, and $g^{-1}[B]$ is Borel whenever $B$ is.

    That continuous functions are Borel is a standard fact we state without proof: the preimage of an open set under a continuous function is open, and open sets are Borel ([Wikipedia: Measurable function](https://en.wikipedia.org/wiki/Measurable_function)). $\blacksquare$
    ///

    For example, if $U$ is the uniformly random number above, then $V := 2U - 1$ is a random variable whose values are spread over $[-1, 1]$: a crude model of scale noise between $-1$ and $+1$ lb.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch5-sec-distributions -->
    ## Distributions

    A random variable assigns a probability to every statement "$X \in B$." Collecting those probabilities into one function gives the distribution.

    /// note | 📖 **Definition**
    <u>**Distribution**</u>

    The distribution of a {term}`random variable` $X$ on $(\Omega, \mathcal F, \mathbb P)$ is the function $\mathbb P_X : \mathcal B(\mathbb R) \to [0, 1]$ defined by $\mathbb P_X(B) := \mathbb P(X \in B)$.
    ///

    /// admonition | 📐 **Theorem (Distributions Are Probability Measures)**
        attrs: {class: theorem, id: ch5-thm-distributions-are-probability-measures}
    For every random variable $X$, $\mathbb P_X$ is a {term}`probability measure` on $(\mathbb R, \mathcal B(\mathbb R))$. Hence $(\mathbb R, \mathcal B(\mathbb R), \mathbb P_X)$ is a probability space.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    $\mathbb P_X(B) = \mathbb P(X^{-1}[B]) \ge 0$ for every Borel $B$, and $\mathbb P_X(\mathbb R) = \mathbb P(\Omega) = 1$. Let $B_1, B_2, \ldots$ be pairwise disjoint Borel sets. Their preimages are pairwise disjoint: if $\omega \in X^{-1}[B_i] \cap X^{-1}[B_j]$ with $i \ne j$, then $X(\omega) \in B_i \cap B_j = \emptyset$, which is impossible. Since preimages preserve unions, countable additivity of $\mathbb P$ gives
    $$\mathbb P_X\Big(\bigcup_n B_n\Big) = \mathbb P\Big(\bigcup_n X^{-1}[B_n]\Big) = \sum_n \mathbb P(X^{-1}[B_n]) = \sum_n \mathbb P_X(B_n). \qquad \blacksquare$$
    ///

    The distribution is also called the *law* of $X$, or the *push-forward* of $\mathbb P$ by $X$: the function $X$ carries ("pushes") the probability on $\Omega$ forward onto the real line.

    **Notation.** For a probability measure $\mu$ on $(\mathbb R, \mathcal B(\mathbb R))$, we write $X \sim \mu$ ("$X$ has distribution $\mu$") iff $\mathbb P_X = \mu$. Two random variables $X$ and $Y$, possibly on different probability spaces, are *identically distributed* iff $\mathbb P_X = \mathbb P_Y$.

    In the coin example, $\mathbb P_X(\{0\}) = \tfrac14$, $\mathbb P_X(\{1\}) = \tfrac12$, $\mathbb P_X(\{2\}) = \tfrac14$, and $\mathbb P_X(B)$ is the sum of these numbers over the points of $\{0, 1, 2\}$ that lie in $B$. The number of *tails*, $X'(\omega) := 2 - X(\omega)$, has exactly the same distribution, yet $X' \ne X$ (for instance $X'(HH) = 0$). Identically distributed random variables need not be equal; they only agree on how likely each range of values is.

    /// attention | 🗝️ **Key Idea**
    Any probability that involves only $X$ is determined by $\mathbb P_X$. Once the distribution is known, the sample space fades into the background, which is why filtering texts rarely mention $\Omega$: they specify distributions.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch5-sec-cumulative-distribution-functions -->
    ## Cumulative Distribution Functions

    A distribution is a function on *sets*, which is awkward to write down or plot. Because the rays generate $\mathcal B(\mathbb R)$, it is natural to record only the probabilities of the rays.

    /// note | 📖 **Definition**
    <u>**Cumulative distribution function**</u>

    The cumulative distribution function (CDF) of a {term}`random variable` $X$ is the function $F_X : \mathbb R \to [0, 1]$ defined by $F_X(x) := \mathbb P(X \le x)$.
    ///

    /// admonition | 📐 **Theorem (Properties of CDFs)**
        attrs: {class: theorem, id: ch5-thm-properties-of-cdfs}
    For every random variable $X$:

    1. $F_X$ is nondecreasing: $x \le y$ implies $F_X(x) \le F_X(y)$.
    2. $F_X$ is right-continuous: $\lim_{t \to x^+} F_X(t) = F_X(x)$ for every $x \in \mathbb R$.
    3. $\lim_{x \to -\infty} F_X(x) = 0$ and $\lim_{x \to \infty} F_X(x) = 1$.
    4. $\mathbb P(a < X \le b) = F_X(b) - F_X(a)$ whenever $a < b$.
    5. The left limit $F_X(x^-) := \lim_{t \to x^-} F_X(t)$ exists and equals $\mathbb P(X < x)$. Hence $\mathbb P(X = x) = F_X(x) - F_X(x^-)$: the probability of a single value is the size of the jump of $F_X$ there.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Write $F := F_X$. All facts about $\mathbb P$ used here are from [Chapter 4](#ch4-sec-consequences-of-the-axioms).

    1. If $x \le y$ then $\{X \le x\} \subseteq \{X \le y\}$, so monotonicity of $\mathbb P$ gives $F(x) \le F(y)$.
    2. The events $A_n := \{X \le x + \tfrac1n\}$ decrease, and $\bigcap_n A_n = \{X \le x\}$: if $X(\omega) \le x + \tfrac1n$ for every $n$, then $X(\omega) \le x$ by the Archimedean property. Continuity from above gives $F(x + \tfrac1n) \to F(x)$. Now let $\varepsilon > 0$ and pick $N$ with $F(x + \tfrac1N) < F(x) + \varepsilon$. For every $t$ with $x < t < x + \tfrac1N$, part 1 gives $F(x) \le F(t) \le F(x + \tfrac1N) < F(x) + \varepsilon$. So $|F(t) - F(x)| < \varepsilon$ whenever $0 < t - x < \tfrac1N$.
    3. The events $\{X \le -n\}$ decrease to $\emptyset$, because every real number $X(\omega)$ exceeds $-n$ for some $n$. Continuity from above gives $F(-n) \to 0$, and for $x < -n$ monotonicity gives $0 \le F(x) \le F(-n)$, so $F(x) \to 0$ as $x \to -\infty$. Similarly the events $\{X \le n\}$ increase to $\Omega$, continuity from below gives $F(n) \to 1$, and $F(n) \le F(x) \le 1$ for $x > n$.
    4. $\{X \le b\}$ is the disjoint union of $\{X \le a\}$ and $\{a < X \le b\}$, so finite additivity gives $F(b) = F(a) + \mathbb P(a < X \le b)$.
    5. The events $\{X \le x - \tfrac1n\}$ increase to $\{X < x\}$, so continuity from below gives $F(x - \tfrac1n) \to \mathbb P(X < x)$. The same squeezing argument as in part 2 extends this to every $t \to x^-$. Finally, $\{X \le x\}$ is the disjoint union of $\{X < x\}$ and $\{X = x\}$. $\blacksquare$
    ///

    In the coin example, $F_X$ is a staircase: $0$ for $x < 0$, $\tfrac14$ on $[0, 1)$, $\tfrac34$ on $[1, 2)$, and $1$ on $[2, \infty)$. It jumps by $\tfrac14, \tfrac12, \tfrac14$ at $0, 1, 2$, exactly the probabilities of those values, and at each jump it takes the upper value (right-continuity). The figure also shows the CDF of the standard normal distribution, defined below, which has no jumps at all.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch5_cdf_examples.svg" class="graphic" alt="Left: the staircase CDF of the number of heads in two fair coin tosses, with jumps of 1/4, 1/2, 1/4 at 0, 1, 2. Right: the smooth S-shaped CDF of the standard normal distribution together with its bell-shaped density." />
    """)
    return


@app.cell
def _(IMAGES_DIR, math, np, plt):
    # jb: include=false
    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(10, 3.8))

    _levels = [0.0, 0.25, 0.75, 1.0]
    _edges = [-1.0, 0.0, 1.0, 2.0, 3.0]
    for _i, _lvl in enumerate(_levels):
        _ax1.plot([_edges[_i], _edges[_i + 1]], [_lvl, _lvl], color="C1", linewidth=2)
    for _j, _x in enumerate([0, 1, 2]):
        _ax1.plot(_x, _levels[_j + 1], "o", color="C1")
        _ax1.plot(_x, _levels[_j], "o", markerfacecolor="white", markeredgecolor="C1")
    _ax1.set_xlim(-1, 3)
    _ax1.set_ylim(-0.05, 1.05)
    _ax1.set_xlabel("$x$ (number of heads)")
    _ax1.set_ylabel("$F_X(x)$")
    _ax1.set_title("CDF of the number of heads in two tosses", style="italic")
    _ax1.grid(visible=True, alpha=0.9, linewidth=0.4)

    _xs = np.linspace(-4, 4, 400)
    _Phi = np.array([0.5 * (1 + math.erf(_t / math.sqrt(2))) for _t in _xs])
    _phi = np.exp(-_xs**2 / 2) / math.sqrt(2 * math.pi)
    _ax2.plot(_xs, _Phi, color="C1", linewidth=2, label=r"CDF $\Phi(x)$")
    _ax2.plot(_xs, _phi, color="C0", linewidth=1.5, linestyle="--", label=r"density $\varphi(x)$")
    _ax2.set_xlabel("$x$")
    _ax2.set_ylim(-0.05, 1.05)
    _ax2.set_title("Standard normal CDF and density", style="italic")
    _ax2.legend(loc="center right")
    _ax2.grid(visible=True, alpha=0.9, linewidth=0.4)

    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch5_cdf_examples.svg")
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The CDF loses nothing: it determines the whole distribution. The proof needs a tool from measure theory, so we only state it.

    /// admonition | 📐 **Theorem (A CDF Determines Its Distribution)**
        attrs: {class: theorem, id: ch5-thm-a-cdf-determines-its-distribution}
    If $X$ and $Y$ are random variables with $F_X = F_Y$, then $\mathbb P_X = \mathbb P_Y$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Not given here. $F_X = F_Y$ says that the probability measures $\mathbb P_X$ and $\mathbb P_Y$ agree on every ray. The rays form a collection closed under finite intersections ($(-\infty, a] \cap (-\infty, b] = (-\infty, \min(a,b)]$), and they generate $\mathcal B(\mathbb R)$. Dynkin's $\pi$-$\lambda$ theorem says that two probability measures that agree on such a collection agree on the $\sigma$-algebra it generates ([Wikipedia: Dynkin system](https://en.wikipedia.org/wiki/Dynkin_system)).
    ///

    Conversely, properties 1 to 3 are not just necessary; they are exactly what it takes to be a CDF. The proof builds the random variable explicitly from the uniformly random number $U$.

    /// admonition | 📐 **Theorem (Every Such Function Is a CDF)**
        attrs: {class: theorem, id: ch5-thm-every-such-function-is-a-cdf}
    Let $F : \mathbb R \to [0, 1]$ be nondecreasing and right-continuous, with $\lim_{x \to -\infty} F(x) = 0$ and $\lim_{x \to \infty} F(x) = 1$. For $u \in (0, 1)$ define
    $$G(u) := \inf\{x \in \mathbb R : F(x) \ge u\}.$$
    On the uniform probability space $([0,1], \text{Borel sets}, \lambda)$, let $X(\omega) := G(\omega)$ for $0 < \omega < 1$ and $X(0) := X(1) := 0$. Then $X$ is a random variable and $F_X = F$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    *$G$ is well defined.* Fix $u \in (0, 1)$ and let $S_u := \{x \in \mathbb R : F(x) \ge u\}$. Since $F(x) \to 1 > u$ as $x \to \infty$, some $x$ has $F(x) \ge u$, so $S_u \ne \emptyset$. Since $F(x) \to 0 < u$ as $x \to -\infty$, there is an $x_0$ with $F(x) < u$ for all $x \le x_0$, so $x_0$ is a lower bound of $S_u$. By the completeness of $\mathbb R$ ([Chapter 3](#ch3-sec-bounds-and-completeness)), $S_u$ has an {term}`infimum`.

    *Key equivalence.* For $u \in (0, 1)$ and $x \in \mathbb R$: $G(u) \le x \iff u \le F(x)$.

    - ($\Leftarrow$) If $F(x) \ge u$, then $x \in S_u$, so $G(u) = \inf S_u \le x$.
    - ($\Rightarrow$) Suppose $G(u) \le x$. For each $n$, $x + \tfrac1n > \inf S_u$, so $x + \tfrac1n$ is not a lower bound of $S_u$: some $s_n \in S_u$ has $s_n < x + \tfrac1n$. Since $F$ is nondecreasing, $F(x + \tfrac1n) \ge F(s_n) \ge u$. Letting $n \to \infty$ and using right-continuity, $F(x) \ge u$.

    *Conclusion.* Fix $x \in \mathbb R$. By the key equivalence, $\{X \le x\}$ consists of the $\omega \in (0,1)$ with $\omega \le F(x)$, together with the points $0$ and $1$ if $x \ge 0$. That is, $\{X \le x\} = \big((0, F(x)] \cap (0, 1)\big) \cup N_x$ with $N_x \subseteq \{0, 1\}$. This is a Borel set, so $X$ is a random variable by the measurability test. Its probability is the length of $(0, F(x)] \cap (0, 1)$, which is $F(x)$ (also when $F(x) = 0$ or $F(x) = 1$), plus $\lambda(N_x) = 0$. So $F_X(x) = F(x)$. $\blacksquare$
    ///

    The function $G$ is called the *quantile function* of $F$; when $F$ is continuous and strictly increasing it is simply the inverse function $F^{-1}$. Computers generate pseudo-random numbers that imitate $U$, and the theorem is one standard way to turn them into samples with any desired distribution ([Wikipedia: Inverse transform sampling](https://en.wikipedia.org/wiki/Inverse_transform_sampling)).

    /// attention | 🗝️ **Key Idea**
    A function $F : \mathbb R \to [0,1]$ is the CDF of some random variable if and only if it is nondecreasing, right-continuous, and tends to $0$ at $-\infty$ and $1$ at $+\infty$; and the CDF determines the distribution. So we may specify a distribution simply by writing down such a function, and a random variable with that distribution is guaranteed to exist.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch5-sec-discrete-random-variables -->
    ## Discrete Random Variables

    Some random variables take only a list of values, like the number of heads. To add up probabilities over such a list we need sums over countable sets. Recall from [Chapter 3](#ch3-sec-countable-and-uncountable-sets) that a {term}`countable` set is one that injects into $\mathbb N$; finite sets are countable. For a countable set $C$ and numbers $a_c \ge 0$, $\sum_{c \in C} a_c$ means $\sum_{n} a_{c_n}$ for an enumeration $c_1, c_2, \ldots$ of $C$. By [Appendix C: Series](#appc-sec-series), the value (possibly $\infty$) does not depend on the enumeration, and the terms may be grouped arbitrarily. The same holds for real $a_c$ of either sign when $\sum_{c \in C} |a_c| < \infty$. If $C$ is finite, the sum is an ordinary finite sum.

    /// note | 📖 **Definition**
    <u>**Discrete random variable**</u>

    A {term}`random variable` $X$ is discrete iff there is a {term}`countable` set $C \subseteq \mathbb R$ with $\mathbb P(X \in C) = 1$.
    ///

    (A countable set $C$ is a Borel set, being a countable union of the one-point intervals $[c, c]$, so $\mathbb P(X \in C)$ makes sense.)

    /// note | 📖 **Definition**
    <u>**Probability mass function**</u>

    The probability mass function (PMF) of a {term}`random variable` $X$ is the function $p_X : \mathbb R \to [0, 1]$ defined by $p_X(x) := \mathbb P(X = x)$.
    ///

    /// admonition | 📐 **Theorem (A PMF Determines a Discrete Distribution)**
        attrs: {class: theorem, id: ch5-thm-a-pmf-determines-a-discrete-distribution}
    Let $X$ be discrete with $\mathbb P(X \in C) = 1$ for a countable set $C$. Then

    1. $\mathbb P(X \in B) = \sum_{x \in B \cap C} p_X(x)$ for every Borel set $B$;
    2. $\sum_{x \in C} p_X(x) = 1$;
    3. $p_X(x) = 0$ for every $x \notin C$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    $\{X \in B\}$ is the disjoint union of $\{X \in B \cap C\}$ and $\{X \in B \setminus C\}$. The second is contained in $\{X \notin C\}$, which has probability $0$, so it has probability $0$ by monotonicity. The first is the disjoint union of the countably many events $\{X = x\}$, $x \in B \cap C$, so countable additivity gives part 1. Part 2 is part 1 with $B = \mathbb R$. For part 3, $\{X = x\} \subseteq \{X \notin C\}$ when $x \notin C$. $\blacksquare$
    ///

    **Examples.**

    - The number of heads $X$ has $p_X(0) = \tfrac14$, $p_X(1) = \tfrac12$, $p_X(2) = \tfrac14$, and $C = \{0, 1, 2\}$.
    - For $p \in [0, 1]$, a random variable $X$ has the *Bernoulli distribution* with parameter $p$ iff $p_X(1) = p$ and $p_X(0) = 1 - p$. Every indicator $\mathbf 1_A$ of an event $A$ is Bernoulli with parameter $\mathbb P(A)$. Chapter 6 uses indicators to turn relative frequencies into averages.
    - *Every digital reading is discrete.* The HX711 delivers a 24-bit integer [@avia_hx711_datasheet], so a reading can take at most $2^{24}$ values, and anything computed from finitely many readings takes finitely many values. The continuous models below are idealizations; the section on quantization measures what the idealization costs.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch5-sec-continuous-random-variables -->
    ## Continuous Random Variables

    For the uniformly random number $U$, every single value has probability zero: $\mathbb P(U = x) = \lambda([x, x]) = 0$. Its PMF is identically $0$ and tells us nothing. Instead, probabilities of intervals are *areas*: $\mathbb P(a < U \le b) = b - a = \int_a^b 1\,dt$ for $0 \le a < b \le 1$. Random variables whose probabilities are areas under a curve are called continuous.

    /// note | 📖 **Definition**
    <u>**Probability density function**</u>

    A probability density function (PDF) is a function $f : \mathbb R \to [0, \infty)$ such that the (possibly {term}`improper <improper integral>`) {term}`Riemann integral` $\int_{-\infty}^{x} f(t)\,dt$ exists for every $x \in \mathbb R$ and $\int_{-\infty}^{\infty} f(t)\,dt = 1$. A PDF $f$ is a *density of* a {term}`random variable` $X$ iff $F_X(x) = \int_{-\infty}^{x} f(t)\,dt$ for every $x \in \mathbb R$.
    ///

    /// note | 📖 **Definition**
    <u>**Continuous random variable**</u>

    A {term}`random variable` $X$ is continuous iff some {term}`probability density function` is a density of $X$. We then write $f_X$ for a chosen density of $X$.
    ///

    "Continuous" refers to the existence of a density, not to continuity of $X$ as a function on $\Omega$ (which would not even make sense, since $\Omega$ has no notion of nearness). Some books say *absolutely continuous*.

    /// admonition | 📐 **Theorem (Densities Give Interval Probabilities)**
        attrs: {class: theorem, id: ch5-thm-densities-give-interval-probabilities}
    Let $X$ have density $f_X$. Then:

    1. $\mathbb P(a < X \le b) = \int_a^b f_X(t)\,dt$ whenever $a < b$.
    2. $F_X$ is continuous, so $\mathbb P(X = x) = 0$ for every $x \in \mathbb R$. Consequently $\mathbb P(a < X \le b) = \mathbb P(a \le X \le b) = \mathbb P(a < X < b) = \mathbb P(a \le X < b)$.
    3. At every $x$ where $f_X$ is continuous, $F_X$ is differentiable and $F_X'(x) = f_X(x)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    1. By property 4 of CDFs, $\mathbb P(a < X \le b) = \int_{-\infty}^b f_X - \int_{-\infty}^a f_X = \int_a^b f_X$, by additivity of the integral over adjacent intervals.
    2. A (possibly improper) integral is a continuous function of its upper limit ([Appendix C: The Fundamental Theorem of Calculus](#appc-sec-the-fundamental-theorem-of-calculus), [Appendix C: Improper Integrals](#appc-sec-improper-integrals)), so $F_X$ is continuous. By property 5 of CDFs, $\mathbb P(X = x) = F_X(x) - F_X(x^-) = 0$. The equalities follow by finite additivity, adding or removing endpoints of probability $0$.
    3. This is the first part of the fundamental theorem of calculus applied to $F_X(x) = \int_{-\infty}^x f_X$. $\blacksquare$
    ///

    **Remarks.**

    - *Densities are not unique.* Changing $f_X$ at finitely many points changes no integral, so it gives another density of the same $X$. By part 3, a density is pinned down at every point where it is continuous, which is all that ever matters in practice.
    - *A density is not a probability.* $f_X(x)$ can exceed $1$ (the uniform distribution on $[0, \tfrac12]$, defined below, has density $2$ there). By part 3, $\mathbb P(x < X \le x + h) \approx f_X(x)\,h$ for small $h > 0$: the density is probability *per unit length*, measured for scale noise in "per lb."
    - *Discrete and continuous are mutually exclusive.* If $X$ is continuous and $C$ is countable, countable additivity and part 2 give $\mathbb P(X \in C) = \sum_{c \in C} \mathbb P(X = c) = 0$.
    - *Some random variables are neither.* Suppose the scale's converter saturates, so that every weight above its maximum $m$ is reported as $m$. If the incoming weight $X$ is continuous with $\mathbb P(X \ge m) > 0$, the reported value $\min(X, m)$ has $\mathbb P(\min(X,m) = m) = \mathbb P(X \ge m) > 0$, so it is not continuous; and it spreads the remaining probability continuously below $m$, so it is not discrete either. There are even random variables with a continuous CDF and no density ([Wikipedia: Cantor distribution](https://en.wikipedia.org/wiki/Cantor_distribution)).
    - *The Lebesgue generalization.* With the Lebesgue integral, every density $f_X$ above also satisfies $\mathbb P(X \in B) = \int_B f_X$ for *every* Borel set $B$, and a density may be any nonnegative Borel function with integral $1$ ([Wikipedia: Probability density function](https://en.wikipedia.org/wiki/Probability_density_function), [Wikipedia: Lebesgue integration](https://en.wikipedia.org/wiki/Lebesgue_integration)). The Riemann integral cannot even be defined over most Borel sets, which is why we work with intervals.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch5-sec-the-uniform-and-normal-distributions -->
    ## The Uniform and Normal Distributions

    Two distributions do almost all the work in this book. Because a CDF determines its distribution, we can name a distribution by giving a density.

    /// note | 📖 **Definition**
    <u>**Uniform distribution**</u>

    Let $a < b$ be real numbers. A {term}`random variable` $X$ has the uniform distribution on $[a, b]$, written $X \sim \mathcal U(a, b)$, iff the function
    $$f(x) := \begin{cases} \dfrac{1}{b - a}, & a \le x \le b, \\[4pt] 0, & \text{otherwise}, \end{cases}$$
    is a density of $X$.
    ///

    The function $f$ is a PDF: it is nonnegative, Riemann integrable on every bounded interval, and $\int_{-\infty}^\infty f = (b-a) \cdot \frac{1}{b-a} = 1$. Integrating it gives the CDF: $F_X(x) = 0$ for $x < a$, $F_X(x) = \frac{x - a}{b - a}$ for $a \le x \le b$, and $F_X(x) = 1$ for $x > b$. For $a \le c < d \le b$, $\mathbb P(c < X \le d) = \frac{d - c}{b - a}$: subintervals of equal length are equally likely, which is what "uniform" means. The random variable $U(\omega) = \omega$ on Chapter 4's uniform probability space satisfies $U \sim \mathcal U(0, 1)$, and the theorem on every CDF guarantees $\mathcal U(a, b)$ exists for all $a < b$.

    /// note | 📖 **Definition**
    <u>**Normal distribution**</u>

    Let $\mu \in \mathbb R$ and $\sigma > 0$. A {term}`random variable` $X$ has the normal (or Gaussian) distribution with parameters $\mu$ and $\sigma^2$, written $X \sim \mathcal N(\mu, \sigma^2)$, iff the function
    $$\varphi_{\mu, \sigma}(x) := \frac{1}{\sigma\sqrt{2\pi}} \exp\!\Big(-\frac{(x - \mu)^2}{2\sigma^2}\Big)$$
    is a density of $X$. The case $\mathcal N(0, 1)$ is the *standard* normal distribution; its density and CDF are written $\varphi := \varphi_{0,1}$ and $\Phi$.
    ///

    /// admonition | 📐 **Theorem (The Normal Density Is a PDF)**
        attrs: {class: theorem, id: ch5-thm-the-normal-density-is-a-pdf}
    For every $\mu \in \mathbb R$ and $\sigma > 0$, $\varphi_{\mu,\sigma}$ is a probability density function.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    $\varphi_{\mu,\sigma}$ is positive and continuous (the {term}`exponential function` is continuous), so it is Riemann integrable on every bounded interval. Substituting $x = \mu + \sigma z$, $dx = \sigma\,dz$ on $[\mu - \sigma M, \mu + \sigma M]$ gives
    $$\int_{\mu - \sigma M}^{\mu + \sigma M} \varphi_{\mu,\sigma}(x)\,dx = \frac{1}{\sqrt{2\pi}} \int_{-M}^{M} e^{-z^2/2}\,dz.$$
    As $M \to \infty$ the right side tends to $\frac{1}{\sqrt{2\pi}} \cdot \sqrt{2\pi} = 1$ by the Gaussian integral ([Appendix C: Multiple Integrals](#appc-sec-multiple-integrals)), which includes the convergence of the improper integral. Since the integrand is positive, the improper integral over $\mathbb R$ exists and equals this limit. $\blacksquare$
    ///

    The parameter $\mu$ is the center of symmetry, $\varphi_{\mu,\sigma}(\mu + t) = \varphi_{\mu,\sigma}(\mu - t)$, and $\sigma$ sets the width: the next section shows that changing $\sigma$ simply stretches the bell horizontally. Chapter 6 shows that $\mu$ is the expected value of $X$ and $\sigma^2$ its variance; until then they are just parameters. The CDF $\Phi$ has no formula in terms of elementary functions and is computed numerically ([Wikipedia: Error function](https://en.wikipedia.org/wiki/Error_function)).

    Why this particular bell? A load cell's noise is the sum of many small, roughly independent effects, and Chapter 8 states the central limit theorem, which says that such sums are approximately normal. Chapter 8 also shows the normal distribution makes the optimal filter linear. Both facts are reasons to *choose* this model; neither makes it true for a particular sensor.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch5-sec-functions-of-a-random-variable -->
    ## Functions of a Random Variable

    A scale that reports in kilograms instead of pounds, or that adds a calibration offset, applies an affine map $x \mapsto ax + b$ to its readings. The [Density of $aX + b$ theorem](#ch5-thm-density-of-ax-b) below says how densities transform under such maps.

    /// admonition | 📐 **Theorem (Density of $aX + b$)**
        attrs: {class: theorem, id: ch5-thm-density-of-ax-b}
    Let $X$ have density $f_X$, and let $a, b \in \mathbb R$ with $a \ne 0$. Then $Y := aX + b$ is continuous with density
    $$f_Y(y) = \frac{1}{|a|}\, f_X\!\Big(\frac{y - b}{a}\Big).$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    $Y$ is a random variable by the theorem on building random variables. Fix $y \in \mathbb R$ and put $t_y := \frac{y - b}{a}$. We use the substitution $t = \frac{s - b}{a}$, $dt = \frac{ds}{a}$ ([Appendix C: The Fundamental Theorem of Calculus](#appc-sec-the-fundamental-theorem-of-calculus)), applied on bounded intervals and then extended to the improper integrals by letting the infinite endpoint go to infinity.

    *Case $a > 0$.* $\{Y \le y\} = \{X \le t_y\}$, so
    $$F_Y(y) = \int_{-\infty}^{t_y} f_X(t)\,dt = \int_{-\infty}^{y} f_X\!\Big(\frac{s - b}{a}\Big) \frac{1}{a}\,ds.$$

    *Case $a < 0$.* Multiplying by a negative number reverses inequalities, so $\{Y \le y\} = \{X \ge t_y\}$. Since $\mathbb P(X = t_y) = 0$,
    $$F_Y(y) = 1 - F_X(t_y) = \int_{t_y}^{\infty} f_X(t)\,dt = \int_{y}^{-\infty} f_X\!\Big(\frac{s-b}{a}\Big)\frac{1}{a}\,ds = \int_{-\infty}^{y} f_X\!\Big(\frac{s-b}{a}\Big)\frac{1}{|a|}\,ds,$$
    because as $t$ runs from $t_y$ up to $\infty$, $s = at + b$ runs from $y$ down to $-\infty$.

    In both cases $F_Y(y) = \int_{-\infty}^y f_Y$ for every $y$. Finally $f_Y \ge 0$, and $\int_{-\infty}^\infty f_Y = \lim_{y \to \infty} F_Y(y) = 1$ by property 3 of CDFs, so $f_Y$ is a PDF. $\blacksquare$
    ///

    /// admonition | 📐 **Corollary (Affine Maps of Normal and Uniform Random Variables)**
        attrs: {class: corollary, id: ch5-cor-affine-maps-of-normal-and-uniform-random-variables}
    Let $a, b \in \mathbb R$ with $a \ne 0$.

    1. If $X \sim \mathcal N(\mu, \sigma^2)$, then $aX + b \sim \mathcal N(a\mu + b, a^2\sigma^2)$.
    2. In particular, if $X \sim \mathcal N(\mu, \sigma^2)$ then $\frac{X - \mu}{\sigma} \sim \mathcal N(0, 1)$, and if $Z \sim \mathcal N(0, 1)$ then $\mu + \sigma Z \sim \mathcal N(\mu, \sigma^2)$.
    3. If $U \sim \mathcal U(0, 1)$ and $c < d$, then $c + (d - c)U \sim \mathcal U(c, d)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    1. By the theorem,
    $$f_{aX+b}(y) = \frac{1}{|a|} \cdot \frac{1}{\sigma\sqrt{2\pi}} \exp\!\Big(-\frac{\big(\frac{y-b}{a} - \mu\big)^2}{2\sigma^2}\Big) = \frac{1}{|a|\sigma\sqrt{2\pi}} \exp\!\Big(-\frac{\big(y - (a\mu + b)\big)^2}{2a^2\sigma^2}\Big),$$
    which is $\varphi_{a\mu + b,\, |a|\sigma}(y)$.
    2. Take $a = \frac1\sigma$, $b = -\frac\mu\sigma$ in part 1. For the second statement, apply part 1 to $Z \sim \mathcal N(0, 1)$ with $a = \sigma$, $b = \mu$.
    3. By the theorem with $a = d - c$, $b = c$, the density of $c + (d-c)U$ at $y$ is $\frac{1}{d-c}$ if $0 \le \frac{y-c}{d-c} \le 1$, that is, if $c \le y \le d$, and $0$ otherwise. $\blacksquare$
    ///

    Part 2 is how simulations produce normal noise: draw a standard normal sample $Z$ and return $\mu + \sigma Z$. NumPy's `rng.normal(loc=mu, scale=sigma)` does exactly this. It also means a single table of $\Phi$ answers every question about every normal distribution, since $\mathbb P(|X - \mu| \le k\sigma) = \mathbb P(|Z| \le k)$:
    """)
    return


@app.cell(hide_code=True)
def _(math, mo):
    _lines = [
        r"| $k$ | $\mathbb P(\lvert X - \mu\rvert \le k\sigma)$ | $\mathbb P(\lvert X - \mu\rvert > k\sigma)$ |",
        "|:---|:---:|:---:|",
    ]
    for _k in (1, 2, 3, 5):
        _p = math.erf(_k / math.sqrt(2))
        _lines.append(f"| ${_k}$ | ${_p:.4f}$ | ${1 - _p:.2g}$ |")
    _lines += [
        "",
        r"So about 68% of normal readings fall within $\sigma$ of $\mu$, 95% within $2\sigma$, "
        r"and 99.7% within $3\sigma$. A deviation of $5\sigma$ or more should happen about once "
        r"in two million readings, a number to remember when we discuss outliers at the end of the chapter.",
    ]
    mo.md("\n".join(_lines))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch5-sec-quantization-noise -->
    ### Quantization Noise

    A digital scale cannot display every real number. Suppose it shows the weight rounded to the nearest multiple of a resolution $\Delta > 0$, for example $\Delta = 0.1$ lb. By the Archimedean property ([Chapter 3](#ch3-thm-archimedean-property)), each $y \in \mathbb R$ lies in exactly one interval $[n, n+1)$ with $n \in \mathbb Z$; write $\lfloor y \rfloor := n$. Define the rounding function and its *cells*
    $$Q(y) := \Delta \Big\lfloor \frac{y}{\Delta} + \frac12 \Big\rfloor, \qquad C_j := \big[j\Delta - \tfrac\Delta2,\ j\Delta + \tfrac\Delta2\big) \quad (j \in \mathbb Z),$$
    so that $Q(y) = j\Delta$ exactly when $y \in C_j$. The cells are pairwise disjoint and their union is $\mathbb R$. If the incoming weight is a random variable $X$, the displayed value is $Q(X)$ and the *quantization error* is $E := Q(X) - X$, which always lies in $(-\tfrac\Delta2, \tfrac\Delta2]$. Both are random variables: $\{Q(X) \le c\} = \bigcup_{j : j\Delta \le c} \{X \in C_j\}$ is a countable union of events, and $E$ is a sum of random variables.

    A common modeling assumption is that $E \sim \mathcal U(-\tfrac\Delta2, \tfrac\Delta2)$. Call a density $f$ *unimodal* iff there is an $m \in \mathbb R$ such that $f$ is nondecreasing on $(-\infty, m]$ and nonincreasing on $[m, \infty)$. The following theorem says when the assumption is justified.

    /// admonition | 📐 **Theorem (Quantization Error Is Nearly Uniform)**
        attrs: {class: theorem, id: ch5-thm-quantization-error-is-nearly-uniform}
    Let $X$ have a unimodal density $f$ bounded by $M$. Then for all $-\tfrac\Delta2 \le e_1 < e_2 \le \tfrac\Delta2$,
    $$\Big|\, \mathbb P(e_1 < E \le e_2) - \frac{e_2 - e_1}{\Delta} \,\Big| \le 3M\Delta \cdot \frac{e_2 - e_1}{\Delta}.$$
    That is, every interval probability of $E$ is within a relative error $3M\Delta$ of the corresponding probability under $\mathcal U(-\tfrac\Delta2, \tfrac\Delta2)$. If $X \sim \mathcal N(\mu, \sigma^2)$ for any $\mu$, the relative error is at most $3\Delta/(\sigma\sqrt{2\pi}) < 1.2\,\Delta/\sigma$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Let $\ell := e_2 - e_1$. On the event $\{X \in C_j\}$ we have $E = j\Delta - X$, so
    $$\{e_1 < E \le e_2\} \cap \{X \in C_j\} = \{X \in I_j\}, \qquad I_j := [\,j\Delta - e_2,\ j\Delta - e_1),$$
    an interval of length $\ell$ contained in $C_j$ (because $-\tfrac\Delta2 \le e_1 < e_2 \le \tfrac\Delta2$). The cells partition $\mathbb R$, so countable additivity gives
    $$\mathbb P(e_1 < E \le e_2) = \sum_{j \in \mathbb Z} \int_{I_j} f, \qquad \frac{\ell}{\Delta} = \frac{\ell}{\Delta}\,\mathbb P(X \in \mathbb R) = \sum_{j \in \mathbb Z} \frac{\ell}{\Delta}\int_{C_j} f.$$
    Let $s_j$ and $i_j$ be the supremum and infimum of $f$ on $C_j$. Bounding each integral by its integrand's extremes, both $\int_{I_j} f$ and $\frac{\ell}{\Delta}\int_{C_j} f$ lie in the interval $[\ell\, i_j, \ell\, s_j]$, so they differ by at most $\ell\,(s_j - i_j)$. Both series converge, so the difference of their sums is the sum of the differences, and
    $$\Big|\,\mathbb P(e_1 < E \le e_2) - \frac{\ell}{\Delta}\,\Big| \le \ell \sum_{j \in \mathbb Z} (s_j - i_j).$$
    It remains to show $\sum_j (s_j - i_j) \le 3M$. Let $C_{j_0}$ be the cell containing $m$. For $j < j_0$, the cell $C_j$ lies to the left of $m$, where $f$ is nondecreasing, so $s_j - i_j \le f\big(j\Delta + \tfrac\Delta2\big) - f\big(j\Delta - \tfrac\Delta2\big)$. These bounds telescope: for any $J$, $\sum_{j=-J}^{j_0 - 1}(s_j - i_j) \le f\big(j_0\Delta - \tfrac\Delta2\big) - f\big(-J\Delta - \tfrac\Delta2\big) \le M$. The cells to the right of $C_{j_0}$ contribute at most $M$ in the same way, and $s_{j_0} - i_{j_0} \le M$. So the sum is at most $3M$, and dividing the final bound by $\ell/\Delta$ gives the relative form.

    For $X \sim \mathcal N(\mu, \sigma^2)$: $\varphi_{\mu,\sigma}$ increases on $(-\infty, \mu]$ and decreases on $[\mu, \infty)$ because $-(x - \mu)^2$ does and $\exp$ is increasing, and its maximum is $M = \varphi_{\mu,\sigma}(\mu) = \frac{1}{\sigma\sqrt{2\pi}}$. Finally $3/\sqrt{2\pi} \approx 1.197$. $\blacksquare$
    ///

    So quantization error behaves like uniform noise when the noise $\sigma$ is large compared with the resolution $\Delta$. With the canonical scale numbers ($\sigma = 1$ lb, $\Delta = 0.1$ lb) the relative error is below $12\%$. When $\sigma$ is comparable to or smaller than $\Delta$, the bound says nothing, and the error really is far from uniform. Try it below: the true weight is $155.03$ lb and the display resolution is $0.1$ lb.
    """)
    return


@app.cell
def _(np):
    # jb: include=false
    std_normal_draws = np.random.default_rng(1).standard_normal(20_000)
    return (std_normal_draws,)


@app.cell(hide_code=True)
def _(mo):
    quant_sigma_slider = mo.ui.slider(
        steps=[0.005, 0.01, 0.02, 0.03, 0.05, 0.075, 0.1, 0.15, 0.2, 0.3, 0.5],
        value=0.2,
        label=r"noise $\sigma$ (lb)",
        show_value=True,
    )
    return (quant_sigma_slider,)


@app.cell(hide_code=True)
def _(graphic, math, mo, np, plt, quant_sigma_slider, std_normal_draws):
    _delta = 0.1
    _x_true = 155.03
    _sigma = quant_sigma_slider.value
    _z = _x_true + _sigma * std_normal_draws
    _q = _delta * np.floor(_z / _delta + 0.5)
    _err = _q - _z

    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(10, 3.8))
    _heights, _, _ = _ax1.hist(_err, bins=np.linspace(-_delta / 2, _delta / 2, 41), density=True,
                               color="C0", alpha=0.6, label="simulated error $E$")
    _ax1.axhline(1 / _delta, color="black", linewidth=1.5,
                 label=r"$\mathcal{U}(-\Delta/2, \Delta/2)$ density")
    _ax1.set_ylim(0, max(1.6 / _delta, 1.1 * _heights.max()))
    _ax1.set_xlabel("quantization error $E$ (lb)")
    _ax1.set_ylabel("density (1/lb)")
    _ax1.set_title("Distribution of the quantization error", style="italic")
    _ax1.legend(loc="upper right", fontsize=8)
    _ax1.grid(visible=True, alpha=0.9, linewidth=0.4)

    _k = np.arange(1, 31)
    _ax2.plot(_k, np.full(30, _x_true), color="black", linewidth=1.2, label="true weight")
    _ax2.plot(_k, _z[:30], ".", color="C0", label="weight + noise")
    _ax2.plot(_k, _q[:30], "o", markerfacecolor="none", markeredgecolor="black",
              label="displayed reading")
    _ax2.set_xlabel("sample $k$")
    _ax2.set_ylabel("weight (lb)")
    _ax2.set_title("First 30 readings at 10 samples/s", style="italic")
    _ax2.legend(loc="upper right", fontsize=8)
    _ax2.grid(visible=True, alpha=0.9, linewidth=0.4)
    _fig.tight_layout()
    _plot = graphic(_fig)
    plt.close(_fig)

    _bound = 3 * _delta / (_sigma * math.sqrt(2 * math.pi))
    _avg_err = _q.mean() - _x_true
    mo.vstack([
        quant_sigma_slider,
        _plot,
        mo.md(
            f"Relative error bound $3\\Delta/(\\sigma\\sqrt{{2\\pi}})$ = **{_bound:.2f}**"
            + (" (meaningful)" if _bound < 1 else " (no information)")
            + f". Average of the {len(_q):,} displayed readings minus the true weight: **{_avg_err:+.4f} lb**."
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With $\sigma = 0.2$ lb the error histogram is flat and averaging the displayed readings recovers the true weight. Now drag $\sigma$ down to $0.005$ lb. Nearly every reading displays $155.0$, the error concentrates near $-0.03$ lb, and the average of the displayed readings is stuck $0.03$ lb too low no matter how many readings we take. Quantization is then a *deterministic* error, and no amount of averaging removes it. Paradoxically, a little noise helps: it spreads the readings across neighboring display values so their average carries information finer than $\Delta$, a technique engineers call *dither* ([Wikipedia: Dither](https://en.wikipedia.org/wiki/Dither)). Chapter 9 computes the variance of quantization noise and studies {term}`quantization` further.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch5-sec-joint-distributions -->
    ## Joint Distributions

    Filters combine several random quantities: consecutive readings $Z_1, Z_2, \ldots$, or (from Chapter 7 on) a prediction and a measurement. Questions such as "are both of the first two readings above 156 lb?" involve several random variables at once, so we need probabilities of sets in $\mathbb R^n$, the set of $n$-tuples of real numbers (the {term}`Cartesian product` of $n$ copies of $\mathbb R$).

    A *box* in $\mathbb R^n$ is a product $I_1 \times \cdots \times I_n$ of intervals. The *Borel $\sigma$-algebra* of $\mathbb R^n$ is $\mathcal B(\mathbb R^n) := \sigma(\{\text{boxes in } \mathbb R^n\})$; for $n = 1$ it is $\mathcal B(\mathbb R)$. For random variables $X_1, \ldots, X_n$ on the same probability space, write $(X_1, \ldots, X_n)$ for the function $\Omega \to \mathbb R^n$, $\omega \mapsto (X_1(\omega), \ldots, X_n(\omega))$.

    /// admonition | 📐 **Lemma (Vectors of Random Variables)**
        attrs: {class: lemma, id: ch5-lem-vectors-of-random-variables}
    If $X_1, \ldots, X_n$ are random variables on $(\Omega, \mathcal F, \mathbb P)$, then $\{(X_1, \ldots, X_n) \in B\} \in \mathcal F$ for every $B \in \mathcal B(\mathbb R^n)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    As in the measurability test, the collection of $B \subseteq \mathbb R^n$ whose preimage under $(X_1, \ldots, X_n)$ is in $\mathcal F$ is a $\sigma$-algebra. It contains every box, because the preimage of $I_1 \times \cdots \times I_n$ is $\{X_1 \in I_1\} \cap \cdots \cap \{X_n \in I_n\}$, a finite intersection of events. So it contains the $\sigma$-algebra generated by the boxes. $\blacksquare$
    ///

    /// note | 📖 **Definition**
    <u>**Joint distribution**</u>

    The joint distribution of {term}`random variables <random variable>` $X_1, \ldots, X_n$ on the same probability space is the function $\mathbb P_{X_1, \ldots, X_n} : \mathcal B(\mathbb R^n) \to [0, 1]$ defined by $\mathbb P_{X_1, \ldots, X_n}(B) := \mathbb P\big((X_1, \ldots, X_n) \in B\big)$.
    ///

    Exactly as for one random variable, the joint distribution is a probability measure on $(\mathbb R^n, \mathcal B(\mathbb R^n))$. It determines each individual distribution, for example $\mathbb P_{X_1}(B) = \mathbb P_{X_1, \ldots, X_n}(B \times \mathbb R^{n-1})$; in this context the individual distributions are called *marginal distributions*. The converse fails: the marginals do not determine the joint distribution. In the coin example, the pairs $(X, X)$ and $(X, X')$, with $X'$ the number of tails, have identical marginals (all four are the distribution of $X$), but $\mathbb P(X = 2, X = 2) = \tfrac14$ while $\mathbb P(X = 2, X' = 2) = 0$. How random variables *relate* to each other is extra information.

    The *joint CDF* is $F_{X_1, \ldots, X_n}(x_1, \ldots, x_n) := \mathbb P(X_1 \le x_1, \ldots, X_n \le x_n)$. By the same $\pi$-$\lambda$ argument as in one dimension, it determines the joint distribution.

    /// note | 📖 **Definition**
    <u>**Joint density**</u>

    A function $f : \mathbb R^n \to [0, \infty)$ is a joint density of {term}`random variables <random variable>` $X_1, \ldots, X_n$ iff
    $$F_{X_1, \ldots, X_n}(x_1, \ldots, x_n) = \int_{-\infty}^{x_1} \cdots \int_{-\infty}^{x_n} f(t_1, \ldots, t_n)\,dt_n \cdots dt_1 \quad \text{for every } (x_1, \ldots, x_n) \in \mathbb R^n.$$
    ///

    As in one dimension, these are (possibly improper) Riemann integrals. We assume, as holds for every joint density in this book, that $f$ is regular enough for Fubini's theorem ([Appendix C: Multiple Integrals](#appc-sec-multiple-integrals)), so that iterated integrals of $f$ over boxes and quadrants exist and may be computed in any order.

    /// admonition | 📐 **Theorem (Box Probabilities)**
        attrs: {class: theorem, id: ch5-thm-box-probabilities}
    If $f$ is a joint density of $(X, Y)$, then for all $a_1 < b_1$ and $a_2 < b_2$,
    $$\mathbb P(a_1 < X \le b_1,\ a_2 < Y \le b_2) = \int_{a_1}^{b_1} \int_{a_2}^{b_2} f(s, t)\,dt\,ds.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Write $G := F_{X,Y}$. For any $y$, the event $\{X \le b_1, Y \le y\}$ is the disjoint union of $\{X \le a_1, Y \le y\}$ and $\{a_1 < X \le b_1, Y \le y\}$, so $\mathbb P(a_1 < X \le b_1, Y \le y) = G(b_1, y) - G(a_1, y)$. Splitting the same way in $Y$,
    $$\mathbb P(a_1 < X \le b_1,\ a_2 < Y \le b_2) = \big[G(b_1, b_2) - G(a_1, b_2)\big] - \big[G(b_1, a_2) - G(a_1, a_2)\big].$$
    Substitute the integral formula for each $G$ term. By additivity over adjacent intervals, $\int_{-\infty}^{b_1} - \int_{-\infty}^{a_1} = \int_{a_1}^{b_1}$ in $s$, and likewise in $t$, which leaves $\int_{a_1}^{b_1}\int_{a_2}^{b_2} f\,dt\,ds$. $\blacksquare$
    ///

    With the Lebesgue integral, $\mathbb P\big((X,Y) \in B\big) = \iint_B f$ holds for every Borel set $B \subseteq \mathbb R^2$, not just boxes. Moreover, every nonnegative $f$ on $\mathbb R^n$ with integral $1$ is the joint density of some random variables (take $\Omega = \mathbb R^n$ with the probability measure $B \mapsto \int_B f$). Both facts need measure theory ([Wikipedia: Probability density function](https://en.wikipedia.org/wiki/Probability_density_function)).

    /// note | 📖 **Definition**
    <u>**Marginal density**</u>

    If $f$ is a {term}`joint density` of $X_1, \ldots, X_n$, the marginal density of $X_i$ is the function obtained by integrating $f$ over all variables except the $i$-th. For $n = 2$ and a joint density $f$ of $(X, Y)$:
    $$f_X(x) := \int_{-\infty}^{\infty} f(x, y)\,dy, \qquad f_Y(y) := \int_{-\infty}^{\infty} f(x, y)\,dx.$$
    ///

    /// admonition | 📐 **Theorem (The Marginal Density Is a Density)**
        attrs: {class: theorem, id: ch5-thm-the-marginal-density-is-a-density}
    If $f$ is a joint density of $(X, Y)$, then $X$ is continuous and its marginal density $f_X$ is a density of $X$. The same holds for $Y$, and for each $X_i$ when there are $n$ random variables.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    The events $\{X \le x, Y \le n\}$ increase with $n$, and their union is $\{X \le x\}$ because every real number $Y(\omega)$ is at most some integer $n$. Continuity from below and Fubini's theorem give
    $$F_X(x) = \lim_{n \to \infty} \int_{-\infty}^{x}\int_{-\infty}^{n} f(s, t)\,dt\,ds = \lim_{n \to \infty} \int_{-\infty}^{n}\int_{-\infty}^{x} f(s, t)\,ds\,dt = \int_{-\infty}^{\infty}\int_{-\infty}^{x} f(s, t)\,ds\,dt.$$
    The last step is the definition of an improper integral in $t$. Exchanging the order once more, $F_X(x) = \int_{-\infty}^x \int_{-\infty}^\infty f(s,t)\,dt\,ds = \int_{-\infty}^x f_X(s)\,ds$. Taking $x \to \infty$ shows $\int f_X = 1$, so $f_X$ is a PDF and a density of $X$. For $n$ variables, integrate out one variable at a time. $\blacksquare$
    ///

    **Example.** Let $(X, Y)$ have joint density $f(x, y) = x + y$ for $(x, y) \in [0,1]^2$ and $f = 0$ elsewhere. It is a valid joint density: $\int_0^1\int_0^1 (x + y)\,dy\,dx = \int_0^1 (x + \tfrac12)\,dx = 1$. The marginal density of $X$ is $f_X(x) = \int_0^1 (x + y)\,dy = x + \tfrac12$ for $x \in [0, 1]$ (and $0$ elsewhere), and by symmetry $f_Y(y) = y + \tfrac12$ on $[0, 1]$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch5-sec-independence -->
    ## Independence

    [Chapter 4](#ch4-sec-independence) called events independent when the probability of their intersection factors. Random variables are independent when *every* question about one is independent of every question about the others.

    /// note | 📖 **Definition**
    <u>**Independent random variables**</u>

    {term}`Random variables <random variable>` $X_1, \ldots, X_n$ on the same probability space are independent iff
    $$\mathbb P(X_1 \in B_1, \ldots, X_n \in B_n) = \prod_{i=1}^{n} \mathbb P(X_i \in B_i) \quad \text{for all Borel sets } B_1, \ldots, B_n \subseteq \mathbb R.$$
    An arbitrary {term}`indexed family` of random variables on the same probability space is independent iff every finite subfamily is.
    ///

    Taking $B_i = \mathbb R$ for the indices outside a subfamily shows that the definition is the same as requiring that, for every choice of Borel sets, the events $\{X_1 \in B_1\}, \ldots, \{X_n \in B_n\}$ are mutually independent in the sense of [Chapter 4](#ch4-sec-independence). Checking all Borel sets is impractical; the following criteria reduce it to CDFs, PMFs, or densities.

    /// admonition | 📐 **Theorem (Factorization Criteria)**
        attrs: {class: theorem, id: ch5-thm-factorization-criteria}
    Let $X_1, \ldots, X_n$ be random variables on the same probability space.

    1. *(CDFs)* They are independent iff $F_{X_1, \ldots, X_n}(x_1, \ldots, x_n) = \prod_{i=1}^n F_{X_i}(x_i)$ for all $(x_1, \ldots, x_n) \in \mathbb R^n$.
    2. *(PMFs)* If each $X_i$ is discrete, they are independent iff $\mathbb P(X_1 = x_1, \ldots, X_n = x_n) = \prod_{i=1}^n p_{X_i}(x_i)$ for all $(x_1, \ldots, x_n) \in \mathbb R^n$.
    3. *(Densities)* If each $X_i$ has a density $f_{X_i}$, they are independent iff $(x_1, \ldots, x_n) \mapsto \prod_{i=1}^n f_{X_i}(x_i)$ is a joint density of $X_1, \ldots, X_n$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    1. ($\Rightarrow$) Take $B_i = (-\infty, x_i]$. ($\Leftarrow$) Not given here: it follows from Dynkin's $\pi$-$\lambda$ theorem, applied one coordinate at a time ([Wikipedia: Independence (probability theory)](https://en.wikipedia.org/wiki/Independence_(probability_theory)), [Wikipedia: Dynkin system](https://en.wikipedia.org/wiki/Dynkin_system)).
    2. ($\Rightarrow$) Take $B_i = \{x_i\}$. ($\Leftarrow$) Let $\mathbb P(X_i \in C_i) = 1$ with $C_i$ countable, and let $B_1, \ldots, B_n$ be Borel. The event $\{X_1 \in B_1, \ldots, X_n \in B_n\}$ differs from the disjoint union of the events $\{X_1 = x_1, \ldots, X_n = x_n\}$ over $(x_1, \ldots, x_n) \in (B_1 \cap C_1) \times \cdots \times (B_n \cap C_n)$ only by a subset of $\bigcup_i \{X_i \notin C_i\}$, which has probability $0$ by the union bound. That index set is countable ([Chapter 3](#ch3-sec-countable-and-uncountable-sets)), so countable additivity and the hypothesis give
    $$\mathbb P(X_1 \in B_1, \ldots, X_n \in B_n) = \sum_{x_1 \in B_1 \cap C_1} \cdots \sum_{x_n \in B_n \cap C_n} \prod_{i=1}^n p_{X_i}(x_i) = \prod_{i=1}^n \sum_{x_i \in B_i \cap C_i} p_{X_i}(x_i) = \prod_{i=1}^n \mathbb P(X_i \in B_i),$$
    where the middle step factors a sum of nonnegative products ([Appendix C: Series](#appc-sec-series)) and the last step is the theorem on PMFs.
    3. An iterated integral of a product of functions of separate variables is the product of the one-dimensional integrals (pull each factor that does not depend on the current integration variable out of that integral). So for every $(x_1, \ldots, x_n)$,
    $$\int_{-\infty}^{x_1}\cdots\int_{-\infty}^{x_n} \prod_{i=1}^n f_{X_i}(t_i)\,dt_n\cdots dt_1 = \prod_{i=1}^n \int_{-\infty}^{x_i} f_{X_i} = \prod_{i=1}^n F_{X_i}(x_i).$$
    ($\Rightarrow$) By part 1, the right side equals $F_{X_1, \ldots, X_n}(x_1, \ldots, x_n)$, so the product is a joint density. ($\Leftarrow$) If the product is a joint density, the left side equals $F_{X_1, \ldots, X_n}(x_1, \ldots, x_n)$, so the joint CDF factors, and part 1 gives independence. $\blacksquare$
    ///

    **Examples.**

    - If $X, Y \sim \mathcal N(0, 1)$ are independent, their joint density is $\varphi(x)\varphi(y) = \frac{1}{2\pi} e^{-(x^2 + y^2)/2}$. It depends only on the distance from the origin, a symmetry Chapter 12 exploits.
    - The pair with joint density $x + y$ on $[0,1]^2$ is *not* independent. Directly from the definition,
    $$\mathbb P\big(X \le \tfrac12, Y \le \tfrac12\big) = \int_0^{1/2}\!\!\int_0^{1/2} (s + t)\,dt\,ds = \tfrac18, \quad \text{but} \quad \mathbb P\big(X \le \tfrac12\big)\,\mathbb P\big(Y \le \tfrac12\big) = \Big(\int_0^{1/2} \big(s + \tfrac12\big)\,ds\Big)^2 = \tfrac{9}{64}.$$

    /// admonition | 📐 **Theorem (Functions of Independent Random Variables)**
        attrs: {class: theorem, id: ch5-thm-functions-of-independent-random-variables}
    If $X_1, \ldots, X_n$ are independent and $g_1, \ldots, g_n : \mathbb R \to \mathbb R$ are Borel, then $g_1(X_1), \ldots, g_n(X_n)$ are independent.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    For Borel sets $B_i$, $\{g_i(X_i) \in B_i\} = \{X_i \in g_i^{-1}[B_i]\}$, and each $g_i^{-1}[B_i]$ is Borel. Apply the definition of independence to the Borel sets $g_i^{-1}[B_i]$. $\blacksquare$
    ///

    For example, if the noise values $V_1, \ldots, V_n$ are independent, so are the readings $x_1 + V_1, \ldots, x_n + V_n$. We also need to *group* independent random variables, for example to know that $V_1 + V_2$ is independent of $V_3$. A function $g : \mathbb R^m \to \mathbb R$ is Borel iff $g^{-1}[B] \in \mathcal B(\mathbb R^m)$ for every $B \in \mathcal B(\mathbb R)$; continuous functions, such as sums, products, and linear combinations, are Borel, by the same fact about open sets as in one dimension. For Borel $g$, $g(X_1, \ldots, X_m)$ is a random variable, because $\{g(X_1, \ldots, X_m) \in B\} = \{(X_1, \ldots, X_m) \in g^{-1}[B]\}$ is an event by the [Vectors of Random Variables lemma](#ch5-lem-vectors-of-random-variables).

    /// admonition | 📐 **Theorem (Grouping)**
        attrs: {class: theorem, id: ch5-thm-grouping}
    If $X_1, \ldots, X_n$ are independent, $1 \le m < n$, and $g : \mathbb R^m \to \mathbb R$ is Borel, then $g(X_1, \ldots, X_m), X_{m+1}, \ldots, X_n$ are independent.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Not given here; like the CDF criterion, it follows from Dynkin's $\pi$-$\lambda$ theorem ([Wikipedia: Dynkin system](https://en.wikipedia.org/wiki/Dynkin_system)).
    ///

    The most important case in this book is a sequence of independent copies of one random variable.

    /// note | 📖 **Definition**
    <u>**Independent and identically distributed**</u>

    An {term}`indexed family` of {term}`random variables <random variable>` is independent and identically distributed (i.i.d.) iff it is independent and all of its members have the same {term}`distribution`.
    ///

    /// admonition | 📐 **Theorem (Existence of i.i.d. Sequences)**
        attrs: {class: theorem, id: ch5-thm-existence-of-i-i-d-sequences}
    For every probability measure $\mu$ on $(\mathbb R, \mathcal B(\mathbb R))$ there is a probability space carrying an i.i.d. {term}`sequence` $X_1, X_2, \ldots$ of random variables with $X_k \sim \mu$ for every $k$. More generally, for any sequence $\mu_1, \mu_2, \ldots$ of such measures there are independent $X_1, X_2, \ldots$ with $X_k \sim \mu_k$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Not given here. The probability space is an infinite product of copies of $(\mathbb R, \mathcal B(\mathbb R), \mu)$, whose existence is the Kolmogorov extension theorem ([Wikipedia: Kolmogorov extension theorem](https://en.wikipedia.org/wiki/Kolmogorov_extension_theorem), [Wikipedia: Product measure](https://en.wikipedia.org/wiki/Product_measure)).
    ///

    A seeded random-number generator, such as `np.random.default_rng(1)` in this book's simulations, produces a deterministic sequence of numbers designed to look like one realization of such an i.i.d. sequence.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch5-sec-sums-of-independent-random-variables -->
    ## Sums of Independent Random Variables

    Averaging measurements means adding them, so we need the distribution of a sum. For discrete random variables it follows directly from countable additivity.

    /// admonition | 📐 **Theorem (Discrete Convolution)**
        attrs: {class: theorem, id: ch5-thm-discrete-convolution}
    Let $X$ and $Y$ be independent and discrete, with $\mathbb P(X \in C) = \mathbb P(Y \in D) = 1$ for countable sets $C, D$. Then $X + Y$ is discrete and
    $$p_{X+Y}(s) = \sum_{x \in C} p_X(x)\, p_Y(s - x) \quad \text{for every } s \in \mathbb R.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    $X + Y$ is a random variable. Outside the event $\{X \in C, Y \in D\}$, whose complement has probability $0$ by the union bound, $X + Y$ takes values in $\{c + d : c \in C, d \in D\}$, the image of the countable set $C \times D$ under addition, which is countable. So $X + Y$ is discrete. Fix $s$. The event $\{X + Y = s\} \cap \{X \in C\}$ is the disjoint union over $x \in C$ of $\{X = x, Y = s - x\}$, and the rest of $\{X + Y = s\}$ lies in $\{X \notin C\}$, which has probability $0$. Countable additivity and independence give $p_{X+Y}(s) = \sum_{x \in C} \mathbb P(X = x)\,\mathbb P(Y = s - x)$. $\blacksquare$
    ///

    For example, the total of two independent fair dice has $p(s) = \sum_{x=1}^{6} \tfrac16 \cdot \tfrac16\,\mathbf 1[1 \le s - x \le 6] = \frac{6 - |s - 7|}{36}$ for $s = 2, \ldots, 12$: a triangle peaked at $7$, even though each die is flat. Adding independent quantities piles probability toward the middle; this is the seed of the averaging effect of Chapter 6.

    For densities, the sum is replaced by an integral. The *convolution* of two functions $f, g : \mathbb R \to [0, \infty)$ is $(f * g)(s) := \int_{-\infty}^\infty f(x)\,g(s - x)\,dx$.

    /// admonition | 📐 **Theorem (Continuous Convolution)**
        attrs: {class: theorem, id: ch5-thm-continuous-convolution}
    If $X$ and $Y$ are independent with densities $f_X$ and $f_Y$, then $X + Y$ is continuous with density $f_X * f_Y$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Not given here. The proof integrates the joint density $f_X(x) f_Y(y)$ over the half-plane $\{(x, y) : x + y \le s\}$, which is not a box, so it needs the Lebesgue integral ([Wikipedia: Convolution of probability distributions](https://en.wikipedia.org/wiki/Convolution_of_probability_distributions)). The formula is the discrete one with the sum replaced by an integral.
    ///

    For example, if $X, Y \sim \mathcal U(0, 1)$ are independent, then $(f_X * f_Y)(s) = \int_0^1 \mathbf 1[0 \le s - x \le 1]\,dx$ is the length of $[0, 1] \cap [s - 1, s]$, which is $s$ for $0 \le s \le 1$, $2 - s$ for $1 \le s \le 2$, and $0$ otherwise: again a triangle. For normal random variables the convolution can be computed exactly, and the result is the most useful fact of this section.

    /// admonition | 📐 **Theorem (Sums of Independent Normals)**
        attrs: {class: theorem, id: ch5-thm-sums-of-independent-normals}
    If $X \sim \mathcal N(\mu_1, \sigma_1^2)$ and $Y \sim \mathcal N(\mu_2, \sigma_2^2)$ are independent, then $X + Y \sim \mathcal N(\mu_1 + \mu_2,\ \sigma_1^2 + \sigma_2^2)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    First let $\mu_1 = \mu_2 = 0$, and write $a := \sigma_1$, $b := \sigma_2$, $c := \sqrt{a^2 + b^2}$. By the convolution theorem, $X + Y$ has density
    $$h(s) = \int_{-\infty}^{\infty} \frac{1}{2\pi a b} \exp\!\Big(-\frac{x^2}{2a^2} - \frac{(s - x)^2}{2b^2}\Big)\,dx.$$
    Complete the square in $x$. Over the common denominator $2a^2b^2$, the numerator of the exponent's negative is
    $$b^2x^2 + a^2(s - x)^2 = c^2x^2 - 2a^2 s x + a^2 s^2 = c^2\Big(x - \frac{a^2 s}{c^2}\Big)^2 + \frac{a^2 b^2 s^2}{c^2},$$
    where the last step uses $a^2 s^2 - \frac{a^4 s^2}{c^2} = \frac{a^2 s^2 (c^2 - a^2)}{c^2} = \frac{a^2b^2s^2}{c^2}$. Hence, with $m := a^2 s / c^2$ and $\tau := ab/c$,
    $$h(s) = \frac{1}{2\pi ab}\, e^{-s^2/(2c^2)} \int_{-\infty}^{\infty} \exp\!\Big(-\frac{(x - m)^2}{2\tau^2}\Big)\,dx = \frac{1}{2\pi ab}\, e^{-s^2/(2c^2)}\, \tau\sqrt{2\pi} = \frac{1}{c\sqrt{2\pi}}\, e^{-s^2/(2c^2)},$$
    because $\varphi_{m, \tau}$ integrates to $1$. So $X + Y \sim \mathcal N(0, c^2)$.

    In general, $X - \mu_1 \sim \mathcal N(0, \sigma_1^2)$ and $Y - \mu_2 \sim \mathcal N(0, \sigma_2^2)$ by the affine corollary, and they are independent by the theorem on functions of independent random variables. By the first case their sum is $\mathcal N(0, \sigma_1^2 + \sigma_2^2)$, and adding the constant $\mu_1 + \mu_2$ gives the claim by the affine corollary again. $\blacksquare$
    ///

    /// admonition | 📐 **Corollary (Linear Combinations of Independent Normals)**
        attrs: {class: corollary, id: ch5-cor-linear-combinations-of-independent-normals}
    If $X_1, \ldots, X_n$ are independent with $X_i \sim \mathcal N(\mu_i, \sigma_i^2)$, and $a_1, \ldots, a_n, b \in \mathbb R$ with not all $a_i = 0$, then
    $$\sum_{i=1}^n a_i X_i + b \sim \mathcal N\Big(\sum_{i=1}^n a_i\mu_i + b,\ \sum_{i=1}^n a_i^2\sigma_i^2\Big).$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Terms with $a_i = 0$ contribute nothing, so drop them; by the theorem on functions of independent random variables, the remaining $a_i X_i$ are independent, and $a_i X_i \sim \mathcal N(a_i\mu_i, a_i^2\sigma_i^2)$ by the affine corollary. Induct on the number of terms: by the grouping theorem, the sum of the first $m - 1$ terms is independent of the $m$-th, so the theorem applies to them. Finally add $b$ using the affine corollary. $\blacksquare$
    ///

    For example, if $V_1, \ldots, V_k$ are i.i.d. $\mathcal N(0, \sigma^2)$, then their average $\frac1k\sum_{i=1}^k V_i$ (take $a_i = \frac1k$) is $\mathcal N(0, \sigma^2/k)$: the width parameter of the average is $\sqrt k$ times smaller than that of a single noise value. Chapter 6 proves that this $\sigma^2/k$ law holds for *any* noise distribution with a variance, normal or not.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch5-sec-stochastic-processes -->
    ## Stochastic Processes

    A filter does not see one random variable but a stream of them, one per time step. The Introduction defined a {term}`signal` as a function whose domain is a set of times and whose values are the quantity being represented. The random version of a signal is a stochastic process.

    /// note | 📖 **Definition**
    <u>**Stochastic process**</u>

    A stochastic process is an {term}`indexed family` $(X_t)_{t \in T}$ of {term}`random variables <random variable>` on a common probability space, where the index set $T$ is interpreted as a set of times (or positions). It is a *discrete-time* process if $T \subseteq \mathbb Z$; in this book usually $T = \mathbb N^+ = \{1, 2, \ldots\}$ and the index is written $k$.
    ///

    A stochastic process is really a function of two arguments, $(t, \omega) \mapsto X_t(\omega)$. Fixing the time $t$ gives a random variable $X_t$. Fixing the outcome $\omega$ gives the function $t \mapsto X_t(\omega)$ on $T$, called the *sample path* (or *realization*) at $\omega$, and a sample path is a signal. So:

    /// attention | 🗝️ **Key Idea**
    A random signal is a stochastic process. The signal we actually record is one of its sample paths, chosen by the outcome $\omega$ that occurred.
    ///

    The scale readings form the process $(Z_k)_{k = 1}^{30}$, one random variable per sample at 10 samples/s. The figure shows five of its sample paths. The highlighted one is the Introduction's data; the others are what the scale might equally well have shown. A filter must work well for *all* of them, which is why we analyze filters through the distributions of the random variables $Z_k$, not through one recorded signal.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch5_sample_paths.svg" class="graphic" alt="Five sample paths of 30 simulated scale readings around a true weight of 155 lb. One path, the Introduction's data, is highlighted; the other four wander differently around the same black line at 155 lb." />
    """)
    return


@app.cell
def _(IMAGES_DIR, np, plt, std_normal_draws):
    # jb: include=false
    _t = 0.1 * np.arange(1, 31)
    _fig, _ax = plt.subplots(figsize=(8, 4))
    _ax.axhline(155, color="black", linewidth=1.2, label="true weight $x_k = 155$ lb")
    for _seed in (11, 12, 13, 14):
        _path = 155 + np.random.default_rng(_seed).standard_normal(30)
        _ax.plot(_t, _path, "-", color="0.65", linewidth=0.8, marker=".", markersize=4)
    _ax.plot([], [], "-", color="0.65", marker=".", label="other sample paths")
    _ax.plot(_t, 155 + std_normal_draws[:30], "-", color="C0", linewidth=1.6, marker="o",
             markersize=4, label="the Introduction's sample path (seed 1)")
    _ax.set_xlabel("time (s)")
    _ax.set_ylabel("reading $Z_k(\\omega)$ (lb)")
    _ax.set_ylim(151.5, 158.5)
    _ax.set_title("Five sample paths of the scale-reading process", style="italic")
    _ax.legend(loc="upper right", fontsize=8)
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch5_sample_paths.svg")
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch5-sec-the-measurement-noise-model -->
    ## The Measurement-Noise Model

    We can now make the Introduction's informal {term}`noise` precise.

    /// note | 📖 **Definition**
    <u>**Measurement noise**</u>

    Let $Z_k$ be the {term}`random variable` giving the measurement at step $k$ of a quantity whose true value is the real number $x_k$. The measurement noise at step $k$ is the random variable $V_k := Z_k - x_k$.
    ///

    By definition $Z_k = x_k + V_k$, so this equation is not an assumption. The assumptions are about the distribution of the noise process $(V_k)$. The model used throughout Parts I and II of this book is:

    > **Standard measurement-noise model.** For $k = 1, 2, \ldots$, $\ Z_k = x_k + V_k$, where $x_1, x_2, \ldots$ are fixed real numbers (unknown to the filter) and $V_1, V_2, \ldots$ are i.i.d. $\mathcal N(0, \sigma^2)$ for some $\sigma > 0$.

    Each part of the model is a separate claim about the sensor:

    - *Additive:* the noise does not depend on the true value (a 200 lb person sees the same scatter as a 100 lb person).
    - *Centered at zero* ($\mu = 0$): the scale is not systematically high or low. Chapter 6 calls this "zero mean."
    - *Identically distributed:* the sensor does not change over time.
    - *Independent:* the noise has no memory; one reading's error says nothing about the next.
    - *Normal:* the shape of the scatter is the bell curve.

    Under the model, $Z_k \sim \mathcal N(x_k, \sigma^2)$ by the affine corollary, and $Z_1, Z_2, \ldots$ are independent by the theorem on functions of independent random variables. For the scale, $x_k = 155$ lb and $\sigma = 1$ lb, and a seeded generator (seed 1) produced the Introduction's readings. A model is *chosen*, not proved, so the right question is how well it matches reality. The widget below simulates readings $155 + V$ with $V \sim \mathcal N(\mu, \sigma^2)$ and compares their histogram, scaled so its total area is $1$, with the density $\varphi_{155 + \mu,\, \sigma}$. With $n = 30$, $\mu = 0$, and $\sigma = 1$, the readings are the Introduction's 30 samples (before it rounds them to 0.01 lb).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    noise_mu_slider = mo.ui.slider(-2.0, 2.0, 0.1, value=0.0, label=r"noise center $\mu$ (lb)", show_value=True)
    noise_sigma_slider = mo.ui.slider(0.2, 3.0, 0.1, value=1.0, label=r"noise width $\sigma$ (lb)", show_value=True)
    noise_n_slider = mo.ui.slider(
        steps=[30, 100, 300, 1000, 3000, 10000, 20000], value=30,
        label=r"number of readings $n$", show_value=True,
    )
    return noise_mu_slider, noise_n_slider, noise_sigma_slider


@app.cell(hide_code=True)
def _(
    graphic,
    math,
    mo,
    noise_mu_slider,
    noise_n_slider,
    noise_sigma_slider,
    np,
    plt,
    std_normal_draws,
):
    _mu = noise_mu_slider.value
    _sigma = noise_sigma_slider.value
    _n = noise_n_slider.value
    _readings = 155 + _mu + _sigma * std_normal_draws[:_n]

    _fig, _ax = plt.subplots(figsize=(8, 4))
    _ax.hist(_readings, bins=155 + _mu + _sigma * np.linspace(-4, 4, 25), density=True, color="C0",
             alpha=0.6, label=f"histogram of {_n:,} simulated readings")
    _xs = np.linspace(143, 167, 800)
    _ax.plot(_xs, np.exp(-(_xs - 155 - _mu) ** 2 / (2 * _sigma**2)) / (_sigma * math.sqrt(2 * math.pi)),
             color="black", linewidth=1.5, label=r"density $\varphi_{155+\mu,\,\sigma}$")
    _ax.axvline(155, color="black", linestyle=":", linewidth=1, label="true weight 155 lb")
    _ax.set_xlim(143, 167)
    _ax.set_xlabel("reading (lb)")
    _ax.set_ylabel("density (1/lb)")
    _ax.set_title("Simulated scale readings versus the normal density", style="italic")
    _ax.legend(loc="upper right", fontsize=8)
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _fig.tight_layout()
    _plot = graphic(_fig)
    plt.close(_fig)

    _dev = np.abs(_readings - 155 - _mu)
    _f1 = np.mean(_dev <= _sigma)
    _f2 = np.mean(_dev <= 2 * _sigma)
    mo.vstack([
        noise_mu_slider,
        noise_sigma_slider,
        noise_n_slider,
        _plot,
        mo.md(
            f"Fraction of readings within $\\sigma$ of $155 + \\mu$: **{_f1:.3f}** (model: 0.683). "
            f"Within $2\\sigma$: **{_f2:.3f}** (model: 0.954)."
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Three things to notice:

    - Moving $\mu$ shifts the whole histogram and changing $\sigma$ stretches it, without changing its shape. That is the affine corollary at work: every reading is $155 + \mu + \sigma Z$ for the same standard normal samples $Z$ (and the bins, $\sigma/3$ wide, stretch with them), so the fractions within $\sigma$ and $2\sigma$ do not move.
    - With $n = 30$ the histogram is a ragged approximation of the bell; with $n = 20{,}000$ it is nearly indistinguishable from it. The fraction of readings in a bin is an average of indicator random variables, and Chapter 6 proves that such averages converge to the bin's probability.
    - A nonzero $\mu$ moves every reading the same way. No amount of averaging can detect or remove it from readings alone: the data would look exactly like an honest scale weighing a different person.

    /// caution | ⚠️ **Assumptions and Failure Modes**
    The standard model can fail in each of its parts. The most common failures for a scale, and where this book deals with them:

    - **Quantization.** Readings are discrete multiples of a resolution $\Delta$. The error is close to $\mathcal U(-\tfrac\Delta2, \tfrac\Delta2)$ only when $\sigma \gg \Delta$; when $\sigma \lesssim \Delta$ it is a nearly deterministic offset that averaging cannot remove (the quantization theorem above; Chapter 9).
    - **Outliers.** The normal model says a $5\sigma$ error happens about once in two million readings. Real sensors produce gross errors far more often: someone leans on the counter, a pet steps on the scale, a cable glitches. Normal noise has *light tails*; real noise often has *heavy tails*. A single outlier can drag an average far off. Chapter 8 shows how the best estimator changes for non-normal noise, and Chapter 14 rejects outliers by gating.
    - **Drift.** The zero point of a load cell creeps with temperature, so the noise is no longer centered at zero and no longer identically distributed. This is a slowly varying offset, a {term}`sensor bias`, which Chapter 11 estimates.
    - **Correlated noise.** A person sways at about once per second, so consecutive readings at 10 samples/s err in the same direction. The noise values are then *dependent*, and averaging helps much less than the $\sigma^2/k$ law suggests (Chapter 6 quantifies this with covariances; Chapter 10 tests for it).
    - **A moving truth.** The model allows the true values $x_k$ to change, but averaging is designed for a constant value. When the truth moves, the error of an estimate includes a lag as well as noise (Chapter 6 for the EMA; Chapter 9 models the motion as {term}`process noise`).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch5-sec-summary -->
    ## Summary

    - A {term}`random variable` is a function $X : \Omega \to \mathbb R$ whose preimages of Borel sets are events; it suffices to check the rays $\{X \le b\}$. Sums, products, affine maps, and continuous functions of random variables are random variables.
    - The {term}`distribution` $\mathbb P_X(B) = \mathbb P(X \in B)$ is a probability measure on $\mathbb R$. It is determined by the {term}`CDF <cumulative distribution function>` $F_X$, and a function is a CDF exactly when it is nondecreasing, right-continuous, and goes from $0$ to $1$.
    - {term}`Discrete random variables <discrete random variable>` are described by a {term}`PMF <probability mass function>`, {term}`continuous random variables <continuous random variable>` by a {term}`density <probability density function>`, whose integrals over intervals are probabilities.
    - The {term}`uniform <uniform distribution>` and {term}`normal <normal distribution>` distributions; $aX + b$ has density $\frac{1}{|a|}f_X\big(\frac{y-b}{a}\big)$, so affine maps of normal random variables are normal. Quantization error is nearly uniform when the noise is much wider than the resolution, and a deterministic offset when it is not.
    - Several random variables have a {term}`joint distribution`, possibly a {term}`joint density`, whose integral over the other variables is the {term}`marginal density`. They are {term}`independent <independent random variables>` when the joint CDF, PMF, or density factors.
    - Sums of independent random variables have convolved distributions; sums of independent normals are normal, with the $\sigma^2$ parameters adding.
    - A {term}`stochastic process` is a time-indexed family of random variables, and each of its sample paths is a signal.
    - The standard model of {term}`measurement noise` is $Z_k = x_k + V_k$ with $V_k$ {term}`i.i.d. <independent and identically distributed>` $\mathcal N(0, \sigma^2)$. It is an assumption, and it fails under quantization, outliers, drift, correlated noise, and a moving truth.

    <!-- label: ch5-sec-whats-next -->
    ## What's Next

    We can now describe the scale's noise completely, but we cannot yet say how *large* it is in a single number, or prove that averaging shrinks it. [Chapter 6](#ch6) defines the expected value and the variance of a random variable, proves that the average of $k$ readings has variance $\sigma^2/k$, and computes exactly how much noise and how much lag the Introduction's EMA lets through.
    """)
    return


if __name__ == "__main__":
    app.run()
