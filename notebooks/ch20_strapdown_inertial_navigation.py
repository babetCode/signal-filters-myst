# /// script
# dependencies = [
#     "marimo>=0.25.1",
#     "matplotlib==3.11.2",
#     "numpy==2.5.3",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="20. Strapdown Inertial Navigation", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "Dead Reckoning a Walking Foot"
    abbreviations:
      IMU: inertial measurement unit
      INS: inertial navigation system
      ENU: east-north-up
      FLU: forward-left-up
      MEMS: micro-electro-mechanical systems
      GLRT: generalized likelihood ratio test
      SHOE: stance hypothesis optimal detector
      ZUPT: zero-velocity update
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
    [Chapter 19](ch19_ahrs.md) estimated the {term}`attitude` of an {term}`inertial measurement unit`. An IMU strapped to a shoe can, in principle, do much more: integrate its {term}`gyroscope` once to get attitude, its {term}`accelerometer` twice to get position, and so track every stride a person takes, with no camera, beacon, or satellite in sight. That is **strapdown inertial navigation**, the key concept of this chapter.

    Its central difficulty is also the reason this chapter belongs in a book about filters. Integration accumulates errors. We will derive exactly how fast: a constant accelerometer error grows into a position error proportional to $t^2$, and a constant gyroscope error into one proportional to $t^3$. With a consumer-grade IMU, the position is off by meters within a few seconds. Walking offers a way out: once per stride, the foot stands still on the ground, so its true velocity is known to be zero. This chapter builds the navigation equations, a synthetic walking simulator with exact ground truth, and detectors that find the stationary moments. [Chapter 21](ch21_zero_velocity_updates.md) turns those moments into Kalman filter measurements.

    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    Inertial navigation integrates, and integration turns small constant sensor errors into position errors that grow like $t^2$ and $t^3$. A walking foot is stationary once per stride, which provides a perfect velocity measurement roughly every second, provided we can detect when it happens.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// important | 🔗 **Prerequisites**
        attrs: {class: no-icon}
    - [Chapter 17](ch17_rotations.md): rotation matrices, ZYX Euler angles, the kinematics $\dot{\mathbf R} = \mathbf R[\boldsymbol\omega]_\times$, the exponential map, and the small-angle approximation.
    - [Chapter 18](ch18_quaternions.md): the Hamilton product, $\dot q = \tfrac12 q \otimes [0, \boldsymbol\omega]$, and exact integration for a constant rate.
    - [Chapter 19](ch19_ahrs.md): the IMU sensor models, specific force, tilt from the accelerometer, and the error-state convention $q = \hat q \otimes \delta q(\delta\boldsymbol\theta)$.
    - [Chapter 8](ch8_bayesian_view.md) and [Chapter 12](ch12_vectors_matrices_covariance.md): likelihoods and the multivariate normal density (only for the GLRT detector).
    - [Chapter 9](ch9_noise_levels.md): white noise, random walks, and the chi-squared distribution.
    - [Appendix C: Taylor's Theorem](appendix_c_calculus.md) and [Appendix C: The Fundamental Theorem of Calculus](appendix_c_calculus.md).
    - [Appendix D: Cross Products and Skew-Symmetric Matrices](appendix_d_linear_algebra.md) and [Appendix D: The Matrix Exponential](appendix_d_linear_algebra.md).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conventions

    We use the orientation conventions of Chapters 17–19 without change:

    - **Navigation frame $n$:** a local-level {term}`reference frame` with axes East, North, Up (ENU). Gravity is $\mathbf g^n = [0, 0, -g]^\top$ with $g = 9.81\ \text{m/s}^2$.
    - **Body frame $b$:** fixed to the IMU, with axes forward, left, up (FLU). At zero attitude the body frame coincides with ENU, facing East.
    - $\mathbf R^n_b$ is the {term}`rotation matrix` that maps body coordinates to navigation coordinates, $\mathbf v^n = \mathbf R^n_b \mathbf v^b$, and $q^n_b$ is the corresponding Hamilton, scalar-first unit {term}`quaternion`. {term}`Euler angles` are ZYX: $\mathbf R^n_b = \mathbf R_z(\psi)\mathbf R_y(\theta)\mathbf R_x(\phi)$. Because the FLU $y$ axis points left, a **positive pitch $\theta$ tilts the forward axis (the toe) down**.
    - $\boldsymbol\omega^b$ is the {term}`angular velocity` of the body relative to the navigation frame, in body coordinates, and the kinematics are $\dot{\mathbf R}^n_b = \mathbf R^n_b[\boldsymbol\omega^b]_\times$, $\dot q^n_b = \tfrac12 q^n_b \otimes [0, \boldsymbol\omega^b]$. We neglect the Earth's rotation ($7.3\times10^{-5}$ rad/s, about 140 times smaller than the gyroscope bias below) and treat the walking area as flat with constant $g$.
    - The {term}`specific force` is $\mathbf f^b = (\mathbf R^n_b)^\top(\mathbf a^n - \mathbf g^n)$, where $\mathbf a^n$ is the acceleration of the IMU in the navigation frame. At rest and level it reads $[0, 0, +g]$.
    - The IMU samples at 100 Hz ($\Delta t = 0.01$ s) and its measurements are
    $$\boldsymbol\omega_m = \boldsymbol\omega^b + \mathbf b_g + \mathbf n_g, \qquad \mathbf f_m = \mathbf f^b + \mathbf b_a + \mathbf n_a,$$
    with constant {term}`sensor biases <sensor bias>` $\mathbf b_g, \mathbf b_a$ and {term}`white noise` samples $\mathbf n_g, \mathbf n_a$ that are independent, zero-mean, and normal with covariances $\sigma_g^2\mathbf I$ and $\sigma_a^2\mathbf I$.

    | Parameter | Default value |
    |---|---|
    | sample rate | 100 Hz |
    | gyroscope white noise $\sigma_g$ | 0.01 rad/s |
    | gyroscope bias, per axis | 0.01 rad/s |
    | accelerometer white noise $\sigma_a$ | 0.05 m/s² |
    | accelerometer bias, per axis | 0.05 m/s² |

    These are typical of an inexpensive MEMS IMU. Where no confusion is possible we write $\mathbf R := \mathbf R^n_b$, $q := q^n_b$, $\boldsymbol\omega := \boldsymbol\omega^b$, and $\mathbf f := \mathbf f^b$. A hat marks a computed quantity, as in [Chapter 7](ch7_optimal_alpha.md): $\hat{\mathbf p}$ is the computed position and $\mathbf p$ the true one.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Dead Reckoning and Strapdown Navigation

    Sailors without satellites estimated their position from a known starting point, their speed, their heading, and the time elapsed. The method needs no position measurement after the start, which is both its appeal and its weakness.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Dead reckoning**</u>

    A method that estimates the position $\mathbf p(t)$ of a moving object as a known initial position $\mathbf p(0)$ plus the integral (or sum) of estimated velocities or displacements over $[0, t]$, without using any measurement of position at a time after $0$.
    ///

    Early inertial navigation systems mounted the accelerometers on a gimbaled platform that motors kept level and pointing North, so that the accelerometers measured navigation-frame components directly. Modern MEMS sensors are instead fixed rigidly to the vehicle (here, the shoe), and the platform's job is done in software by tracking $\mathbf R$.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Strapdown inertial navigation**</u>

    Dead reckoning in which the attitude, velocity, and position of a body are computed by numerically integrating the angular rate and specific force measured by an inertial measurement unit that is rigidly attached to the body.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The Navigation Equations

    Three differential equations relate the IMU's outputs to the quantities we want.

    - **Position.** The velocity $\mathbf v := \dot{\mathbf p}$ of the IMU relative to the navigation frame is, by definition, the derivative of its position: $\dot{\mathbf p} = \mathbf v$.
    - **Velocity.** By definition $\dot{\mathbf v} = \mathbf a^n$. Multiply the definition of specific force by $\mathbf R$ and use $\mathbf R\mathbf R^\top = \mathbf I$ (rotation matrices are orthogonal, [Chapter 17](ch17_rotations.md)): $\mathbf R\mathbf f = \mathbf a^n - \mathbf g^n$. Hence $\dot{\mathbf v} = \mathbf R\mathbf f + \mathbf g^n$. The accelerometer cannot sense gravity as an acceleration (a falling IMU reads zero), so we must add $\mathbf g^n$ back, and to add it we must know which way is down in body coordinates. Attitude errors therefore become velocity errors.
    - **Attitude.** $\dot q = \tfrac12 q \otimes [0, \boldsymbol\omega]$, equivalently $\dot{\mathbf R} = \mathbf R[\boldsymbol\omega]_\times$ ([Chapter 18](ch18_quaternions.md)).

    $$\boxed{\;\dot q = \tfrac12\, q\otimes[0, \boldsymbol\omega], \qquad \dot{\mathbf v} = \mathbf R(q)\,\mathbf f + \mathbf g^n, \qquad \dot{\mathbf p} = \mathbf v.\;}$$

    A strapdown INS integrates these equations with the measured $\boldsymbol\omega_m$ and $\mathbf f_m$ in place of the unknown true $\boldsymbol\omega$ and $\mathbf f$. Integrating them in that order (attitude, then velocity, then position) is called **mechanization**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Discrete Implementation at 100 Hz

    The IMU delivers samples $\boldsymbol\omega_k, \mathbf f_k$ at times $t_k = k\,\Delta t$. Between samples we know nothing, so we assume every signal varies linearly from one sample to the next and integrate that assumption exactly:

    1. **Attitude.** With $\bar{\boldsymbol\omega}_k := \tfrac12(\boldsymbol\omega_{k-1} + \boldsymbol\omega_k)$, the time average of the linearly interpolated rate,
    $$q_k = q_{k-1} \otimes \operatorname{Exp}_q(\bar{\boldsymbol\omega}_k\Delta t),$$
    where $\operatorname{Exp}_q$ maps a rotation vector to its unit quaternion. This is [Chapter 18](ch18_quaternions.md)'s exact update for a rate held constant over the sample period, applied to the averaged rate instead of the latest sample $\boldsymbol\omega_k$; for a rate that changes linearly about a fixed axis, it is exact.[^coning] We renormalize $q_k$ after each step to remove round-off.
    2. **Velocity.** With $\mathbf a_k := \mathbf R(q_k)\mathbf f_k + \mathbf g^n$, the trapezoidal rule gives $\mathbf v_k = \mathbf v_{k-1} + \tfrac12(\mathbf a_{k-1} + \mathbf a_k)\Delta t$.
    3. **Position.** Likewise $\mathbf p_k = \mathbf p_{k-1} + \tfrac12(\mathbf v_{k-1} + \mathbf v_k)\Delta t$.

    The [trapezoidal rule](https://en.wikipedia.org/wiki/Trapezoidal_rule) is exact for linear integrands, and for twice-differentiable integrands its total error over a fixed time span is proportional to $\Delta t^2$. Once we have a simulator with exact ground truth we will check this rate numerically. The helper functions below are the ones from Chapters 17 and 18.

    [^coning]: When the rotation axis changes during a sample period, averaging $\boldsymbol\omega$ ignores the fact that rotations about different axes do not commute. Integrating the rotation vector to second order adds the correction $\tfrac{\Delta t^2}{12}\,\boldsymbol\omega_{k-1}\times\boldsymbol\omega_k$, the two-sample *coning* correction; see @savage1998. For the walking motions in this chapter it changes the computed positions by 1–2 cm over a 20 s walk, so we omit it.
    """)
    return


@app.cell
def helpers(np):
    # jb: echo=true
    G = 9.81                          # gravity magnitude, m/s^2
    G_N = np.array([0.0, 0.0, -G])    # gravity in ENU coordinates

    def skew(a):
        """[a]_x, so that skew(a) @ b == np.cross(a, b)."""
        return np.array([[0.0, -a[2], a[1]], [a[2], 0.0, -a[0]], [-a[1], a[0], 0.0]])

    def quat_mult(p, q):
        """Hamilton product p ⊗ q of scalar-first quaternions."""
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The mechanization itself is a short loop. We also need an initial attitude. While the IMU is at rest, $\mathbf f = \mathbf R^\top[0, 0, g]^\top = g\,[-\sin\theta,\ \cos\theta\sin\phi,\ \cos\theta\cos\phi]^\top$, so roll and pitch follow from the mean accelerometer reading exactly as in [Chapter 19](ch19_ahrs.md): $\phi = \operatorname{atan2}(f_y, f_z)$ and $\theta = \operatorname{atan2}\big(-f_x, \sqrt{f_y^2 + f_z^2}\big)$. Gravity says nothing about yaw, so we set $\psi = 0$. This choice is called **leveling**.
    """)
    return


@app.cell
def strapdown_cell(G_N, np, quat_exp, quat_mult, quat_to_rotmat):
    # jb: echo=true
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
        attrs: {class: no-icon}
    The navigation equations above assume:

    1. **A non-rotating, flat Earth with constant gravity.** Neglecting the Earth's rotation and curvature is harmless for a walk of a few minutes with MEMS sensors, whose biases are far larger. For hours-long navigation with precise sensors, the Coriolis and transport-rate terms must be added.
    2. **A rigid mount at a single point.** The equations describe the motion of the point where the accelerometer sits. A strap that slips or a sensor that wobbles on the shoe adds motion the foot did not make.
    3. **Measurements that represent the signals between samples.** The discrete scheme assumes the rates and forces vary linearly between samples. Impacts (heel strike) contain frequencies far above 50 Hz, which a 100 Hz IMU cannot represent; the result is integration error in exactly the moments that matter most.
    4. **Sensors within range.** A gyroscope or accelerometer that saturates reports a clipped value, and the integral of a clipped signal is wrong from then on.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## How Errors Grow

    Feeding $\boldsymbol\omega_m$ and $\mathbf f_m$ into the navigation equations integrates the biases and noise along with the signal. To see how fast the result degrades, we follow [Chapter 19](ch19_ahrs.md)'s error-state convention: an error is what must be *added to the computed value to obtain the true one*,
    $$\mathbf p = \hat{\mathbf p} + \delta\mathbf p, \qquad \mathbf v = \hat{\mathbf v} + \delta\mathbf v, \qquad \mathbf R = \hat{\mathbf R}\operatorname{Exp}(\delta\boldsymbol\theta),$$
    where $\operatorname{Exp}$ is [Chapter 17](ch17_rotations.md)'s exponential map and $\delta\boldsymbol\theta$ is a small rotation vector in body coordinates. So $\delta\mathbf p = -e$ in the notation $e = \hat x - x$ of [Chapter 7](ch7_optimal_alpha.md); only the sign differs, and every growth law below is about magnitudes.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Drift**</u>

    The part of the error of an estimate that is produced by integrating (or summing) errors in the measured rates of change of the estimated quantity, as opposed to an error present in the initial value.
    ///

    The cleanest setting isolates one error source at a time: an IMU lying motionless and level, so that the true attitude is $\mathbf R = \mathbf I$, the true rates are $\boldsymbol\omega = \mathbf 0$ and $\mathbf f = [0, 0, g]^\top$, and the true position and velocity stay zero.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// important | 📐 **Theorem (Drift Laws)**
        attrs: {class: no-icon}
    Let an IMU be at rest and level, and let the navigation equations be integrated exactly from the true initial velocity and position $\hat{\mathbf v}(0) = \hat{\mathbf p}(0) = \mathbf 0$. Suppose exactly one of the following errors is present and there is no noise.

    1. **Accelerometer bias** $\mathbf b_a$ (constant), with the correct initial attitude: $\ \delta\mathbf p(t) = -\tfrac12\,\mathbf b_a\,t^2$.
    2. **Tilt error** $\delta\boldsymbol\theta = [0, \varepsilon, 0]^\top$ in the initial attitude (constant, since the gyroscope is perfect): $\ \delta p_x(t) = \tfrac12\,g\sin\varepsilon\;t^2 \approx \tfrac12\,g\,\varepsilon\,t^2$ and $\delta p_y = 0$.
    3. **Gyroscope bias** $\mathbf b_g = [0, b, 0]^\top$ with $b \ne 0$, with the correct initial attitude: $\ \delta p_x(t) = -\,g\,\dfrac{bt - \sin bt}{b^2} = -\tfrac16\,g\,b\,t^3\,\big(1 + O\big((bt)^2\big)\big)$ and $\delta p_y = 0$.

    Each statement also holds for the other horizontal axis, with signs given by the same computation.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    In every case the true acceleration is zero, so $\delta\mathbf p = -\hat{\mathbf p}$, and $\hat{\mathbf p}$ is the double integral of the computed acceleration $\hat{\mathbf a} = \hat{\mathbf R}\,\mathbf f_m + \mathbf g^n$ (two applications of the [fundamental theorem of calculus](appendix_c_calculus.md)).

    1. The attitude is correct, $\hat{\mathbf R} = \mathbf I$, and $\mathbf f_m = [0, 0, g]^\top + \mathbf b_a$, so $\hat{\mathbf a} = \mathbf b_a$. Integrating twice gives $\hat{\mathbf p} = \tfrac12\mathbf b_a t^2$.
    2. From $\mathbf R = \hat{\mathbf R}\operatorname{Exp}(\delta\boldsymbol\theta)$ and $\mathbf R = \mathbf I$ we get $\hat{\mathbf R} = \operatorname{Exp}(\delta\boldsymbol\theta)^\top = \operatorname{Exp}(-\delta\boldsymbol\theta) = \mathbf R_y(-\varepsilon)$, because the exponential of a rotation vector along a coordinate axis is the elementary rotation about that axis ([Chapter 17](ch17_rotations.md)). Then $\hat{\mathbf a} = \mathbf R_y(-\varepsilon)[0, 0, g]^\top + \mathbf g^n = [-g\sin\varepsilon,\ 0,\ g(\cos\varepsilon - 1)]^\top$, a constant, so $\hat p_x = -\tfrac12 g\sin\varepsilon\, t^2$ and $\hat p_y = 0$. Finally $\sin\varepsilon = \varepsilon + O(\varepsilon^3)$ ([Taylor's theorem](appendix_c_calculus.md)).
    3. The computed attitude solves $\dot{\hat{\mathbf R}} = \hat{\mathbf R}[\boldsymbol\omega_m]_\times = \hat{\mathbf R}[b\,\mathbf e_y]_\times$ with $\hat{\mathbf R}(0) = \mathbf I$, whose unique solution is $\hat{\mathbf R}(t) = \exp(t[b\,\mathbf e_y]_\times) = \mathbf R_y(bt)$ ([Appendix D: The Matrix Exponential](appendix_d_linear_algebra.md)). Then $\hat{\mathbf a}(t) = [g\sin bt,\ 0,\ g(\cos bt - 1)]^\top$. Integrating, $\hat v_x(t) = g(1 - \cos bt)/b$ and $\hat p_x(t) = g(bt - \sin bt)/b^2$. Since $\sin x = x - x^3/6 + O(x^5)$, we get $bt - \sin bt = \tfrac16 (bt)^3\big(1 + O((bt)^2)\big)$. $\blacksquare$
    ///

    The three laws share one mechanism with different numbers of integrations. A bias in $\mathbf f$ is integrated twice. A tilt error rotates the $g$ that the accelerometer senses partly into the horizontal, creating a false horizontal acceleration $g\varepsilon$ that is integrated twice. A gyroscope bias makes the tilt itself grow linearly ($\delta\theta_y = -bt$), adding a third integration. [Chapter 21](ch21_zero_velocity_updates.md) derives the general linearized error equations, of which these are special cases.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Noise and Leveling

    White noise drifts too, but more slowly. Summing $t/\Delta t$ independent accelerometer noise samples, each contributing $\mathbf n_a\Delta t$ to the velocity, gives a {term}`random walk` in velocity with per-axis standard deviation $\sigma_a\sqrt{\Delta t\,t}$; integrating it once more gives a position standard deviation of $\sigma_a\sqrt{\Delta t/3}\;t^{3/2}$. Gyroscope noise makes the tilt a random walk with standard deviation $\sigma_g\sqrt{\Delta t\,t}$, and two integrations of $g$ times that tilt give $g\,\sigma_g\sqrt{\Delta t/20}\;t^{5/2}$.[^iwp] The table compares all five sources with the default parameters and an initial tilt of $\varepsilon = 0.005$ rad, which is what leveling produces with a $0.05\ \text{m/s}^2$ accelerometer bias (see below).

    One more observation matters for [Chapter 21](ch21_zero_velocity_updates.md). If we level with a biased accelerometer, the computed attitude makes $\hat{\mathbf R}\mathbf f_m$ point straight up. While the IMU stays still in that orientation, the horizontal accelerometer bias and the tilt error it causes therefore cancel *exactly*: the tilt error is $\varepsilon \approx b_{a,x}/g$, and $\tfrac12 g\varepsilon t^2 - \tfrac12 b_{a,x}t^2 = 0$. Only the vertical bias component still drifts. At rest, a horizontal accelerometer bias and a tilt error are indistinguishable.

    [^iwp]: Both results use $\operatorname{Var}\big(\sum_i \mathbf n_i\big) = \sum_i\operatorname{Var}(\mathbf n_i)$ for independent samples ([Chapter 6](ch6_expectation_and_variance.md)), approximated by integrals for small $\Delta t$; for example, the position is a sum of $t/\Delta t$ noise samples weighted by the remaining time, and $\sigma_a^2\Delta t\int_0^t (t-s)^2\,ds = \sigma_a^2\Delta t\,t^3/3$. We checked both formulas by Monte Carlo simulation.
    """)
    return


@app.cell(hide_code=True)
def _(G, mo, np):
    _dt, _ba, _eps, _bg, _sa, _sg = 0.01, 0.05, 0.005, 0.01, 0.05, 0.01
    _laws = [
        ("accelerometer bias $b_a$", r"$\tfrac12 b_a t^2$", lambda t: 0.5 * _ba * t**2),
        (r"tilt error $\varepsilon$", r"$\tfrac12 g\varepsilon t^2$", lambda t: 0.5 * G * _eps * t**2),
        ("gyroscope bias $b_g$", r"$\tfrac16 g b_g t^3$", lambda t: G * _bg * t**3 / 6),
        (r"accelerometer noise $\sigma_a$ (1 std.)", r"$\sigma_a\sqrt{\Delta t/3}\,t^{3/2}$", lambda t: _sa * np.sqrt(_dt / 3) * t**1.5),
        (r"gyroscope noise $\sigma_g$ (1 std.)", r"$g\sigma_g\sqrt{\Delta t/20}\,t^{5/2}$", lambda t: G * _sg * np.sqrt(_dt / 20) * t**2.5),
    ]
    _rows = "\n".join(
        f"| {_name} | {_law} | {_f(1.0) * 100:.1f} cm | {_f(10.0):.2f} m | {_f(30.0):.1f} m |"
        for _name, _law, _f in _laws
    )
    mo.md(
        "| Error source | Horizontal position error | after 1 s | after 10 s | after 30 s |\n"
        "|---|---|---|---|---|\n" + _rows
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Two facts stand out. After one second, roughly one stride, every source contributes only centimeters. After ten seconds, the gyroscope bias alone has moved the computed position by more than 16 m, and after thirty seconds by more than 400 m. Because the error grows like a power of $t$, shortening the integration interval is enormously effective: halving it divides the gyroscope-bias term by eight.

    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    Free-running inertial navigation with a consumer IMU is accurate to centimeters for about a second and useless after ten. Its errors are small over short intervals, so anything that periodically resets them (such as a known zero velocity once per stride) can keep the whole trajectory accurate.
    ///

    ### Interactive: Drift Demo

    The sliders set the three error sources for the motionless, level IMU of the theorem. Each solid curve is the horizontal position error $\lVert\delta\mathbf p_h\rVert$ produced by the actual 100 Hz mechanization with one source switched on; the dashed curves are the drift laws. The black curve has all three sources on at once. The axes are logarithmic, so each power law is a straight line whose slope is its exponent: 2, 2, and 3.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    drift_ba = mo.ui.slider(0.0, 0.2, 0.005, value=0.05, label=r"accelerometer bias $b_a$ (m/s²)", show_value=True)
    drift_tilt = mo.ui.slider(0.0, 20.0, 0.5, value=5.0, label=r"tilt error $\varepsilon$ (mrad)", show_value=True)
    drift_bg = mo.ui.slider(0.0, 0.03, 0.001, value=0.01, label=r"gyroscope bias $b_g$ (rad/s)", show_value=True)
    drift_T = mo.ui.slider(5, 60, 5, value=30, label="duration (s)", show_value=True)
    return drift_T, drift_ba, drift_bg, drift_tilt


@app.cell(hide_code=True)
def _(
    G,
    drift_T,
    drift_ba,
    drift_bg,
    drift_tilt,
    graphic,
    mo,
    np,
    plt,
    quat_exp,
    strapdown,
):
    _ba, _eps, _bg, _T = drift_ba.value, drift_tilt.value * 1e-3, drift_bg.value, drift_T.value
    _dt = 0.01
    _N = int(round(_T / _dt)) + 1
    _t = np.arange(_N) * _dt
    _zero = np.zeros(3)

    def _horizontal_error(ba, eps, bg):
        _omega_m = np.tile([0.0, bg, 0.0], (_N, 1))
        _f_m = np.tile([ba, 0.0, G], (_N, 1))
        _q0 = quat_exp(np.array([0.0, -eps, 0.0]))   # R_hat = Exp(-dtheta) when R = I
        _, _, _p_hat = strapdown(_omega_m, _f_m, _dt, _q0, _zero, _zero)
        return np.hypot(_p_hat[:, 0], _p_hat[:, 1])  # |dp_h| = |p_h - p_hat_h| with p = 0

    _fig, _ax = plt.subplots(figsize=(7, 4.2))
    _cases = [
        (_ba, (_ba, 0.0, 0.0), 0.5 * _ba * _t**2, "C0", 5.0, "accelerometer bias"),
        (_eps, (0.0, _eps, 0.0), 0.5 * G * _eps * _t**2, "C2", 2.0, "tilt error"),
        (_bg, (0.0, 0.0, _bg), G * _bg * _t**3 / 6, "C3", 2.0, "gyroscope bias"),
    ]
    _m = _t > 0
    for _on, _args, _law, _c, _lw, _name in _cases:
        if _on > 0:
            _ax.loglog(_t[_m], _horizontal_error(*_args)[_m], color=_c, lw=_lw, alpha=0.8,
                       label=f"{_name}: simulated")
            _ax.loglog(_t[_m], _law[_m], color=_c, ls="--", lw=1.2, label=f"{_name}: drift law")
    _total = _horizontal_error(_ba, _eps, _bg)
    if np.any(_total[_m] > 0):
        _ax.loglog(_t[_m], np.maximum(_total[_m], 1e-9), color="black", lw=1.5, label="all three together")
    _ax.axhline(1.0, color="gray", lw=0.8, ls=":")
    _ax.set_ylim(1e-4, 1e4)
    _ax.set_xlim(_dt, _T)
    _ax.set_xlabel("time (s)")
    _ax.set_ylabel("horizontal position error (m)")
    _ax.set_title("Drift of a motionless, level IMU", style="italic")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4, which="both")
    _ax.legend(fontsize=7.5, loc="upper left")
    _fig.tight_layout()
    mo.vstack([drift_ba, drift_tilt, drift_bg, drift_T, graphic(_fig)])
    return


@app.cell(hide_code=True)
def _(G, drift_ba, drift_bg, drift_tilt, mo, np):
    def _t_one_meter(coef, power):
        return (1.0 / coef) ** (1.0 / power) if coef > 0 else np.inf

    _t_a = _t_one_meter(0.5 * drift_ba.value, 2)
    _t_e = _t_one_meter(0.5 * G * drift_tilt.value * 1e-3, 2)
    _t_g = _t_one_meter(G * drift_bg.value / 6, 3)
    _fmt = lambda x: "never" if not np.isfinite(x) else f"{x:.1f} s"
    mo.md(
        f"With these settings, the drift laws predict 1 m of horizontal error after "
        f"{_fmt(_t_a)} from the accelerometer bias alone, {_fmt(_t_e)} from the tilt error alone, "
        f"and {_fmt(_t_g)} from the gyroscope bias alone. Notice that with all three on, the "
        f"accelerometer-bias and tilt terms have opposite signs, so the black curve can lie below "
        f"the individual curves: errors add as vectors, not as magnitudes."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
        attrs: {class: no-icon}
    The drift laws assume:

    1. **A motionless, level IMU.** During real motion the specific force is not $[0, 0, g]$ and the attitude changes, so the same errors project differently onto the axes. The mechanisms (and the powers of $t$) survive, but the coefficients change; [Chapter 21](ch21_zero_velocity_updates.md) gives the general equations.
    2. **Constant biases.** Real biases wander slowly (a random walk) and change with temperature. Over the short intervals that matter here (one stride), constant is a good approximation.
    3. **Small angles.** The $t^3$ law for a gyroscope bias needs $bt \ll 1$. With $b = 0.01$ rad/s, the tilt reaches $0.3$ rad after 30 s, and the simulated curve bends below the law, as the demo shows at long durations.
    4. **One source at a time.** Errors add as vectors and can partially cancel, as the leveling example showed. The laws give the size of each contribution, not the total.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Gait Cycle

    Walking is periodic, and clinicians describe one period of one leg with a fixed vocabulary of events [see @perry2024]. For the foot that carries our IMU, in order:

    - **Heel strike** (initial contact): the heel touches the ground.
    - **Foot flat:** the whole sole rests on the ground.
    - **Heel off:** the heel lifts as the body rolls forward over the forefoot.
    - **Toe off:** the toes leave the ground.
    - The foot then travels through the air until its next heel strike.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Stride**</u>

    For a given foot, the time interval from one heel strike of that foot to its next heel strike, together with the motion of the foot during that interval.
    ///

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Gait cycle**</u>

    The ordered sequence of events that one foot passes through during a stride (heel strike, foot flat, heel off, toe off, and the next heel strike), with the time of each event expressed as a percentage of the stride's duration, heel strike being $0\%$ and the next heel strike $100\%$.
    ///

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Stance phase**</u>

    The part of a stride during which the foot is in contact with the ground: from heel strike to toe off.
    ///

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Swing phase**</u>

    The part of a stride during which the foot is not in contact with the ground: from toe off to the next heel strike.
    ///

    The interval from a heel strike of one foot to the next heel strike of the *other* foot is called a *step*, so every stride contains two steps. At a comfortable walking speed, stance takes about $60\%$ of the gait cycle and swing about $40\%$. Within stance, foot flat lasts from roughly $10$–$15\%$ to $40$–$50\%$ of the cycle, and during that time the foot, and an IMU strapped to it, is **stationary**: its velocity and angular velocity are both zero. That happens once per stride, about once a second.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch20_gait_cycle.svg" class="graphic" alt="A timeline of one gait cycle from 0 to 100 percent. Stance phase occupies 0 to 60 percent and swing phase 60 to 100 percent. Events are marked at heel strike (0 percent), foot flat (15 percent), heel off (45 percent), toe off (60 percent), and the next heel strike (100 percent). The interval from foot flat to heel off is shaded and labeled as the stationary period." />
    """)
    return


@app.cell(hide_code=True)
def _(IMAGES_DIR, plt):
    # jb: include=false
    _fig, _ax = plt.subplots(figsize=(8, 2.8))
    _ax.broken_barh([(0, 60)], (0.6, 0.3), facecolors="C0", alpha=0.35)
    _ax.broken_barh([(60, 40)], (0.6, 0.3), facecolors="C1", alpha=0.35)
    _ax.text(30, 0.75, "stance phase (about 60%)", ha="center", va="center")
    _ax.text(80, 0.75, "swing phase (about 40%)", ha="center", va="center")
    _ax.broken_barh([(15, 30)], (0.2, 0.3), facecolors="0.85", edgecolor="0.3", hatch="//")
    _ax.text(30, 0.35, "foot flat: stationary", ha="center", va="center",
             bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
    for _x, _name in [(0, "heel strike"), (15, "foot flat"), (45, "heel off"), (60, "toe off"), (100, "heel strike")]:
        _ax.vlines(_x, 0.12, 0.95, color="black", lw=1)
        _ax.text(_x, 0.06, f"{_name}\n{_x}%", ha="center", va="top", fontsize=9)
    _ax.set_xlim(-8, 108)
    _ax.set_ylim(-0.45, 1.0)
    _ax.set_yticks([])
    _ax.set_xticks([])
    for _s in ["left", "right", "top", "bottom"]:
        _ax.spines[_s].set_visible(False)
    _ax.set_title("One gait cycle of the instrumented foot (simulator defaults)", style="italic")
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch20_gait_cycle.svg")
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A Synthetic Gait Simulator

    To test navigation algorithms we need IMU data *and* the exact trajectory that produced it. Real walking data comes with neither exact truth nor control over the error sources, so we build a simulator: an analytic trajectory of the foot, from which the true $\boldsymbol\omega^b$ and $\mathbf f^b$ follow by differentiation, plus the sensor errors of our IMU model. [Chapter 21](ch21_zero_velocity_updates.md) reuses it unchanged.

    The model describes the motion of the IMU, strapped to the top of the foot. Each stride has a stationary part (foot flat to heel off) and a **moving window** (heel off to the next foot flat) of duration $T_m$. Within a moving window we use the normalized time $\tau := (t - t_{\text{heel off}})/T_m \in [0, 1]$. All event times are rounded to whole samples.

    1. **Footprints.** During stance $i$ the IMU sits at position $\mathbf P_i$ with heading $\psi_i$, starting from $\mathbf P_0 = \mathbf 0$ and $\psi_0 = 0$ (facing East). Stride $i$ turns the foot by $\Delta\psi_i$ and raises it by $h_i$ (zero on level ground):
    $$\psi_{i+1} = \psi_i + \Delta\psi_i, \qquad \mathbf P_{i+1} = \mathbf P_i + \mathbf d_i, \qquad \mathbf d_i = [L\cos\chi_i,\ L\sin\chi_i,\ h_i]^\top, \qquad \chi_i = \psi_i + \tfrac12\Delta\psi_i,$$
    so the foot travels a horizontal distance $L$ along the average of its two headings.
    2. **Minimum-jerk profile.** Every transition uses
    $$s(\tau) = 10\tau^3 - 15\tau^4 + 6\tau^5, \qquad s'(\tau) = 30\tau^2(1-\tau)^2, \qquad s''(\tau) = 60\tau(1-\tau)(1-2\tau).$$
    It rises from $s(0) = 0$ to $s(1) = 1$, and its velocity and acceleration vanish at both ends, so the foot starts and stops smoothly. It is the unique polynomial of degree at most 5 with these six boundary values, and among all motions between two rest positions it minimizes the integrated squared jerk (the third derivative), as @flash1985 showed for reaching movements.
    3. **Position.** $\ \mathbf p(\tau) = \mathbf P_i + s(\tau)\,\mathbf d_i + h_c\,c(\tau)\,\mathbf e_z$, where $c(\tau) = 256\,\tau^4(1-\tau)^4$ is a clearance bump of height $1$ at $\tau = \tfrac12$ and $h_c$ is the peak clearance.[^bump]
    4. **Heading and pitch.** $\ \psi(\tau) = \psi_i + s(\tau)\,\Delta\psi_i$. The pitch must be toe-down ($\theta > 0$) around toe off and toe-up around heel strike. We use
    $$\theta(\tau) = A\,\tau^3(1-\tau)^4 + B\,\tau^4(1-\tau)^3,$$
    whose value and first two derivatives vanish at both ends, and choose $A, B$ so that $\theta(\tau_{\text{toe off}}) = \theta_{\text{toe off}}$ and $\theta(\tau_{\text{heel strike}}) = \theta_{\text{heel strike}}$: two linear equations in two unknowns. Roll is zero.
    5. **Derivatives.** By the chain rule, $\dot{\mathbf p} = \mathbf p'(\tau)/T_m$ and $\ddot{\mathbf p} = \mathbf p''(\tau)/T_m^2$, and likewise for $\psi$ and $\theta$. The attitude is $\mathbf R = \mathbf R_z(\psi)\mathbf R_y(\theta)$, the true specific force is $\mathbf f^b = \mathbf R^\top(\ddot{\mathbf p} - \mathbf g^n)$, and the true body rate follows from the lemma below.
    6. **Sensor errors.** Each bias component is the default magnitude with a random sign; white noise is added to every sample, exactly as in the IMU model.

    The defaults describe a comfortable walk: stride time $T = 1.1$ s, stride length $L = 1.4$ m (a gait speed of $1.27$ m/s), stance $60\%$, foot flat $30\%$ of the cycle (so $T_m = 0.77$ s), clearance $h_c = 0.12$ m, and pitch $0.5$ rad toe-down at toe off and $-0.35$ rad toe-up at heel strike.

    [^bump]: The simpler bump $64\tau^3(1-\tau)^3$ looks almost the same, but its jerk is $+384$ at $\tau = 0$ and $-384$ at $\tau = 1$. The error of the trapezoidal rule over a smooth stretch is proportional to the difference of the integrand's derivative at its two ends, so the integrated vertical velocity would end every stride a few millimeters per second off, a drift caused by the simulator rather than the sensors. The jerk of $256\tau^4(1-\tau)^4$ vanishes at both ends, and that of $s$ is the same ($60$) at both ends, so these error terms cancel.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// important | 📐 **Lemma (Body Rate of a Yawing, Pitching Foot)**
        attrs: {class: no-icon}
    If $\mathbf R(t) = \mathbf R_z(\psi(t))\,\mathbf R_y(\theta(t))$ with differentiable $\psi$ and $\theta$, then $\mathbf R^\top\dot{\mathbf R} = [\boldsymbol\omega]_\times$ with
    $$\boldsymbol\omega = \big[-\dot\psi\sin\theta,\ \ \dot\theta,\ \ \dot\psi\cos\theta\big]^\top.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    This is [Chapter 17](ch17_rotations.md)'s Euler-rate theorem with $\phi \equiv 0$; directly: by the product rule, $\mathbf R^\top\dot{\mathbf R} = \mathbf R_y^\top(\mathbf R_z^\top\dot{\mathbf R}_z)\mathbf R_y + \mathbf R_y^\top\dot{\mathbf R}_y = \dot\psi\,\mathbf R_y^\top[\mathbf e_z]_\times\mathbf R_y + \dot\theta\,[\mathbf e_y]_\times$, using Chapter 17's elementary rates $\mathbf R_z^\top\dot{\mathbf R}_z = \dot\psi[\mathbf e_z]_\times$ and $\mathbf R_y^\top\dot{\mathbf R}_y = \dot\theta[\mathbf e_y]_\times$. Chapter 17's identity $\mathbf Q^\top[\mathbf a]_\times\mathbf Q = [\mathbf Q^\top\mathbf a]_\times$ for a rotation matrix $\mathbf Q$ gives $\mathbf R_y^\top[\mathbf e_z]_\times\mathbf R_y = [\mathbf R_y^\top\mathbf e_z]_\times$, and $\mathbf R_y(\theta)^\top\mathbf e_z = [-\sin\theta, 0, \cos\theta]^\top$ (the third row of $\mathbf R_y$). Adding the two cross-product matrices gives the claim. $\blacksquare$
    ///

    The simulator returns a dictionary with the time stamps, the true trajectory and attitude, the true and measured IMU signals, the biases, the true stationary samples, the event times, and per-stride ground truth for [Chapter 21](ch21_zero_velocity_updates.md)'s gait parameters.
    """)
    return


@app.cell
def simulator(G_N, np):
    # jb: echo=true
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Our running example is a U-turn: ten straight strides East, four strides that each turn $45^\circ$ to the left, and ten straight strides back, with two seconds of standing before and one after. That is 24 strides in about 29 seconds.
    """)
    return


@app.cell
def _(np, simulate_gait):
    # jb: echo=true
    walk_turns = np.r_[np.zeros(10), np.full(4, np.pi / 4), np.zeros(10)]
    sim = simulate_gait(n_strides=24, turn_angles=walk_turns, seed=0)
    return sim, walk_turns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The figure shows three strides of the simulated foot. During each shaded foot-flat interval, every true signal is constant: zero velocity, zero angular rate, and specific force $[0, 0, g]$. The measured signals (blue) carry the biases and noise. Notice that the large specific forces come from the foot's own acceleration, up to about $2g$, and that the pitch rate peaks at about $6.5$ rad/s ($370^\circ$/s) in mid-swing, as the foot rotates from toe-down to toe-up.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch20_simulated_imu.svg" class="graphic" alt="Five stacked time plots over three simulated strides: forward position rising in steps, foot height with a 12 cm bump per stride, pitch angle going toe-down then toe-up, the y-axis gyroscope signal, and the x and z accelerometer signals. Foot-flat intervals are shaded; measured signals are noisy blue dots around black true curves." />
    """)
    return


@app.cell(hide_code=True)
def _(IMAGES_DIR, np, plt, sim):
    # jb: include=false
    _t = sim["t"]
    _k = (_t >= 1.6) & (_t <= 5.9)
    _fig, _axs = plt.subplots(5, 1, figsize=(8, 10), sharex=True)
    _panels = [
        (sim["p"][:, 0], None, "forward position $p_x$ (m)"),
        (sim["p"][:, 2], None, "height $p_z$ (m)"),
        (np.degrees(sim["pitch"]), None, "pitch $\\theta$ (deg)"),
        (sim["omega"][:, 1], sim["omega_m"][:, 1], "gyroscope $\\omega_y$ (rad/s)"),
    ]
    for _ax, (_true, _meas, _lab) in zip(_axs[:4], _panels):
        if _meas is not None:
            _ax.plot(_t[_k], _meas[_k], ".", color="C0", ms=2.5, label="measured")
        _ax.plot(_t[_k], _true[_k], color="black", lw=1.2, label="true")
        _ax.set_ylabel(_lab, fontsize=9)
    _axs[3].legend(fontsize=8, loc="upper right")
    _ax = _axs[4]
    _ax.plot(_t[_k], sim["f_m"][_k, 0], ".", color="C0", ms=2.5, label="measured $f_x$, $f_z$")
    _ax.plot(_t[_k], sim["f_m"][_k, 2], ".", color="C0", ms=2.5)
    _ax.plot(_t[_k], sim["f"][_k, 0], color="black", lw=1.2, label="true $f_x$")
    _ax.plot(_t[_k], sim["f"][_k, 2], color="black", lw=1.2, ls="--", label="true $f_z$")
    _ax.set_ylabel("specific force (m/s²)", fontsize=9)
    _ax.legend(fontsize=8, loc="upper right", ncol=3)
    _ax.set_xlabel("time (s)")
    for _ax in _axs:
        _ax.fill_between(_t[_k], 0, 1, where=sim["still"][_k], color="0.85", transform=_ax.get_xaxis_transform(), lw=0)
        for _te in sim["events"]["toe_off"]:
            if 1.6 <= _te <= 5.9:
                _ax.axvline(_te, color="C1", lw=0.8, ls=":")
        for _te in sim["events"]["heel_strike"]:
            if 1.6 <= _te <= 5.9:
                _ax.axvline(_te, color="C3", lw=0.8, ls="--")
        _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _axs[0].set_title("Three simulated strides (shaded: foot flat; dotted: toe off; dashed: heel strike)", style="italic", fontsize=10)
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch20_simulated_imu.svg")
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Validating the Simulator

    A simulator whose IMU signals were inconsistent with its trajectory (a sign error in $\omega_x$, say) would silently corrupt every later experiment. The test is to integrate its **noise-free, bias-free** IMU output with the strapdown mechanization, starting from the true initial state, and compare with the true trajectory. Agreement cannot be perfect, because the trapezoidal rule has an error proportional to $\Delta t^2$. So the test is that the discrepancy **shrinks by a factor of about four each time the sample rate doubles**. An inconsistent signal would leave an error that does not shrink.
    """)
    return


@app.cell(hide_code=True)
def _(np, simulate_gait, strapdown, walk_turns):
    # jb: include=false
    validation = {}
    for _fs in [100.0, 200.0, 400.0]:
        _s = simulate_gait(n_strides=24, turn_angles=walk_turns, fs=_fs, gyro_noise=0.0,
                           gyro_bias=0.0, accel_noise=0.0, accel_bias=0.0)
        _q, _v, _p = strapdown(_s["omega_m"], _s["f_m"], _s["dt"], _s["q"][0], _s["v"][0], _s["p"][0])
        validation[_fs] = dict(sim=_s, p=_p, err=np.linalg.norm(_p - _s["p"], axis=1))
    return (validation,)


@app.cell(hide_code=True)
def _(mo, validation):
    _rates = sorted(validation)
    _rows = []
    for _j, _fs in enumerate(_rates):
        _e = validation[_fs]["err"]
        _ratio = "" if _j == 0 else f"{validation[_rates[_j - 1]]['err'][-1] / _e[-1]:.1f}"
        _rows.append(f"| {_fs:.0f} Hz | {_e.max() * 100:.2f} cm | {_e[-1] * 100:.2f} cm | {_ratio} |")
    _walked = validation[100.0]["sim"]["stride_length"].sum()
    mo.md(
        "| Sample rate | Largest position error | Final position error | Reduction factor |\n"
        "|---|---|---|---|\n" + "\n".join(_rows) + "\n\n"
        f"Each doubling of the rate divides the error by about four, as second-order accuracy predicts, "
        f"so the simulated signals are consistent with the simulated trajectory. At 100 Hz the "
        f"integration error accumulated over the whole {_walked:.1f} m walk is "
        f"{validation[100.0]['err'][-1]:.2f} m. It accumulates because each stride leaves a velocity "
        f"error of a millimeter or two per second that is never removed. Sensor errors, as we will "
        f"see, produce hundreds of meters, and Chapter 21 removes the velocity error at every stance, "
        f"so integration error is not what limits us."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch20_strapdown_validation.svg" class="graphic" alt="Top view of the simulated U-turn walk. The true path (black) goes 14 m East, turns left in a half circle, and returns West about 3.7 m further North. The noise-free strapdown solution at 100 Hz (orange, dashed) lies on top of it." />
    """)
    return


@app.cell(hide_code=True)
def _(IMAGES_DIR, plt, validation):
    # jb: include=false
    _s, _p = validation[100.0]["sim"], validation[100.0]["p"]
    _fig, _ax = plt.subplots(figsize=(7, 3.6))
    _ax.plot(_s["p"][:, 0], _s["p"][:, 1], color="black", lw=2, label="true path")
    _ax.plot(_p[:, 0], _p[:, 1], color="C1", ls="--", lw=1.5, label="noise-free strapdown, 100 Hz")
    _ax.plot(_s["footprints"][:, 0], _s["footprints"][:, 1], "o", mfc="none", mec="black", ms=5, label="footprints (stance)")
    _ax.set_aspect("equal")
    _ax.set_xlabel("East (m)")
    _ax.set_ylabel("North (m)")
    _ax.set_title("Strapdown integration of the simulator's noise-free IMU output", style="italic")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.legend(fontsize=8, loc="center left")
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch20_strapdown_validation.svg")
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Detecting Zero Velocity

    The stationary moments are only useful if we can find them from the IMU data alone.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Zero-velocity detector**</u>

    A function that maps the IMU samples in a time window around sample $k$ to one of two decisions for sample $k$: *stationary* (the IMU's velocity and angular velocity are zero) or *moving*.
    ///

    A detector can err in two ways. A **missed detection** calls a stationary sample moving; it only wastes an opportunity. A **false detection** calls a moving sample stationary; [Chapter 21](ch21_zero_velocity_updates.md) will then tell the filter that a foot moving at several meters per second has zero velocity, which is far more harmful. All our detectors look at the $W = 5$ samples (50 ms) centered on $k$, which we call the window $\Omega_k$, and declare *stationary* when a test statistic $T(k)$ falls below a threshold $\gamma$.

    If the IMU is stationary throughout the window, then $\boldsymbol\omega = \mathbf 0$ and $\mathbf a^n = \mathbf 0$, so $\mathbf f = \mathbf R^\top[0, 0, g]^\top = g\,\mathbf u$, where $\mathbf u := \mathbf R^\top\mathbf e_z$ is the unit vector pointing up, expressed in body coordinates. It is unknown (it depends on how the foot is resting) but constant. Two simple detectors each test half of this:

    - **Acceleration magnitude:** $\ T_{\text{MAG}}(k) = \dfrac{1}{\sigma_a^2 W}\displaystyle\sum_{j\in\Omega_k}\big(\lVert\mathbf f_{m,j}\rVert - g\big)^2.$ Stationary implies $\lVert\mathbf f\rVert = g$, but not conversely: $\lVert\mathbf f\rVert = \lVert\mathbf a^n - \mathbf g^n\rVert = g$ holds for every acceleration on a sphere of radius $g$ around $\mathbf g^n$ (for instance, a foot decelerating forward while dropping), and a swinging foot passes through that sphere.
    - **Angular-rate energy:** $\ T_{\text{ARE}}(k) = \dfrac{1}{\sigma_g^2 W}\displaystyle\sum_{j\in\Omega_k}\lVert\boldsymbol\omega_{m,j}\rVert^2.$ Stationary implies $\boldsymbol\omega = \mathbf 0$, but a foot that translates without rotating passes this test too.

    The detector of @skog2010, called SHOE (stance hypothesis optimal detector), combines both conditions, and it is not an ad hoc combination: it is the generalized likelihood ratio test (GLRT) for "stationary" against "moving".
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// important | 📐 **Theorem (GLRT for a Stationary IMU)**
        attrs: {class: no-icon}
    Within the window $\Omega_k$, model the measurements as $\mathbf f_{m,j} = \boldsymbol\mu_j + \mathbf n_{a,j}$ and $\boldsymbol\omega_{m,j} = \boldsymbol\nu_j + \mathbf n_{g,j}$, with all noise vectors independent, $\mathbf n_{a,j} \sim \mathcal N(\mathbf 0, \sigma_a^2\mathbf I)$, $\mathbf n_{g,j} \sim \mathcal N(\mathbf 0, \sigma_g^2\mathbf I)$, and no biases. Consider the hypotheses

    - $H_0$ (stationary): $\boldsymbol\mu_j = g\,\mathbf u$ and $\boldsymbol\nu_j = \mathbf 0$ for all $j \in \Omega_k$, for some unknown unit vector $\mathbf u$;
    - $H_1$ (moving): $\boldsymbol\mu_j, \boldsymbol\nu_j \in \mathbb R^3$ arbitrary and unknown.

    Let $\bar{\mathbf f}_k$ be the mean of the $\mathbf f_{m,j}$ over the window, and assume $\bar{\mathbf f}_k \ne \mathbf 0$. Then the generalized likelihood ratio $L_k := \sup_{H_1}\ell \,/ \sup_{H_0}\ell$, where $\ell$ is the {term}`likelihood` of the $2W$ measured vectors and each supremum is over that hypothesis's unknowns, satisfies $\tfrac{2}{W}\ln L_k = T_{\text{SHOE}}(k)$ with
    $$T_{\text{SHOE}}(k) := \frac1W\sum_{j\in\Omega_k}\left(\frac{1}{\sigma_a^2}\Big\lVert\mathbf f_{m,j} - g\,\frac{\bar{\mathbf f}_k}{\lVert\bar{\mathbf f}_k\rVert}\Big\rVert^2 + \frac{1}{\sigma_g^2}\big\lVert\boldsymbol\omega_{m,j}\big\rVert^2\right).$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    A measurement $\mathbf y \sim \mathcal N(\boldsymbol\mu, \sigma^2\mathbf I)$ in $\mathbb R^3$ has density $(2\pi\sigma^2)^{-3/2}\exp\big(-\lVert\mathbf y - \boldsymbol\mu\rVert^2/(2\sigma^2)\big)$: the multivariate normal density of [Chapter 12](ch12_vectors_matrices_covariance.md) with determinant $\sigma^6$ and inverse covariance $\sigma^{-2}\mathbf I$. By independence, $\ell$ is the product of $2W$ such densities, so
    $$\ell = C\exp\Big(-\frac12\sum_{j\in\Omega_k}\Big(\frac{\lVert\mathbf f_{m,j} - \boldsymbol\mu_j\rVert^2}{\sigma_a^2} + \frac{\lVert\boldsymbol\omega_{m,j} - \boldsymbol\nu_j\rVert^2}{\sigma_g^2}\Big)\Big), \qquad C := (2\pi\sigma_a^2)^{-3W/2}(2\pi\sigma_g^2)^{-3W/2}.$$
    Under $H_1$, choosing $\boldsymbol\mu_j = \mathbf f_{m,j}$ and $\boldsymbol\nu_j = \boldsymbol\omega_{m,j}$ makes the exponent zero, its largest possible value, so $\sup_{H_1}\ell = C$. Under $H_0$, we must minimize $\sum_j\lVert\mathbf f_{m,j} - g\mathbf u\rVert^2$ over unit vectors $\mathbf u$. Expanding with $\lVert\mathbf u\rVert = 1$,
    $$\sum_{j}\lVert\mathbf f_{m,j} - g\mathbf u\rVert^2 = \sum_j\lVert\mathbf f_{m,j}\rVert^2 - 2gW\,\mathbf u\cdot\bar{\mathbf f}_k + Wg^2,$$
    which is smallest when $\mathbf u\cdot\bar{\mathbf f}_k$ is largest. By the Cauchy–Schwarz inequality ([Appendix D: Vectors](appendix_d_linear_algebra.md)), $\mathbf u\cdot\bar{\mathbf f}_k \le \lVert\bar{\mathbf f}_k\rVert$, with equality exactly for $\mathbf u = \bar{\mathbf f}_k/\lVert\bar{\mathbf f}_k\rVert$. Substituting this $\mathbf u$ gives $\sup_{H_0}\ell = C\exp\big(-\tfrac{W}{2}T_{\text{SHOE}}(k)\big)$, and dividing, $\ln L_k = \tfrac W2 T_{\text{SHOE}}(k)$. $\blacksquare$
    ///

    A GLRT rejects $H_0$ when the ratio is large, so SHOE declares the sample **stationary when $T_{\text{SHOE}}(k) < \gamma$**. The statistic is small only if the specific force has magnitude $g$ *and* a constant direction across the window, *and* the angular rate is near zero.

    How small is small? Under $H_0$, $W\,T_{\text{SHOE}}$ is a sum of squared standardized noise components: $3W$ from the gyroscope and $3W$ from the accelerometer, of which two are absorbed in fitting the direction $\mathbf u$. It is therefore approximately {term}`chi-squared <chi-squared distribution>` with $6W - 2$ degrees of freedom (exactly so in the limit of small noise; we confirmed it by simulation), so $T_{\text{SHOE}}$ averages $6 - 2/W = 5.6$ at rest. Biases, which the theorem ignores, add about $\lVert\mathbf b_g\rVert^2/\sigma_g^2 + (\mathbf b_a\cdot\mathbf u)^2/\sigma_a^2 \approx 4$ with our defaults. Real shoes also vibrate and creep, so practical thresholds sit far above these values and are tuned on recorded walks.
    """)
    return


@app.cell
def detectors(G, np):
    # jb: echo=true
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Evaluating the Detectors

    Because the simulator knows exactly when the foot is still, we can score each detector on the U-turn walk (with sensor errors). For each detector and threshold, the table lists the percentage of truly stationary samples it detects, the percentage of moving samples it falsely declares stationary, and the fastest true foot speed among the samples it declares stationary. Detection never reaches $100\%$ at small $\gamma$, because windows at the edges of each foot-flat interval contain some motion.
    """)
    return


@app.cell(hide_code=True)
def _(np, sim, stat_are, stat_mag, stat_shoe):
    # jb: include=false
    detector_stats = {
        "SHOE": stat_shoe(sim["f_m"], sim["omega_m"]),
        "acceleration magnitude": stat_mag(sim["f_m"], sim["omega_m"]),
        "angular-rate energy": stat_are(sim["f_m"], sim["omega_m"]),
    }
    true_speed = np.linalg.norm(sim["v"], axis=1)

    def score_detector(stat, gamma):
        """Percent detected, percent false, max true speed among declared-stationary samples."""
        decided = stat < gamma
        still = sim["still"]
        return (100 * decided[still].mean(), 100 * decided[~still].mean(),
                true_speed[decided].max() if decided.any() else 0.0)

    return detector_stats, score_detector, true_speed


@app.cell(hide_code=True)
def _(detector_stats, mo, np, score_detector, sim):
    _rows = []
    for _name, _stat in detector_stats.items():
        for _gamma in [30, 300, 3000]:
            _det, _false, _vmax = score_detector(_stat, _gamma)
            _rows.append(f"| {_name} | {_gamma} | {_det:.1f}% | {_false:.2f}% | {_vmax:.2f} m/s |")
    _shoe_still = detector_stats["SHOE"][sim["still"]]
    _shoe_moving = detector_stats["SHOE"][~sim["still"]]
    mo.md(
        "| Detector | $\\gamma$ | Stationary samples detected | Moving samples flagged | Fastest flagged speed |\n"
        "|---|---|---|---|---|\n" + "\n".join(_rows) + "\n\n"
        f"On this walk the SHOE statistic has median {np.median(_shoe_still):.1f} on stationary samples "
        f"and never falls below {_shoe_moving.min():.0f} on moving ones, a gap of more than two orders "
        f"of magnitude. The acceleration-magnitude test, by contrast, starts declaring mid-swing samples "
        f"stationary at moderate thresholds, with the foot moving at over 3 m/s. We use SHOE with "
        f"threshold 1000 from here on."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Interactive: Detector Explorer

    Choose a detector and move the threshold. The top panel shows the statistic (log scale) over five strides, the threshold $\gamma$ (dashed), the true foot-flat intervals (gray), and the samples declared stationary (orange band). The bottom panel shows the true foot speed; red crosses mark false detections, moving samples declared stationary.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    det_choice = mo.ui.dropdown(
        options=["SHOE", "acceleration magnitude", "angular-rate energy"], value="SHOE", label="detector"
    )
    det_log_gamma = mo.ui.slider(0.5, 5.5, 0.1, value=3.0, label=r"$\log_{10}\gamma$", show_value=True)
    return det_choice, det_log_gamma


@app.cell(hide_code=True)
def _(
    det_choice,
    det_log_gamma,
    detector_stats,
    graphic,
    mo,
    np,
    plt,
    sim,
    true_speed,
):
    _stat = detector_stats[det_choice.value]
    _gamma = 10 ** det_log_gamma.value
    _t = sim["t"]
    _k = (_t >= 1.5) & (_t <= 7.6)
    _decided = _stat < _gamma
    _fig, (_a0, _a1) = plt.subplots(2, 1, figsize=(8, 5.2), sharex=True, height_ratios=[1.6, 1])
    for _ax in (_a0, _a1):
        _ax.fill_between(_t[_k], 0, 1, where=sim["still"][_k], color="0.85", lw=0,
                         transform=_ax.get_xaxis_transform(), label="true foot flat")
        _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _a0.semilogy(_t[_k], np.maximum(_stat[_k], 1e-2), color="C0", lw=1.2, label=f"{det_choice.value} statistic")
    _a0.axhline(_gamma, color="black", ls="--", lw=1, label=r"threshold $\gamma$")
    _a0.fill_between(_t[_k], 0.92, 1.0, where=_decided[_k], color="C1", lw=0,
                     transform=_a0.get_xaxis_transform(), label="declared stationary")
    _a0.set_ylim(1e-1, 1e7)
    _a0.set_ylabel("statistic")
    _a0.legend(fontsize=7.5, loc="lower right", ncol=2)
    _a0.set_title(f"{det_choice.value} detector, $\\gamma = 10^{{{det_log_gamma.value:.1f}}}$", style="italic")
    _a1.plot(_t[_k], true_speed[_k], color="black", lw=1.2, label="true speed")
    _false = _decided & ~sim["still"] & _k
    _a1.plot(_t[_false], true_speed[_false], "x", color="red", ms=5, label="false detection")
    _a1.set_ylabel("speed (m/s)")
    _a1.set_xlabel("time (s)")
    _a1.legend(fontsize=7.5, loc="upper right")
    _fig.tight_layout()
    mo.vstack([mo.hstack([det_choice, det_log_gamma], justify="start"), graphic(_fig)])
    return


@app.cell(hide_code=True)
def _(det_choice, det_log_gamma, detector_stats, mo, score_detector):
    _det, _false, _vmax = score_detector(detector_stats[det_choice.value], 10 ** det_log_gamma.value)
    mo.md(
        f"Over the whole 29 s walk, this setting detects {_det:.1f}% of the stationary samples and "
        f"declares {_false:.2f}% of the moving samples stationary; the fastest of those was moving at "
        f"{_vmax:.2f} m/s."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
        attrs: {class: no-icon}
    The detectors assume:

    1. **A foot that is truly still for at least a window.** In running, foot flat can last only a few samples, and every window that covers it also covers motion; the statistic never drops below the walking threshold, and stances are missed. Raising $\gamma$ to catch them invites false detections. [Chapter 21](ch21_zero_velocity_updates.md) shows the consequences.
    2. **A threshold matched to the motion.** A threshold tuned for walking is wrong for running, shuffling, or standing while swaying. Adaptive thresholds and motion classification are active research topics.
    3. **White, Gaussian, bias-free noise.** Biases inflate the statistic at rest (here by about 4). Vibration from footwear or the ground looks like motion.
    4. **A stationary ground.** In an elevator or a moving train, a foot can be still relative to the floor while moving relative to the Earth. All three detectors will declare it stationary, and a zero-velocity measurement will then be false.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Dead Reckoning a Walking Foot

    We now have everything needed to try pure dead reckoning on the U-turn walk with realistic sensor errors: level with the first second of standing, set $\psi = 0$, $\hat{\mathbf v} = \hat{\mathbf p} = \mathbf 0$, and run the mechanization. As a first attempt to use the stationary moments, we also try the crudest possible fix: whenever SHOE declares a sample stationary, overwrite the computed velocity with zero.
    """)
    return


