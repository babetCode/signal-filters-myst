# /// script
# dependencies = [
#     "marimo>=0.25.1",
#     "matplotlib==3.11.2",
#     "numpy==2.5.3",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="8. The Bayesian View", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "Priors, Likelihoods, and Posteriors"
    abbreviations:
      iff: if and only if
      diff: null
      GPS: Global Positioning System
      MMSE: minimum mean squared error
      MAP: maximum a posteriori
      MSE: mean squared error
      CLT: central limit theorem
    numbering:
      equations: false
    -->
    """)
    return


@app.cell
def imports():
    # jb: include=false
    import marimo as mo
    import math
    import numpy as np
    import matplotlib.pyplot as plt
    from textwrap import dedent

    return dedent, math, mo, np, plt


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

    def mixture_pdf(eta, eps, var1, var2):
        """Density of outlier-mixture noise: N(0, var1) w.p. 1-eps, N(0, var2) w.p. eps."""
        return (1 - eps) * normal_pdf(eta, 0.0, var1) + eps * normal_pdf(eta, 0.0, var2)

    return mixture_pdf, normal_pdf


@app.cell
def scale_data(np):
    # jb: include=false
    scale_x = 155.0
    scale_R = 1.0
    # Same data as the Introduction: 3 s at 10 samples/s, noise sigma = 1 lb, seed 1
    scale_z = np.round(scale_x + np.random.default_rng(1).normal(0.0, 1.0, 30), 2)
    scale_t = np.arange(1, 31) / 10
    # The same readings with three large outliers (a hand on the counter, a bump)
    scale_z_outliers = scale_z.copy()
    scale_z_outliers[[5, 13, 21]] += np.array([9.0, -7.0, 12.0])
    return scale_R, scale_t, scale_x, scale_z, scale_z_outliers


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Chapter 7](ch7_optimal_alpha.md) treated the true weight as an unknown constant and asked how to combine two noisy estimates of it. This chapter takes a different point of view, the *Bayesian* one: we describe everything we know about the unknown by a probability density, and we update that density with Bayes' theorem whenever a measurement arrives.

    Why bother, if Chapter 7 already gave the answer? The Bayesian view delivers four things Chapter 7 could not:

    1. An independent derivation of the same gain, which explains *why* the formula looks the way it does.
    2. A proof that, when the noise is normal, the optimal gain is not just the best gain but the best estimator of *any* form.
    3. A recipe for what to do when the noise is *not* normal, for instance when a reading occasionally goes wild.
    4. The **Bayes filter**, a general recursion for estimating a changing quantity, of which the Kalman filter is the normal special case.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// important | 🔗 **Prerequisites**
    - [Chapter 4](ch4_probability_spaces.md): {term}`conditional probability`, the law of total probability, and Bayes' theorem for events.
    - [Chapter 5](ch5_random_variables.md): {term}`probability density functions <probability density function>`, the {term}`normal distribution` and the integral $\int_{-\infty}^\infty e^{-u^2/2}\,du = \sqrt{2\pi}$, the density of $aX + b$, {term}`joint densities <joint density>` (defined through the joint CDF) and {term}`marginal densities <marginal density>`, {term}`independent random variables` and the factorization of their joint density, the continuous convolution formula, and sums of independent normal random variables.
    - [Chapter 6](ch6_expectation_and_variance.md): {term}`expected value` and the law of the unconscious statistician (LOTUS) for densities, {term}`variance`, and {term}`mean squared error`, including $\text{MSE} = \text{variance} + \text{bias}^2$.
    - [Chapter 7](ch7_optimal_alpha.md): the lowercase convention for random quantities, {term}`estimation error`, {term}`error variance`, and the Optimal Gain theorem.
    - [Appendix C: The Riemann Integral](#appc-sec-the-riemann-integral), [Improper Integrals](appendix_c_calculus.md), and [Multiple Integrals](appendix_c_calculus.md) (Fubini's theorem and substitution).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// attention | 🗝️ **Key Idea**
    The posterior is proportional to the likelihood times the prior. With a normal prior and normal measurement noise, the posterior is normal, its mean is exactly Chapter 7's optimal update, and that mean is the best estimator of all in the mean-squared-error sense.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch8-sec-from-events-to-densities -->
    ## From Events to Densities

    In [Chapter 4](ch4_probability_spaces.md), Bayes' theorem for events,

    $$\mathbb P(A \mid B) = \frac{\mathbb P(B \mid A)\,\mathbb P(A)}{\mathbb P(B)},$$

    updated the probability that card 1 hides the queen in three-card monte from $1/3$ to $1/2$ once card 3 was revealed not to be the queen. Each factor has a role: $\mathbb P(A) = 1/3$ is what we believed *before* the observation, $\mathbb P(B \mid A) = 1$ says how well the hypothesis "card 1 is the queen" predicts the observation, $\mathbb P(B) = 2/3$ is the total probability of the observation, and $\mathbb P(A \mid B) = 1/2$ is what we believe *after* it.

    Now consider a continuous version. You are driving on *x-axis avenue*, an infinitely long, perfectly straight road. From your odometer you believe your position is about $100$ m, give or take $20$ m. Then your GPS reports a position of $130$ m, and you know its readings have normal noise with a standard deviation of $10$ m. Where are you?

    Bayes' theorem for events cannot answer this directly. Your position $x$ and the reading $z$ are continuous random variables, so $\mathbb P(z = 130) = 0$ (Chapter 5), and the conditional probability $\mathbb P(x \in A \mid z = 130)$ would require dividing by zero. The fix is to work with densities instead of probabilities.

    **Notation.** Following Chapter 7, the random variables are lowercase: $x$ is the unknown and $z$ the measurement. To keep random variables and their possible values apart, we write $\xi$ ("xi") for a possible value of $x$ and $\zeta$ ("zeta") for a possible value of $z$. So $f_x(\xi)$ is the density of $x$ at $\xi$, and $f_{x,z}(\xi, \zeta)$ is the joint density of $x$ and $z$ at $(\xi, \zeta)$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch8-sec-conditional-densities -->
    ## Conditional Densities

    /// note | 📖 **Definition**
    <u>**Conditional density**</u>

    Let $x$ and $z$ be random variables with a {term}`joint density` $f_{x,z}$, and let $f_z$ be the {term}`marginal density` of $z$. For each $\zeta$ with $f_z(\zeta) > 0$, the conditional density of $x$ given $z = \zeta$ is the function $f_{x \mid z}(\cdot \mid \zeta)$ defined by
    $$f_{x\mid z}(\xi \mid \zeta) := \frac{f_{x,z}(\xi, \zeta)}{f_z(\zeta)}, \qquad \xi \in \mathbb R.$$
    The same formula defines the conditional density of $x$ given $z_1 = \zeta_1, \ldots, z_k = \zeta_k$ when $x, z_1, \ldots, z_k$ have a joint density, with the joint density of $(z_1, \ldots, z_k)$ in the denominator.
    ///

    Exchanging the roles of $x$ and $z$ gives $f_{z \mid x}(\zeta \mid \xi) := f_{x,z}(\xi, \zeta)/f_x(\xi)$ for $f_x(\xi) > 0$. A conditional density is a genuine probability density in $\xi$: it is nonnegative, and since the marginal density is obtained by integrating out the other variable (Chapter 5),

    $$\int_{-\infty}^{\infty} f_{x\mid z}(\xi \mid \zeta)\,d\xi = \frac{1}{f_z(\zeta)}\int_{-\infty}^{\infty} f_{x,z}(\xi, \zeta)\,d\xi = \frac{f_z(\zeta)}{f_z(\zeta)} = 1.$$

    Why is this the right definition? It describes $x$ when $z$ is known to lie in a tiny interval around $\zeta$. One can show that, under mild regularity conditions on $f_{x,z}$, the event-based conditional probability $\mathbb P(x \le a \mid \zeta \le z \le \zeta + h)$, whose denominator is positive for every $h > 0$, converges to $\int_{-\infty}^{a} f_{x\mid z}(\xi \mid \zeta)\,d\xi$ as $h \to 0$. We will not need this fact, only the definition.

    /// admonition | 📐 **Theorem (Bayes' Theorem for Densities)**
        attrs: {class: theorem, id: ch8-thm-bayes-theorem-for-densities}
    Let $x$ and $z$ have a joint density, assume $f_x(\xi) > 0$ for every $\xi \in \mathbb R$, and let $f_z(\zeta) > 0$. Then for every $\xi$
    $$f_{x\mid z}(\xi \mid \zeta) = \frac{f_{z\mid x}(\zeta \mid \xi)\,f_x(\xi)}{f_z(\zeta)}, \qquad\text{where}\qquad f_z(\zeta) = \int_{-\infty}^{\infty} f_{z\mid x}(\zeta \mid \xi')\,f_x(\xi')\,d\xi'.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    By the two definitions of conditional density, both $f_{x\mid z}(\xi\mid\zeta)\,f_z(\zeta)$ and $f_{z\mid x}(\zeta\mid\xi)\,f_x(\xi)$ equal $f_{x,z}(\xi, \zeta)$. Dividing by $f_z(\zeta) > 0$ gives the first formula. The marginal density of $z$ is $f_z(\zeta) = \int f_{x,z}(\xi', \zeta)\,d\xi'$, and the integrand equals $f_{z\mid x}(\zeta \mid \xi')\,f_x(\xi')$ for every $\xi'$ because $f_x > 0$ everywhere. $\blacksquare$
    ///

    The assumption $f_x > 0$ only avoids dividing by zero. Without it the theorem still holds once we agree that $f_{z\mid x}(\zeta\mid\xi)\,f_x(\xi) := 0$ where $f_x(\xi) = 0$, except possibly for a set of values $\zeta$ of probability zero; see [Wikipedia: Bayes' theorem](https://en.wikipedia.org/wiki/Bayes%27_theorem) for the general statement.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In filtering we rarely write down a joint density directly. Instead we specify how the measurement is produced, $z = x + v$, and the next lemma turns that into the ingredients of Bayes' theorem.

    /// admonition | 📐 **Lemma (Additive Noise)**
        attrs: {class: lemma, id: ch8-lem-additive-noise}
    Let $x$ and $v$ be independent random variables with densities $f_x$ and $f_v$, and let $z := x + v$. Then $(x, z)$ has the joint density
    $$f_{x,z}(\xi, \zeta) = f_x(\xi)\,f_v(\zeta - \xi),$$
    and wherever $f_x(\xi) > 0$ the conditional density of $z$ given $x = \xi$ is $f_{z\mid x}(\zeta \mid \xi) = f_v(\zeta - \xi)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    By independence, $(x, v)$ has the joint density $f_x(\xi)\,f_v(\eta)$ (Chapter 5's factorization criteria). For numbers $a$ and $b$, the event $\{x \le a, z \le b\}$ is the event that $(x, v)$ lies in the region $B := \{(\xi, \eta) : \xi \le a,\ \eta \le b - \xi\}$. Its probability is the integral of the joint density over $B$ (Chapter 5 notes that this holds for every Borel set once the Lebesgue integral is available; $B$ is not a box), and by Fubini's theorem ([Appendix C: Multiple Integrals](#appc-sec-multiple-integrals))
    $$\mathbb P(x \le a,\ z \le b) = \int_{-\infty}^{a} f_x(\xi)\left(\int_{-\infty}^{b - \xi} f_v(\eta)\,d\eta\right) d\xi = \int_{-\infty}^{a} \int_{-\infty}^{b} f_x(\xi)\,f_v(\zeta - \xi)\,d\zeta\,d\xi,$$
    where the inner integral was rewritten with the shift $\eta = \zeta - \xi$. This expresses the joint CDF of $(x, z)$ as a double integral of $f_x(\xi)\,f_v(\zeta - \xi)$, so that function is a joint density of $(x, z)$ (Chapter 5). Dividing by $f_x(\xi)$ gives the conditional density. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch8-sec-prior-likelihood-posterior-and-evidence -->
    ## Prior, Likelihood, Posterior, and Evidence

    Bayes' theorem for densities has four ingredients, and each has a name. In all four definitions, $x$ is an unknown and $z$ a measurement of it, with a joint density, and $\zeta$ is the observed value of $z$.

    /// note | 📖 **Definition**
    <u>**Prior**</u>

    The prior of an unknown $x$ for a measurement $z$ is the probability density of $x$ used before $z$ is incorporated: the marginal density $f_x$, or, when earlier measurements $z_1, \ldots, z_{k-1}$ have already been incorporated, the {term}`conditional density` of $x$ given their observed values.
    ///

    /// note | 📖 **Definition**
    <u>**Likelihood**</u>

    For an observed value $\zeta$ of a measurement $z$ of an unknown $x$, the likelihood is the function $\xi \mapsto f_{z\mid x}(\zeta \mid \xi)$: the {term}`conditional density` of $z$ given $x = \xi$, evaluated at the observed $\zeta$ and regarded as a function of the possible values $\xi$ of $x$.
    ///

    /// note | 📖 **Definition**
    <u>**Posterior**</u>

    The posterior of an unknown $x$ given the observed value $\zeta$ of a measurement $z$ (and the observed values of any earlier measurements) is the {term}`conditional density` $\xi \mapsto f_{x\mid z}(\xi \mid \zeta)$ of $x$ given these observations.
    ///

    /// note | 📖 **Definition**
    <u>**Evidence**</u>

    The evidence of an observed value $\zeta$ of a measurement $z$ is the number $f_z(\zeta) = \int_{-\infty}^{\infty} f_{z\mid x}(\zeta\mid\xi)\,f_x(\xi)\,d\xi$: the density of $z$ at $\zeta$ computed from the {term}`likelihood` and the {term}`prior` (conditional on earlier measurements, if any).
    ///

    In these words, Bayes' theorem for densities reads

    $$\text{posterior}(\xi) = \frac{\text{likelihood}(\xi)\times\text{prior}(\xi)}{\text{evidence}}.$$

    The evidence does not depend on $\xi$; it only rescales the product so that it integrates to $1$. So we often write $\text{posterior} \propto \text{likelihood} \times \text{prior}$ ("is proportional to") and normalize at the end. Two cautions about these words:

    - **The likelihood is not a density in $\xi$.** It is a density in $\zeta$ for each fixed $\xi$, but as a function of $\xi$ it need not integrate to $1$.
    - **The prior is not the prediction.** The Introduction deliberately called $\hat x_k^-$ the {term}`prediction` and not the prior. In this book a prediction is an {term}`estimate`: a single value (or, in Chapter 7, a random variable). A prior is a whole density. They are related: when the prior is the normal density $\mathcal N(\hat x_k^-, P_k^-)$, the prediction is its mean and $P_k^-$ is its variance. Many texts use "prior" for both.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **The model must be right.** Bayes' theorem is exact, but the posterior is only as good as the prior and the likelihood fed into it. A prior that is far too narrow, or a likelihood with the wrong noise level, produces a confidently wrong posterior.
    - **Densities are required.** The formulas need $x$ and $z$ to have a joint density. Discrete unknowns use Chapter 4's version with sums; mixtures of the two are handled by measure theory.
    - **Division by zero.** The posterior is defined only for observations with $f_z(\zeta) > 0$. An observation that the model considers impossible (for instance an outlier far beyond what normal noise can produce) yields an evidence of essentially zero and a posterior dominated by numerical round-off; this is a symptom of a wrong model.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch8-sec-normal-prior-normal-likelihood -->
    ## Normal Prior, Normal Likelihood

    For the rest of the chapter we write

    $$\mathcal N(\xi;\, \mu, \sigma^2) := \frac{1}{\sqrt{2\pi\sigma^2}}\exp\!\left(-\frac{(\xi - \mu)^2}{2\sigma^2}\right)$$

    for the density of the {term}`normal distribution` $\mathcal N(\mu, \sigma^2)$ at $\xi$ (Chapter 5). When both the prior and the noise are normal, the posterior can be computed in closed form, by completing the square once more.

    /// admonition | 📐 **Theorem (Normal Update)**
        attrs: {class: theorem, id: ch8-thm-normal-update}
    Let $x \sim \mathcal N(m, P^-)$ and $v \sim \mathcal N(0, R)$ be independent with $P^- > 0$ and $R > 0$, let $z := x + v$, and let $K := P^-/(P^- + R)$. Then for every $\zeta \in \mathbb R$:

    1. The evidence is $f_z(\zeta) = \mathcal N(\zeta;\, m, P^- + R)$; that is, $z \sim \mathcal N(m, P^- + R)$.
    2. The posterior is $f_{x\mid z}(\xi\mid\zeta) = \mathcal N\big(\xi;\, m + K(\zeta - m),\ (1 - K)\,P^-\big)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    By the Additive Noise lemma, the joint density is
    $$f_x(\xi)\,f_v(\zeta - \xi) = \frac{1}{2\pi\sqrt{P^- R}}\exp\!\Big(-\tfrac12 q(\xi)\Big), \qquad q(\xi) := \frac{(\xi - m)^2}{P^-} + \frac{(\zeta - \xi)^2}{R}.$$
    Let $P := P^-R/(P^- + R)$, so that $1/P = 1/P^- + 1/R$, and let $\mu := P\,(m/P^- + \zeta/R)$. Expanding $q$ and completing the square in $\xi$,
    $$q(\xi) = \frac{\xi^2}{P} - \frac{2\xi\mu}{P} + \frac{m^2}{P^-} + \frac{\zeta^2}{R} = \frac{(\xi - \mu)^2}{P} + \Big(\frac{m^2}{P^-} + \frac{\zeta^2}{R} - \frac{\mu^2}{P}\Big).$$
    Using $\mu^2/P = P\,(m/P^- + \zeta/R)^2 = (mR + \zeta P^-)^2/\big(P^-R(P^- + R)\big)$, the bracket is
    $$\frac{(m^2R + \zeta^2P^-)(P^- + R) - (mR + \zeta P^-)^2}{P^-R\,(P^- + R)} = \frac{P^-R\,(\zeta - m)^2}{P^-R\,(P^- + R)} = \frac{(\zeta - m)^2}{P^- + R}.$$
    So the joint density equals $\frac{1}{2\pi\sqrt{P^-R}}\exp\!\big(-\frac{(\zeta - m)^2}{2(P^- + R)}\big)\exp\!\big(-\frac{(\xi - \mu)^2}{2P}\big)$.

    1. Integrating over $\xi$, with $\int e^{-(\xi-\mu)^2/(2P)}\,d\xi = \sqrt{2\pi P}$ (Chapter 5's integral after the substitution $u = (\xi - \mu)/\sqrt P$) and $P/(P^-R) = 1/(P^- + R)$:
       $$f_z(\zeta) = \frac{\sqrt{2\pi P}}{2\pi\sqrt{P^-R}}\exp\!\Big(-\frac{(\zeta - m)^2}{2(P^- + R)}\Big) = \mathcal N(\zeta;\, m, P^- + R).$$
    2. Dividing the joint density by $f_z(\zeta)$ leaves $\frac{1}{\sqrt{2\pi P}}\exp\!\big(-\frac{(\xi - \mu)^2}{2P}\big) = \mathcal N(\xi;\, \mu, P)$. Finally, $P/P^- = R/(P^- + R) = 1 - K$ and $P/R = K$, so $\mu = (1-K)\,m + K\zeta = m + K(\zeta - m)$ and $P = (1 - K)P^-$. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Compare with [Chapter 7](ch7_optimal_alpha.md): $K$ is exactly the optimal gain $P^-/(P^- + R)$, the posterior mean $m + K(\zeta - m)$ is exactly the optimal update with prediction $m$ and measurement $\zeta$, and the posterior variance $(1 - K)P^-$ is exactly the optimal error variance. Two different questions get the same answer:

    | | Chapter 7 | Chapter 8 |
    |:---|:---|:---|
    | The true value $x$ is | an unknown number | a random variable with a prior |
    | $P^-$ is the variance of | the prediction's error | our belief about $x$ |
    | The question | which gain minimizes the error variance? | what do we believe after seeing $z$? |
    | The answer | $\hat x^- + K(z - \hat x^-)$, error variance $(1-K)P^-$ | posterior $\mathcal N\big(m + K(\zeta - m), (1-K)P^-\big)$ |

    They agree because in both views the gap between the prediction and the truth has variance $P^-$ and is independent of the measurement noise.

    Item 1 of the theorem is Chapter 5's theorem on sums of independent normals once more, and its proof completes the same square. What is new is item 2: the same computation also produces the posterior.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch8-sec-where-am-i-on-x-axis-avenue -->
    ### Where Am I on x-Axis Avenue?

    Back to the road. The odometer gives the prior $x \sim \mathcal N(100, 20^2)$ (in meters), and the GPS reading has noise $v \sim \mathcal N(0, 10^2)$. With the reading $\zeta = 130$ m, the theorem gives $K = 400/(400 + 100) = 0.8$, posterior mean $100 + 0.8 \cdot 30 = 124$ m, and posterior standard deviation $\sqrt{0.2 \cdot 400} \approx 8.9$ m, tighter than either source. Use the sliders to change the three inputs. The likelihood, regarded as a function of $\xi$, is $f_v(\zeta - \xi) = \mathcal N(\xi;\, \zeta, R)$, a bell centered at the reading.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    gps_prior_sd = mo.ui.slider(2, 40, 1, value=20, label="Prior standard deviation (m)", show_value=True)
    gps_noise_sd = mo.ui.slider(2, 40, 1, value=10, label="GPS noise standard deviation (m)", show_value=True)
    gps_reading = mo.ui.slider(40, 160, 1, value=130, label=r"GPS reading $\zeta$ (m)", show_value=True)
    return gps_noise_sd, gps_prior_sd, gps_reading


@app.cell(hide_code=True)
def _(gps_noise_sd, gps_prior_sd, gps_reading, graphic, mo, normal_pdf, np, plt):
    _m, _Pm, _R, _zeta = 100.0, gps_prior_sd.value**2, gps_noise_sd.value**2, float(gps_reading.value)
    _K = _Pm / (_Pm + _R)
    _mu = _m + _K * (_zeta - _m)
    _P = (1 - _K) * _Pm
    _grid = np.linspace(0, 200, 1001)
    _prior = normal_pdf(_grid, _m, _Pm)
    _lik = normal_pdf(_grid, _zeta, _R)
    _post = _prior * _lik
    _post = _post / (_post.sum() * (_grid[1] - _grid[0]))

    _fig, _ax = plt.subplots(figsize=(8, 3.6))
    _ax.plot(_grid, _prior, color="red", linestyle=":", linewidth=2, label="prior $f_x$")
    _ax.plot(_grid, _lik, color="C0", linestyle="--", label=r"likelihood $f_v(\zeta - \xi)$")
    _ax.plot(_grid, _post, color="C1", linewidth=2, label=r"posterior (likelihood $\times$ prior, normalized)")
    _ax.plot(_grid, normal_pdf(_grid, _mu, _P), color="black", linestyle=(0, (1, 3)), linewidth=1,
             label=r"$\mathcal{N}(m + K(\zeta-m), (1-K)P^-)$")
    _ax.plot([_zeta], [0], "o", markerfacecolor="none", markeredgecolor="black", markeredgewidth=1.5, clip_on=False, zorder=5)
    _ax.set_xlabel(r"position $\xi$ (m)")
    _ax.set_ylabel("density (1/m)")
    _ax.set_ylim(bottom=0)
    _ax.set_title(r"Prior $\times$ likelihood = posterior (up to normalization)", style="italic")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.legend(fontsize=8, loc="upper left")
    _fig.tight_layout()
    _out = mo.vstack([
        mo.hstack([gps_prior_sd, gps_noise_sd, gps_reading], justify="start", gap=2),
        graphic(_fig),
        mo.md(
            rf"$K = {_K:.3f}$; posterior mean ${_mu:.1f}$ m; posterior standard deviation ${np.sqrt(_P):.1f}$ m "
            rf"(prior ${gps_prior_sd.value}$ m, GPS ${gps_noise_sd.value}$ m)."
        ),
    ])
    plt.close(_fig)
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The dotted black curve is the theorem's closed form; it lies exactly on the numerically normalized product. Notice that the posterior's width does not depend on the reading $\zeta$ at all, only on the two variances, just as $P_k$ did not depend on the measurements in Chapter 7.

    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **Normality** of both the prior and the noise is what makes the posterior normal and its mean linear in $\zeta$. With non-normal noise the posterior has another shape, and its mean is a nonlinear function of $\zeta$ (see *When the Noise Is Not Normal* below).
    - **Independence** of $x$ and $v$ is what makes the joint density factor. If the noise depends on the true value, the likelihood must be modeled accordingly.
    - **Known variances.** As in Chapter 7, the formulas use $P^-$ and $R$; if they are wrong, the posterior mean is a non-optimal update and the posterior variance is wrong.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch8-sec-the-best-estimator-of-all -->
    ## The Best Estimator of All

    Chapter 7 found the best *gain*: the best estimator of the form $\hat x^- + \alpha(z - \hat x^-)$. Could an estimator of some other form, perhaps a nonlinear function of $z$, do better? To answer this we compare against every function of $z$ at once, and the posterior provides the winner.

    For each $\zeta$ with $f_z(\zeta) > 0$, the **posterior mean** is

    $$m(\zeta) := \int_{-\infty}^{\infty} \xi\, f_{x\mid z}(\xi \mid \zeta)\,d\xi,$$

    the mean of the posterior density (when the integral converges absolutely). It is also written $\mathbb E[x \mid z = \zeta]$, the *conditional expectation* of $x$ given $z = \zeta$, and $\mathbb E[x \mid z] := m(z)$ denotes the random variable obtained by plugging the measurement into $m$.

    /// note | 📖 **Definition**
    <u>**Minimum mean squared error estimator**</u>

    Let $x$ and $z$ be random variables with $\mathbb E[x^2] < \infty$. An estimator $g^*(z)$ of $x$, where $g^*$ is a function from $\mathbb R$ to $\mathbb R$, is a minimum mean squared error (MMSE) estimator if $\mathbb E\big[(x - g^*(z))^2\big] \le \mathbb E\big[(x - g(z))^2\big]$ for every function $g : \mathbb R \to \mathbb R$ for which $g(z)$ is a random variable with $\mathbb E[g(z)^2] < \infty$.
    ///

    /// admonition | 📐 **Theorem (The Posterior Mean Is the MMSE Estimator)**
        attrs: {class: theorem, id: ch8-thm-the-posterior-mean-is-the-mmse-estimator}
    Let $x$ and $z$ have a joint density with $\mathbb E[x^2] < \infty$, and let $g$ be any function for which $g(z)$ is a random variable with $\mathbb E[g(z)^2] < \infty$. Then
    $$\mathbb E\big[(x - g(z))^2\big] = \mathbb E\big[(x - m(z))^2\big] + \mathbb E\big[(m(z) - g(z))^2\big].$$
    Consequently, the posterior mean $m(z) = \mathbb E[x \mid z]$ is an MMSE estimator, and every $g$ with $\mathbb E[(m(z) - g(z))^2] > 0$ is strictly worse.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    By LOTUS for joint densities (Chapter 6), and then by Fubini's theorem with $f_{x,z}(\xi,\zeta) = f_{x\mid z}(\xi\mid\zeta)\,f_z(\zeta)$ (values $\zeta$ with $f_z(\zeta) = 0$ contribute nothing),
    $$\mathbb E\big[(x - g(z))^2\big] = \iint (\xi - g(\zeta))^2 f_{x,z}(\xi,\zeta)\,d\xi\,d\zeta = \int f_z(\zeta)\left(\int (\xi - g(\zeta))^2 f_{x\mid z}(\xi\mid\zeta)\,d\xi\right)d\zeta.$$
    Fix $\zeta$ and write $c := g(\zeta)$ and $\mu := m(\zeta)$. Expanding $(\xi - c)^2 = (\xi - \mu)^2 + 2(\xi - \mu)(\mu - c) + (\mu - c)^2$ and using $\int f_{x\mid z}(\xi\mid\zeta)\,d\xi = 1$ and $\int (\xi - \mu)\,f_{x\mid z}(\xi\mid\zeta)\,d\xi = \mu - \mu = 0$,
    $$\int (\xi - c)^2 f_{x\mid z}(\xi\mid\zeta)\,d\xi = \int (\xi - \mu)^2 f_{x\mid z}(\xi\mid\zeta)\,d\xi + (\mu - c)^2.$$
    This is Chapter 6's "MSE = variance + bias$^2$" applied to the posterior. Integrating against $f_z(\zeta)$ gives the identity; the assumption $\mathbb E[x^2] < \infty$ (with $\mathbb E[g(z)^2] < \infty$) makes every integral finite, apart from values $\zeta$ of probability zero, which do not affect the integrals. Both terms on the right are nonnegative, and only the second depends on $g$, so the sum is smallest when $g = m$. $\blacksquare$
    ///

    /// admonition | 📐 **Corollary (The Optimal Gain Is Optimal Among All Estimators)**
        attrs: {class: corollary, id: ch8-cor-the-optimal-gain-is-optimal-among-all-estimators}
    In the setting of the Normal Update theorem, $\mathbb E[x \mid z] = m + K(z - m)$, and no function of $z$ has a smaller mean squared error. Its mean squared error is $(1 - K)P^-$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    The posterior is $\mathcal N(m + K(\zeta - m), (1-K)P^-)$, whose mean is $m + K(\zeta - m)$. By the theorem this is an MMSE estimator, and its mean squared error is $\int f_z(\zeta)\int (\xi - m(\zeta))^2 f_{x\mid z}(\xi\mid\zeta)\,d\xi\,d\zeta = \int f_z(\zeta)\,(1-K)P^-\,d\zeta = (1-K)P^-$, because the posterior variance is the same for every $\zeta$. $\blacksquare$
    ///

    So when the prior and the noise are normal, nothing beats Chapter 7's update: not a cleverer gain, not a nonlinear rule, nothing. [Chapter 12](ch12_vectors_matrices_covariance.md) extends this to vectors, where the conditional mean of a jointly normal pair is again linear.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **Mean squared error is a choice.** Other measures of "best" give other estimators: the posterior median minimizes the mean *absolute* error, and the MAP estimate below is the peak of the posterior. For a normal posterior they all coincide.
    - **Finite second moment.** The theorem needs $\mathbb E[x^2] < \infty$; without it the mean squared error of every estimator can be infinite.
    - **Linearity is special to the normal case.** In general $\mathbb E[x \mid z]$ is a nonlinear function of $z$ and may be hard to compute. The best *gain* from Chapter 7 is then only the best *linear* estimator, and it can be beaten, as the next section shows.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch8-sec-the-peak-of-the-posterior -->
    ## The Peak of the Posterior

    The posterior mean is not the only natural single-number summary of a posterior. Another is its peak.

    /// note | 📖 **Definition**
    <u>**Maximum a posteriori estimate**</u>

    Given an observed value $\zeta$ of a measurement $z$, a maximum a posteriori (MAP) estimate of the unknown $x$ is a value $\hat\xi$ at which the {term}`posterior` density is largest: $f_{x\mid z}(\hat\xi \mid \zeta) \ge f_{x\mid z}(\xi \mid \zeta)$ for every $\xi \in \mathbb R$.
    ///

    A MAP estimate need not exist (the posterior may have no largest value) or be unique (it may have two equally high peaks). For a normal posterior $\mathcal N(\mu, P)$ the MAP estimate is the mean $\mu$, because $\exp$ is increasing and $-(\xi - \mu)^2/(2P)$ is largest exactly at $\xi = \mu$. So in the normal case, the MAP estimate, the MMSE estimate, and Chapter 7's optimal update are one and the same. For a skewed or two-peaked posterior they differ, as the next section shows.

    If the prior is nearly constant over the range where the likelihood is large, then the posterior is nearly proportional to the likelihood, and the MAP estimate is approximately the value of $\xi$ that maximizes the likelihood, the *maximum likelihood estimate* ([Wikipedia: Maximum likelihood estimation](https://en.wikipedia.org/wiki/Maximum_likelihood_estimation)).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch8-sec-when-the-noise-is-not-normal -->
    ## When the Noise Is Not Normal

    Real scales occasionally produce a wild reading: you steady yourself on the counter, the dog bumps the platform. A simple model of this: usually the noise is $\mathcal N(0, \sigma_1^2)$ with $\sigma_1 = 1$ lb, but with a small probability $\varepsilon$ it is an *outlier* drawn from $\mathcal N(0, \sigma_2^2)$ with a much larger $\sigma_2$. Precisely, $v := (1 - b)\,\sigma_1 g_1 + b\,\sigma_2 g_2$, where $g_1, g_2 \sim \mathcal N(0, 1)$ and $b$ (with $\mathbb P(b = 1) = \varepsilon$, $\mathbb P(b = 0) = 1 - \varepsilon$) are independent of each other and of $x$. By the law of total probability (Chapter 4), $\mathbb P(v \le a) = (1-\varepsilon)\,\mathbb P(\sigma_1 g_1 \le a) + \varepsilon\,\mathbb P(\sigma_2 g_2 \le a)$, so $v$ has the *mixture* density

    $$f_v(\eta) = (1 - \varepsilon)\,\mathcal N(\eta;\, 0, \sigma_1^2) + \varepsilon\,\mathcal N(\eta;\, 0, \sigma_2^2),$$

    with mean $0$ and variance $R = (1-\varepsilon)\sigma_1^2 + \varepsilon\sigma_2^2$ (integrate $\eta$ and $\eta^2$ against each part). Let the prior be $x \sim \mathcal N(m, P^-)$ with $m = 155$ lb and $P^- = 1\ \text{lb}^2$, as if several readings had already been averaged.

    **The best gain.** Chapter 7 needs only means and variances, so the best estimator of the form $m + \alpha(z - m)$ uses $K = P^-/(P^- + R)$ and has mean squared error $P^-R/(P^- + R)$. With $\varepsilon = 0.1$ and $\sigma_2 = 10$ lb, $R = 10.9\ \text{lb}^2$, so $K \approx 0.08$: because *any* reading might be an outlier, the best gain nearly ignores *every* reading.

    **The best estimator.** Bayes' theorem gives the posterior $\propto \mathcal N(\xi;\, m, P^-)\,f_v(\zeta - \xi)$. The proof of the Normal Update theorem showed that $\mathcal N(\xi;\, m, P^-)\,\mathcal N(\zeta - \xi;\, 0, \sigma^2) = \mathcal N(\zeta;\, m, P^- + \sigma^2)\,\mathcal N(\xi;\, \mu, P)$ with $\mu = m + \frac{P^-}{P^- + \sigma^2}(\zeta - m)$ and $P = \frac{P^-\sigma^2}{P^- + \sigma^2}$. Applying this to each part of the mixture, the posterior is itself a mixture of two normal densities,

    $$f_{x\mid z}(\xi\mid\zeta) = w_1(\zeta)\,\mathcal N(\xi;\, \mu_1, P_1) + w_2(\zeta)\,\mathcal N(\xi;\, \mu_2, P_2), \qquad w_i(\zeta) = \frac{\pi_i\,\mathcal N(\zeta;\, m, P^- + \sigma_i^2)}{\sum_j \pi_j\,\mathcal N(\zeta;\, m, P^- + \sigma_j^2)},$$

    where $\pi_1 = 1 - \varepsilon$, $\pi_2 = \varepsilon$, $K_i = P^-/(P^- + \sigma_i^2)$, $\mu_i = m + K_i(\zeta - m)$, and $P_i = (1 - K_i)P^-$. The weight $w_2(\zeta)$ is the posterior probability that the reading was an outlier. The MMSE estimator is the posterior mean

    $$\mathbb E[x \mid z = \zeta] = w_1(\zeta)\,\mu_1(\zeta) + w_2(\zeta)\,\mu_2(\zeta),$$

    a *nonlinear* function of $\zeta$. For a reading near $m$, $w_1 \approx 1$ and it uses the gain $K_1 = 0.5$; for a reading far from $m$, $w_2 \approx 1$ and it uses the gain $K_2 \approx 0.01$, essentially ignoring the outlier. By the theorem of the previous section it can only beat the best gain. Explore it below: the left panel shows the posterior for one reading $\zeta$; the right panel shows each estimator as a function of $\zeta$, and the text reports Monte Carlo mean squared errors from 100,000 simulated readings. With $\varepsilon = 0$ (or $\sigma_2 = \sigma_1$) the noise is normal, and the curves coincide.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    out_eps = mo.ui.slider(0.0, 0.5, 0.02, value=0.1, label=r"Outlier probability $\varepsilon$", show_value=True)
    out_sd = mo.ui.slider(1.0, 20.0, 0.5, value=10.0, label=r"Outlier standard deviation $\sigma_2$ (lb)", show_value=True)
    out_zeta = mo.ui.slider(145.0, 175.0, 0.5, value=158.0, label=r"Observed reading $\zeta$ (lb)", show_value=True)
    return out_eps, out_sd, out_zeta


@app.cell
def _(np):
    # jb: include=false
    _rng = np.random.default_rng(8)
    out_mc = {
        "x": _rng.standard_normal(100_000),
        "g1": _rng.standard_normal(100_000),
        "g2": _rng.standard_normal(100_000),
        "u": _rng.uniform(size=100_000),
    }
    return (out_mc,)


@app.cell(hide_code=True)
def _(graphic, mixture_pdf, mo, normal_pdf, np, out_eps, out_mc, out_sd, out_zeta, plt):
    _m, _Pm, _s1 = 155.0, 1.0, 1.0
    _eps, _s2, _zeta = out_eps.value, out_sd.value, out_zeta.value
    _R = (1 - _eps) * _s1**2 + _eps * _s2**2
    _K_lin = _Pm / (_Pm + _R)

    def _mmse(zz):
        _w1 = (1 - _eps) * normal_pdf(zz, _m, _Pm + _s1**2)
        _w2 = _eps * normal_pdf(zz, _m, _Pm + _s2**2)
        _mu1 = _m + _Pm / (_Pm + _s1**2) * (zz - _m)
        _mu2 = _m + _Pm / (_Pm + _s2**2) * (zz - _m)
        return (_w1 * _mu1 + _w2 * _mu2) / (_w1 + _w2), _w2 / (_w1 + _w2)

    _grid = np.linspace(140.0, 180.0, 4001)
    _h = _grid[1] - _grid[0]
    _prior = normal_pdf(_grid, _m, _Pm)
    _lik = mixture_pdf(_zeta - _grid, _eps, _s1**2, _s2**2)
    _post = _prior * _lik
    _post = _post / (_post.sum() * _h)
    _mean, _p_out = _mmse(_zeta)
    _map = _grid[np.argmax(_post)]
    _lin = _m + _K_lin * (_zeta - _m)

    # Estimator curves over a range of readings
    _zz = np.linspace(145.0, 175.0, 241)
    _post_all = normal_pdf(_grid[None, :], _m, _Pm) * mixture_pdf(_zz[:, None] - _grid[None, :], _eps, _s1**2, _s2**2)
    _map_curve = _grid[np.argmax(_post_all, axis=1)]
    _mmse_curve = _mmse(_zz)[0]

    # Monte Carlo mean squared errors
    _x = _m + np.sqrt(_Pm) * out_mc["x"]
    _v = np.where(out_mc["u"] < _eps, _s2 * out_mc["g2"], _s1 * out_mc["g1"])
    _z = _x + _v
    _mse_lin = np.mean((_m + _K_lin * (_z - _m) - _x) ** 2)
    _mse_mmse = np.mean((_mmse(_z)[0] - _x) ** 2)

    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(10, 3.9))
    _ax1.plot(_grid, _prior, color="red", linestyle=":", linewidth=2, label="prior")
    _ax1.plot(_grid, _lik, color="C0", linestyle="--", label="likelihood")
    _ax1.plot(_grid, _post, color="C1", linewidth=2, label="posterior")
    _ax1.axvline(_mean, color="C1", linewidth=1, label=f"posterior mean (MMSE) {_mean:.2f}")
    _ax1.axvline(_map, color="C3", linestyle="-.", linewidth=1, label=f"MAP {_map:.2f}")
    _ax1.axvline(_lin, color="gray", linestyle="--", linewidth=1, label=f"best gain {_lin:.2f}")
    _ax1.plot([_zeta], [0], "o", markerfacecolor="none", markeredgecolor="black", markeredgewidth=1.5, clip_on=False, zorder=5)
    _ax1.set_xlim(145, 175)
    _ax1.set_ylim(bottom=0)
    _ax1.set_xlabel(r"weight $\xi$ (lb)")
    _ax1.set_ylabel("density (1/lb)")
    _ax1.set_title(rf"Posterior for the reading $\zeta = {_zeta:.1f}$ lb", style="italic")
    _ax1.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax1.legend(fontsize=7, loc="upper right")

    _ax2.plot(_zz, _mmse_curve, color="C1", linewidth=2, label="posterior mean (MMSE)")
    _ax2.plot(_zz, _map_curve, color="C3", linestyle="-.", linewidth=1, label="MAP")
    _ax2.plot(_zz, _m + _K_lin * (_zz - _m), color="gray", linestyle="--", label=rf"best gain $K = {_K_lin:.3f}$")
    _ax2.plot(_zz, _m + 0.5 * (_zz - _m), color="C0", linestyle=":", label=r"gain $0.5$ (no outliers)")
    _ax2.set_ylim(150, 165)
    _ax2.set_xlabel(r"reading $\zeta$ (lb)")
    _ax2.set_ylabel("estimate (lb)")
    _ax2.set_title("Estimate as a function of the reading", style="italic")
    _ax2.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax2.legend(fontsize=7, loc="upper left")
    _fig.tight_layout()

    _out = mo.vstack([
        mo.hstack([out_eps, out_sd, out_zeta], justify="start", gap=2),
        graphic(_fig),
        mo.md(
            rf"Noise variance $R = {_R:.2f}\ \text{{lb}}^2$. Posterior probability that this reading is an outlier: "
            rf"${_p_out:.3f}$. Mean squared error over 100,000 simulated readings: best gain ${_mse_lin:.3f}\ \text{{lb}}^2$ "
            rf"(formula $P^-R/(P^-+R) = {_Pm * _R / (_Pm + _R):.3f}$), posterior mean ${_mse_mmse:.3f}\ \text{{lb}}^2$."
        ),
    ])
    plt.close(_fig)
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With the default settings, the posterior mean has a mean squared error of about $0.6\ \text{lb}^2$, against about $0.9\ \text{lb}^2$ for the best gain. For readings about $4$ lb from the prior mean (try $\zeta = 159.5$ lb) the posterior has two bumps, one for "good reading" and one for "outlier", and as $\zeta$ crosses this region the MAP estimate jumps from one bump to the other while the posterior mean moves smoothly.

    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **The nonlinear estimator needs the exact noise model.** It used $\varepsilon$ and $\sigma_2$. With a wrong outlier model it can do worse than the best gain, which only needs $R$.
    - **The best gain is still the best *linear* estimator**, and its mean squared error formula $P^-R/(P^-+R)$ still holds exactly, as the simulation confirms. Chapter 7's theorem never assumed normality.
    - **In practice**, outliers are often handled by *gating*, which rejects readings whose innovation is implausibly large ([Chapter 14](ch14_kalman_filters_in_practice.md)); it is a crude version of the posterior-mean curve above.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch8-sec-why-normal-the-central-limit-theorem -->
    ## Why Normal? The Central Limit Theorem

    Everything is simple when the noise is normal, and the previous section showed that it can be costly when it is not. So why is normal noise such a common assumption? Because measurement noise is often the *sum* of many small, independent effects (thermal noise in the load cell, tiny body movements, electrical interference), and sums of many independent effects are approximately normal.

    /// admonition | 📐 **Theorem (Central Limit Theorem)**
        attrs: {class: theorem, id: ch8-thm-central-limit-theorem}
    Let $y_1, y_2, y_3, \ldots$ be independent and identically distributed random variables with mean $\mu$ and variance $\sigma^2$, where $0 < \sigma^2 < \infty$, and let
    $$s_n := \frac{y_1 + \cdots + y_n - n\mu}{\sigma\sqrt n}.$$
    Then for every $a \in \mathbb R$,
    $$\lim_{n \to \infty} \mathbb P(s_n \le a) = \Phi(a) := \int_{-\infty}^{a} \frac{1}{\sqrt{2\pi}}\, e^{-u^2/2}\,du.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Not proven here; the standard proof uses characteristic functions, which this book does not develop. See [Wikipedia: Central limit theorem](https://en.wikipedia.org/wiki/Central_limit_theorem) and the references there. What is easy to check is the scaling: by linearity, $\mathbb E s_n = 0$, and since the $y_i$ are independent, hence uncorrelated, Chapter 6 gives $\operatorname{Var} s_n = n\sigma^2/(\sigma^2 n) = 1$. The theorem says that the *shape* of the distribution of $s_n$ also approaches the standard normal one.
    ///

    The demonstration below adds up $n$ independent copies of a chosen distribution, standardizes the sum to $s_n$, and compares a histogram of $20{,}000$ simulated values of $s_n$ with the standard normal density. Even a fair coin ($\pm 1$) becomes bell-shaped, although its sums can only take a lattice of values. The outlier mixture of the previous section converges too, but more slowly, and its tails stay too heavy for a long time.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    clt_dist = mo.ui.dropdown(
        options=["uniform on [-1/2, 1/2]", "fair coin: -1 or +1", "outlier mixture (epsilon = 0.1, sigma_2 = 10)"],
        value="uniform on [-1/2, 1/2]",
        label="Distribution of each term",
    )
    clt_n = mo.ui.slider(1, 50, 1, value=1, label=r"Number of terms $n$", show_value=True)
    return clt_dist, clt_n


@app.cell
def _(np):
    # jb: include=false
    _rng = np.random.default_rng(9)
    _M, _N = 20_000, 50
    _mix = np.where(_rng.uniform(size=(_M, _N)) < 0.1, 10.0, 1.0) * _rng.standard_normal((_M, _N))
    clt_samples = {
        "uniform on [-1/2, 1/2]": (_rng.uniform(-0.5, 0.5, (_M, _N)), 0.0, 1 / 12),
        "fair coin: -1 or +1": (_rng.choice([-1.0, 1.0], size=(_M, _N)), 0.0, 1.0),
        "outlier mixture (epsilon = 0.1, sigma_2 = 10)": (_mix, 0.0, 0.9 + 0.1 * 100.0),
    }
    return (clt_samples,)


@app.cell(hide_code=True)
def _(clt_dist, clt_n, clt_samples, graphic, math, mo, normal_pdf, np, plt):
    _y, _mu, _var = clt_samples[clt_dist.value]
    _n = clt_n.value
    _s = (_y[:, :_n].sum(axis=1) - _n * _mu) / np.sqrt(_var * _n)
    _grid = np.linspace(-4, 4, 401)

    _fig, _ax = plt.subplots(figsize=(8, 3.6))
    _ax.hist(_s, bins=np.linspace(-4, 4, 81), density=True, color="C0", alpha=0.6, label=rf"simulated $s_n$, $n = {_n}$")
    _ax.plot(_grid, normal_pdf(_grid, 0.0, 1.0), color="black", linewidth=1.5, label=r"standard normal density")
    _ax.set_xlim(-4, 4)
    _ax.set_xlabel(r"standardized sum $s_n$")
    _ax.set_ylabel("density")
    _ax.set_title("Sums of independent terms approach the normal distribution", style="italic")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.legend(fontsize=8, loc="upper right")
    _fig.tight_layout()

    _Phi1 = 0.5 * (1 + math.erf(1 / math.sqrt(2)))
    _tail3 = 1 - math.erf(3 / math.sqrt(2))
    _out = mo.vstack([
        mo.hstack([clt_dist, clt_n], justify="start", gap=2),
        graphic(_fig),
        mo.md(
            rf"Simulated $\mathbb P(s_n \le 1) = {np.mean(_s <= 1):.3f}$ versus $\Phi(1) = {_Phi1:.3f}$; "
            rf"simulated $\mathbb P(|s_n| > 3) = {np.mean(np.abs(_s) > 3):.4f}$ versus ${_tail3:.4f}$ for the normal distribution."
        ),
    ])
    plt.close(_fig)
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **Finite variance.** Without it the theorem fails. The average of $n$ independent standard [Cauchy](https://en.wikipedia.org/wiki/Cauchy_distribution) random variables has the same Cauchy distribution for every $n$, so averaging never helps.
    - **Many comparable effects.** If one effect dominates, such as an occasional outlier, a sum of a few terms is far from normal, and the tails converge last: rare large errors are underestimated by a normal model.
    - **Independence.** The basic theorem assumes independent terms. Versions for weakly dependent terms exist, but strongly correlated effects (a slow sway) need not average out.
    - **A limit, not an equality.** For any finite $n$, normality is an approximation. Whether it is good enough is an empirical question about the sensor, which [Chapter 9](ch9_noise_levels.md) tests with the measurements themselves.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch8-sec-the-bayes-filter -->
    ## The Bayes Filter

    So far we have incorporated one measurement. A filter must handle a stream of them while the true value may change. The Bayesian answer is a two-step recursion. We state it for the scalar model used throughout Parts I and II:

    - **(B1)** The initial value $x_0$ has a density $p_0$.
    - **(B2)** For $k \ge 1$, $\;x_k = x_{k-1} + \Delta x_k + w_k\;$ and $\;z_k = x_k + v_k$, where the expected changes $\Delta x_k$ are known numbers.
    - **(B3)** $x_0, w_1, v_1, w_2, v_2, \ldots$ are independent, each $w_k$ has the density $f_w$, and each $v_k$ has the density $f_v$.

    The random part $w_k$ of the change is the gap between the actual and the expected change that the Introduction called process noise[^w-forward]. Write $\zeta_1, \zeta_2, \ldots$ for the observed measurements, and define, for $k \ge 1$,

    - the **prior at step $k$**, $p_k^-$: the conditional density of $x_k$ given $z_1 = \zeta_1, \ldots, z_{k-1} = \zeta_{k-1}$ (for $k = 1$, simply the density of $x_1$);
    - the **posterior at step $k$**, $p_k$: the conditional density of $x_k$ given $z_1 = \zeta_1, \ldots, z_k = \zeta_k$.

    [^w-forward]: Defined precisely in [Chapter 9](ch9_noise_levels.md) as process noise.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// admonition | 📐 **Theorem (Bayes Filter Recursion)**
        attrs: {class: theorem, id: ch8-thm-bayes-filter-recursion}
    Assume (B1)–(B3), and let the observed values $\zeta_1, \zeta_2, \ldots$ have positive joint density. With $p_0$ the density of $x_0$, for every $k \ge 1$:
    $$\textbf{predict:}\quad p_k^-(\xi) = \int_{-\infty}^{\infty} f_w(\xi - \Delta x_k - \xi')\,p_{k-1}(\xi')\,d\xi',$$
    $$\textbf{update:}\quad p_k(\xi) = \frac{f_v(\zeta_k - \xi)\,p_k^-(\xi)}{\int_{-\infty}^{\infty} f_v(\zeta_k - \xi')\,p_k^-(\xi')\,d\xi'}.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    *Step 1: the joint density.* The function
    $$J_k(\xi_0, \ldots, \xi_k, \zeta_1, \ldots, \zeta_k) := p_0(\xi_0)\prod_{j=1}^{k} f_w(\xi_j - \xi_{j-1} - \Delta x_j)\,f_v(\zeta_j - \xi_j)$$
    is a joint density of $(x_0, \ldots, x_k, z_1, \ldots, z_k)$. Indeed, add the variables in the order $x_1, z_1, x_2, z_2, \ldots$. Each new variable is an earlier one plus a known number plus a fresh noise term ($w_j$ or $v_j$) that is independent of all variables added so far, because those are functions of $x_0$ and earlier noise terms (B3). The proof of the Additive Noise lemma (Fubini's theorem and a shift in the innermost integral) then shows that adding the variable multiplies the joint density by $f_w(\xi_j - \xi_{j-1} - \Delta x_j)$ or $f_v(\zeta_j - \xi_j)$.

    *Step 2: two marginals.* Let $a_k(\xi)$ be the joint density of $(x_k, z_1, \ldots, z_k)$ at $(\xi, \zeta_1, \ldots, \zeta_k)$, and $b_k(\xi)$ that of $(x_k, z_1, \ldots, z_{k-1})$ at $(\xi, \zeta_1, \ldots, \zeta_{k-1})$, with $a_0 := p_0$. Marginal densities are obtained by integrating out the other variables (Chapter 5). Integrating $J_k$ over $\xi_0, \ldots, \xi_{k-1}$ by Fubini's theorem, and noting that only the factor $f_w(\xi_k - \xi_{k-1} - \Delta x_k)$ links $\xi_k$ to the earlier variables, gives
    $$a_k(\xi) = f_v(\zeta_k - \xi)\,b_k(\xi), \qquad b_k(\xi) = \int f_w(\xi - \xi' - \Delta x_k)\,a_{k-1}(\xi')\,d\xi'.$$
    (For $b_k$, also integrate over $\zeta_k$, using $\int f_v(\zeta_k - \xi_k)\,d\zeta_k = 1$.)

    *Step 3: normalize.* Let $c_k := \int a_k(\xi)\,d\xi$, the joint density of $(z_1, \ldots, z_k)$ at the observed values, with $c_0 := 1$. By the definition of conditional density, $p_k = a_k/c_k$ and $p_k^- = b_k/c_{k-1}$. Dividing the formula for $b_k$ by $c_{k-1}$ gives the predict step. Dividing $a_k = f_v(\zeta_k - \cdot)\,b_k$ by $c_k$ gives $p_k(\xi) = f_v(\zeta_k - \xi)\,p_k^-(\xi)\,c_{k-1}/c_k$, and integrating both sides over $\xi$ shows $c_k/c_{k-1} = \int f_v(\zeta_k - \xi')\,p_k^-(\xi')\,d\xi'$, which gives the update step. $\blacksquare$
    ///

    The update step is Bayes' theorem with the prior $p_k^-$ and the likelihood $\xi \mapsto f_v(\zeta_k - \xi)$. The predict step spreads the previous posterior out: it is the density of a sum of two independent random variables, the previous state shifted by $\Delta x_k$ and the change $w_k$, which is Chapter 5's convolution formula. If there is no random change ($w_k = 0$, so $x_k = x_{k-1} + \Delta x_k$ exactly), the predict step is just the shift $p_k^-(\xi) = p_{k-1}(\xi - \Delta x_k)$, and the update is unchanged. (The same proof applies with the factors $f_w$ removed: every $x_k$ is then $x_0$ plus a known number, so only $x_0$ and the measurements need densities.) The constant bathroom-scale weight is this case with $\Delta x_k = 0$: the posterior after $k$ readings is proportional to $p_0(\xi)\prod_{j=1}^k f_v(\zeta_j - \xi)$.

    For general models, where $x_k$ depends on $x_{k-1}$ through a *transition density*, the predict step is called the Chapman–Kolmogorov equation; see [Wikipedia: Recursive Bayesian estimation](https://en.wikipedia.org/wiki/Recursive_Bayesian_estimation).

    /// note | 📖 **Definition**
    <u>**Bayes filter**</u>

    A {term}`filter` that, at each step $k$, computes the {term}`posterior` density of the current value $x_k$ given the measurements $z_1, \ldots, z_k$ from the posterior at step $k - 1$ by two steps: a predict step, which propagates the density through the model of how $x$ changes, and an update step, which multiplies the resulting {term}`prior` by the {term}`likelihood` of $z_k$ and normalizes. Its estimates are single-number summaries of the posteriors, such as their means.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When everything is normal, every density in the recursion is normal, and the filter only has to track two numbers per step.

    /// admonition | 📐 **Corollary (The Normal Bayes Filter)**
        attrs: {class: corollary, id: ch8-cor-the-normal-bayes-filter}
    Assume (B1)–(B3) with $p_0 = \mathcal N(\hat x_0, P_0)$, $f_w = \mathcal N(0, Q)$, and $f_v = \mathcal N(0, R)$, where $P_0, Q, R > 0$ (or $w_k = 0$, in which case set $Q := 0$). Then for every $k \ge 1$, $p_k^- = \mathcal N(\hat x_k^-, P_k^-)$ and $p_k = \mathcal N(\hat x_k, P_k)$, where
    $$\hat x_k^- = \hat x_{k-1} + \Delta x_k, \quad P_k^- = P_{k-1} + Q, \quad K_k = \frac{P_k^-}{P_k^- + R}, \quad \hat x_k = \hat x_k^- + K_k(\zeta_k - \hat x_k^-), \quad P_k = (1 - K_k)P_k^-.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    By induction on $k$; suppose $p_{k-1} = \mathcal N(\hat x_{k-1}, P_{k-1})$ (true for $k = 1$ by assumption). *Predict:* since $\mathcal N(\xi - \Delta x_k - \xi';\, 0, Q) = \mathcal N(\xi - \Delta x_k;\, \xi', Q)$, the predict integral is exactly the evidence integral of the Normal Update theorem, with prior $\mathcal N(\hat x_{k-1}, P_{k-1})$ for $\xi'$, noise variance $Q$, and "observation" $\xi - \Delta x_k$. By item 1 it equals $\mathcal N(\xi - \Delta x_k;\, \hat x_{k-1}, P_{k-1} + Q) = \mathcal N(\xi;\, \hat x_k^-, P_k^-)$. If $w_k = 0$, the shift gives the same result with $Q = 0$. *Update:* the normalized product $\mathcal N(\xi;\, \hat x_k^-, P_k^-)\,\mathcal N(\zeta_k - \xi;\, 0, R)$ is, by the computation in the proof of the Normal Update theorem, $\mathcal N(\xi;\, \hat x_k^- + K_k(\zeta_k - \hat x_k^-),\, (1 - K_k)P_k^-)$. $\blacksquare$
    ///

    These are Chapter 7's update equations, plus one new equation: in the predict step, the variance grows by $Q$. [Chapter 9](ch9_noise_levels.md) derives the same recursion from means and variances alone, without assuming normality, and gives it its name: the Kalman filter.

    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **Independence (B3)** is what lets the filter forget the past: all the information in $z_1, \ldots, z_{k-1}$ is carried by $p_{k-1}$. If noise terms are correlated over time, the recursion above is no longer exact.
    - **A correct model.** The filter is exact for the assumed $p_0$, $f_w$, $f_v$, and $\Delta x_k$. A wrong model gives a confidently wrong posterior; [Chapter 9](ch9_noise_levels.md) shows how to detect this.
    - **Computation.** Outside the normal case, the integrals rarely have a closed form. A grid works in one dimension (next section), but the number of grid points grows exponentially with the number of unknowns. This is why the normal case, the Kalman filter, matters so much, and why approximations such as particle filters ([Chapter 16](ch16_unscented_kalman_filter.md)) exist.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch8-sec-a-grid-bayes-filter -->
    ## A Grid Bayes Filter

    A computer cannot store a whole density, but it can store its values on a fine, evenly spaced grid $\xi_1 < \xi_2 < \cdots < \xi_N$ with spacing $h$. Integrals become Riemann sums ([Appendix C: The Riemann Integral](#appc-sec-the-riemann-integral)), $\int g(\xi)\,d\xi \approx h\sum_i g(\xi_i)$: the predict step becomes a discrete convolution, and the update a pointwise multiplication followed by normalization. This is a *grid* (or *histogram*) Bayes filter. It works for any noise densities, normal or not.
    """)
    return


