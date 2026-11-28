# /// script
# dependencies = [
#     "marimo>=0.25.1",
#     "matplotlib==3.11.2",
#     "numpy==2.5.3",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="12. Vectors, Matrices, and Covariance", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "Uncertainty in Many Dimensions"
    abbreviations:
      iff: if and only if
      diff: null
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
    IMAGES_DIR = Path(__file__).parent.parent / "notebooks" / "public"
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

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
    /// important | 🔗 **Prerequisites**
    - [Chapter 4](ch4_probability_spaces.md): {term}`almost surely`, and [continuity of probability from below](#ch4-thm-continuity-from-below) (one lemma only).
    - [Chapter 5](ch5_random_variables.md): {term}`random variables <random variable>`, [joint and marginal densities](#ch5-sec-joint-distributions), [independence as factorization of the joint density](#ch5-thm-factorization-criteria), and the {term}`normal distribution`.
    - [Chapter 6](ch6_expectation_and_variance.md): [linearity of expectation](#ch6-thm-linearity-and-positivity-of-expectation), {term}`variance`, {term}`covariance`, the {term}`correlation coefficient`, and [Chebyshev's inequality](#ch6-thm-chebyshevs-inequality).
    - [Chapter 7](ch7_optimal_alpha.md) and [Chapter 11](ch11_measurement_functions.md): the optimal gains $P^-/(P^- + R)$ and $P^-h/(h^2P^- + R)$, and [the tare-offset example](#ch11-sec-two-unknowns-one-reading).
    - [Chapter 8](ch8_bayesian_view.md): {term}`conditional densities <conditional density>` and the {term}`minimum mean squared error estimator`.
    - [Chapter 9](ch9_noise_levels.md): the {term}`chi-squared distribution` and the {term}`normalized innovation squared`.
    - [Appendix C: Multiple Integrals](#appc-sec-multiple-integrals): [iterated integrals](#appc-thm-tonelli-and-fubini), [the change-of-variables formula](#appc-thm-change-of-variables), and [polar coordinates](#appc-cor-polar-coordinates).
    - [Appendix D: Linear Algebra](appendix_d_linear_algebra.md): the sections listed in [the toolkit below](#ch12-sec-notation-and-linear-algebra-toolkit).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Chapter 10](ch10_process_models.md) and [Chapter 11](ch11_measurement_functions.md) both ended with two unknowns whose errors are correlated: a weight and its rate of change, and a weight and the scale's offset. In both cases the correlation mattered. An error in the rate becomes an error in tomorrow's weight; a reading that pins down weight plus offset tells us about the offset only to the extent that we know the weight. A single variance per unknown cannot express this. We need the variance of every unknown *and* the covariance of every pair, organized so that the rules of Chapter 6 still apply.

    That organization is the **covariance matrix**, and the distribution built on it is the **multivariate normal distribution**. This chapter develops both. Its payoff is one formula: what a jointly normal vector's distribution becomes once part of it has been observed. That formula turns out to be the Kalman filter's update step.

    /// attention | 🗝️ **Key Idea**
    A covariance matrix records the variance of every component of a random vector and the covariance of every pair. When jointly normal quantities are partly observed, the mean of the rest moves by (cross-covariance) $\times$ (covariance of the observed part)$^{-1}$ $\times$ (surprise), and their covariance shrinks by a Schur complement. That is the Kalman update.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch12-sec-notation-and-linear-algebra-toolkit -->
    ## Notation and Linear-Algebra Toolkit

    From now on, **bold lowercase letters are column vectors** ($\mathbf x \in \mathbb R^n$), **bold uppercase letters are matrices** ($\mathbf A \in \mathbb R^{m\times n}$ has $m$ rows and $n$ columns), and plain letters are scalars. $\mathbf A^\top$ is the {term}`transpose`, $\mathbf I$ the {term}`identity matrix`, and $\mathbf 0$ a vector or matrix of zeros. The facts below are proven or precisely cited in Appendix D:

    - Matrix products are associative and distribute over sums; $(\mathbf A\mathbf B)^\top = \mathbf B^\top\mathbf A^\top$ ([Appendix D: Matrix Multiplication](#appd-sec-matrix-multiplication), [Appendix D: Transpose, Identity, and Inverse](#appd-sec-transpose-identity-and-inverse)).
    - For {term}`invertible <invertible matrix>` $\mathbf A, \mathbf B$: $(\mathbf A\mathbf B)^{-1} = \mathbf B^{-1}\mathbf A^{-1}$ and $(\mathbf A^\top)^{-1} = (\mathbf A^{-1})^\top$ ([Appendix D: Transpose, Identity, and Inverse](#appd-sec-transpose-identity-and-inverse)). A square matrix is invertible iff the only vector it maps to $\mathbf 0$ is $\mathbf 0$ ([Appendix D: Linear Independence, Basis, and Rank](#appd-sec-linear-independence-basis-and-rank)).
    - {term}`Determinants <determinant>`: $\det(\mathbf A\mathbf B) = \det\mathbf A\,\det\mathbf B$, $\det\mathbf A^\top = \det\mathbf A$, and a square $\mathbf A$ is invertible iff $\det\mathbf A \neq 0$ ([Appendix D: Determinants](#appd-sec-determinants)).
    - A {term}`symmetric matrix` $\mathbf A$ is {term}`positive semidefinite` if $\mathbf a^\top\mathbf A\mathbf a \ge 0$ for every $\mathbf a$, and {term}`positive definite` if $\mathbf a^\top\mathbf A\mathbf a > 0$ for every $\mathbf a \neq \mathbf 0$ ([Appendix D: Symmetric and Positive Definite Matrices](#appd-sec-symmetric-and-positive-definite-matrices)).
    - **Spectral theorem:** every symmetric $\mathbf A$ can be written $\mathbf A = \mathbf Q\boldsymbol\Lambda\mathbf Q^\top$, with $\mathbf Q$ an {term}`orthogonal matrix` ($\mathbf Q^\top\mathbf Q = \mathbf Q\mathbf Q^\top = \mathbf I$) whose columns are {term}`eigenvectors <eigenvector>` and $\boldsymbol\Lambda$ diagonal with the corresponding {term}`eigenvalues <eigenvalue>` ([Appendix D: Symmetric and Positive Definite Matrices](#appd-sec-symmetric-and-positive-definite-matrices); see also [Appendix D: Eigenvalues and Eigenvectors](#appd-sec-eigenvalues-and-eigenvectors) and [Appendix D: Orthogonal Matrices](#appd-sec-orthogonal-matrices)).
    - **Cholesky:** every positive definite $\boldsymbol\Sigma$ can be written $\boldsymbol\Sigma = \mathbf L\mathbf L^\top$ with $\mathbf L$ lower triangular with positive diagonal entries ([Appendix D: Cholesky Decomposition](#appd-sec-cholesky-decomposition)).
    - Block matrices multiply block by block, like numbers, as long as the block sizes match and the order of factors is kept ([Appendix D: Block Matrices and the Schur Complement](#appd-sec-block-matrices-and-the-schur-complement)).

    Two small consequences are used repeatedly.

    /// admonition | 📐 **Lemma (Positive Definite Matrices)**
        attrs: {class: lemma, id: ch12-lem-positive-definite-matrices}
    Let $\boldsymbol\Sigma \in \mathbb R^{n\times n}$ be positive definite.

    1. $\boldsymbol\Sigma$ is invertible, and $\boldsymbol\Sigma^{-1}$ is positive definite.
    2. If $\mathbf A \in \mathbb R^{n\times n}$ is invertible, then $\mathbf A\boldsymbol\Sigma\mathbf A^\top$ is positive definite.
    3. $\det\boldsymbol\Sigma > 0$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    1. If $\boldsymbol\Sigma\mathbf a = \mathbf 0$ then $\mathbf a^\top\boldsymbol\Sigma\mathbf a = 0$, so $\mathbf a = \mathbf 0$; hence $\boldsymbol\Sigma$ is invertible. Its inverse is symmetric, since $(\boldsymbol\Sigma^{-1})^\top = (\boldsymbol\Sigma^\top)^{-1} = \boldsymbol\Sigma^{-1}$. For $\mathbf a \neq \mathbf 0$, let $\mathbf b := \boldsymbol\Sigma^{-1}\mathbf a \neq \mathbf 0$; then $\mathbf a^\top\boldsymbol\Sigma^{-1}\mathbf a = \mathbf b^\top\boldsymbol\Sigma\mathbf b > 0$.
    2. $\mathbf A\boldsymbol\Sigma\mathbf A^\top$ is symmetric, and for $\mathbf a \neq \mathbf 0$ the vector $\mathbf A^\top\mathbf a$ is nonzero (because $\mathbf A^\top$ is invertible), so $\mathbf a^\top\mathbf A\boldsymbol\Sigma\mathbf A^\top\mathbf a = (\mathbf A^\top\mathbf a)^\top\boldsymbol\Sigma(\mathbf A^\top\mathbf a) > 0$.
    3. With the Cholesky factor, $\det\boldsymbol\Sigma = \det\mathbf L\,\det\mathbf L^\top = (\det\mathbf L)^2$, and $\det\mathbf L \neq 0$ because $\mathbf L$ is invertible (if $\mathbf L$ were not, neither would $\mathbf L\mathbf L^\top = \boldsymbol\Sigma$ be). $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch12-sec-random-vectors-and-mean-vectors -->
    ## Random Vectors and Mean Vectors

    In the bulking example of Chapter 10, after a prediction step we are uncertain about two numbers: the error $e^x$ in the predicted weight and the error $e^r$ in the predicted rate. It is natural to stack them.

    /// note | 📖 **Definition**
    <u>**Random vector**</u>

    A list $\mathbf x = [x_1, \ldots, x_n]^\top$ of {term}`random variables <random variable>` defined on the same probability space. Equivalently, a function $\mathbf x: \Omega \to \mathbb R^n$ each of whose components is a random variable.
    ///

    The *distribution* of a random vector is the {term}`joint distribution` of its components ([Chapter 5](#ch5-sec-joint-distributions)). When it has a {term}`joint density` $f_{\mathbf x}: \mathbb R^n \to [0, \infty)$, probabilities are integrals over regions of $\mathbb R^n$: $\mathbb P(\mathbf x \in B) = \int_B f_{\mathbf x}(\mathbf x)\,d\mathbf x$. As in the scalar case, we use the same letter for a random vector and for a point where its density is evaluated when no confusion can arise.

    The expected value of a vector or matrix whose entries are random variables is taken entry by entry.

    /// note | 📖 **Definition**
    <u>**Mean vector**</u>

    For a random vector $\mathbf x = [x_1, \ldots, x_n]^\top$ whose components all have finite {term}`expected values <expected value>`, the vector
    $$\boldsymbol\mu = \mathbb E[\mathbf x] := \big[\mathbb E[x_1], \ldots, \mathbb E[x_n]\big]^\top.$$
    ///

    Linearity of expectation carries over to matrices.

    /// admonition | 📐 **Lemma (Linearity for Random Matrices)**
        attrs: {class: lemma, id: ch12-lem-linearity-for-random-matrices}
    Let $\mathbf X$ be an $m\times n$ matrix of random variables with finite expected values, and let $\mathbf A \in \mathbb R^{p\times m}$, $\mathbf B \in \mathbb R^{n\times q}$, $\mathbf C \in \mathbb R^{p\times q}$ be constant. Then $\mathbb E[\mathbf A\mathbf X\mathbf B + \mathbf C] = \mathbf A\,\mathbb E[\mathbf X]\,\mathbf B + \mathbf C$ and $\mathbb E[\mathbf X^\top] = \mathbb E[\mathbf X]^\top$. In particular, $\mathbb E[\mathbf A\mathbf x + \mathbf b] = \mathbf A\boldsymbol\mu + \mathbf b$ for a random vector $\mathbf x$ with mean $\boldsymbol\mu$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Entry $(i, j)$ of $\mathbf A\mathbf X\mathbf B + \mathbf C$ is $\sum_{k=1}^m\sum_{l=1}^n A_{ik}X_{kl}B_{lj} + C_{ij}$, a linear combination of entries of $\mathbf X$ plus a constant. By linearity of expectation ([Chapter 6](#ch6-thm-linearity-and-positivity-of-expectation)) its expected value is $\sum_{k,l} A_{ik}\,\mathbb E[X_{kl}]\,B_{lj} + C_{ij}$, which is entry $(i, j)$ of $\mathbf A\,\mathbb E[\mathbf X]\,\mathbf B + \mathbf C$. Transposition only relabels entries. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch12-sec-covariance-matrices -->
    ## Covariance Matrices

    /// note | 📖 **Definition**
    <u>**Covariance matrix**</u>

    For a random vector $\mathbf x \in \mathbb R^n$ with mean $\boldsymbol\mu$ whose components all have finite {term}`variances <variance>`, the $n \times n$ matrix
    $$\operatorname{Cov}(\mathbf x) := \mathbb E\big[(\mathbf x - \boldsymbol\mu)(\mathbf x - \boldsymbol\mu)^\top\big],$$
    whose entry $(i, j)$ is the {term}`covariance` $\operatorname{Cov}(x_i, x_j)$.
    ///

    The diagonal entries are the variances $\operatorname{Var}(x_i)$. We often write $\boldsymbol\Sigma$ for a covariance matrix, and $\mathbf P$ for the covariance of an estimation error. For two components with standard deviations $\sigma_x, \sigma_y$ and {term}`correlation coefficient` $\rho$,
    $$\boldsymbol\Sigma = \begin{bmatrix}\sigma_x^2 & \rho\,\sigma_x\sigma_y\\ \rho\,\sigma_x\sigma_y & \sigma_y^2\end{bmatrix}.$$

    /// admonition | 📐 **Theorem (Covariance Matrices Are Symmetric and Positive Semidefinite)**
        attrs: {class: theorem, id: ch12-thm-covariance-matrices-are-symmetric-and-positive-semidefinite}
    Let $\boldsymbol\Sigma = \operatorname{Cov}(\mathbf x)$. Then $\boldsymbol\Sigma$ is symmetric, and for every $\mathbf a \in \mathbb R^n$
    $$\mathbf a^\top\boldsymbol\Sigma\,\mathbf a = \operatorname{Var}(\mathbf a^\top\mathbf x) \ge 0.$$
    So $\boldsymbol\Sigma$ is positive semidefinite.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Symmetry: $\operatorname{Cov}(x_i, x_j) = \operatorname{Cov}(x_j, x_i)$. For the quadratic form, the linearity lemma gives $\mathbb E[\mathbf a^\top\mathbf x] = \mathbf a^\top\boldsymbol\mu$ and
    $$\mathbf a^\top\boldsymbol\Sigma\,\mathbf a = \mathbb E\big[\mathbf a^\top(\mathbf x - \boldsymbol\mu)(\mathbf x - \boldsymbol\mu)^\top\mathbf a\big] = \mathbb E\big[(\mathbf a^\top\mathbf x - \mathbf a^\top\boldsymbol\mu)^2\big] = \operatorname{Var}(\mathbf a^\top\mathbf x),$$
    because $(\mathbf x - \boldsymbol\mu)^\top\mathbf a$ is the same number as $\mathbf a^\top(\mathbf x - \boldsymbol\mu)$. A variance is never negative. $\blacksquare$
    ///

    When is a covariance matrix positive *definite*? The answer needs one fact about variances.

    /// admonition | 📐 **Lemma (Zero Variance)**
        attrs: {class: lemma, id: ch12-lem-zero-variance}
    A random variable $y$ with finite variance has $\operatorname{Var}(y) = 0$ iff $y = \mathbb E[y]$ {term}`almost surely`.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    ($\Leftarrow$) If $y = \mathbb E[y]$ almost surely, then $(y - \mathbb E[y])^2$ has the same distribution as the constant $0$, so its expected value, $\operatorname{Var}(y)$, is $0$.
    ($\Rightarrow$) By Chebyshev's inequality ([Chapter 6](#ch6-thm-chebyshevs-inequality)), the events $A_j := \{|y - \mathbb E[y]| \ge 1/j\}$ have $\mathbb P(A_j) \le j^2\operatorname{Var}(y) = 0$ for every $j \in \mathbb N^+$. They increase with $j$, and their union is $\{y \neq \mathbb E[y]\}$, so by continuity from below ([Chapter 4](#ch4-thm-continuity-from-below)) $\mathbb P(y \neq \mathbb E[y]) = \lim_{j\to\infty}\mathbb P(A_j) = 0$. $\blacksquare$
    ///

    /// admonition | 📐 **Theorem (When a Covariance Matrix Is Positive Definite)**
        attrs: {class: theorem, id: ch12-thm-when-a-covariance-matrix-is-positive-definite}
    $\operatorname{Cov}(\mathbf x)$ is positive definite iff no linear combination $\mathbf a^\top\mathbf x$ with $\mathbf a \neq \mathbf 0$ is almost surely constant.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    $\operatorname{Cov}(\mathbf x)$ is positive semidefinite, so it is positive definite iff $\mathbf a^\top\operatorname{Cov}(\mathbf x)\,\mathbf a \neq 0$ for every $\mathbf a \neq \mathbf 0$. By the [Covariance Matrices Are Symmetric and Positive Semidefinite theorem](#ch12-thm-covariance-matrices-are-symmetric-and-positive-semidefinite) and the [Zero Variance lemma](#ch12-lem-zero-variance), $\mathbf a^\top\operatorname{Cov}(\mathbf x)\,\mathbf a = \operatorname{Var}(\mathbf a^\top\mathbf x) = 0$ iff $\mathbf a^\top\mathbf x$ is almost surely constant. $\blacksquare$
    ///

    For example, if $x$ is a weight, $c$ an offset, and $y = x + c$ a noise-free reading, then $[1, 1, -1]\,[x, c, y]^\top = 0$ always, so $\operatorname{Cov}([x, c, y]^\top)$ is singular. Measurement noise prevents this for a state and its measurement. For two components the condition is easy to read off.

    /// admonition | 📐 **Corollary (Two Components)**
        attrs: {class: corollary, id: ch12-cor-two-components}
    Let $\sigma_x, \sigma_y > 0$. The matrix $\begin{bmatrix}\sigma_x^2 & \rho\sigma_x\sigma_y\\ \rho\sigma_x\sigma_y & \sigma_y^2\end{bmatrix}$ is positive semidefinite iff $|\rho| \le 1$, and positive definite iff $|\rho| < 1$. In particular, every correlation coefficient lies in $[-1, 1]$, which gives a second proof of Chapter 6's bound.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Expanding shows that for $\mathbf a = [a_1, a_2]^\top$,
    $$\mathbf a^\top\boldsymbol\Sigma\,\mathbf a = \sigma_x^2a_1^2 + 2\rho\sigma_x\sigma_y a_1a_2 + \sigma_y^2a_2^2 = (\sigma_x a_1 + \rho\sigma_y a_2)^2 + (1 - \rho^2)\,\sigma_y^2a_2^2.$$
    If $|\rho| \le 1$ both terms are $\ge 0$. If $|\rho| < 1$ the sum is $0$ only if $a_2 = 0$ and then $\sigma_x a_1 = 0$, that is, only if $\mathbf a = \mathbf 0$. For $\mathbf a = [-\rho\sigma_y, \sigma_x]^\top \neq \mathbf 0$ the first term is $0$ and the second is $(1 - \rho^2)\sigma_y^2\sigma_x^2$, which is $< 0$ if $|\rho| > 1$ and $= 0$ if $|\rho| = 1$. The last claim follows because every covariance matrix is positive semidefinite. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The most important rule is how a covariance matrix changes under a linear map. It is the matrix version of $\operatorname{Var}(aX + b) = a^2\operatorname{Var}(X)$.

    /// admonition | 📐 **Theorem (Affine Transformation of Mean and Covariance)**
        attrs: {class: theorem, id: ch12-thm-affine-transformation-of-mean-and-covariance}
    Let $\mathbf x \in \mathbb R^n$ have mean $\boldsymbol\mu$ and covariance $\boldsymbol\Sigma$, and let $\mathbf A \in \mathbb R^{m\times n}$ and $\mathbf b \in \mathbb R^m$ be constant. Then $\mathbf y := \mathbf A\mathbf x + \mathbf b$ has
    $$\mathbb E[\mathbf y] = \mathbf A\boldsymbol\mu + \mathbf b, \qquad \operatorname{Cov}(\mathbf y) = \mathbf A\boldsymbol\Sigma\mathbf A^\top.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    The mean follows from the linearity lemma. Then $\mathbf y - \mathbb E[\mathbf y] = \mathbf A(\mathbf x - \boldsymbol\mu)$, so
    $$\operatorname{Cov}(\mathbf y) = \mathbb E\big[\mathbf A(\mathbf x - \boldsymbol\mu)(\mathbf x - \boldsymbol\mu)^\top\mathbf A^\top\big] = \mathbf A\,\mathbb E\big[(\mathbf x - \boldsymbol\mu)(\mathbf x - \boldsymbol\mu)^\top\big]\,\mathbf A^\top = \mathbf A\boldsymbol\Sigma\mathbf A^\top. \;\blacksquare$$
    ///

    **Example (the rate model).** In Chapter 10's rate model, one prediction step maps the error vector $\mathbf e = [e^x, e^r]^\top$ (weight, daily rate) to $\mathbf F\mathbf e$ with $\mathbf F = \begin{bmatrix}1 & 1\\ 0 & 1\end{bmatrix}$, ignoring process noise. Suppose today the errors are uncorrelated, with standard deviations $1$ lb and $0.1$ lb/day: $\mathbf P = \operatorname{diag}(1, 0.01)$. Then
    $$\mathbf F\mathbf P\mathbf F^\top = \begin{bmatrix}1.01 & 0.01\\ 0.01 & 0.01\end{bmatrix}, \qquad \mathbf F^{10}\mathbf P(\mathbf F^{10})^\top = \begin{bmatrix}2 & 0.1\\ 0.1 & 0.01\end{bmatrix},$$
    since $\mathbf F^{10} = \begin{bmatrix}1 & 10\\ 0 & 1\end{bmatrix}$. The correlation grows from $0$ to about $0.10$ after one day and to $0.1/\sqrt{2 \cdot 0.01} \approx 0.71$ after ten days without a weigh-in: the prediction ties the weight error to the rate error. This one line of matrix algebra replaces Chapter 10's separate formulas for two variances and a covariance.

    Between two different random vectors we need the covariance of every component of one with every component of the other.

    /// note | 📖 **Definition**
    <u>**Cross-covariance matrix**</u>

    For random vectors $\mathbf x \in \mathbb R^n$ and $\mathbf y \in \mathbb R^m$ on the same probability space, with means $\boldsymbol\mu_x, \boldsymbol\mu_y$ and components of finite variance, the $n\times m$ matrix
    $$\operatorname{Cov}(\mathbf x, \mathbf y) := \mathbb E\big[(\mathbf x - \boldsymbol\mu_x)(\mathbf y - \boldsymbol\mu_y)^\top\big],$$
    whose entry $(i, j)$ is $\operatorname{Cov}(x_i, y_j)$.
    ///

    We call $\mathbf x$ and $\mathbf y$ *uncorrelated* if $\operatorname{Cov}(\mathbf x, \mathbf y) = \mathbf 0$.

    /// admonition | 📐 **Lemma (Rules for Cross-Covariances)**
        attrs: {class: lemma, id: ch12-lem-rules-for-cross-covariances}
    For random vectors $\mathbf x, \mathbf y$ as above and constant $\mathbf A, \mathbf B, \mathbf a, \mathbf b$ of compatible sizes:

    1. $\operatorname{Cov}(\mathbf x, \mathbf x) = \operatorname{Cov}(\mathbf x)$ and $\operatorname{Cov}(\mathbf y, \mathbf x) = \operatorname{Cov}(\mathbf x, \mathbf y)^\top$.
    2. $\operatorname{Cov}(\mathbf A\mathbf x + \mathbf a, \mathbf B\mathbf y + \mathbf b) = \mathbf A\operatorname{Cov}(\mathbf x, \mathbf y)\mathbf B^\top$.
    3. If $n = m$: $\operatorname{Cov}(\mathbf x + \mathbf y) = \operatorname{Cov}(\mathbf x) + \operatorname{Cov}(\mathbf y) + \operatorname{Cov}(\mathbf x, \mathbf y) + \operatorname{Cov}(\mathbf y, \mathbf x)$; if $\mathbf x, \mathbf y$ are uncorrelated, $\operatorname{Cov}(\mathbf x + \mathbf y) = \operatorname{Cov}(\mathbf x) + \operatorname{Cov}(\mathbf y)$.
    4. If every $x_i$ is independent of every $y_j$, then $\mathbf x$ and $\mathbf y$ are uncorrelated.
    5. The stacked vector $\begin{bmatrix}\mathbf x\\ \mathbf y\end{bmatrix}$ has covariance $\begin{bmatrix}\operatorname{Cov}(\mathbf x) & \operatorname{Cov}(\mathbf x, \mathbf y)\\ \operatorname{Cov}(\mathbf y, \mathbf x) & \operatorname{Cov}(\mathbf y)\end{bmatrix}$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    1. The first is the definition; for the second, transpose the matrix inside the expectation, using $(\mathbf u\mathbf v^\top)^\top = \mathbf v\mathbf u^\top$.
    2. The centered vectors are $\mathbf A(\mathbf x - \boldsymbol\mu_x)$ and $\mathbf B(\mathbf y - \boldsymbol\mu_y)$; pull $\mathbf A$ and $\mathbf B^\top$ out of the expectation with the linearity lemma.
    3. Expand $\mathbb E\big[(\mathbf u + \mathbf v)(\mathbf u + \mathbf v)^\top\big]$ for the centered vectors $\mathbf u = \mathbf x - \boldsymbol\mu_x$, $\mathbf v = \mathbf y - \boldsymbol\mu_y$ into four terms and use linearity.
    4. Each entry $\operatorname{Cov}(x_i, y_j)$ is $0$, because independent random variables are uncorrelated ([Chapter 6](#ch6-thm-independent-implies-uncorrelated)).
    5. Compare entries block by block with the definitions. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **Finite variances.** Covariance matrices exist only when every component has a finite variance. Some heavy-tailed noise models (the Cauchy distribution, for example) have none, and then nothing in this chapter applies.
    - **Positive semidefinite, not always definite.** A covariance matrix is singular exactly when some combination of the components is constant. In a filter this happens when a quantity is known exactly (for example, a state with zero initial uncertainty that never receives process noise); formulas that invert such a matrix then fail.
    - **Numerically computed covariances** can lose symmetry or positive semidefiniteness through rounding. A covariance estimated from fewer samples than its dimension is always singular. Chapter 13 and [Chapter 14](#ch14-sec-numerical-stability) discuss remedies.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch12-sec-the-multivariate-normal-distribution -->
    ## The Multivariate Normal Distribution

    Chapter 5's normal density has the variance in the denominator of the exponent. The multivariate version puts the inverse covariance matrix there. We first build the simplest example from scalar normals. Let $y_1, \ldots, y_n$ be independent standard normal random variables and $\mathbf y := [y_1, \ldots, y_n]^\top$. By independence ([Chapter 5](#ch5-thm-factorization-criteria)), the joint density is the product of the marginal densities:
    $$f_{\mathbf y}(\mathbf y) = \prod_{i=1}^n \frac{1}{\sqrt{2\pi}}e^{-y_i^2/2} = (2\pi)^{-n/2}\exp\Big(-\tfrac12\,\mathbf y^\top\mathbf y\Big).$$
    Its mean is $\mathbf 0$ and its covariance is $\mathbf I$ (unit variances, and independent components are uncorrelated). This is the case $\boldsymbol\mu = \mathbf 0$, $\boldsymbol\Sigma = \mathbf I$ of the following definition.

    /// note | 📖 **Definition**
    <u>**Multivariate normal distribution**</u>

    Let $\boldsymbol\mu \in \mathbb R^n$ and let $\boldsymbol\Sigma \in \mathbb R^{n\times n}$ be positive definite. A random vector $\mathbf x$ has the multivariate normal distribution $\mathcal N(\boldsymbol\mu, \boldsymbol\Sigma)$ iff it has the joint density
    $$f(\mathbf x) = (2\pi)^{-n/2}(\det\boldsymbol\Sigma)^{-1/2}\exp\Big(-\tfrac12(\mathbf x - \boldsymbol\mu)^\top\boldsymbol\Sigma^{-1}(\mathbf x - \boldsymbol\mu)\Big) \qquad \text{for all } \mathbf x \in \mathbb R^n.$$
    Random vectors $\mathbf x$ and $\mathbf z$ are *jointly normal* iff the stacked vector $[\mathbf x; \mathbf z]$ has a multivariate normal distribution.
    ///

    For $n = 1$ and $\boldsymbol\Sigma = [\sigma^2]$ this is Chapter 5's $\mathcal N(\mu, \sigma^2)$. The formula makes sense because $\det\boldsymbol\Sigma > 0$ and $\boldsymbol\Sigma^{-1}$ exists (lemma above). Some authors also allow singular $\boldsymbol\Sigma$, defining a random vector to be multivariate normal iff every linear combination $\mathbf a^\top\mathbf x$ is normal or constant; such a vector has no density when $\boldsymbol\Sigma$ is singular ([Wikipedia: Multivariate normal distribution](https://en.wikipedia.org/wiki/Multivariate_normal_distribution)). We will not need that generality.

    Two questions arise at once: is $f$ really a density (does it integrate to $1$?), and are $\boldsymbol\mu$ and $\boldsymbol\Sigma$ really the mean and covariance? Both answers come from transforming the standard normal vector $\mathbf y$, for which we need the change-of-variables formula for multiple integrals.

    /// admonition | 📐 **Theorem (Densities Under Invertible Affine Maps)**
        attrs: {class: theorem, id: ch12-thm-densities-under-invertible-affine-maps}
    Let $\mathbf y$ have joint density $f_{\mathbf y}$ on $\mathbb R^n$, let $\mathbf A \in \mathbb R^{n\times n}$ be invertible, and $\mathbf b \in \mathbb R^n$. Then $\mathbf x := \mathbf A\mathbf y + \mathbf b$ has the joint density
    $$f_{\mathbf x}(\mathbf x) = \frac{f_{\mathbf y}\big(\mathbf A^{-1}(\mathbf x - \mathbf b)\big)}{|\det\mathbf A|}.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Not proven here. For every Borel set $B \subseteq \mathbb R^n$, $\mathbb P(\mathbf x \in B) = \mathbb P\big(\mathbf y \in \mathbf A^{-1}(B - \mathbf b)\big) = \int_{\mathbf A^{-1}(B - \mathbf b)} f_{\mathbf y}(\mathbf y)\,d\mathbf y$. The change-of-variables theorem for multiple integrals, applied to the invertible map $\mathbf y = \mathbf A^{-1}(\mathbf x - \mathbf b)$ whose Jacobian determinant is the constant $\det\mathbf A^{-1} = 1/\det\mathbf A$, turns this into $\int_B f_{\mathbf y}\big(\mathbf A^{-1}(\mathbf x - \mathbf b)\big)\,|\det\mathbf A|^{-1}\,d\mathbf x$. See [Appendix C: Multiple Integrals](#appc-sec-multiple-integrals) and [Wikipedia: Integration by substitution (substitution for multiple variables)](https://en.wikipedia.org/wiki/Integration_by_substitution#Substitution_for_multiple_variables). $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// admonition | 📐 **Theorem (Existence, Mean, and Covariance of the Multivariate Normal)**
        attrs: {class: theorem, id: ch12-thm-existence-mean-and-covariance-of-the-multivariate-normal}
    Let $\boldsymbol\mu \in \mathbb R^n$, let $\boldsymbol\Sigma$ be positive definite with Cholesky factor $\mathbf L$ ($\boldsymbol\Sigma = \mathbf L\mathbf L^\top$), and let $\mathbf y$ be a standard normal vector as above. Then:

    1. $\mathbf x := \mathbf L\mathbf y + \boldsymbol\mu$ has the distribution $\mathcal N(\boldsymbol\mu, \boldsymbol\Sigma)$; in particular, the density in the definition integrates to $1$;
    2. every random vector with distribution $\mathcal N(\boldsymbol\mu, \boldsymbol\Sigma)$ has mean $\boldsymbol\mu$ and covariance $\boldsymbol\Sigma$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    1. $\mathbf L$ is invertible (lemma above), so by the previous theorem $\mathbf x$ has density
    $$f_{\mathbf x}(\mathbf x) = \frac{(2\pi)^{-n/2}}{|\det\mathbf L|}\exp\Big(-\tfrac12\big(\mathbf L^{-1}(\mathbf x - \boldsymbol\mu)\big)^\top\big(\mathbf L^{-1}(\mathbf x - \boldsymbol\mu)\big)\Big).$$
    The exponent is $-\tfrac12(\mathbf x - \boldsymbol\mu)^\top(\mathbf L^{-1})^\top\mathbf L^{-1}(\mathbf x - \boldsymbol\mu) = -\tfrac12(\mathbf x - \boldsymbol\mu)^\top(\mathbf L\mathbf L^\top)^{-1}(\mathbf x - \boldsymbol\mu)$, and $|\det\mathbf L| = (\det\boldsymbol\Sigma)^{1/2}$ because $\det\boldsymbol\Sigma = (\det\mathbf L)^2$. So $f_{\mathbf x}$ is exactly the density in the definition. Being the density of a random vector, it integrates to $1$.
    2. For $\mathbf x$ from part 1, the affine-transformation theorem gives mean $\mathbf L\mathbf 0 + \boldsymbol\mu = \boldsymbol\mu$ and covariance $\mathbf L\mathbf I\mathbf L^\top = \boldsymbol\Sigma$. Means and covariances are computed from the density alone ([Chapter 6](#ch6-thm-lotus)), so every random vector with this density has the same mean and covariance. $\blacksquare$
    ///

    Part 1 is also how simulations draw samples from $\mathcal N(\boldsymbol\mu, \boldsymbol\Sigma)$: draw independent standard normals and compute $\mathbf L\mathbf y + \boldsymbol\mu$ with `np.linalg.cholesky`. The [Normalization lemma](#ch12-lem-normalization) below lets us recognize a multivariate normal density from the shape of its exponent alone, without computing determinants.

    /// admonition | 📐 **Lemma (Normalization)**
        attrs: {class: lemma, id: ch12-lem-normalization}
    Let $f$ be a joint density on $\mathbb R^n$, $\mathbf m \in \mathbb R^n$, and $\boldsymbol\Sigma$ positive definite. If there is a constant $\kappa$ such that $f(\mathbf x) = \kappa\exp\big(-\tfrac12(\mathbf x - \mathbf m)^\top\boldsymbol\Sigma^{-1}(\mathbf x - \mathbf m)\big)$ for all $\mathbf x$, then $f$ is the $\mathcal N(\mathbf m, \boldsymbol\Sigma)$ density.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Let $g$ be the $\mathcal N(\mathbf m, \boldsymbol\Sigma)$ density and $\kappa_{\boldsymbol\Sigma} := (2\pi)^{-n/2}(\det\boldsymbol\Sigma)^{-1/2}$ its constant. Then $f = (\kappa/\kappa_{\boldsymbol\Sigma})\,g$. Both $f$ and $g$ integrate to $1$ (the latter by the previous theorem), so $\kappa/\kappa_{\boldsymbol\Sigma} = 1$. $\blacksquare$
    ///

    /// admonition | 📐 **Theorem (Invertible Affine Maps Preserve Normality)**
        attrs: {class: theorem, id: ch12-thm-invertible-affine-maps-preserve-normality}
    If $\mathbf x \sim \mathcal N(\boldsymbol\mu, \boldsymbol\Sigma)$, $\mathbf A \in \mathbb R^{n\times n}$ is invertible, and $\mathbf b \in \mathbb R^n$, then $\mathbf A\mathbf x + \mathbf b \sim \mathcal N(\mathbf A\boldsymbol\mu + \mathbf b,\ \mathbf A\boldsymbol\Sigma\mathbf A^\top)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Let $\mathbf m := \mathbf A\boldsymbol\mu + \mathbf b$. By the change-of-variables theorem, $\mathbf y := \mathbf A\mathbf x + \mathbf b$ has density $f_{\mathbf x}\big(\mathbf A^{-1}(\mathbf y - \mathbf b)\big)/|\det\mathbf A|$. Since $\mathbf A^{-1}(\mathbf y - \mathbf b) - \boldsymbol\mu = \mathbf A^{-1}(\mathbf y - \mathbf m)$, the exponent is
    $$-\tfrac12(\mathbf y - \mathbf m)^\top(\mathbf A^{-1})^\top\boldsymbol\Sigma^{-1}\mathbf A^{-1}(\mathbf y - \mathbf m) = -\tfrac12(\mathbf y - \mathbf m)^\top(\mathbf A\boldsymbol\Sigma\mathbf A^\top)^{-1}(\mathbf y - \mathbf m).$$
    So the density of $\mathbf y$ is a constant times $\exp\big(-\tfrac12(\mathbf y - \mathbf m)^\top(\mathbf A\boldsymbol\Sigma\mathbf A^\top)^{-1}(\mathbf y - \mathbf m)\big)$, where $\mathbf A\boldsymbol\Sigma\mathbf A^\top$ is positive definite (lemma above). By the normalization lemma, $\mathbf y \sim \mathcal N(\mathbf m, \mathbf A\boldsymbol\Sigma\mathbf A^\top)$. $\blacksquare$
    ///

    The same conclusion holds for any $\mathbf A \in \mathbb R^{m\times n}$ whose $m$ rows are linearly independent, so that $\mathbf A\boldsymbol\Sigma\mathbf A^\top$ is still positive definite. One proof extends $\mathbf A$ to an invertible matrix by adding rows and then keeps only the first $m$ components, using the marginal theorem below ([Wikipedia: Multivariate normal distribution](https://en.wikipedia.org/wiki/Multivariate_normal_distribution)). We only need the invertible case.

    Finally, independent normal pieces stack into a normal vector.

    /// admonition | 📐 **Corollary (Stacking Independent Normal Vectors)**
        attrs: {class: corollary, id: ch12-cor-stacking-independent-normal-vectors}
    If $\mathbf x \sim \mathcal N(\boldsymbol\mu_x, \boldsymbol\Sigma_x)$ and $\mathbf v \sim \mathcal N(\boldsymbol\mu_v, \boldsymbol\Sigma_v)$ are independent (their joint density is the product of their densities), then
    $$\begin{bmatrix}\mathbf x\\ \mathbf v\end{bmatrix} \sim \mathcal N\left(\begin{bmatrix}\boldsymbol\mu_x\\ \boldsymbol\mu_v\end{bmatrix}, \begin{bmatrix}\boldsymbol\Sigma_x & \mathbf 0\\ \mathbf 0 & \boldsymbol\Sigma_v\end{bmatrix}\right).$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Let $\mathbf D$ be the block-diagonal matrix above. It is positive definite, since $[\mathbf a; \mathbf b]^\top\mathbf D[\mathbf a; \mathbf b] = \mathbf a^\top\boldsymbol\Sigma_x\mathbf a + \mathbf b^\top\boldsymbol\Sigma_v\mathbf b > 0$ unless $\mathbf a$ and $\mathbf b$ are both $\mathbf 0$, and multiplying block by block shows that its inverse is block diagonal with blocks $\boldsymbol\Sigma_x^{-1}$ and $\boldsymbol\Sigma_v^{-1}$. So the product of the two densities is a constant times
    $$\exp\Big(-\tfrac12\big[(\mathbf x - \boldsymbol\mu_x)^\top\boldsymbol\Sigma_x^{-1}(\mathbf x - \boldsymbol\mu_x) + (\mathbf v - \boldsymbol\mu_v)^\top\boldsymbol\Sigma_v^{-1}(\mathbf v - \boldsymbol\mu_v)\big]\Big) = \exp\Big(-\tfrac12\,\mathbf d^\top\mathbf D^{-1}\mathbf d\Big),$$
    with $\mathbf d$ the stacked deviation from the stacked mean. Apply the normalization lemma. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch12-sec-mahalanobis-distance-and-confidence-ellipses -->
    ## Mahalanobis Distance and Confidence Ellipses

    How far is a point from the center of a multivariate normal distribution? Plain distance is the wrong measure: a deviation of 2 lb is ordinary along a direction with a standard deviation of 5 lb and extraordinary along one with 0.1 lb. The right measure counts standard deviations, direction by direction.

    /// note | 📖 **Definition**
    <u>**Mahalanobis distance**</u>

    For $\boldsymbol\mu \in \mathbb R^n$ and a positive definite $\boldsymbol\Sigma \in \mathbb R^{n\times n}$, the Mahalanobis distance of $\mathbf x \in \mathbb R^n$ from $\boldsymbol\mu$ with respect to $\boldsymbol\Sigma$ is
    $$d_{\boldsymbol\Sigma}(\mathbf x, \boldsymbol\mu) := \sqrt{(\mathbf x - \boldsymbol\mu)^\top\boldsymbol\Sigma^{-1}(\mathbf x - \boldsymbol\mu)}.$$
    ///

    The square root is of a nonnegative number because $\boldsymbol\Sigma^{-1}$ is positive definite. For $n = 1$ it is $|x - \mu|/\sigma$, the number of standard deviations. In general, with the Cholesky factor $\boldsymbol\Sigma = \mathbf L\mathbf L^\top$ and $\mathbf y := \mathbf L^{-1}(\mathbf x - \boldsymbol\mu)$, we have $d_{\boldsymbol\Sigma}(\mathbf x, \boldsymbol\mu)^2 = \mathbf y^\top\mathbf y$: the Mahalanobis distance is the ordinary length after transforming to coordinates in which the distribution is standard normal.

    /// admonition | 📐 **Theorem (Squared Mahalanobis Distance Is Chi-Squared)**
        attrs: {class: theorem, id: ch12-thm-squared-mahalanobis-distance-is-chi-squared}
    If $\mathbf x \sim \mathcal N(\boldsymbol\mu, \boldsymbol\Sigma)$ in $\mathbb R^n$, then $d_{\boldsymbol\Sigma}(\mathbf x, \boldsymbol\mu)^2$ has the {term}`chi-squared distribution` with $n$ degrees of freedom, the distribution of a sum of squares of $n$ independent standard normal random variables.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    By the invertible-affine-map theorem, $\mathbf y := \mathbf L^{-1}(\mathbf x - \boldsymbol\mu) \sim \mathcal N\big(\mathbf 0, \mathbf L^{-1}\boldsymbol\Sigma(\mathbf L^{-1})^\top\big) = \mathcal N(\mathbf 0, \mathbf I)$. The $\mathcal N(\mathbf 0, \mathbf I)$ density is the product of $n$ standard normal densities, so $y_1, \ldots, y_n$ are independent standard normal random variables ([Chapter 5](#ch5-thm-factorization-criteria)). And $d_{\boldsymbol\Sigma}(\mathbf x, \boldsymbol\mu)^2 = (\mathbf x - \boldsymbol\mu)^\top(\mathbf L^{-1})^\top\mathbf L^{-1}(\mathbf x - \boldsymbol\mu) = \mathbf y^\top\mathbf y = \sum_{i=1}^n y_i^2$. $\blacksquare$
    ///

    For $n = 1$ this is [Chapter 9](#ch9-sec-checking-the-noise-levels)'s normalized innovation squared, $\tilde y_k^2/S_k$. In two dimensions the distribution has a simple closed form.

    /// admonition | 📐 **Theorem (Two Dimensions)**
        attrs: {class: theorem, id: ch12-thm-two-dimensions}
    If $\mathbf x \sim \mathcal N(\boldsymbol\mu, \boldsymbol\Sigma)$ in $\mathbb R^2$, then for every $r \ge 0$
    $$\mathbb P\big(d_{\boldsymbol\Sigma}(\mathbf x, \boldsymbol\mu) \le r\big) = 1 - e^{-r^2/2}.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    With $\mathbf y$ as in the previous proof, the probability is the integral of the $\mathcal N(\mathbf 0, \mathbf I)$ density over the disk $y_1^2 + y_2^2 \le r^2$. In polar coordinates $y_1 = s\cos\theta$, $y_2 = s\sin\theta$, whose area element is $s\,ds\,d\theta$ ([Appendix C: Multiple Integrals](#appc-sec-multiple-integrals)),
    $$\int_0^{2\pi}\!\!\int_0^r \frac{1}{2\pi}e^{-s^2/2}\,s\,ds\,d\theta = \int_0^r s\,e^{-s^2/2}\,ds = \Big[-e^{-s^2/2}\Big]_0^r = 1 - e^{-r^2/2},$$
    using the fundamental theorem of calculus ([Appendix C: The Fundamental Theorem of Calculus](#appc-sec-the-fundamental-theorem-of-calculus)). $\blacksquare$
    ///

    So the probability $p$ is captured within Mahalanobis distance $r_p := \sqrt{-2\ln(1 - p)}$. Two surprises for anyone used to one dimension: within one "standard deviation" ($r = 1$) lies only $1 - e^{-1/2} \approx 39\%$ of the probability, not $68\%$; within $r = 2$, about $86\%$; and 95% needs $r_{0.95} = \sqrt{-2\ln 0.05} \approx 2.45$.

    /// note | 📖 **Definition**
    <u>**Confidence ellipse**</u>

    For $\mathbf x \sim \mathcal N(\boldsymbol\mu, \boldsymbol\Sigma)$ in $\mathbb R^2$ and a probability $p \in (0, 1)$, the $p$ confidence ellipse is the set
    $$E_p := \big\{\mathbf x \in \mathbb R^2 : d_{\boldsymbol\Sigma}(\mathbf x, \boldsymbol\mu)^2 \le -2\ln(1 - p)\big\},$$
    where $d_{\boldsymbol\Sigma}$ is the {term}`Mahalanobis distance`.
    ///

    By the two-dimensional theorem above, $\mathbb P(\mathbf x \in E_p) = p$ exactly. In $n$ dimensions the same construction, with the chi-squared quantile in place of $-2\ln(1-p)$, gives a confidence *ellipsoid*. Statisticians reserve "confidence region" for a region that covers an unknown fixed parameter with a given frequency; the regions here describe where a random vector lies and are also called *probability* or *error ellipses*. In filtering, the random vector is the state given the data, and the ellipse is where the state lies with probability $p$, according to the filter.

    Why an ellipse? Because it is the smallest region with probability $p$, and because its shape is easy to compute.

    /// admonition | 📐 **Theorem (Shape and Optimality of the Confidence Ellipse)**
        attrs: {class: theorem, id: ch12-thm-shape-and-optimality-of-the-confidence-ellipse}
    Let $\boldsymbol\Sigma = \mathbf Q\boldsymbol\Lambda\mathbf Q^\top$ with $\mathbf Q = [\mathbf q_1\ \mathbf q_2]$ orthogonal and $\boldsymbol\Lambda = \operatorname{diag}(\lambda_1, \lambda_2)$ (spectral theorem), and let $r_p := \sqrt{-2\ln(1-p)}$.

    1. $\lambda_1, \lambda_2 > 0$, and in the rotated coordinates $\mathbf u := \mathbf Q^\top(\mathbf x - \boldsymbol\mu)$,
    $$E_p = \Big\{\boldsymbol\mu + \mathbf Q\mathbf u : \frac{u_1^2}{\lambda_1} + \frac{u_2^2}{\lambda_2} \le r_p^2\Big\}.$$
    So $E_p$ is an ellipse centered at $\boldsymbol\mu$ whose semi-axes point along the eigenvectors $\mathbf q_i$ and have lengths $r_p\sqrt{\lambda_i}$.
    2. Every region $B \subseteq \mathbb R^2$ with $\mathbb P(\mathbf x \in B) = p$ has at least the area of $E_p$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    1. Since $\boldsymbol\Sigma\mathbf q_i = \lambda_i\mathbf q_i$ and $\mathbf q_i^\top\mathbf q_i = 1$, we get $\lambda_i = \mathbf q_i^\top\boldsymbol\Sigma\mathbf q_i > 0$. Next, $\boldsymbol\Sigma^{-1} = \mathbf Q\boldsymbol\Lambda^{-1}\mathbf Q^\top$, because $\mathbf Q\boldsymbol\Lambda\mathbf Q^\top\mathbf Q\boldsymbol\Lambda^{-1}\mathbf Q^\top = \mathbf Q\mathbf Q^\top = \mathbf I$. Hence $(\mathbf x - \boldsymbol\mu)^\top\boldsymbol\Sigma^{-1}(\mathbf x - \boldsymbol\mu) = \mathbf u^\top\boldsymbol\Lambda^{-1}\mathbf u = u_1^2/\lambda_1 + u_2^2/\lambda_2$, and $\mathbf x = \boldsymbol\mu + \mathbf Q\mathbf u$. The map $\mathbf u \mapsto \boldsymbol\mu + \mathbf Q\mathbf u$ preserves lengths and angles (it is a rotation, possibly with a reflection, followed by a shift), so it carries the axis-aligned ellipse onto $E_p$ with the coordinate axes going to the directions $\mathbf q_i$.
    2. The density $f$ of $\mathbf x$ is a decreasing function of $d_{\boldsymbol\Sigma}(\mathbf x, \boldsymbol\mu)$, so with $t := (2\pi)^{-1}(\det\boldsymbol\Sigma)^{-1/2}e^{-r_p^2/2} > 0$ we have $f \ge t$ on $E_p$ and $f < t$ outside it. If $B$ has infinite area there is nothing to prove. Otherwise
    $$0 = \mathbb P(\mathbf x \in B) - \mathbb P(\mathbf x \in E_p) = \int_{B\setminus E_p} f - \int_{E_p\setminus B} f \le t\,\big(\operatorname{area}(B\setminus E_p) - \operatorname{area}(E_p\setminus B)\big) = t\,\big(\operatorname{area}(B) - \operatorname{area}(E_p)\big),$$
    so $\operatorname{area}(B) \ge \operatorname{area}(E_p)$. $\blacksquare$
    ///

    In code, part 1 gives the boundary directly: points $\boldsymbol\mu + \mathbf Q\,[r_p\sqrt{\lambda_1}\cos\theta,\ r_p\sqrt{\lambda_2}\sin\theta]^\top$ for $\theta \in [0, 2\pi]$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ```python
    def confidence_ellipse(mu, Sigma, p, n_points=200):
        "\"\"Boundary of the p confidence ellipse of N(mu, Sigma) in 2-D (2 x n_points)."\"\"
        r = np.sqrt(-2 * np.log(1 - p))        # Mahalanobis radius
        lam, Q = np.linalg.eigh(Sigma)         # Sigma = Q diag(lam) Q^T
        theta = np.linspace(0, 2 * np.pi, n_points)
        u = r * np.sqrt(lam)[:, None] * np.vstack([np.cos(theta), np.sin(theta)])
        return np.asarray(mu, dtype=float)[:, None] + Q @ u
    ```
    """)
    return


@app.cell
def _(np):
    # jb: include=false
    def confidence_ellipse(mu, Sigma, p, n_points=200):
        """Boundary of the p confidence ellipse of N(mu, Sigma) in 2-D (2 x n_points)."""
        r = np.sqrt(-2 * np.log(1 - p))        # Mahalanobis radius
        lam, Q = np.linalg.eigh(Sigma)         # Sigma = Q diag(lam) Q^T
        theta = np.linspace(0, 2 * np.pi, n_points)
        u = r * np.sqrt(lam)[:, None] * np.vstack([np.cos(theta), np.sin(theta)])
        return np.asarray(mu, dtype=float)[:, None] + Q @ u

    return (confidence_ellipse,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Explore the ellipse below. The cloud shows 1000 samples drawn as $\mathbf L\mathbf y + \boldsymbol\mu$; the black segments are the semi-axes $r_p\sqrt{\lambda_i}\,\mathbf q_i$. With $\rho = 0$ the axes are horizontal and vertical with lengths $r_p\sigma_x$ and $r_p\sigma_y$. With $\sigma_x = \sigma_y$ and $\rho \ne 0$ they lie along the diagonals. As $|\rho| \to 1$ the ellipse collapses toward a line segment, the covariance matrix approaches a singular one, and one combination of the two components becomes almost constant.
    """)
    return


@app.cell(hide_code=True)
def _(mo, np):
    ell_sx = mo.ui.slider(0.5, 3.0, step=0.1, value=2.0, show_value=True, label=r"$\sigma_x$")
    ell_sy = mo.ui.slider(0.5, 3.0, step=0.1, value=1.0, show_value=True, label=r"$\sigma_y$")
    ell_rho = mo.ui.slider(-0.95, 0.95, step=0.05, value=0.6, show_value=True, label=r"$\rho$")
    ell_p = mo.ui.dropdown(
        options={"39% (r = 1)": float(1 - np.exp(-0.5)),
                 "86% (r = 2)": float(1 - np.exp(-2.0)),
                 "95%": 0.95, "99%": 0.99},
        value="95%", label="Probability $p$",
    )
    return ell_p, ell_rho, ell_sx, ell_sy


@app.cell
def _(np):
    # jb: include=false
    ellipse_draws = np.random.default_rng(4).standard_normal((2, 1000))
    return (ellipse_draws,)


@app.cell(hide_code=True)
def _(
    confidence_ellipse,
    ell_p,
    ell_rho,
    ell_sx,
    ell_sy,
    ellipse_draws,
    graphic,
    mo,
    np,
    plt,
):
    _sx, _sy, _rho, _p = ell_sx.value, ell_sy.value, ell_rho.value, ell_p.value
    _Sigma = np.array([[_sx**2, _rho * _sx * _sy], [_rho * _sx * _sy, _sy**2]])
    _L = np.linalg.cholesky(_Sigma)
    _pts = _L @ ellipse_draws
    _r2 = -2 * np.log(1 - _p)
    _d2 = np.sum(np.linalg.solve(_L, _pts) ** 2, axis=0)
    _frac = np.mean(_d2 <= _r2)
    _lam, _Q = np.linalg.eigh(_Sigma)
    _bdry = confidence_ellipse([0.0, 0.0], _Sigma, _p)

    _fig, _ax = plt.subplots(figsize=(6, 6))
    _inside = _d2 <= _r2
    _ax.plot(_pts[0, _inside], _pts[1, _inside], ".", color="C0", ms=3, alpha=0.6, label="samples inside")
    _ax.plot(_pts[0, ~_inside], _pts[1, ~_inside], ".", color="gray", ms=3, alpha=0.6, label="samples outside")
    _ax.plot(_bdry[0], _bdry[1], color="C1", lw=2, label=f"{_p:.0%} confidence ellipse")
    for _i in range(2):
        _v = np.sqrt(_r2 * _lam[_i]) * _Q[:, _i]
        _ax.plot([0, _v[0]], [0, _v[1]], color="black", lw=1.5)
    _ax.set_aspect("equal")
    _ax.set_xlim(-9, 9)
    _ax.set_ylim(-9, 9)
    _ax.set_xlabel("$x_1$")
    _ax.set_ylabel("$x_2$")
    _ax.set_title("Samples from $\\mathcal{N}(\\mathbf{0}, \\boldsymbol{\\Sigma})$ and a confidence ellipse", style="italic")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.legend(fontsize=8, loc="upper left")
    _fig.tight_layout()

    _text = mo.md(
        f"Fraction of the 1000 samples inside the ellipse: **{_frac:.1%}** (theory: {_p:.1%}). "
        f"Eigenvalues $\\lambda_1 = {_lam[0]:.2f}$, $\\lambda_2 = {_lam[1]:.2f}$; "
        f"semi-axes $r_p\\sqrt{{\\lambda_i}} = {np.sqrt(_r2 * _lam[0]):.2f}$ and {np.sqrt(_r2 * _lam[1]):.2f}."
    )
    mo.vstack([mo.hstack([ell_sx, ell_sy, ell_rho, ell_p], justify="start", gap=1.5), graphic(_fig), _text])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **Normality.** The probability $1 - e^{-r^2/2}$ and the chi-squared law hold for normal vectors. For other distributions with the same covariance, the ellipse still has the same shape, but the probability inside it can be quite different (heavy tails put more mass outside).
    - **The dimension matters.** In $n$ dimensions the radius for probability $p$ is the square root of the chi-squared quantile with $n$ degrees of freedom, which grows with $n$. Using the two-dimensional radius for a higher-dimensional state undercovers.
    - **Estimated covariances.** An ellipse drawn from a covariance matrix that was itself estimated, or computed by a mis-tuned filter, inherits those errors. Checking whether true errors actually fall inside the filter's ellipses at the advertised rate is the consistency test of [Chapter 14](#ch14-sec-consistency-tests).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch12-sec-marginals-and-conditioning -->
    ## Marginals and Conditioning

    Now split a jointly normal vector into two parts: $\mathbf x \in \mathbb R^n$, which we want to know, and $\mathbf z \in \mathbb R^m$, which we will observe. Write
    $$\begin{bmatrix}\mathbf x\\ \mathbf z\end{bmatrix} \sim \mathcal N\left(\begin{bmatrix}\boldsymbol\mu_x\\ \boldsymbol\mu_z\end{bmatrix}, \boldsymbol\Sigma\right), \qquad \boldsymbol\Sigma = \begin{bmatrix}\boldsymbol\Sigma_{xx} & \boldsymbol\Sigma_{xz}\\ \boldsymbol\Sigma_{zx} & \boldsymbol\Sigma_{zz}\end{bmatrix},$$
    with $\boldsymbol\Sigma$ positive definite, $\boldsymbol\Sigma_{xz} = \operatorname{Cov}(\mathbf x, \mathbf z)$, and $\boldsymbol\Sigma_{zx} = \boldsymbol\Sigma_{xz}^\top$. Two questions: what is the distribution of $\mathbf z$ alone, and what is the distribution of $\mathbf x$ once we know $\mathbf z$? Both answers come from rewriting the quadratic form in the exponent, which is completing the square with matrices.

    /// admonition | 📐 **Lemma (Completing the Square with a Schur Complement)**
        attrs: {class: lemma, id: ch12-lem-completing-the-square-with-a-schur-complement}
    With $\boldsymbol\Sigma$ as above:

    1. $\boldsymbol\Sigma_{zz}$ is positive definite, hence invertible;
    2. with $\mathbf G := \boldsymbol\Sigma_{xz}\boldsymbol\Sigma_{zz}^{-1}$, the {term}`Schur complement` $\boldsymbol\Sigma_{x\mid z} := \boldsymbol\Sigma_{xx} - \boldsymbol\Sigma_{xz}\boldsymbol\Sigma_{zz}^{-1}\boldsymbol\Sigma_{zx}$ of $\boldsymbol\Sigma_{zz}$ in $\boldsymbol\Sigma$ is positive definite;
    3. for all $\mathbf d_x \in \mathbb R^n$ and $\mathbf d_z \in \mathbb R^m$,
    $$\begin{bmatrix}\mathbf d_x\\ \mathbf d_z\end{bmatrix}^\top\boldsymbol\Sigma^{-1}\begin{bmatrix}\mathbf d_x\\ \mathbf d_z\end{bmatrix} = (\mathbf d_x - \mathbf G\mathbf d_z)^\top\boldsymbol\Sigma_{x\mid z}^{-1}(\mathbf d_x - \mathbf G\mathbf d_z) + \mathbf d_z^\top\boldsymbol\Sigma_{zz}^{-1}\mathbf d_z.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    1. For $\mathbf a \neq \mathbf 0$, $\mathbf a^\top\boldsymbol\Sigma_{zz}\mathbf a = [\mathbf 0; \mathbf a]^\top\boldsymbol\Sigma\,[\mathbf 0; \mathbf a] > 0$.

    2. Let $\mathbf T := \begin{bmatrix}\mathbf I & -\mathbf G\\ \mathbf 0 & \mathbf I\end{bmatrix}$. Multiplying block by block and using $\mathbf G\boldsymbol\Sigma_{zz} = \boldsymbol\Sigma_{xz}$,
    $$\mathbf T\boldsymbol\Sigma = \begin{bmatrix}\boldsymbol\Sigma_{xx} - \mathbf G\boldsymbol\Sigma_{zx} & \boldsymbol\Sigma_{xz} - \mathbf G\boldsymbol\Sigma_{zz}\\ \boldsymbol\Sigma_{zx} & \boldsymbol\Sigma_{zz}\end{bmatrix} = \begin{bmatrix}\boldsymbol\Sigma_{x\mid z} & \mathbf 0\\ \boldsymbol\Sigma_{zx} & \boldsymbol\Sigma_{zz}\end{bmatrix}.$$
    Since $\boldsymbol\Sigma_{zz}^{-1}$ is symmetric, $\mathbf G^\top = \boldsymbol\Sigma_{zz}^{-1}\boldsymbol\Sigma_{zx}$, so $\boldsymbol\Sigma_{zz}\mathbf G^\top = \boldsymbol\Sigma_{zx}$. Multiplying on the right by $\mathbf T^\top = \begin{bmatrix}\mathbf I & \mathbf 0\\ -\mathbf G^\top & \mathbf I\end{bmatrix}$ therefore gives
    $$\mathbf T\boldsymbol\Sigma\mathbf T^\top = \begin{bmatrix}\boldsymbol\Sigma_{x\mid z} & \mathbf 0\\ \boldsymbol\Sigma_{zx} - \boldsymbol\Sigma_{zz}\mathbf G^\top & \boldsymbol\Sigma_{zz}\end{bmatrix} = \begin{bmatrix}\boldsymbol\Sigma_{x\mid z} & \mathbf 0\\ \mathbf 0 & \boldsymbol\Sigma_{zz}\end{bmatrix} =: \mathbf D.$$
    $\mathbf T$ is invertible, with $\mathbf T^{-1} = \begin{bmatrix}\mathbf I & \mathbf G\\ \mathbf 0 & \mathbf I\end{bmatrix}$ (multiply to check), so $\mathbf D$ is positive definite by the [Positive Definite Matrices lemma](#ch12-lem-positive-definite-matrices), and so is its block $\boldsymbol\Sigma_{x\mid z}$ (test $\mathbf D$ with vectors $[\mathbf a; \mathbf 0]$).

    3. From $\mathbf T\boldsymbol\Sigma\mathbf T^\top = \mathbf D$ we get $\boldsymbol\Sigma = \mathbf T^{-1}\mathbf D(\mathbf T^\top)^{-1}$ and so $\boldsymbol\Sigma^{-1} = \mathbf T^\top\mathbf D^{-1}\mathbf T$, where $\mathbf D^{-1}$ is block diagonal with blocks $\boldsymbol\Sigma_{x\mid z}^{-1}$ and $\boldsymbol\Sigma_{zz}^{-1}$. With $\mathbf d := [\mathbf d_x; \mathbf d_z]$, $\mathbf d^\top\boldsymbol\Sigma^{-1}\mathbf d = (\mathbf T\mathbf d)^\top\mathbf D^{-1}(\mathbf T\mathbf d)$ and $\mathbf T\mathbf d = [\mathbf d_x - \mathbf G\mathbf d_z;\ \mathbf d_z]$. Expanding block by block gives the claim. $\blacksquare$
    ///

    For scalars ($n = m = 1$) the identity is the familiar completion of the square of a quadratic in two variables; for matrices, the Schur complement plays the role of "what is left over".
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Throughout, write $\mathbf d_x := \mathbf x - \boldsymbol\mu_x$, $\mathbf d_z := \mathbf z - \boldsymbol\mu_z$, and
    $$\mathbf m(\mathbf z) := \boldsymbol\mu_x + \mathbf G(\mathbf z - \boldsymbol\mu_z), \qquad \kappa_{x\mid z} := (2\pi)^{-n/2}\big(\det\boldsymbol\Sigma_{x\mid z}\big)^{-1/2}.$$
    By the [Completing the Square with a Schur Complement lemma](#ch12-lem-completing-the-square-with-a-schur-complement), $\mathbf d_x - \mathbf G\mathbf d_z = \mathbf x - \mathbf m(\mathbf z)$, so the joint density factors as
    $$f(\mathbf x, \mathbf z) = \kappa\,\exp\Big(-\tfrac12\,\mathbf d_z^\top\boldsymbol\Sigma_{zz}^{-1}\mathbf d_z\Big)\,\exp\Big(-\tfrac12\big(\mathbf x - \mathbf m(\mathbf z)\big)^\top\boldsymbol\Sigma_{x\mid z}^{-1}\big(\mathbf x - \mathbf m(\mathbf z)\big)\Big), \qquad (\ast)$$
    where $\kappa$ is the constant of the joint density.

    /// admonition | 📐 **Theorem (Marginals of a Multivariate Normal)**
        attrs: {class: theorem, id: ch12-thm-marginals-of-a-multivariate-normal}
    $\mathbf z \sim \mathcal N(\boldsymbol\mu_z, \boldsymbol\Sigma_{zz})$ and $\mathbf x \sim \mathcal N(\boldsymbol\mu_x, \boldsymbol\Sigma_{xx})$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    The marginal density of $\mathbf z$ is $f_{\mathbf z}(\mathbf z) = \int_{\mathbb R^n} f(\mathbf x, \mathbf z)\,d\mathbf x$ ([Chapter 5](#ch5-thm-the-marginal-density-is-a-density), with $n$ variables integrated out). In $(\ast)$, for fixed $\mathbf z$ the last factor is $1/\kappa_{x\mid z}$ times the $\mathcal N(\mathbf m(\mathbf z), \boldsymbol\Sigma_{x\mid z})$ density in $\mathbf x$, so its integral over $\mathbf x$ is $1/\kappa_{x\mid z}$, whatever $\mathbf z$ is. Hence
    $$f_{\mathbf z}(\mathbf z) = \frac{\kappa}{\kappa_{x\mid z}}\exp\Big(-\tfrac12(\mathbf z - \boldsymbol\mu_z)^\top\boldsymbol\Sigma_{zz}^{-1}(\mathbf z - \boldsymbol\mu_z)\Big),$$
    and the normalization lemma gives $\mathbf z \sim \mathcal N(\boldsymbol\mu_z, \boldsymbol\Sigma_{zz})$. For $\mathbf x$, note that $[\mathbf z; \mathbf x]$ is obtained from $[\mathbf x; \mathbf z]$ by an invertible linear map (a reordering of components), so it is normal with mean $[\boldsymbol\mu_z; \boldsymbol\mu_x]$ and the blocks of $\boldsymbol\Sigma$ rearranged accordingly; apply the first part with the roles exchanged. $\blacksquare$
    ///

    /// admonition | 📐 **Corollary (Uncorrelated Jointly Normal Vectors Are Independent)**
        attrs: {class: corollary, id: ch12-cor-uncorrelated-jointly-normal-vectors-are-independent}
    If $\mathbf x$ and $\mathbf z$ are jointly normal and $\operatorname{Cov}(\mathbf x, \mathbf z) = \mathbf 0$, then $\mathbf x$ and $\mathbf z$ are independent: their joint density is the product of their marginal densities.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    With $\boldsymbol\Sigma_{xz} = \mathbf 0$ we have $\mathbf G = \mathbf 0$, $\mathbf m(\mathbf z) = \boldsymbol\mu_x$, and $\boldsymbol\Sigma_{x\mid z} = \boldsymbol\Sigma_{xx}$, so by $(\ast)$ the joint density is a constant times the product of the exponentials of the $\mathcal N(\boldsymbol\mu_z, \boldsymbol\Sigma_{zz})$ and $\mathcal N(\boldsymbol\mu_x, \boldsymbol\Sigma_{xx})$ densities. By the theorem these are the marginal densities, so $f(\mathbf x, \mathbf z) = c\,f_{\mathbf x}(\mathbf x)f_{\mathbf z}(\mathbf z)$ for a constant $c$; integrating both sides over $\mathbb R^{n+m}$ gives $c = 1$. $\blacksquare$
    ///

    Chapter 6 showed that uncorrelated random variables need not be independent. For *jointly* normal ones they must be.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now the main result. The {term}`conditional density` of $\mathbf x$ given $\mathbf z = \mathbf z$ is $f(\mathbf x, \mathbf z)/f_{\mathbf z}(\mathbf z)$, exactly as in [Chapter 8](#ch8-sec-conditional-densities) but with joint densities of vectors.

    /// admonition | 📐 **Theorem (Conditioning a Joint Normal Distribution)**
        attrs: {class: theorem, id: ch12-thm-conditioning-a-joint-normal-distribution}
    For every $\mathbf z \in \mathbb R^m$, the conditional distribution of $\mathbf x$ given $\mathbf z = \mathbf z$ is
    $$\mathcal N\Big(\boldsymbol\mu_x + \boldsymbol\Sigma_{xz}\boldsymbol\Sigma_{zz}^{-1}(\mathbf z - \boldsymbol\mu_z),\ \ \boldsymbol\Sigma_{xx} - \boldsymbol\Sigma_{xz}\boldsymbol\Sigma_{zz}^{-1}\boldsymbol\Sigma_{zx}\Big).$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Divide $(\ast)$ by the formula for $f_{\mathbf z}$ in the proof of the marginal theorem. The factors depending only on $\mathbf z$ cancel, leaving
    $$\frac{f(\mathbf x, \mathbf z)}{f_{\mathbf z}(\mathbf z)} = \kappa_{x\mid z}\exp\Big(-\tfrac12\big(\mathbf x - \mathbf m(\mathbf z)\big)^\top\boldsymbol\Sigma_{x\mid z}^{-1}\big(\mathbf x - \mathbf m(\mathbf z)\big)\Big),$$
    which is the $\mathcal N(\mathbf m(\mathbf z), \boldsymbol\Sigma_{x\mid z})$ density, and $\mathbf m(\mathbf z) = \boldsymbol\mu_x + \boldsymbol\Sigma_{xz}\boldsymbol\Sigma_{zz}^{-1}(\mathbf z - \boldsymbol\mu_z)$. $\blacksquare$
    ///

    Read the formula as a recipe:

    - **Mean:** start from the old mean $\boldsymbol\mu_x$ and add a matrix $\mathbf G = \boldsymbol\Sigma_{xz}\boldsymbol\Sigma_{zz}^{-1}$ times the *surprise* $\mathbf z - \boldsymbol\mu_z$. Components of $\mathbf x$ that are uncorrelated with $\mathbf z$ do not move.
    - **Covariance:** subtract $\boldsymbol\Sigma_{xz}\boldsymbol\Sigma_{zz}^{-1}\boldsymbol\Sigma_{zx}$, which is positive semidefinite ($\mathbf a^\top\boldsymbol\Sigma_{xz}\boldsymbol\Sigma_{zz}^{-1}\boldsymbol\Sigma_{zx}\mathbf a = (\boldsymbol\Sigma_{zx}\mathbf a)^\top\boldsymbol\Sigma_{zz}^{-1}(\boldsymbol\Sigma_{zx}\mathbf a) \ge 0$). So observing $\mathbf z$ never increases the variance of any linear combination of $\mathbf x$. Remarkably, the new covariance does not depend on the observed value $\mathbf z$ at all, so it can be computed before any data arrive.
    - **Scalars:** for $n = m = 1$ with standard deviations $\sigma_x, \sigma_z$ and correlation $\rho$, the conditional mean is $\mu_x + \rho\,\frac{\sigma_x}{\sigma_z}(z - \mu_z)$ and the conditional variance is $\sigma_x^2(1 - \rho^2)$.

    Geometrically, conditioning is slicing: fix $z$, cut the joint density along that line, and rescale the slice to integrate to $1$. The figure shows this for a weight $x \sim \mathcal N(155, 4)$ and a reading $z = x + v$ with independent $v \sim \mathcal N(0, 1)$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch12_conditioning_slice.svg" class="graphic" alt="Left: confidence ellipses of the joint distribution of a weight x and a reading z, with the horizontal line z = 157 and the line of conditional means. Right: the prior density of x, centered at 155, and the much narrower conditional density given z = 157, centered at 156.6." />
    """)
    return


@app.cell
def _(IMAGES_DIR, np, plt):
    # jb: include=false
    _mu = np.array([155.0, 155.0])
    _S = np.array([[4.0, 4.0], [4.0, 5.0]])
    _z_obs = 157.0
    _m = _mu[0] + _S[0, 1] / _S[1, 1] * (_z_obs - _mu[1])
    _v = _S[0, 0] - _S[0, 1] ** 2 / _S[1, 1]
    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    _lam, _Q = np.linalg.eigh(_S)
    _th = np.linspace(0, 2 * np.pi, 200)
    for _p, _ls in [(0.39, ":"), (0.86, "--"), (0.99, "-")]:
        _r = np.sqrt(-2 * np.log(1 - _p))
        _b = _mu[:, None] + _Q @ (_r * np.sqrt(_lam)[:, None] * np.vstack([np.cos(_th), np.sin(_th)]))
        _ax1.plot(_b[0], _b[1], color="C0", ls=_ls, lw=1.2, label=f"{_p:.0%} ellipse of $(x, z)$")
    _zs = np.linspace(147, 163, 2)
    _ax1.plot(_mu[0] + _S[0, 1] / _S[1, 1] * (_zs - _mu[1]), _zs, color="C1", lw=1.5, label=r"conditional mean $m(z)$")
    _ax1.axhline(_z_obs, color="black", lw=1, label=f"observed $z = {_z_obs:.0f}$")
    _ax1.plot([_m], [_z_obs], "o", color="C1")
    _ax1.set_xlim(147, 163)
    _ax1.set_ylim(147, 163)
    _ax1.set_aspect("equal")
    _ax1.set_xlabel("Weight $x$ (lb)")
    _ax1.set_ylabel("Reading $z$ (lb)")
    _ax1.set_title("Joint distribution of weight and reading", style="italic")
    _ax1.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax1.legend(fontsize=8, loc="upper left")
    _xs = np.linspace(147, 163, 400)
    _ax2.plot(_xs, np.exp(-0.5 * (_xs - _mu[0]) ** 2 / _S[0, 0]) / np.sqrt(2 * np.pi * _S[0, 0]), color="black", ls="--",
              label=r"before: $\mathcal{N}(155, 4)$")
    _ax2.plot(_xs, np.exp(-0.5 * (_xs - _m) ** 2 / _v) / np.sqrt(2 * np.pi * _v), color="C1", lw=2,
              label=rf"given $z = {_z_obs:.0f}$: $\mathcal{{N}}({_m:.1f}, {_v:.1f})$")
    _ax2.axvline(_z_obs, color="gray", lw=0.8, ls=":")
    _ax2.set_xlabel("Weight $x$ (lb)")
    _ax2.set_ylabel("Density (1/lb)")
    _ax2.set_title("Conditioning is slicing", style="italic")
    _ax2.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax2.legend(fontsize=8, loc="upper left")
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch12_conditioning_slice.svg")
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here $\operatorname{Cov}(x, z) = \operatorname{Var}(x) = 4$ and $\operatorname{Var}(z) = 4 + 1 = 5$, so the reading $z = 157$ moves the mean by $\tfrac45 \cdot 2 = 1.6$ lb to $156.6$ lb and shrinks the variance from $4$ to $4 - \tfrac{16}{5} = 0.8$ lb$^2$. That is precisely Chapter 7's update with gain $4/5$.

    The conditional mean also has a meaning that does not depend on normality: it is the best *linear* estimate for any distribution with these means and covariances. For jointly normal vectors it is moreover the conditional expectation $\mathbb E[\mathbf x \mid \mathbf z]$, which [Chapter 8](#ch8-thm-the-posterior-mean-is-the-mmse-estimator) showed is the best estimate of all.

    /// admonition | 📐 **Theorem (Best Linear Estimator)**
        attrs: {class: theorem, id: ch12-thm-best-linear-estimator}
    Let $\mathbf x, \mathbf z$ be random vectors (not necessarily normal) with finite variances, means $\boldsymbol\mu_x, \boldsymbol\mu_z$, covariances $\boldsymbol\Sigma_{xx}, \boldsymbol\Sigma_{xz}, \boldsymbol\Sigma_{zz}$, and $\boldsymbol\Sigma_{zz}$ positive definite. For every matrix $\mathbf A \in \mathbb R^{n\times m}$ and vector $\mathbf b \in \mathbb R^n$, the error $\mathbf e := \mathbf x - (\mathbf A\mathbf z + \mathbf b)$ satisfies
    $$\mathbb E[\mathbf e\mathbf e^\top] = \boldsymbol\Sigma_{x\mid z} + (\mathbf G - \mathbf A)\boldsymbol\Sigma_{zz}(\mathbf G - \mathbf A)^\top + \mathbf c\,\mathbf c^\top, \qquad \mathbf c := \boldsymbol\mu_x - \mathbf A\boldsymbol\mu_z - \mathbf b.$$
    Hence every component's mean squared error $\mathbb E[e_i^2]$ is at least the $i$-th diagonal entry of $\boldsymbol\Sigma_{x\mid z}$, with equality for all components iff $\mathbf A = \mathbf G$ and $\mathbf b = \boldsymbol\mu_x - \mathbf G\boldsymbol\mu_z$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Let $\mathbf e^* := \mathbf x - \boldsymbol\mu_x - \mathbf G(\mathbf z - \boldsymbol\mu_z)$. It has mean $\mathbf 0$, and by the cross-covariance rules
    $$\operatorname{Cov}(\mathbf e^*, \mathbf z) = \boldsymbol\Sigma_{xz} - \mathbf G\boldsymbol\Sigma_{zz} = \mathbf 0, \qquad \operatorname{Cov}(\mathbf e^*) = \boldsymbol\Sigma_{xx} - \mathbf G\boldsymbol\Sigma_{zx} - \boldsymbol\Sigma_{xz}\mathbf G^\top + \mathbf G\boldsymbol\Sigma_{zz}\mathbf G^\top = \boldsymbol\Sigma_{x\mid z},$$
    because $\mathbf G\boldsymbol\Sigma_{zz}\mathbf G^\top = \boldsymbol\Sigma_{xz}\mathbf G^\top = \boldsymbol\Sigma_{xz}\boldsymbol\Sigma_{zz}^{-1}\boldsymbol\Sigma_{zx} = \mathbf G\boldsymbol\Sigma_{zx}$. Rearranging, $\mathbf e = \mathbf e^* + \mathbf g$ with $\mathbf g := (\mathbf G - \mathbf A)(\mathbf z - \boldsymbol\mu_z) + \mathbf c$. The cross terms vanish: $\mathbb E[\mathbf e^*\mathbf g^\top] = \operatorname{Cov}(\mathbf e^*, \mathbf z)(\mathbf G - \mathbf A)^\top + \mathbb E[\mathbf e^*]\,\mathbf c^\top = \mathbf 0$. And $\mathbb E[\mathbf g\mathbf g^\top] = (\mathbf G - \mathbf A)\boldsymbol\Sigma_{zz}(\mathbf G - \mathbf A)^\top + \mathbf c\mathbf c^\top$, because $\mathbf z - \boldsymbol\mu_z$ has mean $\mathbf 0$. This proves the formula. Both added matrices are positive semidefinite, so their diagonal entries are $\ge 0$. They are all $0$ iff $\mathbf c = \mathbf 0$ and every row $\mathbf r$ of $\mathbf G - \mathbf A$ has $\mathbf r\boldsymbol\Sigma_{zz}\mathbf r^\top = 0$, that is, $\mathbf r = \mathbf 0$ since $\boldsymbol\Sigma_{zz}$ is positive definite. $\blacksquare$
    ///

    This is Chapter 7's "optimal among linear combinations", now for vectors: the conditioning formula is the best linear update whatever the distributions, and for jointly normal vectors it is the best update, linear or not.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **Joint normality, not just normal components.** Let $x \sim \mathcal N(0, 1)$ and let $s = \pm 1$ with probability $\tfrac12$ each, independent of $x$. Then $z := s\,x$ is also $\mathcal N(0, 1)$ and $\operatorname{Cov}(x, z) = \mathbb E[s]\,\mathbb E[x^2] = 0$, yet $|z| = |x|$, so they are far from independent. By the corollary, $[x; z]$ cannot be jointly normal. The conditioning theorem needs the *joint* distribution to be normal.
    - **Without normality** the formula still gives the best linear estimate, but it is no longer the conditional distribution. With outliers or multimodal errors the best nonlinear estimate can be much better ([Chapter 8](#ch8-sec-when-the-noise-is-not-normal)), and the reported covariance $\boldsymbol\Sigma_{x\mid z}$ no longer describes the actual spread given the observed value.
    - **The covariances must be right.** The update uses $\boldsymbol\Sigma_{xz}$ and $\boldsymbol\Sigma_{zz}$ as given. If they are wrong (a mis-tuned filter), the mean moves by the wrong amount and the reported covariance is wrong, even though the formula is applied perfectly.
    - **Numerics.** Computing $\boldsymbol\Sigma_{xx} - \boldsymbol\Sigma_{xz}\boldsymbol\Sigma_{zz}^{-1}\boldsymbol\Sigma_{zx}$ by subtraction can lose symmetry or positive definiteness through rounding when the result is much smaller than $\boldsymbol\Sigma_{xx}$. Chapter 13's Joseph form is the standard remedy.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch12-sec-the-kalman-update-in-disguise -->
    ## The Kalman Update in Disguise

    Now apply the conditioning theorem to filtering. Before a measurement, the filter's knowledge of the state $\mathbf x \in \mathbb R^n$ is a prediction $\hat{\mathbf x}^-$ with error covariance $\mathbf P^-$; in the language of [Chapter 8](#ch8-sec-prior-likelihood-posterior-and-evidence), the {term}`prior` is $\mathbf x \sim \mathcal N(\hat{\mathbf x}^-, \mathbf P^-)$, with $\mathbf P^-$ positive definite. The measurement is
    $$\mathbf z = \mathbf H\mathbf x + \mathbf v, \qquad \mathbf v \sim \mathcal N(\mathbf 0, \mathbf R)\ \text{independent of}\ \mathbf x,$$
    with a known matrix $\mathbf H \in \mathbb R^{m\times n}$ (the vector version of Chapter 11's linear measurement function; Chapter 13 calls it the {term}`measurement matrix`) and $\mathbf R$ positive definite.

    **The joint distribution.** By the stacking corollary, $[\mathbf x; \mathbf v]$ is normal with block-diagonal covariance. And
    $$\begin{bmatrix}\mathbf x\\ \mathbf z\end{bmatrix} = \begin{bmatrix}\mathbf I & \mathbf 0\\ \mathbf H & \mathbf I\end{bmatrix}\begin{bmatrix}\mathbf x\\ \mathbf v\end{bmatrix},$$
    where the matrix is invertible (its inverse has $-\mathbf H$ in place of $\mathbf H$). By the invertible-affine-map theorem, $[\mathbf x; \mathbf z]$ is jointly normal with mean $[\hat{\mathbf x}^-;\ \mathbf H\hat{\mathbf x}^-]$ and covariance
    $$\begin{bmatrix}\mathbf I & \mathbf 0\\ \mathbf H & \mathbf I\end{bmatrix}\begin{bmatrix}\mathbf P^- & \mathbf 0\\ \mathbf 0 & \mathbf R\end{bmatrix}\begin{bmatrix}\mathbf I & \mathbf H^\top\\ \mathbf 0 & \mathbf I\end{bmatrix} = \begin{bmatrix}\mathbf P^- & \mathbf P^-\mathbf H^\top\\ \mathbf H\mathbf P^- & \mathbf H\mathbf P^-\mathbf H^\top + \mathbf R\end{bmatrix}.$$

    **Conditioning.** Read off $\boldsymbol\Sigma_{xx} = \mathbf P^-$, $\boldsymbol\Sigma_{xz} = \mathbf P^-\mathbf H^\top$, and $\boldsymbol\Sigma_{zz} = \mathbf S := \mathbf H\mathbf P^-\mathbf H^\top + \mathbf R$, the covariance of the measurement. The conditioning theorem says that, given the measurement $\mathbf z$, the state is normal with
    $$\boxed{\ \hat{\mathbf x} = \hat{\mathbf x}^- + \mathbf K\,(\mathbf z - \mathbf H\hat{\mathbf x}^-), \qquad \mathbf P = \mathbf P^- - \mathbf K\mathbf H\mathbf P^- = (\mathbf I - \mathbf K\mathbf H)\,\mathbf P^-, \qquad \mathbf K := \mathbf P^-\mathbf H^\top\mathbf S^{-1}.\ }$$
    This is the Kalman filter's update step for vectors: prediction plus gain times {term}`innovation`, with the innovation $\mathbf z - \mathbf H\hat{\mathbf x}^-$ having covariance $\mathbf S$ (it is $\boldsymbol\Sigma_{zz}$, the covariance of $\mathbf z$ around its predicted value). For one state and one measurement, $\mathbf H = h$, it reads $K = P^-h/(h^2P^- + R)$, Chapter 11's gain, and for $h = 1$ it is Chapter 7's $P^-/(P^- + R)$. The covariance update, a Schur complement, is $P = (1 - Kh)P^-$.

    [Chapter 13](#ch13-sec-the-optimal-gain) derives the same gain without assuming normality, by minimizing the error variance over all gains, and adds the prediction step. The best-linear-estimator theorem above already tells us why the two derivations agree: the conditional mean of jointly normal vectors is the best linear update.

    **Example: weight and offset.** Return to Chapter 11's scale, with the offset converted to pounds using the calibrated sensitivity (so $c = 85{,}000/20{,}000 = 4.25$ lb nominally). The state is $\mathbf x = [x, c]^\top$ (weight, offset). Before anyone steps on, the filter believes $x \sim \mathcal N(150, 5^2)$ and, from the last tare, $c \sim \mathcal N(4.25, \sigma_c^2)$, independently, so $\mathbf P^- = \operatorname{diag}(25, \sigma_c^2)$. Actually, the person weighs 155 lb and the offset has drifted to $5.25$ lb. A 3-second standing measurement averages 30 readings, $z_1 = x + c + v_1$ with $\operatorname{Var}(v_1) = 1/30$ lb$^2$, so $\mathbf H = [1\ \ 1]$. An empty-platform measurement, also an average of 30 readings, is $z_0 = c + v_0$, with row $[0\ \ 1]$. Conditioning on both measurements at once uses the stacked $\mathbf H = \begin{bmatrix}1 & 1\\ 0 & 1\end{bmatrix}$ and $\mathbf R = \operatorname{diag}(1/30, 1/30)$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ```python
    def condition_on_measurement(x_prior, P_prior, H, R, z):
        "\"\"Mean and covariance of x given z = H x + v, for x ~ N(x_prior, P_prior), v ~ N(0, R)."\"\"
        S = H @ P_prior @ H.T + R                # covariance of z (Sigma_zz)
        K = P_prior @ H.T @ np.linalg.inv(S)     # Sigma_xz Sigma_zz^{-1}
        x_post = x_prior + K @ (z - H @ x_prior)
        P_post = P_prior - K @ S @ K.T           # Schur complement
        return x_post, P_post
    ```
    """)
    return


@app.cell
def _(np):
    # jb: include=false
    def condition_on_measurement(x_prior, P_prior, H, R, z):
        """Mean and covariance of x given z = H x + v, for x ~ N(x_prior, P_prior), v ~ N(0, R)."""
        S = H @ P_prior @ H.T + R                # covariance of z (Sigma_zz)
        K = P_prior @ H.T @ np.linalg.inv(S)     # Sigma_xz Sigma_zz^{-1}
        x_post = x_prior + K @ (z - H @ x_prior)
        P_post = P_prior - K @ S @ K.T           # Schur complement
        return x_post, P_post

    return (condition_on_measurement,)


@app.cell(hide_code=True)
def _(mo):
    offset_sd = mo.ui.slider(0.2, 5.0, step=0.1, value=2.0, show_value=True, label=r"Prior offset s.d. $\sigma_c$ (lb)")
    use_empty = mo.ui.checkbox(value=False, label="Also condition on the empty-platform measurement")
    return offset_sd, use_empty


@app.cell(hide_code=True)
def _(
    condition_on_measurement,
    confidence_ellipse,
    graphic,
    mo,
    np,
    offset_sd,
    plt,
    use_empty,
):
    _x_true = np.array([155.0, 5.25])
    _noise = np.random.default_rng(5).normal(0.0, 1.0, 2) / np.sqrt(30)
    _z1 = np.array([_x_true[0] + _x_true[1] + _noise[0]])
    _z0 = np.array([_x_true[1] + _noise[1]])
    _x_prior = np.array([150.0, 4.25])
    _P_prior = np.diag([25.0, offset_sd.value**2])
    _x1, _P1 = condition_on_measurement(_x_prior, _P_prior, np.array([[1.0, 1.0]]), np.array([[1 / 30]]), _z1)
    _H2 = np.array([[1.0, 1.0], [0.0, 1.0]])
    _x2, _P2 = condition_on_measurement(_x_prior, _P_prior, _H2, np.diag([1 / 30, 1 / 30]), np.concatenate([_z1, _z0]))

    _fig, _ax = plt.subplots(figsize=(7, 5.5))
    _e = confidence_ellipse(_x_prior, _P_prior, 0.95)
    _ax.plot(_e[0], _e[1], color="gray", ls="--", lw=1.5, label="before: 95% ellipse")
    _e = confidence_ellipse(_x1, _P1, 0.95)
    _ax.plot(_e[0], _e[1], color="C0", lw=2, label="given the standing measurement")
    _ax.plot(*_x1, "o", color="C0", ms=5)
    if use_empty.value:
        _e = confidence_ellipse(_x2, _P2, 0.95)
        _ax.fill(_e[0], _e[1], color="C1", alpha=0.4, label="given both measurements")
        _ax.plot(*_x2, "o", color="C1", ms=5)
    _ax.plot(*_x_true, "k+", ms=14, mew=2, label="truth")
    _ax.set_xlim(135, 168)
    _ax.set_ylim(-8, 16)
    _ax.set_xlabel("Weight $x$ (lb)")
    _ax.set_ylabel("Offset $c$ (lb)")
    _ax.set_title("Conditioning on scale readings", style="italic")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.legend(fontsize=8, loc="upper right")
    _fig.tight_layout()

    def _describe(_m, _P):
        _r = _P[0, 1] / np.sqrt(_P[0, 0] * _P[1, 1])
        return (rf"weight {_m[0]:.2f} $\pm$ {2 * np.sqrt(_P[0, 0]):.2f} lb, offset {_m[1]:.2f} $\pm$ {2 * np.sqrt(_P[1, 1]):.2f} lb "
                rf"($\pm 2$ s.d.), correlation {_r:+.2f}")

    _lines = [f"Given the standing measurement: {_describe(_x1, _P1)}."]
    if use_empty.value:
        _lines.append(f"Given both measurements: {_describe(_x2, _P2)}.")
    mo.vstack([mo.hstack([offset_sd, use_empty], justify="start", gap=2), graphic(_fig), mo.md("  \n".join(_lines))])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The standing measurement pins down $x + c$ very precisely but leaves $x - c$ almost as uncertain as before: the ellipse becomes a thin diagonal sliver, and the weight and offset become strongly *negatively* correlated (if the offset is higher, the weight must be lower). How uncertain the weight remains depends entirely on how well we knew the offset: with $\sigma_c = 2$ lb the weight is still uncertain by about $\pm 3.7$ lb (two standard deviations), and no number of standing readings would change that. This is Chapter 11's "two unknowns, one reading", now quantified. Check the box to add the empty-platform measurement: its row $[0\ \ 1]$ cuts across the sliver, and both unknowns are pinned down. Chapter 13 turns the question "do the measurements cut across every direction?" into the rank test for {term}`observability`.

    Conditioning on the two measurements one after the other, using the first result as the prior for the second, gives exactly the same answer as conditioning on both at once (try it with `condition_on_measurement`). [Chapter 14](#ch14-sec-sequential-updates) uses this to process measurements one at a time.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch12-sec-summary -->
    ## Summary

    - From here on, bold lowercase letters are vectors and bold uppercase letters are matrices.
    - A **random vector** is a list of random variables; its **mean vector** and **covariance matrix** $\operatorname{Cov}(\mathbf x) = \mathbb E[(\mathbf x - \boldsymbol\mu)(\mathbf x - \boldsymbol\mu)^\top]$ collect all means, variances, and covariances. Covariance matrices are symmetric and positive semidefinite, with $\mathbf a^\top\boldsymbol\Sigma\mathbf a = \operatorname{Var}(\mathbf a^\top\mathbf x)$, and positive definite unless some combination of components is constant.
    - Under $\mathbf y = \mathbf A\mathbf x + \mathbf b$: $\mathbb E\mathbf y = \mathbf A\boldsymbol\mu + \mathbf b$ and $\operatorname{Cov}(\mathbf y) = \mathbf A\boldsymbol\Sigma\mathbf A^\top$. The **cross-covariance matrix** $\operatorname{Cov}(\mathbf x, \mathbf y)$ obeys the same rules.
    - The **multivariate normal distribution** $\mathcal N(\boldsymbol\mu, \boldsymbol\Sigma)$ has mean $\boldsymbol\mu$ and covariance $\boldsymbol\Sigma$. Invertible affine maps, marginals, and conditionals of normal vectors are normal, and uncorrelated jointly normal vectors are independent.
    - The squared **Mahalanobis distance** of a normal vector is chi-squared with $n$ degrees of freedom. In two dimensions the **confidence ellipse** $d^2 \le -2\ln(1-p)$ has probability $p$, semi-axes $r_p\sqrt{\lambda_i}$ along the eigenvectors of $\boldsymbol\Sigma$, and the smallest area of all regions with probability $p$.
    - **Conditioning** a joint normal: mean $\boldsymbol\mu_x + \boldsymbol\Sigma_{xz}\boldsymbol\Sigma_{zz}^{-1}(\mathbf z - \boldsymbol\mu_z)$, covariance the Schur complement $\boldsymbol\Sigma_{xx} - \boldsymbol\Sigma_{xz}\boldsymbol\Sigma_{zz}^{-1}\boldsymbol\Sigma_{zx}$. Without normality the same formula is the best linear estimator.
    - With $\boldsymbol\Sigma_{xz} = \mathbf P^-\mathbf H^\top$ and $\boldsymbol\Sigma_{zz} = \mathbf H\mathbf P^-\mathbf H^\top + \mathbf R$, conditioning is the Kalman update $\hat{\mathbf x} = \hat{\mathbf x}^- + \mathbf K(\mathbf z - \mathbf H\hat{\mathbf x}^-)$, $\mathbf P = (\mathbf I - \mathbf K\mathbf H)\mathbf P^-$.

    <!-- label: ch12-sec-whats-next -->
    ## What's Next

    We now have every ingredient of the Kalman filter for state vectors: a process model to predict (Chapter 10), a measurement model to compare with (Chapter 11), and the covariance algebra and conditioning formula to combine them (this chapter). [Chapter 13](ch13_kalman_filter.md) assembles them into the multivariate Kalman filter, proves its prediction and update steps without assuming normality, runs it on the two-state bulking model, and makes "can the measurements separate the unknowns?" precise as observability.
    """)
    return


if __name__ == "__main__":
    app.run()
