# /// script
# dependencies = [
#     "marimo>=0.25.1",
#     "matplotlib==3.11.2",
#     "numpy==2.5.3",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="Quaternions", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "Singularity-Free Attitude"
    abbreviations:
      ENU: east-north-up
      FLU: forward-left-up
      NED: north-east-down
      JPL: Jet Propulsion Laboratory
      IMU: inertial measurement unit
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
    IMAGES_DIR = Path(__file__).parent / "public"

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
    [Chapter 17](ch17_rotations_v2.md) ended with a negative result: no description of every rotation by three numbers is free of jumps and singularities. Quaternions get around it with one extra number. A unit quaternion is a point on the unit sphere in $\mathbb R^4$; multiplying quaternions composes rotations; and the attitude kinematics become the *linear* equation $\dot q = \tfrac12 q\otimes[0, \boldsymbol\omega^b]$, whose coefficients never blow up. Quaternions are also cheap: four numbers instead of nine, and restoring unit length after rounding is a single division. Every attitude filter in the rest of this book stores the attitude as a unit quaternion.

    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    The unit quaternion $q = [\cos\tfrac\vartheta2,\ \sin\tfrac\vartheta2\,\mathbf u]$ represents the rotation by $\vartheta$ about $\mathbf u$. Vectors rotate as $q\otimes[0, \mathbf v]\otimes q^*$, rotations compose by the Hamilton product $\otimes$, and attitude evolves by the singularity-free linear equation $\dot q = \tfrac12 q\otimes[0, \boldsymbol\omega^b]$. The one price is that $q$ and $-q$ represent the same rotation.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// seealso | 🔗 **Prerequisites**
        attrs: {class: no-icon}
    - [Chapter 17](ch17_rotations_v2.md): rotation matrices and their properties (especially $\mathbf R(\mathbf u\times\mathbf v) = \mathbf R\mathbf u\times\mathbf R\mathbf v$), ZYX Euler angles and their extraction, Rodrigues' formula, Euler's rotation theorem, rotation vectors and $\operatorname{Exp}$, angular velocity, and the constant-angular-velocity theorem. The rotation angle is written $\vartheta$ because $\theta$ is pitch.
    - [Appendix D: Cross Products and Skew-Symmetric Matrices](appendix_d_linear_algebra_v2.md): $\mathbf a\times(\mathbf b\times\mathbf c) = \mathbf b(\mathbf a\cdot\mathbf c) - \mathbf c(\mathbf a\cdot\mathbf b)$ and $(\mathbf a\times\mathbf b)\cdot\mathbf c = \mathbf a\cdot(\mathbf b\times\mathbf c)$.
    - [Appendix D: The Matrix Exponential](appendix_d_linear_algebra_v2.md): $\tfrac{d}{dt}\exp(t\mathbf A) = \mathbf A\exp(t\mathbf A) = \exp(t\mathbf A)\mathbf A$ and $\exp(-\mathbf A) = \exp(\mathbf A)^{-1}$.
    - [Chapter 3](ch3_sets_for_probability_v2.md): the definition of a {term}`field`, for one remark.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Quaternions

    Complex numbers multiply points of the plane, and multiplying by a unit complex number rotates the plane. In 1843 William Rowan Hamilton found the analog for three dimensions: it needs a four-dimensional number system ([Wikipedia: Quaternion](https://en.wikipedia.org/wiki/Quaternion)).

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Quaternion**</u>

    A quaternion is an element $q = [q_w, q_x, q_y, q_z]$ of $\mathbb H := \mathbb R^4$, also written $q = q_w + q_x\,i + q_y\,j + q_z\,k$. Its *scalar part* is $q_w$ and its *vector part* is $\mathbf q_v := [q_x, q_y, q_z]^\top \in \mathbb R^3$; we write $q = [q_w, \mathbf q_v]$. Quaternions are added and multiplied by real numbers as vectors of $\mathbb R^4$, and multiplied with each other by the Hamilton product.
    ///

    We identify a real number $a$ with the quaternion $[a, \mathbf 0]$ and a vector $\mathbf v \in \mathbb R^3$ with the *pure* quaternion $[0, \mathbf v]$; in particular $i$, $j$, $k$ are $[0, \mathbf e_x]$, $[0, \mathbf e_y]$, $[0, \mathbf e_z]$. Quaternions are plain (not bold) because they are not elements of $\mathbb R^3$.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Hamilton product**</u>

    The Hamilton product of quaternions $p = [p_w, \mathbf p_v]$ and $q = [q_w, \mathbf q_v]$ is
    $$p\otimes q := \big[\,p_wq_w - \mathbf p_v\cdot\mathbf q_v,\ \ p_w\mathbf q_v + q_w\mathbf p_v + \mathbf p_v\times\mathbf q_v\,\big].$$
    ///

    Written out in components,
    $$p\otimes q = \begin{bmatrix}p_wq_w - p_xq_x - p_yq_y - p_zq_z\\ p_wq_x + p_xq_w + p_yq_z - p_zq_y\\ p_wq_y - p_xq_z + p_yq_w + p_zq_x\\ p_wq_z + p_xq_y - p_yq_x + p_zq_w\end{bmatrix}.$$

    The definition reproduces Hamilton's famous rules. For example $i\otimes j = [0 - \mathbf e_x\cdot\mathbf e_y,\ \mathbf e_x\times\mathbf e_y] = [0, \mathbf e_z] = k$, while $j\otimes i = [0, \mathbf e_y\times\mathbf e_x] = -k$, and $i\otimes i = [-\mathbf e_x\cdot\mathbf e_x, \mathbf 0] = -1$. In full:
    $$i\otimes i = j\otimes j = k\otimes k = i\otimes j\otimes k = -1,\qquad i\otimes j = k = -j\otimes i,\quad j\otimes k = i = -k\otimes j,\quad k\otimes i = j = -i\otimes k.$$

    Four elementary facts follow straight from the definition:

    - **Real numbers act as scalars:** $[a, \mathbf 0]\otimes q = q\otimes[a, \mathbf 0] = a\,q$.
    - **Bilinearity:** every component of $p\otimes q$ is a sum of products of one component of $p$ and one of $q$, so $\otimes$ distributes over addition and real factors pull out. In particular the product rule $\tfrac{d}{dt}(p\otimes q) = \dot p\otimes q + p\otimes\dot q$ holds.
    - **Products of pure quaternions** combine the dot and cross products: $[0, \mathbf u]\otimes[0, \mathbf v] = [-\mathbf u\cdot\mathbf v,\ \mathbf u\times\mathbf v]$.
    - **Non-commutativity:** $p\otimes q - q\otimes p = [0,\ 2\,\mathbf p_v\times\mathbf q_v]$, because every other term is symmetric in $p$ and $q$. So $p$ and $q$ commute exactly when their vector parts are parallel.

    /// important | 📐 **Theorem (Associativity)**
        attrs: {class: no-icon}
    For all quaternions $p, q, r$: $(p\otimes q)\otimes r = p\otimes(q\otimes r)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Write $p = [a, \mathbf u]$, $q = [b, \mathbf v]$, $r = [c, \mathbf w]$. Expanding with the definition,
    $$(p\otimes q)\otimes r = \big[abc - c\,\mathbf u\cdot\mathbf v - a\,\mathbf v\cdot\mathbf w - b\,\mathbf u\cdot\mathbf w - (\mathbf u\times\mathbf v)\cdot\mathbf w,\ \ \mathbf s - (\mathbf u\cdot\mathbf v)\mathbf w + (\mathbf u\times\mathbf v)\times\mathbf w\big],$$
    $$p\otimes(q\otimes r) = \big[abc - c\,\mathbf u\cdot\mathbf v - a\,\mathbf v\cdot\mathbf w - b\,\mathbf u\cdot\mathbf w - \mathbf u\cdot(\mathbf v\times\mathbf w),\ \ \mathbf s - (\mathbf v\cdot\mathbf w)\mathbf u + \mathbf u\times(\mathbf v\times\mathbf w)\big],$$
    where $\mathbf s := ab\,\mathbf w + ac\,\mathbf v + bc\,\mathbf u + a\,\mathbf v\times\mathbf w + b\,\mathbf u\times\mathbf w + c\,\mathbf u\times\mathbf v$ collects the terms the two expansions share. The scalar parts agree because $(\mathbf u\times\mathbf v)\cdot\mathbf w = \mathbf u\cdot(\mathbf v\times\mathbf w)$. For the vector parts, the triple-product expansion gives
    $$(\mathbf u\times\mathbf v)\times\mathbf w = -\mathbf w\times(\mathbf u\times\mathbf v) = \mathbf v(\mathbf u\cdot\mathbf w) - \mathbf u(\mathbf v\cdot\mathbf w),\qquad \mathbf u\times(\mathbf v\times\mathbf w) = \mathbf v(\mathbf u\cdot\mathbf w) - \mathbf w(\mathbf u\cdot\mathbf v),$$
    so both remaining parts equal $\mathbf v(\mathbf u\cdot\mathbf w) - \mathbf u(\mathbf v\cdot\mathbf w) - \mathbf w(\mathbf u\cdot\mathbf v)$. $\blacksquare$
    ///

    Associativity lets us drop parentheses in products such as $q\otimes v\otimes q^*$. Because $\otimes$ is bilinear, multiplying by a fixed quaternion is a linear map of $\mathbb R^4$, so it has a $4\times 4$ matrix:
    $$p\otimes q = [p]_L\,q = [q]_R\,p,\qquad [p]_L = \begin{bmatrix}p_w & -\mathbf p_v^\top\\ \mathbf p_v & p_w\mathbf I + [\mathbf p_v]_\times\end{bmatrix},\quad [q]_R = \begin{bmatrix}q_w & -\mathbf q_v^\top\\ \mathbf q_v & q_w\mathbf I - [\mathbf q_v]_\times\end{bmatrix}.$$
    (Check the bottom rows against the definition: $\mathbf p_v q_w + (p_w\mathbf I + [\mathbf p_v]_\times)\mathbf q_v$ and $\mathbf q_v p_w + (q_w\mathbf I - [\mathbf q_v]_\times)\mathbf p_v$ both equal $p_w\mathbf q_v + q_w\mathbf p_v + \mathbf p_v\times\mathbf q_v$.)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conjugate, Norm, and Inverse

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Quaternion conjugate**</u>

    The conjugate of a quaternion $q = [q_w, \mathbf q_v]$ is $q^* := [q_w, -\mathbf q_v]$.
    ///

    The *norm* of a quaternion is its Euclidean norm as a vector of $\mathbb R^4$, $\|q\| := \sqrt{q_w^2 + q_x^2 + q_y^2 + q_z^2} = \sqrt{q_w^2 + \|\mathbf q_v\|^2}$.

    /// important | 📐 **Lemma (Conjugates)**
        attrs: {class: no-icon}
    For all quaternions $p, q$: (1) $(q^*)^* = q$; (2) $(p\otimes q)^* = q^*\otimes p^*$; (3) $q\otimes q^* = q^*\otimes q = \|q\|^2$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    (1) is immediate. (2) Write $p = [a, \mathbf u]$, $q = [b, \mathbf v]$. Then $(p\otimes q)^* = [ab - \mathbf u\cdot\mathbf v,\ -a\mathbf v - b\mathbf u - \mathbf u\times\mathbf v]$, and $q^*\otimes p^* = [b, -\mathbf v]\otimes[a, -\mathbf u] = [ab - \mathbf v\cdot\mathbf u,\ -b\mathbf u - a\mathbf v + \mathbf v\times\mathbf u]$; these agree because $\mathbf v\times\mathbf u = -\mathbf u\times\mathbf v$. (3) $[b, \mathbf v]\otimes[b, -\mathbf v] = [b^2 + \mathbf v\cdot\mathbf v,\ -b\mathbf v + b\mathbf v - \mathbf v\times\mathbf v] = [\|q\|^2, \mathbf 0]$, and the same computation with $\mathbf v$ replaced by $-\mathbf v$ gives $q^*\otimes q$. $\blacksquare$
    ///

    /// important | 📐 **Theorem (The Norm Is Multiplicative)**
        attrs: {class: no-icon}
    For all quaternions $p, q$: $\ \|p\otimes q\| = \|p\|\,\|q\|$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    By the lemma and associativity,
    $$\|p\otimes q\|^2 = (p\otimes q)\otimes(p\otimes q)^* = p\otimes(q\otimes q^*)\otimes p^* = p\otimes\|q\|^2\otimes p^* = \|q\|^2\,(p\otimes p^*) = \|q\|^2\|p\|^2,$$
    where we used that the real number $\|q\|^2$ acts as a scalar. Take square roots. $\blacksquare$
    ///

    For $q \ne 0$, the lemma shows that $q^{-1} := q^*/\|q\|^2$ satisfies $q\otimes q^{-1} = q^{-1}\otimes q = 1$, and it is the only such quaternion (if $r\otimes q = 1$ then $r = r\otimes q\otimes q^{-1} = q^{-1}$). So every nonzero quaternion has a multiplicative inverse: $\mathbb H$ satisfies every axiom of a {term}`field` except commutativity of multiplication.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Unit quaternion**</u>

    A unit quaternion is a quaternion $q$ with $\|q\| = 1$.
    ///

    For a unit quaternion, $q^{-1} = q^*$. By multiplicativity of the norm, products and conjugates of unit quaternions are again unit quaternions. Geometrically, the unit quaternions form the unit sphere in $\mathbb R^4$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Rotating Vectors with Unit Quaternions

    Start with a concrete case. Let $q = [\cos 45^\circ, 0, 0, \sin 45^\circ] = \tfrac{1}{\sqrt2}[1, 0, 0, 1]$ and $\mathbf v = \mathbf e_x$ (East). Then
    $$q\otimes[0, \mathbf e_x] = \tfrac{1}{\sqrt2}\big[-\mathbf e_z\cdot\mathbf e_x,\ \mathbf e_x + \mathbf e_z\times\mathbf e_x\big] = \tfrac{1}{\sqrt2}[0,\ \mathbf e_x + \mathbf e_y],$$
    $$q\otimes[0, \mathbf e_x]\otimes q^* = \tfrac12\,[0, \mathbf e_x + \mathbf e_y]\otimes[1, -\mathbf e_z] = \tfrac12\big[(\mathbf e_x + \mathbf e_y)\cdot\mathbf e_z,\ \mathbf e_x + \mathbf e_y - (\mathbf e_x + \mathbf e_y)\times\mathbf e_z\big] = \tfrac12[0,\ \mathbf e_x + \mathbf e_y + \mathbf e_y - \mathbf e_x] = [0, \mathbf e_y].$$
    The "sandwich" turned East into North: a $90^\circ$ rotation about Up, with $q = [\cos\tfrac{\vartheta}{2}, \sin\tfrac{\vartheta}{2}\,\mathbf e_z]$ for $\vartheta = 90^\circ$. Note the half angle. The general statement:

    /// important | 📐 **Theorem (Quaternion Rotation)**
        attrs: {class: no-icon}
    Let $q = [s, \mathbf w]$ be a unit quaternion. For every $\mathbf v \in \mathbb R^3$,
    $$q\otimes[0, \mathbf v]\otimes q^* = [0,\ \mathbf R(q)\mathbf v],\qquad \mathbf R(q) := (s^2 - \|\mathbf w\|^2)\,\mathbf I + 2\,\mathbf w\mathbf w^\top + 2s\,[\mathbf w]_\times.$$
    Every unit quaternion can be written $q = [\cos\tfrac\vartheta2,\ \sin\tfrac\vartheta2\,\mathbf u]$ with $\mathbf u$ a unit vector and $\vartheta \in [0, 2\pi]$, and then $\mathbf R(q) = \mathbf R(\mathbf u, \vartheta) = \operatorname{Exp}(\vartheta\mathbf u)$. In particular, $\mathbf R(q) \in SO(3)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    First, $q\otimes[0, \mathbf v] = [-\mathbf w\cdot\mathbf v,\ s\mathbf v + \mathbf w\times\mathbf v]$. Multiplying on the right by $q^* = [s, -\mathbf w]$, the scalar part is $-s\,\mathbf w\cdot\mathbf v + (s\mathbf v + \mathbf w\times\mathbf v)\cdot\mathbf w = 0$ (because $(\mathbf w\times\mathbf v)\cdot\mathbf w = 0$), and the vector part is
    $$(\mathbf w\cdot\mathbf v)\mathbf w + s(s\mathbf v + \mathbf w\times\mathbf v) - (s\mathbf v + \mathbf w\times\mathbf v)\times\mathbf w = (\mathbf w\cdot\mathbf v)\mathbf w + s^2\mathbf v + 2s\,\mathbf w\times\mathbf v - (\mathbf w\times\mathbf v)\times\mathbf w.$$
    By the triple-product expansion, $(\mathbf w\times\mathbf v)\times\mathbf w = -\mathbf w\times(\mathbf w\times\mathbf v) = \|\mathbf w\|^2\mathbf v - (\mathbf w\cdot\mathbf v)\mathbf w$, so the vector part is $(s^2 - \|\mathbf w\|^2)\mathbf v + 2(\mathbf w\cdot\mathbf v)\mathbf w + 2s\,\mathbf w\times\mathbf v = \mathbf R(q)\mathbf v$.

    For the second claim, $s^2 + \|\mathbf w\|^2 = 1$ gives $s \in [-1, 1]$; let $\vartheta := 2\arccos s \in [0, 2\pi]$, so that $s = \cos\tfrac\vartheta2$ and $\|\mathbf w\| = \sqrt{1 - s^2} = \sin\tfrac\vartheta2$. Take $\mathbf u := \mathbf w/\|\mathbf w\|$ if $\mathbf w \ne \mathbf 0$ (any unit vector otherwise). Substituting and using $\cos^2\tfrac\vartheta2 - \sin^2\tfrac\vartheta2 = \cos\vartheta$, $2\sin^2\tfrac\vartheta2 = 1 - \cos\vartheta$, and $2\sin\tfrac\vartheta2\cos\tfrac\vartheta2 = \sin\vartheta$:
    $$\mathbf R(q)\mathbf v = \cos\vartheta\,\mathbf v + (1 - \cos\vartheta)(\mathbf u\cdot\mathbf v)\mathbf u + \sin\vartheta\,\mathbf u\times\mathbf v.$$
    Rodrigues' formula ([Chapter 17](ch17_rotations_v2.md)) gives the same expression for $\mathbf R(\mathbf u, \vartheta)\mathbf v$, because $[\mathbf u]_\times^2\mathbf v = (\mathbf u\cdot\mathbf v)\mathbf u - \mathbf v$. Finally, $\mathbf R(\mathbf u, \vartheta) = \operatorname{Exp}(\vartheta\mathbf u) \in SO(3)$ by Chapter 17. $\blacksquare$
    ///

    In components (using $q_w^2 + q_x^2 + q_y^2 + q_z^2 = 1$ to simplify the diagonal), the theorem's matrix is
    $$\mathbf R(q) = \begin{bmatrix}1 - 2(q_y^2 + q_z^2) & 2(q_xq_y - q_wq_z) & 2(q_xq_z + q_wq_y)\\ 2(q_xq_y + q_wq_z) & 1 - 2(q_x^2 + q_z^2) & 2(q_yq_z - q_wq_x)\\ 2(q_xq_z - q_wq_y) & 2(q_yq_z + q_wq_x) & 1 - 2(q_x^2 + q_y^2)\end{bmatrix}.$$

    **Our convention.** The attitude quaternion $q^n_b$ is the unit quaternion with $\mathbf R(q^n_b) = \mathbf R^n_b$, so it rotates body coordinates into navigation coordinates:
    $$[0, \mathbf v^n] = q^n_b\otimes[0, \mathbf v^b]\otimes(q^n_b)^*.$$

    /// important | 📐 **Theorem (Composition)**
        attrs: {class: no-icon}
    For unit quaternions $p, q$: $\ \mathbf R(p\otimes q) = \mathbf R(p)\,\mathbf R(q)$ and $\mathbf R(q^*) = \mathbf R(q)^\top$. Hence $q^n_c = q^n_b\otimes q^b_c$, in the same order as $\mathbf R^n_c = \mathbf R^n_b\mathbf R^b_c$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    By associativity and the conjugate lemma, $(p\otimes q)\otimes[0, \mathbf v]\otimes(p\otimes q)^* = p\otimes\big(q\otimes[0, \mathbf v]\otimes q^*\big)\otimes p^* = p\otimes[0, \mathbf R(q)\mathbf v]\otimes p^* = [0, \mathbf R(p)\mathbf R(q)\mathbf v]$ for every $\mathbf v$. Next, $\mathbf R(q^*)\mathbf R(q) = \mathbf R(q^*\otimes q) = \mathbf R(1) = \mathbf I$, so $\mathbf R(q^*) = \mathbf R(q)^{-1} = \mathbf R(q)^\top$. $\blacksquare$
    ///

    Composing two attitudes costs 16 multiplications with quaternions and 27 with $3\times 3$ matrices, and a quaternion needs four numbers of storage instead of nine.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Double Cover

    $\mathbf R(q)$ is quadratic in $q$, so $\mathbf R(-q) = \mathbf R(q)$: a rotation has (at least) two quaternions. There are no others.

    /// important | 📐 **Theorem (Two Quaternions per Rotation)**
        attrs: {class: no-icon}
    For unit quaternions $p, q$: $\ \mathbf R(p) = \mathbf R(q)$ if and only if $p = q$ or $p = -q$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    "If" was just shown. Conversely, suppose $\mathbf R(p) = \mathbf R(q)$, and let $r := q^*\otimes p = [s, \mathbf w]$, a unit quaternion with $\mathbf R(r) = \mathbf R(q)^\top\mathbf R(p) = \mathbf I$. Suppose $\mathbf w \ne \mathbf 0$ and pick a unit vector $\mathbf v \perp \mathbf w$. Then $\mathbf v = \mathbf R(r)\mathbf v = (s^2 - \|\mathbf w\|^2)\mathbf v + 2s\,\mathbf w\times\mathbf v$. The vector $\mathbf w\times\mathbf v$ is nonzero and perpendicular to $\mathbf v$, so comparing components gives $s = 0$ and then $-\|\mathbf w\|^2 = 1$, which is impossible. Hence $\mathbf w = \mathbf 0$, $s = \pm 1$, and $p = q\otimes r = \pm q$. $\blacksquare$
    ///

    In practice we also need to go back from a matrix to its two quaternions.

    /// important | 📐 **Theorem (Quaternion from a Rotation Matrix)**
        attrs: {class: no-icon}
    If $q$ is a unit quaternion and $\mathbf R(q) = \mathbf R$ has entries $r_{ij}$, then
    $$4q_w^2 = 1 + r_{11} + r_{22} + r_{33},\quad 4q_x^2 = 1 + r_{11} - r_{22} - r_{33},\quad 4q_y^2 = 1 - r_{11} + r_{22} - r_{33},\quad 4q_z^2 = 1 - r_{11} - r_{22} + r_{33},$$
    $$4q_wq_x = r_{32} - r_{23},\quad 4q_wq_y = r_{13} - r_{31},\quad 4q_wq_z = r_{21} - r_{12},\quad 4q_xq_y = r_{12} + r_{21},\quad 4q_xq_z = r_{13} + r_{31},\quad 4q_yq_z = r_{23} + r_{32}.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Read off the component form of $\mathbf R(q)$. For example, $r_{11} + r_{22} + r_{33} = 3 - 4(q_x^2 + q_y^2 + q_z^2) = 4q_w^2 - 1$, $\ 1 + r_{11} - r_{22} - r_{33} = 4q_x^2$ after using $q_w^2 + q_x^2 + q_y^2 + q_z^2 = 1$, $\ r_{32} - r_{23} = 2(q_yq_z + q_wq_x) - 2(q_yq_z - q_wq_x) = 4q_wq_x$, and $r_{12} + r_{21} = 4q_xq_y$. The others are identical. $\blacksquare$
    ///

    **Algorithm.** The four squared components sum to $4$, so the largest is at least $1$. Take the positive square root of the largest (so that component is at least $\tfrac12$ in absolute value), then divide the three products containing it by four times that component to get the other three components. This returns one of $\pm q$ and never divides by a small number. (Using only the $q_w$ formulas, as many short codes do, fails near $180^\circ$ rotations, where $q_w \approx 0$.)

    The two theorems together say that unit quaternions cover the rotations exactly twice, and smoothly. The precise name for this is the following.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Double cover**</u>

    A continuous surjective function $f: X \to Y$ between subsets of Euclidean spaces is a double cover if every $y \in Y$ has exactly two preimages, and every $y \in Y$ has an open ball $B$ around it such that $f^{-1}[B\cap Y]$ is the union of two disjoint sets, on each of which $f$ is a bijection onto $B\cap Y$ with a continuous inverse.
    ///

    /// important | 📐 **Theorem (Unit Quaternions Doubly Cover the Rotations)**
        attrs: {class: no-icon}
    The function $q \mapsto \mathbf R(q)$ from the unit quaternions to $SO(3)$ is a double cover.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    The entries of $\mathbf R(q)$ are polynomials in $q$, so the map is continuous. It is surjective by Euler's rotation theorem and the quaternion-rotation theorem ($\mathbf R(\mathbf u, \vartheta) = \mathbf R([\cos\tfrac\vartheta2, \sin\tfrac\vartheta2\mathbf u])$). Each rotation has exactly the two preimages $\pm q$, which are distinct because $q \ne 0$. For the local condition, fix $\mathbf R_0 \in SO(3)$ and let $i$ be the index of the largest of the four expressions $1 + r_{11} + r_{22} + r_{33}$, $1 + r_{11} - r_{22} - r_{33}$, ... at $\mathbf R_0$, which is at least $1$. These expressions are continuous in the entries, so on a small enough ball $B$ around $\mathbf R_0$ the $i$-th one stays positive. On $B\cap SO(3)$ the algorithm above with index $i$ defines a continuous $g_+$ with $\mathbf R(g_+(\mathbf R)) = \mathbf R$ and $i$-th component positive; $g_- := -g_+$ is a second one. Every preimage of $\mathbf R \in B$ is $\pm g_+(\mathbf R)$, so $f^{-1}[B\cap SO(3)]$ is the union of the images of $g_+$ and $g_-$, which are disjoint (the sign of the $i$-th component differs), and $f$ is a bijection from each onto $B\cap SO(3)$ with continuous inverse $g_\pm$. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/ch18_double_cover_v2.svg" class="graphic" alt="Plot against rotation angle from 0 to 720 degrees about Up. The rotation-matrix entry cos(angle) completes two full periods, returning to 1 at 360 and 720 degrees. The quaternion components cos(angle/2) and sin(angle/2) complete only one period: at 360 degrees the quaternion is minus 1, and it returns to plus 1 only at 720 degrees." />

    The figure shows what this means for a body turning steadily about Up. After one full turn ($360^\circ$) the attitude is back where it started and $\mathbf R = \mathbf I$, but the quaternion, which tracked the motion continuously, has arrived at $-1$; it takes a second full turn to return to $+1$. (This is the mathematics behind the "plate trick"; see [Wikipedia: Plate trick](https://en.wikipedia.org/wiki/Plate_trick).) Practical consequences:

    - **Comparing attitudes.** Never measure attitude error by $\|\hat q - q\|$, which is about $2$ when $\hat q \approx -q$ even though the attitudes agree. Use the rotation angle of $q^*\otimes\hat q$, which is $2\arccos|\langle\hat q, q\rangle|$, where $\langle\hat q, q\rangle = \hat q_wq_w + \hat{\mathbf q}_v\cdot\mathbf q_v$ is the dot product in $\mathbb R^4$ (it is the scalar part of $q^*\otimes\hat q$).
    - **Do not flip signs inside a filter.** Integration keeps $q(t)$ continuous; arbitrarily replacing $q$ by $-q$ (for example, forcing $q_w \ge 0$ at every step) introduces jumps that break interpolation and averaging. Choose a sign only for display.
    - **Averaging and interpolating.** Before averaging or interpolating quaternions, flip them into the same hemisphere as a reference, $\langle q_i, q_{\text{ref}}\rangle \ge 0$.
    """)
    return


@app.cell
def make_double_cover_fig(IMAGES_DIR, np, plt):
    # jb: include=false
    _deg = np.linspace(0, 720, 721)
    _a = np.radians(_deg)
    _fig, _ax = plt.subplots(figsize=(7.5, 3.8))
    _ax.plot(_deg, np.cos(_a), color="0.3", ls="--", label=r"$r_{11} = \cos\vartheta$ (rotation matrix)")
    _ax.plot(_deg, np.cos(_a / 2), color="C0", label=r"$q_w = \cos(\vartheta/2)$")
    _ax.plot(_deg, np.sin(_a / 2), color="C1", label=r"$q_z = \sin(\vartheta/2)$")
    for _x in (360, 720):
        _ax.axvline(_x, color="k", lw=0.8)
    _ax.annotate(r"$\mathbf{R} = \mathbf{I}$ but $q = -1$", xy=(360, -1), xytext=(395, -0.72),
                 arrowprops=dict(arrowstyle="->", lw=0.8), fontsize=10,
                 bbox=dict(fc="white", ec="none", alpha=0.85))
    _ax.annotate(r"$q = +1$ again", xy=(720, 1), xytext=(560, 1.12),
                 arrowprops=dict(arrowstyle="->", lw=0.8), fontsize=10)
    _ax.set_xticks(np.arange(0, 721, 90))
    _ax.set_ylim(-1.25, 1.3)
    _ax.set_xlabel(r"rotation angle $\vartheta$ about Up (deg)")
    _ax.set_ylabel("component value")
    _ax.set_title("A full turn takes q to −q", style="italic")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.legend(loc="lower left", fontsize=9)
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "ch18_double_cover_v2.svg")
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conversions

    **Axis–angle and rotation vector.** By the quaternion-rotation theorem, the rotation vector $\boldsymbol\theta = \vartheta\mathbf u$ corresponds to
    $$\operatorname{Exp}_q(\boldsymbol\theta) := \Big[\cos\frac{\|\boldsymbol\theta\|}{2},\ \sin\frac{\|\boldsymbol\theta\|}{2}\,\frac{\boldsymbol\theta}{\|\boldsymbol\theta\|}\Big]\ \ (\boldsymbol\theta \ne \mathbf 0),\qquad \operatorname{Exp}_q(\mathbf 0) := [1, \mathbf 0],$$
    so that $\mathbf R(\operatorname{Exp}_q(\boldsymbol\theta)) = \operatorname{Exp}(\boldsymbol\theta)$. For a small rotation vector, $\operatorname{Exp}_q(\delta\boldsymbol\theta) \approx [1, \tfrac12\delta\boldsymbol\theta]$, since $\cos x = 1 - O(x^2)$ and $\sin x = x + O(x^3)$. Conversely, a unit quaternion with $\mathbf q_v \ne \mathbf 0$ has angle $\vartheta = 2\operatorname{atan2}(\|\mathbf q_v\|, q_w) \in (0, 2\pi)$ and axis $\mathbf q_v/\|\mathbf q_v\|$; replacing $q$ by $-q$ first when $q_w < 0$ gives the rotation vector $\operatorname{Log}_q(q)$ with $\|\operatorname{Log}_q(q)\| \le \pi$.

    **Rotation matrix.** $\mathbf R(q)$ by the component formula; $q$ from $\mathbf R$ by the largest-square algorithm above.

    **Euler angles.** The elementary rotations are $\mathbf R_x(\phi) = \operatorname{Exp}(\phi\,\mathbf e_x)$ and so on, so their quaternions are $q_x(\phi) := [\cos\tfrac\phi2, \sin\tfrac\phi2, 0, 0]$, $q_y(\theta) := [\cos\tfrac\theta2, 0, \sin\tfrac\theta2, 0]$, and $q_z(\psi) := [\cos\tfrac\psi2, 0, 0, \sin\tfrac\psi2]$. By the composition theorem the attitude with ZYX Euler angles $(\phi, \theta, \psi)$ is $q^n_b = q_z(\psi)\otimes q_y(\theta)\otimes q_x(\phi)$. Multiplying out, with $c_\phi := \cos\tfrac\phi2$, $s_\phi := \sin\tfrac\phi2$, and so on (half angles here),
    $$q^n_b = \begin{bmatrix}c_\phi c_\theta c_\psi + s_\phi s_\theta s_\psi\\ s_\phi c_\theta c_\psi - c_\phi s_\theta s_\psi\\ c_\phi s_\theta c_\psi + s_\phi c_\theta s_\psi\\ c_\phi c_\theta s_\psi - s_\phi s_\theta c_\psi\end{bmatrix}.$$
    In the other direction, apply Chapter 17's extraction to the entries of $\mathbf R(q)$:
    $$\phi = \operatorname{atan2}\big(2(q_yq_z + q_wq_x),\ 1 - 2(q_x^2 + q_y^2)\big),\quad \theta = \arcsin\big(2(q_wq_y - q_xq_z)\big),\quad \psi = \operatorname{atan2}\big(2(q_xq_y + q_wq_z),\ 1 - 2(q_y^2 + q_z^2)\big).$$
    Gimbal lock now lives only in this last conversion, where $2(q_wq_y - q_xq_z) = \pm 1$. The quaternion itself is perfectly well behaved there; only its translation into Euler angles is not.

    **Composition order.** Exactly as with matrices: a rotation expressed in body coordinates (such as a gyroscope increment) multiplies on the **right**, $q^n_b \leftarrow q^n_b\otimes\Delta q$; a rotation expressed in navigation coordinates multiplies on the **left**.

    The reference implementation below follows these formulas.
    """)
    return


@app.cell
def quaternion_library(np):
    # jb: echo=true
    def qmul(p, q):
        """Hamilton product p ⊗ q of scalar-first quaternions [w, x, y, z]."""
        pw, px, py, pz = p
        qw, qx, qy, qz = q
        return np.array([pw * qw - px * qx - py * qy - pz * qz,
                         pw * qx + px * qw + py * qz - pz * qy,
                         pw * qy - px * qz + py * qw + pz * qx,
                         pw * qz + px * qy - py * qx + pz * qw])

    def qconj(q):
        return np.array([q[0], -q[1], -q[2], -q[3]])

    def q_to_R(q):
        """Unit quaternion q^n_b -> rotation matrix R^n_b."""
        w, x, y, z = q
        return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
                         [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
                         [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)]])

    def R_to_q(R):
        """Rotation matrix -> one of its two unit quaternions (largest-square method)."""
        sq = np.array([1 + R[0, 0] + R[1, 1] + R[2, 2], 1 + R[0, 0] - R[1, 1] - R[2, 2],
                       1 - R[0, 0] + R[1, 1] - R[2, 2], 1 - R[0, 0] - R[1, 1] + R[2, 2]])
        i = int(np.argmax(sq))
        c = 0.5 * np.sqrt(sq[i])          # the largest component, >= 1/2
        f = 1.0 / (4.0 * c)
        if i == 0:
            q = [c, (R[2, 1] - R[1, 2]) * f, (R[0, 2] - R[2, 0]) * f, (R[1, 0] - R[0, 1]) * f]
        elif i == 1:
            q = [(R[2, 1] - R[1, 2]) * f, c, (R[0, 1] + R[1, 0]) * f, (R[0, 2] + R[2, 0]) * f]
        elif i == 2:
            q = [(R[0, 2] - R[2, 0]) * f, (R[0, 1] + R[1, 0]) * f, c, (R[1, 2] + R[2, 1]) * f]
        else:
            q = [(R[1, 0] - R[0, 1]) * f, (R[0, 2] + R[2, 0]) * f, (R[1, 2] + R[2, 1]) * f, c]
        return np.array(q)

    def q_exp(theta_vec):
        """Rotation vector -> unit quaternion Exp_q."""
        angle = np.linalg.norm(theta_vec)
        if angle < 1e-12:
            return np.array([1.0, *(0.5 * np.asarray(theta_vec))])
        return np.array([np.cos(angle / 2), *(np.sin(angle / 2) / angle * np.asarray(theta_vec))])

    def q_log(q):
        """Unit quaternion -> rotation vector with norm <= pi."""
        q = q if q[0] >= 0 else -q
        n = np.linalg.norm(q[1:])
        if n < 1e-12:
            return 2.0 * q[1:]
        return 2.0 * np.arctan2(n, q[0]) / n * q[1:]

    def euler_to_q(phi, theta, psi):
        """ZYX Euler angles (roll, pitch, yaw) -> q^n_b."""
        cf, sf = np.cos(phi / 2), np.sin(phi / 2)
        ct, st = np.cos(theta / 2), np.sin(theta / 2)
        cp, sp = np.cos(psi / 2), np.sin(psi / 2)
        return np.array([cf * ct * cp + sf * st * sp, sf * ct * cp - cf * st * sp,
                         cf * st * cp + sf * ct * sp, cf * ct * sp - sf * st * cp])

    def q_to_euler(q):
        """q^n_b -> principal ZYX Euler angles (roll, pitch, yaw)."""
        w, x, y, z = q
        return np.array([np.arctan2(2 * (y * z + w * x), 1 - 2 * (x * x + y * y)),
                         np.arcsin(np.clip(2 * (w * y - x * z), -1.0, 1.0)),
                         np.arctan2(2 * (x * y + w * z), 1 - 2 * (y * y + z * z))])

    def q_rotate(q, v):
        """Rotate a 3-vector: the vector part of q ⊗ [0, v] ⊗ q*."""
        return qmul(qmul(q, np.array([0.0, *v])), qconj(q))[1:]

    return R_to_q, euler_to_q, q_exp, q_log, q_rotate, q_to_R, q_to_euler, qconj, qmul


@app.cell
def rotation_helpers(np):
    # jb: include=false
    # Rotation-matrix helpers from Chapter 17 (the notebooks are self-contained).
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
        angle = np.linalg.norm(theta_vec)
        if angle < 1e-12:
            return np.eye(3) + skew(theta_vec)
        K = skew(theta_vec / angle)
        return np.eye(3) + np.sin(angle) * K + (1.0 - np.cos(angle)) * K @ K

    return Exp, euler_to_R


@app.cell
def _(
    Exp,
    R_to_q,
    euler_to_R,
    euler_to_q,
    np,
    q_exp,
    q_log,
    q_rotate,
    q_to_R,
    q_to_euler,
    qmul,
):
    # jb: include=false
    _rng = np.random.default_rng(18)
    # Row labels avoid the "|" character, which would split a markdown table cell.
    _rows = {
        r"associativity: $(p\otimes q)\otimes r$ vs. $p\otimes(q\otimes r)$": [],
        r"norm: $\lVert p\otimes q\rVert$ vs. $\lVert p\rVert\,\lVert q\rVert$": [],
        r"sandwich: $q\otimes[0,\mathbf v]\otimes q^*$ vs. $[0, \mathbf R(q)\mathbf v]$": [],
        r"composition: $\mathbf R(p\otimes q)$ vs. $\mathbf R(p)\mathbf R(q)$": [],
        r"$\mathbf R(\operatorname{Exp}_q(\boldsymbol\theta))$ vs. $\operatorname{Exp}(\boldsymbol\theta)$": [],
        r"$\mathbf R(\operatorname{Exp}_q(\operatorname{Log}_q q))$ vs. $\mathbf R(q)$": [],
        r"matrix round trip: `R_to_q`$(\mathbf R(q))$ vs. $\pm q$": [],
        r"Euler: $\mathbf R(q_z\otimes q_y\otimes q_x)$ vs. $\mathbf R_z\mathbf R_y\mathbf R_x$": [],
        r"Euler round trip (away from gimbal lock)": [],
    }
    _keys = list(_rows)
    for _ in range(1000):
        _p, _q, _r = _rng.normal(size=(3, 4))
        _rows[_keys[0]].append(np.abs(qmul(qmul(_p, _q), _r) - qmul(_p, qmul(_q, _r))).max())
        _rows[_keys[1]].append(abs(np.linalg.norm(qmul(_p, _q)) - np.linalg.norm(_p) * np.linalg.norm(_q)))
        _p, _q = _p / np.linalg.norm(_p), _q / np.linalg.norm(_q)
        _v = _rng.normal(size=3)
        _rows[_keys[2]].append(np.abs(q_rotate(_q, _v) - q_to_R(_q) @ _v).max())
        _rows[_keys[3]].append(np.abs(q_to_R(qmul(_p, _q)) - q_to_R(_p) @ q_to_R(_q)).max())
        _th = _rng.normal(size=3)
        _rows[_keys[4]].append(np.abs(q_to_R(q_exp(_th)) - Exp(_th)).max())
        _rows[_keys[5]].append(np.abs(q_to_R(q_exp(q_log(_q))) - q_to_R(_q)).max())
        _qb = R_to_q(q_to_R(_q))
        _rows[_keys[6]].append(min(np.abs(_qb - _q).max(), np.abs(_qb + _q).max()))
        _ang = np.array([_rng.uniform(-3, 3), _rng.uniform(-1.4, 1.4), _rng.uniform(-3, 3)])
        _rows[_keys[7]].append(np.abs(q_to_R(euler_to_q(*_ang)) - euler_to_R(*_ang)).max())
        _rows[_keys[8]].append(np.abs(q_to_euler(euler_to_q(*_ang)) - _ang).max())
    check_table = "\n".join(
        ["| check (1000 random cases) | largest entry difference |", "|---|---|"]
        + [f"| {_k} | {max(_v):.1e} |" for _k, _v in _rows.items()]
    )
    return (check_table,)


@app.cell(hide_code=True)
def _(check_table, mo):
    mo.md(rf"""
    As a sanity check, here is how closely the code satisfies the theorems of this chapter on random inputs. Every error is at the level of floating-point rounding.

    {check_table}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Quaternion Kinematics

    Chapter 17 described a turning body by $\dot{\mathbf R}^n_b = \mathbf R^n_b[\boldsymbol\omega^b]_\times$. Here is the same law for the attitude quaternion.

    /// important | 📐 **Theorem (Quaternion Kinematics)**
        attrs: {class: no-icon}
    Let $t \mapsto q(t)$ be a differentiable path of unit quaternions with $\mathbf R(q(t)) = \mathbf R^n_b(t)$, and let $\boldsymbol\omega^b$ be the body's angular velocity. Then
    $$\dot q = \tfrac12\,q\otimes[0, \boldsymbol\omega^b] = \tfrac12\,[0, \boldsymbol\omega^n]\otimes q.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    *Step 1: $q^*\otimes\dot q$ is pure.* Let $\Omega := q^*\otimes\dot q$. Differentiating $q^*\otimes q = 1$ with the product rule gives $\dot q^*\otimes q + q^*\otimes\dot q = 0$, and $\dot q^*\otimes q = (q^*\otimes\dot q)^* = \Omega^*$ by the conjugate lemma. So $\Omega^* = -\Omega$, meaning the scalar part of $\Omega$ is zero: $\Omega = [0, \mathbf a]$ for some $\mathbf a \in \mathbb R^3$. Multiplying $\Omega = q^*\otimes\dot q$ on the left by $q$ gives $\dot q = q\otimes\Omega$.

    *Step 2: identify $\mathbf a$.* Fix $\mathbf v \in \mathbb R^3$ and write $v := [0, \mathbf v]$. Differentiating $[0, \mathbf R(q)\mathbf v] = q\otimes v\otimes q^*$,
    $$[0, \dot{\mathbf R}\mathbf v] = \dot q\otimes v\otimes q^* + q\otimes v\otimes\dot q^* = q\otimes(\Omega\otimes v + v\otimes\Omega^*)\otimes q^* = q\otimes(\Omega\otimes v - v\otimes\Omega)\otimes q^*.$$
    By the commutator formula, $\Omega\otimes v - v\otimes\Omega = [0, 2\,\mathbf a\times\mathbf v]$, so $\dot{\mathbf R}\mathbf v = \mathbf R\,(2\mathbf a\times\mathbf v) = \mathbf R[2\mathbf a]_\times\mathbf v$ for every $\mathbf v$. Hence $\dot{\mathbf R} = \mathbf R[2\mathbf a]_\times$, and since the angular velocity is the *unique* vector with this property, $2\mathbf a = \boldsymbol\omega^b$. Therefore $\dot q = q\otimes[0, \tfrac12\boldsymbol\omega^b]$.

    *Step 3: navigation form.* $q\otimes[0, \boldsymbol\omega^b] = (q\otimes[0, \boldsymbol\omega^b]\otimes q^*)\otimes q = [0, \mathbf R^n_b\boldsymbol\omega^b]\otimes q = [0, \boldsymbol\omega^n]\otimes q$. $\blacksquare$
    ///

    In matrix form, $q\otimes[0, \boldsymbol\omega] = \big[[0, \boldsymbol\omega]\big]_R\,q$, so
    $$\dot q = \tfrac12\,\boldsymbol\Omega(\boldsymbol\omega^b)\,q,\qquad \boldsymbol\Omega(\boldsymbol\omega) := \begin{bmatrix}0 & -\boldsymbol\omega^\top\\ \boldsymbol\omega & -[\boldsymbol\omega]_\times\end{bmatrix}.$$
    Compare this with the Euler-angle kinematics $\dot{\boldsymbol\Theta} = \mathbf E(\phi, \theta)\boldsymbol\omega^b$ of Chapter 17:

    - It is **linear** in the attitude $q$.
    - Its coefficients are bounded by $\|\boldsymbol\omega^b\|$ and involve no division, so it is valid at **every** attitude. There is no gimbal lock.
    - $\boldsymbol\Omega(\boldsymbol\omega)$ is skew-symmetric ($\boldsymbol\Omega^\top = -\boldsymbol\Omega$, as $[\boldsymbol\omega]_\times^\top = -[\boldsymbol\omega]_\times$), so $\tfrac{d}{dt}\|q\|^2 = 2\,q^\top\dot q = q^\top\boldsymbol\Omega q = 0$: exact solutions stay unit quaternions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exact Integration with the Exponential Map

    An IMU delivers $\boldsymbol\omega^b$ as samples $\boldsymbol\omega_k$ every $\Delta t$. Treating the rate as constant within each sample period, as in Chapter 17, the quaternion equation can be solved exactly.

    /// important | 📐 **Theorem (Exact Quaternion Update)**
        attrs: {class: no-icon}
    If $\boldsymbol\omega^b = \boldsymbol\omega$ is constant on $[t_0, t_0 + \Delta t]$, then $q(t_0 + \Delta t) = q(t_0)\otimes\operatorname{Exp}_q(\boldsymbol\omega\,\Delta t)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    *Uniqueness.* With $\mathbf A := \tfrac12\boldsymbol\Omega(\boldsymbol\omega)$ constant, any solution of $\dot q = \mathbf A q$ satisfies $\tfrac{d}{dt}\big(\exp(-(t - t_0)\mathbf A)\,q(t)\big) = \exp(-(t - t_0)\mathbf A)(-\mathbf A q + \dot q) = 0$, so $q(t) = \exp((t - t_0)\mathbf A)\,q(t_0)$: there is exactly one solution with a given $q(t_0)$.

    *The candidate solves the equation.* If $\boldsymbol\omega = \mathbf 0$ there is nothing to prove. Otherwise let $\alpha := \|\boldsymbol\omega\|$, $\hat{\boldsymbol\omega} := \boldsymbol\omega/\alpha$, and $e(\tau) := \operatorname{Exp}_q(\boldsymbol\omega\tau) = [\cos\tfrac{\alpha\tau}2, \sin\tfrac{\alpha\tau}2\,\hat{\boldsymbol\omega}]$. Then
    $$\dot e(\tau) = \tfrac\alpha2\big[-\sin\tfrac{\alpha\tau}2,\ \cos\tfrac{\alpha\tau}2\,\hat{\boldsymbol\omega}\big] \quad\text{and}\quad e(\tau)\otimes[0, \tfrac12\boldsymbol\omega] = \big[-\tfrac\alpha2\sin\tfrac{\alpha\tau}2,\ \tfrac\alpha2\cos\tfrac{\alpha\tau}2\,\hat{\boldsymbol\omega} + \tfrac\alpha2\sin\tfrac{\alpha\tau}2\,\hat{\boldsymbol\omega}\times\hat{\boldsymbol\omega}\big],$$
    which agree because $\hat{\boldsymbol\omega}\times\hat{\boldsymbol\omega} = \mathbf 0$. So $p(t) := q(t_0)\otimes e(t - t_0)$ satisfies $\dot p = \tfrac12 p\otimes[0, \boldsymbol\omega]$ and $p(t_0) = q(t_0)$. By uniqueness $p = q$. $\blacksquare$
    ///

    This is the quaternion version of $\mathbf R_k = \mathbf R_{k-1}\operatorname{Exp}(\boldsymbol\omega_k\Delta t)$, and it is the attitude update used in Chapters 19–21 (Chapter 20 applies it to the average of two consecutive gyro samples):
    $$q_k = q_{k-1}\otimes\operatorname{Exp}_q(\boldsymbol\omega_k\Delta t).$$
    The increment multiplies on the right because $\boldsymbol\omega_k$ is in body coordinates. Floating-point rounding still nudges $\|q_k\|$ away from 1 by about $10^{-16}$ per step, so implementations divide by $\|q_k\|$ every step or every few steps; that costs almost nothing.

    ### Why Not Just Use Euler's Method?

    The simplest numerical method for $\dot q = \tfrac12 q\otimes[0, \boldsymbol\omega]$ is the forward Euler step $q_k = q_{k-1} + \Delta t\,\dot q_{k-1}$, that is,
    $$q_k = q_{k-1}\otimes\big[1,\ \tfrac12\boldsymbol\omega_k\Delta t\big].$$

    /// important | 📐 **Theorem (Euler Steps Inflate the Norm)**
        attrs: {class: no-icon}
    The forward Euler step satisfies $\|q_k\|^2 = \|q_{k-1}\|^2\,\big(1 + \tfrac14\|\boldsymbol\omega_k\|^2\Delta t^2\big)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    The norm is multiplicative and $\|[1, \tfrac12\boldsymbol\omega_k\Delta t]\|^2 = 1 + \tfrac14\|\boldsymbol\omega_k\|^2\Delta t^2$. $\blacksquare$
    ///

    So the norm grows geometrically, without bound. With a turn rate of 2 rad/s at 100 Hz, $\|q\|$ grows by $35\%$ in one minute. A non-unit $q$ is not just "slightly off": the general formula $\mathbf R(q) = (s^2 - \|\mathbf w\|^2)\mathbf I + 2\mathbf w\mathbf w^\top + 2s[\mathbf w]_\times$ scales every vector by $\|q\|^2$, and the simplified component formula (which assumed $\|q\| = 1$) is not even orthogonal. Normalizing after every Euler step fixes the norm, but not the direction: the normalized increment $[1, \tfrac12\boldsymbol\omega\Delta t]/\|\cdot\|$ is a rotation by $2\arctan(\tfrac12\|\boldsymbol\omega\|\Delta t) = \|\boldsymbol\omega\|\Delta t - \tfrac1{12}(\|\boldsymbol\omega\|\Delta t)^3 + \dots$ instead of $\|\boldsymbol\omega\|\Delta t$, a systematic under-rotation that accumulates.

    ### Interactive: Normalization Drift

    A body turns at a constant rate about a fixed oblique axis for 60 s. Three integrators process the same exact gyroscope samples: forward Euler without normalization, forward Euler with normalization after every step, and the exact exponential update. The left panel shows how far $\|q_k\|$ is from 1; the right panel shows the attitude error, the rotation angle of $q_{\text{true}}^*\otimes(q_k/\|q_k\|)$. (Normalization does not change the direction of $q_k$, so the two Euler variants have identical attitude error.)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    drift_omega = mo.ui.slider(steps=[0.5, 1, 2, 5, 10], value=2,
                               label=r"turn rate $\|\boldsymbol\omega\|$ (rad/s)", show_value=True)
    drift_rate = mo.ui.slider(steps=[25, 50, 100, 200, 400], value=100,
                              label="sample rate (Hz)", show_value=True)
    return drift_omega, drift_rate


@app.cell
def _(np):
    # jb: include=false
    def qmul_arr(P, Q):
        """Row-wise Hamilton product of (N, 4) arrays."""
        pw, px, py, pz = P.T
        qw, qx, qy, qz = Q.T
        return np.column_stack([pw * qw - px * qx - py * qy - pz * qz,
                                pw * qx + px * qw + py * qz - pz * qy,
                                pw * qy - px * qz + py * qw + pz * qx,
                                pw * qz + px * qy - py * qx + pz * qw])

    def attitude_error_deg(Q_true, Q_est):
        """Rotation angle (deg) of q_true* ⊗ (q_est / |q_est|), row-wise."""
        _qn = Q_est / np.linalg.norm(Q_est, axis=1, keepdims=True)
        _conj = Q_true * np.array([1.0, -1.0, -1.0, -1.0])
        _r = qmul_arr(_conj, _qn)
        return np.degrees(2 * np.arctan2(np.linalg.norm(_r[:, 1:], axis=1), np.abs(_r[:, 0])))

    return attitude_error_deg, qmul_arr


@app.cell(hide_code=True)
def _(
    attitude_error_deg,
    drift_omega,
    drift_rate,
    euler_to_q,
    graphic,
    mo,
    np,
    plt,
    q_exp,
    qmul,
    qmul_arr,
):
    _w, _fs = float(drift_omega.value), float(drift_rate.value)
    _dt, _T = 1.0 / _fs, 60.0
    _N = int(round(_T * _fs))
    _u = np.array([1.0, 2.0, 2.0]) / 3.0
    _q0 = euler_to_q(0.3, -0.2, 1.0)
    _dq_exact = q_exp(_w * _u * _dt)
    _dq_euler = np.array([1.0, *(0.5 * _w * _u * _dt)])
    _qe, _qn, _qx = _q0.copy(), _q0.copy(), _q0.copy()
    _E, _Nm, _X = np.zeros((_N, 4)), np.zeros((_N, 4)), np.zeros((_N, 4))
    for _k in range(_N):
        _qe = qmul(_qe, _dq_euler)
        _qn = qmul(_qn, _dq_euler)
        _qn = _qn / np.linalg.norm(_qn)
        _qx = qmul(_qx, _dq_exact)
        _E[_k], _Nm[_k], _X[_k] = _qe, _qn, _qx
    _t = np.arange(1, _N + 1) * _dt
    _half = 0.5 * _w * _t
    _Qt = qmul_arr(np.tile(_q0, (_N, 1)),
                   np.column_stack([np.cos(_half), np.outer(np.sin(_half), _u)]))

    _floor = 1e-17
    _fig, (_a1, _a2) = plt.subplots(1, 2, figsize=(10, 3.9))
    for _Q, _lab, _c in [(_E, "Euler", "C3"), (_Nm, "Euler + normalize", "C1"), (_X, "exact exponential", "C0")]:
        _a1.semilogy(_t, np.maximum(np.abs(np.linalg.norm(_Q, axis=1) - 1.0), _floor), color=_c, label=_lab)
    _a2.semilogy(_t, np.maximum(attitude_error_deg(_Qt, _E), _floor), color="C3",
                 label="Euler (with or without normalizing)")
    _a2.semilogy(_t, np.maximum(attitude_error_deg(_Qt, _X), _floor), color="C0", label="exact exponential")
    _a1.set_ylabel(r"$|\,\|q_k\| - 1\,|$")
    _a2.set_ylabel("attitude error (deg)")
    _a1.set_title("Norm drift", style="italic")
    _a2.set_title("Attitude error", style="italic")
    for _a in (_a1, _a2):
        _a.set_xlabel("time (s)")
        _a.set_ylim(1e-17, 1e2)
        _a.grid(visible=True, alpha=0.9, linewidth=0.4)
        _a.legend(fontsize=8, loc="center right")
    _fig.tight_layout()

    drift_summary = dict(
        norm_sim=np.linalg.norm(_E[-1]), norm_pred=(1 + 0.25 * _w**2 * _dt**2) ** (_N / 2),
        ang_sim=attitude_error_deg(_Qt[-1:], _Nm[-1:])[0], ang_pred=np.degrees(_N * (_w * _dt) ** 3 / 12),
    )
    _out = mo.vstack([mo.hstack([drift_omega, drift_rate], justify="start"), graphic(_fig)])
    plt.close(_fig)
    _out
    return (drift_summary,)


@app.cell(hide_code=True)
def _(drift_summary, mo):
    mo.md(rf"""
    After 60 s the unnormalized Euler quaternion has norm ${drift_summary['norm_sim']:.4f}$ (the theorem predicts $(1 + \tfrac14\|\boldsymbol\omega\|^2\Delta t^2)^{{N/2}} = {drift_summary['norm_pred']:.4f}$), and the normalized Euler attitude is off by ${drift_summary['ang_sim']:.3g}^\circ$ (the cubic term predicts about $N(\|\boldsymbol\omega\|\Delta t)^3/12 = {drift_summary['ang_pred']:.3g}^\circ$). The exact update stays at rounding level. Raising the sample rate shrinks the Euler errors but never removes them; the exponential update costs one extra $\sin$ and $\cos$ per step.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
        attrs: {class: no-icon}
    - **The rate is held constant over each sample.** The exact update is exact only for a zero-order-hold rate. If the axis of rotation changes within a sample (vibration, fast oscillation), the true increment differs from $\operatorname{Exp}_q(\boldsymbol\omega_k\Delta t)$ at second order; high-end systems add *coning* corrections that use several consecutive samples.
    - **The gyroscope measures $\boldsymbol\omega^b$ perfectly.** It does not: bias and noise are integrated along with the motion. No integrator can remove them, which is why [Chapter 19](ch19_ahrs_v2.md) fuses other sensors.
    - **Unit norm.** Formulas such as the component form of $\mathbf R(q)$ and the Euler-angle extraction assume $\|q\| = 1$. Normalize before using them.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Gimbal Lock, Avoided

    Chapter 17's simulation turned a body at a steady $0.5$ rad/s about its own $y$ axis, passing close to pitch $90^\circ$, and its Euler angles misbehaved violently. Below, the same motion is integrated with the exact quaternion update. Move the time slider to animate the body; the dropdown sets how close the path comes to gimbal lock. The quaternion components (top right) trace smooth sinusoids however close the path comes, while the Euler angles extracted from them (bottom right) swing by $180^\circ$ in an instant. The singularity was never in the attitude, only in its description.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    gl_miss = mo.ui.dropdown(options={"3°": 3.0, "0.5°": 0.5, "0° (straight through)": 0.0},
                             value="3°", label="closest approach to gimbal lock")
    gl_time = mo.ui.slider(0.0, 6.0, 0.05, value=2.5, label="time $t$ (s)", show_value=True)
    return gl_miss, gl_time


@app.cell
def _(euler_to_q, gl_miss, np, q_exp, q_to_euler, qmul):
    # jb: include=false
    _dt = 0.01
    gl_t = np.arange(0.0, 6.0 + 1e-9, _dt)
    _q = euler_to_q(np.radians(gl_miss.value), 0.0, 0.0)
    _dq = q_exp(np.array([0.0, 0.5, 0.0]) * _dt)
    gl_q = np.zeros((len(gl_t), 4))
    gl_q[0] = _q
    for _k in range(1, len(gl_t)):
        _q = qmul(_q, _dq)
        gl_q[_k] = _q
    gl_eul = np.degrees(np.array([q_to_euler(_qq) for _qq in gl_q]))
    return gl_eul, gl_q, gl_t


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
        _P = np.array([[-L/2, -W/2, -H/2], [L/2, -W/2, -H/2], [L/2 + 0.25, 0, -H/2],
                       [L/2, W/2, -H/2], [-L/2, W/2, -H/2],
                       [-L/2, -W/2, H/2], [L/2, -W/2, H/2], [L/2 + 0.25, 0, H/2],
                       [L/2, W/2, H/2], [-L/2, W/2, H/2]]) @ R.T
        _faces = [_P[[0, 1, 2, 3, 4]], _P[[5, 6, 7, 8, 9]]]
        _faces += [_P[[_i, (_i + 1) % 5, (_i + 1) % 5 + 5, _i + 5]] for _i in range(5)]
        ax.add_collection3d(Poly3DCollection(_faces, facecolor="0.85", edgecolor="0.35",
                                             alpha=0.55, lw=0.5))

    return draw_axes, draw_body, setup_3d


@app.cell(hide_code=True)
def _(
    draw_axes,
    draw_body,
    gl_eul,
    gl_miss,
    gl_q,
    gl_t,
    gl_time,
    graphic,
    mo,
    np,
    plt,
    q_to_R,
    setup_3d,
):
    _k = int(np.argmin(np.abs(gl_t - gl_time.value)))
    _fig = plt.figure(figsize=(10.5, 4.6))
    _ax3 = _fig.add_subplot(1, 2, 1, projection="3d")
    setup_3d(_ax3, lim=1.1, elev=18, azim=-55, zoom=1.35)
    draw_axes(_ax3, np.eye(3), 1.15, ["0.55"] * 3, ["E", "N", "U"], lw=0.9, ls="--", fontsize=10)
    _R = q_to_R(gl_q[_k])
    draw_body(_ax3, _R)
    draw_axes(_ax3, _R, 0.9, ["C3", "C2", "C0"], [r"$x_b$", r"$y_b$", r"$z_b$"])
    _ax3.set_title(f"t = {gl_t[_k]:.2f} s", style="italic", fontsize=11)

    _axq = _fig.add_subplot(2, 2, 2)
    for _i, (_lab, _c) in enumerate(zip([r"$q_w$", r"$q_x$", r"$q_y$", r"$q_z$"], ["k", "C3", "C2", "C0"])):
        _axq.plot(gl_t, gl_q[:, _i], color=_c, label=_lab)
    _axq.set_ylabel("quaternion")
    _axq.set_ylim(-1.1, 1.1)
    _axq.legend(fontsize=8, ncol=4, loc="lower left")
    _axe = _fig.add_subplot(2, 2, 4, sharex=_axq)
    for _i, (_lab, _ls) in enumerate(zip([r"roll $\phi$", r"pitch $\theta$", r"yaw $\psi$"], ["-", "-", "--"])):
        _axe.plot(gl_t, gl_eul[:, _i], color=f"C{_i}", ls=_ls, label=_lab)
    _axe.set_ylabel("Euler angle (deg)")
    _axe.set_xlabel("time (s)")
    _axe.set_ylim(-200, 200)
    _axe.legend(fontsize=8, ncol=3, loc="lower left")
    for _a in (_axq, _axe):
        _a.axvline(gl_t[_k], color="0.3", lw=1.0)
        _a.grid(visible=True, alpha=0.9, linewidth=0.4)
    _axq.set_title(f"closest approach to gimbal lock: {gl_miss.selected_key}", style="italic", fontsize=10)
    _fig.tight_layout()

    _q, _e = gl_q[_k], gl_eul[_k]
    _txt = mo.md(
        rf"$q = [{_q[0]:.3f},\ {_q[1]:.3f},\ {_q[2]:.3f},\ {_q[3]:.3f}]$, "
        rf"$\|q\| = {np.linalg.norm(_q):.12f}$; "
        rf"$(\phi, \theta, \psi) = ({_e[0]:.1f}^\circ,\ {_e[1]:.1f}^\circ,\ {_e[2]:.1f}^\circ)$"
    )
    _out = mo.vstack([mo.hstack([gl_miss, gl_time], justify="start"), graphic(_fig), _txt])
    plt.close(_fig)
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Interpolating Attitudes (Slerp)

    This section is optional; nothing later depends on it. To move smoothly from attitude $q_0$ to attitude $q_1$ (for animation, or to resample attitude between two time stamps), turn at a constant angular velocity. The relative rotation is $q_0^*\otimes q_1$, with rotation vector $\boldsymbol\theta := \operatorname{Log}_q(q_0^*\otimes q_1)$; by the exact-update theorem, turning at the body rate $\boldsymbol\theta$ per unit time for a time $\tau \in [0, 1]$ gives the *spherical linear interpolation*
    $$\operatorname{slerp}(q_0, q_1; \tau) := q_0\otimes\operatorname{Exp}_q\big(\tau\,\operatorname{Log}_q(q_0^*\otimes q_1)\big),$$
    which starts at $q_0$, ends at $\pm q_1$ (the same attitude as $q_1$), and turns about a fixed body axis at a constant rate. Because $\operatorname{Log}_q$ returns the rotation vector with $\|\boldsymbol\theta\| \le \pi$, this is the shorter of the two ways around. An equivalent closed form, $\big(\sin((1-\tau)\Phi)\,q_0 + \sin(\tau\Phi)\,q_1\big)/\sin\Phi$ with $\cos\Phi = \langle q_0, q_1\rangle$, is common in graphics code; it takes the short way only if $q_1$ is first replaced by $-q_1$ whenever $\langle q_0, q_1\rangle < 0$ ([Wikipedia: Slerp](https://en.wikipedia.org/wiki/Slerp)).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Hamilton versus JPL Conventions

    Two incompatible quaternion conventions are in wide use, and formulas from one silently give wrong answers in the other. This book uses the **Hamilton** convention throughout. Much of the older spacecraft and robotics literature (for example, many error-state Kalman filter papers) uses the **JPL** convention.

    | | Hamilton (this book) | JPL |
    |---|---|---|
    | Product rule | $i\otimes j = k$ | $i\otimes j = -k$ |
    | Storage order | scalar first, $[q_w, q_x, q_y, q_z]$ | scalar last, $[q_x, q_y, q_z, q_w]$ |
    | Attitude quaternion | rotates body to navigation, $\mathbf R(q^n_b) = \mathbf R^n_b$ | usually rotates navigation to body |
    | Kinematics | $\dot q^n_b = \tfrac12\,q^n_b\otimes[0, \boldsymbol\omega^b]$ | $\dot q = \tfrac12\,\boldsymbol\Omega_{\text{JPL}}(\boldsymbol\omega)\,q$, with a different $\boldsymbol\Omega$ |

    Flipping the sign of $i\otimes j$ flips the sign of the cross-product term in the product, so the JPL product of $p$ and $q$ equals the Hamilton product $q\otimes p$ of the same four numbers in the opposite order. As a consequence, the same four numbers that represent $\mathbf R$ in the Hamilton sandwich formula represent $\mathbf R^\top$ in the JPL one. [Sommer et al. (2018), *Why and How to Avoid the Flipped Quaternion Multiplication*](https://doi.org/10.3390/aerospace5030072) explains the history and argues for Hamilton; [Solà (2017), *Quaternion Kinematics for the Error-State Kalman Filter*](https://arxiv.org/abs/1711.02508) uses Hamilton and tabulates the differences. Storage order is a separate trap: SciPy's `Rotation.from_quat`, for instance, expects scalar-last order by default even though its product is Hamilton's.

    /// caution | ⚠️ **Assumptions and Failure Modes**
        attrs: {class: no-icon}
    Before using a quaternion formula, data file, or library from elsewhere, check four things: the product rule ($i\otimes j = \pm k$), the storage order (scalar first or last), the direction of the attitude quaternion (body-to-navigation or the reverse), and the frame conventions (ENU/FLU here; NED/forward-right-down is common). Getting any one of them wrong typically produces attitudes that look plausible at rest and go wrong as soon as the body turns.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - A {term}`quaternion` is an element of $\mathbb H = \mathbb R^4$, $q = [q_w, \mathbf q_v]$. The {term}`Hamilton product` $p\otimes q = [p_wq_w - \mathbf p_v\cdot\mathbf q_v,\ p_w\mathbf q_v + q_w\mathbf p_v + \mathbf p_v\times\mathbf q_v]$ is associative and bilinear but not commutative.
    - The {term}`quaternion conjugate` $q^* = [q_w, -\mathbf q_v]$ satisfies $(p\otimes q)^* = q^*\otimes p^*$ and $q\otimes q^* = \|q\|^2$, which makes the norm multiplicative: $\|p\otimes q\| = \|p\|\|q\|$.
    - A {term}`unit quaternion` $q = [\cos\tfrac\vartheta2, \sin\tfrac\vartheta2\mathbf u]$ rotates vectors by $\vartheta$ about $\mathbf u$ via $q\otimes[0, \mathbf v]\otimes q^* = [0, \mathbf R(q)\mathbf v]$, and $\mathbf R(p\otimes q) = \mathbf R(p)\mathbf R(q)$. Our attitude quaternion $q^n_b$ satisfies $\mathbf R(q^n_b) = \mathbf R^n_b$.
    - $q \mapsto \mathbf R(q)$ is a {term}`double cover`: exactly $\pm q$ give the same rotation. Compare attitudes by the angle $2\arccos|\langle\hat q, q\rangle|$, never by $\|\hat q - q\|$.
    - Conversions: $\operatorname{Exp}_q$/$\operatorname{Log}_q$ for rotation vectors, the component formula and largest-square algorithm for matrices, and $q_z(\psi)\otimes q_y(\theta)\otimes q_x(\phi)$ for Euler angles.
    - Kinematics: $\dot q = \tfrac12 q\otimes[0, \boldsymbol\omega^b] = \tfrac12\boldsymbol\Omega(\boldsymbol\omega^b)q$, linear and singularity-free. For a rate held constant over each sample, $q_k = q_{k-1}\otimes\operatorname{Exp}_q(\boldsymbol\omega_k\Delta t)$ is exact; forward Euler inflates the norm by $\sqrt{1 + \|\boldsymbol\omega\|^2\Delta t^2/4}$ per step and under-rotates even when normalized.
    - This book uses the Hamilton convention; the JPL convention reverses the product and usually the direction of the attitude quaternion.

    ## What's Next

    We can now propagate attitude exactly from *perfect* gyroscope readings. Real gyroscopes have bias and noise, so integrated attitude drifts away from the truth. [Chapter 19](ch19_ahrs_v2.md) fixes this by fusing the gyroscope with two sensors that see fixed directions, gravity through an accelerometer and the Earth's magnetic field through a magnetometer: first with a complementary filter that is exactly the Introduction's alpha filter, then with an error-state Kalman filter built on the quaternion machinery of this chapter.
    """)
    return


if __name__ == "__main__":
    app.run()
