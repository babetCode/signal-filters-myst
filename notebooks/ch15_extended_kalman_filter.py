# /// script
# dependencies = [
#     "marimo>=0.25.1",
#     "matplotlib==3.11.2",
#     "numpy==2.5.3",
#     "scipy==1.18.1",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="15. The Extended Kalman Filter", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "Linearization"
    abbreviations:
      EKF: extended Kalman filter
      IEKF: iterated extended Kalman filter
      UKF: unscented Kalman filter
      RK4: classical fourth-order Runge–Kutta method
      NEES: normalized estimation error squared
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
    from scipy.stats import chi2
    from textwrap import dedent
    from pathlib import Path

    return Path, chi2, dedent, mo, np, plt


@app.cell
def display_settings(Path, dedent, mo, plt):
    # jb: include=false
    plt.style.use("default")
    IMAGES_DIR = Path(__file__).parent.parent / "notebooks" / "public"
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    def graphic(x):
        return mo.Html(dedent(f'''\
            <div class="graphic">
                {mo.as_html(x)}
            </div>
            '''))

    def sci(value, digits=0):
        """LaTeX scientific notation, e.g. 1.2 \\times 10^{-7}."""
        _mantissa, _exponent = f"{value:.{digits}e}".split("e")
        return rf"{_mantissa} \times 10^{{{int(_exponent)}}}"

    return IMAGES_DIR, graphic, sci


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// seealso | 🔗 **Prerequisites**
        attrs: {class: no-icon}
    - [Chapter 5](ch5_random_variables.md): the distribution of $aX + b$ when $X$ is normal.
    - [Chapter 6](ch6_expectation_and_variance.md): linearity and monotonicity of expectation; the law of large numbers.
    - [Chapter 10](ch10_process_models.md): process models and discretization of continuous-time models.
    - [Chapter 11](ch11_measurement_functions.md): measurement functions.
    - [Chapter 12](ch12_vectors_matrices_covariance.md): mean vectors, covariance matrices, $\operatorname{Cov}(\mathbf A\mathbf x + \mathbf b) = \mathbf A\boldsymbol\Sigma\mathbf A^\top$, multivariate normal distributions, and confidence ellipses.
    - [Chapter 13](ch13_kalman_filter.md): the Kalman filter's predict and update equations, and the Joseph form.
    - [Chapter 14](ch14_kalman_filters_in_practice.md): the continuous white-noise acceleration model for $\mathbf Q$, multi-rate operation, NEES consistency tests, and filter divergence.
    - [Appendix C: Taylor's Theorem](appendix_c_calculus.md): the Lagrange form of the remainder.
    - [Appendix C: Functions of Several Variables](appendix_c_calculus.md): partial derivatives, the Jacobian, the chain rule, and first-order Taylor approximation.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The Kalman filter of [Chapter 13](ch13_kalman_filter.md) assumes that the next state is a *linear* function of the current one and that the sensor measures a linear function of the state. Most real systems break at least one of these assumptions. A pendulum's angular acceleration depends on $\sin\theta$; a camera measures positions through trigonometry; and every orientation filter in Parts 5 and 6 rotates vectors by matrices that depend on the state.

    This chapter's key concept is **linearization**: near the current estimate, replace each nonlinear function by the affine function that matches it best, and run the Kalman filter on that approximation. The result is the **extended Kalman filter** (EKF). It is the most widely used nonlinear filter, and it is the filter behind the attitude and gait estimators of [Chapter 19](ch19_ahrs.md) and [Chapter 21](ch21_zero_velocity_updates.md).

    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    The EKF moves the estimate through the true nonlinear functions, but moves the covariance through their Jacobians evaluated at the current estimate. It works well when the state's uncertainty is small compared with the region over which those functions look linear.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Nonlinear Systems

    Start with a concrete system. A bob hangs from a rigid rod of length $L$ whose other end turns freely about a fixed pivot. Let $\theta$ be the rod's angle from the downward vertical (counterclockwise positive) and $\omega := \dot\theta$ its angular velocity. In the pendulum example later in this chapter we derive

    $$\ddot\theta = -\frac{g}{L}\sin\theta - c\,\dot\theta,$$

    where $g$ is gravitational acceleration and $c$ is a damping rate. A camera looking along the pivot axis reports the bob's horizontal position, $L\sin\theta$. Both the dynamics and the measurement involve $\sin\theta$, and no matrix $\mathbf F$ satisfies $\mathbf F\mathbf x = [\,\omega,\ -\tfrac gL\sin\theta - c\omega\,]^\top$ for every state $\mathbf x = [\theta, \omega]^\top$. Chapter 13's model cannot describe this system.

    The pendulum fits a {term}`state-space model` with additive noise,

    $$\mathbf x_k = f(\mathbf x_{k-1}, \mathbf u_k) + \mathbf w_k, \qquad \mathbf z_k = h(\mathbf x_k) + \mathbf v_k,$$

    where:

    - $\mathbf x_k \in \mathbb R^n$ is the state, $\mathbf u_k \in \mathbb R^l$ a known {term}`control input`, and $\mathbf z_k \in \mathbb R^m$ the measurement;
    - $f: \mathbb R^n \times \mathbb R^l \to \mathbb R^n$ is the *process function*, the deterministic part of the {term}`process model`;
    - $h: \mathbb R^n \to \mathbb R^m$ is the {term}`measurement function`;
    - $\mathbf w_k$ and $\mathbf v_k$ are zero-mean noise vectors with covariance matrices $\mathbf Q$ and $\mathbf R$, as in [Chapter 13](ch13_kalman_filter.md).

    A function $\phi: \mathbb R^n \to \mathbb R^m$ is **affine** if there exist an $m \times n$ matrix $\mathbf A$ and a vector $\mathbf b \in \mathbb R^m$ such that $\phi(\mathbf x) = \mathbf A\mathbf x + \mathbf b$ for every $\mathbf x \in \mathbb R^n$. (These are the "linear functions" of school algebra; in linear algebra, "linear" also requires $\mathbf b = \mathbf 0$.) A function of two vector arguments, such as $f$, is affine if it is affine as a function of the stacked vector $(\mathbf x, \mathbf u)$; that is, if $f(\mathbf x, \mathbf u) = \mathbf F\mathbf x + \mathbf B\mathbf u + \mathbf c$ for some fixed $\mathbf F$, $\mathbf B$, $\mathbf c$.

    Chapter 13's linear state-space model is the case $f(\mathbf x, \mathbf u) = \mathbf F\mathbf x + \mathbf B\mathbf u$ and $h(\mathbf x) = \mathbf H\mathbf x$. A known constant $\mathbf c$ changes nothing essential: it can be treated as part of a known control input.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Nonlinear system**</u>

    A {term}`system` modeled, in a chosen state $\mathbf x_k$, by a {term}`state-space model` $\mathbf x_k = f(\mathbf x_{k-1}, \mathbf u_k) + \mathbf w_k$ and $\mathbf z_k = h(\mathbf x_k) + \mathbf v_k$, in which the process function $f$ is not affine in $(\mathbf x_{k-1}, \mathbf u_k)$ or the measurement function $h$ is not affine in $\mathbf x_k$.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Why does nonlinearity break the Kalman filter? Its derivation in [Chapter 13](ch13_kalman_filter.md) uses three facts from [Chapter 12](ch12_vectors_matrices_covariance.md), and each holds for affine maps $\mathbf x \mapsto \mathbf A\mathbf x + \mathbf b$:

    1. the mean passes through the map: $\mathbb E[\mathbf A\mathbf x + \mathbf b] = \mathbf A\,\mathbb E[\mathbf x] + \mathbf b$;
    2. the covariance transforms as $\operatorname{Cov}(\mathbf A\mathbf x + \mathbf b) = \mathbf A\operatorname{Cov}(\mathbf x)\mathbf A^\top$;
    3. an affine function of a normal random vector is normal.

    None of these holds for a general nonlinear $\phi$. For example, if $x$ equals $-1$ or $1$ with probability $\tfrac12$ each, then $\mathbb E[x^2] = 1$ but $(\mathbb E x)^2 = 0$, so the mean does not pass through $\phi(x) = x^2$. And if $x$ is normal, $x^2$ is never negative, so it cannot be normal. Without these facts the exact {term}`Bayes filter` of [Chapter 8](ch8_bayesian_view.md) generally has no closed form, and we must approximate. The rest of this chapter builds the most common approximation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## How a Gaussian Transforms Through a Nonlinearity

    To see what goes wrong, and how badly, take the simplest case: a scalar $x \sim \mathcal N(\mu, \sigma^2)$ and $y = \phi(x)$ for a differentiable $\phi: \mathbb R \to \mathbb R$. There are two ways to estimate the mean and variance of $y$.

    - **Monte Carlo.** Draw many independent samples $x^{(1)}, \ldots, x^{(N)}$, compute $y^{(i)} = \phi(x^{(i)})$, and take their sample mean and {term}`sample variance`. By the law of large numbers ([Chapter 6](ch6_expectation_and_variance.md)) these converge to $\mathbb E[y]$ and $\operatorname{Var}(y)$ as $N \to \infty$, whenever those exist. This is accurate but costs $N$ evaluations of $\phi$.
    - **Tangent line.** Replace $\phi$ by its tangent line at the mean, $\phi(x) \approx \phi(\mu) + \phi'(\mu)(x - \mu)$. The right-hand side has the form $ax + b$, so by [Chapter 5](ch5_random_variables.md) the approximation $y_{\text{lin}} := \phi(\mu) + \phi'(\mu)(x - \mu)$ is exactly normal:

    $$y_{\text{lin}} \sim \mathcal N\big(\phi(\mu),\ \phi'(\mu)^2\sigma^2\big).$$

    This costs one evaluation of $\phi$ and one of $\phi'$.

    How far off is the tangent line's mean $\phi(\mu)$? Taylor's theorem answers this exactly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// important | 📐 **Lemma (Mean Error of the Tangent Line)**
        attrs: {class: no-icon}
    Let $\phi: \mathbb R \to \mathbb R$ be twice continuously differentiable with $|\phi''(t)| \le M$ for all $t$, and let $x$ be a random variable with mean $\mu$ and finite variance $\sigma^2$. Then $\mathbb E[\phi(x)]$ exists and

    $$\big|\,\mathbb E[\phi(x)] - \phi(\mu)\,\big| \le \frac{M\sigma^2}{2}.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Define the remainder $r(t) := \phi(t) - \phi(\mu) - \phi'(\mu)(t - \mu)$, a continuous function of $t$. By [Taylor's theorem](appendix_c_calculus.md) with the Lagrange remainder, for each $t$ there is a $\xi$ between $\mu$ and $t$ with $r(t) = \tfrac12\phi''(\xi)(t - \mu)^2$, so

    $$|r(t)| \le \tfrac M2 (t - \mu)^2 \quad \text{for every } t.$$

    *Existence.* Since $|t - \mu| \le 1 + (t - \mu)^2$, we get $|\phi(x)| \le |\phi(\mu)| + |\phi'(\mu)|\big(1 + (x-\mu)^2\big) + \tfrac M2 (x - \mu)^2$. The right-hand side has finite expectation because $\mathbb E[(x - \mu)^2] = \sigma^2 < \infty$, so $\mathbb E[\phi(x)]$ exists by monotonicity of expectation.

    *Bound.* By linearity of expectation and $\mathbb E[x - \mu] = 0$,

    $$\mathbb E[\phi(x)] = \phi(\mu) + \phi'(\mu)\,\mathbb E[x - \mu] + \mathbb E[r(x)] = \phi(\mu) + \mathbb E[r(x)].$$

    Finally, $\big|\mathbb E[r(x)]\big| \le \mathbb E\big[|r(x)|\big] \le \tfrac M2\,\mathbb E[(x - \mu)^2] = \tfrac{M\sigma^2}{2}$. $\blacksquare$
    ///

    The bound cannot be improved: for $\phi(x) = x^2$ we have $M = 2$ and $\mathbb E[x^2] - \mu^2 = \operatorname{Var}(x) = \sigma^2 = M\sigma^2/2$ exactly. The lemma does not assume $x$ is normal. It says that the tangent line's mean error grows with the *spread* $\sigma^2$ and with the *curvature* bound $M$. The variance is harder to bound in general, but the same rule of thumb applies, as the explorer below shows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    phi_dropdown = mo.ui.dropdown(
        options={"sin x": "sin", "x²": "square", "x³": "cube", "exp x": "exp"},
        value="sin x",
        label=r"$\phi(x)$",
    )
    mu_slider = mo.ui.slider(-2.0, 2.0, 0.05, value=0.8, label=r"$\mu$", show_value=True)
    sigma_slider = mo.ui.slider(0.05, 1.5, 0.05, value=0.5, label=r"$\sigma$", show_value=True)
    return mu_slider, phi_dropdown, sigma_slider


