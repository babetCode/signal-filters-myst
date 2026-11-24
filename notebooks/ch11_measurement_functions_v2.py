# /// script
# dependencies = [
#     "marimo>=0.25.1",
#     "matplotlib==3.11.2",
#     "numpy==2.5.3",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="Measurement Functions", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "When Sensors Measure Something Else"
    abbreviations:
      iff: if and only if
      diff: null
      ADC: analog-to-digital converter
      SPS: samples per second
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
def display_settings(Path, dedent, mo, plt):
    # jb: include=false
    plt.style.use("default")
    IMAGES_DIR = Path(__file__).parent / "public"

    def graphic(x):
        return mo.Html(dedent(f'''\
            <div class="graphic">
                {mo.as_html(x)}
            </div>
            '''))

    return IMAGES_DIR, graphic


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// seealso | 🔗 **Prerequisites**
        attrs: {class: no-icon}
    - [Chapter 5](ch5_random_variables_v2.md): measurement noise and the normal distribution.
    - [Chapter 6](ch6_expectation_and_variance_v2.md): linearity of expectation, $\operatorname{Var}(aX + b)$, variances and covariances of sums, and unbiased estimators.
    - [Chapter 7](ch7_optimal_alpha_v2.md): the optimal gain by completing the square, and what correlated errors do to an average.
    - [Chapter 9](ch9_noise_levels_v2.md): the scalar Kalman filter and the innovation variance.
    - [Chapter 10](ch10_process_models_v2.md): system state, process model, and control input.
    - [Appendix C: Functions of Several Variables](appendix_c_calculus_v2.md) (optional; only for the partial-derivative route to the normal equations) and [Appendix C: Taylor's Theorem](appendix_c_calculus_v2.md) (only for the preview of nonlinear measurement functions).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Every chapter so far has assumed that the scale reports pounds: $z_k = x_k + v_k$. It doesn't. Its load cell produces a tiny voltage, and its analog-to-digital converter turns that voltage into an integer, a number of *counts*, that is only *related* to your weight. Most sensors are like this: a thermometer reports a resistance, an accelerometer a voltage, a GPS receiver signal travel times. The filter's state is the quantity we care about; the sensor reports something else.

    The bridge between the two is a **measurement function**: the reading the sensor should produce for a given state. This chapter writes it down for the scale, estimates its unknown parameters from weights we know (calibration by least squares), and adds it to the Kalman filter. Along the way we meet a problem the scalar filter cannot solve. If the scale's offset drifts, it becomes a second unknown, and a reading cannot tell a heavier person on a scale with a low offset from a lighter person on a scale with a high one.

    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    A measurement function $h$ predicts what the sensor should read for a given state. The filter compares the actual reading with that prediction and converts the surprise back into state units through the gain $K = P^-h/(h^2P^- + R)$. Errors in $h$ are not noise: they are bias, and no amount of averaging removes them.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## From Pounds to Counts

    A bathroom scale's load cells are strain gauges wired as a bridge whose output voltage is proportional to the force on the platform, plus a small imbalance even when the platform is empty. The HX711 converter samples that voltage at 10 or 80 SPS and outputs a 24-bit signed integer [@avia_hx711_datasheet]. Over the scale's working range the count is, to a good approximation, a straight-line function of the weight on the platform:
    $$z_k = h\,x_k + c + v_k,$$
    where

    - $x_k$ is the weight in pounds (the state),
    - $h$ is the **sensitivity**, the number of counts per pound (our scale: $h = 20{,}000$ counts/lb),
    - $c$ is the **offset**, the reading with an empty platform (our scale: $c = 85{,}000$ counts), and
    - $v_k$ is noise. When a person stands on the scale it is dominated by body sway; we use a standard deviation of $20{,}000$ counts, which is $1$ lb, as in earlier chapters.

    So a 155 lb person produces readings around $20{,}000 \cdot 155 + 85{,}000 = 3{,}185{,}000$ counts. One count is $1/20{,}000 = 0.00005$ lb, so the converter's resolution is far finer than the noise, and the quantization noise of [Chapter 9](ch9_noise_levels_v2.md) is negligible here.

    The straight line $x \mapsto hx + c$ is an example of the following idea.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Measurement function**</u>

    For a sensor that measures a system, the function $h$ that maps each possible state $x$ to the reading the sensor would produce in state $x$ if there were no noise.
    ///

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Measurement model**</u>

    An equation that describes each measurement as the {term}`measurement function` of the state plus a random error:
    $$z_k = h(x_k) + v_k,$$
    where $h$ is known and $v_k$ is a random variable with a specified distribution (the {term}`measurement noise`), usually with mean $0$ and variance $R$.
    ///

    When the noise has mean $0$, $h(x)$ is the *average* reading in state $x$. For the scale we reuse the letter $h$: the measurement function is $x \mapsto hx + c$, and the number $h$ is its slope. Chapters 7–10 used the measurement model with $h(x) = x$. Together with a process model, a measurement model completes the description a Kalman filter needs: the process model says how the state moves, and the measurement model says what the sensor reports about it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Calibration by Least Squares

    The manufacturer does not know $h$ and $c$ exactly: they vary from one load cell to the next. They have to be measured.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Calibration**</u>

    The process of estimating the unknown parameters of a sensor's measurement function (such as $h$ and $c$ in $z = hx + c + v$) from readings taken while the measured quantity has known values.
    ///

    To calibrate the scale we place known weights on it: an empty platform and plates of $45$, $90$, and $135$ lb, taking $m$ readings each. That gives $n = 4m$ pairs $(x_i, z_i)$, where $x_i$ is the known plate weight and $z_i = h x_i + c + v_i$. Each pair alone is noisy. Which line fits all of them best? The standard answer is to make the misfits, squared, as small as possible.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Least squares**</u>

    A method of fitting a family of functions $g_\theta$, indexed by parameters $\theta$, to data pairs $(x_1, z_1), \ldots, (x_n, z_n)$: the *least-squares estimate* is a parameter value $\hat\theta$ that minimizes the sum of squared residuals
    $$J(\theta) := \sum_{i=1}^{n}\big(z_i - g_\theta(x_i)\big)^2.$$
    ///

    For a straight line, $\theta = (h, c)$ and $g_\theta(x) = hx + c$. Write
    $$\bar x := \frac1n\sum_{i=1}^n x_i, \qquad \bar z := \frac1n\sum_{i=1}^n z_i, \qquad S_{xx} := \sum_{i=1}^n (x_i - \bar x)^2, \qquad S_{xz} := \sum_{i=1}^n (x_i - \bar x)(z_i - \bar z).$$

    /// important | 📐 **Theorem (Least-Squares Line)**
        attrs: {class: no-icon}
    If the $x_i$ are not all equal, then $J(h, c) = \sum_{i=1}^n (z_i - h x_i - c)^2$ has exactly one minimizer,
    $$\hat h = \frac{S_{xz}}{S_{xx}}, \qquad \hat c = \bar z - \hat h\,\bar x.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    We complete the square twice, first in $c$ and then in $h$, as Chapter 7 did for the gain.

    *Step 1 (best $c$ for a fixed $h$).* Let $r_i := z_i - h x_i$ and $\bar r := \frac1n\sum_i r_i = \bar z - h\bar x$. Then $r_i - c = (r_i - \bar r) + (\bar r - c)$, and since $\sum_i (r_i - \bar r) = 0$, the cross term vanishes:
    $$J(h, c) = \sum_{i=1}^n (r_i - \bar r)^2 + n\,(\bar r - c)^2.$$
    For fixed $h$ this is smallest exactly when $c = \bar r = \bar z - h\bar x$.

    *Step 2 (best $h$).* With that $c$, $r_i - \bar r = (z_i - \bar z) - h(x_i - \bar x)$, so, writing $S_{zz} := \sum_i (z_i - \bar z)^2$,
    $$J(h, \bar z - h\bar x) = S_{zz} - 2h\,S_{xz} + h^2 S_{xx} = S_{xx}\Big(h - \frac{S_{xz}}{S_{xx}}\Big)^2 + S_{zz} - \frac{S_{xz}^2}{S_{xx}}.$$
    Because $S_{xx} > 0$ (the $x_i$ are not all equal), this is smallest exactly when $h = S_{xz}/S_{xx} = \hat h$.

    *Conclusion.* For every $(h, c)$, $J(h, c) \ge J(h, \bar z - h\bar x) \ge J(\hat h, \bar z - \hat h\bar x) = J(\hat h, \hat c)$. Equality throughout requires $h = \hat h$ (Step 2) and then $c = \bar z - \hat h\bar x = \hat c$ (Step 1). $\blacksquare$
    ///

    The same answer comes from calculus ([Appendix C: Functions of Several Variables](appendix_c_calculus_v2.md)): at a minimum both partial derivatives vanish,
    $$\frac{\partial J}{\partial c} = -2\sum_{i=1}^n (z_i - h x_i - c) = 0, \qquad \frac{\partial J}{\partial h} = -2\sum_{i=1}^n x_i\,(z_i - h x_i - c) = 0.$$
    These are the **normal equations**. Vanishing derivatives are only a *necessary* condition for a minimum; the proof above shows that here they are also sufficient. The name comes from geometry: the equations say that the list of residuals $(z_i - hx_i - c)_i$ has dot product $0$ with the lists $(1, \ldots, 1)$ and $(x_1, \ldots, x_n)$, that is, it is perpendicular ("normal") to both ([Appendix D: Vectors](appendix_d_linear_algebra_v2.md)).
    """)
    return


@app.cell
def _(np):
    # jb: echo=true
    def fit_line(x, z):
        """Least-squares line z ~ h x + c through the points (x_i, z_i).

        z may hold several data sets, one per row (same x for all)."""
        x = np.asarray(x, dtype=float)
        z = np.asarray(z, dtype=float)
        x_bar = x.mean()
        z_bar = z.mean(axis=-1)
        S_xx = np.sum((x - x_bar) ** 2)
        S_xz = np.sum((x - x_bar) * (z - z_bar[..., None]), axis=-1)
        h_hat = S_xz / S_xx
        c_hat = z_bar - h_hat * x_bar
        return h_hat, c_hat

    return (fit_line,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    How accurate is the calibration? The answer depends on the noise, on the number of readings, and on how spread out the plates are.

    /// important | 📐 **Theorem (Accuracy of the Calibration)**
        attrs: {class: no-icon}
    Suppose the plate weights $x_i$ are known exactly, not all equal, and $z_i = h x_i + c + v_i$, where the $v_i$ have mean $0$, variance $R$, and are pairwise {term}`uncorrelated`. Then $\hat h$ and $\hat c$ are {term}`unbiased`, and
    $$\operatorname{Var}(\hat h) = \frac{R}{S_{xx}}, \qquad \operatorname{Var}(\hat c) = R\Big(\frac1n + \frac{\bar x^2}{S_{xx}}\Big), \qquad \operatorname{Cov}(\hat h, \hat c) = -\frac{\bar x\,R}{S_{xx}}.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Since $\sum_i (x_i - \bar x) = 0$, we have $S_{xz} = \sum_i (x_i - \bar x)\,z_i$ and $\sum_i (x_i - \bar x)\,x_i = S_{xx}$. Substituting $z_i = h x_i + c + v_i$,
    $$\hat h = \frac{1}{S_{xx}}\sum_{i=1}^n (x_i - \bar x)(h x_i + c + v_i) = h + \frac{1}{S_{xx}}\sum_{i=1}^n (x_i - \bar x)\,v_i.$$
    So $\mathbb E[\hat h] = h$, and, the $v_i$ being uncorrelated, $\operatorname{Var}(\hat h) = \frac{1}{S_{xx}^2}\sum_i (x_i - \bar x)^2 R = R/S_{xx}$ ([Chapter 6](ch6_expectation_and_variance_v2.md)). Next, with $\bar v := \frac1n\sum_i v_i$, we have $\bar z = h\bar x + c + \bar v$, so
    $$\hat c = \bar z - \hat h\,\bar x = c + \bar v - (\hat h - h)\,\bar x,$$
    and $\mathbb E[\hat c] = c$. The covariance of $\bar v$ and $\hat h - h$ is $\frac{1}{n S_{xx}}\sum_i (x_i - \bar x)R = 0$. Hence $\operatorname{Var}(\hat c) = \operatorname{Var}(\bar v) + \bar x^2\operatorname{Var}(\hat h) = R/n + \bar x^2 R/S_{xx}$, and $\operatorname{Cov}(\hat h, \hat c) = \operatorname{Cov}(\hat h, \bar v) - \bar x\operatorname{Var}(\hat h) = -\bar x R/S_{xx}$. $\blacksquare$
    ///

    /// important | 📐 **Corollary (Calibration Error at a Given Weight)**
        attrs: {class: no-icon}
    Under the same assumptions, the calibrated line's error at a weight $x$, $(\hat h x + \hat c) - (hx + c)$, has mean $0$ and variance
    $$R\Big(\frac1n + \frac{(x - \bar x)^2}{S_{xx}}\Big).$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    The error is $(\hat h - h)x + (\hat c - c)$, with mean $0$ and variance $x^2\operatorname{Var}(\hat h) + \operatorname{Var}(\hat c) + 2x\operatorname{Cov}(\hat h, \hat c) = R\big(x^2 + \bar x^2 - 2x\bar x\big)/S_{xx} + R/n$. $\blacksquare$
    ///

    Three lessons follow. More readings (larger $n$) help, but so do plates that are far apart (larger $S_{xx}$). The line is most accurate in the middle of the plates, at $x = \bar x$, and gets worse the farther we extrapolate: a 155 lb person is beyond our heaviest plate. And $\hat h$ and $\hat c$ are negatively correlated when $\bar x > 0$: a line that is too steep must start too low to pass through the middle of the data. With our plates the correlation coefficient is $-\bar x/\sqrt{S_{xx}/n + \bar x^2} \approx -0.80$, whatever $m$ is. Uncertainties that are correlated like this are the subject of [Chapter 12](ch12_vectors_matrices_covariance_v2.md).

    The plot below simulates a calibration. The left panel shows each reading's deviation from the true line, converted to pounds, together with the fitted line's deviation; the shaded band is $\pm 2$ standard deviations from the corollary. The right panel repeats the calibration 1000 times and plots the errors of $\hat h$ and $\hat c$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    cal_sigma = mo.ui.slider(
        1000, 40000, step=1000, value=20000, show_value=True,
        label="Noise per plate reading (counts)",
    )
    cal_m = mo.ui.slider(1, 30, step=1, value=10, show_value=True, label="Readings per plate $m$")
    return cal_m, cal_sigma


@app.cell
def _(cal_m, cal_sigma, fit_line, np):
    # jb: include=false
    H_TRUE = 20_000.0  # counts/lb
    C_TRUE = 85_000.0  # counts
    PLATES = np.array([0.0, 45.0, 90.0, 135.0])
    _eps = np.random.default_rng(11).standard_normal((4, 30))
    _eps_mc = np.random.default_rng(12).standard_normal((1000, 4, 30))
    cal_x = np.repeat(PLATES, cal_m.value)
    cal_z = np.round(H_TRUE * cal_x + C_TRUE + cal_sigma.value * _eps[:, : cal_m.value].ravel())
    h_hat, c_hat = fit_line(cal_x, cal_z)
    _z_mc = H_TRUE * cal_x + C_TRUE + cal_sigma.value * _eps_mc[:, :, : cal_m.value].reshape(1000, -1)
    h_hat_mc, c_hat_mc = fit_line(cal_x, _z_mc)
    return C_TRUE, H_TRUE, c_hat, c_hat_mc, cal_x, cal_z, h_hat, h_hat_mc


@app.cell(hide_code=True)
def _(
    C_TRUE,
    H_TRUE,
    c_hat,
    c_hat_mc,
    cal_m,
    cal_sigma,
    cal_x,
    cal_z,
    graphic,
    h_hat,
    h_hat_mc,
    mo,
    np,
    plt,
):
    _R = cal_sigma.value**2
    _n = cal_x.size
    _xbar = cal_x.mean()
    _Sxx = np.sum((cal_x - _xbar) ** 2)
    _sd_h = np.sqrt(_R / _Sxx)
    _sd_c = np.sqrt(_R * (1 / _n + _xbar**2 / _Sxx))
    _xs = np.linspace(-10, 200, 300)
    _band = 2 * np.sqrt(_R * (1 / _n + (_xs - _xbar) ** 2 / _Sxx)) / H_TRUE
    _err155 = ((h_hat - H_TRUE) * 155 + (c_hat - C_TRUE)) / H_TRUE
    _sd155 = np.sqrt(_R * (1 / _n + (155 - _xbar) ** 2 / _Sxx)) / H_TRUE

    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    _ax1.plot(cal_x, (cal_z - H_TRUE * cal_x - C_TRUE) / H_TRUE, "o", mfc="none", mec="black", ms=5, label="Readings")
    _ax1.plot(_xs, ((h_hat - H_TRUE) * _xs + (c_hat - C_TRUE)) / H_TRUE, color="C1", lw=2, label="Fitted line")
    _ax1.fill_between(_xs, -_band, _band, color="C1", alpha=0.2, label=r"$\pm 2$ s.d. of the fitted line")
    _ax1.axhline(0, color="black", lw=1.2, label="True line")
    _ax1.axvline(155, color="gray", ls=":", lw=1)
    _ax1.text(157, 0.92, "155 lb", color="gray", fontsize=9, transform=_ax1.get_xaxis_transform())
    _ax1.set_xlabel("Plate weight (lb)")
    _ax1.set_ylabel("Deviation from true line (lb)")
    _ax1.set_title("Calibration readings and fitted line", style="italic")
    _ax1.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax1.legend(fontsize=8, loc="lower left")

    _ax2.plot(h_hat_mc - H_TRUE, c_hat_mc - C_TRUE, ".", color="C0", ms=3, alpha=0.5, label="1000 calibrations")
    _ax2.plot([h_hat - H_TRUE], [c_hat - C_TRUE], "*", color="C1", ms=14, mec="black", label="This calibration")
    _ax2.axhline(0, color="black", lw=0.8)
    _ax2.axvline(0, color="black", lw=0.8)
    _ax2.set_xlabel(r"$\hat h - h$ (counts/lb)")
    _ax2.set_ylabel(r"$\hat c - c$ (counts)")
    _ax2.set_title("Calibration errors are negatively correlated", style="italic")
    _ax2.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax2.legend(fontsize=8, loc="upper right")
    _fig.tight_layout()

    _text = mo.md(
        f"This calibration: $\\hat h = {h_hat:,.0f}$ counts/lb, $\\hat c = {c_hat:,.0f}$ counts. "
        f"Theory: s.d.$(\\hat h) = {_sd_h:,.0f}$, s.d.$(\\hat c) = {_sd_c:,.0f}$; "
        f"over 1000 simulated calibrations: {np.std(h_hat_mc):,.0f} and {np.std(c_hat_mc):,.0f}, "
        f"correlation {np.corrcoef(h_hat_mc, c_hat_mc)[0, 1]:.2f}. "
        f"At 155 lb this calibration is off by **{_err155:+.2f} lb** (s.d. {_sd155:.2f} lb)."
    )
    mo.vstack([mo.hstack([cal_sigma, cal_m], justify="start", gap=2), graphic(_fig), _text])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With the default settings (the same 1 lb noise as a swaying person, 10 readings per plate) the calibration error at 155 lb has a standard deviation of about $0.3$ lb. That is larger than the uncertainty left after filtering 30 readings of a standing person ($1/\sqrt{30} \approx 0.18$ lb), and unlike that uncertainty, it will not shrink however long the person stands on the scale. Fortunately, plates do not sway: their readings are much less noisy than a person's, so a real calibration does far better. Move the noise slider down to see how quickly the error shrinks.

    Under the stated assumptions, least squares is the best we can do among unbiased estimators that are linear in the readings: this is the Gauss–Markov theorem ([Wikipedia: Gauss–Markov theorem](https://en.wikipedia.org/wiki/Gauss%E2%80%93Markov_theorem)). If the noise is also normal, the least-squares line is the line that makes the observed readings most likely ([Chapter 8](ch8_bayesian_view_v2.md)'s {term}`likelihood`), because the normal density decreases with the squared residual.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
        attrs: {class: no-icon}
    - **The plate weights are exact.** Certified calibration weights are accurate to a tiny fraction of a percent. If the $x_i$ themselves have random errors, the fitted slope is biased toward $0$ ([Wikipedia: Errors-in-variables models](https://en.wikipedia.org/wiki/Errors-in-variables_models)).
    - **The noise has mean $0$, a common variance, and no correlation.** If some plates are read more noisily than others, least squares is still unbiased but no longer the most accurate; weighting each squared residual by the inverse of its noise variance is better ([Wikipedia: Weighted least squares](https://en.wikipedia.org/wiki/Weighted_least_squares)). If the offset drifts *during* the calibration, the readings share a slowly changing error, which biases $\hat c$, and the variance formulas no longer apply.
    - **The sensor is linear.** Real load cells deviate slightly from a straight line, and they show hysteresis (the reading depends on whether the load was increasing or decreasing) and creep (a slow drift under constant load). Use plates spanning the whole working range, since the corollary shows that extrapolation amplifies errors.
    - **At least two different plate weights.** With a single plate, $S_{xx} = 0$, and any line through the average reading fits equally well: one known weight cannot determine two parameters. This is the first appearance of this chapter's main obstacle.
    - **Outliers.** Squaring gives large residuals a large influence. One mistaken reading (say, someone leaning on the platform) can tilt the line.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Filtering in Counts

    Now let a person stand on the calibrated scale. For the moment we take $h$ and $c$ as known exactly; the next section relaxes this. The process model is that of a constant weight, $x_k = x_{k-1} + w_k$ with process-noise variance $Q$ ($Q = 0$ for someone standing perfectly still), and the measurement model is
    $$z_k = h\,x_k + c + v_k, \qquad \operatorname{Var}(v_k) = R \ \text{counts}^2.$$
    The prediction step is unchanged ([Chapter 10](ch10_process_models_v2.md)): $\hat x_k^- = \hat x_{k-1}$, $P_k^- = P_{k-1} + Q$. The update must compare a reading in counts with a prediction in pounds, so it first converts the prediction into the reading it implies, $h\hat x_k^- + c$, and uses the difference as the {term}`innovation`:
    $$\tilde y_k := z_k - (h\,\hat x_k^- + c), \qquad \hat x_k = \hat x_k^- + K_k\,\tilde y_k.$$
    The innovation is in counts and the estimate in pounds, so the gain $K_k$ is in pounds per count. Which gain is best?

    /// important | 📐 **Theorem (Optimal Gain with a Measurement Function)**
        attrs: {class: no-icon}
    Suppose the prediction error $e_k^- := \hat x_k^- - x_k$ has mean $0$ and variance $P_k^- > 0$, and the measurement noise $v_k$ has mean $0$, variance $R > 0$, and is uncorrelated with $e_k^-$. Then:

    1. For every gain $K$, the updated estimate is unbiased, with error variance
    $$P(K) = (1 - Kh)^2 P_k^- + K^2 R.$$
    2. $P(K)$ is minimized by exactly one gain,
    $$K_k = \frac{P_k^-\,h}{h^2 P_k^- + R}, \qquad\text{which gives}\qquad P_k = (1 - K_k h)\,P_k^- = \frac{P_k^- R}{h^2 P_k^- + R}.$$
    3. The innovation has mean $0$ and variance $S_k = h^2 P_k^- + R$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    The estimation error is
    $$e_k = \hat x_k^- + K\big(h x_k + c + v_k - h\hat x_k^- - c\big) - x_k = e_k^- + K\,(v_k - h\,e_k^-) = (1 - Kh)\,e_k^- + K\,v_k.$$
    Its mean is $0$ by linearity, and since $e_k^-$ and $v_k$ are uncorrelated its variance is $(1 - Kh)^2 P_k^- + K^2 R$ ([Chapter 6](ch6_expectation_and_variance_v2.md)). Expanding and completing the square in $K$, with $S := h^2 P_k^- + R > 0$,
    $$P(K) = S\,K^2 - 2h P_k^- K + P_k^- = S\Big(K - \frac{h P_k^-}{S}\Big)^2 + P_k^- - \frac{h^2 (P_k^-)^2}{S},$$
    which is smallest exactly when $K = hP_k^-/S$, with minimum $P_k^-\big(S - h^2 P_k^-\big)/S = P_k^- R/S$. Since $1 - K_k h = (S - h^2P_k^-)/S = R/S$, this equals $(1 - K_k h)P_k^-$. Finally, the innovation is $\tilde y_k = h x_k + c + v_k - h\hat x_k^- - c = v_k - h\,e_k^-$, with mean $0$ and variance $h^2 P_k^- + R$. $\blacksquare$
    ///

    With $h = 1$ and $c = 0$ this is Chapter 7's {term}`optimal gain` $P^-/(P^- + R)$. The general formula makes sense in the limits: if the sensor is insensitive ($h \to 0$) the gain goes to $0$ and the reading is ignored; if the noise vanishes ($R \to 0$) the gain goes to $1/h$, which converts the reading straight into pounds, $\hat x_k = (z_k - c)/h$.

    In fact, filtering in counts is the same as converting to pounds first.

    /// important | 📐 **Theorem (Filtering in Counts Equals Filtering in Pounds)**
        attrs: {class: no-icon}
    Let $h \neq 0$. Running the filter above on the counts $z_k$ produces the same estimates and error variances as running Chapter 9's filter on the converted readings $y_k := (z_k - c)/h$ with measurement variance $R/h^2$, from the same $\hat x_0$ and $P_0$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    The two filters share the prediction step, so it suffices to show that one update step gives the same result from the same $\hat x_k^-$ and $P_k^-$; the claim then follows by induction on $k$. Chapter 9's gain for $y_k$ is $K' = P_k^-/(P_k^- + R/h^2)$, and its estimate is
    $$\hat x_k^- + K'\Big(\frac{z_k - c}{h} - \hat x_k^-\Big) = \hat x_k^- + \frac{K'}{h}\big(z_k - (h\hat x_k^- + c)\big).$$
    Now $K'/h = P_k^-/(hP_k^- + R/h) = hP_k^-/(h^2P_k^- + R) = K_k$, so the estimates agree, and $(1 - K')P_k^- = \frac{R/h^2}{P_k^- + R/h^2}P_k^- = \frac{P_k^- R}{h^2P_k^- + R} = P_k$. $\blacksquare$
    ///

    So what matters is the noise *in state units*, $R/h^2$: a more sensitive sensor with the same noise in counts is a better sensor. Why, then, bother with $h$ at all? Because "convert to the state first" only works when the measurement function can be inverted. Later in this chapter it cannot: once the offset is unknown, a reading has two unknowns behind it, and a nonlinear sensor can map many states to the same reading. The form $K = P^-h/(h^2P^- + R)$ survives in both cases, and in [Chapter 13](ch13_kalman_filter_v2.md) it becomes the Kalman gain for vectors.
    """)
    return


