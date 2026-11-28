# /// script
# dependencies = [
#     "marimo>=0.25.1",
#     "matplotlib==3.11.2",
#     "numpy==2.5.3",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="19. Attitude and Heading Reference Systems", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "Fusing Gyroscopes, Accelerometers, and Magnetometers"
    short_title: "19. AHRS"
    description: "Fusing a drifting gyroscope with an accelerometer and a magnetometer to estimate attitude, with complementary and error-state Kalman filters."
    label: ch19
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


@app.cell
def rotation_helpers(np):
    # jb: include=false
    # Rotation and quaternion helpers from Chapters 17 and 18 (notebooks are self-contained).
    def skew(a):
        return np.array([[0.0, -a[2], a[1]], [a[2], 0.0, -a[0]], [-a[1], a[0], 0.0]])

    def rot_x(phi):
        c, s = np.cos(phi), np.sin(phi)
        return np.array([[1.0, 0.0, 0.0], [0.0, c, -s], [0.0, s, c]])

    def rot_y(theta):
        c, s = np.cos(theta), np.sin(theta)
        return np.array([[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]])

    def rot_z(psi):
        c, s = np.cos(psi), np.sin(psi)
        return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])

    def euler_to_R(phi, theta, psi):
        return rot_z(psi) @ rot_y(theta) @ rot_x(phi)

    def Exp(theta_vec):
        angle = np.sqrt(theta_vec @ theta_vec)
        if angle < 1e-12:
            return np.eye(3) + skew(theta_vec)
        K = skew(theta_vec / angle)
        return np.eye(3) + np.sin(angle) * K + (1.0 - np.cos(angle)) * K @ K

    def Log(R):
        cos_angle = np.clip((np.trace(R) - 1.0) / 2.0, -1.0, 1.0)
        angle = np.arccos(cos_angle)
        vee = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]])
        if angle < 1e-8:
            return 0.5 * vee
        return angle / (2.0 * np.sin(angle)) * vee

    def qmul(p, q):
        pw, px, py, pz = p
        qw, qx, qy, qz = q
        return np.array([pw * qw - px * qx - py * qy - pz * qz,
                         pw * qx + px * qw + py * qz - pz * qy,
                         pw * qy - px * qz + py * qw + pz * qx,
                         pw * qz + px * qy - py * qx + pz * qw])

    def q_to_R(q):
        w, x, y, z = q
        return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
                         [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
                         [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)]])

    def q_exp(theta_vec):
        angle = np.sqrt(theta_vec @ theta_vec)
        if angle < 1e-12:
            return np.array([1.0, *(0.5 * theta_vec)])
        return np.array([np.cos(angle / 2), *(np.sin(angle / 2) / angle * theta_vec)])

    def euler_to_q(phi, theta, psi):
        cf, sf = np.cos(phi / 2), np.sin(phi / 2)
        ct, st = np.cos(theta / 2), np.sin(theta / 2)
        cp, sp = np.cos(psi / 2), np.sin(psi / 2)
        return np.array([cf * ct * cp + sf * st * sp, sf * ct * cp - cf * st * sp,
                         cf * st * cp + sf * ct * sp, cf * ct * sp - sf * st * cp])

    def qmul_arr(P, Q):
        """Row-wise Hamilton product of (N, 4) arrays."""
        pw, px, py, pz = P.T
        qw, qx, qy, qz = Q.T
        return np.column_stack([pw * qw - px * qx - py * qy - pz * qz,
                                pw * qx + px * qw + py * qz - pz * qy,
                                pw * qy - px * qz + py * qw + pz * qx,
                                pw * qz + px * qy - py * qx + pz * qw])

    return Exp, Log, euler_to_R, euler_to_q, q_exp, q_to_R, qmul, qmul_arr, rot_x, rot_y, skew


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [Chapter 18](#ch18-thm-exact-quaternion-update) integrates *perfect* gyroscope readings exactly. Real readings are not perfect: a gyroscope bias of just $0.01$ rad/s, typical of inexpensive MEMS sensors, makes the integrated attitude $34^\circ$ wrong after one minute. Two other sensors see directions that do not drift: an accelerometer at rest measures gravity, which fixes "down", and a magnetometer measures the Earth's magnetic field, which fixes "north". Both are noisy, and both are corrupted when the body accelerates or a magnetic object comes near. An **attitude and heading reference system** (AHRS) fuses the three into one attitude estimate. This chapter builds two: a *complementary filter*, which turns out to be exactly the Introduction's alpha filter, and an *error-state Kalman filter* that also estimates the gyroscope bias and reports its own uncertainty. The same attitude machinery is the core of the inertial navigation in Chapters 20 and 21.

    /// attention | 🗝️ **Key Idea**
    Gyroscopes are accurate over short times but drift; gravity and the magnetic field are accurate over long times but noisy and easily disturbed. Fusing them means trusting the gyroscope for fast changes and the reference directions for slow ones.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// important | 🔗 **Prerequisites**
    - [Introduction](#intro): [the alpha filter](#intro-sec-predicting-the-change) $\hat x_k = \hat x_k^- + \alpha(z_k - \hat x_k^-)$ with prediction $\hat x_k^- = \hat x_{k-1} + \Delta x_k$ and [first-measurement initialization](#intro-sec-initialization).
    - [Chapter 6](#ch6): [variance of sums of independent random variables](#ch6-thm-variance-of-a-linear-combination), and [the steady-state variance](#ch6-thm-ema-of-a-constant-value) $\sigma^2\alpha/(2-\alpha)$ of an exponential moving average.
    - [Chapter 9](#ch9): {term}`white noise`, {term}`random walks <random walk>`, and the theorem that [the steady-state Kalman filter is an exponential moving average](#ch9-thm-the-steady-state-kalman-filter-is-an-ema).
    - [Chapter 11](#ch11): [sensor bias](#ch11-sec-sensor-bias-and-a-drifting-tare) and [calibration](#ch11-sec-calibration-by-least-squares).
    - [Chapters 13](#ch13), [14](#ch14), and [15](#ch15): [the Kalman filter equations](#ch13-sec-the-algorithm), the {term}`Joseph form`, [sequential updates](#ch14-sec-sequential-updates), {term}`gating`, and [the extended Kalman filter with its Jacobians](#ch15-sec-the-extended-kalman-filter).
    - [Chapter 17](#ch17): [ENU/FLU frames](#ch17-sec-reference-frames), [rotation matrices and their properties](#ch17-thm-properties-of-rotation-matrices), [ZYX Euler angles](#ch17-sec-elementary-rotations-and-euler-angles), [angular velocity](#ch17-sec-angular-velocity), $\operatorname{Exp}$ and $\operatorname{Log}$, [the small-angle approximation](#ch17-thm-small-angle-approximation), and the error-state convention $\mathbf R = \hat{\mathbf R}\operatorname{Exp}(\delta\boldsymbol\theta)$.
    - [Chapter 18](#ch18): {term}`unit quaternions <unit quaternion>`, [the exact update](#ch18-thm-exact-quaternion-update) $q_k = q_{k-1}\otimes\operatorname{Exp}_q(\boldsymbol\omega_k\Delta t)$, and $\operatorname{Exp}_q(\delta\boldsymbol\theta) \approx [1, \tfrac12\delta\boldsymbol\theta]$.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch19-sec-inertial-sensors-and-their-models -->
    ## Inertial Sensors and Their Models

    Phones, drones, game controllers, and gait sensors all carry the same trio of tiny MEMS sensors. We define each by what it measures.

    /// note | 📖 **Definition**
    <u>**Gyroscope**</u>

    A gyroscope is a sensor that measures the angular velocity of the body it is attached to, relative to non-rotating space, about one or more axes fixed in the body.
    ///

    Because we treat the navigation frame as non-rotating ([Chapter 17](#ch17-sec-reference-frames)), a three-axis gyroscope measures $\boldsymbol\omega^b$, the angular velocity of $b$ relative to $n$ in body coordinates.

    An accelerometer does *not* measure acceleration. Inside a MEMS accelerometer, a tiny proof mass $m$ hangs on springs in a case fixed to the body, and the sensor reports the spring force per unit mass along its axes. Once the mass has settled it moves with the case, with acceleration $\mathbf a^n$, so Newton's second law in the (non-rotating) navigation frame reads $m\mathbf a^n = \mathbf F_{\text{spring}} + m\mathbf g^n$. The sensor therefore reports $\mathbf F_{\text{spring}}/m = \mathbf a^n - \mathbf g^n$, in body axes.

    /// note | 📖 **Definition**
    <u>**Specific force**</u>

    The specific force on a body is $\mathbf f := \mathbf a - \mathbf g$, its acceleration relative to non-rotating space minus the gravitational acceleration; equivalently, the non-gravitational force acting on it per unit mass. In body coordinates,
    $$\mathbf f^b = (\mathbf R^n_b)^\top(\mathbf a^n - \mathbf g^n).$$
    ///

    Two examples fix the sign. A body at rest and level has $\mathbf a^n = \mathbf 0$ and $\mathbf R^n_b = \mathbf I$, so $\mathbf f^b = -\mathbf g^n = [0, 0, +g]^\top$: the floor pushes up. A body in free fall has $\mathbf a^n = \mathbf g^n$ and $\mathbf f^b = \mathbf 0$.

    /// note | 📖 **Definition**
    <u>**Accelerometer**</u>

    An accelerometer is a sensor that measures specific force along one or more axes fixed in the body.
    ///

    /// note | 📖 **Definition**
    <u>**Inertial measurement unit**</u>

    An inertial measurement unit (IMU) is a device, rigidly attached to a body, that measures at regular sample times the body's angular velocity $\boldsymbol\omega^b$ and specific force $\mathbf f^b$ along three perpendicular body-fixed axes; that is, a three-axis gyroscope and a three-axis accelerometer.
    ///

    /// note | 📖 **Definition**
    <u>**Magnetometer**</u>

    A magnetometer is a sensor that measures the local magnetic field vector along one or more axes fixed in the body.
    ///

    Many products sold as "9-axis IMUs" add a three-axis magnetometer, though a magnetometer is not an inertial sensor.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch19-sec-measurement-models -->
    ### Measurement Models

    We model the three sensors as in the book-wide conventions:
    $$\boldsymbol\omega_m = \boldsymbol\omega^b + \mathbf b_g + \mathbf n_g,\qquad \mathbf f_m = \mathbf f^b + \mathbf b_a + \mathbf n_a,\qquad \mathbf m_m = (\mathbf R^n_b)^\top\mathbf m^n + \mathbf n_m,$$
    where $\mathbf b_g$ and $\mathbf b_a$ are {term}`sensor biases <sensor bias>` (constant, or a slow {term}`random walk`), $\mathbf n_g$, $\mathbf n_a$, $\mathbf n_m$ are zero-mean Gaussian {term}`white noise` with independent components, and $\mathbf m^n = [0, 22, -42]^\top\ \mu\text{T}$ is the Earth's field in the navigation frame: it points north and steeply down, as at mid-northern latitudes. The default parameters, typical of a consumer MEMS IMU, are

    | quantity | value |
    |:---|:---|
    | sample rate | 100 Hz ($\Delta t = 0.01$ s) |
    | gyroscope noise $\sigma_g$ / bias | 0.01 rad/s / 0.01 rad/s per axis |
    | accelerometer noise $\sigma_a$ / bias | 0.05 m/s$^2$ / 0.05 m/s$^2$ per axis |
    | magnetometer noise $\sigma_m$ | 0.5 $\mu$T per axis |
    | gravity $\mathbf g^n$ | $[0, 0, -9.81]^\top$ m/s$^2$ |

    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **Calibrated, aligned sensors.** We assume scale factors are calibrated and that the three sensors' axes coincide with the body axes and with each other ([Chapter 11](#ch11-sec-calibration-by-least-squares)). Misalignment of $1^\circ$ turns a fast rotation about one axis into a false rate about another.
    - **Earth rotation is neglected.** The Earth turns at $7.3\times 10^{-5}$ rad/s, far below the assumed gyroscope bias. Navigation-grade gyroscopes are good enough to sense it, and then it must be modeled.
    - **Magnetic north.** $\mathbf m^n$ has no East component, so "North" here means *magnetic* north. Geographic north differs by the local magnetic declination, a known correction of a few degrees in most places.
    - **A clean magnetic field.** The model assumes the magnetometer sees only the Earth's field. Iron fixed to the body (*hard-iron* offsets and *soft-iron* distortions) must be calibrated out, and iron near the body (steel furniture, reinforced floors, electronics) changes $\mathbf m^n$ itself, often by tens of percent indoors.
    - **Saturation.** Consumer gyroscopes typically saturate at 2000$^\circ$/s and accelerometers at a few $g$; a foot strike can exceed the latter.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ```python
    FS = 100.0                              # sample rate (Hz)
    DT = 1.0 / FS                           # sample period (s)
    GRAVITY = 9.81                          # m/s^2
    G_N = np.array([0.0, 0.0, -GRAVITY])    # gravity in ENU
    M_N = np.array([0.0, 22.0, -42.0])      # Earth's field in ENU (uT)
    SIGMA_G, GYRO_BIAS = 0.01, 0.01         # rad/s
    SIGMA_A, ACCEL_BIAS = 0.05, 0.05        # m/s^2
    SIGMA_M = 0.5                           # uT
    ```
    """)
    return


@app.cell
def imu_parameters(np):
    # jb: include=false
    FS = 100.0                              # sample rate (Hz)
    DT = 1.0 / FS                           # sample period (s)
    GRAVITY = 9.81                          # m/s^2
    G_N = np.array([0.0, 0.0, -GRAVITY])    # gravity in ENU
    M_N = np.array([0.0, 22.0, -42.0])      # Earth's field in ENU (uT)
    SIGMA_G, GYRO_BIAS = 0.01, 0.01         # rad/s
    SIGMA_A, ACCEL_BIAS = 0.05, 0.05        # m/s^2
    SIGMA_M = 0.5                           # uT
    return ACCEL_BIAS, DT, GRAVITY, G_N, M_N, SIGMA_A, SIGMA_G, SIGMA_M


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch19-sec-attitude-and-heading -->
    ### Attitude and Heading

    /// note | 📖 **Definition**
    <u>**Attitude**</u>

    The attitude of a body is the orientation of its body frame relative to the navigation frame, that is, the rotation matrix $\mathbf R^n_b$ (equivalently, the pair of unit quaternions $\pm q^n_b$, or Euler angles away from gimbal lock).
    ///

    /// note | 📖 **Definition**
    <u>**Heading**</u>

    The heading of a body whose forward axis is not vertical is its yaw angle $\psi$: the angle, measured counterclockwise about Up, from East to the horizontal projection of the body's forward axis.
    ///

    The horizontal projection of the forward axis is the first column of $\mathbf R^n_b$ with its third entry dropped, $\cos\theta\,[\cos\psi, \sin\psi]$ ([Chapter 17](#ch17-thm-euler-angles-from-a-rotation-matrix), Euler-angle theorem), so for $|\theta| < 90^\circ$ its direction is exactly $\psi$. A compass bearing (clockwise from North) is $90^\circ - \psi$, modulo $360^\circ$. Roll and pitch together are called *tilt*: they say which way is down in body coordinates.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch19-sec-tilt-from-the-accelerometer -->
    ## Tilt from the Accelerometer

    At rest, $\mathbf a^n = \mathbf 0$ and the accelerometer measures $\mathbf f^b = (\mathbf R^n_b)^\top[0, 0, g]^\top$, which is $g$ times the third row of $\mathbf R^n_b$. Chapter 17's Euler-angle theorem gives that row, so
    $$\mathbf f^b = g\,\big[-\sin\theta,\ \cos\theta\sin\phi,\ \cos\theta\cos\phi\big]^\top.$$

    /// admonition | 📐 **Theorem (Tilt from Gravity)**
        attrs: {class: theorem, id: ch19-thm-tilt-from-gravity}
    If the body is not accelerating and the accelerometer is error-free, then for $|\theta| < 90^\circ$
    $$\phi = \operatorname{atan2}(f_y, f_z),\qquad \theta = \operatorname{atan2}\Big(-f_x,\ \sqrt{f_y^2 + f_z^2}\Big).$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    With $c := g\cos\theta > 0$, the formula above says $(f_z, f_y) = c(\cos\phi, \sin\phi)$, which is the definition of $\phi = \operatorname{atan2}(f_y, f_z)$. Also $\sqrt{f_y^2 + f_z^2} = c = g\cos\theta$ and $-f_x = g\sin\theta$, so $(\sqrt{f_y^2 + f_z^2}, -f_x) = g(\cos\theta, \sin\theta)$ and $\theta = \operatorname{atan2}(-f_x, \sqrt{f_y^2 + f_z^2}) \in (-\tfrac\pi2, \tfrac\pi2)$. $\blacksquare$
    ///

    Gravity cannot reveal the heading: turning the body about Up by any angle $\gamma$ replaces $\mathbf R^n_b$ by $\mathbf R_z(\gamma)\mathbf R^n_b$, and $(\mathbf R_z(\gamma)\mathbf R^n_b)^\top\mathbf e_z = (\mathbf R^n_b)^\top\mathbf R_z(\gamma)^\top\mathbf e_z = (\mathbf R^n_b)^\top\mathbf e_z$, so the reading is unchanged.

    **How good is accelerometer tilt?** To first order, an error component of size $\varepsilon$ perpendicular to gravity tips the measured vertical by $\varepsilon/g$ radians. Hence:

    - **noise** of $\sigma_a = 0.05$ m/s$^2$ gives about $0.05/9.81\ \text{rad} = 0.29^\circ$ of tilt noise per sample;
    - **bias** of $0.05$ m/s$^2$ gives a constant tilt error of about $0.29^\circ$, and nothing in a static accelerometer reading can tell this apart from a real tilt;
    - **linear acceleration** is the big one: a horizontal acceleration $a$ tips the apparent vertical by $\arctan(a/g)$, so $1$ m/s$^2$ already gives $5.8^\circ$. A walking foot reaches tens of m/s$^2$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch19-sec-heading-from-the-magnetometer -->
    ## Heading from the Magnetometer

    The Earth's field $\mathbf m^n = [0, B_N, -B_D]^\top$ has a horizontal part $B_N = 22\ \mu$T pointing north and a vertical part $B_D = 42\ \mu$T pointing down; it dips $\arctan(42/22) \approx 62^\circ$ below the horizon. To read the heading, we first undo roll and pitch.

    /// admonition | 📐 **Theorem (Tilt-Compensated Heading)**
        attrs: {class: theorem, id: ch19-thm-tilt-compensated-heading}
    If $\mathbf m_m = (\mathbf R^n_b)^\top\mathbf m^n$ exactly, with $\mathbf R^n_b = \mathbf R_z(\psi)\mathbf R_y(\theta)\mathbf R_x(\phi)$, then the *leveled* field $\mathbf m_h := \mathbf R_y(\theta)\mathbf R_x(\phi)\,\mathbf m_m$ equals $[B_N\sin\psi,\ B_N\cos\psi,\ -B_D]^\top$. Hence
    $$\psi = \operatorname{atan2}(m_{h,x},\ m_{h,y}) = \operatorname{atan2}\big(\cos\theta\,m_x + \sin\theta\sin\phi\,m_y + \sin\theta\cos\phi\,m_z,\ \ \cos\phi\,m_y - \sin\phi\,m_z\big).$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    $(\mathbf R^n_b)^\top = \mathbf R_x(\phi)^\top\mathbf R_y(\theta)^\top\mathbf R_z(\psi)^\top$, so $\mathbf R_y(\theta)\mathbf R_x(\phi)\mathbf m_m = \mathbf R_z(\psi)^\top\mathbf m^n$, and
    $$\mathbf R_z(\psi)^\top\mathbf m^n = \begin{bmatrix}\cos\psi & \sin\psi & 0\\ -\sin\psi & \cos\psi & 0\\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}0\\ B_N\\ -B_D\end{bmatrix} = \begin{bmatrix}B_N\sin\psi\\ B_N\cos\psi\\ -B_D\end{bmatrix}.$$
    Since $B_N > 0$, $(m_{h,y}, m_{h,x}) = B_N(\cos\psi, \sin\psi)$ gives $\psi = \operatorname{atan2}(m_{h,x}, m_{h,y})$. Multiplying out $\mathbf R_y(\theta)\mathbf R_x(\phi)\mathbf m_m$ gives the explicit form. $\blacksquare$
    ///

    Check: facing East ($\psi = 0$), the field's horizontal part points along the body's left axis, so $m_{h,x} = 0$, $m_{h,y} = B_N$, and $\psi = 0$.

    **Why tilt compensation matters.** Because the vertical part of the field is nearly twice the horizontal part, ignoring tilt (using $\operatorname{atan2}(m_x, m_y)$ directly) is badly wrong: with the field above, a $5^\circ$ pitch causes heading errors of up to $9.6^\circ$, and a $10^\circ$ pitch up to $19.7^\circ$.

    Together, the two theorems give a complete **snapshot attitude** from a single accelerometer-and-magnetometer sample: roll and pitch from gravity, then heading from the leveled field. It is the standard way to initialize an attitude filter, but used on its own it inherits every accelerometer and magnetometer error at full strength.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ```python
    def tilt_from_accel(f):
        "\"\"Roll and pitch (rad) from a specific-force sample, assuming no acceleration."\"\"
        roll = np.arctan2(f[1], f[2])
        pitch = np.arctan2(-f[0], np.hypot(f[1], f[2]))
        return roll, pitch

    def heading_from_mag(m, roll, pitch):
        "\"\"Tilt-compensated yaw (rad, counterclockwise from East) from a magnetometer sample."\"\"
        m_h = rot_y(pitch) @ rot_x(roll) @ m
        return np.arctan2(m_h[0], m_h[1])
    ```
    """)
    return


@app.cell
def snapshot_functions(np, rot_x, rot_y):
    # jb: include=false
    def tilt_from_accel(f):
        """Roll and pitch (rad) from a specific-force sample, assuming no acceleration."""
        roll = np.arctan2(f[1], f[2])
        pitch = np.arctan2(-f[0], np.hypot(f[1], f[2]))
        return roll, pitch

    def heading_from_mag(m, roll, pitch):
        """Tilt-compensated yaw (rad, counterclockwise from East) from a magnetometer sample."""
        m_h = rot_y(pitch) @ rot_x(roll) @ m
        return np.arctan2(m_h[0], m_h[1])

    return heading_from_mag, tilt_from_accel


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch19-sec-integrating-the-gyroscope -->
    ## Integrating the Gyroscope

    The gyroscope alone gives attitude by Chapter 18's exact update, $\hat q_k = \hat q_{k-1}\otimes\operatorname{Exp}_q(\boldsymbol\omega_{m,k}\Delta t)$. Every error in $\boldsymbol\omega_m$ is integrated along with the motion. The single-axis case shows how.

    /// admonition | 📐 **Theorem (Gyroscope Integration Error)**
        attrs: {class: theorem, id: ch19-thm-gyroscope-integration-error}
    Suppose a body turns about a fixed axis by angle $\theta_k$ at time $k\Delta t$, and $\hat\theta_k = \hat\theta_{k-1} + \omega_{m,k}\Delta t$ with $\omega_{m,k}\Delta t = (\theta_k - \theta_{k-1}) + (b + n_k)\Delta t$, where $b$ is a constant bias and the $n_k$ are independent with mean $0$ and variance $\sigma_g^2$. Then the error $e_k := \hat\theta_k - \theta_k$ satisfies
    $$\mathbb E[e_k] = e_0 + b\,t_k,\qquad \operatorname{Var}(e_k) = \sigma_g^2\,\Delta t\,t_k,\qquad t_k := k\Delta t,$$
    for a deterministic initial error $e_0$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Subtracting $\theta_k = \theta_{k-1} + (\theta_k - \theta_{k-1})$ from the recursion gives $e_k = e_{k-1} + (b + n_k)\Delta t$, so $e_k = e_0 + kb\Delta t + \Delta t\sum_{j=1}^k n_j$. Take expectations, and use that the variance of a sum of independent random variables is the sum of their variances ([Chapter 6](#ch6-thm-variance-of-a-linear-combination)): $\operatorname{Var}(e_k) = k\,\Delta t^2\sigma_g^2 = \sigma_g^2\Delta t\,t_k$. $\blacksquare$
    ///

    The bias produces an error growing linearly in time; the noise produces a random walk whose standard deviation grows like $\sqrt{t}$. With our defaults, after one minute the bias contributes $0.01 \times 60 = 0.6$ rad $= 34^\circ$ and the noise only $0.01\sqrt{0.01\times 60} = 0.0077$ rad $= 0.44^\circ$. The bias dominates, which is why the Kalman filter below estimates it. The figure shows a body pitching back and forth for a minute: the accelerometer's pitch is noisy and wobbles with linear acceleration but stays centered on the truth, while the gyroscope's pitch is smooth but walks steadily away. This growing error is called *drift*[^drift].

    [^drift]: Used informally here; defined precisely in [Chapter 20](#ch20-sec-how-errors-grow).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch19_drift_vs_noise.svg" class="graphic" alt="Pitch angle over 60 seconds. The true pitch oscillates between about plus and minus 30 degrees. The accelerometer pitch follows it with several degrees of noise and wobble. The gyroscope-only pitch follows the shape exactly but drifts steadily upward, about 34 degrees off after one minute." />
    """)
    return


@app.cell
def pitch_simulator(DT, GRAVITY, SIGMA_A, SIGMA_G, np):
    # jb: include=false
    def simulate_pitch(T=30.0, lin_acc=1.0, gyro_bias=0.01, seed=19):
        """Single-axis pitch motion: truth, gyro samples, and accelerometer pitch.
        Index i = 0..N-1 corresponds to time step k = i + 1."""
        _N = int(round(T / DT))
        _t = np.arange(1, _N + 1) * DT

        def _theta(tt):
            return np.radians(20) * np.sin(2 * np.pi * 0.1 * tt) + np.radians(10) * np.sin(2 * np.pi * 0.37 * tt + 1)

        _th = _theta(_t)
        _rng = np.random.default_rng(seed)
        _omega_m = (_th - _theta(_t - DT)) / DT + gyro_bias + SIGMA_G * _rng.normal(size=_N)
        _a = lin_acc * np.sin(2 * np.pi * 0.4 * _t + 0.3)            # East acceleration
        _fx = np.cos(_th) * _a - np.sin(_th) * GRAVITY + SIGMA_A * _rng.normal(size=_N)
        _fy = SIGMA_A * _rng.normal(size=_N)
        _fz = np.sin(_th) * _a + np.cos(_th) * GRAVITY + SIGMA_A * _rng.normal(size=_N)
        _z = np.arctan2(-_fx, np.hypot(_fy, _fz))
        return dict(t=_t, theta=_th, omega_m=_omega_m, z=_z)

    return (simulate_pitch,)


@app.cell
def make_drift_fig(DT, IMAGES_DIR, np, plt, simulate_pitch):
    # jb: include=false
    _s = simulate_pitch(T=60.0, lin_acc=1.0, gyro_bias=0.01)
    _gyro = _s["z"][0] + np.concatenate([[0.0], np.cumsum(_s["omega_m"][1:] * DT)])
    _fig, _ax = plt.subplots(figsize=(8, 3.8))
    _ax.plot(_s["t"], np.degrees(_s["z"]), color="C0", lw=0.6, alpha=0.7, label="accelerometer pitch")
    _ax.plot(_s["t"], np.degrees(_gyro), color="red", ls=":", lw=1.8, label="gyroscope only")
    _ax.plot(_s["t"], np.degrees(_s["theta"]), color="k", lw=1.2, label="truth")
    _ax.set_xlabel("time (s)")
    _ax.set_ylabel("pitch (deg)")
    _ax.set_title("Gyroscope drift versus accelerometer noise", style="italic")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.legend(fontsize=9, loc="upper left")
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch19_drift_vs_noise.svg")
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch19-sec-the-complementary-filter -->
    ## The Complementary Filter

    The two error patterns are complementary: the gyroscope is good exactly where the accelerometer is bad (fast changes) and bad exactly where it is good (long-term average). Start with the simplest case, a body that only pitches about its own $y$ axis (roll and yaw stay zero). By Chapter 17's Euler-angle kinematics with $\phi = 0$, the pitch rate is then exactly the $y$ gyroscope rate, $\dot\theta = \omega_y$. We have two signals:

    - the gyroscope, whose increment $\omega_{m,k}\Delta t$ predicts the change in pitch from step $k-1$ to step $k$;
    - the accelerometer pitch $z_k := \operatorname{atan2}(-f_x, \sqrt{f_y^2 + f_z^2})$, a direct but noisy measurement of $\theta_k$.

    The **complementary filter** blends them:

    $$\hat\theta_1 = z_1;\qquad \hat\theta_k^- = \hat\theta_{k-1} + \omega_{m,k}\Delta t,\qquad \hat\theta_k = \hat\theta_k^- + \alpha\,(z_k - \hat\theta_k^-)\quad(k \ge 2).$$

    /// attention | 🗝️ **Key Idea**
    This is *exactly* the Introduction's alpha filter, $\hat x_k = \hat x_k^- + \alpha(z_k - \hat x_k^-)$ with $\hat x_k^- = \hat x_{k-1} + \Delta x_k$, with the predicted change supplied by the gyroscope, $\Delta x_k = \omega_{m,k}\Delta t$, and the measurement supplied by the accelerometer. Nothing about the recursion is new; only the source of $\Delta x_k$ is.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ```python
    def complementary_filter(omega_m, z, alpha, dt):
        "\"\"Scalar complementary filter = the Introduction's alpha filter with dx_k = omega_k * dt.
        Index i holds time step k = i + 1; omega_m[i] covers the interval from k - 1 to k."\"\"
        est = np.zeros(len(z))
        est[0] = z[0]                                   # first-measurement initialization
        for i in range(1, len(z)):
            prediction = est[i - 1] + omega_m[i] * dt   # x_k^- = x_{k-1} + dx_k
            est[i] = prediction + alpha * (z[i] - prediction)
        return est
    ```
    """)
    return


@app.cell
def complementary_code(np):
    # jb: include=false
    def complementary_filter(omega_m, z, alpha, dt):
        """Scalar complementary filter = the Introduction's alpha filter with dx_k = omega_k * dt.
        Index i holds time step k = i + 1; omega_m[i] covers the interval from k - 1 to k."""
        est = np.zeros(len(z))
        est[0] = z[0]                                   # first-measurement initialization
        for i in range(1, len(z)):
            prediction = est[i - 1] + omega_m[i] * dt   # x_k^- = x_{k-1} + dx_k
            est[i] = prediction + alpha * (z[i] - prediction)
        return est

    return (complementary_filter,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch19-sec-why-it-is-called-complementary -->
    ### Why It Is Called Complementary

    Let $\mathcal L$ denote the exponential moving average with gain $\alpha$, started from zero: $\mathcal L[y]_1 := 0$ and $\mathcal L[y]_k := (1 - \alpha)\mathcal L[y]_{k-1} + \alpha\,y_k$ for $k \ge 2$. Let $G_k := \hat\theta_1 + \sum_{j=2}^k\omega_{m,j}\Delta t$ be the gyroscope-only angle.

    /// admonition | 📐 **Theorem (Complementary Decomposition)**
        attrs: {class: theorem, id: ch19-thm-complementary-decomposition}
    For every $k \ge 1$,
    $$\hat\theta_k = \mathcal L[z]_k + \big(G_k - \mathcal L[G]_k\big).$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Let $D_k := \hat\theta_k - G_k$, so $D_1 = 0$. For $k \ge 2$, using $G_k = G_{k-1} + \omega_{m,k}\Delta t$,
    $$D_k = (1 - \alpha)(\hat\theta_{k-1} + \omega_{m,k}\Delta t) + \alpha z_k - G_k = (1 - \alpha)(\hat\theta_{k-1} - G_{k-1}) + (1 - \alpha)G_k + \alpha z_k - G_k = (1 - \alpha)D_{k-1} + \alpha(z_k - G_k).$$
    This is the recursion defining $\mathcal L[z - G]$, with the same start, so $D = \mathcal L[z - G]$. The map $\mathcal L$ is linear (each $\mathcal L[y]_k$ is a fixed weighted sum of $y_2, \dots, y_k$), so $D = \mathcal L[z] - \mathcal L[G]$. $\blacksquare$
    ///

    The exponential moving average $\mathcal L$ is a *low-pass* filter: it passes slowly varying signals and averages out fast fluctuations ([Chapter 6](#ch6-thm-ema-of-a-constant-value) showed it shrinks white-noise variance by the factor $\alpha/(2-\alpha)$). Its complement $\mathcal I - \mathcal L$ (identity minus $\mathcal L$) is a *high-pass* filter: it removes constants and slow trends. So the estimate is the accelerometer angle, low-passed, plus the gyroscope angle, high-passed, and the two filters add up to the identity. If both sensors were perfect ($z = G = \theta$), the output would be exactly $\theta$, with no lag and no distortion.

    /// note | 📖 **Definition**
    <u>**Complementary filter**</u>

    A complementary filter is a {term}`filter` that estimates a signal from two measured versions of it, $z^{(1)}$ and $z^{(2)}$, as $\mathcal L[z^{(1)}] + \big(z^{(2)} - \mathcal L[z^{(2)}]\big)$, where $\mathcal L$ is a linear low-pass filter that passes constant signals unchanged. Equivalently, it low-passes one measurement and high-passes the other with filters that sum to the identity.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch19-sec-errors-and-the-time-constant -->
    ### Errors and the Time Constant

    Let $e_k := \hat\theta_k - \theta_k$, let $d_k := \omega_{m,k}\Delta t - (\theta_k - \theta_{k-1})$ be the gyroscope increment error, and $v_k := z_k - \theta_k$ the accelerometer pitch error. Subtracting $\theta_k$ from the update gives the error recursion
    $$e_k = (1 - \alpha)(e_{k-1} + d_k) + \alpha\,v_k.$$

    /// admonition | 📐 **Theorem (Complementary-Filter Errors)**
        attrs: {class: theorem, id: ch19-thm-complementary-filter-errors}
    Let $0 < \alpha \le 1$ and define the **time constant** $\tau := \Delta t\,(1 - \alpha)/\alpha$.

    1. *Gyroscope bias.* If $d_k = b\Delta t$ (constant bias, no noise) and $v_k = 0$, then $e_k \to b\tau$ as $k \to \infty$.
    2. *Accelerometer noise.* If $d_k = 0$ and the $v_k$ are independent with mean $0$ and variance $\sigma_v^2$, then $\operatorname{Var}(e_k) \to \sigma_v^2\,\alpha/(2 - \alpha)$.
    3. *Gyroscope noise.* If $v_k = 0$ and $d_k = n_k\Delta t$ with the $n_k$ independent, mean $0$, variance $\sigma_g^2$, then $\operatorname{Var}(e_k) \to \sigma_g^2\Delta t^2(1-\alpha)^2/\big(\alpha(2 - \alpha)\big)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    1. $e_k - b\tau = (1-\alpha)e_{k-1} + (1-\alpha)b\Delta t - b\Delta t\tfrac{1-\alpha}{\alpha} = (1-\alpha)\big(e_{k-1} - b\Delta t\tfrac{1-\alpha}{\alpha}\big) = (1-\alpha)(e_{k-1} - b\tau)$, so $e_k - b\tau = (1-\alpha)^{k-1}(e_1 - b\tau) \to 0$ when $\alpha > 0$.
    2. $e_k = (1-\alpha)e_{k-1} + \alpha v_k$, and $e_{k-1}$ depends only on $e_1$ and $v_j$ with $j < k$, so it is independent of $v_k$ and the variances add: $V_k = (1-\alpha)^2V_{k-1} + \alpha^2\sigma_v^2$. The fixed point is $V = \alpha^2\sigma_v^2/(1 - (1-\alpha)^2) = \sigma_v^2\alpha/(2-\alpha)$, and $V_k - V = (1-\alpha)^2(V_{k-1} - V) \to 0$. (This is Chapter 6's exponential-moving-average result.)
    3. The same argument with $e_k = (1-\alpha)e_{k-1} + (1-\alpha)\Delta t\,n_k$ gives the fixed point $(1-\alpha)^2\Delta t^2\sigma_g^2/(1 - (1-\alpha)^2)$. $\blacksquare$
    ///

    **Why $\tau$ is a time constant.** Two facts justify the name. First, $1 - \alpha = \tau/(\tau + \Delta t)$ exactly, so an initial error decays like $(1-\alpha)^k = (1 + \Delta t/\tau)^{-k} \approx e^{-k\Delta t/\tau} = e^{-t/\tau}$ when $\Delta t \ll \tau$: errors shrink by a factor of $e$ every $\tau$ seconds. Second, the filter is the discretization of a continuous-time filter with that time constant. Consider
    $$\dot{\hat\theta} = \omega_m + \frac{1}{\tau}\big(z - \hat\theta\big),$$
    which integrates the gyroscope and continually pulls the estimate toward the accelerometer at rate $1/\tau$. Replacing the derivative by the backward difference $(\hat\theta_k - \hat\theta_{k-1})/\Delta t$ and evaluating the right side at step $k$ gives $\hat\theta_k(1 + \Delta t/\tau) = \hat\theta_{k-1} + \omega_{m,k}\Delta t + (\Delta t/\tau)z_k$, that is,
    $$\hat\theta_k = \frac{\tau}{\tau + \Delta t}\big(\hat\theta_{k-1} + \omega_{m,k}\Delta t\big) + \frac{\Delta t}{\tau + \Delta t}\,z_k,$$
    which is the complementary filter with $\alpha = \Delta t/(\tau + \Delta t)$, i.e. $\tau = \Delta t(1-\alpha)/\alpha$. In the continuous version the bias result is immediate: at steady state the error satisfies $\dot e = b - e/\tau = 0$, so $e = b\tau$.

    **Frequency interpretation.** In the continuous filter, the accelerometer path is the low-pass system $\tau\dot y + y = u$. For a sinusoidal input $u = \sin(2\pi f t)$, try $y = A\sin(2\pi f t - \varphi)$: by the identity $a\sin x + b\cos x = \sqrt{a^2 + b^2}\,\sin(x + \operatorname{atan2}(b, a))$, the left side becomes $A\sqrt{1 + (2\pi f\tau)^2}\,\sin(2\pi f t - \varphi + \arctan(2\pi f\tau))$, which equals $u$ exactly when
    $$A = \frac{1}{\sqrt{1 + (2\pi f\tau)^2}},\qquad \varphi = \arctan(2\pi f\tau).$$
    The complementary path $u - y = \tau\dot y$ has amplitude $2\pi f\tau A = 2\pi f\tau/\sqrt{1 + (2\pi f\tau)^2}$. So accelerometer disturbances at frequency $f$ are scaled by $1/\sqrt{1 + (2\pi f\tau)^2}$ (slow ones pass, fast ones are blocked), gyroscope-angle errors by $2\pi f\tau/\sqrt{1 + (2\pi f\tau)^2}$ (slow drift is blocked, fast motion passes), and the two cross at the cutoff frequency $f_c = 1/(2\pi\tau)$.

    **Choosing $\alpha$.** A large $\tau$ (small $\alpha$) suppresses accelerometer noise and linear acceleration better but lets gyroscope bias cause a larger error $b\tau$ and makes recovery slower; a small $\tau$ does the opposite. If the only errors were white noise, [Chapter 9](#ch9-thm-steady-state-gain)'s steady-state Kalman gain would give the optimal $\alpha$ (the known increments $\Delta x_k$ shift the estimates but not their variances, so they do not change the gains): with process noise $Q = \sigma_g^2\Delta t^2$ (the gyroscope increment) and measurement noise $R = (\sigma_a/g)^2$ (the accelerometer pitch), $K_\infty \approx 0.019$, i.e. $\tau \approx 0.5$ s. But bias and linear acceleration are not white, and they pull $\tau$ in opposite directions. The way out is to *estimate* the bias, which the Kalman filter below does.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch19-sec-interactive-tuning-the-complementary-filter -->
    ### Interactive: Tuning the Complementary Filter

    A body pitches back and forth for 30 s while being pushed east and west (linear acceleration at 0.4 Hz). The top panel shows the truth (black), the accelerometer pitch (blue), the gyroscope-only pitch (red dotted), and the complementary filter (orange). The bottom panel shows the filter's error, with the predicted bias error $b\tau$ dashed. Try a large gyroscope bias with a small $\alpha$, then strong linear acceleration with a large $\alpha$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    cf_alpha = mo.ui.slider(steps=[0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0], value=0.02,
                            label=r"gain $\alpha$", show_value=True)
    cf_bias = mo.ui.slider(0.0, 0.1, 0.005, value=0.01, label="gyroscope bias $b$ (rad/s)", show_value=True)
    cf_acc = mo.ui.slider(0.0, 3.0, 0.25, value=0.5, label=r"linear acceleration amplitude (m/s$^2$)",
                          show_value=True)
    return cf_acc, cf_alpha, cf_bias


@app.cell(hide_code=True)
def _(
    DT,
    cf_acc,
    cf_alpha,
    cf_bias,
    complementary_filter,
    graphic,
    mo,
    np,
    plt,
    simulate_pitch,
):
    _s = simulate_pitch(T=30.0, lin_acc=cf_acc.value, gyro_bias=cf_bias.value)
    _alpha = float(cf_alpha.value)
    _est = complementary_filter(_s["omega_m"], _s["z"], _alpha, DT)
    _gyro = _s["z"][0] + np.concatenate([[0.0], np.cumsum(_s["omega_m"][1:] * DT)])
    _tau = DT * (1 - _alpha) / _alpha
    _err = np.degrees(_est - _s["theta"])

    _fig, (_a1, _a2) = plt.subplots(2, 1, figsize=(8.5, 5.6), sharex=True,
                                    gridspec_kw=dict(height_ratios=[3, 2]))
    _a1.plot(_s["t"], np.degrees(_s["z"]), color="C0", lw=0.6, alpha=0.7, label="accelerometer")
    _a1.plot(_s["t"], np.degrees(_gyro), color="red", ls=":", lw=1.6, label="gyroscope only")
    _a1.plot(_s["t"], np.degrees(_s["theta"]), color="k", lw=1.2, label="truth")
    _a1.plot(_s["t"], np.degrees(_est), color="C1", lw=1.4, label="complementary filter")
    _a1.set_ylim(-45, 45)
    _a1.set_ylabel("pitch (deg)")
    _a1.legend(fontsize=8, ncol=4, loc="upper center")
    _a1.set_title(rf"$\alpha = {_alpha:g}$, $\tau = {_tau:.3g}$ s", style="italic")
    _a2.plot(_s["t"], _err, color="C1", lw=1.0, label="filter error")
    _a2.axhline(np.degrees(cf_bias.value * _tau), color="k", ls="--", lw=1.0, label=r"predicted bias error $b\tau$")
    _lim = max(2.0, 1.2 * np.abs(_err[100:]).max())
    _a2.set_ylim(-_lim, _lim)
    _a2.set_ylabel("error (deg)")
    _a2.set_xlabel("time (s)")
    _a2.legend(fontsize=8, loc="upper right")
    for _a in (_a1, _a2):
        _a.grid(visible=True, alpha=0.9, linewidth=0.4)
    _fig.tight_layout()

    _rms = np.sqrt(np.mean(_err[500:] ** 2))
    _rms_acc = np.sqrt(np.mean(np.degrees(_s["z"] - _s["theta"])[500:] ** 2))
    _txt = mo.md(
        rf"Time constant $\tau = {_tau:.3g}$ s (cutoff $f_c = {1 / (2 * np.pi * _tau):.3g}$ Hz). "
        rf"Predicted bias error $b\tau = {np.degrees(cf_bias.value * _tau):.2f}^\circ$. "
        rf"RMS error after 5 s: filter ${_rms:.2f}^\circ$, accelerometer alone ${_rms_acc:.2f}^\circ$."
        if _alpha < 1 else
        r"With $\alpha = 1$ the filter ignores the gyroscope and returns the accelerometer pitch."
    )
    _out = mo.vstack([mo.hstack([cf_alpha, cf_bias, cf_acc], justify="start"), graphic(_fig), _txt])
    plt.close(_fig)
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **Single-axis motion.** $\dot\theta = \omega_y$ holds only when $\phi = 0$; in general $\dot\theta = \cos\phi\,\omega_y - \sin\phi\,\omega_z$ ([Chapter 17](#ch17-thm-euler-angle-kinematics)). Running one scalar filter per Euler angle works for small tilts but inherits gimbal lock and couples errors between axes. The fix is to apply the same idea to the whole rotation, as the Kalman filter below and the Mahony filter at the end of the chapter do.
    - **Gyroscope bias is not removed,** only limited to $b\tau$. Adding an integral term or estimating the bias removes it.
    - **Linear acceleration is not modeled.** It enters as a slowly varying accelerometer error that the low-pass path lets through whenever its frequency is below $f_c$.
    - **Angles wrap.** For heading, the innovation $z_k - \hat\theta_k^-$ must be wrapped into $(-\pi, \pi]$.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch19-sec-an-error-state-kalman-filter -->
    ## An Error-State Kalman Filter

    The complementary filter has two weaknesses: it is scalar, and it cannot remove gyroscope bias. A Kalman filter fixes both, but putting attitude directly into its state is awkward:

    - **Euler angles** have gimbal lock ([Chapter 17](#ch17-sec-gimbal-lock)).
    - **A quaternion** has four numbers for three degrees of freedom. Its unit-norm constraint means the "uncertainty" along $q$ itself is meaningless, so the $4\times 4$ covariance is singular (or wrong), and an additive correction $\hat q + \mathbf K\tilde{\mathbf y}$ leaves the unit sphere.
    - **A rotation vector** for the whole attitude jumps at $180^\circ$.

    The way out is the one announced at the end of Chapter 17: use three numbers only *locally*. Keep the attitude itself as a unit quaternion, propagated exactly as in Chapter 18, and let the Kalman filter estimate only the small rotation $\delta\boldsymbol\theta$ between that quaternion and the truth. After every measurement update, fold the estimated error into the quaternion and reset it to zero, so $\delta\boldsymbol\theta$ never grows large.

    /// note | 📖 **Definition**
    <u>**Error-state Kalman filter**</u>

    An error-state Kalman filter is a filter that keeps (1) a *nominal state* $\hat{\mathbf x}_k$, propagated with the noise-free nonlinear process model, and (2) a Gaussian estimate (mean and covariance) of the *error state* $\delta\mathbf x_k$, defined by $\mathbf x_k = \hat{\mathbf x}_k \oplus \delta\mathbf x_k$ for a fixed composition rule $\oplus$. The error estimate is propagated and updated with the linearized ({term}`extended Kalman filter`) equations, and after each update its mean is *injected* into the nominal state ($\hat{\mathbf x} \leftarrow \hat{\mathbf x}\oplus\delta\hat{\mathbf x}$) and *reset* to zero.
    ///

    <!-- label: ch19-sec-state-error-and-nominal-propagation -->
    ### State, Error, and Nominal Propagation

    The nominal state is the attitude quaternion and the gyroscope-bias estimate, $(\hat q, \hat{\mathbf b}_g)$. The error state is
    $$\delta\mathbf x = \begin{bmatrix}\delta\boldsymbol\theta\\ \delta\mathbf b_g\end{bmatrix} \in \mathbb R^6,\qquad q = \hat q\otimes\delta q(\delta\boldsymbol\theta),\quad \mathbf b_g = \hat{\mathbf b}_g + \delta\mathbf b_g,\qquad \delta q(\delta\boldsymbol\theta) := \operatorname{Exp}_q(\delta\boldsymbol\theta) \approx \big[1, \tfrac12\delta\boldsymbol\theta\big].$$
    In matrix form the attitude error is the right (body-frame) perturbation of Chapter 17, $\mathbf R = \hat{\mathbf R}\operatorname{Exp}(\delta\boldsymbol\theta)$, where $\hat{\mathbf R} := \mathbf R(\hat q)$. An error here is what must be *added to* the nominal value to obtain the true one (the opposite sign to Chapter 7's $e = \hat x - x$). We model the bias as a slow {term}`random walk`, $\dot{\mathbf b}_g = \mathbf w_b$ with intensity $\sigma_{bg}^2$, so the filter can follow a slowly changing bias.

    The nominal state is propagated with the bias-corrected rate $\hat{\boldsymbol\omega}_k := \boldsymbol\omega_{m,k} - \hat{\mathbf b}_g$ and Chapter 18's exact update:
    $$\hat q_k = \hat q_{k-1}\otimes\operatorname{Exp}_q(\hat{\boldsymbol\omega}_k\Delta t),\qquad \hat{\mathbf b}_{g,k} = \hat{\mathbf b}_{g,k-1}.$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch19-sec-error-dynamics -->
    ### Error Dynamics

    We need one more identity about cross-product matrices.

    /// admonition | 📐 **Lemma (Commutator of Cross-Product Matrices)**
        attrs: {class: lemma, id: ch19-lem-commutator-of-cross-product-matrices}
    For all $\mathbf a, \mathbf b \in \mathbb R^3$: $\ [\mathbf a]_\times[\mathbf b]_\times - [\mathbf b]_\times[\mathbf a]_\times = [\mathbf a\times\mathbf b]_\times$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Apply both sides to any $\mathbf c$ and use the triple-product expansion ([Appendix D: Cross Products and Skew-Symmetric Matrices](#appd-sec-cross-products-and-skew-symmetric-matrices)) three times:
    $\mathbf a\times(\mathbf b\times\mathbf c) - \mathbf b\times(\mathbf a\times\mathbf c) = \mathbf b(\mathbf a\cdot\mathbf c) - \mathbf c(\mathbf a\cdot\mathbf b) - \mathbf a(\mathbf b\cdot\mathbf c) + \mathbf c(\mathbf b\cdot\mathbf a) = \mathbf b(\mathbf a\cdot\mathbf c) - \mathbf a(\mathbf b\cdot\mathbf c)$, and $(\mathbf a\times\mathbf b)\times\mathbf c = -\mathbf c\times(\mathbf a\times\mathbf b) = -\mathbf a(\mathbf c\cdot\mathbf b) + \mathbf b(\mathbf c\cdot\mathbf a)$, which is the same. $\blacksquare$
    ///

    /// admonition | 📐 **Theorem (Attitude Error Dynamics)**
        attrs: {class: theorem, id: ch19-thm-attitude-error-dynamics}
    Let the true attitude obey $\dot{\mathbf R} = \mathbf R[\boldsymbol\omega]_\times$ with $\boldsymbol\omega = \boldsymbol\omega_m - \mathbf b_g - \mathbf n_g$, and the nominal attitude obey $\dot{\hat{\mathbf R}} = \hat{\mathbf R}[\hat{\boldsymbol\omega}]_\times$ with $\hat{\boldsymbol\omega} = \boldsymbol\omega_m - \hat{\mathbf b}_g$. If $\mathbf R = \hat{\mathbf R}\operatorname{Exp}(\delta\boldsymbol\theta)$, then to first order in the small quantities $\delta\boldsymbol\theta$, $\delta\mathbf b_g$, $\mathbf n_g$,
    $$\dot{\delta\boldsymbol\theta} = -[\hat{\boldsymbol\omega}]_\times\,\delta\boldsymbol\theta - \delta\mathbf b_g - \mathbf n_g,\qquad \dot{\delta\mathbf b}_g = \mathbf w_b.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Write $\mathbf E := \operatorname{Exp}(\delta\boldsymbol\theta) = \mathbf I + [\delta\boldsymbol\theta]_\times + (\text{second order})$ (Chapter 17's small-angle theorem), so $\dot{\mathbf E} = [\dot{\delta\boldsymbol\theta}]_\times$ to first order. Differentiating $\mathbf R = \hat{\mathbf R}\mathbf E$ with the product rule and using both kinematic equations,
    $$\hat{\mathbf R}\mathbf E[\boldsymbol\omega]_\times = \dot{\mathbf R} = \hat{\mathbf R}[\hat{\boldsymbol\omega}]_\times\mathbf E + \hat{\mathbf R}\dot{\mathbf E}\quad\Longrightarrow\quad \dot{\mathbf E} = \mathbf E[\boldsymbol\omega]_\times - [\hat{\boldsymbol\omega}]_\times\mathbf E.$$
    Substituting the first-order forms of $\mathbf E$ and $\dot{\mathbf E}$:
    $$[\dot{\delta\boldsymbol\theta}]_\times = [\boldsymbol\omega - \hat{\boldsymbol\omega}]_\times + [\delta\boldsymbol\theta]_\times[\boldsymbol\omega]_\times - [\hat{\boldsymbol\omega}]_\times[\delta\boldsymbol\theta]_\times.$$
    Since $\boldsymbol\omega - \hat{\boldsymbol\omega} = -\delta\mathbf b_g - \mathbf n_g$ is itself small, replacing $\boldsymbol\omega$ by $\hat{\boldsymbol\omega}$ in the product term changes it only at second order. The lemma then gives $[\delta\boldsymbol\theta]_\times[\hat{\boldsymbol\omega}]_\times - [\hat{\boldsymbol\omega}]_\times[\delta\boldsymbol\theta]_\times = [\delta\boldsymbol\theta\times\hat{\boldsymbol\omega}]_\times = [-\hat{\boldsymbol\omega}\times\delta\boldsymbol\theta]_\times$. So $[\dot{\delta\boldsymbol\theta}]_\times = [-\delta\mathbf b_g - \mathbf n_g - \hat{\boldsymbol\omega}\times\delta\boldsymbol\theta]_\times$; a cross-product matrix determines its vector. The bias equation follows from $\delta\mathbf b_g = \mathbf b_g - \hat{\mathbf b}_g$ with $\hat{\mathbf b}_g$ constant between updates. $\blacksquare$
    ///

    The term $-[\hat{\boldsymbol\omega}]_\times\delta\boldsymbol\theta$ has a simple meaning: $\delta\boldsymbol\theta$ is expressed in body axes, and those axes turn at $\hat{\boldsymbol\omega}$, so a fixed error looks like it rotates the other way. The term $-\delta\mathbf b_g$ is the gyroscope-bias drift of the single-axis theorem above. In matrix form, $\dot{\delta\mathbf x} = \mathbf F\,\delta\mathbf x + (\text{noise})$ with
    $$\mathbf F = \begin{bmatrix}-[\hat{\boldsymbol\omega}]_\times & -\mathbf I\\ \mathbf 0 & \mathbf 0\end{bmatrix}.$$

    **Discretization.** Over one sample period $\hat{\boldsymbol\omega} = \hat{\boldsymbol\omega}_k$ is constant. The attitude part $\dot{\delta\boldsymbol\theta} = -[\hat{\boldsymbol\omega}_k]_\times\delta\boldsymbol\theta$ then has the exact solution $\exp(-\Delta t[\hat{\boldsymbol\omega}_k]_\times)\,\delta\boldsymbol\theta = \operatorname{Exp}(\hat{\boldsymbol\omega}_k\Delta t)^\top\delta\boldsymbol\theta$ (Chapter 17's constant-rate argument and $\operatorname{Exp}(-\mathbf a) = \operatorname{Exp}(\mathbf a)^\top$). The bias error and the gyroscope noise sample $\mathbf n_{g,k}$ act over $\Delta t$, adding $-\Delta t\,\delta\mathbf b_g - \Delta t\,\mathbf n_{g,k}$ to first order. So the discrete error model is $\delta\mathbf x_k = \boldsymbol\Phi_k\,\delta\mathbf x_{k-1} + (\text{noise})$ with
    $$\boldsymbol\Phi_k = \begin{bmatrix}\operatorname{Exp}(\hat{\boldsymbol\omega}_k\Delta t)^\top & -\Delta t\,\mathbf I\\ \mathbf 0 & \mathbf I\end{bmatrix},\qquad \mathbf Q = \begin{bmatrix}\sigma_g^2\Delta t^2\,\mathbf I & \mathbf 0\\ \mathbf 0 & \sigma_{bg}^2\Delta t\,\mathbf I\end{bmatrix}.$$
    The covariance $\sigma_g^2\Delta t^2\mathbf I$ is that of $-\Delta t\,\mathbf n_{g,k}$ for per-sample noise of standard deviation $\sigma_g$; the bias random walk adds variance $\sigma_{bg}^2\Delta t$ per period ([Chapter 9](#ch9-lem-a-random-walk-spreads-out)). $\boldsymbol\Phi_k$ agrees with $\mathbf I + \mathbf F\Delta t$ to first order in $\Delta t$ (Chapter 21 uses that simpler form for its larger state). The covariance prediction is Chapter 13's $\mathbf P_k^- = \boldsymbol\Phi_k\mathbf P_{k-1}\boldsymbol\Phi_k^\top + \mathbf Q$. The error *mean* needs no prediction: it is zero after every reset, and $\boldsymbol\Phi_k\mathbf 0 = \mathbf 0$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch19-sec-measurement-updates -->
    ### Measurement Updates

    **Accelerometer.** Assume for now that the body is not accelerating ($\mathbf a^n \approx \mathbf 0$) and ignore the accelerometer bias. Then the accelerometer measures gravity:
    $$\mathbf f_m = \mathbf R^\top(-\mathbf g^n) + \mathbf v_a,\qquad \mathbf v_a \sim \mathcal N(\mathbf 0, \mathbf R_{\text{acc}}),\quad \mathbf R_{\text{acc}} = \sigma_{\text{acc}}^2\mathbf I.$$
    (In this chapter the measurement-noise covariance of [Chapter 13](#ch13-sec-the-state-space-model) is written $\mathbf R_{\text{acc}}$ or $\mathbf R_{\text{mag}}$, to keep $\mathbf R$ for attitude.) The filter's $\sigma_{\text{acc}}$ is a tuning choice, usually set well above the sensor's $0.05$ m/s$^2$ to absorb the linear acceleration and bias that the model leaves out.

    /// admonition | 📐 **Theorem (Measurement Jacobians)**
        attrs: {class: theorem, id: ch19-thm-measurement-jacobians}
    Let $\hat{\mathbf h}_a := \hat{\mathbf R}^\top(-\mathbf g^n)$ and $\hat{\mathbf h}_m := \hat{\mathbf R}^\top\mathbf m^n$ be the predicted accelerometer and magnetometer readings. With $\mathbf R = \hat{\mathbf R}\operatorname{Exp}(\delta\boldsymbol\theta)$, to first order in $\delta\boldsymbol\theta$,
    $$\mathbf R^\top(-\mathbf g^n) = \hat{\mathbf h}_a + [\hat{\mathbf h}_a]_\times\,\delta\boldsymbol\theta,\qquad \mathbf R^\top\mathbf m^n = \hat{\mathbf h}_m + [\hat{\mathbf h}_m]_\times\,\delta\boldsymbol\theta.$$
    So the measurement matrices with respect to $\delta\mathbf x = [\delta\boldsymbol\theta; \delta\mathbf b_g]$ are $\mathbf H_{\text{acc}} = \big[[\hat{\mathbf h}_a]_\times\ \ \mathbf 0\big]$ and $\mathbf H_{\text{mag}} = \big[[\hat{\mathbf h}_m]_\times\ \ \mathbf 0\big]$, and the innovations are $\mathbf f_m - \hat{\mathbf h}_a$ and $\mathbf m_m - \hat{\mathbf h}_m$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    For any fixed $\mathbf v^n$, $\mathbf R^\top\mathbf v^n = \operatorname{Exp}(\delta\boldsymbol\theta)^\top\hat{\mathbf R}^\top\mathbf v^n = \operatorname{Exp}(-\delta\boldsymbol\theta)\,\hat{\mathbf h} \approx (\mathbf I - [\delta\boldsymbol\theta]_\times)\hat{\mathbf h} = \hat{\mathbf h} - \delta\boldsymbol\theta\times\hat{\mathbf h} = \hat{\mathbf h} + \hat{\mathbf h}\times\delta\boldsymbol\theta$, with $\hat{\mathbf h} := \hat{\mathbf R}^\top\mathbf v^n$. Apply this with $\mathbf v^n = -\mathbf g^n$ and $\mathbf v^n = \mathbf m^n$. Neither measurement depends on $\mathbf b_g$. $\blacksquare$
    ///

    **What each sensor can see.** $[\hat{\mathbf h}_a]_\times\delta\boldsymbol\theta = \hat{\mathbf h}_a\times\delta\boldsymbol\theta$ vanishes exactly when $\delta\boldsymbol\theta$ is parallel to $\hat{\mathbf h}_a$, the body-frame direction of Up. In navigation coordinates such an error is $\hat{\mathbf R}\,\delta\boldsymbol\theta \parallel \mathbf e_z$: a heading error. So, to first order as well as exactly (as shown earlier), gravity observes tilt but not heading. The magnetometer is blind to rotations about $\mathbf m^n$ instead, and since $\mathbf m^n$ is not vertical, the two sensors together observe all three components of $\delta\boldsymbol\theta$ ([Chapter 13](#ch13-sec-observability)'s observability). The bias has no direct measurement; it becomes observable through $\boldsymbol\Phi_k$, because a bias error makes the attitude error grow in a recognizable way.

    **Update.** For each available measurement, in turn ({term}`sequential updates <sequential update>`, [Chapter 14](#ch14-thm-sequential-update); valid because accelerometer and magnetometer noise are independent), apply the extended Kalman filter update of [Chapter 15](#ch15-sec-update) to the error state, whose predicted mean is zero:
    $$\mathbf S = \mathbf H\mathbf P^-\mathbf H^\top + \mathbf R_{\text{meas}},\quad \mathbf K = \mathbf P^-\mathbf H^\top\mathbf S^{-1},\quad \delta\hat{\mathbf x} = \mathbf K\,(\mathbf z - \hat{\mathbf h}),\quad \mathbf P = (\mathbf I - \mathbf K\mathbf H)\mathbf P^-(\mathbf I - \mathbf K\mathbf H)^\top + \mathbf K\mathbf R_{\text{meas}}\mathbf K^\top,$$
    using the {term}`Joseph form` for numerical robustness.

    <!-- label: ch19-sec-injection-and-reset -->
    ### Injection and Reset

    The estimated error $\delta\hat{\mathbf x} = [\delta\hat{\boldsymbol\theta}; \delta\hat{\mathbf b}_g]$ is folded into the nominal state,
    $$\hat q \leftarrow \hat q\otimes\delta q(\delta\hat{\boldsymbol\theta}),\qquad \hat{\mathbf b}_g \leftarrow \hat{\mathbf b}_g + \delta\hat{\mathbf b}_g,$$
    followed by $\hat q \leftarrow \hat q/\|\hat q\|$ to remove rounding. The error is now measured from the new nominal state, so its mean becomes $\mathbf 0$. Its covariance changes slightly too: the new attitude error $\delta\boldsymbol\theta^+$ satisfies $\operatorname{Exp}(\delta\boldsymbol\theta^+) = \operatorname{Exp}(-\delta\hat{\boldsymbol\theta})\operatorname{Exp}(\delta\boldsymbol\theta)$. The [Baker–Campbell–Hausdorff formula](https://en.wikipedia.org/wiki/Baker%E2%80%93Campbell%E2%80%93Hausdorff_formula), $\operatorname{Log}(\operatorname{Exp}(\mathbf a)\operatorname{Exp}(\mathbf b)) = \mathbf a + \mathbf b + \tfrac12\mathbf a\times\mathbf b + (\text{third order})$ (its second-order term is the commutator of the [Commutator of Cross-Product Matrices lemma](#ch19-lem-commutator-of-cross-product-matrices)), gives $\delta\boldsymbol\theta^+ \approx \delta\boldsymbol\theta - \delta\hat{\boldsymbol\theta} - \tfrac12\delta\hat{\boldsymbol\theta}\times\delta\boldsymbol\theta$, whose Jacobian with respect to $\delta\boldsymbol\theta$ is $\mathbf I - \tfrac12[\delta\hat{\boldsymbol\theta}]_\times$. Hence
    $$\mathbf P \leftarrow \mathbf G_r\mathbf P\mathbf G_r^\top,\qquad \mathbf G_r = \begin{bmatrix}\mathbf I - \tfrac12[\delta\hat{\boldsymbol\theta}]_\times & \mathbf 0\\ \mathbf 0 & \mathbf I\end{bmatrix}.$$
    The corrections are small, so $\mathbf G_r \approx \mathbf I$ and many implementations skip this step; it costs almost nothing, so we keep it. For a fuller treatment of every step, see @sola2017.

    **Initialization.** Start from the snapshot attitude of the first accelerometer and magnetometer sample, $\hat{\mathbf b}_g = \mathbf 0$, and a covariance that reflects how wrong these can be, here $\mathbf P_0 = \operatorname{diag}\big((5^\circ)^2\mathbf I,\ (0.02\text{ rad/s})^2\mathbf I\big)$.
    """)
    return


@app.cell(hide_code=True)
def _(jacobian_check, mo):
    mo.md(rf"""
    Every Jacobian above was derived to first order, so it is worth checking numerically. Perturbing the attitude error by $\pm 10^{{-6}}$ rad along each axis at a random attitude and differencing the exact nonlinear expressions gives

    {jacobian_check}

    The differences are at the level of the finite-difference error for $\mathbf H_{{\text{{acc}}}}$, $\mathbf H_{{\text{{mag}}}}$, and $\mathbf G_r$. For $\boldsymbol\Phi_k$ the remaining difference comes from the second-order terms the theorem neglects; it shrinks in proportion to the size of the errors.
    """)
    return


@app.cell
def _(Exp, GRAVITY, G_N, Log, M_N, np, skew):
    # jb: include=false
    _rng = np.random.default_rng(3)
    _Rh = Exp(_rng.normal(size=3))
    _eps = 1e-6

    def _fd(fun, x0):
        _J = np.zeros((3, 3))
        for _i in range(3):
            _e = np.zeros(3)
            _e[_i] = _eps
            _J[:, _i] = (fun(x0 + _e) - fun(x0 - _e)) / (2 * _eps)
        return _J

    _z = np.zeros(3)
    _Ha = _fd(lambda d: (_Rh @ Exp(d)).T @ (-G_N), _z)
    _Hm = _fd(lambda d: (_Rh @ Exp(d)).T @ M_N, _z)
    _dhat = np.array([0.02, -0.015, 0.01])
    _Gr = _fd(lambda d: Log(Exp(_dhat).T @ Exp(d)), _dhat)
    # one-step propagation of a small attitude error with a bias error, against Phi_k
    _dt, _wm = 0.01, np.array([0.8, -1.5, 2.0])
    _b_true, _b_hat = np.array([0.01, -0.01, 0.01]), np.zeros(3)
    _d0 = np.array([0.002, -0.001, 0.003])
    _R0 = _Rh @ Exp(_d0)
    _R1 = _R0 @ Exp((_wm - _b_true) * _dt)
    _Rh1 = _Rh @ Exp((_wm - _b_hat) * _dt)
    _d1 = Log(_Rh1.T @ _R1)
    _d1_pred = Exp((_wm - _b_hat) * _dt).T @ _d0 - _dt * (_b_true - _b_hat)
    _rows = [
        ("accelerometer Jacobian $\\mathbf H_{\\text{acc}}$ (attitude block)", np.abs(_Ha - skew(_Rh.T @ (-G_N))).max(), GRAVITY),
        ("magnetometer Jacobian $\\mathbf H_{\\text{mag}}$ (attitude block)", np.abs(_Hm - skew(_Rh.T @ M_N)).max(), np.linalg.norm(M_N)),
        ("reset Jacobian $\\mathbf G_r$ (attitude block)", np.abs(_Gr - (np.eye(3) - 0.5 * skew(_dhat))).max(), 1.0),
        ("one step of $\\boldsymbol\\Phi_k$ versus exact propagation", np.abs(_d1 - _d1_pred).max(), np.abs(_d1).max()),
    ]
    jacobian_check = "\n".join(
        ["| quantity | largest difference | typical entry size |", "|:---|:---:|:---:|"]
        + [f"| {_name} | {_diff:.1e} | {_size:.1e} |" for _name, _diff, _size in _rows]
    )
    return (jacobian_check,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch19-sec-implementation -->
    ### Implementation

    The whole filter fits in one function. Each step predicts with the gyroscope, then (optionally) updates with the accelerometer and the magnetometer. The `gate` option skips an accelerometer update when $\big|\|\mathbf f_m\| - g\big| > 0.5$ m/s$^2$ and a magnetometer update when $\big|\|\mathbf m_m\| - \|\mathbf m^n\|\big| > 2\ \mu$T; we discuss it under failure modes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ```python
    def ahrs_eskf(w_m, f_m, m_m, dt, q0, P0, sigma_g=0.01, sigma_bg=1e-5,
                  sigma_acc=1.0, sigma_mag=0.5, use_mag=True, gate=True):
        "\"\"Error-state Kalman filter for attitude and gyroscope bias.
        Row i of w_m covers the interval ending at sample i of f_m and m_m.
        Returns quaternions q^n_b, bias estimates, and 6x6 error covariances."\"\"
        n = len(w_m)
        q, b, P = q0.copy(), np.zeros(3), P0.copy()
        Q = np.diag([(sigma_g * dt) ** 2] * 3 + [sigma_bg ** 2 * dt] * 3)
        R_acc, R_mag = sigma_acc ** 2 * np.eye(3), sigma_mag ** 2 * np.eye(3)
        Phi = np.eye(6)
        Phi[0:3, 3:6] = -dt * np.eye(3)
        q_hist, b_hist, P_hist = np.zeros((n, 4)), np.zeros((n, 3)), np.zeros((n, 6, 6))

        def update(q, b, P, z, h, R_meas):
            H = np.zeros((3, 6))
            H[:, 0:3] = skew(h)                        # d h / d(dtheta) = [h]x
            S = H @ P @ H.T + R_meas
            K = P @ H.T @ np.linalg.inv(S)
            dx = K @ (z - h)
            IKH = np.eye(6) - K @ H
            P = IKH @ P @ IKH.T + K @ R_meas @ K.T     # Joseph form
            q = qmul(q, q_exp(dx[0:3]))                # inject attitude
            q = q / np.linalg.norm(q)
            b = b + dx[3:6]                            # inject bias
            G_r = np.eye(6)
            G_r[0:3, 0:3] -= 0.5 * skew(dx[0:3])       # reset
            return q, b, G_r @ P @ G_r.T

        for k in range(n):
            # predict: nominal state with the exact quaternion update, covariance with Phi
            w_hat = w_m[k] - b
            q = qmul(q, q_exp(w_hat * dt))
            Phi[0:3, 0:3] = Exp(w_hat * dt).T
            P = Phi @ P @ Phi.T + Q
            # accelerometer (gravity) update
            if not gate or abs(np.linalg.norm(f_m[k]) - GRAVITY) < 0.5:
                q, b, P = update(q, b, P, f_m[k], q_to_R(q).T @ (-G_N), R_acc)
            # magnetometer update
            if use_mag and (not gate or abs(np.linalg.norm(m_m[k]) - np.linalg.norm(M_N)) < 2.0):
                q, b, P = update(q, b, P, m_m[k], q_to_R(q).T @ M_N, R_mag)
            q_hist[k], b_hist[k], P_hist[k] = q, b, P
        return q_hist, b_hist, P_hist
    ```
    """)
    return


@app.cell
def eskf_code(Exp, GRAVITY, G_N, M_N, np, q_exp, q_to_R, qmul, skew):
    # jb: include=false
    def ahrs_eskf(w_m, f_m, m_m, dt, q0, P0, sigma_g=0.01, sigma_bg=1e-5,
                  sigma_acc=1.0, sigma_mag=0.5, use_mag=True, gate=True):
        """Error-state Kalman filter for attitude and gyroscope bias.
        Row i of w_m covers the interval ending at sample i of f_m and m_m.
        Returns quaternions q^n_b, bias estimates, and 6x6 error covariances."""
        n = len(w_m)
        q, b, P = q0.copy(), np.zeros(3), P0.copy()
        Q = np.diag([(sigma_g * dt) ** 2] * 3 + [sigma_bg ** 2 * dt] * 3)
        R_acc, R_mag = sigma_acc ** 2 * np.eye(3), sigma_mag ** 2 * np.eye(3)
        Phi = np.eye(6)
        Phi[0:3, 3:6] = -dt * np.eye(3)
        q_hist, b_hist, P_hist = np.zeros((n, 4)), np.zeros((n, 3)), np.zeros((n, 6, 6))

        def update(q, b, P, z, h, R_meas):
            H = np.zeros((3, 6))
            H[:, 0:3] = skew(h)                        # d h / d(dtheta) = [h]x
            S = H @ P @ H.T + R_meas
            K = P @ H.T @ np.linalg.inv(S)
            dx = K @ (z - h)
            IKH = np.eye(6) - K @ H
            P = IKH @ P @ IKH.T + K @ R_meas @ K.T     # Joseph form
            q = qmul(q, q_exp(dx[0:3]))                # inject attitude
            q = q / np.linalg.norm(q)
            b = b + dx[3:6]                            # inject bias
            G_r = np.eye(6)
            G_r[0:3, 0:3] -= 0.5 * skew(dx[0:3])       # reset
            return q, b, G_r @ P @ G_r.T

        for k in range(n):
            # predict: nominal state with the exact quaternion update, covariance with Phi
            w_hat = w_m[k] - b
            q = qmul(q, q_exp(w_hat * dt))
            Phi[0:3, 0:3] = Exp(w_hat * dt).T
            P = Phi @ P @ Phi.T + Q
            # accelerometer (gravity) update
            if not gate or abs(np.linalg.norm(f_m[k]) - GRAVITY) < 0.5:
                q, b, P = update(q, b, P, f_m[k], q_to_R(q).T @ (-G_N), R_acc)
            # magnetometer update
            if use_mag and (not gate or abs(np.linalg.norm(m_m[k]) - np.linalg.norm(M_N)) < 2.0):
                q, b, P = update(q, b, P, m_m[k], q_to_R(q).T @ M_N, R_mag)
            q_hist[k], b_hist[k], P_hist[k] = q, b, P
        return q_hist, b_hist, P_hist

    return (ahrs_eskf,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch19-sec-simulation -->
    ## Simulation

    The simulator produces one minute of synthetic motion at 100 Hz. The true attitude follows smooth Euler angles: roll oscillating $\pm 25^\circ$ at 0.15 Hz, pitch $\pm 20^\circ$ at 0.1 Hz, and yaw swinging between $-30^\circ$ and $90^\circ$ over 50 s. The true body rate over each sample period is the exact one, $\boldsymbol\omega_k = \operatorname{Log}(\mathbf R_{k-1}^\top\mathbf R_k)/\Delta t$. The body is also shaken by a linear acceleration of adjustable amplitude: sinusoids at 0.5 Hz (East) and 0.37 Hz (North), and half the amplitude at 0.9 Hz (Up). The sensors follow the models above with the default noise levels, a gyroscope bias of the chosen magnitude on each axis (with signs $+, -, +$), and optionally the default accelerometer bias and a 10-second magnetic disturbance of $[20, 10, 0]\ \mu$T (as if walking past a steel cabinet). The noise realization is the same for every setting, so differences between runs are caused only by the settings.

    The plots show the filter's attitude error expressed in navigation coordinates, $\hat{\mathbf R}\,\delta\boldsymbol\theta$ with $\delta\boldsymbol\theta = \operatorname{Log}(\hat{\mathbf R}^\top\mathbf R)$ (Chapter 17's small-angle consequence 3), because its components have direct meanings: rotation errors about East and North are tilt errors, and the error about Up is the heading error. The shaded bands are $\pm 2\sigma$ from the filter's own covariance, transformed the same way ($\hat{\mathbf R}\mathbf P_{\theta\theta}\hat{\mathbf R}^\top$). The last panel compares the bias estimates (colored) with the true biases (dashed).
    """)
    return


@app.cell
def imu_simulator(
    ACCEL_BIAS,
    DT,
    G_N,
    Log,
    M_N,
    SIGMA_A,
    SIGMA_G,
    SIGMA_M,
    euler_to_R,
    euler_to_q,
    np,
):
    # jb: include=false
    def simulate_imu(T=60.0, lin_acc=1.0, gyro_bias=0.01, accel_bias=True, mag_disturbance=False, seed=7):
        _N = int(round(T / DT))
        _t = np.arange(_N + 1) * DT
        _phi = np.radians(25) * np.sin(2 * np.pi * 0.15 * _t)
        _theta = np.radians(20) * np.sin(2 * np.pi * 0.10 * _t + 0.5)
        _psi = np.radians(30) + np.radians(60) * np.sin(2 * np.pi * 0.02 * _t)
        _R = np.array([euler_to_R(*_e) for _e in zip(_phi, _theta, _psi)])
        _q = np.array([euler_to_q(*_e) for _e in zip(_phi, _theta, _psi)])
        _omega = np.array([Log(_R[_k - 1].T @ _R[_k]) for _k in range(1, _N + 1)]) / DT
        _a_n = lin_acc * np.column_stack([np.sin(2 * np.pi * 0.5 * _t),
                                          np.sin(2 * np.pi * 0.37 * _t + 1.0),
                                          0.5 * np.sin(2 * np.pi * 0.9 * _t + 2.0)])
        _f_true = np.einsum("kji,kj->ki", _R, _a_n - G_N)
        _m_field = np.tile(M_N, (_N + 1, 1))
        if mag_disturbance:
            _m_field[(_t > 35) & (_t < 45)] += np.array([20.0, 10.0, 0.0])
        _m_true = np.einsum("kji,kj->ki", _R, _m_field)
        _rng = np.random.default_rng(seed)
        _b_g = gyro_bias * np.array([1.0, -1.0, 1.0])
        _b_a = ACCEL_BIAS * np.array([1.0, -1.0, 1.0]) if accel_bias else np.zeros(3)
        _w_m = _omega + _b_g + SIGMA_G * _rng.normal(size=(_N, 3))
        _f_m = _f_true + _b_a + SIGMA_A * _rng.normal(size=(_N + 1, 3))
        _m_m = _m_true + SIGMA_M * _rng.normal(size=(_N + 1, 3))
        return dict(t=_t, q_true=_q, b_g=_b_g, w_m=_w_m, f_m=_f_m, m_m=_m_m)

    return (simulate_imu,)


@app.cell
def _(
    DT,
    ahrs_eskf,
    euler_to_q,
    heading_from_mag,
    np,
    q_exp,
    qmul,
    qmul_arr,
    tilt_from_accel,
):
    # jb: include=false
    def _q_to_R_arr(Q):
        _w, _x, _y, _z = Q.T
        return np.stack([np.column_stack([1 - 2 * (_y**2 + _z**2), 2 * (_x * _y - _w * _z), 2 * (_x * _z + _w * _y)]),
                         np.column_stack([2 * (_x * _y + _w * _z), 1 - 2 * (_x**2 + _z**2), 2 * (_y * _z - _w * _x)]),
                         np.column_stack([2 * (_x * _z - _w * _y), 2 * (_y * _z + _w * _x), 1 - 2 * (_x**2 + _y**2)])],
                        axis=1)

    def _angle_deg(Q_true, Q_est):
        _r = qmul_arr(Q_est * np.array([1.0, -1.0, -1.0, -1.0]), Q_true)
        return np.degrees(2 * np.arctan2(np.linalg.norm(_r[:, 1:], axis=1), np.abs(_r[:, 0])))

    def snapshot_q(f, m):
        _roll, _pitch = tilt_from_accel(f)
        return euler_to_q(_roll, _pitch, heading_from_mag(m, _roll, _pitch))

    def run_ahrs(sim, sigma_acc=1.0, use_mag=True, gate=True):
        """Run the filter on a simulation and collect everything the plots need."""
        _q0 = snapshot_q(sim["f_m"][0], sim["m_m"][0])
        _P0 = np.diag([np.radians(5.0) ** 2] * 3 + [0.02**2] * 3)
        _Q, _B, _P = ahrs_eskf(sim["w_m"], sim["f_m"][1:], sim["m_m"][1:], DT, _q0, _P0,
                               sigma_acc=sigma_acc, use_mag=use_mag, gate=gate)
        _Qt = sim["q_true"][1:]
        # body-frame error dtheta = Log(q_hat* q_true) (Hamilton product), then rotated into navigation axes
        _r = qmul_arr(_Q * np.array([1.0, -1.0, -1.0, -1.0]), _Qt)
        _r = _r * np.sign(_r[:, :1] + 1e-300)
        _vn = np.linalg.norm(_r[:, 1:], axis=1, keepdims=True)
        _dth = 2 * np.arctan2(_vn, _r[:, :1]) * _r[:, 1:] / np.maximum(_vn, 1e-300)
        _Rh = _q_to_R_arr(_Q)
        _err_n = np.einsum("kij,kj->ki", _Rh, _dth)
        _sig_n = np.sqrt(np.einsum("kii->ki", _Rh @ _P[:, 0:3, 0:3] @ np.transpose(_Rh, (0, 2, 1))))
        # gyroscope-only integration and per-sample snapshot attitude, for comparison
        _qg = _q0.copy()
        _Qg = np.zeros_like(_Q)
        for _k in range(len(_Q)):
            _qg = qmul(_qg, q_exp(sim["w_m"][_k] * DT))
            _Qg[_k] = _qg
        _Qs = np.array([snapshot_q(_f, _m) for _f, _m in zip(sim["f_m"][1:], sim["m_m"][1:])])
        return dict(t=sim["t"][1:], err_n=np.degrees(_err_n), sig_n=np.degrees(_sig_n), b_hat=_B,
                    b_true=sim["b_g"], ang_eskf=_angle_deg(_Qt, _Q), ang_gyro=_angle_deg(_Qt, _Qg),
                    ang_snap=_angle_deg(_Qt, _Qs))

    return (run_ahrs,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch19-sec-interactive-the-error-state-filter-at-work -->
    ### Interactive: The Error-State Filter at Work

    The default settings are a realistic, well-behaved case. Then try the failure modes discussed below: switch off the magnetometer, add the magnetic disturbance (with and without gating), turn up the linear acceleration with a small $\sigma_{\text{acc}}$ and gating off, or remove the accelerometer bias to see the filter become consistent.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    ek_bias = mo.ui.slider(0.0, 0.05, 0.005, value=0.01, label="gyroscope bias per axis (rad/s)", show_value=True)
    ek_acc = mo.ui.slider(0.0, 3.0, 0.25, value=1.0, label=r"linear acceleration amplitude (m/s$^2$)", show_value=True)
    ek_sig = mo.ui.slider(steps=[0.05, 0.1, 0.2, 0.5, 1.0, 2.0], value=1.0,
                          label=r"filter's $\sigma_{\text{acc}}$ (m/s$^2$)", show_value=True)
    ek_mag = mo.ui.checkbox(value=True, label="use magnetometer")
    ek_gate = mo.ui.checkbox(value=True, label="gate accelerometer and magnetometer")
    ek_abias = mo.ui.checkbox(value=True, label="accelerometer bias")
    ek_dist = mo.ui.checkbox(value=False, label="magnetic disturbance (35–45 s)")
    return ek_abias, ek_acc, ek_bias, ek_dist, ek_gate, ek_mag, ek_sig


@app.cell
def _(ek_abias, ek_acc, ek_bias, ek_dist, ek_gate, ek_mag, ek_sig, run_ahrs, simulate_imu):
    # jb: include=false
    ek_result = run_ahrs(
        simulate_imu(lin_acc=ek_acc.value, gyro_bias=ek_bias.value, accel_bias=ek_abias.value,
                     mag_disturbance=ek_dist.value),
        sigma_acc=float(ek_sig.value), use_mag=ek_mag.value, gate=ek_gate.value,
    )
    return (ek_result,)


@app.cell(hide_code=True)
def _(
    ek_abias,
    ek_acc,
    ek_bias,
    ek_dist,
    ek_gate,
    ek_mag,
    ek_result,
    ek_sig,
    graphic,
    mo,
    np,
    plt,
):
    _r = ek_result
    _t = _r["t"]
    _fig, _axs = plt.subplots(2, 2, figsize=(10.5, 6.2), sharex=True)
    _names = ["about East (tilt)", "about North (tilt)", "about Up (heading)"]
    for _i, _ax in enumerate([_axs[0, 0], _axs[0, 1], _axs[1, 0]]):
        _ax.fill_between(_t, -2 * _r["sig_n"][:, _i], 2 * _r["sig_n"][:, _i], color="C1", alpha=0.2,
                         lw=0, label=r"$\pm 2\sigma$")
        _ax.plot(_t, _r["err_n"][:, _i], color="C1", lw=0.9, label="error")
        _ax.axhline(0, color="k", lw=0.6)
        _lim = max(1.0, 1.15 * np.abs(_r["err_n"][200:, _i]).max(), 2.3 * _r["sig_n"][200:, _i].max())
        _ax.set_ylim(-_lim, _lim)
        _ax.set_ylabel("error (deg)")
        _ax.set_title(f"Attitude error {_names[_i]}", style="italic", fontsize=10)
        _ax.legend(fontsize=8, loc="upper right")
    _axb = _axs[1, 1]
    for _i, _ls in enumerate(["-", "--", ":"]):
        _axb.plot(_t, _r["b_hat"][:, _i], color=f"C{_i}", lw=1.2, label=f"estimate, axis {'xyz'[_i]}")
        _axb.axhline(_r["b_true"][_i], color=f"C{_i}", ls="--", lw=0.8)
    _axb.set_ylabel("gyroscope bias (rad/s)")
    _axb.set_title("Bias estimates (dashed: truth)", style="italic", fontsize=10)
    _axb.legend(fontsize=8, loc="lower right")
    for _ax in _axs.flat:
        _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    for _ax in _axs[1]:
        _ax.set_xlabel("time (s)")
    _fig.tight_layout()

    _late = _t > 10
    _within = (np.abs(_r["err_n"]) <= 2 * _r["sig_n"])[_late].mean(axis=0)
    _table = "\n".join([
        "| method | RMS attitude error, t > 10 s | final attitude error |",
        "|:---|:---:|:---:|",
        rf"| gyroscope only | {np.sqrt(np.mean(_r['ang_gyro'][_late] ** 2)):.2f}$^\circ$ | {_r['ang_gyro'][-1]:.2f}$^\circ$ |",
        rf"| accelerometer + magnetometer snapshot | {np.sqrt(np.mean(_r['ang_snap'][_late] ** 2)):.2f}$^\circ$ | {_r['ang_snap'][-1]:.2f}$^\circ$ |",
        rf"| error-state Kalman filter | {np.sqrt(np.mean(_r['ang_eskf'][_late] ** 2)):.2f}$^\circ$ | {_r['ang_eskf'][-1]:.2f}$^\circ$ |",
    ])
    _cons = mo.md(
        _table + "\n\n"
        + r"Fraction of time ($t > 10$ s) the filter's error lies inside its own $\pm 2\sigma$ band: "
        + f"East {100 * _within[0]:.0f}%, North {100 * _within[1]:.0f}%, Up {100 * _within[2]:.0f}% "
        + "(about 95% is expected for a consistent filter)."
    )
    _out = mo.vstack([
        mo.hstack([ek_bias, ek_acc, ek_sig], justify="start"),
        mo.hstack([ek_mag, ek_gate, ek_abias, ek_dist], justify="start"),
        graphic(_fig),
        _cons,
    ])
    plt.close(_fig)
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With the default settings (gyroscope bias $0.01$ rad/s, linear acceleration $1$ m/s$^2$, $\sigma_{\text{acc}} = 1$ m/s$^2$, accelerometer bias on), the three approaches compare as follows. Gyroscope integration alone is off by about $34^\circ$ RMS and $50^\circ$ at the end; the accelerometer-and-magnetometer snapshot never drifts but is about $10^\circ$ wrong at any instant, almost entirely because of the linear acceleration; the error-state filter stays below $1^\circ$. Its bias estimates lock onto the truth within about ten seconds; this is what lets it outperform the complementary filter, whose bias error $b\tau$ never goes away. Raising the gyroscope bias to $0.05$ rad/s makes gyroscope-only integration useless (over $130^\circ$ RMS) but barely changes the filter.

    The tilt error about East stays inside its $\pm 2\sigma$ band, but the errors about North and Up sit at a constant offset, outside it, about half the time. The filter is *inconsistent* ({term}`filter consistency`, [Chapter 9](#ch9-sec-checking-the-noise-levels)). The cause is the accelerometer bias, which the six-state model does not contain: uncheck "accelerometer bias" and all three components stay inside their bands about 95–99% of the time. The next section explains why the filter cannot simply learn this bias.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch19-sec-failure-modes -->
    ## Failure Modes

    Every measurement model above rested on an assumption. Here is what happens when each fails, with settings you can reproduce in the interactive simulation.

    **Linear acceleration.** The accelerometer update assumed $\mathbf a^n \approx \mathbf 0$. With the linear-acceleration amplitude at $3$ m/s$^2$, a filter that trusts the accelerometer ($\sigma_{\text{acc}} = 0.05$ m/s$^2$, gating off) tilts to follow the apparent gravity and is off by about $11^\circ$ RMS. Three remedies, in increasing sophistication:

    1. *Inflate $\mathbf R_{\text{acc}}$.* With $\sigma_{\text{acc}} = 2$ m/s$^2$ the same run has errors around $1.4^\circ$. The cost is slower correction when the body really is still.
    2. *Gate on the magnitude.* At rest $\|\mathbf f\| = g$, so skip the update when $\big|\|\mathbf f_m\| - g\big|$ is large. This catches vertical accelerations but is weak against horizontal ones: a horizontal acceleration $a$ changes the magnitude only to $\sqrt{g^2 + a^2} \approx g + a^2/(2g)$, so $2$ m/s$^2$ sideways changes it by only $0.2$ m/s$^2$. In the simulation, gating alone (with $\sigma_{\text{acc}} = 0.05$) reduces the error only to about $6.5^\circ$. An *adaptive* covariance, for example $\mathbf R_{\text{acc}} = \big(\sigma_{\text{acc}}^2 + c\,(\|\mathbf f_m\| - g)^2\big)\mathbf I$, is a smooth version of the same idea with the same weakness.
    3. *Gate on the innovation.* [Chapter 14](#ch14-sec-outlier-gating)'s {term}`gating` with the {term}`normalized innovation squared` rejects any accelerometer reading inconsistent with the predicted gravity direction, whatever its magnitude. Foot-mounted systems go further and use gravity only while the foot is detected to be stationary ([Chapter 21](#ch21)).

    **Magnetic disturbances.** Check "magnetic disturbance": between 35 and 45 s the field is distorted by $[20, 10, 0]\ \mu$T. Without gating, the heading error reaches about $30^\circ$ and, because the magnetometer update uses the full field vector, the tilt is dragged off by more than $10^\circ$ as well. With gating the disturbed readings are rejected (the field magnitude rises from $47.4$ to $56.5\ \mu$T) and the filter coasts on the gyroscope with almost no penalty. Magnitude gating misses a disturbance that rotates the field without changing its strength, so practical systems also check the *dip angle* between $\mathbf f_m$ and $\mathbf m_m$ (it should be $90^\circ + 62^\circ$ at rest), and many apply the magnetometer only to heading, projecting its innovation onto the horizontal plane so that it cannot corrupt the tilt.

    **No magnetometer: heading is unobservable.** Uncheck "use magnetometer". As shown above, gravity carries no heading information, so nothing corrects the heading error: it wanders (about $12^\circ$ RMS in this run), and the filter knows it, since its heading $\sigma$ grows steadily (to about $10^\circ$ after a minute) while the tilt stays accurate. The gyroscope-bias component along the vertical is also poorly observable, because a vertical bias error looks exactly like a slow heading change; it becomes partly observable only because this body keeps tilting. Chapter 21 meets the same problem with the foot-mounted filter, where heading and vertical gyroscope bias are unobservable from zero-velocity updates.

    **Accelerometer bias.** For a body at rest, a horizontal accelerometer bias $b$ and a tilt of $b/g$ radians produce identical readings, so no amount of data from the accelerometer alone can separate them; this is a failure of {term}`observability`, not of tuning. Our $0.05$ m/s$^2$ bias becomes a constant tilt error of about $0.3^\circ$. The magnetometer then turns it into a heading error up to about $\tan 62^\circ \approx 1.9$ times larger, because the leveling step misreads part of the steep vertical field as horizontal. Calibration (Chapter 11) is the practical remedy; motion with varying attitude makes the bias weakly observable, which is why Chapter 21's 15-state filter includes it.

    **Large initial errors.** The Jacobians are first-order. Starting from the snapshot attitude keeps the initial error to a few degrees, where linearization is excellent. Starting from an arbitrary attitude with a small $\mathbf P_0$ can make the first corrections point the wrong way ([Chapter 15](#ch15-sec-large-initial-error)'s failure modes).

    /// caution | ⚠️ **Assumptions and Failure Modes**
    The error-state filter of this chapter assumes:

    - a gyroscope with white noise and a constant or slowly wandering bias, sampled fast enough that the rate is nearly constant over each sample;
    - no linear acceleration when the accelerometer is used, and no accelerometer bias (both are absorbed, imperfectly, by an inflated $\sigma_{\text{acc}}$);
    - an undisturbed, calibrated magnetic field of known direction;
    - attitude errors small enough for the first-order Jacobians, which the reset keeps true once the filter has converged.

    When the second or third assumption fails, the filter's covariance no longer describes its errors: it becomes overconfident, and gating or adaptive noise is needed to keep it honest. When a sensor is missing, the corresponding attitude component becomes unobservable and its uncertainty grows without bound.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch19-sec-mahony-and-madgwick-filters -->
    ## Mahony and Madgwick Filters

    Two lighter-weight attitude filters are so widely used, especially on microcontrollers, that they deserve a mention.

    The **Mahony filter** [@mahony2008] is the complementary filter done properly in three dimensions. With unit reference directions $\mathbf v^n_i$ (Up and magnetic north), their measured body-frame directions $\mathbf v_i$ (normalized $\mathbf f_m$ and $\mathbf m_m$), and their predictions $\hat{\mathbf v}_i := \hat{\mathbf R}^\top\mathbf v^n_i$, it forms the correction rate $\boldsymbol\omega_c := \sum_i k_i\,\mathbf v_i\times\hat{\mathbf v}_i$ and integrates
    $$\dot{\hat q} = \tfrac12\,\hat q\otimes\big[0,\ \boldsymbol\omega_m - \hat{\mathbf b}_g + k_P\,\boldsymbol\omega_c\big],\qquad \dot{\hat{\mathbf b}}_g = -k_I\,\boldsymbol\omega_c.$$
    By the measurement-Jacobian theorem, if $\mathbf R = \hat{\mathbf R}\operatorname{Exp}(\delta\boldsymbol\theta)$ then $\mathbf v_i \approx \hat{\mathbf v}_i + \hat{\mathbf v}_i\times\delta\boldsymbol\theta$, and the triple-product expansion gives $\mathbf v_i\times\hat{\mathbf v}_i \approx \|\hat{\mathbf v}_i\|^2\,\delta\boldsymbol\theta_\perp$, the part of the attitude error perpendicular to $\hat{\mathbf v}_i$. So the proportional term rotates the estimate toward the truth (as the gain $\alpha$ did in the scalar complementary filter), and the integral term drives the bias estimate until the correction vanishes, which removes the $b\tau$ error.

    The **Madgwick filter** [@madgwick2011] instead takes one gradient-descent step per sample on the mismatch $\|\hat q^*\otimes[0, \mathbf v^n_i]\otimes\hat q - [0, \mathbf v_i]\|^2$ and blends that step with the gyroscope-integrated quaternion through a single gain.

    Both need only a handful of operations per sample, have one or two gains instead of covariance matrices, and are robust in practice. What they do not provide is an uncertainty estimate, a principled way to weight sensors of different quality, or a framework that extends to more states. That framework, the error-state Kalman filter, is exactly what Chapter 21 extends from 6 states to 15.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch19-sec-summary -->
    ## Summary

    - An {term}`inertial measurement unit` combines a {term}`gyroscope`, which measures $\boldsymbol\omega^b$, and an {term}`accelerometer`, which measures the {term}`specific force` $\mathbf f^b = (\mathbf R^n_b)^\top(\mathbf a^n - \mathbf g^n)$, reading $[0, 0, g]$ at rest and level. A {term}`magnetometer` measures $(\mathbf R^n_b)^\top\mathbf m^n$. All three have noise; the inertial sensors also have bias.
    - At rest, the accelerometer gives roll $\phi = \operatorname{atan2}(f_y, f_z)$ and pitch $\theta = \operatorname{atan2}(-f_x, \sqrt{f_y^2 + f_z^2})$ but no heading. The magnetometer, leveled by roll and pitch, gives the {term}`heading` $\psi = \operatorname{atan2}(m_{h,x}, m_{h,y})$. Together they give a drift-free but noisy and easily disturbed snapshot {term}`attitude`.
    - Integrating the gyroscope gives smooth attitude whose error grows like $b\,t$ (bias) plus a random walk of standard deviation $\sigma_g\sqrt{\Delta t\,t}$ (noise).
    - The scalar {term}`complementary filter` is exactly the Introduction's alpha filter with $\Delta x_k = \omega_{m,k}\Delta t$. It low-passes the accelerometer and high-passes the gyroscope with filters that sum to the identity. Its time constant is $\tau = \Delta t(1-\alpha)/\alpha$, a constant gyroscope bias leaves an error $b\tau$, and the crossover frequency is $1/(2\pi\tau)$.
    - The {term}`error-state Kalman filter` keeps the attitude as a quaternion $\hat q$ and estimates the small error $\delta\boldsymbol\theta$ in $q = \hat q\otimes\delta q(\delta\boldsymbol\theta)$, together with the gyroscope-bias error. Its error dynamics are $\dot{\delta\boldsymbol\theta} = -[\hat{\boldsymbol\omega}]_\times\delta\boldsymbol\theta - \delta\mathbf b_g - \mathbf n_g$, its measurement matrices are $\big[[\hat{\mathbf h}]_\times\ \ \mathbf 0\big]$ for gravity and the magnetic field, and after each update the error is injected into $\hat q$ and reset.
    - Failure modes: linear acceleration corrupts tilt (inflate $\mathbf R_{\text{acc}}$ or gate), magnetic disturbances corrupt heading and, through the full-vector update, tilt (gate on magnitude and dip, or update heading only), heading is unobservable without a magnetometer, and accelerometer bias is indistinguishable from tilt.

    <!-- label: ch19-sec-whats-next -->
    ## What's Next

    An AHRS answers "which way is the body pointing?" [Chapter 20](#ch20) asks "where is it?" Rotating the specific force into the navigation frame, adding gravity back, and integrating twice gives velocity and position: strapdown inertial navigation. Every error studied here returns there, amplified: a tilt error of $0.3^\circ$ leaks $g\sin(0.3^\circ) \approx 0.05$ m/s$^2$ of gravity into the horizontal acceleration, which integrates to meters of position error within seconds. Chapter 20 derives how fast that happens and builds the walking-foot simulator that [Chapter 21](#ch21) then rescues with zero-velocity updates.
    """)
    return


if __name__ == "__main__":
    app.run()