@app.cell
def _(np):
    # jb: include=false
    # Fixed standard-normal draws, rescaled by the sliders (keeps the explorer deterministic).
    std_normal_draws = np.random.default_rng(15).standard_normal(20_000)

    scalar_functions = {
        "sin": (np.sin, np.cos, r"\sin x"),
        "square": (lambda t: t**2, lambda t: 2 * t, r"x^2"),
        "cube": (lambda t: t**3, lambda t: 3 * t**2, r"x^3"),
        "exp": (np.exp, np.exp, r"e^x"),
    }
    return scalar_functions, std_normal_draws


@app.cell(hide_code=True)
def _(
    graphic,
    mo,
    mu_slider,
    np,
    phi_dropdown,
    plt,
    scalar_functions,
    sigma_slider,
    std_normal_draws,
):
    _phi, _dphi, _name = scalar_functions[phi_dropdown.value]
    _mu, _sigma = mu_slider.value, sigma_slider.value

    _x = _mu + _sigma * std_normal_draws
    _y = _phi(_x)
    _mc_mean, _mc_std = _y.mean(), _y.std(ddof=1)
    _lin_mean, _lin_std = _phi(_mu), abs(_dphi(_mu)) * _sigma

    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(10, 4))

    _grid = np.linspace(_mu - 3.5 * _sigma, _mu + 3.5 * _sigma, 400)
    _ax1.axvspan(_mu - 2 * _sigma, _mu + 2 * _sigma, color="0.85", label=r"$\mu \pm 2\sigma$")
    _ax1.plot(_grid, _phi(_grid), "k-", label=rf"$\phi(x) = {_name}$")
    _ax1.plot(_grid, _lin_mean + _dphi(_mu) * (_grid - _mu), "r:", linewidth=2, label="tangent line at $\\mu$")
    _ax1.plot([_mu], [_lin_mean], "ro")
    _ax1.set_xlabel("$x$")
    _ax1.set_ylabel(r"$\phi(x)$")
    _ax1.set_title("The function and its tangent line", style="italic")
    _ax1.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax1.legend(loc="best", fontsize=8)

    _lo, _hi = np.percentile(_y, [0.5, 99.5])
    _span = _hi - _lo if _hi > _lo else 1.0
    _lo, _hi = _lo - 0.1 * _span, _hi + 0.1 * _span
    _ax2.hist(_y, bins=80, range=(_lo, _hi), density=True, color="C0", alpha=0.35, label="Monte Carlo samples of $y$")
    _yy = np.linspace(_lo, _hi, 400)
    if _lin_std > 0:
        _ax2.plot(_yy, np.exp(-0.5 * ((_yy - _lin_mean) / _lin_std) ** 2) / (_lin_std * np.sqrt(2 * np.pi)),
                  "r:", linewidth=2, label="tangent-line Gaussian")
    _ax2.axvline(_mc_mean, color="k", linewidth=1.5, label="Monte Carlo mean")
    _ax2.axvline(_lin_mean, color="r", linestyle=":", linewidth=1.5, label=r"tangent-line mean $\phi(\mu)$")
    _ax2.set_xlim(_lo, _hi)
    _ax2.set_xlabel(r"$y = \phi(x)$")
    _ax2.set_ylabel("density")
    _ax2.set_title("Distribution of $y$", style="italic")
    _ax2.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax2.legend(loc="best", fontsize=8)
    _fig.tight_layout()

    _table = mo.md(rf"""
    | | Monte Carlo ($N = {_x.size:,}$) | Tangent line |
    |---|---|---|
    | mean of $y$ | {_mc_mean:.4f} | {_lin_mean:.4f} |
    | standard deviation of $y$ | {_mc_std:.4f} | {_lin_std:.4f} |
    """)

    mo.vstack([mo.hstack([phi_dropdown, mu_slider, sigma_slider], justify="start", gap=2), graphic(_fig), _table])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Try $\phi(x) = \sin x$ with $\mu = 0.8$. At $\sigma = 0.1$ the two means differ by less than $0.005$. At $\sigma = 1$ the tangent line misses the mean by more than $0.2$, because $\sin x$ never exceeds 1, so the distribution of $y$ piles up just below 1 instead of spreading symmetrically. With $\phi(x) = x^2$ and $\mu = 0$, the tangent line is flat, so it predicts zero variance, which is badly wrong for any $\sigma$. These are the same errors an EKF makes at every step.

    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    Pushing a Gaussian through a nonlinear function shifts its mean (by about $\tfrac12\phi''(\mu)\sigma^2$), changes its spread, and bends its shape. The tangent line keeps the Gaussian shape and misses the shift. Its error is small when $\sigma$ is small compared with the distance over which $\phi'$ changes appreciably.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Linearization

    The tangent line generalizes to functions of several variables. Let $\phi: \mathbb R^n \to \mathbb R^m$ have components $\phi_1, \ldots, \phi_m$ whose first partial derivatives exist at a point $\mathbf a$. The {term}`Jacobian` of $\phi$ at $\mathbf a$ ([Appendix C: Functions of Several Variables](appendix_c_calculus.md)) is the $m \times n$ matrix

    $$\mathbf J_\phi(\mathbf a) := \begin{bmatrix} \dfrac{\partial\phi_1}{\partial x_1}(\mathbf a) & \cdots & \dfrac{\partial\phi_1}{\partial x_n}(\mathbf a) \\ \vdots & & \vdots \\ \dfrac{\partial\phi_m}{\partial x_1}(\mathbf a) & \cdots & \dfrac{\partial\phi_m}{\partial x_n}(\mathbf a)\end{bmatrix}.$$

    Row $i$ is the {term}`gradient` of $\phi_i$; column $j$ says how every output responds to a small change in $x_j$ alone.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Linearization**</u>

    The linearization of a function $\phi: \mathbb R^n \to \mathbb R^m$ at a point $\mathbf a \in \mathbb R^n$ where all first {term}`partial derivatives <partial derivative>` of $\phi$ exist is the affine function
    $$\mathbf x \mapsto \phi(\mathbf a) + \mathbf J_\phi(\mathbf a)(\mathbf x - \mathbf a),$$
    where $\mathbf J_\phi(\mathbf a)$ is the {term}`Jacobian` of $\phi$ at $\mathbf a$. To *linearize* $\phi$ at $\mathbf a$ is to replace $\phi$ by this function.
    ///

    For $n = m = 1$ the linearization is the tangent line of the previous section. The next theorem says in what sense it approximates $\phi$.

    /// important | 📐 **Theorem (First-Order Taylor Approximation)**
        attrs: {class: no-icon}
    Let $U \subseteq \mathbb R^n$ be open, $\mathbf a \in U$, and let $\phi: U \to \mathbb R^m$ have continuous first partial derivatives on $U$. Then
    $$\lim_{\mathbf x \to \mathbf a}\frac{\big\|\phi(\mathbf x) - \phi(\mathbf a) - \mathbf J_\phi(\mathbf a)(\mathbf x - \mathbf a)\big\|}{\|\mathbf x - \mathbf a\|} = 0.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Not given here; see [Appendix C: Functions of Several Variables](appendix_c_calculus.md). $\blacksquare$
    ///

    In words: the error of the linearization shrinks faster than the distance to $\mathbf a$. The theorem says nothing about points far from $\mathbf a$, which is exactly where the EKF gets into trouble. One special case is exact everywhere.

    /// important | 📐 **Lemma (Linearizing an Affine Function)**
        attrs: {class: no-icon}
    If $\phi(\mathbf x) = \mathbf A\mathbf x + \mathbf b$, then $\mathbf J_\phi(\mathbf a) = \mathbf A$ for every $\mathbf a$, so the linearization of $\phi$ at any point is $\phi$ itself.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    The $i$-th component is $\phi_i(\mathbf x) = \sum_{j=1}^n A_{ij}x_j + b_i$, so $\partial\phi_i/\partial x_j = A_{ij}$ at every point. Hence $\phi(\mathbf a) + \mathbf A(\mathbf x - \mathbf a) = \mathbf A\mathbf a + \mathbf b + \mathbf A\mathbf x - \mathbf A\mathbf a = \phi(\mathbf x)$. $\blacksquare$
    ///

    For a process function $f(\mathbf x, \mathbf u)$ we linearize in $\mathbf x$ only, with $\mathbf u$ held fixed, and write $\partial f/\partial\mathbf x\,(\mathbf a, \mathbf u)$ for the Jacobian of $\mathbf x \mapsto f(\mathbf x, \mathbf u)$ at $\mathbf a$. The EKF linearizes at the best available guess of the state, the current estimate:

    $$\mathbf F_k := \frac{\partial f}{\partial \mathbf x}\big(\hat{\mathbf x}_{k-1}, \mathbf u_k\big), \qquad \mathbf H_k := \mathbf J_h\big(\hat{\mathbf x}_k^-\big).$$

    For example, the pendulum's measurement function $h(\theta, \omega) = L\sin\theta$ has $\mathbf J_h = [\,L\cos\theta,\ 0\,]$. At $\theta = \pi/2$ (rod horizontal) this is the zero matrix: there, a small change in angle does not change the measurement to first order. We will meet this point again.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Extended Kalman Filter

    ### Assumptions

    We keep Chapter 13's assumptions (A2)–(A5), with (A1) now saying that $f$, $h$, $\mathbf Q$, $\mathbf R$, and the inputs $\mathbf u_k$ are known, and add two more:

    - **(E1) Independent noise.** $\mathbf x_0, \mathbf w_1, \mathbf w_2, \ldots, \mathbf v_1, \mathbf v_2, \ldots$ are independent.
    - **(E2) Smoothness.** For each $\mathbf u$, the functions $\mathbf x \mapsto f(\mathbf x, \mathbf u)$ and $h$ have continuous first partial derivatives.

    Chapter 13 needed only *uncorrelated* noise because the Kalman filter's errors are fixed linear combinations of past noise. The EKF's estimates depend on past noise *nonlinearly*, and only independence guarantees that a new noise vector is uncorrelated with every function of the past. (E2) makes the Jacobians exist and lets the First-Order Taylor theorem apply.

    ### Predict

    Suppose that, given the measurements $\mathbf z_1, \ldots, \mathbf z_{k-1}$, the state $\mathbf x_{k-1}$ has mean $\hat{\mathbf x}_{k-1}$ and covariance $\mathbf P_{k-1}$. (For $k = 1$ these are $\hat{\mathbf x}_0$ and $\mathbf P_0$.) Given those measurements, $\hat{\mathbf x}_{k-1}$ and $\mathbf F_k$ are fixed numbers. By the definition of the linearization,

    $$f(\mathbf x_{k-1}, \mathbf u_k) = f(\hat{\mathbf x}_{k-1}, \mathbf u_k) + \mathbf F_k(\mathbf x_{k-1} - \hat{\mathbf x}_{k-1}) + \mathbf r_k,$$

    where the remainder $\mathbf r_k$ is small compared with $\|\mathbf x_{k-1} - \hat{\mathbf x}_{k-1}\|$ when that distance is small (First-Order Taylor theorem). **The EKF's first approximation is to drop $\mathbf r_k$**:

    $$\mathbf x_k \approx f(\hat{\mathbf x}_{k-1}, \mathbf u_k) + \mathbf F_k(\mathbf x_{k-1} - \hat{\mathbf x}_{k-1}) + \mathbf w_k.$$

    The right-hand side is a constant plus $\mathbf F_k$ times $\mathbf x_{k-1}$ plus $\mathbf w_k$. By (E1), $\mathbf w_k$ is independent of $\mathbf x_{k-1}$ and of $\mathbf z_1, \ldots, \mathbf z_{k-1}$ (all of which are functions of $\mathbf x_0, \mathbf w_1, \ldots, \mathbf w_{k-1}, \mathbf v_1, \ldots, \mathbf v_{k-1}$), so given the measurements it still has mean $\mathbf 0$ and covariance $\mathbf Q$ and is uncorrelated with $\mathbf x_{k-1}$. Linearity of expectation and Chapter 13's Covariance Rules then give the mean and covariance of the right-hand side:

    $$\hat{\mathbf x}_k^- := f(\hat{\mathbf x}_{k-1}, \mathbf u_k), \qquad \mathbf P_k^- := \mathbf F_k\mathbf P_{k-1}\mathbf F_k^\top + \mathbf Q.$$

    The mean is moved through $f$ itself and the covariance through its Jacobian. The two agree at $\hat{\mathbf x}_{k-1}$, which is the only point the approximation uses.

    ### Update

    Expand $h$ about the prediction: $h(\mathbf x_k) = h(\hat{\mathbf x}_k^-) + \mathbf H_k(\mathbf x_k - \hat{\mathbf x}_k^-) + \mathbf s_k$. **The second approximation drops the remainder $\mathbf s_k$.** Moving the known terms to the left,

    $$\mathbf z_k' := \mathbf z_k - h(\hat{\mathbf x}_k^-) + \mathbf H_k\hat{\mathbf x}_k^- \approx \mathbf H_k\mathbf x_k + \mathbf v_k.$$

    The vector $\mathbf z_k'$ is known once $\mathbf z_k$ arrives, and the right-hand side is exactly Chapter 13's linear measurement model with measurement matrix $\mathbf H_k$. Chapter 13's optimal update for that model gives

    $$\mathbf S_k = \mathbf H_k\mathbf P_k^-\mathbf H_k^\top + \mathbf R, \qquad \mathbf K_k = \mathbf P_k^-\mathbf H_k^\top\mathbf S_k^{-1},$$

    $$\hat{\mathbf x}_k = \hat{\mathbf x}_k^- + \mathbf K_k\big(\mathbf z_k' - \mathbf H_k\hat{\mathbf x}_k^-\big) = \hat{\mathbf x}_k^- + \mathbf K_k\big(\mathbf z_k - h(\hat{\mathbf x}_k^-)\big), \qquad \mathbf P_k = (\mathbf I - \mathbf K_k\mathbf H_k)\mathbf P_k^-.$$

    So the {term}`innovation` is $\tilde{\mathbf y}_k := \mathbf z_k - h(\hat{\mathbf x}_k^-)$, the measurement minus the measurement predicted by the nonlinear $h$. The Jacobian enters only through the gain and the covariances.

    If both remainders $\mathbf r_k$ and $\mathbf s_k$ were zero and the noise were Gaussian, Chapter 13's Gaussian-conditioning theorem would make $\hat{\mathbf x}_k$ and $\mathbf P_k$ the exact conditional mean and covariance. The remainders are not zero, so the EKF's $\hat{\mathbf x}_k$ and $\mathbf P_k$ are approximations and the EKF has no optimality guarantee. In particular, $\mathbf P_k$ is the covariance the filter *believes*; whether its actual errors have that covariance is what Chapter 14's NEES test checks.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The EKF contains the Kalman filter as a special case.

    /// important | 📐 **Lemma (The EKF Generalizes the Kalman Filter)**
        attrs: {class: no-icon}
    If $f(\mathbf x, \mathbf u) = \mathbf F\mathbf x + \mathbf B\mathbf u$ and $h(\mathbf x) = \mathbf H\mathbf x$, then the EKF's equations are exactly the Kalman filter's equations of [Chapter 13](ch13_kalman_filter.md).
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    By the Lemma on linearizing an affine function, $\mathbf F_k = \mathbf F$ and $\mathbf H_k = \mathbf H$ for every $k$. Moreover $f(\hat{\mathbf x}_{k-1}, \mathbf u_k) = \mathbf F\hat{\mathbf x}_{k-1} + \mathbf B\mathbf u_k$ and $h(\hat{\mathbf x}_k^-) = \mathbf H\hat{\mathbf x}_k^-$. Substituting these into the EKF's equations gives Chapter 13's equations term by term. $\blacksquare$
    ///

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Extended Kalman filter**</u>

    For a {term}`state-space model` $\mathbf x_k = f(\mathbf x_{k-1}, \mathbf u_k) + \mathbf w_k$, $\mathbf z_k = h(\mathbf x_k) + \mathbf v_k$ with noise covariances $\mathbf Q$ and $\mathbf R$, the {term}`filter` that starts from an initial estimate $\hat{\mathbf x}_0$ and covariance $\mathbf P_0$ and, for each $k \ge 1$, computes
    $$\hat{\mathbf x}_k^- = f(\hat{\mathbf x}_{k-1}, \mathbf u_k), \qquad \mathbf P_k^- = \mathbf F_k\mathbf P_{k-1}\mathbf F_k^\top + \mathbf Q,$$
    $$\mathbf S_k = \mathbf H_k\mathbf P_k^-\mathbf H_k^\top + \mathbf R, \qquad \mathbf K_k = \mathbf P_k^-\mathbf H_k^\top\mathbf S_k^{-1},$$
    $$\hat{\mathbf x}_k = \hat{\mathbf x}_k^- + \mathbf K_k\big(\mathbf z_k - h(\hat{\mathbf x}_k^-)\big), \qquad \mathbf P_k = (\mathbf I - \mathbf K_k\mathbf H_k)\mathbf P_k^-,$$
    where $\mathbf F_k$ is the {term}`Jacobian` of $\mathbf x \mapsto f(\mathbf x, \mathbf u_k)$ at $\hat{\mathbf x}_{k-1}$ and $\mathbf H_k$ is the Jacobian of $h$ at $\hat{\mathbf x}_k^-$. Computing $\mathbf P_k$ with the {term}`Joseph form` instead gives the same matrix in exact arithmetic.
    ///

    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    The EKF is the Kalman filter with three substitutions:

    | | Kalman filter | Extended Kalman filter |
    |---|---|---|
    | prediction | $\mathbf F\hat{\mathbf x}_{k-1} + \mathbf B\mathbf u_k$ | $f(\hat{\mathbf x}_{k-1}, \mathbf u_k)$ |
    | predicted measurement | $\mathbf H\hat{\mathbf x}_k^-$ | $h(\hat{\mathbf x}_k^-)$ |
    | matrices in $\mathbf P_k^-$, $\mathbf S_k$, $\mathbf K_k$, $\mathbf P_k$ | $\mathbf F$, $\mathbf H$ | Jacobians $\mathbf F_k$, $\mathbf H_k$ at the current estimate |
    ///

    /// caution | ⚠️ **Assumptions and Failure Modes**
        attrs: {class: no-icon}
    - **Dropped remainders are not small.** When the uncertainty is large compared with the region over which $f$ or $h$ looks linear, the predicted mean is biased (as in the Gaussian explorer above) and $\mathbf P_k$ is typically too small. The filter becomes overconfident and can diverge.
    - **The linearization point is far from the truth.** The Jacobians then describe the wrong part of the function, and the update can push the estimate the wrong way. A large initial error is the usual cause.
    - **(E2) fails.** If $f$ or $h$ is not differentiable at the estimate (a saturation, an absolute value, or an angle that wraps from $\pi$ to $-\pi$), the Jacobian is undefined or meaningless there. Reparametrize the state, or use a derivative-free filter ([Chapter 16](ch16_unscented_kalman_filter.md)).
    - **Non-additive noise.** If the model is $\mathbf x_k = f(\mathbf x_{k-1}, \mathbf u_k, \mathbf w_k)$, linearize in $\mathbf w$ as well: $\mathbf P_k^- = \mathbf F_k\mathbf P_{k-1}\mathbf F_k^\top + \mathbf L_k\mathbf Q\mathbf L_k^\top$ with $\mathbf L_k := \partial f/\partial\mathbf w$ at $(\hat{\mathbf x}_{k-1}, \mathbf u_k, \mathbf 0)$, and similarly for $\mathbf v$ in $h$.
    - **(E1) fails.** Correlated noise has the same effects as in Chapter 13: overconfidence, and gains that are no longer appropriate.
    - **Wrong Jacobians.** A coding or derivation error in $\mathbf F_k$ or $\mathbf H_k$ does not stop the filter from running; it silently makes the covariance wrong. Always check Jacobians numerically, as below.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Example: Tracking a Pendulum

    ### The Model

    Treat the bob as a point mass $m$ on a rigid, massless rod. The bob moves on a circle of radius $L$, so its displacement along the circle from the bottom is $L\theta$ and its acceleration along the circle is $L\ddot\theta$. Two forces act along the circle:

    - the component of gravity along the circle, $-mg\sin\theta$, which always pulls toward the bottom;
    - a damping force $-mLc\,\dot\theta$, which models pivot friction and air drag as proportional to the bob's speed $L\dot\theta$, with damping rate $c > 0$.

    Newton's second law along the circle, $mL\ddot\theta = -mg\sin\theta - mLc\,\dot\theta$, gives

    $$\ddot\theta = -\frac gL\sin\theta - c\,\dot\theta, \qquad L = 1\ \text{m},\quad g = 9.81\ \text{m/s}^2,\quad c = 0.1\ \text{s}^{-1}.$$

    For small angles, $\sin\theta \approx \theta$ makes this linear, but at $\theta = 1$ rad, $\sin\theta \approx 0.84$: a 16% error. With the state $\mathbf x = [\theta, \omega]^\top$, the model is the {term}`differential equation`

    $$\dot{\mathbf x} = a(\mathbf x) := \begin{bmatrix}\omega \\ -\tfrac gL\sin\theta - c\,\omega\end{bmatrix}.$$

    Unlike the linear equations of [Chapter 10](ch10_process_models.md), this equation has no known closed-form solution, so we {term}`discretize <discretization>` it numerically. The classical fourth-order Runge–Kutta method (RK4) advances the state by one time step $\Delta t$ using four evaluations of $a$:

    $$\mathbf k_1 = a(\mathbf x),\quad \mathbf k_2 = a\big(\mathbf x + \tfrac{\Delta t}2\mathbf k_1\big),\quad \mathbf k_3 = a\big(\mathbf x + \tfrac{\Delta t}2\mathbf k_2\big),\quad \mathbf k_4 = a\big(\mathbf x + \Delta t\,\mathbf k_3\big),$$

    $$f(\mathbf x) := \mathbf x + \frac{\Delta t}6\big(\mathbf k_1 + 2\mathbf k_2 + 2\mathbf k_3 + \mathbf k_4\big).$$

    For smooth $a$, the error of RK4 after a fixed time is at most a constant times $\Delta t^4$, compared with $\Delta t$ for Euler's method $\mathbf x + \Delta t\,a(\mathbf x)$ ([Wikipedia: Runge–Kutta methods](https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods)). We use $\Delta t = 0.01$ s.
    """)
    return


@app.cell(hide_code=True)
def _(mo, rk4_accuracy, sci):
    mo.md(rf"""
    At this step size, a 10 s RK4 trajectory starting from $\mathbf x = [1, 0]^\top$ differs from one computed with $\Delta t = 0.001$ s by at most ${sci(rk4_accuracy['rk4_diff'])}$ rad, so we treat the RK4 step as exact. Euler's method is not good enough here: after 10 s its swing amplitude is {rk4_accuracy['amp_euler']:.2f} rad instead of {rk4_accuracy['amp_rk4']:.2f} rad, because at this step size it adds energy at nearly the rate the damping removes it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Process noise.** A real pendulum is nudged by things the model ignores, such as air currents and an uneven pivot. We model these as continuous white angular-acceleration noise of intensity $q = 0.01\ \text{rad}^2/\text{s}^3$ added to $\ddot\theta$. Chapter 14's continuous white-noise acceleration model then gives

    $$\mathbf Q = q\begin{bmatrix}\Delta t^3/3 & \Delta t^2/2 \\ \Delta t^2/2 & \Delta t\end{bmatrix}.$$

    That formula is exact when $\ddot\theta$ is pure noise; for the pendulum it is the leading term for small $\Delta t$, which is accurate enough at $\Delta t = 0.01$ s. The process model is $\mathbf x_k = f(\mathbf x_{k-1}) + \mathbf w_k$ with $\mathbf w_k \sim \mathcal N(\mathbf 0, \mathbf Q)$; there is no control input.

    **Measurements.** Every fifth step (20 Hz), the camera reports the bob's horizontal position,

    $$z_k = h(\mathbf x_k) + v_k, \qquad h(\mathbf x) := L\sin\theta, \qquad v_k \sim \mathcal N(0, \sigma_z^2), \quad \sigma_z = 0.05\ \text{m},$$

    so $\mathbf R = [\sigma_z^2]$ is $1 \times 1$. On the other four steps the filter only predicts, as in the multi-rate filters of [Chapter 14](ch14_kalman_filters_in_practice.md).

    **Truth.** The simulated pendulum starts at rest at $\theta_0 = 1$ rad (57°), so $\mathbf x_0 = [1, 0]^\top$, and follows exactly this model, with noise drawn from the stated distributions. The filter's model is therefore correct, and every error below comes from the filter's approximations rather than from model mismatch.

    ### The Jacobians

    Differentiating $a$ entry by entry gives its Jacobian, and $h$'s Jacobian was computed above:

    $$\mathbf A(\mathbf x) := \mathbf J_a(\mathbf x) = \begin{bmatrix}0 & 1 \\ -\tfrac gL\cos\theta & -c\end{bmatrix}, \qquad \mathbf J_h(\mathbf x) = \begin{bmatrix}L\cos\theta & 0\end{bmatrix}.$$

    The process Jacobian $\mathbf J_f$ needs the chain rule, because $f$ composes $a$ with itself four times.

    /// important | 📐 **Lemma (Jacobian of an RK4 Step)**
        attrs: {class: no-icon}
    Let $a: \mathbb R^n \to \mathbb R^n$ have continuous first partial derivatives and Jacobian $\mathbf A(\mathbf x)$, and let $f$ be the RK4 step above. Then $f$ has continuous first partial derivatives and
    $$\mathbf J_f(\mathbf x) = \mathbf I + \frac{\Delta t}6\big(\mathbf K_1 + 2\mathbf K_2 + 2\mathbf K_3 + \mathbf K_4\big),$$
    where
    $$\mathbf K_1 = \mathbf A(\mathbf x), \quad \mathbf K_2 = \mathbf A\big(\mathbf x + \tfrac{\Delta t}2\mathbf k_1\big)\big(\mathbf I + \tfrac{\Delta t}2\mathbf K_1\big), \quad \mathbf K_3 = \mathbf A\big(\mathbf x + \tfrac{\Delta t}2\mathbf k_2\big)\big(\mathbf I + \tfrac{\Delta t}2\mathbf K_2\big), \quad \mathbf K_4 = \mathbf A\big(\mathbf x + \Delta t\,\mathbf k_3\big)\big(\mathbf I + \Delta t\,\mathbf K_3\big).$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    We show that $\mathbf K_i$ is the Jacobian of the stage $\mathbf k_i$, viewed as a function of $\mathbf x$. For $\mathbf k_1 = a(\mathbf x)$ this is the definition of $\mathbf A$. Next, $\mathbf k_2 = a(\mathbf g_2(\mathbf x))$ with $\mathbf g_2(\mathbf x) := \mathbf x + \tfrac{\Delta t}2\mathbf k_1(\mathbf x)$. A partial derivative of a sum is the sum of the partial derivatives, a constant factor comes out, and the Jacobian of $\mathbf x \mapsto \mathbf x$ is $\mathbf I$, so $\mathbf J_{\mathbf g_2} = \mathbf I + \tfrac{\Delta t}2\mathbf K_1$. The chain rule ([Appendix C: Functions of Several Variables](appendix_c_calculus.md)) gives $\mathbf J_{\mathbf k_2}(\mathbf x) = \mathbf A(\mathbf g_2(\mathbf x))\,\mathbf J_{\mathbf g_2}(\mathbf x) = \mathbf K_2$. The same argument with $\mathbf g_3(\mathbf x) := \mathbf x + \tfrac{\Delta t}2\mathbf k_2(\mathbf x)$ and $\mathbf g_4(\mathbf x) := \mathbf x + \Delta t\,\mathbf k_3(\mathbf x)$ gives $\mathbf K_3$ and $\mathbf K_4$. Finally, $f = \mathbf x + \tfrac{\Delta t}6(\mathbf k_1 + 2\mathbf k_2 + 2\mathbf k_3 + \mathbf k_4)$ gives the formula by the same sum and constant-factor rules. Each $\mathbf K_i$ is built from continuous functions by sums, products, and composition, so it is continuous. $\blacksquare$
    ///

    Multiplying out the products shows $\mathbf J_f(\mathbf x) = \mathbf I + \Delta t\,\mathbf A(\mathbf x) + (\text{terms in } \Delta t^2, \Delta t^3, \Delta t^4)$. To first order in $\Delta t$ it is the Jacobian of Euler's step, and many texts use $\mathbf I + \Delta t\,\mathbf A$ as $\mathbf F_k$. We use the exact Jacobian of the step we actually take, so that the covariance prediction matches the state prediction and the numerical check below can verify it to rounding error. For the EKF,

    $$\mathbf F_k = \mathbf J_f(\hat{\mathbf x}_{k-1}), \qquad \mathbf H_k = \begin{bmatrix}L\cos\hat\theta_k^- & 0\end{bmatrix}.$$

    ### Implementation

    The model functions accept either one state of shape `(2,)` or a batch of states of shape `(2, N)`, which the next chapter uses to move many points through $f$ at once.
    """)
    return


@app.cell
def pendulum_model(np):
    # jb: echo=true
    PEND_L = 1.0    # rod length L (m)
    GRAV = 9.81     # gravitational acceleration g (m/s^2)
    DAMP_C = 0.1    # damping rate c (1/s)
    DT = 0.01       # time step (s)


    def pendulum_rhs(x):
        """a(x): time derivative of the state x = [theta, omega]."""
        theta, omega = x[0], x[1]
        return np.array([omega, -(GRAV / PEND_L) * np.sin(theta) - DAMP_C * omega])


    def pendulum_rhs_jacobian(x):
        """A(x): Jacobian of a at a single state x."""
        return np.array([[0.0, 1.0],
                         [-(GRAV / PEND_L) * np.cos(x[0]), -DAMP_C]])


    def f_pendulum(x):
        """f(x): one RK4 step of length DT."""
        k1 = pendulum_rhs(x)
        k2 = pendulum_rhs(x + 0.5 * DT * k1)
        k3 = pendulum_rhs(x + 0.5 * DT * k2)
        k4 = pendulum_rhs(x + DT * k3)
        return x + DT / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


    def F_pendulum(x):
        """Jacobian of the RK4 step at x, by the chain rule through its stages."""
        I = np.eye(2)
        k1 = pendulum_rhs(x)
        k2 = pendulum_rhs(x + 0.5 * DT * k1)
        k3 = pendulum_rhs(x + 0.5 * DT * k2)
        K1 = pendulum_rhs_jacobian(x)
        K2 = pendulum_rhs_jacobian(x + 0.5 * DT * k1) @ (I + 0.5 * DT * K1)
        K3 = pendulum_rhs_jacobian(x + 0.5 * DT * k2) @ (I + 0.5 * DT * K2)
        K4 = pendulum_rhs_jacobian(x + DT * k3) @ (I + DT * K3)
        return I + DT / 6 * (K1 + 2 * K2 + 2 * K3 + K4)


    def h_pendulum(x):
        """h(x): horizontal position of the bob (m), as a 1-vector."""
        return np.array([PEND_L * np.sin(x[0])])


    def H_pendulum(x):
        """Jacobian of h at a single state x."""
        return np.array([[PEND_L * np.cos(x[0]), 0.0]])

    return (
        DT,
        F_pendulum,
        H_pendulum,
        PEND_L,
        f_pendulum,
        h_pendulum,
        pendulum_rhs,
        pendulum_rhs_jacobian,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The EKF itself is two short functions that take the model as arguments, plus a loop that runs them. Following Chapter 13, the gain is computed by solving a linear system rather than inverting $\mathbf S_k$, and $\mathbf P_k$ uses the Joseph form. A missing measurement is marked by `NaN`, and on those steps the loop only predicts.
    """)
    return