@app.cell
def _(np):
    # jb: echo=true
    def kalman_filter_counts(z, h, c, Q, R, x0, P0):
        """Scalar Kalman filter: x_k = x_{k-1} + w_k (lb), z_k = h x_k + c + v_k (counts)."""
        x_hat, P = float(x0), float(P0)
        estimates, variances = [], []
        for z_k in z:
            # Predict: constant weight plus process noise
            x_pred, P_pred = x_hat, P + Q
            # Update: compare the reading with the reading the prediction implies
            z_pred = h * x_pred + c          # counts
            S = h * h * P_pred + R           # innovation variance (counts^2)
            K = P_pred * h / S               # gain (lb per count)
            x_hat = x_pred + K * (z_k - z_pred)
            P = (1 - K * h) * P_pred
            estimates.append(x_hat)
            variances.append(P)
        return np.array(estimates), np.array(variances)

    return (kalman_filter_counts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Sensor Bias and a Drifting Tare

    The filter above assumed that $h$ and $c$ are known. In reality we use the calibrated $\hat h$ and $\hat c$, and the true offset may since have moved: load cells and converters drift with temperature, and the platform's own weight can change (a bath mat left on it). The filter then interprets the readings with the wrong measurement function.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Sensor bias**</u>

    Given the measurement function $h$ used to interpret a sensor, the sensor's *bias* at step $k$ is the mean difference between the actual reading and the reading $h$ predicts when the true state is $x_k$:
    $$b_k := \mathbb E[z_k] - h(x_k).$$
    The sensor is *unbiased* (with respect to $h$) iff $b_k = 0$ for every $k$.
    ///

    A bias is a property of the sensor *together with* the function we use to interpret it, just as {term}`estimator bias` in [Chapter 6](ch6_expectation_and_variance_v2.md) is a property of an estimator. If the true readings are $z_k = h x_k + c + v_k$ with zero-mean $v_k$, but we interpret them with $x \mapsto \hat h x + \hat c$, the bias is $b_k = (h - \hat h)\,x_k + (c - \hat c)$: a gain error contributes a bias proportional to the weight, and an offset error a constant one.

    /// important | 📐 **Theorem (Bias Does Not Average Out)**
        attrs: {class: no-icon}
    Let the true readings of a constant weight $x$ be $z_k = h x + c + v_k$ with $\mathbb E[v_k] = 0$, and let the filter use $\hat h \neq 0$ and $\hat c$ with $Q = 0$ and first-measurement initialization. Then for every number of readings $N$,
    $$\mathbb E[\hat x_N] - x = \frac{(h - \hat h)\,x + (c - \hat c)}{\hat h}.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    By the previous theorem, the filter's estimates are those of Chapter 9's filter applied to $y_k = (z_k - \hat c)/\hat h$. With $Q = 0$ and first-measurement initialization that filter's gains are $1/k$ ([Chapter 7](ch7_optimal_alpha_v2.md), [Chapter 9](ch9_noise_levels_v2.md)), so $\hat x_N$ is the average $\frac1N\sum_{k=1}^N y_k$. By linearity of expectation, $\mathbb E[\hat x_N] = (hx + c - \hat c)/\hat h$; subtract $x = \hat h x/\hat h$. $\blacksquare$
    ///

    The filter's reported variance $P_N$ shrinks like $1/N$, but the bias stays. The filter becomes *confidently wrong*. A 1% error in $h$ is an error of about 1.5 lb at 155 lb; an offset that has drifted by 10,000 counts is a 0.5 lb error for everyone.

    The plot below filters 3 seconds of readings (30 samples at 10 SPS) from a 155 lb person, interpreted with the calibration from the previous plot; move the calibration sliders there and this plot changes too. The slider here shifts the true offset away from its calibrated value. The circles are the readings converted with the calibrated function, $(z_k - \hat c)/\hat h$; the right axis shows the corresponding counts. The filter starts with no information ($\hat x_0 = 0$, $P_0 = 10^6$ lb²), which is equivalent to first-measurement initialization.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    tare_drift = mo.ui.slider(
        -40000, 40000, step=2000, value=0, show_value=True,
        label="Offset drift since calibration (counts)",
    )
    return (tare_drift,)


@app.cell(hide_code=True)
def _(
    C_TRUE,
    H_TRUE,
    c_hat,
    graphic,
    h_hat,
    kalman_filter_counts,
    mo,
    np,
    plt,
    tare_drift,
):
    _x_true = 155.0
    _sigma = 20_000.0
    _t = np.arange(1, 31) / 10
    _c_now = C_TRUE + tare_drift.value
    _z = np.round(H_TRUE * _x_true + _c_now + _sigma * np.random.default_rng(1).normal(0.0, 1.0, 30))
    _est, _P = kalman_filter_counts(_z, h_hat, c_hat, Q=0.0, R=_sigma**2, x0=0.0, P0=1e6)
    _bias = ((H_TRUE - h_hat) * _x_true + (_c_now - c_hat)) / h_hat

    _fig, _ax = plt.subplots(figsize=(8, 4.3))
    _ax.plot(_t, (_z - c_hat) / h_hat, "o", mfc="none", mec="black", label=r"Converted readings $(z_k - \hat c)/\hat h$")
    _ax.axhline(_x_true, color="black", lw=1.5, label="True weight")
    _ax.plot(_t, _est, color="C1", lw=2, label="Estimate")
    _ax.fill_between(_t, _est - 2 * np.sqrt(_P), _est + 2 * np.sqrt(_P), color="C1", alpha=0.2, label=r"$\pm 2\sqrt{P_k}$")
    _ax.set_ylim(150, 160)
    _ax.set_xlabel("Time (s)")
    _ax.set_ylabel("Weight (lb)")
    _sec = _ax.secondary_yaxis(
        "right", functions=(lambda w: (h_hat * w + c_hat) / 1e6, lambda z: (z * 1e6 - c_hat) / h_hat)
    )
    _sec.set_ylabel("Reading (millions of counts)")
    _ax.set_title("Filtering raw counts with the calibrated measurement function", style="italic")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.legend(fontsize=8, loc="lower right")
    _fig.tight_layout()

    _text = mo.md(
        f"After 3 s the filter reports **{_est[-1]:.2f} ± {2 * np.sqrt(_P[-1]):.2f} lb** (±2 s.d.); "
        f"the true weight is 155 lb, an error of **{_est[-1] - _x_true:+.2f} lb**. "
        f"The bias predicted by the theorem is **{_bias:+.2f} lb**; the rest is noise."
    )
    mo.vstack([tare_drift, graphic(_fig), _text])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
        attrs: {class: no-icon}
    - **The measurement function is known.** Calibration errors and offset drift are biases. They do not show up in $P_k$, so the filter reports more confidence than it deserves. Re-zeroing ("taring") the scale before each use removes offset drift; periodic recalibration catches changes in $h$.
    - **The noise is white with known variance $R$.** Body sway is slow, so consecutive readings share part of their error. As in [Chapter 7](ch7_optimal_alpha_v2.md), ignoring that correlation makes the filter overconfident. Estimating $R$ from data ([Chapter 9](ch9_noise_levels_v2.md)) at the sampling rate actually used helps; so does sampling more slowly.
    - **The sensor stays in its linear range.** The HX711's 24-bit output tops out at $2^{23} - 1 = 8{,}388{,}607$ counts, which on our scale is about $(8{,}388{,}607 - 85{,}000)/20{,}000 \approx 415$ lb. Beyond that every reading is the same, and the model fails silently.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Two Unknowns, One Reading

    Suppose the offset drifts enough that we cannot trust the last tare, and we try to estimate it along with the weight. Every reading of a person on the platform has the form $z = hx + c + v$. For any number $\delta$, the pair $(x + \delta,\; c - h\delta)$ predicts *exactly* the same reading as $(x, c)$:
    $$h\,(x + \delta) + (c - h\delta) = hx + c.$$
    So the readings, however many, cannot distinguish a person who is 1 lb heavier on a scale whose offset is 20,000 counts lower. Averaging pins down the combination $hx + c$ ever more precisely, but tells us nothing about how it splits between $x$ and $c$. In the left panel below, all the pairs consistent with the averaged readings lie in a diagonal band, and the band never shrinks to a point.

    The remedy is a reading in which the two unknowns enter differently. With the platform **empty**, $x = 0$ and the reading is $z_0 = c + v_0$, which measures the offset alone: a horizontal band in the right panel. Together, the two kinds of reading pin down both unknowns. This is exactly what a scale does when it tares itself at power-on, before you step on.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch11_two_unknowns_v2.svg" class="graphic" alt="Two panels in the plane of weight (horizontal) and offset in pound-equivalents (vertical). Left: thirty standing readings constrain the pair only to a diagonal band. Right: thirty empty-platform readings add a horizontal band, and the two bands intersect in a small region around the true pair." />
    """)
    return


@app.cell
def _(IMAGES_DIR, np, plt):
    # jb: include=false
    _x0, _c0 = 155.0, 85_000.0 / 20_000.0  # true weight and offset (lb-equivalent)
    _half = 2 / np.sqrt(30)  # +/- 2 s.d. of a 30-reading average (lb)
    _xs = np.linspace(145, 165, 200)
    _fig, _axes = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True)
    for _i, _ax in enumerate(_axes):
        _ax.fill_between(_xs, _x0 + _c0 - _xs - _half, _x0 + _c0 - _xs + _half, color="C0", alpha=0.25,
                         label=r"standing readings: $x + c/h \approx$ const.")
        if _i == 1:
            _ax.axhspan(_c0 - _half, _c0 + _half, color="C3", alpha=0.25, label=r"empty-platform readings: $c/h \approx$ const.")
        _ax.plot([_x0], [_c0], "k+", ms=12, mew=2, label="true $(x, c/h)$")
        _ax.set_xlim(145, 165)
        _ax.set_ylim(-5, 14)
        _ax.set_xlabel("Weight $x$ (lb)")
        _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
        _ax.legend(fontsize=8, loc="upper right")
    _axes[0].set_ylabel("Offset $c/h$ (lb)")
    _axes[0].set_title("Thirty standing readings", style="italic")
    _axes[1].set_title("Plus thirty empty-platform readings", style="italic")
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch11_two_unknowns_v2.svg")
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What if the offset drifts *while* the person stands on the scale, as it might for a scale that monitors a patient's weight around the clock? Then there is no empty-platform reading to lean on, and treating the last tare value $\hat c$ as exact makes every converted reading $y_k = (z_k - \hat c)/h$ share the same error $(c - \hat c)/h$. If the tare is uncertain with variance $\sigma_c^2$ (in counts²), the average of $N$ converted readings has error variance
    $$\frac{\sigma_c^2}{h^2} + \frac{R}{N h^2},$$
    which never falls below $\sigma_c^2/h^2$. A scalar filter that ignores the shared error reports only the second term, exactly the overconfidence that [Chapter 7](ch7_optimal_alpha_v2.md) predicted for correlated errors.

    The honest model has two unknowns, weight and offset, each with its own process model (the offset, say, a slow {term}`random walk`). Their uncertainties become correlated, just like $\hat h$ and $\hat c$ in the calibration and like weight and rate in [Chapter 10](ch10_process_models_v2.md)'s rate model, and a single number $P_k$ can no longer describe them. That is the job of the covariance matrix in [Chapter 12](ch12_vectors_matrices_covariance_v2.md). [Chapter 13](ch13_kalman_filter_v2.md) then turns this chapter's question, "can the readings separate the unknowns?", into a precise test called {term}`observability`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Sensors That Measure Something Else

    In general a sensor reports some function of the state, $z_k = h(x_k) + v_k$, and $h$ need not be a straight line. Two examples we will meet again:

    - **A swinging pendulum** ([Chapter 15](ch15_extended_kalman_filter_v2.md)). The state is the angle $\theta$, but a camera reports the horizontal position of the bob, $h(\theta) = L\sin\theta$ for a rod of length $L$.
    - **An inertial sensor** ([Chapter 19](ch19_ahrs_v2.md)). An accelerometer at rest reports gravity as seen in the sensor's own tilted axes, a nonlinear function of the attitude.

    The gain formula needs a slope, and a curve has a different slope at each point. Near the prediction, the curve is close to its tangent line (first-order Taylor approximation, [Appendix C: Taylor's Theorem](appendix_c_calculus_v2.md)):
    $$h(x) \approx h(\hat x_k^-) + h'(\hat x_k^-)\,(x - \hat x_k^-).$$
    This is a measurement function of this chapter's form, with sensitivity $h'(\hat x_k^-)$ and an offset chosen so that the line passes through $(\hat x_k^-, h(\hat x_k^-))$. So the natural filter uses the innovation $z_k - h(\hat x_k^-)$ and the gain $P_k^- h'(\hat x_k^-)\big/\big(h'(\hat x_k^-)^2 P_k^- + R\big)$. That is the extended Kalman filter of [Chapter 15](ch15_extended_kalman_filter_v2.md), which also explains when the tangent line is a poor substitute.

    The slope also tells us how informative a reading is. The figure shows $h(\theta) = \sin\theta$ (with $L = 1$ m) and readings with noise standard deviation $0.05$ m. Near $\theta = 30°$ the curve is steep, and the readings consistent with a given angle ($\pm 2$ standard deviations, shaded) correspond to a narrow range of angles. Near $\theta = 85°$ the curve is nearly flat, and the same reading is consistent with every angle from about $64°$ to $116°$. There the linearized gain is almost $0$, and rightly so: one reading cannot tell the angles apart, the same obstacle as the drifting offset, now caused by a flat slope instead of a second unknown.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch11_nonlinear_h_v2.svg" class="graphic" alt="The curve sin(theta) for theta from 0 to 120 degrees, with tangent lines at 30 and 85 degrees. Horizontal bands of plus or minus two noise standard deviations around each reading map to a narrow range of angles at 30 degrees and a wide range at 85 degrees." />
    """)
    return


