---
title: 'Appendix C: Calculus'
# marimo-version: 0.25.1
# css_file: notebook-styles.css
subtitle: "Limits, Derivatives, and Integrals"
abbreviations:
  iff: if and only if
  diff: null
  EMA: exponential moving average
numbering:
  equations: false
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
from math import factorial
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

Calculus is built on a single idea: the **limit**, which makes "gets as close as we like" precise. Infinite sums, instantaneous rates of change, areas, and exponential decay are all limits, and a filter designer meets every one of them:

- **Probability** ([Chapter 4](ch4_probability_spaces_v2.md)) adds up infinitely many probabilities. Such a sum is a *series*, and the continuity of probability is a statement about limits of sequences.
- **Densities and expectations** ([Chapter 5](ch5_random_variables_v2.md) and [Chapter 6](ch6_expectation_and_variance_v2.md)) are *integrals*. The normal density only makes sense once we know that $\int_{-\infty}^{\infty} e^{-x^2/2}\,dx = \sqrt{2\pi}$.
- **Continuous-time models** ([Chapter 10](ch10_process_models_v2.md)) are *differential equations*. Turning them into the recursions that a filter runs requires solving them.
- **The extended Kalman filter** ([Chapter 15](ch15_extended_kalman_filter_v2.md)) replaces nonlinear functions by first-order *Taylor approximations*, which are built from *Jacobians*.

This appendix builds all of these from the axioms of the real numbers in [Chapter 3](ch3_sets_for_probability_v2.md). Every result is either proven or stated precisely with a link to a proof. (The italicized words above are used informally here; each is defined precisely below.)

:::{attention icon=false} 🗝️ **Key Idea**
A limit is the exact value that a family of approximations approaches: every tolerance, however small, is eventually met. Every concept in this appendix (the sum of a series, the derivative, the integral, the exponential function) is a limit.
:::
  
:::{seealso icon=false} 🔗 **Prerequisites**
- [Chapter 2](ch2_axioms_of_set_theory_v2.md): functions, the natural numbers $\mathbb N = \{0, 1, 2, \ldots\}$, induction, and the Recursion Theorem.
- [Chapter 3](ch3_sets_for_probability_v2.md): sequences, finite sums $\sum$, countable sets, $\mathbb R$ as a complete ordered field (every nonempty subset of $\mathbb R$ that is bounded above has a supremum), the Archimedean property and the density of $\mathbb Q$, absolute value and the triangle inequality, intervals, and the extended real numbers $[0, \infty]$.
:::

### How to Read This Appendix

You don't need to read this appendix in one sitting. Each main-path chapter's Prerequisites box names the sections it uses:

| Before reading | Read these sections |
|---|---|
| Chapter 4 | Sequences and Limits; Series |
| Chapters 5 and 6 | Limits of Functions and Continuity through Improper Integrals; Multiple Integrals |
| Chapters 7 and 13 | Derivatives; The Mean Value Theorem and Extrema |
| Chapter 10 | Taylor's Theorem; Exponential and Logarithm; Linear Differential Equations |
| Chapters 11, 15, and 16 | Taylor's Theorem; Functions of Several Variables |
| Chapters 12 and 14 | The Fundamental Theorem of Calculus; Multiple Integrals |

Throughout, $\mathbb N^+ := \mathbb N \setminus \{0\}$, and "for every $\varepsilon > 0$" means "for every real number $\varepsilon > 0$". We use two facts about absolute values from Chapter 3 constantly: the triangle inequality $|x + y| \le |x| + |y|$, and its consequence $\big||x| - |y|\big| \le |x - y|$ (the *reverse triangle inequality*).
  
## Sequences and Limits

Recall the {term}`exponential moving average` from the [Introduction](introduction_v2.md): starting from an initial value $\hat x_0$, it computes $\hat x_k = \hat x_{k-1} + \alpha(z_k - \hat x_{k-1})$ with a smoothing factor $0 < \alpha < 1$. Suppose there is no noise at all, so every measurement equals the true weight, $z_k = x$, but the initial value $\hat x_0$ is wrong. Subtracting $x$ from both sides of the update shows that the error $e_k := \hat x_k - x$ satisfies

$$e_k = (\hat x_{k-1} - x) + \alpha(x - \hat x_{k-1}) = (1 - \alpha)\,e_{k-1}, \qquad\text{so}\qquad e_k = (1-\alpha)^k e_0$$

by induction on $k$. With $\alpha = 0.2$, each step removes 20% of the remaining error. The error is never exactly zero (unless $e_0 = 0$), yet it becomes as small as we like: for any tolerance, say $0.1$ lb, there is a step after which the error stays below that tolerance forever. "Eventually within any tolerance" is exactly what a limit is.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Limit of a sequence
: A real number $L$ is a limit of a {term}`sequence` $(a_n)_{n \in \mathbb N}$ of real numbers if and only if for every $\varepsilon > 0$ there exists $N \in \mathbb N$ such that $|a_n - L| < \varepsilon$ for every $n \ge N$:
  $$\forall \varepsilon > 0\ \exists N \in \mathbb N\ \forall n \ge N:\ |a_n - L| < \varepsilon.$$
  Sequences indexed by $n \ge m$ for some other starting index $m$ are handled the same way.
:::
::::

Read the definition as a game. A skeptic names a tolerance $\varepsilon$; we must answer with an index $N$ after which every term stays within $\varepsilon$ of $L$. A smaller $\varepsilon$ may require a larger $N$, but we must be able to answer every $\varepsilon$. The order of the quantifiers matters ([Chapter 1](ch1_language_of_logic_v2.md)): $N$ may depend on $\varepsilon$, but not the other way around.

:::{important icon=false} 📐 **Lemma (Uniqueness of Limits)**
A sequence has at most one limit.
:::

:::{admonition icon=false} ✍️ **Proof**
Suppose $L \ne L'$ are both limits of $(a_n)$, and let $\varepsilon := |L - L'|/2 > 0$. There are $N$ and $N'$ with $|a_n - L| < \varepsilon$ for $n \ge N$ and $|a_n - L'| < \varepsilon$ for $n \ge N'$. For $n = \max(N, N')$ the triangle inequality gives $|L - L'| \le |L - a_n| + |a_n - L'| < 2\varepsilon = |L - L'|$, a contradiction. $\blacksquare$
:::

So we may speak of *the* limit and write $\lim_{n\to\infty} a_n = L$ or $a_n \to L$.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Convergent
: A sequence of real numbers is convergent if and only if it has a {term}`limit <limit of a sequence>` that is a real number. A sequence that is not convergent is called *divergent*.
:::
::::

A sequence $(a_n)$ **diverges to $\infty$**, written $a_n \to \infty$, if for every $M \in \mathbb R$ there is $N$ with $a_n > M$ for all $n \ge N$; divergence to $-\infty$ is defined symmetrically. Such a sequence is divergent, because $\infty$ is not a real number. The notation $\lim a_n = \infty$ is still useful, and it matches the extended real numbers of Chapter 3.
  
:::{important icon=false} 📐 **Lemma (Three Basic Sequences)**
1. $\lim_{n\to\infty} 1/n = 0$ (for $n \ge 1$).
2. If $|q| < 1$, then $\lim_{n\to\infty} q^n = 0$.
3. The sequence $\big((-1)^n\big)_{n\in\mathbb N}$ is divergent.
:::

:::{admonition icon=false} ✍️ **Proof**
1. Let $\varepsilon > 0$. By the Archimedean property there is $N \in \mathbb N^+$ with $N > 1/\varepsilon$. For $n \ge N$, $|1/n - 0| = 1/n \le 1/N < \varepsilon$.
2. If $q = 0$ there is nothing to prove. Otherwise $1/|q| > 1$, so $1/|q| = 1 + h$ with $h > 0$. *Bernoulli's inequality* $(1 + h)^n \ge 1 + nh$ holds for every $n \in \mathbb N$ by induction: it is an equality for $n = 0$, and $(1+h)^{n+1} \ge (1 + nh)(1 + h) = 1 + (n+1)h + nh^2 \ge 1 + (n+1)h$. Hence for $n \ge 1$,
$$|q^n - 0| = \frac{1}{(1+h)^n} \le \frac{1}{1 + nh} < \frac{1}{nh}.$$
Given $\varepsilon > 0$, choose $N \in \mathbb N^+$ with $N > 1/(h\varepsilon)$. For $n \ge N$, $|q^n| < 1/(nh) \le 1/(Nh) < \varepsilon$.
3. Suppose $(-1)^n \to L$. With $\varepsilon = 1$ there is $N$ with $|(-1)^n - L| < 1$ for all $n \ge N$. Then $2 = |(-1)^N - (-1)^{N+1}| \le |(-1)^N - L| + |L - (-1)^{N+1}| < 2$, a contradiction. $\blacksquare$
:::

For the EMA, $|e_k - 0| = |e_0|\,|1 - \alpha|^k$. Given $\varepsilon > 0$ (and $e_0 \ne 0$), part 2 with $q = |1-\alpha|$ and tolerance $\varepsilon/|e_0|$ gives an $N$ with $|e_k| < \varepsilon$ for all $k \ge N$. So $e_k \to 0$ for every $0 < \alpha < 1$: without noise, the EMA forgets any initial error. (The same holds for $1 \le \alpha < 2$, since part 2 only needs $|1 - \alpha| < 1$.)

The interactive figure below plays the $\varepsilon$–$N$ game. Pick a sequence and a tolerance; the shaded band is $(L - \varepsilon, L + \varepsilon)$, and the dotted line marks the smallest $N$ that wins. The first sequence is the EMA's remaining error fraction $(1-\alpha)^n$ with $\alpha = 0.2$, and the second is the gain $1/n$ of the cumulative average.

```{marimo} python
:hide-code: true

eps_seq = mo.ui.dropdown(
    options={
        "EMA error fraction 0.8ⁿ": "ema",
        "cumulative-average gain 1/n": "inv",
        "alternating (−1)ⁿ/n": "alt",
        "divergent (−1)ⁿ": "div",
    },
    value="EMA error fraction 0.8ⁿ",
    label="sequence",
)
eps_slider = mo.ui.slider(
    start=0.02, stop=0.5, step=0.01, value=0.1, label=r"tolerance $\varepsilon$"
)
```

```{marimo} python
:hide-code: true

_eps = eps_slider.value
_kind = eps_seq.value
_seqs = {
    "ema": (lambda n: 0.8**n, r"$a_n = 0.8^n$"),
    "inv": (lambda n: 1.0 / n, r"$a_n = 1/n$"),
    "alt": (lambda n: (-1.0) ** n / n, r"$a_n = (-1)^n/n$"),
    "div": (lambda n: (-1.0) ** n, r"$a_n = (-1)^n$"),
}
_f, _name = _seqs[_kind]
_L = 0.0
_n = np.arange(1, 61)
_a = _f(_n)
if _kind == "div":
    _N = None
else:
    # |a_n - L| decreases in n for these sequences, so the first index inside the band wins.
    _big = np.arange(1, 200_001)
    _N = int(_big[np.argmax(np.abs(_f(_big) - _L) < _eps)])

_inside = np.abs(_a - _L) < _eps
_fig, _ax = plt.subplots(figsize=(7, 3.6))
_ax.axhspan(_L - _eps, _L + _eps, color="C1", alpha=0.2, label=r"$(L-\varepsilon,\ L+\varepsilon)$")
_ax.axhline(_L, color="black", linewidth=1, label=r"$L = 0$")
_ax.plot(_n[_inside], _a[_inside], "o", color="C0", markersize=4, label="inside the band")
_ax.plot(_n[~_inside], _a[~_inside], "o", mfc="none", mec="black", markersize=5, label="outside the band")
if _N is not None and _N <= _n[-1]:
    _ax.axvline(_N, color="red", linestyle=":", label=f"$N = {_N}$")
_ax.set_xlabel("index $n$")
_ax.set_ylabel("$a_n$")
_ax.set_ylim(-1.15, 1.15)
_ax.grid(visible=True, alpha=0.9, linewidth=0.4)
_ax.legend(loc="lower right", fontsize=8)
_ax.set_title(f"First 60 terms of {_name} with $\\varepsilon = {_eps:.2f}$", style="italic")
_fig.tight_layout()

if _N is None:
    _text = (
        f"No $N$ exists for $\\varepsilon = {_eps:.2f}$: consecutive terms differ by $2$, so they "
        "cannot both lie within $\\varepsilon \\le 1$ of any $L$. The band shown is for the candidate $L = 0$."
    )
else:
    _text = (
        f"With $\\varepsilon = {_eps:.2f}$, the smallest winning index is $N = {_N}$: "
        f"$|a_n - 0| < {_eps:.2f}$ for every $n \\ge {_N}$."
    )
mo.vstack([mo.hstack([eps_seq, eps_slider], justify="start"), graphic(_fig), mo.md(_text)])
```

### Limit Laws

Limits would be of little use if each one had to be computed from the definition. The limit laws let us combine known limits.

:::{important icon=false} 📐 **Lemma (Convergent Sequences Are Bounded)**
If $(a_n)$ converges, there is $M \in \mathbb R$ with $|a_n| \le M$ for every $n$.
:::

:::{admonition icon=false} ✍️ **Proof**
Let $a_n \to L$. With $\varepsilon = 1$ there is $N$ with $|a_n - L| < 1$, hence $|a_n| < |L| + 1$, for $n \ge N$. Take $M := \max(|a_0|, \ldots, |a_{N-1}|, |L| + 1)$. $\blacksquare$
:::

:::{important icon=false} 📐 **Theorem (Limit Laws for Sequences)**
Let $a_n \to a$ and $b_n \to b$, and let $c \in \mathbb R$. Then:
1. $a_n + b_n \to a + b$ and $c\,a_n \to c\,a$.
2. $a_n b_n \to ab$.
3. If $b \ne 0$ and $b_n \ne 0$ for every $n$, then $a_n / b_n \to a/b$.
4. *(Order)* If $a_n \le b_n$ for every $n \ge N_0$, then $a \le b$.
5. *(Squeeze)* If $a = b$ and $a_n \le c_n \le b_n$ for every $n$, then $c_n \to a$.
:::

:::{admonition icon=false} ✍️ **Proof**
Let $\varepsilon > 0$. In each part, "for large $n$" means "for all $n$ beyond some index", and finitely many such conditions can be met at once by taking the largest of the indices.
1. For large $n$, $|a_n - a| < \varepsilon/2$ and $|b_n - b| < \varepsilon/2$, so $|(a_n + b_n) - (a + b)| \le |a_n - a| + |b_n - b| < \varepsilon$. If $c = 0$ the second claim is trivial; otherwise for large $n$, $|a_n - a| < \varepsilon/|c|$, so $|c\,a_n - c\,a| < \varepsilon$.
2. Write $a_n b_n - ab = a_n(b_n - b) + b(a_n - a)$. By the lemma, $|a_n| \le M$ for some $M > 0$. For large $n$, $|b_n - b| < \varepsilon/(2M)$ and $|a_n - a| < \varepsilon/(2|b| + 2)$, so $|a_n b_n - ab| < \varepsilon/2 + \varepsilon/2 = \varepsilon$.
3. By part 2 it suffices to show $1/b_n \to 1/b$. For large $n$, $|b_n - b| < |b|/2$, so by the reverse triangle inequality $|b_n| > |b|/2$, and then $\left|\frac{1}{b_n} - \frac{1}{b}\right| = \frac{|b - b_n|}{|b_n||b|} < \frac{2|b_n - b|}{|b|^2}$. For large $n$ this is below $\varepsilon$, because $|b_n - b| < \varepsilon|b|^2/2$ eventually.
4. Suppose $a > b$ and let $\varepsilon := (a - b)/2$. For large $n$ (also $n \ge N_0$), $a_n > a - \varepsilon = b + \varepsilon > b_n$, contradicting $a_n \le b_n$.
5. For large $n$, $a - \varepsilon < a_n \le c_n \le b_n < a + \varepsilon$, so $|c_n - a| < \varepsilon$. $\blacksquare$
:::

Part 4 says that limits preserve non-strict inequalities. In particular, if every $a_n$ lies in a closed interval $[p, q]$, so does the limit. Strict inequalities are *not* preserved: $1/n > 0$ for every $n$, but the limit is $0$.
  
### Monotone Sequences and Completeness

A sequence $(a_n)$ is **increasing** if $a_n \le a_{n+1}$ for every $n$, **decreasing** if $a_n \ge a_{n+1}$ for every $n$, and **monotone** if it is one of the two; with strict inequalities it is *strictly* increasing or decreasing. It is **bounded above** if the set $\{a_n : n \in \mathbb N\}$ has an {term}`upper bound`, and **bounded** if $|a_n| \le M$ for some $M$ and every $n$.

In probability, increasing sequences appear naturally: if $A_1 \subseteq A_2 \subseteq \cdots$ are events, their probabilities increase and never exceed $1$. Do such numbers have to converge? Yes, and this is precisely where the completeness of $\mathbb R$ enters.

:::{important icon=false} 📐 **Theorem (Monotone Convergence)**
1. An increasing sequence that is bounded above converges, and its limit is $\sup\{a_n : n \in \mathbb N\}$.
2. A decreasing sequence that is bounded below converges, and its limit is $\inf\{a_n : n \in \mathbb N\}$.
3. An increasing sequence that is not bounded above diverges to $\infty$.
:::

:::{admonition icon=false} ✍️ **Proof**
1. The set $\{a_n\}$ is nonempty and bounded above, so its {term}`supremum` $S$ exists because $\mathbb R$ is a {term}`complete ordered field`. Let $\varepsilon > 0$. Since $S$ is the *least* upper bound, $S - \varepsilon$ is not an upper bound, so $a_N > S - \varepsilon$ for some $N$. For $n \ge N$, monotonicity gives $S - \varepsilon < a_N \le a_n \le S$, so $|a_n - S| < \varepsilon$.
2. Apply part 1 to the increasing sequence $(-a_n)$, using $\inf A = -\sup(-A)$.
3. Given $M$, some $a_N > M$ because $M$ is not an upper bound, and then $a_n \ge a_N > M$ for every $n \ge N$. $\blacksquare$
:::

The theorem fails in $\mathbb Q$. The decimal truncations $1, 1.4, 1.41, 1.414, \ldots$ of $\sqrt 2$ form an increasing sequence of rationals bounded above by $2$, but no rational number is its limit ([Appendix B: Incompleteness of the Rationals](appendix_b_number_systems_v2.md)). Every theorem below that relies on Monotone Convergence (Bolzano–Weierstrass, the Cauchy criterion, the intermediate and extreme value theorems, and everything built on them) is ultimately a consequence of completeness.

Because an increasing sequence always converges either to a real number or to $\infty$, we can assign it a limit in the extended real numbers in every case: $\lim a_n = \sup\{a_n\} \in (-\infty, \infty]$. The same convention applies to increasing sequences with values in $[0, \infty]$, which may contain the term $\infty$ itself.
  
### Subsequences and Cauchy Sequences

The sequence $(-1)^n$ diverges, but its even-indexed terms $1, 1, 1, \ldots$ converge. Given a sequence $(a_n)$ and a strictly increasing sequence of indices $n_0 < n_1 < n_2 < \cdots$ in $\mathbb N$, the sequence $(a_{n_k})_{k \in \mathbb N}$ is a **subsequence** of $(a_n)$. By induction, $n_k \ge k$ for every $k$.

:::{important icon=false} 📐 **Lemma (Subsequences of Convergent Sequences)**
If $a_n \to L$, then every subsequence $a_{n_k} \to L$.
:::

:::{admonition icon=false} ✍️ **Proof**
Given $\varepsilon > 0$, choose $N$ with $|a_n - L| < \varepsilon$ for $n \ge N$. For $k \ge N$ we have $n_k \ge k \ge N$, so $|a_{n_k} - L| < \varepsilon$. $\blacksquare$
:::

:::{important icon=false} 📐 **Lemma (Monotone Subsequence)**
Every sequence of real numbers has a monotone subsequence.
:::

:::{admonition icon=false} ✍️ **Proof**
Call an index $m$ a *peak* if $a_m \ge a_n$ for every $n > m$.

*Case 1: there are infinitely many peaks.* Let $m_0$ be the least peak and, recursively, $m_{k+1}$ the least peak greater than $m_k$ (the Recursion Theorem of [Chapter 2](ch2_axioms_of_set_theory_v2.md)). Each $m_k$ is a peak and $m_{k+1} > m_k$, so $a_{m_k} \ge a_{m_{k+1}}$: the subsequence is decreasing.

*Case 2: there are finitely many peaks.* Let $n_0$ be larger than every peak. Recursively, since $n_k$ is not a peak, there is an $n > n_k$ with $a_n > a_{n_k}$; let $n_{k+1}$ be the least such $n$. Then $n_{k+1} > n_k$ is again not a peak, and $(a_{n_k})$ is strictly increasing. $\blacksquare$
:::

:::{important icon=false} 📐 **Theorem (Bolzano–Weierstrass)**
Every bounded sequence of real numbers has a convergent subsequence.
:::

:::{admonition icon=false} ✍️ **Proof**
By the previous lemma the sequence has a monotone subsequence, which is bounded because the sequence is. By Monotone Convergence it converges. $\blacksquare$
:::

To prove that a sequence converges using the definition, we must already know the limit. The next definition tests convergence using only the terms themselves.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Cauchy sequence
: A sequence $(a_n)$ of real numbers is a Cauchy sequence if and only if for every $\varepsilon > 0$ there exists $N \in \mathbb N$ such that $|a_m - a_n| < \varepsilon$ for all $m, n \ge N$.
:::
::::

:::{important icon=false} 📐 **Theorem (Cauchy Criterion)**
A sequence of real numbers is {term}`convergent` if and only if it is a {term}`Cauchy sequence`.
:::

:::{admonition icon=false} ✍️ **Proof**
($\Rightarrow$) Let $a_n \to L$ and $\varepsilon > 0$. Choose $N$ with $|a_n - L| < \varepsilon/2$ for $n \ge N$. For $m, n \ge N$, $|a_m - a_n| \le |a_m - L| + |L - a_n| < \varepsilon$.

($\Leftarrow$) Let $(a_n)$ be Cauchy. It is bounded: with $\varepsilon = 1$ there is $N$ with $|a_n| < |a_N| + 1$ for $n \ge N$, and only finitely many terms come before $N$. By Bolzano–Weierstrass, some subsequence $a_{n_k} \to L$. Let $\varepsilon > 0$. Choose $N$ with $|a_m - a_n| < \varepsilon/2$ for $m, n \ge N$, and then $k$ with $k \ge N$ and $|a_{n_k} - L| < \varepsilon/2$. Since $n_k \ge k \ge N$, every $n \ge N$ satisfies $|a_n - L| \le |a_n - a_{n_k}| + |a_{n_k} - L| < \varepsilon$. $\blacksquare$
:::
  
:::{caution icon=false} ⚠️ **Assumptions and Failure Modes**
- **Convergence says nothing about speed.** For the EMA error $(1-\alpha)^k$, the index $N$ needed for a given $\varepsilon$ grows roughly like $1/\alpha$ as $\alpha$ shrinks. A convergent filter can still take an impractically long time to forget a bad initial value.
- **Limits preserve $\le$, not $<$.** A sequence of positive numbers may have limit $0$.
- **Completeness is essential.** In $\mathbb Q$, Monotone Convergence, Bolzano–Weierstrass, and the Cauchy criterion all fail; the decimal truncations of $\sqrt 2$ are a Cauchy sequence of rationals with no rational limit.
- **A convergent subsequence does not make the sequence convergent**, as $(-1)^n$ shows.
:::

:::{attention icon=false} 🗝️ **Key Idea**
$a_n \to L$ means that every tolerance $\varepsilon > 0$ is eventually met forever. The limit laws combine limits; the completeness of $\mathbb R$ guarantees limits for bounded monotone sequences and for Cauchy sequences, even when we cannot name the limit in advance.
:::
  
## Series

The EMA's estimate is a weighted sum of every measurement it has seen. Unrolling the recursion ([Introduction](introduction_v2.md)) gives

$$\hat x_k = \sum_{n=0}^{k-1} \alpha(1-\alpha)^n z_{k-n} + (1-\alpha)^k\,\hat x_0,$$

so the measurement from $n$ steps ago has weight $\alpha(1-\alpha)^n$. As $k$ grows, the list of weights $\alpha,\ \alpha(1-\alpha),\ \alpha(1-\alpha)^2, \ldots$ grows without end. In what sense do infinitely many weights "add up to $1$"? The answer is a limit: their finite sums approach $1$.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Series
: Let $(a_n)_{n\in\mathbb N}$ be a sequence of real numbers. The series $\sum_{n=0}^\infty a_n$ is the sequence $(s_N)_{N\in\mathbb N}$ of its *partial sums* $s_N := \sum_{n=0}^{N} a_n$. The series converges if and only if $(s_N)$ is {term}`convergent`; its limit $S$ is then called the *sum* of the series, and we write $\sum_{n=0}^\infty a_n = S$. Otherwise the series diverges. Series that start at another index are defined in the same way.
:::
::::

The symbol $\sum_{n=0}^\infty a_n$ thus names both the series and, when it exists, its sum. Two consequences of the limit laws are used constantly:

- **Linearity.** If $\sum a_n$ and $\sum b_n$ converge and $c \in \mathbb R$, then $\sum (a_n + b_n) = \sum a_n + \sum b_n$ and $\sum c\,a_n = c\sum a_n$, because partial sums add and scale.
- **Finitely many terms don't matter for convergence.** Changing, adding, or removing finitely many terms changes every partial sum beyond some index by the same constant, so it changes the sum but not whether the series converges.

:::{important icon=false} 📐 **Lemma (Term Test)**
If $\sum a_n$ converges, then $a_n \to 0$.
:::

:::{admonition icon=false} ✍️ **Proof**
Let $s_N \to S$. The shifted sequence $(s_{N-1})_{N \ge 1}$ also converges to $S$, so $a_N = s_N - s_{N-1} \to S - S = 0$ by the limit laws. $\blacksquare$
:::

The term test gives a {term}`necessary condition` for convergence. The harmonic series below shows that it is not a {term}`sufficient condition`.

:::{important icon=false} 📐 **Lemma (Finite Geometric Sum)**
For every real $q \ne 1$ and every $N \in \mathbb N$,
$$\sum_{n=0}^{N} q^n = \frac{1 - q^{N+1}}{1 - q}.$$
:::