@app.cell
def ekf_impl(F_pendulum, H_pendulum, f_pendulum, h_pendulum, np):
    # jb: echo=true
    def ekf_predict(x, P, f, F_jac, Q):
        """Predict: x^- = f(x),  P^- = F P F^T + Q with F the Jacobian at x."""
        F = F_jac(x)
        return f(x), F @ P @ F.T + Q


    def ekf_update(x_pred, P_pred, z, h, H_jac, R):
        """Update with H the Jacobian at the prediction; Joseph-form covariance."""
        H = H_jac(x_pred)
        y = z - h(x_pred)                         # innovation
        S = H @ P_pred @ H.T + R                  # innovation covariance
        K = np.linalg.solve(S, H @ P_pred).T      # K = P^- H^T S^-1
        I_KH = np.eye(len(x_pred)) - K @ H
        P = I_KH @ P_pred @ I_KH.T + K @ R @ K.T  # Joseph form
        return x_pred + K @ y, P


    def run_ekf(zs, x0_hat, P0, Q, R, F_jac=F_pendulum, H_jac=H_pendulum):
        """Run the EKF on the pendulum. zs[k] is the measurement at step k, or NaN.

        Returns the estimates (shape (len(zs), 2)) and covariances (len(zs), 2, 2);
        row 0 holds the initial estimate and covariance.
        """
        x, P = np.asarray(x0_hat, float), np.asarray(P0, float)
        xs_hat, Ps = [x], [P]
        for k in range(1, len(zs)):
            x, P = ekf_predict(x, P, f_pendulum, F_jac, Q)
            if not np.isnan(zs[k]):
                x, P = ekf_update(x, P, np.array([zs[k]]), h_pendulum, H_jac, R)
            xs_hat.append(x)
            Ps.append(P)
        return np.array(xs_hat), np.array(Ps)

    return (run_ekf,)


