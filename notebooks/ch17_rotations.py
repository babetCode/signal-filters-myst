# /// script
# dependencies = [
#     "marimo>=0.25.1",
#     "matplotlib==3.11.2",
#     "numpy==2.5.3",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="17. Rotations", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "Frames, Matrices, and Singularities"
    abbreviations:
      ENU: east-north-up
      FLU: forward-left-up
      NED: north-east-down
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
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    from textwrap import dedent
    from pathlib import Path

    return Path, Poly3DCollection, dedent, mo, np, plt


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
    A sensor strapped to a shoe measures angular rate and acceleration along its *own* axes, and those axes tumble with every step. Gravity, the Earth's magnetic field, and the path walked are described in axes fixed to the ground. Every orientation filter in Parts V and VI therefore needs three things: a precise way to convert vectors between the two sets of axes, an equation for how that conversion changes as the body turns, and a map of where each description of orientation breaks down. This chapter supplies all three. Rotation matrices do the conversion, the angular-velocity equation $\dot{\mathbf R} = \mathbf R[\boldsymbol\omega]_\times$ describes its evolution, and gimbal lock is the breakdown that motivates quaternions in [Chapter 18](ch18_quaternions.md).

    /// attention | 🗝️ **Key Idea**
    The orientation of a body is a rotation matrix $\mathbf R^n_b$ that converts body coordinates into navigation coordinates. It evolves according to $\dot{\mathbf R}^n_b = \mathbf R^n_b[\boldsymbol\omega^b]_\times$, where $\boldsymbol\omega^b$ is what a gyroscope measures. Every description of orientation by only three numbers, such as yaw, pitch, and roll, is singular somewhere.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// important | 🔗 **Prerequisites**
    - [Chapter 12](ch12_vectors_matrices_covariance.md): [bold lowercase vectors and bold uppercase matrices](#ch12-sec-notation-and-linear-algebra-toolkit).
    - [Appendix D: Matrix Multiplication](#appd-sec-matrix-multiplication), [Transpose, Identity, and Inverse](#appd-sec-transpose-identity-and-inverse), and [Linear Independence, Basis, and Rank](#appd-sec-linear-independence-basis-and-rank): a matrix is determined by its action on a basis, and [a square matrix with a left inverse is invertible](#appd-thm-invertible-matrix-theorem).
    - [Appendix D: Determinants](#appd-sec-determinants): $\det(\mathbf A\mathbf B) = \det\mathbf A\det\mathbf B$, $\det\mathbf A^\top = \det\mathbf A$, and cofactor expansion of a $3\times 3$ determinant.
    - [Appendix D: Trace](#appd-sec-trace), [Orthogonal Matrices](#appd-sec-orthogonal-matrices), and [Eigenvalues and Eigenvectors](#appd-sec-eigenvalues-and-eigenvectors).
    - [Appendix D: Cross Products and Skew-Symmetric Matrices](#appd-sec-cross-products-and-skew-symmetric-matrices): $[\mathbf a]_\times\mathbf b = \mathbf a\times\mathbf b$, every $3\times 3$ skew-symmetric matrix is $[\mathbf a]_\times$ for exactly one $\mathbf a$, and [the triple-product expansion](#appd-thm-cross-product-identities) $\mathbf a\times(\mathbf b\times\mathbf c) = \mathbf b(\mathbf a\cdot\mathbf c) - \mathbf c(\mathbf a\cdot\mathbf b)$.
    - [Appendix D: The Matrix Exponential](#appd-sec-the-matrix-exponential): $\exp(\mathbf A) = \sum_{m\ge 0}\mathbf A^m/m!$, $\tfrac{d}{dt}\exp(t\mathbf A) = \mathbf A\exp(t\mathbf A) = \exp(t\mathbf A)\mathbf A$, and $\exp(\mathbf A + \mathbf B) = \exp(\mathbf A)\exp(\mathbf B)$ when $\mathbf A\mathbf B = \mathbf B\mathbf A$.
    - [Appendix C: Derivatives](#appc-sec-derivatives) ([the product rule](#appc-thm-differentiation-rules), applied entrywise to matrices) and [Appendix C: Exponential and Logarithm](#appc-sec-exponential-and-logarithm) (the power series and remainder bounds of $\sin$ and $\cos$).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch17-sec-reference-frames -->
    ## Reference Frames

    Picture an inertial sensor clipped to the top of a shoe. When you stand still facing east on level ground, the sensor's "forward" axis points east, its "left" axis points north, and its "up" axis points up. Take a step and all three sensor axes swing through space, while east, north, and up stay where they are. To talk about either set of axes precisely we need the notion of a frame.

    /// note | 📖 **Definition**
    <u>**Reference frame**</u>

    A reference frame $a$ is a point $O_a$ (its *origin*) together with an ordered triple $(\mathbf a_1, \mathbf a_2, \mathbf a_3)$ of mutually perpendicular unit vectors (its *axes*) that is right-handed: $\mathbf a_1\times\mathbf a_2 = \mathbf a_3$.
    ///

    Because the axes are perpendicular unit vectors, every vector $\mathbf v$ in space can be written in exactly one way as $\mathbf v = v_1\mathbf a_1 + v_2\mathbf a_2 + v_3\mathbf a_3$, with $v_i = \mathbf v\cdot\mathbf a_i$ (take the dot product of both sides with $\mathbf a_i$). The column $\mathbf v^a := [v_1, v_2, v_3]^\top \in \mathbb R^3$ is the **coordinate vector of $\mathbf v$ in frame $a$**. A superscript always names the frame. The arrow $\mathbf v$ is the same physical object in every frame; only its coordinates change. Dot and cross products of arrows can be computed from coordinates in any right-handed frame with the usual formulas of [Appendix D](appendix_d_linear_algebra.md), so we use the two interchangeably.

    This book uses two frames from here on:

    - **Navigation frame $n$:** local-level east-north-up (ENU). Its origin is a fixed point on the ground; $x$ points East, $y$ North, $z$ Up. Gravity is $\mathbf g^n = [0, 0, -g]^\top$ with $g = 9.81\ \text{m/s}^2$.
    - **Body frame $b$:** forward-left-up (FLU), rigidly attached to the sensor; $x$ points forward, $y$ left, $z$ up.

    At *zero attitude* the two frames' axes coincide: the body faces East, level.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch17_frames.svg" class="graphic" alt="Two 3-D sketches. Left: the body frame x, y, z axes coincide with the dashed East, North, Up navigation axes. Right: the body is yawed 35 degrees, pitched nose-up 20 degrees, and rolled 10 degrees, so its axes point away from East, North, Up." />
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **The navigation frame is treated as non-rotating.** In reality an ENU frame turns with the Earth at $7.29\times 10^{-5}$ rad/s (about 15$^\circ$/h). Gyroscopes measure rotation relative to non-rotating space, so we are ignoring a rate roughly 140 times smaller than the gyroscope bias we assume in [Chapter 19](#ch19-sec-measurement-models). Navigation-grade systems cannot ignore it.
    - **The navigation frame is treated as flat.** Over the few hundred meters of a walk, the Earth's curvature changes the direction of "up" by less than 0.01$^\circ$.
    - **Conventions differ between texts.** Aerospace texts often use north-east-down (NED) and forward-right-down axes. Mixing conventions silently flips signs, so every formula in Chapters 17–21 uses exactly the conventions above.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch17-sec-rotation-matrices -->
    ## Rotation Matrices

    Write a vector in body axes, $\mathbf v = v^b_1\mathbf b_1 + v^b_2\mathbf b_2 + v^b_3\mathbf b_3$, and take navigation coordinates of both sides. Coordinates are linear, so

    $$\mathbf v^n = v^b_1\mathbf b_1^n + v^b_2\mathbf b_2^n + v^b_3\mathbf b_3^n = \underbrace{\begin{bmatrix}\mathbf b_1^n & \mathbf b_2^n & \mathbf b_3^n\end{bmatrix}}_{=:\ \mathbf R^n_b}\mathbf v^b.$$

    So converting body coordinates to navigation coordinates is multiplication by the matrix $\mathbf R^n_b$ whose **columns are the body axes expressed in navigation coordinates**. Two properties of this matrix follow from the axes being a right-handed frame:

    - The $(i, j)$ entry of $(\mathbf R^n_b)^\top\mathbf R^n_b$ is $\mathbf b_i^n\cdot\mathbf b_j^n = \mathbf b_i\cdot\mathbf b_j$, which is $1$ if $i = j$ and $0$ otherwise. So $(\mathbf R^n_b)^\top\mathbf R^n_b = \mathbf I$.
    - Cofactor expansion along the third column shows that the determinant of any $3\times 3$ matrix with columns $\mathbf a, \mathbf b, \mathbf c$ is $(\mathbf a\times\mathbf b)\cdot\mathbf c$. Hence $\det\mathbf R^n_b = (\mathbf b_1\times\mathbf b_2)\cdot\mathbf b_3 = \mathbf b_3\cdot\mathbf b_3 = 1$.

    /// note | 📖 **Definition**
    <u>**Rotation matrix**</u>

    A rotation matrix is a real $3\times 3$ matrix $\mathbf R$ with $\mathbf R^\top\mathbf R = \mathbf I$ and $\det\mathbf R = +1$.
    ///

    /// note | 📖 **Definition**
    <u>**Special orthogonal group**</u>

    The special orthogonal group is the set of all rotation matrices,
    $$SO(3) := \{\mathbf R \in \mathbb R^{3\times 3} : \mathbf R^\top\mathbf R = \mathbf I,\ \det\mathbf R = 1\},$$
    together with matrix multiplication as its operation.
    ///

    The name says that $SO(3)$ is a *group*[^group]; the theorem below proves it. Conversely, every rotation matrix comes from a frame: its columns $\mathbf r_1, \mathbf r_2, \mathbf r_3$ are perpendicular unit vectors (because $\mathbf R^\top\mathbf R = \mathbf I$), so $\mathbf r_1\times\mathbf r_2$ is a unit vector perpendicular to both, hence $\pm\mathbf r_3$, and $\det\mathbf R = (\mathbf r_1\times\mathbf r_2)\cdot\mathbf r_3 = 1$ forces the plus sign. So rotation matrices and orientations of a right-handed frame relative to $n$ are the same thing.

    [^group]: A *group* is a set with an associative operation that has an identity element and an inverse for every element. Rotation matrices are associative because matrix multiplication is.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// admonition | 📐 **Theorem (Properties of Rotation Matrices)**
        attrs: {class: theorem, id: ch17-thm-properties-of-rotation-matrices}
    Let $\mathbf R, \mathbf R_1, \mathbf R_2 \in SO(3)$ and $\mathbf u, \mathbf v, \mathbf a \in \mathbb R^3$. Then

    1. $\mathbf R$ is invertible with $\mathbf R^{-1} = \mathbf R^\top$, so $\mathbf R\mathbf R^\top = \mathbf I$, and $\mathbf R^\top \in SO(3)$;
    2. $\mathbf I \in SO(3)$ and $\mathbf R_1\mathbf R_2 \in SO(3)$;
    3. $(\mathbf R\mathbf u)\cdot(\mathbf R\mathbf v) = \mathbf u\cdot\mathbf v$, and in particular $\|\mathbf R\mathbf v\| = \|\mathbf v\|$;
    4. $\mathbf R(\mathbf u\times\mathbf v) = (\mathbf R\mathbf u)\times(\mathbf R\mathbf v)$;
    5. $\mathbf R[\mathbf a]_\times\mathbf R^\top = [\mathbf R\mathbf a]_\times$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    1. $\mathbf R^\top\mathbf R = \mathbf I$ says $\mathbf R^\top$ is a left inverse of the square matrix $\mathbf R$, hence its inverse ([Appendix D: Transpose, Identity, and Inverse](#appd-sec-transpose-identity-and-inverse)), so $\mathbf R\mathbf R^\top = \mathbf I$ as well. Then $(\mathbf R^\top)^\top\mathbf R^\top = \mathbf R\mathbf R^\top = \mathbf I$ and $\det\mathbf R^\top = \det\mathbf R = 1$.
    2. $\mathbf I^\top\mathbf I = \mathbf I$ and $\det\mathbf I = 1$. Also $(\mathbf R_1\mathbf R_2)^\top\mathbf R_1\mathbf R_2 = \mathbf R_2^\top(\mathbf R_1^\top\mathbf R_1)\mathbf R_2 = \mathbf I$ and $\det(\mathbf R_1\mathbf R_2) = \det\mathbf R_1\det\mathbf R_2 = 1$.
    3. $(\mathbf R\mathbf u)\cdot(\mathbf R\mathbf v) = \mathbf u^\top\mathbf R^\top\mathbf R\mathbf v = \mathbf u^\top\mathbf v$. Take $\mathbf u = \mathbf v$ for the norm.
    4. For every $\mathbf c \in \mathbb R^3$, using the determinant formula above twice and item 3,
    $$\big((\mathbf R\mathbf u)\times(\mathbf R\mathbf v)\big)\cdot(\mathbf R\mathbf c) = \det\big(\mathbf R\begin{bmatrix}\mathbf u & \mathbf v & \mathbf c\end{bmatrix}\big) = \det\mathbf R\,\det\begin{bmatrix}\mathbf u & \mathbf v & \mathbf c\end{bmatrix} = (\mathbf u\times\mathbf v)\cdot\mathbf c = \big(\mathbf R(\mathbf u\times\mathbf v)\big)\cdot(\mathbf R\mathbf c).$$
    So $\mathbf d := (\mathbf R\mathbf u)\times(\mathbf R\mathbf v) - \mathbf R(\mathbf u\times\mathbf v)$ satisfies $\mathbf d\cdot\mathbf R\mathbf c = 0$ for every $\mathbf c$. Choosing $\mathbf c = \mathbf R^\top\mathbf d$ gives $\|\mathbf d\|^2 = 0$.
    5. For every $\mathbf b$, items 4 and 1 give $\mathbf R[\mathbf a]_\times\mathbf R^\top\mathbf b = \mathbf R(\mathbf a\times\mathbf R^\top\mathbf b) = (\mathbf R\mathbf a)\times(\mathbf R\mathbf R^\top\mathbf b) = [\mathbf R\mathbf a]_\times\mathbf b$. Matrices that agree on every vector are equal. $\blacksquare$
    ///

    Item 3 says rotations preserve lengths and angles; item 4 says they preserve handedness. Item 5 is the identity we use most: rotating a cross-product matrix is the same as rotating its vector.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch17-sec-passive-and-active-readings -->
    ### Passive and Active Readings

    The same matrix $\mathbf R^n_b$ can be read in two ways, and we use both:

    - **Passive (change of coordinates):** $\mathbf v^n = \mathbf R^n_b\mathbf v^b$ expresses one fixed arrow in a different frame. Nothing moves.
    - **Active (moving vectors):** applied to the navigation coordinates $\mathbf e_i$ of the $i$-th navigation axis, it returns $\mathbf R^n_b\mathbf e_i = \mathbf b_i^n$, the $i$-th body axis. So $\mathbf R^n_b$ is the rotation, written in navigation coordinates, that carries the navigation axes onto the body axes.

    The reverse conversion uses the inverse, $\mathbf R^b_n := (\mathbf R^n_b)^{-1} = (\mathbf R^n_b)^\top$, so $\mathbf v^b = (\mathbf R^n_b)^\top\mathbf v^n$. For a third frame $c$ (say, a sensor mounted on the shoe at an angle), $\mathbf v^n = \mathbf R^n_b\mathbf v^b = \mathbf R^n_b\mathbf R^b_c\mathbf v^c$, so

    $$\mathbf R^n_c = \mathbf R^n_b\,\mathbf R^b_c.$$

    Adjacent matching indices "cancel". The order matters, because matrix multiplication is not commutative; we will see a concrete example once we have elementary rotations.

    /// tip | **Notation in other texts**
    Other common names for $\mathbf R^n_b$ are the *direction cosine matrix* $\mathbf C^n_b$ and $\mathbf R_{nb}$. Some texts write $\mathbf R$ for our $\mathbf R^b_n$. Always check which way a matrix converts before using a formula from another source.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch17-sec-elementary-rotations-and-euler-angles -->
    ## Elementary Rotations and Euler Angles

    The simplest rotations turn about a single navigation axis. Rotating the navigation frame about its $z$ axis by an angle $\psi$, counterclockwise when seen from above, moves the $x$ axis to $[\cos\psi, \sin\psi, 0]^\top$ and the $y$ axis to $[-\sin\psi, \cos\psi, 0]^\top$, and leaves $z$ alone. Putting these as columns, and doing the same for the other two axes (the cyclic order is $x\to y\to z\to x$, so a rotation about $y$ turns $z$ toward $x$):

    $$\mathbf R_x(\phi) = \begin{bmatrix}1 & 0 & 0\\ 0 & \cos\phi & -\sin\phi\\ 0 & \sin\phi & \cos\phi\end{bmatrix},\quad
    \mathbf R_y(\theta) = \begin{bmatrix}\cos\theta & 0 & \sin\theta\\ 0 & 1 & 0\\ -\sin\theta & 0 & \cos\theta\end{bmatrix},\quad
    \mathbf R_z(\psi) = \begin{bmatrix}\cos\psi & -\sin\psi & 0\\ \sin\psi & \cos\psi & 0\\ 0 & 0 & 1\end{bmatrix}.$$

    Each is in $SO(3)$ (check $\mathbf R^\top\mathbf R = \mathbf I$ and $\det = \cos^2 + \sin^2 = 1$). They are **active and right-handed**: a positive angle turns counterclockwise when viewed from the positive end of the axis, looking toward the origin. Equivalently, with your right thumb along the axis, your fingers curl in the positive direction.

    /// note | 📖 **Definition**
    <u>**Euler angles**</u>

    The (ZYX, or yaw-pitch-roll) Euler angles of a rotation matrix $\mathbf R$ are any triple $(\phi, \theta, \psi) \in \mathbb R^3$ with
    $$\mathbf R = \mathbf R_z(\psi)\,\mathbf R_y(\theta)\,\mathbf R_x(\phi).$$
    $\phi$ is the *roll*, $\theta$ the *pitch*, and $\psi$ the *yaw*. We collect them as $\boldsymbol\Theta := [\phi, \theta, \psi]^\top$.
    ///

    Other texts use other axis sequences (ZXZ, XYZ, ...). In this book "Euler angles" always means ZYX with $\mathbf R = \mathbf R^n_b$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch17-sec-reading-the-product-as-three-motions -->
    ### Reading the Product as Three Motions

    /// admonition | 📐 **Lemma (Rotating About a Body Axis)**
        attrs: {class: lemma, id: ch17-lem-rotating-about-a-body-axis}
    If a frame $a$ has attitude $\mathbf R^n_a = \mathbf R_1$ and is then rotated by an angle $\gamma$ about its *own* $i$-th axis, the new frame $a'$ has attitude $\mathbf R^n_{a'} = \mathbf R_1\,\mathbf R_i(\gamma)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Relative to $a$, the frame $a'$ is obtained by an elementary rotation about $a$'s $i$-th axis, so by the same construction as above (with $a$ in place of $n$) $\mathbf R^a_{a'} = \mathbf R_i(\gamma)$. The composition rule gives $\mathbf R^n_{a'} = \mathbf R^n_a\mathbf R^a_{a'} = \mathbf R_1\mathbf R_i(\gamma)$. $\blacksquare$
    ///

    Starting from zero attitude ($\mathbf I$), the lemma applied three times shows that $\mathbf R_z(\psi)\mathbf R_y(\theta)\mathbf R_x(\phi)$ is the attitude reached by

    1. yawing by $\psi$ about the Up axis,
    2. then pitching by $\theta$ about the body's new $y$ axis,
    3. then rolling by $\phi$ about the body's newest $x$ axis.

    (Read right to left as active rotations of vectors, the same product also means: roll about the fixed East axis, then pitch about the fixed North axis, then yaw about Up.)

    Because our body axes are forward-left-up, the signs have the following meanings. Two of them are easy to get backwards:

    /// tip | **What the signs mean (FLU body, ENU navigation)**
    - **Yaw $\psi > 0$:** the nose turns from East toward North, counterclockwise seen from above (a left turn).
    - **Pitch $\theta > 0$: the nose goes *down*.** A right-handed turn about the left-pointing $y$ axis carries forward toward down: $\mathbf R_y(\theta)\mathbf e_x = [\cos\theta, 0, -\sin\theta]^\top$.
    - **Roll $\phi > 0$:** the left side goes up and the right side down: $\mathbf R_x(\phi)\mathbf e_y = [0, \cos\phi, \sin\phi]^\top$.

    In the NED/forward-right-down convention common in aerospace, positive pitch is nose *up* and positive yaw is a turn to the *right*.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(R_order_1, R_order_2, mo):
    mo.md(rf"""
    The order of the three factors matters. For example, $\mathbf R_z(90^\circ)\mathbf R_x(90^\circ)\mathbf e_x = {R_order_1}$ (rolling a forward-pointing vector does nothing, then yawing turns it north), whereas $\mathbf R_x(90^\circ)\mathbf R_z(90^\circ)\mathbf e_x = {R_order_2}$ (yawing turns it north, then rolling about East turns north into up).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch17-sec-from-matrix-to-angles -->
    ### From Matrix to Angles

    Recovering the angles from a matrix needs the two-argument arctangent. For $(x, y) \ne (0, 0)$, $\operatorname{atan2}(y, x)$ denotes the unique angle $a \in (-\pi, \pi]$ with $(x, y) = r(\cos a, \sin a)$ for some $r > 0$. (Unlike $\arctan(y/x)$, it knows which quadrant $(x, y)$ is in.)

    /// admonition | 📐 **Theorem (Euler Angles from a Rotation Matrix)**
        attrs: {class: theorem, id: ch17-thm-euler-angles-from-a-rotation-matrix}
    Write $r_{ij}$ for the entries of $\mathbf R \in SO(3)$ and $c_\theta := \cos\theta$, $s_\theta := \sin\theta$, and so on.

    1. $\mathbf R_z(\psi)\mathbf R_y(\theta)\mathbf R_x(\phi)$ has third row $[-s_\theta,\ c_\theta s_\phi,\ c_\theta c_\phi]$ and first column $[c_\psi c_\theta,\ s_\psi c_\theta,\ -s_\theta]^\top$.
    2. If $|r_{31}| < 1$, then
    $$\theta = -\arcsin r_{31},\qquad \phi = \operatorname{atan2}(r_{32}, r_{33}),\qquad \psi = \operatorname{atan2}(r_{21}, r_{11})$$
    satisfy $\mathbf R = \mathbf R_z(\psi)\mathbf R_y(\theta)\mathbf R_x(\phi)$, and this is the only triple with $\theta \in (-\tfrac\pi2, \tfrac\pi2)$ and $\phi, \psi \in (-\pi, \pi]$.
    3. If $r_{31} = -1$ then $\theta = \tfrac\pi2$, and $\mathbf R_z(\psi)\mathbf R_y(\tfrac\pi2)\mathbf R_x(\phi)$ depends only on $\psi - \phi$, which equals $\operatorname{atan2}(r_{23}, r_{22})$. If $r_{31} = +1$ then $\theta = -\tfrac\pi2$, and the product depends only on $\psi + \phi = \operatorname{atan2}(-r_{23}, r_{22})$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    1. $\mathbf e_z^\top\mathbf R_z(\psi) = \mathbf e_z^\top$, so the third row is $\mathbf e_z^\top\mathbf R_y(\theta)\mathbf R_x(\phi) = [-s_\theta, 0, c_\theta]\,\mathbf R_x(\phi) = [-s_\theta,\ c_\theta s_\phi,\ c_\theta c_\phi]$. Similarly $\mathbf R_x(\phi)\mathbf e_x = \mathbf e_x$, so the first column is $\mathbf R_z(\psi)\mathbf R_y(\theta)\mathbf e_x = \mathbf R_z(\psi)[c_\theta, 0, -s_\theta]^\top = [c_\psi c_\theta,\ s_\psi c_\theta,\ -s_\theta]^\top$.
    2. *Existence.* With $\theta$ as defined, $c_\theta = \sqrt{1 - r_{31}^2} > 0$. The rows of $\mathbf R$ are unit vectors (because $\mathbf R\mathbf R^\top = \mathbf I$), so $r_{32}^2 + r_{33}^2 = 1 - r_{31}^2 = c_\theta^2$, and therefore $(r_{33}, r_{32}) = c_\theta(\cos\phi, \sin\phi)$ with $\phi = \operatorname{atan2}(r_{32}, r_{33})$. The columns are unit vectors too, so in the same way $(r_{11}, r_{21}) = c_\theta(\cos\psi, \sin\psi)$. By item 1, $\mathbf R' := \mathbf R_z(\psi)\mathbf R_y(\theta)\mathbf R_x(\phi)$ has the same third row and first column as $\mathbf R$.
    Let $\mathbf M := \mathbf R'^\top\mathbf R \in SO(3)$. Equal first columns give $\mathbf M\mathbf e_x = \mathbf R'^\top\mathbf R'\mathbf e_x = \mathbf e_x$. Equal third rows give $\mathbf R^\top\mathbf e_z = \mathbf R'^\top\mathbf e_z =: \mathbf w$, so $\mathbf M^\top\mathbf w = \mathbf R^\top\mathbf R'\mathbf R'^\top\mathbf e_z = \mathbf w$ and hence $\mathbf M\mathbf w = \mathbf w$. Now $\mathbf w = [-s_\theta, c_\theta s_\phi, c_\theta c_\phi]^\top$ is not parallel to $\mathbf e_x$ because $c_\theta \ne 0$, so $\mathbf e_x\times\mathbf w \ne \mathbf 0$, and by property 4, $\mathbf M(\mathbf e_x\times\mathbf w) = \mathbf M\mathbf e_x\times\mathbf M\mathbf w = \mathbf e_x\times\mathbf w$. The vectors $\mathbf e_x$, $\mathbf w$, $\mathbf e_x\times\mathbf w$ are linearly independent (the third is nonzero and perpendicular to the first two, which are independent), and $\mathbf M$ fixes all three, so $\mathbf M = \mathbf I$ and $\mathbf R = \mathbf R'$.
    *Uniqueness.* Any triple with $\mathbf R = \mathbf R_z(\psi)\mathbf R_y(\theta)\mathbf R_x(\phi)$ has $\sin\theta = -r_{31}$ by item 1, which fixes $\theta$ in $(-\tfrac\pi2, \tfrac\pi2)$. Then $c_\theta > 0$, and $(r_{33}, r_{32}) = c_\theta(\cos\phi, \sin\phi)$ fixes $\phi \in (-\pi, \pi]$ by the definition of $\operatorname{atan2}$; likewise for $\psi$.
    3. Multiplying out with $\theta = \tfrac\pi2$ gives
    $$\mathbf R_z(\psi)\mathbf R_y(\tfrac\pi2)\mathbf R_x(\phi) = \begin{bmatrix}0 & -\sin(\psi-\phi) & \cos(\psi-\phi)\\ 0 & \cos(\psi-\phi) & \sin(\psi-\phi)\\ -1 & 0 & 0\end{bmatrix},$$
    which depends only on $\psi - \phi$, and $(r_{22}, r_{23}) = (\cos(\psi-\phi), \sin(\psi-\phi))$. The case $\theta = -\tfrac\pi2$ is the same computation, with $\psi + \phi$ in place of $\psi - \phi$ and $r_{23} = -\sin(\psi+\phi)$. $\blacksquare$
    ///

    Item 2 shows every rotation matrix has Euler angles (item 3 covers the remaining cases), and that restricting $\theta$ to $[-\tfrac\pi2, \tfrac\pi2]$ removes most ambiguity; without that restriction $(\phi + \pi,\ \pi - \theta,\ \psi + \pi)$ always gives the same matrix as $(\phi, \theta, \psi)$. Item 3 is the troublesome case: at $\theta = \pm 90^\circ$ infinitely many triples give the same matrix. That is our first sighting of gimbal lock.

    /// caution | ⚠️ **Assumptions and Failure Modes**
    - The formulas assume $\mathbf R$ is exactly orthogonal. A matrix that has drifted from orthogonality (for example after many numerical integration steps) can give $|r_{31}| > 1$, where $\arcsin$ is undefined; clip $r_{31}$ to $[-1, 1]$ or re-orthonormalize first.
    - Near $\theta = \pm 90^\circ$, $(r_{32}, r_{33})$ and $(r_{11}, r_{21})$ are both tiny, so $\phi$ and $\psi$ individually become extremely sensitive to rounding and noise, even though the matrix itself is perfectly well behaved.
    - $\phi$ and $\psi$ jump by $360^\circ$ when they cross $\pm 180^\circ$. Never difference or average angles without wrapping the result back into $(-\pi, \pi]$.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ```python
    def skew(a):
        "\"\"Cross-product matrix: skew(a) @ b == np.cross(a, b)."\"\"
        return np.array([[0.0, -a[2], a[1]],
                         [a[2], 0.0, -a[0]],
                         [-a[1], a[0], 0.0]])

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
        "\"\"ZYX Euler angles (roll, pitch, yaw) -> R^n_b."\"\"
        return rot_z(psi) @ rot_y(theta) @ rot_x(phi)

    def R_to_euler(R):
        "\"\"R^n_b -> principal ZYX Euler angles (roll, pitch, yaw).
        At gimbal lock (|r31| = 1) only psi -/+ phi is determined; we set phi = 0."\"\"
        r31 = np.clip(R[2, 0], -1.0, 1.0)
        theta = -np.arcsin(r31)
        if abs(r31) < 1.0 - 1e-12:
            return np.array([np.arctan2(R[2, 1], R[2, 2]), theta,
                             np.arctan2(R[1, 0], R[0, 0])])
        if r31 < 0:   # theta = +pi/2: only psi - phi is determined
            return np.array([0.0, theta, np.arctan2(R[1, 2], R[1, 1])])
        return np.array([0.0, theta, np.arctan2(-R[1, 2], R[1, 1])])

    def Exp(theta_vec):
        "\"\"Rotation vector -> rotation matrix (Rodrigues' formula)."\"\"
        angle = np.linalg.norm(theta_vec)
        if angle < 1e-12:
            return np.eye(3) + skew(theta_vec)
        K = skew(theta_vec / angle)
        return np.eye(3) + np.sin(angle) * K + (1.0 - np.cos(angle)) * K @ K

    def Log(R):
        "\"\"Rotation matrix -> rotation vector with norm in [0, pi]."\"\"
        cos_angle = np.clip((np.trace(R) - 1.0) / 2.0, -1.0, 1.0)
        angle = np.arccos(cos_angle)
        vee = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]])
        if angle < 1e-8:
            return 0.5 * vee
        if np.pi - angle < 1e-6:   # R + I = 2 u u^T: take the largest column
            B = (R + np.eye(3)) / 2.0
            j = np.argmax(np.diag(B))
            u = B[:, j] / np.sqrt(B[j, j])
            return angle * u
        return angle / (2.0 * np.sin(angle)) * vee
    ```
    """)
    return


@app.cell
def rotation_helpers(np):
    # jb: include=false
    def skew(a):
        """Cross-product matrix: skew(a) @ b == np.cross(a, b)."""
        return np.array([[0.0, -a[2], a[1]],
                         [a[2], 0.0, -a[0]],
                         [-a[1], a[0], 0.0]])

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
        """ZYX Euler angles (roll, pitch, yaw) -> R^n_b."""
        return rot_z(psi) @ rot_y(theta) @ rot_x(phi)

    def R_to_euler(R):
        """R^n_b -> principal ZYX Euler angles (roll, pitch, yaw).
        At gimbal lock (|r31| = 1) only psi -/+ phi is determined; we set phi = 0."""
        r31 = np.clip(R[2, 0], -1.0, 1.0)
        theta = -np.arcsin(r31)
        if abs(r31) < 1.0 - 1e-12:
            return np.array([np.arctan2(R[2, 1], R[2, 2]), theta,
                             np.arctan2(R[1, 0], R[0, 0])])
        if r31 < 0:   # theta = +pi/2: only psi - phi is determined
            return np.array([0.0, theta, np.arctan2(R[1, 2], R[1, 1])])
        return np.array([0.0, theta, np.arctan2(-R[1, 2], R[1, 1])])

    def Exp(theta_vec):
        """Rotation vector -> rotation matrix (Rodrigues' formula)."""
        angle = np.linalg.norm(theta_vec)
        if angle < 1e-12:
            return np.eye(3) + skew(theta_vec)
        K = skew(theta_vec / angle)
        return np.eye(3) + np.sin(angle) * K + (1.0 - np.cos(angle)) * K @ K

    def Log(R):
        """Rotation matrix -> rotation vector with norm in [0, pi]."""
        cos_angle = np.clip((np.trace(R) - 1.0) / 2.0, -1.0, 1.0)
        angle = np.arccos(cos_angle)
        vee = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]])
        if angle < 1e-8:
            return 0.5 * vee
        if np.pi - angle < 1e-6:   # R + I = 2 u u^T: take the largest column
            B = (R + np.eye(3)) / 2.0
            j = np.argmax(np.diag(B))
            u = B[:, j] / np.sqrt(B[j, j])
            return angle * u
        return angle / (2.0 * np.sin(angle)) * vee

    return Exp, Log, R_to_euler, euler_to_R, rot_x, rot_z, skew


@app.cell
def _(np, rot_x, rot_z):
    # jb: include=false
    def _fmt(v):
        v = np.where(np.abs(v) < 1e-12, 0.0, v)
        return r"[" + ", ".join(f"{x:.0f}" for x in v) + r"]^\top"

    _ex = np.array([1.0, 0.0, 0.0])
    R_order_1 = _fmt(rot_z(np.pi / 2) @ rot_x(np.pi / 2) @ _ex)
    R_order_2 = _fmt(rot_x(np.pi / 2) @ rot_z(np.pi / 2) @ _ex)
    return R_order_1, R_order_2


@app.cell
def plot_helpers(Poly3DCollection, np):
    # jb: include=false
    def setup_3d(ax, lim=1.15, zlim=None, elev=20, azim=-60, zoom=1.3):
        _zl = (-lim, lim) if zlim is None else zlim
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_zlim(*_zl)
        ax.set_box_aspect((1, 1, (_zl[1] - _zl[0]) / (2 * lim)), zoom=zoom)
        ax.view_init(elev=elev, azim=azim)
        ax.set_axis_off()

    def draw_axes(ax, R, length, colors, labels, lw=2.0, ls="-", fontsize=11):
        for _i in range(3):
            _v = R[:, _i] * length
            ax.plot([0, _v[0]], [0, _v[1]], [0, _v[2]], color=colors[_i], lw=lw, ls=ls)
            ax.text(*(_v * 1.13), labels[_i], color=colors[_i], fontsize=fontsize,
                    ha="center", va="center")

    def draw_body(ax, R, L=0.9, W=0.4, H=0.14):
        """A flat wedge pointing along body x, so 'forward' is obvious."""
        _P = np.array([[-L/2, -W/2, -H/2], [L/2, -W/2, -H/2], [L/2 + 0.25, 0, -H/2],
                       [L/2, W/2, -H/2], [-L/2, W/2, -H/2],
                       [-L/2, -W/2, H/2], [L/2, -W/2, H/2], [L/2 + 0.25, 0, H/2],
                       [L/2, W/2, H/2], [-L/2, W/2, H/2]]) @ R.T
        _faces = [_P[[0, 1, 2, 3, 4]], _P[[5, 6, 7, 8, 9]]]
        _faces += [_P[[_i, (_i + 1) % 5, (_i + 1) % 5 + 5, _i + 5]] for _i in range(5)]
        ax.add_collection3d(Poly3DCollection(_faces, facecolor="0.85", edgecolor="0.35",
                                             alpha=0.55, lw=0.5))

    return draw_axes, draw_body, setup_3d


@app.cell
def make_frames_fig(IMAGES_DIR, draw_axes, draw_body, euler_to_R, np, plt, setup_3d):
    # jb: include=false
    _fig = plt.figure(figsize=(9, 4.2))
    _cases = [((0.0, 0.0, 0.0), "Zero attitude: body axes = ENU"),
              ((np.radians(10), np.radians(-20), np.radians(35)),
               r"Yaw $35^\circ$, pitch $-20^\circ$ (nose up), roll $10^\circ$")]
    for _j, (_ang, _title) in enumerate(_cases):
        _ax = _fig.add_subplot(1, 2, _j + 1, projection="3d")
        setup_3d(_ax, lim=1.1, zlim=(-0.5, 1.2), zoom=1.45)
        _R = euler_to_R(*_ang)
        draw_axes(_ax, np.eye(3), 1.2, ["0.45"] * 3, ["E", "N", "U"], lw=1.0, ls="--")
        draw_body(_ax, _R)
        draw_axes(_ax, _R, 0.95, ["C3", "C2", "C0"], [r"$x_b$", r"$y_b$", r"$z_b$"])
        _ax.set_title(_title, style="italic", fontsize=11)
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch17_frames.svg")
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch17-sec-angular-velocity -->
    ## Angular Velocity

    A walking foot's attitude changes continuously, $\mathbf R^n_b = \mathbf R^n_b(t)$. A gyroscope measures neither $\mathbf R^n_b$ nor the Euler angles; it measures how fast the body is turning. To say precisely what that means, differentiate the defining property of a rotation matrix.

    /// admonition | 📐 **Lemma (The Rate of a Rotation Is Skew-Symmetric)**
        attrs: {class: lemma, id: ch17-lem-the-rate-of-a-rotation-is-skew-symmetric}
    If $t \mapsto \mathbf R(t) \in SO(3)$ is differentiable, then $\mathbf R^\top\dot{\mathbf R}$ is skew-symmetric at every $t$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Differentiate $\mathbf R^\top\mathbf R = \mathbf I$ entrywise with the product rule: $\dot{\mathbf R}^\top\mathbf R + \mathbf R^\top\dot{\mathbf R} = \mathbf 0$, that is, $(\mathbf R^\top\dot{\mathbf R})^\top = -\mathbf R^\top\dot{\mathbf R}$. $\blacksquare$
    ///

    Since every $3\times 3$ skew-symmetric matrix is $[\mathbf a]_\times$ for exactly one vector $\mathbf a$ ([Appendix D: Cross Products and Skew-Symmetric Matrices](#appd-sec-cross-products-and-skew-symmetric-matrices)), the following definition makes sense.

    /// note | 📖 **Definition**
    <u>**Angular velocity**</u>

    The angular velocity of the body frame $b$ relative to the navigation frame $n$, expressed in body coordinates, is the unique vector $\boldsymbol\omega^b(t) \in \mathbb R^3$ with
    $$(\mathbf R^n_b)^\top\dot{\mathbf R}^n_b = [\boldsymbol\omega^b]_\times,\qquad\text{equivalently}\qquad \dot{\mathbf R}^n_b = \mathbf R^n_b\,[\boldsymbol\omega^b]_\times.$$
    Its navigation-frame coordinates are $\boldsymbol\omega^n := \mathbf R^n_b\boldsymbol\omega^b$.
    ///

    This matches the angular velocity of elementary physics. Take a point fixed to the body, with constant body coordinates $\mathbf p^b$. Its navigation coordinates $\mathbf p^n(t) = \mathbf R^n_b(t)\mathbf p^b$ change at the rate
    $$\dot{\mathbf p}^n = \dot{\mathbf R}^n_b\mathbf p^b = \mathbf R^n_b(\boldsymbol\omega^b\times\mathbf p^b) = (\mathbf R^n_b\boldsymbol\omega^b)\times(\mathbf R^n_b\mathbf p^b) = \boldsymbol\omega^n\times\mathbf p^n,$$
    by property 4. So every point of the body moves as if spinning about the axis $\boldsymbol\omega^n$ at $\|\boldsymbol\omega^n\|$ radians per second, by the right-hand rule. Property 5 gives the navigation-frame form of the definition, $\dot{\mathbf R}^n_b(\mathbf R^n_b)^\top = \mathbf R^n_b[\boldsymbol\omega^b]_\times(\mathbf R^n_b)^\top = [\boldsymbol\omega^n]_\times$.

    /// admonition | 📐 **Lemma (Elementary Rotation Rates)**
        attrs: {class: lemma, id: ch17-lem-elementary-rotation-rates}
    For differentiable angles, $\mathbf R_x(\phi)^\top\tfrac{d}{dt}\mathbf R_x(\phi) = \dot\phi\,[\mathbf e_x]_\times$, $\ \mathbf R_y(\theta)^\top\tfrac{d}{dt}\mathbf R_y(\theta) = \dot\theta\,[\mathbf e_y]_\times$, and $\mathbf R_z(\psi)^\top\tfrac{d}{dt}\mathbf R_z(\psi) = \dot\psi\,[\mathbf e_z]_\times$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    By the chain rule, $\tfrac{d}{dt}\mathbf R_z(\psi) = \dot\psi\begin{bmatrix}-\sin\psi & -\cos\psi & 0\\ \cos\psi & -\sin\psi & 0\\ 0 & 0 & 0\end{bmatrix}$, and multiplying by $\mathbf R_z(\psi)^\top$ on the left gives $\dot\psi\begin{bmatrix}0 & -1 & 0\\ 1 & 0 & 0\\ 0 & 0 & 0\end{bmatrix} = \dot\psi\,[\mathbf e_z]_\times$. The other two are the same computation. $\blacksquare$
    ///

    So a body that only yaws has $\boldsymbol\omega^b = [0, 0, \dot\psi]^\top$, as expected.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch17-sec-gimbal-lock -->
    ## Gimbal Lock

    Euler angles are the most intuitive description of attitude, so it is tempting to integrate them directly from gyroscope readings. That requires the relation between the Euler-angle rates $\dot{\boldsymbol\Theta} = [\dot\phi, \dot\theta, \dot\psi]^\top$ and the angular velocity.

    /// admonition | 📐 **Theorem (Euler-Angle Kinematics)**
        attrs: {class: theorem, id: ch17-thm-euler-angle-kinematics}
    If $\mathbf R^n_b(t) = \mathbf R_z(\psi(t))\mathbf R_y(\theta(t))\mathbf R_x(\phi(t))$ with differentiable angles, then
    $$\boldsymbol\omega^b = \mathbf W(\phi, \theta)\,\dot{\boldsymbol\Theta},\qquad \mathbf W(\phi, \theta) = \begin{bmatrix}1 & 0 & -\sin\theta\\ 0 & \cos\phi & \sin\phi\cos\theta\\ 0 & -\sin\phi & \cos\phi\cos\theta\end{bmatrix},\qquad \det\mathbf W = \cos\theta.$$
    Whenever $\cos\theta \ne 0$, the Euler-angle rates are $\dot{\boldsymbol\Theta} = \mathbf E(\phi, \theta)\,\boldsymbol\omega^b$ with
    $$\mathbf E(\phi, \theta) := \mathbf W(\phi, \theta)^{-1} = \begin{bmatrix}1 & \sin\phi\tan\theta & \cos\phi\tan\theta\\ 0 & \cos\phi & -\sin\phi\\ 0 & \sin\phi/\cos\theta & \cos\phi/\cos\theta\end{bmatrix}.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Abbreviate $\mathbf R_x := \mathbf R_x(\phi)$ and so on. By the product rule, $\dot{\mathbf R} = \dot{\mathbf R}_z\mathbf R_y\mathbf R_x + \mathbf R_z\dot{\mathbf R}_y\mathbf R_x + \mathbf R_z\mathbf R_y\dot{\mathbf R}_x$. Multiply on the left by $\mathbf R^\top = \mathbf R_x^\top\mathbf R_y^\top\mathbf R_z^\top$ and use the elementary-rate lemma:
    $$\mathbf R^\top\dot{\mathbf R} = \dot\psi\,(\mathbf R_y\mathbf R_x)^\top[\mathbf e_z]_\times(\mathbf R_y\mathbf R_x) + \dot\theta\,\mathbf R_x^\top[\mathbf e_y]_\times\mathbf R_x + \dot\phi\,[\mathbf e_x]_\times.$$
    Property 5, applied with the rotation matrices $(\mathbf R_y\mathbf R_x)^\top$ and $\mathbf R_x^\top$, turns this into $\big[\dot\psi\,(\mathbf R_y\mathbf R_x)^\top\mathbf e_z + \dot\theta\,\mathbf R_x^\top\mathbf e_y + \dot\phi\,\mathbf e_x\big]_\times$. Direct multiplication gives $\mathbf R_x^\top\mathbf e_y = [0, \cos\phi, -\sin\phi]^\top$ and $(\mathbf R_y\mathbf R_x)^\top\mathbf e_z = \mathbf R_x^\top[-\sin\theta, 0, \cos\theta]^\top = [-\sin\theta, \sin\phi\cos\theta, \cos\phi\cos\theta]^\top$. These three vectors are the columns of $\mathbf W$. Expanding $\det\mathbf W$ along its first column gives $\cos\phi\cdot\cos\phi\cos\theta + \sin\phi\cdot\sin\phi\cos\theta = \cos\theta$, and multiplying out $\mathbf W\mathbf E$ gives $\mathbf I$. $\blacksquare$
    ///

    The proof also explains the columns of $\mathbf W$: they are the body-frame directions of the *roll axis* (body $x$), the *pitch axis* (the body $y$ axis after yawing), and the *yaw axis* (Up). The angular velocity is $\dot\phi$ times the first plus $\dot\theta$ times the second plus $\dot\psi$ times the third. The pitch axis is always perpendicular to the other two, so $\mathbf W$ is singular exactly when the roll axis lines up with the yaw axis, at $\theta = \pm 90^\circ$.

    /// note | 📖 **Definition**
    <u>**Gimbal lock**</u>

    An attitude is in gimbal lock (for a given Euler-angle sequence) if the matrix that maps Euler-angle rates to angular velocity at that attitude is singular. For ZYX Euler angles this happens exactly when $\cos\theta = 0$, that is, at pitch $\theta = \pm 90^\circ$.
    ///

    The name comes from mechanical gimbals: three nested rings whose rotation angles are exactly a set of Euler angles. At gimbal lock two of the rings' axes line up and the mechanism can no longer turn about the third direction ([Wikipedia: Gimbal lock](https://en.wikipedia.org/wiki/Gimbal_lock)). For a filter, gimbal lock means three things:

    1. **Some angular velocities are unreachable.** At $\theta = 90^\circ$ the columns of $\mathbf W$ span only the plane of $\mathbf e_x$ and $[0, \cos\phi, -\sin\phi]^\top$. A body rotating about any other axis has no finite Euler-angle rates.
    2. **Near gimbal lock the rates blow up.** The entries of $\mathbf E$ grow like $1/\cos\theta$, so a gentle, constant body rotation that passes near $\theta = 90^\circ$ produces huge roll and yaw rates (figure below). Integrating $\dot{\boldsymbol\Theta} = \mathbf E\boldsymbol\omega^b$ numerically fails there.
    3. **The angles stop being determined.** By the Euler-angle theorem (item 3), at $\theta = 90^\circ$ every pair $(\phi, \psi)$ with the same $\psi - \phi$ gives the same matrix.
    """)
    return


@app.cell(hide_code=True)
def _(lock_example, mo):
    mo.md(rf"""
    For instance, computing both products numerically,

    {lock_example}

    The attitude is the same; only its description differs.
    """)
    return


@app.cell
def _(euler_to_R, np):
    # jb: include=false
    def _bmat(M):
        _M = np.where(np.abs(M) < 5e-5, 0.0, M)
        _rows = [" & ".join(f"{x:.4f}" for x in r) for r in _M]
        return r"\begin{bmatrix}" + r"\\ ".join(_rows) + r"\end{bmatrix}"

    _A = euler_to_R(np.radians(10), np.radians(90), np.radians(40))
    _B = euler_to_R(np.radians(30), np.radians(90), np.radians(60))
    lock_example = (
        r"$$\mathbf R_z(40^\circ)\mathbf R_y(90^\circ)\mathbf R_x(10^\circ) = " + _bmat(_A)
        + r" = \mathbf R_z(60^\circ)\mathbf R_y(90^\circ)\mathbf R_x(30^\circ).$$"
        + "\n\n"
        + rf"(The largest entry difference is below $10^{{{int(np.floor(np.log10(np.abs(_A - _B).max() + 1e-300))) + 1}}}$: rounding error.)"
    )
    return (lock_example,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch17_euler_rates.svg" class="graphic" alt="Two stacked plots over 6 seconds. Top: pitch rises linearly to about 87 degrees and falls back, while roll and yaw each jump by about 180 degrees within half a second at t of about 3 seconds. Bottom: the pitch rate stays near 0.5 radians per second, but the roll and yaw rates spike to about 9.5 radians per second at the same moment." />

    In this simulation the body starts with $3^\circ$ of roll and turns at a constant $0.5$ rad/s about its own $y$ axis, so the nose sweeps a circle that passes $3^\circ$ from straight down. Nothing physical happens at $t \approx 3.1$ s; the body keeps turning at the same rate. Yet roll and yaw each swing through about $180^\circ$ in under a second, and their rates spike to almost twenty times the actual rotation rate. A filter that integrated Euler angles would need a tiny time step here, and with a path passing exactly through $\theta = 90^\circ$ no time step is small enough.
    """)
    return


@app.cell
def make_euler_rates_fig(Exp, IMAGES_DIR, R_to_euler, euler_to_R, np, plt):
    # jb: include=false
    def _E(phi, theta):
        return np.array([[1, np.sin(phi) * np.tan(theta), np.cos(phi) * np.tan(theta)],
                         [0, np.cos(phi), -np.sin(phi)],
                         [0, np.sin(phi) / np.cos(theta), np.cos(phi) / np.cos(theta)]])

    _R0 = euler_to_R(np.radians(3.0), 0.0, 0.0)
    _w = np.array([0.0, 0.5, 0.0])
    _t = np.linspace(0.0, 6.0, 1201)
    _eul = np.array([R_to_euler(_R0 @ Exp(_w * _tt)) for _tt in _t])
    _rates = np.array([_E(_e[0], _e[1]) @ _w for _e in _eul])

    _fig, _axs = plt.subplots(2, 1, figsize=(7, 5.6), sharex=True)
    _labels = [r"roll $\phi$", r"pitch $\theta$", r"yaw $\psi$"]
    _rate_labels = [r"$\dot\phi$", r"$\dot\theta$", r"$\dot\psi$"]
    _styles = ["-", "-", "--"]
    for _i in range(3):
        _axs[0].plot(_t, np.degrees(_eul[:, _i]), ls=_styles[_i], color=f"C{_i}", label=_labels[_i])
        _axs[1].plot(_t, _rates[:, _i], ls=_styles[_i], color=f"C{_i}", label=_rate_labels[_i])
    _axs[0].set_ylabel("angle (deg)")
    _axs[1].set_ylabel("Euler-angle rate (rad/s)")
    _axs[1].set_xlabel("time (s)")
    _axs[0].set_title(r"Constant body rate of 0.5 rad/s passing $3^\circ$ from gimbal lock", style="italic")
    for _a in _axs:
        _a.grid(visible=True, alpha=0.9, linewidth=0.4)
        _a.legend(loc="upper left", fontsize=9)
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch17_euler_rates.svg")
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch17-sec-interactive-approaching-gimbal-lock -->
    ### Interactive: Approaching Gimbal Lock

    Set the yaw, pitch, and roll below. The shaded wedge is the body (its point is "forward"), the dashed gray axes are East, North, Up, and the dotted lines are the three gimbal axes. The panel on the right shows $\det\mathbf W = \cos\theta$ and the Euler-angle rates $\dot{\boldsymbol\Theta} = \mathbf E\boldsymbol\omega^b$ needed to produce a steady body rotation of $\boldsymbol\omega^b = [0, 0, 1]^\top$ rad/s about the body's own $z$ axis. Drag the pitch toward $\pm 90^\circ$ and watch the roll axis swing onto the yaw axis and the required rates explode.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    yaw_slider = mo.ui.slider(-180, 180, 1, value=30, label=r"yaw $\psi$ (deg)", show_value=True)
    pitch_slider = mo.ui.slider(-90, 90, 1, value=-60, label=r"pitch $\theta$ (deg)", show_value=True)
    roll_slider = mo.ui.slider(-180, 180, 1, value=20, label=r"roll $\phi$ (deg)", show_value=True)
    return pitch_slider, roll_slider, yaw_slider


@app.cell(hide_code=True)
def _(
    draw_axes,
    draw_body,
    euler_to_R,
    graphic,
    mo,
    np,
    pitch_slider,
    plt,
    roll_slider,
    rot_z,
    setup_3d,
    yaw_slider,
):
    _phi, _theta, _psi = np.radians([roll_slider.value, pitch_slider.value, yaw_slider.value])
    _R = euler_to_R(_phi, _theta, _psi)
    _fig = plt.figure(figsize=(5.6, 5.2))
    _ax = _fig.add_subplot(projection="3d")
    setup_3d(_ax, lim=1.2, elev=18, azim=-55)
    draw_axes(_ax, np.eye(3), 1.2, ["0.55"] * 3, ["E", "N", "U"], lw=0.9, ls="--", fontsize=10)
    draw_body(_ax, _R)
    draw_axes(_ax, _R, 0.9, ["C3", "C2", "C0"], [r"$x_b$", r"$y_b$", r"$z_b$"])
    _gimbal = {"yaw axis": (np.array([0.0, 0.0, 1.0]), "C4"),
               "pitch axis": (rot_z(_psi) @ np.array([0.0, 1.0, 0.0]), "C1"),
               "roll axis": (_R[:, 0], "C3")}
    for _name, (_a, _c) in _gimbal.items():
        _ax.plot(*np.array([-1.35 * _a, 1.35 * _a]).T, color=_c, ls=":", lw=1.6)
        _ax.text(*(1.45 * _a), _name, color=_c, fontsize=9)
    _ax.set_title(rf"yaw {yaw_slider.value}$^\circ$, pitch {pitch_slider.value}$^\circ$, roll {roll_slider.value}$^\circ$",
                  style="italic", fontsize=11)
    _fig.tight_layout()

    _c = np.cos(_theta)
    if abs(_c) < 1e-9:
        _rates_md = (
            r"**Gimbal lock.** $\mathbf W$ is singular: Euler-angle rates can only produce angular "
            r"velocities in a plane, and $\mathbf E$ does not exist."
        )
        if abs(np.cos(_phi)) > 1e-9:
            _rates_md += r" In particular, no finite rates produce $\boldsymbol\omega^b = [0, 0, 1]^\top$."
    else:
        _rates = np.array([np.cos(_phi) * np.tan(_theta), -np.sin(_phi), np.cos(_phi) / _c])
        _rates_md = (
            r"Rates for $\boldsymbol\omega^b = [0,0,1]^\top$ rad/s:" + "\n\n"
            + rf"$\dot\phi = {_rates[0]:.2f}$ rad/s" + "\n\n"
            + rf"$\dot\theta = {_rates[1]:.2f}$ rad/s" + "\n\n"
            + rf"$\dot\psi = {_rates[2]:.2f}$ rad/s"
        )
    _angle = np.degrees(np.arccos(np.clip(abs(_R[:, 0] @ np.array([0, 0, 1.0])), 0, 1)))
    _panel = mo.md(
        rf"$\det\mathbf W = \cos\theta = {_c:.4f}$" + "\n\n"
        + rf"Angle between roll and yaw axes: ${_angle:.1f}^\circ$" + "\n\n"
        + _rates_md
    )
    _out = mo.vstack([
        mo.hstack([yaw_slider, pitch_slider, roll_slider], justify="start"),
        mo.hstack([graphic(_fig), _panel], align="center"),
    ])
    plt.close(_fig)
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch17-sec-axisangle-representation-and-rodrigues-formula -->
    ## Axis–Angle Representation and Rodrigues' Formula

    Euler angles describe a rotation as three turns about coordinate axes. A single turn about a well-chosen axis is enough. A door turns about its hinge; turning $90^\circ$ about Up carries East to North. In this section we make "turning about an axis" precise. We write the rotation angle as $\vartheta$ (a variant of the letter theta), because $\theta$ is reserved for pitch.

    Fix a unit vector $\mathbf u$ (the axis) and an angle $\vartheta$. Split any vector $\mathbf v$ into its component along the axis and the rest:
    $$\mathbf v_\parallel := (\mathbf u\cdot\mathbf v)\,\mathbf u,\qquad \mathbf v_\perp := \mathbf v - \mathbf v_\parallel.$$
    Turning $\mathbf v$ about $\mathbf u$ should leave $\mathbf v_\parallel$ alone and turn $\mathbf v_\perp$ by $\vartheta$ within the plane perpendicular to $\mathbf u$. In that plane, $\mathbf u\times\mathbf v_\perp$ is $\mathbf v_\perp$ turned by $+90^\circ$: it is perpendicular to both $\mathbf u$ and $\mathbf v_\perp$, it has the same length as $\mathbf v_\perp$ (because $\mathbf u\perp\mathbf v_\perp$ and $\|\mathbf u\| = 1$), and $(\mathbf u, \mathbf v_\perp, \mathbf u\times\mathbf v_\perp)$ is right-handed. So, exactly as in the plane, turning $\mathbf v_\perp$ by $\vartheta$ gives $\cos\vartheta\,\mathbf v_\perp + \sin\vartheta\,\mathbf u\times\mathbf v_\perp$.

    <img src="public/ch17_rodrigues.svg" class="graphic" alt="A 3-D sketch of a vertical axis u, a vector v split into a vertical part along u and a horizontal part perpendicular to u, the vector u cross v-perpendicular at 90 degrees to it, and the rotated vector, whose tip lies on the circle traced around the axis." />

    /// note | 📖 **Definition**
    <u>**Axis-angle representation**</u>

    An axis–angle representation of a rotation matrix $\mathbf R$ is a pair $(\mathbf u, \vartheta)$ of a unit vector $\mathbf u \in \mathbb R^3$ and an angle $\vartheta \in \mathbb R$ such that, for every $\mathbf v \in \mathbb R^3$,
    $$\mathbf R\mathbf v = \mathbf v_\parallel + \cos\vartheta\,\mathbf v_\perp + \sin\vartheta\,\mathbf u\times\mathbf v_\perp,\qquad \mathbf v_\parallel := (\mathbf u\cdot\mathbf v)\mathbf u,\quad \mathbf v_\perp := \mathbf v - \mathbf v_\parallel.$$
    We write $\mathbf R(\mathbf u, \vartheta)$ for this matrix: the right-handed rotation by $\vartheta$ about $\mathbf u$.
    ///

    /// admonition | 📐 **Theorem (Rodrigues' Formula)**
        attrs: {class: theorem, id: ch17-thm-rodrigues-formula}
    For every unit vector $\mathbf u$ and angle $\vartheta$,
    $$\mathbf R(\mathbf u, \vartheta) = \mathbf I + \sin\vartheta\,[\mathbf u]_\times + (1 - \cos\vartheta)\,[\mathbf u]_\times^2.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Multiplying out $[\mathbf u]_\times[\mathbf u]_\times$ gives $\mathbf u\mathbf u^\top - \|\mathbf u\|^2\mathbf I$ (for example, the $(1,1)$ entry is $-u_2^2 - u_3^2 = u_1^2 - \|\mathbf u\|^2$ and the $(1,2)$ entry is $u_1u_2$). With $\|\mathbf u\| = 1$ this says $[\mathbf u]_\times^2\mathbf v = (\mathbf u\cdot\mathbf v)\mathbf u - \mathbf v = -\mathbf v_\perp$, so $\mathbf v_\perp = -[\mathbf u]_\times^2\mathbf v$ and $\mathbf v_\parallel = \mathbf v + [\mathbf u]_\times^2\mathbf v$. Also $\mathbf u\times\mathbf v_\perp = \mathbf u\times\mathbf v - \mathbf u\times\mathbf v_\parallel = [\mathbf u]_\times\mathbf v$, since $\mathbf v_\parallel$ is parallel to $\mathbf u$. Substituting into the definition,
    $$\mathbf R(\mathbf u, \vartheta)\mathbf v = \mathbf v + [\mathbf u]_\times^2\mathbf v - \cos\vartheta\,[\mathbf u]_\times^2\mathbf v + \sin\vartheta\,[\mathbf u]_\times\mathbf v$$
    for every $\mathbf v$, which is the claim. $\blacksquare$
    ///
    """)
    return


@app.cell
def make_rodrigues_fig(IMAGES_DIR, np, plt, setup_3d):
    # jb: include=false
    _fig = plt.figure(figsize=(6, 4.6))
    _ax = _fig.add_subplot(projection="3d")
    setup_3d(_ax, lim=0.9, zlim=(-0.25, 1.0), elev=24, azim=-62, zoom=1.5)
    _u = np.array([0.0, 0.0, 1.0])
    _v = np.array([0.8, 0.0, 0.55])
    _vt = np.radians(70)
    _vpar = (_u @ _v) * _u
    _vperp = _v - _vpar
    _uxv = np.cross(_u, _vperp)
    _rot = _vpar + np.cos(_vt) * _vperp + np.sin(_vt) * _uxv

    def _arrow(start, vec, color, label, ls="-", lw=2.0, off=(0, 0, 0)):
        _ax.quiver(*start, *vec, color=color, lw=lw, ls=ls, arrow_length_ratio=0.08)
        _ax.text(*(start + vec + np.array(off)), label, color=color, fontsize=12)

    _o = np.zeros(3)
    _ax.plot([0, 0], [0, 0], [-0.3, 1.0], color="k", lw=1.0)
    _arrow(_o, 0.9 * _u, "k", r"$\mathbf{u}$", off=(0.03, 0, 0.03))
    _arrow(_o, _v, "C0", r"$\mathbf{v}$", off=(0.03, 0, 0.03))
    _arrow(_o, _rot, "C1", r"$\mathbf{R}(\mathbf{u},\vartheta)\mathbf{v}$", off=(0.0, 0.03, 0.05))
    _arrow(_vpar, _vperp, "C0", "", ls="--", lw=1.5)
    _ax.text(*(_vpar + 0.55 * _vperp + np.array([0.0, 0.0, 0.04])), r"$\mathbf{v}_\perp$",
             color="C0", fontsize=12)
    _arrow(_vpar, _uxv, "C2", r"$\mathbf{u}\times\mathbf{v}_\perp$", ls="--", lw=1.5, off=(-0.25, 0.03, 0.03))
    _ax.text(*(0.5 * _vpar + np.array([-0.17, 0, 0])), r"$\mathbf{v}_\parallel$", color="0.3", fontsize=12)
    _s = np.linspace(0, 2 * np.pi, 200)
    _circ = _vpar[:, None] + np.outer(_vperp, np.cos(_s)) + np.outer(_uxv, np.sin(_s))
    _ax.plot(*_circ, color="0.6", lw=0.8)
    _s = np.linspace(0, _vt, 40)
    _arc = _vpar[:, None] + 0.35 * (np.outer(_vperp, np.cos(_s)) + np.outer(_uxv, np.sin(_s)))
    _ax.plot(*_arc, color="C1", lw=1.2)
    _mid = _vpar + 0.42 * (np.cos(_vt / 2) * _vperp + np.sin(_vt / 2) * _uxv)
    _ax.text(*_mid, r"$\vartheta$", color="C1", fontsize=13)
    _ax.set_title(r"Rotating $\mathbf{v}$ about $\mathbf{u}$ by the angle $\vartheta$",
                  style="italic", fontsize=11)
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch17_rodrigues.svg")
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So far $\mathbf R(\mathbf u, \vartheta)$ is just a matrix. [Euler's Rotation Theorem](#ch17-thm-eulers-rotation-theorem) below shows it is always a rotation matrix and, more surprisingly, that *every* rotation matrix is a single turn about some axis.

    /// admonition | 📐 **Theorem (Euler's Rotation Theorem)**
        attrs: {class: theorem, id: ch17-thm-eulers-rotation-theorem}
    1. $\mathbf R(\mathbf u, \vartheta) \in SO(3)$ for every unit vector $\mathbf u$ and angle $\vartheta$.
    2. Every $\mathbf R \in SO(3)$ equals $\mathbf R(\mathbf u, \vartheta)$ for some unit vector $\mathbf u$ and some $\vartheta \in [0, \pi]$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    1. Choose a unit vector $\mathbf a \perp \mathbf u$ and let $\mathbf b := \mathbf u\times\mathbf a$. The matrix $\mathbf B := [\mathbf u\ \mathbf a\ \mathbf b]$ has perpendicular unit columns with $\mathbf u\times\mathbf a = \mathbf b$, so $\mathbf B \in SO(3)$. From the definition, $\mathbf R(\mathbf u, \vartheta)\mathbf u = \mathbf u$, $\ \mathbf R(\mathbf u, \vartheta)\mathbf a = \cos\vartheta\,\mathbf a + \sin\vartheta\,\mathbf b$, and, since $\mathbf u\times\mathbf b = \mathbf u\times(\mathbf u\times\mathbf a) = -\mathbf a$, $\ \mathbf R(\mathbf u, \vartheta)\mathbf b = \cos\vartheta\,\mathbf b - \sin\vartheta\,\mathbf a$. These three equations say $\mathbf R(\mathbf u, \vartheta)\mathbf B = \mathbf B\,\mathbf R_x(\vartheta)$ column by column, so $\mathbf R(\mathbf u, \vartheta) = \mathbf B\,\mathbf R_x(\vartheta)\,\mathbf B^\top \in SO(3)$ by properties 1 and 2.
    2. First, $\det(\mathbf R - \mathbf I) = \det\big(\mathbf R(\mathbf I - \mathbf R^\top)\big) = \det\mathbf R\,\det\big((\mathbf I - \mathbf R)^\top\big) = \det(\mathbf I - \mathbf R) = (-1)^3\det(\mathbf R - \mathbf I)$, so $\det(\mathbf R - \mathbf I) = 0$. Hence $1$ is an eigenvalue of $\mathbf R$: there is a unit vector $\mathbf u$ with $\mathbf R\mathbf u = \mathbf u$. Choose $\mathbf a$, $\mathbf b$ as in part 1. By property 3, $\mathbf R\mathbf a$ is a unit vector with $\mathbf R\mathbf a\cdot\mathbf u = \mathbf R\mathbf a\cdot\mathbf R\mathbf u = \mathbf a\cdot\mathbf u = 0$, so it lies in the plane spanned by $\mathbf a$ and $\mathbf b$: $\mathbf R\mathbf a = \cos\vartheta\,\mathbf a + \sin\vartheta\,\mathbf b$ with $\vartheta := \operatorname{atan2}(\mathbf R\mathbf a\cdot\mathbf b, \mathbf R\mathbf a\cdot\mathbf a)$. By property 4, $\mathbf R\mathbf b = \mathbf R\mathbf u\times\mathbf R\mathbf a = \cos\vartheta\,\mathbf b - \sin\vartheta\,\mathbf a$. So $\mathbf R$ and $\mathbf R(\mathbf u, \vartheta)$ agree on the basis $\mathbf u, \mathbf a, \mathbf b$, hence everywhere. Finally, Rodrigues' formula shows $\mathbf R(-\mathbf u, -\vartheta) = \mathbf R(\mathbf u, \vartheta)$, so if $\vartheta < 0$ we may replace $(\mathbf u, \vartheta)$ by $(-\mathbf u, -\vartheta)$. $\blacksquare$
    ///

    /// admonition | 📐 **Corollary (Angle and Axis from the Matrix)**
        attrs: {class: corollary, id: ch17-cor-angle-and-axis-from-the-matrix}
    $\operatorname{tr}\mathbf R(\mathbf u, \vartheta) = 1 + 2\cos\vartheta$ and $\mathbf R(\mathbf u, \vartheta) - \mathbf R(\mathbf u, \vartheta)^\top = 2\sin\vartheta\,[\mathbf u]_\times$. Consequently, for $\mathbf R \in SO(3)$ the angle $\vartheta \in [0, \pi]$ in Euler's theorem is $\vartheta = \arccos\tfrac{\operatorname{tr}\mathbf R - 1}{2}$, and

    - if $0 < \vartheta < \pi$, the axis is unique: $[\mathbf u]_\times = (\mathbf R - \mathbf R^\top)/(2\sin\vartheta)$;
    - if $\vartheta = 0$, then $\mathbf R = \mathbf I$ and every axis works;
    - if $\vartheta = \pi$, then $\mathbf R = 2\mathbf u\mathbf u^\top - \mathbf I$, which determines $\mathbf u$ up to sign: both $\pm\mathbf u$ work.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    $\operatorname{tr}\mathbf I = 3$, $\operatorname{tr}[\mathbf u]_\times = 0$, and $\operatorname{tr}[\mathbf u]_\times^2 = \operatorname{tr}(\mathbf u\mathbf u^\top) - 3 = 1 - 3 = -2$, so Rodrigues' formula gives $\operatorname{tr}\mathbf R = 3 - 2(1 - \cos\vartheta)$. Since $[\mathbf u]_\times^\top = -[\mathbf u]_\times$ while $\mathbf I$ and $[\mathbf u]_\times^2$ are symmetric, $\mathbf R - \mathbf R^\top = 2\sin\vartheta\,[\mathbf u]_\times$. On $[0, \pi]$, $\cos$ is one-to-one, which gives $\vartheta$; for $0 < \vartheta < \pi$, $\sin\vartheta > 0$ gives $\mathbf u$. At $\vartheta = \pi$, Rodrigues' formula reads $\mathbf R = \mathbf I + 2(\mathbf u\mathbf u^\top - \mathbf I)$. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch17-sec-rotation-vectors-and-the-exponential-map -->
    ## Rotation Vectors and the Exponential Map

    An axis–angle pair uses four numbers tied together by one constraint, $\|\mathbf u\| = 1$. Multiplying them packs the same information into a single vector.

    /// note | 📖 **Definition**
    <u>**Rotation vector**</u>

    A rotation vector of a rotation matrix $\mathbf R$ is a vector $\boldsymbol\theta \in \mathbb R^3$ with $\mathbf R = \operatorname{Exp}(\boldsymbol\theta)$, where
    $$\operatorname{Exp}(\boldsymbol\theta) := \mathbf R\big(\boldsymbol\theta/\|\boldsymbol\theta\|,\ \|\boldsymbol\theta\|\big)\ \text{ for } \boldsymbol\theta \ne \mathbf 0,\qquad \operatorname{Exp}(\mathbf 0) := \mathbf I.$$
    That is, the direction of $\boldsymbol\theta$ is a rotation axis of $\mathbf R$ and its length is the rotation angle: $\boldsymbol\theta = \vartheta\mathbf u$.
    ///

    By Euler's rotation theorem every rotation matrix has a rotation vector with $\|\boldsymbol\theta\| \le \pi$. The name $\operatorname{Exp}$ is no accident.

    /// admonition | 📐 **Theorem (Rotation Vectors and the Matrix Exponential)**
        attrs: {class: theorem, id: ch17-thm-rotation-vectors-and-the-matrix-exponential}
    For every $\boldsymbol\theta \in \mathbb R^3$, $\ \operatorname{Exp}(\boldsymbol\theta) = \exp\big([\boldsymbol\theta]_\times\big)$, the matrix exponential of the cross-product matrix.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    For $\boldsymbol\theta = \mathbf 0$ both sides are $\mathbf I$. Otherwise write $\boldsymbol\theta = \vartheta\mathbf u$ with $\|\mathbf u\| = 1$. From the proof of Rodrigues' formula, $[\mathbf u]_\times^2 = \mathbf u\mathbf u^\top - \mathbf I$, and $[\mathbf u]_\times\mathbf u = \mathbf u\times\mathbf u = \mathbf 0$, so $[\mathbf u]_\times^3 = [\mathbf u]_\times(\mathbf u\mathbf u^\top - \mathbf I) = -[\mathbf u]_\times$. By induction, for $m \ge 0$, $[\mathbf u]_\times^{2m+1} = (-1)^m[\mathbf u]_\times$, and for $m \ge 1$, $[\mathbf u]_\times^{2m} = (-1)^{m-1}[\mathbf u]_\times^2$. The exponential series converges absolutely ([Appendix D: The Matrix Exponential](#appd-sec-the-matrix-exponential)), so we may group its odd and even terms:
    $$\exp(\vartheta[\mathbf u]_\times) = \mathbf I + \Big(\sum_{m\ge 0}\frac{(-1)^m\vartheta^{2m+1}}{(2m+1)!}\Big)[\mathbf u]_\times + \Big(\sum_{m\ge 1}\frac{(-1)^{m-1}\vartheta^{2m}}{(2m)!}\Big)[\mathbf u]_\times^2 = \mathbf I + \sin\vartheta\,[\mathbf u]_\times + (1 - \cos\vartheta)[\mathbf u]_\times^2,$$
    using the power series of $\sin$ and $\cos$ ([Appendix C: Exponential and Logarithm](#appc-sec-exponential-and-logarithm)). By Rodrigues' formula this is $\mathbf R(\mathbf u, \vartheta) = \operatorname{Exp}(\boldsymbol\theta)$. $\blacksquare$
    ///

    The exponential form makes several properties one-liners. For $\mathbf a, \boldsymbol\theta \in \mathbb R^3$, $\mathbf R \in SO(3)$, and scalars $s, t$:

    - $\operatorname{Exp}(-\boldsymbol\theta) = \exp([\boldsymbol\theta]_\times^\top) = \operatorname{Exp}(\boldsymbol\theta)^\top$, because transposing the series transposes each term.
    - $\operatorname{Exp}(\mathbf R\mathbf a) = \mathbf R\operatorname{Exp}(\mathbf a)\mathbf R^\top$, because $[\mathbf R\mathbf a]_\times = \mathbf R[\mathbf a]_\times\mathbf R^\top$ (property 5) and $(\mathbf R\mathbf A\mathbf R^\top)^m = \mathbf R\mathbf A^m\mathbf R^\top$.
    - $\operatorname{Exp}(s\mathbf u)\operatorname{Exp}(t\mathbf u) = \operatorname{Exp}((s+t)\mathbf u)$: turns about the same axis add, because $[s\mathbf u]_\times$ and $[t\mathbf u]_\times$ commute.
    - In general $\operatorname{Exp}(\mathbf a)\operatorname{Exp}(\mathbf b) \ne \operatorname{Exp}(\mathbf a + \mathbf b)$, because rotations about different axes do not commute.

    The inverse direction uses the corollary above: $\operatorname{Log}(\mathbf R) := \vartheta\mathbf u$ with $\vartheta = \arccos\tfrac{\operatorname{tr}\mathbf R - 1}{2} \in [0, \pi]$ and $\mathbf u$ as given there (choosing either sign at $\vartheta = \pi$), so that $\operatorname{Exp}(\operatorname{Log}\mathbf R) = \mathbf R$. The `Exp` and `Log` functions in the code above implement exactly these formulas.
    """)
    return


@app.cell(hide_code=True)
def _(exp_example, mo):
    mo.md(rf"""
    {exp_example}
    """)
    return


@app.cell
def _(Exp, Log, np):
    # jb: include=false
    _a = np.array([np.pi / 2, 0.0, 0.0])
    _b = np.array([0.0, np.pi / 2, 0.0])
    _ang_prod = np.degrees(np.linalg.norm(Log(Exp(_a) @ Exp(_b))))
    _ang_sum = np.degrees(np.linalg.norm(_a + _b))
    exp_example = (
        r"For example, a $90^\circ$ turn about East followed by a $90^\circ$ turn about North is a single turn of "
        + rf"$\|\operatorname{{Log}}(\operatorname{{Exp}}(\mathbf a)\operatorname{{Exp}}(\mathbf b))\| = {_ang_prod:.1f}^\circ$, "
        + r"whereas $\operatorname{Exp}(\mathbf a + \mathbf b)$ is a turn of "
        + rf"$\|\mathbf a + \mathbf b\| = {_ang_sum:.1f}^\circ$ about a different axis."
    )
    return (exp_example,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch17-sec-integrating-a-constant-angular-velocity -->
    ### Integrating a Constant Angular Velocity

    The exponential map solves the angular-velocity equation exactly when the rate is constant. This is the basis of every attitude update in Chapters 18–21.

    /// admonition | 📐 **Theorem (Constant Angular Velocity)**
        attrs: {class: theorem, id: ch17-thm-constant-angular-velocity}
    If $\dot{\mathbf R} = \mathbf R[\boldsymbol\omega]_\times$ on an interval $[t_0, t_1]$ with $\boldsymbol\omega$ constant, then $\mathbf R(t) = \mathbf R(t_0)\operatorname{Exp}\big(\boldsymbol\omega\,(t - t_0)\big)$ for all $t$ in the interval.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    Let $\mathbf X(t) := \mathbf R(t)\exp\big(-(t - t_0)[\boldsymbol\omega]_\times\big)$. By the product rule and $\tfrac{d}{dt}\exp(t\mathbf A) = \exp(t\mathbf A)\mathbf A$,
    $$\dot{\mathbf X} = \mathbf R[\boldsymbol\omega]_\times\exp\big(-(t-t_0)[\boldsymbol\omega]_\times\big) - \mathbf R\,\exp\big(-(t-t_0)[\boldsymbol\omega]_\times\big)[\boldsymbol\omega]_\times = \mathbf 0,$$
    because $[\boldsymbol\omega]_\times$ commutes with every power of itself and hence with its exponential. So $\mathbf X(t) = \mathbf X(t_0) = \mathbf R(t_0)$; multiply on the right by $\exp((t - t_0)[\boldsymbol\omega]_\times)$, the inverse of $\exp(-(t - t_0)[\boldsymbol\omega]_\times)$. $\blacksquare$
    ///

    With gyroscope samples $\boldsymbol\omega_k$ at period $\Delta t$, this gives the discrete attitude update
    $$\mathbf R_k = \mathbf R_{k-1}\operatorname{Exp}(\boldsymbol\omega_k\Delta t).$$
    The body rate multiplies on the **right**, because $\boldsymbol\omega$ is expressed in body coordinates (compare the lemma on rotating about a body axis).

    /// caution | ⚠️ **Assumptions and Failure Modes**
    - **Constant rate within each step.** If $\boldsymbol\omega$ changes direction during a sample period, the true increment is not $\operatorname{Exp}(\boldsymbol\omega_k\Delta t)$, because rotations about different axes do not commute. The resulting error (called *coning* in the navigation literature) is small at 100 Hz for walking motion but grows with vibration and lower sample rates.
    - **Rounding.** Each product $\mathbf R_{k-1}\operatorname{Exp}(\cdot)$ is computed in floating point, so after many steps $\mathbf R_k$ drifts slightly away from $SO(3)$. Practical code re-orthonormalizes occasionally, or stores the attitude as a quaternion and normalizes it ([Chapter 18](#ch18-sec-why-not-just-use-eulers-method)).
    - **Tiny angles.** Evaluating $\sin\vartheta/\vartheta$ and $(1 - \cos\vartheta)/\vartheta^2$ naively loses precision for very small $\vartheta$; use their Taylor series there.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch17-sec-small-angles -->
    ## Small Angles

    Attitude *errors* in a working filter are small: a fraction of a degree to a few degrees. For such rotations the exponential is nearly linear.

    /// admonition | 📐 **Theorem (Small-Angle Approximation)**
        attrs: {class: theorem, id: ch17-thm-small-angle-approximation}
    For every $\delta\boldsymbol\theta \in \mathbb R^3$ with $\vartheta := \|\delta\boldsymbol\theta\|$ and every $\mathbf v \in \mathbb R^3$,
    $$\big\|\big(\operatorname{Exp}(\delta\boldsymbol\theta) - \mathbf I - [\delta\boldsymbol\theta]_\times\big)\mathbf v\big\| \le \Big(\frac{\vartheta^2}{2} + \frac{\vartheta^3}{6}\Big)\|\mathbf v\|.$$
    So $\operatorname{Exp}(\delta\boldsymbol\theta) = \mathbf I + [\delta\boldsymbol\theta]_\times$ up to an error of second order in $\vartheta$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    For $\vartheta = 0$ there is nothing to prove. Otherwise, with $\delta\boldsymbol\theta = \vartheta\mathbf u$, Rodrigues' formula gives $\operatorname{Exp}(\delta\boldsymbol\theta) - \mathbf I - [\delta\boldsymbol\theta]_\times = (\sin\vartheta - \vartheta)[\mathbf u]_\times + (1 - \cos\vartheta)[\mathbf u]_\times^2$. From the proof of Rodrigues' formula, $\|[\mathbf u]_\times\mathbf v\| = \|\mathbf u\times\mathbf v_\perp\| = \|\mathbf v_\perp\| \le \|\mathbf v\|$ and $\|[\mathbf u]_\times^2\mathbf v\| = \|\mathbf v_\perp\| \le \|\mathbf v\|$. Taylor's theorem with the Lagrange remainder gives $|\sin\vartheta - \vartheta| \le \vartheta^3/6$ and $0 \le 1 - \cos\vartheta \le \vartheta^2/2$. The triangle inequality finishes the proof. $\blacksquare$
    ///

    Three consequences are used repeatedly in the rest of the book:

    1. **Small rotations commute to first order.** Writing $\operatorname{Exp}(\mathbf a) = \mathbf I + [\mathbf a]_\times + (\text{second order})$ and likewise for $\mathbf b$, $\ \operatorname{Exp}(\mathbf a)\operatorname{Exp}(\mathbf b) = \mathbf I + [\mathbf a + \mathbf b]_\times + (\text{second order})$, where "second order" means bounded by a constant times $\max(\|\mathbf a\|, \|\mathbf b\|)^2$ when both are at most 1. The order of small rotations only matters at second order.
    2. **Small Euler angles are a rotation vector.** Rodrigues' formula with $\mathbf u = \mathbf e_x$ reproduces $\mathbf R_x(\phi)$, so $\mathbf R_x(\phi) = \operatorname{Exp}(\phi\,\mathbf e_x)$, and likewise for $y$ and $z$. By consequence 1, $\mathbf R_z(\psi)\mathbf R_y(\theta)\mathbf R_x(\phi) = \mathbf I + \big[[\phi, \theta, \psi]^\top\big]_\times + (\text{second order})$.
    3. **The error-state convention.** If $\hat{\mathbf R}$ is an estimate of the true attitude $\mathbf R$, we describe the error by the small rotation vector $\delta\boldsymbol\theta := \operatorname{Log}(\hat{\mathbf R}^\top\mathbf R)$, so that
    $$\mathbf R = \hat{\mathbf R}\operatorname{Exp}(\delta\boldsymbol\theta) \approx \hat{\mathbf R}\big(\mathbf I + [\delta\boldsymbol\theta]_\times\big).$$
    Because $\operatorname{Exp}(\delta\boldsymbol\theta)$ multiplies on the right, $\delta\boldsymbol\theta$ is expressed in body coordinates (a *right* or *body-frame* perturbation). By the conjugation property of $\operatorname{Exp}$, the same error in navigation coordinates is $\hat{\mathbf R}\,\delta\boldsymbol\theta$, since $\hat{\mathbf R}\operatorname{Exp}(\delta\boldsymbol\theta) = \operatorname{Exp}(\hat{\mathbf R}\,\delta\boldsymbol\theta)\hat{\mathbf R}$. [Chapter 19](ch19_ahrs.md) and [Chapter 21](ch21_zero_velocity_updates.md) use exactly this convention.
    """)
    return


@app.cell(hide_code=True)
def _(mo, small_angle_table):
    mo.md(rf"""
    How small is "small"? The table compares $\operatorname{{Exp}}(\delta\boldsymbol\theta)$ with $\mathbf I + [\delta\boldsymbol\theta]_\times$ for a rotation about a fixed oblique axis (largest entry difference) and with the bound of the theorem.

    {small_angle_table}

    At $1^\circ$ the linearization is accurate to about $10^{{-4}}$; at $30^\circ$ it is off by more than $10\%$.
    """)
    return


@app.cell
def _(Exp, np, skew):
    # jb: include=false
    _u = np.array([1.0, 2.0, -2.0]) / 3.0
    _rows = ["| angle | max entry error | bound $\\vartheta^2/2 + \\vartheta^3/6$ |", "|:---|:---:|:---:|"]
    for _deg in [1, 5, 10, 30]:
        _t = np.radians(_deg)
        _err = np.abs(Exp(_t * _u) - np.eye(3) - skew(_t * _u)).max()
        _rows.append(rf"| {_deg}$^\circ$ | {_err:.1e} | {_t**2/2 + _t**3/6:.1e} |")
    small_angle_table = "\n".join(_rows)
    return (small_angle_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
    The first-order formulas are only as good as the angle is small. A filter whose attitude error grows to tens of degrees (for example after a bad initialization) linearizes about the wrong point, and its Jacobians, built from $\mathbf I + [\delta\boldsymbol\theta]_\times$, can point the correction in the wrong direction. This is the rotational version of the extended Kalman filter's failure modes in [Chapter 15](#ch15-sec-failure-modes).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch17-sec-why-three-numbers-are-never-enough -->
    ## Why Three Numbers Are Never Enough

    Euler angles fail at gimbal lock and jump at $\pm 180^\circ$. The rotation vector $\operatorname{Log}(\mathbf R)$ also jumps: at $\vartheta = \pi$ it switches between $\pi\mathbf u$ and $-\pi\mathbf u$, two very different vectors for nearly the same rotation. The Gibbs vector $\tan(\vartheta/2)\,\mathbf u$, another popular choice, is infinite at $\vartheta = \pi$. This is not bad luck.

    /// admonition | 📐 **Theorem (No Global Three-Parameter Description)**
        attrs: {class: theorem, id: ch17-thm-no-global-three-parameter-description}
    There is no continuous injective function from $SO(3)$ to $\mathbb R^3$. Consequently, every way of assigning three real numbers to every rotation either jumps somewhere (is discontinuous) or assigns the same numbers to two different rotations.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: proof}
    *Sketch.* The full argument uses topology beyond this book; see @stuelpnagel1964. In outline, regard $SO(3)$ as a subset of $\mathbb R^9$ (the nine entries).

    1. $SO(3)$ is *compact*[^compact]: it is closed (it is defined by the continuous equations $\mathbf R^\top\mathbf R = \mathbf I$ and $\det\mathbf R = 1$) and bounded (every entry has absolute value at most 1, because the columns are unit vectors).
    2. $SO(3)$ is three-dimensional in the precise sense that near every $\mathbf R$ it looks like a ball in $\mathbb R^3$: the map $\boldsymbol\theta \mapsto \mathbf R\operatorname{Exp}(\boldsymbol\theta)$, restricted to $\|\boldsymbol\theta\| < \pi$, is a continuous bijection onto a neighborhood of $\mathbf R$ with continuous inverse $\mathbf R' \mapsto \operatorname{Log}(\mathbf R^\top\mathbf R')$.
    3. Suppose $f: SO(3) \to \mathbb R^3$ were continuous and injective. Composing $f$ with the maps of step 2 gives continuous injective maps from open balls of $\mathbb R^3$ into $\mathbb R^3$. By Brouwer's [invariance of domain](https://en.wikipedia.org/wiki/Invariance_of_domain) theorem such maps have open images, so $f(SO(3))$ is open in $\mathbb R^3$. It is also compact (a continuous image of a compact set), hence closed. The only nonempty subset of $\mathbb R^3$ that is both open and closed is $\mathbb R^3$ itself, which is unbounded, hence not compact. This contradiction shows no such $f$ exists. $\blacksquare$
    ///

    In practice the failure shows up in one of two ways: a jump (Euler angles wrapping at $\pm 180^\circ$, the rotation vector flipping at $\vartheta = \pi$) or a singular kinematic equation (gimbal lock, where angle rates become infinite). There are two ways out, and the next two chapters use one each:

    - **Use more than three numbers.** The matrix $\mathbf R$ itself uses nine numbers with six constraints. A *unit quaternion* uses four numbers with one constraint, has no singularities, and has a kinematic equation that is linear in the attitude. That is [Chapter 18](ch18_quaternions.md).
    - **Use three numbers only locally.** A small rotation vector $\delta\boldsymbol\theta$ measured from a reference attitude is perfectly well behaved near $\mathbf 0$, far from its jump at $\pi$. If the reference is updated after every step, the three numbers never get large. That is the error-state filter of [Chapter 19](#ch19-sec-an-error-state-kalman-filter).

    [^compact]: A subset of $\mathbb R^m$ is *open* if every point has a small ball around it inside the set, *closed* if its complement is open, and *compact* if it is closed and bounded (equivalent to the general definition by the [Heine–Borel theorem](https://en.wikipedia.org/wiki/Heine%E2%80%93Borel_theorem)).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- label: ch17-sec-summary -->
    ## Summary

    - A {term}`reference frame` is an origin with a right-handed triple of perpendicular unit axes. The navigation frame $n$ is ENU, the body frame $b$ is FLU, and $\mathbf v^n = \mathbf R^n_b\mathbf v^b$, where the columns of $\mathbf R^n_b$ are the body axes in navigation coordinates.
    - {term}`Rotation matrices <rotation matrix>` satisfy $\mathbf R^\top\mathbf R = \mathbf I$ and $\det\mathbf R = 1$. They form the {term}`special orthogonal group` $SO(3)$, preserve lengths, angles, and cross products, and compose as $\mathbf R^n_c = \mathbf R^n_b\mathbf R^b_c$.
    - {term}`Euler angles` write $\mathbf R^n_b = \mathbf R_z(\psi)\mathbf R_y(\theta)\mathbf R_x(\phi)$: yaw, then pitch about the new $y$ axis, then roll. In FLU/ENU, positive pitch is nose down. The angles are recovered with $\operatorname{atan2}$ and are unique for $|\theta| < 90^\circ$.
    - The {term}`angular velocity` is defined by $\dot{\mathbf R}^n_b = \mathbf R^n_b[\boldsymbol\omega^b]_\times$.
    - Euler-angle rates satisfy $\boldsymbol\omega^b = \mathbf W\dot{\boldsymbol\Theta}$ with $\det\mathbf W = \cos\theta$. At $\theta = \pm 90^\circ$ ({term}`gimbal lock`) $\mathbf W$ is singular; nearby, Euler-angle rates blow up.
    - Every rotation is a single turn about an axis ({term}`axis-angle representation`, Euler's rotation theorem), given by Rodrigues' formula, and $\operatorname{Exp}(\boldsymbol\theta) = \exp([\boldsymbol\theta]_\times)$ for the {term}`rotation vector` $\boldsymbol\theta = \vartheta\mathbf u$. For a constant rate, $\mathbf R(t) = \mathbf R(t_0)\operatorname{Exp}(\boldsymbol\omega(t - t_0))$.
    - Small rotations satisfy $\operatorname{Exp}(\delta\boldsymbol\theta) \approx \mathbf I + [\delta\boldsymbol\theta]_\times$, which defines the error-state convention $\mathbf R = \hat{\mathbf R}\operatorname{Exp}(\delta\boldsymbol\theta)$.
    - No continuous one-to-one description of all rotations by three numbers exists.

    <!-- label: ch17-sec-whats-next -->
    ## What's Next

    [Chapter 18](ch18_quaternions.md) introduces quaternions: four numbers on a unit sphere whose product composes rotations, whose kinematic equation $\dot q = \tfrac12 q\otimes[0, \boldsymbol\omega^b]$ is linear and never singular, and whose only quirk is that $q$ and $-q$ describe the same rotation. They are the attitude representation used in every filter for the rest of the book.
    """)
    return


if __name__ == "__main__":
    app.run()