:::{admonition icon=false} ✍️ **Proof**
Let $s_N := \sum_{n=0}^{N} q^n$. Then $q\,s_N = \sum_{n=1}^{N+1} q^n$, and every term except $q^0$ and $q^{N+1}$ cancels in the difference: $s_N - q\,s_N = 1 - q^{N+1}$. Divide by $1 - q \ne 0$. $\blacksquare$
:::

:::{important icon=false} 📐 **Theorem (Geometric Series)**
The series $\sum_{n=0}^\infty q^n$ converges if and only if $|q| < 1$, and then
$$\sum_{n=0}^\infty q^n = \frac{1}{1 - q}.$$
:::

:::{admonition icon=false} ✍️ **Proof**
If $|q| < 1$, then $q^{N+1} \to 0$ (Lemma: Three Basic Sequences), so by the limit laws $s_N = (1 - q^{N+1})/(1-q) \to 1/(1-q)$. If $|q| \ge 1$, then $|q^n| \ge 1$ for every $n$, so $q^n \not\to 0$ and the series diverges by the term test. $\blacksquare$
:::

**Back to the EMA.** With $q = 1 - \alpha \in (0, 1)$, the finite geometric sum gives $\sum_{n=0}^{k-1} \alpha(1-\alpha)^n = \alpha\cdot\frac{1 - (1-\alpha)^k}{\alpha} = 1 - (1-\alpha)^k$, and the initial value receives the remaining weight $(1-\alpha)^k$, so the $k + 1$ weights always add up to exactly $1$. The infinite list of measurement weights adds up to $1$ in the sense of the definition: $\sum_{n=0}^\infty \alpha(1-\alpha)^n = \alpha\cdot\frac{1}{1 - (1-\alpha)} = 1$. The weight on the initial value, $(1-\alpha)^k \to 0$, is exactly the forgetting we found in Sequences and Limits.

:::{important icon=false} 📐 **Theorem (Harmonic Series)**
$\sum_{n=1}^\infty \frac1n$ diverges to $\infty$, even though $\frac1n \to 0$.
:::

:::{admonition icon=false} ✍️ **Proof**
For each $j \ge 1$ there are $2^{j-1}$ integers $n$ with $2^{j-1} < n \le 2^j$, and each has $\frac1n \ge \frac{1}{2^j}$, so their terms add up to at least $\frac12$. Hence the partial sum up to $n = 2^m$ is at least $1 + \frac m2$. The partial sums are increasing and unbounded, so they diverge to $\infty$ by Monotone Convergence. $\blacksquare$
:::
  
### Series with Nonnegative Terms

If every $a_n \ge 0$, the partial sums increase. By Monotone Convergence the series converges if and only if its partial sums are bounded, and otherwise it diverges to $\infty$. In both cases we write
$$\sum_{n=0}^\infty a_n = \sup_N s_N \in [0, \infty],$$
a value in the {term}`extended real numbers`. The same definition applies when some terms equal $\infty$, using the convention $x + \infty = \infty$ from Chapter 3.

:::{important icon=false} 📐 **Theorem (Comparison Test)**
If $0 \le a_n \le b_n$ for every $n$, then $\sum a_n \le \sum b_n$ in $[0, \infty]$. In particular, if $\sum b_n$ converges then so does $\sum a_n$, and if $\sum a_n$ diverges then so does $\sum b_n$.
:::

:::{admonition icon=false} ✍️ **Proof**
For every $N$, $\sum_{n=0}^N a_n \le \sum_{n=0}^N b_n \le \sup_M \sum_{n=0}^M b_n = \sum b_n$. Taking the supremum over $N$ gives $\sum a_n \le \sum b_n$. $\blacksquare$
:::

**Example.** $\sum_{n=1}^\infty \frac{1}{n^2}$ converges and is at most $2$. For $n \ge 2$, $\frac{1}{n^2} \le \frac{1}{n(n-1)} = \frac{1}{n-1} - \frac1n$, and the partial sums of the right side *telescope*: $\sum_{n=2}^N \big(\frac{1}{n-1} - \frac1n\big) = 1 - \frac1N \le 1$. By comparison, $\sum_{n=2}^\infty \frac{1}{n^2} \le 1$; adding the term for $n = 1$ gives at most $2$. (The exact value is $\pi^2/6 \approx 1.645$.)

### Absolute Convergence

A series $\sum a_n$ **converges absolutely** if $\sum |a_n|$ converges.

:::{important icon=false} 📐 **Theorem (Absolute Convergence Implies Convergence)**
If $\sum |a_n|$ converges, then $\sum a_n$ converges and $\left|\sum a_n\right| \le \sum |a_n|$.
:::

:::{admonition icon=false} ✍️ **Proof**
Let $s_N$ and $t_N$ be the partial sums of $\sum a_n$ and $\sum |a_n|$. Since $(t_N)$ converges, it is a {term}`Cauchy sequence`. For $M > N$, the triangle inequality (extended to finitely many terms by induction) gives
$$|s_M - s_N| = \Big|\sum_{n=N+1}^M a_n\Big| \le \sum_{n=N+1}^M |a_n| = |t_M - t_N|,$$
so $(s_N)$ is Cauchy as well and converges by the Cauchy Criterion. Finally $|s_N| \le t_N \le \sum|a_n|$ for every $N$, and $|s_N| \to \left|\sum a_n\right|$ by the reverse triangle inequality, so the order law gives the inequality. $\blacksquare$
:::

:::{important icon=false} 📐 **Lemma (Ratio Test)**
If there are $N \in \mathbb N$ and $0 \le q < 1$ such that $|a_{n+1}| \le q\,|a_n|$ for every $n \ge N$, then $\sum a_n$ converges absolutely.
:::

:::{admonition icon=false} ✍️ **Proof**
By induction, $|a_n| \le |a_N|\,q^{n-N}$ for every $n \ge N$. The series $\sum_{n \ge N} |a_N|\,q^{n-N} = |a_N|/(1-q)$ converges (geometric series and linearity), so $\sum_{n \ge N} |a_n|$ converges by comparison. The first $N$ terms don't affect convergence. $\blacksquare$
:::

**Example (the exponential series).** Let $n! := 1 \cdot 2 \cdots n$, defined by the recursion $0! := 1$, $(n+1)! := (n+1)\,n!$. For every real $x$, the series $\sum_{n=0}^\infty \frac{x^n}{n!}$ converges absolutely. This is trivial for $x = 0$; otherwise the ratio of consecutive terms is $\frac{|x|^{n+1}/(n+1)!}{|x|^n/n!} = \frac{|x|}{n+1} \le \frac12$ for every $n \ge 2|x|$, so the ratio test applies with $q = \frac12$. This series will define the exponential function.
  
### Sums in Any Order

A series adds its terms in a specific order: $a_0$ first, then $a_1$, and so on. Probability often needs sums with no natural order, such as the total probability of the outcomes in a countable set, or a sum over all pairs $(m, n) \in \mathbb N \times \mathbb N$. For nonnegative terms the order never matters, and the cleanest way to see this is to define the sum without using any order.

Let $I$ be a {term}`countable` set and let $a: I \to [0, \infty]$, written $i \mapsto a_i$. The **sum** of this family is

$$\sum_{i \in I} a_i := \sup\Big\{\sum_{i \in F} a_i : F \subseteq I \text{ finite}\Big\} \in [0, \infty].$$

For finite $I$, this is the ordinary finite sum, since adding nonnegative terms never decreases a finite sum.

:::{important icon=false} 📐 **Theorem (Nonnegative Sums in Any Order)**
Let $I$ be a countable set and $a: I \to [0, \infty]$.
1. *(Order)* If $I$ is infinite and $\sigma: \mathbb N \to I$ is a {term}`bijection <bijective>`, then $\sum_{n=0}^\infty a_{\sigma(n)} = \sum_{i \in I} a_i$.
2. *(Grouping)* If $J$ is countable and $(I_j)_{j \in J}$ is an {term}`indexed family` of pairwise disjoint sets with $\bigcup_{j \in J} I_j = I$, then
$$\sum_{i \in I} a_i = \sum_{j \in J} \Big(\sum_{i \in I_j} a_i\Big).$$
:::

:::{admonition icon=false} ✍️ **Proof**
1. Let $S := \sum_{i\in I} a_i$ and $s_N := \sum_{n=0}^N a_{\sigma(n)}$. Because $\sigma$ is injective, $s_N$ is the sum over the finite set $F_N := \sigma[\{0, \ldots, N\}]$, so $s_N \le S$, and therefore $\sum_n a_{\sigma(n)} = \sup_N s_N \le S$. Conversely, a finite $F \subseteq I$ is contained in $F_N$ for $N := \max \sigma^{-1}[F]$ (any $N$ if $F = \emptyset$), so $\sum_{i\in F} a_i \le s_N \le \sup_N s_N$. Taking the supremum over $F$ gives $S \le \sup_N s_N$.
2. Let $b_j := \sum_{i\in I_j} a_i$, $S := \sum_{i \in I} a_i$, and $T := \sum_{j \in J} b_j$.
    - $S \le T$: Let $F \subseteq I$ be finite. Each $i \in F$ lies in exactly one $I_j$, so $F$ meets $I_j$ only for $j$ in a finite set $G \subseteq J$. Regrouping the finite sum, $\sum_{i \in F} a_i = \sum_{j \in G} \sum_{i \in F \cap I_j} a_i \le \sum_{j\in G} b_j \le T$.
    - $T \le S$: Let $G \subseteq J$ be finite and, for each $j \in G$, let $F_j \subseteq I_j$ be finite. The $F_j$ are disjoint, so $\sum_{j \in G}\sum_{i \in F_j} a_i = \sum_{i \in \bigcup_j F_j} a_i \le S$. Taking the supremum over each $F_j$ in turn gives $\sum_{j \in G} b_j \le S$, and the supremum over $G$ gives $T \le S$. $\blacksquare$
:::

For real terms of both signs, write $a_i^+ := \max(a_i, 0)$ and $a_i^- := \max(-a_i, 0)$, so that $a_i = a_i^+ - a_i^-$, $|a_i| = a_i^+ + a_i^-$, and $0 \le a_i^\pm \le |a_i|$. A family $a: I \to \mathbb R$ is **absolutely summable** if $\sum_{i \in I} |a_i| < \infty$. Then $\sum_{i\in I} a_i^\pm \le \sum_{i\in I}|a_i| < \infty$, and we define $\sum_{i \in I} a_i := \sum_{i\in I} a_i^+ - \sum_{i\in I} a_i^-$. For an absolutely summable family, writing it as a difference of *any* two summable nonnegative families gives the same sum, by enumerating the index set and using part 1 together with the linearity of series.

:::{important icon=false} 📐 **Corollary (Absolutely Convergent Sums in Any Order)**
Let $a: I \to \mathbb R$ be absolutely summable.
1. For every bijection $\sigma: \mathbb N \to I$, the series $\sum_n a_{\sigma(n)}$ converges absolutely, with sum $\sum_{i\in I} a_i$. In particular, rearranging an absolutely convergent series does not change its sum.
2. Under the hypotheses of part 2 of the theorem, each family $(a_i)_{i \in I_j}$ and the family of inner sums $\big(\sum_{i\in I_j} a_i\big)_{j\in J}$ are absolutely summable, and $\sum_{i\in I} a_i = \sum_{j\in J}\sum_{i\in I_j} a_i$.
:::

:::{admonition icon=false} ✍️ **Proof**
1. By part 1 of the theorem, $\sum_n |a_{\sigma(n)}| = \sum_{i\in I}|a_i| < \infty$ and $\sum_n a^\pm_{\sigma(n)} = \sum_{i\in I} a_i^\pm$. Subtracting these two convergent series gives $\sum_n a_{\sigma(n)} = \sum_{i \in I} a_i$.
2. Each $\sum_{i\in I_j}|a_i| \le \sum_{i\in I}|a_i| < \infty$. The inner sums $b_j := \sum_{i \in I_j} a_i = b_j^+ - b_j^-$, with $b_j^\pm := \sum_{i\in I_j} a_i^\pm$, satisfy $|b_j| \le \sum_{i\in I_j} |a_i|$, so by part 2 of the theorem (applied to $|a|$) $\sum_j |b_j| \le \sum_{i\in I} |a_i| < \infty$. Applying part 2 of the theorem to $a^+$ and to $a^-$ and subtracting, $\sum_{j} b_j = \sum_j b_j^+ - \sum_j b_j^- = \sum_{i\in I} a_i^+ - \sum_{i\in I} a_i^- = \sum_{i\in I} a_i$. $\blacksquare$
:::

:::{important icon=false} 📐 **Corollary (Cauchy Product)**
1. If $a_n, b_n \ge 0$ for every $n$, then $\sum_{(k, m) \in \mathbb N\times\mathbb N} a_k\,b_m = \Big(\sum_{n=0}^\infty a_n\Big)\Big(\sum_{n=0}^\infty b_n\Big)$ in $[0, \infty]$, with Chapter 3's convention $0 \cdot \infty = 0$.
2. If $\sum a_n$ and $\sum b_n$ converge absolutely and $c_n := \sum_{k=0}^n a_k\,b_{n-k}$, then $\sum c_n$ converges absolutely and
$$\sum_{n=0}^\infty c_n = \Big(\sum_{n=0}^\infty a_n\Big)\Big(\sum_{n=0}^\infty b_n\Big).$$
:::

:::{admonition icon=false} ✍️ **Proof**
The index set $\mathbb N \times \mathbb N$ is countable by Chapter 3.
1. Let $B := \sum_m b_m$. Group by rows $\{k\}\times\mathbb N$. Each row sum is $\sum_m a_k b_m = a_k B$: by linearity if $B < \infty$, and because both sides are $0$ (if $a_k = 0$) or $\infty$ (if $a_k > 0$) when $B = \infty$. In the same way, $\sum_k a_k B = \big(\sum_k a_k\big)B$.
2. By part 1 applied to $|a_n|$ and $|b_n|$, the family $(a_k b_m)$ is absolutely summable. By the previous corollary, grouping by rows gives $\sum_{(k,m)} a_k b_m = \sum_k a_k \sum_m b_m$ (using linearity for each row), while grouping by the finite diagonals $\{(k, m) : k + m = n\}$ gives $\sum_n c_n$, which converges absolutely. $\blacksquare$
:::
  