@app.cell
def simulation(DT, PEND_L, f_pendulum, np, pendulum_rhs):
    # jb: include=false
    Q_INTENSITY = 0.01                      # q (rad^2/s^3)
    Q_PEND = Q_INTENSITY * np.array([[DT**3 / 3, DT**2 / 2], [DT**2 / 2, DT]])
    SIGMA_Z = 0.05                          # measurement noise std (m)
    R_PEND = np.array([[SIGMA_Z**2]])
    MEAS_EVERY = 5                          # 20 Hz measurements at 100 Hz steps
    N_STEPS = 1000                          # 10 s
    X0_TRUE = np.array([1.0, 0.0])
    TIMES = DT * np.arange(N_STEPS + 1)

    def simulate_truth(x0, n_steps, rng, n_runs=None):
        """Truth x_k = f(x_{k-1}) + w_k. With n_runs, simulate that many runs at
        once; the result then has shape (n_steps + 1, 2, n_runs)."""
        _chol = np.linalg.cholesky(Q_PEND)
        _shape = (2,) if n_runs is None else (2, n_runs)
        _x = np.array(x0, float) if n_runs is None else np.repeat(np.asarray(x0, float)[:, None], n_runs, axis=1)
        _out = [_x]
        for _ in range(n_steps):
            _x = f_pendulum(_x) + _chol @ rng.standard_normal(_shape)
            _out.append(_x)
        return np.array(_out)

    def measure(xs, sigma_z, unit_noise):
        """Measurements at every MEAS_EVERY-th step, NaN elsewhere."""
        _zs = np.full(len(xs), np.nan)
        _idx = np.arange(MEAS_EVERY, len(xs), MEAS_EVERY)
        _zs[_idx] = PEND_L * np.sin(xs[_idx, 0]) + sigma_z * unit_noise[: _idx.size]
        return _zs

    def nees_series(xs, xs_hat, Ps):
        """NEES e^T P^-1 e at every step."""
        _e = xs_hat - xs
        return np.einsum("ki,kij,kj->k", _e, np.linalg.inv(Ps), _e)

    _rng = np.random.default_rng(3)
    truth = simulate_truth(X0_TRUE, N_STEPS, _rng)
    unit_meas_noise = _rng.standard_normal(N_STEPS // MEAS_EVERY)
    zs_main = measure(truth, SIGMA_Z, unit_meas_noise)

    # Accuracy of the RK4 step (quoted in the text).
    def _integrate(step, dt, n):
        _x, _thetas = np.array([1.0, 0.0]), []
        for _ in range(n):
            _x = step(_x, dt)
            _thetas.append(_x[0])
        return _x, np.array(_thetas)

    def _rk4(x, dt):
        _k1 = pendulum_rhs(x)
        _k2 = pendulum_rhs(x + 0.5 * dt * _k1)
        _k3 = pendulum_rhs(x + 0.5 * dt * _k2)
        _k4 = pendulum_rhs(x + dt * _k3)
        return x + dt / 6 * (_k1 + 2 * _k2 + 2 * _k3 + _k4)

    _x_coarse, _th_coarse = _integrate(_rk4, 0.01, 1000)
    _x_fine, _ = _integrate(_rk4, 0.001, 10000)
    _, _th_euler = _integrate(lambda x, dt: x + dt * pendulum_rhs(x), 0.01, 1000)
    rk4_accuracy = {
        "rk4_diff": np.abs(_x_coarse - _x_fine).max(),
        "amp_rk4": np.abs(_th_coarse[-250:]).max(),
        "amp_euler": np.abs(_th_euler[-250:]).max(),
    }
    return (
        MEAS_EVERY,
        N_STEPS,
        Q_PEND,
        R_PEND,
        SIGMA_Z,
        TIMES,
        X0_TRUE,
        measure,
        nees_series,
        rk4_accuracy,
        simulate_truth,
        truth,
        unit_meas_noise,
        zs_main,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Checking the Jacobians Numerically

    A wrong Jacobian does not crash an EKF; it quietly makes the covariance wrong. So before trusting a filter, compare every analytic Jacobian with a finite-difference approximation. The central difference

    $$\frac{\phi(\mathbf a + \varepsilon\mathbf e_j) - \phi(\mathbf a - \varepsilon\mathbf e_j)}{2\varepsilon},$$

    where $\mathbf e_j$ is the $j$-th standard basis vector, approximates column $j$ of $\mathbf J_\phi(\mathbf a)$. For smooth $\phi$, Taylor's theorem shows its error is proportional to $\varepsilon^2$. Floating-point arithmetic adds a rounding error of roughly $u\,\|\phi(\mathbf a)\|/\varepsilon$, where $u \approx 1.1 \times 10^{-16}$ is the unit roundoff of double precision ([Wikipedia: Machine epsilon](https://en.wikipedia.org/wiki/Machine_epsilon)). With $\varepsilon = 10^{-6}$ both are below about $10^{-9}$ for the pendulum, so a correct Jacobian agrees to about nine decimal places and a wrong one stands out.
    """)
    return


@app.cell
def jacobian_check(F_pendulum, H_pendulum, f_pendulum, h_pendulum, np):
    # jb: echo=true
    def numerical_jacobian(fun, x, eps=1e-6):
        """Central-difference approximation of the Jacobian of fun at x."""
        x = np.asarray(x, dtype=float)
        columns = []
        for j in range(x.size):
            step = np.zeros_like(x)
            step[j] = eps
            columns.append((fun(x + step) - fun(x - step)) / (2 * eps))
        return np.column_stack(columns)


    def max_jacobian_error(fun, jac, states):
        """Largest entrywise |analytic - numerical| over the given states."""
        return max(np.abs(jac(s) - numerical_jacobian(fun, s)).max() for s in states)


    _rng = np.random.default_rng(15)
    test_states = np.column_stack([_rng.uniform(-np.pi, np.pi, 200),   # theta (rad)
                                   _rng.uniform(-6.0, 6.0, 200)])     # omega (rad/s)
    jacobian_errors = {
        "F": max_jacobian_error(f_pendulum, F_pendulum, test_states),
        "H": max_jacobian_error(h_pendulum, H_pendulum, test_states),
    }
    return jacobian_errors, max_jacobian_error, test_states


@app.cell(hide_code=True)
def _(jacobian_errors, mo, sci):
    mo.md(rf"""
    Over 200 random states with $\theta \in [-\pi, \pi]$ and $\omega \in [-6, 6]$ rad/s, the largest entrywise difference is ${sci(jacobian_errors['F'])}$ for $\mathbf J_f$ and ${sci(jacobian_errors['H'])}$ for $\mathbf J_h$: rounding error, so both derivations are correct.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Results

    We start the filter at $\hat{\mathbf x}_0 = [0.5, 0.5]^\top$, an error of $0.5$ in each component, with $\mathbf P_0 = \operatorname{diag}(0.5^2, 0.5^2)$, so the initial error is one standard deviation in each component.
    """)
    return


@app.cell
def main_run(Q_PEND, R_PEND, np, run_ekf, zs_main):
    # jb: include=false
    X0_HAT_MAIN = np.array([0.5, 0.5])
    P0_MAIN = np.diag([0.5**2, 0.5**2])
    xs_hat_main, Ps_main = run_ekf(zs_main, X0_HAT_MAIN, P0_MAIN, Q_PEND, R_PEND)
    return Ps_main, xs_hat_main


@app.cell
def make_results_fig(
    IMAGES_DIR,
    PEND_L,
    Ps_main,
    TIMES,
    np,
    plt,
    truth,
    xs_hat_main,
    zs_main,
):
    # jb: include=false
    _fig, _axes = plt.subplots(3, 1, figsize=(9, 8), sharex=True)
    _meas = ~np.isnan(zs_main)
    _axes[0].plot(TIMES[_meas], zs_main[_meas], "o", mfc="none", mec="k", ms=4, label="measurement $z_k$")
    _axes[0].plot(TIMES, PEND_L * np.sin(truth[:, 0]), "k-", linewidth=1, label=r"truth $L\sin\theta$")
    _axes[0].set_ylabel("horizontal position (m)")
    for _i, (_ax, _label, _unit) in enumerate(zip(_axes[1:], [r"\theta", r"\omega"], ["rad", "rad/s"])):
        _sd = np.sqrt(Ps_main[:, _i, _i])
        _ax.fill_between(TIMES, xs_hat_main[:, _i] - 2 * _sd, xs_hat_main[:, _i] + 2 * _sd,
                         color="C1", alpha=0.2, label=r"$\pm 2\sigma$")
        _ax.plot(TIMES, truth[:, _i], "k-", linewidth=1, label="truth")
        _ax.plot(TIMES, xs_hat_main[:, _i], "C1-", linewidth=1.2, label="EKF estimate")
        _ax.set_ylabel(rf"${_label}$ ({_unit})")
    _axes[2].set_xlabel("time (s)")
    for _ax in _axes:
        _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
        _ax.legend(loc="upper right", fontsize=8, ncol=3)
    _axes[0].set_title("EKF tracking a pendulum from horizontal-position measurements", style="italic")
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch15_ekf_pendulum.svg")
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch15_ekf_pendulum.svg" class="graphic" alt="Three stacked plots over 10 seconds: noisy horizontal-position measurements around the true sinusoid-like curve; the EKF's angle estimate converging onto the true angle within half a second with a narrow two-sigma band; and the angular-velocity estimate doing the same." />
    """)
    return


@app.cell(hide_code=True)
def _(Ps_main, TIMES, mo, np, truth, xs_hat_main):
    _after = TIMES >= 1.0
    _err = np.abs(xs_hat_main - truth)[_after]
    _sd = np.sqrt(np.stack([Ps_main[:, 0, 0], Ps_main[:, 1, 1]], axis=1))[_after]
    _inside = np.mean(_err <= 2 * _sd, axis=0)
    _rmse = np.sqrt(np.mean(_err**2, axis=0))
    mo.md(rf"""
    The angle estimate locks on within about half a second. After the first second, its root-mean-square error is {_rmse[0]:.3f} rad for $\theta$ and {_rmse[1]:.3f} rad/s for $\omega$, and the truth lies inside the $\pm 2\sigma$ band at {100 * _inside[0]:.0f}% of the steps for $\theta$ and {100 * _inside[1]:.0f}% for $\omega$, close to the 95% a consistent filter should give. The angular velocity is never measured: the filter infers it from how the measured position changes, through the dynamics.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### What the Linearized Covariance Misses

    The EKF's covariance prediction is exactly the linearized propagation of the Gaussian explorer, applied at every step. The figure below shows its effect over many steps. It starts from 3000 states drawn from $\mathcal N\big([1, 0]^\top, \operatorname{diag}(0.45^2, 0.45^2)\big)$, moves each through $f$ for 0.6 s and 1.2 s (with $\mathbf Q = \mathbf 0$ to isolate the effect), and compares their sample mean and 95% {term}`confidence ellipse` (black) with what the same number of EKF predict steps computes (red dotted).

    <img src="public/ch15_linearized_cloud.svg" class="graphic" alt="Phase-plane plot of angle versus angular velocity showing three clouds of points at 0, 0.6 and 1.2 seconds. At time zero the sample ellipse and the linearized ellipse coincide. Later the cloud bends into a crescent; the linearized ellipse is shifted and misoriented relative to the sample ellipse." />

    At $t = 0$ the two ellipses coincide. As time passes the cloud bends into a crescent, because the pendulum's period grows with its amplitude, so states with larger swings fall behind. The linearized prediction stays an ellipse, and its center is the image of the mean, $f(\cdots f(\boldsymbol\mu))$, rather than the mean of the image. Measurements usually keep the uncertainty small enough that this does not matter. When they do not, the next section shows what happens.
    """)
    return


@app.cell
def make_cloud_fig(F_pendulum, IMAGES_DIR, f_pendulum, np, plt):
    # jb: include=false
    def _ellipse(m, P, k2=5.991):
        _w, _V = np.linalg.eigh(P)
        _t = np.linspace(0, 2 * np.pi, 200)
        return m[:, None] + _V @ (np.sqrt(k2 * _w)[:, None] * np.vstack([np.cos(_t), np.sin(_t)]))

    _rng = np.random.default_rng(4)
    _mu = np.array([1.0, 0.0])
    _P = np.diag([0.45**2, 0.45**2])
    _X = _mu[:, None] + np.linalg.cholesky(_P) @ _rng.standard_normal((2, 3000))
    _m, _Pl = _mu.copy(), _P.copy()
    _fig, _ax = plt.subplots(figsize=(8, 5.5))
    _offsets = {0: (0.25, 0.75), 60: (0.3, -0.6), 120: (-0.2, 1.4)}
    for _k in range(121):
        if _k in _offsets:
            _first = _k == 0
            _ax.plot(_X[0], _X[1], ".", color="0.6", ms=1.5, label="sampled states" if _first else None)
            _e = _ellipse(_X.mean(axis=1), np.cov(_X))
            _ax.plot(_e[0], _e[1], "k-", label="sample mean and 95% ellipse" if _first else None)
            _ax.plot(*_X.mean(axis=1), "kx", ms=8)
            _e = _ellipse(_m, _Pl)
            _ax.plot(_e[0], _e[1], "r:", linewidth=2, label="linearized (EKF) mean and 95% ellipse" if _first else None)
            _ax.plot(*_m, "r+", ms=10, mew=2)
            _ax.annotate(f"t = {_k * 0.01:.1f} s", _m + np.array(_offsets[_k]), fontsize=10)
        _F = F_pendulum(_m)
        _Pl = _F @ _Pl @ _F.T
        _m = f_pendulum(_m)
        _X = f_pendulum(_X)
    _ax.set_xlabel(r"$\theta$ (rad)")
    _ax.set_ylabel(r"$\omega$ (rad/s)")
    _ax.set_title("Sampled versus linearized uncertainty of the pendulum state", style="italic")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.legend(loc="lower left", fontsize=8)
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch15_linearized_cloud.svg")
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Failure Modes

    ### Large Initial Error

    The measurement $h(\theta) = L\sin\theta$ takes the same value at $\theta$ and at $\pi - \theta$. From one camera reading, a bob below the pivot is indistinguishable from its mirror image above the pivot, and the Jacobian $L\cos\theta$ vanishes at $\theta = \pi/2$ and changes sign beyond it.

    Suppose the truth is $\theta = 1$ rad but the estimate is $\hat\theta = 1.8$ rad. The predicted measurement $L\sin 1.8 \approx 0.97$ m exceeds the actual one, about $L\sin 1 \approx 0.84$ m, so the innovation is negative. Since $\mathbf H_k = [L\cos 1.8,\ 0]$ has a negative first entry, the gain on $\theta$ is negative too, and the update *increases* $\hat\theta$, toward the mirror solution $\pi - 1 \approx 2.14$ rad that explains the measurement just as well. Linearized at the wrong place, the filter walks the wrong way. Once there, its model carries the estimate over the top, and the filter decides the pendulum is spinning.

    Use the sliders to change the initial angle error $\hat\theta_0 - \theta_0$ (with $\hat\omega_0 = \omega_0$ and $\mathbf P_0 = \operatorname{diag}(0.5^2, 0.5^2)$) and the measurement noise $\sigma_z$, which sets both the simulated noise and the filter's $\mathbf R$. The truth and the underlying random draws stay fixed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    init_error_slider = mo.ui.slider(-1.5, 1.5, 0.05, value=0.3, label=r"initial angle error $\hat\theta_0 - \theta_0$ (rad)", show_value=True)
    noise_slider = mo.ui.slider(0.01, 0.5, 0.01, value=0.05, label=r"measurement noise $\sigma_z$ (m)", show_value=True)
    return init_error_slider, noise_slider


@app.cell(hide_code=True)
def _(
    Q_PEND,
    TIMES,
    X0_TRUE,
    graphic,
    init_error_slider,
    measure,
    mo,
    noise_slider,
    np,
    plt,
    run_ekf,
    truth,
    unit_meas_noise,
):
    _sigma_z = noise_slider.value
    _zs = measure(truth, _sigma_z, unit_meas_noise)
    _x0_hat = X0_TRUE + np.array([init_error_slider.value, 0.0])
    _xs_hat, _Ps = run_ekf(_zs, _x0_hat, np.diag([0.5**2, 0.5**2]), Q_PEND, np.array([[_sigma_z**2]]))

    # Show angles wrapped to (-pi, pi], breaking the line where the wrap jumps.
    _wrapped = np.angle(np.exp(1j * _xs_hat[:, 0]))
    _jumps = np.abs(np.diff(_wrapped, prepend=_wrapped[0])) > np.pi
    _center = np.column_stack([np.where(_jumps, np.nan, _wrapped), _xs_hat[:, 1]])

    _fig, _axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    for _i, (_ax, _label, _unit) in enumerate(zip(_axes, [r"\theta", r"\omega"], ["rad, wrapped to $(-\\pi, \\pi]$", "rad/s"])):
        _sd = np.sqrt(_Ps[:, _i, _i])
        _ax.fill_between(TIMES, _center[:, _i] - 2 * _sd, _center[:, _i] + 2 * _sd, color="C1", alpha=0.2, label=r"$\pm 2\sigma$")
        _ax.plot(TIMES, truth[:, _i], "k-", linewidth=1, label="truth")
        _ax.plot(TIMES, _center[:, _i], "C1-", linewidth=1.2, label="EKF estimate")
        _ax.set_ylabel(rf"${_label}$ ({_unit})")
        _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _axes[0].axhline(np.pi / 2, color="0.4", linestyle="--", linewidth=1, label=r"$\theta = \pi/2$")
    _axes[0].set_ylim(-np.pi, np.pi)
    _axes[1].set_ylim(-8, 8)
    _axes[0].legend(loc="upper right", fontsize=8, ncol=4)
    _axes[1].set_xlabel("time (s)")
    _axes[0].set_title("EKF from a chosen initial error", style="italic")
    _fig.tight_layout()

    _late = TIMES >= 5.0
    _rmse = np.sqrt(np.mean(np.angle(np.exp(1j * (_xs_hat[_late, 0] - truth[_late, 0]))) ** 2))
    _verdict = "The filter converged." if _rmse < 0.2 else "The filter diverged: its estimate left the true trajectory and did not return."
    mo.vstack([
        mo.hstack([init_error_slider, noise_slider], justify="start", gap=2),
        graphic(_fig),
        mo.md(rf"Initial estimate $\hat\theta_0 = {_x0_hat[0]:.2f}$ rad. Root-mean-square angle error (wrapped) over the last 5 s: {_rmse:.3f} rad. {_verdict}"),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With $\sigma_z = 0.05$ m, every initial error that leaves $\hat\theta_0$ below $\pi/2$ converges, even $-1.5$ rad, while errors that put $\hat\theta_0$ beyond $\pi/2$ diverge. The size of the error matters less than which side of the fold it lands on. Larger $\sigma_z$ makes each update more cautious, which helps near the fold but slows convergence everywhere.

    ### Strong Nonlinearity

    The Gaussian explorer showed that the tangent line describes a wide distribution poorly. In a filter, this shows up as overconfidence. Panel (a) below runs the EKF 50 times from initial estimates drawn from $\mathcal N(\mathbf x_0, \mathbf P_0)$, so that the initial covariance is honest, with $\mathbf P_0 = \sigma_0^2\mathbf I$ for a narrow $\sigma_0 = 0.1$ and a wide $\sigma_0 = 0.6$. It plots the average {term}`normalized estimation error squared` over the runs that converged, with the 95% band of [Chapter 14](ch14_kalman_filters_in_practice.md) for a consistent filter.

    ### Bad Jacobians

    Panel (b) repeats the experiment with $\sigma_0 = 0.1$ for two filters: the correct one, and one that reuses the Jacobians of the small-angle (linear) pendulum, replacing $\cos\theta$ by $1$ in both $\mathbf A$ and $\mathbf H$. That is a natural mistake when an existing linear model is "upgraded" to an EKF.
    """)
    return


@app.cell
def nees_experiments(
    DT,
    F_pendulum,
    PEND_L,
    Q_PEND,
    R_PEND,
    SIGMA_Z,
    X0_TRUE,
    measure,
    nees_series,
    np,
    pendulum_rhs_jacobian,
    run_ekf,
    simulate_truth,
):
    # jb: include=false
    def F_small_angle(x):
        """Wrong on purpose: RK4-step Jacobian of the small-angle model (cos(theta) -> 1)."""
        _Asmall = pendulum_rhs_jacobian(np.zeros(2))
        _I = np.eye(2)
        _K1 = _Asmall
        _K2 = _Asmall @ (_I + 0.5 * DT * _K1)
        _K3 = _Asmall @ (_I + 0.5 * DT * _K2)
        _K4 = _Asmall @ (_I + DT * _K3)
        return _I + DT / 6 * (_K1 + 2 * _K2 + 2 * _K3 + _K4)

    def H_small_angle(x):
        """Wrong on purpose: measurement Jacobian with cos(theta) -> 1."""
        return np.array([[PEND_L, 0.0]])

    def _monte_carlo(sigma0, n_runs, n_steps, seed, F_jac=F_pendulum, H_jac=None):
        _rng = np.random.default_rng(seed)
        _P0 = sigma0**2 * np.eye(2)
        _truths = simulate_truth(X0_TRUE, n_steps, _rng, n_runs=n_runs)
        _nees, _converged = [], 0
        for _r in range(n_runs):
            _xs = _truths[:, :, _r]
            _zs = measure(_xs, SIGMA_Z, _rng.standard_normal(n_steps))
            _x0_hat = X0_TRUE + sigma0 * _rng.standard_normal(2)
            _kw = {"F_jac": F_jac} if H_jac is None else {"F_jac": F_jac, "H_jac": H_jac}
            _xh, _Ph = run_ekf(_zs, _x0_hat, _P0, Q_PEND, R_PEND, **_kw)
            if np.sqrt(np.mean((_xh[-50:, 0] - _xs[-50:, 0]) ** 2)) < 0.2:
                _converged += 1
                _nees.append(nees_series(_xs, _xh, _Ph))
        return np.mean(_nees, axis=0), _converged

    nees_narrow, conv_narrow = _monte_carlo(0.1, 50, 200, seed=21)
    nees_wide, conv_wide = _monte_carlo(0.6, 50, 200, seed=21)
    nees_good_jac, conv_good_jac = _monte_carlo(0.1, 30, 500, seed=22)
    nees_bad_jac, conv_bad_jac = _monte_carlo(0.1, 30, 500, seed=22, F_jac=F_small_angle, H_jac=H_small_angle)
    return (
        F_small_angle,
        H_small_angle,
        conv_bad_jac,
        conv_good_jac,
        conv_narrow,
        conv_wide,
        nees_bad_jac,
        nees_good_jac,
        nees_narrow,
        nees_wide,
    )


@app.cell
def make_nees_fig(
    DT,
    IMAGES_DIR,
    chi2,
    conv_bad_jac,
    conv_wide,
    nees_bad_jac,
    nees_good_jac,
    nees_narrow,
    nees_wide,
    np,
    plt,
):
    # jb: include=false
    def _band(n_runs, dim=2):
        return chi2.ppf(0.025, dim * n_runs) / n_runs, chi2.ppf(0.975, dim * n_runs) / n_runs

    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    _t1 = DT * np.arange(len(nees_narrow))
    _lo, _hi = _band(conv_wide)
    _ax1.axhspan(_lo, _hi, color="0.85", label=f"95% band ({conv_wide} runs)")
    _ax1.plot(_t1, nees_narrow, "k-", linewidth=1, label=r"narrow prior, $\sigma_0 = 0.1$")
    _ax1.plot(_t1, nees_wide, "C1-", linewidth=1.2, label=r"wide prior, $\sigma_0 = 0.6$")
    _ax1.set_title("(a) Strong nonlinearity", style="italic")

    _t2 = DT * np.arange(len(nees_good_jac))
    _lo, _hi = _band(conv_bad_jac)
    _ax2.axhspan(_lo, _hi, color="0.85", label=f"95% band ({conv_bad_jac} runs)")
    _ax2.plot(_t2, nees_good_jac, "k-", linewidth=1, label="correct Jacobians")
    _ax2.plot(_t2, nees_bad_jac, "C1-", linewidth=1.2, label="small-angle Jacobians")
    _ax2.set_title("(b) Bad Jacobians", style="italic")
    for _ax in (_ax1, _ax2):
        _ax.set_xlabel("time (s)")
        _ax.set_ylabel("average NEES")
        _ax.set_ylim(0, 7)
        _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
        _ax.legend(loc="upper right", fontsize=8)
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch15_nees_failure_modes.svg")
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch15_nees_failure_modes.svg" class="graphic" alt="Two plots of average NEES over time with a shaded 95% band near 2. Left: with a narrow prior the curve stays in the band; with a wide prior it spikes to about 4.5 in the first half second. Right: with correct Jacobians the curve stays near the band; with small-angle Jacobians it stays well above it." />
    """)
    return


@app.cell(hide_code=True)
def _(
    DT,
    conv_bad_jac,
    conv_wide,
    max_jacobian_error,
    F_small_angle,
    H_small_angle,
    f_pendulum,
    h_pendulum,
    mo,
    nees_bad_jac,
    nees_good_jac,
    nees_narrow,
    nees_wide,
    np,
    test_states,
):
    _half = int(round(0.5 / DT))
    _bad_F = max_jacobian_error(f_pendulum, F_small_angle, test_states)
    _bad_H = max_jacobian_error(h_pendulum, H_small_angle, test_states)
    mo.md(rf"""
    **Panel (a).** With the narrow prior, the average NEES over the first half second is {np.mean(nees_narrow[:_half]):.1f}, consistent with the state dimension 2. With the wide prior, {50 - conv_wide} of the 50 runs diverge (their estimates crossed the fold, as in the slider demo), and even the {conv_wide} that converge average {np.mean(nees_wide[:_half]):.1f} over the first half second, peaking at {np.max(nees_wide):.1f}: during the transient the filter believes its errors are much smaller than they are. Once the measurements have shrunk the uncertainty, the tangent-line approximation becomes good and the NEES returns to the band.

    **Panel (b).** The small-angle filter runs without complaint and its estimates look reasonable, but its average NEES over 5 s is {np.mean(nees_bad_jac):.1f} instead of {np.mean(nees_good_jac):.1f}, highest when the pendulum swings far from vertical. The numerical check catches the mistake at once: on the same 200 test states the small-angle Jacobians differ from the finite-difference ones by up to {_bad_F:.2f} (for $\mathbf J_f$) and {_bad_H:.2f} (for $\mathbf J_h$), compared with about $10^{{-10}}$ for the correct ones.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The Iterated EKF

    The update linearizes $h$ at the prediction $\hat{\mathbf x}_k^-$, but the update itself moves the estimate, often to where the linearization is more accurate. The **iterated extended Kalman filter** (IEKF) relinearizes there and repeats. Starting from $\mathbf x^{(0)} := \hat{\mathbf x}_k^-$, for $i = 0, 1, 2, \ldots$ it computes

    $$\mathbf H^{(i)} := \mathbf J_h(\mathbf x^{(i)}), \qquad \mathbf K^{(i)} := \mathbf P_k^-\mathbf H^{(i)\top}\big(\mathbf H^{(i)}\mathbf P_k^-\mathbf H^{(i)\top} + \mathbf R\big)^{-1},$$

    $$\mathbf x^{(i+1)} := \hat{\mathbf x}_k^- + \mathbf K^{(i)}\Big(\mathbf z_k - h(\mathbf x^{(i)}) - \mathbf H^{(i)}\big(\hat{\mathbf x}_k^- - \mathbf x^{(i)}\big)\Big),$$

    until $\mathbf x^{(i+1)}$ stops changing. Then $\hat{\mathbf x}_k$ is the last iterate and $\mathbf P_k = (\mathbf I - \mathbf K^{(i)}\mathbf H^{(i)})\mathbf P_k^-$. The first iteration is exactly the EKF update. @bell1993 show that the iterations are Gauss–Newton steps for the {term}`maximum a posteriori estimate` under the Gaussian assumptions, that is, for the $\mathbf x$ that minimizes

    $$\big(\mathbf z_k - h(\mathbf x)\big)^\top\mathbf R^{-1}\big(\mathbf z_k - h(\mathbf x)\big) + \big(\mathbf x - \hat{\mathbf x}_k^-\big)^\top\big(\mathbf P_k^-\big)^{-1}\big(\mathbf x - \hat{\mathbf x}_k^-\big).$$

    The IEKF helps when an accurate measurement passes through a strongly curved $h$. It does nothing for the prediction step, and it cannot resolve an ambiguity like the pendulum's fold: started on the wrong side, Gauss–Newton converges to the wrong minimum.

    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    Most of the EKF's failures trace back to its one approximation, the dropped Taylor remainders; the rest are mistakes in the Jacobians. Guard against both by:

    - verifying every Jacobian numerically before running the filter;
    - running Monte Carlo NEES tests (Chapter 14) with realistic initial errors, not just small ones;
    - initializing as close to the truth as possible (for the pendulum, from the first measurement, $\hat\theta_0 = \arcsin(z_1/L)$ with $z_1$ clipped to $[-L, L]$, which lands on the correct side of the fold whenever the bob stays below the pivot);
    - when the uncertainty must stay large, inflating $\mathbf Q$, iterating the update, or switching to the filters of the next chapter.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - A {term}`nonlinear system` has a process function or a measurement function that is not affine. The Kalman filter's derivation relies on affine maps and cannot be applied directly.
    - A Gaussian pushed through a nonlinear function has a shifted mean, a changed spread, and a non-Gaussian shape. The tangent line misses the mean shift, by at most $M\sigma^2/2$ when $|\phi''| \le M$.
    - The {term}`linearization` of $\phi$ at $\mathbf a$ is $\mathbf x \mapsto \phi(\mathbf a) + \mathbf J_\phi(\mathbf a)(\mathbf x - \mathbf a)$. Its error shrinks faster than $\|\mathbf x - \mathbf a\|$.
    - The {term}`extended Kalman filter` moves the estimate through $f$ and $h$ and the covariance through their Jacobians at the current estimate. For affine models it is exactly the Kalman filter.
    - On the pendulum, the EKF converges quickly and is consistent when started near the truth. It diverges when the initial estimate lies on the wrong side of the measurement's fold, becomes overconfident when the initial uncertainty is large, and silently loses consistency with wrong Jacobians.

    ## What's Next

    The EKF approximates the *function*. [Chapter 16](ch16_unscented_kalman_filter.md) approximates the *distribution* instead: it pushes a few carefully chosen points through the exact nonlinear functions and rebuilds the mean and covariance from them. That **unscented Kalman filter** needs no Jacobians, captures the mean shift that the tangent line misses, and, on the same pendulum, tolerates larger initial uncertainty. The chapter closes with particle filters, which can represent the two-sided ambiguity of the fold that defeats every Gaussian filter.
    """)
    return


if __name__ == "__main__":
    app.run()
