# /// script
# dependencies = [
#     "marimo>=0.25.1",
#     "matplotlib==3.11.2",
#     "numpy==2.5.3",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="21. Zero-Velocity Updates", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "Gait Analysis with a Foot-Mounted IMU"
    abbreviations:
      IMU: inertial measurement unit
      INS: inertial navigation system
      ZUPT: zero-velocity update
      ZARU: zero angular rate update
      EKF: extended Kalman filter
      SHOE: stance hypothesis optimal detector
      ENU: east-north-up
      FLU: forward-left-up
      HDE: heuristic drift elimination
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
    [Chapter 20](ch20_strapdown_inertial_navigation.md) left us with two facts. A foot-mounted IMU integrated on its own drifts hundreds of meters in half a minute. Yet once per stride the foot stands still, and a detector can tell us when. This chapter combines them. Its key concept is the **zero-velocity update**: treating "the velocity is zero" as a *measurement* in a Kalman filter.

    The payoff is larger than it looks. A velocity measurement corrects more than the velocity, because the filter's covariance matrix records how attitude errors and sensor biases *produced* the velocity error during the preceding swing. One update therefore corrects all of them. The result is a trajectory accurate to millimeters per stride, from which we compute the quantities a clinician wants: stride length, stride time, cadence, gait speed, foot clearance, and turning angle. We will also meet a hard limit: no number of zero-velocity updates can tell the filter which way it is facing.

    /// attention | 🗝️ **Key Idea**
    "The foot is not moving" is a measurement. Fed to an error-state Kalman filter once per stride, it bounds the velocity error and, through the filter's cross-covariances, corrects position, tilt, and sensor biases too. Heading is the exception: it is unobservable from zero-velocity information.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// important | 🔗 **Prerequisites**
    - [Chapter 20](ch20_strapdown_inertial_navigation.md): [the navigation equations](#ch20-sec-the-navigation-equations) and their [discrete mechanization](#ch20-sec-discrete-implementation-at-100-hz), [the drift laws](#ch20-thm-drift-laws), [the gait cycle](#ch20-sec-the-gait-cycle), [the gait simulator](#ch20-sec-a-synthetic-gait-simulator), and [the SHOE detector](#ch20-thm-glrt-for-a-stationary-imu).
    - [Chapter 19](ch19_ahrs.md): [the error-state Kalman filter](#ch19-sec-an-error-state-kalman-filter) with the right (body-frame) attitude perturbation $q = \hat q\otimes\delta q(\delta\boldsymbol\theta)$, [its injection and reset steps](#ch19-sec-injection-and-reset), and [the magnetometer](#ch19-sec-heading-from-the-magnetometer).
    - [Chapter 13](ch13_kalman_filter.md): [the Kalman filter](#ch13-sec-the-algorithm), [the Joseph form](#ch13-sec-update), [observability](#ch13-sec-observability), and [the rank test](#ch13-thm-rank-test-for-observability).
    - [Chapter 15](ch15_extended_kalman_filter.md): [linearization](#ch15-sec-linearization) and [the extended Kalman filter](#ch15-sec-the-extended-kalman-filter).
    - [Chapter 10](ch10_process_models.md): [discretization of continuous-time models](#ch10-sec-continuous-time-models-and-discretization).
    - [Chapter 17](ch17_rotations.md) and [Chapter 18](ch18_quaternions.md): $\operatorname{Exp}$, $\operatorname{Exp}_q$, $\operatorname{Log}_q$, [the small-angle approximation](#ch17-thm-small-angle-approximation) $\operatorname{Exp}(\delta\boldsymbol\theta) \approx \mathbf I + [\delta\boldsymbol\theta]_\times$, and the identity $[\mathbf R\mathbf a]_\times = \mathbf R[\mathbf a]_\times\mathbf R^\top$.
    - [Appendix D: Cross Products and Skew-Symmetric Matrices](#appd-sec-cross-products-and-skew-symmetric-matrices), [Appendix D: The Matrix Exponential](#appd-sec-the-matrix-exponential), and [Appendix D: Block Matrices and the Schur Complement](#appd-sec-block-matrices-and-the-schur-complement).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch21-sec-tools-from-chapter-20 -->
    ## Tools from Chapter 20

    We use Chapter 20's conventions (ENU navigation frame, FLU body frame, $\mathbf R := \mathbf R^n_b$, specific force $\mathbf f = \mathbf R^\top(\mathbf a^n - \mathbf g^n)$, IMU model $\boldsymbol\omega_m = \boldsymbol\omega + \mathbf b_g + \mathbf n_g$, $\mathbf f_m = \mathbf f + \mathbf b_a + \mathbf n_a$ at 100 Hz) and its code. Notebooks are self-contained, so the quaternion helpers, the mechanization with leveling, the gait simulator, and the detectors are copied verbatim into hidden cells of this notebook; see [Chapter 20](ch20_strapdown_inertial_navigation.md) for the code and its derivations. Our running example is again the U-turn walk with the default sensor errors, and SHOE with threshold $\gamma = 10^3$ decides which samples are stationary.
    """)
    return


@app.cell
def helpers(np):
    # jb: include=false
    # Copied verbatim from Chapter 20.
    G = 9.81                          # gravity magnitude, m/s^2
    G_N = np.array([0.0, 0.0, -G])    # gravity in ENU coordinates

    def skew(a):
        """[a]_x, so that skew(a) @ b == np.cross(a, b)."""
        return np.array([[0.0, -a[2], a[1]], [a[2], 0.0, -a[0]], [-a[1], a[0], 0.0]])

    def quat_mult(p, q):
        """Hamilton product of scalar-first quaternions p and q."""
        pw, px, py, pz = p
        qw, qx, qy, qz = q
        return np.array([
            pw * qw - px * qx - py * qy - pz * qz,
            pw * qx + px * qw + py * qz - pz * qy,
            pw * qy - px * qz + py * qw + pz * qx,
            pw * qz + px * qy - py * qx + pz * qw,
        ])

    def quat_conj(q):
        return np.array([q[0], -q[1], -q[2], -q[3]])

    def quat_exp(phi):
        """Unit quaternion of the rotation vector phi."""
        angle = np.linalg.norm(phi)
        if angle < 1e-12:
            q = np.array([1.0, 0.5 * phi[0], 0.5 * phi[1], 0.5 * phi[2]])
            return q / np.linalg.norm(q)
        return np.concatenate([[np.cos(angle / 2)], np.sin(angle / 2) * phi / angle])

    def quat_log(q):
        """Rotation vector of the unit quaternion q (angle in [0, pi])."""
        q = q if q[0] >= 0 else -q
        s = np.linalg.norm(q[1:])
        if s < 1e-12:
            return 2.0 * q[1:]
        return 2.0 * np.arctan2(s, q[0]) * q[1:] / s

    def quat_to_rotmat(q):
        """Rotation matrix R(q), body to navigation."""
        w, x, y, z = q
        return np.array([
            [1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
            [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
            [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)],
        ])

    def rotmat_to_euler(R):
        """ZYX Euler angles (roll, pitch, yaw) of R = Rz(yaw) Ry(pitch) Rx(roll); R may be (..., 3, 3)."""
        roll = np.arctan2(R[..., 2, 1], R[..., 2, 2])
        pitch = -np.arcsin(np.clip(R[..., 2, 0], -1.0, 1.0))
        yaw = np.arctan2(R[..., 1, 0], R[..., 0, 0])
        return roll, pitch, yaw

    return (
        G,
        G_N,
        quat_conj,
        quat_exp,
        quat_log,
        quat_mult,
        quat_to_rotmat,
        rotmat_to_euler,
        skew,
    )


@app.cell
def strapdown_cell(G_N, np, quat_exp, quat_mult, quat_to_rotmat):
    # jb: include=false
    # Copied verbatim from Chapter 20.
    def strapdown(omega_m, f_m, dt, q0, v0, p0):
        """Integrate N x 3 arrays of IMU samples from the initial state (q0, v0, p0)."""
        N = len(omega_m)
        q, v, p = np.empty((N, 4)), np.empty((N, 3)), np.empty((N, 3))
        q[0], v[0], p[0] = q0, v0, p0
        a_prev = quat_to_rotmat(q0) @ f_m[0] + G_N
        for k in range(1, N):
            q_k = quat_mult(q[k - 1], quat_exp(0.5 * (omega_m[k - 1] + omega_m[k]) * dt))
            q[k] = q_k / np.linalg.norm(q_k)
            a_k = quat_to_rotmat(q[k]) @ f_m[k] + G_N      # navigation-frame acceleration
            v[k] = v[k - 1] + 0.5 * (a_prev + a_k) * dt
            p[k] = p[k - 1] + 0.5 * (v[k - 1] + v[k]) * dt
            a_prev = a_k
        return q, v, p

    def align_level(f_m_still):
        """Initial attitude from the mean specific force of a stationary IMU (yaw = 0)."""
        fx, fy, fz = f_m_still.mean(axis=0)
        roll, pitch = np.arctan2(fy, fz), np.arctan2(-fx, np.hypot(fy, fz))
        return quat_mult(quat_exp(np.array([0.0, pitch, 0.0])), quat_exp(np.array([roll, 0.0, 0.0])))

    return align_level, strapdown


@app.cell
def simulator(G_N, np):
    # jb: include=false
    # Copied verbatim from Chapter 20.
    def min_jerk(x):
        """Minimum-jerk profile s(x) = 10x^3 - 15x^4 + 6x^5 and its first two derivatives."""
        return (10 * x**3 - 15 * x**4 + 6 * x**5, 30 * x**2 * (1 - x) ** 2,
                60 * x * (1 - x) * (1 - 2 * x))

    def simulate_gait(
        n_strides=20, stride_time=1.1, stride_length=1.4, stance_frac=0.6, flat_frac=0.3,
        clearance=0.12, pitch_toe_off=0.5, pitch_heel_strike=-0.35, turn_angles=0.0, rise=0.0,
        still_start=2.0, still_end=1.0, fs=100.0, gyro_noise=0.01, gyro_bias=0.01,
        accel_noise=0.05, accel_bias=0.05, seed=0,
    ):
        """Foot-mounted IMU during walking. Angles in rad, lengths in m, times in s.
        turn_angles and rise are per stride (scalars are broadcast)."""
        dt = 1.0 / fs
        # Event timing in whole samples; each moving window starts at heel off
        nT = round(stride_time * fs)
        n_move = round((1.0 - flat_frac) * stride_time * fs)
        n_push = round(0.5 * (stance_frac - flat_frac) * stride_time * fs)   # heel off -> toe off
        n_swing = round((1.0 - stance_frac) * stride_time * fs)              # toe off -> heel strike
        n0 = round(still_start * fs)
        N = n0 + (n_strides - 1) * nT + n_move + round(still_end * fs) + 1
        turns = np.broadcast_to(np.asarray(turn_angles, float), (n_strides,))
        rises = np.broadcast_to(np.asarray(rise, float), (n_strides,))

        # Footprints (IMU position during foot flat) and stance headings
        psi_fp = np.concatenate([[0.0], np.cumsum(turns)])
        chi = psi_fp[:-1] + 0.5 * turns
        d = np.stack([stride_length * np.cos(chi), stride_length * np.sin(chi), rises], axis=1)
        P_fp = np.vstack([np.zeros(3), np.cumsum(d, axis=0)])

        # Stride index i, sample within stride u, normalized time tau of the moving window
        k = np.arange(N)
        i = np.clip((k - n0) // nT, 0, n_strides - 1)
        u = k - n0 - i * nT
        moving = (u > 0) & (u < n_move)
        m, after = moving.astype(float), (u >= n_move).astype(float)
        tau = np.clip(u / n_move, 0.0, 1.0)
        Tm = n_move * dt

        # Position: minimum-jerk along the stride vector plus the clearance bump
        s, s1, s2 = min_jerk(tau)
        c = 256 * tau**4 * (1 - tau) ** 4
        c1 = 1024 * tau**3 * (1 - tau) ** 3 * (1 - 2 * tau)
        c2 = 1024 * tau**2 * (1 - tau) ** 2 * (3 - 14 * tau + 14 * tau**2)
        p = P_fp[i] + (m * s + after)[:, None] * d[i]
        p[:, 2] += m * clearance * c
        v = (m * s1 / Tm)[:, None] * d[i]
        v[:, 2] += m * clearance * c1 / Tm
        a = (m * s2 / Tm**2)[:, None] * d[i]
        a[:, 2] += m * clearance * c2 / Tm**2

        # Heading: minimum-jerk turn. Pitch: A tau^3 (1-tau)^4 + B tau^4 (1-tau)^3 through the keyframes
        psi = psi_fp[i] + (m * s + after) * turns[i]
        psi_dot = m * s1 / Tm * turns[i]
        tau_to, tau_hs = n_push / n_move, (n_push + n_swing) / n_move
        basis = lambda x: np.array([x**3 * (1 - x) ** 4, x**4 * (1 - x) ** 3])
        A, B = np.linalg.solve(np.stack([basis(tau_to), basis(tau_hs)]), [pitch_toe_off, pitch_heel_strike])
        theta = m * (A * tau**3 * (1 - tau) ** 4 + B * tau**4 * (1 - tau) ** 3)
        theta_dot = m * (A * tau**2 * (1 - tau) ** 3 * (3 - 7 * tau)
                         + B * tau**3 * (1 - tau) ** 2 * (4 - 7 * tau)) / Tm

        # Attitude R = Rz(psi) Ry(theta), quaternion, body rate (lemma), specific force
        cps, sps, cth, sth = np.cos(psi), np.sin(psi), np.cos(theta), np.sin(theta)
        R = np.zeros((N, 3, 3))
        R[:, 0, 0], R[:, 0, 1], R[:, 0, 2] = cps * cth, -sps, cps * sth
        R[:, 1, 0], R[:, 1, 1], R[:, 1, 2] = sps * cth, cps, sps * sth
        R[:, 2, 0], R[:, 2, 2] = -sth, cth
        q = np.stack([np.cos(psi / 2) * np.cos(theta / 2), -np.sin(psi / 2) * np.sin(theta / 2),
                      np.cos(psi / 2) * np.sin(theta / 2), np.sin(psi / 2) * np.cos(theta / 2)], axis=1)
        omega = np.stack([-psi_dot * sth, theta_dot, psi_dot * cth], axis=1)
        f = np.einsum("nji,nj->ni", R, a - G_N)

        # Sensor errors: constant biases with random signs, plus white noise
        rng = np.random.default_rng(seed)
        b_g = gyro_bias * rng.choice([-1.0, 1.0], 3)
        b_a = accel_bias * rng.choice([-1.0, 1.0], 3)
        omega_m = omega + b_g + gyro_noise * rng.standard_normal((N, 3))
        f_m = f + b_a + accel_noise * rng.standard_normal((N, 3))

        t_ho = (n0 + np.arange(n_strides) * nT) * dt
        events = dict(heel_off=t_ho, toe_off=t_ho + n_push * dt,
                      heel_strike=t_ho + (n_push + n_swing) * dt, foot_flat=t_ho + Tm)
        return dict(
            t=k * dt, dt=dt, p=p, v=v, a=a, q=q, R=R, roll=0 * psi, pitch=theta, yaw=psi,
            omega=omega, f=f, omega_m=omega_m, f_m=f_m, b_g=b_g, b_a=b_a, still=~moving,
            events=events, footprints=P_fp, headings=psi_fp,
            stride_length=np.linalg.norm(d[:, :2], axis=1), stride_time=np.full(n_strides, nT * dt),
            clearance=np.full(n_strides, clearance), turn=np.array(turns),
        )

    return (simulate_gait,)


@app.cell
def detectors(G, np):
    # jb: include=false
    # Copied verbatim from Chapter 20.
    def imu_windows(x, W):
        """Windows of W samples centered on each sample (edges padded): shape (N, W, 3)."""
        h = W // 2
        xp = np.concatenate([np.repeat(x[:1], h, axis=0), x, np.repeat(x[-1:], W - 1 - h, axis=0)])
        return np.stack([xp[j:j + len(x)] for j in range(W)], axis=1)

    def stat_mag(f_m, omega_m, W=5, sigma_a=0.05, sigma_g=0.01):
        """Acceleration-magnitude statistic."""
        return ((np.linalg.norm(imu_windows(f_m, W), axis=2) - G) ** 2).mean(axis=1) / sigma_a**2

    def stat_are(f_m, omega_m, W=5, sigma_a=0.05, sigma_g=0.01):
        """Angular-rate-energy statistic."""
        return (imu_windows(omega_m, W) ** 2).sum(axis=2).mean(axis=1) / sigma_g**2

    def stat_shoe(f_m, omega_m, W=5, sigma_a=0.05, sigma_g=0.01):
        """SHOE (GLRT) statistic of Skog et al. (2010)."""
        fw, ww = imu_windows(f_m, W), imu_windows(omega_m, W)
        u = fw.mean(axis=1)
        u /= np.linalg.norm(u, axis=1, keepdims=True)
        accel_term = ((fw - G * u[:, None, :]) ** 2).sum(axis=2) / sigma_a**2
        gyro_term = (ww**2).sum(axis=2) / sigma_g**2
        return (accel_term + gyro_term).mean(axis=1)

    return stat_are, stat_mag, stat_shoe


@app.cell
def _(np, simulate_gait, stat_shoe):
    # jb: editor=true
    walk_turns = np.r_[np.zeros(10), np.full(4, np.pi / 4), np.zeros(10)]
    sim = simulate_gait(n_strides=24, turn_angles=walk_turns, seed=0)
    GAMMA = 1e3
    stationary = stat_shoe(sim["f_m"], sim["omega_m"]) < GAMMA
    return GAMMA, sim, stationary, walk_turns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch21-sec-zero-velocity-as-a-measurement -->
    ## Zero Velocity as a Measurement

    A Kalman filter combines a prediction with measurements, and a measurement is anything with a known relationship to the state plus noise of known covariance. Nothing requires a sensor to produce it.

    /// note | 📖 **Definition**
    <u>**Pseudo-measurement**</u>

    A measurement $\mathbf z_k$ used in a filter's update step whose value is not produced by a sensor reading of $h(\mathbf x_k)$ but is known from a constraint on the system, together with a measurement model $\mathbf z_k = h(\mathbf x_k) + \mathbf v_k$ whose noise $\mathbf v_k$ represents how well the constraint holds.
    ///

    During foot flat the true velocity is zero. So at every sample $k$ that the detector declares stationary we may "measure" $\mathbf z_k := \mathbf 0 \in \mathbb R^3$ with the model
    $$\mathbf z_k = \mathbf v_k + \mathbf n_{z,k}, \qquad \mathbf n_{z,k} \sim \mathcal N(\mathbf 0, \sigma_z^2\mathbf I), \qquad \sigma_z = 0.01\ \text{m/s}.$$
    The noise does not come from a sensor. It represents everything that makes the constraint imperfect: the sole compresses, the strap and skin move, and samples at the edges of a detected stance may belong to a foot that is just starting or finishing a motion.

    /// note | 📖 **Definition**
    <u>**Zero-velocity update**</u>

    The update step of a navigation filter that uses the pseudo-measurement $\mathbf z_k = \mathbf 0$ of the IMU's velocity, with model $\mathbf z_k = \mathbf v_k + \mathbf n_{z,k}$, at the samples $k$ that a zero-velocity detector declares stationary.
    ///

    This measurement model is linear in the state, but the process model is not: the attitude enters the velocity equation through $\mathbf R(q)\mathbf f$. So we use an extended Kalman filter ([Chapter 15](#ch15-sec-the-extended-kalman-filter)) in the error-state form of [Chapter 19](#ch19-sec-an-error-state-kalman-filter).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch21-sec-the-error-state-filter -->
    ## The Error-State Filter

    An {term}`error-state Kalman filter` keeps two things apart:

    - a **nominal state** $\hat{\mathbf x} = (\hat{\mathbf p}, \hat{\mathbf v}, \hat q, \hat{\mathbf b}_a, \hat{\mathbf b}_g)$, propagated by Chapter 20's mechanization with bias-corrected readings $\hat{\boldsymbol\omega} := \boldsymbol\omega_m - \hat{\mathbf b}_g$ and $\hat{\mathbf f} := \mathbf f_m - \hat{\mathbf b}_a$ (the bias estimates are held constant between updates);
    - an **error state** $\delta\mathbf x = [\delta\mathbf p^\top, \delta\mathbf v^\top, \delta\boldsymbol\theta^\top, \delta\mathbf b_a^\top, \delta\mathbf b_g^\top]^\top \in \mathbb R^{15}$, the small correction that turns the nominal state into the true one:
    $$\mathbf p = \hat{\mathbf p} + \delta\mathbf p,\quad \mathbf v = \hat{\mathbf v} + \delta\mathbf v,\quad q = \hat q\otimes\operatorname{Exp}_q(\delta\boldsymbol\theta)\ \ \big(\text{so } \mathbf R = \hat{\mathbf R}\operatorname{Exp}(\delta\boldsymbol\theta)\big),\quad \mathbf b_a = \hat{\mathbf b}_a + \delta\mathbf b_a,\quad \mathbf b_g = \hat{\mathbf b}_g + \delta\mathbf b_g.$$

    We write this as $\mathbf x = \hat{\mathbf x}\oplus\delta\mathbf x$. The filter estimates the mean and covariance $\mathbf P$ of $\delta\mathbf x$. The attitude error is a rotation vector, three numbers, even though the nominal attitude is a four-number quaternion, so the covariance is $15\times15$ and never singular for want of a unit-norm constraint.

    For the true state we need a model of how the biases evolve. We model each as a slow {term}`random walk`, $\dot{\mathbf b}_a = \mathbf w_a$ and $\dot{\mathbf b}_g = \mathbf w_g$, with white noise of intensities $\sigma_{ba}^2$ and $\sigma_{bg}^2$. The truth then obeys
    $$\dot{\mathbf p} = \mathbf v, \qquad \dot{\mathbf v} = \mathbf R(\mathbf f_m - \mathbf b_a - \mathbf n_a) + \mathbf g^n, \qquad \dot{\mathbf R} = \mathbf R[\boldsymbol\omega_m - \mathbf b_g - \mathbf n_g]_\times, \qquad \dot{\mathbf b}_a = \mathbf w_a, \qquad \dot{\mathbf b}_g = \mathbf w_g,$$
    obtained by solving the IMU model for the true $\mathbf f$ and $\boldsymbol\omega$, while the nominal state obeys the same equations with all noise set to zero and the biases replaced by their (constant) estimates.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch21-sec-the-linearized-error-model -->
    ### The Linearized Error Model

    One identity does most of the work: [Chapter 19](#ch19-lem-commutator-of-cross-product-matrices)'s commutator lemma, $[\mathbf a]_\times[\mathbf b]_\times - [\mathbf b]_\times[\mathbf a]_\times = [\mathbf a\times\mathbf b]_\times$ for all $\mathbf a, \mathbf b \in \mathbb R^3$. The attitude row below is Chapter 19's attitude-error theorem; we repeat its short proof so that the whole model is derived in one place.

    /// admonition | 📐 **Theorem (Linearized INS Error Model)**
        attrs: {class: theorem, id: ch21-thm-linearized-ins-error-model}
    Neglecting products of two or more of the small quantities $\delta\mathbf x$, $\mathbf n_a$, $\mathbf n_g$, the error state obeys
    $$\begin{aligned}
    \dot{\delta\mathbf p} &= \delta\mathbf v,\\
    \dot{\delta\mathbf v} &= -\hat{\mathbf R}[\hat{\mathbf f}]_\times\,\delta\boldsymbol\theta - \hat{\mathbf R}\,\delta\mathbf b_a - \hat{\mathbf R}\,\mathbf n_a,\\
    \dot{\delta\boldsymbol\theta} &= -[\hat{\boldsymbol\omega}]_\times\,\delta\boldsymbol\theta - \delta\mathbf b_g - \mathbf n_g,\\
    \dot{\delta\mathbf b}_a &= \mathbf w_a, \qquad \dot{\delta\mathbf b}_g = \mathbf w_g.
    \end{aligned}$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    *Position.* $\dot{\delta\mathbf p} = \dot{\mathbf p} - \dot{\hat{\mathbf p}} = \mathbf v - \hat{\mathbf v} = \delta\mathbf v$.

    *Velocity.* Write $\mathbf f_m - \mathbf b_a - \mathbf n_a = \hat{\mathbf f} - \delta\mathbf b_a - \mathbf n_a$ and $\mathbf R = \hat{\mathbf R}\operatorname{Exp}(\delta\boldsymbol\theta) = \hat{\mathbf R}(\mathbf I + [\delta\boldsymbol\theta]_\times) + O(\lVert\delta\boldsymbol\theta\rVert^2)$ ([Chapter 17](#ch17-thm-small-angle-approximation)). Then
    $$\dot{\mathbf v} - \dot{\hat{\mathbf v}} = \hat{\mathbf R}(\mathbf I + [\delta\boldsymbol\theta]_\times)(\hat{\mathbf f} - \delta\mathbf b_a - \mathbf n_a) - \hat{\mathbf R}\hat{\mathbf f} = \hat{\mathbf R}[\delta\boldsymbol\theta]_\times\hat{\mathbf f} - \hat{\mathbf R}\,\delta\mathbf b_a - \hat{\mathbf R}\,\mathbf n_a + (\text{second order}),$$
    and $[\delta\boldsymbol\theta]_\times\hat{\mathbf f} = \delta\boldsymbol\theta\times\hat{\mathbf f} = -\hat{\mathbf f}\times\delta\boldsymbol\theta = -[\hat{\mathbf f}]_\times\delta\boldsymbol\theta$.

    *Attitude.* Let $\mathbf E := \operatorname{Exp}(\delta\boldsymbol\theta) = \hat{\mathbf R}^\top\mathbf R$ and $\boldsymbol\omega := \boldsymbol\omega_m - \mathbf b_g - \mathbf n_g = \hat{\boldsymbol\omega} - \delta\mathbf b_g - \mathbf n_g$. Differentiating $\mathbf R = \hat{\mathbf R}\mathbf E$ and using $\dot{\mathbf R} = \mathbf R[\boldsymbol\omega]_\times$, $\dot{\hat{\mathbf R}} = \hat{\mathbf R}[\hat{\boldsymbol\omega}]_\times$:
    $$\hat{\mathbf R}\mathbf E[\boldsymbol\omega]_\times = \hat{\mathbf R}[\hat{\boldsymbol\omega}]_\times\mathbf E + \hat{\mathbf R}\dot{\mathbf E} \quad\Longrightarrow\quad \dot{\mathbf E} = \mathbf E[\boldsymbol\omega]_\times - [\hat{\boldsymbol\omega}]_\times\mathbf E.$$
    To first order $\mathbf E = \mathbf I + [\delta\boldsymbol\theta]_\times$ and $\dot{\mathbf E} = [\dot{\delta\boldsymbol\theta}]_\times$, so
    $$[\dot{\delta\boldsymbol\theta}]_\times = [\boldsymbol\omega - \hat{\boldsymbol\omega}]_\times + [\delta\boldsymbol\theta]_\times[\boldsymbol\omega]_\times - [\hat{\boldsymbol\omega}]_\times[\delta\boldsymbol\theta]_\times.$$
    Replacing $\boldsymbol\omega$ by $\hat{\boldsymbol\omega}$ in the middle term changes it only at second order, and then the commutator lemma gives $[\delta\boldsymbol\theta]_\times[\hat{\boldsymbol\omega}]_\times - [\hat{\boldsymbol\omega}]_\times[\delta\boldsymbol\theta]_\times = [\delta\boldsymbol\theta\times\hat{\boldsymbol\omega}]_\times = [-[\hat{\boldsymbol\omega}]_\times\delta\boldsymbol\theta]_\times$. Since $\mathbf a \mapsto [\mathbf a]_\times$ is linear and one-to-one, $\dot{\delta\boldsymbol\theta} = -\delta\mathbf b_g - \mathbf n_g - [\hat{\boldsymbol\omega}]_\times\delta\boldsymbol\theta$.

    *Biases.* $\dot{\delta\mathbf b}_a = \dot{\mathbf b}_a - \dot{\hat{\mathbf b}}_a = \mathbf w_a - \mathbf 0$, and likewise for $\mathbf b_g$. $\blacksquare$
    ///

    Each term has a physical reading. A tilt error rotates the sensed specific force, producing a false acceleration $-\hat{\mathbf R}[\hat{\mathbf f}]_\times\delta\boldsymbol\theta = \hat{\mathbf R}(\delta\boldsymbol\theta\times\hat{\mathbf f})$; at rest, $\hat{\mathbf f} = [0, 0, g]^\top$ and this is Chapter 20's $g\varepsilon$. An accelerometer bias error appears directly as an acceleration error. A gyroscope bias error makes the attitude error grow linearly, and the term $-[\hat{\boldsymbol\omega}]_\times\delta\boldsymbol\theta$ says that a body-frame error vector is carried along as the body rotates. These are exactly the three mechanisms of Chapter 20's drift laws.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In matrix form, with the noise vector $\mathbf w := [\mathbf n_a^\top, \mathbf n_g^\top, \mathbf w_a^\top, \mathbf w_g^\top]^\top$, the theorem reads $\dot{\delta\mathbf x} = \mathbf F\,\delta\mathbf x + \mathbf G\,\mathbf w$ with the block matrices
    $$\mathbf F = \begin{bmatrix}
    \mathbf 0 & \mathbf I & \mathbf 0 & \mathbf 0 & \mathbf 0\\
    \mathbf 0 & \mathbf 0 & -\hat{\mathbf R}[\hat{\mathbf f}]_\times & -\hat{\mathbf R} & \mathbf 0\\
    \mathbf 0 & \mathbf 0 & -[\hat{\boldsymbol\omega}]_\times & \mathbf 0 & -\mathbf I\\
    \mathbf 0 & \mathbf 0 & \mathbf 0 & \mathbf 0 & \mathbf 0\\
    \mathbf 0 & \mathbf 0 & \mathbf 0 & \mathbf 0 & \mathbf 0
    \end{bmatrix},\qquad
    \mathbf G = \begin{bmatrix}
    \mathbf 0 & \mathbf 0 & \mathbf 0 & \mathbf 0\\
    -\hat{\mathbf R} & \mathbf 0 & \mathbf 0 & \mathbf 0\\
    \mathbf 0 & -\mathbf I & \mathbf 0 & \mathbf 0\\
    \mathbf 0 & \mathbf 0 & \mathbf I & \mathbf 0\\
    \mathbf 0 & \mathbf 0 & \mathbf 0 & \mathbf I
    \end{bmatrix},$$
    where every block is $3\times3$. $\mathbf F$ changes at every sample because $\hat{\mathbf R}$, $\hat{\mathbf f}$, and $\hat{\boldsymbol\omega}$ do.

    Signs in this matrix are easy to get wrong, and a wrong sign produces a filter that runs without complaint and gives poor results. So before using it we check it numerically, in the spirit of [Chapter 15](#ch15-sec-checking-the-jacobians-numerically)'s Jacobian check: perturb a nominal state by $\pm\varepsilon$ along each error coordinate, propagate both the perturbed state (as "truth") and the nominal state through one step of the *nonlinear* mechanization, measure the resulting error state, and difference. For a step of $\Delta t = 10^{-6}$ s this gives $(\boldsymbol\Phi - \mathbf I)/\Delta t \approx \mathbf F$ column by column.
    """)
    return


@app.cell
def ekf_model(G_N, np, quat_conj, quat_exp, quat_log, quat_mult, quat_to_rotmat, skew):
    # jb: editor=true
    I3 = np.eye(3)

    def error_state_F(R_hat, f_hat, omega_hat):
        """Continuous-time matrix F of the error state [dp, dv, dtheta, db_a, db_g]."""
        F = np.zeros((15, 15))
        F[0:3, 3:6] = I3
        F[3:6, 6:9] = -R_hat @ skew(f_hat)
        F[3:6, 9:12] = -R_hat
        F[6:9, 6:9] = -skew(omega_hat)
        F[6:9, 12:15] = -I3
        return F

    def nominal_step(x, omega_prev, omega_k, f_prev, f_k, dt):
        """Chapter 20's mechanization for one sample, with bias-corrected readings. x = (p, v, q, b_a, b_g)."""
        p, v, q, b_a, b_g = x
        q_new = quat_mult(q, quat_exp(0.5 * (omega_prev + omega_k - 2 * b_g) * dt))
        q_new /= np.linalg.norm(q_new)
        a_prev = quat_to_rotmat(q) @ (f_prev - b_a) + G_N
        a_k = quat_to_rotmat(q_new) @ (f_k - b_a) + G_N
        v_new = v + 0.5 * (a_prev + a_k) * dt
        return (p + 0.5 * (v + v_new) * dt, v_new, q_new, b_a, b_g)

    def inject(x, dx):
        """Apply a 15-element error state dx to a nominal state x (x oplus dx)."""
        p, v, q, b_a, b_g = x
        q_new = quat_mult(q, quat_exp(dx[6:9]))
        return (p + dx[0:3], v + dx[3:6], q_new / np.linalg.norm(q_new), b_a + dx[9:12], b_g + dx[12:15])

    def error_between(x, x_hat):
        """The error state dx with x = x_hat oplus dx."""
        dtheta = quat_log(quat_mult(quat_conj(x_hat[2]), x[2]))
        return np.concatenate([x[0] - x_hat[0], x[1] - x_hat[1], dtheta, x[3] - x_hat[3], x[4] - x_hat[4]])

    return I3, error_between, error_state_F, inject, nominal_step


@app.cell
def _(error_between, error_state_F, inject, nominal_step, np, quat_to_rotmat):
    # jb: editor=true
    _rng = np.random.default_rng(3)
    _q = _rng.standard_normal(4)
    _x_hat = (_rng.standard_normal(3), _rng.standard_normal(3), _q / np.linalg.norm(_q),
              0.1 * _rng.standard_normal(3), 0.05 * _rng.standard_normal(3))
    _omega_m = 2.0 * _rng.standard_normal(3)                     # rad/s
    _f_m = 5.0 * _rng.standard_normal(3) + [0.0, 0.0, 9.81]      # m/s^2

    def numerical_Phi(x_hat, omega_m, f_m, dt, eps=1e-5):
        """Central-difference Jacobian of one nonlinear step with respect to the error state."""
        x_next = nominal_step(x_hat, omega_m, omega_m, f_m, f_m, dt)
        Phi = np.zeros((15, 15))
        for j in range(15):
            dx = np.zeros(15)
            dx[j] = eps
            plus = error_between(nominal_step(inject(x_hat, dx), omega_m, omega_m, f_m, f_m, dt), x_next)
            minus = error_between(nominal_step(inject(x_hat, -dx), omega_m, omega_m, f_m, f_m, dt), x_next)
            Phi[:, j] = (plus - minus) / (2 * eps)
        return Phi

    _F = error_state_F(quat_to_rotmat(_x_hat[2]), _f_m - _x_hat[3], _omega_m - _x_hat[4])
    F_check_error = np.abs((numerical_Phi(_x_hat, _omega_m, _f_m, 1e-6) - np.eye(15)) / 1e-6 - _F).max()
    Phi_check_error = np.abs(numerical_Phi(_x_hat, _omega_m, _f_m, 0.01) - (np.eye(15) + _F * 0.01)).max()
    F_check_scale = np.abs(_F).max()
    return F_check_error, F_check_scale, Phi_check_error


@app.cell(hide_code=True)
def _(F_check_error, F_check_scale, Phi_check_error, mo):
    mo.md(
        f"For a random nominal state and IMU reading, the largest entry of $\\mathbf F$ is "
        f"{F_check_scale:.1f}, and the largest difference between the numerical and analytic "
        f"matrices is {F_check_error:.1e}, which is the size of the finite-difference error. "
        f"Every sign is right. With the real step $\\Delta t = 0.01$ s, the one-step Jacobian of the "
        f"nonlinear mechanization differs from $\\mathbf I + \\mathbf F\\Delta t$ by at most "
        f"{Phi_check_error:.1e}, which motivates the discretization below."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch21-sec-discretization-and-process-noise -->
    ### Discretization and Process Noise

    Over one sample period we hold $\mathbf F$ constant at its value $\mathbf F_k$ at the start of the period. The exact transition matrix of $\dot{\delta\mathbf x} = \mathbf F_k\delta\mathbf x$ is then the matrix exponential $e^{\mathbf F_k\Delta t} = \mathbf I + \mathbf F_k\Delta t + \tfrac12\mathbf F_k^2\Delta t^2 + \cdots$ ([Chapter 10](#ch10-thm-exact-discretization), [Appendix D: The Matrix Exponential](#appd-sec-the-matrix-exponential)). We keep the first two terms,
    $$\boldsymbol\Phi_k = \mathbf I + \mathbf F_k\,\Delta t,$$
    which the check above showed to be accurate to about $10^{-3}$ per step at 100 Hz.

    For the process noise, recall that the IMU noise is a sequence of independent samples with per-axis standard deviations $\sigma_a$ and $\sigma_g$. Over one period the sample $\mathbf n_{a,k}$ changes the velocity error by $-\hat{\mathbf R}\mathbf n_{a,k}\Delta t$, whose covariance is $\hat{\mathbf R}(\sigma_a^2\mathbf I)\hat{\mathbf R}^\top\Delta t^2 = \sigma_a^2\Delta t^2\,\mathbf I$, because $\hat{\mathbf R}$ is orthogonal. Likewise the attitude error changes by $-\mathbf n_{g,k}\Delta t$ with covariance $\sigma_g^2\Delta t^2\,\mathbf I$, and a random walk of intensity $\sigma_{ba}^2$ grows by variance $\sigma_{ba}^2\Delta t$ per period ([Chapter 9](#ch9-lem-a-random-walk-spreads-out)). Position receives no noise directly. Hence
    $$\mathbf Q = \operatorname{diag}\big(\mathbf 0,\ \sigma_a^2\Delta t^2\,\mathbf I,\ \sigma_g^2\Delta t^2\,\mathbf I,\ \sigma_{ba}^2\Delta t\,\mathbf I,\ \sigma_{bg}^2\Delta t\,\mathbf I\big),$$
    and the predict step of [Chapter 13](#ch13-thm-predict) becomes $\mathbf P_k^- = \boldsymbol\Phi_k\mathbf P_{k-1}\boldsymbol\Phi_k^\top + \mathbf Q$. Only the covariance needs predicting: after every update the error estimate is reset to zero (below), and $\boldsymbol\Phi_k\mathbf 0 = \mathbf 0$. We use $\sigma_a = 0.05\ \text{m/s}^2$ and $\sigma_g = 0.01$ rad/s as in the IMU model. Our simulated biases are constant, so we choose small bias random walks, $\sigma_{ba} = 10^{-4}\ \text{m/s}^2/\sqrt{\text{s}}$ and $\sigma_{bg} = 10^{-5}\ \text{rad/s}/\sqrt{\text{s}}$, which still let the filter follow a slowly changing bias.

    /// caution | ⚠️ **Assumptions and Failure Modes**
    The error model and its discretization assume:

    1. **Small errors.** Every product of two error terms was dropped. Frequent updates and resets keep the attitude error at milliradians; after a long gap without updates, or a poor initial alignment, tilt errors of several degrees make the linearization, and with it the gain, wrong ([Chapter 15](#ch15-sec-large-initial-error)).
    2. **An IMU with only biases and white noise.** Real sensors also have scale-factor errors, misaligned axes, and temperature-dependent biases. Unmodeled, they act like extra process noise that $\mathbf Q$ does not contain, and the filter becomes overconfident; adding them as states, or inflating $\mathbf Q$ ([Chapter 14](#ch14-sec-an-unmodeled-bias)), are the remedies.
    3. **Noise that is white at the sample rate.** Many IMUs low-pass filter internally, which correlates consecutive noise samples and changes the effective $\mathbf Q$.
    4. **A short sample period.** $\boldsymbol\Phi_k = \mathbf I + \mathbf F_k\Delta t$ is accurate when the entries of $\mathbf F_k\Delta t$ are small. During a swing they reach about $0.2$ (specific forces of $2g$ times $\Delta t = 0.01$ s); faster motions or lower sample rates call for the next term of the series.
    5. **The navigation equations of Chapter 20,** including a non-rotating Earth.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch21-sec-update-injection-and-reset -->
    ### Update, Injection, and Reset

    **Update.** At a stationary sample, the innovation is $\tilde{\mathbf y}_k = \mathbf z_k - \hat{\mathbf v}_k = -\hat{\mathbf v}_k$. Since $\mathbf v_k = \hat{\mathbf v}_k + \delta\mathbf v_k$,
    $$\tilde{\mathbf y}_k = \delta\mathbf v_k + \mathbf n_{z,k} = \mathbf H\,\delta\mathbf x_k + \mathbf n_{z,k}, \qquad \mathbf H = \begin{bmatrix}\mathbf 0 & \mathbf I & \mathbf 0 & \mathbf 0 & \mathbf 0\end{bmatrix}.$$
    This is a linear measurement of the error state, so [Chapter 13](#ch13-sec-update)'s update applies as is. Its measurement noise covariance, called $\mathbf R$ in Chapter 13, we write $\mathbf R_{\text{meas}} := \sigma_z^2\mathbf I$, because here $\mathbf R$ is the attitude: $\ \mathbf S_k = \mathbf H\mathbf P_k^-\mathbf H^\top + \mathbf R_{\text{meas}}$, $\ \mathbf K_k = \mathbf P_k^-\mathbf H^\top\mathbf S_k^{-1}$, $\ \delta\hat{\mathbf x}_k = \mathbf K_k\tilde{\mathbf y}_k$, and the {term}`Joseph form` $\mathbf P_k = (\mathbf I - \mathbf K_k\mathbf H)\mathbf P_k^-(\mathbf I - \mathbf K_k\mathbf H)^\top + \mathbf K_k\mathbf R_{\text{meas}}\mathbf K_k^\top$.

    Why does a velocity measurement correct the attitude and the biases? Because $\mathbf H$ selects the velocity columns of $\mathbf P_k^-$, so $\mathbf K_k = \mathbf P_k^-\mathbf H^\top\mathbf S_k^{-1}$ has, in its attitude and bias rows, the cross-covariances $\operatorname{Cov}(\delta\boldsymbol\theta, \delta\mathbf v)$, $\operatorname{Cov}(\delta\mathbf b_a, \delta\mathbf v)$, and $\operatorname{Cov}(\delta\mathbf b_g, \delta\mathbf v)$, times $\mathbf S_k^{-1}$. During the swing, $\mathbf F$ built exactly these cross-covariances, because the velocity error was driven by $-\hat{\mathbf R}[\hat{\mathbf f}]_\times\delta\boldsymbol\theta - \hat{\mathbf R}\delta\mathbf b_a$. The filter knows which tilt and bias errors would explain the velocity error it now sees, and in what proportion. Chapter 20's naive velocity reset threw this information away. During the stance itself the same mechanism plays the role of [Chapter 19](#ch19-sec-measurement-updates)'s gravity update: a tilt error $\delta\theta$ makes the computed velocity of the resting foot grow at about $g\,\delta\theta$, and the zero-velocity updates see that growth. This is the foot-mounted form of using gravity only while the foot is known to be still.

    **Injection.** The estimated error is moved into the nominal state, $\hat{\mathbf x} \leftarrow \hat{\mathbf x}\oplus\delta\hat{\mathbf x}$: $\hat{\mathbf p} \leftarrow \hat{\mathbf p} + \delta\hat{\mathbf p}$, $\hat{\mathbf v} \leftarrow \hat{\mathbf v} + \delta\hat{\mathbf v}$, $\hat q \leftarrow \hat q\otimes\operatorname{Exp}_q(\delta\hat{\boldsymbol\theta})$, $\hat{\mathbf b}_a \leftarrow \hat{\mathbf b}_a + \delta\hat{\mathbf b}_a$, $\hat{\mathbf b}_g \leftarrow \hat{\mathbf b}_g + \delta\hat{\mathbf b}_g$.

    **Reset.** The error is now measured from the new nominal state, so its estimate returns to zero and its covariance must be re-expressed. For the vector parts the new error is $\delta\mathbf p - \delta\hat{\mathbf p}$ and so on, with Jacobian $\mathbf I$. For the attitude, the new error $\delta\boldsymbol\theta^+$ satisfies $\operatorname{Exp}(\delta\boldsymbol\theta^+) = \operatorname{Exp}(-\delta\hat{\boldsymbol\theta})\operatorname{Exp}(\delta\boldsymbol\theta)$. The [Baker–Campbell–Hausdorff formula](https://en.wikipedia.org/wiki/Baker%E2%80%93Campbell%E2%80%93Hausdorff_formula) gives $\log(e^{\mathbf A}e^{\mathbf B}) = \mathbf A + \mathbf B + \tfrac12(\mathbf A\mathbf B - \mathbf B\mathbf A) + \cdots$, and with the commutator lemma ($\mathbf A = -[\delta\hat{\boldsymbol\theta}]_\times$, $\mathbf B = [\delta\boldsymbol\theta]_\times$) this yields $\delta\boldsymbol\theta^+ \approx \delta\boldsymbol\theta - \delta\hat{\boldsymbol\theta} - \tfrac12\,\delta\hat{\boldsymbol\theta}\times\delta\boldsymbol\theta$. Its Jacobian with respect to $\delta\boldsymbol\theta$ is $\mathbf I - \tfrac12[\delta\hat{\boldsymbol\theta}]_\times$, so
    $$\mathbf P \leftarrow \mathbf G_r\mathbf P\mathbf G_r^\top, \qquad \mathbf G_r = \operatorname{blockdiag}\big(\mathbf I,\ \mathbf I,\ \mathbf I - \tfrac12[\delta\hat{\boldsymbol\theta}]_\times,\ \mathbf I,\ \mathbf I\big).$$
    The corrections $\delta\hat{\boldsymbol\theta}$ are milliradians, so $\mathbf G_r \approx \mathbf I$ and many implementations skip this step; it costs nothing, so we keep it. (We also checked $\mathbf G_r$ numerically. For the derivation in full, see @sola2017 [Section 7].)

    /// tip | **The filter, one sample at a time**
    1. Build $\boldsymbol\Phi_k = \mathbf I + \mathbf F_k\Delta t$ from the nominal state and the bias-corrected readings at the start of the period.
    2. Propagate the nominal state with Chapter 20's mechanization.
    3. Predict the covariance: $\mathbf P \leftarrow \boldsymbol\Phi_k\mathbf P\boldsymbol\Phi_k^\top + \mathbf Q$.
    4. If the detector declares sample $k$ stationary: update, inject, and reset.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The implementation follows the box line by line. It has one option we have not met yet, `zaru`, which adds a second pseudo-measurement and is explained in the section on observability; until then it stays off.

    **Initialization.** The first second of standing levels the attitude as in [Chapter 20](#ch20-sec-noise-and-leveling). Without a heading reference the filter cannot know which way it faces, so we *define* the navigation frame's $x$ axis by the initial heading, $\hat\psi_0 := 0$; in the simulator this is East, so estimates and truth are directly comparable. Position starts at the origin by the same kind of definition. The initial standard deviations are therefore essentially zero for position and yaw, $0.01$ m/s for velocity, $0.01$ rad for roll and pitch, and the bias magnitudes (doubled for the gyroscope) for the biases.
    """)
    return


@app.cell
def ekf_cell(I3, error_state_F, inject, nominal_step, np, quat_to_rotmat, skew):
    # jb: editor=true
    def zupt_ekf(omega_m, f_m, dt, stationary, q0, zaru=False, sigma_a=0.05, sigma_g=0.01,
                 sigma_ba=1e-4, sigma_bg=1e-5, sigma_z=0.01):
        """15-state error-state EKF with zero-velocity updates (and optional ZARU)."""
        N = len(omega_m)
        x = (np.zeros(3), np.zeros(3), q0.copy(), np.zeros(3), np.zeros(3))  # p, v, q, b_a, b_g
        P = np.diag(np.r_[np.full(3, 1e-8), np.full(3, 0.01**2), [0.01**2, 0.01**2, 1e-8],
                          np.full(3, 0.05**2), np.full(3, 0.02**2)])
        Q = np.diag(np.r_[np.zeros(3), np.full(3, (sigma_a * dt) ** 2), np.full(3, (sigma_g * dt) ** 2),
                          np.full(3, sigma_ba**2 * dt), np.full(3, sigma_bg**2 * dt)])
        H_v = np.hstack([np.zeros((3, 3)), I3, np.zeros((3, 9))])      # ZUPT: measures dv
        H_w = np.hstack([np.zeros((3, 12)), I3])                       # ZARU: measures db_g
        out = dict(p=np.zeros((N, 3)), v=np.zeros((N, 3)), q=np.zeros((N, 4)),
                   b_a=np.zeros((N, 3)), b_g=np.zeros((N, 3)), P_diag=np.zeros((N, 15)),
                   P_theta=np.zeros((N, 3, 3)))

        def record(k):
            for key, value in zip(["p", "v", "q", "b_a", "b_g"], x):
                out[key][k] = value
            out["P_diag"][k] = np.diag(P)
            out["P_theta"][k] = P[6:9, 6:9]      # attitude-error covariance (body frame)

        record(0)
        for k in range(1, N):
            # 1-3: linearize at the start of the period, propagate nominal state and covariance
            Phi = np.eye(15) + error_state_F(quat_to_rotmat(x[2]), f_m[k - 1] - x[3], omega_m[k - 1] - x[4]) * dt
            x = nominal_step(x, omega_m[k - 1], omega_m[k], f_m[k - 1], f_m[k], dt)
            P = Phi @ P @ Phi.T + Q
            # 4: pseudo-measurement update at stationary samples
            if stationary[k]:
                H, y, R_meas = H_v, -x[1], sigma_z**2 * I3              # innovation 0 - v_hat
                if zaru:
                    H = np.vstack([H_v, H_w])
                    y = np.r_[-x[1], omega_m[k] - x[4]]                 # innovation omega_m - b_g_hat
                    R_meas = np.diag(np.r_[np.full(3, sigma_z**2), np.full(3, sigma_g**2)])
                S = H @ P @ H.T + R_meas
                K = np.linalg.solve(S, H @ P).T                         # K = P H^T S^-1
                dx = K @ y
                A = np.eye(15) - K @ H
                P = A @ P @ A.T + K @ R_meas @ K.T                      # Joseph form
                x = inject(x, dx)                                       # x_hat <- x_hat oplus dx_hat
                G_r = np.eye(15)
                G_r[6:9, 6:9] = I3 - 0.5 * skew(dx[6:9])
                P = G_r @ P @ G_r.T                                     # reset
            record(k)
        return out

    return (zupt_ekf,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch21-sec-results-with-and-without-zero-velocity-updates -->
    ## Results: With and Without Zero-Velocity Updates

    We run the filter twice on the same U-turn walk, once with no updates at all (the nominal state is then exactly Chapter 20's free strapdown solution) and once with zero-velocity updates at every sample that SHOE declares stationary.
    """)
    return


@app.cell
def _(align_level, np, quat_to_rotmat, rotmat_to_euler, sim, stationary, zupt_ekf):
    # jb: editor=true
    q0 = align_level(sim["f_m"][:100])
    run_free = zupt_ekf(sim["omega_m"], sim["f_m"], sim["dt"], np.zeros(len(sim["t"]), bool), q0)
    run_zupt = zupt_ekf(sim["omega_m"], sim["f_m"], sim["dt"], stationary, q0)

    def estimated_yaw(run):
        return rotmat_to_euler(np.array([quat_to_rotmat(q) for q in run["q"]]))[2]

    def nav_attitude_std(run):
        """Std. dev. of the attitude error about East, North, Up: covariance of R_hat dtheta."""
        R_hat = np.array([quat_to_rotmat(q) for q in run["q"]])
        cov = R_hat @ run["P_theta"] @ np.transpose(R_hat, (0, 2, 1))
        return np.sqrt(np.diagonal(cov, axis1=1, axis2=2))

    return estimated_yaw, nav_attitude_std, q0, run_free, run_zupt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch21_zupt_results.svg" class="graphic" alt="Three panels. Left: top view of the U-turn walk; the zero-velocity-update estimate (orange) follows the true path (black) closely, with a small sideways offset on the return leg. Middle: position error on a logarithmic scale; without updates it grows to hundreds of meters, with updates it stays below about half a meter, inside the filter's two-sigma bound. Right: forward velocity over three strides; the estimate tracks the true bell-shaped velocity and is held at zero during each stance." />
    """)
    return


@app.cell(hide_code=True)
def _(IMAGES_DIR, np, plt, run_free, run_zupt, sim, stationary):
    # jb: include=false
    _t = sim["t"]
    _fig, _axs = plt.subplots(1, 3, figsize=(13, 3.9), width_ratios=[1.3, 1, 1])
    _a = _axs[0]
    _a.plot(sim["p"][:, 0], sim["p"][:, 1], color="black", lw=2, label="true path")
    _a.plot(run_zupt["p"][:, 0], run_zupt["p"][:, 1], color="C1", lw=1.3, label="ZUPT estimate")
    _a.plot(run_free["p"][:, 0], run_free["p"][:, 1], color="C3", lw=1, label="no updates (leaves the plot)")
    _a.set_xlim(-2, 18)
    _a.set_ylim(-3, 6.5)
    _a.set_aspect("equal")
    _a.set_xlabel("East (m)")
    _a.set_ylabel("North (m)")
    _a.legend(fontsize=7.5, loc="upper left")
    _a.set_title("Top view", style="italic")
    _a = _axs[1]
    _m = _t > 0.05
    _a.semilogy(_t[_m], np.linalg.norm(run_free["p"] - sim["p"], axis=1)[_m], color="C3", label="no updates")
    _a.semilogy(_t[_m], np.linalg.norm(run_zupt["p"] - sim["p"], axis=1)[_m], color="C1", label="ZUPT")
    _sig = np.sqrt(run_zupt["P_diag"][:, 0] + run_zupt["P_diag"][:, 1] + run_zupt["P_diag"][:, 2])
    _a.semilogy(_t[_m], 2 * _sig[_m], color="C1", ls=":", label=r"ZUPT $2\sigma$ (filter)")
    _a.set_ylim(1e-3, 1e3)
    _a.set_xlabel("time (s)")
    _a.set_ylabel("position error (m)")
    _a.legend(fontsize=7.5, loc="upper left")
    _a.set_title("Position error", style="italic")
    _a = _axs[2]
    _k = (_t >= 5.0) & (_t <= 8.6)
    _a.fill_between(_t[_k], 0, 1, where=stationary[_k], color="0.85", lw=0,
                    transform=_a.get_xaxis_transform(), label="detected stance")
    _a.plot(_t[_k], sim["v"][_k, 0], color="black", lw=2, label="true $v_x$")
    _a.plot(_t[_k], run_zupt["v"][_k, 0], color="C1", lw=1.2, label=r"ZUPT $\hat v_x$")
    _a.set_xlabel("time (s)")
    _a.set_ylabel("East velocity (m/s)")
    _a.legend(fontsize=7.5, loc="upper right")
    _a.set_title("Velocity over three strides", style="italic")
    for _a in _axs:
        _a.grid(visible=True, alpha=0.9, linewidth=0.4)
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch21_zupt_results.svg")
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo, np, run_free, run_zupt, sim):
    _e_free = np.linalg.norm(run_free["p"][-1] - sim["p"][-1])
    _err = np.linalg.norm(run_zupt["p"] - sim["p"], axis=1)
    _sig = np.sqrt(run_zupt["P_diag"][:, 0:3].sum(axis=1))
    _inside = 100 * np.mean(_err <= 2 * _sig)
    _walked = sim["stride_length"].sum()
    mo.md(
        f"Without updates the final position is {_e_free:.0f} m from the truth. With zero-velocity "
        f"updates it is {_err[-1]:.2f} m off after {_walked:.1f} m of walking, "
        f"{100 * _err[-1] / _walked:.1f}% of the distance traveled, and the error is within the "
        f"filter's own $2\\sigma$ bound {_inside:.0f}% of the time, so the filter's confidence is "
        f"about right. The velocity panel shows the mechanism: during each swing the velocity is "
        f"integrated freely, and at each stance the updates pull it, and everything correlated with "
        f"it, back into line."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch21-sec-observability-what-zero-velocity-cannot-see -->
    ## Observability: What Zero Velocity Cannot See

    The top view shows a pattern that tuning cannot remove: the return leg is displaced sideways, as if the whole path had been rotated slightly. That is a heading error, and it is not the filter's fault.

    /// admonition | 📐 **Theorem (Heading and Position Are Unobservable)**
        attrs: {class: theorem, id: ch21-thm-heading-and-position-are-unobservable}
    Let $(\mathbf p(t), \mathbf v(t), \mathbf R(t), \mathbf b_a, \mathbf b_g)$ be a trajectory of the true-state model, let $\varepsilon \in \mathbb R$, $\mathbf c \in \mathbb R^3$, and let $\mathbf R_\varepsilon := \mathbf R_z(\varepsilon)$. Then the rotated and translated trajectory
    $$\big(\mathbf R_\varepsilon\mathbf p(t) + \mathbf c,\ \ \mathbf R_\varepsilon\mathbf v(t),\ \ \mathbf R_\varepsilon\mathbf R(t),\ \ \mathbf b_a,\ \ \mathbf b_g\big)$$
    produces exactly the same IMU measurements and the same zero-velocity pseudo-measurements, for the same noise. Consequently these data cannot distinguish a trajectory from its copies rotated about the vertical or translated: heading and horizontal position are known only through the initial condition and the integrated gyroscope readings, and the uncertainty that gyroscope noise adds to the heading is never removed by later measurements.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Write $\mathbf R' := \mathbf R_\varepsilon\mathbf R$ and $\mathbf a' := \mathbf R_\varepsilon\mathbf a^n$ (the second derivative of the new position, since $\mathbf R_\varepsilon$ and $\mathbf c$ are constant). *Angular rate:* $\mathbf R'^\top\dot{\mathbf R}' = \mathbf R^\top\mathbf R_\varepsilon^\top\mathbf R_\varepsilon\dot{\mathbf R} = \mathbf R^\top\dot{\mathbf R} = [\boldsymbol\omega]_\times$, so the true body rate, and hence $\boldsymbol\omega_m$, is unchanged. *Specific force:* $\mathbf R'^\top(\mathbf a' - \mathbf g^n) = \mathbf R^\top(\mathbf a^n - \mathbf R_\varepsilon^\top\mathbf g^n) = \mathbf R^\top(\mathbf a^n - \mathbf g^n) = \mathbf f$, because a rotation about the vertical leaves $\mathbf g^n = [0, 0, -g]^\top$ fixed. So $\mathbf f_m$ is unchanged. *Zero velocity:* $\mathbf R_\varepsilon\mathbf v = \mathbf 0$ exactly when $\mathbf v = \mathbf 0$, so the stationary samples and the pseudo-measurements $\mathbf z_k = \mathbf 0$ are the same. Two different states thus produce identical measurements, which is exactly what [Chapter 13](#ch13-sec-observability)'s definition of {term}`observability` rules out. $\blacksquare$
    ///

    The proof uses only that gravity is vertical and that "zero" looks the same in every direction. Gravity defines *down*, so tilt can be observed; nothing in the data defines *North*.

    <!-- label: ch21-sec-which-other-errors-are-hidden -->
    ### Which Other Errors Are Hidden?

    The theorem finds two symmetries of the nonlinear problem. The linearized model may hide more. Take the simplest case, a foot resting level with heading zero: $\hat{\mathbf R} = \mathbf I$, $\hat{\mathbf f} = [0, 0, g]^\top$, $\hat{\boldsymbol\omega} = \mathbf 0$. Then $\mathbf F$ is constant, and we can see what the measured $\delta\mathbf v$ reveals by differentiating it with the error model (without noise):
    $$\dot{\delta\mathbf v} = \begin{bmatrix} g\,\delta\theta_y - \delta b_{a,x}\\ -g\,\delta\theta_x - \delta b_{a,y}\\ -\delta b_{a,z}\end{bmatrix}, \qquad \ddot{\delta\mathbf v} = -[\hat{\mathbf f}]_\times\dot{\delta\boldsymbol\theta} = [\hat{\mathbf f}]_\times\delta\mathbf b_g = \begin{bmatrix} -g\,\delta b_{g,y}\\ g\,\delta b_{g,x}\\ 0\end{bmatrix},$$
    and every higher derivative is zero. A stationary foot therefore reveals eight numbers: the three components of $\delta\mathbf v$, the combinations $g\,\delta\theta_y - \delta b_{a,x}$ and $g\,\delta\theta_x + \delta b_{a,y}$, $\delta b_{a,z}$, and $\delta b_{g,x}$, $\delta b_{g,y}$. Seven directions of the 15-dimensional error state stay hidden:

    - $\delta\mathbf p$ (three): position never enters the velocity equations.
    - $\delta\theta_z$: yaw, as the theorem says.
    - $\delta b_{g,z}$: the vertical gyroscope bias, which drives only $\delta\theta_z$.
    - $(\delta\theta_y, \delta b_{a,x}) = (1, g)$ and $(\delta\theta_x, \delta b_{a,y}) = (1, -g)$: a tilt error and a horizontal accelerometer bias that cancel exactly. This is Chapter 20's leveling observation, now as an observability statement.

    The code confirms this with [Chapter 13](#ch13-thm-rank-test-for-observability)'s rank test on $\boldsymbol\Phi = \mathbf I + \mathbf F\Delta t$ (whose powers span the same rows as those of $\mathbf F$, so the null space is the same).
    """)
    return


@app.cell
def _(G, I3, error_state_F, np):
    # jb: editor=true
    _Phi = np.eye(15) + error_state_F(np.eye(3), np.array([0.0, 0.0, G]), np.zeros(3)) * 0.01
    _H_zupt = np.hstack([np.zeros((3, 3)), I3, np.zeros((3, 9))])
    _H_zaru = np.hstack([np.zeros((3, 12)), I3])

    def observability_matrix(H, Phi):
        return np.vstack([H @ np.linalg.matrix_power(Phi, i) for i in range(15)])

    _O = observability_matrix(_H_zupt, _Phi)
    rank_zupt = np.linalg.matrix_rank(_O)
    rank_zupt_zaru = np.linalg.matrix_rank(observability_matrix(np.vstack([_H_zupt, _H_zaru]), _Phi))
    # The seven hidden directions derived above, as columns (order: p, v, theta, b_a, b_g)
    _hidden = np.zeros((15, 7))
    _hidden[0, 0] = _hidden[1, 1] = _hidden[2, 2] = 1.0       # position
    _hidden[8, 3] = 1.0                                       # yaw
    _hidden[14, 4] = 1.0                                      # vertical gyroscope bias
    _hidden[7, 5], _hidden[9, 5] = 1.0, G                     # tilt about y with x accel bias
    _hidden[6, 6], _hidden[10, 6] = 1.0, -G                   # tilt about x with y accel bias
    hidden_residual = np.abs(_O @ _hidden).max()
    return hidden_residual, rank_zupt, rank_zupt_zaru


@app.cell(hide_code=True)
def _(hidden_residual, mo, rank_zupt, rank_zupt_zaru):
    mo.md(
        f"The observability matrix has rank {rank_zupt} out of 15, and it maps the seven hidden "
        f"directions to vectors no larger than {hidden_residual:.0e} (round-off), so they span its "
        f"null space. With the zero angular rate update introduced below, the rank becomes "
        f"{rank_zupt_zaru}."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The resting foot is the worst case. During the swing the foot pitches and accelerates, $\hat{\mathbf f}$ and $\hat{\mathbf R}$ change, and over a whole stride more combinations become visible. The tilt and accelerometer-bias pairs separate, and the gyroscope's body $z$ axis tilts away from vertical during the swing, so $\delta b_{g,z}$ becomes **weakly** observable: it leaves a small tilt signature that the next stance detects. Yaw and position stay hidden, because the theorem holds for every motion. In practice the vertical gyroscope bias is learned slowly and imperfectly, and the heading error keeps growing in the meantime.

    <!-- label: ch21-sec-zero-angular-rate-updates -->
    ### Zero Angular Rate Updates

    Zero velocity is not the only thing we know at rest: the foot is not rotating either.

    /// note | 📖 **Definition**
    <u>**Zero angular rate update**</u>

    The update step of a navigation filter that, at the samples a zero-velocity detector declares stationary, uses the gyroscope reading $\mathbf z_k := \boldsymbol\omega_{m,k}$ as a pseudo-measurement of the gyroscope bias, with model $\mathbf z_k = \mathbf b_g + \mathbf n_{g,k}$, which follows from the IMU model with the true angular rate $\boldsymbol\omega_k = \mathbf 0$.
    ///

    With $\mathbf b_g = \hat{\mathbf b}_g + \delta\mathbf b_g$, the innovation is $\tilde{\mathbf y}_k = \boldsymbol\omega_{m,k} - \hat{\mathbf b}_g = \delta\mathbf b_g + \mathbf n_{g,k}$, so $\mathbf H = [\mathbf 0\ \mathbf 0\ \mathbf 0\ \mathbf 0\ \mathbf I]$ with noise covariance $\sigma_g^2\mathbf I$. Stacked under the zero-velocity rows, it makes all three gyroscope biases directly observable at rest; the rank rises from 8 to 9 because $\delta b_{g,z}$ leaves the null space. The ZARU limits the *rate* at which the heading drifts, not the heading itself. Averaging $N$ stationary gyroscope samples determines each bias component to a standard deviation of about $\sigma_g/\sqrt N$ ([Chapter 6](#ch6-thm-mean-and-variance-of-the-sample-mean)), so after it the heading uncertainty grows only through that small residual bias uncertainty and the random walk of gyroscope noise, with standard deviation $\sigma_g\sqrt{\Delta t\,t}$.[^zaru-noise]

    [^zaru-noise]: Strictly, the same gyroscope sample is used both to propagate the attitude and to update the bias, which correlates process and measurement noise. With dozens of stationary samples per stance, ignoring this correlation is a standard and harmless simplification.
    """)
    return


@app.cell
def _(q0, sim, stationary, zupt_ekf):
    # jb: editor=true
    run_zaru = zupt_ekf(sim["omega_m"], sim["f_m"], sim["dt"], stationary, q0, zaru=True)
    return (run_zaru,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch21_observability.svg" class="graphic" alt="Three panels over the 29-second walk. Left: heading error with two-sigma bands; with zero-velocity updates only it grows to several degrees, with zero angular rate updates added it stays below one degree. Middle: the estimated vertical gyroscope bias; with zero-velocity updates only it creeps slowly toward the true value, with zero angular rate updates it reaches the true value during the first second. Right: filter standard deviations of the three attitude errors with zero-velocity updates only; roll and pitch stay near one milliradian while yaw grows steadily." />
    """)
    return


@app.cell(hide_code=True)
def _(IMAGES_DIR, estimated_yaw, nav_attitude_std, np, plt, run_zaru, run_zupt, sim):
    # jb: include=false
    _t = sim["t"]
    _fig, _axs = plt.subplots(1, 3, figsize=(13, 3.8))
    for _run, _c, _name in [(run_zupt, "C0", "ZUPT"), (run_zaru, "C1", "ZUPT + ZARU")]:
        _yerr = np.degrees(np.angle(np.exp(1j * (estimated_yaw(_run) - sim["yaw"]))))
        _s2 = 2 * np.degrees(nav_attitude_std(_run)[:, 2])
        _axs[0].plot(_t, _yerr, color=_c, lw=1.3, label=f"{_name}: error")
        _axs[0].fill_between(_t, -_s2, _s2, color=_c, alpha=0.2, lw=0, label=rf"{_name}: $\pm2\sigma$")
        _axs[1].plot(_t, _run["b_g"][:, 2], color=_c, lw=1.3, label=_name)
    _axs[1].axhline(sim["b_g"][2], color="black", lw=1.5, label="true $b_{g,z}$")
    _std = np.degrees(nav_attitude_std(run_zupt))
    for _j, _ls, _c, _name in [(0, "-", "gray", "about East (tilt)"), (1, "--", "gray", "about North (tilt)"),
                               (2, "-", "C0", "about Up (heading)")]:
        _axs[2].plot(_t, _std[:, _j], ls=_ls, lw=1.5, color=_c, label=_name)
    _axs[0].set_ylabel("heading error (deg)")
    _axs[0].set_title("Heading error", style="italic")
    _axs[1].set_ylabel("estimated $b_{g,z}$ (rad/s)")
    _axs[1].set_title("Vertical gyroscope bias", style="italic")
    _axs[2].set_ylabel("standard deviation (deg)")
    _axs[2].set_title("Attitude uncertainty, ZUPT only", style="italic")
    for _a in _axs:
        _a.set_xlabel("time (s)")
        _a.grid(visible=True, alpha=0.9, linewidth=0.4)
        _a.legend(fontsize=7.5, loc="best")
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch21_observability.svg")
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(estimated_yaw, mo, np, run_zaru, run_zupt, sim):
    def _final_heading_error(run):
        return np.degrees(np.angle(np.exp(1j * (estimated_yaw(run)[-1] - sim["yaw"][-1]))))

    mo.md(
        f"With zero-velocity updates alone, the estimated vertical gyroscope bias creeps toward its "
        f"true value of {sim['b_g'][2]:.3f} rad/s and ends at {run_zupt['b_g'][-1, 2]:.4f} rad/s, and "
        f"the heading error reaches {_final_heading_error(run_zupt):.1f} degrees. Its "
        f"$2\\sigma$ band stays wide and keeps growing, while the tilt uncertainties stay small and "
        f"bounded (right). Adding "
        f"zero angular rate updates pins the bias down during the first second of standing "
        f"(final estimate {run_zaru['b_g'][-1, 2]:.4f} rad/s) and keeps the final heading error to "
        f"{_final_heading_error(run_zaru):.2f} degrees; the final position error drops from "
        f"{np.linalg.norm(run_zupt['p'][-1] - sim['p'][-1]):.2f} m to "
        f"{np.linalg.norm(run_zaru['p'][-1] - sim['p'][-1]):.2f} m. Over a long walk, though, both "
        f"bands keep growing: no stationary measurement can stop it."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    One detail in the right panel deserves a comment. With zero-velocity updates only, the heading uncertainty grows during the initial standing period and then *drops* after the first stride. While the foot stood still, the vertical gyroscope bias turned the computed heading, so the heading error and the bias error became strongly correlated. When the first swing makes the bias weakly observable, the update learns part of the bias error and, through that correlation, part of the heading error it caused. This is the same cross-covariance mechanism by which a velocity measurement corrects tilt. It does not contradict the theorem: what is recovered is drift whose cause became visible, not the heading itself.

    <!-- label: ch21-sec-heading-aids -->
    ### Heading Aids

    Bounding the heading error requires a measurement that depends on heading. The common options:

    - **Magnetometer.** [Chapter 19](#ch19-thm-tilt-compensated-heading)'s tilt-compensated heading is a measurement of yaw. Since $\mathbf R = \hat{\mathbf R}\operatorname{Exp}(\delta\boldsymbol\theta) = \operatorname{Exp}(\hat{\mathbf R}\,\delta\boldsymbol\theta)\hat{\mathbf R}$, the navigation-frame attitude error is $\hat{\mathbf R}\,\delta\boldsymbol\theta$, and to first order the heading error is its vertical component, $\mathbf e_z^\top\hat{\mathbf R}\,\delta\boldsymbol\theta$. A heading measurement therefore has $\mathbf H = [\mathbf 0\ \ \mathbf 0\ \ \mathbf e_z^\top\hat{\mathbf R}\ \ \mathbf 0\ \ \mathbf 0]$. The difficulty is physical: indoors, and especially near the floor, steel and electronics distort the Earth's field by tens of degrees, so magnetic updates need gating ([Chapter 14](#ch14-sec-outlier-gating)) or must be accepted only when the measured field has the expected magnitude and dip.
    - **Heuristic drift elimination.** Most buildings have corridors along a few dominant directions. When the walker has gone straight for several strides in a direction close to a dominant one, the filter applies a pseudo-measurement that the heading *equals* that direction; see @borenstein2009. It works where its assumption holds and corrupts the heading where it does not.
    - **Other sources:** satellite positioning outdoors, maps, or a second foot-mounted IMU combined with the constraint that the two feet are never more than a leg length apart [@skog2012].

    For gait analysis, heading drift matters less than it does for navigation: stride length, stride time, and clearance are computed within a stride, and a slowly rotating heading affects only the turning angle, by the drift accumulated during one stride.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch21-sec-gait-parameters -->
    ## Gait Parameters

    The corrected trajectory turns into clinical numbers stride by stride. First we segment it: a **detected stance** is a run of at least five consecutive stationary samples (50 ms). For detected stance $j$, let $\hat{\mathbf P}_j$ be the mean estimated position over the stance and $\hat\psi_j$ the mean estimated heading (a circular mean, so that headings near $\pm180^\circ$ average correctly). Stride $i$ is the motion between detected stances $i-1$ and $i$.

    /// note | 📖 **Definition**
    <u>**Stride length**</u>

    The horizontal distance between the positions of a specified point on a foot during the foot-flat periods of two consecutive stance phases of that foot.
    ///

    We estimate it as $\lVert(\hat{\mathbf P}_i - \hat{\mathbf P}_{i-1})_{xy}\rVert$, the horizontal part of the displacement between stance positions. The **stride time** is the duration of the stride. A foot-mounted IMU cannot see heel strike precisely, but it sees the start of each detected stance (foot flat) with a nearly constant delay, so we measure stride time between consecutive stance onsets. The first stride starts from standing and has no previous onset, so time-based parameters start with the second stride; clinical protocols usually discard the first strides of a walk anyway, as the walker is still accelerating.

    /// note | 📖 **Definition**
    <u>**Cadence**</u>

    The number of steps (heel strikes of either foot) per unit time, usually expressed in steps per minute.
    ///

    One instrumented foot sees one heel strike per stride. Assuming the two legs take steps of equal duration, each stride contains two steps, so we estimate cadence as $2\cdot 60/T_{\text{stride}}$ steps per minute, with $T_{\text{stride}}$ in seconds.

    /// note | 📖 **Definition**
    <u>**Gait speed**</u>

    The horizontal distance a walker travels per unit time.
    ///

    Per stride, it is the stride length divided by the stride time.

    /// note | 📖 **Definition**
    <u>**Foot clearance**</u>

    For a stride and a specified point on the foot, the maximum height of that point during the swing phase above its height during the foot-flat period of the preceding stance phase.
    ///

    Our specified point is the IMU on the top of the foot. Clinicians are often interested in a different quantity, the *minimum toe clearance* in mid-swing, which needs the position of the toe and therefore a model of the foot's geometry relative to the sensor. Finally, the **turning angle** of stride $i$ is the change of heading between its two stances, $\hat\psi_i - \hat\psi_{i-1}$.
    """)
    return


@app.cell
def _(np):
    # jb: editor=true
    def stance_segments(stationary, min_len=5):
        """Start and end (exclusive) indices of runs of at least min_len stationary samples."""
        edges = np.diff(np.r_[False, stationary, False].astype(int))
        starts, ends = np.flatnonzero(edges == 1), np.flatnonzero(edges == -1)
        keep = ends - starts >= min_len
        return starts[keep], ends[keep]

    def gait_parameters(t, p, yaw, stationary, min_len=5):
        """Per-stride gait parameters from an estimated trajectory and the stationary decisions."""
        s, e = stance_segments(stationary, min_len)
        P = np.array([p[a:b].mean(axis=0) for a, b in zip(s, e)]).reshape(-1, 3)
        psi = np.unwrap([np.angle(np.mean(np.exp(1j * yaw[a:b]))) for a, b in zip(s, e)])
        stride_length = np.linalg.norm(np.diff(P[:, :2], axis=0), axis=1)
        stride_time = np.diff(t[s])[1:]          # onset to onset, from the second stride on
        clearance = np.array([p[e[i]:s[i + 1], 2].max() - P[i, 2] for i in range(len(s) - 1)])
        return dict(stride_length=stride_length, stride_time=stride_time, cadence=120.0 / stride_time,
                    gait_speed=stride_length[1:] / stride_time, clearance=clearance,
                    turning_angle=np.degrees(np.diff(psi)), n_stances=len(s))

    return (gait_parameters,)


@app.cell(hide_code=True)
def _(estimated_yaw, gait_parameters, np, run_zaru, run_zupt, sim, stationary):
    # jb: include=false
    def true_gait_parameters(s):
        T = s["stride_time"]
        return dict(stride_length=s["stride_length"], stride_time=T[1:], cadence=120.0 / T[1:],
                    gait_speed=s["stride_length"][1:] / T[1:], clearance=s["clearance"],
                    turning_angle=np.degrees(s["turn"]))

    gait_truth = true_gait_parameters(sim)
    gait_zupt = gait_parameters(sim["t"], run_zupt["p"], estimated_yaw(run_zupt), stationary)
    gait_zaru = gait_parameters(sim["t"], run_zaru["p"], estimated_yaw(run_zaru), stationary)
    return gait_truth, gait_zaru, gait_zupt, true_gait_parameters


@app.cell(hide_code=True)
def _(gait_truth, gait_zaru, gait_zupt, mo, np):
    _rows = []
    for _key, _label, _fmt in [
        ("stride_length", "stride length (m)", ".3f"),
        ("stride_time", "stride time (s)", ".3f"),
        ("cadence", "cadence (steps/min)", ".1f"),
        ("gait_speed", "gait speed (m/s)", ".3f"),
        ("clearance", "foot clearance (m)", ".3f"),
        ("turning_angle", "turning angle (deg)", ".2f"),
    ]:
        _tr, _a, _b = gait_truth[_key], gait_zupt[_key], gait_zaru[_key]
        _rows.append(
            f"| {_label} | {_tr.mean():{_fmt}} | {_b.mean():{_fmt}} | {np.abs(_a - _tr).mean():{_fmt}} "
            f"| {np.abs(_b - _tr).mean():{_fmt}} | {np.abs(_b - _tr).max():{_fmt}} |"
        )
    mo.md(
        f"The detector found {gait_zaru['n_stances']} stances, the initial standing period plus one "
        f"per stride, so all {len(gait_truth['stride_length'])} strides are segmented correctly. "
        f"Means are over strides; errors compare each stride's estimate with its true value.\n\n"
        "| Parameter | True mean | Estimated mean (ZUPT + ZARU) | Mean abs. error, ZUPT | "
        "Mean abs. error, ZUPT + ZARU | Max abs. error, ZUPT + ZARU |\n"
        "|:---|:---:|:---:|:---:|:---:|:---:|\n" + "\n".join(_rows)
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Stride length is accurate to a few millimeters, about $0.2\%$ of the stride, and clearance to a couple of millimeters. Stride time, cadence, and gait speed inherit an error of at most one sample period (10 ms) from the timing of the detector. Turning angle is where ZARU matters most: without it, the vertical gyroscope bias adds its drift over each stride to every turning angle, as the observability analysis predicted.

    <img src="public/ch21_gait_parameters.svg" class="graphic" alt="Two panels plotting per-stride values for the 24 strides. Left: stride length, true value 1.4 m, with estimates from both filters within about a centimeter. Right: turning angle, true value 0 degrees except 45 degrees on strides 11 to 14, with both estimates on top of the truth." />
    """)
    return


@app.cell(hide_code=True)
def _(IMAGES_DIR, gait_truth, gait_zaru, gait_zupt, np, plt):
    # jb: include=false
    _fig, _axs = plt.subplots(1, 2, figsize=(11, 3.6))
    _i = np.arange(1, len(gait_truth["stride_length"]) + 1)
    for _a, _key, _lab in [(_axs[0], "stride_length", "stride length (m)"), (_axs[1], "turning_angle", "turning angle (deg)")]:
        _a.plot(_i, gait_truth[_key], color="black", lw=1.5, label="truth")
        _a.plot(_i, gait_zupt[_key], "s", mfc="none", mec="C0", ms=5, label="ZUPT")
        _a.plot(_i, gait_zaru[_key], "o", color="C1", ms=3.5, label="ZUPT + ZARU")
        _a.set_xlabel("stride")
        _a.set_ylabel(_lab)
        _a.grid(visible=True, alpha=0.9, linewidth=0.4)
        _a.legend(fontsize=8)
    _axs[0].set_ylim(1.35, 1.45)
    _axs[0].set_title("Stride length per stride", style="italic")
    _axs[1].set_title("Turning angle per stride", style="italic")
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch21_gait_parameters.svg")
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch21-sec-interactive-tuning-the-detector -->
    ## Interactive: Tuning the Detector

    The whole pipeline (simulate, detect, filter, segment) runs again for each setting. The noise slider scales both IMU noise levels; the detector and the filter are told the true noise level, so the SHOE statistic and $\mathbf Q$ scale with it. Try a threshold of $10^{1.5}$ or $10^{4.5}$, and then raise the noise to see that a threshold that worked for one sensor fails for another.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    ui_log_gamma = mo.ui.slider(1.0, 5.0, 0.1, value=3.0, label=r"detector threshold $\log_{10}\gamma$", show_value=True)
    ui_noise = mo.ui.slider(0.5, 10.0, 0.5, value=1.0, label="IMU noise (multiple of default)", show_value=True)
    ui_zaru = mo.ui.checkbox(value=True, label="zero angular rate updates")
    return ui_log_gamma, ui_noise, ui_zaru


@app.cell(hide_code=True)
def _(
    align_level,
    estimated_yaw,
    gait_parameters,
    graphic,
    mo,
    np,
    plt,
    simulate_gait,
    stat_shoe,
    ui_log_gamma,
    ui_noise,
    ui_zaru,
    walk_turns,
    zupt_ekf,
):
    _m = ui_noise.value
    _s = simulate_gait(n_strides=24, turn_angles=walk_turns, seed=0, gyro_noise=0.01 * _m, accel_noise=0.05 * _m)
    _st = stat_shoe(_s["f_m"], _s["omega_m"], sigma_a=0.05 * _m, sigma_g=0.01 * _m) < 10**ui_log_gamma.value
    _run = zupt_ekf(_s["omega_m"], _s["f_m"], _s["dt"], _st, align_level(_s["f_m"][:100]),
                    zaru=ui_zaru.value, sigma_a=0.05 * _m, sigma_g=0.01 * _m)
    _gp = gait_parameters(_s["t"], _run["p"], estimated_yaw(_run), _st)
    _fig, (_a0, _a1) = plt.subplots(1, 2, figsize=(11, 3.8), width_ratios=[1.3, 1])
    _a0.plot(_s["p"][:, 0], _s["p"][:, 1], color="black", lw=2, label="true path")
    _a0.plot(_run["p"][:, 0], _run["p"][:, 1], color="C1", lw=1.3, label="estimate")
    _a0.set_xlim(-2, 18)
    _a0.set_ylim(-4, 7.5)
    _a0.set_aspect("equal")
    _a0.set_xlabel("East (m)")
    _a0.set_ylabel("North (m)")
    _a0.legend(fontsize=8, loc="upper left")
    _a0.set_title("Top view", style="italic")
    _n = len(_gp["stride_length"])
    _a1.axhline(_s["stride_length"][0], color="black", lw=1.5, label="true stride length")
    if _n > 0:
        _a1.plot(np.arange(1, _n + 1), _gp["stride_length"], "o", color="C1", ms=4, label="estimated")
    _a1.set_xlabel("detected stride")
    _a1.set_ylabel("stride length (m)")
    _a1.set_ylim(0, 2.5)
    _a1.legend(fontsize=8, loc="lower right")
    _a1.set_title("Stride lengths", style="italic")
    for _a in (_a0, _a1):
        _a.grid(visible=True, alpha=0.9, linewidth=0.4)
    _fig.tight_layout()
    interactive_result = dict(
        n_stances=_gp["n_stances"], n_true=len(_s["stride_length"]) + 1,
        final_error=np.linalg.norm(_run["p"][-1] - _s["p"][-1]),
        stride_mae=(np.abs(_gp["stride_length"] - _s["stride_length"]).mean()
                    if _n == len(_s["stride_length"]) else None),
    )
    mo.vstack([ui_log_gamma, ui_noise, ui_zaru, graphic(_fig)])
    return (interactive_result,)


@app.cell(hide_code=True)
def _(interactive_result, mo):
    _r = interactive_result
    _seg = (
        f"all strides are segmented correctly and the mean stride-length error is {100 * _r['stride_mae']:.1f} cm"
        if _r["stride_mae"] is not None
        else "the segmentation is broken, so the per-stride parameters no longer correspond to real strides"
    )
    mo.md(
        f"The detector found {_r['n_stances']} stances where there are {_r['n_true']}; {_seg}. "
        f"The final position error is {_r['final_error']:.2f} m."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch21-sec-failure-modes -->
    ## Failure Modes

    /// caution | ⚠️ **Assumptions and Failure Modes**
    Zero-velocity-aided inertial navigation rests on these assumptions:

    1. **The foot is truly still during every detected stance, and every stance is detected.** False detections inject false zero-velocity measurements; missed detections leave the INS free-running for longer. Both depend on the threshold, the sensor noise, and the gait.
    2. **Stances are long enough and frequent enough.** The error grows like $t^3$ between updates (Chapter 20). In running, foot flat can be shorter than the detector's window.
    3. **The ground is level, flat, and stationary.** Foot clearance as defined above assumes level ground, and a foot standing in a moving elevator or vehicle is not at zero velocity relative to the Earth.
    4. **The sensors stay within range.** Saturated readings corrupt the swing, and the filter then attributes the resulting velocity error to the wrong causes.
    5. **Errors stay small.** The error model is linear in $\delta\mathbf x$. Long gaps between updates, or a bad initialization, can make the errors large enough that the linearization fails ([Chapter 15](#ch15-sec-large-initial-error)).
    6. **Heading is not observable** from zero velocity alone, so long walks need a heading aid.
    ///

    The table runs the same filter (ZUPT and ZARU) on scenarios that break the first four assumptions. Running is simulated with a stride time of 0.75 s, a stride length of 2.6 m (3.5 m/s), stance at $35\%$ and foot flat at $6\%$ of the cycle; stairs with strides of 0.6 m that climb 0.34 m (two 17 cm steps per stride) and a 10 cm clearance bump; saturation by clipping the gyroscope at $\pm250^\circ/\text{s}$ ($4.36$ rad/s), a common factory default range, below the $6.5$ rad/s peak of our walk.
    """)
    return


@app.cell(hide_code=True)
def _(
    GAMMA,
    align_level,
    estimated_yaw,
    gait_parameters,
    np,
    sim,
    simulate_gait,
    stat_shoe,
    zupt_ekf,
):
    # jb: include=false
    def _evaluate(s, gamma, label):
        _st = stat_shoe(s["f_m"], s["omega_m"]) < gamma
        _run = zupt_ekf(s["omega_m"], s["f_m"], s["dt"], _st, align_level(s["f_m"][:100]), zaru=True)
        _gp = gait_parameters(s["t"], _run["p"], estimated_yaw(_run), _st)
        return dict(label=label, n=_gp["n_stances"], n_true=len(s["stride_length"]) + 1,
                    length=_gp["stride_length"].mean() if len(_gp["stride_length"]) else np.nan,
                    length_true=s["stride_length"].mean(),
                    clearance=_gp["clearance"].mean() if len(_gp["clearance"]) else np.nan,
                    clearance_true=s["clearance"].mean(),
                    final=np.linalg.norm(_run["p"][-1] - s["p"][-1]))

    _running = simulate_gait(n_strides=24, stride_time=0.75, stride_length=2.6, stance_frac=0.35,
                             flat_frac=0.06, clearance=0.25, pitch_toe_off=0.7, pitch_heel_strike=-0.4)
    _stairs = simulate_gait(n_strides=12, stride_time=1.3, stride_length=0.6, rise=0.34, clearance=0.10)
    _saturated = dict(sim, omega_m=np.clip(sim["omega_m"], -np.radians(250), np.radians(250)))
    failure_results = [
        _evaluate(sim, GAMMA, r"walking, $\gamma = 10^3$ (baseline)"),
        _evaluate(sim, 10.0, r"walking, threshold too low, $\gamma = 10$"),
        _evaluate(sim, 3e4, r"walking, threshold too high, $\gamma = 3\cdot10^4$"),
        _evaluate(_running, GAMMA, r"running, walking threshold $\gamma = 10^3$"),
        _evaluate(_running, 1e4, r"running, raised threshold $\gamma = 10^4$"),
        _evaluate(_stairs, GAMMA, r"stairs, $\gamma = 10^3$"),
        _evaluate(_saturated, GAMMA, r"walking, gyroscope clipped at $\pm250^\circ$/s"),
    ]
    return (failure_results,)


@app.cell(hide_code=True)
def _(failure_results, mo):
    _rows = [
        f"| {_r['label']} | {_r['n']} ({_r['n_true']}) | {_r['length']:.2f} ({_r['length_true']:.2f}) "
        f"| {_r['clearance']:.2f} ({_r['clearance_true']:.2f}) | {_r['final']:.2f} |"
        for _r in failure_results
    ]
    mo.md(
        "| Scenario | Stances found (true) | Mean stride length, m (true) | Mean foot clearance, m (true) "
        "| Final position error, m |\n|:---|:---:|:---:|:---:|:---:|\n" + "\n".join(_rows)
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Reading the table row by row:

    - **Threshold too low.** Noise occasionally pushes the statistic above $\gamma$ in the middle of a stance, splitting it in two. Navigation barely suffers (most stationary samples still get updates), but segmentation breaks: there are more "stances" than strides, and per-stride parameters become meaningless.
    - **Threshold too high.** Samples at the start and end of the swing, where the foot moves slowly, are declared stationary. The filter is told that a moving foot is still, and it believes it: here the estimated strides shrink by about a third. Higher thresholds still also create spurious stances in mid-swing.
    - **Running.** Foot flat lasts about 50 ms, barely one detector window, so at the walking threshold almost no stances are found and the INS runs free between the rare updates. Raising the threshold recovers the stances, but each one now yields only a few updates, some at samples where the foot is still moving, and the stride lengths are off by about 5%. Practical systems use higher sample rates, thresholds that adapt to the detected gait speed, or a separate motion classifier.
    - **Stairs.** The foot is flat on each step, so detection and navigation work, but the clearance definition fails: measured from the preceding stance, the maximum height during a climbing stride is the 0.34 m rise, not the 10 cm by which the foot clears the step edge. Clearance on stairs needs the geometry of the steps. Real stair descent adds a further problem: the forefoot often lands first and the foot rotates during stance, which a detector tuned on level walking can miss.
    - **Saturation.** The clipped gyroscope under-reports the swing rotation, so the computed attitude is wrong during the swing, and with it the gravity compensation. The resulting velocity error is attributed to tilt and bias errors that do not exist. Choose ranges with margin: $\pm2000^\circ/\text{s}$ and $\pm16\,g$ are common for foot-mounted IMUs. Our simulator has no heel-strike impacts, whose acceleration spikes of several $g$ make accelerometer saturation a real risk too.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch21-sec-further-reading -->
    ## Further Reading

    - @foxlin2005, *Pedestrian Tracking with Shoe-Mounted Inertial Sensors*: the paper that introduced zero-velocity updates in a Kalman filter for foot-mounted IMUs.
    - @skog2010, *Zero-Velocity Detection—An Algorithm Evaluation*: the SHOE detector and a comparison of detectors on real data.
    - @nilsson2012, *Foot-Mounted INS for Everybody: An Open-Source Embedded Implementation*: OpenShoe, an open hardware and software implementation of the filter in this chapter.
    - @jimenez2009, *A Comparison of Pedestrian Dead-Reckoning Algorithms Using a Low-Cost MEMS IMU*: zero-velocity-aided INS compared with step-counting approaches.
    - @sola2017, *Quaternion Kinematics for the Error-State Kalman Filter*: a thorough derivation of error-state filters, including the reset step.
    - @borenstein2009, *Heuristic Reduction of Gyro Drift for Personnel Tracking Systems*: heuristic drift elimination.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch21-sec-summary -->
    ## Summary

    - A **pseudo-measurement** is a measurement known from a constraint rather than read from a sensor. The **zero-velocity update** uses $\mathbf z = \mathbf 0 = \mathbf v + \mathbf n_z$ at every sample a detector declares stationary.
    - The **error-state filter** propagates a nominal state with the strapdown mechanization and a 15-state error $[\delta\mathbf p, \delta\mathbf v, \delta\boldsymbol\theta, \delta\mathbf b_a, \delta\mathbf b_g]$ with the linearized model $\dot{\delta\mathbf v} = -\hat{\mathbf R}[\hat{\mathbf f}]_\times\delta\boldsymbol\theta - \hat{\mathbf R}\delta\mathbf b_a - \hat{\mathbf R}\mathbf n_a$, $\dot{\delta\boldsymbol\theta} = -[\hat{\boldsymbol\omega}]_\times\delta\boldsymbol\theta - \delta\mathbf b_g - \mathbf n_g$, discretized as $\boldsymbol\Phi = \mathbf I + \mathbf F\Delta t$. The update uses $\mathbf H = [\mathbf 0\ \mathbf I\ \mathbf 0\ \mathbf 0\ \mathbf 0]$, followed by injection and reset. We verified $\mathbf F$ numerically against the nonlinear mechanization.
    - Because of the cross-covariances, a velocity measurement corrects position, tilt, and biases as well. On our walk, the error drops from hundreds of meters to tens of centimeters.
    - **Heading and position are unobservable**: rotating the trajectory about the vertical changes no measurement. At rest, the vertical gyroscope bias and two tilt/accelerometer-bias combinations are hidden too. The **zero angular rate update** makes the gyroscope biases observable and slows heading drift; bounding it requires a heading aid such as a magnetometer or heuristic drift elimination.
    - Per stride we estimate **stride length**, stride time, **cadence**, **gait speed**, **foot clearance**, and turning angle, with errors of millimeters, milliseconds, and fractions of a degree on simulated walking.
    - The method fails when its assumptions fail: thresholds that do not match the gait or sensor, running, stairs (for clearance), and sensor saturation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch21-sec-whats-next -->
    ## What's Next

    This chapter ends the main path. We started in the [Introduction](introduction.md) with a bathroom scale and the question of how much to trust a new measurement, and we end with a fifteen-state filter that tracks a walking foot. It runs on the same predict-and-update structure, and its gain answers the same question. Natural next steps go beyond this book. An offline gait analysis can smooth each stride with the Rauch–Tung–Striebel smoother mentioned in [Chapter 14](#ch14-sec-smoothing), using measurements on both sides of every swing. Real recordings bring the effects our simulator leaves out: impacts, soft tissue, and walkers who shuffle, stop, and turn on the spot. If any foundation along the way felt thin, the [appendices](appendix_c_calculus.md) build it from the ground up.
    """)
    return


if __name__ == "__main__":
    app.run()