:::{caution icon=false} ⚠️ **Assumptions and Failure Modes**
- **Terms tending to $0$ is not enough.** The harmonic series diverges although $\frac1n \to 0$.
- **The geometric series needs $|q| < 1$.** For an EMA-style recursion $e_k = (1-\alpha)e_{k-1}$ with $\alpha \le 0$ or $\alpha \ge 2$, we have $|1 - \alpha| \ge 1$: the weights never decay, and an initial error is never forgotten.
- **The comparison test needs nonnegative terms.** $-n \le 0$ for every $n$ and $\sum 0$ converges, but $\sum(-n)$ diverges.
- **Without absolute convergence, order matters.** The alternating harmonic series $1 - \frac12 + \frac13 - \cdots$ converges (by the [alternating series test](https://en.wikipedia.org/wiki/Alternating_series_test)) but not absolutely, and [Riemann's rearrangement theorem](https://en.wikipedia.org/wiki/Riemann_series_theorem) shows that its terms can be reordered to sum to any real number at all. This is why [Chapter 6](ch6_expectation_and_variance_v2.md) defines an expected value only when the defining sum converges absolutely.
:::

:::{attention icon=false} 🗝️ **Key Idea**
A series is the sequence of its partial sums, and its sum is their limit. The geometric series $\sum q^n = \frac{1}{1-q}$ for $|q| < 1$ explains why the EMA's weights add up to $1$. Sums of nonnegative terms, and absolutely convergent sums, do not depend on order or grouping, which is exactly what countable additivity in probability needs.
:::
  
## Limits of Functions and Continuity

A scale's display rounds the true weight to a step of $\Delta = 0.1$ lb ([Chapter 4](ch4_probability_spaces_v2.md) starts from this example). The display shows $Q(x) := \Delta\lfloor x/\Delta + \tfrac12\rfloor$, where $\lfloor y\rfloor$ denotes the greatest integer $\le y$ (it exists by the Archimedean property). Near a true weight of $155.02$ lb, small changes in weight don't change the display at all. Near $155.05$ lb, an arbitrarily small increase flips the display from $155.0$ to $155.1$. *Continuity* makes "small changes in the input cause small changes in the output" precise. It is built on the limit of a function.

Limits of functions also let us talk about values a function never takes. The average slope of $x \mapsto x^2$ between $1$ and $1 + h$ is $g(h) := \frac{(1+h)^2 - 1}{h}$ for $h \ne 0$. At $h = 0$ the formula reads $0/0$, which is meaningless, but for $h \ne 0$ we have $g(h) = 2 + h$, which is close to $2$ whenever $h$ is close to $0$.

A point $a \in \mathbb R$ is an **accumulation point** of a set $D \subseteq \mathbb R$ if for every $\delta > 0$ there is an $x \in D$ with $0 < |x - a| < \delta$. For example, $0$ is an accumulation point of $\mathbb R \setminus \{0\}$, and every point of an {term}`interval` with more than one point, including its endpoints, is an accumulation point of the interval.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Limit of a function
: Let $D \subseteq \mathbb R$ and $f: D \to \mathbb R$.

  - *At a point:* if $a \in \mathbb R$ is an accumulation point of $D$, a real number $L$ is a limit of $f$ at $a$, written $\lim_{x \to a} f(x) = L$, if and only if for every $\varepsilon > 0$ there exists $\delta > 0$ such that $|f(x) - L| < \varepsilon$ for every $x \in D$ with $0 < |x - a| < \delta$.
  - *At infinity:* if $D$ is not bounded above, a real number $L$ is a limit of $f$ at $\infty$, written $\lim_{x \to \infty} f(x) = L$, if and only if for every $\varepsilon > 0$ there exists $M \in \mathbb R$ such that $|f(x) - L| < \varepsilon$ for every $x \in D$ with $x > M$. Limits at $-\infty$ are defined symmetrically.
:::
::::

The proof of uniqueness for sequences works here too (the accumulation-point condition guarantees that the $x$ it needs exists), so we speak of *the* limit. The condition $0 < |x - a|$ means that the value $f(a)$, if it is defined at all, plays no role. For the average slope above, $|g(h) - 2| = |h| < \varepsilon$ whenever $0 < |h| < \delta := \varepsilon$, so $\lim_{h\to 0} g(h) = 2$.

**One-sided limits** restrict the domain. The right-hand limit $\lim_{x \to a^+} f(x)$ is the limit at $a$ of the restriction of $f$ to $D \cap (a, \infty)$, and the left-hand limit $\lim_{x\to a^-} f(x)$ uses $D \cap (-\infty, a)$. If $a$ is an accumulation point of both sets, then $\lim_{x\to a} f(x) = L$ if and only if both one-sided limits equal $L$: a $\delta$ for $f$ works for both restrictions, and conversely the smaller of the two one-sided $\delta$'s works for $f$.

**Infinite limits:** $\lim_{x \to a} f(x) = \infty$ means that for every $M \in \mathbb R$ there is a $\delta > 0$ with $f(x) > M$ for every $x \in D$ with $0 < |x - a| < \delta$. The variants for $-\infty$, for one-sided limits, and for $x \to \pm\infty$ are analogous. For example, $\lim_{x \to 0^+} 1/x = \infty$.

:::{important icon=false} 📐 **Lemma (Sequential Characterization of Limits)**
Let $a$ be an accumulation point of $D$, $f: D \to \mathbb R$, and $L \in \mathbb R$. Then $\lim_{x\to a} f(x) = L$ if and only if $f(x_n) \to L$ for every sequence $(x_n)$ in $D \setminus\{a\}$ with $x_n \to a$. The analogous statement holds at $\pm\infty$, with sequences $x_n \to \pm\infty$.
:::

:::{admonition icon=false} ✍️ **Proof**
($\Rightarrow$) Let $\varepsilon > 0$ and take $\delta$ from the definition. Since $x_n \to a$, there is $N$ with $|x_n - a| < \delta$ for $n \ge N$; as $x_n \ne a$, this gives $|f(x_n) - L| < \varepsilon$.

($\Leftarrow$) Suppose the limit is not $L$. Then there is an $\varepsilon > 0$ for which no $\delta$ works: for every $n \ge 1$ there is an $x_n \in D$ with $0 < |x_n - a| < 1/n$ but $|f(x_n) - L| \ge \varepsilon$[^countable-choice]. Then $x_n \to a$ with $x_n \ne a$, but $f(x_n) \not\to L$.

The proof at $\pm\infty$ is the same, with $|x - a| < \delta$ replaced by $x > M$ (or $x < M$). $\blacksquare$
:::

:::{important icon=false} 📐 **Corollary (Limit Laws for Functions)**
The Limit Laws for Sequences (sums, scalar multiples, products, quotients with nonzero limit and nonvanishing denominator, order, and squeeze) hold for limits of functions at a point, at $\pm\infty$, and for one-sided limits.
:::

:::{admonition icon=false} ✍️ **Proof**
For example, if $f(x) \to A$ and $g(x) \to B$ as $x \to a$, then for every sequence $x_n \to a$ in $D\setminus\{a\}$ we have $f(x_n) \to A$ and $g(x_n) \to B$, so $f(x_n) + g(x_n) \to A + B$ by the sequence laws; by the lemma, $f(x) + g(x) \to A + B$. The other laws follow in the same way. $\blacksquare$
:::

[^countable-choice]: Choosing one $x_n$ for every $n$ at once uses the axiom of countable choice, as in [Chapter 3](ch3_sets_for_probability_v2.md). The same remark applies to the proofs of uniform continuity and the extreme value theorem below.
  
### Continuity

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Continuous
: Let $D \subseteq \mathbb R$, $f: D \to \mathbb R$, and $a \in D$. The function $f$ is continuous at $a$ if and only if for every $\varepsilon > 0$ there exists $\delta > 0$ such that $|f(x) - f(a)| < \varepsilon$ for every $x \in D$ with $|x - a| < \delta$. It is continuous (on $D$) if and only if it is continuous at every point of $D$.
:::
::::

If $a \in D$ is an accumulation point of $D$, continuity at $a$ says exactly that $\lim_{x\to a} f(x) = f(a)$: the limit exists *and* equals the value. (At a point of $D$ that is not an accumulation point, every function is continuous.) The proof of the Sequential Characterization gives: $f$ is continuous at $a$ if and only if $f(x_n) \to f(a)$ for every sequence $(x_n)$ in $D$ with $x_n \to a$.

:::{important icon=false} 📐 **Lemma (Building Continuous Functions)**
1. Constant functions, the identity $x \mapsto x$, and $x \mapsto |x|$ are continuous on $\mathbb R$.
2. If $f, g: D \to \mathbb R$ are continuous at $a$ and $c \in \mathbb R$, then $f + g$, $cf$, and $fg$ are continuous at $a$, and so is $f/g$ if $g(x) \ne 0$ for every $x \in D$.
3. If $g: D \to E$ is continuous at $a$ and $f: E \to \mathbb R$ is continuous at $g(a)$, then the {term}`composition` $f \circ g$ is continuous at $a$.

Consequently every polynomial is continuous on $\mathbb R$, and every quotient of polynomials is continuous wherever its denominator is nonzero.
:::

:::{admonition icon=false} ✍️ **Proof**
1. For a constant any $\delta$ works. For the identity take $\delta := \varepsilon$; for $|x|$ also take $\delta := \varepsilon$, since $\big||x| - |a|\big| \le |x - a|$.
2. Use the sequential characterization of continuity and the Limit Laws for Sequences.
3. Let $\varepsilon > 0$. Continuity of $f$ at $g(a)$ gives $\eta > 0$ with $|f(y) - f(g(a))| < \varepsilon$ for $y \in E$ with $|y - g(a)| < \eta$. Continuity of $g$ at $a$ (with tolerance $\eta$) gives $\delta > 0$ with $|g(x) - g(a)| < \eta$ for $x \in D$ with $|x - a| < \delta$. For such $x$, $|f(g(x)) - f(g(a))| < \varepsilon$. $\blacksquare$
:::

**The display is discontinuous at half-steps.** Let $c := (m + \frac12)\Delta$ for an integer $m$. Then $c/\Delta + \frac12 = m + 1$, so $Q(c) = (m+1)\Delta$, while every $x \in [c - \Delta, c)$ has $x/\Delta + \frac12 \in [m, m+1)$ and hence $Q(x) = m\Delta$. Take $\varepsilon := \Delta/2$. For every $\delta > 0$, the point $x := c - \min(\delta, \Delta)/2$ satisfies $|x - c| < \delta$ but $|Q(x) - Q(c)| = \Delta > \varepsilon$. So $Q$ is not continuous at $c$. At every other point $x_0$, the number $x_0/\Delta + \frac12$ lies strictly between two consecutive integers, so $Q$ is constant on an interval around $x_0$ and therefore continuous at $x_0$.
  
### The Intermediate Value Theorem

:::{important icon=false} 📐 **Theorem (Intermediate Value Theorem)**
Let $f: [a, b] \to \mathbb R$ be continuous and let $y$ lie between $f(a)$ and $f(b)$ (inclusive). Then $f(c) = y$ for some $c \in [a, b]$.
:::

:::{admonition icon=false} ✍️ **Proof**
Replacing $f$ and $y$ by $-f$ and $-y$ if necessary, assume $f(a) \le y \le f(b)$. The set $S := \{x \in [a,b] : f(x) \le y\}$ contains $a$ and is bounded above by $b$, so $c := \sup S$ exists and $c \in [a, b]$.

- *$f(c) \le y$:* Suppose $f(c) > y$. Continuity at $c$ with $\varepsilon := f(c) - y$ gives $\delta > 0$ with $f(x) > y$ for every $x \in [a,b]$ with $|x - c| < \delta$. Since $c$ is the least upper bound of $S$, some $x \in S$ has $c - \delta < x \le c$; then $f(x) > y$, contradicting $x \in S$.
- *$f(c) \ge y$:* Suppose $f(c) < y$. Then $c \ne b$ because $f(b) \ge y$, so $c < b$. Continuity with $\varepsilon := y - f(c)$ gives $\delta > 0$ with $f(x) < y$ for every $x \in [a, b]$ with $|x - c| < \delta$. The point $x := \min(c + \delta/2, b)$ is then in $S$ and greater than $c = \sup S$, a contradiction.

Hence $f(c) = y$. $\blacksquare$
:::

:::{important icon=false} 📐 **Corollary (Square Roots)**
For every $y \ge 0$ there is exactly one $x \ge 0$ with $x^2 = y$. We write $\sqrt y := x$.
:::

:::{admonition icon=false} ✍️ **Proof**
Let $b := \max(1, y)$. The polynomial $x \mapsto x^2$ is continuous on $[0, b]$, with $0^2 = 0 \le y$ and $b^2 \ge b \ge y$, so the intermediate value theorem gives existence. Uniqueness: if $0 \le x < x'$ then $x^2 < x'^2$, so $x \mapsto x^2$ is strictly increasing on $[0, \infty)$. $\blacksquare$
:::

The next lemma shows that inverses of strictly increasing functions between intervals are automatically continuous. We use it for $\sqrt{\phantom{y}}$ now and for the natural logarithm later.

:::{important icon=false} 📐 **Lemma (Continuous Inverse)**
Let $I$ and $J$ be intervals and let $f: I \to J$ be a strictly increasing bijection. Then the {term}`inverse function` $f^{-1}: J \to I$ is strictly increasing and continuous.
:::

:::{admonition icon=false} ✍️ **Proof**
If $y < y'$ in $J$, then $f^{-1}(y) \ge f^{-1}(y')$ would give $y \ge y'$ because $f$ is increasing; so $f^{-1}$ is strictly increasing. For continuity, let $y_0 \in J$, $x_0 := f^{-1}(y_0)$, and $\varepsilon > 0$. If $x_0$ is not the least element of $I$, pick $p \in I$ with $p < x_0$ and set $x_- := \max(p, x_0 - \varepsilon/2)$; it lies in $I$ because $I$ is an interval, and $x_0 - \varepsilon < x_- < x_0$. Set $\delta_- := y_0 - f(x_-) > 0$. Symmetrically, if $x_0$ is not the greatest element of $I$, pick $x_+ \in I$ with $x_0 < x_+ < x_0 + \varepsilon$ and set $\delta_+ := f(x_+) - y_0 > 0$. Let $\delta$ be the smaller of the $\delta_\pm$ that are defined (if neither is, $I = \{x_0\}$ and there is nothing to prove).

Let $y \in J$ with $|y - y_0| < \delta$. If $y < y_0$, then $x_0 = f^{-1}(y_0)$ is not the least element of $I$ (since $f^{-1}(y) < x_0$), so $x_-$ is defined, and $f(x_-) = y_0 - \delta_- < y < y_0$ gives $x_- < f^{-1}(y) < x_0$. The case $y > y_0$ is symmetric. In every case $|f^{-1}(y) - x_0| < \varepsilon$. $\blacksquare$
:::

Since $x \mapsto x^2$ is a strictly increasing bijection from $[0,\infty)$ onto $[0, \infty)$ (by the Square Roots corollary), its inverse $\sqrt{\phantom{y}}$ is continuous on $[0, \infty)$.
  
### Uniform Continuity

In the definition of continuity, $\delta$ may depend on the point $a$ as well as on $\varepsilon$. A function $f: D \to \mathbb R$ is **uniformly continuous** if one $\delta$ works for all points at once: for every $\varepsilon > 0$ there is $\delta > 0$ such that $|f(x) - f(x')| < \varepsilon$ for all $x, x' \in D$ with $|x - x'| < \delta$. For example, $x \mapsto x^2$ is continuous on $\mathbb R$ but not uniformly continuous: for $x = n$ and $x' = n + \frac1n$, the inputs are within $\frac1n$ of each other, yet $x'^2 - x^2 = 2 + \frac{1}{n^2} \ge 2$. On a closed bounded interval this cannot happen. Uniform continuity is what makes continuous functions integrable.

:::{important icon=false} 📐 **Theorem (Uniform Continuity on Closed Bounded Intervals)**
Every continuous function $f: [a, b] \to \mathbb R$ is uniformly continuous.
:::

:::{admonition icon=false} ✍️ **Proof**
Suppose not. Then there is an $\varepsilon > 0$ such that for every $n \ge 1$ there are $x_n, x_n' \in [a, b]$ with $|x_n - x_n'| < 1/n$ but $|f(x_n) - f(x_n')| \ge \varepsilon$. The sequence $(x_n)$ is bounded, so by Bolzano–Weierstrass some subsequence $x_{n_k} \to c$, and $c \in [a, b]$ by the order law. Also $|x'_{n_k} - c| \le 1/n_k + |x_{n_k} - c| \to 0$, so $x'_{n_k} \to c$. By continuity at $c$, $f(x_{n_k}) - f(x'_{n_k}) \to f(c) - f(c) = 0$, contradicting $|f(x_{n_k}) - f(x'_{n_k})| \ge \varepsilon$. $\blacksquare$
:::

:::{caution icon=false} ⚠️ **Assumptions and Failure Modes**
- **The intermediate value theorem needs continuity.** The display $Q$ jumps from $155.0$ to $155.1$ but never shows $155.05$.
- **It also needs an interval.** $f(x) = 1/x$ is continuous on $[-1, 0) \cup (0, 1]$ with $f(-1) < 0 < f(1)$, yet it is never $0$.
- **Uniform continuity needs a closed bounded interval.** $x^2$ on $\mathbb R$ fails (shown above), and so does $1/x$ on $(0, 1]$: near $0$, inputs $\frac1n$ and $\frac{1}{2n}$ are close but their values differ by $n$.
- **Completeness again.** Over $\mathbb Q$, the function $x^2 - 2$ is continuous on $\{q \in \mathbb Q : 0 \le q \le 2\}$, negative at $0$ and positive at $2$, but never $0$.
:::

:::{attention icon=false} 🗝️ **Key Idea**
$\lim_{x\to a} f(x) = L$ means $f(x)$ is eventually within any tolerance of $L$ once $x \ne a$ is close enough to $a$; continuity at $a$ means the limit is the value $f(a)$. On a closed bounded interval, a continuous function takes every intermediate value and is uniformly continuous; both facts rest on the completeness of $\mathbb R$.
:::
  
## Derivatives

A cart starts at rest and accelerates at a constant $a$ (in m/s²), so its position after $t$ seconds is $p(t) = \frac12 a t^2$. Its average velocity over the time interval from $t$ to $t + h$ is

$$\frac{p(t+h) - p(t)}{h} = \frac{\frac12 a(t^2 + 2th + h^2) - \frac12 a t^2}{h} = at + \tfrac12 a h \qquad (h \ne 0),$$

which tends to $at$ as $h \to 0$. That limit is the cart's velocity at time $t$. The alpha–beta filter of the [Introduction](introduction_v2.md) estimates such a rate from differences of noisy positions; the derivative is the exact quantity those differences approximate.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Derivative
: Let $D \subseteq \mathbb R$, $f: D \to \mathbb R$, and let $a \in D$ be an accumulation point of $D$. The derivative of $f$ at $a$ is the {term}`limit <limit of a function>`
  $$f'(a) := \lim_{h \to 0} \frac{f(a + h) - f(a)}{h},$$
  taken over the nonzero $h$ with $a + h \in D$, provided this limit exists as a real number. If $f'(a)$ exists for every $a$ in a set $E \subseteq D$, the function $f': E \to \mathbb R$, $a \mapsto f'(a)$, is also called the derivative of $f$ on $E$.
:::
::::

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Differentiable
: A function $f: D \to \mathbb R$ is differentiable at $a \in D$ if and only if $a$ is an accumulation point of $D$ and the {term}`derivative` $f'(a)$ exists. It is differentiable on a set $E \subseteq D$ if and only if it is differentiable at every point of $E$, and differentiable if and only if it is differentiable on $D$.
:::
::::

Some notation and vocabulary:

- Other notations for $f'(a)$ are $\frac{df}{dx}(a)$ and $\frac{d}{dx}f(x)\big|_{x=a}$. For a function of time, a dot is common: $\dot p(t) := p'(t)$. Chapter 10 and the orientation chapters use the dot.
- On a closed interval $D = [a, b]$, the derivative at an endpoint only uses points inside the interval, so it is automatically one-sided.
- Higher derivatives are defined recursively: $f'' := (f')'$, and in general $f^{(0)} := f$ and $f^{(n+1)} := (f^{(n)})'$. We say $f$ is *$n$ times differentiable* on $D$ if $f^{(n)}(x)$ exists for every $x \in D$, and *continuously differentiable* on $D$ if $f'$ exists and is continuous on $D$.

For the cart, $\dot p(t) = at$ is the velocity and $\ddot p(t) = a$ is the acceleration.

:::{important icon=false} 📐 **Lemma (Carathéodory's Criterion)**
Let $f: D \to \mathbb R$ and let $a \in D$ be an accumulation point of $D$. Then $f$ is differentiable at $a$ if and only if there is a function $\varphi: D \to \mathbb R$ that is continuous at $a$ and satisfies
$$f(x) - f(a) = \varphi(x)\,(x - a) \qquad \text{for every } x \in D.$$
In that case $f'(a) = \varphi(a)$.
:::

:::{admonition icon=false} ✍️ **Proof**
($\Rightarrow$) Define $\varphi(x) := \frac{f(x) - f(a)}{x - a}$ for $x \ne a$ and $\varphi(a) := f'(a)$. The identity holds for $x \ne a$ by construction and for $x = a$ because both sides are $0$. Writing $x = a + h$, the statement $\lim_{x\to a}\varphi(x) = \varphi(a)$ is exactly the definition of $f'(a)$, so $\varphi$ is continuous at $a$.

($\Leftarrow$) For $x \ne a$, $\frac{f(x) - f(a)}{x - a} = \varphi(x)$, which tends to $\varphi(a)$ as $x \to a$ because $\varphi$ is continuous at $a$. $\blacksquare$
:::

:::{important icon=false} 📐 **Corollary (Differentiable Implies Continuous)**
If $f$ is differentiable at $a$, then $f$ is continuous at $a$.
:::

:::{admonition icon=false} ✍️ **Proof**
$f(x) = f(a) + \varphi(x)(x - a)$, and the right side is continuous at $a$ by the Building Continuous Functions lemma. $\blacksquare$
:::

Writing $r(h) := f(a + h) - f(a) - f'(a)\,h$, the definition of the derivative says exactly that $r(h)/h \to 0$ as $h \to 0$:

$$f(a + h) = f(a) + f'(a)\,h + r(h), \qquad \lim_{h\to 0}\frac{r(h)}{h} = 0.$$

So near $a$, the *tangent line* $h \mapsto f(a) + f'(a)h$ approximates $f(a+h)$ with an error that is small even compared with $h$. This **first-order approximation** is the idea behind the extended Kalman filter ([Chapter 15](ch15_extended_kalman_filter_v2.md)); Taylor's Theorem below bounds the error $r(h)$.
  
### Rules of Differentiation

:::{important icon=false} 📐 **Theorem (Differentiation Rules)**
Let $f, g: D \to \mathbb R$ be differentiable at $a \in D$ and let $c \in \mathbb R$.
1. *(Linearity)* $(f + g)'(a) = f'(a) + g'(a)$ and $(cf)'(a) = c\,f'(a)$.
2. *(Product rule)* $(fg)'(a) = f'(a)\,g(a) + f(a)\,g'(a)$.
3. *(Quotient rule)* If $g(x) \ne 0$ for every $x \in D$, then $\left(\frac fg\right)'(a) = \frac{f'(a)\,g(a) - f(a)\,g'(a)}{g(a)^2}$.
4. *(Chain rule)* Let $g: D \to E$ be differentiable at $a$ and $f: E \to \mathbb R$ be differentiable at $g(a)$. Then $f \circ g$ is differentiable at $a$ and $(f \circ g)'(a) = f'(g(a))\,g'(a)$.
:::

:::{admonition icon=false} ✍️ **Proof**
By Carathéodory's criterion, write $f(x) - f(a) = \varphi(x)(x - a)$ and $g(x) - g(a) = \psi(x)(x - a)$ with $\varphi, \psi$ continuous at $a$, $\varphi(a) = f'(a)$, and $\psi(a) = g'(a)$. In each part we exhibit a function that is continuous at $a$ (by the Building Continuous Functions lemma, using that $g$ is continuous at $a$) and apply the criterion again.
1. $(f+g)(x) - (f+g)(a) = (\varphi + \psi)(x)\,(x - a)$ and $(cf)(x) - (cf)(a) = c\,\varphi(x)\,(x - a)$.
2. $f(x)g(x) - f(a)g(a) = \big(f(x) - f(a)\big)g(x) + f(a)\big(g(x) - g(a)\big) = \big[\varphi(x)\,g(x) + f(a)\,\psi(x)\big](x - a)$, and the bracket has value $f'(a)g(a) + f(a)g'(a)$ at $a$.
3. First, $\frac{1}{g(x)} - \frac{1}{g(a)} = -\frac{g(x) - g(a)}{g(x)\,g(a)} = \left[-\frac{\psi(x)}{g(x)\,g(a)}\right](x - a)$, so $(1/g)'(a) = -g'(a)/g(a)^2$. Then apply the product rule to $f \cdot \frac1g$.
4. Let $b := g(a)$ and write $f(y) - f(b) = \chi(y)(y - b)$ for $y \in E$, with $\chi$ continuous at $b$ and $\chi(b) = f'(b)$. Then for every $x \in D$,
$$f(g(x)) - f(g(a)) = \chi(g(x))\,\big(g(x) - g(a)\big) = \big[\chi(g(x))\,\psi(x)\big](x - a).$$
The bracket is continuous at $a$ (a composition and a product of functions continuous at the relevant points) with value $f'(g(a))\,g'(a)$. $\blacksquare$
:::

The tempting proof of the chain rule, multiplying and dividing by $g(x) - g(a)$, fails when $g(x) = g(a)$ for $x$ arbitrarily close to $a$ (for example, when $g$ is constant). Carathéodory's criterion avoids dividing by anything.

:::{important icon=false} 📐 **Corollary (Power Rule for Integer Exponents)**
For every $n \in \mathbb N^+$, $\frac{d}{dx}x^n = n\,x^{n-1}$ on $\mathbb R$, and $\frac{d}{dx}x^{-n} = -n\,x^{-n-1}$ for $x \ne 0$. Consequently, every polynomial is differentiable with $\frac{d}{dx}\sum_{k=0}^m c_k x^k = \sum_{k=1}^m k\,c_k\,x^{k-1}$.
:::

:::{admonition icon=false} ✍️ **Proof**
Constants have derivative $0$ (the difference quotient is $0$), and $\frac{d}{dx}x = 1$ (the difference quotient is $h/h = 1$). By induction with the product rule, $\frac{d}{dx}x^{n+1} = \frac{d}{dx}(x^n \cdot x) = n x^{n-1}\cdot x + x^n \cdot 1 = (n+1)x^n$. For negative exponents, the quotient rule gives $\frac{d}{dx}\frac{1}{x^n} = \frac{0 \cdot x^n - 1\cdot n x^{n-1}}{x^{2n}} = -n x^{-n-1}$. The statement about polynomials follows by linearity. $\blacksquare$
:::

:::{important icon=false} 📐 **Theorem (Derivative of an Inverse Function)**
Let $I$ and $J$ be intervals with more than one point, let $f: I \to J$ be a strictly increasing bijection, let $a \in I$, and let $b := f(a)$. If $f$ is differentiable at $a$ with $f'(a) \ne 0$, then $f^{-1}$ is differentiable at $b$ and
$$(f^{-1})'(b) = \frac{1}{f'(a)}.$$
:::

:::{admonition icon=false} ✍️ **Proof**
By the Continuous Inverse lemma, $f^{-1}$ is continuous. Write $f(x) - f(a) = \varphi(x)(x - a)$ with $\varphi$ continuous at $a$ and $\varphi(a) = f'(a) \ne 0$. For $x \ne a$, $\varphi(x) = \frac{f(x) - f(a)}{x - a} \ne 0$ because $f$ is injective, so $\varphi$ is nonzero on all of $I$. Substituting $x = f^{-1}(y)$ for $y \in J$ gives $y - b = \varphi(f^{-1}(y))\,\big(f^{-1}(y) - f^{-1}(b)\big)$, that is,
$$f^{-1}(y) - f^{-1}(b) = \left[\frac{1}{\varphi(f^{-1}(y))}\right](y - b).$$
The bracket is continuous at $b$ (composition of $f^{-1}$, continuous at $b$, with $1/\varphi$, continuous at $a = f^{-1}(b)$), with value $1/f'(a)$. Apply Carathéodory's criterion. $\blacksquare$
:::

**Example.** With $f(x) = x^2$ on $I = J = [0, \infty)$, for every $y > 0$ we get $\frac{d}{dy}\sqrt y = \frac{1}{2\sqrt y}$. At $y = 0$ the theorem does not apply because $f'(0) = 0$, and indeed $\sqrt{\phantom{y}}$ is not differentiable at $0$: the difference quotient $\frac{\sqrt h - 0}{h} = \frac{1}{\sqrt h}$ tends to $\infty$ as $h \to 0^+$.

:::{caution icon=false} ⚠️ **Assumptions and Failure Modes**
- **Continuous does not imply differentiable.** $|x|$ is continuous at $0$, but its difference quotient $|h|/h$ is $1$ for $h > 0$ and $-1$ for $h < 0$, so it has no limit.
- **Differentiating noisy data amplifies noise.** If $z_k = x(t_k) + v_k$ with noise of typical size $\sigma$, the difference quotient $(z_k - z_{k-1})/\Delta t$ contains the noise term $(v_k - v_{k-1})/\Delta t$, whose typical size grows like $\sigma/\Delta t$ as the sample period shrinks[^typical-size]. Rates must be estimated, not differentiated, which is what the alpha–beta filter and the Kalman filter do.
- **Quantized signals are useless for slopes.** The display $Q$ has derivative $0$ wherever it is differentiable and is not differentiable at the jumps.
:::

:::{attention icon=false} 🗝️ **Key Idea**
The derivative $f'(a)$ is the limit of the difference quotients $\frac{f(a+h) - f(a)}{h}$. Equivalently, $f(a + h) = f(a) + f'(a)h + r(h)$ with $r(h)/h \to 0$: the tangent line is the best linear approximation near $a$. The sum, product, quotient, and chain rules all follow from writing $f(x) - f(a) = \varphi(x)(x - a)$.
:::

[^typical-size]: Used informally here; [Chapter 6](ch6_expectation_and_variance_v2.md) makes "typical size" precise as the standard deviation.
  
## The Mean Value Theorem and Extrema

[Chapter 7](ch7_optimal_alpha_v2.md) combines a prediction with error variance $P^- > 0$ and a measurement with noise variance $R > 0$, and shows that the gain $\alpha$ produces the error variance[^variance-informal]

$$P(\alpha) = (1 - \alpha)^2 P^- + \alpha^2 R.$$

Which $\alpha$ makes $P(\alpha)$ smallest? Chapter 7 answers by completing the square. Calculus offers a second route: at a minimum inside an interval, the graph has a horizontal tangent. This section proves that fact, together with the Mean Value Theorem, which turns information about $f'$ into information about $f$.

Let $f: D \to \mathbb R$. The function has a **(global) maximum** at $c \in D$ if $f(c) \ge f(x)$ for every $x \in D$, and a **local maximum** at $c$ if there is $\delta > 0$ such that $f(c) \ge f(x)$ for every $x \in D$ with $|x - c| < \delta$. Minima are defined with $\le$, and an **extremum** is a maximum or a minimum. A point $c$ is an **interior point** of $D$ if $(c - \delta, c + \delta) \subseteq D$ for some $\delta > 0$.

:::{important icon=false} 📐 **Theorem (Extreme Value Theorem)**
Let $a \le b$ and let $f: [a, b] \to \mathbb R$ be continuous. Then $f$ is bounded, and there are $c_1, c_2 \in [a, b]$ with $f(c_1) \le f(x) \le f(c_2)$ for every $x \in [a, b]$.
:::

:::{admonition icon=false} ✍️ **Proof**
*Bounded above:* otherwise, for every $n$ there is $x_n \in [a, b]$ with $f(x_n) > n$. By Bolzano–Weierstrass some subsequence $x_{n_k} \to c$, and $c \in [a, b]$ by the order law. By continuity $f(x_{n_k}) \to f(c)$, so the convergent sequence $(f(x_{n_k}))$ is bounded; but $f(x_{n_k}) > n_k \ge k$, a contradiction.

*Maximum attained:* let $M := \sup\{f(x) : x \in [a, b]\}$. For every $n \ge 1$, $M - \frac1n$ is not an upper bound, so there is $x_n$ with $M - \frac1n < f(x_n) \le M$. Again some subsequence $x_{n_k} \to c_2 \in [a,b]$. By the squeeze law $f(x_{n_k}) \to M$, and by continuity $f(x_{n_k}) \to f(c_2)$. By uniqueness of limits, $f(c_2) = M$.

Applying both parts to $-f$ gives boundedness below and $c_1$. $\blacksquare$
:::

:::{important icon=false} 📐 **Lemma (Interior Extremum)**
If $f: D \to \mathbb R$ has a local maximum or local minimum at an interior point $c$ of $D$ and is differentiable at $c$, then $f'(c) = 0$.
:::

:::{admonition icon=false} ✍️ **Proof**
Consider a local maximum (for a minimum, apply this to $-f$). Choose $\delta > 0$ with $(c - \delta, c + \delta) \subseteq D$ and $f(x) \le f(c)$ on that interval. For $0 < h < \delta$ the difference quotient $\frac{f(c + h) - f(c)}{h}$ is $\le 0$, and for $-\delta < h < 0$ it is $\ge 0$. Both one-sided limits of the difference quotient equal $f'(c)$, so the order law for limits of functions gives $f'(c) \le 0$ and $f'(c) \ge 0$. $\blacksquare$
:::

:::{important icon=false} 📐 **Theorem (Rolle's Theorem)**
Let $a < b$, and let $f: [a, b] \to \mathbb R$ be continuous on $[a,b]$ and differentiable on $(a, b)$, with $f(a) = f(b)$. Then $f'(c) = 0$ for some $c \in (a, b)$.
:::

:::{admonition icon=false} ✍️ **Proof**
By the Extreme Value Theorem, $f$ attains a minimum at some $c_1$ and a maximum at some $c_2$. If both lie in $\{a, b\}$, then the minimum and maximum both equal $f(a) = f(b)$, so $f$ is constant and $f'(c) = 0$ for every $c \in (a, b)$. Otherwise one of them, say $c$, lies in $(a, b)$, which is an interior point of $[a, b]$, and the Interior Extremum lemma gives $f'(c) = 0$. $\blacksquare$
:::

:::{important icon=false} 📐 **Theorem (Mean Value Theorem)**
Let $a < b$, and let $f: [a, b] \to \mathbb R$ be continuous on $[a,b]$ and differentiable on $(a,b)$. Then there is $c \in (a, b)$ with
$$f'(c) = \frac{f(b) - f(a)}{b - a}.$$
:::

:::{admonition icon=false} ✍️ **Proof**
Let $m := \frac{f(b) - f(a)}{b - a}$ and $g(x) := f(x) - f(a) - m(x - a)$. Then $g$ is continuous on $[a,b]$, differentiable on $(a, b)$ with $g' = f' - m$, and $g(a) = g(b) = 0$. Rolle's Theorem gives $c \in (a,b)$ with $0 = g'(c) = f'(c) - m$. $\blacksquare$
:::

In words: a cart that travels 100 m in 10 s has velocity exactly 10 m/s at some instant, whatever it does in between.

:::{important icon=false} 📐 **Corollary (Monotonicity and Constant Functions)**
Let $I$ be an interval and let $f: I \to \mathbb R$ be continuous and differentiable at every interior point of $I$.
1. If $f'(x) = 0$ for every interior point $x$, then $f$ is constant.
2. If $f'(x) \ge 0$ for every interior point $x$, then $f$ is increasing ($x < y \Rightarrow f(x) \le f(y)$); if $f'(x) > 0$, then $f$ is strictly increasing. The analogous statements hold for $\le 0$ and $< 0$ with decreasing.
3. If $g: I \to \mathbb R$ satisfies the same hypotheses as $f$ and $f'(x) = g'(x)$ at every interior point $x$, then $f - g$ is constant.
:::

:::{admonition icon=false} ✍️ **Proof**
Let $x < y$ in $I$. Since $I$ is an interval, $[x, y] \subseteq I$, and every point of $(x, y)$ is an interior point of $I$. The Mean Value Theorem gives $c \in (x, y)$ with $f(y) - f(x) = f'(c)\,(y - x)$, whose sign is the sign of $f'(c)$. This proves parts 1 and 2. For part 3, apply part 1 to $f - g$. $\blacksquare$
:::

**The optimal gain by calculus.** $P$ is a polynomial in $\alpha$ with
$$P'(\alpha) = -2(1-\alpha)P^- + 2\alpha R = 2(P^- + R)\Big(\alpha - \frac{P^-}{P^- + R}\Big).$$
Let $\alpha^* := \frac{P^-}{P^- + R}$. Then $P' < 0$ on $(-\infty, \alpha^*)$ and $P' > 0$ on $(\alpha^*, \infty)$, so by the corollary $P$ is strictly decreasing on $(-\infty, \alpha^*]$ and strictly increasing on $[\alpha^*, \infty)$. Hence $\alpha^*$ is the unique minimizer of $P$ over all of $\mathbb R$. Substituting $1 - \alpha^* = \frac{R}{P^- + R}$ gives the minimum value $P(\alpha^*) = \frac{R^2 P^- + (P^-)^2 R}{(P^- + R)^2} = \frac{P^- R}{P^- + R}$, in agreement with Chapter 7.

:::{caution icon=false} ⚠️ **Assumptions and Failure Modes**
- **A zero derivative does not imply an extremum.** $f(x) = x^3$ has $f'(0) = 0$, but it is strictly increasing. The Interior Extremum lemma gives a necessary condition only.
- **Extrema on the boundary need not be critical points.** On $[0, 1]$, $f(x) = x$ has its maximum at $1$ where $f'(1) = 1$. The lemma requires an interior point.
- **The Extreme Value Theorem needs a closed bounded interval and continuity.** $f(x) = x$ on $(0,1)$ has no maximum, $1/x$ on $(0, 1]$ is unbounded, and $f(x) = x$ for $x < 1$ with $f(1) := 0$ has supremum $1$ on $[0, 1]$ but never reaches it.
- **The Mean Value Theorem needs differentiability on all of $(a,b)$.** For $|x|$ on $[-1, 1]$ the average slope is $0$, but the derivative is never $0$.
- **"Zero derivative implies constant" needs an interval.** On $\mathbb R\setminus\{0\}$, the function that is $-1$ for $x < 0$ and $1$ for $x > 0$ has derivative $0$ everywhere but is not constant. This is why two antiderivatives differ by a constant only on an interval.
:::

:::{attention icon=false} 🗝️ **Key Idea**
Continuous functions on closed bounded intervals attain their extremes, and at an interior extremum the derivative vanishes. The Mean Value Theorem, $f(b) - f(a) = f'(c)(b - a)$, converts knowledge of the derivative into knowledge of the function: its sign gives monotonicity, and a zero derivative on an interval means a constant function.
:::

[^variance-informal]: Variance is defined in [Chapter 6](ch6_expectation_and_variance_v2.md). Here $P^-$ and $R$ are simply positive numbers, and nothing in this section depends on what they mean.
  
## Taylor's Theorem

[Chapter 6](ch6_expectation_and_variance_v2.md) shows that an EMA with smoothing factor $\alpha$, fed constant-plus-noise measurements, ends up with noise {term}`variance` $\sigma^2 g(\alpha)$, where $g(\alpha) := \frac{\alpha}{2 - \alpha}$ (only the function $g$ matters here). For small $\alpha$ engineers use $g(\alpha) \approx \frac{\alpha}{2}$. Where does that come from, and how wrong can it be?

By the quotient and chain rules, $g'(\alpha) = \frac{2}{(2-\alpha)^2}$ and $g''(\alpha) = \frac{4}{(2-\alpha)^3}$ for $\alpha < 2$. So $g(0) = 0$ and $g'(0) = \frac12$, and $\frac\alpha2$ is the tangent line at $0$. Taylor's Theorem generalizes tangent lines to polynomials of any degree and, crucially, says how large the error is.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Taylor polynomial
: Let $n \in \mathbb N$ and let $f$ be a function whose derivatives $f', f'', \ldots, f^{(n)}$ exist at the point $a$ (with $f^{(0)} := f$). The Taylor polynomial of degree $n$ of $f$ at $a$ is
  $$T_{n,a}f(x) := \sum_{k=0}^{n} \frac{f^{(k)}(a)}{k!}\,(x - a)^k = f(a) + f'(a)(x - a) + \frac{f''(a)}{2}(x-a)^2 + \cdots + \frac{f^{(n)}(a)}{n!}(x - a)^n.$$
:::
::::

The factorials make $T_{n,a}f$ match $f$ to order $n$ at $a$: by the power and chain rules, the $j$-th derivative of $(x - a)^k$ at $x = a$ is $k!$ if $j = k$ and $0$ otherwise, so $(T_{n,a}f)^{(j)}(a) = f^{(j)}(a)$ for $j = 0, 1, \ldots, n$. The degree-$1$ Taylor polynomial is the tangent line.

:::{important icon=false} 📐 **Theorem (Taylor's Theorem with Lagrange Remainder)**
Let $I$ be an interval, $n \in \mathbb N$, and $f: I \to \mathbb R$ be $n + 1$ times differentiable on $I$. For all $a, x \in I$ with $x \ne a$, there is a $\xi$ strictly between $a$ and $x$ with
$$f(x) = T_{n,a}f(x) + \frac{f^{(n+1)}(\xi)}{(n+1)!}\,(x - a)^{n+1}.$$
:::

:::{admonition icon=false} ✍️ **Proof**
Fix $x$. For $t \in I$ define
$$G(t) := f(x) - \sum_{k=0}^{n} \frac{f^{(k)}(t)}{k!}(x - t)^k - K\,\frac{(x - t)^{n+1}}{(n+1)!},$$
with the constant $K$ chosen so that $G(a) = 0$ (possible because $(x - a)^{n+1} \ne 0$). Also $G(x) = 0$, because at $t = x$ only the $k = 0$ term survives and it equals $f(x)$. Each $f^{(k)}$ with $k \le n$ is differentiable on $I$, so the product and chain rules give, for $k \ge 1$,
$$\frac{d}{dt}\Big[\frac{f^{(k)}(t)}{k!}(x - t)^k\Big] = \frac{f^{(k+1)}(t)}{k!}(x-t)^k - \frac{f^{(k)}(t)}{(k-1)!}(x - t)^{k-1},$$
and $f'(t)$ for $k = 0$. Summing over $k = 0, \ldots, n$, consecutive terms cancel (the sum *telescopes*), leaving $\frac{f^{(n+1)}(t)}{n!}(x - t)^n$. Therefore
$$G'(t) = -\frac{f^{(n+1)}(t)}{n!}(x - t)^n + K\,\frac{(x - t)^n}{n!} = \frac{(x - t)^n}{n!}\big(K - f^{(n+1)}(t)\big).$$
Rolle's Theorem on the closed interval between $a$ and $x$ gives a $\xi$ strictly between them with $G'(\xi) = 0$. Since $(x - \xi)^n \ne 0$, $K = f^{(n+1)}(\xi)$, and $G(a) = 0$ is exactly the claimed formula. $\blacksquare$
:::

For $n = 0$ the theorem is the Mean Value Theorem. Its main use is an error bound:

:::{important icon=false} 📐 **Corollary (Taylor Error Bound)**
Under the hypotheses of the theorem, if $|f^{(n+1)}(t)| \le M$ for every $t$ between $a$ and $x$, then
$$\big|f(x) - T_{n,a}f(x)\big| \le \frac{M\,|x - a|^{n+1}}{(n+1)!}.$$
:::

:::{admonition icon=false} ✍️ **Proof**
Take absolute values in the theorem. $\blacksquare$
:::

**The EMA variance approximation.** With $n = 1$ and $a = 0$, for $0 < \alpha < 1$ there is $\xi \in (0, \alpha)$ with
$$g(\alpha) = \frac{\alpha}{2} + \frac{g''(\xi)}{2}\alpha^2 = \frac{\alpha}{2} + \frac{2\alpha^2}{(2 - \xi)^3}.$$
Since $2 - \alpha < 2 - \xi < 2$, the error lies between $\frac{\alpha^2}{4}$ and $\frac{2\alpha^2}{(2-\alpha)^3}$. For $\alpha = 0.1$: $\frac{\alpha}{2} = 0.05$, while $g(0.1) = 0.0526\ldots$, and the error $0.0026$ indeed lies between $0.0025$ and $0.0029$. The approximation underestimates the noise by a relative amount of roughly $\alpha/2$.

**The geometric series as a Taylor polynomial.** Let $f(x) = \frac{1}{1-x}$ for $x < 1$. By induction with the chain rule, $f^{(k)}(x) = \frac{k!}{(1-x)^{k+1}}$, so $f^{(k)}(0) = k!$ and
$$T_{n,0}f(x) = 1 + x + x^2 + \cdots + x^n.$$
By the finite geometric sum, the error is exactly $f(x) - T_{n,0}f(x) = \frac{1}{1-x} - \frac{1 - x^{n+1}}{1-x} = \frac{x^{n+1}}{1 - x}$. For $|x| < 1$ it tends to $0$ as $n \to \infty$; for $x \le -1$ it does not, no matter how large $n$ is.

:::{important icon=false} 📐 **Corollary (Second-Derivative Test)**
Let $I$ be an interval, let $f: I \to \mathbb R$ be twice differentiable on $I$, and let $c \in I$ with $f'(c) = 0$. If $f''(t) \ge 0$ for every $t \in I$, then $f$ has a global minimum on $I$ at $c$.
:::

:::{admonition icon=false} ✍️ **Proof**
For $x \in I$ with $x \ne c$, Taylor's Theorem with $n = 1$ gives $f(x) = f(c) + 0 + \frac{f''(\xi)}{2}(x - c)^2 \ge f(c)$. $\blacksquare$
:::

For Chapter 7's error variance, $P''(\alpha) = 2(P^- + R) > 0$ on all of $\mathbb R$, which confirms once more that the critical point $\alpha^*$ is the global minimizer. An interactive comparison of Taylor polynomials of different degrees appears in Exponential and Logarithm, once the exponential, sine, and cosine functions have been defined; that section also derives the power series of $\sin$ and $\cos$ and remainder bounds such as $|\sin x - x| \le |x|^3/6$.

:::{caution icon=false} ⚠️ **Assumptions and Failure Modes**
- **Taylor polynomials are local.** The error bound grows like $|x - a|^{n+1}$, so it says nothing useful far from $a$. For $\frac{1}{1-x}$ the polynomials never converge when $x \le -1$, however large the degree.
- **The bound needs a bound on $f^{(n+1)}$** between $a$ and $x$. For $\frac{\alpha}{2-\alpha}$, $g''$ blows up as $\alpha \to 2$, and so does the error.
- **The theorem needs $n+1$ derivatives on the whole interval.** $f(x) = x|x|$ is differentiable with $f'(x) = 2|x|$, but $f''(0)$ does not exist, so the degree-$1$ remainder formula is unavailable on intervals containing $0$.
- **Even infinitely many derivatives may not be enough** to make the Taylor polynomials converge to $f$; see the example in Exponential and Logarithm.
:::

:::{attention icon=false} 🗝️ **Key Idea**
The Taylor polynomial $T_{n,a}f$ is the polynomial of degree $n$ that matches $f$ and its first $n$ derivatives at $a$. Its error is $\frac{f^{(n+1)}(\xi)}{(n+1)!}(x - a)^{n+1}$ for some $\xi$ between $a$ and $x$, so a bound on the next derivative turns "approximately" into a guaranteed error bar.
:::
  
## The Riemann Integral

A foot-mounted inertial sensor ([Chapter 20](ch20_strapdown_inertial_navigation_v2.md)) knows its velocity $v(t)$ but not its position. If the velocity were constant on each short time interval $[t_{i-1}, t_i]$, the distance traveled would be exactly $\sum_i v(t_i)\,(t_i - t_{i-1})$: the total area of rectangles under the graph of $v$. For a velocity that varies continuously, these sums approach a single number as the intervals shrink, and that number is the distance. The *integral* is this limit.

For a first example, take $f(x) = x^2$ on $[0, 1]$, cut into $n$ equal pieces, and use the height at each right endpoint. Using $\sum_{i=1}^n i^2 = \frac{n(n+1)(2n+1)}{6}$ (proved by induction on $n$),

$$\sum_{i=1}^n \Big(\frac in\Big)^2 \frac1n = \frac{n(n+1)(2n+1)}{6n^3} = \frac{(1 + \frac1n)(2 + \frac1n)}{6} \to \frac13.$$

So the area under $x^2$ between $0$ and $1$ should be $\frac13$. To make "should be" precise, we must say which sums are allowed and in what sense they converge.

Let $a < b$. A **subdivision** $P$ of $[a, b]$ is a finite list of points $a = x_0 < x_1 < \cdots < x_n = b$. (Many books call this a *partition*; we avoid that word because Chapter 3 uses {term}`partition` for something else.) It cuts $[a, b]$ into the subintervals $[x_{i-1}, x_i]$ of widths $\Delta x_i := x_i - x_{i-1}$, and its **mesh** is $\operatorname{mesh}(P) := \max_i \Delta x_i$. A **tagged subdivision** $(P, t)$ also chooses a *tag* $t_i \in [x_{i-1}, x_i]$ in each subinterval. The *uniform* subdivision into $n$ pieces has $x_i = a + i\,\frac{b-a}{n}$ and mesh $\frac{b-a}{n}$, which by the Archimedean property is smaller than any given $\delta > 0$ once $n$ is large.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Riemann sum
: Let $a < b$, $f: [a, b] \to \mathbb R$, and let $(P, t)$ be a tagged subdivision of $[a, b]$ with points $a = x_0 < x_1 < \cdots < x_n = b$ and tags $t_i \in [x_{i-1}, x_i]$. The Riemann sum of $f$ for $(P, t)$ is
  $$R(f, P, t) := \sum_{i=1}^{n} f(t_i)\,(x_i - x_{i-1}).$$
  It adds the signed areas of the rectangles with bases $[x_{i-1}, x_i]$ and heights $f(t_i)$.
:::
::::

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Riemann integral
: Let $a < b$ and $f: [a, b] \to \mathbb R$. The function $f$ is *Riemann integrable* on $[a, b]$ with Riemann integral $I \in \mathbb R$ if and only if for every $\varepsilon > 0$ there exists $\delta > 0$ such that
  $$|R(f, P, t) - I| < \varepsilon \quad\text{for every tagged subdivision } (P, t) \text{ of } [a, b] \text{ with } \operatorname{mesh}(P) < \delta.$$
  We then write $\int_a^b f(x)\,dx := I$. By convention, $\int_a^a f(x)\,dx := 0$ and $\int_b^a f(x)\,dx := -\int_a^b f(x)\,dx$.
:::
::::

The integral is unique when it exists: if $I$ and $I'$ both satisfy the definition with $\delta$ and $\delta'$, a uniform subdivision with mesh below $\min(\delta, \delta')$ gives $|I - I'| < 2\varepsilon$ for every $\varepsilon > 0$. The variable $x$ in $\int_a^b f(x)\,dx$ is a placeholder (any other letter gives the same number), and $dx$ is a reminder of the widths $\Delta x_i$. "Signed" means that rectangles below the axis count negatively. If $f$ is integrable, then for *every* sequence of tagged subdivisions whose meshes tend to $0$, the Riemann sums converge to $\int_a^b f(x)\,dx$, whatever the tags.

The interactive figure shows Riemann sums of $x^2$ for different tag choices. However the tags are chosen, the error shrinks as the mesh does; midpoint tags happen to be especially accurate. The second integrand reappears in The Fundamental Theorem of Calculus as the variance of quantization noise.

```{marimo} python
:hide-code: true

riemann_fn = mo.ui.dropdown(
    options={
        "x² on [0, 1]": "unit",
        "x² on [−½, ½] (quantization)": "quant",
    },
    value="x² on [0, 1]",
    label="integrand",
)
riemann_n = mo.ui.slider(start=1, stop=50, step=1, value=6, label="subintervals $n$")
riemann_tag = mo.ui.dropdown(
    options={
        "left endpoints": "left",
        "midpoints": "mid",
        "right endpoints": "right",
        "random tags": "random",
    },
    value="right endpoints",
    label="tags",
)
```

```{marimo} python
:hide-code: true

_a, _b = (0.0, 1.0) if riemann_fn.value == "unit" else (-0.5, 0.5)
_exact = (_b**3 - _a**3) / 3
_n = riemann_n.value
_x = np.linspace(_a, _b, _n + 1)
_left, _right = _x[:-1], _x[1:]
_rng = np.random.default_rng(3)
_tags = {
    "left": _left,
    "mid": (_left + _right) / 2,
    "right": _right,
    "random": _left + _rng.random(_n) * (_right - _left),
}[riemann_tag.value]
_heights = _tags**2
_R = float(np.sum(_heights * (_right - _left)))

_fig, _ax = plt.subplots(figsize=(7, 3.6))
_ax.bar(_left, _heights, width=_right - _left, align="edge", color="C1", alpha=0.3,
        edgecolor="C1", label="rectangles")
_xx = np.linspace(_a, _b, 400)
_ax.plot(_xx, _xx**2, color="black", linewidth=1.5, label="$f(x) = x^2$")
_ax.plot(_tags, _heights, "o", color="C0", markersize=4, label="tags $(t_i, f(t_i))$")
_ax.set_xlabel("$x$")
_ax.set_ylabel("$f(x)$")
_ax.grid(visible=True, alpha=0.9, linewidth=0.4)
_ax.legend(loc="upper center", fontsize=8)
_ax.set_title(f"Riemann sum with $n = {_n}$ subintervals (mesh {(_b - _a) / _n:.3f})", style="italic")
_fig.tight_layout()

_text = (
    f"Riemann sum $R = {_R:.5f}$; integral $= {_exact:.5f}$; "
    f"error $R - \\int = {_R - _exact:+.5f}$."
)
mo.vstack([mo.hstack([riemann_fn, riemann_tag, riemann_n], justify="start"), graphic(_fig), mo.md(_text)])
```

### Which Functions Are Integrable?

Proving integrability from the definition requires knowing $I$ in advance. As with sequences, a Cauchy criterion avoids this.

:::{important icon=false} 📐 **Lemma (Cauchy Criterion for Integrals)**
A function $f: [a, b] \to \mathbb R$ is Riemann integrable if and only if for every $\varepsilon > 0$ there is $\delta > 0$ such that $|R(f, P, t) - R(f, P', t')| < \varepsilon$ for all tagged subdivisions $(P, t)$ and $(P', t')$ of $[a,b]$ with meshes below $\delta$.
:::

:::{admonition icon=false} ✍️ **Proof**
($\Rightarrow$) Take $\delta$ for $\varepsilon/2$ in the definition and use the triangle inequality.

($\Leftarrow$) For each $n \ge 1$, let $\delta_n$ be a $\delta$ that works for $\varepsilon = \frac1n$. Let $(P_n, t^{(n)})$ be a uniform subdivision with mesh below $\min(\delta_1, \ldots, \delta_n)$, tagged at the left endpoints, and let $r_n := R(f, P_n, t^{(n)})$. For $m \ge n$, both $P_m$ and $P_n$ have mesh below $\delta_n$, so $|r_m - r_n| < \frac1n$. Thus $(r_n)$ is a Cauchy sequence and converges to some $I$. Given $\varepsilon > 0$, choose $n$ with $\frac1n < \frac\varepsilon2$ and $|r_n - I| < \frac\varepsilon2$. Every tagged subdivision $(P, t)$ with mesh below $\delta_n$ satisfies $|R(f, P, t) - I| \le |R(f, P, t) - r_n| + |r_n - I| < \frac1n + \frac\varepsilon2 < \varepsilon$. $\blacksquare$
:::

:::{important icon=false} 📐 **Theorem (Continuous Functions Are Integrable)**
Every continuous function $f: [a, b] \to \mathbb R$ is Riemann integrable on $[a, b]$.
:::

:::{admonition icon=false} ✍️ **Proof**
Let $\varepsilon > 0$. By uniform continuity there is $\delta > 0$ with $|f(x) - f(x')| < \frac{\varepsilon}{2(b - a)}$ whenever $|x - x'| < \delta$. Let $(P, t)$ and $(P', t')$ be tagged subdivisions with meshes below $\delta$, and let $a = y_0 < y_1 < \cdots < y_m = b$ list the points of $P$ and $P'$ together. Each $[y_{j-1}, y_j]$ lies inside exactly one subinterval $[x_{i-1}, x_i]$ of $P$; let $\tau_j := t_i$ be that subinterval's tag. The pieces of $[x_{i-1}, x_i]$ have widths adding up to $\Delta x_i$, so $R(f, P, t) = \sum_j f(\tau_j)\,\Delta y_j$, and likewise $R(f, P', t') = \sum_j f(\tau'_j)\,\Delta y_j$. Both $\tau_j$ and $\tau'_j$ lie in a subinterval of width less than $\delta$ that contains $y_j$, so
$$|f(\tau_j) - f(\tau'_j)| \le |f(\tau_j) - f(y_j)| + |f(y_j) - f(\tau'_j)| < \frac{\varepsilon}{b - a}.$$
Hence $|R(f, P, t) - R(f, P', t')| < \sum_j \frac{\varepsilon}{b-a}\,\Delta y_j = \varepsilon$, and the Cauchy criterion applies. $\blacksquare$
:::

In particular $x^2$ is integrable on $[0,1]$, so the uniform right-endpoint sums computed above (whose meshes $\frac1n$ tend to $0$) converge to the integral: $\int_0^1 x^2\,dx = \frac13$.

:::{important icon=false} 📐 **Theorem (Properties of the Integral)**
Let $f, g: [a,b] \to \mathbb R$ be Riemann integrable and $c \in \mathbb R$.
1. *(Linearity)* $f + g$ and $cf$ are integrable, with $\int_a^b (f + g) = \int_a^b f + \int_a^b g$ and $\int_a^b cf = c\int_a^b f$.
2. *(Monotonicity)* If $f(x) \le g(x)$ for every $x$, then $\int_a^b f \le \int_a^b g$. In particular, constants $m \le f \le M$ give $m(b - a) \le \int_a^b f \le M(b - a)$.
3. If $|f|$ is also integrable (for example, if $f$ is continuous), then $\left|\int_a^b f\right| \le \int_a^b |f|$.
:::

:::{admonition icon=false} ✍️ **Proof**
1. Riemann sums are linear in the function: $R(f + g, P, t) = R(f, P, t) + R(g, P, t)$ and $R(cf, P, t) = c\,R(f, P, t)$. Use the smaller of the two $\delta$'s, as in the limit laws.
2. A constant function $m$ has every Riemann sum equal to $m(b - a)$, so $\int_a^b m = m(b-a)$. Suppose $\int f > \int g$ and let $\varepsilon := \frac12(\int f - \int g)$. A tagged subdivision with mesh below both $\delta$'s has $R(f, P, t) > \int f - \varepsilon = \int g + \varepsilon > R(g, P, t)$, contradicting $R(f, P, t) \le R(g, P, t)$, which holds term by term.
3. Apply part 2 to $-|f| \le f \le |f|$. $\blacksquare$
:::
  
### Splitting the Interval

:::{important icon=false} 📐 **Lemma (Integrable Functions Are Bounded)**
If $f$ is Riemann integrable on $[a, b]$, then $f$ is bounded on $[a, b]$.
:::

:::{admonition icon=false} ✍️ **Proof**
Take $\varepsilon = 1$ with its $\delta$, and fix a tagged subdivision $(P, t)$ with mesh below $\delta$. For any $i$ and any $s \in [x_{i-1}, x_i]$, replacing the tag $t_i$ by $s$ gives another admissible tagged subdivision whose Riemann sum differs by $(f(s) - f(t_i))\,\Delta x_i$. Both sums are within $1$ of the integral, so $|f(s) - f(t_i)|\,\Delta x_i < 2$, that is, $|f(s)| < |f(t_i)| + 2/\Delta x_i$. The largest of these finitely many bounds bounds $|f|$ on $[a, b]$. $\blacksquare$
:::

:::{important icon=false} 📐 **Lemma (Additivity over Intervals)**
Let $a < b < c$ and $f: [a, c] \to \mathbb R$. Then $f$ is integrable on $[a, c]$ if and only if it is integrable on $[a, b]$ and on $[b, c]$, and in that case
$$\int_a^c f(x)\,dx = \int_a^b f(x)\,dx + \int_b^c f(x)\,dx.$$
Consequently, if $f$ is integrable on every closed bounded subinterval of an interval $J$, this formula holds for all $a, b, c \in J$ in any order.
:::

:::{admonition icon=false} ✍️ **Proof**
($\Leftarrow$) Let $I_1$ and $I_2$ be the integrals over $[a, b]$ and $[b, c]$. By the previous lemma, $|f| \le M$ on $[a, c]$ for some $M > 0$. Given $\varepsilon > 0$, let $\delta_1, \delta_2$ work for $\varepsilon/3$ on the two pieces, and let $\delta := \min(\delta_1, \delta_2, \varepsilon/(6M))$. Let $(P, t)$ be a tagged subdivision of $[a, c]$ with mesh below $\delta$. If $b$ is one of its points, $(P, t)$ splits into tagged subdivisions of $[a, b]$ and $[b, c]$ with mesh below $\delta$, and its Riemann sum, the sum of theirs, is within $\frac{2\varepsilon}3$ of $I_1 + I_2$. Otherwise $b$ lies inside exactly one subinterval $[x_{j-1}, x_j]$. Inserting $b$ as a new point and tagging both new pieces with $b$ changes the Riemann sum by $(f(b) - f(t_j))\,\Delta x_j$, which has absolute value below $2M\delta \le \frac\varepsilon3$, and produces a tagged subdivision that splits as before. Either way, $|R(f, P, t) - (I_1 + I_2)| < \varepsilon$.

($\Rightarrow$) We check the Cauchy criterion on $[a, b]$ (the case $[b, c]$ is symmetric). Given $\varepsilon > 0$, let $\delta$ work for $\varepsilon/2$ on $[a, c]$, and fix a tagged subdivision $(Q, s)$ of $[b, c]$ with mesh below $\delta$. If $(P, t)$ and $(P', t')$ are tagged subdivisions of $[a, b]$ with meshes below $\delta$, appending $(Q, s)$ to each gives two tagged subdivisions of $[a, c]$ with meshes below $\delta$. Their Riemann sums are within $\frac\varepsilon2$ of the integral over $[a, c]$, so they differ by less than $\varepsilon$; and their difference is exactly $R(f, P, t) - R(f, P', t')$. The formula then follows from the first part.

For the last sentence: the cases with two equal points are trivial, and every other ordering reduces to $a < b < c$ by the convention $\int_q^p = -\int_p^q$ (for example, if $b < a < c$, then $\int_b^c = \int_b^a + \int_a^c$ rearranges to the claim). $\blacksquare$
:::

:::{important icon=false} 📐 **Lemma (Changing Finitely Many Values)**
If $f$ is integrable on $[a, b]$ and $g: [a, b] \to \mathbb R$ differs from $f$ at only finitely many points, then $g$ is integrable with the same integral.
:::

:::{admonition icon=false} ✍️ **Proof**
By induction it suffices to treat one point $p$, with $d := |g(p) - f(p)| > 0$. In a tagged subdivision, $p$ can be the tag of at most two subintervals (subintervals overlap only at endpoints), so $|R(g, P, t) - R(f, P, t)| \le 2d\,\operatorname{mesh}(P)$. If $\delta$ works for $f$ with $\varepsilon/2$, then $\min(\delta, \varepsilon/(4d))$ works for $g$ with $\varepsilon$. $\blacksquare$
:::

A function $f: [a,b] \to \mathbb R$ is **piecewise continuous** if there is a subdivision $a = c_0 < c_1 < \cdots < c_m = b$ such that, for each $j$, the restriction of $f$ to $(c_{j-1}, c_j)$ agrees there with some continuous function $g_j: [c_{j-1}, c_j] \to \mathbb R$. In other words, $f$ has finitely many jumps, and the one-sided limits exist at each of them. A density that is $1$ on $[0, 1]$ and $0$ elsewhere, viewed on $[-1, 2]$, is a typical example.

:::{important icon=false} 📐 **Corollary (Piecewise Continuous Functions Are Integrable)**
A piecewise continuous $f$ as above is integrable on $[a, b]$, and $\int_a^b f(x)\,dx = \sum_{j=1}^m \int_{c_{j-1}}^{c_j} g_j(x)\,dx$.
:::

:::{admonition icon=false} ✍️ **Proof**
On $[c_{j-1}, c_j]$, $f$ differs from the continuous (hence integrable) $g_j$ at most at the two endpoints, so it is integrable there with the same integral. Additivity, applied $m - 1$ times, finishes the proof. $\blacksquare$
:::

:::{important icon=false} 📐 **Lemma (Mean Value Theorem for Integrals)**
If $f: [a, b] \to \mathbb R$ is continuous, then $\int_a^b f(x)\,dx = f(c)\,(b - a)$ for some $c \in [a, b]$.
:::

:::{admonition icon=false} ✍️ **Proof**
By the Extreme Value Theorem, $f(c_1) \le f(x) \le f(c_2)$ for all $x$, for some $c_1, c_2 \in [a, b]$. By monotonicity, $y := \frac{1}{b - a}\int_a^b f$ lies in $[f(c_1), f(c_2)]$, and the intermediate value theorem on the closed interval between $c_1$ and $c_2$ gives a $c$ with $f(c) = y$. $\blacksquare$
:::

:::{caution icon=false} ⚠️ **Assumptions and Failure Modes**
- **Too many discontinuities.** Let $f(x) = 1$ for rational $x$ and $0$ for irrational $x$, on $[0, 1]$. Every subinterval contains rationals and irrationals[^irrationals], so for every subdivision, all-rational tags give Riemann sum $1$ and all-irrational tags give $0$. The Cauchy criterion fails, so $f$ is not Riemann integrable. The exact condition is [Lebesgue's criterion](https://en.wikipedia.org/wiki/Riemann_integral#Integrability): a bounded function is Riemann integrable if and only if its set of discontinuities has measure zero (it can be covered by countably many intervals of total length as small as we like). The [Lebesgue integral](https://en.wikipedia.org/wiki/Lebesgue_integral) integrates this $f$ (to $0$) and is the general tool of probability theory; Chapters 5 and 6 only need the Riemann integral.
- **Unbounded functions** are never Riemann integrable, by the boundedness lemma; $1/\sqrt x$ on $(0, 1]$ needs an *improper* integral.
- **Infinite intervals** are not covered by the definition; $\int_{-\infty}^\infty e^{-x^2/2}\,dx$ also needs an improper integral.
:::

:::{attention icon=false} 🗝️ **Key Idea**
The Riemann integral $\int_a^b f(x)\,dx$ is the limit of Riemann sums $\sum f(t_i)\,\Delta x_i$ as the mesh tends to $0$, uniformly over all choices of tags. Continuous and piecewise continuous functions are integrable, and the integral is linear, monotone, and additive over adjacent intervals.
:::

[^irrationals]: Chapter 3 shows every interval $(p, q)$ contains a rational. It also contains an irrational: pick a rational $r \in (p - \sqrt2, q - \sqrt2)$; then $r + \sqrt 2 \in (p, q)$, and it is irrational because $\sqrt2$ is ([Appendix B: Incompleteness of the Rationals](appendix_b_number_systems_v2.md)).
  
## The Fundamental Theorem of Calculus

An inertial sensor measures acceleration $a(t)$ and must recover velocity. If $v(0)$ is known, the velocity at time $t$ is the initial velocity plus the accumulated acceleration, $v(t) = v(0) + \int_0^t a(s)\,ds$, and differentiating this accumulated integral should give back the acceleration. The Fundamental Theorem of Calculus makes this precise: integration and differentiation undo each other. As a bonus, it replaces the page of algebra we needed for $\int_0^1 x^2\,dx$ with one line.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Antiderivative
: Let $J$ be an interval with more than one point and $f: J \to \mathbb R$. A function $F: J \to \mathbb R$ is an antiderivative of $f$ on $J$ if and only if $F$ is {term}`differentiable` on $J$ and $F'(x) = f(x)$ for every $x \in J$.
:::
::::

By the Monotonicity and Constant Functions corollary, two antiderivatives of the same $f$ on an interval differ by a constant. The *indefinite integral* notation $\int f(x)\,dx = F(x) + C$ expresses this: it stands for "$F$ is an antiderivative of $f$, and so is $F + C$ for every constant $C$, and these are all of them".

:::{important icon=false} 📐 **Theorem (Fundamental Theorem of Calculus, Part 1)**
Let $J$ be an interval with more than one point, $f: J \to \mathbb R$ continuous, and $c \in J$. Then
$$F(x) := \int_c^x f(s)\,ds \qquad (x \in J)$$
is an antiderivative of $f$ on $J$: $F'(x) = f(x)$ for every $x \in J$.
:::

:::{admonition icon=false} ✍️ **Proof**
$F$ is defined because $f$ is continuous, hence integrable, on every closed bounded subinterval of $J$. Let $x \in J$ and $\varepsilon > 0$. Continuity of $f$ at $x$ gives $\delta > 0$ with $|f(s) - f(x)| < \varepsilon$ for $s \in J$ with $|s - x| < \delta$. Let $h \ne 0$ with $x + h \in J$ and $|h| < \delta$. By additivity, $F(x + h) - F(x) = \int_x^{x+h} f(s)\,ds$, and $\int_x^{x+h} f(x)\,ds = f(x)\,h$ (the integral of a constant). Therefore, using parts 2 and 3 of Properties of the Integral on the interval between $x$ and $x + h$,
$$\left|\frac{F(x+h) - F(x)}{h} - f(x)\right| = \frac{1}{|h|}\left|\int_x^{x+h} \big(f(s) - f(x)\big)\,ds\right| \le \frac{1}{|h|}\,\varepsilon\,|h| = \varepsilon.$$
As $\varepsilon > 0$ was arbitrary, the difference quotient tends to $f(x)$. $\blacksquare$
:::

In particular, every continuous function on an interval has an antiderivative. Even without continuity, accumulated integrals are continuous:

:::{important icon=false} 📐 **Lemma (Integrals Are Continuous in Their Limits)**
Let $J$ be an interval, let $f$ be Riemann integrable on every closed bounded subinterval of $J$, and let $c \in J$. Then $F(x) := \int_c^x f(s)\,ds$ is continuous on $J$.
:::

:::{admonition icon=false} ✍️ **Proof**
Let $x \in J$ and $\varepsilon > 0$. Choose $\eta > 0$ smaller than the distance from $x$ to each endpoint of $J$ that does not belong to $J$; then $[p, q] := J \cap [x - \eta, x + \eta]$ is a closed bounded interval. By the boundedness lemma, $|f| \le M$ on $[p, q]$ for some $M > 0$. For $y \in J$ with $|y - x| < \min(\eta, \varepsilon/M)$, we have $y \in [p, q]$, and additivity and monotonicity give $|F(y) - F(x)| = \left|\int_x^y f\right| \le M|y - x| < \varepsilon$. $\blacksquare$
:::

:::{important icon=false} 📐 **Theorem (Fundamental Theorem of Calculus, Part 2)**
Let $a < b$, let $f: [a, b] \to \mathbb R$ be Riemann integrable, and let $F: [a, b] \to \mathbb R$ be continuous on $[a, b]$ and differentiable on $(a, b)$ with $F'(x) = f(x)$ for every $x \in (a, b)$. Then
$$\int_a^b f(x)\,dx = F(b) - F(a) =: \Big[F(x)\Big]_a^b.$$
:::

:::{admonition icon=false} ✍️ **Proof**
Let $\varepsilon > 0$ and take $\delta$ from the definition of the integral. Let $P$ be any subdivision with mesh below $\delta$. On each $[x_{i-1}, x_i]$, the Mean Value Theorem gives a $t_i \in (x_{i-1}, x_i)$ with $F(x_i) - F(x_{i-1}) = F'(t_i)\,\Delta x_i = f(t_i)\,\Delta x_i$. With these tags the Riemann sum telescopes:
$$R(f, P, t) = \sum_{i=1}^n \big(F(x_i) - F(x_{i-1})\big) = F(b) - F(a).$$
Hence $\left|F(b) - F(a) - \int_a^b f\right| < \varepsilon$ for every $\varepsilon > 0$, so the two numbers are equal. $\blacksquare$
:::

**Examples.** For $n \in \mathbb N$, $\frac{x^{n+1}}{n+1}$ is an antiderivative of $x^n$, so $\int_a^b x^n\,dx = \frac{b^{n+1} - a^{n+1}}{n+1}$. In particular $\int_0^1 x^2\,dx = \frac13$, without any sums of squares.

**Quantization noise.** A quantizer with step $\Delta$ (like the scale's $0.1$ lb display) makes a rounding error between $-\frac\Delta2$ and $\frac\Delta2$. If the error is spread evenly over that interval, its average square is
$$\frac{1}{\Delta}\int_{-\Delta/2}^{\Delta/2} x^2\,dx = \frac{1}{\Delta}\Big[\frac{x^3}{3}\Big]_{-\Delta/2}^{\Delta/2} = \frac{1}{\Delta}\Big(\frac{\Delta^3}{24} + \frac{\Delta^3}{24}\Big) = \frac{\Delta^2}{12}.$$
For $\Delta = 0.1$ lb this is about $0.00083$ lb², whose square root is about $0.029$ lb. [Chapter 9](ch9_noise_levels_v2.md) identifies this number as the {term}`variance` of quantization noise. (With $\Delta = 1$ it is the $\frac{1}{12}$ of the Riemann-sum figure.)
  
### Integration by Parts and Substitution

Each differentiation rule, read backwards through the Fundamental Theorem, becomes an integration rule. The product rule gives integration by parts, and the chain rule gives substitution.

:::{important icon=false} 📐 **Theorem (Integration by Parts)**
Let $f, g: [a, b] \to \mathbb R$ be continuously differentiable. Then
$$\int_a^b f(x)\,g'(x)\,dx = \Big[f(x)\,g(x)\Big]_a^b - \int_a^b f'(x)\,g(x)\,dx.$$
:::

:::{admonition icon=false} ✍️ **Proof**
By the product rule, $fg$ is an antiderivative of $f'g + fg'$, which is continuous and hence integrable. By Part 2, $\int_a^b (f'g + fg') = [fg]_a^b$. Since $f'g$ and $fg'$ are continuous, linearity splits the left side, and rearranging gives the claim. $\blacksquare$
:::

:::{important icon=false} 📐 **Theorem (Integration by Substitution)**
Let $\varphi: [a, b] \to \mathbb R$ be continuously differentiable, and let $f$ be continuous on an interval $J$ that contains $\varphi(t)$ for every $t \in [a, b]$. Then
$$\int_a^b f(\varphi(t))\,\varphi'(t)\,dt = \int_{\varphi(a)}^{\varphi(b)} f(x)\,dx.$$
:::

:::{admonition icon=false} ✍️ **Proof**
By Part 1, $F(y) := \int_{\varphi(a)}^y f(x)\,dx$ is an antiderivative of $f$ on $J$. By the chain rule, $(F \circ \varphi)'(t) = f(\varphi(t))\,\varphi'(t)$, which is continuous and hence integrable on $[a, b]$. By Part 2, the left side equals $F(\varphi(b)) - F(\varphi(a)) = \int_{\varphi(a)}^{\varphi(b)} f(x)\,dx$. $\blacksquare$
:::

In Leibniz notation, substitution is the bookkeeping rule "$x = \varphi(t)$, $dx = \varphi'(t)\,dt$, and the limits move with $x$". The most frequent case in this book is an affine change of scale: for $\mu \in \mathbb R$ and $\sigma > 0$, the substitution $x = \mu + \sigma u$ gives
$$\int_{s}^{t} f(\mu + \sigma u)\,\sigma\,du = \int_{\mu + \sigma s}^{\mu + \sigma t} f(x)\,dx,$$
which [Chapter 5](ch5_random_variables_v2.md) uses to reduce every normal density to the standard one.

:::{caution icon=false} ⚠️ **Assumptions and Failure Modes**
- **Part 1 needs continuity.** For the step function $f = 0$ on $[-1, 0]$ and $f = 1$ on $(0, 1]$, the accumulated integral is $F(x) = \int_{-1}^x f = \max(x, 0)$, which has a corner at $0$: $F'(0)$ does not exist.
- **Part 2 needs $F' = f$ at every point of $(a, b)$, and an integrable $f$.** $F(x) = -1/x$ has $F'(x) = 1/x^2 > 0$ for every $x \ne 0$, yet $F(1) - F(-1) = -2 < 0$. There is no contradiction: $F$ is undefined at $0$, and $1/x^2$ is unbounded on $[-1, 1]$, so it is not Riemann integrable there.
- **"$+ C$" is only valid on an interval**, for the reason given in the Mean Value Theorem section.
:::

:::{attention icon=false} 🗝️ **Key Idea**
Accumulating a continuous $f$ produces an antiderivative ($\frac{d}{dx}\int_c^x f = f$), and integrating a derivative recovers the net change ($\int_a^b F' = F(b) - F(a)$). Integrals are therefore computed by finding antiderivatives, and the product and chain rules become integration by parts and substitution.
:::
  
## Exponential and Logarithm

Many quantities change at a rate proportional to their own size: the voltage on a capacitor discharging through a resistor, the temperature difference between a sensor and its surroundings, or the influence of an old measurement on an EMA. In continuous time this is the differential equation $\dot y = a\,y$. The simplest case, $a = 1$ and $y(0) = 1$, asks for a function $E$ with $E' = E$ and $E(0) = 1$.

No polynomial works, because differentiating lowers the degree. So try an "infinite polynomial" $E(x) = \sum_n c_n x^n$ and differentiate it term by term (which we must justify): $\sum_n (n+1)\,c_{n+1}\,x^n = \sum_n c_n\,x^n$ suggests $c_{n+1} = \frac{c_n}{n+1}$, and $c_0 = E(0) = 1$ then forces $c_n = \frac{1}{n!}$. We take this guess as the definition and prove that it works.

:::{important icon=false} 📐 **Lemma (Differentiating a Power Series)**
Let $(c_n)$ be a sequence of real numbers such that $\sum_n |c_n|\,r^n$ converges for every $r \ge 0$. Then:
1. For every $x \in \mathbb R$ the series $\sum_n c_n x^n$ converges absolutely, so $f(x) := \sum_{n=0}^\infty c_n x^n$ defines a function $f: \mathbb R \to \mathbb R$.
2. The coefficients $c'_n := (n+1)\,c_{n+1}$ of the term-by-term derivative satisfy the same hypothesis.
3. $f$ is differentiable on $\mathbb R$, with $f'(x) = \sum_{n=1}^\infty n\,c_n\,x^{n-1} = \sum_{n=0}^\infty c'_n\,x^n$.
:::

:::{admonition icon=false} ✍️ **Proof**
1. $|c_n x^n| = |c_n|\,|x|^n$; use the hypothesis with $r = |x|$.
2. By induction, $n \le 2^n$ and $n(n-1) \le 2^n$ for every $n \in \mathbb N$. (For the second, check $n \le 3$ directly; for $n \ge 3$, $(n+1)n = n(n-1)\cdot\frac{n+1}{n-1} \le 2^n \cdot 2$.) For $r > 0$, $n\,r^{n-1} = \frac{n\,r^n}{r} \le \frac{(2r)^n}{r}$, so $\sum_n |c'_n|\,r^n = \sum_{n \ge 1} n\,|c_n|\,r^{n-1} \le \frac1r\sum_n |c_n|\,(2r)^n < \infty$ by comparison. The case $r = 0$ is trivial.
3. Fix $x$, let $0 < |h| \le 1$, and let $\rho := |x| + 1$. For $n \ge 2$, Taylor's Theorem with degree $1$, applied to the polynomial $t \mapsto t^n$ at $x$, gives $(x + h)^n = x^n + n x^{n-1} h + \frac12 n(n-1)\,\xi^{n-2} h^2$ for some $\xi$ between $x$ and $x + h$, so $|\xi| \le \rho$ and
$$\left|\frac{(x+h)^n - x^n}{h} - n x^{n-1}\right| \le \tfrac12 n(n-1)\,\rho^{n-2}\,|h|.$$
This also holds for $n = 0, 1$, where the left side is $0$. By linearity of series and $\left|\sum a_n\right| \le \sum|a_n|$,
$$\left|\frac{f(x+h) - f(x)}{h} - \sum_{n\ge1} n\,c_n\,x^{n-1}\right| = \left|\sum_n c_n\Big[\frac{(x+h)^n - x^n}{h} - n x^{n-1}\Big]\right| \le \frac{|h|}{2}\sum_{n \ge 2} n(n-1)\,|c_n|\,\rho^{n-2}.$$
The last series is $\sum_n |c''_n|\,\rho^n$ for the coefficients $c''$ of the twice term-by-term differentiated series, so it converges by part 2 applied twice. The right side is therefore a constant times $|h|$, which tends to $0$ as $h \to 0$. $\blacksquare$
:::

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Exponential function
: The exponential function $\exp: \mathbb R \to \mathbb R$ is defined by the power series
  $$\exp(x) := \sum_{n=0}^\infty \frac{x^n}{n!} = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots,$$
  which converges absolutely for every real $x$ (Series: the exponential series example).
:::
::::
  
:::{important icon=false} 📐 **Theorem (Properties of the Exponential Function)**
1. $\exp$ is differentiable, with $\exp' = \exp$ and $\exp(0) = 1$.
2. $\exp(x)\exp(-x) = 1$ for every $x$; in particular $\exp(x) \ne 0$.
3. $\exp(a + b) = \exp(a)\exp(b)$ for all $a, b \in \mathbb R$.
4. $\exp(x) > 0$ for every $x$.
5. $\exp$ is strictly increasing, $\exp(x) \ge 1 + x$ for $x \ge 0$, $\lim_{x\to\infty}\exp(x) = \infty$, and $\lim_{x \to -\infty}\exp(x) = 0$.
6. $\exp$ is a bijection from $\mathbb R$ onto $(0, \infty)$.
7. *(Uniqueness)* Let $J$ be an interval with more than one point, $t_0 \in J$, and $a, c \in \mathbb R$. The only differentiable $y: J \to \mathbb R$ with $y'(t) = a\,y(t)$ for every $t \in J$ and $y(t_0) = c$ is $y(t) = c\exp\big(a(t - t_0)\big)$.
:::

:::{admonition icon=false} ✍️ **Proof**
1. The coefficients $\frac{1}{n!}$ satisfy the lemma's hypothesis (the exponential series converges absolutely at $x = r$). By the lemma, $\exp'(x) = \sum_{n \ge 1} \frac{n\,x^{n-1}}{n!} = \sum_{n\ge1}\frac{x^{n-1}}{(n-1)!} = \exp(x)$. Every term with $n \ge 1$ vanishes at $0$, so $\exp(0) = 1$.
2. Let $g(x) := \exp(x)\exp(-x)$. By the product and chain rules, $g'(x) = \exp(x)\exp(-x) - \exp(x)\exp(-x) = 0$, so $g$ is constant on $\mathbb R$ and equals $g(0) = 1$.
3. Fix $b$ and let $h(x) := \exp(x + b)\exp(-x)$. As in part 2, $h' = 0$, so $h(x) = h(0) = \exp(b)$. Multiplying by $\exp(x)$ and using part 2 gives $\exp(x + b) = \exp(x)\exp(b)$.
4. By part 3, $\exp(x) = \exp(x/2)^2 \ge 0$, and $\exp(x) \ne 0$ by part 2.
5. $\exp' = \exp > 0$, so $\exp$ is strictly increasing. For $x \ge 0$ every term of the series is nonnegative, so $\exp(x)$ is at least the partial sum $1 + x$; hence $\exp(x) > M$ whenever $x > M \ge 0$. For $x > 0$, part 2 gives $0 < \exp(-x) = \frac{1}{\exp(x)} \le \frac{1}{1+x} < \frac1x$, so $\exp(-x) \to 0$ as $x \to \infty$.
6. $\exp$ is injective by part 5 and takes values in $(0, \infty)$ by part 4. Given $y > 0$, part 5 provides $p < q$ with $\exp(p) < y < \exp(q)$. Since $\exp$ is continuous (it is differentiable), the intermediate value theorem on $[p, q]$ gives an $x$ with $\exp(x) = y$.
7. That this $y$ works follows from the chain rule. Conversely, let $y$ be any such function and $u(t) := y(t)\exp\big(-a(t - t_0)\big)$. Then $u'(t) = y'(t)\exp(\cdots) - a\,y(t)\exp(\cdots) = 0$, so $u$ is constant on the interval $J$ and equals $u(t_0) = c$. Multiplying by $\exp\big(a(t - t_0)\big)$ and using part 2 gives $y(t) = c\exp\big(a(t - t_0)\big)$. $\blacksquare$
:::

**The number $e$ and the notation $e^x$.** Let $e := \exp(1) = \sum_n \frac{1}{n!} \approx 2.718281828$. By part 3 and induction, $\exp(nx) = \exp(x)^n$ for $n \in \mathbb N$, so $\exp(n) = e^n$ and $\exp(-n) = e^{-n}$. For a rational number $p/q$ with $q \in \mathbb N^+$, $\exp(p/q)^q = \exp(p) = e^p$, so $\exp(p/q)$ is the unique positive $q$-th root of $e^p$, which is what $e^{p/q}$ means. Thus $\exp$ extends the powers of $e$ from rational to real exponents, and we write $e^x := \exp(x)$ for every real $x$.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Natural logarithm
: The natural logarithm $\ln: (0, \infty) \to \mathbb R$ is the {term}`inverse function` of the bijection $\exp: \mathbb R \to (0, \infty)$. That is, for $y > 0$, $\ln y$ is the unique real number $x$ with $e^x = y$.
:::
::::

:::{important icon=false} 📐 **Theorem (Properties of the Natural Logarithm)**
1. $\ln 1 = 0$, $\ln e = 1$, $\ln(yz) = \ln y + \ln z$, and $\ln(1/y) = -\ln y$ for all $y, z > 0$.
2. $\ln$ is strictly increasing, continuous, and differentiable, with $\frac{d}{dy}\ln y = \frac1y$.
3. $\lim_{y\to\infty} \ln y = \infty$ and $\lim_{y \to 0^+}\ln y = -\infty$.
4. $\ln x = \int_1^x \frac{dt}{t}$ for every $x > 0$.
:::

:::{admonition icon=false} ✍️ **Proof**
1. $e^0 = 1$ and $e^1 = e$. Also $e^{\ln y + \ln z} = e^{\ln y}\,e^{\ln z} = yz$, so $\ln(yz) = \ln y + \ln z$; with $z = 1/y$ this gives $\ln y + \ln(1/y) = \ln 1 = 0$.
2. $\exp$ is a strictly increasing bijection between the intervals $\mathbb R$ and $(0, \infty)$, so $\ln$ is strictly increasing and continuous by the Continuous Inverse lemma. Since $\exp'(x) = e^x \ne 0$, the Derivative of an Inverse Function theorem gives $\ln'(y) = \frac{1}{\exp'(\ln y)} = \frac{1}{e^{\ln y}} = \frac1y$.
3. Given $M$, every $y > e^M$ has $\ln y > M$, and every $y \in (0, e^{-M})$ has $\ln y < -M$, because $\ln$ is increasing.
4. By part 2, $\ln$ is an antiderivative of $t \mapsto 1/t$ on $(0, \infty)$; apply Part 2 of the Fundamental Theorem on the interval between $1$ and $x$ (with the convention for reversed limits if $x < 1$). $\blacksquare$
:::

**Real powers.** For $a > 0$ and $x \in \mathbb R$, define $a^x := e^{x\ln a}$. For integer $x$ this agrees with repeated multiplication, since $e^{n\ln a} = (e^{\ln a})^n = a^n$, and the rules $a^{x+y} = a^x a^y$, $(a^x)^y = a^{xy}$, and $(ab)^x = a^x b^x$ follow from the properties of $\exp$ and $\ln$. By the chain rule, $\frac{d}{dx}a^x = (\ln a)\,a^x$, and for $x > 0$ and every real $r$, $\frac{d}{dx}x^r = \frac{d}{dx}e^{r\ln x} = e^{r\ln x}\cdot\frac rx = r\,x^{r-1}$. For example, $\sqrt x = x^{1/2}$ has derivative $\frac12 x^{-1/2}$, as found earlier.

**Why the EMA is "exponential".** For $0 < \alpha < 1$ let $\lambda := -\ln(1 - \alpha) > 0$. Then the weight of a measurement $n$ steps old is $\alpha(1 - \alpha)^n = \alpha\,e^{-\lambda n}$: it decays exponentially with age, halving every $\ln 2/\lambda$ steps. Taylor's Theorem with degree $1$ for $\ln(1 - \alpha)$ at $0$ (whose derivatives are $-\frac{1}{1-\alpha}$ and $-\frac{1}{(1-\alpha)^2}$) gives $\lambda = \alpha + \frac{\alpha^2}{2(1-\xi)^2}$ for some $\xi \in (0, \alpha)$, so $\lambda \approx \alpha$ for small $\alpha$ and the half-life is about $0.69/\alpha$ steps. With $\alpha = 0.05$ at 10 samples per second, a measurement's weight halves about every 13.5 samples, or 1.35 s.
  
### Sine and Cosine

Sine and cosine can be defined by power series in the same way. For every real $x$, let
$$\sin x := \sum_{n=0}^\infty (-1)^n\frac{x^{2n+1}}{(2n+1)!} = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \cdots, \qquad \cos x := \sum_{n=0}^\infty (-1)^n \frac{x^{2n}}{(2n)!} = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \cdots.$$
Written as $\sum_k c_k x^k$, each has $|c_k| \le \frac{1}{k!}$, so by comparison with the exponential series both satisfy the hypothesis of the Differentiating a Power Series lemma.

:::{important icon=false} 📐 **Theorem (Properties of Sine and Cosine)**
1. $\sin$ and $\cos$ are differentiable, with $\sin' = \cos$ and $\cos' = -\sin$; also $\sin 0 = 0$ and $\cos 0 = 1$.
2. $\sin(-x) = -\sin x$ and $\cos(-x) = \cos x$.
3. $\sin^2 x + \cos^2 x = 1$ for every $x$; consequently $|\sin x| \le 1$ and $|\cos x| \le 1$.
:::

:::{admonition icon=false} ✍️ **Proof**
1. By the lemma, $\sin'(x) = \sum_n (-1)^n \frac{(2n+1)x^{2n}}{(2n+1)!} = \sum_n (-1)^n\frac{x^{2n}}{(2n)!} = \cos x$, and $\cos'(x) = \sum_{n\ge1}(-1)^n\frac{x^{2n-1}}{(2n-1)!} = -\sum_{m \ge 0}(-1)^m\frac{x^{2m+1}}{(2m+1)!} = -\sin x$, with $m = n - 1$. The values at $0$ are the constant terms.
2. $(-x)^{2n+1} = -x^{2n+1}$ and $(-x)^{2n} = x^{2n}$, term by term.
3. $\frac{d}{dx}\big(\sin^2 x + \cos^2 x\big) = 2\sin x\cos x - 2\cos x \sin x = 0$, so $\sin^2 + \cos^2$ is constant and equals its value $0 + 1$ at $0$. Then $\sin^2 x \le 1$, so $|\sin x| \le 1$, and likewise for $\cos$. $\blacksquare$
:::

The remaining facts of trigonometry also follow from the series, and we cite them: $\cos$ has a smallest positive zero, and $\pi$ is defined as twice that zero; $\sin$ and $\cos$ have period $2\pi$; and $\theta \mapsto (\cos\theta, \sin\theta)$ maps $[0, 2\pi)$ bijectively onto the unit circle $\{(x, y) : x^2 + y^2 = 1\}$, with $\theta$ equal to the arc length from $(1, 0)$. So these series are the familiar sine and cosine, with angles in radians. Proofs are in Rudin (1976), *Principles of Mathematical Analysis*, Chapter 8, and summarized in [Wikipedia: Trigonometric functions](https://en.wikipedia.org/wiki/Trigonometric_functions).

**The small-angle approximation.** Since $\sin''(0) = -\sin 0 = 0$, the degree-$2$ Taylor polynomial of $\sin$ at $0$ is just $x$, and the error bound (with $|\sin'''| = |\cos| \le 1$) gives
$$|\sin x - x| \le \frac{|x|^3}{6}.$$
At $10^\circ \approx 0.1745$ rad the error is at most $0.00089$, about $0.5\%$ of $\sin x$. The pendulum of [Chapter 15](ch15_extended_kalman_filter_v2.md) and the small rotations of [Chapter 17](ch17_rotations_v2.md) rely on this approximation.

### Taylor Polynomials in Action

For $\exp$, $\sin$, and $\cos$, the Taylor polynomials at $0$ are exactly the partial sums of the defining series, so they converge to the function at every $x$. The error bound confirms it: every derivative of $\sin$ and $\cos$ is bounded by $1$, and every derivative of $\exp$ on $[-r, r]$ by $e^r$, so the error at $|x| \le r$ is at most $e^r\frac{r^{n+1}}{(n+1)!}$, which tends to $0$ by the term test applied to the exponential series. For $\ln(1 + x)$, the derivatives $\frac{(-1)^{k-1}(k-1)!}{(1+x)^k}$ give $T_{n,0}(x) = x - \frac{x^2}{2} + \frac{x^3}{3} - \cdots \pm \frac{x^n}{n}$, which converge only for $-1 < x \le 1$. Move the slider to watch the polynomials hug each function near $0$ and peel away far from it.

```{marimo} python
:hide-code: true

taylor_fn = mo.ui.dropdown(
    options={
        "exp(x)": "exp",
        "sin(x)": "sin",
        "cos(x)": "cos",
        "ln(1 + x)": "log1p",
        "1/(1 − x)": "geom",
    },
    value="sin(x)",
    label="function",
)
taylor_deg = mo.ui.slider(start=0, stop=15, step=1, value=3, label="degree $n$")
```

```{marimo} python
:hide-code: true

_n = taylor_deg.value
_kind = taylor_fn.value
_ks = range(_n + 1)
_boundary = None
if _kind == "exp":
    _coef = [1 / factorial(k) for k in _ks]
    _f, _xlim, _ylim, _name = np.exp, (-4.0, 4.0), (-10, 55), r"$e^x$"
elif _kind == "sin":
    _coef = [0.0 if k % 2 == 0 else (-1) ** ((k - 1) // 2) / factorial(k) for k in _ks]
    _f, _xlim, _ylim, _name = np.sin, (-2 * np.pi, 2 * np.pi), (-3, 3), r"$\sin x$"
elif _kind == "cos":
    _coef = [(-1) ** (k // 2) / factorial(k) if k % 2 == 0 else 0.0 for k in _ks]
    _f, _xlim, _ylim, _name = np.cos, (-2 * np.pi, 2 * np.pi), (-3, 3), r"$\cos x$"
elif _kind == "log1p":
    _coef = [0.0] + [(-1) ** (k - 1) / k for k in _ks if k >= 1]
    _f, _xlim, _ylim, _name = np.log1p, (-0.95, 3.0), (-3, 3), r"$\ln(1+x)$"
    _boundary = 1.0
else:
    _coef = [1.0 for _k in _ks]
    _f, _xlim, _ylim, _name = (lambda x: 1 / (1 - x)), (-2.5, 0.9), (-3, 10), r"$1/(1-x)$"
    _boundary = -1.0

_x = np.linspace(_xlim[0], _xlim[1], 800)
_T = np.polynomial.polynomial.polyval(_x, _coef)
_near = np.abs(_x) <= 0.5
_err_near = float(np.max(np.abs(_f(_x[_near]) - _T[_near])))
_err_all = float(np.max(np.abs(_f(_x) - _T)))

_fig, _ax = plt.subplots(figsize=(7, 3.6))
_ax.plot(_x, _f(_x), color="black", linewidth=1.5, label=_name)
_ax.plot(_x, _T, color="C1", linewidth=1.5, linestyle="--", label=f"Taylor polynomial, degree {_n}")
_ax.axvspan(-0.5, 0.5, color="C1", alpha=0.1, label=r"$|x| \leq 0.5$")
if _boundary is not None:
    _ax.axvline(_boundary, color="red", linestyle=":", label="edge of convergence")
_ax.set_xlim(*_xlim)
_ax.set_ylim(*_ylim)
_ax.set_xlabel("$x$")
_ax.set_ylabel("value")
_ax.grid(visible=True, alpha=0.9, linewidth=0.4)
_ax.legend(loc="upper left", fontsize=8)
_ax.set_title(f"Taylor polynomial of {_name} at 0, degree {_n}", style="italic")
_fig.tight_layout()

_text = (
    f"Largest error for $|x| \\le 0.5$: ${_err_near:.2e}$. "
    f"Largest error over the plotted range: ${_err_all:.2e}$."
)
mo.vstack([mo.hstack([taylor_fn, taylor_deg], justify="start"), graphic(_fig), mo.md(_text)])
```

:::{caution icon=false} ⚠️ **Assumptions and Failure Modes**
- **Taylor series need not converge.** For $x > 1$, the terms $\frac{x^n}{n}$ of the series for $\ln(1 + x)$ satisfy $\frac{x^n}{n} \ge x - 1 > 0$ (by Bernoulli's inequality $x^n \ge 1 + n(x-1)$), so they do not tend to $0$ and the polynomials diverge, although $\ln(1+x)$ is perfectly well behaved there.
- **Infinitely many derivatives are not enough.** The function equal to $e^{-1/x^2}$ for $x \ne 0$ and $0$ at $x = 0$ has derivatives of every order, all equal to $0$ at $x = 0$ ([Wikipedia: Non-analytic smooth function](https://en.wikipedia.org/wiki/Non-analytic_smooth_function)). Every Taylor polynomial at $0$ is therefore the zero polynomial, although the function is positive everywhere except $0$.
- **Real powers need a positive base.** $a^x$ is defined only for $a > 0$; for example, $(-1)^{1/2}$ is not a real number.
- **Floating-point limits.** In double precision, $e^x$ overflows for $x$ above about $709.8$, and $e^{-x^2/2}$ underflows to exactly $0$ for $|x|$ above about $38.6$. Products of many small likelihoods should be computed as sums of their logarithms.
:::

:::{attention icon=false} 🗝️ **Key Idea**
The exponential function $e^x = \sum_n \frac{x^n}{n!}$ is the unique solution of $y' = y$ with $y(0) = 1$. It turns sums into products ($e^{a+b} = e^a e^b$), it is a bijection from $\mathbb R$ onto $(0, \infty)$, and its inverse is the natural logarithm, with $\frac{d}{dy}\ln y = \frac1y$. Every solution of $\dot y = ay$ is $y(t) = y(t_0)\,e^{a(t - t_0)}$, and the EMA's weights $\alpha(1-\alpha)^n = \alpha e^{-\lambda n}$ decay exponentially.
:::
  
## Improper Integrals

An analog low-pass filter with time constant $\tau > 0$ gives an input from $t$ seconds ago the weight $\frac1\tau e^{-t/\tau}$ (Linear Differential Equations derives this). Like the EMA's weights, these weights should add up to $1$, but "adding up" now means integrating over the unbounded interval $[0, \infty)$, which the Riemann integral does not cover. Likewise, the normal density lives on all of $\mathbb R$. We extend the integral by one more limit.

A function $f$ is **locally integrable** on an interval $(a, b)$ if it is Riemann integrable on every closed bounded interval $[s, t] \subseteq (a, b)$. Continuous functions, and functions that are piecewise continuous on every such $[s,t]$, are locally integrable.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Improper integral
: Let $-\infty \le a < b \le \infty$, and let $f$ be a real-valued function that is defined at least on $(a, b)$ and is Riemann integrable on every closed bounded interval $[s, t] \subseteq (a, b)$. Fix $c \in (a, b)$. The improper integral $\int_a^b f(x)\,dx$ converges if and only if both limits
  $$\lim_{s \to a^+} \int_s^c f(x)\,dx \qquad\text{and}\qquad \lim_{t \to b^-}\int_c^t f(x)\,dx$$
  exist as real numbers, where $s \to a^+$ means $s \to -\infty$ if $a = -\infty$, and $t \to b^-$ means $t \to \infty$ if $b = \infty$. Its value is then the sum of the two limits. Otherwise the improper integral diverges.
:::
::::

The choice of $c$ does not matter: replacing $c$ by $c'$ changes the two integrals by $+\int_c^{c'} f$ and $-\int_c^{c'} f$ (additivity), so the limits exist for $c'$ exactly when they exist for $c$, and their sum is the same. Nor does the notation clash with the ordinary integral: if $a$ is finite and $f$ is Riemann integrable on $[a, c]$, then $f$ is bounded there, say by $M$, and $\left|\int_s^c f - \int_a^c f\right| = \left|\int_a^s f\right| \le M(s - a) \to 0$; the same holds at $b$. When only one endpoint is a problem, we simply write, for example, $\int_a^\infty f(x)\,dx = \lim_{t\to\infty}\int_a^t f(x)\,dx$. If $\lim_{s\to a^+}\int_s^c f$ exists, then $x \mapsto \int_a^x f(s)\,ds := \lim_{s\to a^+}\int_s^c f + \int_c^x f$ is continuous on $(a, b)$, by the lemma Integrals Are Continuous in Their Limits; [Chapter 5](ch5_random_variables_v2.md) uses this for cumulative distribution functions $\int_{-\infty}^x f$.

For **nonnegative** $f$, the integral $\int_c^t f$ increases with $t$ and $\int_s^c f$ increases as $s$ decreases. The next lemma shows that such limits always exist in $(-\infty, \infty]$, so for $f \ge 0$ we may write $\int_a^b f(x)\,dx = \infty$ when the improper integral diverges.

:::{important icon=false} 📐 **Lemma (Monotone Functions Have One-Sided Limits)**
Let $c < b \le \infty$ and let $F: [c, b) \to \mathbb R$ be increasing. If $F$ is bounded above, then $\lim_{t \to b^-} F(t) = \sup\{F(t) : c \le t < b\}$; otherwise $\lim_{t\to b^-}F(t) = \infty$.
:::

:::{admonition icon=false} ✍️ **Proof**
This is the proof of Monotone Convergence with $t$ in place of $n$. If $S$ is the supremum and $\varepsilon > 0$, some $t_0$ has $F(t_0) > S - \varepsilon$, and every $t \in (t_0, b)$ has $S - \varepsilon < F(t_0) \le F(t) \le S$. If $F$ is unbounded and $M \in \mathbb R$, some $t_0$ has $F(t_0) > M$, and then $F(t) > M$ for all $t \in (t_0, b)$. $\blacksquare$
:::

**Examples.**

1. *Exponential weights.* $\int_0^t \frac1\tau e^{-s/\tau}\,ds = \big[-e^{-s/\tau}\big]_0^t = 1 - e^{-t/\tau} \to 1$ as $t \to \infty$, so $\int_0^\infty \frac1\tau e^{-s/\tau}\,ds = 1$. The analog filter's weights add up to $1$, just like the EMA's.
2. *Power tails.* For $p \ne 1$, $\int_1^t x^{-p}\,dx = \frac{t^{1-p} - 1}{1 - p}$, which tends to $\frac{1}{p-1}$ if $p > 1$ and to $\infty$ if $p < 1$ (because $t^{1-p} = e^{(1-p)\ln t}$). For $p = 1$, $\int_1^t \frac{dx}{x} = \ln t \to \infty$. So $\int_1^\infty x^{-p}\,dx$ converges if and only if $p > 1$, mirroring the series $\sum \frac{1}{n^2}$ and $\sum \frac1n$.
3. *Unbounded integrands.* $\int_0^1 x^{-1/2}\,dx = \lim_{s\to0^+}\big[2\sqrt x\big]_s^1 = 2$: the integrand is unbounded near $0$, but the area is finite. By contrast, $\int_s^1 \frac{dx}{x} = -\ln s \to \infty$ as $s \to 0^+$.

:::{important icon=false} 📐 **Theorem (Comparison Test for Integrals)**
Let $f$ and $g$ be locally integrable on $(a, b)$ with $0 \le f(x) \le g(x)$ for every $x \in (a, b)$. Then $\int_a^b f \le \int_a^b g$ in $[0, \infty]$. In particular, if $\int_a^b g$ converges, so does $\int_a^b f$.
:::

:::{admonition icon=false} ✍️ **Proof**
For $c \le t < b$, monotonicity gives $\int_c^t f \le \int_c^t g \le \lim_{t' \to b^-}\int_c^{t'} g$, since $\int_c^{t'} g$ increases with $t'$. By the lemma, $\lim_{t\to b^-}\int_c^t f$ exists in $[0, \infty]$ and is at most the corresponding limit for $g$. The same argument applies at $a$, and adding the two pieces gives the claim. $\blacksquare$
:::

:::{important icon=false} 📐 **Theorem (Absolute Convergence of Integrals)**
Let $f$ and $|f|$ be locally integrable on $(a, b)$ (for example, $f$ piecewise continuous on every closed bounded subinterval). If $\int_a^b |f(x)|\,dx$ converges, then $\int_a^b f(x)\,dx$ converges and $\left|\int_a^b f\right| \le \int_a^b |f|$.
:::

:::{admonition icon=false} ✍️ **Proof**
Let $f^\pm := \frac12(|f| \pm f)$. These are locally integrable by linearity, and $0 \le f^\pm \le |f|$, so $\int_a^b f^+$ and $\int_a^b f^-$ converge by comparison. Since $f = f^+ - f^-$, the limit laws show that $\int_a^b f$ converges, with value $\int_a^b f^+ - \int_a^b f^-$. Finally, $\left|\int_s^t f\right| \le \int_s^t |f|$ for every $[s, t] \subseteq (a, b)$, and the order law carries this inequality to the limits. $\blacksquare$
:::

:::{important icon=false} 📐 **Corollary (Gaussian Moments Converge)**
For every $n \in \mathbb N$, the improper integral $\int_{-\infty}^{\infty} |x|^n e^{-x^2/2}\,dx$ converges. In particular (with $n = 0$), $\int_{-\infty}^\infty e^{-x^2/2}\,dx$ converges.
:::

:::{admonition icon=false} ✍️ **Proof**
Choose $m \in \mathbb N$ with $2m \ge n$. For $x \ge 0$, $e^{x^2/4} \ge \frac{(x^2/4)^m}{m!}$, because the right side is one term of a series with nonnegative terms whose sum is the left side; so $x^{2m} \le 4^m m!\,e^{x^2/4}$. Also $x^n \le 1 + x^{2m}$ (check $x \le 1$ and $x \ge 1$ separately) and $1 \le e^{x^2/4}$, so $x^n \le C e^{x^2/4}$ with $C := 1 + 4^m m!$. Finally $(x - 2)^2 \ge 0$ gives $\frac{x^2}{4} \ge x - 1$. Altogether, for $x \ge 0$,
$$0 \le x^n e^{-x^2/2} \le C e^{-x^2/4} \le C e^{1 - x},$$
and $\int_0^\infty C e^{1 - x}\,dx = Ce$ converges by Example 1. By comparison, $\int_0^\infty x^n e^{-x^2/2}\,dx$ converges. The substitution $x = -u$ shows that $\int_{-t}^0 |x|^n e^{-x^2/2}\,dx = \int_0^t u^n e^{-u^2/2}\,du$ for every $t > 0$, so the left tail converges too. $\blacksquare$
:::

The value of $\int_{-\infty}^\infty e^{-x^2/2}\,dx$ is computed in Multiple Integrals.

:::{caution icon=false} ⚠️ **Assumptions and Failure Modes**
- **Both tails must converge separately.** $\int_{-t}^t x\,dx = 0$ for every $t$, yet $\int_{-\infty}^\infty x\,dx$ diverges because $\int_0^t x\,dx = t^2/2 \to \infty$. The same happens for the Cauchy density $\frac{1}{\pi(1 + x^2)}$: by the substitution $u = 1 + x^2$, $\int_0^t \frac{x}{1 + x^2}\,dx = \frac12\ln(1 + t^2) \to \infty$, so $\int |x|/(\pi(1 + x^2))\,dx$ diverges, which is why the Cauchy distribution has no mean ([Chapter 6](ch6_expectation_and_variance_v2.md)).
- **A convergent integral does not force $f(x) \to 0$**, unlike the term test for series. A continuous function made of triangular spikes, one of height $1$ and base width $2/n^2$ centered at each integer $n \ge 2$ and $0$ elsewhere, has $\int_0^\infty f = \sum_{n\ge2}\frac{1}{n^2} < \infty$, but $f(n) = 1$ for every such $n$.
- **Comparison needs nonnegative integrands**, as for series.
:::

:::{attention icon=false} 🗝️ **Key Idea**
An improper integral is a limit of ordinary integrals over growing bounded intervals, taken separately at each problematic endpoint. For nonnegative integrands it always exists in $[0, \infty]$, and comparison with a known convergent integral, such as $\int_0^\infty e^{-x}\,dx$, proves convergence. In particular, all the integrals $\int |x|^n e^{-x^2/2}\,dx$ needed for the normal distribution converge.
:::
  
## Functions of Several Variables

The pendulum of [Chapter 15](ch15_extended_kalman_filter_v2.md) has length $L = 1$ m, and its sensor measures the horizontal position of the bob, $h(\theta) = L\sin\theta$, where $\theta$ is the angle from vertical. A Kalman filter needs a *linear* measurement function, so the extended Kalman filter replaces $h$ near its current estimate $\theta_0$ by the tangent line:

$$L\sin\theta \approx L\sin\theta_0 + L\cos\theta_0\,(\theta - \theta_0).$$

How good is this? By the Taylor Error Bound with degree $1$ and $|\sin''| = |\sin| \le 1$, the error is at most $L\,\frac{(\theta - \theta_0)^2}{2}$, whatever $\theta_0$ is. The figure shows the tangent line and the actual error over a window $|\theta - \theta_0| \le w$. For comparison, the pendulum's position sensor has noise of typical size $0.05$ m (its {term}`standard deviation`, defined in [Chapter 6](ch6_expectation_and_variance_v2.md)): when the filter's uncertainty in $\theta$ is small, the approximation error is far below the sensor noise, and when it is large, it is not.

```{marimo} python
:hide-code: true

lin_theta0 = mo.ui.slider(
    start=-3.0, stop=3.0, step=0.05, value=0.5, label=r"operating point $\theta_0$ (rad)"
)
lin_width = mo.ui.slider(start=0.05, stop=1.5, step=0.05, value=0.5, label=r"half-width $w$ (rad)")
```

```{marimo} python
:hide-code: true

_t0 = lin_theta0.value
_w = lin_width.value
_th = np.linspace(-np.pi, np.pi, 600)
_tangent = np.sin(_t0) + np.cos(_t0) * (_th - _t0)
_win = np.linspace(_t0 - _w, _t0 + _w, 400)
_err = np.abs(np.sin(_win) - (np.sin(_t0) + np.cos(_t0) * (_win - _t0)))

_fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(9, 3.6))
_ax1.plot(_th, np.sin(_th), color="black", linewidth=1.5, label=r"$L\sin\theta$")
_ax1.plot(_th, _tangent, color="C1", linestyle="--", label="tangent line")
_ax1.axvspan(_t0 - _w, _t0 + _w, color="C1", alpha=0.2, label=r"$|\theta - \theta_0| \leq w$")
_ax1.plot([_t0], [np.sin(_t0)], "o", color="C0")
_ax1.set_xlim(-np.pi, np.pi)
_ax1.set_ylim(-2, 2)
_ax1.set_xlabel(r"angle $\theta$ (rad)")
_ax1.set_ylabel("horizontal position (m)")
_ax1.grid(visible=True, alpha=0.9, linewidth=0.4)
_ax1.legend(loc="lower right", fontsize=8)
_ax1.set_title(r"Tangent line at $\theta_0$", style="italic")

_ax2.plot(_win - _t0, _err, color="C0", label="actual error")
_ax2.plot(_win - _t0, (_win - _t0) ** 2 / 2, color="red", linestyle=":", label=r"bound $(\theta - \theta_0)^2/2$")
_ax2.axhline(0.05, color="gray", linewidth=1, label="sensor noise std 0.05 m")
_ax2.set_xlabel(r"$\theta - \theta_0$ (rad)")
_ax2.set_ylabel("error (m)")
_ax2.grid(visible=True, alpha=0.9, linewidth=0.4)
_ax2.legend(loc="upper center", fontsize=8)
_ax2.set_title("Linearization error in the window", style="italic")
_fig.tight_layout()

_text = (
    f"Largest error for $|\\theta - \\theta_0| \\le {_w:.2f}$: ${float(np.max(_err)):.4f}$ m; "
    f"Taylor bound $w^2/2 = {_w**2 / 2:.4f}$ m."
)
mo.vstack([mo.hstack([lin_theta0, lin_width], justify="start"), graphic(_fig), mo.md(_text)])
```

The pendulum's *process model* is harder: it has two inputs, the angle $\theta$ and the angular velocity $\omega$. A simple Euler discretization with time step $\Delta t$, gravity $g$, and damping $c$ (Chapter 15 derives it) maps the state at one step to the next by
$$f(\theta, \omega) = \Big(\theta + \Delta t\,\omega,\ \ \omega - \Delta t\,\tfrac{g}{L}\sin\theta - \Delta t\,c\,\omega\Big).$$
To linearize $f$, we need to know how each output responds to a small change in each input separately. This section extends derivatives to functions of several variables.

### Points, Distances, and Continuity in $\mathbb R^n$

An element $\mathbf x = (x_1, \ldots, x_n)$ of $\mathbb R^n$ is an $n$-tuple of real numbers (a function $\{1, \ldots, n\} \to \mathbb R$, as in Chapter 3). Sums and real multiples are taken coordinatewise, and $\mathbf e_i$ denotes the point with $1$ in coordinate $i$ and $0$ elsewhere. The *Euclidean length* of $\mathbf x$ is $\|\mathbf x\| := \sqrt{x_1^2 + \cdots + x_n^2}$, and $\|\mathbf x - \mathbf y\|$ is the distance between $\mathbf x$ and $\mathbf y$. [Appendix D: Vectors](appendix_d_linear_algebra_v2.md) studies this {term}`norm` and proves the triangle inequality $\|\mathbf x + \mathbf y\| \le \|\mathbf x\| + \|\mathbf y\|$. We also use the elementary bounds
$$|x_i| \le \|\mathbf x\| \le |x_1| + \cdots + |x_n|,$$
which hold because $x_i^2 \le \sum_j x_j^2 \le \big(\sum_j |x_j|\big)^2$ and $\sqrt{\phantom{y}}$ is increasing. For $n = 1$, $\|x\| = |x|$.

The *open ball* of radius $r > 0$ around $\mathbf a$ is $B(\mathbf a, r) := \{\mathbf x \in \mathbb R^n : \|\mathbf x - \mathbf a\| < r\}$, and a set $U \subseteq \mathbb R^n$ is **open** if every $\mathbf a \in U$ has some ball $B(\mathbf a, r) \subseteq U$. Limits and continuity carry over verbatim with $\|\cdot\|$ in place of $|\cdot|$. For $D \subseteq \mathbb R^n$, $f: D \to \mathbb R^m$, and $\mathbf a \in D$, the function $f$ is continuous at $\mathbf a$ if for every $\varepsilon > 0$ there is $\delta > 0$ with $\|f(\mathbf x) - f(\mathbf a)\| < \varepsilon$ for every $\mathbf x \in D$ with $\|\mathbf x - \mathbf a\| < \delta$; and $\lim_{\mathbf x \to \mathbf a} f(\mathbf x) = \mathbf L$ means the same with $0 < \|\mathbf x - \mathbf a\| < \delta$ and $\mathbf L$ in place of $f(\mathbf a)$. For $n = m = 1$ these are exactly the definitions of {term}`continuous` and of the {term}`limit of a function`, so the words keep their meaning. By the bounds above, $f = (f_1, \ldots, f_m)$ is continuous at $\mathbf a$ if and only if every coordinate function $f_i$ is, and the one-variable lemmas about sums, products, compositions, and sequences carry over word for word, using the triangle inequality for $\|\cdot\|$.
  
### Partial Derivatives, Gradients, and Jacobians

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Partial derivative
: Let $U \subseteq \mathbb R^n$ be open, $f: U \to \mathbb R$, $\mathbf a \in U$, and $i \in \{1, \ldots, n\}$. The partial derivative of $f$ with respect to $x_i$ at $\mathbf a$ is
  $$\frac{\partial f}{\partial x_i}(\mathbf a) := \lim_{h \to 0} \frac{f(\mathbf a + h\,\mathbf e_i) - f(\mathbf a)}{h},$$
  provided this limit exists as a real number. Equivalently, it is the {term}`derivative` at $0$ of the one-variable function $h \mapsto f(\mathbf a + h\,\mathbf e_i)$: change $x_i$ and hold every other coordinate fixed.
:::
::::

Because $U$ is open, $\mathbf a + h\mathbf e_i \in U$ for all sufficiently small $|h|$, so the limit makes sense. In practice, a partial derivative is computed with the one-variable rules, treating the other variables as constants. For the pendulum's process model $f = (f_1, f_2)$:
$$\frac{\partial f_1}{\partial\theta} = 1, \quad \frac{\partial f_1}{\partial\omega} = \Delta t, \quad \frac{\partial f_2}{\partial\theta} = -\Delta t\,\frac gL\cos\theta, \quad \frac{\partial f_2}{\partial \omega} = 1 - c\,\Delta t.$$
The shorthand $\partial_i f := \partial f/\partial x_i$ is also common.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Gradient
: Let $U \subseteq \mathbb R^n$ be open and $f: U \to \mathbb R$. If all $n$ partial derivatives of $f$ exist at $\mathbf a \in U$, the gradient of $f$ at $\mathbf a$ is the $n$-tuple of those partial derivatives:
  $$\nabla f(\mathbf a) := \Big(\frac{\partial f}{\partial x_1}(\mathbf a), \ldots, \frac{\partial f}{\partial x_n}(\mathbf a)\Big).$$
:::
::::

:::{important icon=false} 📐 **Corollary (Interior Extremum in Several Variables)**
Let $U \subseteq \mathbb R^n$ be open and let $f: U \to \mathbb R$ have a local minimum or maximum at $\mathbf a \in U$ (that is, $f(\mathbf a) \le f(\mathbf x)$ for every $\mathbf x$ in some ball around $\mathbf a$, or $\ge$ for every such $\mathbf x$). If $\frac{\partial f}{\partial x_i}(\mathbf a)$ exists, it equals $0$. In particular, if $\nabla f(\mathbf a)$ exists, then $\nabla f(\mathbf a) = (0, \ldots, 0)$.
:::

:::{admonition icon=false} ✍️ **Proof**
The one-variable function $h \mapsto f(\mathbf a + h\mathbf e_i)$ is defined on an interval around $0$ and has a local extremum at the interior point $0$. Apply the Interior Extremum lemma. $\blacksquare$
:::

**Example (least squares).** [Chapter 11](ch11_measurement_functions_v2.md) fits a calibration line $z \approx m x + c$ to data $(x_1, z_1), \ldots, (x_N, z_N)$ by minimizing $S(m, c) := \sum_{i=1}^N (z_i - m x_i - c)^2$. Holding $c$ fixed and differentiating in $m$, and vice versa,
$$\frac{\partial S}{\partial m} = -2\sum_{i=1}^N x_i\,(z_i - m x_i - c), \qquad \frac{\partial S}{\partial c} = -2\sum_{i=1}^N (z_i - m x_i - c).$$
At a minimizer the gradient is $(0, 0)$, which gives two linear equations for $m$ and $c$, the *normal equations*.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Jacobian
: Let $U \subseteq \mathbb R^n$ be open and $f = (f_1, \ldots, f_m): U \to \mathbb R^m$. If all partial derivatives $\frac{\partial f_i}{\partial x_j}$ exist at $\mathbf a \in U$, the Jacobian of $f$ at $\mathbf a$ is the rectangular array with $m$ rows and $n$ columns whose entry in row $i$ and column $j$ is $\frac{\partial f_i}{\partial x_j}(\mathbf a)$:
  $$\mathbf J_f(\mathbf a) := \begin{bmatrix} \frac{\partial f_1}{\partial x_1}(\mathbf a) & \cdots & \frac{\partial f_1}{\partial x_n}(\mathbf a) \\ \vdots & \ddots & \vdots \\ \frac{\partial f_m}{\partial x_1}(\mathbf a) & \cdots & \frac{\partial f_m}{\partial x_n}(\mathbf a)\end{bmatrix}.$$
  Row $i$ is the gradient of the coordinate function $f_i$.
:::
::::

Such an array is a {term}`matrix`, studied in [Appendix D: Matrices and Linear Maps](appendix_d_linear_algebra_v2.md). Some books use "Jacobian" for the {term}`determinant` of this array when $m = n$; we call that the *Jacobian determinant*, $\det\mathbf J_f(\mathbf a)$. For the pendulum, with state $(\theta, \omega)$,
$$\mathbf J_f(\theta, \omega) = \begin{bmatrix} 1 & \Delta t \\ -\Delta t\,\frac gL\cos\theta & 1 - c\,\Delta t\end{bmatrix}, \qquad \mathbf J_h(\theta, \omega) = \begin{bmatrix} L\cos\theta & 0 \end{bmatrix},$$
where $h(\theta, \omega) := L\sin\theta$ is the measurement function viewed as a function of the whole state. These are the matrices $\mathbf F_k = \partial f/\partial\mathbf x$ and $\mathbf H_k = \partial h/\partial \mathbf x$ of Chapter 15.

Since a partial derivative is a limit of difference quotients, a Jacobian can be checked numerically. The code below compares the analytic Jacobian of the pendulum step with central differences $\frac{f(\mathbf x + h\mathbf e_j) - f(\mathbf x - h\mathbf e_j)}{2h}$, using the constants of Chapter 15 ($\Delta t = 0.01$ s, $g = 9.81$ m/s², $L = 1$ m, $c = 0.1$ s⁻¹). This is a standard guard against the "bad Jacobian" failure mode of the extended Kalman filter.

```{marimo} python
:echo: true
def pendulum_step(x, dt=0.01, g=9.81, L=1.0, c=0.1):
    """One Euler step of the damped pendulum; x = (theta, omega)."""
    theta, omega = x
    return np.array([
        theta + dt * omega,
        omega - dt * (g / L) * np.sin(theta) - dt * c * omega,
    ])

def pendulum_jacobian(x, dt=0.01, g=9.81, L=1.0, c=0.1):
    """Analytic Jacobian of pendulum_step at x."""
    theta = x[0]
    return np.array([
        [1.0, dt],
        [-dt * (g / L) * np.cos(theta), 1.0 - c * dt],
    ])

def numerical_jacobian(f, x, h=1e-6):
    """Central differences: column j approximates the partial derivatives with respect to x_j."""
    x = np.asarray(x, dtype=float)
    columns = []
    for j in range(x.size):
        e_j = np.zeros_like(x)
        e_j[j] = 1.0
        columns.append((f(x + h * e_j) - f(x - h * e_j)) / (2 * h))
    return np.column_stack(columns)

_x0 = np.array([0.5, 0.1])
_J_exact = pendulum_jacobian(_x0)
_J_numeric = numerical_jacobian(pendulum_step, _x0)
_names = ["∂f₁/∂θ", "∂f₁/∂ω", "∂f₂/∂θ", "∂f₂/∂ω"]
_rows = [
    f"| {_name} | {_a:.8f} | {_b:.8f} |"
    for _name, _a, _b in zip(_names, _J_exact.ravel(), _J_numeric.ravel())
]
mo.md(
    "Jacobian entries at θ = 0.5, ω = 0.1:\n\n"
    "| entry | analytic | central differences |\n|---|---|---|\n"
    + "\n".join(_rows)
    + f"\n\nLargest difference: {np.max(np.abs(_J_exact - _J_numeric)):.1e}"
)
```

### Differentiability and the First-Order Taylor Approximation

For $\mathbf h \in \mathbb R^n$, write $\mathbf J_f(\mathbf a)\,\mathbf h$ for the point of $\mathbb R^m$ whose $i$-th coordinate is $\sum_{j=1}^n \frac{\partial f_i}{\partial x_j}(\mathbf a)\,h_j$ ([Appendix D: Matrix Multiplication](appendix_d_linear_algebra_v2.md) calls this the product of the matrix with the vector $\mathbf h$). We extend the word *differentiable* to several variables: a function $f: U \to \mathbb R^m$ on an open $U \subseteq \mathbb R^n$ whose partial derivatives all exist at $\mathbf a \in U$ is differentiable at $\mathbf a$ if
$$\lim_{\mathbf h \to \mathbf 0} \frac{\|f(\mathbf a + \mathbf h) - f(\mathbf a) - \mathbf J_f(\mathbf a)\,\mathbf h\|}{\|\mathbf h\|} = 0.$$
For $n = m = 1$, $\mathbf J_f(a)h = f'(a)h$, and the condition says exactly that $\frac{f(a+h) - f(a)}{h} - f'(a) \to 0$; so it agrees with the definition of {term}`differentiable` in Derivatives. The approximation $f(\mathbf x) \approx f(\mathbf a) + \mathbf J_f(\mathbf a)(\mathbf x - \mathbf a)$ is the **first-order Taylor approximation** of $f$ at $\mathbf a$; Chapter 15 calls using it in place of $f$ {term}`linearization`.

Existence of the partial derivatives alone is not enough. Let $f(x, y) := \frac{xy}{x^2 + y^2}$ for $(x, y) \ne (0, 0)$ and $f(0, 0) := 0$. Then $f = 0$ on both axes, so both partial derivatives at $(0, 0)$ exist and equal $0$; but $f(t, t) = \frac12$ for every $t \ne 0$, so $f$ is not even continuous at the origin, and the first-order approximation $f \approx 0$ is wrong along the diagonal. Continuity of the partial derivatives repairs this.

:::{important icon=false} 📐 **Theorem (First-Order Taylor Approximation)**
Let $U \subseteq \mathbb R^n$ be open and $f: U \to \mathbb R^m$. If all partial derivatives $\frac{\partial f_i}{\partial x_j}$ exist on $U$ and are continuous at $\mathbf a \in U$, then $f$ is differentiable at $\mathbf a$:
$$f(\mathbf a + \mathbf h) = f(\mathbf a) + \mathbf J_f(\mathbf a)\,\mathbf h + \mathbf r(\mathbf h), \qquad \lim_{\mathbf h \to \mathbf 0}\frac{\|\mathbf r(\mathbf h)\|}{\|\mathbf h\|} = 0.$$
:::

:::{admonition icon=false} ✍️ **Proof**
Since $\|\mathbf r\| \le \sum_i |r_i|$, it suffices to treat one coordinate, so let $m = 1$. Choose $\rho > 0$ with $B(\mathbf a, \rho) \subseteq U$ and let $0 < \|\mathbf h\| < \rho$. Set $\mathbf p_0 := \mathbf a$ and $\mathbf p_j := \mathbf a + (h_1, \ldots, h_j, 0, \ldots, 0)$ for $j = 1, \ldots, n$, so that $\mathbf p_n = \mathbf a + \mathbf h$ and $\mathbf p_j - \mathbf p_{j-1} = h_j\mathbf e_j$. Each point $\mathbf p_{j-1} + s\mathbf e_j$ with $s$ between $0$ and $h_j$ differs from $\mathbf a$ by $(h_1, \ldots, h_{j-1}, s, 0, \ldots, 0)$, whose length is at most $\|\mathbf h\|$, so it lies in the ball. On that segment, the one-variable function $s \mapsto f(\mathbf p_{j-1} + s\mathbf e_j)$ has derivative $\frac{\partial f}{\partial x_j}(\mathbf p_{j-1} + s\mathbf e_j)$, so the Mean Value Theorem gives a point $\mathbf q_j$ on the segment with $f(\mathbf p_j) - f(\mathbf p_{j-1}) = \frac{\partial f}{\partial x_j}(\mathbf q_j)\,h_j$ (if $h_j = 0$, take $\mathbf q_j := \mathbf p_{j-1}$). Summing the telescoping differences,
$$r(\mathbf h) := f(\mathbf a + \mathbf h) - f(\mathbf a) - \sum_{j=1}^n \frac{\partial f}{\partial x_j}(\mathbf a)\,h_j = \sum_{j=1}^n \Big(\frac{\partial f}{\partial x_j}(\mathbf q_j) - \frac{\partial f}{\partial x_j}(\mathbf a)\Big)h_j.$$
Since $|h_j| \le \|\mathbf h\|$, we get $|r(\mathbf h)| \le \|\mathbf h\|\sum_j \big|\frac{\partial f}{\partial x_j}(\mathbf q_j) - \frac{\partial f}{\partial x_j}(\mathbf a)\big|$. Given $\varepsilon > 0$, continuity of the $n$ partial derivatives at $\mathbf a$ gives $\delta \le \rho$ such that each term of the last sum is below $\varepsilon/n$ whenever $\|\mathbf q_j - \mathbf a\| < \delta$, which holds when $\|\mathbf h\| < \delta$. Hence $|r(\mathbf h)|/\|\mathbf h\| < \varepsilon$ for $0 < \|\mathbf h\| < \delta$. $\blacksquare$
:::

A function whose partial derivatives exist and are continuous on all of $U$ is called **continuously differentiable** on $U$. The pendulum's $f$ and $h$ are continuously differentiable, because their partial derivatives are built from $\sin$, $\cos$, and constants.
  
### The Chain Rule

Chapter 15 composes nonlinear functions (for example, a measurement function applied to a predicted state). The chain rule says that the Jacobian of a composition is the product of the Jacobians.

:::{important icon=false} 📐 **Theorem (Chain Rule in Several Variables)**
Let $U \subseteq \mathbb R^n$ and $V \subseteq \mathbb R^m$ be open, let $g: U \to \mathbb R^m$ with $g(\mathbf x) \in V$ for every $\mathbf x \in U$, let $f: V \to \mathbb R^p$, and let $\mathbf a \in U$. If all partial derivatives of $g$ exist at $\mathbf a$ and $f$ is differentiable at $g(\mathbf a)$, then all partial derivatives of $f \circ g$ exist at $\mathbf a$, and
$$\frac{\partial (f\circ g)_i}{\partial x_j}(\mathbf a) = \sum_{k=1}^m \frac{\partial f_i}{\partial y_k}\big(g(\mathbf a)\big)\,\frac{\partial g_k}{\partial x_j}(\mathbf a).$$
In matrix form, $\mathbf J_{f\circ g}(\mathbf a) = \mathbf J_f\big(g(\mathbf a)\big)\,\mathbf J_g(\mathbf a)$.
:::

:::{admonition icon=false} ✍️ **Proof**
Fix $j$, let $\mathbf b := g(\mathbf a)$, and let $\boldsymbol\gamma(s) := g(\mathbf a + s\mathbf e_j)$ for $s$ near $0$. Each coordinate $\gamma_k$ is differentiable at $0$ with $\gamma_k'(0) = \frac{\partial g_k}{\partial x_j}(\mathbf a)$, hence continuous at $0$. Write $f(\mathbf b + \mathbf k) = f(\mathbf b) + \mathbf J_f(\mathbf b)\mathbf k + \mathbf r(\mathbf k)$, and let $\rho(\mathbf k) := \|\mathbf r(\mathbf k)\|/\|\mathbf k\|$ for $\mathbf k \ne \mathbf 0$ and $\rho(\mathbf 0) := 0$. Differentiability of $f$ at $\mathbf b$ says that $\rho$ is continuous at $\mathbf 0$, and $\|\mathbf r(\mathbf k)\| = \rho(\mathbf k)\,\|\mathbf k\|$ for every $\mathbf k$ (including $\mathbf k = \mathbf 0$, where $\mathbf r(\mathbf 0) = \mathbf 0$). With $\mathbf k(s) := \boldsymbol\gamma(s) - \mathbf b$, for $s \ne 0$,
$$\frac{f(\boldsymbol\gamma(s)) - f(\mathbf b)}{s} = \mathbf J_f(\mathbf b)\,\frac{\mathbf k(s)}{s} + \frac{\mathbf r(\mathbf k(s))}{s}.$$
As $s \to 0$, the $i$-th coordinate of the first term, $\sum_k \frac{\partial f_i}{\partial y_k}(\mathbf b)\,\frac{k_k(s)}{s}$, tends to $\sum_k \frac{\partial f_i}{\partial y_k}(\mathbf b)\,\gamma_k'(0)$ by the limit laws. The second term has length $\rho(\mathbf k(s))\,\frac{\|\mathbf k(s)\|}{|s|} \le \rho(\mathbf k(s))\sum_k \frac{|k_k(s)|}{|s|}$. Here $\mathbf k(s) \to \mathbf 0$, so $\rho(\mathbf k(s)) \to 0$ by continuity of $\rho$ at $\mathbf 0$, while $\sum_k |k_k(s)/s| \to \sum_k|\gamma_k'(0)|$ stays bounded; so the second term tends to $\mathbf 0$. $\blacksquare$
:::

:::{caution icon=false} ⚠️ **Assumptions and Failure Modes**
- **Linearization is local.** The first-order error is bounded by the second derivatives times the squared distance from the operating point. For the pendulum it is at most $\frac{(\theta - \theta_0)^2}{2}$ m, which is negligible near $\theta_0$ but can exceed the sensor noise once $|\theta - \theta_0|$ is more than about $0.3$ rad (try $\theta_0$ near $\pi/2$ in the figure above). An extended Kalman filter whose uncertainty is that large is linearizing in a region where the approximation fails ([Chapter 15](ch15_extended_kalman_filter_v2.md)).
- **Partial derivatives alone are not enough.** $\frac{xy}{x^2+y^2}$ has both partial derivatives at the origin but is not continuous there. The theorems above assume continuous partial derivatives, or differentiability.
- **Jacobians are easy to get wrong** by a sign or a missing factor; a central-difference check like the one above catches most mistakes.
:::

:::{attention icon=false} 🗝️ **Key Idea**
A partial derivative is an ordinary derivative in one coordinate with the others frozen. Arranging all of them in the Jacobian $\mathbf J_f(\mathbf a)$ gives the first-order Taylor approximation $f(\mathbf a + \mathbf h) \approx f(\mathbf a) + \mathbf J_f(\mathbf a)\mathbf h$, valid when the partial derivatives are continuous, and the Jacobian of a composition is the product of Jacobians.
:::
  
## Multiple Integrals

[Chapter 5](ch5_random_variables_v2.md) defines the normal density as $c\,e^{-x^2/2}$, where the constant $c$ must make the total probability $1$: $c = 1/\int_{-\infty}^\infty e^{-x^2/2}\,dx$. The Fundamental Theorem cannot compute this integral, because $e^{-x^2/2}$ has no antiderivative that can be written with finitely many elementary functions ([Wikipedia: Nonelementary integral](https://en.wikipedia.org/wiki/Nonelementary_integral)). The classic trick is to square the integral, which turns it into an integral over the plane, and then switch to polar coordinates, where an extra factor $r$ makes an antiderivative appear. Integrals over the plane are needed anyway: the joint density of two random variables is integrated over regions of $\mathbb R^2$.

### Integrals over Boxes

A **box** in $\mathbb R^n$ is a set $B = [a_1, b_1] \times \cdots \times [a_n, b_n]$ with $a_i < b_i$. A **grid** on $B$ consists of a subdivision $P_i$ of each side $[a_i, b_i]$. It cuts $B$ into *cells*, each a product of one subinterval from every $P_i$, and the *volume* $\operatorname{vol}(C)$ of a cell $C$ is the product of its side lengths. The mesh of the grid is the largest mesh of the $P_i$. A tagged grid chooses a tag $\mathbf t_C \in C$ in every cell, and its Riemann sum is $R(f, P, \mathbf t) := \sum_C f(\mathbf t_C)\operatorname{vol}(C)$. Replacing tagged subdivisions by tagged grids in the definition of the {term}`Riemann integral` defines $\int_B f(\mathbf x)\,d\mathbf x$, also written $\iint_B f(x, y)\,d(x, y)$ when $n = 2$. For $n = 1$ nothing changes.

:::{important icon=false} 📐 **Theorem (Continuous Functions on Boxes Are Integrable)**
Every continuous $f: B \to \mathbb R$ on a box $B \subseteq \mathbb R^n$ is Riemann integrable on $B$. The integral over boxes is linear and monotone, and if a box is cut into two boxes by a hyperplane $x_i = c$, the integral is the sum of the integrals over the two pieces.
:::

:::{admonition icon=false} ✍️ **Proof**
Not repeated here: the one-variable proofs (Cauchy Criterion for Integrals, Uniform Continuity on Closed Bounded Intervals, Continuous Functions Are Integrable, Properties of the Integral, Additivity over Intervals) carry over word for word. The two ingredients they need hold in $\mathbb R^n$: Bolzano–Weierstrass (apply the one-variable theorem to the first coordinates, then to the second coordinates of the resulting subsequence, and so on), and the fact that all the points of two grids together form a grid that refines both. See [Wikipedia: Multiple integral](https://en.wikipedia.org/wiki/Multiple_integral).
:::

:::{important icon=false} 📐 **Theorem (Fubini's Theorem for Continuous Functions on Rectangles)**
Let $f: [a, b] \times [c, d] \to \mathbb R$ be continuous. Then $G(x) := \int_c^d f(x, y)\,dy$ is continuous on $[a, b]$, and
$$\iint_{[a,b]\times[c,d]} f(x, y)\,d(x, y) = \int_a^b \left(\int_c^d f(x, y)\,dy\right)dx = \int_c^d \left(\int_a^b f(x, y)\,dx\right)dy.$$
:::

:::{admonition icon=false} ✍️ **Proof**
$G$ is defined because $y \mapsto f(x, y)$ is continuous. By uniform continuity on the rectangle, for every $\varepsilon > 0$ there is $\delta > 0$ with $|f(x, y) - f(x', y)| < \frac{\varepsilon}{d - c}$ whenever $|x - x'| < \delta$, so $|G(x) - G(x')| \le \int_c^d |f(x, y) - f(x', y)|\,dy \le \varepsilon$; thus $G$ is continuous, hence integrable.

For the equality, let $\varepsilon > 0$ and let $\delta$ be small enough for $\varepsilon/2$ both in the definition of the double integral and in the definition of $\int_a^b G$. Take a subdivision $a = x_0 < \cdots < x_N = b$ with tags $s_i$, and a subdivision $c = y_0 < \cdots < y_M = d$, both with mesh below $\delta$. For each $i$ and $j$, the Mean Value Theorem for Integrals, applied to the continuous function $y \mapsto f(s_i, y)$, gives $u_{ij} \in [y_{j-1}, y_j]$ with $\int_{y_{j-1}}^{y_j} f(s_i, y)\,dy = f(s_i, u_{ij})\,\Delta y_j$. By additivity,
$$\sum_{i} G(s_i)\,\Delta x_i = \sum_{i}\sum_{j} f(s_i, u_{ij})\,\Delta x_i\,\Delta y_j.$$
The left side is a Riemann sum for $\int_a^b G$, and the right side is a Riemann sum for the double integral with tags $(s_i, u_{ij})$ in the cells $[x_{i-1}, x_i] \times [y_{j-1}, y_j]$, both with mesh below $\delta$. Hence the two integrals differ by less than $\varepsilon$, for every $\varepsilon > 0$. The other order follows by exchanging the roles of $x$ and $y$. $\blacksquare$
:::

By induction on the dimension, the integral of a continuous function over a box in $\mathbb R^n$ equals the iterated integral in any order of the coordinates.

### Integrals over the Whole Space

For a continuous $f: \mathbb R^n \to [0, \infty)$, the integrals $\int_{[-R, R]^n} f$ increase with $R$ (the larger box splits into the smaller one and pieces with nonnegative integrals), so by the lemma on monotone functions the limit
$$\int_{\mathbb R^n} f(\mathbf x)\,d\mathbf x := \lim_{R\to\infty}\int_{[-R, R]^n} f(\mathbf x)\,d\mathbf x$$
exists in $[0, \infty]$. For $n = 1$ it agrees with the improper integral $\int_{-\infty}^\infty f(x)\,dx$. The two theorems below are standard results of Lebesgue integration theory, which we state without proof. They are phrased with Lebesgue integrals; for the continuous functions in this book, every Lebesgue integral that also exists as an (improper) Riemann integral in the sense above has the same value ([Wikipedia: Lebesgue integral](https://en.wikipedia.org/wiki/Lebesgue_integral)).

:::{important icon=false} 📐 **Theorem (Tonelli and Fubini)**
Let $D \subseteq \mathbb R^2$ be a closed set (for example $\mathbb R^2$ itself, a quadrant, a disk, or a triangle), and let $f: \mathbb R^2 \to \mathbb R$ be continuous on $D$ and $0$ outside $D$.
1. *(Tonelli)* If $f \ge 0$, then in $[0, \infty]$,
$$\int_{\mathbb R^2} f = \int_{-\infty}^\infty\left(\int_{-\infty}^\infty f(x, y)\,dy\right)dx = \int_{-\infty}^\infty\left(\int_{-\infty}^\infty f(x, y)\,dx\right)dy.$$
2. *(Fubini)* If $\int_{\mathbb R^2}|f| < \infty$, the inner integrals converge absolutely for all $x$ (respectively $y$) outside a set of measure zero, and the same equalities hold with all values finite.

The analogous statements hold in $\mathbb R^n$ for any grouping of the coordinates.
:::

:::{admonition icon=false} ✍️ **Proof**
Not proved here. For continuous functions on rectangles, this is the previous theorem; the general statements are Tonelli's and Fubini's theorems for the Lebesgue integral, which apply to every function of this form. See [Wikipedia: Fubini's theorem](https://en.wikipedia.org/wiki/Fubini%27s_theorem).
:::

**Example (exchanging the order over a triangle).** Let $t_0 < t_1$, let $f$ be continuous on the closed triangle $T := \{(s, t) : t_0 \le s \le t \le t_1\}$, and extend it by $0$. It is bounded on $T$ (by the extreme value theorem in two variables, proved like the one-variable version), so $\int_{\mathbb R^2}|f| < \infty$, and integrating in either order gives
$$\int_{t_0}^{t_1}\left(\int_{t_0}^{t} f(s, t)\,ds\right)dt = \int_{t_0}^{t_1}\left(\int_{s}^{t_1} f(s, t)\,dt\right)ds.$$
With $f(s, t) := g(s)$ for a continuous $g$, the inner integral on the right is $(t_1 - s)\,g(s)$, so $\int_{t_0}^{t_1}\int_{t_0}^{t} g(s)\,ds\,dt = \int_{t_0}^{t_1}(t_1 - s)\,g(s)\,ds$. This special case, used in [Chapter 14](ch14_kalman_filters_in_practice_v2.md), also follows from integration by parts with $G(t) := \int_{t_0}^t g(s)\,ds$ and $t \mapsto t - t_1$.

:::{important icon=false} 📐 **Theorem (Change of Variables)**
Let $U, V \subseteq \mathbb R^n$ be open, and let $T: U \to V$ be a bijection such that $T$ and $T^{-1}$ are continuously differentiable. Then for every continuous $f: V \to [0, \infty)$,
$$\int_V f(\mathbf x)\,d\mathbf x = \int_U f\big(T(\mathbf u)\big)\,\big|\det \mathbf J_T(\mathbf u)\big|\,d\mathbf u,$$
where both sides are Lebesgue integrals with values in $[0, \infty]$, and $\det$ is the {term}`determinant` ([Appendix D: Determinants](appendix_d_linear_algebra_v2.md)).
:::

:::{admonition icon=false} ✍️ **Proof**
Not proved here. See [Wikipedia: Integration by substitution, substitution for multiple variables](https://en.wikipedia.org/wiki/Integration_by_substitution#Substitution_for_multiple_variables). For $n = 1$ and an increasing $T$ it is the substitution rule of The Fundamental Theorem of Calculus.
:::

The factor $|\det\mathbf J_T|$ measures how $T$ stretches volume near $\mathbf u$: a tiny box of volume $v$ around $\mathbf u$ is mapped to a region of volume approximately $|\det\mathbf J_T(\mathbf u)|\,v$. For an affine map $T(\mathbf u) = \mathbf A\mathbf u + \mathbf b$ with an invertible matrix $\mathbf A$, the Jacobian is $\mathbf A$ everywhere, which [Chapter 12](ch12_vectors_matrices_covariance_v2.md) uses for the multivariate normal density.

:::{important icon=false} 📐 **Corollary (Polar Coordinates)**
Let $f: \mathbb R^2 \to [0, \infty)$ be continuous and $0 < \rho \le \infty$, and let $D_\rho := \{(x, y) : x^2 + y^2 < \rho^2\}$ be the open disk of radius $\rho$ (with $D_\infty := \mathbb R^2$). Then
$$\int_{D_\rho} f = \int_0^{2\pi}\left(\int_0^\rho f(r\cos\theta, r\sin\theta)\,r\,dr\right)d\theta.$$
For $\rho = \infty$ the left side is $\int_{\mathbb R^2} f$ as defined above.
:::

:::{admonition icon=false} ✍️ **Proof**
Let $T(r, \theta) := (r\cos\theta, r\sin\theta)$ on $U := (0, \rho) \times (0, 2\pi)$. By the cited facts about sine and cosine, $T$ is a bijection from $U$ onto $V := D_\rho$ minus the ray $\{(x, 0) : x \ge 0\}$, and its inverse is continuously differentiable (also cited). Its Jacobian determinant is
$$\det\begin{bmatrix}\cos\theta & -r\sin\theta \\ \sin\theta & r\cos\theta\end{bmatrix} = r\cos^2\theta + r\sin^2\theta = r > 0.$$
The removed ray has zero area (it can be covered by rectangles of arbitrarily small total area), so $\int_V f = \int_{D_\rho} f$. Apply Change of Variables, then Tonelli on $U$. $\blacksquare$
:::
  
### The Gaussian Integral

:::{important icon=false} 📐 **Theorem (Gaussian Integral)**
$$\int_{-\infty}^{\infty} e^{-x^2/2}\,dx = \sqrt{2\pi}.$$
:::

:::{admonition icon=false} ✍️ **Proof**
Let $I := \int_{-\infty}^\infty e^{-x^2/2}\,dx$, which converges by Gaussian Moments Converge, and $I_R := \int_{-R}^R e^{-x^2/2}\,dx$, so that $I_R \to I$ as $R \to \infty$. Let $f(x, y) := e^{-(x^2 + y^2)/2} = e^{-x^2/2}\,e^{-y^2/2}$, a positive continuous function.

*Cartesian coordinates.* By Fubini on the square and linearity (the inner integral $I_R$ is a constant),
$$\int_{[-R,R]^2} f = \int_{-R}^R e^{-x^2/2}\left(\int_{-R}^R e^{-y^2/2}\,dy\right)dx = I_R \int_{-R}^R e^{-x^2/2}\,dx = I_R^2,$$
so $\int_{\mathbb R^2} f = \lim_{R\to\infty} I_R^2 = I^2$.

*Polar coordinates.* Since $\cos^2\theta + \sin^2\theta = 1$, we have $f(r\cos\theta, r\sin\theta) = e^{-r^2/2}$. By the chain rule, $-e^{-r^2/2}$ is an antiderivative of $r\,e^{-r^2/2}$, so
$$\int_0^t e^{-r^2/2}\,r\,dr = 1 - e^{-t^2/2} \to 1 \qquad (t \to \infty).$$
The inner integral is $1$ for every $\theta$, and the Polar Coordinates corollary gives $\int_{\mathbb R^2} f = \int_0^{2\pi} 1\,d\theta = 2\pi$.

Hence $I^2 = 2\pi$. Since the integrand is positive, $I > 0$, so $I = \sqrt{2\pi}$. $\blacksquare$
:::

:::{important icon=false} 📐 **Corollary (Normal Density Integrals)**
For every $\mu \in \mathbb R$ and $\sigma > 0$:
1. $\displaystyle\int_{-\infty}^\infty \frac{1}{\sigma\sqrt{2\pi}}\,e^{-(x-\mu)^2/(2\sigma^2)}\,dx = 1$.
2. $\displaystyle\int_{-\infty}^\infty x\,e^{-x^2/2}\,dx = 0$.
3. $\displaystyle\int_{-\infty}^\infty x^2\,e^{-x^2/2}\,dx = \sqrt{2\pi}$.
:::

:::{admonition icon=false} ✍️ **Proof**
All three integrands are continuous, and the integrals converge absolutely by Gaussian Moments Converge (after the substitution below for part 1). By the substitution $x = -u$, the integral of an even integrand over $[-t, 0]$ equals its integral over $[0, t]$, and for an odd integrand it equals the negative.
1. The substitution $x = \mu + \sigma u$ gives $\int_{\mu + \sigma s}^{\mu + \sigma t} e^{-(x-\mu)^2/(2\sigma^2)}\,dx = \sigma\int_s^t e^{-u^2/2}\,du$. Letting $s \to -\infty$ and $t \to \infty$, the left side tends to the integral in part 1 times $\sigma\sqrt{2\pi}$, and the right side to $\sigma\sqrt{2\pi}$ by the theorem.
2. $\int_0^t x\,e^{-x^2/2}\,dx = 1 - e^{-t^2/2} \to 1$, and by oddness the left tail tends to $-1$. The sum is $0$.
3. Integration by parts with $f(x) = x$ and $g(x) = -e^{-x^2/2}$ (so $g'(x) = x\,e^{-x^2/2}$) gives $\int_0^t x^2 e^{-x^2/2}\,dx = -t\,e^{-t^2/2} + \int_0^t e^{-x^2/2}\,dx$. Since $e^{t^2/2} \ge 1 + \frac{t^2}{2}$, we have $0 \le t\,e^{-t^2/2} \le \frac{t}{1 + t^2/2} \to 0$, and by evenness $\int_0^\infty e^{-x^2/2}\,dx = \frac{\sqrt{2\pi}}{2}$. So $\int_0^\infty x^2 e^{-x^2/2}\,dx = \frac{\sqrt{2\pi}}{2}$, and by evenness the full integral is $\sqrt{2\pi}$. $\blacksquare$
:::

Part 1 says that the {term}`normal distribution`'s density integrates to $1$ ([Chapter 5](ch5_random_variables_v2.md)). Dividing parts 2 and 3 by $\sqrt{2\pi}$ shows that the standard normal distribution has mean $0$ and variance $1$ ([Chapter 6](ch6_expectation_and_variance_v2.md)).

:::{caution icon=false} ⚠️ **Assumptions and Failure Modes**
- **Fubini needs absolute integrability.** For $f(x, y) = \frac{x^2 - y^2}{(x^2 + y^2)^2}$ on $(0, 1]^2$, the inner integral is $\int_0^1 f(x, y)\,dy = \big[\frac{y}{x^2 + y^2}\big]_0^1 = \frac{1}{1 + x^2}$, so integrating $y$ first gives $\frac\pi4$, while integrating $x$ first gives $-\frac\pi4$ by the symmetry $f(y, x) = -f(x, y)$. Here $\iint |f| = \infty$.
- **Change of variables needs a bijection with nonzero Jacobian determinant.** Letting $\theta$ run over $(0, 4\pi)$ would count every point twice, and the factor $r$ vanishes at $r = 0$, which is why $r = 0$ is excluded from $U$ (a set of zero area, so nothing is lost).
- **No closed form for normal probabilities.** Because $e^{-x^2/2}$ has no elementary antiderivative, probabilities such as $\int_a^b e^{-x^2/2}\,dx/\sqrt{2\pi}$ are computed numerically (via the [error function](https://en.wikipedia.org/wiki/Error_function)), not by the Fundamental Theorem.
:::

:::{attention icon=false} 🗝️ **Key Idea**
Integrals over boxes are limits of Riemann sums over grids, and for continuous functions they can be computed one coordinate at a time (Fubini). Changing variables multiplies the integrand by $|\det\mathbf J_T|$; in polar coordinates that factor is $r$, which turns the squared Gaussian integral into an elementary one and proves $\int_{-\infty}^\infty e^{-x^2/2}\,dx = \sqrt{2\pi}$.
:::
  
## Linear Differential Equations

Before a sensor's voltage reaches an analog-to-digital converter, it often passes through an analog low-pass filter: a resistor $R_\Omega$ in series with a capacitor $C$. If $u(t)$ is the input voltage and $y(t)$ the capacitor voltage, the current through the resistor is $\frac{u - y}{R_\Omega}$, and it charges the capacitor at the rate $C\dot y$, so

$$\dot y(t) = -\frac1\tau\,y(t) + \frac1\tau\,u(t), \qquad \tau := R_\Omega C.$$

The converter only sees samples $y_k := y(k\,\Delta t)$. How is $y_k$ related to $y_{k-1}$? Answering this requires solving the equation, and the answer turns out to be an old friend.

Throughout this section the unknown is a function of time $t$, and $\dot x := \frac{dx}{dt}$.

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Differential equation
: Let $J$ be an interval with more than one point, $n \in \mathbb N^+$, and $F$ a given real-valued function of $n + 2$ real variables. The (ordinary) differential equation of order $n$
  $$F\big(t, x(t), \dot x(t), \ldots, x^{(n)}(t)\big) = 0$$
  is the condition, on an unknown function $x: J \to \mathbb R$, that $x$ is $n$ times {term}`differentiable` on $J$ and satisfies the equation for every $t \in J$. A function that satisfies the condition is a *solution*. A *system* of differential equations is the same with an unknown $\mathbf x: J \to \mathbb R^d$ and an $\mathbb R^d$-valued $F$.
:::
::::

The low-pass filter is an instance of the **first-order linear differential equation with constant coefficients**,
$$\dot x(t) = a\,x(t) + b\,u(t),$$
where $a, b \in \mathbb R$ are constants and $u: J \to \mathbb R$ is a given input ([Chapter 10](ch10_process_models_v2.md) calls it a {term}`control input`). Written as $F(t, x, \dot x) := \dot x - a x - b\,u(t) = 0$, it fits the definition with $n = 1$. "Linear" refers to the right side being a linear combination of $x$ and $u$. The case $u = 0$ was solved in Exponential and Logarithm: the only solutions are $x(t) = x(t_0)\,e^{a(t - t_0)}$.

:::{important icon=false} 📐 **Theorem (Solution of the Linear Differential Equation)**
Let $J$ be an interval with more than one point, $t_0 \in J$, $a, b, x_0 \in \mathbb R$, and let $u: J \to \mathbb R$ be continuous. The differential equation $\dot x(t) = a\,x(t) + b\,u(t)$ has exactly one solution on $J$ with $x(t_0) = x_0$, namely
$$x(t) = e^{a(t - t_0)}\,x_0 + \int_{t_0}^t e^{a(t - s)}\,b\,u(s)\,ds.$$
:::

:::{admonition icon=false} ✍️ **Proof**
*Any solution has this form.* Let $x$ be a solution and multiply the equation by the *integrating factor* $e^{-at}$. By the product rule,
$$\frac{d}{dt}\Big(e^{-at}x(t)\Big) = e^{-at}\big(\dot x(t) - a\,x(t)\big) = e^{-at}\,b\,u(t).$$
The right side is continuous, hence integrable on the interval between $t_0$ and $t$, so Part 2 of the Fundamental Theorem gives $e^{-at}x(t) - e^{-at_0}x_0 = \int_{t_0}^t e^{-as}\,b\,u(s)\,ds$. Multiplying by $e^{at}$ (a constant with respect to $s$) gives the formula.

*The formula is a solution.* Write it as $x(t) = e^{at}\Big(e^{-at_0}x_0 + \int_{t_0}^t e^{-as}\,b\,u(s)\,ds\Big)$. By Part 1 of the Fundamental Theorem the bracket is differentiable with derivative $e^{-at}\,b\,u(t)$, so by the product rule $\dot x(t) = a\,x(t) + e^{at}e^{-at}\,b\,u(t) = a\,x(t) + b\,u(t)$. Also $x(t_0) = x_0$. $\blacksquare$
:::

The two terms have clear meanings. The first is the memory of the initial condition: for $a < 0$ it decays by a factor $e$ every $\tau := -1/a$ seconds (the *time constant*), and for $a > 0$ it grows. The second is a weighted sum of past inputs, where an input from $t - s$ seconds ago has weight $e^{a(t-s)}b$. For the low-pass filter that weight is $\frac1\tau e^{-(t-s)/\tau}$: the exponential weights of Improper Integrals, a continuous-time version of the EMA's weights.
  
### Exact Discretization

A digital filter runs in steps of $\Delta t$, so we want a recursion for the samples $x_k := x(t_k)$ at $t_k := t_0 + k\,\Delta t$. Suppose the input is held constant during each sample period, $u(t) = u_k$ for $t_{k-1} < t \le t_k$ (a *zero-order hold*, which is what a digital-to-analog converter or a once-per-step control command produces). Such an input jumps at the sample times, so we solve one period at a time: on $[t_{k-1}, t_k]$, let $x$ be the solution of $\dot x = a\,x + b\,u_k$ that starts from the value $x(t_{k-1})$ reached at the end of the previous period.

:::{important icon=false} 📐 **Theorem (Exact Discretization)**
Under a zero-order hold, the samples satisfy exactly
$$x_k = a_d\,x_{k-1} + b_d\,u_k, \qquad a_d := e^{a\Delta t}, \qquad b_d := \begin{cases} b\,\dfrac{e^{a\Delta t} - 1}{a} & a \ne 0, \\[1ex] b\,\Delta t & a = 0. \end{cases}$$
:::

:::{admonition icon=false} ✍️ **Proof**
Apply the previous theorem on $[t_{k-1}, t_k]$ with the constant input $u_k$: $x_k = e^{a\Delta t}x_{k-1} + \int_{t_{k-1}}^{t_k} e^{a(t_k - s)}\,b\,u_k\,ds$. The substitution $\sigma = t_k - s$ turns the integral into $b\,u_k\int_0^{\Delta t} e^{a\sigma}\,d\sigma$, which equals $b\,u_k\frac{e^{a\Delta t} - 1}{a}$ for $a \ne 0$ (antiderivative $e^{a\sigma}/a$) and $b\,u_k\,\Delta t$ for $a = 0$. $\blacksquare$
:::

No approximation is involved: for any $\Delta t$, the recursion reproduces the continuous solution exactly at the sample times. This is the scalar case of the {term}`discretization` of [Chapter 10](ch10_process_models_v2.md).

**The low-pass filter is an EMA.** For the RC filter, $a = -\frac1\tau$ and $b = \frac1\tau$, so $a_d = e^{-\Delta t/\tau}$ and $b_d = \frac1\tau\cdot\frac{e^{-\Delta t/\tau} - 1}{-1/\tau} = 1 - e^{-\Delta t/\tau}$. With $\alpha := 1 - e^{-\Delta t/\tau} \in (0, 1)$,
$$y_k = (1 - \alpha)\,y_{k-1} + \alpha\,u_k = y_{k-1} + \alpha\,(u_k - y_{k-1}),$$
which is exactly the {term}`exponential moving average`, with the held input $u_k$ in the role of the measurement $z_k$. Conversely, an EMA with smoothing factor $\alpha$ at sample period $\Delta t$ behaves like an RC filter with time constant $\tau = -\Delta t/\ln(1 - \alpha)$: the [Introduction](introduction_v2.md)'s $\alpha = 0.05$ at 10 samples per second corresponds to $\tau \approx 1.95$ s. For $\Delta t \ll \tau$, Taylor's Theorem gives $\alpha \approx \Delta t/\tau$.

**Euler's method.** Replacing $\dot x$ on $(t_{k-1}, t_k]$ by the difference quotient $\frac{x_k - x_{k-1}}{\Delta t}$ evaluated with the values at $t_{k-1}$ gives the approximation $x_k \approx (1 + a\Delta t)\,x_{k-1} + b\,\Delta t\,u_k$. Its coefficients are the degree-$1$ Taylor polynomials of $a_d$ and $b_d$ in $\Delta t$, and the Taylor Error Bound gives $|e^{a\Delta t} - (1 + a\Delta t)| \le \frac{(a\Delta t)^2}{2}e^{|a|\Delta t}$ per step. Euler's method is simple and works well for small $\Delta t$. For large $\Delta t$ it can fail badly, as the figure shows for the decay $\dot x = -x/\tau$ with $x(0) = 1$.

```{marimo} python
:hide-code: true

ode_ratio = mo.ui.slider(start=0.1, stop=3.0, step=0.1, value=0.5, label=r"sample period $\Delta t / \tau$")
```

```{marimo} python
:hide-code: true

_r = ode_ratio.value  # sample period in units of the time constant (tau = 1 s)
_t = np.linspace(0, 10, 500)
_k = np.arange(0, int(np.floor(10 / _r + 1e-9)) + 1)
_exact = np.exp(-_r) ** _k
_euler = (1 - _r) ** _k

_fig, _ax = plt.subplots(figsize=(7, 3.6))
_ax.plot(_t, np.exp(-_t), color="black", linewidth=1.5, label=r"true solution $e^{-t/\tau}$")
_ax.plot(_k * _r, _exact, "o", color="C1", markersize=6, label=r"exact discretization, $a_d = e^{-\Delta t/\tau}$")
_ax.plot(_k * _r, _euler, "s:", color="red", markersize=4, label=r"Euler, $1 - \Delta t/\tau$")
_ax.axhline(0, color="gray", linewidth=0.8)
_ax.set_xlim(0, 10)
_ax.set_ylim(-2.5, 2.5)
_ax.set_xlabel(r"time $t/\tau$")
_ax.set_ylabel("$x(t)$")
_ax.grid(visible=True, alpha=0.9, linewidth=0.4)
_ax.legend(loc="upper right", fontsize=8)
_ax.set_title(f"Discretizing exponential decay with $\\Delta t = {_r:.1f}\\,\\tau$", style="italic")
_fig.tight_layout()

if np.isclose(_r, 1):
    _verdict = "Euler's factor is exactly $0$: it jumps to $0$ after one step."
elif np.isclose(_r, 2):
    _verdict = "Euler's factor is exactly $-1$: its samples flip sign forever and never decay."
elif _r > 2:
    _verdict = "Since $|1 - \\Delta t/\\tau| > 1$, Euler's recursion grows without bound, although the true solution decays."
elif _r > 1:
    _verdict = "Euler's factor is negative, so its samples alternate in sign, although the true solution is always positive."
else:
    _verdict = "Both recursions decay; Euler's per-step error in the factor is about $(\\Delta t/\\tau)^2/2$."
_text = (
    f"Exact factor $e^{{-\\Delta t/\\tau}} = {np.exp(-_r):.3f}$; "
    f"Euler factor $1 - \\Delta t/\\tau = {0.0 if np.isclose(_r, 1) else 1 - _r:.3f}$. "
    + _verdict
)
mo.vstack([ode_ratio, graphic(_fig), mo.md(_text)])
```

**Vector states.** For a state vector $\mathbf x(t) \in \mathbb R^d$ and the system $\dot{\mathbf x} = \mathbf A\mathbf x + \mathbf B\mathbf u$, the same integrating-factor argument, with the {term}`matrix exponential` $e^{\mathbf A t}$ in place of $e^{at}$, gives $\mathbf x(t) = e^{\mathbf A(t - t_0)}\mathbf x_0 + \int_{t_0}^t e^{\mathbf A(t-s)}\mathbf B\,\mathbf u(s)\,ds$ and the exact discretization $\mathbf x_k = e^{\mathbf A\Delta t}\mathbf x_{k-1} + \big(\int_0^{\Delta t} e^{\mathbf A\sigma}\,d\sigma\big)\mathbf B\,\mathbf u_k$ under a zero-order hold. [Appendix D: The Matrix Exponential](appendix_d_linear_algebra_v2.md) develops $e^{\mathbf A t}$, and Chapters 10 and 14 use these formulas.

:::{caution icon=false} ⚠️ **Assumptions and Failure Modes**
- **The zero-order hold is an assumption.** If the input varies within a sample period (a measured acceleration, say), the recursion $x_k = a_d x_{k-1} + b_d u_k$ is only an approximation, whose error depends on how fast $u$ changes.
- **Euler's method can be unstable.** For $a < 0$ the exact factor $e^{a\Delta t}$ always lies in $(0, 1)$, but Euler's factor $1 + a\Delta t$ is negative for $\Delta t > \tau$ and below $-1$ for $\Delta t > 2\tau$, where the recursion diverges like a geometric sequence with $|q| > 1$.
- **Time-varying coefficients.** If $a$ depends on $t$, the same proof works with the integrating factor $e^{-\int_{t_0}^t a(s)\,ds}$.
- **Nonlinear equations** such as the pendulum's $\ddot\theta = -\frac gL\sin\theta - c\,\dot\theta$ generally have no closed-form solution. The [Picard–Lindelöf theorem](https://en.wikipedia.org/wiki/Picard%E2%80%93Lindel%C3%B6f_theorem) guarantees a unique solution, at least for a short time, when the right side is continuously differentiable, and numerical methods such as the [Runge–Kutta methods](https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods) approximate it; Chapter 15 uses the classical fourth-order method (RK4) to simulate the true pendulum.
:::

:::{attention icon=false} 🗝️ **Key Idea**
The integrating factor $e^{-at}$ turns $\dot x = ax + bu$ into $\frac{d}{dt}(e^{-at}x) = e^{-at}bu$, which the Fundamental Theorem solves: $x(t) = e^{a(t-t_0)}x_0 + \int_{t_0}^t e^{a(t-s)}\,b\,u(s)\,ds$. Under a zero-order hold, the samples obey the exact recursion $x_k = e^{a\Delta t}x_{k-1} + b\frac{e^{a\Delta t} - 1}{a}u_k$. For an RC low-pass filter this recursion is precisely the EMA.
:::
  
## Summary

- **Limits.** $a_n \to L$ means every tolerance $\varepsilon > 0$ is eventually met for good. Limit laws combine limits, and the completeness of $\mathbb R$ yields Monotone Convergence, Bolzano–Weierstrass, and the Cauchy criterion.
- **Series.** A series is the sequence of its partial sums. The geometric series $\sum q^n = \frac{1}{1-q}$ ($|q| < 1$) shows that the EMA's weights add up to $1$. Nonnegative and absolutely convergent sums can be reordered and regrouped freely.
- **Continuity and derivatives.** Continuous functions on $[a, b]$ take every intermediate value, attain their extremes, and are uniformly continuous. The derivative is the limit of difference quotients; the sum, product, quotient, and chain rules, the Mean Value Theorem, and Taylor's Theorem with Lagrange remainder follow, and the last turns approximations into guaranteed error bounds.
- **Integrals.** The Riemann integral is the limit of Riemann sums as the mesh shrinks. Continuous and piecewise continuous functions are integrable, the Fundamental Theorem connects integrals with antiderivatives, and improper integrals extend integration to unbounded intervals and integrands.
- **Exponential and logarithm.** $e^x = \sum \frac{x^n}{n!}$ is the unique solution of $y' = y$, $y(0) = 1$; it satisfies $e^{a+b} = e^ae^b$, and $\ln$ is its inverse. Sine and cosine are defined by power series as well.
- **Several variables.** Partial derivatives, gradients, and Jacobians give the first-order Taylor approximation $f(\mathbf a + \mathbf h) \approx f(\mathbf a) + \mathbf J_f(\mathbf a)\mathbf h$, and the chain rule multiplies Jacobians. Fubini's theorem and polar coordinates prove $\int_{-\infty}^\infty e^{-x^2/2}\,dx = \sqrt{2\pi}$.
- **Linear differential equations.** $\dot x = ax + bu$ has the solution $x(t) = e^{a(t-t_0)}x_0 + \int_{t_0}^t e^{a(t-s)}\,b\,u(s)\,ds$, whose exact discretization under a zero-order hold turns an RC low-pass filter into an EMA.

## What's Next

If you came here from a main-path chapter, return to it now: [Chapter 4](ch4_probability_spaces_v2.md) uses Sequences and Limits and Series for countable additivity and the continuity of probability; [Chapter 5](ch5_random_variables_v2.md) and [Chapter 6](ch6_expectation_and_variance_v2.md) use the integrals and the Gaussian integral for densities and expectations; [Chapter 10](ch10_process_models_v2.md) uses Linear Differential Equations; and [Chapter 15](ch15_extended_kalman_filter_v2.md) uses Functions of Several Variables. The vector and matrix versions of these ideas, including the matrix exponential for $\dot{\mathbf x} = \mathbf A\mathbf x + \mathbf B\mathbf u$ and derivatives with respect to matrices for the Kalman gain, are in [Appendix D: Linear Algebra](appendix_d_linear_algebra_v2.md).