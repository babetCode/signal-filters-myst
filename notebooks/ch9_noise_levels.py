# /// script
# dependencies = [
#     "marimo>=0.25.1",
#     "matplotlib==3.11.2",
#     "numpy==2.5.3",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="9. Noise Levels", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "The Scalar Kalman Filter"
    abbreviations:
      iff: if and only if
      diff: null
      ADC: analog-to-digital converter
      SPS: samples per second
      RMS: root mean square
      EMA: exponential moving average
      NIS: normalized innovation squared
      RMSE: root-mean-square error
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
    from pathlib import Path

    return Path, dedent, mo, np, plt


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

    def chi2_1_pdf(t):
        t = np.asarray(t, dtype=float)
        return np.where(t > 0, np.exp(-t / 2) / np.sqrt(2 * np.pi * np.maximum(t, 1e-300)), 0.0)

    def steady_state(Q, R):
        """Return (p, K_inf, P_inf) for the scalar random-walk Kalman filter."""
        p = (Q + np.sqrt(Q**2 + 4 * Q * R)) / 2
        return p, p / (p + R), p * R / (p + R)

    def nis_interval(N, rng_seed=12, level=0.95):
        """Central interval for the average of N independent chi-squared(1) values (by simulation)."""
        _c = np.random.default_rng(rng_seed).chisquare(N, 200_000) / N
        return tuple(np.percentile(_c, [50 * (1 - level), 50 * (1 + level)]))

    return chi2_1_pdf, nis_interval, normal_pdf, steady_state


