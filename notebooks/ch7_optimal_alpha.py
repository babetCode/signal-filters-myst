# /// script
# dependencies = [
#     "marimo>=0.25.1",
#     "matplotlib==3.11.2",
#     "numpy==2.5.3",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="7. The Optimal Alpha", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "Combining Two Noisy Estimates"
    abbreviations:
      iff: if and only if
      diff: null
      EMA: exponential moving average
      MSE: mean squared error
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
    import matplotlib.pyplot as plt
    from textwrap import dedent

    return dedent, mo, np, plt


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
def helpers(np):
    # jb: include=false
    def normal_pdf(x, mean, var):
        return np.exp(-((x - mean) ** 2) / (2 * var)) / np.sqrt(2 * np.pi * var)

    def ema_filter(alpha, z):
        """EMA with first-measurement initialization along the last axis."""
        z = np.asarray(z, dtype=float)
        out = np.empty_like(z)
        out[..., 0] = z[..., 0]
        for k in range(1, z.shape[-1]):
            out[..., k] = out[..., k - 1] + alpha * (z[..., k] - out[..., k - 1])
        return out

    def ema_error_variance(alpha, R, k):
        """Exact EMA error variance (Chapter 6), first-measurement initialization."""
        k = np.asarray(k, dtype=float)
        b = (1 - alpha) ** 2
        if b == 1.0:
            return np.full_like(k, R)
        return R * (b ** (k - 1) + alpha**2 * (1 - b ** (k - 1)) / (1 - b))

    return ema_error_variance, ema_filter, normal_pdf


