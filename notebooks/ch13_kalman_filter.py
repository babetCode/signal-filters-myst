# /// script
# dependencies = [
#     "marimo>=0.25.1",
#     "matplotlib==3.11.2",
#     "numpy==2.5.3",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="13. The Kalman Filter", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "The Multivariate Filter"
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In Part II the state was a single number. Many quantities we care about are not. The bulking example needs a weight *and* a rate of gain; a moving cart needs a position and a velocity; a foot-mounted inertial sensor (Part VI) needs fifteen numbers. This chapter generalizes the scalar {term}`Kalman filter` of [Chapter 9](#ch9-sec-the-scalar-kalman-filter) to a state *vector*. Every scalar becomes a vector or a matrix, every proof becomes a few lines of matrix algebra, and the whole filter follows from one idea: choose the gain that minimizes the total error variance.

    /// attention | 🗝️ **Key Idea**
    The multivariate Kalman filter predicts with $\hat{\mathbf x}_k^- = \mathbf F\hat{\mathbf x}_{k-1} + \mathbf B\mathbf u_k$ and $\mathbf P_k^- = \mathbf F\mathbf P_{k-1}\mathbf F^\top + \mathbf Q$, then corrects the prediction with the gain $\mathbf K_k = \mathbf P_k^-\mathbf H^\top\mathbf S_k^{-1}$, the unique gain that minimizes the error variance of every component of the state at once. Each step is the matrix version of a scalar step you already know.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// important | 🔗 **Prerequisites**
    - [Introduction](introduction.md): [the alpha-beta filter](#intro-sec-beta-weighting-term).
    - [Chapter 6](ch6_expectation_and_variance.md): [linearity of expectation](#ch6-thm-linearity-and-positivity-of-expectation); [covariance](#ch6-sec-covariance-and-correlation).
    - [Chapter 7](ch7_optimal_alpha.md): [the optimal gain by completing the square](#ch7-sec-completing-the-square).
    - [Chapter 8](ch8_bayesian_view.md): [the minimum mean squared error estimator](#ch8-thm-the-posterior-mean-is-the-mmse-estimator) and [the Bayes filter](#ch8-sec-the-bayes-filter) (only for the cross-check section).
    - [Chapter 9](ch9_noise_levels.md): [the scalar Kalman filter](#ch9-sec-the-scalar-kalman-filter), [process noise](#ch9-sec-process-noise), [white noise](#ch9-sec-process-noise), [steady-state gain](#ch9-thm-steady-state-gain), [innovation variance](#ch9-sec-innovations).
    - [Chapter 10](ch10_process_models.md): [process models](#ch10-sec-linear-process-models), [control inputs](#ch10-sec-systems-states-and-inputs), [rate models](#ch10-sec-rate-models-when-the-state-needs-two-numbers).
    - [Chapter 11](ch11_measurement_functions.md): [measurement models](#ch11-sec-from-pounds-to-counts), the gain $P^-h/(h^2P^- + R)$, [the tare-offset example](#ch11-sec-two-unknowns-one-reading).
    - [Chapter 12](ch12_vectors_matrices_covariance.md): [random vectors](#ch12-sec-random-vectors-and-mean-vectors), [mean vectors](#ch12-sec-random-vectors-and-mean-vectors), [covariance and cross-covariance matrices](#ch12-sec-covariance-matrices), $\operatorname{Cov}(\mathbf A\mathbf x + \mathbf b) = \mathbf A\boldsymbol\Sigma\mathbf A^\top$, [the multivariate normal distribution](#ch12-sec-the-multivariate-normal-distribution), [conditioning a joint Gaussian](#ch12-thm-conditioning-a-joint-normal-distribution).
    - [Appendix C: The Mean Value Theorem and Extrema](#appc-sec-the-mean-value-theorem-and-extrema): [at an interior minimum the derivative vanishes](#appc-lem-interior-extremum).
    - Appendix D: [Matrix Multiplication](#appd-sec-matrix-multiplication); [Transpose, Identity, and Inverse](#appd-sec-transpose-identity-and-inverse); [Linear Independence, Basis, and Rank](#appd-sec-linear-independence-basis-and-rank); [Trace](#appd-sec-trace); [Symmetric and Positive Definite Matrices](#appd-sec-symmetric-and-positive-definite-matrices); [Derivatives with Respect to Matrices](#appd-sec-derivatives-with-respect-to-matrices).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch13-sec-a-second-state-variable -->
    ## A Second State Variable

    The Introduction's alpha-beta filter tracked a weight estimate $\hat x_k$ *and* a predicted daily change $\widehat{\Delta x}_k$, corrected by two hand-picked gains $\alpha$ and $\beta$. [Chapter 10](#ch10-sec-rate-models-when-the-state-needs-two-numbers) showed why one number is not enough when a quantity changes at an unknown rate: the rate has to be estimated too. So collect both numbers in a vector,

    $$\mathbf x_k = \begin{bmatrix} x_k \\ r_k \end{bmatrix},$$

    where $x_k$ is the true weight on day $k$ (lb), as in Parts I and II, and $r_k$ is the true rate of gain (lb/day). If the rate stayed constant during each day of length $\Delta t = 1$ day, then $x_k = x_{k-1} + \Delta t\, r_{k-1}$ and $r_k = r_{k-1}$, that is,

    $$\mathbf x_k = \mathbf F\mathbf x_{k-1}, \qquad \mathbf F = \begin{bmatrix} 1 & \Delta t \\ 0 & 1\end{bmatrix}.$$

    The scale measures only the weight, so $z_k = x_k + v_k = \mathbf H\mathbf x_k + v_k$ with $\mathbf H = \begin{bmatrix} 1 & 0 \end{bmatrix}$.

    Two questions remain, and they are the same two questions as in the scalar case: by how much should a *vector* prediction be corrected by a (here scalar) measurement, and how uncertain is the result? The rest of this chapter answers them for every linear model at once.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch13-sec-the-state-space-model -->
    ## The State-Space Model

    From here on, bold lowercase letters are column vectors and bold uppercase letters are matrices; $\mathbf a^\top$ is the transpose. As in [Chapter 12](#ch12-lem-rules-for-cross-covariances), for random vectors $\mathbf a$ and $\mathbf b$ with finite second moments,

    $$\operatorname{Cov}(\mathbf a) := \mathbb E\big[(\mathbf a - \mathbb E\mathbf a)(\mathbf a - \mathbb E\mathbf a)^\top\big], \qquad \operatorname{Cov}(\mathbf a, \mathbf b) := \mathbb E\big[(\mathbf a - \mathbb E\mathbf a)(\mathbf b - \mathbb E\mathbf b)^\top\big],$$

    where the expectation of a matrix is taken entry by entry.

    /// note | 📖 **Definition**
    <u>**State-space model**</u>

    A pair of equations indexed by the time step $k \in \mathbb N^+$: a {term}`process model` that gives a state vector $\mathbf x_k \in \mathbb R^n$ in terms of $\mathbf x_{k-1}$, a known {term}`control input` $\mathbf u_k \in \mathbb R^l$, and a process-noise vector $\mathbf w_k \in \mathbb R^n$; and a {term}`measurement model` that gives a measurement vector $\mathbf z_k \in \mathbb R^m$ in terms of $\mathbf x_k$ and a measurement-noise vector $\mathbf v_k \in \mathbb R^m$. A state-space model is *linear* if it has the form
    $$\mathbf x_k = \mathbf F_k\mathbf x_{k-1} + \mathbf B_k\mathbf u_k + \mathbf w_k, \qquad \mathbf z_k = \mathbf H_k\mathbf x_k + \mathbf v_k$$
    for matrices $\mathbf F_k \in \mathbb R^{n\times n}$, $\mathbf B_k \in \mathbb R^{n\times l}$, and $\mathbf H_k \in \mathbb R^{m\times n}$.
    ///

    /// note | 📖 **Definition**
    <u>**State transition matrix**</u>

    In a linear state-space model, the matrix $\mathbf F_k \in \mathbb R^{n\times n}$ that multiplies $\mathbf x_{k-1}$ in the process model.
    ///

    /// note | 📖 **Definition**
    <u>**Measurement matrix**</u>

    In a linear state-space model, the matrix $\mathbf H_k \in \mathbb R^{m\times n}$ that multiplies $\mathbf x_k$ in the measurement model.
    ///

    /// note | 📖 **Definition**
    <u>**Process noise covariance**</u>

    The covariance matrix $\mathbf Q_k := \operatorname{Cov}(\mathbf w_k)$ of the process-noise vector of a state-space model.
    ///

    /// note | 📖 **Definition**
    <u>**Measurement noise covariance**</u>

    The covariance matrix $\mathbf R_k := \operatorname{Cov}(\mathbf v_k)$ of the measurement-noise vector of a state-space model.
    ///

    The matrix $\mathbf B_k$ is called the *control-input matrix*. In the bulking example $n = 2$, $m = 1$, there is no control input ($\mathbf B_k = \mathbf 0$), $\mathbf F_k = \mathbf F$, $\mathbf H_k = \mathbf H$, and $\mathbf R_k = \sigma_v^2 = 1\ \text{lb}^2$. Its $\mathbf Q_k$ is derived in the example below.

    To keep the formulas readable we drop the subscript $k$ from $\mathbf F, \mathbf B, \mathbf H, \mathbf Q, \mathbf R$. Every result below still holds with the subscripts restored, because each proof uses one time step at a time.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch13-sec-assumptions -->
    ### Assumptions

    The derivation uses the following assumptions about the linear state-space model. They are the vector versions of the scalar assumptions of Chapters 7 and 9.

    - **(A1) Known model.** The matrices $\mathbf F, \mathbf B, \mathbf H, \mathbf Q, \mathbf R$ and the control inputs $\mathbf u_k$ are known, non-random numbers.
    - **(A2) Zero-mean noise.** $\mathbb E\mathbf w_k = \mathbf 0$ and $\mathbb E\mathbf v_k = \mathbf 0$ for all $k$. $\mathbf Q$ is positive semidefinite (as every covariance matrix is) and $\mathbf R$ is {term}`positive definite`.
    - **(A3) Uncorrelated in time.** $\operatorname{Cov}(\mathbf w_j, \mathbf w_k) = \mathbf 0$ and $\operatorname{Cov}(\mathbf v_j, \mathbf v_k) = \mathbf 0$ whenever $j \ne k$. When $\mathbf Q$ and $\mathbf R$ do not depend on $k$, this makes both sequences vector versions of {term}`white noise`.
    - **(A4) Mutually uncorrelated.** $\operatorname{Cov}(\mathbf w_j, \mathbf v_k) = \mathbf 0$ for all $j, k$, and the initial state is uncorrelated with all noise: $\operatorname{Cov}(\mathbf x_0, \mathbf w_k) = \mathbf 0$ and $\operatorname{Cov}(\mathbf x_0, \mathbf v_k) = \mathbf 0$.
    - **(A5) Known initial condition.** $\mathbb E\mathbf x_0 = \hat{\mathbf x}_0$ and $\operatorname{Cov}(\mathbf x_0) = \mathbf P_0$ for a known vector $\hat{\mathbf x}_0$ and a known matrix $\mathbf P_0$.

    Only *uncorrelatedness* is assumed, not independence, and no distribution is assumed. One more assumption is used only in the cross-check section:

    - **(A6) Gaussian.** All randomness comes from independent Gaussian sources: $\mathbf x_0 = \hat{\mathbf x}_0 + \mathbf G_0\boldsymbol\xi_0$, $\mathbf w_k = \mathbf G_k\boldsymbol\xi_k$, and $\mathbf v_k = \boldsymbol\eta_k$ for constant matrices $\mathbf G_k$ and independent random vectors $\boldsymbol\xi_0, \boldsymbol\xi_1, \ldots, \boldsymbol\eta_1, \boldsymbol\eta_2, \ldots$, each with a {term}`multivariate normal distribution`. (The matrices $\mathbf G_k$ allow a singular $\mathbf Q$, as in the bulking example below, where $\mathbf w_k = \boldsymbol\Gamma a_k$ comes from a single scalar $a_k$.)

    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **(A1) fails** when the model is wrong (wrong $\mathbf F$ or $\mathbf H$) or when an input is not known. The filter then becomes biased, and its reported covariance no longer describes its errors. An unknown input can be moved into the noise (Chapter 10 did this with logging error) or estimated as an extra state. [Chapter 14](#ch14-sec-consistency-tests) shows how to detect a wrong model with consistency tests.
    - **(A2) fails** when a noise has a nonzero mean, such as a {term}`sensor bias`. The estimates inherit the bias. The fix is to add the bias to the state, which works only if the enlarged model is observable (see Observability below); Chapter 14 does this for an accelerometer.
    - **(A3) fails** when noise is correlated in time, for example slow drift. The filter then treats repeated errors as independent evidence and becomes overconfident. The fixes are to model the correlated part as an extra state, or to inflate $\mathbf Q$ or $\mathbf R$.
    - **(A4) fails** when the same disturbance affects both the process and the sensor. The cross terms that vanish in the proofs below then survive, and the optimal gain changes, just as Chapter 7's correlated-errors gain $(P^- - c)/(P^- + R - 2c)$ differs from $P^-/(P^- + R)$.
    - **(A5) fails** when $\hat{\mathbf x}_0$ or $\mathbf P_0$ is wrong. The early estimates are then poor, but for observable models the effect fades (Chapter 14, Initialization).
    - **Nonlinear models** are not covered at all; they are the subject of Part IV.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch13-sec-two-covariance-rules -->
    ### Two Covariance Rules

    Every proof in this chapter reduces to the following bookkeeping. It extends [Chapter 12](#ch12-lem-rules-for-cross-covariances)'s rules for covariances and cross-covariances of two vectors to sums of several.

    /// admonition | 📐 **Lemma (Covariance Rules)**
        attrs: {class: lemma, id: ch13-lem-covariance-rules}
    Let $\mathbf a_1, \ldots, \mathbf a_p$ and $\mathbf b_1, \ldots, \mathbf b_q$ be random vectors with finite second moments, $\mathbf A_i$ and $\mathbf C_j$ constant matrices, and $\mathbf c$, $\mathbf d$ constant vectors of compatible sizes. Then

    1. $\operatorname{Cov}\Big(\sum_i \mathbf A_i\mathbf a_i + \mathbf c,\ \sum_j \mathbf C_j\mathbf b_j + \mathbf d\Big) = \sum_i\sum_j \mathbf A_i\operatorname{Cov}(\mathbf a_i, \mathbf b_j)\mathbf C_j^\top$;
    2. $\operatorname{Cov}(\mathbf b, \mathbf a) = \operatorname{Cov}(\mathbf a, \mathbf b)^\top$, and $\operatorname{Cov}(\mathbf a + \mathbf b) = \operatorname{Cov}(\mathbf a) + \operatorname{Cov}(\mathbf a, \mathbf b) + \operatorname{Cov}(\mathbf a, \mathbf b)^\top + \operatorname{Cov}(\mathbf b)$.

    In particular, if $\operatorname{Cov}(\mathbf a, \mathbf b) = \mathbf 0$ then $\operatorname{Cov}(\mathbf A\mathbf a + \mathbf C\mathbf b) = \mathbf A\operatorname{Cov}(\mathbf a)\mathbf A^\top + \mathbf C\operatorname{Cov}(\mathbf b)\mathbf C^\top$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Each entry of $\mathbf A\mathbf X\mathbf C^\top$ is a fixed linear combination of the entries of $\mathbf X$, so linearity of expectation ([Chapter 6](#ch6-thm-linearity-and-positivity-of-expectation)) gives $\mathbb E[\mathbf A\mathbf X\mathbf C^\top] = \mathbf A\,\mathbb E[\mathbf X]\,\mathbf C^\top$ for a random matrix $\mathbf X$ and, in the same way, $\mathbb E[\sum_i\mathbf A_i\mathbf a_i + \mathbf c] = \sum_i\mathbf A_i\bar{\mathbf a}_i + \mathbf c$ with $\bar{\mathbf a}_i := \mathbb E\mathbf a_i$. Hence the centered first argument is $\sum_i\mathbf A_i(\mathbf a_i - \bar{\mathbf a}_i)$, and likewise the centered second argument is $\sum_j\mathbf C_j(\mathbf b_j - \bar{\mathbf b}_j)$. Multiplying out,

    $$\mathbb E\Big[\Big(\sum_i\mathbf A_i(\mathbf a_i - \bar{\mathbf a}_i)\Big)\Big(\sum_j\mathbf C_j(\mathbf b_j - \bar{\mathbf b}_j)\Big)^\top\Big] = \sum_i\sum_j\mathbf A_i\,\mathbb E\big[(\mathbf a_i - \bar{\mathbf a}_i)(\mathbf b_j - \bar{\mathbf b}_j)^\top\big]\,\mathbf C_j^\top,$$

    which is part 1. For part 2, transposing $(\mathbf b - \bar{\mathbf b})(\mathbf a - \bar{\mathbf a})^\top$ gives $(\mathbf a - \bar{\mathbf a})(\mathbf b - \bar{\mathbf b})^\top$, and transposition commutes with taking expectations entrywise; the formula for $\operatorname{Cov}(\mathbf a + \mathbf b)$ is part 1 with both arguments equal to $\mathbf a + \mathbf b$. The final statement is part 1 with the two cross terms equal to $\mathbf 0$. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch13-sec-predict -->
    ## Predict

    A filter of the form used throughout this book alternates two steps. Starting from $\hat{\mathbf x}_0$, for $k = 1, 2, \ldots$ it computes

    $$\hat{\mathbf x}_k^- := \mathbf F\hat{\mathbf x}_{k-1} + \mathbf B\mathbf u_k, \qquad \hat{\mathbf x}_k := \hat{\mathbf x}_k^- + \mathbf K_k\big(\mathbf z_k - \mathbf H\hat{\mathbf x}_k^-\big),$$

    for some gain matrices $\mathbf K_k \in \mathbb R^{n\times m}$. Throughout, the gains are **deterministic**: they may depend on $k$ and on the model, but not on the measurements. Write the errors as

    $$\mathbf e_k^- := \hat{\mathbf x}_k^- - \mathbf x_k, \qquad \mathbf e_k := \hat{\mathbf x}_k - \mathbf x_k \quad (\text{so } \mathbf e_0 = \hat{\mathbf x}_0 - \mathbf x_0),$$

    and their covariances as $\mathbf P_k^- := \operatorname{Cov}(\mathbf e_k^-)$ and $\mathbf P_k := \operatorname{Cov}(\mathbf e_k)$, the vector versions of the {term}`estimation error` and {term}`error variance` of [Chapter 7](#ch7-sec-setting-up-the-problem).

    /// admonition | 📐 **Lemma (Errors Are Linear in the Noise)**
        attrs: {class: lemma, id: ch13-lem-errors-are-linear-in-the-noise}
    For every $k \in \mathbb N^+$,
    $$\mathbf e_k^- = \mathbf F\mathbf e_{k-1} - \mathbf w_k, \qquad \mathbf e_k = (\mathbf I - \mathbf K_k\mathbf H)\mathbf e_k^- + \mathbf K_k\mathbf v_k.$$
    Consequently, under (A3) and (A4), $\operatorname{Cov}(\mathbf e_{k-1}, \mathbf w_k) = \mathbf 0$ and $\operatorname{Cov}(\mathbf e_k^-, \mathbf v_k) = \mathbf 0$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Substitute the model. The control term $\mathbf B\mathbf u_k$ appears in both $\hat{\mathbf x}_k^-$ and $\mathbf x_k$, so it cancels:
    $$\mathbf e_k^- = \mathbf F\hat{\mathbf x}_{k-1} + \mathbf B\mathbf u_k - (\mathbf F\mathbf x_{k-1} + \mathbf B\mathbf u_k + \mathbf w_k) = \mathbf F\mathbf e_{k-1} - \mathbf w_k.$$
    With $\mathbf z_k = \mathbf H\mathbf x_k + \mathbf v_k$,
    $$\mathbf e_k = \hat{\mathbf x}_k^- + \mathbf K_k(\mathbf H\mathbf x_k + \mathbf v_k - \mathbf H\hat{\mathbf x}_k^-) - \mathbf x_k = \mathbf e_k^- - \mathbf K_k\mathbf H\mathbf e_k^- + \mathbf K_k\mathbf v_k.$$

    By induction on $k$, these two formulas show that $\mathbf e_{k-1}$ is a sum of constant matrices times $\mathbf e_0, \mathbf w_1, \ldots, \mathbf w_{k-1}, \mathbf v_1, \ldots, \mathbf v_{k-1}$, and that $\mathbf e_k^-$ is such a sum of $\mathbf e_0, \mathbf w_1, \ldots, \mathbf w_k, \mathbf v_1, \ldots, \mathbf v_{k-1}$. (The gains are deterministic, so the coefficients are constant.) Since $\hat{\mathbf x}_0$ is constant, part 1 of the Covariance Rules gives $\operatorname{Cov}(\mathbf e_0, \mathbf w_k) = -\operatorname{Cov}(\mathbf x_0, \mathbf w_k) = \mathbf 0$ by (A4). Each remaining term in $\operatorname{Cov}(\mathbf e_{k-1}, \mathbf w_k)$ contains $\operatorname{Cov}(\mathbf w_j, \mathbf w_k)$ with $j < k$, which is $\mathbf 0$ by (A3), or $\operatorname{Cov}(\mathbf v_j, \mathbf w_k)$, which is $\mathbf 0$ by (A4). The same argument, with the roles of $\mathbf w$ and $\mathbf v$ exchanged, gives $\operatorname{Cov}(\mathbf e_k^-, \mathbf v_k) = \mathbf 0$, because $\mathbf e_k^-$ involves only $\mathbf v_j$ with $j < k$. $\blacksquare$
    ///

    /// admonition | 📐 **Theorem (Predict)**
        attrs: {class: theorem, id: ch13-thm-predict}
    Assume (A1)–(A4). If $\mathbb E\mathbf e_{k-1} = \mathbf 0$ and $\operatorname{Cov}(\mathbf e_{k-1}) = \mathbf P_{k-1}$, then the prediction $\hat{\mathbf x}_k^- = \mathbf F\hat{\mathbf x}_{k-1} + \mathbf B\mathbf u_k$ satisfies
    $$\mathbb E\mathbf e_k^- = \mathbf 0, \qquad \mathbf P_k^- = \mathbf F\mathbf P_{k-1}\mathbf F^\top + \mathbf Q.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    By the Lemma, $\mathbf e_k^- = \mathbf F\mathbf e_{k-1} - \mathbf w_k$, so $\mathbb E\mathbf e_k^- = \mathbf F\mathbf 0 - \mathbf 0 = \mathbf 0$ by linearity and (A2). The Lemma also gives $\operatorname{Cov}(\mathbf e_{k-1}, \mathbf w_k) = \mathbf 0$, so the last statement of the Covariance Rules (with $\mathbf A = \mathbf F$ and $\mathbf C = -\mathbf I$) gives $\mathbf P_k^- = \mathbf F\mathbf P_{k-1}\mathbf F^\top + \mathbf Q$. $\blacksquare$
    ///

    For $n = 1$ and $\mathbf F = a$ this is [Chapter 10](#ch10-thm-linear-prediction)'s $P_k^- = a^2P_{k-1} + Q$. The control input shifts the prediction but adds no uncertainty, because it is known exactly. A control input that is itself *measured* with noise, such as an accelerometer reading, contributes that noise to $\mathbf w_k$; Chapter 14 works this out for a cart.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch13-sec-update -->
    ## Update

    The update corrects the prediction with the {term}`innovation` $\tilde{\mathbf y}_k := \mathbf z_k - \mathbf H\hat{\mathbf x}_k^-$, the part of the measurement the prediction did not anticipate.

    /// admonition | 📐 **Theorem (Innovation Covariance)**
        attrs: {class: theorem, id: ch13-thm-innovation-covariance}
    Assume (A1)–(A4) and $\mathbb E\mathbf e_k^- = \mathbf 0$. Then $\mathbb E\tilde{\mathbf y}_k = \mathbf 0$ and
    $$\operatorname{Cov}(\tilde{\mathbf y}_k) = \mathbf S_k := \mathbf H\mathbf P_k^-\mathbf H^\top + \mathbf R.$$
    Moreover, $\mathbf S_k$ is symmetric and positive definite, hence invertible.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    $\tilde{\mathbf y}_k = \mathbf H\mathbf x_k + \mathbf v_k - \mathbf H\hat{\mathbf x}_k^- = -\mathbf H\mathbf e_k^- + \mathbf v_k$, so its mean is $\mathbf 0$. Since $\operatorname{Cov}(\mathbf e_k^-, \mathbf v_k) = \mathbf 0$ (Lemma), the Covariance Rules give $\operatorname{Cov}(\tilde{\mathbf y}_k) = \mathbf H\mathbf P_k^-\mathbf H^\top + \mathbf R$. Both terms are symmetric. For $\mathbf a \ne \mathbf 0$,
    $$\mathbf a^\top\mathbf S_k\mathbf a = (\mathbf H^\top\mathbf a)^\top\mathbf P_k^-(\mathbf H^\top\mathbf a) + \mathbf a^\top\mathbf R\mathbf a > 0,$$
    because the first term is $\ge 0$ ($\mathbf P_k^-$ is a covariance matrix, hence positive semidefinite by [Chapter 12](#ch12-thm-covariance-matrices-are-symmetric-and-positive-semidefinite)) and the second is $> 0$ by (A2). Finally, if $\mathbf S_k\mathbf a = \mathbf 0$ then $\mathbf a^\top\mathbf S_k\mathbf a = 0$, so $\mathbf a = \mathbf 0$; a square matrix whose only null vector is $\mathbf 0$ has full rank and is invertible ([Appendix D: Linear Independence, Basis, and Rank](#appd-sec-linear-independence-basis-and-rank)). $\blacksquare$
    ///

    /// note | 📖 **Definition**
    <u>**Innovation covariance**</u>

    The covariance matrix $\mathbf S_k := \operatorname{Cov}(\tilde{\mathbf y}_k)$ of the innovation $\tilde{\mathbf y}_k = \mathbf z_k - \mathbf H_k\hat{\mathbf x}_k^-$ of a linear state-space model. Under (A1)–(A4), $\mathbf S_k = \mathbf H_k\mathbf P_k^-\mathbf H_k^\top + \mathbf R_k$.
    ///

    For $m = 1$ this is the {term}`innovation variance` of [Chapter 9](#ch9-sec-innovations). Now the update error, for *any* gain:

    /// admonition | 📐 **Theorem (Update with an Arbitrary Gain)**
        attrs: {class: theorem, id: ch13-thm-update-with-an-arbitrary-gain}
    Assume (A1)–(A4) and $\mathbb E\mathbf e_k^- = \mathbf 0$. For every deterministic $\mathbf K_k \in \mathbb R^{n\times m}$, the update $\hat{\mathbf x}_k = \hat{\mathbf x}_k^- + \mathbf K_k\tilde{\mathbf y}_k$ satisfies $\mathbb E\mathbf e_k = \mathbf 0$ and
    $$\mathbf P_k = (\mathbf I - \mathbf K_k\mathbf H)\mathbf P_k^-(\mathbf I - \mathbf K_k\mathbf H)^\top + \mathbf K_k\mathbf R\mathbf K_k^\top.$$
    This matrix is symmetric and positive semidefinite.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    By the Lemma, $\mathbf e_k = (\mathbf I - \mathbf K_k\mathbf H)\mathbf e_k^- + \mathbf K_k\mathbf v_k$, so $\mathbb E\mathbf e_k = \mathbf 0$, and since $\operatorname{Cov}(\mathbf e_k^-, \mathbf v_k) = \mathbf 0$ the Covariance Rules give the formula. Each term has the form $\mathbf M\mathbf A\mathbf M^\top$ with $\mathbf A$ symmetric positive semidefinite, and $\mathbf a^\top\mathbf M\mathbf A\mathbf M^\top\mathbf a = (\mathbf M^\top\mathbf a)^\top\mathbf A(\mathbf M^\top\mathbf a) \ge 0$; a sum of symmetric positive semidefinite matrices is symmetric positive semidefinite. $\blacksquare$
    ///

    /// note | 📖 **Definition**
    <u>**Joseph form**</u>

    The expression
    $$\mathbf P_k = (\mathbf I - \mathbf K_k\mathbf H_k)\mathbf P_k^-(\mathbf I - \mathbf K_k\mathbf H_k)^\top + \mathbf K_k\mathbf R_k\mathbf K_k^\top$$
    for the error covariance after an update $\hat{\mathbf x}_k = \hat{\mathbf x}_k^- + \mathbf K_k(\mathbf z_k - \mathbf H_k\hat{\mathbf x}_k^-)$ with an arbitrary deterministic gain $\mathbf K_k$.
    ///

    The name honors Peter Joseph, whose book with Richard Bucy popularized it [@bucy1968]. Two consequences matter already. Every gain gives an **unbiased** estimate; the gain only decides how large the error covariance is. And the update never needs the measurement to compute $\mathbf P_k$: the whole covariance sequence can be computed before any data arrive.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch13-sec-the-optimal-gain -->
    ## The Optimal Gain

    Which gain should we use? A matrix cannot be minimized directly, so we need a single number that measures the size of $\mathbf P_k$. Because $\mathbb E\mathbf e_k = \mathbf 0$, the $i$-th diagonal entry of $\mathbf P_k$ is $\mathbb E[e_{k,i}^2]$, the {term}`mean squared error` of the $i$-th state component. Their sum is the {term}`trace`:

    $$\operatorname{tr}\mathbf P_k = \sum_{i=1}^n\mathbb E\big[e_{k,i}^2\big] = \mathbb E\big[\|\mathbf e_k\|^2\big],$$

    the mean squared length of the error vector. In the bulking example this adds $\text{lb}^2$ to $(\text{lb/day})^2$, which looks like an arbitrary choice of units. The theorem below shows that the choice does not matter: the gain that minimizes the trace minimizes the error variance of *every* linear combination of state components at once.

    Write $\mathbf P^- := \mathbf P_k^-$, $\mathbf S := \mathbf H\mathbf P^-\mathbf H^\top + \mathbf R$, and $\mathbf P(\mathbf K) := (\mathbf I - \mathbf K\mathbf H)\mathbf P^-(\mathbf I - \mathbf K\mathbf H)^\top + \mathbf K\mathbf R\mathbf K^\top$.

    /// admonition | 📐 **Theorem (Kalman Gain)**
        attrs: {class: theorem, id: ch13-thm-kalman-gain}
    Let $\mathbf P^-$ be symmetric positive semidefinite and $\mathbf R$ symmetric positive definite. Then $\operatorname{tr}\mathbf P(\mathbf K)$ has exactly one minimizer over all $\mathbf K \in \mathbb R^{n\times m}$, namely
    $$\mathbf K^* = \mathbf P^-\mathbf H^\top\mathbf S^{-1}.$$
    Moreover, for every $\mathbf K$,
    $$\mathbf P(\mathbf K) = \mathbf P(\mathbf K^*) + (\mathbf K - \mathbf K^*)\,\mathbf S\,(\mathbf K - \mathbf K^*)^\top,$$
    so $\mathbf a^\top\mathbf P(\mathbf K)\mathbf a \ge \mathbf a^\top\mathbf P(\mathbf K^*)\mathbf a$ for every $\mathbf a \in \mathbb R^n$: no other gain gives a smaller error variance for any linear combination $\mathbf a^\top\mathbf e_k$ of the state errors.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    *Step 1 (expand).* Multiplying out and using $\mathbf H\mathbf P^-\mathbf H^\top + \mathbf R = \mathbf S$,
    $$\mathbf P(\mathbf K) = \mathbf P^- - \mathbf K\mathbf H\mathbf P^- - \mathbf P^-\mathbf H^\top\mathbf K^\top + \mathbf K\mathbf S\mathbf K^\top.$$
    Since $\mathbf P^-$ is symmetric, $\mathbf P^-\mathbf H^\top\mathbf K^\top = (\mathbf K\mathbf H\mathbf P^-)^\top$, and a matrix and its transpose have the same trace, so
    $$\operatorname{tr}\mathbf P(\mathbf K) = \operatorname{tr}\mathbf P^- - 2\operatorname{tr}(\mathbf H\mathbf P^-\mathbf K) + \operatorname{tr}(\mathbf K\mathbf S\mathbf K^\top),$$
    where we also used the cyclic property $\operatorname{tr}(\mathbf K\mathbf H\mathbf P^-) = \operatorname{tr}(\mathbf H\mathbf P^-\mathbf K)$ ([Appendix D: Trace](#appd-sec-trace)).

    *Step 2 (find the candidate).* $\operatorname{tr}\mathbf P(\mathbf K)$ is a polynomial in the $nm$ entries of $\mathbf K$, defined on all of $\mathbb R^{n\times m}$. At a minimizer, each partial derivative $\partial/\partial K_{ij}$ must vanish: fixing all other entries leaves a differentiable function of one variable with a minimum at an interior point, whose derivative is zero ([Appendix C: The Mean Value Theorem and Extrema](#appc-sec-the-mean-value-theorem-and-extrema)). [Appendix D: Derivatives with Respect to Matrices](#appd-sec-derivatives-with-respect-to-matrices) proves $\partial\operatorname{tr}(\mathbf A\mathbf X)/\partial\mathbf X = \mathbf A^\top$ and $\partial\operatorname{tr}(\mathbf X\mathbf A\mathbf X^\top)/\partial\mathbf X = \mathbf X(\mathbf A + \mathbf A^\top)$, where $\partial f/\partial\mathbf X$ is the matrix of partial derivatives $\partial f/\partial X_{ij}$. With $\mathbf A = \mathbf H\mathbf P^-$ in the first and $\mathbf A = \mathbf S = \mathbf S^\top$ in the second,
    $$\frac{\partial\operatorname{tr}\mathbf P(\mathbf K)}{\partial\mathbf K} = -2\mathbf P^-\mathbf H^\top + 2\mathbf K\mathbf S.$$
    This is $\mathbf 0$ exactly when $\mathbf K = \mathbf P^-\mathbf H^\top\mathbf S^{-1} = \mathbf K^*$ ($\mathbf S$ is invertible by the Innovation Covariance theorem). So $\mathbf K^*$ is the only candidate.

    *Step 3 (it is the minimum: complete the square).* The inverse of a symmetric matrix is symmetric, so $\mathbf K^{*\top} = \mathbf S^{-1}\mathbf H\mathbf P^-$. Hence $\mathbf K\mathbf S\mathbf K^{*\top} = \mathbf K\mathbf H\mathbf P^-$ and $\mathbf K^*\mathbf S\mathbf K^\top = (\mathbf K\mathbf S\mathbf K^{*\top})^\top = \mathbf P^-\mathbf H^\top\mathbf K^\top$, and therefore
    $$(\mathbf K - \mathbf K^*)\mathbf S(\mathbf K - \mathbf K^*)^\top = \mathbf K\mathbf S\mathbf K^\top - \mathbf K\mathbf H\mathbf P^- - \mathbf P^-\mathbf H^\top\mathbf K^\top + \mathbf K^*\mathbf S\mathbf K^{*\top}.$$
    Comparing with Step 1, $\mathbf P(\mathbf K) = \mathbf P^- - \mathbf K^*\mathbf S\mathbf K^{*\top} + (\mathbf K - \mathbf K^*)\mathbf S(\mathbf K - \mathbf K^*)^\top$. Setting $\mathbf K = \mathbf K^*$ shows $\mathbf P(\mathbf K^*) = \mathbf P^- - \mathbf K^*\mathbf S\mathbf K^{*\top}$, which proves the displayed identity. For any $\mathbf a$, with $\mathbf b := (\mathbf K - \mathbf K^*)^\top\mathbf a$, the extra term contributes $\mathbf b^\top\mathbf S\mathbf b \ge 0$. Summing over the standard basis vectors $\mathbf a = \mathbf e_1, \ldots, \mathbf e_n$, the extra trace is $\sum_i\mathbf b_i^\top\mathbf S\mathbf b_i$, where $\mathbf b_i^\top$ is the $i$-th row of $\mathbf K - \mathbf K^*$. Since $\mathbf S$ is positive definite, this is $> 0$ unless every row is zero, that is, unless $\mathbf K = \mathbf K^*$. $\blacksquare$
    ///

    /// note | 📖 **Definition**
    <u>**Kalman gain**</u>

    The gain $\mathbf K_k := \mathbf P_k^-\mathbf H_k^\top\mathbf S_k^{-1}$ in the update $\hat{\mathbf x}_k = \hat{\mathbf x}_k^- + \mathbf K_k(\mathbf z_k - \mathbf H_k\hat{\mathbf x}_k^-)$, where $\mathbf P_k^-$ is the error covariance of the prediction and $\mathbf S_k = \mathbf H_k\mathbf P_k^-\mathbf H_k^\top + \mathbf R_k$ is the innovation covariance.
    ///

    The Kalman gain is the vector version of the {term}`optimal gain`. For $n = m = 1$ and $\mathbf H = h$ it is [Chapter 11](#ch11-thm-optimal-gain-with-a-measurement-function)'s $K = P^-h/(h^2P^- + R)$, and for $h = 1$ it is Chapter 7's $P^-/(P^- + R)$. Step 3 is Chapter 7's completing-the-square argument with matrices.

    /// admonition | 📐 **Corollary (Simplified Covariance Update)**
        attrs: {class: corollary, id: ch13-cor-simplified-covariance-update}
    At the Kalman gain, and only there in general,
    $$\mathbf P_k = (\mathbf I - \mathbf K_k\mathbf H)\mathbf P_k^- = \mathbf P_k^- - \mathbf K_k\mathbf S_k\mathbf K_k^\top.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    The proof of the theorem gave $\mathbf P(\mathbf K^*) = \mathbf P^- - \mathbf K^*\mathbf S\mathbf K^{*\top}$, and $\mathbf K^*\mathbf S\mathbf K^{*\top} = \mathbf K^*\mathbf S\mathbf S^{-1}\mathbf H\mathbf P^- = \mathbf K^*\mathbf H\mathbf P^-$. $\blacksquare$
    ///

    The simplified form is cheaper, but it is *only* correct at the optimal gain, and a computer never uses exactly the optimal gain: the gain it uses is $\mathbf K = \mathbf K^* + \boldsymbol\delta$, with $\boldsymbol\delta$ caused by rounding (or by a deliberately chosen non-optimal gain, as in the alpha-beta filter below). Then:

    - The Joseph form evaluated at $\mathbf K$ is the *exact* covariance of the gain actually used, for every $\boldsymbol\delta$ (Theorem: Update with an Arbitrary Gain). By the Kalman Gain theorem it exceeds the optimum by only $\boldsymbol\delta\mathbf S\boldsymbol\delta^\top$, which is second order in $\boldsymbol\delta$.
    - The simplified form evaluated at $\mathbf K$ is $(\mathbf I - \mathbf K\mathbf H)\mathbf P^- = \mathbf P(\mathbf K^*) - \boldsymbol\delta\mathbf H\mathbf P^-$, which differs from the true covariance $\mathbf P(\mathbf K^*) + \boldsymbol\delta\mathbf S\boldsymbol\delta^\top$ by $-\boldsymbol\delta\mathbf H\mathbf P^- - \boldsymbol\delta\mathbf S\boldsymbol\delta^\top$: an error of *first* order in $\boldsymbol\delta$, and in general not even a symmetric matrix.

    This is why the Joseph form exists. The table below checks both claims on the bulking model of the next sections (steady-state $\mathbf P^-$, $\sigma_a = 0.05\ \text{lb/day}^2$, $R = 1\ \text{lb}^2$), with the two entries of the gain perturbed in opposite directions, $\mathbf K = [(1 + \varepsilon)K^*_1,\ (1 - \varepsilon)K^*_2]^\top$, as rounding might. Each column reports the largest absolute entry of a matrix difference, relative to the largest entry of $\mathbf P(\mathbf K^*)$.
    """)
    return


@app.cell
def gain_perturbation_check(np):
    # jb: include=false
    _dt = 1.0
    _F = np.array([[1.0, _dt], [0.0, 1.0]])
    _G = np.array([[_dt**2 / 2], [_dt]])
    _Q = 0.05**2 * _G @ _G.T
    _H = np.array([[1.0, 0.0]])
    _R = np.array([[1.0]])
    _P = np.eye(2)
    for _ in range(2000):
        _Pm = _F @ _P @ _F.T + _Q
        _S = _H @ _Pm @ _H.T + _R
        _K = _Pm @ _H.T @ np.linalg.inv(_S)
        _P = (np.eye(2) - _K @ _H) @ _Pm

    def _joseph(K):
        _IKH = np.eye(2) - K @ _H
        return _IKH @ _Pm @ _IKH.T + K @ _R @ K.T

    _Popt = _joseph(_K)
    _scale = np.abs(_Popt).max()
    _rows = []
    _rng = np.random.default_rng(0)
    for _eps in [1e-1, 1e-2, 1e-3, 1e-4]:
        _Kp = _K * np.array([[1 + _eps], [1 - _eps]])
        _true = _joseph(_Kp)  # exact covariance of the gain actually used
        _simple = (np.eye(2) - _Kp @ _H) @ _Pm
        _rows.append((
            _eps,
            np.abs(_true - _Popt).max() / _scale,
            np.abs(_simple - _true).max() / _scale,
            np.abs(_simple - _simple.T).max() / _scale,
        ))
    # Monte Carlo confirmation that the Joseph form is the actual covariance
    _Kp = 1.5 * _K
    _N = 200_000
    _em = _rng.multivariate_normal(np.zeros(2), _Pm, size=_N)
    _v = _rng.normal(0.0, 1.0, size=(_N, 1))
    _e = _em @ (np.eye(2) - _Kp @ _H).T + _v @ _Kp.T
    gain_mc_rel_err = np.abs(np.cov(_e.T) - _joseph(_Kp)).max() / np.abs(_joseph(_Kp)).max()
    gain_perturbation_rows = _rows
    return gain_mc_rel_err, gain_perturbation_rows


@app.cell(hide_code=True)
def _(gain_mc_rel_err, gain_perturbation_rows, mo):
    _lines = [
        "| $\\varepsilon$ | true excess over optimum (Joseph) | error of the simplified form | asymmetry of the simplified form |",
        "|:---|:---:|:---:|:---:|",
    ]
    for _eps, _excess, _err, _asym in gain_perturbation_rows:
        _lines.append(f"| ${_eps:.0e}$ | ${_excess:.1e}$ | ${_err:.1e}$ | ${_asym:.1e}$ |")
    _lines += [
        "",
        r"Each tenfold reduction of $\varepsilon$ shrinks the true excess about hundredfold "
        r"(second order) but the simplified form's error only about tenfold (first order), and the "
        r"simplified form is not even symmetric. A Monte Carlo simulation with $200{,}000$ draws and the clearly "
        r"non-optimal gain $1.5\,\mathbf K^*$ reproduces the Joseph-form covariance to within a "
        rf"relative error of ${gain_mc_rel_err:.1e}$.",
    ]
    mo.md("\n".join(_lines))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **"Optimal" means optimal among filters of this form**: linear updates $\hat{\mathbf x}_k^- + \mathbf K_k\tilde{\mathbf y}_k$ with deterministic gains, under (A1)–(A5). Under the Gaussian assumption (A6) it is optimal among *all* estimators (next section). Without (A6), a nonlinear estimator can do better, for example when the noise contains outliers (Chapter 8's counterexample).
    - **Data-dependent gains** break the proofs. If the gain depends on the measurements (for example, by skipping measurements that look like outliers, as in Chapter 14), the errors are no longer linear in the noise, and $\mathbf P_k$ is only an approximation of the error covariance.
    - **Wrong $\mathbf Q$ or $\mathbf R$.** If the filter computes its gain from incorrect noise covariances, the gain is not optimal for the true system, but every gain gives an unbiased estimate, so the filter stays unbiased. The covariance it *reports*, however, is wrong. The true covariance follows from the Joseph form with the true $\mathbf Q$ and $\mathbf R$ and the gains actually used. Chapter 14 shows how to detect this from data.
    - **$\mathbf R$ only positive semidefinite** (a perfect measurement of some combination of states): $\mathbf S$ can be singular when $\mathbf P^-$ is too. Then the inverse must be replaced, or the perfectly measured combination removed from the state.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch13-sec-cross-check-gaussian-conditioning -->
    ## Cross-Check: Gaussian Conditioning

    [Chapter 12](#ch12-thm-conditioning-a-joint-normal-distribution) derived, with the Schur complement, the conditional distribution of one part of a jointly Gaussian vector given the other: if
    $$\begin{bmatrix}\mathbf a \\ \mathbf b\end{bmatrix} \sim \mathcal N\left(\begin{bmatrix}\boldsymbol\mu_a \\ \boldsymbol\mu_b\end{bmatrix}, \begin{bmatrix}\boldsymbol\Sigma_{aa} & \boldsymbol\Sigma_{ab} \\ \boldsymbol\Sigma_{ba} & \boldsymbol\Sigma_{bb}\end{bmatrix}\right)$$
    with $\boldsymbol\Sigma_{bb}$ invertible, then given $\mathbf b = \boldsymbol\beta$, $\mathbf a$ is normal with mean $\boldsymbol\mu_a + \boldsymbol\Sigma_{ab}\boldsymbol\Sigma_{bb}^{-1}(\boldsymbol\beta - \boldsymbol\mu_b)$ and covariance $\boldsymbol\Sigma_{aa} - \boldsymbol\Sigma_{ab}\boldsymbol\Sigma_{bb}^{-1}\boldsymbol\Sigma_{ba}$. Nothing in that derivation mentions gains or traces, yet it produces the same update.

    /// admonition | 📐 **Theorem (The Update Is Gaussian Conditioning)**
        attrs: {class: theorem, id: ch13-thm-the-update-is-gaussian-conditioning}
    Let $\mathbf x \sim \mathcal N(\hat{\mathbf x}^-, \mathbf P^-)$ and $\mathbf v \sim \mathcal N(\mathbf 0, \mathbf R)$ be independent, with $\mathbf P^-$ and $\mathbf R$ positive definite, and let $\mathbf z = \mathbf H\mathbf x + \mathbf v$. Then, given $\mathbf z = \boldsymbol\zeta$, $\mathbf x$ is normal with mean $\hat{\mathbf x}^- + \mathbf K(\boldsymbol\zeta - \mathbf H\hat{\mathbf x}^-)$ and covariance $(\mathbf I - \mathbf K\mathbf H)\mathbf P^-$, where $\mathbf K = \mathbf P^-\mathbf H^\top\mathbf S^{-1}$ is the Kalman gain.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Independent normal vectors stack into a normal vector (Chapter 12, Corollary: Stacking Independent Normal Vectors), so $(\mathbf x, \mathbf v)$ is multivariate normal with mean $(\hat{\mathbf x}^-, \mathbf 0)$ and block-diagonal covariance $\operatorname{diag}(\mathbf P^-, \mathbf R)$. Now
    $$\begin{bmatrix}\mathbf x \\ \mathbf z\end{bmatrix} = \mathbf T\begin{bmatrix}\mathbf x \\ \mathbf v\end{bmatrix}, \qquad \mathbf T := \begin{bmatrix}\mathbf I & \mathbf 0 \\ \mathbf H & \mathbf I\end{bmatrix},$$
    and $\mathbf T$ is invertible (its inverse replaces $\mathbf H$ by $-\mathbf H$). An invertible linear image of a normal vector is normal (Chapter 12, Theorem: Invertible Affine Maps Preserve Normality), here with mean $(\hat{\mathbf x}^-, \mathbf H\hat{\mathbf x}^-)$ and, by $\operatorname{Cov}(\mathbf T\mathbf y) = \mathbf T\operatorname{Cov}(\mathbf y)\mathbf T^\top$, covariance
    $$\begin{bmatrix}\mathbf I & \mathbf 0 \\ \mathbf H & \mathbf I\end{bmatrix}\begin{bmatrix}\mathbf P^- & \mathbf 0 \\ \mathbf 0 & \mathbf R\end{bmatrix}\begin{bmatrix}\mathbf I & \mathbf H^\top \\ \mathbf 0 & \mathbf I\end{bmatrix} = \begin{bmatrix}\mathbf P^- & \mathbf P^-\mathbf H^\top \\ \mathbf H\mathbf P^- & \mathbf S\end{bmatrix}.$$
    The block $\mathbf S$ is invertible (Innovation Covariance theorem). The conditioning formula gives the mean $\hat{\mathbf x}^- + \mathbf P^-\mathbf H^\top\mathbf S^{-1}(\boldsymbol\zeta - \mathbf H\hat{\mathbf x}^-)$ and the covariance $\mathbf P^- - \mathbf P^-\mathbf H^\top\mathbf S^{-1}\mathbf H\mathbf P^- = (\mathbf I - \mathbf K\mathbf H)\mathbf P^-$. $\blacksquare$
    ///

    Applied at every step, this is [Chapter 8](#ch8-sec-the-bayes-filter)'s {term}`Bayes filter` with Gaussian densities. Under (A1)–(A6), the conditional distribution of $\mathbf x_{k-1}$ given $\mathbf z_1, \ldots, \mathbf z_{k-1}$ is Gaussian. The prediction step maps it through the linear process model with independent Gaussian noise, which keeps it Gaussian with mean $\hat{\mathbf x}_k^-$ and covariance $\mathbf P_k^-$, and the theorem performs the update. By induction on $k$, $\hat{\mathbf x}_k = \mathbb E[\mathbf x_k \mid \mathbf z_1, \ldots, \mathbf z_k]$ and $\mathbf P_k = \operatorname{Cov}(\mathbf x_k \mid \mathbf z_1, \ldots, \mathbf z_k)$; a detailed proof is in @barshalom2002 [Ch. 5]. The conditional mean is the {term}`minimum mean squared error estimator` (Chapter 8). So:

    - **Without (A6)**, the Kalman filter is the best filter of the linear form above (previous section).
    - **With (A6)**, it is the best estimator of any form whatsoever, linear or not.

    Two independent derivations, one minimizing a trace and one conditioning a Gaussian, give the same formulas. The cell below repeats the comparison numerically for a random example with four states and two measurements.
    """)
    return


@app.cell
def conditioning_check(np):
    # jb: include=false
    _rng = np.random.default_rng(12)
    _n, _m = 4, 2
    _A = _rng.normal(size=(_n, _n))
    _Pm = _A @ _A.T + 0.1 * np.eye(_n)
    _Bm = _rng.normal(size=(_m, _m))
    _R = _Bm @ _Bm.T + 0.1 * np.eye(_m)
    _H = _rng.normal(size=(_m, _n))
    _xm = _rng.normal(size=_n)
    _zeta = _rng.normal(size=_m)
    # Kalman update
    _S = _H @ _Pm @ _H.T + _R
    _K = _Pm @ _H.T @ np.linalg.inv(_S)
    _x_kf = _xm + _K @ (_zeta - _H @ _xm)
    _P_kf = (np.eye(_n) - _K @ _H) @ _Pm
    # Gaussian conditioning on the joint covariance
    _T = np.block([[np.eye(_n), np.zeros((_n, _m))], [_H, np.eye(_m)]])
    _Sigma = _T @ np.block([[_Pm, np.zeros((_n, _m))], [np.zeros((_m, _n)), _R]]) @ _T.T
    _Saa, _Sab = _Sigma[:_n, :_n], _Sigma[:_n, _n:]
    _Sba, _Sbb = _Sigma[_n:, :_n], _Sigma[_n:, _n:]
    _x_c = _xm + _Sab @ np.linalg.solve(_Sbb, _zeta - _H @ _xm)
    _P_c = _Saa - _Sab @ np.linalg.solve(_Sbb, _Sba)
    conditioning_mean_diff = np.abs(_x_kf - _x_c).max()
    conditioning_cov_diff = np.abs(_P_kf - _P_c).max()
    return conditioning_cov_diff, conditioning_mean_diff


@app.cell(hide_code=True)
def _(conditioning_cov_diff, conditioning_mean_diff, mo):
    mo.md(rf"""
    The largest difference between the two means is ${conditioning_mean_diff:.1e}$, and between the two covariances ${conditioning_cov_diff:.1e}$: equal up to floating-point rounding.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch13-sec-the-algorithm -->
    ## The Algorithm

    Collecting the results gives the multivariate {term}`Kalman filter`. For $n = m = 1$ it is exactly the scalar filter of [Chapter 9](#ch9-sec-the-scalar-kalman-filter).

    /// attention | 🗝️ **Key Idea**
    Start from $\hat{\mathbf x}_0$ and $\mathbf P_0$. For $k = 1, 2, \ldots$:

    **Predict**
    $$\hat{\mathbf x}_k^- = \mathbf F\hat{\mathbf x}_{k-1} + \mathbf B\mathbf u_k, \qquad \mathbf P_k^- = \mathbf F\mathbf P_{k-1}\mathbf F^\top + \mathbf Q.$$

    **Update**
    $$\tilde{\mathbf y}_k = \mathbf z_k - \mathbf H\hat{\mathbf x}_k^-, \qquad \mathbf S_k = \mathbf H\mathbf P_k^-\mathbf H^\top + \mathbf R, \qquad \mathbf K_k = \mathbf P_k^-\mathbf H^\top\mathbf S_k^{-1},$$
    $$\hat{\mathbf x}_k = \hat{\mathbf x}_k^- + \mathbf K_k\tilde{\mathbf y}_k, \qquad \mathbf P_k = (\mathbf I - \mathbf K_k\mathbf H)\mathbf P_k^-(\mathbf I - \mathbf K_k\mathbf H)^\top + \mathbf K_k\mathbf R\mathbf K_k^\top.$$
    ///

    The implementation below follows the box line by line. Two choices deserve a comment. It never forms $\mathbf S_k^{-1}$: since $\mathbf S_k$ and $\mathbf P_k^-$ are symmetric, $\mathbf K_k^\top = \mathbf S_k^{-1}\mathbf H\mathbf P_k^-$, which is the solution $\mathbf X$ of the linear system $\mathbf S_k\mathbf X = \mathbf H\mathbf P_k^-$, and solving a system is cheaper and more accurate than inverting a matrix. And it uses the Joseph form, for the reasons given above.
    """)
    return


@app.cell
def kalman_filter_impl(np):
    # jb: editor=true
    def kf_predict(x, P, F, Q, B=None, u=None):
        """Predict step: x^- = F x + B u,  P^- = F P F^T + Q."""
        x_pred = F @ x if B is None else F @ x + B @ u
        P_pred = F @ P @ F.T + Q
        return x_pred, P_pred


    def kf_update(x_pred, P_pred, z, H, R):
        """Update step with the Kalman gain; covariance in Joseph form."""
        y = z - H @ x_pred                        # innovation
        S = H @ P_pred @ H.T + R                  # innovation covariance
        K = np.linalg.solve(S, H @ P_pred).T      # K = P^- H^T S^-1
        x = x_pred + K @ y
        I_KH = np.eye(len(x)) - K @ H
        P = I_KH @ P_pred @ I_KH.T + K @ R @ K.T  # Joseph form
        return x, P, K, y, S


    def kalman_filter(zs, F, H, Q, R, x0, P0, B=None, us=None):
        """Run the filter on measurements zs[0], zs[1], ... (that is, z_1, z_2, ...).

        Returns a dict of arrays: estimates "x", covariances "P", predictions
        "x_pred", "P_pred", gains "K", innovations "y", innovation covariances "S".
        """
        x, P = np.asarray(x0, float), np.asarray(P0, float)
        out = {key: [] for key in ("x", "P", "x_pred", "P_pred", "K", "y", "S")}
        for k, z in enumerate(zs):
            u = None if us is None else us[k]
            x_pred, P_pred = kf_predict(x, P, F, Q, B, u)
            x, P, K, y, S = kf_update(x_pred, P_pred, np.atleast_1d(z), H, R)
            for key, value in zip(out, (x, P, x_pred, P_pred, K, y, S)):
                out[key].append(value)
        return {key: np.array(value) for key, value in out.items()}

    return kalman_filter, kf_update


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch13-sec-example-a-bulk-then-a-cut -->
    ## Example: A Bulk, Then a Cut

    Back to the 28 daily weigh-ins of the bulking example: you weigh 155 lb on day 1 and gain 1.4 lb/week (0.2 lb/day), and each morning's reading has noise with $\sigma_v = 1$ lb. This time the diet changes halfway: after the weigh-in on day 15 you switch to a cut and *lose* 1.4 lb/week from then on. The readings on days 1 to 15 are exactly the Introduction's (same true weights, same noise); from day 16 on, the true weight falls instead of rising. The Introduction's alpha-beta filter, with its hand-picked gains, can only follow such a change slowly. The Kalman filter with state $\mathbf x_k = [x_k, r_k]^\top$ chooses its gains itself.

    **Process noise.** The model $\mathbf x_k = \mathbf F\mathbf x_{k-1}$ says the rate never changes. To allow change, suppose that during day $k$ the rate changes at an unknown constant "acceleration" $a_k$ (lb/day$^2$), with the $a_k$ uncorrelated across days, mean $0$, and variance $\sigma_a^2$. Over one day,
    $$r_k = r_{k-1} + a_k\Delta t, \qquad x_k = x_{k-1} + r_{k-1}\Delta t + \tfrac12 a_k\Delta t^2,$$
    so $\mathbf w_k = \boldsymbol\Gamma a_k$ with $\boldsymbol\Gamma = [\tfrac12\Delta t^2,\ \Delta t]^\top$, and by the Covariance Rules
    $$\mathbf Q = \operatorname{Cov}(\boldsymbol\Gamma a_k) = \sigma_a^2\boldsymbol\Gamma\boldsymbol\Gamma^\top = \sigma_a^2\begin{bmatrix}\tfrac14\Delta t^4 & \tfrac12\Delta t^3 \\ \tfrac12\Delta t^3 & \Delta t^2\end{bmatrix}.$$
    The $a_k$ are uncorrelated across days, so (A3) holds. This *piecewise-constant acceleration* model is one of two standard choices; [Chapter 14](#ch14-sec-choosing-q) compares it with the other.

    **Initial condition.** On day 0, before the first weigh-in, you know your weight to about $\pm 1$ lb and have no idea of the rate beyond "within about $\pm 0.5$ lb/day": $\hat{\mathbf x}_0 = [155, 0]^\top$, $\mathbf P_0 = \operatorname{diag}(1, 0.25)$.

    The diet change is a single jump of the rate by $-0.4$ lb/day, not a stream of small zero-mean accelerations, so the model is deliberately imperfect, as every real model is. The sliders set the filter's $\sigma_a$ and $R$; the data always have $\sigma_v = 1$ lb.
    """)
    return


@app.cell
def bulk_data(np):
    # jb: include=false
    bulk_days = 28
    bulk_dt = 1.0
    _k = np.arange(0, bulk_days + 1)
    bulk_rate_true = np.where(_k < 15, 0.2, -0.2)  # r_k, lb/day (change from day k to k+1)
    bulk_x_true = np.empty(bulk_days + 1)  # x_k, lb, for k = 0, ..., 28
    bulk_x_true[0] = 154.8  # so that x_1 = 155, as in the Introduction
    for _i in range(1, bulk_days + 1):
        bulk_x_true[_i] = bulk_x_true[_i - 1] + bulk_rate_true[_i - 1] * bulk_dt
    # Same noise as the Introduction's weigh-ins (seed 2, rounded to 0.1 lb), so
    # days 1-15 reproduce the Introduction's data exactly.
    bulk_z = np.round(bulk_x_true[1:] + np.random.default_rng(2).normal(0.0, 1.0, bulk_days), 1)
    return bulk_days, bulk_dt, bulk_rate_true, bulk_x_true, bulk_z


@app.cell
def bulk_model(bulk_dt, np):
    # jb: include=false
    bulk_F = np.array([[1.0, bulk_dt], [0.0, 1.0]])
    bulk_H = np.array([[1.0, 0.0]])
    bulk_Gamma = np.array([[bulk_dt**2 / 2], [bulk_dt]])
    bulk_x0 = np.array([155.0, 0.0])
    bulk_P0 = np.diag([1.0, 0.25])
    return bulk_F, bulk_Gamma, bulk_H, bulk_P0, bulk_x0


@app.cell(hide_code=True)
def _(mo):
    sigma_a_slider = mo.ui.slider(
        steps=[0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0],
        value=0.05,
        label=r"filter's $\sigma_a$ (lb/day$^2$)",
        show_value=True,
    )
    r_slider = mo.ui.slider(
        steps=[0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 10.0],
        value=1.0,
        label=r"filter's $R$ (lb$^2$)",
        show_value=True,
    )
    return r_slider, sigma_a_slider


@app.cell(hide_code=True)
def bulk_interactive(
    bulk_F,
    bulk_Gamma,
    bulk_H,
    bulk_P0,
    bulk_days,
    bulk_rate_true,
    bulk_x0,
    bulk_x_true,
    bulk_z,
    graphic,
    kalman_filter,
    mo,
    np,
    plt,
    r_slider,
    sigma_a_slider,
):
    _Q = sigma_a_slider.value**2 * bulk_Gamma @ bulk_Gamma.T
    _R = np.array([[r_slider.value]])
    bulk_result = kalman_filter(bulk_z, bulk_F, bulk_H, _Q, _R, bulk_x0, bulk_P0)

    _days = np.arange(1, bulk_days + 1)
    _x = bulk_result["x"]
    _sd = np.sqrt(np.stack([bulk_result["P"][:, 0, 0], bulk_result["P"][:, 1, 1]], axis=1))
    _fig, (_ax1, _ax2) = plt.subplots(2, 1, figsize=(7.5, 6.5), sharex=True)
    _ax1.plot(np.arange(0, bulk_days + 1), bulk_x_true, color="black", lw=1.2, label="truth")
    _ax1.plot(_days, bulk_z, "o", mfc="none", mec="black", label="measurements")
    _ax1.plot(_days, bulk_result["x_pred"][:, 0], ":", color="red", label="predictions")
    _ax1.plot(_days, _x[:, 0], "-", color="C1", label="estimates")
    _ax1.fill_between(_days, _x[:, 0] - 2 * _sd[:, 0], _x[:, 0] + 2 * _sd[:, 0], color="C1", alpha=0.2, label=r"$\pm 2\sigma$")
    _ax1.set_ylabel("weight (lb)")
    _ax1.legend(loc="lower center", ncol=3, fontsize=8)
    _ax1.set_title("Weight", style="italic")
    _ax2.step(np.arange(0, bulk_days + 1), bulk_rate_true, where="post", color="black", lw=1.2, label="truth")
    _ax2.plot(_days, _x[:, 1], "-", color="C1", label="estimate")
    _ax2.fill_between(_days, _x[:, 1] - 2 * _sd[:, 1], _x[:, 1] + 2 * _sd[:, 1], color="C1", alpha=0.2, label=r"$\pm 2\sigma$")
    _ax2.axhline(0, color="gray", lw=0.6)
    _ax2.set_ylabel("rate (lb/day)")
    _ax2.set_xlabel("day")
    _ax2.set_ylim(-0.9, 0.9)
    _ax2.legend(loc="upper right", fontsize=8)
    _ax2.set_title("Rate of gain", style="italic")
    for _ax in (_ax1, _ax2):
        _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _fig.tight_layout()
    mo.vstack([mo.hstack([sigma_a_slider, r_slider], justify="start", gap=2), graphic(_fig)])
    return (bulk_result,)


@app.cell(hide_code=True)
def _(bulk_rate_true, bulk_result, mo, np):
    _K = bulk_result["K"][:, :, 0]
    _x = bulk_result["x"]
    _sd_r = np.sqrt(bulk_result["P"][:, 1, 1])
    _inside = np.mean(np.abs(_x[:, 1] - bulk_rate_true[1:]) <= 2 * _sd_r)
    mo.md(rf"""
    With these settings the filter estimates a rate of ${_x[13, 1]:+.3f} \pm {2 * _sd_r[13]:.3f}$ lb/day on day 14 (truth $+0.2$) and ${_x[-1, 1]:+.3f} \pm {2 * _sd_r[-1]:.3f}$ lb/day on day 28 (truth $-0.2$), where $\pm$ is two standard deviations. The true rate lies inside the $\pm 2\sigma$ band on {100 * _inside:.0f}% of the days. The gains went from $\mathbf K_1 = [{_K[0, 0]:.3f},\ {_K[0, 1]:.4f}]^\top$ on day 1 to $\mathbf K_{{28}} = [{_K[-1, 0]:.3f},\ {_K[-1, 1]:.4f}]^\top$ on day 28.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Things to try:

    - **Small $\sigma_a$** (say $0.005$) tells the filter that the rate hardly ever changes. The rate band shrinks, and after the diet change the estimated rate creeps toward the truth over weeks while the true rate sits far outside the band. This is the vector version of [Chapter 9](#ch9-thm-no-process-noise)'s observation that $Q = 0$ turns the filter into a running average that stops listening.
    - **Large $\sigma_a$** (say $0.5$) lets the rate change quickly, so the estimate can follow the cut within days, but every noisy reading now moves the rate estimate by tenths of a lb/day, and the $\pm 2\sigma$ band becomes so wide that it says little.
    - **Small $R$** makes the filter trust each reading; **large $R$** makes it trust its own predictions. The data, with true $\sigma_v = 1$ lb, do not change.
    - In every setting, the gains settle to constants within a few weeks. The section Alpha-Beta Revisited shows what those constants are.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch13-sec-observability -->
    ## Observability

    The bulking filter estimated a rate that the scale never measures. That worked because a rate leaves a trace in the weights: two different rates produce different weight sequences. [Chapter 11](#ch11-sec-two-unknowns-one-reading)'s tare offset is the opposite case: a heavier person on a scale with a smaller offset can produce exactly the same readings. Observability makes the difference precise.

    /// note | 📖 **Definition**
    <u>**Observability**</u>

    The property of a linear state-space model that, when all noise and control inputs are zero, the measurements $\mathbf z_1, \ldots, \mathbf z_N$ determine the state $\mathbf x_1$ uniquely for some $N \in \mathbb N^+$; that is, the linear map $\mathbf x_1 \mapsto (\mathbf z_1, \ldots, \mathbf z_N)$ is injective for some $N$. A model with this property is called *observable*.
    ///

    Setting the inputs to zero loses nothing: a known input adds a known vector to each $\mathbf z_k$, which can be subtracted. Setting the noise to zero is the point: if two different states produce the same noise-free measurements, they produce measurements with the same distribution, and no estimator can tell them apart from any amount of data.

    For a time-invariant model with no noise and no input, $\mathbf x_{1+i} = \mathbf F^i\mathbf x_1$, so $\mathbf z_{1+i} = \mathbf H\mathbf F^i\mathbf x_1$. Let $\mathcal N_j := \{\mathbf x \in \mathbb R^n : \mathbf H\mathbf F^i\mathbf x = \mathbf 0 \text{ for } 0 \le i < j\}$ be the set of states that produce $j$ zero measurements, with $\mathcal N_0 = \mathbb R^n$. Each $\mathcal N_j$ is a subspace (the null space of a matrix).

    /// admonition | 📐 **Lemma (The Null-Space Chain Stops by Step $n$)**
        attrs: {class: lemma, id: ch13-lem-the-null-space-chain-stops-by-step-n}
    $\mathcal N_0 \supseteq \mathcal N_1 \supseteq \mathcal N_2 \supseteq \cdots$, and $\mathcal N_j = \mathcal N_n$ for every $j \ge n$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    The inclusions hold because each $\mathcal N_{j+1}$ imposes one more condition than $\mathcal N_j$. Next, $\mathbf x \in \mathcal N_{j+1}$ if and only if $\mathbf H\mathbf x = \mathbf 0$ and $\mathbf F\mathbf x \in \mathcal N_j$, because $\mathbf H\mathbf F^i\mathbf x = \mathbf 0$ for $1 \le i \le j$ says exactly $\mathbf H\mathbf F^{i'}(\mathbf F\mathbf x) = \mathbf 0$ for $0 \le i' < j$. So if $\mathcal N_{j+1} = \mathcal N_j$ for some $j$, then
    $$\mathcal N_{j+2} = \{\mathbf x : \mathbf H\mathbf x = \mathbf 0,\ \mathbf F\mathbf x \in \mathcal N_{j+1}\} = \{\mathbf x : \mathbf H\mathbf x = \mathbf 0,\ \mathbf F\mathbf x \in \mathcal N_j\} = \mathcal N_{j+1},$$
    and by induction the chain is constant from $j$ on. It remains to find such a $j \le n$. A subspace properly contained in another has strictly smaller dimension ([Appendix D: Linear Independence, Basis, and Rank](#appd-sec-linear-independence-basis-and-rank)), and $\dim\mathcal N_0 = n$. If all of the first $n$ inclusions were proper, then $\dim\mathcal N_n \le 0$, so $\mathcal N_n = \{\mathbf 0\}$ and $\mathcal N_{n+1} = \mathcal N_n$ anyway. Either way some $j \le n$ has $\mathcal N_{j+1} = \mathcal N_j$, and then $\mathcal N_i = \mathcal N_n$ for all $i \ge n$. $\blacksquare$
    ///

    /// admonition | 📐 **Theorem (Rank Test for Observability)**
        attrs: {class: theorem, id: ch13-thm-rank-test-for-observability}
    A time-invariant linear state-space model is observable if and only if its *observability matrix*
    $$\mathcal O := \begin{bmatrix}\mathbf H \\ \mathbf H\mathbf F \\ \vdots \\ \mathbf H\mathbf F^{n-1}\end{bmatrix} \in \mathbb R^{nm\times n}$$
    has {term}`rank` $n$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    The map $\mathbf x_1 \mapsto (\mathbf z_1, \ldots, \mathbf z_N)$ is linear, so it is injective exactly when its null space, which is $\mathcal N_N$, is $\{\mathbf 0\}$ (if two states give equal outputs, their difference gives zero output). By the Lemma, $\mathcal N_N \supseteq \mathcal N_n$ for $N \le n$ and $\mathcal N_N = \mathcal N_n$ for $N \ge n$, so some $N$ works if and only if $\mathcal N_n = \{\mathbf 0\}$. And $\mathcal N_n$ is the null space of $\mathcal O$, which is $\{\mathbf 0\}$ exactly when the $n$ columns of $\mathcal O$ are linearly independent, that is, when $\operatorname{rank}\mathcal O = n$ (Appendix D). $\blacksquare$
    ///

    For a time-varying model the same argument without the Lemma shows: $\mathbf x_1$ is determined by $\mathbf z_1, \ldots, \mathbf z_N$ if and only if the stacked matrix with rows $\mathbf H_1$, $\mathbf H_2\mathbf F_2$, $\mathbf H_3\mathbf F_3\mathbf F_2$, …, $\mathbf H_N\mathbf F_N\cdots\mathbf F_2$ has rank $n$.

    **Bulking.** $\mathcal O = \begin{bmatrix}1 & 0 \\ 1 & \Delta t\end{bmatrix}$ has determinant $\Delta t \ne 0$, so rank 2: the model is observable, and the rate can be learned from weights alone.

    **Tare offset.** In Chapter 11 the scale reports raw counts $z = hx + c + v$ with $h = 20{,}000$ counts/lb, an offset $c$ near $85{,}000$ counts, and $\sigma_v = 20{,}000$ counts. Treat the unknown offset as a second constant state: $\mathbf x = [x, c]^\top$, $\mathbf F = \mathbf I$, $\mathbf H = [h,\ 1]$. Then
    $$\mathcal O = \begin{bmatrix} h & 1 \\ h & 1\end{bmatrix}$$
    has rank 1, so the model is **not** observable. The null space is spanned by $\mathbf d = [1, -h]^\top$: a person 1 lb heavier on a scale whose offset is 20,000 counts lower produces exactly the same readings, forever. The fix from Chapter 11 is to read the scale with the platform **empty** before you step on. Those readings have $\mathbf H_k = [0,\ 1]$, so the stacked matrix contains the rows $[0,\ 1]$ and $[h,\ 1]$ and has rank 2.

    The filter below sees 30 readings at 10 Hz. The first $n_e$ are taken with the platform empty; then you (155 lb) step on. Its prior is deliberately vague: $\hat{\mathbf x}_0 = [150\ \text{lb},\ 80{,}000\ \text{counts}]^\top$ with standard deviations of 20 lb and 50,000 counts.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    n_empty_slider = mo.ui.slider(
        start=0, stop=10, step=1, value=3, label=r"empty-platform readings $n_e$", show_value=True
    )
    return (n_empty_slider,)


@app.cell
def tare_setup(np):
    # jb: include=false
    tare_h = 20_000.0  # counts/lb
    tare_c = 85_000.0  # counts
    tare_sigma = 20_000.0  # counts
    tare_weight = 155.0  # lb
    tare_n = 30
    tare_noise = np.random.default_rng(5).normal(0.0, tare_sigma, tare_n)

    def tare_filter(n_empty, kf_update):
        """Constant state [weight, offset]; returns estimates and std devs."""
        _x = np.array([150.0, 80_000.0])
        _P = np.diag([20.0**2, 50_000.0**2])
        _R = np.array([[tare_sigma**2]])
        _est, _sd = [], []
        for _j in range(tare_n):
            _Hj = np.array([[0.0, 1.0]]) if _j < n_empty else np.array([[tare_h, 1.0]])
            _z = _Hj @ np.array([tare_weight, tare_c]) + tare_noise[_j]
            _x, _P, *_ = kf_update(_x, _P, _z, _Hj, _R)  # F = I, Q = 0: no predict step
            _est.append(_x.copy())
            _sd.append(np.sqrt(np.diag(_P)))
        return np.array(_est), np.array(_sd)

    return tare_filter, tare_n, tare_weight


@app.cell(hide_code=True)
def tare_interactive(
    graphic,
    kf_update,
    mo,
    n_empty_slider,
    np,
    plt,
    tare_filter,
    tare_n,
    tare_weight,
):
    _ne = n_empty_slider.value
    tare_est, tare_sd = tare_filter(_ne, kf_update)
    _est0, _sd0 = tare_filter(0, kf_update)
    _t = 0.1 * np.arange(1, tare_n + 1)
    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(10, 3.8))
    for _ax in (_ax1, _ax2):
        if _ne > 0:
            _ax.axvspan(0.05, 0.1 * _ne + 0.05, color="gray", alpha=0.15, label="platform empty")
    _ax1.axhline(tare_weight, color="black", lw=1.2, label="truth")
    _ax1.plot(_t, tare_est[:, 0], color="C1", label="estimate")
    _ax1.fill_between(_t, tare_est[:, 0] - 2 * tare_sd[:, 0], tare_est[:, 0] + 2 * tare_sd[:, 0], color="C1", alpha=0.2, label=r"$\pm 2\sigma$")
    _ax1.set_ylim(140, 170)
    _ax1.set_xlabel("time (s)")
    _ax1.set_ylabel("weight (lb)")
    _ax1.set_title("Weight estimate", style="italic")
    _ax1.legend(loc="upper right", fontsize=8)
    _ax2.plot(_t, _sd0[:, 0], "--", color="gray", label=r"$n_e = 0$ (unobservable)")
    _ax2.plot(_t, tare_sd[:, 0], color="C1", label=rf"$n_e = {_ne}$")
    _ax2.set_yscale("log")
    _ax2.set_xlabel("time (s)")
    _ax2.set_ylabel("standard deviation of weight (lb)")
    _ax2.set_title("Weight uncertainty", style="italic")
    _ax2.legend(loc="upper right", fontsize=8)
    for _ax in (_ax1, _ax2):
        _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _fig.tight_layout()
    mo.vstack([n_empty_slider, graphic(_fig)])
    return tare_est, tare_sd


@app.cell(hide_code=True)
def _(mo, n_empty_slider, tare_est, tare_sd):
    mo.md(rf"""
    After 3 s with $n_e = {n_empty_slider.value}$, the filter reports a weight of ${tare_est[-1, 0]:.2f} \pm {2 * tare_sd[-1, 0]:.2f}$ lb ($\pm 2\sigma$). With $n_e = 0$, the weight's standard deviation stalls near 2.5 lb no matter how long you stand there. The readings pin down $hx + c$ ever more precisely, but they say nothing about the split between $x$ and $c$, so that split stays as uncertain as the prior made it. A single empty reading breaks the tie, and more empty readings tighten it further.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **Observability is a yes-or-no property; information is a matter of degree.** A model can be observable and still learn a state very slowly when $\mathcal O$ is nearly rank deficient. Chapter 14 estimates an accelerometer bias that is observable but takes seconds to learn.
    - **Unobservable directions are never corrected.** The filter's covariance in an unobservable direction never shrinks below what the prior and the prediction step give it. If $\mathbf Q$ adds uncertainty in that direction, the covariance grows without bound. Part VI meets this for real: zero-velocity updates cannot observe the heading of a walking foot, so heading drift must be bounded by another sensor.
    - **The rank test assumes the model is right.** A state that is observable in the model but not in reality, for example because $\mathbf H$ is wrong, is "observed" incorrectly.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch13-sec-alpha-beta-revisited -->
    ## Alpha-Beta Revisited

    The Introduction built the alpha-beta filter by intuition. Here is its precise form.

    /// note | 📖 **Definition**
    <u>**Alpha-beta filter**</u>

    A filter for a scalar quantity that keeps an estimate $\hat x_k$ and an estimated change per step $\widehat{\Delta x}_{k+1}$ and, for constants $\alpha$ and $\beta$, computes for each step $k$
    $$\hat x_k^- := \hat x_{k-1} + \widehat{\Delta x}_k, \qquad \tilde y_k := z_k - \hat x_k^-, \qquad \hat x_k := \hat x_k^- + \alpha\,\tilde y_k, \qquad \widehat{\Delta x}_{k+1} := \widehat{\Delta x}_k + \beta\,\tilde y_k.$$
    ///

    /// admonition | 📐 **Theorem (The Alpha-Beta Filter Is a Constant-Gain Kalman Filter)**
        attrs: {class: theorem, id: ch13-thm-the-alpha-beta-filter-is-a-constant-gain-kalman-filter}
    Let $\mathbf F = \begin{bmatrix}1 & \Delta t \\ 0 & 1\end{bmatrix}$ and $\mathbf H = [1\ \ 0]$, and run the Kalman filter's mean equations $\hat{\mathbf x}_k^- = \mathbf F\hat{\mathbf x}_{k-1}$, $\hat{\mathbf x}_k = \hat{\mathbf x}_k^- + \mathbf K\tilde{\mathbf y}_k$ with a *constant* gain $\mathbf K = [\alpha,\ \beta/\Delta t]^\top$ in place of $\mathbf K_k$. Write $\hat{\mathbf x}_k = [\hat x_k, \hat r_k]^\top$ and $\widehat{\Delta x}_{k+1} := \hat r_k\Delta t$. Then $\hat x_k$ and $\widehat{\Delta x}_{k+1}$ satisfy exactly the alpha-beta recursion.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    The prediction is $\hat{\mathbf x}_k^- = [\hat x_{k-1} + \hat r_{k-1}\Delta t,\ \hat r_{k-1}]^\top = [\hat x_{k-1} + \widehat{\Delta x}_k,\ \hat r_{k-1}]^\top$, whose first entry is the alpha-beta prediction $\hat x_k^-$. The innovation $z_k - \mathbf H\hat{\mathbf x}_k^- = z_k - \hat x_k^-$ is the alpha-beta $\tilde y_k$. The update gives $\hat x_k = \hat x_k^- + \alpha\tilde y_k$ and $\hat r_k = \hat r_{k-1} + (\beta/\Delta t)\tilde y_k$; multiplying the latter by $\Delta t$ gives $\widehat{\Delta x}_{k+1} = \widehat{\Delta x}_k + \beta\tilde y_k$. $\blacksquare$
    ///

    So the alpha-beta filter is a Kalman filter whose gain has been frozen. The bulking example showed that the Kalman filter's own gains settle to constants. Freezing them at those limits gives the alpha-beta filter that is *optimal in steady state*: the vector version of [Chapter 9](#ch9-thm-the-steady-state-kalman-filter-is-an-ema)'s theorem that the steady-state scalar Kalman filter is an exponential moving average with $\alpha = K_\infty$.

    **The Riccati recursion.** Because the gains do not depend on the data, we can eliminate the update and write the predicted covariance in terms of itself:
    $$\mathbf P_{k+1}^- = \mathbf F\Big(\mathbf P_k^- - \mathbf P_k^-\mathbf H^\top\big(\mathbf H\mathbf P_k^-\mathbf H^\top + \mathbf R\big)^{-1}\mathbf H\mathbf P_k^-\Big)\mathbf F^\top + \mathbf Q.$$
    This is the (discrete-time) *Riccati recursion*. A fixed point solves the [discrete algebraic Riccati equation](https://en.wikipedia.org/wiki/Algebraic_Riccati_equation). Iterating the recursion until it stops changing is the simplest way to find the {term}`steady-state gain` $\mathbf K_\infty$.

    /// admonition | 📐 **Theorem (Convergence of the Riccati Recursion)**
        attrs: {class: theorem, id: ch13-thm-convergence-of-the-riccati-recursion}
    Suppose the model is time-invariant and observable, $\mathbf R$ is positive definite, and $\mathbf Q = \mathbf G\mathbf G^\top$ for a matrix $\mathbf G$ with $\operatorname{rank}[\mathbf G,\ \mathbf F\mathbf G,\ \ldots,\ \mathbf F^{n-1}\mathbf G] = n$ (the noise can push the state in every direction). Then for every symmetric positive semidefinite $\mathbf P_0$, the sequence $\mathbf P_k^-$ converges to the same limit $\mathbf P_\infty^-$, and therefore $\mathbf K_k$ converges to $\mathbf K_\infty = \mathbf P_\infty^-\mathbf H^\top(\mathbf H\mathbf P_\infty^-\mathbf H^\top + \mathbf R)^{-1}$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Not given here; this is a standard result of linear estimation theory. See, for example, @barshalom2002 [Ch. 5], which also proves that the resulting steady-state filter is stable.
    ///

    For the bulking model, observability was checked above, and with $\mathbf G = \sigma_a\boldsymbol\Gamma$,
    $$[\boldsymbol\Gamma,\ \mathbf F\boldsymbol\Gamma] = \begin{bmatrix}\tfrac12\Delta t^2 & \tfrac32\Delta t^2 \\ \Delta t & \Delta t\end{bmatrix}$$
    has determinant $-\Delta t^3 \ne 0$. So the gains converge, and the limit does not depend on $\mathbf P_0$. Two dimensionless numbers describe the limit: the gains $\alpha$ and $\beta$, and the **tracking index**
    $$\Lambda := \frac{\sigma_a\Delta t^2}{\sigma_v}, \qquad \sigma_v := \sqrt R,$$
    which compares how far an unpredictable acceleration moves the state in one step with the measurement noise.

    /// admonition | 📐 **Theorem (Steady-State Alpha-Beta Gains)**
        attrs: {class: theorem, id: ch13-thm-steady-state-alpha-beta-gains}
    For the model with $\mathbf F$ and $\mathbf H$ as above, $\mathbf Q = \sigma_a^2\boldsymbol\Gamma\boldsymbol\Gamma^\top$, $R = \sigma_v^2$, and $\sigma_a, \sigma_v, \Delta t > 0$, let $\mathbf K_\infty = [\alpha,\ \beta/\Delta t]^\top$ be the steady-state gain. Then $0 < \alpha < 1$, $\beta > 0$, and

    1. $\dfrac{\beta^2}{1 - \alpha} = \Lambda^2$;
    2. $\alpha = \sqrt{2\beta} - \dfrac{\beta}{2}$;
    3. the steady-state error covariance is $\mathbf P_\infty = \sigma_v^2\begin{bmatrix}\alpha & \beta/\Delta t \\ \beta/\Delta t & \dfrac{\beta(\alpha - \beta/2)}{(1 - \alpha)\Delta t^2}\end{bmatrix}$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Write $T := \Delta t$, $r := \sigma_v^2$, $q := \sigma_a^2$, and let $\mathbf M = \begin{bmatrix}m_{11} & m_{12} \\ m_{12} & m_{22}\end{bmatrix}$ be the steady-state predicted covariance, $\mathbf P = (\mathbf I - \mathbf K\mathbf H)\mathbf M$ the steady-state updated covariance, and $\mathbf K = [k_1, k_2]^\top$. Since $\mathbf S = m_{11} + r$, the gain is $k_1 = m_{11}/(m_{11} + r)$, $k_2 = m_{12}/(m_{11} + r)$, so $1 - k_1 = r/(m_{11} + r)$ and $m_{11} + r = r/(1 - k_1)$. Multiplying out $\mathbf P = (\mathbf I - \mathbf K\mathbf H)\mathbf M$:
    $$P_{11} = (1 - k_1)m_{11} = k_1r, \qquad P_{12} = (1 - k_1)m_{12} = k_2r, \qquad P_{22} = m_{22} - k_2m_{12}.$$
    The steady state also satisfies $\mathbf M = \mathbf F\mathbf P\mathbf F^\top + \mathbf Q$, which entry by entry reads

    - (a) $m_{22} = P_{22} + qT^2$,
    - (b) $m_{12} = P_{12} + TP_{22} + \tfrac12qT^3$,
    - (c) $m_{11} = P_{11} + 2TP_{12} + T^2P_{22} + \tfrac14qT^4$.

    *Signs.* By (b), $k_1m_{12} = m_{12} - P_{12} = TP_{22} + \tfrac12qT^3 > 0$, since $P_{22} \ge 0$ ($\mathbf P$ is a covariance matrix). Also $k_1 \ge 0$, so $k_1 > 0$ and $m_{12} > 0$, hence $k_2 > 0$. And $k_1 < 1$ because $r > 0$. With $\alpha = k_1$ and $\beta = k_2T$ this gives $0 < \alpha < 1$ and $\beta > 0$.

    *Part 1.* From (a) and $P_{22} = m_{22} - k_2m_{12}$: $k_2m_{12} = qT^2$. Substituting $m_{12} = k_2(m_{11} + r) = k_2r/(1 - k_1)$ gives $k_2^2r/(1 - k_1) = qT^2$, that is, $(k_2T)^2/(1 - k_1) = qT^4/r = \Lambda^2$.

    *Part 3.* $P_{11} = \alpha r$ and $P_{12} = (\beta/T)r$ were shown above. From (b), $TP_{22} = k_1m_{12} - \tfrac12qT^3 = \dfrac{k_1k_2r}{1 - k_1} - \dfrac{k_2^2rT}{2(1 - k_1)}$, using $qT^2 = k_2^2r/(1 - k_1)$ from Part 1. Dividing by $T$ and substituting $k_1 = \alpha$, $k_2 = \beta/T$ gives $P_{22} = r\beta(\alpha - \beta/2)/\big((1 - \alpha)T^2\big)$.

    *Part 2.* From (c), $k_1m_{11} = m_{11} - P_{11} = 2TP_{12} + T^2P_{22} + \tfrac14qT^4$. The left side is $k_1^2r/(1 - k_1)$. On the right, $T^2P_{22} = T\cdot TP_{22} = \dfrac{Tk_1k_2r}{1 - k_1} - \tfrac12qT^4$. Hence
    $$\frac{k_1^2r}{1 - k_1} = 2Tk_2r + \frac{Tk_1k_2r}{1 - k_1} - \tfrac14qT^4.$$
    Multiply by $(1 - k_1)/r$ and use $qT^4(1 - k_1)/r = \Lambda^2(1 - \alpha) = \beta^2$ (Part 1):
    $$\alpha^2 = 2\beta(1 - \alpha) + \alpha\beta - \tfrac14\beta^2, \quad\text{that is,}\quad \big(\alpha + \tfrac12\beta\big)^2 = 2\beta.$$
    Since $\alpha + \beta/2 > 0$, taking the positive square root gives $\alpha = \sqrt{2\beta} - \beta/2$. $\blacksquare$
    ///

    Solving relations 1 and 2 for $\alpha$ and $\beta$ gives the closed form published by @kalata1984:
    $$\alpha = -\frac{\Lambda^2 + 8\Lambda - (\Lambda + 4)\sqrt{\Lambda^2 + 8\Lambda}}{8}, \qquad \beta = \frac{\Lambda^2 + 4\Lambda - \Lambda\sqrt{\Lambda^2 + 8\Lambda}}{4}.$$
    You can confirm by substitution that these satisfy relations 1 and 2. The table compares them with the gains reached by iterating the Riccati recursion 3,000 times from $\mathbf P_0 = 10^3\,\mathbf I$.
    """)
    return


@app.cell
def kalata_check(np):
    # jb: include=false
    def kalata_gains(lam):
        _root = np.sqrt(lam**2 + 8 * lam)
        return -(lam**2 + 8 * lam - (lam + 4) * _root) / 8, (lam**2 + 4 * lam - lam * _root) / 4

    def riccati_gains(sigma_a, r, dt, steps, P0):
        """Iterate the Riccati recursion for the constant-rate model.

        sigma_a may be an array (one model per entry); returns gains of shape (steps, len, 2).
        """
        _sa = np.atleast_1d(np.asarray(sigma_a, float))
        _F = np.array([[1.0, dt], [0.0, 1.0]])
        _G = np.array([dt**2 / 2, dt])
        _Q = _sa[:, None, None] ** 2 * np.outer(_G, _G)[None]
        _P = np.broadcast_to(P0, (_sa.size, 2, 2)).copy()
        _gains = np.empty((steps, _sa.size, 2))
        for _k in range(steps):
            _Pm = _F @ _P @ _F.T + _Q
            _S = _Pm[:, 0, 0] + r
            _K = _Pm[:, :, 0] / _S[:, None]
            _P = _Pm - _K[:, :, None] * _Pm[:, None, 0, :]  # (I - K H) P^-
            _gains[_k] = _K
        return _gains

    kalata_lams = np.array([0.01, 0.05, 0.1, 0.5, 1.0, 10.0])
    _g = riccati_gains(kalata_lams, 1.0, 1.0, 3000, 1e3 * np.eye(2))[-1]
    kalata_table = [
        (_lam, _g[_i, 0], _g[_i, 1], *kalata_gains(_lam))
        for _i, _lam in enumerate(kalata_lams)
    ]
    return kalata_gains, kalata_lams, kalata_table, riccati_gains


@app.cell(hide_code=True)
def _(kalata_table, mo):
    _lines = [
        r"| $\Lambda$ | $\alpha$ (Riccati) | $\alpha$ (Kalata) | $\beta$ (Riccati) | $\beta$ (Kalata) | $\beta^2/(1-\alpha) - \Lambda^2$ | $\sqrt{2\beta} - \beta/2 - \alpha$ |",
        "|:---|:---:|:---:|:---:|:---:|:---:|:---:|",
    ]
    for _lam, _a_r, _b_r, _a_k, _b_k in kalata_table:
        _lines.append(
            f"| {_lam:g} | {_a_r:.8f} | {_a_k:.8f} | {_b_r:.8f} | {_b_k:.8f} "
            f"| {_b_r**2 / (1 - _a_r) - _lam**2:.1e} | {(2 * _b_r) ** 0.5 - _b_r / 2 - _a_r:.1e} |"
        )
    _lines += [
        "",
        "(Here $\\sigma_v = 1$ and $\\Delta t = 1$, so $\\sigma_a = \\Lambda$; the gains depend only on $\\Lambda$.) "
        "The two columns agree to all printed digits, and the last two columns check relations 1 and 2 directly.",
    ]
    mo.md("\n".join(_lines))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The sliders from the bulking example also drive the figure below. On the left, the Kalman gains of the bulking filter, expressed as $\alpha_k := K_{k,1}$ and $\beta_k := K_{k,2}\,\Delta t$, settle onto Kalata's steady-state values (dashed). On the right, Kalata's formulas are drawn as curves over five decades of $\Lambda$, the Riccati results from the table as dots, and your current setting as a star.
    """)
    return


@app.cell(hide_code=True)
def alpha_beta_interactive(
    bulk_P0,
    bulk_dt,
    graphic,
    kalata_gains,
    kalata_lams,
    kalata_table,
    mo,
    np,
    plt,
    r_slider,
    riccati_gains,
    sigma_a_slider,
):
    _sa, _r = sigma_a_slider.value, r_slider.value
    ab_lambda = _sa * bulk_dt**2 / np.sqrt(_r)
    ab_alpha_k, ab_beta_k = kalata_gains(ab_lambda)
    _steps = 100
    _g = riccati_gains(_sa, _r, bulk_dt, _steps, bulk_P0)[:, 0, :]
    ab_alpha_riccati, ab_beta_riccati = _g[-1, 0], _g[-1, 1] * bulk_dt

    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(10, 3.8))
    _k = np.arange(1, _steps + 1)
    _ax1.plot(_k, _g[:, 0], color="C1", label=r"$\alpha_k$")
    _ax1.plot(_k, _g[:, 1] * bulk_dt, color="C0", label=r"$\beta_k$")
    _ax1.axhline(ab_alpha_k, color="C1", ls="--", lw=0.9, label=r"Kalata $\alpha$")
    _ax1.axhline(ab_beta_k, color="C0", ls="--", lw=0.9, label=r"Kalata $\beta$")
    _ax1.set_yscale("log")
    _ax1.set_xlabel("day $k$")
    _ax1.set_ylabel("gain")
    _ax1.set_title(rf"Kalman gains, $\Lambda = {ab_lambda:.3g}$", style="italic")
    _ax1.legend(fontsize=8, loc="upper right")
    _lam = np.logspace(-3, 2, 300)
    _a, _b = kalata_gains(_lam)
    _ax2.plot(_lam, _a, color="C1", label=r"$\alpha$ (Kalata)")
    _ax2.plot(_lam, _b, color="C0", label=r"$\beta$ (Kalata)")
    _tab = np.array(kalata_table)
    _ax2.plot(_tab[:, 0], _tab[:, 1], "o", mfc="none", mec="C1", label=r"$\alpha$ (Riccati)")
    _ax2.plot(_tab[:, 0], _tab[:, 2], "o", mfc="none", mec="C0", label=r"$\beta$ (Riccati)")
    _ax2.plot([ab_lambda, ab_lambda], [ab_alpha_k, ab_beta_k], "*", color="black", ms=10, label="current setting")
    _ax2.set_xscale("log")
    _ax2.set_yscale("log")
    _ax2.set_xlabel(r"tracking index $\Lambda$")
    _ax2.set_ylabel("steady-state gain")
    _ax2.set_title("Steady-state gains", style="italic")
    _ax2.legend(fontsize=8, loc="lower right")
    for _ax in (_ax1, _ax2):
        _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _fig.tight_layout()
    mo.vstack([mo.hstack([sigma_a_slider, r_slider], justify="start", gap=2), graphic(_fig)])
    return ab_alpha_k, ab_alpha_riccati, ab_beta_k, ab_beta_riccati, ab_lambda


@app.cell(hide_code=True)
def _(
    ab_alpha_k,
    ab_alpha_riccati,
    ab_beta_k,
    ab_beta_riccati,
    ab_lambda,
    mo,
    r_slider,
    sigma_a_slider,
):
    mo.md(rf"""
    With $\sigma_a = {sigma_a_slider.value:g}$ lb/day$^2$ and $R = {r_slider.value:g}$ lb$^2$, the tracking index is $\Lambda = {ab_lambda:.4g}$. Kalata's formulas give $\alpha = {ab_alpha_k:.4f}$ and $\beta = {ab_beta_k:.4f}$; after 100 days the Kalman filter's own gains are $\alpha_{{100}} = {ab_alpha_riccati:.4f}$ and $\beta_{{100}} = {ab_beta_riccati:.4f}$. (For very small $\Lambda$ the gains are still falling after 100 days; the theorem only promises convergence in the limit.) By Part 3 of the theorem, the steady-state filter knows your weight to within one standard deviation of $\sigma_v\sqrt\alpha = {(r_slider.value * ab_alpha_k) ** 0.5:.2f}$ lb, compared with $\sigma_v = {r_slider.value ** 0.5:.2f}$ lb for a single reading. In the Introduction you picked $\alpha$ and $\beta$ with sliders; now they follow from the noise levels alone.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **Steady state only.** The frozen gains are optimal only after the Kalman filter's transient has died out. Early on, the Kalman filter uses *larger* gains (it knows it does not know much yet), so an alpha-beta filter started from a poor guess converges more slowly than the Kalman filter would.
    - **The process-noise model matters.** Kalata's relations assume the piecewise-constant acceleration $\mathbf Q$ used here. With the continuous white-noise acceleration $\mathbf Q$ of [Chapter 14](#ch14-sec-continuous-white-noise-acceleration), the steady-state gains satisfy different relations; see @barshalom2002 [Ch. 6].
    - **Regular sampling and a position-only measurement.** The relations assume a fixed $\Delta t$ and $\mathbf H = [1\ \ 0]$. With irregular or missing samples, the Kalman filter's time-varying gains adapt; frozen gains do not.
    - **Model violations still hurt.** The diet change in the example is not a small white acceleration. Neither the Kalman filter nor its frozen version handles a sudden jump optimally; Chapter 14 shows what happens when $\mathbf Q$ is too small for such a maneuver.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch13-sec-summary -->
    ## Summary

    - A **linear state-space model** $\mathbf x_k = \mathbf F\mathbf x_{k-1} + \mathbf B\mathbf u_k + \mathbf w_k$, $\mathbf z_k = \mathbf H\mathbf x_k + \mathbf v_k$, with zero-mean, white, mutually uncorrelated noises of covariances $\mathbf Q$ and $\mathbf R$, is all the Kalman filter needs. No Gaussian assumption is required for its optimality among linear filters.
    - **Predict:** $\hat{\mathbf x}_k^- = \mathbf F\hat{\mathbf x}_{k-1} + \mathbf B\mathbf u_k$ and $\mathbf P_k^- = \mathbf F\mathbf P_{k-1}\mathbf F^\top + \mathbf Q$.
    - **Update with any gain:** the estimate is unbiased, and the **Joseph form** $(\mathbf I - \mathbf K\mathbf H)\mathbf P^-(\mathbf I - \mathbf K\mathbf H)^\top + \mathbf K\mathbf R\mathbf K^\top$ is its exact error covariance.
    - **The Kalman gain** $\mathbf K = \mathbf P^-\mathbf H^\top\mathbf S^{-1}$, with $\mathbf S = \mathbf H\mathbf P^-\mathbf H^\top + \mathbf R$, minimizes the trace of the error covariance, and with it the error variance of every linear combination of state components. Only at this gain does the covariance simplify to $(\mathbf I - \mathbf K\mathbf H)\mathbf P^-$.
    - **Gaussian conditioning** gives the same update. Under Gaussian assumptions the Kalman filter computes the conditional mean, the best estimator of any form.
    - **Observability:** a time-invariant model is observable if and only if $[\mathbf H; \mathbf H\mathbf F; \ldots; \mathbf H\mathbf F^{n-1}]$ has rank $n$. Unobservable directions, like the split between weight and tare offset, are never corrected by measurements.
    - **The alpha-beta filter** is the Kalman filter for a constant-rate model with its gain frozen. Freezing it at the steady-state gain gives $\alpha$ and $\beta$ as functions of the tracking index $\Lambda = \sigma_a\Delta t^2/\sigma_v$ alone (Kalata's relations).

    <!-- label: ch13-sec-whats-next -->
    ## What's Next

    The derivation assumed that $\mathbf Q$, $\mathbf R$, $\hat{\mathbf x}_0$, and $\mathbf P_0$ are known, that a measurement arrives at every step, and that the arithmetic is exact. [Chapter 14](ch14_kalman_filters_in_practice.md) drops these assumptions one by one: how to initialize the filter and choose $\mathbf Q$, how to handle measurements that are missing, late, or arrive at different rates, how to fuse a 10 Hz position sensor with a 100 Hz accelerometer, how to reject outliers, how to *test* whether a filter's covariance tells the truth, and how to keep it numerically healthy.
    """)
    return


if __name__ == "__main__":
    app.run()