@app.cell
def _(G_N, np, quat_exp, quat_mult, quat_to_rotmat):
    # jb: echo=true
    def strapdown_with_reset(omega_m, f_m, dt, q0, stationary):
        """Strapdown mechanization that sets the velocity to zero at every stationary sample."""
        N = len(omega_m)
        q, v, p = q0.copy(), np.zeros(3), np.zeros(3)
        positions = np.zeros((N, 3))
        a_prev = quat_to_rotmat(q) @ f_m[0] + G_N
        for k in range(1, N):
            q = quat_mult(q, quat_exp(0.5 * (omega_m[k - 1] + omega_m[k]) * dt))
            q /= np.linalg.norm(q)
            a_k = quat_to_rotmat(q) @ f_m[k] + G_N
            v_new = v + 0.5 * (a_prev + a_k) * dt
            p = p + 0.5 * (v + v_new) * dt
            v = np.zeros(3) if stationary[k] else v_new
            a_prev = a_k
            positions[k] = p
        return positions

    return (strapdown_with_reset,)


@app.cell(hide_code=True)
def _(align_level, detector_stats, np, sim, strapdown, strapdown_with_reset):
    # jb: include=false
    _q0 = align_level(sim["f_m"][:100])
    _, _, dr_free = strapdown(sim["omega_m"], sim["f_m"], sim["dt"], _q0, np.zeros(3), np.zeros(3))
    dr_reset = strapdown_with_reset(sim["omega_m"], sim["f_m"], sim["dt"], _q0, detector_stats["SHOE"] < 1000)
    dr_err_free = np.linalg.norm(dr_free - sim["p"], axis=1)
    dr_err_reset = np.linalg.norm(dr_reset - sim["p"], axis=1)
    return dr_err_free, dr_err_reset, dr_free, dr_reset


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch20_dead_reckoning.svg" class="graphic" alt="Left: top view of the U-turn walk. The true path (black) and the velocity-reset solution (orange) stay within a few meters of each other, while the free strapdown solution (red) leaves the plot within seconds. Right: position error versus time on a logarithmic scale; the free solution's error grows past 100 meters while the reset solution's error stays at meters." />
    """)
    return


@app.cell(hide_code=True)
def _(
    IMAGES_DIR,
    dr_err_free,
    dr_err_reset,
    dr_free,
    dr_reset,
    np,
    plt,
    sim,
):
    # jb: include=false
    _t = sim["t"]
    _fig, (_a0, _a1) = plt.subplots(1, 2, figsize=(10, 4))
    _a0.plot(sim["p"][:, 0], sim["p"][:, 1], color="black", lw=2, label="true path")
    _a0.plot(dr_free[:, 0], dr_free[:, 1], color="C3", lw=1.2, label="free strapdown")
    _a0.plot(dr_reset[:, 0], dr_reset[:, 1], color="C1", lw=1.2, label="velocity reset")
    _a0.set_xlim(-4, 20)
    _a0.set_ylim(-8, 12)
    _a0.set_aspect("equal")
    _a0.set_xlabel("East (m)")
    _a0.set_ylabel("North (m)")
    _a0.legend(fontsize=8, loc="upper right")
    _a0.set_title("Top view", style="italic")
    _m = _t > 0.05
    _a1.semilogy(_t[_m], dr_err_free[_m], color="C3", label="free strapdown")
    _a1.semilogy(_t[_m], dr_err_reset[_m], color="C1", label="velocity reset")
    _bgh = np.hypot(sim["b_g"][0], sim["b_g"][1])
    _tt = np.linspace(0.3, _t[-1], 100)
    _a1.semilogy(_tt, 9.81 * _bgh * _tt**3 / 6, color="gray", ls=":",
                 label=r"drift law $\frac{1}{6}\,g\,|b_{g,h}|\,t^3$")
    _a1.set_xlabel("time (s)")
    _a1.set_ylabel("position error (m)")
    _a1.set_ylim(1e-3, 1e4)
    _a1.legend(fontsize=8, loc="lower right")
    _a1.set_title("Position error", style="italic")
    for _ax in (_a0, _a1):
        _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch20_dead_reckoning.svg")
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(dr_err_free, dr_err_reset, mo, np, sim):
    _walked = sim["stride_length"].sum()
    mo.md(
        f"After the {sim['t'][-1]:.0f} s walk of {_walked:.1f} m, free strapdown navigation is "
        f"{dr_err_free[-1]:.0f} m from the truth. Until the U-turn its error follows the gyroscope-bias "
        f"drift law (dotted) for the horizontal part of the bias, of magnitude "
        f"{np.hypot(sim['b_g'][0], sim['b_g'][1]):.3f} rad/s; after the turn the foot faces the other "
        f"way, the same body-frame bias tilts the attitude the other way, and the growth slows. "
        f"Resetting the velocity at every detected "
        f"stance reduces the final error to {dr_err_reset[-1]:.1f} m: a huge improvement, but still "
        f"far from useful for measuring strides of 1.4 m."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The velocity reset fails for three reasons, and each points to what a better method must do:

    1. **The causes survive.** Resetting $\hat{\mathbf v}$ removes a symptom. The gyroscope bias keeps tilting the computed attitude, so each swing integrates a larger false acceleration than the last.
    2. **The damage is already done.** By the time the foot lands, the velocity error accumulated during the swing has already been integrated into the position. Zeroing the velocity does not undo it.
    3. **Heading is never corrected.** The vertical gyroscope bias turns the computed heading steadily, which bends the whole path; a velocity reset carries no information about heading at all.

    A Kalman filter fixes the first two. It treats "velocity is zero" as a measurement, and because its covariance matrix records how velocity errors were caused by attitude and bias errors (and how they leaked into position), a single measurement of the velocity error corrects all of them. The third is a question of observability, and its answer is less comforting.

    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    The stationary moments carry information about every error that produced the velocity error, not just the velocity error itself. Extracting that information requires a model of how errors propagate, which is exactly what a Kalman filter provides.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - **Strapdown inertial navigation** integrates $\dot q = \tfrac12 q\otimes[0, \boldsymbol\omega]$, $\dot{\mathbf v} = \mathbf R\mathbf f + \mathbf g^n$, $\dot{\mathbf p} = \mathbf v$ with measured rates and forces. At 100 Hz we use the exact quaternion update for the averaged rate, the trapezoidal rule for velocity and position, and leveling for the initial roll and pitch.
    - Integration turns constant sensor errors into **drift**: $\tfrac12 b_a t^2$ from an accelerometer bias, $\tfrac12 g\varepsilon t^2$ from a tilt error, and $\tfrac16 g b_g t^3$ from a gyroscope bias, plus slower random walks from noise. A consumer IMU is accurate to centimeters for about a second and off by tens of meters after ten.
    - In the **gait cycle**, stance takes about $60\%$ and swing about $40\%$; during foot flat the foot is stationary once per **stride**.
    - Our **gait simulator** produces exact ground truth from an analytic foot trajectory. Its noise-free output, integrated by the mechanization, reproduces the trajectory with an error that shrinks as $\Delta t^2$.
    - **Zero-velocity detectors** find the stationary moments. The acceleration-magnitude and angular-rate tests each check half of the stationary condition; SHOE, the GLRT, checks both and separates stance from swing by orders of magnitude on our data.
    - Free dead reckoning diverges to hundreds of meters in half a minute, and simply resetting the velocity at each stance still leaves meters of error.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What's Next

    [Chapter 21](ch21_zero_velocity_updates.md) treats "the foot is stationary" as a measurement of the velocity, $\mathbf v = \mathbf 0$, and feeds it to an error-state extended Kalman filter with fifteen states: errors in position, velocity, attitude, and both sensor biases. We derive how those errors propagate, see which ones the zero-velocity measurements can and cannot correct, and finally turn the corrected trajectory into the numbers a clinician wants: stride length, stride time, cadence, gait speed, foot clearance, and turning angle.
    """)
    return


if __name__ == "__main__":
    app.run()