@app.cell
def scale_data(np):
    # jb: include=false
    scale_x = 155.0
    scale_R = 1.0
    # Same data as the Introduction: 3 s at 10 samples/s, noise sigma = 1 lb, seed 1
    scale_z = np.round(scale_x + np.random.default_rng(1).normal(0.0, 1.0, 30), 2)
    scale_t = np.arange(1, 31) / 10
    return scale_R, scale_t, scale_x, scale_z


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The [Introduction](#intro-sec-whats-next) ended with a question:

    > Given some amount of noise in our prediction $\hat x_k^-$ and in our measurement $z_k$, what value of $\alpha$ should we pick?

    This chapter answers it. Suppose the prediction's error has variance $P^-$, the measurement's noise has variance $R$, both errors have mean zero, and they are uncorrelated. Then the gain that makes the new estimate's error variance as small as possible is

    $$\alpha^* = \frac{P^-}{P^- + R},$$

    and the resulting estimate is more certain than either source on its own. The derivation needs nothing beyond [Chapter 6](#ch6-thm-variance-of-a-linear-combination)'s rule for the variance of a weighted sum and the high-school trick of completing the square. With it we prove that the Introduction's cumulative average was the best possible filter for a constant weight, and we arrive at the update equation at the heart of every Kalman filter[^kf-forward].

    [^kf-forward]: Used informally here; defined precisely in [Chapter 9](#ch9-sec-the-scalar-kalman-filter).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// important | 🔗 **Prerequisites**
    - [Introduction](introduction.md): {term}`estimate`, {term}`prediction` $\hat x_k^-$, {term}`innovation`, [the cumulative average](#intro-sec-a-recursive-average), and the {term}`exponential moving average` (EMA) with [first-measurement initialization](#intro-sec-initialization).
    - [Chapter 2](ch2_axioms_of_set_theory.md): [proof by induction](#ch2-thm-induction).
    - [Chapter 5](ch5_random_variables.md): {term}`random variables <random variable>`, the {term}`normal distribution`, and [the measurement-noise model](#ch5-sec-the-measurement-noise-model) $z_k = x_k + v_k$.
    - [Chapter 6](ch6_expectation_and_variance.md): [linearity of expectation](#ch6-thm-linearity-and-positivity-of-expectation), {term}`variance`, {term}`covariance` and [its properties](#ch6-thm-properties-of-covariance) (including linearity in each argument and [the Cauchy–Schwarz inequality](#ch6-thm-cauchyschwarz-inequality)), {term}`uncorrelated` random variables, [the variance of a linear combination](#ch6-thm-variance-of-a-linear-combination), in particular $\operatorname{Var}(aX + bY) = a^2\operatorname{Var}X + b^2\operatorname{Var}Y + 2ab\operatorname{Cov}(X, Y)$, [Bienaymé's corollary](#ch6-cor-bienayme), {term}`unbiased` estimators, {term}`mean squared error` and [the bias–variance decomposition](#ch6-thm-biasvariance-decomposition), the variance $\sigma^2/k$ of the {term}`sample mean`, and [the EMA's error variance](#ch6-thm-ema-of-a-constant-value), including [the corollary that for a constant value averaging beats the EMA](#ch6-cor-for-a-constant-value-averaging-beats-the-ema).
    - [Appendix C: Derivatives](#appc-sec-derivatives) (optional; only for the alternative derivation in one tip).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// attention | 🗝️ **Key Idea**
    To combine two unbiased, uncorrelated sources of information about the same quantity, weight each source in proportion to the *other* source's variance. The optimal gain $\alpha^* = P^-/(P^- + R)$ does exactly this, and the combined error variance $P^-R/(P^- + R)$ is smaller than both $P^-$ and $R$.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch7-sec-a-concrete-example -->
    ## A Concrete Example

    Return to the bathroom scale from the Introduction: the true weight is $x = 155$ lb, the scale delivers 10 readings per second, and each reading has measurement noise with standard deviation $1$ lb, so variance $R = 1\ \text{lb}^2$. The first five readings are
    """)
    return


@app.cell(hide_code=True)
def _(mo, scale_z):
    _avg4 = scale_z[:4].mean()
    _z5 = scale_z[4]
    mo.md(rf"""
    $$z_1, \ldots, z_5 = {scale_z[0]:.2f},\ {scale_z[1]:.2f},\ {scale_z[2]:.2f},\ {scale_z[3]:.2f},\ {scale_z[4]:.2f}\ \text{{lb}}.$$

    After four readings the cumulative average is $\hat x_4 = {_avg4:.2f}$ lb. By Chapter 6, the error of an average of four readings has variance $R/4 = 0.25\ \text{{lb}}^2$. Because the weight does not change, our prediction for the fifth step is the previous estimate, $\hat x_5^- = \hat x_4$, with error variance $P_5^- = 0.25\ \text{{lb}}^2$. The cumulative average combines it with $z_5$ using $\alpha = 1/5$:

    $$\hat x_5 = \hat x_5^- + \tfrac15\,(z_5 - \hat x_5^-) = {_avg4:.2f} + \tfrac15\,({_z5:.2f} - {_avg4:.2f}) = {_avg4 + (_z5 - _avg4) / 5:.2f}\ \text{{lb}}.$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here is an intuitive reason why $1/5$ is the right gain. The prediction has one quarter of the measurement's variance, so it is "worth" four readings and deserves four times the weight: weights $4/5$ and $1/5$. Notice that the measurement's weight can be written as

    $$\frac15 = \frac{0.25}{0.25 + 1} = \frac{P_5^-}{P_5^- + R},$$

    the prediction's variance divided by the total. In this chapter we turn this intuition into a theorem, make precise what "right" means, and find out when it fails.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch7-sec-random-quantities-in-lowercase -->
    ## Random Quantities in Lowercase

    In Chapters 4–6, random variables were written in uppercase ($X$, $Y$) and their values in lowercase ($x$, $y$). From here on we adopt the convention of the filtering literature instead:

    - The symbols $x_k$, $z_k$, $v_k$, $\hat x_k$, $\hat x_k^-$, $e_k$, $e_k^-$ denote {term}`random variables <random variable>`: functions on a {term}`probability space` $(\Omega, \mathcal F, \mathbb P)$. The same symbols also denote the values these functions take at the outcome that actually occurred, and the context makes clear which is meant. For example, $\mathbb E[z_5]$ treats $z_5$ as a random variable, while "$z_5 = 155.91$" reports its observed value.
    - Uppercase letters such as $P_k$, $P_k^-$, and $R$ (and later $Q$ and $S_k$) are *not* random: they are numbers, namely variances. The gain $\alpha$ is also a number. This is the reason for the switch: Kalman filter texts reserve uppercase letters for variances (which become matrices in Part III), so random quantities must be written in lowercase.
    - A number $c$ can be regarded as the constant random variable $\omega \mapsto c$, with $\mathbb E c = c$ and $\operatorname{Var} c = 0$, so all of Chapter 6's rules apply to it. A true weight $x$ that does not change is such a constant.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch7-sec-setting-up-the-problem -->
    ## Setting Up the Problem

    We have two sources of information about the same unknown quantity $x$ (a constant or a random variable): a prediction $\hat x^-$, such as the previous estimate, and a measurement $z$. Each is the truth plus an error. To talk about these errors we name them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// note | 📖 **Definition**
    <u>**Estimation error**</u>

    The estimation error of an {term}`estimate` $\hat x$ of a quantity $x$ (both random variables on the same probability space) is the random variable
    $$e := \hat x - x.$$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A positive error means the estimate is too high. The prediction's estimation error is the *prediction error* $e^- := \hat x^- - x$, and the measurement's is the {term}`measurement noise` $v = z - x$ of Chapter 5. So

    $$\hat x^- = x + e^-, \qquad z = x + v.$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// note | 📖 **Definition**
    <u>**Error variance**</u>

    The error variance of an {term}`estimate` $\hat x$ of a quantity $x$ is the {term}`variance` of its {term}`estimation error`,
    $$P := \operatorname{Var}(\hat x - x),$$
    defined whenever this variance is finite.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Since $\mathbb E[e^2] = \operatorname{Var} e + (\mathbb E e)^2$ (Chapter 6), an estimate whose error has mean zero has error variance $P = \mathbb E[e^2]$, its {term}`mean squared error`. Throughout this chapter we assume:

    - **(A1) Zero-mean errors:** $\mathbb E e^- = 0$ and $\mathbb E v = 0$.
    - **(A2) Known, finite variances:** $\operatorname{Var} e^- = P^-$ and $\operatorname{Var} v = R$ are known numbers with $P^- \ge 0$, $R \ge 0$, and $P^- + R > 0$.
    - **(A3) Uncorrelated errors:** $\operatorname{Cov}(e^-, v) = 0$.

    Independence of $e^-$ and $v$ implies (A3) (Chapter 6), but (A3) is weaker, and it is all we need. Nothing is assumed about the *shape* of the distributions: only means, variances, and one covariance appear.

    We look for an estimate of the form

    $$\hat x = (1 - \alpha)\,\hat x^- + \alpha\, z = \hat x^- + \alpha\,(z - \hat x^-)$$

    for some number $\alpha$. The difference $z - \hat x^-$ is the {term}`innovation`, and $\alpha$ has a name.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// note | 📖 **Definition**
    <u>**Gain**</u>

    The gain of an update of the form $\hat x = \hat x^- + \alpha\,(z - \hat x^-)$ is the number $\alpha$ by which it multiplies the {term}`innovation` $z - \hat x^-$.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Why restrict ourselves to this form? Any estimate built linearly from the two sources is $a\hat x^- + bz$ for some numbers $a, b$. The next lemma shows that requiring the estimate to be right on average, whatever the true weight is, forces $a + b = 1$, which is exactly the form above.

    /// admonition | 📐 **Lemma (Unbiased Combinations)**
        attrs: {class: lemma, id: ch7-lem-unbiased-combinations}
    Assume (A1) and let $x$ be a constant. For numbers $a, b$, the estimate $a\hat x^- + bz$ satisfies $\mathbb E[a\hat x^- + bz] = x$ for every possible value $x \in \mathbb R$ if and only if $a + b = 1$. In that case $a\hat x^- + bz = \hat x^- + b\,(z - \hat x^-)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    By linearity of expectation and (A1),
    $$\mathbb E[a\hat x^- + bz] = a\,(x + \mathbb E e^-) + b\,(x + \mathbb E v) = (a + b)\,x.$$
    If $a + b = 1$, this equals $x$ for every $x$. Conversely, if it equals $x$ for every $x$, then taking $x = 1$ gives $a + b = 1$. Finally, $a = 1 - b$ gives $a\hat x^- + bz = \hat x^- + b\,(z - \hat x^-)$. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// admonition | 📐 **Lemma (Error of the Update)**
        attrs: {class: lemma, id: ch7-lem-error-of-the-update}
    For every number $\alpha$, the estimation error of $\hat x = \hat x^- + \alpha\,(z - \hat x^-)$ is
    $$e = (1 - \alpha)\,e^- + \alpha\, v.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Substitute $\hat x^- = x + e^-$ and $z = x + v$:
    $$\hat x - x = (1 - \alpha)(x + e^-) + \alpha\,(x + v) - x = (1 - \alpha)\,e^- + \alpha\, v,$$
    because $(1 - \alpha)x + \alpha x - x = 0$. $\blacksquare$
    ///

    The true value $x$ cancels: the error of the combination depends only on the errors of the two sources.

    /// admonition | 📐 **Theorem (Zero-Mean Error for Every Gain)**
        attrs: {class: theorem, id: ch7-thm-zero-mean-error-for-every-gain}
    Assume (A1). For every $\alpha \in \mathbb R$, the error of $\hat x = \hat x^- + \alpha\,(z - \hat x^-)$ has mean zero: $\mathbb E e = 0$. In particular, when $x$ is a constant, $\hat x$ is an {term}`unbiased` estimator of $x$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    By the previous lemma and linearity of expectation, $\mathbb E e = (1 - \alpha)\,\mathbb E e^- + \alpha\,\mathbb E v = 0$. If $x$ is constant, $\mathbb E\hat x = x + \mathbb E e = x$. $\blacksquare$
    ///

    So the mean cannot tell us which gain to choose: every gain is right on average. The variance can.

    /// admonition | 📐 **Lemma (Error Variance of the Update)**
        attrs: {class: lemma, id: ch7-lem-error-variance-of-the-update}
    Assume (A1)–(A3). For every $\alpha \in \mathbb R$, the error variance of $\hat x = \hat x^- + \alpha\,(z - \hat x^-)$ is
    $$P(\alpha) := \operatorname{Var} e = (1 - \alpha)^2 P^- + \alpha^2 R.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    By Chapter 6's rule for the variance of a weighted sum,
    $$\operatorname{Var}\big((1 - \alpha)\,e^- + \alpha\, v\big) = (1 - \alpha)^2 P^- + \alpha^2 R + 2\alpha(1 - \alpha)\operatorname{Cov}(e^-, v),$$
    and the last term is zero by (A3). $\blacksquare$
    ///

    The two terms pull in opposite directions. The prediction's share $(1 - \alpha)^2 P^-$ shrinks as $\alpha$ moves toward $1$ (trusting the measurement), while the measurement's share $\alpha^2 R$ shrinks as $\alpha$ moves toward $0$ (trusting the prediction). The best gain balances them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch7-sec-completing-the-square -->
    ## Completing the Square

    $P(\alpha)$ is a quadratic polynomial in $\alpha$ with a positive leading coefficient, so its graph is a parabola that opens upward. We find its lowest point with algebra alone, by completing the square. First, the property we are after:

    /// note | 📖 **Definition**
    <u>**Optimal gain**</u>

    Given the variances of the prediction error and of the measurement noise and their covariance, an optimal gain is a {term}`gain` $\alpha^*$ whose resulting {term}`error variance` is no larger than that of any other gain: $P(\alpha^*) \le P(\alpha)$ for every $\alpha \in \mathbb R$.
    ///

    /// admonition | 📐 **Theorem (Optimal Gain)**
        attrs: {class: theorem, id: ch7-thm-optimal-gain}
    Assume (A1)–(A3), and define
    $$\alpha^* := \frac{P^-}{P^- + R}, \qquad P^* := \frac{P^- R}{P^- + R}.$$
    Then:

    1. For every $\alpha \in \mathbb R$, $\;P(\alpha) = (P^- + R)\,(\alpha - \alpha^*)^2 + P^*$.
    2. $\alpha^*$ is the unique optimal gain, and its error variance is $P(\alpha^*) = P^*$.
    3. $P^* = (1 - \alpha^*)\,P^- = \alpha^* R$.
    4. If $P^- > 0$ and $R > 0$, then $\dfrac{1}{P^*} = \dfrac{1}{P^-} + \dfrac{1}{R}$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    1. Expanding, $P(\alpha) = (P^- + R)\,\alpha^2 - 2P^-\alpha + P^-$. Since $P^- = (P^- + R)\,\alpha^*$, adding and subtracting $(P^- + R)\,\alpha^{*2}$ gives
       $$P(\alpha) = (P^- + R)\big(\alpha^2 - 2\alpha\alpha^* + \alpha^{*2}\big) + P^- - (P^- + R)\,\alpha^{*2} = (P^- + R)(\alpha - \alpha^*)^2 + P^- - \frac{(P^-)^2}{P^- + R}.$$
       The constant is $\dfrac{P^-(P^- + R) - (P^-)^2}{P^- + R} = \dfrac{P^- R}{P^- + R} = P^*$.
    2. Because $P^- + R > 0$ and $(\alpha - \alpha^*)^2 \ge 0$, item 1 gives $P(\alpha) \ge P^* = P(\alpha^*)$ for every $\alpha$, so $\alpha^*$ is optimal. If $\alpha \ne \alpha^*$, then $(\alpha - \alpha^*)^2 > 0$, so $P(\alpha) > P(\alpha^*)$ and $\alpha$ is not optimal. Hence $\alpha^*$ is the only optimal gain.
    3. $1 - \alpha^* = R/(P^- + R)$, so $(1 - \alpha^*)P^- = P^- R/(P^- + R) = P^*$, and $\alpha^* R = P^- R/(P^- + R) = P^*$.
    4. $\dfrac{1}{P^-} + \dfrac{1}{R} = \dfrac{R + P^-}{P^- R} = \dfrac{1}{P^*}$. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each part of the theorem says something useful:

    - **Weights.** The optimal estimate is $\hat x = \frac{R}{P^- + R}\,\hat x^- + \frac{P^-}{P^- + R}\,z$: each source is weighted in proportion to the *other* source's variance, so the noisier source gets less weight. This is the intuition from the concrete example, now proven.
    - **Shrinking variance.** Item 3, $P^* = (1 - \alpha^*)P^-$, says the update multiplies the prediction's error variance by $1 - \alpha^*$. This is the form used in every Kalman filter.
    - **Precisions add.** The reciprocal of a variance is often called a *precision*. Item 4 says the precision of the combination is the sum of the precisions of its sources.
    - **Cost of any other gain.** Item 1 measures exactly how much worse a gain $\alpha \ne \alpha^*$ is: $(P^- + R)(\alpha - \alpha^*)^2$. We will use this to analyze wrong variances below.

    /// admonition | 📐 **Corollary (Better Than Either Source)**
        attrs: {class: corollary, id: ch7-cor-better-than-either-source}
    Assume (A1)–(A3) with $P^- > 0$ and $R > 0$. Then $0 < \alpha^* < 1$ and $P^* < \min(P^-, R)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Since $0 < P^- < P^- + R$, we have $0 < \alpha^* < 1$. Then $P^* = (1 - \alpha^*)P^- < P^-$ because $1 - \alpha^* < 1$ and $P^- > 0$, and $P^* = \alpha^* R < R$ because $\alpha^* < 1$ and $R > 0$. $\blacksquare$
    ///

    **Limiting cases.** The formulas behave as common sense demands:

    | Situation | Optimal gain | Error variance | Meaning |
    |:---|:---:|:---:|:---|
    | $R = 0$ (perfect measurement) | $\alpha^* = 1$ | $P^* = 0$ | copy the measurement |
    | $P^- = 0$ (perfect prediction) | $\alpha^* = 0$ | $P^* = 0$ | ignore the measurement |
    | $P^- = R$ | $\alpha^* = \tfrac12$ | $P^* = \tfrac12 P^-$ | plain average; variance halves |
    | $R$ much larger than $P^-$ | $0 < \alpha^* < P^-/R$ | $P^- - P^* < (P^-)^2/R$ | measurement nearly ignored |
    | $P^-$ much larger than $R$ | $0 < 1 - \alpha^* < R/P^-$ | $R - P^* < R^2/P^-$ | measurement nearly copied |

    The bounds in the last two rows follow from $\alpha^* = P^-/(P^- + R) < P^-/R$, $1 - \alpha^* = R/(P^- + R) < R/P^-$, and item 3: $P^- - P^* = \alpha^* P^-$ and $R - P^* = (1 - \alpha^*)R$. The last row explains first-measurement initialization: when we know essentially nothing before the first reading, the optimal estimate is essentially the reading itself.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// tip | **The calculus route**
    If you know derivatives ([Appendix C: Derivatives](#appc-sec-derivatives)), you can also set $P'(\alpha) = -2(1 - \alpha)P^- + 2\alpha R$ to zero, which gives $\alpha = \alpha^*$, and note $P''(\alpha) = 2(P^- + R) > 0$. Completing the square gives more: item 1 is an exact formula for the penalty of every other gain, not just the location of the minimum.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **(A1) Zero-mean errors.** If either source has a bias, the estimate inherits a weighted bias, and no gain removes it. See *Bias* below.
    - **(A2) Known variances.** If $P^-$ or $R$ is wrong, the estimate is still zero-mean, but the gain is not optimal and the reported $P^*$ is wrong. See *Mis-specified Variances* below. [Chapter 9](#ch9-sec-estimating-r) shows how to obtain $R$ and $P^-$.
    - **(A3) Uncorrelated errors.** If $\operatorname{Cov}(e^-, v) \ne 0$, the optimal gain changes, and $P^*$ may understate the true error variance. See *Correlated Errors* below.
    - **"Optimal" means optimal among gains.** The theorem compares only estimates of the form $\hat x^- + \alpha(z - \hat x^-)$. A nonlinear rule can do better when the errors are not normal; see [Chapter 8](#ch8-sec-when-the-noise-is-not-normal).
    - **No distributional assumption.** The theorem holds for any error distributions with the stated means, variances, and covariance.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch7-sec-seeing-the-combination -->
    ## Seeing the Combination

    Use the sliders to set $P^-$ and $R$. The left panel shows the error variance $P(\alpha)$ and its two parts; its lowest point is at $\alpha^*$. The right panel shows, for a true weight of $155$ lb, the distributions of the prediction $\hat x^-$, the measurement $z$, and the optimal estimate $\hat x$, assuming normal errors[^normal-for-drawing]. The markers on the horizontal axis show one simulated draw of each: the estimate always lies between the prediction and the measurement, closer to the more reliable one, and its distribution is always the narrowest.

    [^normal-for-drawing]: Drawing a density requires choosing a distribution, so the figure takes $e^-$ and $v$ to be independent and normal. Then $\hat x$ is normal too, by [Chapter 5](#ch5-cor-linear-combinations-of-independent-normals)'s corollary on linear combinations of independent normal random variables. The theorem itself does not use normality.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pm_slider = mo.ui.slider(
        0.1, 4.0, 0.1, value=2.0, label=r"Prediction error variance $P^-$ (lb$^2$)", show_value=True
    )
    r_slider = mo.ui.slider(
        0.1, 4.0, 0.1, value=1.0, label=r"Measurement noise variance $R$ (lb$^2$)", show_value=True
    )
    return pm_slider, r_slider


@app.cell
def _(np):
    # jb: include=false
    combo_draw = np.random.default_rng(3).standard_normal(2)
    return (combo_draw,)


@app.cell(hide_code=True)
def _(combo_draw, graphic, mo, normal_pdf, np, plt, pm_slider, r_slider):
    _Pm, _R = pm_slider.value, r_slider.value
    _a_star = _Pm / (_Pm + _R)
    _P_star = _Pm * _R / (_Pm + _R)
    _alpha = np.linspace(-0.25, 1.25, 301)

    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(10, 3.9))
    _ax1.plot(_alpha, (1 - _alpha) ** 2 * _Pm, color="red", linestyle=":", label=r"$(1-\alpha)^2P^-$")
    _ax1.plot(_alpha, _alpha**2 * _R, color="C0", linestyle="--", label=r"$\alpha^2R$")
    _ax1.plot(_alpha, (1 - _alpha) ** 2 * _Pm + _alpha**2 * _R, color="C1", linewidth=2, label=r"$P(\alpha)$")
    _ax1.plot([_a_star], [_P_star], "o", color="C1")
    _ax1.axvline(_a_star, color="gray", linewidth=0.8)
    _ax1.annotate(rf"$\alpha^*={_a_star:.2f}$", (_a_star, _P_star), textcoords="offset points", xytext=(6, -16))
    _ax1.set_ylim(0, 1.6 * max(_Pm, _R))
    _ax1.set_xlabel(r"gain $\alpha$")
    _ax1.set_ylabel(r"error variance (lb$^2$)")
    _ax1.set_title("Error variance versus gain", style="italic")
    _ax1.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax1.legend(loc="upper center", fontsize=8)

    _x = 155.0
    _s = np.sqrt(max(_Pm, _R))
    _grid = np.linspace(_x - 4 * _s, _x + 4 * _s, 600)
    _xm = _x + np.sqrt(_Pm) * combo_draw[0]
    _zz = _x + np.sqrt(_R) * combo_draw[1]
    _xh = _xm + _a_star * (_zz - _xm)
    _ax2.plot(_grid, normal_pdf(_grid, _x, _Pm), color="red", linestyle=":", label=r"prediction $\hat x^-$")
    _ax2.plot(_grid, normal_pdf(_grid, _x, _R), color="C0", linestyle="--", label=r"measurement $z$")
    _ax2.plot(_grid, normal_pdf(_grid, _x, _P_star), color="C1", linewidth=2, label=r"estimate $\hat x$")
    _ax2.axvline(_x, color="black", linewidth=1, label="true weight $x$")
    _ax2.plot([_xm], [0], "D", color="red", clip_on=False, zorder=5)
    _ax2.plot([_zz], [0], "o", markerfacecolor="none", markeredgecolor="black", markeredgewidth=1.5, clip_on=False, zorder=5)
    _ax2.plot([_xh], [0], "o", color="C1", clip_on=False, zorder=6)
    _ax2.set_ylim(bottom=0)
    _ax2.set_xlabel("weight (lb)")
    _ax2.set_ylabel(r"density (1/lb)")
    _ax2.set_title("Distributions of the two sources and the estimate", style="italic")
    _ax2.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax2.legend(loc="upper right", fontsize=8)
    _fig.tight_layout()

    _out = mo.vstack([
        mo.hstack([pm_slider, r_slider], justify="start", gap=2),
        graphic(_fig),
        mo.md(
            rf"$\alpha^* = {_a_star:.3f}$, $\;P^* = {_P_star:.3f}\ \text{{lb}}^2$, "
            rf"standard deviations: prediction ${np.sqrt(_Pm):.2f}$ lb, measurement ${np.sqrt(_R):.2f}$ lb, "
            rf"estimate ${np.sqrt(_P_star):.2f}$ lb."
        ),
    ])
    plt.close(_fig)
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch7-sec-checking-by-simulation -->
    ## Checking by Simulation

    A proof settles the question, but a simulation is a cheap guard against algebra slips and misread assumptions. The simulation below draws $N = 20{,}000$ independent pairs $(e^-, v)$ with the variances $P^-$ and $R$ chosen above, forms the error $e = (1-\alpha)e^- + \alpha v$ for gains $\alpha = 0, 0.05, \ldots, 1$, and compares the sample variance of $e$ with the formula $P(\alpha)$.

    - Choose **uniform** errors to see that the result does not depend on normality: only means, variances, and the covariance matter.
    - Move the **correlation** slider away from $0$ to preview *Correlated Errors* below: the simulated variances then follow a different curve, and the minimum moves away from $P^-/(P^- + R)$.
    - The **comparison gain** adds a second histogram, so you can see how much wider the error distribution of a non-optimal gain is.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mc_shape = mo.ui.dropdown(options=["normal", "uniform"], value="normal", label="Error distribution")
    mc_rho = mo.ui.slider(
        -0.9, 0.9, 0.1, value=0.0, label=r"Correlation of $e^-$ and $v$", show_value=True
    )
    mc_alpha = mo.ui.slider(0.0, 1.0, 0.05, value=0.9, label=r"Comparison gain $\alpha$", show_value=True)
    return mc_alpha, mc_rho, mc_shape


@app.cell
def _(np):
    # jb: include=false
    _rng = np.random.default_rng(7)
    mc_normal = _rng.standard_normal((2, 20000))
    mc_uniform = (_rng.uniform(size=(2, 20000)) - 0.5) * np.sqrt(12.0)  # mean 0, variance 1
    return mc_normal, mc_uniform


@app.cell(hide_code=True)
def _(
    graphic,
    mc_alpha,
    mc_normal,
    mc_rho,
    mc_shape,
    mc_uniform,
    mo,
    np,
    plt,
    pm_slider,
    r_slider,
):
    _Pm, _R, _rho = pm_slider.value, r_slider.value, mc_rho.value
    _g = mc_normal if mc_shape.value == "normal" else mc_uniform
    _em = np.sqrt(_Pm) * _g[0]
    _v = np.sqrt(_R) * (_rho * _g[0] + np.sqrt(1 - _rho**2) * _g[1])
    _c = _rho * np.sqrt(_Pm * _R)
    _D = _Pm + _R - 2 * _c
    _a_opt = (_Pm - _c) / _D
    _a_naive = _Pm / (_Pm + _R)

    _grid = np.linspace(0, 1, 21)
    _sample_var = np.array([((1 - _a) * _em + _a * _v).var() for _a in _grid])
    _fine = np.linspace(0, 1, 201)
    _theory = (1 - _fine) ** 2 * _Pm + _fine**2 * _R + 2 * _fine * (1 - _fine) * _c
    _naive = (1 - _fine) ** 2 * _Pm + _fine**2 * _R

    _e_opt = (1 - _a_opt) * _em + _a_opt * _v
    _e_cmp = (1 - mc_alpha.value) * _em + mc_alpha.value * _v

    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(10, 3.9))
    _lim = 4 * np.sqrt(max(_Pm, _R))
    _bins = np.linspace(-_lim, _lim, 61)
    _ax1.hist(_e_cmp, bins=_bins, density=True, color="gray", alpha=0.5,
              label=rf"$\alpha={mc_alpha.value:.2f}$: var $={_e_cmp.var():.3f}$")
    _ax1.hist(_e_opt, bins=_bins, density=True, color="C1", alpha=0.6,
              label=rf"optimal $\alpha={_a_opt:.2f}$: var $={_e_opt.var():.3f}$")
    _ax1.set_xlabel(r"estimation error $e$ (lb)")
    _ax1.set_ylabel("density (1/lb)")
    _ax1.set_title("Histogram of simulated errors", style="italic")
    _ax1.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax1.legend(fontsize=8, loc="upper right")

    _ax2.plot(_fine, _theory, color="C1", linewidth=2, label=r"formula with covariance $c$")
    if _rho != 0:
        _ax2.plot(_fine, _naive, color="gray", linestyle="--", label=r"formula ignoring $c$")
    _ax2.plot(_grid, _sample_var, "o", markerfacecolor="none", markeredgecolor="black", label="simulation")
    _ax2.axvline(_a_opt, color="C1", linewidth=0.8)
    _ax2.set_xlabel(r"gain $\alpha$")
    _ax2.set_ylabel(r"error variance (lb$^2$)")
    _ax2.set_title("Sample variance versus formula", style="italic")
    _ax2.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax2.legend(fontsize=8, loc="upper center")
    _fig.tight_layout()

    _out = mo.vstack([
        mo.hstack([pm_slider, r_slider], justify="start", gap=2),
        mo.hstack([mc_shape, mc_rho, mc_alpha], justify="start", gap=2),
        graphic(_fig),
        mo.md(
            rf"Covariance $c = {_c:.3f}$; optimal gain ${_a_opt:.3f}$ "
            rf"(the uncorrelated formula would give $P^-/(P^-+R) = {_a_naive:.3f}$); "
            rf"largest gap between simulation and formula: ${np.max(np.abs(_sample_var - ((1 - _grid) ** 2 * _Pm + _grid**2 * _R + 2 * _grid * (1 - _grid) * _c))):.3f}\ \text{{lb}}^2$."
        ),
    ])
    plt.close(_fig)
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch7-sec-the-cumulative-average-was-optimal -->
    ## The Cumulative Average Was Optimal

    Now apply the theorem step by step. Suppose the true weight $x$ is constant and the scale delivers measurements

    $$z_k = x + v_k, \qquad k = 1, 2, 3, \ldots,$$

    where the noises $v_k$ have mean $0$, the same variance $R > 0$, and are pairwise uncorrelated: $\operatorname{Cov}(v_i, v_j) = 0$ for $i \ne j$. The filter uses first-measurement initialization, $\hat x_1 := z_1$. For $k \ge 2$ its prediction is the previous estimate, $\hat x_k^- := \hat x_{k-1}$, because nothing changes between steps, and its update is

    $$\hat x_k := \hat x_k^- + \alpha_k\,(z_k - \hat x_k^-).$$

    We write $e_k := \hat x_k - x$ and $e_k^- := \hat x_k^- - x$ for the estimation and prediction errors at step $k$, and $P_k$ and $P_k^-$ for their error variances. Which gains $\alpha_k$ do we get if, at every step, we choose the optimal gain for that step? To apply the theorem we must check (A3) at each step. For that we use the **linearity of covariance**: applying item 3 of Chapter 6's theorem on the properties of covariance once per term (induction on $n$) gives, for random variables with finite second moments and numbers $a_i$,
    $$\operatorname{Cov}\Big(\sum_{i=1}^n a_i X_i,\; W\Big) = \sum_{i=1}^n a_i \operatorname{Cov}(X_i, W),$$
    and likewise in the second argument.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// admonition | 📐 **Theorem (Optimal Gains for a Constant)**
        attrs: {class: theorem, id: ch7-thm-optimal-gains-for-a-constant}
    Under the assumptions above, if each gain $\alpha_k$ ($k \ge 2$) is chosen as the optimal gain for step $k$, then for every $k \ge 1$
    $$\alpha_k = \frac1k \ (k \ge 2), \qquad P_k = \frac Rk, \qquad e_k = \frac1k\sum_{i=1}^k v_i, \qquad \hat x_k = \frac1k\sum_{i=1}^k z_i.$$
    So the optimal filter is exactly the Introduction's cumulative average.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    For $k \ge 1$ let $S(k)$ be the statement "$P_k = R/k$ and $e_k = \frac1k\sum_{i=1}^k v_i$". We prove $S(k)$ for all $k \ge 1$ by induction (Chapter 2, applied to $k - 1 \in \mathbb N$).

    *Base case.* $\hat x_1 = z_1$, so $e_1 = z_1 - x = v_1$ and $P_1 = \operatorname{Var} v_1 = R$. This is $S(1)$.

    *Inductive step.* Let $k \ge 2$ and assume $S(k-1)$. Since $\hat x_k^- = \hat x_{k-1}$ and $x$ does not change, $e_k^- = e_{k-1}$. Check (A1)–(A3) for the pair $(\hat x_k^-, z_k)$:

    - (A1): $\mathbb E e_k^- = \frac{1}{k-1}\sum_{i<k}\mathbb E v_i = 0$ and $\mathbb E v_k = 0$.
    - (A2): $P_k^- = P_{k-1} = R/(k-1)$ and $\operatorname{Var} v_k = R$.
    - (A3): by the linearity of covariance, $\operatorname{Cov}(e_k^-, v_k) = \frac{1}{k-1}\sum_{i<k}\operatorname{Cov}(v_i, v_k) = 0$.

    The Optimal Gain theorem therefore gives
    $$\alpha_k = \frac{P_k^-}{P_k^- + R} = \frac{R/(k-1)}{R/(k-1) + R} = \frac{1}{1 + (k-1)} = \frac1k, \qquad P_k = (1 - \alpha_k)\,P_k^- = \frac{k-1}{k}\cdot\frac{R}{k-1} = \frac Rk,$$
    and the Error of the Update lemma gives
    $$e_k = \Big(1 - \frac1k\Big)e_{k-1} + \frac1k v_k = \frac{k-1}{k}\cdot\frac{1}{k-1}\sum_{i<k} v_i + \frac1k v_k = \frac1k\sum_{i=1}^k v_i.$$
    This is $S(k)$. Finally, $\hat x_k = x + e_k = \frac1k\sum_{i=1}^k (x + v_i) = \frac1k\sum_{i=1}^k z_i$. $\blacksquare$
    ///

    Three remarks:

    - The error variance $R/k$ is Chapter 6's variance $\sigma^2/k$ of the {term}`sample mean`, as it must be, since $\hat x_k$ *is* the sample mean.
    - The gains $1/k$ do not depend on $R$ at all: a noisier scale needs the same gains, and only the reported variance $P_k$ changes.
    - With first-measurement initialization, the first step is also of the update form: $\hat x_1 = z_1 = \hat x_1^- + 1\cdot(z_1 - \hat x_1^-)$ for any prediction $\hat x_1^-$, so $\alpha_1 = 1 = 1/1$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The theorem chooses each gain greedily, one step at a time. Could a cleverer combination of all $k$ readings at once do better? No. Among all weighted sums of the readings that are unbiased whatever $x$ is, which by the argument of the Unbiased Combinations lemma are exactly those whose weights add up to $1$, the plain average has the smallest error variance.

    /// admonition | 📐 **Theorem (The Average Is the Best Unbiased Linear Combination)**
        attrs: {class: theorem, id: ch7-thm-the-average-is-the-best-unbiased-linear-combination}
    Under the assumptions above, let $w_1, \ldots, w_k$ be numbers with $\sum_{i=1}^k w_i = 1$, and let $\tilde x := \sum_{i=1}^k w_i z_i$. Then $\tilde x$ has error $\sum_i w_i v_i$ with mean zero and variance
    $$\operatorname{Var}(\tilde x - x) = R\sum_{i=1}^k w_i^2 \;\ge\; \frac Rk,$$
    with equality if and only if $w_i = 1/k$ for every $i$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Since the weights add up to $1$, $\tilde x - x = \sum_i w_i(x + v_i) - x = \sum_i w_i v_i$, which has mean zero by linearity. The $v_i$ are pairwise uncorrelated, so Bienaymé's corollary (Chapter 6) gives $\operatorname{Var}(\tilde x - x) = R\sum_i w_i^2$. The computation in the proof of Chapter 6's corollary *For a Constant Value, Averaging Beats the EMA* shows that weights adding up to $1$ satisfy $\sum_i w_i^2 = \sum_i (w_i - 1/k)^2 + 1/k \ge 1/k$, with equality if and only if every $w_i = 1/k$. $\blacksquare$
    ///

    Chapter 6 used the same computation to show that, for a constant value, the EMA's weights do worse than equal weights. In the long run the gap is large: $R/k$ tends to $0$, while the EMA's error variance tends to $\frac{\alpha}{2-\alpha}R > 0$. For a truly constant weight, the EMA throws information away.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    The two theorems above rest on four assumptions:

    - **The true value is constant.** If $x$ drifts, the gain $1/k$ shrinks toward $0$ and the estimate stops following it. This is why the Introduction switched to the EMA. [Chapter 9](#ch9-sec-process-noise) models the drift as process noise and shows that the optimal gain then levels off at a positive value, which turns the optimal filter into an EMA.
    - **The noise is uncorrelated over time.** If you sway slowly, neighboring readings err in the same direction. The average is still unbiased, but its error variance is larger than the reported $R/k$, so the filter is overconfident (see *Correlated Errors* below).
    - **Every reading has the same variance.** If $\operatorname{Var} v_k = R_k$ varies, the same induction with $\alpha_k = P_{k-1}/(P_{k-1} + R_k)$ and item 4 of the Optimal Gain theorem gives $1/P_k = \sum_{i \le k} 1/R_i$: the optimal filter is no longer the plain average but weights each reading in proportion to $1/R_i$.
    - **First-measurement initialization.** If the filter starts from a guess $\hat x_0$ with known error variance instead, the gains change slightly; [Chapter 9](#ch9-thm-no-process-noise) shows that the guess then acts like a number of extra "virtual" readings.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch7-sec-cumulative-average-versus-ema -->
    ### Cumulative Average Versus EMA

    The figure runs both filters on the Introduction's 30 scale readings. The bands show $\pm 2$ standard deviations of each estimate's error, from $P_k = R/k$ for the cumulative average and from Chapter 6's exact formula for the EMA. The right panel compares the two error variances with a Monte Carlo estimate from 2,000 simulated runs. Whatever $\alpha$ you choose, the EMA's error variance eventually stops shrinking, while the cumulative average's keeps falling like $1/k$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    seq_alpha = mo.ui.slider(0.02, 0.98, 0.02, value=0.2, label=r"EMA gain $\alpha$", show_value=True)
    return (seq_alpha,)


@app.cell
def _(np, scale_x):
    # jb: include=false
    seq_mc_z = scale_x + np.random.default_rng(11).normal(0.0, 1.0, (2000, 30))
    return (seq_mc_z,)


@app.cell(hide_code=True)
def _(
    ema_error_variance,
    ema_filter,
    graphic,
    mo,
    np,
    plt,
    scale_R,
    scale_t,
    scale_x,
    scale_z,
    seq_alpha,
    seq_mc_z,
):
    _k = np.arange(1, scale_z.size + 1)
    _avg = np.cumsum(scale_z) / _k
    _ema = ema_filter(seq_alpha.value, scale_z)
    _P_avg = scale_R / _k
    _P_ema = ema_error_variance(seq_alpha.value, scale_R, _k)

    _mc_avg = np.cumsum(seq_mc_z, axis=1) / _k
    _mc_ema = ema_filter(seq_alpha.value, seq_mc_z)
    _mc_var_avg = ((_mc_avg - scale_x) ** 2).mean(axis=0)
    _mc_var_ema = ((_mc_ema - scale_x) ** 2).mean(axis=0)

    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(10, 3.9))
    _ax1.plot(scale_t, scale_z, "o", markerfacecolor="none", markeredgecolor="black", label="measurement $z_k$")
    _ax1.axhline(scale_x, color="black", linewidth=1, label="true weight")
    _ax1.plot(scale_t, _avg, color="C1", linewidth=2, label="cumulative average")
    _ax1.fill_between(scale_t, _avg - 2 * np.sqrt(_P_avg), _avg + 2 * np.sqrt(_P_avg), color="C1", alpha=0.2)
    _ax1.plot(scale_t, _ema, color="C2", linewidth=1.5, label=rf"EMA, $\alpha={seq_alpha.value:.2f}$")
    _ax1.fill_between(scale_t, _ema - 2 * np.sqrt(_P_ema), _ema + 2 * np.sqrt(_P_ema), color="C2", alpha=0.15)
    _ax1.set_ylim(scale_x - 3.5, scale_x + 4.5)
    _ax1.set_xlabel("time (s)")
    _ax1.set_ylabel("weight (lb)")
    _ax1.set_title(r"Estimates with $\pm 2$ standard deviation bands", style="italic")
    _ax1.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax1.legend(fontsize=8, loc="upper center", ncol=2)

    _ax2.semilogy(_k, _P_avg, color="C1", linewidth=2, label=r"cumulative average: $R/k$")
    _ax2.semilogy(_k, _P_ema, color="C2", linewidth=1.5, label="EMA: exact formula")
    _ax2.semilogy(_k, _mc_var_avg, "o", color="C1", markersize=3, label="Monte Carlo")
    _ax2.semilogy(_k, _mc_var_ema, "o", color="C2", markersize=3, label="Monte Carlo")
    _ax2.axhline(seq_alpha.value / (2 - seq_alpha.value) * scale_R, color="C2", linestyle=":", linewidth=1,
                 label=r"EMA limit $\frac{\alpha}{2-\alpha}R$")
    _ax2.set_xlabel("step $k$")
    _ax2.set_ylabel(r"error variance (lb$^2$)")
    _ax2.set_title("Error variance versus step", style="italic")
    _ax2.grid(visible=True, alpha=0.9, linewidth=0.4, which="both")
    _ax2.legend(fontsize=8, loc="lower left")
    _fig.tight_layout()

    _out = mo.vstack([
        seq_alpha,
        graphic(_fig),
        mo.md(
            rf"After $k = 30$ readings: cumulative average ${_avg[-1]:.2f}$ lb with error variance "
            rf"$R/30 = {_P_avg[-1]:.3f}\ \text{{lb}}^2$; EMA ${_ema[-1]:.2f}$ lb with error variance "
            rf"${_P_ema[-1]:.3f}\ \text{{lb}}^2$ (${_P_ema[-1] / _P_avg[-1]:.1f}$ times larger)."
        ),
    ])
    plt.close(_fig)
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch7-sec-when-the-assumptions-fail -->
    ## When the Assumptions Fail

    Each assumption of the Optimal Gain theorem can fail in practice. Completing the square, the same tool we used for the theorem, tells us exactly what happens in each case.

    <!-- label: ch7-sec-correlated-errors -->
    ### Correlated Errors

    Keep (A1) and (A2), but let the errors be correlated: $\operatorname{Cov}(e^-, v) = c$. This happens when the prediction and the measurement share a source of error. For example, if you sway slowly, the reading $z_k$ and the earlier readings that built $\hat x_k^-$ err in the same direction ($c > 0$). Another classic cause is double counting: feeding a measurement into the filter that was already used to form the prediction.

    /// admonition | 📐 **Theorem (Optimal Gain With Correlated Errors)**
        attrs: {class: theorem, id: ch7-thm-optimal-gain-with-correlated-errors}
    Assume (A1) and (A2), let $c := \operatorname{Cov}(e^-, v)$, and let $D := P^- + R - 2c$. Then $D = \operatorname{Var}(v - e^-) \ge 0$, and for every $\alpha$
    $$P(\alpha) = (1-\alpha)^2 P^- + \alpha^2 R + 2\alpha(1-\alpha)\,c.$$

    1. If $D > 0$, then $P(\alpha) = D\,(\alpha - \alpha_c)^2 + P_c$ with
    $$\alpha_c := \frac{P^- - c}{P^- + R - 2c}, \qquad P_c := \frac{P^- R - c^2}{P^- + R - 2c},$$
    so $\alpha_c$ is the unique optimal gain, and its error variance is $P_c$.
    2. If $D = 0$, then $P(\alpha) = P^-$ for every $\alpha$: every gain is optimal, and the measurement adds no information.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    By Chapter 6, $\operatorname{Var}(v - e^-) = R + P^- - 2c = D$, and variances are nonnegative. The formula for $P(\alpha)$ is the weighted-sum rule with the covariance term kept. Expanding it,
    $$P(\alpha) = (P^- + R - 2c)\,\alpha^2 - 2(P^- - c)\,\alpha + P^- = D\alpha^2 - 2(P^- - c)\,\alpha + P^-.$$

    1. If $D > 0$, complete the square exactly as before: $P(\alpha) = D(\alpha - \alpha_c)^2 + P^- - (P^- - c)^2/D$, and
       $$P^- - \frac{(P^- - c)^2}{D} = \frac{P^-(P^- + R - 2c) - (P^- - c)^2}{D} = \frac{P^- R - c^2}{D} = P_c.$$
       Uniqueness follows as in the Optimal Gain theorem.
    2. By the Cauchy–Schwarz inequality (Chapter 6), $c^2 \le P^- R$. Now suppose $D = 0$, so $c = (P^- + R)/2$. Then $(P^- + R)^2/4 \le P^- R$, that is, $(P^- - R)^2 \le 0$, so $P^- = R = c$. Hence $P^- - c = 0$, and the expansion above reduces to $P(\alpha) = P^-$. $\blacksquare$
    ///

    With $c = 0$, item 1 is the Optimal Gain theorem again. With correlation, two new things can happen:

    - **The optimal gain can leave $[0, 1]$.** If $c > R$, then $\alpha_c > 1$ (because $P^- - c > P^- + R - 2c$), and the best estimate lies *beyond* the measurement, on the far side from the prediction. If $c > P^-$, then $\alpha_c < 0$. Strongly shared errors make extrapolation, not interpolation, the right move.
    - **Ignoring the correlation makes the filter overconfident.**

    /// admonition | 📐 **Theorem (Ignoring Correlation)**
        attrs: {class: theorem, id: ch7-thm-ignoring-correlation}
    Assume (A1) and (A2) with $\operatorname{Cov}(e^-, v) = c$. If a filter nevertheless uses the gain $\alpha^* = P^-/(P^- + R)$ and reports the error variance $P^* = P^-R/(P^- + R)$, the actual error variance of its estimate is
    $$P(\alpha^*) = P^* + 2\alpha^*(1 - \alpha^*)\,c.$$
    If $c > 0$ and $P^-, R > 0$, the reported variance is too small.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    By the formula above, $P(\alpha^*) = \big[(1-\alpha^*)^2 P^- + \alpha^{*2} R\big] + 2\alpha^*(1-\alpha^*)c$, and the bracket equals $P^*$ by item 1 of the Optimal Gain theorem with $\alpha = \alpha^*$. If $P^-, R > 0$, then $0 < \alpha^* < 1$, so the extra term is positive when $c > 0$. $\blacksquare$
    ///

    For example, with $P^- = R = 1\ \text{lb}^2$ and $c = 0.5\ \text{lb}^2$, the filter uses $\alpha^* = 0.5$ and reports $P^* = 0.5\ \text{lb}^2$, but the actual error variance is $0.5 + 2(0.5)(0.5)(0.5) = 0.75\ \text{lb}^2$. Here the gain happens to be optimal anyway ($\alpha_c = 0.5/1 = 0.5$), but the reported variance is wrong: the two sources contain less independent information than the filter believes. Try it in the simulation above with $P^- = R = 1$ and correlation $0.5$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch7-sec-bias -->
    ### Bias

    Keep (A2) and (A3), but suppose $\mathbb E e^- = b^-$ and $\mathbb E v = b_v$. By linearity the error of the update has mean $(1-\alpha)\,b^- + \alpha\, b_v$, and since its variance is unchanged, its mean squared error is (Chapter 6: MSE equals variance plus squared bias)

    $$\mathbb E[e^2] = P(\alpha) + \big((1-\alpha)\,b^- + \alpha\, b_v\big)^2.$$

    The gain that minimizes this depends on the unknown biases, and no gain removes a bias shared by both sources. Averaging does not help either. If every reading of a constant weight has $\mathbb E v_k = b$, say a scale that reads $0.5$ lb heavy, then the cumulative average has $\mathbb E\hat x_k = x + b$ and

    $$\mathbb E\big[(\hat x_k - x)^2\big] = \frac Rk + b^2 \;\ge\; b^2 \quad\text{for every } k.$$

    A bias must be removed by calibration, or estimated as part of what the filter tracks ([Chapter 11](#ch11-sec-sensor-bias-and-a-drifting-tare) treats sensor bias).

    <!-- label: ch7-sec-mis-specified-variances -->
    ### Mis-specified Variances

    A filter computes its gain from the variances it *believes*. Suppose the true variances are $P^-$ and $R$, satisfying (A1)–(A3), but the filter uses assumed values $\tilde P^-$ and $\tilde R$ with $\tilde P^- + \tilde R > 0$.

    /// admonition | 📐 **Theorem (Cost of a Wrong Gain)**
        attrs: {class: theorem, id: ch7-thm-cost-of-a-wrong-gain}
    Let $\tilde\alpha := \tilde P^-/(\tilde P^- + \tilde R)$. The estimate $\hat x = \hat x^- + \tilde\alpha\,(z - \hat x^-)$ still has zero-mean error, and its actual error variance is
    $$P(\tilde\alpha) = P^* + (P^- + R)\,(\tilde\alpha - \alpha^*)^2 \;\ge\; P^*,$$
    while the filter reports $\tilde P := \tilde P^- \tilde R/(\tilde P^- + \tilde R)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    The Zero-Mean Error theorem holds for every gain, including $\tilde\alpha$. The variance formula is item 1 of the Optimal Gain theorem evaluated at $\alpha = \tilde\alpha$. $\blacksquare$
    ///

    Three consequences:

    - **Small gain errors are cheap.** The penalty grows with the *square* of the gain error. With $P^- = R = 1\ \text{lb}^2$, using $\tilde\alpha = 0.6$ instead of $0.5$ costs only $2(0.1)^2 = 0.02\ \text{lb}^2$ on top of $P^* = 0.5\ \text{lb}^2$.
    - **Only the ratio sets the gain.** Multiplying both $\tilde P^-$ and $\tilde R$ by the same factor leaves $\tilde\alpha$ unchanged but multiplies $\tilde P$ by that factor. A filter can therefore estimate well while reporting a misleading error variance. In the sequential constant-weight problem, the gains $1/k$ do not depend on $R$ at all, so a wrong $\tilde R$ changes only the reported $P_k = \tilde R/k$.
    - **The reported variance can be badly wrong.** With $P^- = R = 1\ \text{lb}^2$ but $\tilde R = 0.25\ \text{lb}^2$ (an overly optimistic datasheet), the filter uses $\tilde\alpha = 0.8$, whose actual error variance is $0.2^2 + 0.8^2 = 0.68\ \text{lb}^2$, but it reports $\tilde P = 0.2\ \text{lb}^2$, claiming to be $3.4$ times more certain than it is. [Chapter 9](#ch9-sec-checking-the-noise-levels) shows how to detect this from the measurements alone.

    <!-- label: ch7-sec-linear-is-not-everything -->
    ### Linear Is Not Everything

    The Optimal Gain theorem compares only estimates of the form $\hat x^- + \alpha(z - \hat x^-)$. It says nothing about nonlinear rules such as "if the reading is more than 5 lb from the prediction, ignore it." When the errors are normal, [Chapter 8](#ch8-cor-the-optimal-gain-is-optimal-among-all-estimators) proves that no rule of any kind beats the optimal gain. When the noise has occasional large outliers, Chapter 8 shows a nonlinear rule that does.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch7-sec-from-alpha-to-the-gain-k-k -->
    ## From $\alpha$ to the Gain $K_k$

    From now on we write $K_k$ for the gain used at step $k$; the letter honors Rudolf Kálmán [@kalman1960]. With the optimal gain, one step of the filter reads:

    $$\begin{aligned}
    K_k &= \frac{P_k^-}{P_k^- + R} && \text{(optimal gain)}\\
    \hat x_k &= \hat x_k^- + K_k\,(z_k - \hat x_k^-) && \text{(update the estimate)}\\
    P_k &= (1 - K_k)\,P_k^- && \text{(update the error variance)}
    \end{aligned}$$

    Notice that $K_k$ and $P_k$ depend only on variances, not on the measured values, so they could be computed before any data arrive. The Introduction's EMA is the special case $K_k = \alpha$ for every $k$, and for a constant weight we proved that the optimal choice is instead $K_k = 1/k$. What is still missing is how to obtain $P_k^-$ from $P_{k-1}$ when the true value *changes* between steps. That is the subject of [Chapter 9](ch9_noise_levels.md).

    /// attention | 🗝️ **Key Idea**
    The optimal gain is the fraction of the total variance that belongs to the prediction: $K_k = P_k^-/(P_k^- + R)$. It is close to $1$ when the prediction is much less certain than the measurement, close to $0$ when it is much more certain, and after the update the error variance shrinks by the factor $1 - K_k$.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch7-sec-summary -->
    ## Summary

    - From this chapter on, lowercase symbols such as $x_k$, $z_k$, $v_k$, $\hat x_k$, and $e_k$ denote random variables, and uppercase $P_k$, $P_k^-$, $R$ denote their (non-random) variances.
    - If the prediction error $e^-$ and the measurement noise $v$ have mean zero, then the update $\hat x = \hat x^- + \alpha(z - \hat x^-)$ has zero-mean error for every gain, and if the errors are also uncorrelated its error variance is $P(\alpha) = (1-\alpha)^2P^- + \alpha^2R$.
    - Completing the square shows that the unique optimal gain is $\alpha^* = P^-/(P^- + R)$, with error variance $P^* = P^-R/(P^- + R) = (1-\alpha^*)P^-$, smaller than both $P^-$ and $R$. Precisions add: $1/P^* = 1/P^- + 1/R$.
    - For a constant weight with uncorrelated, equal-variance noise, the optimal gains are exactly $1/k$, with $P_k = R/k$: the Introduction's cumulative average was optimal, and no unbiased weighted sum of the readings does better.
    - Correlated errors change the optimal gain to $(P^- - c)/(P^- + R - 2c)$, and ignoring them makes the filter overconfident. Biases are not removed by any gain or by averaging. Wrong variances leave the estimate unbiased but cost $(P^- + R)(\tilde\alpha - \alpha^*)^2$ and corrupt the reported variance.
    - We renamed the gain $K_k$: $K_k = P_k^-/(P_k^- + R)$, $\hat x_k = \hat x_k^- + K_k(z_k - \hat x_k^-)$, $P_k = (1 - K_k)P_k^-$.

    <!-- label: ch7-sec-whats-next -->
    ## What's Next

    This chapter described the prediction and the measurement only through means, variances, and a covariance, and it optimized only over gains. [Chapter 8](ch8_bayesian_view.md) takes a different view: it treats the unknown weight itself as a random variable, describes what we know about it by a probability density, and updates that density with Bayes' theorem. The same gain reappears, and we learn when it is the best of *all* possible estimators, not just the best gain.
    """)
    return


if __name__ == "__main__":
    app.run()
