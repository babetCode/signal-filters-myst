# /// script
# dependencies = [
#     "marimo>=0.25.1",
#     "matplotlib==3.11.2",
#     "numpy==2.5.3",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="10. Process Models", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "Predicting the Next State"
    description: "Process models with known control inputs, such as daily energy intake, and how they sharpen the Kalman filter's prediction."
    label: ch10
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// important | 🔗 **Prerequisites**
    - [Introduction](#intro): [the bulking example](#intro-sec-alpha-beta-filter), the {term}`prediction` $\hat x_k^-$, and [the alpha-beta filter](#intro-sec-beta-weighting-term).
    - [Chapter 2](#ch2): [proof by induction](#ch2-thm-induction).
    - [Chapter 6](#ch6): [linearity of expectation](#ch6-thm-linearity-and-positivity-of-expectation), $\operatorname{Var}(aX + b) = a^2\operatorname{Var}(X)$, [the variance of a sum](#ch6-sec-variance-of-sums), and the fact that [independent random variables are uncorrelated](#ch6-thm-independent-implies-uncorrelated).
    - [Chapter 7](#ch7): the {term}`estimation error` $e_k = \hat x_k - x_k$ and the {term}`optimal gain` $K_k = P_k^-/(P_k^- + R)$ with $P_k = (1 - K_k)P_k^-$.
    - [Chapter 9](#ch9): [process noise](#ch9-sec-process-noise), [the random-walk model](#ch9-sec-process-noise), {term}`white noise`, [the scalar Kalman filter](#ch9-sec-the-scalar-kalman-filter), the {term}`innovation variance` $S_k = P_k^- + R$, the fact that [innovations are uncorrelated over time](#ch9-thm-properties-of-the-innovations), and the {term}`normalized innovation squared`.
    - [Appendix C: Derivatives](#appc-sec-derivatives), [Appendix C: The Mean Value Theorem and Extrema](#appc-sec-the-mean-value-theorem-and-extrema), [Appendix C: Taylor's Theorem](#appc-sec-taylors-theorem), [Appendix C: Exponential and Logarithm](#appc-sec-exponential-and-logarithm), and [Appendix C: Linear Differential Equations](#appc-sec-linear-differential-equations): only for the section on continuous-time models.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In [Chapter 9](#ch9-sec-process-noise) the Kalman filter predicted each new weight with the random-walk model: tomorrow's weight is today's weight plus an expected change $\Delta x_k$ plus {term}`process noise`. We never asked where $\Delta x_k$ comes from. When you are bulking, your weight changes *because* you eat more than you burn, and you may well know how much you ate. This chapter shows how to put that knowledge into the prediction.

    The rule that turns the previous state, and everything we know about outside influences, into a prediction of the next state is called a **process model**. Whatever the model gets wrong becomes process noise. So a better model means a smaller $Q$, a prediction the filter can trust more, and less need to trade noise against lag. A *wrong* model, on the other hand, quietly biases every estimate. We therefore also need a way to tell, from data alone, whether a model is wrong.

    /// attention | 🗝️ **Key Idea**
    A process model predicts the next state from the current state and the known inputs. Everything the model does not capture becomes process noise. A good model makes $Q$ small; a biased model makes the innovations stop looking like white noise.
    ///

    We start by making the words *system*, *state*, and *input* precise, because a model can only be as good as the choice of what goes into the state. Then we generalize the scalar Kalman filter from the random walk to every linear model, build an energy-balance model for the bulking example, compare it with the random walk, convert continuous-time physics into discrete-time models, and finally learn to test a model using nothing but its innovations.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch10-sec-systems-states-and-inputs -->
    ## Systems, States, and Inputs

    To predict tomorrow's weight, we first have to decide what we are describing and what counts as an outside influence.

    /// note | 📖 **Definition**
    <u>**System**</u>

    A part of the world that we choose to study, specified by a boundary that decides, for every object or quantity under consideration, whether it belongs to the system (is *inside*) or to the system's *environment* (is *outside*).
    ///

    For the bulking example the system is your body. Your weight, fat mass, muscle mass, glycogen, and body water are inside; the food on your plate, the weather, and your gym's opening hours are outside. The boundary is a choice, not a fact of nature: we could have drawn it around your fat mass alone, or around you and your kitchen. Different boundaries lead to different models.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Outside quantities matter when they push the system around. Some of them we know, and some we don't.

    /// note | 📖 **Definition**
    <u>**Control input**</u>

    A quantity outside a system that affects how the system's state changes, and whose value at each step is known to whoever is making the prediction, because it was either chosen (commanded) or measured.
    ///

    The energy you eat on day $k$, written $u_k$ (in kcal) and read from a food log, is a control input to your body. The temperature of your apartment also changes how much energy you burn, but you don't record it; in our model its effect will be part of the process noise. The test is *knowledge*, not *influence*: an outside influence whose value we don't know is not an input, it is noise. The word "control" is historical. It comes from control engineering, where the input is the command an engineer chooses; in filtering the input only has to be known, and nobody has to choose it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The most important modeling decision is which numbers to keep track of. We want a summary of the present that is good enough to predict the future, so that the past can be forgotten. That is exactly what makes a recursive filter possible: each new estimate is computed from the previous estimate and the new data only, as in the recursion theorem of [Chapter 2](#ch2-thm-recursion).

    /// note | 📖 **Definition**
    <u>**System state**</u>

    A list of numbers $x_k$, defined at every step $k$, is a *state* of a system iff (1) every quantity of the system we care about at step $k$ is a function of $x_k$, and (2) for all steps $j > k$, the value of $x_j$ (or, if the system involves randomness, its conditional distribution) is determined by $x_k$ together with the control inputs $u_{k+1}, \ldots, u_j$, and would not change if we also knew $x_0, \ldots, x_{k-1}$ or any other information about the system's past.
    ///

    Some examples:

    1. **A constant weight on a scale** ([Chapter 7](#ch7-thm-optimal-gains-for-a-constant)). The weight itself is a state: it never changes, so knowing it now determines it forever.
    2. **Bulking with a food log.** Under the energy-balance model built below, today's weight together with the food you will log determines the distribution of every future weight. Weight alone is a state.
    3. **A rolling cart.** Its position alone is *not* a state: two carts at the same position, one moving and one at rest, end up in different places. Position and velocity together are a state.
    4. **Bulking without a food log, but with a steady rate of gain.** Two people who weigh the same today but gain at different rates will weigh different amounts next week, so weight alone is not a state; weight and rate together are. We return to this case at the end of the chapter.

    A state is a property of a *model*, not of the body itself: the same body has a one-number state under one model and a two-number state under another. Since every extra number is something more to estimate, we normally choose the shortest list that works, and "the state" means the list chosen in the model at hand. A state usually contains numbers we cannot measure directly. Estimating them is the filter's job.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Once we have a state, a model of the system is a rule for how the state moves.

    /// note | 📖 **Definition**
    <u>**Process model**</u>

    A mathematical rule that determines how a system's state evolves, given its control inputs. In discrete time it is an equation
    $$x_k = f(x_{k-1}, u_k, w_k) \quad \text{for every step } k \ge 1,$$
    where $f$ is a known {term}`function` and $w_k$ is a {term}`random variable` with a specified distribution (the {term}`process noise`). In continuous time it is a {term}`differential equation` for the state $x(t)$.
    ///

    Chapter 9's random-walk model $x_k = x_{k-1} + \Delta x_k + w_k$ is a process model, with the expected change $\Delta x_k$ playing the role of a known input. The constant-weight model of Chapter 7 is the process model $x_k = x_{k-1}$, which has no noise at all. That distinction has a name.

    /// note | 📖 **Definition**
    <u>**Deterministic**</u>

    A process model is *deterministic* iff it contains no random term: the state at each step is a fixed function of the previous state and the input, so the initial state and the inputs determine every later state exactly. A process model that is not deterministic is called *stochastic*.
    ///

    Being deterministic is a property of a model, not of the world. In practice we write a deterministic model of how the state *would* move if there were no unknown influences, and then add process noise to account for everything else.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch10-sec-linear-process-models -->
    ## Linear Process Models

    The Kalman filter of Chapter 9 relied on a model in which the new state is the old state plus known and random terms. The natural generalization lets the old state be scaled.

    /// note | 📖 **Definition**
    <u>**Linear system**</u>

    A system whose process model has the form
    $$x_k = a_k\,x_{k-1} + b_k\,u_k + w_k \quad \text{for every step } k \ge 1,$$
    where the coefficients $a_k$ and $b_k$ are known numbers that do not depend on the state, the inputs, or the noise. In continuous time the corresponding form is $\dot x(t) = \lambda(t)\,x(t) + g(t)\,u(t)$ plus noise. (Part III replaces the numbers by matrices.)
    ///

    The random walk is the case $a_k = b_k = 1$ with $u_k = \Delta x_k$. The constant model is $a_k = 1$, $b_k = 0$, $w_k = 0$. A model such as $x_k = x_{k-1}^2 + w_k$ is not linear, because the new state depends on the square of the old one; [Chapter 15](#ch15) deals with such models.

    The name comes from the following property, which is what makes linear systems easy to analyze: responses to different causes simply add up.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// admonition | 📐 **Theorem (Superposition)**
        attrs: {class: theorem, id: ch10-thm-superposition}
    Consider the deterministic linear model $x_k = a_k x_{k-1} + b_k u_k$. Suppose the initial state $x_0$ with inputs $u_1, u_2, \ldots$ produces the states $x_1, x_2, \ldots$, and the initial state $x_0'$ with inputs $u_1', u_2', \ldots$ produces $x_1', x_2', \ldots$. Then for all numbers $\alpha$ and $\beta$, the initial state $\alpha x_0 + \beta x_0'$ with inputs $\alpha u_k + \beta u_k'$ produces the states $\alpha x_k + \beta x_k'$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Let $y_0 := \alpha x_0 + \beta x_0'$ and $y_k := a_k y_{k-1} + b_k(\alpha u_k + \beta u_k')$ be the states produced by the combined initial state and inputs. We show $y_k = \alpha x_k + \beta x_k'$ by induction on $k$. For $k = 0$ it holds by definition. If it holds for $k - 1$, then
    $$y_k = a_k(\alpha x_{k-1} + \beta x_{k-1}') + b_k(\alpha u_k + \beta u_k') = \alpha(a_k x_{k-1} + b_k u_k) + \beta(a_k x_{k-1}' + b_k u_k') = \alpha x_k + \beta x_k'. \;\blacksquare$$
    ///

    When the coefficients do not change with $k$ we can also write the solution down explicitly.

    /// admonition | 📐 **Lemma (Solution of a Linear Model)**
        attrs: {class: lemma, id: ch10-lem-solution-of-a-linear-model}
    If $x_k = a x_{k-1} + b u_k + w_k$ for every $k \ge 1$, with constant $a$ and $b$, then for every $k \ge 0$
    $$x_k = a^k x_0 + \sum_{j=1}^{k} a^{k-j}\,(b u_j + w_j).$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    For $k = 0$ the sum is empty and the formula reads $x_0 = x_0$. If the formula holds for $k - 1$, then
    $$x_k = a\Big(a^{k-1}x_0 + \sum_{j=1}^{k-1} a^{k-1-j}(b u_j + w_j)\Big) + b u_k + w_k = a^k x_0 + \sum_{j=1}^{k} a^{k-j}(b u_j + w_j),$$
    since the last term is the $j = k$ term of the sum ($a^0 = 1$). $\blacksquare$
    ///

    The factor $a^{k-j}$ says how much an input or a disturbance from step $j$ still matters at step $k$. If $|a| < 1$ the system gradually forgets its past; if $a = 1$ (the random walk) every disturbance persists forever; if $|a| > 1$ old disturbances grow.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch10-sec-predicting-with-a-linear-model -->
    ### Predicting with a Linear Model

    Now let the estimate $\hat x_{k-1}$ of $x_{k-1}$ have the {term}`estimation error` $e_{k-1} := \hat x_{k-1} - x_{k-1}$ with mean $0$ and {term}`error variance` $P_{k-1}$, and suppose the state evolves as
    $$x_k = a\,x_{k-1} + b\,u_k + w_k,$$
    under three assumptions:

    - **(A1)** the numbers $a$, $b$, and $u_k$ are known;
    - **(A2)** the process noise $w_k$ has mean $0$ and variance $Q$;
    - **(A3)** $w_k$ is {term}`uncorrelated` with $e_{k-1}$.

    (A3) holds automatically if $w_k$ is independent of the initial state, of the earlier process noise $w_1, \ldots, w_{k-1}$, and of the measurement noise $v_1, \ldots, v_{k-1}$. The reason is that $e_{k-1}$ is computed from exactly those quantities, so it is independent of $w_k$, and independent random variables are uncorrelated ([Chapter 6](#ch6-thm-independent-implies-uncorrelated)). This is what we get when the process noise is {term}`white noise` independent of everything else.

    We drop the subscripts on $a$ and $b$ only to keep the notation light: the theorem below uses one step at a time, so it holds unchanged for time-varying coefficients.

    /// admonition | 📐 **Theorem (Linear Prediction)**
        attrs: {class: theorem, id: ch10-thm-linear-prediction}
    Under (A1)–(A3), with $\mathbb E[e_{k-1}] = 0$ and $\operatorname{Var}(e_{k-1}) = P_{k-1}$:

    1. The prediction $\hat x_k^- := a\,\hat x_{k-1} + b\,u_k$ has prediction error $e_k^- := \hat x_k^- - x_k$ with mean $0$ and variance
    $$P_k^- = a^2 P_{k-1} + Q.$$
    2. Among all predictions of the form $\theta_1\hat x_{k-1} + \theta_2 u_k + \theta_3$ with numbers $\theta_1, \theta_2, \theta_3$, it is the only one whose error has mean $0$ whatever the mean of $x_{k-1}$ and whatever the input $u_k$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    1. Subtracting the process model from the prediction,
    $$e_k^- = a\,\hat x_{k-1} + b\,u_k - (a\,x_{k-1} + b\,u_k + w_k) = a\,e_{k-1} - w_k.$$
    By linearity of expectation, $\mathbb E[e_k^-] = a\cdot 0 - 0 = 0$. By the rule for the variance of a sum ([Chapter 6](#ch6-thm-variance-of-a-linear-combination)),
    $$\operatorname{Var}(e_k^-) = a^2\operatorname{Var}(e_{k-1}) + \operatorname{Var}(w_k) - 2a\operatorname{Cov}(e_{k-1}, w_k) = a^2 P_{k-1} + Q,$$
    because the covariance is $0$ by (A3).

    2. Write $\hat x_{k-1} = x_{k-1} + e_{k-1}$. The error of $\theta_1\hat x_{k-1} + \theta_2 u_k + \theta_3$ is
    $$\theta_1 e_{k-1} + (\theta_1 - a)\,x_{k-1} + (\theta_2 - b)\,u_k + \theta_3 - w_k,$$
    with mean $(\theta_1 - a)\,\mathbb E[x_{k-1}] + (\theta_2 - b)\,u_k + \theta_3$. If this is $0$ for every value of $\mathbb E[x_{k-1}]$ and $u_k$, then taking both equal to $0$ gives $\theta_3 = 0$; then taking $\mathbb E[x_{k-1}] = 1$, $u_k = 0$ gives $\theta_1 = a$; then taking $u_k = 1$ gives $\theta_2 = b$. Conversely, $\theta_1 = a$, $\theta_2 = b$, $\theta_3 = 0$ gives mean $0$ by part 1. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **(A1) fails: the coefficients or the input are not known exactly.** Then the prediction uses the wrong numbers. If the error is random and unbiased (for example, an imperfect food log), move it into $w_k$ and increase $Q$ accordingly; the next section does exactly this. If the error is systematic (for example, a wrong value of $a$), the prediction is biased, as in the next bullet.
    - **(A2) fails: the process noise has a nonzero mean $\mu_w$.** Then $\mathbb E[e_k^-] = a\,\mathbb E[e_{k-1}] - \mu_w \neq 0$. The bias enters at every step, so the estimate lags behind the truth, just like the exponential moving average lags behind a ramp ([Chapter 6](#ch6-thm-ema-on-a-ramp)). The last section of this chapter shows how to detect this from the innovations.
    - **(A3) fails: the process noise is correlated with past errors.** This happens when the same unmodeled effect pushes the state on several consecutive steps, so that $w_k$ is correlated with $w_{k-1}$. Then $P_k^-$ is wrong (usually too small), and the innovations become correlated in time.
    - **$Q$ is wrong.** The prediction is still unbiased, but the filter weighs it incorrectly: too small a $Q$ makes the filter overconfident and slow to follow real changes; too large a $Q$ makes it follow the measurement noise ([Chapter 9](#ch9-sec-the-scale-with-a-shifting-load)).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The variance recursion also tells us how fast a prediction goes stale when no measurements arrive at all, which is the situation on every day you skip the scale.

    /// admonition | 📐 **Corollary (Prediction Without Measurements)**
        attrs: {class: corollary, id: ch10-cor-prediction-without-measurements}
    If no measurement is incorporated, so that $P_k = P_k^- = a^2 P_{k-1} + Q$ for every $k$, with $Q > 0$ and $P_0 \ge 0$, then:

    1. if $|a| < 1$, $P_k \to Q/(1 - a^2)$ as $k \to \infty$;
    2. if $|a| = 1$, $P_k = P_0 + kQ$ grows without bound, linearly;
    3. if $|a| > 1$, $P_k \ge a^{2(k-1)} Q$ for every $k \ge 1$, so it grows without bound, exponentially.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    1. Let $P^* := Q/(1 - a^2)$, which satisfies $P^* = a^2 P^* + Q$. Subtracting, $P_k - P^* = a^2(P_{k-1} - P^*)$, so by induction $P_k - P^* = a^{2k}(P_0 - P^*) \to 0$ because $0 \le a^2 < 1$ ([Appendix C: Sequences and Limits](#appc-sec-sequences-and-limits)).
    2. With $a^2 = 1$ the recursion reads $P_k = P_{k-1} + Q$; induct.
    3. The recursion $P_k = a^2 P_{k-1} + Q$ has the form of the [Solution of a Linear Model lemma](#ch10-lem-solution-of-a-linear-model) (with $a^2$ in place of $a$ and $Q$ in place of $b u_j + w_j$), so $P_k = a^{2k}P_0 + \sum_{j=1}^{k} a^{2(k-j)} Q$. Every term is nonnegative, and the $j = 1$ term is $a^{2(k-1)}Q$. $\blacksquare$
    ///

    In Chapter 9's random walk ($a = 1$) the prediction variance grows by $Q$ every day without a weigh-in. A model with $|a| < 1$ is pulled back toward an equilibrium, so its prediction uncertainty levels off instead, *provided the model is right*.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch10-sec-the-kalman-filter-with-a-process-model -->
    ### The Kalman Filter with a Process Model

    The update step of Chapter 9 uses only the prediction $\hat x_k^-$, its variance $P_k^-$, and the measurement $z_k = x_k + v_k$; it does not care how the prediction was made. So the scalar {term}`Kalman filter` for a linear process model is Chapter 9's filter with a new prediction step:

    $$
    \begin{aligned}
    \text{predict:}\quad & \hat x_k^- = a\,\hat x_{k-1} + b\,u_k, & P_k^- &= a^2 P_{k-1} + Q,\\
    \text{update:}\quad & K_k = \frac{P_k^-}{P_k^- + R}, & \hat x_k &= \hat x_k^- + K_k\,(z_k - \hat x_k^-), \qquad P_k = (1 - K_k)\,P_k^-.
    \end{aligned}
    $$

    The bulking model below also has a known constant term $c$ in $x_k = a x_{k-1} + b u_k + c + w_k$. A known constant changes the prediction by $c$ and, having variance $0$, leaves $P_k^-$ unchanged (repeat the proof above with $b u_k + c$ in place of $b u_k$). The implementation therefore accepts an optional `c`. It also accepts many simulated runs at once, one per row, which we will use for Monte Carlo comparisons. Notice that $P_k$, $K_k$, and $S_k$ do not depend on the measurements at all, only on $a$, $Q$, $R$, and $P_0$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ```python
    def kalman_filter_1d(z, u, a, b, Q, R, x0, P0, c=0.0):
        "\"\"Scalar Kalman filter for x_k = a x_{k-1} + b u_k + c + w_k, z_k = x_k + v_k.

        z holds z_1..z_N along its last axis (several runs may be stacked as rows);
        u holds u_1..u_N (or a single number used every step).
        Returns estimates x_hat_k, error variances P_k, innovations, and
        innovation variances S_k, for k = 1..N.
        "\"\"
        z = np.asarray(z, dtype=float)
        u = np.broadcast_to(np.asarray(u, dtype=float), z.shape)
        n = z.shape[-1]
        x_hat = np.full(z.shape[:-1], float(x0))
        P = float(P0)
        estimates, innovations = np.empty(z.shape), np.empty(z.shape)
        variances, innovation_vars = np.empty(n), np.empty(n)
        for k in range(n):
            # Predict with the process model
            x_pred = a * x_hat + b * u[..., k] + c
            P_pred = a * a * P + Q
            # Update with the measurement
            S = P_pred + R
            K = P_pred / S
            innovation = z[..., k] - x_pred
            x_hat = x_pred + K * innovation
            P = (1 - K) * P_pred
            estimates[..., k], innovations[..., k] = x_hat, innovation
            variances[k], innovation_vars[k] = P, S
        return estimates, variances, innovations, innovation_vars
    ```
    """)
    return


@app.cell
def _(np):
    # jb: include=false
    def kalman_filter_1d(z, u, a, b, Q, R, x0, P0, c=0.0):
        """Scalar Kalman filter for x_k = a x_{k-1} + b u_k + c + w_k, z_k = x_k + v_k.

        z holds z_1..z_N along its last axis (several runs may be stacked as rows);
        u holds u_1..u_N (or a single number used every step).
        Returns estimates x_hat_k, error variances P_k, innovations, and
        innovation variances S_k, for k = 1..N.
        """
        z = np.asarray(z, dtype=float)
        u = np.broadcast_to(np.asarray(u, dtype=float), z.shape)
        n = z.shape[-1]
        x_hat = np.full(z.shape[:-1], float(x0))
        P = float(P0)
        estimates, innovations = np.empty(z.shape), np.empty(z.shape)
        variances, innovation_vars = np.empty(n), np.empty(n)
        for k in range(n):
            # Predict with the process model
            x_pred = a * x_hat + b * u[..., k] + c
            P_pred = a * a * P + Q
            # Update with the measurement
            S = P_pred + R
            K = P_pred / S
            innovation = z[..., k] - x_pred
            x_hat = x_pred + K * innovation
            P = (1 - K) * P_pred
            estimates[..., k], innovations[..., k] = x_hat, innovation
            variances[k], innovation_vars[k] = P, S
        return estimates, variances, innovations, innovation_vars

    return (kalman_filter_1d,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch10-sec-the-energy-balance-model -->
    ## The Energy-Balance Model

    The Introduction's footnote estimated a daily weight gain from the energy you eat and the energy you burn. Let us turn that recipe into a process model for the 28-day bulk: a 23-year-old man, 175 cm tall, with a moderate activity level, starting at 155 lb. Weight $x_k$ is in pounds and is measured each morning; the input $u_k$ is the energy eaten on day $k$, in kcal.

    1. **Basal metabolic rate.** The Mifflin–St Jeor equation for men [@mifflin1990] estimates
    $$\text{BMR} = 10\,m + 6.25\,H - 5\,A + 5 \ \text{kcal/day},$$
    with mass $m$ in kg, height $H$ in cm, and age $A$ in years. A weight of $x$ lb is a mass of $m = \kappa x$ kg, with $\kappa = 0.45359237$ kg/lb.
    2. **Total daily energy expenditure.** TDEE is BMR times an activity multiplier $s$ ($s = 1.5$ for moderate activity). So
    $$\text{TDEE}(x) = \gamma\,x + \delta, \qquad \gamma := 10\,s\,\kappa, \qquad \delta := s\,(6.25\,H - 5\,A + 5).$$
    The key observation is that **TDEE is linear in weight**: every extra pound costs $\gamma$ kcal per day to maintain.
    3. **Energy balance.** On day $k$ you eat $u_k$ and burn $\text{TDEE}(x_{k-1})$, using the weight at the start of the day. The surplus is $u_k - \gamma x_{k-1} - \delta$ kcal.
    4. **Energy to weight.** With $\rho = 3500$ kcal per lb [@wishnofsky1958], the weight changes by the surplus divided by $\rho$:
    $$x_k = x_{k-1} + \frac{u_k - \gamma x_{k-1} - \delta}{\rho}.$$

    Collecting terms gives the process model
    $$x_k = a\,x_{k-1} + b\,u_k + c, \qquad a = 1 - \frac{\gamma}{\rho}, \qquad b = \frac{1}{\rho}, \qquad c = -\frac{\delta}{\rho}.$$

    In code:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ```python
    def energy_balance_coefficients(age, height_cm, activity, kcal_per_lb=3500.0):
        "\"\"Coefficients of x_k = a x_{k-1} + b u_k + c for a man (Mifflin-St Jeor
        BMR times an activity multiplier); x in lb, u in kcal/day, one-day steps."\"\"
        kappa = 0.45359237                                   # kg per lb
        gamma = 10 * kappa * activity                        # kcal/day per lb
        delta = activity * (6.25 * height_cm - 5 * age + 5)  # kcal/day
        a = 1 - gamma / kcal_per_lb
        b = 1 / kcal_per_lb
        c = -delta / kcal_per_lb
        return a, b, c, gamma, delta

    a_bulk, b_bulk, c_bulk, gamma_bulk, delta_bulk = energy_balance_coefficients(
        age=23, height_cm=175, activity=1.5
    )
    ```
    """)
    return


@app.cell
def _():
    # jb: include=false
    def energy_balance_coefficients(age, height_cm, activity, kcal_per_lb=3500.0):
        """Coefficients of x_k = a x_{k-1} + b u_k + c for a man (Mifflin-St Jeor
        BMR times an activity multiplier); x in lb, u in kcal/day, one-day steps."""
        kappa = 0.45359237                                   # kg per lb
        gamma = 10 * kappa * activity                        # kcal/day per lb
        delta = activity * (6.25 * height_cm - 5 * age + 5)  # kcal/day
        a = 1 - gamma / kcal_per_lb
        b = 1 / kcal_per_lb
        c = -delta / kcal_per_lb
        return a, b, c, gamma, delta

    a_bulk, b_bulk, c_bulk, gamma_bulk, delta_bulk = energy_balance_coefficients(
        age=23, height_cm=175, activity=1.5
    )
    return (
        a_bulk,
        b_bulk,
        c_bulk,
        delta_bulk,
        energy_balance_coefficients,
        gamma_bulk,
    )


@app.cell(hide_code=True)
def _(a_bulk, b_bulk, c_bulk, delta_bulk, gamma_bulk, mo):
    _tdee155 = gamma_bulk * 155 + delta_bulk
    _u_02 = _tdee155 + 0.2 * 3500
    mo.md(rf"""
    gives $\gamma = {gamma_bulk:.4f}$ kcal/day per lb, $\delta = {delta_bulk:.3f}$ kcal/day, and

    $$a = {a_bulk:.6f}, \qquad b = 1/3500 \approx {b_bulk*1e4:.4f}\times 10^{{-4}}\ \text{{lb/kcal}}, \qquad c = {c_bulk:.4f}\ \text{{lb}}.$$

    At 155 lb, TDEE is ${_tdee155:.0f}$ kcal/day, so gaining $0.2$ lb/day (the 1.4 lb/week target) takes an intake of about ${_u_02:.0f}$ kcal/day.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Three remarks make this model easier to read.

    **It is linear.** Strictly, the constant $c$ makes the model *affine* rather than linear in the sense of the definition. But a known constant can be absorbed into the input: with the *effective input* $\tilde u_k := u_k - \delta$, the intake beyond the weight-independent part of TDEE, we have $b\,u_k + c = b\,\tilde u_k$ and $x_k = a\,x_{k-1} + b\,\tilde u_k$. Linearity in the state is what matters for the Kalman filter, and it holds because TDEE is linear in weight. (A BMR formula with a $\sqrt{\text{weight}}$ term would not give a linear model.)

    **It has an equilibrium.** Since $a < 1$, a heavier body burns more, so a constant intake $u$ cannot make you gain forever. Solving $x^* = a\,x^* + b\,u + c$ gives the equilibrium weight
    $$x^* = \frac{b\,u + c}{1 - a} = \frac{u - \delta}{\gamma},$$
    and subtracting $x^* = a x^* + bu + c$ from the model gives $x_k - x^* = a\,(x_{k-1} - x^*)$, so by induction $x_k - x^* = a^k(x_0 - x^*)$. With $a = 0.998056$ the gap shrinks by only about $0.19\%$ per day; it takes $1/(1 - a) \approx 514$ days to shrink by a factor of $e$. Over four weeks the gain is therefore almost a straight line, but it slows slightly as TDEE rises (to about $0.19$ lb/day after four weeks at a constant $3230$ kcal/day).

    **Logging error becomes process noise.** Suppose the true intake is $u_k^{\text{true}}$ but the food log records $u_k = u_k^{\text{true}} + \varepsilon_k$, where the logging errors $\varepsilon_k$ have mean $0$ and variance $\sigma_u^2$. Suppose also that the true weight follows $x_k = a\,x_{k-1} + b\,u_k^{\text{true}} + c + w_k^{\text{m}}$, where $w_k^{\text{m}}$ (variance $q_{\text{m}}$) collects everything else the model misses. Written in terms of what we know,
    $$x_k = a\,x_{k-1} + b\,u_k + c + \underbrace{\big(w_k^{\text{m}} - b\,\varepsilon_k\big)}_{w_k},$$
    so the process noise seen by the filter is $w_k = w_k^{\text{m}} - b\,\varepsilon_k$. If $w_k^{\text{m}}$ and $\varepsilon_k$ are independent, Chapter 6's rules give
    $$Q = q_{\text{m}} + b^2\sigma_u^2.$$
    A logging error of $\sigma_u = 300$ kcal/day contributes $b\,\sigma_u = 300/3500 \approx 0.086$ lb of daily uncertainty. This is the general recipe: anything the model needs but does not know exactly becomes process noise, and its variance follows from Chapter 6.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **Population formulas.** Mifflin–St Jeor predicts the *average* BMR of people with your age, height, and weight. Individuals typically differ by around 10%. A wrong $\gamma$ or $\delta$ is a *bias*, not noise: it adds the same error every day, so the estimate drifts away from the truth instead of scattering around it. The last section shows how to detect this.
    - **The activity multiplier is a guess,** and it changes when your training changes.
    - **The 3500 kcal/lb rule** treats every pound gained or lost as the same tissue. Over months it overestimates weight change, because expenditure adapts and the composition of the change varies [@hall2011]. For four weeks it is a reasonable approximation.
    - **Logging errors are rarely zero-mean.** People tend to under-report what they eat. A systematic under-report is a bias in $u_k$, with the same effect as a wrong TDEE.
    - **Day-to-day water and food-content swings** (about $\pm 1$ lb) are not in the model. They make the *reading* differ from the tissue weight we model, so they belong in the measurement noise $R$, not in $Q$.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch10-sec-comparing-models-on-simulated-data -->
    ## Comparing Models on Simulated Data

    Which model should the filter use: Chapter 9's random walk, or the energy-balance model? We simulate 28 days of bulking in which the intake changes halfway through, which is exactly the kind of change a fixed expected change $\Delta x_k$ cannot anticipate. So, unlike the straight-line weigh-ins of the Introduction and Chapter 9, the true weight here is not a straight line; the plotted month does reuse their measurement noise.

    - **Truth.** The true weight follows the energy-balance model, starting from $x_0 \sim \mathcal N(155, 1)$. The planned intake is $2880$ kcal/day for days 1–14 and $3580$ kcal/day for days 15–28, a surplus of about $350$ and then $1050$ kcal/day at 155 lb (about $0.1$ and then $0.3$ lb/day, so $0.2$ lb/day on average). The actual intake varies around the plan from day to day with a standard deviation of $300$ kcal, and the model misses a little extra (process noise $w_k^{\text{m}}$ with standard deviation $0.05$ lb).
    - **Measurements.** One weigh-in each morning, $z_k = x_k + v_k$ with $v_k \sim \mathcal N(0, 1)$, so $R = 1$ lb$^2$, displayed to 0.1 lb.
    - **Food log.** The logged intake is the actual intake plus a logging error with standard deviation $\sigma_u$ (the slider).
    - **Random-walk filter** (Chapter 9): $\hat x_k^- = \hat x_{k-1} + 0.2$, using the plan's average gain. Its $Q$ is set to the value that gives the smallest error on these simulations, found by trying a grid of values. This is an advantage it would not have in practice, since there we cannot compare with the truth.
    - **Energy-balance filter:** $a$, $b$, $c$ from above, the logged intake, and $Q = q_{\text{m}} + b^2\sigma_u^2$.

    Both filters start from $\hat x_0 = 155$ with $P_0 = 1$. The plot shows one simulated month; the error figures below it are root-mean-square errors over 2000 simulated months.
    """)
    return


@app.cell
def _(a_bulk, b_bulk, c_bulk, np):
    # jb: include=false
    # 28-day bulking simulation (common random numbers for every slider value)
    N_DAYS = 28
    N_RUNS = 2000
    R_BULK = 1.0
    SIGMA_MODEL = 0.05
    SIGMA_DAY = 300.0
    RW_RATE = 0.2
    days = np.arange(1, N_DAYS + 1)
    intake_plan = np.where(days <= 14, 2880.0, 3580.0)
    _rng = np.random.default_rng(10)
    u_true_mc = intake_plan + SIGMA_DAY * _rng.standard_normal((N_RUNS, N_DAYS))
    log_noise_mc = _rng.standard_normal((N_RUNS, N_DAYS))
    _w = SIGMA_MODEL * _rng.standard_normal((N_RUNS, N_DAYS))
    x0_mc = 155.0 + _rng.standard_normal(N_RUNS)
    x_true_mc = np.empty((N_RUNS, N_DAYS))
    _x = x0_mc.copy()
    for _k in range(N_DAYS):
        _x = a_bulk * _x + b_bulk * u_true_mc[:, _k] + c_bulk + _w[:, _k]
        x_true_mc[:, _k] = _x
    _v = np.sqrt(R_BULK) * _rng.standard_normal((N_RUNS, N_DAYS))
    _v[0] = np.random.default_rng(2).normal(0, 1, N_DAYS)  # displayed run: the book's bulking noise
    z_mc = np.round(x_true_mc + _v, 1)
    return (
        N_DAYS,
        R_BULK,
        RW_RATE,
        SIGMA_DAY,
        SIGMA_MODEL,
        days,
        log_noise_mc,
        u_true_mc,
        x0_mc,
        x_true_mc,
        z_mc,
    )


@app.cell
def _(
    R_BULK,
    RW_RATE,
    SIGMA_MODEL,
    a_bulk,
    b_bulk,
    c_bulk,
    kalman_filter_1d,
    log_noise_mc,
    np,
    u_true_mc,
    x_true_mc,
    z_mc,
):
    # jb: include=false
    # Best Q for the random walk, and energy-model error for a grid of logging errors
    _best = (np.inf, None, None)
    for _Q in np.geomspace(1e-3, 0.5, 37):
        _est = kalman_filter_1d(z_mc, RW_RATE, 1.0, 1.0, _Q, R_BULK, 155.0, 1.0)[0]
        _rmse = np.sqrt(np.mean((_est - x_true_mc) ** 2))
        if _rmse < _best[0]:
            _best = (_rmse, _Q, _est)
    rmse_rw, Q_rw, est_rw_mc = _best

    def energy_filter_mc(sigma_u):
        _u_log = u_true_mc + sigma_u * log_noise_mc
        _Q = SIGMA_MODEL**2 + (b_bulk * sigma_u) ** 2
        return kalman_filter_1d(
            z_mc, _u_log, a_bulk, b_bulk, _Q, R_BULK, 155.0, 1.0, c=c_bulk
        )

    sigma_u_grid = np.arange(0, 1501, 50)
    rmse_energy_grid = np.array([
        np.sqrt(np.mean((energy_filter_mc(_s)[0] - x_true_mc) ** 2))
        for _s in sigma_u_grid
    ])
    _worse = sigma_u_grid[rmse_energy_grid > rmse_rw]
    sigma_u_crossover = float(_worse[0]) if _worse.size else float("nan")
    return (
        Q_rw,
        energy_filter_mc,
        est_rw_mc,
        rmse_energy_grid,
        rmse_rw,
        sigma_u_crossover,
        sigma_u_grid,
    )


@app.cell(hide_code=True)
def _(mo):
    model_choice = mo.ui.radio(
        options=["Energy balance", "Random walk", "Both"],
        value="Both",
        label="Process model",
        inline=True,
    )
    sigma_u_slider = mo.ui.slider(
        0, 1500, step=50, value=300, show_value=True,
        label=r"Logging error $\sigma_u$ (kcal/day)",
    )
    return model_choice, sigma_u_slider


@app.cell(hide_code=True)
def _(
    days,
    energy_filter_mc,
    est_rw_mc,
    graphic,
    mo,
    model_choice,
    np,
    plt,
    rmse_rw,
    sigma_u_slider,
    x0_mc,
    x_true_mc,
    z_mc,
):
    _sigma_u = sigma_u_slider.value
    _est_e, _P_e, _, _ = energy_filter_mc(_sigma_u)
    _rmse_e = np.sqrt(np.mean((_est_e - x_true_mc) ** 2))
    _run = 0
    _show_e = model_choice.value in ("Energy balance", "Both")
    _show_r = model_choice.value in ("Random walk", "Both")

    _fig, _ax = plt.subplots(figsize=(8, 4.5))
    _t = np.concatenate([[0], days])
    _ax.plot(_t, np.concatenate([[x0_mc[_run]], x_true_mc[_run]]), color="black", lw=1.5, label="Truth")
    _ax.plot(days, z_mc[_run], "o", mfc="none", mec="black", label="Measurements")
    if _show_e:
        _e = _est_e[_run]
        _sd = np.sqrt(_P_e)
        _ax.plot(days, _e, color="C1", lw=2, label="Energy-balance estimate")
        _ax.fill_between(days, _e - 2 * _sd, _e + 2 * _sd, color="C1", alpha=0.2)
    if _show_r:
        _r = est_rw_mc[_run]
        _ax.plot(days, _r, color="C4", lw=2, ls="--", label="Random-walk estimate")
    _ax.axvline(14.5, color="gray", lw=0.8, ls=":")
    _ax.text(14.7, _ax.get_ylim()[0] + 0.3, "intake increases", color="gray", fontsize=9)
    _ax.set_xlabel("Day $k$")
    _ax.set_ylabel("Weight (lb)")
    _ax.set_title("Bulking month: energy-balance versus random-walk model", style="italic")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.legend(loc="upper left", fontsize=9)
    _fig.tight_layout()

    _summary = mo.md(
        f"Over 2000 simulated months, RMSE of the energy-balance filter: **{_rmse_e:.3f} lb**; "
        f"random-walk filter (best $Q$): **{rmse_rw:.3f} lb**; raw weigh-ins: 1 lb. "
        f"(Shaded: the energy-balance filter's $\\pm 2\\sqrt{{P_k}}$ band.)"
    )
    mo.vstack([mo.hstack([model_choice, sigma_u_slider], justify="start", gap=2), graphic(_fig), _summary])
    return


@app.cell(hide_code=True)
def _(Q_rw, mo, sigma_u_crossover):
    mo.md(rf"""
    Some things to notice:

    - **The random walk lags the diet change.** It predicts $0.2$ lb/day throughout, so in the first two weeks it overestimates the gain and in the last two it underestimates it. To keep up, it needs a large $Q$ (its best value here is $Q \approx {Q_rw:.3f}$ lb$^2$), which in turn makes it follow the noise more.
    - **The energy-balance model knows about the change the day it happens,** because the change is in the input. A known input can do the work of a quantity we would otherwise have to estimate.
    - **A model is only as good as its inputs.** As $\sigma_u$ grows, so does the energy-balance model's $Q = q_{{\text{{m}}}} + b^2\sigma_u^2$. Beyond a logging error of about ${sigma_u_crossover:.0f}$ kcal/day, the simple random walk wins in these simulations, even though the energy model is the "true" one, because a very noisy input carries less information than a well-tuned constant drift.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch10-sec-continuous-time-models-and-discretization -->
    ## Continuous-Time Models and Discretization

    The energy balance does not really happen once a day: you burn energy continuously. Writing $x(t)$ for the weight at time $t$ (in days) and $u(t)$ for the rate of eating (kcal/day), the physics says that the rate of change of stored energy, $\rho\,\dot x(t)$, equals intake minus expenditure:
    $$\rho\,\dot x(t) = u(t) - \gamma\,x(t) - \delta \quad\Longleftrightarrow\quad \dot x(t) = \lambda\,x(t) + g\,\tilde u(t), \qquad \lambda := -\frac{\gamma}{\rho}, \quad g := \frac{1}{\rho},$$
    with the effective input $\tilde u(t) = u(t) - \delta$. This is a linear {term}`differential equation` ([Appendix C: Linear Differential Equations](#appc-sec-linear-differential-equations)). Most physical laws come in this continuous-time form, while a filter runs in discrete steps. Converting one into the other has a name.

    /// note | 📖 **Definition**
    <u>**Discretization**</u>

    Given a continuous-time process model and a sample period $\Delta t > 0$, a *discretization* is a discrete-time process model whose state $x_k$ is meant to represent the continuous-time state at the sample times $t_k := t_0 + k\,\Delta t$. A discretization is *exact* if $x_k = x(t_k)$ for every $k$ (under stated assumptions about the input between samples); otherwise it is an approximation, and its error $x_k - x(t_k)$ must be analyzed.
    ///

    The daily bookkeeping we did above, which uses the weight at the *start* of each day for the whole day, is one discretization. The [Exact Discretization theorem](#ch10-thm-exact-discretization) below gives the exact one.

    /// admonition | 📐 **Theorem (Exact Discretization)**
        attrs: {class: theorem, id: ch10-thm-exact-discretization}
    Let $\lambda \neq 0$ and $g$ be numbers, and let $\tilde u$ be constant on each sample interval: $\tilde u(t) = \tilde u_k$ for $t_{k-1} < t < t_k$. If $x$ is continuous on $[t_{k-1}, t_k]$ and satisfies $\dot x(t) = \lambda\,x(t) + g\,\tilde u_k$ for $t_{k-1} < t < t_k$, then
    $$x(t_k) = e^{\lambda\Delta t}\,x(t_{k-1}) + \frac{e^{\lambda\Delta t} - 1}{\lambda}\,g\,\tilde u_k.$$
    So the exact discretization is $x_k = a\,x_{k-1} + b\,\tilde u_k$ with $a = e^{\lambda\Delta t}$ and $b = g\,(e^{\lambda\Delta t} - 1)/\lambda$. (For $\lambda = 0$ it is $x_k = x_{k-1} + g\,\Delta t\,\tilde u_k$.)
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    On $[t_{k-1}, t_k]$ define
    $$G(t) := e^{-\lambda t}\,x(t) + \frac{g\,\tilde u_k}{\lambda}\,e^{-\lambda t}.$$
    By the product and chain rules and $\tfrac{d}{dt}e^{-\lambda t} = -\lambda e^{-\lambda t}$ ([Appendix C: Derivatives](#appc-sec-derivatives), [Appendix C: Exponential and Logarithm](#appc-sec-exponential-and-logarithm)), for $t_{k-1} < t < t_k$
    $$G'(t) = e^{-\lambda t}\big(\dot x(t) - \lambda\,x(t)\big) - g\,\tilde u_k\,e^{-\lambda t} = e^{-\lambda t}\,g\,\tilde u_k - g\,\tilde u_k\,e^{-\lambda t} = 0.$$
    $G$ is continuous on $[t_{k-1}, t_k]$ (because $x$ is) and has derivative $0$ inside, so it is constant there by the mean value theorem ([Appendix C: The Mean Value Theorem and Extrema](#appc-sec-the-mean-value-theorem-and-extrema)). Hence $G(t_k) = G(t_{k-1})$, that is,
    $$e^{-\lambda t_k}\,x(t_k) - e^{-\lambda t_{k-1}}\,x(t_{k-1}) = \frac{g\,\tilde u_k}{\lambda}\big(e^{-\lambda t_{k-1}} - e^{-\lambda t_k}\big).$$
    Multiplying by $e^{\lambda t_k}$ and using $t_k - t_{k-1} = \Delta t$ gives the claim. For $\lambda = 0$, $\dot x$ is the constant $g\,\tilde u_k$, and the same argument with $G(t) := x(t) - g\,\tilde u_k\,t$ applies. $\blacksquare$
    ///

    The usual shortcut is **Euler's method**: replace the derivative at the start of the interval by a difference quotient, $\dot x(t_{k-1}) \approx (x(t_k) - x(t_{k-1}))/\Delta t$, which is accurate for small $\Delta t$ by the definition of the {term}`derivative`. This gives
    $$x_k = (1 + \lambda\,\Delta t)\,x_{k-1} + g\,\Delta t\,\tilde u_k.$$
    Our daily bookkeeping was exactly Euler's method with $\Delta t = 1$ day: $1 + \lambda = 1 - \gamma/\rho = a$ and $g = 1/\rho = b$.

    How far apart are the two? By Taylor's theorem with the Lagrange remainder ([Appendix C: Taylor's Theorem](#appc-sec-taylors-theorem)), $e^{\lambda\Delta t} = 1 + \lambda\Delta t + \tfrac12 e^{\xi}(\lambda\Delta t)^2$ for some $\xi$ between $0$ and $\lambda\Delta t$. So Euler's coefficient differs from the exact one by a term proportional to $\Delta t^2$ in each step (the same holds for $b$). Over a fixed time span of $T/\Delta t$ steps these errors accumulate to an error proportional to $\Delta t$ ([Wikipedia: Euler method](https://en.wikipedia.org/wiki/Euler_method)). What makes $\Delta t$ "small" is its size relative to the system's own time scale. For $\lambda < 0$ that time scale is the **time constant** $\tau := -1/\lambda$, the time it takes $e^{\lambda t}$ to shrink by a factor of $e$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Accuracy is not the only issue. Euler's method can turn a decaying system into an exploding one.

    /// admonition | 📐 **Theorem (Stability of the Two Discretizations)**
        attrs: {class: theorem, id: ch10-thm-stability-of-the-two-discretizations}
    Let $\lambda < 0$, $\tau = -1/\lambda$, and $\tilde u_k = 0$ for every $k$ (equivalently, look at the deviation from an equilibrium), with $x_0 \neq 0$. Then:

    1. the exact discretization gives $x_k = e^{-k\Delta t/\tau}x_0$, which decays to $0$ without changing sign, for every $\Delta t > 0$;
    2. Euler's method gives $x_k = (1 - \Delta t/\tau)^k x_0$, which
       - decays without changing sign if $\Delta t < \tau$,
       - is exactly $0$ after one step if $\Delta t = \tau$,
       - decays while alternating in sign if $\tau < \Delta t < 2\tau$,
       - alternates with constant magnitude if $\Delta t = 2\tau$, and
       - grows without bound while alternating in sign if $\Delta t > 2\tau$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Both recursions have the form $x_k = r\,x_{k-1}$, so $x_k = r^k x_0$ by induction. For the exact one, $r = e^{-\Delta t/\tau} \in (0, 1)$. For Euler's, $r = 1 - \Delta t/\tau$, which is in $(0,1)$ iff $\Delta t < \tau$, is $0$ iff $\Delta t = \tau$, is in $(-1, 0)$ iff $\tau < \Delta t < 2\tau$, is $-1$ iff $\Delta t = 2\tau$, and is less than $-1$ iff $\Delta t > 2\tau$. Finally, $|r^k| = |r|^k \to 0$ when $|r| < 1$, and $|r|^k \to \infty$ when $|r| > 1$. $\blacksquare$
    ///

    Try it below on the system $\dot x = (1 - x)/\tau$, which starts at $x(0) = 0$ and rises toward $1$. The exact samples always lie on the true curve; Euler's are close only when $\Delta t \ll \tau$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    dt_ratio = mo.ui.slider(
        0.1, 2.5, step=0.05, value=0.5, show_value=True,
        label=r"Sample period relative to time constant, $\Delta t/\tau$",
    )
    return (dt_ratio,)


@app.cell(hide_code=True)
def _(dt_ratio, graphic, mo, np, plt):
    _r = dt_ratio.value
    _t_end = 10.0
    _n = int(np.floor(_t_end / _r + 1e-9))
    _k = np.arange(_n + 1)
    _tc = np.linspace(0, _t_end, 400)
    _exact = 1 - np.exp(-_k * _r)
    _euler = 1 - (1 - _r) ** _k

    _fig, _ax = plt.subplots(figsize=(8, 4))
    _ax.plot(_tc, 1 - np.exp(-_tc), color="black", lw=1.5, label=r"True $x(t) = 1 - e^{-t/\tau}$")
    _ax.plot(_k * _r, _exact, "o", color="C1", ms=6, label="Exact discretization")
    _ax.plot(_k * _r, _euler, "s--", color="C3", ms=5, lw=1, label="Euler's method")
    _ax.set_ylim(-1.5, 3.0)
    _ax.set_xlim(0, _t_end)
    _ax.set_xlabel(r"Time $t/\tau$")
    _ax.set_ylabel("$x$")
    _ax.set_title(rf"Step response with $\Delta t = {_r:.2f}\,\tau$", style="italic")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.legend(loc="lower right", fontsize=9)
    _fig.tight_layout()
    mo.vstack([dt_ratio, graphic(_fig)])
    return


@app.cell(hide_code=True)
def _(a_bulk, b_bulk, c_bulk, delta_bulk, gamma_bulk, mo, np):
    _lam = -gamma_bulk * b_bulk
    _a_exact = np.exp(_lam)
    _b_exact = (np.exp(_lam) - 1) / _lam * b_bulk
    _u = gamma_bulk * 155 + delta_bulk + 700
    _x_eu, _x_ex = 155.0, 155.0
    for _ in range(28):
        _x_eu = a_bulk * _x_eu + b_bulk * _u + c_bulk
        _x_ex = _a_exact * _x_ex + _b_exact * (_u - delta_bulk)
    mo.md(rf"""
    For the bulking model, $\tau = \rho/\gamma \approx {-1/_lam:.0f}$ days, so one day is tiny compared with $\tau$. The exact coefficients are $a = e^{{\lambda}} = {_a_exact:.7f}$ and $b = {_b_exact*1e4:.4f}\times 10^{{-4}}$, against Euler's $a = {a_bulk:.7f}$ and $b = {b_bulk*1e4:.4f}\times 10^{{-4}}$. After 28 days at a constant ${_u:.0f}$ kcal/day the two predictions differ by ${abs(_x_eu - _x_ex):.3f}$ lb, far below the 1 lb scatter of the scale. Euler's method is perfectly adequate here. It would not be adequate for a system whose time constant is comparable to the sample period, such as a fast process sampled slowly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **Constant input between samples.** The exact discretization assumes $\tilde u$ is constant on each interval (a *zero-order hold*). Meals are not spread evenly over the day, so this is an approximation too. For a linear system it hardly matters when $|\lambda|\Delta t \ll 1$, because then essentially only the total energy eaten during the interval affects $x(t_k)$.
    - **Euler needs $\Delta t \ll \tau$** for accuracy and $\Delta t < 2\tau$ for stability. A model can be correct in continuous time and still produce nonsense after a careless discretization.
    - **The noise must be discretized too.** If continuous-time disturbances act throughout the interval, the variance $Q$ of the discrete-time process noise depends on $\Delta t$; [Chapter 14](#ch14-sec-choosing-q) derives it.
    - **Nonlinear models** generally have no closed-form solution, so they are discretized numerically, for example with the Runge–Kutta method used for the pendulum in [Chapter 15](#ch15-sec-the-model).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch10-sec-rate-models-when-the-state-needs-two-numbers -->
    ## Rate Models: When the State Needs Two Numbers

    The energy-balance model needs a food log. Without one, what can we say about how weight changes? A natural assumption is that you gain at some rate $r_k$ that persists from day to day but drifts slowly:
    $$x_k = x_{k-1} + r_{k-1}, \qquad r_k = r_{k-1} + w_k,$$
    with $w_k$ white noise. Now weight alone is not a state: two people with the same weight today but different rates will weigh different amounts tomorrow. The pair $(x_k, r_k)$ is a state, and we must estimate *both* numbers. The Introduction's alpha-beta filter did exactly that, with two hand-picked gains $\alpha$ and $\beta$.

    Can we choose those gains optimally, as Chapter 7 did for $\alpha$? Let the errors be $e_k^x := \hat x_k - x_k$ and $e_k^r := \hat r_k - r_k$. Predicting with $\hat x_k^- = \hat x_{k-1} + \hat r_{k-1}$ and $\hat r_k^- = \hat r_{k-1}$ gives the prediction errors
    $$e_k^{x-} = e_{k-1}^x + e_{k-1}^r, \qquad e_k^{r-} = e_{k-1}^r - w_k,$$
    and therefore, by Chapter 6's rules (with $w_k$ uncorrelated with the earlier errors),
    $$
    \begin{aligned}
    \operatorname{Var}(e_k^{x-}) &= \operatorname{Var}(e_{k-1}^x) + \operatorname{Var}(e_{k-1}^r) + 2\operatorname{Cov}(e_{k-1}^x, e_{k-1}^r),\\
    \operatorname{Cov}(e_k^{x-}, e_k^{r-}) &= \operatorname{Cov}(e_{k-1}^x, e_{k-1}^r) + \operatorname{Var}(e_{k-1}^r).
    \end{aligned}
    $$
    Two things stand out. The variance of the weight prediction depends on the *covariance* between the two errors, so keeping track of two variances is not enough. And even if the errors are uncorrelated today, one prediction step makes them correlated, because an error in the rate becomes part of the error in the weight. To run a Kalman filter on this model we must track two variances and a covariance, three numbers that naturally form a $2\times 2$ table, and we need an update rule for all of them.

    That is what Part III provides. [Chapter 12](#ch12-sec-covariance-matrices) packages variances and covariances into a covariance matrix, and [Chapter 13](#ch13) derives the Kalman filter for state vectors and shows that its steady state is an alpha-beta filter with optimal gains. Notice also what the energy-balance model bought us: with a food log, the rate is computed from the input instead of estimated, and the state stays one number.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch10-sec-validating-a-model-are-the-innovations-white -->
    ## Validating a Model: Are the Innovations White?

    On simulated data we can compare every estimate with the truth. On real data we cannot, so how do we know whether a model is any good? The {term}`innovations <innovation>` $\tilde y_k = z_k - \hat x_k^-$ are the answer, because we can compute them and we know how they should behave. Chapter 9 showed that if the model, $Q$, and $R$ are all correct, the innovations have mean $0$ and variance $S_k = P_k^- + R$, and are uncorrelated over time. So the *normalized innovations*
    $$\nu_k := \frac{\tilde y_k}{\sqrt{S_k}}$$
    should have mean $0$ and variance $1$, and be uncorrelated with each other. A wrong model breaks this pattern. If the model's prediction is too low every day, for example, the innovations are positive for many days in a row, so neighboring innovations are positively correlated. To measure this we need a name for the correlation between different times of the same process.

    /// note | 📖 **Definition**
    <u>**Autocorrelation**</u>

    For a {term}`stochastic process` $(y_k)$ whose terms have finite, positive variances, the autocorrelation between steps $j$ and $k$ is the {term}`correlation coefficient` of $y_j$ and $y_k$:
    $$\rho_y(j, k) := \frac{\operatorname{Cov}(y_j, y_k)}{\sqrt{\operatorname{Var}(y_j)\operatorname{Var}(y_k)}}.$$
    When it depends only on the lag $\ell := k - j$, we write $\rho_y(\ell)$.
    ///

    In signal processing, "autocorrelation" often means the unnormalized $\mathbb E[y_j y_k]$; for a process with mean $0$ and variance $1$, such as the normalized innovations of a correct model, the two meanings agree. {term}`White noise` has $\rho(\ell) = 0$ for every lag $\ell \neq 0$.

    We estimate the autocorrelation of the normalized innovations $\nu_1, \ldots, \nu_N$ from the data. Since their mean is known to be $0$ when the model is right, we do not subtract the sample mean, which also lets the estimate detect a nonzero mean:
    $$r(\ell) := \frac{\sum_{k=1}^{N-\ell} \nu_k\,\nu_{k+\ell}}{\sum_{k=1}^{N} \nu_k^2}, \qquad \ell = 1, 2, \ldots$$
    Even for perfect white noise, $r(\ell)$ is not exactly $0$. How far from $0$ should we expect it to be?

    /// admonition | 📐 **Lemma (Sample Autocorrelation of White Noise)**
        attrs: {class: lemma, id: ch10-lem-sample-autocorrelation-of-white-noise}
    Let $\nu_1, \ldots, \nu_N$ be {term}`independent <independent random variables>`, each with mean $0$ and variance $\sigma^2 > 0$. For every lag $1 \le \ell < N$, the numerator $C_\ell := \sum_{k=1}^{N-\ell}\nu_k\nu_{k+\ell}$ satisfies
    $$\mathbb E[C_\ell] = 0, \qquad \operatorname{Var}(C_\ell) = (N - \ell)\,\sigma^4.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Since $\ell \ge 1$, the two factors of each term $\nu_k\nu_{k+\ell}$ are independent, so $\mathbb E[\nu_k\nu_{k+\ell}] = \mathbb E[\nu_k]\,\mathbb E[\nu_{k+\ell}] = 0$ ([Chapter 6](#ch6-thm-expectation-of-a-product)), and $\mathbb E[C_\ell] = 0$ by linearity. Each term has variance $\mathbb E[\nu_k^2\nu_{k+\ell}^2] = \mathbb E[\nu_k^2]\,\mathbb E[\nu_{k+\ell}^2] = \sigma^4$. Two different terms, with $j < k$, are uncorrelated: the index $j$ is smaller than each of $j + \ell$, $k$, and $k + \ell$, so $\nu_j$ is independent of the product $\nu_{j+\ell}\nu_k\nu_{k+\ell}$ (the $\nu$'s are mutually independent, so $\nu_j$ is independent of any function of the others), and
    $$\mathbb E\big[\nu_j\nu_{j+\ell}\,\nu_k\nu_{k+\ell}\big] = \mathbb E[\nu_j]\;\mathbb E\big[\nu_{j+\ell}\nu_k\nu_{k+\ell}\big] = 0.$$
    The variance of a sum of uncorrelated terms is the sum of their variances, which is $(N - \ell)\sigma^4$. $\blacksquare$
    ///

    The denominator of $r(\ell)$ is close to $N\sigma^2$ for large $N$, by the weak law of large numbers ([Chapter 6](#ch6-thm-weak-law-of-large-numbers)). So $r(\ell)$ has mean close to $0$ and standard deviation close to $\sqrt{N - \ell}/N \le 1/\sqrt N$. More precisely, for independent, identically distributed $\nu_k$ with finite variance, $\sqrt N\,r(\ell)$ converges in distribution to $\mathcal N(0, 1)$ as $N \to \infty$, for each fixed $\ell$; this is a classical result of Bartlett (see [Wikipedia: Correlogram](https://en.wikipedia.org/wiki/Correlogram)). For a correct model with normal noise the normalized innovations are not only uncorrelated but independent: they are linear combinations of the normal initial state and noises, hence jointly normal, and uncorrelated jointly normal random variables are independent ([Chapter 12](#ch12-cor-uncorrelated-jointly-normal-vectors-are-independent)). This gives a practical test.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// tip | **The whiteness test**
    1. Run the filter and compute the normalized innovations $\nu_k = \tilde y_k/\sqrt{S_k}$.
    2. Compute $r(\ell)$ for the first few lags, say $\ell = 1, \ldots, 20$.
    3. If the model is right, about 95% of these values should lie within $\pm 1.96/\sqrt N$. Many values outside the band, or a run of values with the same sign at small lags, is evidence that the model is wrong.
    4. Check the mean and the {term}`normalized innovation squared` too: $\bar\nu$ should lie within about $\pm 1.96/\sqrt N$ of $0$, and the average of $\nu_k^2$ should be close to $1$ ([Chapter 9](#ch9-sec-checking-the-noise-levels)).
    ///

    The test needs data. With $N = 28$ the band is $\pm 1.96/\sqrt{28} \approx \pm 0.37$, so a month of weigh-ins can only reveal gross errors. Below we simulate 26 weeks instead, with the planned intake changing every week. The truth uses the activity multiplier $1.5$; the slider sets the multiplier used by the *filter's* model, so anything other than $1.5$ is a model error of the kind Mifflin–St Jeor makes for individuals.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ```python
    def sample_autocorrelation(nu, max_lag):
        "\"\"r(l) for l = 1..max_lag of a sequence whose mean should be 0."\"\"
        nu = np.asarray(nu, dtype=float)
        n = len(nu)
        denominator = np.sum(nu**2)
        return np.array([np.sum(nu[: n - l] * nu[l:]) / denominator
                         for l in range(1, max_lag + 1)])
    ```
    """)
    return


@app.cell
def _(np):
    # jb: include=false
    def sample_autocorrelation(nu, max_lag):
        """r(l) for l = 1..max_lag of a sequence whose mean should be 0."""
        nu = np.asarray(nu, dtype=float)
        n = len(nu)
        denominator = np.sum(nu**2)
        return np.array([np.sum(nu[: n - l] * nu[l:]) / denominator
                         for l in range(1, max_lag + 1)])

    return (sample_autocorrelation,)


@app.cell
def _(SIGMA_DAY, SIGMA_MODEL, a_bulk, b_bulk, c_bulk, np):
    # jb: include=false
    # 26-week simulation with a different planned intake every week
    N_LONG = 182
    SIGMA_U_LONG = 300.0
    _rng = np.random.default_rng(9)
    _surplus = _rng.uniform(0, 1400, N_LONG // 7)
    _plan = 2530.0 + np.repeat(_surplus, 7)
    _u_true = _plan + SIGMA_DAY * _rng.standard_normal(N_LONG)
    u_log_long = _u_true + SIGMA_U_LONG * _rng.standard_normal(N_LONG)
    _x = 155.0 + _rng.standard_normal()
    x_true_long = np.empty(N_LONG)
    for _k in range(N_LONG):
        _x = a_bulk * _x + b_bulk * _u_true[_k] + c_bulk + SIGMA_MODEL * _rng.standard_normal()
        x_true_long[_k] = _x
    z_long = np.round(x_true_long + _rng.standard_normal(N_LONG), 1)
    return N_LONG, SIGMA_U_LONG, u_log_long, x_true_long, z_long


@app.cell(hide_code=True)
def _(mo):
    activity_model = mo.ui.slider(
        1.30, 1.70, step=0.01, value=1.50, show_value=True,
        label="Activity multiplier used by the model (truth: 1.50)",
    )
    return (activity_model,)


@app.cell(hide_code=True)
def _(
    N_LONG,
    Q_rw,
    R_BULK,
    RW_RATE,
    SIGMA_MODEL,
    SIGMA_U_LONG,
    activity_model,
    energy_balance_coefficients,
    graphic,
    kalman_filter_1d,
    mo,
    np,
    plt,
    sample_autocorrelation,
    u_log_long,
    x_true_long,
    z_long,
):
    _a, _b, _c, _, _ = energy_balance_coefficients(23, 175, activity_model.value)
    _Q = SIGMA_MODEL**2 + (_b * SIGMA_U_LONG) ** 2
    _est, _P, _innov, _S = kalman_filter_1d(z_long, u_log_long, _a, _b, _Q, R_BULK, 155.0, 1.0, c=_c)
    _nu = _innov / np.sqrt(_S)
    _max_lag = 20
    _r = sample_autocorrelation(_nu, _max_lag)
    _band = 1.96 / np.sqrt(N_LONG)
    _outside = int(np.sum(np.abs(_r) > _band))
    _rmse = np.sqrt(np.mean((_est - x_true_long) ** 2))
    _est_rw = kalman_filter_1d(z_long, RW_RATE, 1.0, 1.0, Q_rw, R_BULK, 155.0, 1.0)[0]
    _rmse_rw = np.sqrt(np.mean((_est_rw - x_true_long) ** 2))

    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(10, 4))
    _days = np.arange(1, N_LONG + 1)
    _ax1.plot(_days, _nu, ".", color="C0", ms=4)
    _ax1.axhline(0, color="black", lw=0.8)
    _ax1.axhline(1.96, color="gray", lw=0.8, ls="--")
    _ax1.axhline(-1.96, color="gray", lw=0.8, ls="--")
    _ax1.set_ylim(-4.5, 4.5)
    _ax1.set_xlabel("Day $k$")
    _ax1.set_ylabel(r"$\nu_k$")
    _ax1.set_title("Normalized innovations", style="italic")
    _ax1.grid(visible=True, alpha=0.9, linewidth=0.4)
    _lags = np.arange(1, _max_lag + 1)
    _ax2.fill_between([0.5, _max_lag + 0.5], -_band, _band, color="gray", alpha=0.2, label=r"$\pm 1.96/\sqrt{N}$")
    _ax2.vlines(_lags, 0, _r, color="C1", lw=2)
    _ax2.plot(_lags, _r, "o", color="C1", ms=4)
    _ax2.axhline(0, color="black", lw=0.8)
    _ax2.set_xlim(0.5, _max_lag + 0.5)
    _ax2.set_ylim(-0.5, 0.8)
    _ax2.set_xlabel(r"Lag $\ell$ (days)")
    _ax2.set_ylabel(r"$r(\ell)$")
    _ax2.set_title("Sample autocorrelation", style="italic")
    _ax2.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax2.legend(loc="upper right", fontsize=9)
    _fig.tight_layout()

    _summary = mo.md(
        f"Mean of $\\nu_k$: **{np.mean(_nu):+.2f}** (band $\\pm${_band:.2f}); "
        f"average NIS: **{np.mean(_nu**2):.2f}** (should be near 1); "
        f"lags outside the band: **{_outside} of {_max_lag}**. "
        f"RMSE against the truth: energy-balance **{_rmse:.2f} lb**, random walk **{_rmse_rw:.2f} lb**."
    )
    mo.vstack([activity_model, graphic(_fig), _summary])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    At the true multiplier $1.50$ the innovations look like white noise: their mean is near $0$, their average square is near $1$, and the sample autocorrelations stay inside the band, apart from the occasional value that chance alone allows. Move the slider to $1.40$ or $1.60$, a 7% error in TDEE, and the picture changes completely. The model now predicts too much (or too little) expenditure every day, the estimate lags behind the truth, and the innovations keep the same sign for weeks. Many autocorrelations are positive and outside the band, the mean of $\nu_k$ is far from $0$, and the RMSE is no better than that of the humble random walk (at $1.40$ or $1.65$ it is clearly worse). Errors of about 3% ($1.45$ or $1.55$), on the other hand, are hard to detect even with 26 weeks of data.

    The test never looked at the true weight. It needs only quantities that a real filter computes anyway, which is what makes it useful.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **Passing is not proof.** White innovations mean the data do not contradict the model; they do not show that the model is right. Small errors (here, a few percent in TDEE) pass easily, and the test has little power with little data.
    - **Failing does not say what is wrong.** A wrong model, a wrong $Q$, a wrong $R$, or correlated measurement noise all produce correlated innovations. Combine the test with the mean and NIS checks, and with what you know about the system.
    - **The band is approximate.** It relies on a large-$N$ approximation and on the innovations being independent with a common distribution. With 20 lags, about one value outside the band is expected by chance alone.
    - **Early innovations** depend on the initial guess $\hat x_0$ and $P_0$. If those are badly wrong, discard the first few innovations before testing.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch10-sec-there-is-no-best-model -->
    ## There Is No Best Model

    Is the energy-balance model better than the random walk? The simulations say: it depends. With an accurate food log and an accurate TDEE formula it is clearly better. With a sloppy food log, or with a TDEE that is off by 7–10%, the random walk does as well or better. Every model leaves something out ([Wikipedia: All models are wrong](https://en.wikipedia.org/wiki/All_models_are_wrong)), so the useful question is not "is this model true?" but "is this model good enough for this purpose, with these data?" Some practical criteria:

    1. **Innovation checks.** Mean near $0$, average NIS near $1$, and white innovations. These work on real data, without the truth.
    2. **Prediction error on new data.** Tune a model on one stretch of data and compare models by their one-step prediction errors (the innovations) on another. A model tuned and judged on the same data can look better than it is.
    3. **Simplicity.** Every parameter is something that can be wrong. The random walk has one number to choose ($Q$); the energy-balance model has many (age, height, activity, the 3500 kcal rule, and the noise levels).
    4. **The cost of the inputs.** The energy-balance model is only as good as a daily food log, which takes effort and has its own errors.
    5. **Purpose and time scale.** For a four-week bulk, neglecting metabolic adaptation is harmless; for a year-long weight-loss plan it is not.

    The Kalman filter makes a model's weaknesses visible: every mismatch leaves a structure in the innovations. Using that feedback to revise a model is a large part of filter design in practice.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch10-sec-summary -->
    ## Summary

    - A **system** is the part of the world inside a chosen boundary. A **control input** is an outside influence whose value we know; unknown influences become **process noise**. A **state** summarizes the past well enough to predict the future, and a **process model** says how the state evolves.
    - For a **linear** model $x_k = a\,x_{k-1} + b\,u_k + w_k$, the prediction $\hat x_k^- = a\,\hat x_{k-1} + b\,u_k$ is unbiased with $P_k^- = a^2 P_{k-1} + Q$. The Kalman filter's update step is unchanged.
    - Because TDEE is linear in weight, the bulking energy balance gives the linear model $x_k = a\,x_{k-1} + b\,u_k + c$ with $a = 1 - \gamma/\rho$, $b = 1/\rho$, $c = -\delta/\rho$. Logging error enters as process noise, $Q = q_{\text{m}} + b^2\sigma_u^2$.
    - An input-driven model beats the random walk when its inputs are accurate, and loses when they are not.
    - A continuous-time model $\dot x = \lambda x + g\tilde u$ is discretized exactly by $a = e^{\lambda\Delta t}$, $b = g(e^{\lambda\Delta t} - 1)/\lambda$. Euler's method is accurate only for $\Delta t \ll \tau$ and stable only for $\Delta t < 2\tau$.
    - When a quantity changes at an unknown rate, the state needs two numbers, and their errors become correlated.
    - A correct model produces white innovations. The sample **autocorrelation** of the normalized innovations, compared with $\pm 1.96/\sqrt N$, tests this without knowing the truth.

    <!-- label: ch10-sec-whats-next -->
    ## What's Next

    So far every measurement has been the state plus noise, $z_k = x_k + v_k$. But a scale does not output pounds: its load cell and analog-to-digital converter output a raw number of *counts*, related to your weight through a sensitivity and an offset that must themselves be measured. [Chapter 11](#ch11) adds a **measurement function** to the filter, calibrates it by least squares, and finds that a drifting offset is a second unknown that a single reading cannot separate from the weight. That is the second reason, after this chapter's rate model, to move to state vectors.
    """)
    return


if __name__ == "__main__":
    app.run()
