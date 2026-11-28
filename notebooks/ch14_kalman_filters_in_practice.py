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
app = marimo.App(app_title="14. Kalman Filters in Practice", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "Tuning, Fusion, and Consistency"
    abbreviations:
      NEES: normalized estimation error squared
      NIS: normalized innovation squared
      RTS: Rauch–Tung–Striebel
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
    from scipy import stats
    from scipy.linalg import expm
    from textwrap import dedent
    from pathlib import Path

    return Path, dedent, expm, mo, np, plt, stats


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
    [Chapter 13](ch13_kalman_filter.md) proved that the Kalman filter is optimal, *given* its model: known noise covariances $\mathbf Q$ and $\mathbf R$, a known initial mean and covariance, a measurement at every step, and exact arithmetic. None of these is given in practice. This chapter is about the engineering between the theorem and a working filter: how to choose what the theorem takes as given, how to handle data that arrive late, at different rates, or not at all, how to combine different sensors, and, most importantly, how to *test* whether a filter's reported uncertainty is honest. Everything is demonstrated on one running example, a cart on a track, which is a one-dimensional rehearsal of the foot-mounted inertial navigation of Part VI.

    /// attention | 🗝️ **Key Idea**
    A Kalman filter is only as good as its model. Tune $\mathbf Q$, $\mathbf R$, and $\mathbf P_0$ from physical reasoning, then *check* them: when the model is right, the normalized errors $\mathbf e^\top\mathbf P^{-1}\mathbf e$ and normalized innovations $\tilde{\mathbf y}^\top\mathbf S^{-1}\tilde{\mathbf y}$ follow known chi-squared distributions, and departures from those distributions reveal what is wrong.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// important | 🔗 **Prerequisites**
    - [Chapter 13](ch13_kalman_filter.md): the whole chapter, in particular the state-space model and its assumptions (A1)–(A6), the Joseph form, the Kalman gain, observability, and the piecewise-constant acceleration model.
    - [Chapter 9](ch9_noise_levels.md): the normalized innovation squared, the chi-squared distribution, filter consistency, and what $Q = 0$ does to the gain.
    - [Chapter 10](ch10_process_models.md): discretization of continuous-time models.
    - [Chapter 12](ch12_vectors_matrices_covariance.md): affine transformations of multivariate normal vectors; Mahalanobis distance.
    - [Chapter 5](ch5_random_variables.md): independence; the distribution of a sum of independent random variables.
    - Appendix C: [The Fundamental Theorem of Calculus](#appc-sec-the-fundamental-theorem-of-calculus); [Multiple Integrals](#appc-sec-multiple-integrals): only for the derivation of the continuous white-noise acceleration model.
    - Appendix D: [Cholesky Decomposition](#appd-sec-cholesky-decomposition); [The Matrix Exponential](#appd-sec-the-matrix-exponential).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch14-sec-the-1-d-cart -->
    ## The 1-D Cart

    A cart rolls along a straight track. It starts at rest at position 0, accelerates at $0.5\ \text{m/s}^2$ from $t = 2$ s to $t = 6$ s, cruises at 2 m/s, brakes at $-0.5\ \text{m/s}^2$ from $t = 12$ s to $t = 16$ s, and stops at 20 m. Two sensors watch it:

    - a **position sensor** (think of a ranging beacon) that reports the position at 10 Hz with noise standard deviation $\sigma_p = 0.5$ m;
    - an **accelerometer** that reports the acceleration at 100 Hz with noise standard deviation $\sigma_{\text{acc}} = 0.05\ \text{m/s}^2$, the default inertial-sensor noise used in Parts V and VI. For now it has no bias.

    The state is $\mathbf x = [p, \dot p]^\top$ (position $p$ in m, velocity $\dot p$ in m/s; the letter $v$ stays reserved for measurement noise). The filter steps at the accelerometer's rate, $\Delta t = 0.01$ s, so a position reading arrives every tenth step. The true acceleration is held constant over each 10 ms step, so the truth is generated exactly by
    $$\mathbf x_k = \mathbf F\mathbf x_{k-1} + \mathbf B a_k, \qquad \mathbf F = \begin{bmatrix}1 & \Delta t \\ 0 & 1\end{bmatrix}, \qquad \mathbf B = \begin{bmatrix}\tfrac12\Delta t^2 \\ \Delta t\end{bmatrix}.$$
    """)
    return


@app.cell
def cart_setup(np):
    # jb: include=false
    cart_dt = 0.01  # s, accelerometer and filter step
    cart_ratio = 10  # one position reading every 10 steps (10 Hz)
    cart_steps = 2000  # 20 s
    cart_t = cart_dt * np.arange(1, cart_steps + 1)  # t_k for k = 1, ..., K
    cart_sigma_acc = 0.05  # m/s^2
    cart_sigma_pos = 0.5  # m
    cart_accel = np.zeros(cart_steps)  # a_k, held over (t_{k-1}, t_k]
    cart_accel[(cart_t > 2) & (cart_t <= 6)] = 0.5
    cart_accel[(cart_t > 12) & (cart_t <= 16)] = -0.5
    cart_F = np.array([[1.0, cart_dt], [0.0, 1.0]])
    cart_B = np.array([[cart_dt**2 / 2], [cart_dt]])
    cart_H = np.array([[1.0, 0.0]])
    cart_x = np.zeros((cart_steps + 1, 2))  # truth x_0, ..., x_K
    for _k in range(cart_steps):
        cart_x[_k + 1] = cart_F @ cart_x[_k] + cart_B[:, 0] * cart_accel[_k]
    cart_t_pos = cart_t[cart_ratio - 1 :: cart_ratio]  # times of position readings
    cart_p_at_readings = cart_x[cart_ratio :: cart_ratio, 0]

    def cart_sensors(n_runs, seed, accel_bias=0.0):
        """Simulate n_runs independent accelerometer and position records."""
        _rng = np.random.default_rng(seed)
        _u = cart_accel + accel_bias + cart_sigma_acc * _rng.normal(size=(n_runs, cart_steps))
        _z = cart_p_at_readings + cart_sigma_pos * _rng.normal(size=(n_runs, cart_steps // cart_ratio))
        return _u, _z

    return (
        cart_B,
        cart_F,
        cart_H,
        cart_accel,
        cart_dt,
        cart_p_at_readings,
        cart_ratio,
        cart_sensors,
        cart_sigma_acc,
        cart_sigma_pos,
        cart_steps,
        cart_t,
        cart_t_pos,
        cart_x,
    )


@app.cell
def make_cart_fig(
    IMAGES_DIR,
    cart_accel,
    cart_sensors,
    cart_t,
    cart_t_pos,
    cart_x,
    np,
    plt,
):
    # jb: include=false
    _u, _z = cart_sensors(1, seed=0)
    _fig, _axes = plt.subplots(3, 1, figsize=(7.5, 6.5), sharex=True)
    _t0 = np.concatenate([[0.0], cart_t])
    _axes[0].plot(_t0, cart_x[:, 0], color="black", lw=1.2, label="truth")
    _axes[0].plot(cart_t_pos, _z[0], "o", mfc="none", mec="black", ms=3.5, label="position sensor (10 Hz)")
    _axes[0].set_ylabel("position (m)")
    _axes[1].plot(_t0, cart_x[:, 1], color="black", lw=1.2, label="truth")
    _axes[1].set_ylabel("velocity (m/s)")
    _axes[2].plot(cart_t, _u[0], color="C0", lw=0.5, label="accelerometer (100 Hz)")
    _axes[2].plot(cart_t, cart_accel, color="black", lw=1.2, label="truth")
    _axes[2].set_ylabel("acceleration (m/s$^2$)")
    _axes[2].set_xlabel("time (s)")
    for _ax, _loc in zip(_axes, ["upper left", "upper left", "lower left"]):
        _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
        _ax.legend(loc=_loc, fontsize=8)
    _axes[0].set_title("The 1-D cart: truth and one realization of both sensors", style="italic")
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch14_cart.svg", metadata={"Date": None})
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch14_cart.svg" class="graphic" alt="Three stacked plots over 20 seconds. Position rises from 0 to 20 m along an S-shaped curve, with noisy position readings scattered about half a meter around it. Velocity ramps from 0 to 2 m/s between 2 and 6 s, stays at 2 m/s, and ramps back to 0 between 12 and 16 s. The true acceleration is a pair of rectangular pulses of plus and minus 0.5 m/s squared, and the accelerometer readings jitter around it." />
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch14-sec-an-implementation-for-many-runs-at-once -->
    ### An Implementation for Many Runs at Once

    Several sections below run the same filter on many independent simulated data sets. Because the Kalman gain and the covariances do not depend on the measurements (Chapter 13), all runs share one $\mathbf P_k$, and only the estimates differ. The implementation therefore stores the estimates of $N$ runs as the *rows* of an $N\times n$ array, so that `x @ F.T` applies $\mathbf F$ to every run at once. For a single run, $N = 1$. A missing position reading is marked by `NaN`. The update returns each run's normalized innovation squared $\tilde{\mathbf y}_k^\top\mathbf S_k^{-1}\tilde{\mathbf y}_k$, which the sections on gating and consistency use.
    """)
    return


@app.cell
def kf_impl(np):
    # jb: editor=true
    def kf_predict(x, P, F, Q, B=None, u=None):
        """Predict. x holds one state per row (N x n); all N runs share P."""
        x = x @ F.T if B is None else x @ F.T + u @ B.T
        return x, F @ P @ F.T + Q


    def kf_update(x, P, z, H, R):
        """Joseph-form update of N runs at once (z is N x m).

        Returns the new estimates, covariance, and each run's normalized
        innovation squared y^T S^-1 y.
        """
        y = z - x @ H.T                          # innovations, one row per run
        S = H @ P @ H.T + R
        K = np.linalg.solve(S, H @ P).T          # K = P H^T S^-1
        x = x + y @ K.T
        I_KH = np.eye(P.shape[0]) - K @ H
        P = I_KH @ P @ I_KH.T + K @ R @ K.T
        P = 0.5 * (P + P.T)                      # remove rounding asymmetry
        nis = np.einsum("ri,ij,rj->r", y, np.linalg.inv(S), y)
        return x, P, nis


    def run_filter(u, z, F, B, H, Q, R, x0, P0, ratio, gate=None):
        """Predict with u[:, k] at every step; update with z[:, j] after
        every `ratio` steps unless that reading is NaN (missing).

        u: N x K control inputs; z: N x (K // ratio) measurements.
        gate: if given, skip a reading whose NIS exceeds it (requires N = 1).
        Returns estimates (K x N x n), covariances (K x n x n),
        the NIS of each accepted reading, and the indices of gated readings.
        """
        N, K = u.shape
        n = P0.shape[0]
        x = np.broadcast_to(np.asarray(x0, float), (N, n)).copy()
        P = np.array(P0, float)
        xs, Ps = np.empty((K, N, n)), np.empty((K, n, n))
        nis_accepted, gated = [], []
        for k in range(K):
            x, P = kf_predict(x, P, F, Q, B, u[:, k:k + 1])
            j = (k + 1) // ratio - 1                  # index of a reading due now
            if (k + 1) % ratio == 0 and not np.isnan(z[0, j]):
                x_new, P_new, nis = kf_update(x, P, z[:, j:j + 1], H, R)
                if gate is not None and nis[0] > gate:
                    gated.append(j)                   # reject: keep the prediction
                else:
                    x, P = x_new, P_new
                    nis_accepted.append(nis)
            xs[k], Ps[k] = x, P
        return xs, Ps, np.array(nis_accepted), gated

    return kf_predict, kf_update, run_filter


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch14-sec-initialization -->
    ## Initialization

    The filter needs $\hat{\mathbf x}_0$ and $\mathbf P_0$ before the first measurement. Assumption (A5) of Chapter 13 says they are the true mean and covariance of $\mathbf x_0$; in practice they encode what you know before the data arrive. The two ways to get them wrong are not symmetric:

    - **$\mathbf P_0$ too small** claims knowledge you do not have. The first gains are then too small, and a wrong $\hat{\mathbf x}_0$ is corrected slowly, in the worst case not at all (see Filter Divergence below).
    - **$\mathbf P_0$ too large** only says "I know little", and the first measurements quickly override $\hat{\mathbf x}_0$. The price is purely numerical: very large entries in $\mathbf P_0$ combined with the simplified covariance update can destroy the covariance through rounding (see Numerical Stability below).

    So when in doubt, choose $\mathbf P_0$ large. In the limit the choice of $\hat{\mathbf x}_0$ stops mattering:

    /// admonition | 📐 **Theorem (Diffuse Initialization, Scalar Case)**
        attrs: {class: theorem, id: ch14-thm-diffuse-initialization-scalar-case}
    For the scalar filter with $\hat x_1^- = a\hat x_0 + bu_1$, $P_1^- = a^2P_0 + Q$, and $R > 0$, $a \ne 0$: as $P_0 \to \infty$, the first estimate $\hat x_1 \to z_1$ and $P_1 \to R$, whatever $\hat x_0$ is.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    $K_1 = P_1^-/(P_1^- + R) = 1 - R/(P_1^- + R) \to 1$ because $P_1^- \to \infty$. Then $\hat x_1 = (1 - K_1)\hat x_1^- + K_1z_1$, and $(1 - K_1)\hat x_1^- = R\,(a\hat x_0 + bu_1)/(a^2P_0 + Q + R) \to 0$, so $\hat x_1 \to z_1$. Also $P_1 = (1 - K_1)P_1^- = RP_1^-/(P_1^- + R) \to R$. $\blacksquare$
    ///

    This is the Introduction's *first-measurement initialization*, recovered as the limit of a vague prior. With a state vector, one measurement may not determine the whole state. For the cart's position-only measurement, two readings $\Delta t$ apart determine both position and velocity:

    /// admonition | 📐 **Lemma (Two-Point Initialization)**
        attrs: {class: lemma, id: ch14-lem-two-point-initialization}
    Let $z_j = p_j + v_j$ for $j = 1, 2$, where the measurement noises $v_1, v_2$ are uncorrelated with variance $R$, and suppose the true velocity is constant between the two readings: $p_2 = p_1 + \Delta t\,\dot p$. Then the estimate $\hat{\mathbf x}_2 := [z_2,\ (z_2 - z_1)/\Delta t]^\top$ of $[p_2, \dot p]^\top$ is unbiased with error covariance
    $$\mathbf P_2 = R\begin{bmatrix}1 & 1/\Delta t \\ 1/\Delta t & 2/\Delta t^2\end{bmatrix}.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    The error is $\hat{\mathbf x}_2 - [p_2, \dot p]^\top = [v_2,\ (v_2 - v_1)/\Delta t]^\top$, which has mean $\mathbf 0$. Its entries have variances $R$ and $2R/\Delta t^2$ and covariance $\operatorname{Cov}(v_2, (v_2 - v_1)/\Delta t) = R/\Delta t$ (Chapter 13's Covariance Rules, using $\operatorname{Cov}(v_1, v_2) = 0$). $\blacksquare$
    ///

    The table runs the Kalman filter on the cart's first two position readings (10 Hz, $R = 0.25\ \text{m}^2$, $\mathbf Q = \mathbf 0$, $\hat{\mathbf x}_0 = \mathbf 0$) with $\mathbf P_0 = \lambda\mathbf I$ for growing $\lambda$. Its estimate after the second reading approaches the two-point initialization.
    """)
    return


@app.cell
def init_table(cart_sensors, cart_sigma_pos, kf_predict, kf_update, np):
    # jb: include=false
    _T = 0.1
    _F = np.array([[1.0, _T], [0.0, 1.0]])
    _H = np.array([[1.0, 0.0]])
    _R = np.array([[cart_sigma_pos**2]])
    _z = np.round(cart_sensors(1, seed=0)[1][0, :2], 2)  # first two position readings
    init_rows = []
    for _lam in [1e0, 1e2, 1e4, 1e6]:
        _x, _P = np.zeros((1, 2)), _lam * np.eye(2)
        for _j in range(2):
            _x, _P = kf_predict(_x, _P, _F, np.zeros((2, 2)))
            _x, _P, _ = kf_update(_x, _P, _z[_j : _j + 1][None, :], _H, _R)
        init_rows.append((f"{_lam:.0e}", _x[0, 0], _x[0, 1], _P[0, 0], _P[0, 1], _P[1, 1]))
    _r = cart_sigma_pos**2
    init_rows.append(("two-point", _z[1], (_z[1] - _z[0]) / _T, _r, _r / _T, 2 * _r / _T**2))
    init_z = _z
    return init_rows, init_z


@app.cell(hide_code=True)
def _(init_rows, init_z, mo):
    _lines = [
        rf"Readings: $z_1 = {init_z[0]:.2f}$ m, $z_2 = {init_z[1]:.2f}$ m.",
        "",
        r"| $\lambda$ | $\hat p_2$ (m) | $\hat v_2$ (m/s) | $P_{11}$ | $P_{12}$ | $P_{22}$ |",
        "|:---|:---:|:---:|:---:|:---:|:---:|",
    ]
    for _name, _p, _v, _p11, _p12, _p22 in init_rows:
        _lines.append(f"| {_name} | {_p:.4f} | {_v:.4f} | {_p11:.4f} | {_p12:.4f} | {_p22:.3f} |")
    mo.md("\n".join(_lines))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For the cart we know more than this: it starts at rest near the origin. The filters below use $\hat{\mathbf x}_0 = \mathbf 0$ and $\mathbf P_0 = \operatorname{diag}(1\ \text{m}^2,\ 0.25\ \text{m}^2/\text{s}^2)$, honest but not tight.

    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **The theorem and the lemma assume the first readings are valid.** If the first reading is an outlier, a diffuse prior hands the filter that outlier as its estimate. Gating (below) cannot help, because with a huge $\mathbf P^-$ every reading looks plausible. Robust start-ups use the median of a few readings.
    - **The two-point lemma assumes constant velocity between the readings.** If the object accelerates, add the process noise accumulated over $\Delta t$ to $\mathbf P_2$.
    - **Unobservable states are not initialized by data.** Their initial uncertainty persists (Chapter 13, Observability), so $\mathbf P_0$ for them must be honest.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch14-sec-choosing-q -->
    ## Choosing Q

    $\mathbf Q$ is the covariance of everything the process model leaves out. For a constant-velocity model, what is left out is the acceleration, so $\mathbf Q$ is a statement about how the acceleration behaves between samples. There are two standard statements, and they lead to different matrices.

    <!-- label: ch14-sec-piecewise-constant-acceleration -->
    ### Piecewise-constant acceleration

    Chapter 13 assumed that the acceleration is constant during each step, $a(t) = a_k$ on $(t_{k-1}, t_k]$, with the $a_k$ uncorrelated, mean 0, variance $\sigma_a^2$. Then $\mathbf w_k = \boldsymbol\Gamma a_k$ with $\boldsymbol\Gamma = [\tfrac12\Delta t^2, \Delta t]^\top$ and
    $$\mathbf Q_{\text{pc}} = \sigma_a^2\begin{bmatrix}\tfrac14\Delta t^4 & \tfrac12\Delta t^3 \\ \tfrac12\Delta t^3 & \Delta t^2\end{bmatrix}.$$
    This matrix has rank 1: position and velocity errors are perfectly correlated within a step, because both come from the same $a_k$.

    <!-- label: ch14-sec-continuous-white-noise-acceleration -->
    ### Continuous white-noise acceleration

    Real accelerations do not change once per sample. The second model treats $a(t)$ as *continuous-time white noise*: a signal so erratic that its values at any two different times are uncorrelated, however close the times are. Such a signal is not an ordinary function, and making it precise takes stochastic calculus[^cwn]. We use only the property that defines it for our purpose:

    - **(W)** For integrable deterministic functions $g$ and $h$ and intervals $I$ and $J$, the integral $\int_I g(s)a(s)\,ds$ has mean 0, and
    $$\operatorname{Cov}\Big(\int_I g(s)a(s)\,ds,\ \int_J h(s)a(s)\,ds\Big) = q\int_{I\cap J}g(s)h(s)\,ds.$$

    The constant $q > 0$, in $\text{m}^2/\text{s}^3$, is the *intensity* (power spectral density) of the noise. In particular, integrals over disjoint intervals are uncorrelated.

    [^cwn]: The integrals in (W) are defined as stochastic integrals with respect to a Wiener process, and the covariance formula is the [Itô isometry](https://en.wikipedia.org/wiki/It%C3%B4_isometry). For an accessible treatment, see @barshalom2002 [Ch. 6].

    /// admonition | 📐 **Theorem (Discretized Continuous White-Noise Acceleration)**
        attrs: {class: theorem, id: ch14-thm-discretized-continuous-white-noise-acceleration}
    Let $\ddot p = a(t)$, with $a$ satisfying (W), be sampled at $t_k = k\Delta t$. Then $\mathbf x_k = [p(t_k), \dot p(t_k)]^\top$ satisfies $\mathbf x_k = \mathbf F\mathbf x_{k-1} + \mathbf w_k$ with $\mathbf F = \begin{bmatrix}1 & \Delta t \\ 0 & 1\end{bmatrix}$ and white $\mathbf w_k$ with covariance
    $$\mathbf Q_{\text{cw}} = q\begin{bmatrix}\tfrac13\Delta t^3 & \tfrac12\Delta t^2 \\ \tfrac12\Delta t^2 & \Delta t\end{bmatrix}.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    For a continuous input $a$, integrating $\ddot p = a$ from $t_{k-1}$ gives $\dot p(t) = \dot p(t_{k-1}) + \int_{t_{k-1}}^t a(s)\,ds$ ([Appendix C: The Fundamental Theorem of Calculus](#appc-sec-the-fundamental-theorem-of-calculus)). Integrating once more and exchanging the order of integration over the triangle $t_{k-1} \le s \le t \le t_k$ ([Appendix C: Multiple Integrals](#appc-sec-multiple-integrals)),
    $$p(t_k) = p(t_{k-1}) + \Delta t\,\dot p(t_{k-1}) + \int_{t_{k-1}}^{t_k}\int_{t_{k-1}}^{t}a(s)\,ds\,dt = p(t_{k-1}) + \Delta t\,\dot p(t_{k-1}) + \int_{t_{k-1}}^{t_k}(t_k - s)\,a(s)\,ds.$$
    For white noise these formulas are taken as the definition of the solution. So $\mathbf x_k = \mathbf F\mathbf x_{k-1} + \mathbf w_k$ with $\mathbf w_k = \int_{t_{k-1}}^{t_k}\mathbf g(s)a(s)\,ds$ and $\mathbf g(s) := [t_k - s,\ 1]^\top$. By (W), applied entry by entry, and the substitution $\tau = t_k - s$,
    $$\mathbf Q_{\text{cw}} = q\int_{t_{k-1}}^{t_k}\mathbf g(s)\mathbf g(s)^\top ds = q\int_0^{\Delta t}\begin{bmatrix}\tau^2 & \tau \\ \tau & 1\end{bmatrix}d\tau = q\begin{bmatrix}\tfrac13\Delta t^3 & \tfrac12\Delta t^2 \\ \tfrac12\Delta t^2 & \Delta t\end{bmatrix}.$$
    For $j \ne k$, $\mathbf w_j$ and $\mathbf w_k$ are integrals over disjoint intervals, hence uncorrelated by (W): the sequence is white. $\blacksquare$
    ///

    The same argument works for any linear model $\dot{\mathbf x} = \mathbf A\mathbf x + \mathbf G a(t)$: the transition matrix is the {term}`matrix exponential` $\mathbf F = e^{\mathbf A\Delta t}$ ([Appendix D: The Matrix Exponential](#appd-sec-the-matrix-exponential)) and
    $$\mathbf Q = q\int_0^{\Delta t}e^{\mathbf A\tau}\mathbf G\mathbf G^\top e^{\mathbf A^\top\tau}\,d\tau,$$
    which can be evaluated with a single matrix exponential of a block matrix [@vanloan1978]. For the constant-velocity model, $\mathbf A = \begin{bmatrix}0 & 1 \\ 0 & 0\end{bmatrix}$ satisfies $\mathbf A^2 = \mathbf 0$, so the exponential series stops after two terms, $e^{\mathbf A\tau} = \mathbf I + \mathbf A\tau = \begin{bmatrix}1 & \tau \\ 0 & 1\end{bmatrix}$, and the general formula reduces to the theorem.
    """)
    return


@app.cell
def q_check(expm, np):
    # jb: include=false
    _dt, _q = 0.37, 2.3
    _A = np.array([[0.0, 1.0], [0.0, 0.0]])
    _G = np.array([[0.0], [1.0]])
    _Qcw = _q * np.array([[_dt**3 / 3, _dt**2 / 2], [_dt**2 / 2, _dt]])
    # Van Loan: expm of [[-A, G q G^T], [0, A^T]] dt
    _M = np.block([[-_A, _q * _G @ _G.T], [np.zeros((2, 2)), _A.T]]) * _dt
    _E = expm(_M)
    _Fd = _E[2:, 2:].T
    q_vanloan_err = np.abs(_Fd @ _E[:2, 2:] - _Qcw).max() / np.abs(_Qcw).max()
    # Monte Carlo: approximate white noise by independent steps of length dt/m
    _rng = np.random.default_rng(1)
    _N, _m = 100_000, 50
    _h = _dt / _m
    _p, _v = np.zeros(_N), np.zeros(_N)
    for _ in range(_m):
        _a = _rng.normal(0.0, np.sqrt(_q / _h), _N)
        _p += _v * _h + 0.5 * _a * _h**2
        _v += _a * _h
    q_mc_err = np.abs(np.cov(np.vstack([_p, _v])) - _Qcw).max() / np.abs(_Qcw).max()
    return q_mc_err, q_vanloan_err


@app.cell(hide_code=True)
def _(mo, q_mc_err, q_vanloan_err):
    mo.md(rf"""
    A numerical check with $\Delta t = 0.37$ s and $q = 2.3\ \text{{m}}^2/\text{{s}}^3$: Van Loan's block-exponential method reproduces $\mathbf Q_{{\text{{cw}}}}$ to a relative error of ${q_vanloan_err:.0e}$, and a Monte Carlo simulation that approximates the white noise by 50 independent sub-steps per sample (100,000 runs) gives a sample covariance within ${100 * q_mc_err:.1f}\%$ of it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch14-sec-which-one -->
    ### Which one?

    | | Piecewise-constant acceleration | Continuous white-noise acceleration |
    |:---:|:---|:---|
    | Assumption | $a$ constant within each step, uncorrelated between steps | $a(t)$ white in continuous time |
    | Parameter | $\sigma_a$ ($\text{m/s}^2$) | $q$ ($\text{m}^2/\text{s}^3$) |
    | $\mathbf Q$ | $\sigma_a^2\begin{bmatrix}\Delta t^4/4 & \Delta t^3/2 \\ \Delta t^3/2 & \Delta t^2\end{bmatrix}$ | $q\begin{bmatrix}\Delta t^3/3 & \Delta t^2/2 \\ \Delta t^2/2 & \Delta t\end{bmatrix}$ |
    | Rank | 1 | 2 |
    | Fits when | the acceleration really is held over each step, e.g. a sampled input | the acceleration varies quickly compared with $\Delta t$ |

    With $q = \sigma_a^2\Delta t$ the two models give the same velocity variance per step; they differ in the position entries ($\Delta t^4/4$ versus $\Delta t^4/3$) and in the correlation. For small $\Delta t$ the difference rarely matters. What matters is the *size*: $\sigma_a$ (or $\sqrt{q/\Delta t}$) should be comparable to the accelerations the model does not explain. A common starting point for the piecewise-constant model is $\sigma_a$ between about half and all of the largest expected acceleration [@barshalom2002, Ch. 6], followed by the consistency tests below.

    **The cart.** When an accelerometer is available, the acceleration is no longer unknown: it becomes the {term}`control input`. The reading $u_k = a_k + n_k$ contains white noise $n_k$ with standard deviation $\sigma_{\text{acc}}$, held over the 10 ms step. Substituting $a_k = u_k - n_k$ into the exact truth model,
    $$\mathbf x_k = \mathbf F\mathbf x_{k-1} + \mathbf B u_k - \mathbf B n_k,$$
    so the process noise is $\mathbf w_k = -\mathbf B n_k$ and $\mathbf Q = \sigma_{\text{acc}}^2\mathbf B\mathbf B^\top$: the piecewise-constant form, with the accelerometer's noise in the role of the unknown acceleration. The accelerometer's noise *is* the process noise. (If the true acceleration also varied within a 10 ms step, a small continuous white-noise term would be added.)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch14-sec-sequential-updates -->
    ## Sequential Updates

    When a measurement vector has several components whose noises are uncorrelated, so that $\mathbf R$ is block diagonal, the update can process them one block at a time. With scalar blocks, $\mathbf S$ is a number and the gain needs only a division, and each block can be handled on its own: one can be skipped or rejected while the others are used. The proof goes through a second form of the update.

    /// admonition | 📐 **Lemma (Information Form of the Update)**
        attrs: {class: lemma, id: ch14-lem-information-form-of-the-update}
    Let $\mathbf P^-$ and $\mathbf R$ be positive definite, $\mathbf S = \mathbf H\mathbf P^-\mathbf H^\top + \mathbf R$, $\mathbf K = \mathbf P^-\mathbf H^\top\mathbf S^{-1}$, $\hat{\mathbf x} = \hat{\mathbf x}^- + \mathbf K(\mathbf z - \mathbf H\hat{\mathbf x}^-)$, and $\mathbf P = (\mathbf I - \mathbf K\mathbf H)\mathbf P^-$. Then $\mathbf P$ is invertible, $\mathbf K = \mathbf P\mathbf H^\top\mathbf R^{-1}$, and
    $$\mathbf P^{-1} = (\mathbf P^-)^{-1} + \mathbf H^\top\mathbf R^{-1}\mathbf H, \qquad \mathbf P^{-1}\hat{\mathbf x} = (\mathbf P^-)^{-1}\hat{\mathbf x}^- + \mathbf H^\top\mathbf R^{-1}\mathbf z.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Write $\mathbf A := \mathbf P^-$, so $\mathbf P = \mathbf A - \mathbf A\mathbf H^\top\mathbf S^{-1}\mathbf H\mathbf A$. Multiplying out and collecting terms,
    $$\mathbf P\big(\mathbf A^{-1} + \mathbf H^\top\mathbf R^{-1}\mathbf H\big) = \mathbf I + \mathbf A\mathbf H^\top\Big[\mathbf R^{-1} - \mathbf S^{-1} - \mathbf S^{-1}\mathbf H\mathbf A\mathbf H^\top\mathbf R^{-1}\Big]\mathbf H.$$
    The bracket is $\mathbf R^{-1} - \mathbf S^{-1}(\mathbf R + \mathbf H\mathbf A\mathbf H^\top)\mathbf R^{-1} = \mathbf R^{-1} - \mathbf S^{-1}\mathbf S\mathbf R^{-1} = \mathbf 0$, so the product is $\mathbf I$. For square matrices a one-sided inverse is two-sided (the Invertible Matrix Theorem in [Appendix D: Linear Independence, Basis, and Rank](#appd-sec-linear-independence-basis-and-rank)), which proves the first formula. Next,
    $$\mathbf P\mathbf H^\top\mathbf R^{-1} = \mathbf A\mathbf H^\top\big(\mathbf I - \mathbf S^{-1}\mathbf H\mathbf A\mathbf H^\top\big)\mathbf R^{-1} = \mathbf A\mathbf H^\top\mathbf S^{-1}\big(\mathbf S - \mathbf H\mathbf A\mathbf H^\top\big)\mathbf R^{-1} = \mathbf A\mathbf H^\top\mathbf S^{-1} = \mathbf K.$$
    Finally, $\mathbf P^{-1}\hat{\mathbf x} = \mathbf P^{-1}\hat{\mathbf x}^- + \mathbf P^{-1}\mathbf K(\mathbf z - \mathbf H\hat{\mathbf x}^-) = (\mathbf A^{-1} + \mathbf H^\top\mathbf R^{-1}\mathbf H)\hat{\mathbf x}^- + \mathbf H^\top\mathbf R^{-1}(\mathbf z - \mathbf H\hat{\mathbf x}^-) = \mathbf A^{-1}\hat{\mathbf x}^- + \mathbf H^\top\mathbf R^{-1}\mathbf z$. $\blacksquare$
    ///

    In words: inverse covariances (*information*) add. The prediction contributes $(\mathbf P^-)^{-1}$, the measurement contributes $\mathbf H^\top\mathbf R^{-1}\mathbf H$. This is the matrix version of [Chapter 7](ch7_optimal_alpha.md)'s $1/P = 1/P^- + 1/R$. The covariance formula is also an instance of the matrix inversion lemma ([Appendix D: Block Matrices and the Schur Complement](#appd-sec-block-matrices-and-the-schur-complement)); the direct check above avoids needing it.

    /// admonition | 📐 **Theorem (Sequential Update)**
        attrs: {class: theorem, id: ch14-thm-sequential-update}
    Let $\mathbf P^-$ be positive definite, and split the measurement as $\mathbf z = \begin{bmatrix}\mathbf z_a \\ \mathbf z_b\end{bmatrix}$, $\mathbf H = \begin{bmatrix}\mathbf H_a \\ \mathbf H_b\end{bmatrix}$, $\mathbf R = \begin{bmatrix}\mathbf R_a & \mathbf 0 \\ \mathbf 0 & \mathbf R_b\end{bmatrix}$ with $\mathbf R_a, \mathbf R_b$ positive definite. Updating $(\hat{\mathbf x}^-, \mathbf P^-)$ with $(\mathbf z_a, \mathbf H_a, \mathbf R_a)$, and then updating the result with $(\mathbf z_b, \mathbf H_b, \mathbf R_b)$, with no prediction in between, gives the same estimate and covariance as one update with $(\mathbf z, \mathbf H, \mathbf R)$. By induction, the same holds for any number of blocks.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Because $\mathbf R^{-1} = \operatorname{diag}(\mathbf R_a^{-1}, \mathbf R_b^{-1})$, block multiplication gives $\mathbf H^\top\mathbf R^{-1}\mathbf H = \mathbf H_a^\top\mathbf R_a^{-1}\mathbf H_a + \mathbf H_b^\top\mathbf R_b^{-1}\mathbf H_b$ and $\mathbf H^\top\mathbf R^{-1}\mathbf z = \mathbf H_a^\top\mathbf R_a^{-1}\mathbf z_a + \mathbf H_b^\top\mathbf R_b^{-1}\mathbf z_b$. By the Lemma, the first update produces $\mathbf P_a$ with $\mathbf P_a^{-1} = (\mathbf P^-)^{-1} + \mathbf H_a^\top\mathbf R_a^{-1}\mathbf H_a$, which is positive definite, and $\mathbf P_a^{-1}\hat{\mathbf x}_a = (\mathbf P^-)^{-1}\hat{\mathbf x}^- + \mathbf H_a^\top\mathbf R_a^{-1}\mathbf z_a$. Applying the Lemma again with $(\hat{\mathbf x}_a, \mathbf P_a)$ as the prediction adds the $b$ terms, so the final $\mathbf P^{-1}$ and $\mathbf P^{-1}\hat{\mathbf x}$ equal those of the single update. These two quantities determine $\mathbf P$ and $\hat{\mathbf x}$. $\blacksquare$
    ///

    /// note | 📖 **Definition**
    <u>**Sequential update**</u>

    The processing of a measurement $\mathbf z_k = [\mathbf z_k^{(1)}; \ldots; \mathbf z_k^{(p)}]$ whose noise covariance is block diagonal, $\mathbf R_k = \operatorname{diag}(\mathbf R_k^{(1)}, \ldots, \mathbf R_k^{(p)})$, as $p$ successive Kalman updates, the $i$-th using $(\mathbf z_k^{(i)}, \mathbf H_k^{(i)}, \mathbf R_k^{(i)})$ and starting from the result of the $(i-1)$-th, with no prediction in between.
    ///

    /// admonition | 📐 **Corollary (Decorrelating the Noise)**
        attrs: {class: corollary, id: ch14-cor-decorrelating-the-noise}
    Let $\mathbf R = \mathbf L\mathbf L^\top$ be the {term}`Cholesky decomposition` of a positive definite $\mathbf R$. The transformed measurement $\mathbf z' := \mathbf L^{-1}\mathbf z = (\mathbf L^{-1}\mathbf H)\mathbf x + \mathbf L^{-1}\mathbf v$ has noise covariance $\mathbf I$, and updating with $(\mathbf z', \mathbf L^{-1}\mathbf H, \mathbf I)$ gives the same result as updating with $(\mathbf z, \mathbf H, \mathbf R)$. So any measurement can be processed one scalar at a time.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    $\operatorname{Cov}(\mathbf L^{-1}\mathbf v) = \mathbf L^{-1}\mathbf L\mathbf L^\top\mathbf L^{-\top} = \mathbf I$. The transformed update has $(\mathbf L^{-1}\mathbf H)^\top(\mathbf L^{-1}\mathbf H) = \mathbf H^\top(\mathbf L\mathbf L^\top)^{-1}\mathbf H = \mathbf H^\top\mathbf R^{-1}\mathbf H$ and $(\mathbf L^{-1}\mathbf H)^\top\mathbf z' = \mathbf H^\top\mathbf R^{-1}\mathbf z$, so by the Lemma it produces the same $\mathbf P^{-1}$ and $\mathbf P^{-1}\hat{\mathbf x}$. $\blacksquare$
    ///
    """)
    return


@app.cell
def sequential_check(np):
    # jb: include=false
    def _update(x, P, z, H, R):
        _S = H @ P @ H.T + R
        _K = P @ H.T @ np.linalg.inv(_S)
        return x + _K @ (z - H @ x), (np.eye(len(x)) - _K @ H) @ P

    _rng = np.random.default_rng(4)
    _A = _rng.normal(size=(3, 3))
    _Pm = _A @ _A.T + 0.5 * np.eye(3)
    _x = _rng.normal(size=3)
    _H = _rng.normal(size=(2, 3))
    _z = _rng.normal(size=2)
    _Rd = np.diag([0.4, 0.9])
    _xb, _Pb = _update(_x, _Pm, _z, _H, _Rd)
    _xs, _Ps = _update(_x, _Pm, _z[:1], _H[:1], _Rd[:1, :1])
    _xs, _Ps = _update(_xs, _Ps, _z[1:], _H[1:], _Rd[1:, 1:])
    seq_diff = max(np.abs(_xb - _xs).max(), np.abs(_Pb - _Ps).max())
    _Rc = np.array([[0.4, 0.25], [0.25, 0.9]])
    _xb, _Pb = _update(_x, _Pm, _z, _H, _Rc)
    _Li = np.linalg.inv(np.linalg.cholesky(_Rc))
    _z2, _H2 = _Li @ _z, _Li @ _H
    _xs, _Ps = _update(_x, _Pm, _z2[:1], _H2[:1], np.eye(1))
    _xs, _Ps = _update(_xs, _Ps, _z2[1:], _H2[1:], np.eye(1))
    seq_decor_diff = max(np.abs(_xb - _xs).max(), np.abs(_Pb - _Ps).max())
    _xs, _Ps = _update(_x, _Pm, _z[:1], _H[:1], _Rc[:1, :1])
    _xs, _Ps = _update(_xs, _Ps, _z[1:], _H[1:], _Rc[1:, 1:])
    seq_naive_diff = np.abs(_xb - _xs).max()
    return seq_decor_diff, seq_diff, seq_naive_diff


@app.cell(hide_code=True)
def _(mo, seq_decor_diff, seq_diff, seq_naive_diff):
    mo.md(rf"""
    A numerical check with three states and two measurements: with diagonal $\mathbf R$, the sequential and batch results differ by at most ${seq_diff:.0e}$; with a correlated $\mathbf R$ and the Cholesky decorrelation, by ${seq_decor_diff:.0e}$. Processing the correlated components one at a time *without* decorrelating them, as if $\mathbf R$ were diagonal, changes the estimate by ${seq_naive_diff:.2f}$: the theorem's hypothesis is not decoration.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch14-sec-missing-measurements-and-multi-rate-data -->
    ## Missing Measurements and Multi-Rate Data

    Chapter 13's derivation never assumed that every step has the same measurement model; each proof used one step at a time. So a step may have a measurement of any dimension $m_k$, including $m_k = 0$: **no measurement**. Then there is no innovation, and the update leaves the prediction unchanged,
    $$\hat{\mathbf x}_k = \hat{\mathbf x}_k^-, \qquad \mathbf P_k = \mathbf P_k^-,$$
    which is also what the Joseph form gives with $\mathbf K_k = \mathbf 0$. The filter remains optimal for the data that did arrive. Two situations use this:

    - **Missing data.** A reading is lost (a dropped packet, a sensor glitch). Skip the update; the covariance keeps growing through the predictions until the next reading arrives.
    - **Multi-rate data.** Different sensors report at different rates. Predict at the fastest rate and update with each sensor when, and only when, it reports. If several report at the same instant, process them with sequential updates. The cart does exactly this: it predicts at 100 Hz with each accelerometer sample and updates at 10 Hz with each position reading.

    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **Missing must not mean informative.** Skipping is correct when *whether* a reading arrives does not depend on its value. A sensor that drops out exactly when its reading would be extreme (for example, a range sensor that loses its target when the target is far) removes the large values selectively, and skipping then biases the estimate.
    - **Timestamps must be right.** Multi-rate filtering assumes each reading is applied at the step when it was *taken*. A reading that arrives late must either be applied at its true time (by re-running the filter from that time) or have its delay modeled.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch14-sec-sensor-fusion-on-the-cart -->
    ## Sensor Fusion on the Cart

    /// note | 📖 **Definition**
    <u>**Sensor fusion**</u>

    The combination of measurements from two or more sensors into a single estimate of a state.
    ///

    The cart's two sensors have complementary flaws. The position sensor is noisy, but its errors do not accumulate. The accelerometer is precise from moment to moment, but integrating it twice to get position, which is *dead reckoning*, accumulates every one of its errors: white noise grows into a position error that keeps growing with time, and any bias grows quadratically. A Kalman filter fuses them without any special machinery. The accelerometer drives the prediction at 100 Hz as a control input, with $\mathbf Q = \sigma_{\text{acc}}^2\mathbf B\mathbf B^\top$, and the position readings correct it at 10 Hz with $R = \sigma_p^2$.

    The sliders change what the *filter* believes, as multiples of the true noise levels, and how many position readings are lost (at random, the same readings for every setting). The data stay the same. The upper plot shows the estimation error in position, the error of each raw reading, and the error of dead reckoning from the accelerometer alone; the lower plot shows the velocity error. In both, a consistent filter's error should stay inside its $\pm 2\sigma$ band about 95% of the time.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    q_scale_slider = mo.ui.slider(
        steps=[0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0],
        value=1.0,
        label=r"filter's $\sigma_{\text{acc}} \div$ true",
        show_value=True,
    )
    r_scale_slider = mo.ui.slider(
        steps=[0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 4.0],
        value=1.0,
        label=r"filter's $\sigma_p \div$ true",
        show_value=True,
    )
    dropout_slider = mo.ui.slider(
        start=0.0, stop=0.9, step=0.1, value=0.0, label="fraction of position readings lost", show_value=True
    )
    return dropout_slider, q_scale_slider, r_scale_slider


@app.cell
def fusion_setup(cart_B, cart_dt, cart_sigma_acc, cart_sigma_pos, cart_steps, cart_ratio, np):
    # jb: include=false
    fusion_x0 = np.zeros(2)
    fusion_P0 = np.diag([1.0, 0.25])
    _dropout_draws = np.random.default_rng(7).random(cart_steps // cart_ratio)

    def fusion_models(q_scale, r_scale, dropout):
        """Filter Q and R for the given belief multipliers, and the lost-reading mask."""
        _Q = (q_scale * cart_sigma_acc) ** 2 * cart_B @ cart_B.T
        _R = np.array([[(r_scale * cart_sigma_pos) ** 2]])
        return _Q, _R, _dropout_draws < dropout - 1e-12

    def dead_reckon(u):
        """Integrate accelerometer readings alone (N x K) from the known start at rest."""
        _v = np.cumsum(u * cart_dt, axis=1)
        _v_prev = np.concatenate([np.zeros((u.shape[0], 1)), _v[:, :-1]], axis=1)
        return np.cumsum(_v_prev * cart_dt + 0.5 * u * cart_dt**2, axis=1)

    return dead_reckon, fusion_P0, fusion_models, fusion_x0


@app.cell(hide_code=True)
def fusion_interactive(
    cart_B,
    cart_F,
    cart_H,
    cart_p_at_readings,
    cart_ratio,
    cart_sensors,
    cart_t,
    cart_t_pos,
    cart_x,
    dead_reckon,
    dropout_slider,
    fusion_P0,
    fusion_models,
    fusion_x0,
    graphic,
    mo,
    np,
    plt,
    q_scale_slider,
    r_scale_slider,
    run_filter,
):
    _Q, _R, _lost = fusion_models(q_scale_slider.value, r_scale_slider.value, dropout_slider.value)
    _u, _z = cart_sensors(1, seed=0)
    _z = np.where(_lost[None, :], np.nan, _z)
    _xs, _Ps, _, _ = run_filter(_u, _z, cart_F, cart_B, cart_H, _Q, _R, fusion_x0, fusion_P0, cart_ratio)
    fusion_err = _xs[:, 0, :] - cart_x[1:]
    fusion_sd = np.sqrt(np.stack([_Ps[:, 0, 0], _Ps[:, 1, 1]], axis=1))
    fusion_dr_err = dead_reckon(_u)[0] - cart_x[1:, 0]
    fusion_meas_err = _z[0] - cart_p_at_readings

    _fig, (_ax1, _ax2) = plt.subplots(2, 1, figsize=(7.5, 6.0), sharex=True)
    _ax1.plot(cart_t_pos, fusion_meas_err, "o", mfc="none", mec="black", ms=3, alpha=0.6, label="raw readings")
    _ax1.plot(cart_t, fusion_dr_err, ":", color="red", label="accelerometer only")
    _ax1.fill_between(cart_t, -2 * fusion_sd[:, 0], 2 * fusion_sd[:, 0], color="C1", alpha=0.2, label=r"filter's $\pm 2\sigma$")
    _ax1.plot(cart_t, fusion_err[:, 0], color="C1", lw=1.0, label="fused estimate")
    _ax1.axhline(0, color="black", lw=0.6)
    _ax1.set_ylim(-1.6, 1.6)
    _ax1.set_ylabel("position error (m)")
    _ax1.set_title("Position error", style="italic")
    _ax1.legend(loc="lower left", ncol=2, fontsize=8)
    _ax2.fill_between(cart_t, -2 * fusion_sd[:, 1], 2 * fusion_sd[:, 1], color="C1", alpha=0.2, label=r"filter's $\pm 2\sigma$")
    _ax2.plot(cart_t, fusion_err[:, 1], color="C1", lw=1.0, label="fused estimate")
    _ax2.axhline(0, color="black", lw=0.6)
    _ax2.set_ylim(-0.4, 0.4)
    _ax2.set_ylabel("velocity error (m/s)")
    _ax2.set_xlabel("time (s)")
    _ax2.set_title("Velocity error", style="italic")
    _ax2.legend(loc="lower left", fontsize=8)
    for _ax in (_ax1, _ax2):
        _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _fig.tight_layout()
    mo.vstack([
        mo.hstack([q_scale_slider, r_scale_slider, dropout_slider], justify="start", gap=2),
        graphic(_fig),
    ])
    return fusion_dr_err, fusion_err, fusion_meas_err, fusion_sd


@app.cell(hide_code=True)
def _(fusion_dr_err, fusion_err, fusion_meas_err, fusion_sd, mo, np):
    _inside = np.mean(np.abs(fusion_err) <= 2 * fusion_sd, axis=0)
    _rms_meas = np.sqrt(np.nanmean(fusion_meas_err**2))
    mo.md(rf"""
    Root-mean-square position error: raw readings {_rms_meas:.2f} m, fused estimate {np.sqrt(np.mean(fusion_err[:, 0] ** 2)):.3f} m. Dead reckoning ends {abs(fusion_dr_err[-1]):.2f} m off after 20 s. The fused error lies inside the filter's $\pm 2\sigma$ band {100 * _inside[0]:.0f}% of the time for position and {100 * _inside[1]:.0f}% for velocity.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Things to notice:

    - **Fusion beats both sensors.** With the true noise levels, the fused position error is several times smaller than the raw readings' 0.5 m and does not drift like dead reckoning.
    - **The band breathes.** Between position readings the filter dead-reckons and its uncertainty grows; each reading pulls it back down. With readings lost, the gaps are longer, the band widens during them, and the error still stays inside it: missing data costs accuracy, not honesty.
    - **Wrong beliefs show up as a wrong band, not (at first) as a visibly wrong estimate.** Telling the filter the position sensor is 4 times better than it is (slider at 0.25) makes the band far too narrow for the actual errors; telling it the sensor is worse makes the band too wide. One run makes this hard to judge by eye. The consistency tests below make it a number.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch14-sec-an-unmodeled-bias -->
    ### An Unmodeled Bias

    Real accelerometers have a bias; Part VI's default is $0.05\ \text{m/s}^2$. Dead reckoning turns a constant bias $b$ into a position error of $\tfrac12bt^2$, which is 10 m after 20 s. The filter above assumes zero-mean accelerometer noise, assumption (A2), so a bias violates its model. The remedy suggested in Chapter 13 is to make the bias a state. With $\mathbf x = [p, \dot p, b]^\top$, a constant bias, and $u_k = a_k + b + n_k$,
    $$\mathbf x_k = \begin{bmatrix}1 & \Delta t & -\tfrac12\Delta t^2 \\ 0 & 1 & -\Delta t \\ 0 & 0 & 1\end{bmatrix}\mathbf x_{k-1} + \begin{bmatrix}\tfrac12\Delta t^2 \\ \Delta t \\ 0\end{bmatrix}(u_k - n_k), \qquad z_k = [1\ \ 0\ \ 0]\,\mathbf x_k + v_k.$$
    Is the bias observable from position readings alone? The rank test answers it. For the model with $\mathbf F$ over one 0.1 s interval between position readings (the 100 Hz matrix raised to the 10th power), the observability matrix $[\mathbf H; \mathbf H\mathbf F; \mathbf H\mathbf F^2]$ has rank 3, so yes, but its smallest singular value is small compared with its largest (computed below). The bias is observable, but only weakly, and learning it takes time. The figure compares the two-state filter with the three-state filter on data with a $0.05\ \text{m/s}^2$ bias. The three-state filter starts with $\hat b_0 = 0$ and a standard deviation of $0.1\ \text{m/s}^2$.
    """)
    return


@app.cell
def bias_demo(
    IMAGES_DIR,
    cart_B,
    cart_F,
    cart_H,
    cart_dt,
    cart_ratio,
    cart_sensors,
    cart_sigma_acc,
    cart_sigma_pos,
    cart_t,
    cart_x,
    fusion_P0,
    np,
    plt,
    run_filter,
):
    # jb: include=false
    bias_true = 0.05
    _dt = cart_dt
    _F3 = np.array([[1.0, _dt, -(_dt**2) / 2], [0.0, 1.0, -_dt], [0.0, 0.0, 1.0]])
    _B3 = np.array([[_dt**2 / 2], [_dt], [0.0]])
    _H3 = np.array([[1.0, 0.0, 0.0]])
    _Q3 = cart_sigma_acc**2 * _B3 @ _B3.T
    _P03 = np.diag([1.0, 0.25, 0.1**2])
    _R = np.array([[cart_sigma_pos**2]])
    _F10 = np.linalg.matrix_power(_F3, cart_ratio)
    _O = np.vstack([_H3, _H3 @ _F10, _H3 @ _F10 @ _F10])
    bias_rank = np.linalg.matrix_rank(_O)
    bias_sv = np.linalg.svd(_O, compute_uv=False)

    _N = 100
    _u, _z = cart_sensors(_N, seed=11, accel_bias=bias_true)
    _x2, _P2, _, _ = run_filter(_u, _z, cart_F, cart_B, cart_H, cart_sigma_acc**2 * cart_B @ cart_B.T, _R, np.zeros(2), fusion_P0, cart_ratio)
    _x3, _P3, _, _ = run_filter(_u, _z, _F3, _B3, _H3, _Q3, _R, np.zeros(3), _P03, cart_ratio)
    _truth = cart_x[1:, None, :]
    _e2 = _x2 - _truth
    _e3 = _x3[:, :, :2] - _truth

    bias_inside2 = np.mean(np.abs(_e2[:, :, 0]) <= 2 * np.sqrt(_P2[:, None, 0, 0]))
    bias_inside3 = np.mean(np.abs(_e3[:, :, 0]) <= 2 * np.sqrt(_P3[:, None, 0, 0]))
    bias_rms2 = np.sqrt(np.mean(_e2[:, :, 0] ** 2))
    bias_rms3 = np.sqrt(np.mean(_e3[:, :, 0] ** 2))
    bias_est_final = (_x3[-1, :, 2].mean(), np.sqrt(_P3[-1, 2, 2]))
    _t5 = int(round(5.0 / _dt)) - 1
    bias_est_5s = (_x3[_t5, :, 2].mean(), np.sqrt(_P3[_t5, 2, 2]))

    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(10, 3.8))
    _sd2 = np.sqrt(_P2[:, 0, 0])
    _sd3 = np.sqrt(_P3[:, 0, 0])
    _ax1.fill_between(cart_t, -2 * _sd2, 2 * _sd2, color="C0", alpha=0.15)
    _ax1.plot(cart_t, _e2[:, 0, 0], color="C0", lw=1.0, label="2-state filter (no bias state)")
    _ax1.fill_between(cart_t, -2 * _sd3, 2 * _sd3, color="C1", alpha=0.2)
    _ax1.plot(cart_t, _e3[:, 0, 0], color="C1", lw=1.0, label="3-state filter (bias state)")
    _ax1.axhline(0, color="black", lw=0.6)
    _ax1.set_xlabel("time (s)")
    _ax1.set_ylabel("position error (m)")
    _ax1.set_title(r"Position error with $\pm 2\sigma$ bands (one run)", style="italic")
    _ax1.legend(loc="lower left", fontsize=8)
    _sdb = np.sqrt(_P3[:, 2, 2])
    _ax2.axhline(bias_true, color="black", lw=1.2, label="true bias")
    _ax2.fill_between(cart_t, _x3[:, 0, 2] - 2 * _sdb, _x3[:, 0, 2] + 2 * _sdb, color="C1", alpha=0.2, label=r"$\pm 2\sigma$")
    _ax2.plot(cart_t, _x3[:, 0, 2], color="C1", label="estimated bias")
    _ax2.set_ylim(-0.15, 0.2)
    _ax2.set_xlabel("time (s)")
    _ax2.set_ylabel("accelerometer bias (m/s$^2$)")
    _ax2.set_title("Bias estimate of the 3-state filter (one run)", style="italic")
    _ax2.legend(loc="upper right", fontsize=8)
    for _ax in (_ax1, _ax2):
        _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch14_bias.svg", metadata={"Date": None})
    plt.close(_fig)
    return (
        bias_est_5s,
        bias_est_final,
        bias_inside2,
        bias_inside3,
        bias_rank,
        bias_rms2,
        bias_rms3,
        bias_sv,
        bias_true,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch14_bias.svg" class="graphic" alt="Left: position errors of two filters over 20 seconds. The two-state filter's error wanders up to about a meter, far outside its narrow uncertainty band; the three-state filter's error stays within a few tenths of a meter and inside its band. Right: the three-state filter's bias estimate starts at zero with a wide band and settles onto the true value of 0.05 within several seconds, with a band that narrows steadily." />
    """)
    return


@app.cell(hide_code=True)
def _(
    bias_est_5s,
    bias_est_final,
    bias_inside2,
    bias_inside3,
    bias_rank,
    bias_rms2,
    bias_rms3,
    bias_sv,
    mo,
):
    mo.md(rf"""
    The observability matrix has rank {bias_rank} with singular values {", ".join(f"{_s:.3g}" for _s in bias_sv)}. Over 100 simulated runs, the two-state filter's root-mean-square position error is {bias_rms2:.2f} m, worse than the raw readings, and its error lies inside its own $\pm 2\sigma$ band only {100 * bias_inside2:.0f}% of the time instead of about 95%: it is badly overconfident. The three-state filter's error is {bias_rms3:.2f} m and inside its band {100 * bias_inside3:.0f}% of the time. Its bias estimate (averaged over runs) is ${bias_est_5s[0]:.3f} \pm {2 * bias_est_5s[1]:.3f}$ after 5 s and ${bias_est_final[0]:.4f} \pm {2 * bias_est_final[1]:.4f}\ \text{{m/s}}^2$ after 20 s.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is the pattern of Part VI in miniature: an inertial sensor that is excellent over short times, an aiding measurement that bounds its drift, and sensor biases estimated as extra states, as far as they are observable.

    <!-- label: ch14-sec-outlier-gating -->
    ## Outlier Gating

    Real sensors occasionally produce readings that have nothing to do with the model: a reflection, a loose connector, a person bumping the scale. Chapter 13's filter has no defense against them. The innovation tells us when a reading is implausible, and under the Gaussian assumption we know exactly how implausible. Recall ([Chapter 9](ch9_noise_levels.md), [Chapter 12](ch12_vectors_matrices_covariance.md)) that the {term}`chi-squared distribution` with $d$ degrees of freedom, $\chi^2_{d}$, is the distribution of the sum of squares of $d$ independent standard normal random variables; its mean is $d$. The {term}`normalized innovation squared` $\epsilon_k = \tilde y_k^2/S_k$ of Chapter 9 generalizes to $\epsilon_k := \tilde{\mathbf y}_k^\top\mathbf S_k^{-1}\tilde{\mathbf y}_k$.

    /// admonition | 📐 **Lemma (Normalized Quadratic Forms Are Chi-Squared)**
        attrs: {class: lemma, id: ch14-lem-normalized-quadratic-forms-are-chi-squared}
    If $\mathbf y \sim \mathcal N(\mathbf 0, \boldsymbol\Sigma)$ with $\boldsymbol\Sigma \in \mathbb R^{d\times d}$ positive definite, then $\mathbf y^\top\boldsymbol\Sigma^{-1}\mathbf y \sim \chi^2_{d}$. In particular, under (A1)–(A6), the normalized innovation squared $\tilde{\mathbf y}_k^\top\mathbf S_k^{-1}\tilde{\mathbf y}_k$ of a Kalman filter has distribution $\chi^2_{m}$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Let $\boldsymbol\Sigma = \mathbf L\mathbf L^\top$ be the Cholesky decomposition and $\mathbf u := \mathbf L^{-1}\mathbf y$. Since $\mathbf L^{-1}$ is invertible, $\mathbf u$ is normal with mean $\mathbf 0$ and covariance $\mathbf L^{-1}\boldsymbol\Sigma\mathbf L^{-\top} = \mathbf I$ (Chapter 12, Theorem: Invertible Affine Maps Preserve Normality). Its density is therefore a product of $d$ standard normal densities, so its components are independent standard normals ([Chapter 5](ch5_random_variables.md)). Then $\mathbf y^\top\boldsymbol\Sigma^{-1}\mathbf y = \mathbf y^\top\mathbf L^{-\top}\mathbf L^{-1}\mathbf y = \mathbf u^\top\mathbf u = \sum_i u_i^2 \sim \chi^2_{d}$.

    For the innovation: by Chapter 13, $\tilde{\mathbf y}_k$ is a constant matrix $\mathbf A$ times the stacked vector $\boldsymbol\xi$ of the independent normal sources of assumption (A6), and $\boldsymbol\xi$ is multivariate normal (Chapter 12, Corollary: Stacking Independent Normal Vectors). Its covariance $\mathbf A\operatorname{Cov}(\boldsymbol\xi)\mathbf A^\top = \mathbf S_k$ is positive definite, which forces the rows of $\mathbf A$ to be linearly independent (if $\mathbf a^\top\mathbf A = \mathbf 0$ then $\mathbf a^\top\mathbf S_k\mathbf a = 0$, so $\mathbf a = \mathbf 0$). For such $\mathbf A$, Chapter 12 states that $\mathbf A\boldsymbol\xi$ is again normal. So $\tilde{\mathbf y}_k \sim \mathcal N(\mathbf 0, \mathbf S_k)$, and the first part applies. $\blacksquare$
    ///

    /// note | 📖 **Definition**
    <u>**Gating**</u>

    The practice of updating a filter with a measurement only if its normalized innovation squared $\tilde{\mathbf y}_k^\top\mathbf S_k^{-1}\tilde{\mathbf y}_k$ is at most a chosen threshold $\gamma$, and otherwise discarding the measurement (keeping $\hat{\mathbf x}_k = \hat{\mathbf x}_k^-$, $\mathbf P_k = \mathbf P_k^-$).
    ///

    /// admonition | 📐 **Corollary (False Rejection Rate)**
        attrs: {class: corollary, id: ch14-cor-false-rejection-rate}
    Under (A1)–(A6), a gate with threshold $\gamma$ rejects a valid measurement with probability $1 - F_{\chi^2_{m}}(\gamma)$, where $F_{\chi^2_{m}}$ is the cumulative distribution function of $\chi^2_{m}$.
    ///

    The threshold is therefore chosen as a quantile: the 99% quantile, $\gamma = 6.63$ for $m = 1$ or $9.21$ for $m = 2$, rejects 1% of valid readings. An outlier is rejected when it moves the innovation by several standard deviations $\sqrt{S}$. For the cart, $\sqrt S \approx 0.5$ m, so a 10 m glitch gives a normalized innovation squared near 400.

    The demonstration corrupts 10% of the cart's position readings with a glitch of $\pm 10$ m and runs the fused filter with and without a 99% gate.
    """)
    return


@app.cell
def gating_demo(
    IMAGES_DIR,
    cart_B,
    cart_F,
    cart_H,
    cart_ratio,
    cart_sensors,
    cart_sigma_acc,
    cart_sigma_pos,
    cart_t,
    cart_t_pos,
    cart_x,
    fusion_P0,
    fusion_x0,
    np,
    plt,
    run_filter,
    stats,
):
    # jb: include=false
    gate_gamma = stats.chi2.ppf(0.99, df=1)
    _u, _z_clean = cart_sensors(1, seed=5)
    _rng = np.random.default_rng(22)
    _is_outlier = _rng.random(_z_clean.shape[1]) < 0.10
    _z = _z_clean + _is_outlier * 10.0 * _rng.choice([-1.0, 1.0], size=_z_clean.shape[1])
    _Q = cart_sigma_acc**2 * cart_B @ cart_B.T
    _R = np.array([[cart_sigma_pos**2]])
    _xc, _, _, _ = run_filter(_u, _z_clean, cart_F, cart_B, cart_H, _Q, _R, fusion_x0, fusion_P0, cart_ratio)
    gate_rms_clean = np.sqrt(np.mean((_xc[:, 0, 0] - cart_x[1:, 0]) ** 2))
    _xa, _, _, _ = run_filter(_u, _z, cart_F, cart_B, cart_H, _Q, _R, fusion_x0, fusion_P0, cart_ratio)
    _xb, _Pb, _, _gated = run_filter(_u, _z, cart_F, cart_B, cart_H, _Q, _R, fusion_x0, fusion_P0, cart_ratio, gate=gate_gamma)
    _ea = _xa[:, 0, 0] - cart_x[1:, 0]
    _eb = _xb[:, 0, 0] - cart_x[1:, 0]
    gate_rms = (np.sqrt(np.mean(_ea**2)), np.sqrt(np.mean(_eb**2)))
    gate_counts = (
        int(_is_outlier.sum()),
        int(_is_outlier[_gated].sum()),
        int(len(_gated) - _is_outlier[_gated].sum()),
        int(_z.shape[1] - _is_outlier.sum()),
    )

    _fig, _ax = plt.subplots(figsize=(7.5, 3.6))
    _sd = np.sqrt(_Pb[:, 0, 0])
    _ax.fill_between(cart_t, -2 * _sd, 2 * _sd, color="C1", alpha=0.2, label=r"gated filter's $\pm 2\sigma$")
    _ax.plot(cart_t, _ea, color="C0", lw=1.0, label="no gate")
    _ax.plot(cart_t, _eb, color="C1", lw=1.2, label="99% gate")
    for _j in np.flatnonzero(_is_outlier):
        _ax.axvline(cart_t_pos[_j], color="red", ls=":", lw=0.8)
    _ax.plot([], [], color="red", ls=":", lw=0.8, label="glitched reading")
    _ax.axhline(0, color="black", lw=0.6)
    _ax.set_xlabel("time (s)")
    _ax.set_ylabel("position error (m)")
    _ax.set_title("Fused filter with 10% glitched position readings", style="italic")
    _ax.legend(loc="lower left", ncol=2, fontsize=8)
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch14_gating.svg", metadata={"Date": None})
    plt.close(_fig)
    return gate_counts, gate_gamma, gate_rms, gate_rms_clean


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch14_gating.svg" class="graphic" alt="Position error of two filters over 20 seconds, with dotted red lines at the times of glitched readings. The ungated filter's error jumps at every glitch and decays afterward; the gated filter's error stays small and inside its band." />
    """)
    return


@app.cell(hide_code=True)
def _(gate_counts, gate_gamma, gate_rms, gate_rms_clean, mo):
    mo.md(rf"""
    With $\gamma = {gate_gamma:.2f}$, the gate rejected {gate_counts[1]} of the {gate_counts[0]} glitched readings and {gate_counts[2]} of the {gate_counts[3]} valid ones. The root-mean-square position error is {gate_rms[0]:.3f} m without the gate and {gate_rms[1]:.3f} m with it; the same filter on the same readings *without* the glitches achieves {gate_rms_clean:.3f} m. The gate recovers almost all of the clean-data accuracy.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **Lock-out.** A gate trusts the filter's own $\mathbf S_k$. If the filter has diverged, or its covariance is too small for any other reason, *valid* readings fail the gate, the filter never gets corrected, and it rejects everything from then on. Monitor the rejection rate and re-initialize when it is far above $1 - F_{\chi^2_{m}}(\gamma)$.
    - **Gating makes the gain data-dependent.** Whether a reading is used depends on its value, so Chapter 13's proofs no longer apply exactly, and $\mathbf P_k$ becomes slightly optimistic. For rare, large outliers the effect is negligible.
    - **Small outliers pass.** A glitch of one or two $\sqrt S$ is indistinguishable from noise and is used. If such errors are common, the measurement noise is not Gaussian, and $\mathbf R$ or the noise model should change instead.
    - **The thresholds assume Gaussian innovations**, assumption (A6). Heavy-tailed noise produces more large innovations than $\chi^2$ predicts, and a 99% gate then rejects more than 1% of valid readings.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch14-sec-consistency-tests -->
    ## Consistency Tests

    A filter reports not only an estimate but also how uncertain it is. [Chapter 9](ch9_noise_levels.md) called a filter *consistent* when its estimation errors have mean zero and the variance it reports ({term}`filter consistency`); for vectors, $\mathbb E\mathbf e_k = \mathbf 0$ and $\operatorname{Cov}(\mathbf e_k) = \mathbf P_k$. Chapter 9 tested this with the normalized innovation squared. With a state vector there are two such tests: one that needs the truth and is therefore available only in simulation, and one that needs only the data.

    /// note | 📖 **Definition**
    <u>**Normalized estimation error squared**</u>

    For an estimate $\hat{\mathbf x}_k$ of a state $\mathbf x_k \in \mathbb R^n$ whose reported error covariance $\mathbf P_k$ is positive definite, the number
    $$\epsilon^{\mathbf x}_k := (\hat{\mathbf x}_k - \mathbf x_k)^\top\mathbf P_k^{-1}(\hat{\mathbf x}_k - \mathbf x_k).$$
    ///

    It is the squared {term}`Mahalanobis distance` of the true state from the estimate, measured with the filter's own covariance. Since it needs the true state, it can be computed only when the truth is known, as in a simulation.

    /// admonition | 📐 **Theorem (NEES and NIS of a Correct Filter)**
        attrs: {class: theorem, id: ch14-thm-nees-and-nis-of-a-correct-filter}
    Assume (A1)–(A6), and suppose the filter uses the true $\mathbf F, \mathbf B, \mathbf H, \mathbf Q, \mathbf R$, $\hat{\mathbf x}_0 = \mathbb E\mathbf x_0$, and $\mathbf P_0 = \operatorname{Cov}(\mathbf x_0)$, with $\mathbf P_k$ positive definite. Then $\epsilon^{\mathbf x}_k \sim \chi^2_{n}$ and $\epsilon_k := \tilde{\mathbf y}_k^\top\mathbf S_k^{-1}\tilde{\mathbf y}_k \sim \chi^2_{m}$ for every $k$. In particular, their means are $n$ and $m$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    By Chapter 13, $\mathbf e_k = \hat{\mathbf x}_k - \mathbf x_k$ is a sum of constant matrices times $\mathbf e_0 = \hat{\mathbf x}_0 - \mathbf x_0, \mathbf w_1, \ldots, \mathbf w_k, \mathbf v_1, \ldots, \mathbf v_k$, so under (A6) it is a constant matrix times the stacked vector of independent normal sources. Its mean is $\mathbf 0$ and its covariance is $\mathbf P_k$ (Chapter 13, because the filter's matrices are the true ones), which is positive definite. Exactly as for the innovation in the proof of the Lemma on normalized quadratic forms, $\mathbf e_k \sim \mathcal N(\mathbf 0, \mathbf P_k)$, and that Lemma gives $\epsilon^{\mathbf x}_k \sim \chi^2_{n}$. The statement for the innovation is part of the same Lemma. $\blacksquare$
    ///

    One run gives one $\epsilon^{\mathbf x}_k$ per step, which scatters widely. Averaging $N$ independent simulated runs sharpens the test.

    /// admonition | 📐 **Theorem (Monte Carlo Average)**
        attrs: {class: theorem, id: ch14-thm-monte-carlo-average}
    If $s^{(1)}, \ldots, s^{(N)}$ are independent and each has distribution $\chi^2_{d}$, then $\sum_{i=1}^N s^{(i)} \sim \chi^2_{Nd}$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    The distribution of a sum of independent random variables is determined by their individual distributions ([Chapter 5](ch5_random_variables.md)). So we may take $s^{(i)} = \sum_{j=1}^d u_{ij}^2$ with all $Nd$ variables $u_{ij}$ independent standard normal. The total is then a sum of $Nd$ such squares, which has distribution $\chi^2_{Nd}$ by definition. $\blacksquare$
    ///

    **The test.** Simulate $N$ independent runs, and at each step $k$ average the NEES over the runs: $\bar\epsilon^{\mathbf x}_k := \frac1N\sum_i\epsilon^{\mathbf x,(i)}_k$, where $\epsilon^{\mathbf x,(i)}_k$ is the NEES of run $i$. For a consistent filter, $N\bar\epsilon^{\mathbf x}_k \sim \chi^2_{Nn}$, so $\bar\epsilon^{\mathbf x}_k$ lies in
    $$\Big[\tfrac1N F^{-1}_{\chi^2_{Nn}}(0.025),\ \tfrac1N F^{-1}_{\chi^2_{Nn}}(0.975)\Big]$$
    with probability 95%, where $F^{-1}$ is the quantile function. About 95% of the steps should land inside this band. Averages persistently **above** the band mean the errors are larger than $\mathbf P_k$ claims: the filter is *overconfident*. Averages **below** it mean the filter is *underconfident*: it reports more uncertainty than it has and so gives the measurements too much or too little weight. The NIS test is the same with $m$ in place of $n$, and needs no truth, so it can run on real data. On a single real record, average the NIS over time instead of over runs; the innovations of a correct filter are uncorrelated over time, the vector version of Chapter 9's result [@barshalom2002, Ch. 5], so the same chi-squared band applies.

    The figure runs 50 independent simulations of the cart, each with its own initial-estimate error drawn from $\mathcal N(\mathbf 0, \mathbf P_0)$, its own accelerometer noise, and its own position noise. The sliders are the ones from the sensor-fusion section.
    """)
    return


@app.cell(hide_code=True)
def consistency_interactive(
    cart_B,
    cart_F,
    cart_H,
    cart_ratio,
    cart_sensors,
    cart_t,
    cart_t_pos,
    cart_x,
    dropout_slider,
    fusion_P0,
    fusion_models,
    graphic,
    mo,
    np,
    plt,
    q_scale_slider,
    r_scale_slider,
    run_filter,
    stats,
):
    _N = 50
    _Q, _R, _lost = fusion_models(q_scale_slider.value, r_scale_slider.value, dropout_slider.value)
    _u, _z = cart_sensors(_N, seed=100)
    _z = np.where(_lost[None, :], np.nan, _z)
    _x0 = np.random.default_rng(101).multivariate_normal(np.zeros(2), fusion_P0, size=_N)
    _xs, _Ps, _nis, _ = run_filter(_u, _z, cart_F, cart_B, cart_H, _Q, _R, _x0, fusion_P0, cart_ratio)
    _e = _xs - cart_x[1:, None, :]
    cons_nees = np.einsum("kri,kij,krj->kr", _e, np.linalg.inv(_Ps), _e).mean(axis=1)
    cons_nis = _nis.mean(axis=1)
    cons_nees_band = stats.chi2.ppf([0.025, 0.975], df=2 * _N) / _N
    cons_nis_band = stats.chi2.ppf([0.025, 0.975], df=_N) / _N
    _t_upd = cart_t_pos[~_lost]

    _fig, (_ax1, _ax2) = plt.subplots(2, 1, figsize=(7.5, 6.0), sharex=True)
    _ax1.axhspan(*cons_nees_band, color="gray", alpha=0.25, label="95% band")
    _ax1.axhline(2, color="black", lw=0.8, label="consistent mean $n = 2$")
    _ax1.plot(cart_t, cons_nees, color="C1", lw=0.8, label="average NEES (50 runs)")
    _ax1.set_yscale("log")
    _ax1.set_ylim(0.1, 50)
    _ax1.set_ylabel("NEES")
    _ax1.set_title("Normalized estimation error squared", style="italic")
    _ax1.legend(loc="upper right", fontsize=8)
    _ax2.axhspan(*cons_nis_band, color="gray", alpha=0.25, label="95% band")
    _ax2.axhline(1, color="black", lw=0.8, label="consistent mean $m = 1$")
    _ax2.plot(_t_upd, cons_nis, "o", ms=3, color="C1", label="average NIS (50 runs)")
    _ax2.set_yscale("log")
    _ax2.set_ylim(0.1, 50)
    _ax2.set_ylabel("NIS")
    _ax2.set_xlabel("time (s)")
    _ax2.set_title("Normalized innovation squared", style="italic")
    _ax2.legend(loc="upper right", fontsize=8)
    for _ax in (_ax1, _ax2):
        _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _fig.tight_layout()
    mo.vstack([
        mo.hstack([q_scale_slider, r_scale_slider, dropout_slider], justify="start", gap=2),
        graphic(_fig),
    ])
    return cons_nees, cons_nees_band, cons_nis, cons_nis_band


@app.cell(hide_code=True)
def _(cons_nees, cons_nees_band, cons_nis, cons_nis_band, mo, np):
    _in_nees = np.mean((cons_nees >= cons_nees_band[0]) & (cons_nees <= cons_nees_band[1]))
    _in_nis = np.mean((cons_nis >= cons_nis_band[0]) & (cons_nis <= cons_nis_band[1]))
    mo.md(rf"""
    Average NEES over all steps: {cons_nees.mean():.2f} (consistent: 2), inside the band at {100 * _in_nees:.0f}% of the steps. Average NIS over all updates: {cons_nis.mean():.2f} (consistent: 1), inside the band at {100 * _in_nis:.0f}% of the updates.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With the true noise levels, both averages sit near their consistent values and inside the band about 95% of the time, with or without lost readings. Now mis-tune the filter:

    - **Filter's $\sigma_p$ too small** (0.5): the filter believes the readings too much. NEES and NIS both rise far above the band.
    - **Filter's $\sigma_p$ too large** (2): both fall below it.
    - **Filter's $\sigma_{\text{acc}}$ too small** (0.2) or **too large** (5): NEES moves clearly out of the band, but NIS barely moves. The reason is in $\mathbf S = \mathbf H\mathbf P^-\mathbf H^\top + R$: for this cart, $R = 0.25\ \text{m}^2$ dominates $\mathbf H\mathbf P^-\mathbf H^\top \approx 0.007\ \text{m}^2$, so the innovation's spread hardly depends on $\mathbf Q$. **A passing NIS test does not prove that $\mathbf Q$ is right.** On real data, where NEES is unavailable, a wrong $\mathbf Q$ shows up instead as innovations that are correlated over time (Chapter 10's whiteness test).

    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **The bands assume Gaussian errors**, assumption (A6). With other noise distributions the NEES and NIS means are still $n$ and $m$ for a correctly tuned filter (the trace of $\mathbf P^{-1}\mathbf P$ is $n$), but the 95% bands are wrong.
    - **NEES needs the truth.** It tests a filter design in simulation, and the simulation must include the effects the real system has (biases, maneuvers, outliers). A filter that passes on idealized simulated data can fail on real data.
    - **Averages hide structure.** A filter can be consistent on average and badly inconsistent during maneuvers. Look at the time series, not only the average.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch14-sec-numerical-stability -->
    ## Numerical Stability

    Chapter 13's formulas are exact in exact arithmetic. Computers round, and the covariance recursion can amplify rounding until $\mathbf P_k$ is no longer a covariance matrix at all: not symmetric, or with a negative eigenvalue, which claims a negative variance for some combination of states. Once that happens, the gains are meaningless. Three habits prevent most of the trouble, and `run_filter` above uses all three:

    1. **Use the Joseph form.** It is the exact covariance of whatever gain was actually computed, and it is a sum of terms of the form $\mathbf M\mathbf A\mathbf M^\top$ with $\mathbf A$ positive semidefinite, so it cannot lose positive semidefiniteness through the update. The simplified form $(\mathbf I - \mathbf K\mathbf H)\mathbf P^-$ subtracts two nearly equal matrices when the measurement is much more precise than the prediction, and the difference can be mostly rounding error (Chapter 13 showed its error is first order in the gain error).
    2. **Symmetrize.** Replace $\mathbf P$ by $\tfrac12(\mathbf P + \mathbf P^\top)$ after each update to remove asymmetry from rounding.
    3. **Solve instead of invert.** Compute $\mathbf K^\top$ by solving $\mathbf S\mathbf K^\top = \mathbf H\mathbf P^-$ rather than forming $\mathbf S^{-1}$.

    The demonstration is a worst case that occurs in practice: a precise laser rangefinder ($\sigma = 1$ mm, $R = 10^{-6}\ \text{m}^2$) tracking a slowly moving object with the constant-velocity model ($\Delta t = 0.1$ s, $\sigma_a = 10^{-4}\ \text{m/s}^2$), started from a vague $\mathbf P_0 = 100\,\mathbf I$, and computed in single precision (`float32`, about 7 significant digits), as on a small microcontroller. Only the covariance recursion matters, so no data are needed. The reference is the Joseph form in double precision.
    """)
    return


@app.cell
def stability_demo(IMAGES_DIR, np, plt):
    # jb: include=false
    def _covariances(dtype, form, symmetrize, steps=300):
        _T, _sa, _r, _p0 = 0.1, 1e-4, 1e-6, 100.0
        _F = np.array([[1, _T], [0, 1]], dtype)
        _G = np.array([[_T * _T / 2], [_T]], dtype)
        _Q = (_sa**2 * _G @ _G.T).astype(dtype)
        _H = np.array([[1, 0]], dtype)
        _R = np.array([[_r]], dtype)
        _I = np.eye(2, dtype=dtype)
        _P = (_p0 * np.eye(2)).astype(dtype)
        _out = np.empty((steps, 2, 2))
        for _k in range(steps):
            _P = _F @ _P @ _F.T + _Q
            _S = _H @ _P @ _H.T + _R
            _K = (_P @ _H.T) / _S
            if form == "simplified":
                _P = (_I - _K @ _H) @ _P
            else:
                _P = (_I - _K @ _H) @ _P @ (_I - _K @ _H).T + _K @ _R @ _K.T
            if symmetrize:
                _P = (_P + _P.T) / 2
            _out[_k] = _P.astype(np.float64)
        return _out

    _ref = _covariances(np.float64, "joseph", False)
    _variants = [
        ("double precision, simplified", np.float64, "simplified", False),
        ("single precision, simplified", np.float32, "simplified", False),
        ("single precision, simplified + symmetrize", np.float32, "simplified", True),
        ("single precision, Joseph", np.float32, "joseph", False),
    ]
    stab_rows = []
    _curves = {}
    for _name, _dtype, _form, _sym in _variants:
        _P = _covariances(_dtype, _form, _sym)
        _Ps = 0.5 * (_P + np.transpose(_P, (0, 2, 1)))
        _not_psd = np.linalg.eigvalsh(_Ps)[:, 0] < 0
        _rel = np.abs(_P[:, 0, 0] / _ref[:, 0, 0] - 1)
        stab_rows.append((_name, int(_not_psd.sum()), float(_rel.max()), float(_rel[-1])))
        _curves[_name] = (_rel, _not_psd)

    _fig, _ax = plt.subplots(figsize=(7.5, 3.8))
    _k = np.arange(1, 301)
    _rel_s, _bad_s = _curves["single precision, simplified"]
    _rel_j, _ = _curves["single precision, Joseph"]
    for _i in np.flatnonzero(_bad_s):
        _ax.axvspan(_k[_i] - 0.5, _k[_i] + 0.5, color="red", alpha=0.12, lw=0)
    _ax.plot([], [], color="red", alpha=0.3, lw=6, label="simplified: P not a covariance matrix")
    _ax.plot(_k, np.maximum(_rel_s, 1e-9), color="C0", label="single precision, simplified")
    _ax.plot(_k, np.maximum(_rel_j, 1e-9), color="C1", label="single precision, Joseph")
    _ax.set_yscale("log")
    _ax.set_ylim(1e-9, 1e3)
    _ax.set_xlabel("step $k$")
    _ax.set_ylabel(r"relative error of $P_{11}$")
    _ax.set_title("Single-precision covariance updates versus the double-precision reference", style="italic")
    _ax.legend(loc="upper right", fontsize=8)
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch14_stability.svg", metadata={"Date": None})
    plt.close(_fig)
    stab_first = (float(_covariances(np.float32, "simplified", False, steps=1)[0, 0, 0]), float(_ref[0, 0, 0]))
    return stab_first, stab_rows


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch14_stability.svg" class="graphic" alt="Relative error of the position variance over 300 steps on a logarithmic axis. The single-precision simplified update starts with errors from about ten percent up to fifty times the true value, with a red-shaded stretch of about 80 steps where its matrix is not a valid covariance, before slowly recovering. The single-precision Joseph update stays below about one part in a thousand throughout." />
    """)
    return


@app.cell(hide_code=True)
def _(mo, stab_first, stab_rows):
    _lines = [
        "| Variant | Steps (of 300) where $\\mathbf P$ is not positive semidefinite | Largest relative error of $P_{11}$ | Relative error at step 300 |",
        "|:---|:---:|:---:|:---:|",
    ]
    for _name, _bad, _max, _last in stab_rows:
        _lines.append(f"| {_name} | {_bad} | {_max:.1e} | {_last:.1e} |")
    _lines += [
        "",
        f"After the very first update, the single-precision simplified form reports a position variance of "
        f"{stab_first[0]:.1e} m$^2$ (the correct value is {stab_first[1]:.2e} m$^2$): the gain rounds to exactly 1, "
        "and $1 - K$ rounds to 0. The filter claims perfect knowledge of the position. Symmetrizing does not repair "
        "this, because the damage is not asymmetry. The Joseph form recovers, because its $\\mathbf K\\mathbf R\\mathbf K^\\top$ "
        "term restores the measurement's own variance.",
    ]
    mo.md("\n".join(_lines))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In double precision this example is harmless, which is why desktop experiments rarely show the problem. On embedded hardware, or with larger and more poorly scaled state vectors (Part VI has 15 states mixing meters, radians, and sensor biases), it is real. The most robust remedy is a **square-root filter**, which never forms $\mathbf P$ at all: it propagates a factor $\mathbf L$ with $\mathbf P = \mathbf L\mathbf L^\top$, such as its Cholesky factor, so that $\mathbf P$ is positive semidefinite by construction, and it effectively doubles the available precision. Several variants (square-root covariance, square-root information, and $\mathbf U\mathbf D\mathbf U^\top$ factorizations) are described in [Wikipedia: Kalman filter](https://en.wikipedia.org/wiki/Kalman_filter) and in @barshalom2002.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch14-sec-filter-divergence -->
    ## Filter Divergence

    /// note | 📖 **Definition**
    <u>**Filter divergence**</u>

    The failure of a Kalman filter in which its actual estimation errors become, and remain, much larger than its reported error covariance $\mathbf P_k$ allows, so that the filter, trusting its small $\mathbf P_k$, keeps its gains too small for the measurements to correct those errors.
    ///

    Divergence is the dynamic form of overconfidence: the NEES is not just above its band but far above it and growing, and the errors do not shrink as more data arrive. The most common cause is a $\mathbf Q$ that is too small. [Chapter 9](ch9_noise_levels.md) showed the scalar version: with $Q = 0$, the gain falls like $1/k$, and the filter stops listening. A small $\mathbf Q$ makes $\mathbf P_k$ small, the small $\mathbf P_k$ makes the gain small, and the small gain lets the error grow unchecked whenever reality departs from the model.

    The demonstration removes the cart's accelerometer. A constant-velocity filter must now track the cart from the 10 Hz position readings alone, with the piecewise-constant acceleration $\mathbf Q$ and a chosen $\sigma_a$. The two maneuvers (gray bands) are what the constant-velocity model leaves out. The slider sets $\sigma_a$; the default is deliberately too small.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    div_sigma_a_slider = mo.ui.slider(
        steps=[0.001, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0],
        value=0.01,
        label=r"filter's $\sigma_a$ (m/s$^2$)",
        show_value=True,
    )
    return (div_sigma_a_slider,)


@app.cell
def position_only_setup(cart_H, cart_p_at_readings, cart_sensors, cart_x, cart_ratio, np, run_filter):
    # jb: include=false
    po_T = 0.1
    po_F = np.array([[1.0, po_T], [0.0, 1.0]])
    po_G = np.array([[po_T**2 / 2], [po_T]])
    po_truth = cart_x[cart_ratio::cart_ratio]  # truth at the 10 Hz reading times
    po_z = cart_sensors(1, seed=3)[1]

    def position_only_filter(sigma_a):
        """Constant-velocity filter at 10 Hz using only the position readings."""
        _Q = sigma_a**2 * po_G @ po_G.T
        _R = np.array([[0.25]])
        _u = np.zeros((1, po_z.shape[1]))
        return run_filter(_u, po_z, po_F, None, cart_H, _Q, _R, np.zeros(2), np.diag([1.0, 0.25]), 1)

    return po_F, po_G, po_T, po_truth, po_z, position_only_filter


@app.cell(hide_code=True)
def divergence_interactive(
    cart_t_pos,
    div_sigma_a_slider,
    graphic,
    mo,
    np,
    plt,
    po_truth,
    position_only_filter,
    stats,
):
    _xs, _Ps, _, _ = position_only_filter(div_sigma_a_slider.value)
    div_err = _xs[:, 0, :] - po_truth
    div_sd = np.sqrt(_Ps[:, 0, 0])
    div_nees = np.einsum("ki,kij,kj->k", div_err, np.linalg.inv(_Ps), div_err)
    div_band = stats.chi2.ppf([0.025, 0.975], df=2)

    _fig, (_ax1, _ax2) = plt.subplots(2, 1, figsize=(7.5, 6.0), sharex=True)
    for _ax in (_ax1, _ax2):
        _ax.axvspan(2, 6, color="gray", alpha=0.15)
        _ax.axvspan(12, 16, color="gray", alpha=0.15)
    _ax1.fill_between(cart_t_pos, -2 * div_sd, 2 * div_sd, color="C1", alpha=0.2, label=r"filter's $\pm 2\sigma$")
    _ax1.plot(cart_t_pos, div_err[:, 0], color="C1", label="position error")
    _ax1.axhline(0, color="black", lw=0.6)
    _ax1.set_ylabel("position error (m)")
    _ax1.set_title(rf"Position-only filter, $\sigma_a = {div_sigma_a_slider.value:g}$ m/s$^2$", style="italic")
    _ax1.legend(loc="upper left", fontsize=8)
    _ax2.axhspan(*div_band, color="gray", alpha=0.25, label="95% band for one run")
    _ax2.plot(cart_t_pos, np.maximum(div_nees, 1e-3), color="C1", lw=1.0, label="NEES")
    _ax2.set_yscale("log")
    _ax2.set_ylim(1e-3, 1e5)
    _ax2.set_ylabel("NEES")
    _ax2.set_xlabel("time (s)")
    _ax2.legend(loc="upper left", fontsize=8)
    for _ax in (_ax1, _ax2):
        _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _fig.tight_layout()
    mo.vstack([div_sigma_a_slider, graphic(_fig)])
    return div_band, div_err, div_nees, div_sd


@app.cell(hide_code=True)
def _(div_err, div_nees, div_sd, mo, np):
    _out = np.mean(np.abs(div_err[:, 0]) > 2 * div_sd)
    mo.md(rf"""
    Largest position error: {np.abs(div_err[:, 0]).max():.2f} m, while the filter's final standard deviation is {div_sd[-1]:.2f} m. The error is outside the $\pm 2\sigma$ band {100 * _out:.0f}% of the time, and the average NEES is {div_nees.mean():.3g} (consistent: 2).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With $\sigma_a = 0.01\ \text{m/s}^2$, the filter is sure the cart moves at constant velocity. When the cart accelerates, the filter's estimate lags by meters while it reports centimeters of uncertainty, and because its gains are tiny it keeps lagging long after the maneuver ends: it has diverged. Raising $\sigma_a$ restores consistency. For this trajectory, values near $1\ \text{m/s}^2$, about twice the largest acceleration, keep the NEES near its band. That is more than the rule of thumb above, because a four-second constant acceleration is not white noise at all. Very large values are consistent but noisy, because the filter then follows every reading.

    Remedies, roughly in order of effort:

    - **Increase $\mathbf Q$** until the consistency tests pass during maneuvers, accepting more noise when the motion is calm.
    - **Model what is missing.** Here, the accelerometer, which makes the maneuvers known inputs. In general, add states for the unmodeled effect, as for the bias above.
    - **Adapt.** Monitor the NIS and inflate $\mathbf Q$ when it rises (maneuver detection), or run several models at once and weight them by their innovations (the interacting multiple model estimator) [@barshalom2002].
    - **Never let $\mathbf P$ collapse.** A floor on the diagonal of $\mathbf P$, or a *fading-memory* factor that multiplies $\mathbf P^-$ by a number slightly above 1, keeps the gains from going to zero.

    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **Divergence is invisible to the filter.** Its own $\mathbf P_k$ says everything is fine. Only external checks, the NIS on real data or the NEES in simulation, reveal it.
    - **Gating makes divergence permanent.** A diverged filter with a gate rejects the very readings that could rescue it (lock-out, above).
    - **Other causes.** Besides a small $\mathbf Q$: unmodeled biases (as in the two-state cart filter above), wrong $\mathbf F$ or $\mathbf H$, a $\mathbf P_0$ that is too small, and numerical loss of positive definiteness.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch14-sec-smoothing -->
    ## Smoothing

    The filter's estimate $\hat{\mathbf x}_k$ uses $\mathbf z_1, \ldots, \mathbf z_k$ only, because a real-time filter cannot see the future. When the whole record is available afterwards, as in the gait analysis of Part VI, the estimate of $\mathbf x_k$ can also use $\mathbf z_{k+1}, \ldots, \mathbf z_K$. The **Rauch–Tung–Striebel smoother** does this with one backward pass over the filter's stored output. Starting from $\hat{\mathbf x}_K^s = \hat{\mathbf x}_K$ and $\mathbf P_K^s = \mathbf P_K$, for $k = K-1, \ldots, 1$:
    $$\mathbf C_k = \mathbf P_k\mathbf F^\top(\mathbf P_{k+1}^-)^{-1}, \qquad \hat{\mathbf x}_k^s = \hat{\mathbf x}_k + \mathbf C_k\big(\hat{\mathbf x}_{k+1}^s - \hat{\mathbf x}_{k+1}^-\big), \qquad \mathbf P_k^s = \mathbf P_k + \mathbf C_k\big(\mathbf P_{k+1}^s - \mathbf P_{k+1}^-\big)\mathbf C_k^\top.$$
    Under (A1)–(A6), $\hat{\mathbf x}_k^s = \mathbb E[\mathbf x_k \mid \mathbf z_1, \ldots, \mathbf z_K]$ and $\mathbf P_k^s = \operatorname{Cov}(\mathbf x_k \mid \mathbf z_1, \ldots, \mathbf z_K)$. The proof is not given here; see @rauch1965. The hidden cell below checks the claim numerically against direct Gaussian conditioning on all measurements of a short record, and then applies the smoother to the position-only cart filter with $\sigma_a = 1\ \text{m/s}^2$.
    """)
    return


@app.cell
def rts_demo(
    IMAGES_DIR,
    cart_t_pos,
    np,
    plt,
    po_F,
    po_G,
    po_truth,
    position_only_filter,
):
    # jb: include=false
    def rts_smoother(xs, Ps, F, Q):
        """RTS backward pass over filtered estimates xs (K x n) and covariances Ps (K x n x n)."""
        _xs_s, _Ps_s = xs.copy(), Ps.copy()
        for _k in range(len(xs) - 2, -1, -1):
            _x_pred = F @ xs[_k]
            _P_pred = F @ Ps[_k] @ F.T + Q
            _C = Ps[_k] @ F.T @ np.linalg.inv(_P_pred)
            _xs_s[_k] = xs[_k] + _C @ (_xs_s[_k + 1] - _x_pred)
            _Ps_s[_k] = Ps[_k] + _C @ (_Ps_s[_k + 1] - _P_pred) @ _C.T
        return _xs_s, _Ps_s

    # 1. Check against direct Gaussian conditioning on a short record.
    _rng = np.random.default_rng(8)
    _T, _N = 0.5, 8
    _F = np.array([[1.0, _T], [0.0, 1.0]])
    _G = np.array([[_T**2 / 2], [_T]])
    _Q = 0.3 * _G @ _G.T + 1e-3 * np.eye(2)
    _H = np.array([[1.0, 0.0]])
    _r = 0.4
    _x0, _P0 = np.array([0.0, 1.0]), np.diag([1.0, 0.5])
    # every x_k and z_k is linear in y = [x_0, w_1..w_N, v_1..v_N]
    _dim = 2 + 3 * _N
    _cov = np.zeros((_dim, _dim))
    _cov[:2, :2] = _P0
    for _j in range(_N):
        _cov[2 + 2 * _j : 4 + 2 * _j, 2 + 2 * _j : 4 + 2 * _j] = _Q
        _cov[2 + 2 * _N + _j, 2 + 2 * _N + _j] = _r
    _mean = np.zeros(_dim)
    _mean[:2] = _x0
    _Mx = np.zeros((2, _dim))
    _Mx[:, :2] = np.eye(2)
    _Xmap, _Zmap = [], []
    for _k in range(_N):
        _Mx = _F @ _Mx
        _Mx[:, 2 + 2 * _k : 4 + 2 * _k] += np.eye(2)
        _Mz = _H @ _Mx
        _Mz[0, 2 + 2 * _N + _k] += 1.0
        _Xmap.append(_Mx.copy())
        _Zmap.append(_Mz)
    _Xm, _Zm = np.vstack(_Xmap), np.vstack(_Zmap)
    _z = _Zm @ (_mean + np.linalg.cholesky(_cov) @ _rng.normal(size=_dim))
    _Sxz, _Szz = _Xm @ _cov @ _Zm.T, _Zm @ _cov @ _Zm.T
    _post_mean = _Xm @ _mean + _Sxz @ np.linalg.solve(_Szz, _z - _Zm @ _mean)
    _post_cov = _Xm @ _cov @ _Xm.T - _Sxz @ np.linalg.solve(_Szz, _Sxz.T)
    _x, _P = _x0.copy(), _P0.copy()
    _xf, _Pf = [], []
    for _k in range(_N):
        _x, _P = _F @ _x, _F @ _P @ _F.T + _Q
        _S = _H @ _P @ _H.T + _r
        _K = _P @ _H.T / _S
        _x = _x + _K[:, 0] * (_z[_k] - _x[0])
        _P = (np.eye(2) - _K @ _H) @ _P
        _xf.append(_x)
        _Pf.append(_P)
    _xsm, _Psm = rts_smoother(np.array(_xf), np.array(_Pf), _F, _Q)
    rts_check = (
        np.abs(_xsm.ravel() - _post_mean).max(),
        max(np.abs(_Psm[_k] - _post_cov[2 * _k : 2 * _k + 2, 2 * _k : 2 * _k + 2]).max() for _k in range(_N)),
    )

    # 2. Smooth the position-only cart filter.
    _sa = 1.0
    _xs, _Ps, _, _ = position_only_filter(_sa)
    _xs = _xs[:, 0, :]
    _xs_s, _Ps_s = rts_smoother(_xs, _Ps, po_F, _sa**2 * po_G @ po_G.T)
    _ef, _es = _xs - po_truth, _xs_s - po_truth
    rts_rms = (np.sqrt(np.mean(_ef**2, axis=0)), np.sqrt(np.mean(_es**2, axis=0)))

    _fig, _ax = plt.subplots(figsize=(7.5, 3.6))
    _ax.plot(np.concatenate([[0.0], cart_t_pos]), np.concatenate([[0.0], po_truth[:, 1]]), color="black", lw=1.2, label="truth")
    _ax.plot(cart_t_pos, _xs[:, 1], color="C0", lw=1.0, label="filter (past readings only)")
    _ax.plot(cart_t_pos, _xs_s[:, 1], color="C1", lw=1.4, label="RTS smoother (all readings)")
    _ax.set_xlabel("time (s)")
    _ax.set_ylabel("velocity (m/s)")
    _ax.set_title(r"Velocity from position readings alone, $\sigma_a = 1$ m/s$^2$", style="italic")
    _ax.legend(loc="upper right", fontsize=8)
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch14_rts.svg", metadata={"Date": None})
    plt.close(_fig)
    return rts_check, rts_rms


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch14_rts.svg" class="graphic" alt="Velocity over 20 seconds. The true velocity is a trapezoid rising from 0 to 2 m/s and back. The filter's estimate is noisy and lags behind each ramp; the smoother's estimate is much smoother, rounds the corners slightly, and follows the ramps without lag." />
    """)
    return


@app.cell(hide_code=True)
def _(mo, rts_check, rts_rms):
    mo.md(rf"""
    The smoother agrees with direct conditioning on all measurements to within ${rts_check[0]:.0e}$ (means) and ${rts_check[1]:.0e}$ (covariances). On the cart, it reduces the root-mean-square position error from {rts_rms[0][0]:.3f} m to {rts_rms[1][0]:.3f} m and the velocity error from {rts_rms[0][1]:.3f} m/s to {rts_rms[1][1]:.3f} m/s, and it removes the filter's lag at the maneuvers.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch14-sec-summary -->
    ## Summary

    - **Initialization:** when in doubt, choose $\mathbf P_0$ large. A diffuse prior reproduces first-measurement (scalar) or two-point (position and velocity) initialization.
    - **Choosing $\mathbf Q$:** decide how the unmodeled acceleration behaves. Piecewise-constant acceleration gives $\sigma_a^2\boldsymbol\Gamma\boldsymbol\Gamma^\top$; continuous white-noise acceleration gives $q\,[\Delta t^3/3,\ \Delta t^2/2;\ \Delta t^2/2,\ \Delta t]$, derived by integrating the noise through the dynamics. A noisy control input, like an accelerometer, contributes its own noise as process noise.
    - **Sequential updates:** with block-diagonal $\mathbf R$, processing the blocks one at a time gives exactly the batch result, because information adds: $\mathbf P^{-1} = (\mathbf P^-)^{-1} + \mathbf H^\top\mathbf R^{-1}\mathbf H$. A Cholesky factor of $\mathbf R$ decorrelates any measurement.
    - **Missing and multi-rate data:** a step without a measurement is a step with $m_k = 0$. Predict at the fastest rate, update whenever a reading arrives.
    - **Sensor fusion:** the accelerometer as control input plus position updates beats both sensors. An unmodeled bias makes the filter overconfident; adding the bias as an observable state fixes it.
    - **Gating:** reject readings whose NIS exceeds a $\chi^2_{m}$ quantile. Beware of lock-out.
    - **Consistency:** for a correct filter, NEES $\sim \chi^2_{n}$ and NIS $\sim \chi^2_{m}$. Monte Carlo averages with chi-squared bands detect mis-tuning. NIS alone can miss a wrong $\mathbf Q$.
    - **Numerical stability:** use the Joseph form, symmetrize, and solve instead of inverting; square-root filters for hard cases.
    - **Divergence:** a $\mathbf Q$ too small for the real motion makes the filter confidently wrong. Only external checks reveal it.
    - **Smoothing:** with the whole record available, the RTS smoother's backward pass uses future measurements too.

    <!-- label: ch14-sec-whats-next -->
    ## What's Next

    Every model in Parts II and III was linear: $\mathbf F\mathbf x$, $\mathbf H\mathbf x$. A pendulum's acceleration depends on the *sine* of its angle, a range sensor measures a square root, and an orientation is not a vector at all. [Chapter 15](ch15_extended_kalman_filter.md) begins Part IV by linearizing such models around the current estimate. That gives the extended Kalman filter, and with it a new set of failure modes that the consistency tests of this chapter will help detect.
    """)
    return


if __name__ == "__main__":
    app.run()