@app.cell
def data(Path, np):
    # jb: include=false
    IMAGES_DIR = Path(__file__).parent.parent / "notebooks" / "public"
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # Bathroom scale, the Introduction's 30 readings (seed 1)
    scale_x = 155.0
    scale_z = np.round(scale_x + np.random.default_rng(1).normal(0.0, 1.0, 30), 2)

    # Bathroom scale with a shifting load: 15 s at 10 SPS, random walk with Q = 0.01 lb^2 per step
    shift_Q, shift_R = 0.01, 1.0
    shift_t = np.arange(1, 151) / 10
    shift_x = scale_x + np.cumsum(np.random.default_rng(7).normal(0.0, np.sqrt(shift_Q), shift_t.size))
    shift_z = np.round(shift_x + np.random.default_rng(6).normal(0.0, np.sqrt(shift_R), shift_t.size), 2)

    # Bulking: the Introduction's 28 daily weigh-ins (seed 2)
    bulk_days = np.arange(1, 29)
    bulk_x = 155 + 0.2 * (bulk_days - 1)
    bulk_z = np.round(bulk_x + np.random.default_rng(2).normal(0, 1, 28), 1)
    return (
        IMAGES_DIR,
        bulk_days,
        bulk_x,
        bulk_z,
        scale_x,
        scale_z,
        shift_Q,
        shift_R,
        shift_t,
        shift_x,
        shift_z,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Part I ended with the optimal gain $K_k = P_k^-/(P_k^- + R)$, under the assumption that we *know* the measurement noise variance $R$ and the prediction's error variance $P_k^-$. This chapter answers the Introduction's next question: how do we determine these noise levels?

    $R$ is the easier one: we measure it. $P_k^-$ takes more work, because it depends on how much the true value can change between measurements in ways our prediction does not foresee. Modeling that change as *process noise* with variance $Q$ gives a one-line rule for $P_k^-$, and together with Chapter 7's update it forms the scalar **Kalman filter**. We then prove that in the long run the Kalman filter becomes an exponential moving average, which finally tells us how to choose the EMA's $\alpha$, and we learn to check from the measurements alone whether a filter's noise levels are right.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// important | 🔗 **Prerequisites**
    - [Introduction](introduction.md): the {term}`exponential moving average`, [the alpha filter](#intro-sec-predicting-the-change), [the expected change](#intro-sec-predicting-the-change) $\Delta x_k$, and [the bulking data](#intro-sec-alpha-beta-filter).
    - [Chapter 5](ch5_random_variables.md): the {term}`uniform distribution` and [the theorem that quantization error is nearly uniform](#ch5-thm-quantization-error-is-nearly-uniform), the {term}`normal distribution` and [the density of](#ch5-thm-density-of-ax-b) $aX + b$, [linear combinations of independent normal random variables](#ch5-cor-linear-combinations-of-independent-normals), {term}`independent and identically distributed` random variables, {term}`stochastic processes <stochastic process>`, and [the measurement-noise model](#ch5-sec-the-measurement-noise-model).
    - [Chapter 6](ch6_expectation_and_variance.md): {term}`variance` (including [that of the uniform distribution](#ch6-thm-variances-of-common-distributions)), {term}`covariance` and [its linearity in each argument](#ch6-thm-properties-of-covariance), {term}`uncorrelated` random variables, [Bienaymé's corollary](#ch6-cor-bienayme), the {term}`sample mean` and [its variance](#ch6-thm-mean-and-variance-of-the-sample-mean) $\sigma^2/n$, {term}`unbiased` estimators, and [the EMA's variance](#ch6-thm-ema-of-a-constant-value) $\frac{\alpha}{2-\alpha}\sigma^2$ and [ramp lag](#ch6-thm-ema-on-a-ramp) $c\frac{1-\alpha}{\alpha}$.
    - [Chapter 7](ch7_optimal_alpha.md): {term}`estimation error`, {term}`error variance`, {term}`gain` and {term}`optimal gain`, [the Optimal Gain theorem](#ch7-thm-optimal-gain) (in particular items 1, 3, and 4), [the Error of the Update lemma](#ch7-lem-error-of-the-update), [the optimality of](#ch7-thm-optimal-gains-for-a-constant) $1/k$, [and the gain](#ch7-sec-from-alpha-to-the-gain-k-k) $K_k$.
    - [Chapter 8](ch8_bayesian_view.md): [the normal Bayes filter](#ch8-cor-the-normal-bayes-filter) and [the central limit theorem](#ch8-thm-central-limit-theorem).
    - [Appendix C: Sequences and Limits](#appc-sec-sequences-and-limits) ([geometric convergence](#appc-thm-geometric-series) and [limit laws](#appc-thm-limit-laws-for-sequences)), [Derivatives](#appc-sec-derivatives) and [The Fundamental Theorem of Calculus](#appc-sec-the-fundamental-theorem-of-calculus) (for the $\chi^2$ density, including [integration by parts](#appc-thm-integration-by-parts)), and [Improper Integrals](#appc-sec-improper-integrals).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// attention | 🗝️ **Key Idea**
    $R$ is measured; $Q$ is modeled. The predict step adds $Q$ to the error variance, $P_k^- = P_{k-1} + Q$, and the update step shrinks it, $P_k = (1 - K_k)P_k^-$. With constant $Q > 0$ and $R > 0$ the gain settles to a constant $K_\infty$, and the Kalman filter becomes an EMA with $\alpha = K_\infty$. The innovations, which the filter computes anyway, reveal whether $Q$ and $R$ are right.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch9-sec-estimating-r -->
    ## Estimating $R$

    <!-- label: ch9-sec-the-sample-variance -->
    ### The Sample Variance

    The most direct way to find $R$ is to measure it. Put a known, constant load on the scale, or stand as still as you would during a real weighing, and record $n$ readings $y_1, \ldots, y_n$. If the true value is constant during the recording, the readings differ from one another only through their noise, so their spread estimates the noise variance. The natural measure of spread is the average squared deviation from the {term}`sample mean` $\bar y$, but with a twist: we divide by $n - 1$, not $n$.

    /// note | 📖 **Definition**
    <u>**Sample variance**</u>

    The sample variance of $n \ge 2$ numbers or random variables $y_1, \ldots, y_n$ with {term}`sample mean` $\bar y := \frac1n\sum_{i=1}^n y_i$ is
    $$s^2 := \frac{1}{n-1}\sum_{i=1}^n (y_i - \bar y)^2.$$
    ///

    /// admonition | 📐 **Theorem (Bessel's Correction)**
        attrs: {class: theorem, id: ch9-thm-bessels-correction}
    Let $y_1, \ldots, y_n$ ($n \ge 2$) be pairwise uncorrelated random variables with a common mean $\mu$ and a common finite variance $\sigma^2$. Then $\mathbb E[s^2] = \sigma^2$: the sample variance is an {term}`unbiased` estimator of $\sigma^2$. Dividing by $n$ instead gives an estimator with mean $\frac{n-1}{n}\sigma^2$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Write $y_i - \bar y = (y_i - \mu) - (\bar y - \mu)$ and expand the square:
    $$\sum_{i=1}^n (y_i - \bar y)^2 = \sum_{i=1}^n (y_i - \mu)^2 - 2(\bar y - \mu)\sum_{i=1}^n (y_i - \mu) + n(\bar y - \mu)^2 = \sum_{i=1}^n (y_i - \mu)^2 - n(\bar y - \mu)^2,$$
    because $\sum_i (y_i - \mu) = n(\bar y - \mu)$. Take expectations. Each $\mathbb E[(y_i - \mu)^2] = \sigma^2$, and $\mathbb E[(\bar y - \mu)^2] = \operatorname{Var}\bar y = \sigma^2/n$, since the variance of a sum of pairwise uncorrelated random variables is the sum of their variances (Chapter 6). So $\mathbb E\big[\sum_i (y_i - \bar y)^2\big] = n\sigma^2 - \sigma^2 = (n-1)\sigma^2$. Dividing by $n - 1$ gives $\sigma^2$; dividing by $n$ gives $\frac{n-1}{n}\sigma^2$. $\blacksquare$
    ///

    The deviations from $\bar y$ are systematically smaller than the deviations from the true mean $\mu$, because $\bar y$ is computed from the same data and sits in their middle; dividing by $n - 1$ exactly compensates. For example, the Introduction's 30 readings of a constant 155 lb, whose noise has variance $R = 1\ \text{lb}^2$, give
    """)
    return


@app.cell(hide_code=True)
def _(mo, np, scale_z):
    mo.md(rf"""
    $$\bar y = {scale_z.mean():.3f}\ \text{{lb}}, \qquad s^2 = {np.var(scale_z, ddof=1):.3f}\ \text{{lb}}^2.$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That is about $30\%$ below the true value, which is not a mistake: unbiased only means *right on average*. For normal noise one can show that $\operatorname{Var}(s^2) = 2\sigma^4/(n-1)$ ([Wikipedia: Variance, distribution of the sample variance](https://en.wikipedia.org/wiki/Variance#Distribution_of_the_sample_variance)), so with $n = 30$ the estimate's standard deviation is about $26\%$ of $\sigma^2$. Estimating a variance takes many more readings than estimating a mean. The simulation below draws $20{,}000$ recordings of $n$ readings each from noise with $\sigma^2 = 1$ and shows both versions of the estimator.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    bessel_n = mo.ui.slider(2, 50, 1, value=5, label=r"Readings per recording $n$", show_value=True)
    return (bessel_n,)


@app.cell
def _(np):
    # jb: include=false
    bessel_draws = np.random.default_rng(21).normal(0.0, 1.0, (20_000, 50))
    return (bessel_draws,)


@app.cell(hide_code=True)
def _(bessel_draws, bessel_n, graphic, mo, np, plt):
    _y = bessel_draws[:, : bessel_n.value]
    _s2 = _y.var(axis=1, ddof=1)
    _b2 = _y.var(axis=1, ddof=0)
    _fig, _ax = plt.subplots(figsize=(8, 3.4))
    _bins = np.linspace(0, 4, 81)
    _ax.hist(_b2, bins=_bins, density=True, color="gray", alpha=0.5, label=r"divide by $n$")
    _ax.hist(_s2, bins=_bins, density=True, color="C1", alpha=0.5, label=r"divide by $n-1$ (sample variance)")
    _ax.axvline(1.0, color="black", linewidth=1.5, label=r"true $\sigma^2 = 1$")
    _ax.axvline(_s2.mean(), color="C1", linestyle="--", linewidth=1.5, label=f"mean of $s^2$: {_s2.mean():.3f}")
    _ax.axvline(_b2.mean(), color="gray", linestyle="--", linewidth=1.5, label=f"mean with $1/n$: {_b2.mean():.3f}")
    _ax.set_xlim(0, 4)
    _ax.set_xlabel(r"estimate of $\sigma^2$")
    _ax.set_ylabel("density")
    _ax.set_title(f"Variance estimates from 20,000 recordings of n = {bessel_n.value} readings", style="italic")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.legend(fontsize=8, loc="upper right")
    _fig.tight_layout()
    _out = mo.vstack([
        bessel_n,
        graphic(_fig),
        mo.md(
            rf"Standard deviation of $s^2$ across recordings: ${_s2.std():.3f}$ "
            rf"(formula $\sqrt{{2/(n-1)}} = {np.sqrt(2 / (bessel_n.value - 1)):.3f}$)."
        ),
    ])
    plt.close(_fig)
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **The true value must be constant during the recording.** If it drifts, the drift is counted as noise and $s^2$ overestimates $R$.
    - **The readings must be uncorrelated.** If neighboring readings err in the same direction (a slow sway), then $\operatorname{Var}\bar y > \sigma^2/n$, and the proof shows $\mathbb E[s^2] = \sigma^2 - \big(n\operatorname{Var}\bar y - \sigma^2\big)/(n-1) < \sigma^2$: the noise looks smaller than it is.
    - **Calibration conditions must match use.** A dead weight on the platform captures the electronic noise but not the sway of a living person; the $R$ the filter needs is the variance of everything that makes a reading differ from the quantity being estimated.
    - **Few readings give an uncertain $R$.** As shown above, $30$ readings can easily be off by $25\%$ or more.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch9-sec-datasheets -->
    ### Datasheets

    Before any data exist, a sensor's datasheet gives a first estimate. Noise is usually specified either as an RMS value, which for zero-mean noise is the standard deviation $\sigma$, so $R = \sigma^2$, or as a *peak-to-peak* value. For normal noise a common convention takes peak-to-peak $\approx 6.6\,\sigma$, because $\mathbb P(|v| \le 3.3\sigma) \approx 0.999$. Two cautions apply. First, the units must match the filter's: noise quoted in ADC counts or microvolts must be converted to the units of $z_k$ (pounds here; [Chapter 11](#ch11-sec-from-pounds-to-counts) treats this conversion). Second, a datasheet describes only the electronics. For a bathroom scale such as one built on the HX711 ADC [@avia_hx711_datasheet], the person's own movement usually dominates, so the datasheet value is a lower bound on $R$.

    <!-- label: ch9-sec-quantization -->
    ### Quantization

    A digital sensor or display reports values only on a grid. [Chapter 5](#ch5-sec-quantization-noise) introduced the rounding function and showed that its error is nearly uniform when the noise is large compared with the grid step; here we name the operation and compute the variance it adds. (Chapter 5 wrote the rounding function as $Q$; in this chapter $Q$ is the process noise variance, so we write $q$.)

    /// note | 📖 **Definition**
    <u>**Quantization**</u>

    Quantization with step $\Delta > 0$ is the function $q : \mathbb R \to \mathbb R$, $q(y) := \Delta\,\lfloor y/\Delta + \tfrac12\rfloor$, that rounds each real number to the nearest integer multiple of $\Delta$ (rounding halves up); here $\lfloor t\rfloor$ is the largest integer not exceeding $t$. The quantization error of $y$ is $q(y) - y$, which always lies in $(-\Delta/2, \Delta/2]$ (Chapter 5).
    ///

    /// admonition | 📐 **Theorem (Quantization Noise Variance)**
        attrs: {class: theorem, id: ch9-thm-quantization-noise-variance}
    If the quantization error $u$ is uniformly distributed on $[-\Delta/2, \Delta/2]$, then $\mathbb E u = 0$ and $\operatorname{Var} u = \Delta^2/12$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    This is the uniform case of Chapter 6's theorem on the variances of common distributions, with $a = -\Delta/2$ and $b = \Delta/2$. Directly: the density of $u$ is $1/\Delta$ on the interval, the integrand of $\mathbb E u = \frac1\Delta\int_{-\Delta/2}^{\Delta/2} u\,du$ is odd, so $\mathbb E u = 0$, and
    $$\operatorname{Var} u = \mathbb E[u^2] = \frac1\Delta\int_{-\Delta/2}^{\Delta/2} u^2\,du = \frac1\Delta\cdot\frac{u^3}{3}\bigg|_{-\Delta/2}^{\Delta/2} = \frac1\Delta\cdot\frac{2}{3}\cdot\frac{\Delta^3}{8} = \frac{\Delta^2}{12}. \qquad \blacksquare$$
    ///

    When the quantity being rounded already carries noise with a standard deviation of about $\Delta$ or more, Chapter 5's theorem says the error is nearly uniform, and the rounding adds approximately independent noise: the total measurement noise variance is approximately $R + \Delta^2/12$. A scale that displays to $0.1$ lb adds only $0.01/12 \approx 0.0008\ \text{lb}^2$, negligible next to $R = 1\ \text{lb}^2$; the HX711's 24-bit steps are far smaller still. When the noise is much smaller than $\Delta$, the uniform model fails: every reading rounds to the same grid point, the error is essentially a constant, and a constant error is a bias, not noise, which no amount of averaging removes. The table repeats Chapter 5's experiment (a true value of $155.03$ lb, normal noise with standard deviation $\sigma$, step $\Delta = 0.1$ lb, $100{,}000$ simulated readings) and reports the mean and variance of the quantization error. (For more on when the uniform model holds, see [Wikipedia: Quantization (signal processing)](https://en.wikipedia.org/wiki/Quantization_(signal_processing)).)
    """)
    return


@app.cell(hide_code=True)
def _(mo, np):
    _g = np.random.default_rng(22).standard_normal(100_000)
    _D = 0.1
    _rows = [
        r"| $\sigma$ (lb) | mean error (lb) | error variance (lb$^2$) | variance $\div\ \Delta^2/12$ |",
        "|:---|:---:|:---:|:---:|",
    ]
    for _s in (0.005, 0.01, 0.02, 0.05, 0.2):
        _y = 155.03 + _s * _g
        _u = _D * np.floor(_y / _D + 0.5) - _y
        _rows.append(f"| ${_s}$ | ${_u.mean():+.4f}$ | ${_u.var():.6f}$ | ${_u.var() / (_D**2 / 12):.2f}$ |")
    mo.md("\n".join(_rows))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    From $\sigma = 0.05$ lb on, the error has mean $0$ and variance $\Delta^2/12$ to within a percent. At $\sigma = 0.005$ lb nearly every reading rounds to $155.0$, so the error is a nearly constant $-0.03$ lb with almost no variance.

    <!-- label: ch9-sec-noise-that-is-not-white -->
    ### Noise That Is Not White

    The sample variance assumes the noise in different readings is uncorrelated. Some sensors, gyroscopes in particular, also have slowly wandering errors, and then the sample variance depends on how long you record. The standard tool for separating noise types by time scale is the *Allan variance* ([Wikipedia: Allan variance](https://en.wikipedia.org/wiki/Allan_variance)), which we will meet again with inertial sensors in Parts V and VI.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch9-sec-process-noise -->
    ## Process Noise

    The Introduction distinguished the change we *expect* between two steps, $\Delta x_k$, from the change that actually happens. While bulking you might plan to gain $0.2$ lb per day, but water and food make the actual daily change wander around that plan. On the scale, the load on the platform wanders a little as you shift your weight. The gap between expected and actual change is what makes the prediction uncertain, and it gets a name.

    /// note | 📖 **Definition**
    <u>**Process noise**</u>

    In a model $x_k = x_{k-1} + \Delta x_k + w_k$ of how a true value changes from step $k-1$ to step $k$, in which $\Delta x_k$ is the expected change, the process noise at step $k$ is the random variable $w_k := x_k - x_{k-1} - \Delta x_k$: the difference between the actual change and the expected change. When all the $w_k$ have the same variance, it is written $Q$.
    ///

    /// note | 📖 **Definition**
    <u>**White noise**</u>

    A sequence $(w_k)_{k \ge 1}$ of random variables is white noise if every $w_k$ has mean $0$, all $w_k$ have the same finite variance, and $w_j$ and $w_k$ are {term}`uncorrelated` whenever $j \ne k$.
    ///

    The name comes from signal processing: uncorrelated noise contains all frequencies in equal measure, as white light contains all colors. Some texts require the $w_k$ to be independent, not just uncorrelated; for the variance calculations in this chapter, uncorrelated is enough. The measurement noise $(v_k)$ of the scale is modeled as white noise with variance $R$.

    /// note | 📖 **Definition**
    <u>**Random walk**</u>

    A {term}`stochastic process` $(x_k)_{k \in \mathbb N}$ is a random walk if $x_k = x_{k-1} + w_k$ for every $k \ge 1$, where $(w_k)_{k \ge 1}$ is {term}`white noise` and every $w_k$ is uncorrelated with $x_0$.
    ///

    The model $x_k = x_{k-1} + \Delta x_k + w_k$ with known $\Delta x_k$ and white process noise is a random walk around the expected path $x_0 + \sum_{j \le k}\Delta x_j$; we call it the **random-walk model**. It is the simplest honest model of a quantity that changes in ways we cannot predict.

    /// admonition | 📐 **Lemma (A Random Walk Spreads Out)**
        attrs: {class: lemma, id: ch9-lem-a-random-walk-spreads-out}
    If $(x_k)$ is a random walk whose steps have variance $Q$, then $\operatorname{Var}(x_k - x_0) = kQ$ for every $k \in \mathbb N$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    $x_k - x_0 = \sum_{j=1}^k w_j$ (by induction on $k$), and the $w_j$ are pairwise uncorrelated, so the variance of the sum is the sum of the variances (Chapter 6): $kQ$. $\blacksquare$
    ///

    So a random walk's typical distance from its start grows like $\sqrt{kQ}$ without bound. A filter tracking it can never stop listening to new measurements: its gain must stay away from $0$. The [Prediction Step theorem](#ch9-thm-prediction-step) below gives the prediction's error variance.

    /// admonition | 📐 **Theorem (Prediction Step)**
        attrs: {class: theorem, id: ch9-thm-prediction-step}
    Let $x_k = x_{k-1} + \Delta x_k + w_k$, where $\Delta x_k$ is a known number and $w_k$ has mean $0$ and variance $Q$. Let $\hat x_{k-1}$ be an estimate of $x_{k-1}$ whose error $e_{k-1}$ has mean $0$ and variance $P_{k-1}$, and assume $\operatorname{Cov}(e_{k-1}, w_k) = 0$. Then the prediction $\hat x_k^- := \hat x_{k-1} + \Delta x_k$ has error
    $$e_k^- = e_{k-1} - w_k, \qquad \mathbb E e_k^- = 0, \qquad P_k^- = P_{k-1} + Q.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    $e_k^- = \hat x_k^- - x_k = (\hat x_{k-1} + \Delta x_k) - (x_{k-1} + \Delta x_k + w_k) = e_{k-1} - w_k$. By linearity its mean is $0$, and by Chapter 6, $\operatorname{Var}(e_{k-1} - w_k) = P_{k-1} + Q - 2\operatorname{Cov}(e_{k-1}, w_k) = P_{k-1} + Q$. $\blacksquare$
    ///

    The predict step can only add uncertainty, and the update step can only remove it (Chapter 7's corollary $P_k < P_k^-$). A filter alternates between the two.

    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **The expected change must be right on average.** If the true changes have mean $\Delta x_k + b$ rather than $\Delta x_k$ (for example, a bulking rate other than the planned one), then $\mathbb E w_k = b \ne 0$, the prediction is biased, and the bias accumulates step after step. This is the drift of the Introduction's alpha filter.
    - **The process noise must be white.** A persistent but unknown trend is *not* white: its values are strongly correlated from step to step, so $P_k^- = P_{k-1} + Q$ misdescribes the prediction error. The cure is a better model of the change ([Chapter 10](#ch10-sec-linear-process-models)), or estimating the trend as part of the state ([Chapter 13](#ch13-sec-a-second-state-variable)).
    - **$Q$ is a modeling choice.** Unlike $R$, it usually cannot be measured directly, because the true values are never observed. It is tuned, and then checked with the innovation tests at the end of this chapter.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch9-sec-the-scalar-kalman-filter -->
    ## The Scalar Kalman Filter

    We now have both halves of a filter: the predict step above and Chapter 7's update. Here are the assumptions under which they fit together.

    - **(K1) Process model:** $x_k = x_{k-1} + \Delta x_k + w_k$ for $k \ge 1$, with known numbers $\Delta x_k$.
    - **(K2) Measurement model:** $z_k = x_k + v_k$ for $k \ge 1$.
    - **(K3) Noise:** $(w_k)$ is white noise with variance $Q \ge 0$ and $(v_k)$ is white noise with variance $R > 0$; the initial estimate $\hat x_0$ has error $e_0 := \hat x_0 - x_0$ with mean $0$ and variance $P_0 \ge 0$; and $e_0, w_1, w_2, \ldots, v_1, v_2, \ldots$ are pairwise uncorrelated.

    **The algorithm.** Start from $\hat x_0$ and $P_0$. For each $k = 1, 2, 3, \ldots$:

    $$\begin{aligned}
    &\textbf{Predict:} && \hat x_k^- = \hat x_{k-1} + \Delta x_k, && P_k^- = P_{k-1} + Q,\\
    &\textbf{Update:} && K_k = \frac{P_k^-}{P_k^- + R}, \quad \hat x_k = \hat x_k^- + K_k\,(z_k - \hat x_k^-), && P_k = (1 - K_k)\,P_k^-.
    \end{aligned}$$

    /// note | 📖 **Definition**
    <u>**Kalman filter**</u>

    A recursive {term}`filter` for a quantity that follows a linear model of how it changes and is observed through a linear measurement model, both with additive noise of known variance (covariance, for vectors), that alternates two steps: a predict step, which propagates the estimate and its {term}`error variance` through the model of change, and an update step, which combines the resulting prediction with the new measurement using the {term}`optimal gain`. The *scalar Kalman filter* above is the case of a single unknown with the random-walk model.
    ///

    The filter is named after Rudolf Kálmán, who published it for vector-valued states in @kalman1960. [Chapter 10](ch10_process_models.md) generalizes the process model, [Chapter 11](ch11_measurement_functions.md) the measurement model, and [Chapter 13](ch13_kalman_filter.md) handles vectors. Here is a complete implementation. It accepts a single sequence of measurements or many sequences at once (one per row), which we use for simulations; note that `P_pred`, `S`, `K`, and `P` do not depend on the measurements at all.
    """)
    return


@app.cell
def _(np):
    # jb: editor=true
    def kalman_filter_1d(z, x0, P0, Q, R, dx=0.0):
        """Scalar Kalman filter for x_k = x_{k-1} + dx_k + w_k and z_k = x_k + v_k.

        z      -- measurements z_1, ..., z_n (shape (n,), or (runs, n) for many runs)
        x0, P0 -- initial estimate (a number, or one per run) and its error variance
        Q, R   -- process noise and measurement noise variances
        dx     -- expected change per step (a number, or one value per step)
        Returns a dict of arrays; entry k-1 belongs to step k.
        """
        z = np.asarray(z, dtype=float)
        n = z.shape[-1]
        dx = np.broadcast_to(np.asarray(dx, dtype=float), (n,))
        x_pred, x_est, innov = np.empty(z.shape), np.empty(z.shape), np.empty(z.shape)
        P_pred, P_est, K, S = np.empty(n), np.empty(n), np.empty(n), np.empty(n)
        x, P = x0, P0
        for k in range(n):
            # Predict: propagate the estimate and its error variance
            x_pred[..., k] = x + dx[k]
            P_pred[k] = P + Q
            # Update: combine prediction and measurement with the optimal gain
            S[k] = P_pred[k] + R                  # innovation variance (see below)
            K[k] = P_pred[k] / S[k]               # optimal gain
            innov[..., k] = z[..., k] - x_pred[..., k]
            x = x_pred[..., k] + K[k] * innov[..., k]
            P = (1 - K[k]) * P_pred[k]
            x_est[..., k], P_est[k] = x, P
        return dict(x_pred=x_pred, P_pred=P_pred, S=S, K=K, innov=innov, x=x_est, P=P_est)

    return (kalman_filter_1d,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// admonition | 📐 **Theorem (The Kalman Filter Is Optimal at Every Step)**
        attrs: {class: theorem, id: ch9-thm-the-kalman-filter-is-optimal-at-every-step}
    Assume (K1)–(K3). For every $k \ge 1$:

    1. $e_k^-$ is a linear combination of $e_0, w_1, \ldots, w_k, v_1, \ldots, v_{k-1}$, and $e_k$ is a linear combination of $e_0, w_1, \ldots, w_k, v_1, \ldots, v_k$;
    2. $\mathbb E e_k^- = \mathbb E e_k = 0$, $\operatorname{Var} e_k^- = P_k^-$, and $\operatorname{Var} e_k = P_k$;
    3. $K_k$ is the optimal gain at step $k$: among all gains used with the prediction $\hat x_k^-$ and the measurement $z_k$, it gives the smallest error variance.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    By induction on $k$. For the base we use $k - 1 = 0$: $e_0$ is a linear combination of $e_0$, with mean $0$ and variance $P_0$. Now let $k \ge 1$ and assume that $e_{k-1}$ is a linear combination of $e_0, w_1, \ldots, w_{k-1}, v_1, \ldots, v_{k-1}$ with mean $0$ and variance $P_{k-1}$.

    *Predict.* By (K3), $w_k$ is uncorrelated with each of $e_0, w_1, \ldots, w_{k-1}, v_1, \ldots, v_{k-1}$, so by the linearity of covariance (Chapter 6's properties of covariance) $\operatorname{Cov}(e_{k-1}, w_k) = 0$. The Prediction Step theorem gives $e_k^- = e_{k-1} - w_k$, a linear combination of $e_0, w_1, \ldots, w_k, v_1, \ldots, v_{k-1}$, with mean $0$ and variance $P_{k-1} + Q = P_k^-$.

    *Update.* By the linearity of covariance again, $\operatorname{Cov}(e_k^-, v_k) = 0$, and $\mathbb E v_k = 0$, $\operatorname{Var} v_k = R$. So the pair $(\hat x_k^-, z_k)$ satisfies assumptions (A1)–(A3) of Chapter 7, and the Optimal Gain theorem says that $K_k = P_k^-/(P_k^- + R)$ is the optimal gain, with error variance $(1 - K_k)P_k^- = P_k$. By Chapter 7's Error of the Update lemma, $e_k = (1 - K_k)\,e_k^- + K_k v_k$, a linear combination of $e_0, w_1, \ldots, w_k, v_1, \ldots, v_k$ with mean $0$. $\blacksquare$
    ///

    Two remarks. First, if in addition $e_0$, all $w_k$, and all $v_k$ are independent and normal, then by [Chapter 8](#ch8-cor-the-normal-bayes-filter)'s normal Bayes filter $\hat x_k$ is the posterior mean of $x_k$ given $z_1, \ldots, z_k$ (with prior $\mathcal N(\hat x_0, P_0)$ for $x_0$), and therefore the best estimator of any form in the mean-squared-error sense. Second, without normality, the [Kalman Filter Is Optimal at Every Step theorem](#ch9-thm-the-kalman-filter-is-optimal-at-every-step) still holds; it only uses means, variances, and covariances. (A stronger statement is also true: the Kalman filter's estimate has the smallest error variance among *all* linear combinations of $\hat x_0, z_1, \ldots, z_k$; this is the setting of Kalman's 1960 paper.)

    /// admonition | 📐 **Theorem (No Process Noise)**
        attrs: {class: theorem, id: ch9-thm-no-process-noise}
    Assume (K1)–(K3) with $Q = 0$ and $P_0 > 0$, and let $n_0 := R/P_0$. Then for every $k \ge 1$
    $$\frac{1}{P_k} = \frac{1}{P_0} + \frac{k}{R}, \qquad K_k = \frac{P_k}{R} = \frac{1}{n_0 + k},$$
    and if moreover $\Delta x_k = 0$ for all $k$, then
    $$\hat x_k = \frac{n_0\,\hat x_0 + z_1 + z_2 + \cdots + z_k}{n_0 + k}.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    With $Q = 0$, $P_k^- = P_{k-1}$, and item 4 of the Optimal Gain theorem gives $1/P_k = 1/P_{k-1} + 1/R$; induction on $k$ gives the first formula. Item 3 of the same theorem gives $P_k = K_k R$, so $K_k = P_k/R = 1/(R/P_0 + k)$. For the estimate, use induction again: the case $k = 0$ is trivial, and if the formula holds for $k - 1$, then with $K_k = 1/(n_0 + k)$,
    $$\hat x_k = \Big(1 - \frac{1}{n_0 + k}\Big)\hat x_{k-1} + \frac{z_k}{n_0 + k} = \frac{(n_0 + k - 1)\,\hat x_{k-1} + z_k}{n_0 + k} = \frac{n_0\,\hat x_0 + \sum_{i=1}^{k} z_i}{n_0 + k}. \qquad \blacksquare$$
    ///

    The initial estimate counts as $n_0 = R/P_0$ "virtual measurements". A vague start (large $P_0$) makes $n_0$ tiny and the gains nearly $1, \tfrac12, \tfrac13, \ldots$: the Kalman filter with $Q = 0$ is Chapter 7's cumulative average, and first-measurement initialization ($K_1 = 1$, $P_1 = R$) is the limiting case of knowing nothing beforehand.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **Correct $Q$ and $R$.** The theorem's "optimal" refers to the variances the filter is given. With wrong values the estimate is still unbiased (Chapter 7's Zero-Mean Error theorem), but the gains are not optimal and the reported $P_k$ is wrong. The innovation tests below detect this.
    - **Uncorrelated noise (K3).** Correlated measurement noise or correlated process noise breaks the induction: $\operatorname{Cov}(e_k^-, v_k)$ is no longer zero, and Chapter 7's *Correlated Errors* section applies.
    - **Linear models.** Both models are linear with additive noise. Nonlinear models need the extended or unscented Kalman filter ([Chapter 15](ch15_extended_kalman_filter.md), [Chapter 16](ch16_unscented_kalman_filter.md)).
    - **Initialization.** A wrong $\hat x_0$ with a small $P_0$ is trusted as $n_0 = R/P_0$ readings' worth of information. When in doubt, choose $P_0$ large.
    ///

    <!-- label: ch9-sec-the-scale-with-a-shifting-load -->
    ### The Scale With a Shifting Load

    To see process noise at work, simulate a person whose load on the platform wanders as they shift their weight: a random walk starting at $155$ lb with $Q = 0.01\ \text{lb}^2$ per step (a standard deviation of $0.1$ lb per tenth of a second), measured with $R = 1\ \text{lb}^2$ at 10 SPS for 15 seconds. The filter starts from the vague guess $\hat x_0 = 150$ lb, $P_0 = 100\ \text{lb}^2$. Adjust the filter's $Q$ and $R$ (the simulation's true values are $0.01$ and $1$), and tick the box to pick up the Introduction's 10 lb cat halfway through. The right panel shows the gain $K_k$, which by item 3 of the Optimal Gain theorem also equals $P_k/R$: it settles to a constant, which is the subject of the next section.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    kf_Q = mo.ui.slider(
        steps=[0.0, 0.0001, 0.0003, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0], value=0.01,
        label=r"Filter's $Q$ (lb$^2$ per step)", show_value=True,
    )
    kf_R = mo.ui.slider(
        steps=[0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 10.0], value=1.0, label=r"Filter's $R$ (lb$^2$)", show_value=True,
    )
    kf_cat = mo.ui.checkbox(value=False, label="Pick up a 10 lb cat at 7.5 s")
    return kf_Q, kf_R, kf_cat


@app.cell
def _(kf_cat, np, shift_t, shift_x, shift_z):
    # jb: include=false
    _cat = np.where(shift_t > 7.5, 10.0, 0.0) if kf_cat.value else np.zeros_like(shift_t)
    kf_truth = shift_x + _cat
    kf_z = shift_z + _cat
    return kf_truth, kf_z


@app.cell(hide_code=True)
def _(
    graphic,
    kalman_filter_1d,
    kf_Q,
    kf_R,
    kf_cat,
    kf_truth,
    kf_z,
    mo,
    np,
    plt,
    shift_t,
    steady_state,
):
    _f = kalman_filter_1d(kf_z, 150.0, 100.0, kf_Q.value, kf_R.value)
    _err = _f["x"] - kf_truth
    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(10, 3.9), gridspec_kw={"width_ratios": [1.6, 1]})
    _ax1.plot(shift_t, kf_z, ".", color="C0", markersize=3, label="measurements")
    _ax1.plot(shift_t, kf_truth, color="black", linewidth=1.2, label="true load")
    _ax1.plot(shift_t, _f["x"], color="C1", linewidth=1.8, label="Kalman estimate")
    _ax1.fill_between(shift_t, _f["x"] - 2 * np.sqrt(_f["P"]), _f["x"] + 2 * np.sqrt(_f["P"]), color="C1", alpha=0.2,
                      label=r"$\pm 2\sqrt{P_k}$")
    _lo = min(kf_truth.min(), 152.0) - 2
    _ax1.set_ylim(_lo, kf_truth.max() + 4)
    _ax1.set_xlabel("time (s)")
    _ax1.set_ylabel("load (lb)")
    _ax1.set_title("Kalman filter on a shifting load", style="italic")
    _ax1.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax1.legend(fontsize=8, loc="upper left", ncol=2)

    _ax2.plot(shift_t, _f["K"], color="C1", label=r"gain $K_k = P_k/R$")
    if kf_Q.value > 0:
        _ax2.axhline(steady_state(kf_Q.value, kf_R.value)[1], color="gray", linestyle="--", linewidth=1,
                     label=r"limit $K_\infty$ (next section)")
    _ax2.set_yscale("log")
    _ax2.set_xlabel("time (s)")
    _ax2.set_title("Gain (and error variance / R)", style="italic")
    _ax2.grid(visible=True, alpha=0.9, linewidth=0.4, which="both")
    _ax2.legend(fontsize=8, loc="upper right")
    _fig.tight_layout()
    _out = mo.vstack([
        mo.hstack([kf_Q, kf_R, kf_cat], justify="start", gap=2),
        graphic(_fig),
        mo.md(
            rf"Over the last 10 seconds: actual RMS error ${np.sqrt(np.mean(_err[50:] ** 2)):.3f}$ lb; "
            rf"the filter's reported $\sqrt{{P_k}}$ averages ${np.sqrt(np.mean(_f['P'][50:])):.3f}$ lb. "
            rf"Final gain $K_{{150}} = {_f['K'][-1]:.4f}$."
        ),
    ])
    plt.close(_fig)
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Things to try: with $Q = 0$ the filter is the cumulative average with a prior, its gain keeps falling like $1/k$, and it never catches up with the cat. With $Q = 1$ it follows every wiggle of the noise. In between, for $Q$ within a factor of about three of the true $0.01$ (with $R = 1$), the actual error is smallest and the reported $\sqrt{P_k}$ describes it well. A single 15-second run cannot pin $Q$ down more precisely than that, which is why the tests at the end of this chapter average over many steps.

    <!-- label: ch9-sec-steady-state -->
    ## Steady State

    In the right panel above, the gain stopped changing after a few seconds. This is no accident.

    /// note | 📖 **Definition**
    <u>**Steady-state gain**</u>

    If the gains $K_k$ of a {term}`Kalman filter` converge as $k \to \infty$, their limit $K_\infty := \lim_{k\to\infty} K_k$ is the filter's steady-state gain.
    ///

    /// admonition | 📐 **Theorem (Steady-State Gain)**
        attrs: {class: theorem, id: ch9-thm-steady-state-gain}
    Consider the scalar Kalman filter with constant $Q > 0$ and $R > 0$ and any $P_0 \ge 0$, and let
    $$p := \frac{Q + \sqrt{Q^2 + 4QR}}{2}.$$
    1. $p$ is the unique positive solution of $p = \dfrac{pR}{p + R} + Q$.
    2. $|P_k^- - p| \le \lambda^{k-1}\,|P_1^- - p|$ for every $k \ge 1$, where $\lambda := \big(R/(Q + R)\big)^2 < 1$. Hence $P_k^- \to p$.
    3. Consequently $K_k \to K_\infty = \dfrac{p}{p + R}$ and $P_k \to P_\infty := \dfrac{pR}{p + R} = p - Q = K_\infty R$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    1. Multiplying by $p + R > 0$, the equation is equivalent to $p(p + R) = pR + Q(p + R)$, that is, $p^2 - Qp - QR = 0$. By the quadratic formula its roots are $\big(Q \pm \sqrt{Q^2 + 4QR}\big)/2$. Their product is $-QR < 0$, so exactly one root is positive, namely $p$.
    2. Let $\varphi(s) := \dfrac{sR}{s + R} + Q$ for $s \ge 0$. By the two steps of the filter and item 3 of the Optimal Gain theorem, $P_k = P_k^- R/(P_k^- + R)$ and $P_{k+1}^- = P_k + Q$, so $P_{k+1}^- = \varphi(P_k^-)$, and by item 1, $p = \varphi(p)$. For $s, t \ge 0$,
       $$\varphi(s) - \varphi(t) = R\Big(\frac{s}{s+R} - \frac{t}{t+R}\Big) = \frac{R^2\,(s - t)}{(s + R)(t + R)}.$$
       Every $P_k^- = P_{k-1} + Q \ge Q$, and $p = \varphi(p) \ge Q$. For $s, t \ge Q$ the fraction $R^2/\big((s+R)(t+R)\big)$ is at most $\lambda$, so $|P_{k+1}^- - p| = |\varphi(P_k^-) - \varphi(p)| \le \lambda\,|P_k^- - p|$, and induction gives the bound. Since $0 \le \lambda < 1$, $\lambda^{k-1} \to 0$ ([Appendix C: Sequences and Limits](#appc-sec-sequences-and-limits)), so $P_k^- \to p$.
    3. $K_k = P_k^-/(P_k^- + R)$ and $P_k = P_k^-R/(P_k^- + R)$ are continuous functions of $P_k^-$, so by the limit laws they converge to $p/(p + R)$ and $pR/(p + R)$. By item 1, $pR/(p + R) = p - Q$, and $pR/(p+R) = K_\infty R$. $\blacksquare$
    ///

    The bound in item 2 is conservative. Near the limit, $\varphi(s) - \varphi(p) \approx (1 - K_\infty)^2(s - p)$, so the remaining distance shrinks by about the factor $(1 - K_\infty)^2$ per step. Either way the starting value $P_0$ is forgotten geometrically fast: in the long run, every Kalman filter with the same $Q$ and $R$ uses the same gain.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch9-sec-the-kalman-filter-becomes-an-ema -->
    ### The Kalman Filter Becomes an EMA

    /// admonition | 📐 **Theorem (The Steady-State Kalman Filter Is an EMA)**
        attrs: {class: theorem, id: ch9-thm-the-steady-state-kalman-filter-is-an-ema}
    Assume $Q > 0$ and $R > 0$. If the scalar Kalman filter is started with $P_0 = P_\infty$, then $P_k^- = p$, $K_k = K_\infty$, and $P_k = P_\infty$ for every $k \ge 1$. If moreover $\Delta x_k = 0$ for all $k$, the filter is
    $$\hat x_k = \hat x_{k-1} + K_\infty\,(z_k - \hat x_{k-1}),$$
    the {term}`exponential moving average` with $\alpha = K_\infty$ started at $\hat x_0$ (for general $\Delta x_k$, it is the Introduction's alpha filter with $\alpha = K_\infty$). For any other $P_0 \ge 0$, $K_k \to K_\infty$, so the Kalman filter approaches this EMA.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    If $P_{k-1} = P_\infty$, then $P_k^- = P_\infty + Q = p$, so $K_k = p/(p + R) = K_\infty$ and $P_k = pR/(p + R) = P_\infty$; induction on $k$ starting from $P_0 = P_\infty$ proves the first claim. With $\Delta x_k = 0$ the prediction is $\hat x_k^- = \hat x_{k-1}$, which gives the displayed update. Note $0 < K_\infty < 1$ because $p > 0$. The last claim is the Steady-State Gain theorem. $\blacksquare$
    ///

    This answers the question the Introduction left open: why an EMA, and with which $\alpha$? The EMA is the long-run form of the optimal filter for a value that wanders like a random walk, and its $\alpha$ is determined by the ratio of the two noise levels.

    /// admonition | 📐 **Corollary (Choosing the EMA's $\alpha$)**
        attrs: {class: corollary, id: ch9-cor-choosing-the-emas-alpha}
    Let $Q > 0$, $R > 0$, and $r := Q/R$. Then
    $$K_\infty = \frac{\sqrt{r^2 + 4r} - r}{2}, \qquad\text{equivalently}\qquad \frac QR = \frac{K_\infty^2}{1 - K_\infty}.$$
    So the steady-state gain depends on $Q$ and $R$ only through their ratio, and every $\alpha \in (0, 1)$ is the steady-state gain for exactly one ratio, $Q/R = \alpha^2/(1-\alpha)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Let $s := \sqrt{r^2 + 4r}$. Dividing numerator and denominator of $p$ by $R$ gives $p/R = (r + s)/2$, so $K_\infty = \frac{p/R}{p/R + 1} = \frac{r + s}{r + s + 2}$. This equals $\frac{s - r}{2}$ because $(s - r)(r + s + 2) = s^2 - r^2 + 2s - 2r = 4r + 2s - 2r = 2(r + s)$. Then $2K_\infty + r = s$; squaring, $4K_\infty^2 + 4K_\infty r + r^2 = r^2 + 4r$, so $K_\infty^2 = r(1 - K_\infty)$. Conversely, for $\alpha \in (0,1)$ the ratio $r = \alpha^2/(1-\alpha) > 0$ gives $K_\infty^2 = r(1 - K_\infty)$ and $\alpha^2 = r(1-\alpha)$; since $t \mapsto t^2/(1-t)$ is strictly increasing on $(0, 1)$, $K_\infty = \alpha$. $\blacksquare$
    ///

    | $Q/R$ | $0.0001$ | $0.001$ | $0.01$ | $0.1$ | $1$ | $10$ |
    |:---:|:---:|:---:|:---:|:---:|:---:|:---:|
    | $\alpha = K_\infty$ | $0.0100$ | $0.0311$ | $0.0951$ | $0.270$ | $0.618$ | $0.916$ |

    For the shifting load above, $Q/R = 0.01$ gives $\alpha \approx 0.095$. For small ratios $K_\infty \approx \sqrt{Q/R}$: halving the measurement noise's standard deviation doubles the right $\alpha$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Is the EMA with $\alpha = K_\infty$ really the best EMA? Its long-run error variance can be computed for every $\alpha$, and completing the square one last time answers the question.

    /// admonition | 📐 **Theorem (The Best EMA)**
        attrs: {class: theorem, id: ch9-thm-the-best-ema}
    Assume (K1)–(K3) with $Q > 0$, and let $0 < \alpha < 1$. The alpha filter $\hat x_k = \hat x_k^- + \alpha\,(z_k - \hat x_k^-)$ with $\hat x_k^- = \hat x_{k-1} + \Delta x_k$ (the EMA when $\Delta x_k = 0$) has error variances $V_k := \operatorname{Var} e_k$ that satisfy
    $$V_k = (1 - \alpha)^2\,(V_{k-1} + Q) + \alpha^2 R$$
    and converge, from every $V_0 = P_0$, to
    $$V(\alpha) := \frac{(1 - \alpha)^2 Q + \alpha^2 R}{\alpha(2 - \alpha)} = P_\infty + \frac{(p + R)\,(\alpha - K_\infty)^2}{\alpha(2 - \alpha)}.$$
    So $V(\alpha) \ge P_\infty$, with equality if and only if $\alpha = K_\infty$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    As in the Kalman filter theorem, $e_k = (1 - \alpha)(e_{k-1} - w_k) + \alpha v_k$, where $e_{k-1}$ is a linear combination of $e_0, w_1, \ldots, w_{k-1}, v_1, \ldots, v_{k-1}$ and hence uncorrelated with $w_k$ and $v_k$. The variance of this weighted sum gives the recursion. Subtracting the equation $V(\alpha) = (1-\alpha)^2(V(\alpha) + Q) + \alpha^2R$, which holds because $1 - (1 - \alpha)^2 = \alpha(2 - \alpha)$, gives $V_k - V(\alpha) = (1-\alpha)^2\big(V_{k-1} - V(\alpha)\big)$, so $V_k - V(\alpha) = (1-\alpha)^{2k}\big(V_0 - V(\alpha)\big) \to 0$.

    For the identity, multiply by $\alpha(2 - \alpha)$ and compare coefficients of the two quadratics in $\alpha$. The left side is $(Q + R)\alpha^2 - 2Q\alpha + Q$. The right side is $P_\infty(2\alpha - \alpha^2) + (p + R)(\alpha^2 - 2K_\infty\alpha + K_\infty^2)$. Using $P_\infty = p - Q$, $(p + R)K_\infty = p$, and $(p + R)K_\infty^2 = p^2/(p + R) = Q$ (from $p^2 = Q(p + R)$, item 1 of the Steady-State Gain theorem), its coefficients are $p + R - P_\infty = Q + R$, then $2P_\infty - 2p = -2Q$, then $Q$. They match. Since $\alpha(2 - \alpha) > 0$ and $p + R > 0$, the second term is nonnegative and vanishes only at $\alpha = K_\infty$. $\blacksquare$
    ///

    The two parts of $V(\alpha)$ are a trade-off, like Chapter 6's lag versus noise. The part $\frac{\alpha R}{2 - \alpha}$ is measurement noise passed through the filter; with $Q = 0$ it is exactly Chapter 6's EMA variance. The part $\frac{(1-\alpha)^2 Q}{\alpha(2-\alpha)}$ is the error from lagging behind a wandering true value. A small $\alpha$ suppresses noise but lags; a large $\alpha$ follows the truth but passes noise. The figure shows both parts and their sum for a chosen ratio $Q/R$ (left), and how quickly the gain $K_k$ settles from three different starting variances (right).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    ss_ratio = mo.ui.slider(
        steps=[0.0001, 0.0003, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0], value=0.01,
        label=r"Ratio $Q/R$", show_value=True,
    )
    return (ss_ratio,)


@app.cell(hide_code=True)
def _(graphic, mo, np, plt, ss_ratio, steady_state):
    _R = 1.0
    _Q = ss_ratio.value * _R
    _p, _K, _Pinf = steady_state(_Q, _R)
    _a = np.linspace(0.002, 0.998, 999)
    _noise = _a * _R / (2 - _a)
    _lag = (1 - _a) ** 2 * _Q / (_a * (2 - _a))

    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(10, 3.9))
    _ax1.plot(_a, _noise, color="C0", linestyle="--", label=r"noise passed: $\frac{\alpha R}{2-\alpha}$")
    _ax1.plot(_a, _lag, color="red", linestyle=":", label=r"lag behind the walk: $\frac{(1-\alpha)^2Q}{\alpha(2-\alpha)}$")
    _ax1.plot(_a, _noise + _lag, color="C1", linewidth=2, label=r"total $V(\alpha)$")
    _ax1.plot([_K], [_Pinf], "o", color="C1", label=rf"minimum at $\alpha = K_\infty = {_K:.3f}$")
    _ax1.axvline(_K, color="gray", linewidth=0.8)
    _ax1.set_xscale("log")
    _ax1.set_yscale("log")
    _ax1.set_ylim(_Pinf / 5, 20 * _R)
    _ax1.set_xlabel(r"EMA gain $\alpha$")
    _ax1.set_ylabel(r"steady-state error variance / $R$")
    _ax1.set_title("Steady-state error variance of an EMA", style="italic")
    _ax1.grid(visible=True, alpha=0.9, linewidth=0.4, which="both")
    _ax1.legend(fontsize=8, loc="upper center")

    _k = np.arange(1, 61)
    for _P0, _style, _lab in [(0.0, ":", r"$P_0 = 0$"), (_Pinf, "-", r"$P_0 = P_\infty$"), (100.0, "--", r"$P_0 = 100R$")]:
        _P = _P0
        _Ks = []
        for _ in _k:
            _Pm = _P + _Q
            _Kk = _Pm / (_Pm + _R)
            _P = (1 - _Kk) * _Pm
            _Ks.append(_Kk)
        _ax2.plot(_k, _Ks, linestyle=_style, color="C1", label=_lab)
    _ax2.axhline(_K, color="gray", linewidth=0.8)
    _ax2.set_yscale("log")
    _ax2.set_xlabel("step $k$")
    _ax2.set_ylabel(r"gain $K_k$")
    _ax2.set_title(r"The gain forgets its start", style="italic")
    _ax2.grid(visible=True, alpha=0.9, linewidth=0.4, which="both")
    _ax2.legend(fontsize=8, loc="upper right")
    _fig.tight_layout()
    _out = mo.vstack([
        ss_ratio,
        graphic(_fig),
        mo.md(
            rf"$p = {_p:.4f}R$, $K_\infty = {_K:.4f}$, $P_\infty = {_Pinf:.4f}R$; "
            rf"check: $K_\infty^2/(1-K_\infty) = {_K**2 / (1 - _K):.4f} = Q/R$."
        ),
    ])
    plt.close(_fig)
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **Constant $Q$ and $R$.** A steady state exists only if the noise levels do not change. If the sampling rate changes (the HX711 can switch between 10 and 80 SPS), $Q$ per step changes and so does $K_\infty$. Missing measurements also interrupt the steady state.
    - **$Q > 0$.** With $Q = 0$ the gain tends to $0$ (the No Process Noise theorem) and there is no positive steady state: the optimal filter for a truly constant value is the cumulative average, not an EMA.
    - **The transient.** The EMA is optimal only once the Kalman filter has settled. From a poor start, the Kalman filter's larger early gains converge faster; the EMA's first-measurement initialization is a crude substitute.
    - **A random walk is a model.** The EMA with $\alpha = K_\infty$ is optimal for a random-walk true value. For a deterministic ramp, such as steady bulking, the right model has a nonzero $\Delta x_k$ ([Chapter 10](#ch10-sec-linear-process-models)) or a second state for the rate ([Chapter 13](#ch13-sec-a-second-state-variable)).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch9-sec-innovations -->
    ## Innovations

    A filter never sees its own errors $e_k$, because the true values are unknown. It does see its {term}`innovations <innovation>` $\tilde y_k = z_k - \hat x_k^-$, and they turn out to carry exactly the information needed to check $Q$ and $R$.

    /// note | 📖 **Definition**
    <u>**Innovation variance**</u>

    The innovation variance at step $k$ is the variance $S_k := \operatorname{Var}(\tilde y_k)$ of the {term}`innovation` $\tilde y_k = z_k - \hat x_k^-$.
    ///

    Since $z_k = x_k + v_k$ and $\hat x_k^- = x_k + e_k^-$, the innovation is $\tilde y_k = v_k - e_k^-$: measurement noise minus prediction error.

    /// admonition | 📐 **Lemma (Orthogonality)**
        attrs: {class: lemma, id: ch9-lem-orthogonality}
    Assume (K1)–(K3). For all $1 \le j \le k$, $\operatorname{Cov}(e_k, \tilde y_j) = 0$: the Kalman filter's error is uncorrelated with every innovation so far.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    By induction on $k$; for $k = 1$ only the case $j = k$ below arises. Assume the claim for $k - 1$.

    *Case $j = k$.* Using $e_k = (1 - K_k)e_k^- + K_k v_k$, $\tilde y_k = v_k - e_k^-$, and $\operatorname{Cov}(e_k^-, v_k) = 0$,
    $$\operatorname{Cov}(e_k, \tilde y_k) = -(1 - K_k)P_k^- + K_k R = K_k(P_k^- + R) - P_k^- = 0,$$
    because $K_k = P_k^-/(P_k^- + R)$. This is where the optimal gain matters.

    *Case $j < k$.* Write $e_k = (1 - K_k)(e_{k-1} - w_k) + K_k v_k$. The innovation $\tilde y_j = v_j - e_j^-$ is a linear combination of $e_0, w_1, \ldots, w_j, v_1, \ldots, v_j$ (Kalman filter theorem, item 1), so it is uncorrelated with $w_k$ and $v_k$ by (K3) and the linearity of covariance, and $\operatorname{Cov}(e_{k-1}, \tilde y_j) = 0$ by the inductive hypothesis because $j \le k - 1$. Hence $\operatorname{Cov}(e_k, \tilde y_j) = (1 - K_k)(0 - 0) + K_k \cdot 0 = 0$. $\blacksquare$
    ///

    /// admonition | 📐 **Theorem (Properties of the Innovations)**
        attrs: {class: theorem, id: ch9-thm-properties-of-the-innovations}
    Assume (K1)–(K3). For every $k \ge 1$:
    1. $\mathbb E\tilde y_k = 0$;
    2. $S_k = P_k^- + R$, and therefore $K_k = P_k^-/S_k$;
    3. $\operatorname{Cov}(\tilde y_j, \tilde y_k) = 0$ for every $j \ne k$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    1. $\mathbb E\tilde y_k = \mathbb E v_k - \mathbb E e_k^- = 0$.
    2. $S_k = \operatorname{Var}(v_k - e_k^-) = R + P_k^- - 2\operatorname{Cov}(v_k, e_k^-) = P_k^- + R$.
    3. By symmetry of covariance we may take $j < k$. Write $\tilde y_k = v_k - e_k^- = v_k - e_{k-1} + w_k$. Then $\operatorname{Cov}(\tilde y_k, \tilde y_j) = \operatorname{Cov}(v_k, \tilde y_j) - \operatorname{Cov}(e_{k-1}, \tilde y_j) + \operatorname{Cov}(w_k, \tilde y_j)$. The first and last terms vanish because $\tilde y_j$ is a linear combination of $e_0, w_1, \ldots, w_j, v_1, \ldots, v_j$ with $j < k$; the middle term vanishes by the Orthogonality lemma, since $j \le k - 1$. $\blacksquare$
    ///

    So when the filter's model is right, its innovations are zero-mean, uncorrelated, and have the variances $S_k$ that the filter itself computes. Unlike the errors, the innovations can be computed from the measurements alone, which makes these properties *testable*. Note that item 3 relies on the gains being optimal for the true $Q$ and $R$; a mis-tuned filter produces correlated innovations, which [Chapter 10](#ch10-sec-validating-a-model-are-the-innovations-white) uses as a test of the model.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch9-sec-checking-the-noise-levels -->
    ## Checking the Noise Levels

    The simplest test compares the size of each innovation with the size the filter expects.

    /// note | 📖 **Definition**
    <u>**Normalized innovation squared**</u>

    The normalized innovation squared (NIS) at step $k$ of a Kalman filter is $\epsilon_k := \tilde y_k^2/S_k$, the squared {term}`innovation` divided by the {term}`innovation variance` $S_k = P_k^- + R$ computed by the filter.
    ///

    If the filter's $Q$, $R$, and $P_0$ are the true ones, then by the previous theorem $\mathbb E\epsilon_k = \mathbb E[\tilde y_k^2]/S_k = \operatorname{Var}(\tilde y_k)/S_k = 1$. If the innovations are systematically larger than the filter expects, the NIS averages more than $1$; if smaller, less. To decide how far from $1$ an average may stray by chance, we need its distribution, which brings in a new family of distributions.

    /// note | 📖 **Definition**
    <u>**Chi-squared distribution**</u>

    For $n \in \mathbb N^+$, the chi-squared distribution with $n$ degrees of freedom, written $\chi^2_n$, is the {term}`distribution` of $g_1^2 + \cdots + g_n^2$, where $g_1, \ldots, g_n$ are independent random variables with the standard {term}`normal distribution` $\mathcal N(0, 1)$.
    ///

    /// admonition | 📐 **Theorem (One Degree of Freedom)**
        attrs: {class: theorem, id: ch9-thm-one-degree-of-freedom}
    If $g \sim \mathcal N(0, 1)$, then $g^2 \sim \chi^2_1$ has the density
    $$f(t) = \frac{e^{-t/2}}{\sqrt{2\pi t}} \quad (t > 0), \qquad f(t) = 0 \quad (t \le 0),$$
    with mean $1$ and variance $2$. Consequently $\chi^2_n$ has mean $n$ and variance $2n$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Let $\phi(u) := e^{-u^2/2}/\sqrt{2\pi}$. For $t > 0$, by symmetry of $\phi$,
    $$F(t) := \mathbb P(g^2 \le t) = \mathbb P(-\sqrt t \le g \le \sqrt t) = 2\int_0^{\sqrt t}\phi(u)\,du,$$
    and $F(t) = 0$ for $t \le 0$. By the fundamental theorem of calculus and the chain rule, $F'(t) = 2\phi(\sqrt t)\cdot\frac{1}{2\sqrt t} = f(t)$ for $t > 0$, and since $F(t) \to 0$ as $t \to 0^+$, $F(t) = \int_0^t f(s)\,ds$ (an improper integral at $0$): $f$ is a density of $g^2$. Its mean is $\mathbb E[g^2] = \operatorname{Var} g = 1$. For the variance we need $\mathbb E[g^4]$. Since $\phi'(u) = -u\phi(u)$, integration by parts gives
    $$\int_{-\infty}^{\infty} u^4\phi(u)\,du = \Big[-u^3\phi(u)\Big]_{-\infty}^{\infty} + 3\int_{-\infty}^{\infty} u^2\phi(u)\,du = 0 + 3 \cdot 1 = 3,$$
    because $u^3\phi(u) \to 0$ as $u \to \pm\infty$. So $\operatorname{Var}(g^2) = \mathbb E[g^4] - (\mathbb E[g^2])^2 = 2$. For $\chi^2_n$, add $n$ independent copies: means and variances add (Chapter 6). $\blacksquare$
    ///

    /// admonition | 📐 **Theorem (NIS Under the Normal Model)**
        attrs: {class: theorem, id: ch9-thm-nis-under-the-normal-model}
    Assume (K1)–(K3) with $e_0$, all $w_k$, and all $v_k$ independent and normal, and let the filter use the true $Q$, $R$, and $P_0$. Then $\tilde y_k \sim \mathcal N(0, S_k)$ and $\epsilon_k \sim \chi^2_1$ for every $k$, and the $\epsilon_k$ are independent, so $\sum_{k=1}^N \epsilon_k \sim \chi^2_N$. The average NIS $\bar\epsilon := \frac1N\sum_{k=1}^N \epsilon_k$ has mean $1$ and variance $2/N$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    $\tilde y_k = v_k - e_k^-$ is a linear combination of the independent normal random variables $e_0, w_1, \ldots, w_k, v_1, \ldots, v_k$ (dropping any with coefficient $0$ or variance $0$), so by [Chapter 5](#ch5-cor-linear-combinations-of-independent-normals)'s corollary on linear combinations of independent normal random variables it is normal, with mean $0$ and variance $S_k$ by the Properties of the Innovations theorem. By Chapter 5's formula for $aX + b$, $\tilde y_k/\sqrt{S_k} \sim \mathcal N(0, 1)$, so $\epsilon_k \sim \chi^2_1$. The innovations are uncorrelated, and uncorrelated random variables that are *jointly* normal (as these are, being linear combinations of the same independent normal variables) are independent; this fact is proven in [Chapter 12](#ch12-cor-uncorrelated-jointly-normal-vectors-are-independent). Hence the $\epsilon_k$ are independent, their sum is $\chi^2_N$ by definition, and the mean and variance of $\bar\epsilon$ follow from the previous theorem. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The NIS checks a property that every correctly working filter should have.

    /// note | 📖 **Definition**
    <u>**Filter consistency**</u>

    A filter that reports an {term}`error variance` $P_k$ alongside each estimate $\hat x_k$ is consistent if, at every step $k$, its {term}`estimation error` has mean zero and the reported error variance equals the actual one: $\mathbb E e_k = 0$ and $\operatorname{Var} e_k = P_k$.
    ///

    Under (K1)–(K3) the Kalman filter is consistent; that is item 2 of the Kalman filter theorem. Consistency itself cannot be checked without the true values, but it has a consequence that can: a consistent filter with the right $R$ and $Q$ predicts its innovation variances correctly, so its NIS averages $1$. This gives the **NIS test**: over $N$ steps, compute $\bar\epsilon$, and compare it with the interval that contains $\chi^2_N/N$ with probability $95\%$ (computed here by simulating $\chi^2_N$; by the central limit theorem it is approximately $1 \pm 1.96\sqrt{2/N}$ for large $N$).

    - $\bar\epsilon$ **above** the interval: the innovations are larger than the filter expects. It is overconfident: $Q$ or $R$ is too small, or the model misses something (a cat, a trend, outliers).
    - $\bar\epsilon$ **below** the interval: the innovations are smaller than expected. The filter is underconfident: $Q$ or $R$ is too large.
    - $\bar\epsilon$ **inside** the interval: no evidence of a problem. This does not prove the filter consistent, since a wrong $Q$ and a wrong $R$ can partially cancel, but a failed test does prove that something is wrong.

    Below, the left panel shows the innovations of the shifting-load filter with their $\pm 2\sqrt{S_k}$ band, using the filter settings from the sliders (shown again). The right panel shows a histogram of the NIS values from 300 simulated runs of the same experiment, compared with the $\chi^2_1$ density.
    """)
    return


@app.cell
def _(np, shift_Q, shift_R, shift_t, scale_x):
    # jb: include=false
    _rng = np.random.default_rng(31)
    nis_mc_x = scale_x + np.cumsum(_rng.normal(0.0, np.sqrt(shift_Q), (300, shift_t.size)), axis=1)
    nis_mc_v = _rng.normal(0.0, np.sqrt(shift_R), (300, shift_t.size))
    nis_mc_e0 = _rng.standard_normal(300)
    return nis_mc_e0, nis_mc_v, nis_mc_x


@app.cell(hide_code=True)
def _(
    chi2_1_pdf,
    graphic,
    kalman_filter_1d,
    kf_Q,
    kf_R,
    kf_cat,
    kf_z,
    mo,
    nis_interval,
    nis_mc_e0,
    nis_mc_v,
    nis_mc_x,
    np,
    plt,
    shift_t,
):
    _P0 = 100.0
    _f = kalman_filter_1d(kf_z, 150.0, _P0, kf_Q.value, kf_R.value)
    _nis = _f["innov"] ** 2 / _f["S"]
    _lo, _hi = nis_interval(shift_t.size)

    _cat = np.where(shift_t > 7.5, 10.0, 0.0) if kf_cat.value else np.zeros_like(shift_t)
    _x_mc = nis_mc_x + _cat
    _z_mc = _x_mc + nis_mc_v
    _x0_mc = _x_mc[:, 0] * 0 + 155.0 + np.sqrt(_P0) * nis_mc_e0
    _g = kalman_filter_1d(_z_mc, _x0_mc, _P0, kf_Q.value, kf_R.value)
    _nis_mc = _g["innov"] ** 2 / _g["S"]
    _y = _f["innov"]
    _lag1 = np.corrcoef(_y[10:-1], _y[11:])[0, 1]

    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(10, 3.9))
    _ax1.plot(shift_t, _y, ".", color="C0", markersize=3, label=r"innovation $\tilde y_k$")
    _ax1.fill_between(shift_t, -2 * np.sqrt(_f["S"]), 2 * np.sqrt(_f["S"]), color="C1", alpha=0.2, label=r"$\pm 2\sqrt{S_k}$")
    _ax1.axhline(0, color="black", linewidth=0.8)
    _ax1.set_ylim(-6, 12)
    _ax1.set_xlabel("time (s)")
    _ax1.set_ylabel("innovation (lb)")
    _ax1.set_title("Innovations of one run", style="italic")
    _ax1.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax1.legend(fontsize=8, loc="upper left")

    _t = np.linspace(0.02, 8, 400)
    _ax2.hist(np.clip(_nis_mc.ravel(), 0, 8), bins=np.linspace(0, 8, 41), density=True, color="C0", alpha=0.6,
              label="NIS, 300 simulated runs")
    _ax2.plot(_t, chi2_1_pdf(_t), color="black", linewidth=1.5, label=r"$\chi^2_1$ density")
    _ax2.set_yscale("log")
    _ax2.set_ylim(1e-4, 5)
    _ax2.set_xlabel(r"NIS $\epsilon_k$ (values above 8 shown at 8)")
    _ax2.set_ylabel("density")
    _ax2.set_title("NIS versus the chi-squared distribution", style="italic")
    _ax2.grid(visible=True, alpha=0.9, linewidth=0.4, which="both")
    _ax2.legend(fontsize=8, loc="upper right")
    _fig.tight_layout()

    _verdict = "inside" if _lo <= _nis.mean() <= _hi else ("above" if _nis.mean() > _hi else "below")
    _out = mo.vstack([
        mo.hstack([kf_Q, kf_R, kf_cat], justify="start", gap=2),
        graphic(_fig),
        mo.md(
            rf"This run: average NIS $\bar\epsilon = {_nis.mean():.2f}$ over $N = {shift_t.size}$ steps, "
            rf"{_verdict} the 95% interval $[{_lo:.2f}, {_hi:.2f}]$. Average over all 300 runs: ${_nis_mc.mean():.2f}$. "
            rf"Correlation of neighboring innovations in this run: ${_lag1:+.2f}$."
        ),
    ])
    plt.close(_fig)
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With the true settings ($Q = 0.01$, $R = 1$) the histogram follows the $\chi^2_1$ density and the average NIS is close to $1$. Shrinking $Q$ or $R$ makes the filter overconfident and pushes the average up; enlarging them pushes it down. Picking up the cat produces a burst of huge innovations that no correctly tuned random-walk filter expects. Notice also the correlation of neighboring innovations. It is near zero with the right settings and clearly negative when $Q$ is too large: the filter chases the noise, so each innovation partly undoes the previous one. When $Q$ is too small it is positive on average, because a lagging filter's innovations share a sign for long stretches, but a single 15-second run may not show this clearly.

    The figure below repeats the experiment for many mis-tuned filters at once. Each point is the average NIS (left) or the actual RMS error (right) over 300 runs, for a filter whose $Q$ (or $R$) is the true value multiplied by the factor on the horizontal axis, with the other variance correct. The NIS crosses $1$ at the true value, and the actual error is smallest there, which is the practical meaning of "optimal".
    """)
    return


@app.cell
def _(
    IMAGES_DIR,
    kalman_filter_1d,
    nis_mc_e0,
    nis_mc_v,
    nis_mc_x,
    np,
    plt,
    shift_Q,
    shift_R,
):
    # jb: include=false
    _factors = np.array([0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0])
    _z = nis_mc_x + nis_mc_v
    _x0 = 155.0 + 10.0 * nis_mc_e0
    _res = {"Q": ([], []), "R": ([], [])}
    for _which in ("Q", "R"):
        for _fac in _factors:
            _Qf = shift_Q * _fac if _which == "Q" else shift_Q
            _Rf = shift_R * _fac if _which == "R" else shift_R
            _g = kalman_filter_1d(_z, _x0, 100.0, _Qf, _Rf)
            _res[_which][0].append(np.mean(_g["innov"][:, 20:] ** 2 / _g["S"][20:]))
            _res[_which][1].append(np.sqrt(np.mean((_g["x"][:, 20:] - nis_mc_x[:, 20:]) ** 2)))

    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(10, 3.6))
    for _which, _style, _lab in (("Q", "-o", r"scaling $Q$"), ("R", "--s", r"scaling $R$")):
        _ax1.plot(_factors, _res[_which][0], _style, color="C1" if _which == "Q" else "C0", label=_lab)
        _ax2.plot(_factors, _res[_which][1], _style, color="C1" if _which == "Q" else "C0", label=_lab)
    _ax1.axhline(1.0, color="black", linewidth=1)
    _ax1.set_xscale("log")
    _ax1.set_yscale("log")
    _ax1.set_xlabel("filter's value / true value")
    _ax1.set_ylabel("average NIS")
    _ax1.set_title("Average NIS of a mis-tuned filter", style="italic")
    _ax1.grid(visible=True, alpha=0.9, linewidth=0.4, which="both")
    _ax1.legend(fontsize=8)
    _ax2.set_xscale("log")
    _ax2.set_xlabel("filter's value / true value")
    _ax2.set_ylabel("actual RMS error (lb)")
    _ax2.set_title("Actual error of a mis-tuned filter", style="italic")
    _ax2.grid(visible=True, alpha=0.9, linewidth=0.4, which="both")
    _ax2.legend(fontsize=8)
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch9_nis_mistuning.svg")
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch9_nis_mistuning.svg" class="graphic" alt="Average NIS and actual RMS error of Kalman filters whose Q or R is scaled by factors from 0.01 to 100. The average NIS crosses 1 and the error is smallest at the true values." />
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **The $\chi^2$ interval assumes normal noise.** With outliers or other heavy-tailed noise, large NIS values occur more often than $\chi^2_1$ predicts even for a well-tuned filter.
    - **The test sees $S_k = P_k^- + R$ only.** It detects a wrong total, not which of $Q$ and $R$ is wrong: a too-small $Q$ and a too-large $R$ can cancel. And when $Q$ is small compared with $R$, the total is dominated by $R$: in the figure above, a $Q$ that is ten times too small raises the average NIS by only about $15\%$. Estimate $R$ separately (sample variance), then tune $Q$ with the NIS and the innovations' correlation.
    - **Averages hide structure.** A filter can pass the average test while lagging badly during maneuvers. Also look at the innovations over time and at their correlation from step to step ([Chapter 10](#ch10-sec-validating-a-model-are-the-innovations-white)).
    - **Short records give wide intervals.** With $N = 28$ the 95% interval is roughly $[0.55, 1.59]$; only gross mis-tuning is detectable.
    ///

    <!-- label: ch9-sec-tuning-on-the-bulking-data -->
    ## Tuning on the Bulking Data

    Now the Introduction's 28 daily weigh-ins while bulking: the true weight rises by $0.2$ lb per day, and each reading has noise with standard deviation $1$ lb. Choose the expected daily change $\Delta x$, the filter's $Q$, and the filter's $R$ (the readings' true noise variance is $1$). The filter starts from $\hat x_0 = 150$ lb with $P_0 = 100\ \text{lb}^2$.

    - With $\Delta x = 0$ the random-walk model must explain the steady gain as process noise. A large $Q$ lets it follow the trend but passes more noise; a small $Q$ makes it lag. By the steady-state theorem and Chapter 6's ramp-lag formula, the lag approaches $(0.2 - \Delta x)\frac{1 - K_\infty}{K_\infty}$ lb once the filter has settled (for small $Q$ that takes longer than 28 days), and the innovations stay positive on average. For small $Q$ the NIS flags the mismatch. With the default $Q = 0.1$ it does not, even though the estimate lags by about half a pound: passing the test is not proof of a good model.
    - With $\Delta x = 0.2$ the model is right, and a small $Q$ works best.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    bulk_dx = mo.ui.slider(steps=[0.0, 0.1, 0.2, 0.3], value=0.0, label=r"Expected change $\Delta x$ (lb/day)", show_value=True)
    bulk_Q = mo.ui.slider(
        steps=[0.0, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0], value=0.1, label=r"Filter's $Q$ (lb$^2$ per day)", show_value=True,
    )
    bulk_R = mo.ui.slider(steps=[0.25, 0.5, 1.0, 2.0, 4.0], value=1.0, label=r"Filter's $R$ (lb$^2$)", show_value=True)
    return bulk_Q, bulk_R, bulk_dx


@app.cell(hide_code=True)
def _(
    bulk_Q,
    bulk_R,
    bulk_days,
    bulk_dx,
    bulk_x,
    bulk_z,
    graphic,
    kalman_filter_1d,
    mo,
    nis_interval,
    np,
    plt,
    steady_state,
):
    _f = kalman_filter_1d(bulk_z, 150.0, 100.0, bulk_Q.value, bulk_R.value, dx=bulk_dx.value)
    _nis = _f["innov"] ** 2 / _f["S"]
    _lo, _hi = nis_interval(bulk_z.size)
    _rmse = np.sqrt(np.mean((_f["x"][7:] - bulk_x[7:]) ** 2))

    _fig, _ax = plt.subplots(figsize=(9, 3.9))
    _ax.plot(bulk_days, bulk_z, "o", markerfacecolor="none", markeredgecolor="black", label="weigh-ins")
    _ax.plot(bulk_days, bulk_x, color="black", linewidth=1.2, label="true weight")
    _ax.plot(bulk_days, _f["x_pred"], ":", color="red", marker=".", markersize=4, linewidth=1, label=r"prediction $\hat x_k^-$")
    _ax.plot(bulk_days, _f["x"], color="C1", linewidth=2, label=r"estimate $\hat x_k$")
    _ax.fill_between(bulk_days, _f["x"] - 2 * np.sqrt(_f["P"]), _f["x"] + 2 * np.sqrt(_f["P"]), color="C1", alpha=0.2,
                     label=r"$\pm 2\sqrt{P_k}$")
    _ax.set_ylim(151, 164)
    _ax.set_xlabel("day")
    _ax.set_ylabel("weight (lb)")
    _ax.set_title("Kalman filter on the bulking weigh-ins", style="italic")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.legend(fontsize=8, loc="upper left", ncol=2)
    _fig.tight_layout()

    if bulk_Q.value > 0:
        _p, _K, _Pinf = steady_state(bulk_Q.value, bulk_R.value)
        _ss = (
            rf"Steady-state gain $K_\infty = {_K:.3f}$; predicted steady lag $(0.2 - \Delta x)(1 - K_\infty)/K_\infty = "
            rf"{(0.2 - bulk_dx.value) * (1 - _K) / _K:.2f}$ lb; actual average of $x_k - \hat x_k$ over days 15–28: "
            rf"${np.mean(bulk_x[14:] - _f['x'][14:]):.2f}$ lb."
        )
    else:
        _ss = r"With $Q = 0$ the gain keeps shrinking like $1/k$; there is no steady state."
    _verdict = "inside" if _lo <= _nis.mean() <= _hi else ("above" if _nis.mean() > _hi else "below")
    _out = mo.vstack([
        mo.hstack([bulk_dx, bulk_Q, bulk_R], justify="start", gap=2),
        graphic(_fig),
        mo.md(
            rf"Average NIS ${_nis.mean():.2f}$, {_verdict} the 95% interval $[{_lo:.2f}, {_hi:.2f}]$ for $N = 28$; "
            rf"average innovation ${_f['innov'][7:].mean():+.2f}$ lb; RMS error over days 8–28: ${_rmse:.2f}$ lb. "
            + _ss
        ),
    ])
    plt.close(_fig)
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The random-walk model with $\Delta x = 0$ can be made to work, but only by declaring a steady, predictable trend to be unpredictable noise, and the price is a lag or extra noise. A model that *expects* the gain does much better. Where should $\Delta x$ come from if we do not know the rate in advance? From a better process model, which is the subject of the next chapter.

    <!-- label: ch9-sec-summary -->
    ## Summary

    - **Measuring $R$:** the **sample variance** $s^2 = \frac{1}{n-1}\sum(y_i - \bar y)^2$ of readings of a constant is an unbiased estimate of $R$ (Bessel's correction), though a noisy one; datasheets give a lower bound; **quantization** with step $\Delta$ adds about $\Delta^2/12$ when the signal spans several steps, and a bias when it does not.
    - **Modeling change:** **process noise** $w_k = x_k - x_{k-1} - \Delta x_k$ with variance $Q$, modeled as **white noise**, makes the true value a **random walk** around its expected path, and the predict step gives $P_k^- = P_{k-1} + Q$.
    - **The scalar Kalman filter** alternates predict ($\hat x_k^- = \hat x_{k-1} + \Delta x_k$, $P_k^- = P_{k-1} + Q$) and update ($K_k = P_k^-/(P_k^- + R)$, $\hat x_k = \hat x_k^- + K_k\tilde y_k$, $P_k = (1 - K_k)P_k^-$). It is optimal at every step; with $Q = 0$ it is the cumulative average with $R/P_0$ virtual readings.
    - **Steady state:** with constant $Q, R > 0$, $K_k \to K_\infty = p/(p + R)$ with $p = \big(Q + \sqrt{Q^2 + 4QR}\big)/2$, and the filter becomes an EMA with $\alpha = K_\infty$, where $Q/R = \alpha^2/(1 - \alpha)$. No other EMA has a smaller steady-state error variance.
    - **Checking:** the innovations have mean $0$, **innovation variance** $S_k = P_k^- + R$, and are uncorrelated. The **normalized innovation squared** $\tilde y_k^2/S_k$ follows the **chi-squared distribution** $\chi^2_1$ under normal noise, and its average tests the **consistency** of the filter's noise levels.

    <!-- label: ch9-sec-whats-next -->
    ## What's Next

    The random-walk model treats every change it does not expect as noise. When the change is partly predictable, as a weight gain driven by a known calorie surplus is, a better prediction $\hat x_k^-$ means a smaller $P_k^-$ and a better estimate. [Chapter 10](ch10_process_models.md) builds such process models, including the bulking energy balance, and shows how to evaluate them with the innovations introduced here.
    """)
    return


if __name__ == "__main__":
    app.run()