@app.cell
def _(IMAGES_DIR, np, plt):
    # jb: include=false
    _sig = 0.05
    _th = np.linspace(0, 120, 400)
    _fig, _ax = plt.subplots(figsize=(8, 4.3))
    _ax.plot(_th, np.sin(np.radians(_th)), color="black", lw=1.5, label=r"$h(\theta) = \sin\theta$")
    for _th0, _col in [(30.0, "C1"), (85.0, "C3")]:
        _z0 = np.sin(np.radians(_th0))
        _slope = np.cos(np.radians(_th0)) * np.pi / 180  # per degree
        _ax.plot(_th, _z0 + _slope * (_th - _th0), color=_col, ls="--", lw=1.2, label=f"tangent at {_th0:.0f}°")
        _ax.axhspan(_z0 - 2 * _sig, _z0 + 2 * _sig, color=_col, alpha=0.12)
        _lo = np.degrees(np.arcsin(max(-1.0, _z0 - 2 * _sig)))
        _hi_val = _z0 + 2 * _sig
        _hi = np.degrees(np.arcsin(_hi_val)) if _hi_val < 1 else 180 - _lo
        _ax.axvspan(_lo, min(_hi, 120), color=_col, alpha=0.12)
        _ax.plot([_th0], [_z0], "o", color=_col)
    _ax.set_xlim(0, 120)
    _ax.set_ylim(0, 1.15)
    _ax.set_xlabel(r"Angle $\theta$ (degrees)")
    _ax.set_ylabel("Horizontal bob position (m)")
    _ax.set_title("A flat measurement function carries little information", style="italic")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.legend(fontsize=8, loc="lower right")
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch11_nonlinear_h_v2.svg")
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - A **measurement function** $h$ gives the reading a sensor would produce in each state; a **measurement model** $z_k = h(x_k) + v_k$ adds the noise. A bathroom scale's HX711 reports counts, $z = hx + c + v$, with sensitivity $h$ and offset $c$.
    - **Calibration** estimates $h$ and $c$ from known weights. The **least-squares** line is $\hat h = S_{xz}/S_{xx}$, $\hat c = \bar z - \hat h\bar x$, proven by completing the square. It is unbiased, with $\operatorname{Var}(\hat h) = R/S_{xx}$, $\operatorname{Var}(\hat c) = R(1/n + \bar x^2/S_{xx})$, and negatively correlated errors; it is least accurate far from the plates.
    - With a measurement function the optimal gain is $K = P^-h/(h^2P^- + R)$, the innovation is $z - (h\hat x^- + c)$, and its variance is $S = h^2P^- + R$. For a known, invertible $h$ this is equivalent to converting to state units first, with noise variance $R/h^2$.
    - **Sensor bias** (from calibration error or a drifting offset) does not average out, and the filter's $P_k$ does not include it.
    - A drifting offset is a second unknown that standing readings cannot separate from the weight; an empty-platform reading can. Likewise, a flat stretch of a nonlinear $h$ makes readings uninformative.

    ## What's Next

    Twice now one number has not been enough: Chapter 10's weight and rate, and this chapter's weight and offset. In both cases the uncertainties of the two unknowns are correlated, and the correlation is exactly what lets a filter learn about one unknown from a reading of the other. [Chapter 12](ch12_vectors_matrices_covariance_v2.md) introduces the tools for this: random vectors, covariance matrices, and the multivariate normal distribution. It ends by showing that conditioning a joint normal distribution on a measurement is the Kalman update in disguise.
    """)
    return


if __name__ == "__main__":
    app.run()