@app.cell
def _(np):
    # jb: editor=true
    def grid_bayes_filter(z, grid, prior, likelihood, Q=0.0, dx=0.0):
        """Grid (histogram) Bayes filter for x_k = x_{k-1} + dx + w_k, z_k = x_k + v_k.

        z          -- measurements z_1, ..., z_n
        grid       -- evenly spaced possible values of x
        prior      -- density of x_0 evaluated on the grid
        likelihood -- function (z_k, grid) -> f_v(z_k - grid)
        Q          -- variance of a normal change w_k (0 means w_k = 0)
        dx         -- known expected change per step
        Returns an array whose row k-1 is the posterior density p_k on the grid.
        """
        h = grid[1] - grid[0]
        p = prior / (prior.sum() * h)
        if Q > 0:
            half = int(np.ceil(5 * np.sqrt(Q) / h))
            u = np.arange(-half, half + 1) * h
            kernel = np.exp(-(u**2) / (2 * Q))
            kernel = kernel / kernel.sum()  # discrete density of w_k, sums to 1
        posteriors = []
        for zk in z:
            # Predict: shift by dx, then convolve with the density of w_k
            p = np.interp(grid - dx, grid, p, left=0.0, right=0.0)
            if Q > 0:
                p = np.convolve(p, kernel, mode="same")
            # Update: multiply by the likelihood of z_k and normalize
            p = p * likelihood(zk, grid)
            p = p / (p.sum() * h)
            posteriors.append(p)
        return np.array(posteriors)

    return (grid_bayes_filter,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We run it on the Introduction's 30 bathroom-scale readings (true weight $155$ lb, noise standard deviation $1$ lb). Before the first reading we only know that the person weighs roughly $150 \pm 20$ lb, so the prior is $p_0 = \mathcal N(150, 10^2)$. For comparison, the normal Bayes filter (Chapter 7's update recursion with the same prior and $R = 1\ \text{lb}^2$) is drawn as a dashed purple line.

    - With **normal noise** and the **normal likelihood**, the grid filter and the normal Bayes filter agree to within the grid's resolution, as the corollary predicts.
    - Switch the data to include **three outliers** (at $0.6$ s, $1.4$ s, and $2.2$ s). The normal filter is yanked toward each one. Switch the grid filter's likelihood to the **outlier mixture** ($\varepsilon = 0.1$, $\sigma_2 = 10$ lb) and it barely notices them.
    - Add a **random change per step** to see the predict step at work: the posterior can no longer become arbitrarily narrow, because each step adds uncertainty. The normal Bayes filter then uses the matching $Q$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    grid_data = mo.ui.dropdown(options=["normal noise", "normal noise + 3 outliers"], value="normal noise", label="Data")
    grid_lik = mo.ui.dropdown(
        options=["normal (sigma = 1 lb)", "outlier mixture (epsilon = 0.1, sigma_2 = 10 lb)"],
        value="normal (sigma = 1 lb)",
        label="Grid filter's likelihood",
    )
    grid_sw = mo.ui.slider(
        steps=[0.0, 0.05, 0.1, 0.2, 0.3, 0.5], value=0.0, label=r"Random change per step: std of $w_k$ (lb)", show_value=True
    )
    grid_k = mo.ui.slider(1, 30, 1, value=30, label=r"Show the posterior at step $k$", show_value=True)
    return grid_data, grid_k, grid_lik, grid_sw


@app.cell(hide_code=True)
def _(
    grid_bayes_filter,
    grid_data,
    grid_k,
    grid_lik,
    grid_sw,
    graphic,
    mixture_pdf,
    mo,
    normal_pdf,
    np,
    plt,
    scale_R,
    scale_t,
    scale_x,
    scale_z,
    scale_z_outliers,
):
    _z = scale_z if grid_data.value == "normal noise" else scale_z_outliers
    _Q = grid_sw.value**2
    _m0, _P0 = 150.0, 100.0
    _grid = np.linspace(110.0, 200.0, 4501)
    _h = _grid[1] - _grid[0]
    if grid_lik.value.startswith("normal"):
        def _lik(zk, g):
            return normal_pdf(zk - g, 0.0, scale_R)
    else:
        def _lik(zk, g):
            return mixture_pdf(zk - g, 0.1, 1.0, 100.0)
    _posts = grid_bayes_filter(_z, _grid, normal_pdf(_grid, _m0, _P0), _lik, Q=_Q)
    _gmean = (_posts * _grid).sum(axis=1) * _h
    _gvar = (_posts * (_grid[None, :] - _gmean[:, None]) ** 2).sum(axis=1) * _h

    # Normal Bayes filter (Chapter 7's update with variance growth Q)
    _xs, _Ps = np.empty(_z.size), np.empty(_z.size)
    _xh, _P = _m0, _P0
    for _i, _zk in enumerate(_z):
        _Pm = _P + _Q
        _K = _Pm / (_Pm + scale_R)
        _xh = _xh + _K * (_zk - _xh)
        _P = (1 - _K) * _Pm
        _xs[_i], _Ps[_i] = _xh, _P

    _k = grid_k.value
    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(10, 3.9))
    _ax1.fill_between(_grid, _posts[_k - 1], step="mid", color="C1", alpha=0.45, label="grid posterior $p_k$")
    _ax1.plot(_grid, normal_pdf(_grid, _xs[_k - 1], _Ps[_k - 1]), color="C4", linestyle="--", label="normal Bayes filter")
    _ax1.axvline(scale_x, color="black", linewidth=1, label="true weight")
    _ax1.plot([_z[_k - 1]], [0], "o", markerfacecolor="none", markeredgecolor="black", markeredgewidth=1.5,
              clip_on=True, zorder=5, label=r"reading $z_k$")
    _ax1.set_xlim(151, 159)
    _ax1.set_ylim(bottom=0)
    _ax1.set_xlabel(r"weight $\xi$ (lb)")
    _ax1.set_ylabel("density (1/lb)")
    _ax1.set_title(f"Posterior at step k = {_k}", style="italic")
    _ax1.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax1.legend(fontsize=7, loc="upper left")

    _ax2.plot(scale_t, _z, "o", markerfacecolor="none", markeredgecolor="black", label="measurements")
    _ax2.axhline(scale_x, color="black", linewidth=1, label="true weight")
    _ax2.plot(scale_t, _gmean, color="C1", linewidth=2, label="grid posterior mean")
    _ax2.fill_between(scale_t, _gmean - 2 * np.sqrt(_gvar), _gmean + 2 * np.sqrt(_gvar), color="C1", alpha=0.2)
    _ax2.plot(scale_t, _xs, color="C4", linestyle="--", label="normal Bayes filter")
    _ax2.axvline(scale_t[_k - 1], color="gray", linewidth=0.8)
    _ax2.set_ylim(150, 162) if grid_data.value == "normal noise" else _ax2.set_ylim(145, 170)
    _ax2.set_xlabel("time (s)")
    _ax2.set_ylabel("weight (lb)")
    _ax2.set_title(r"Estimates with $\pm 2$ standard deviation band (grid)", style="italic")
    _ax2.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax2.legend(fontsize=7, loc="upper right", ncol=2)
    _fig.tight_layout()

    _out = mo.vstack([
        mo.hstack([grid_data, grid_lik], justify="start", gap=2),
        mo.hstack([grid_sw, grid_k], justify="start", gap=2),
        graphic(_fig),
        mo.md(
            rf"At step $k = {_k}$: grid posterior mean ${_gmean[_k - 1]:.4f}$ lb, variance ${_gvar[_k - 1]:.5f}\ \text{{lb}}^2$; "
            rf"normal Bayes filter mean ${_xs[_k - 1]:.4f}$ lb, variance ${_Ps[_k - 1]:.5f}\ \text{{lb}}^2$."
        ),
    ])
    plt.close(_fig)
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With normal noise, the normal likelihood, and no random change, the two filters agree to about four decimal places, and after $30$ readings the posterior variance is $1/(1/100 + 30/1) \approx 0.0333\ \text{lb}^2$, essentially Chapter 7's $R/30$: a vague prior acts like no prior at all. The grid filter costs thousands of multiplications per step where the normal filter needs a handful, which is the practical reason for the Kalman filter's popularity; the grid filter's advantage is that it does not care what shape the densities have.

    <!-- label: ch8-sec-summary -->
    ## Summary

    - For continuous random variables, Bayes' theorem works with densities: the **conditional density** $f_{x\mid z}(\xi\mid\zeta) = f_{x,z}(\xi,\zeta)/f_z(\zeta)$, and **posterior** = **likelihood** $\times$ **prior** / **evidence**. For additive noise $z = x + v$, the likelihood is $\xi \mapsto f_v(\zeta - \xi)$.
    - With a normal prior $\mathcal N(m, P^-)$ and normal noise $\mathcal N(0, R)$, the posterior is $\mathcal N\big(m + K(\zeta - m), (1-K)P^-\big)$ with $K = P^-/(P^- + R)$: exactly Chapter 7's optimal update, and the evidence is $\mathcal N(m, P^- + R)$.
    - The posterior mean $\mathbb E[x\mid z]$ is the **minimum mean squared error estimator** among all functions of $z$. In the normal case it is linear, so Chapter 7's update is the best estimator of any form; the **MAP estimate** coincides with it.
    - With non-normal noise, such as occasional outliers, the MMSE estimator is nonlinear and can beat every gain.
    - The **central limit theorem** explains why normal noise is a common, but not universal, model.
    - The **Bayes filter** alternates predict (spread the density through the model) and update (Bayes' theorem). With normal densities it reduces to Chapter 7's update plus the variance growth $P_k^- = P_{k-1} + Q$; on a grid it handles any densities in one dimension.

    <!-- label: ch8-sec-whats-next -->
    ## What's Next

    Part I answered the Introduction's question: given the noise levels $P_k^-$ and $R$, the best gain is $K_k = P_k^-/(P_k^- + R)$. But where do these numbers come from? [Chapter 9](ch9_noise_levels.md) opens Part II by estimating $R$ from data, deriving $P_k^-$ from a model of how the true value changes, and assembling the result into the scalar Kalman filter. It then answers the Introduction's original question about the EMA: in the long run the Kalman filter *becomes* an EMA, with a gain determined by the two noise levels.
    """)
    return


if __name__ == "__main__":
    app.run()
