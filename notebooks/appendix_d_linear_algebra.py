# /// script
# dependencies = [
#     "marimo>=0.25.1",
#     "matplotlib==3.11.2",
#     "numpy==2.5.3",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="Appendix D: Linear Algebra", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "From Vectors to Matrix Calculus"
    abbreviations:
      ODE: ordinary differential equation
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
    /// seealso | 🔗 **Prerequisites**
        attrs: {class: no-icon}
    - [Chapter 2](ch2_axioms_of_set_theory.md): functions, the set $Y^X$ of all functions from $X$ to $Y$, Cartesian products, induction, and definition by recursion.
    - [Chapter 3](ch3_sets_for_probability.md): finite sums $\sum$, composition and inverse functions, and $\mathbb R$ as a complete ordered field (including absolute value).
    - [Appendix C: Limits of Functions and Continuity](appendix_c_calculus.md): square roots of nonnegative numbers.
    - Only for The Matrix Exponential: [Appendix C: Sequences and Limits](appendix_c_calculus.md) (limit laws), [Appendix C: Series](appendix_c_calculus.md) (comparison test, Cauchy product), [Appendix C: Exponential and Logarithm](appendix_c_calculus.md), [Appendix C: Limits of Functions and Continuity](appendix_c_calculus.md) (intermediate value theorem), [Appendix C: Derivatives](appendix_c_calculus.md) (product rule), and [Appendix C: The Mean Value Theorem and Extrema](appendix_c_calculus.md).
    - Only for Derivatives with Respect to Matrices: [Appendix C: Functions of Several Variables](appendix_c_calculus.md) (partial derivatives) and [Appendix C: The Mean Value Theorem and Extrema](appendix_c_calculus.md) (interior extrema).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    From [Chapter 12](ch12_vectors_matrices_covariance.md) on, the state of a filter is no longer one number but a list of numbers (the position and velocity of a cart, a weight and its rate of gain, an attitude and a gyro bias), and its uncertainty is a square table of numbers. Every scalar formula from Parts 1–2 gets a counterpart in which scalars become vectors and matrices:

    | Scalar (Parts 1–2) | Vectors and matrices (Part 3 on) |
    |---|---|
    | $\hat x_k^- = a\,\hat x_{k-1}$ | $\hat{\mathbf x}_k^- = \mathbf F\,\hat{\mathbf x}_{k-1}$ |
    | $P_k^- = a^2 P_{k-1} + Q$ | $\mathbf P_k^- = \mathbf F\mathbf P_{k-1}\mathbf F^\top + \mathbf Q$ |
    | $K_k = P_k^- h\,(h^2 P_k^- + R)^{-1}$ | $\mathbf K_k = \mathbf P_k^-\mathbf H^\top(\mathbf H\mathbf P_k^-\mathbf H^\top + \mathbf R)^{-1}$ |
    | $P_k = (1 - K_k h)\,P_k^-$ | $\mathbf P_k = (\mathbf I - \mathbf K_k\mathbf H)\,\mathbf P_k^-$ |

    Reading the right-hand column requires knowing what products, transposes, and inverses of matrices are; when an inverse exists; and why the result is again a valid covariance. This appendix builds exactly that, from the definition of a vector up to the matrix calculus that derives the Kalman gain.

    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    A matrix is a linear map written as a table of numbers, and multiplying matrices composes the maps. Most of what the Kalman filter needs follows from this and from one theorem about symmetric matrices: each one is a set of perpendicular axes with a stretch factor along each axis (the spectral theorem).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **How to use this appendix.** It is optional. If you have taken a linear algebra course, skim the definitions (they fix the notation used in the rest of the book) and read the sections that first courses often skip: Symmetric and Positive Definite Matrices, Cholesky Decomposition, Block Matrices and the Schur Complement, and Derivatives with Respect to Matrices. Each section is used in the following places:

    | Section | Used in |
    |---|---|
    | Vectors; Matrices and Linear Maps; Matrix Multiplication; Transpose, Identity, and Inverse | Chapter 12 onward |
    | Linear Independence, Basis, and Rank | Chapter 13 (observability) |
    | Determinants | Chapter 12 (the multivariate normal density), Chapter 17 (rotations) |
    | Trace | Chapters 12–13 (the Kalman gain minimizes a trace) |
    | Orthogonal Matrices | Chapter 12 (ellipse axes), Chapters 17–21 (rotations) |
    | Eigenvalues and Eigenvectors; Symmetric and Positive Definite Matrices | Chapter 12 (covariance matrices, confidence ellipses) |
    | Cholesky Decomposition | Chapter 16 (sigma points), simulating correlated noise |
    | Block Matrices and the Schur Complement | Chapter 12 (Gaussian conditioning), Chapter 13 (matrix inversion lemma) |
    | Cross Products and Skew-Symmetric Matrices | Chapters 17–21 |
    | The Matrix Exponential | Chapter 14 (discretizing the process noise), Chapters 17–18 (rotation vectors) |
    | Derivatives with Respect to Matrices | Chapter 13 (the Kalman gain) |

    **Notation.** Scalars are plain ($a$, $\lambda$, $x_i$), vectors are bold lowercase ($\mathbf x$), and matrices are bold uppercase ($\mathbf A$). Unless a proof says otherwise, it uses only the field and order axioms of $\mathbb R$ and finite sums.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Vectors

    A cart on a track is at position $3$ m and moves at $0.5$ m/s. Its state is the list $(3, 0.5)$: a first entry and a second entry. A list of $n$ numbers indexed by $1, \ldots, n$ is precisely a {term}`function` from $\{1, \ldots, n\}$ to $\mathbb R$, so that is how we define it. Throughout, $\{1, \ldots, n\} := \{k \in \mathbb N : 1 \le k \le n\}$ for $n \in \mathbb N^+$.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Vector**</u>

    For $n \in \mathbb N^+$, a vector in $\mathbb R^n$ is a function $\mathbf x : \{1, \ldots, n\} \to \mathbb R$. Its $i$-th entry is $x_i := \mathbf x(i)$, and we write $\mathbf x = (x_1, \ldots, x_n)$. The set of all such vectors is $\mathbb R^n := \mathbb R^{\{1, \ldots, n\}}$.
    ///

    Two vectors are equal exactly when all their entries are equal, because that is what equality of functions means ([Chapter 2](ch2_axioms_of_set_theory.md)). In displayed formulas we write vectors as columns.

    For $\mathbf x, \mathbf y \in \mathbb R^n$ and $c \in \mathbb R$, addition and scalar multiplication act entry by entry:

    $$(\mathbf x + \mathbf y)_i := x_i + y_i, \qquad (c\mathbf x)_i := c\,x_i \qquad (i = 1, \ldots, n).$$

    The zero vector is $\mathbf 0 := (0, \ldots, 0)$, and $-\mathbf x := (-1)\mathbf x$ and $\mathbf x - \mathbf y := \mathbf x + (-\mathbf y)$. Because both operations act entry by entry, rules such as $\mathbf x + \mathbf y = \mathbf y + \mathbf x$, $(\mathbf x + \mathbf y) + \mathbf z = \mathbf x + (\mathbf y + \mathbf z)$, $c(\mathbf x + \mathbf y) = c\mathbf x + c\mathbf y$, $(c + d)\mathbf x = c\mathbf x + d\mathbf x$, $(cd)\mathbf x = c(d\mathbf x)$, $\mathbf x + \mathbf 0 = \mathbf x$, and $\mathbf x - \mathbf x = \mathbf 0$ all hold: comparing $i$-th entries turns each one into a field axiom of $\mathbb R$ ([Chapter 3](ch3_sets_for_probability.md)). We use them without comment.

    A **linear combination** of vectors $\mathbf v_1, \ldots, \mathbf v_k \in \mathbb R^n$ is a vector $c_1\mathbf v_1 + \cdots + c_k\mathbf v_k = \sum_{j=1}^k c_j\mathbf v_j$ with $c_1, \ldots, c_k \in \mathbb R$. The **standard basis vectors** $\mathbf e_1, \ldots, \mathbf e_n \in \mathbb R^n$ are defined by $(\mathbf e_j)_i := 1$ if $i = j$ and $(\mathbf e_j)_i := 0$ otherwise. Every vector is a linear combination of them,

    $$\mathbf x = \sum_{j=1}^n x_j\mathbf e_j,$$

    because the $i$-th entry of the right side is $\sum_j x_j(\mathbf e_j)_i = x_i$ (only the term $j = i$ is nonzero).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Dot product and norm

    Suppose a 3-D position estimate is off by $\mathbf e = (0.3, -0.4, 1.2)$ m (East, North, Up). How far off is it? Pythagoras says $\sqrt{0.3^2 + 0.4^2 + 1.2^2} = \sqrt{1.69} = 1.3$ m. The sum of products of entries inside the square root is the dot product.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Dot product**</u>

    The dot product of $\mathbf x, \mathbf y \in \mathbb R^n$ is the number
    $$\mathbf x\cdot\mathbf y := \sum_{i=1}^n x_i y_i.$$
    ///

    /// important | 📐 **Lemma (Dot Product Rules)**
        attrs: {class: no-icon}
    For all $\mathbf x, \mathbf y, \mathbf z \in \mathbb R^n$ and $c \in \mathbb R$:

    1. $\mathbf x\cdot\mathbf y = \mathbf y\cdot\mathbf x$;
    2. $(\mathbf x + \mathbf y)\cdot\mathbf z = \mathbf x\cdot\mathbf z + \mathbf y\cdot\mathbf z$ and $(c\mathbf x)\cdot\mathbf y = c\,(\mathbf x\cdot\mathbf y)$;
    3. $\mathbf x\cdot\mathbf x \ge 0$, with equality if and only if $\mathbf x = \mathbf 0$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    (1) and (2) hold term by term ($x_iy_i = y_ix_i$, $(x_i + y_i)z_i = x_iz_i + y_iz_i$, $(cx_i)y_i = c(x_iy_i)$), and finite sums can be split and scaled ([Chapter 3](ch3_sets_for_probability.md)). For (3), each $x_i^2 \ge 0$ in an ordered field, so the sum is $\ge 0$. If $\mathbf x\cdot\mathbf x = 0$, then for each $i$ we have $0 \le x_i^2 \le \sum_j x_j^2 = 0$, so $x_i^2 = 0$ and therefore $x_i = 0$ (a field has no zero divisors). Conversely, $\mathbf 0\cdot\mathbf 0 = 0$. $\blacksquare$
    ///

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Norm**</u>

    The (Euclidean) norm of $\mathbf x \in \mathbb R^n$ is the nonnegative square root
    $$\|\mathbf x\| := \sqrt{\mathbf x\cdot\mathbf x}.$$
    ///

    The square root exists because $\mathbf x\cdot\mathbf x \ge 0$.[^sqrt] For the position error above, $\mathbf e\cdot\mathbf e = 1.69\ \text{m}^2$ and $\|\mathbf e\| = 1.3$ m. Since $(c\mathbf x)\cdot(c\mathbf x) = c^2\,\mathbf x\cdot\mathbf x$ and $\sqrt{c^2} = |c|$, we have $\|c\mathbf x\| = |c|\,\|\mathbf x\|$. A **unit vector** is a vector $\mathbf u$ with $\|\mathbf u\| = 1$; for $\mathbf x \ne \mathbf 0$, $\mathbf x/\|\mathbf x\|$ is one. Two vectors $\mathbf x, \mathbf y$ are **orthogonal** if $\mathbf x\cdot\mathbf y = 0$.

    [^sqrt]: Every $s \ge 0$ has exactly one nonnegative square root $\sqrt s$, by the intermediate value theorem; see the Square Roots corollary in [Appendix C: Limits of Functions and Continuity](appendix_c_calculus.md).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// important | 📐 **Theorem (Cauchy–Schwarz Inequality)**
        attrs: {class: no-icon}
    For all $\mathbf x, \mathbf y \in \mathbb R^n$,
    $$|\mathbf x\cdot\mathbf y| \le \|\mathbf x\|\,\|\mathbf y\|,$$
    with equality if and only if $\mathbf y = \mathbf 0$ or $\mathbf x$ is a scalar multiple of $\mathbf y$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    If $\mathbf y = \mathbf 0$, both sides are $0$. Otherwise $\mathbf y\cdot\mathbf y > 0$; put $t := (\mathbf x\cdot\mathbf y)/(\mathbf y\cdot\mathbf y)$. By the dot product rules,
    $$0 \le (\mathbf x - t\mathbf y)\cdot(\mathbf x - t\mathbf y) = \mathbf x\cdot\mathbf x - 2t\,(\mathbf x\cdot\mathbf y) + t^2\,(\mathbf y\cdot\mathbf y) = \|\mathbf x\|^2 - \frac{(\mathbf x\cdot\mathbf y)^2}{\|\mathbf y\|^2}.$$
    So $(\mathbf x\cdot\mathbf y)^2 \le \|\mathbf x\|^2\|\mathbf y\|^2$. Both $|\mathbf x\cdot\mathbf y|$ and $\|\mathbf x\|\|\mathbf y\|$ are nonnegative, and for $a, b \ge 0$, $a^2 \le b^2$ implies $a \le b$; this gives the inequality. Equality holds exactly when $\mathbf x - t\mathbf y = \mathbf 0$ (rule 3). If $\mathbf x = s\mathbf y$ for some $s$, then $t = s$ and indeed $\mathbf x - t\mathbf y = \mathbf 0$. $\blacksquare$
    ///

    /// important | 📐 **Corollary (Triangle Inequality)**
        attrs: {class: no-icon}
    For all $\mathbf x, \mathbf y \in \mathbb R^n$, $\|\mathbf x + \mathbf y\| \le \|\mathbf x\| + \|\mathbf y\|$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    $\|\mathbf x + \mathbf y\|^2 = \|\mathbf x\|^2 + 2\,\mathbf x\cdot\mathbf y + \|\mathbf y\|^2 \le \|\mathbf x\|^2 + 2\|\mathbf x\|\|\mathbf y\| + \|\mathbf y\|^2 = (\|\mathbf x\| + \|\mathbf y\|)^2$ by Cauchy–Schwarz. Take nonnegative square roots as in the previous proof. $\blacksquare$
    ///

    For nonzero $\mathbf x, \mathbf y$, Cauchy–Schwarz says $\mathbf x\cdot\mathbf y/(\|\mathbf x\|\|\mathbf y\|) \in [-1, 1]$; this number is the cosine of the angle between them, and orthogonal vectors are those at a right angle. The correlation coefficient of [Chapter 6](ch6_expectation_and_variance.md) has exactly this form, which is why it also lies in $[-1, 1]$.

    /// caution | ⚠️ **Assumptions and Failure Modes**
        attrs: {class: no-icon}
    The dot product adds products of entries, so $\|\mathbf x\|$ is physically meaningful only when all entries share a unit. For the cart state (position in m, velocity in m/s), $\|\mathbf x\|^2$ would add m² to m²/s², and changing the position unit from m to cm would change which of two states counts as "larger". The Kalman filter does not fall into this trap: its gain is the same no matter how the entries are weighted (see Derivatives with Respect to Matrices below).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Matrices and Linear Maps

    Over a time step $\Delta t$, a cart moving at constant velocity goes from position $p$ and velocity $v$ to

    $$p' = 1\cdot p + \Delta t\cdot v, \qquad v' = 0\cdot p + 1\cdot v.$$

    Everything about this prediction is captured by the table of coefficients
    $\begin{bmatrix} 1 & \Delta t \\ 0 & 1 \end{bmatrix}$: row $i$ holds the coefficients of the $i$-th output. A position sensor reads $z = 1\cdot p + 0\cdot v$, with the one-row table $\begin{bmatrix} 1 & 0\end{bmatrix}$. A table of numbers indexed by a row and a column is a function of two indices.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Matrix**</u>

    For $m, n \in \mathbb N^+$, an $m \times n$ matrix is a function $\mathbf A : \{1, \ldots, m\} \times \{1, \ldots, n\} \to \mathbb R$. Its $(i, j)$ entry is $a_{ij} := \mathbf A(i, j)$, where $i$ is the row index and $j$ the column index. The set of all $m \times n$ matrices is $\mathbb R^{m\times n} := \mathbb R^{\{1, \ldots, m\}\times\{1, \ldots, n\}}$.
    ///

    We display $\mathbf A$ as an array with $a_{ij}$ in row $i$ and column $j$, and also write $[\mathbf A]_{ij}$ for $a_{ij}$ when $\mathbf A$ is a longer expression. $\mathbf A$ is **square** if $m = n$. Its $j$-th **column** is the vector $\mathbf a_j := (a_{1j}, \ldots, a_{mj}) \in \mathbb R^m$, and we write $\mathbf A = [\mathbf a_1 \ \cdots\ \mathbf a_n]$. Addition, scalar multiplication, and the zero matrix $\mathbf 0$ are defined entry by entry exactly as for vectors, and obey the same rules.

    The **matrix–vector product** of $\mathbf A \in \mathbb R^{m\times n}$ and $\mathbf x \in \mathbb R^n$ is the vector $\mathbf A\mathbf x \in \mathbb R^m$ with entries

    $$(\mathbf A\mathbf x)_i := \sum_{j=1}^n a_{ij}x_j \qquad (i = 1, \ldots, m).$$

    Equivalently, $\mathbf A\mathbf x = \sum_{j=1}^n x_j\mathbf a_j$ is the linear combination of the columns with coefficients from $\mathbf x$ (compare $i$-th entries). In particular $\mathbf A\mathbf e_j = \mathbf a_j$. For the cart with $\Delta t = 0.1$ s and state $(3, 0.5)$:

    $$\begin{bmatrix} 1 & 0.1 \\ 0 & 1 \end{bmatrix}\begin{bmatrix} 3 \\ 0.5 \end{bmatrix} = \begin{bmatrix} 3.05 \\ 0.5 \end{bmatrix}, \qquad \begin{bmatrix} 1 & 0 \end{bmatrix}\begin{bmatrix} 3.05 \\ 0.5 \end{bmatrix} = 3.05.$$

    Both maps $\mathbf x \mapsto \mathbf A\mathbf x$ respect addition and scaling. That property has a name.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Linear map**</u>

    A function $T : \mathbb R^n \to \mathbb R^m$ is a linear map if $T(\mathbf x + \mathbf y) = T(\mathbf x) + T(\mathbf y)$ and $T(c\mathbf x) = c\,T(\mathbf x)$ for all $\mathbf x, \mathbf y \in \mathbb R^n$ and $c \in \mathbb R$.
    ///

    /// important | 📐 **Theorem (Matrices Are Linear Maps)**
        attrs: {class: no-icon}
    1. For every $\mathbf A \in \mathbb R^{m\times n}$, the map $T_{\mathbf A} : \mathbb R^n \to \mathbb R^m$, $T_{\mathbf A}(\mathbf x) := \mathbf A\mathbf x$, is linear.
    2. For every linear map $T : \mathbb R^n \to \mathbb R^m$ there is exactly one $\mathbf A \in \mathbb R^{m\times n}$ with $T = T_{\mathbf A}$: the matrix whose $j$-th column is $T(\mathbf e_j)$.

    So $\mathbf A \mapsto T_{\mathbf A}$ is a bijection from $\mathbb R^{m\times n}$ onto the set of linear maps $\mathbb R^n \to \mathbb R^m$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    (1) $(\mathbf A(\mathbf x + \mathbf y))_i = \sum_j a_{ij}(x_j + y_j) = \sum_j a_{ij}x_j + \sum_j a_{ij}y_j$, and $(\mathbf A(c\mathbf x))_i = \sum_j a_{ij}cx_j = c\sum_j a_{ij}x_j$.

    (2) Existence: let $\mathbf A$ have columns $\mathbf a_j := T(\mathbf e_j)$. Linearity extends to finite sums by induction on the number of terms, so $T(\mathbf x) = T\big(\sum_j x_j\mathbf e_j\big) = \sum_j x_jT(\mathbf e_j) = \sum_j x_j\mathbf a_j = \mathbf A\mathbf x$. Uniqueness: if $T_{\mathbf A} = T_{\mathbf B}$, then for each $j$ the $j$-th columns agree, $\mathbf a_j = \mathbf A\mathbf e_j = \mathbf B\mathbf e_j = \mathbf b_j$, so $\mathbf A = \mathbf B$. $\blacksquare$
    ///

    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    A matrix *is* a linear map, recorded by where it sends each standard basis vector: column $j$ is the image of $\mathbf e_j$. To find the matrix of a linear map, find where it sends each $\mathbf e_j$.
    ///

    **Examples.** Rotating the plane counterclockwise by an angle $\theta$ is linear (it carries the parallelogram spanned by $\mathbf x$ and $\mathbf y$ onto the one spanned by their images),[^rotation-informal] and it sends $\mathbf e_1$ to $(\cos\theta, \sin\theta)$ and $\mathbf e_2$ to $(-\sin\theta, \cos\theta)$. Its matrix is therefore

    $$\mathbf R(\theta) = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}.$$

    Not every useful map is linear. A linear map sends $\mathbf 0$ to $\mathbf 0$, because $T(\mathbf 0) = T(0\cdot\mathbf 0) = 0\cdot T(\mathbf 0) = \mathbf 0$. So adding a constant offset, $\mathbf x \mapsto \mathbf x + \mathbf b$ with $\mathbf b \ne \mathbf 0$, is not linear, and neither is the pendulum's $\theta \mapsto L\sin\theta$ ([Chapter 15](ch15_extended_kalman_filter.md) handles such maps by approximating them with linear ones).

    [^rotation-informal]: This geometric argument is informal; [Chapter 17](ch17_rotations.md) defines rotations precisely as matrices.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Matrix Multiplication

    Predicting the cart two steps ahead applies the prediction twice: $\mathbf x \mapsto \mathbf F(\mathbf F\mathbf x)$ with $\mathbf F = \begin{bmatrix} 1 & \Delta t \\ 0 & 1\end{bmatrix}$. Working it out, $\mathbf F(\mathbf F(p, v)) = \mathbf F(p + \Delta t\,v,\ v) = (p + 2\Delta t\,v,\ v)$, which is again linear with matrix $\begin{bmatrix} 1 & 2\Delta t \\ 0 & 1\end{bmatrix}$. In general, the composition of $\mathbf x \mapsto \mathbf B\mathbf x$ followed by $\mathbf y \mapsto \mathbf A\mathbf y$ has entry formula
    $\big(\mathbf A(\mathbf B\mathbf x)\big)_i = \sum_j a_{ij}\sum_k b_{jk}x_k = \sum_k\big(\sum_j a_{ij}b_{jk}\big)x_k$, and the bracket is the entry of the matrix of the composition.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Matrix product**</u>

    The matrix product of $\mathbf A \in \mathbb R^{m\times n}$ and $\mathbf B \in \mathbb R^{n\times p}$ is the matrix $\mathbf A\mathbf B \in \mathbb R^{m\times p}$ with entries
    $$[\mathbf A\mathbf B]_{ik} := \sum_{j=1}^n a_{ij}b_{jk} \qquad (i = 1, \ldots, m;\ k = 1, \ldots, p).$$
    It is defined only when the number of columns of $\mathbf A$ equals the number of rows of $\mathbf B$.
    ///

    We identify each $\mathbf x \in \mathbb R^n$ with the $n\times 1$ matrix whose $(i, 1)$ entry is $x_i$, and each $1\times 1$ matrix with its single entry. Then the matrix–vector product $\mathbf A\mathbf x$ is the special case $p = 1$ of the matrix product. Comparing entries also shows that the $k$-th column of $\mathbf A\mathbf B$ is $\mathbf A\mathbf b_k$, i.e. $\mathbf A[\mathbf b_1\ \cdots\ \mathbf b_p] = [\mathbf A\mathbf b_1\ \cdots\ \mathbf A\mathbf b_p]$.

    /// important | 📐 **Theorem (Products Compose Maps)**
        attrs: {class: no-icon}
    For $\mathbf A \in \mathbb R^{m\times n}$, $\mathbf B \in \mathbb R^{n\times p}$, and every $\mathbf x \in \mathbb R^p$: $(\mathbf A\mathbf B)\mathbf x = \mathbf A(\mathbf B\mathbf x)$. That is, $T_{\mathbf A\mathbf B} = T_{\mathbf A}\circ T_{\mathbf B}$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    $\big(\mathbf A(\mathbf B\mathbf x)\big)_i = \sum_{j=1}^n a_{ij}\sum_{k=1}^p b_{jk}x_k = \sum_{k=1}^p\Big(\sum_{j=1}^n a_{ij}b_{jk}\Big)x_k = \big((\mathbf A\mathbf B)\mathbf x\big)_i$, by distributivity and exchanging the order of two finite sums. $\blacksquare$
    ///

    /// important | 📐 **Corollary (Associativity)**
        attrs: {class: no-icon}
    For $\mathbf A \in \mathbb R^{m\times n}$, $\mathbf B \in \mathbb R^{n\times p}$, $\mathbf C \in \mathbb R^{p\times q}$: $(\mathbf A\mathbf B)\mathbf C = \mathbf A(\mathbf B\mathbf C)$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    By the theorem, $T_{(\mathbf A\mathbf B)\mathbf C} = T_{\mathbf A\mathbf B}\circ T_{\mathbf C} = (T_{\mathbf A}\circ T_{\mathbf B})\circ T_{\mathbf C}$ and $T_{\mathbf A(\mathbf B\mathbf C)} = T_{\mathbf A}\circ T_{\mathbf B\mathbf C} = T_{\mathbf A}\circ(T_{\mathbf B}\circ T_{\mathbf C})$. {term}`Composition` of functions is associative ([Chapter 3](ch3_sets_for_probability.md)), so the two maps are equal, and by the uniqueness part of "Matrices Are Linear Maps" so are the two matrices. $\blacksquare$
    ///

    We therefore write $\mathbf A\mathbf B\mathbf C$ without parentheses. Comparing entries also gives the distributive laws $\mathbf A(\mathbf B + \mathbf C) = \mathbf A\mathbf B + \mathbf A\mathbf C$, $(\mathbf A + \mathbf B)\mathbf C = \mathbf A\mathbf C + \mathbf B\mathbf C$, and $(c\mathbf A)\mathbf B = c(\mathbf A\mathbf B) = \mathbf A(c\mathbf B)$ whenever the sizes fit.

    **Order matters.** Matrix multiplication is not commutative:

    $$\begin{bmatrix} 0 & 1 \\ 0 & 0\end{bmatrix}\begin{bmatrix} 0 & 0 \\ 1 & 0\end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 0 & 0\end{bmatrix}, \qquad \begin{bmatrix} 0 & 0 \\ 1 & 0\end{bmatrix}\begin{bmatrix} 0 & 1 \\ 0 & 0\end{bmatrix} = \begin{bmatrix} 0 & 0 \\ 0 & 1\end{bmatrix}.$$

    Sizes can also rule one order out entirely: with $\mathbf H = [1\ \ 0] \in \mathbb R^{1\times 2}$, "predict, then measure" is $\mathbf H\mathbf F \in \mathbb R^{1\times 2}$, while $\mathbf F\mathbf H$ is undefined. Read products right to left: in $\mathbf A\mathbf B\mathbf x$, $\mathbf B$ acts first.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Block matrices

    A cart moving in 3-D has state $(\mathbf p, \mathbf v) \in \mathbb R^6$ with position $\mathbf p \in \mathbb R^3$ and velocity $\mathbf v \in \mathbb R^3$. Its prediction matrix is the $6\times 6$ matrix

    $$\mathbf F = \begin{bmatrix} \mathbf I_3 & \Delta t\,\mathbf I_3 \\ \mathbf 0 & \mathbf I_3\end{bmatrix}, \qquad \text{where } \mathbf I_3 := \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix},$$

    described by four $3\times 3$ **blocks**. Matrices built this way can be multiplied block by block, as if the blocks were numbers, provided we keep the order of each product.

    /// important | 📐 **Lemma (Block Multiplication)**
        attrs: {class: no-icon}
    Let $\mathbf A \in \mathbb R^{m\times n}$ and $\mathbf B \in \mathbb R^{n\times p}$, and split $m = m_1 + m_2$, $n = n_1 + n_2$, $p = p_1 + p_2$ into positive integers. Let $\mathbf A_{rs} \in \mathbb R^{m_r\times n_s}$ consist of the entries of $\mathbf A$ in the $r$-th group of rows and $s$-th group of columns, and similarly $\mathbf B_{st} \in \mathbb R^{n_s\times p_t}$. Then
    $$\begin{bmatrix} \mathbf A_{11} & \mathbf A_{12} \\ \mathbf A_{21} & \mathbf A_{22}\end{bmatrix}\begin{bmatrix} \mathbf B_{11} & \mathbf B_{12} \\ \mathbf B_{21} & \mathbf B_{22}\end{bmatrix} = \begin{bmatrix} \mathbf A_{11}\mathbf B_{11} + \mathbf A_{12}\mathbf B_{21} & \mathbf A_{11}\mathbf B_{12} + \mathbf A_{12}\mathbf B_{22} \\ \mathbf A_{21}\mathbf B_{11} + \mathbf A_{22}\mathbf B_{21} & \mathbf A_{21}\mathbf B_{12} + \mathbf A_{22}\mathbf B_{22}\end{bmatrix}.$$
    The same holds if the rows of $\mathbf A$ or the columns of $\mathbf B$ are not split (one block row or one block column), for example $\begin{bmatrix} \mathbf A_{11} & \mathbf A_{12} \\ \mathbf A_{21} & \mathbf A_{22}\end{bmatrix}\begin{bmatrix} \mathbf x_1 \\ \mathbf x_2\end{bmatrix} = \begin{bmatrix} \mathbf A_{11}\mathbf x_1 + \mathbf A_{12}\mathbf x_2 \\ \mathbf A_{21}\mathbf x_1 + \mathbf A_{22}\mathbf x_2\end{bmatrix}$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Let row $i$ lie in the $r$-th row group and column $k$ in the $t$-th column group. Split the defining sum at $n_1$:
    $[\mathbf A\mathbf B]_{ik} = \sum_{j \le n_1} a_{ij}b_{jk} + \sum_{j > n_1} a_{ij}b_{jk}$. The first sum is the corresponding entry of $\mathbf A_{r1}\mathbf B_{1t}$ and the second is the corresponding entry of $\mathbf A_{r2}\mathbf B_{2t}$. $\blacksquare$
    ///

    For the 3-D cart this gives $\mathbf F^2 = \begin{bmatrix} \mathbf I_3\mathbf I_3 + \Delta t\,\mathbf I_3\mathbf 0 & \mathbf I_3\,\Delta t\,\mathbf I_3 + \Delta t\,\mathbf I_3\mathbf I_3 \\ \mathbf 0 & \mathbf I_3\mathbf I_3\end{bmatrix} = \begin{bmatrix} \mathbf I_3 & 2\Delta t\,\mathbf I_3 \\ \mathbf 0 & \mathbf I_3\end{bmatrix}$, using $\mathbf I_3\mathbf M = \mathbf M\mathbf I_3 = \mathbf M$ (proved in the next section). The 15-state error model of [Chapter 21](ch21_zero_velocity_updates.md) is written entirely in such blocks.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Transpose, Identity, and Inverse

    ### Transpose

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Transpose**</u>

    The transpose of $\mathbf A \in \mathbb R^{m\times n}$ is the matrix $\mathbf A^\top \in \mathbb R^{n\times m}$ with entries $[\mathbf A^\top]_{ij} := a_{ji}$.
    ///

    Rows become columns: $\begin{bmatrix} 1 & 0\end{bmatrix}^\top = \begin{bmatrix} 1 \\ 0\end{bmatrix}$. For vectors $\mathbf x, \mathbf y \in \mathbb R^n$ (that is, $n\times 1$ matrices), $\mathbf x^\top \in \mathbb R^{1\times n}$ is a row, and two products are available:

    - $\mathbf x^\top\mathbf y = \sum_i x_iy_i = \mathbf x\cdot\mathbf y$, a $1\times 1$ matrix, i.e. a number;
    - the **outer product** $\mathbf x\mathbf y^\top \in \mathbb R^{n\times n}$, with entries $[\mathbf x\mathbf y^\top]_{ij} = x_iy_j$.

    For an error vector $\mathbf e$, the outer product $\mathbf e\mathbf e^\top$ collects all products $e_ie_j$; its expected value is the covariance matrix of [Chapter 12](ch12_vectors_matrices_covariance.md).

    /// important | 📐 **Lemma (Transpose Rules)**
        attrs: {class: no-icon}
    Whenever the sizes fit:

    1. $(\mathbf A^\top)^\top = \mathbf A$, $(\mathbf A + \mathbf B)^\top = \mathbf A^\top + \mathbf B^\top$, and $(c\mathbf A)^\top = c\mathbf A^\top$;
    2. $(\mathbf A\mathbf B)^\top = \mathbf B^\top\mathbf A^\top$;
    3. $\begin{bmatrix} \mathbf A_{11} & \mathbf A_{12} \\ \mathbf A_{21} & \mathbf A_{22}\end{bmatrix}^\top = \begin{bmatrix} \mathbf A_{11}^\top & \mathbf A_{21}^\top \\ \mathbf A_{12}^\top & \mathbf A_{22}^\top\end{bmatrix}$;
    4. $(\mathbf A\mathbf x)\cdot\mathbf y = \mathbf x\cdot(\mathbf A^\top\mathbf y)$ for $\mathbf A \in \mathbb R^{m\times n}$, $\mathbf x \in \mathbb R^n$, $\mathbf y \in \mathbb R^m$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    (1) and (3) are immediate from the definition. (2): $[(\mathbf A\mathbf B)^\top]_{ik} = [\mathbf A\mathbf B]_{ki} = \sum_j a_{kj}b_{ji} = \sum_j [\mathbf B^\top]_{ij}[\mathbf A^\top]_{jk} = [\mathbf B^\top\mathbf A^\top]_{ik}$. (4): $(\mathbf A\mathbf x)\cdot\mathbf y = (\mathbf A\mathbf x)^\top\mathbf y = \mathbf x^\top\mathbf A^\top\mathbf y = \mathbf x\cdot(\mathbf A^\top\mathbf y)$ by (2) and associativity. $\blacksquare$
    ///

    ### Identity

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Identity matrix**</u>

    For $n \in \mathbb N^+$, the $n\times n$ identity matrix $\mathbf I_n$ (or $\mathbf I$) has entries $[\mathbf I]_{ij} := \delta_{ij}$, where $\delta_{ij} := 1$ if $i = j$ and $\delta_{ij} := 0$ otherwise.
    ///

    Its columns are $\mathbf e_1, \ldots, \mathbf e_n$. For $\mathbf A \in \mathbb R^{m\times n}$, $[\mathbf I_m\mathbf A]_{ik} = \sum_j \delta_{ij}a_{jk} = a_{ik}$, so $\mathbf I_m\mathbf A = \mathbf A$, and likewise $\mathbf A\mathbf I_n = \mathbf A$. More generally, a **diagonal matrix** $\operatorname{diag}(d_1, \ldots, d_n)$ has $d_i$ in position $(i, i)$ and zeros elsewhere; comparing entries shows $\operatorname{diag}(c_1, \ldots, c_n)\operatorname{diag}(d_1, \ldots, d_n) = \operatorname{diag}(c_1d_1, \ldots, c_nd_n)$. For square $\mathbf A$, **powers** are defined by recursion ([Chapter 2](ch2_axioms_of_set_theory.md)): $\mathbf A^0 := \mathbf I$ and $\mathbf A^{k+1} := \mathbf A^k\mathbf A$. By induction on $l$ and associativity, $\mathbf A^k\mathbf A^l = \mathbf A^{k+l}$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Inverse

    Running the cart prediction backwards, from $(p', v')$ to $(p, v) = (p' - \Delta t\,v',\ v')$, undoes $\mathbf F$. Its matrix $\begin{bmatrix} 1 & -\Delta t \\ 0 & 1\end{bmatrix}$ satisfies

    $$\begin{bmatrix} 1 & \Delta t \\ 0 & 1\end{bmatrix}\begin{bmatrix} 1 & -\Delta t \\ 0 & 1\end{bmatrix} = \begin{bmatrix} 1 & -\Delta t + \Delta t \\ 0 & 1\end{bmatrix} = \mathbf I, \quad\text{and likewise in the other order.}$$

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Invertible matrix**</u>

    A square matrix $\mathbf A \in \mathbb R^{n\times n}$ is invertible if there is a matrix $\mathbf B \in \mathbb R^{n\times n}$ with $\mathbf A\mathbf B = \mathbf I$ and $\mathbf B\mathbf A = \mathbf I$.
    ///

    Such a $\mathbf B$ is unique: if $\mathbf C$ also works, then $\mathbf B = \mathbf B\mathbf I = \mathbf B(\mathbf A\mathbf C) = (\mathbf B\mathbf A)\mathbf C = \mathbf I\mathbf C = \mathbf C$. We call it the **inverse** $\mathbf A^{-1}$. Only square matrices are called invertible; $\mathbf H = [1\ \ 0]$ has no inverse, reflecting that one reading cannot recover two unknowns ([Chapter 11](ch11_measurement_functions.md)).

    /// important | 📐 **Lemma (Inverse Rules)**
        attrs: {class: no-icon}
    Let $\mathbf A, \mathbf B \in \mathbb R^{n\times n}$ be invertible and $c \ne 0$. Then $\mathbf A^{-1}$, $\mathbf A\mathbf B$, $\mathbf A^\top$, and $c\mathbf A$ are invertible, with
    $$(\mathbf A^{-1})^{-1} = \mathbf A, \qquad (\mathbf A\mathbf B)^{-1} = \mathbf B^{-1}\mathbf A^{-1}, \qquad (\mathbf A^\top)^{-1} = (\mathbf A^{-1})^\top, \qquad (c\mathbf A)^{-1} = c^{-1}\mathbf A^{-1}.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    In each case, multiply the claimed inverse by the matrix in both orders. For example $(\mathbf A\mathbf B)(\mathbf B^{-1}\mathbf A^{-1}) = \mathbf A(\mathbf B\mathbf B^{-1})\mathbf A^{-1} = \mathbf A\mathbf A^{-1} = \mathbf I$ and $(\mathbf B^{-1}\mathbf A^{-1})(\mathbf A\mathbf B) = \mathbf I$ similarly; and $\mathbf A^\top(\mathbf A^{-1})^\top = (\mathbf A^{-1}\mathbf A)^\top = \mathbf I^\top = \mathbf I$ by the transpose rules, and similarly in the other order. $\blacksquare$
    ///

    We write $\mathbf A^{-\top} := (\mathbf A^\top)^{-1} = (\mathbf A^{-1})^\top$. A diagonal matrix $\operatorname{diag}(d_1, \ldots, d_n)$ with all $d_i \ne 0$ has inverse $\operatorname{diag}(1/d_1, \ldots, 1/d_n)$. Not every square matrix is invertible:

    /// important | 📐 **Lemma (A Null Vector Prevents Inversion)**
        attrs: {class: no-icon}
    If $\mathbf A\mathbf x = \mathbf 0$ for some $\mathbf x \ne \mathbf 0$, then $\mathbf A$ is not invertible. If $\mathbf A$ is invertible, then for every $\mathbf b$ the equation $\mathbf A\mathbf x = \mathbf b$ has exactly one solution, $\mathbf x = \mathbf A^{-1}\mathbf b$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    If $\mathbf A$ had an inverse, then $\mathbf x = \mathbf A^{-1}\mathbf A\mathbf x = \mathbf A^{-1}\mathbf 0 = \mathbf 0$, a contradiction. For the second claim, $\mathbf A(\mathbf A^{-1}\mathbf b) = \mathbf b$ shows existence, and $\mathbf A\mathbf x = \mathbf b$ implies $\mathbf x = \mathbf A^{-1}\mathbf A\mathbf x = \mathbf A^{-1}\mathbf b$. $\blacksquare$
    ///

    For example, $\begin{bmatrix} 1 & 1 \\ 1 & 1\end{bmatrix}\begin{bmatrix} 1 \\ -1\end{bmatrix} = \mathbf 0$, so this matrix is not invertible.

    /// tip | **Solve, don't invert**
        attrs: {class: no-icon}
    In code, compute $\mathbf A^{-1}\mathbf b$ with `np.linalg.solve(A, b)` rather than `np.linalg.inv(A) @ b`. It is faster and more accurate, and the same applies to the factor $\mathbf S^{-1}$ in the Kalman gain.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Linear Independence, Basis, and Rank

    In [Chapter 11](ch11_measurement_functions.md), a load cell reads $z = hx + c$: the weight $x$ scaled by $h$, plus a tare offset $c$. With state $(x, c)$, two readings taken with a person on the platform, and one reading with a person plus one of the empty platform, are described by the rows of

    $$\begin{bmatrix} h & 1 \\ h & 1\end{bmatrix} \qquad\text{and}\qquad \begin{bmatrix} h & 1 \\ 0 & 1\end{bmatrix}.$$

    The first pair of readings can never separate $x$ from $c$: the first matrix sends $(1, -h)$ (one more pound, $h$ fewer counts of offset) to $(h - h, h - h) = \mathbf 0$, so the states $(x, c)$ and $(x + 1, c - h)$ produce identical readings. The second pair can. The difference is whether the columns are linearly independent.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Linear independence**</u>

    A list $(\mathbf v_1, \ldots, \mathbf v_k)$ of vectors in $\mathbb R^n$ is linearly independent if the only scalars $c_1, \ldots, c_k$ with $c_1\mathbf v_1 + \cdots + c_k\mathbf v_k = \mathbf 0$ are $c_1 = \cdots = c_k = 0$. Otherwise the list is linearly dependent. (The empty list is linearly independent.)
    ///

    /// important | 📐 **Lemma (Dependence)**
        attrs: {class: no-icon}
    1. A list $(\mathbf v_1, \ldots, \mathbf v_k)$ is linearly dependent if and only if some $\mathbf v_l$ is a linear combination of the others (an empty linear combination is $\mathbf 0$).
    2. The columns of $\mathbf A \in \mathbb R^{m\times n}$ are linearly independent if and only if $\mathbf A\mathbf x = \mathbf 0$ implies $\mathbf x = \mathbf 0$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    (1) If $\sum_j c_j\mathbf v_j = \mathbf 0$ with $c_l \ne 0$, then $\mathbf v_l = -\sum_{j\ne l}(c_j/c_l)\mathbf v_j$. Conversely, if $\mathbf v_l = \sum_{j\ne l}d_j\mathbf v_j$, then $\sum_{j \ne l}d_j\mathbf v_j - \mathbf v_l = \mathbf 0$ has the nonzero coefficient $-1$. (2) $\mathbf A\mathbf x = \sum_j x_j\mathbf a_j$, so the condition is the definition of independence of $(\mathbf a_1, \ldots, \mathbf a_n)$. $\blacksquare$
    ///

    A **subspace** of $\mathbb R^n$ is a subset $V \subseteq \mathbb R^n$ that contains $\mathbf 0$ and is closed under addition and scalar multiplication. The **span** of a list of vectors is the set of all their linear combinations; it is a subspace, because sums and multiples of linear combinations are linear combinations. The **column space** of $\mathbf A$ is the span of its columns, which is the set $\{\mathbf A\mathbf x : \mathbf x \in \mathbb R^n\}$ of all its possible outputs.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Basis**</u>

    A list $(\mathbf b_1, \ldots, \mathbf b_k)$ of vectors in a subspace $V$ of $\mathbb R^n$ is a basis of $V$ if it is linearly independent and its span is $V$.
    ///

    /// important | 📐 **Lemma (Coordinates)**
        attrs: {class: no-icon}
    A list $(\mathbf b_1, \ldots, \mathbf b_k)$ in $V$ is a basis of $V$ if and only if every $\mathbf v \in V$ can be written as $\mathbf v = \sum_j c_j\mathbf b_j$ in exactly one way.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    "At least one way" is the spanning condition. If the list is independent and $\sum_j c_j\mathbf b_j = \sum_j d_j\mathbf b_j$, then $\sum_j(c_j - d_j)\mathbf b_j = \mathbf 0$, so $c_j = d_j$ for all $j$. Conversely, if representations are unique, then $\sum_j c_j\mathbf b_j = \mathbf 0 = \sum_j 0\,\mathbf b_j$ forces every $c_j = 0$. $\blacksquare$
    ///

    The standard basis $(\mathbf e_1, \ldots, \mathbf e_n)$ is a basis of $\mathbb R^n$: it spans (shown under Vectors), and $\sum_j c_j\mathbf e_j = (c_1, \ldots, c_n) = \mathbf 0$ forces every $c_j = 0$. The next theorem, which we state without proof, says that every basis of $\mathbb R^n$ has $n$ vectors.

    /// important | 📐 **Theorem (Dimension)**
        attrs: {class: no-icon}
    1. Every subspace $V$ of $\mathbb R^n$ has a basis, and all bases of $V$ have the same number of vectors, called the **dimension** $\dim V$. In particular $\dim\mathbb R^n = n$.
    2. Every linearly independent list in $V$ has at most $\dim V$ vectors, and a list of exactly $\dim V$ vectors in $V$ is linearly independent if and only if it spans $V$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Not given here. The key step is the Steinitz exchange lemma; see [Axler (2024), *Linear Algebra Done Right*, 4th ed., Chapter 2](https://linear.axler.net/). $\blacksquare$
    ///

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Rank**</u>

    The rank of $\mathbf A \in \mathbb R^{m\times n}$, written $\operatorname{rank}\mathbf A$, is the largest $k \ge 0$ such that some $k$ columns of $\mathbf A$ form a linearly independent list.
    ///

    By the Dimension theorem, $\operatorname{rank}\mathbf A$ is the dimension of the column space. It is also a theorem that $\operatorname{rank}\mathbf A^\top = \operatorname{rank}\mathbf A$ ("row rank equals column rank"; [Axler, Chapter 3](https://linear.axler.net/)). For the load cell with $h \ne 0$: in the first matrix, $h\,(1, 1) - (h, h) = \mathbf 0$, so the columns are dependent, while each column alone is nonzero; its rank is $1$. In the second, $c_1(h, 0) + c_2(1, 1) = \mathbf 0$ forces $c_2 = 0$ (second entry) and then $c_1 = 0$; its rank is $2$. [Chapter 13](ch13_kalman_filter.md) turns this into the rank test for observability.

    /// important | 📐 **Theorem (Invertible Matrix Theorem)**
        attrs: {class: no-icon}
    For $\mathbf A \in \mathbb R^{n\times n}$ the following are equivalent:

    1. $\mathbf A$ is invertible;
    2. $\mathbf A\mathbf x = \mathbf 0$ only for $\mathbf x = \mathbf 0$;
    3. the columns of $\mathbf A$ are linearly independent;
    4. $\operatorname{rank}\mathbf A = n$;
    5. the columns of $\mathbf A$ form a basis of $\mathbb R^n$;
    6. there is $\mathbf B \in \mathbb R^{n\times n}$ with $\mathbf B\mathbf A = \mathbf I$;
    7. there is $\mathbf B \in \mathbb R^{n\times n}$ with $\mathbf A\mathbf B = \mathbf I$.

    In particular, for square matrices a one-sided inverse is two-sided: if $\mathbf B\mathbf A = \mathbf I$ or $\mathbf A\mathbf B = \mathbf I$, then $\mathbf B = \mathbf A^{-1}$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    (1 ⇒ 6, 7) Take $\mathbf B = \mathbf A^{-1}$. (6 ⇒ 2) If $\mathbf A\mathbf x = \mathbf 0$, then $\mathbf x = \mathbf B\mathbf A\mathbf x = \mathbf 0$. (2 ⇔ 3) Lemma (Dependence). (3 ⇔ 4) $\mathbf A$ has exactly $n$ columns. (3 ⇒ 5) By the Dimension theorem, $n$ independent vectors in $\mathbb R^n$ span it. (7 ⇒ 5) Every $\mathbf y = \mathbf A(\mathbf B\mathbf y)$ is a linear combination of the columns, so the $n$ columns span $\mathbb R^n$ and, by the Dimension theorem, are independent.

    (5 ⇒ 1) Each $\mathbf e_i$ is a linear combination of the columns, $\mathbf e_i = \mathbf A\mathbf b_i$ for some $\mathbf b_i$. Put $\mathbf B := [\mathbf b_1\ \cdots\ \mathbf b_n]$; then $\mathbf A\mathbf B = [\mathbf A\mathbf b_1\ \cdots\ \mathbf A\mathbf b_n] = \mathbf I$. Moreover $\mathbf A(\mathbf B\mathbf A - \mathbf I) = (\mathbf A\mathbf B)\mathbf A - \mathbf A = \mathbf 0$, so every column $\mathbf c$ of $\mathbf B\mathbf A - \mathbf I$ satisfies $\mathbf A\mathbf c = \mathbf 0$, hence $\mathbf c = \mathbf 0$ by (3), which (5) includes. So $\mathbf B\mathbf A = \mathbf I$ too.

    These implications connect all seven statements. Finally, if $\mathbf B\mathbf A = \mathbf I$, then $\mathbf A$ is invertible by (6) and $\mathbf B = \mathbf B\mathbf A\mathbf A^{-1} = \mathbf A^{-1}$; if $\mathbf A\mathbf B = \mathbf I$, then $\mathbf B = \mathbf A^{-1}\mathbf A\mathbf B = \mathbf A^{-1}$. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Determinants

    The matrix $\begin{bmatrix} a & b \\ c & d\end{bmatrix}$ sends the unit square to the parallelogram spanned by its columns $(a, c)$ and $(b, d)$, whose area is $|ad - bc|$.[^area] The same number decides invertibility: we prove below that the matrix is invertible exactly when $ad - bc \ne 0$. The determinant extends this number to $n\times n$ matrices; it appears in the multivariate normal density of [Chapter 12](ch12_vectors_matrices_covariance.md) as $\det\boldsymbol\Sigma$.

    For $n \ge 2$, $\mathbf A \in \mathbb R^{n\times n}$, and $i, j \in \{1, \ldots, n\}$, let $\mathbf A_{(i,j)} \in \mathbb R^{(n-1)\times(n-1)}$ be $\mathbf A$ with row $i$ and column $j$ deleted. Precisely, $[\mathbf A_{(i,j)}]_{kl} := a_{k'l'}$, where $k' := k$ if $k < i$ and $k' := k + 1$ if $k \ge i$, and $l'$ is defined from $l$ and $j$ in the same way.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Determinant**</u>

    The determinant of a square matrix is defined by recursion on its size $n$: for $n = 1$, $\det[a] := a$; for $n \ge 2$ and $\mathbf A \in \mathbb R^{n\times n}$,
    $$\det\mathbf A := \sum_{j=1}^n (-1)^{1+j}\,a_{1j}\det\mathbf A_{(1,j)},$$
    where $\mathbf A_{(1,j)}$ is $\mathbf A$ with row $1$ and column $j$ deleted (expansion along the first row).
    ///

    For $n = 2$ and $n = 3$ this gives

    $$\det\begin{bmatrix} a & b \\ c & d\end{bmatrix} = ad - bc, \qquad \det\begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i\end{bmatrix} = a(ei - fh) - b(di - fg) + c(dh - eg).$$

    **Examples.** The cart matrix $\begin{bmatrix} 1 & \Delta t \\ 0 & 1\end{bmatrix}$ has determinant $1$: it shears the unit square without changing its area. A rotation has $\det\mathbf R(\theta) = \cos^2\theta + \sin^2\theta = 1$. A $2\times 2$ covariance matrix with standard deviations $\sigma_x, \sigma_y$ and correlation coefficient $\rho$ has
    $$\det\begin{bmatrix} \sigma_x^2 & \rho\sigma_x\sigma_y \\ \rho\sigma_x\sigma_y & \sigma_y^2\end{bmatrix} = \sigma_x^2\sigma_y^2(1 - \rho^2),$$
    which shrinks to $0$ as $|\rho| \to 1$, when the two errors become exact multiples of each other. A $3\times 3$ example we will meet again under Cholesky Decomposition:
    $$\det\begin{bmatrix} 4 & 2 & -2 \\ 2 & 10 & 2 \\ -2 & 2 & 6\end{bmatrix} = 4(60 - 4) - 2(12 + 4) + (-2)(4 + 20) = 144.$$

    [^area]: This area formula is an interpretation and is not used in any proof below; see [Wikipedia: Determinant](https://en.wikipedia.org/wiki/Determinant). You can check it in the interactive figure under Eigenvalues and Eigenvectors.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A square matrix is **lower triangular** if $a_{ij} = 0$ whenever $j > i$ (only zeros above the diagonal), and **upper triangular** if $a_{ij} = 0$ whenever $i > j$.

    /// important | 📐 **Lemma (Triangular Determinants)**
        attrs: {class: no-icon}
    If $\mathbf A \in \mathbb R^{n\times n}$ is lower triangular, then $\det\mathbf A = a_{11}a_{22}\cdots a_{nn}$. In particular, $\det\mathbf I = 1$ and $\det\operatorname{diag}(d_1, \ldots, d_n) = d_1\cdots d_n$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Induction on $n$; the case $n = 1$ is the definition. For $n \ge 2$ the first row is $(a_{11}, 0, \ldots, 0)$, so the definition gives $\det\mathbf A = a_{11}\det\mathbf A_{(1,1)}$. The entries of $\mathbf A_{(1,1)}$ are $[\mathbf A_{(1,1)}]_{kl} = a_{k+1,l+1}$, which vanish when $l > k$; so $\mathbf A_{(1,1)}$ is lower triangular with diagonal $a_{22}, \ldots, a_{nn}$, and the induction hypothesis finishes the proof. $\blacksquare$
    ///

    The general properties of the determinant are proved with the Leibniz formula, which writes $\det\mathbf A$ as a sum over all permutations of $\{1, \ldots, n\}$. We state them and prove them only for $n = 2$.

    /// important | 📐 **Theorem (Properties of the Determinant)**
        attrs: {class: no-icon}
    For $\mathbf A, \mathbf B \in \mathbb R^{n\times n}$:

    1. $\det\mathbf A^\top = \det\mathbf A$;
    2. $\det(\mathbf A\mathbf B) = \det\mathbf A\,\det\mathbf B$;
    3. the determinant can be expanded along any row $i$ or any column $j$:
    $\det\mathbf A = \sum_{j=1}^n(-1)^{i+j}a_{ij}\det\mathbf A_{(i,j)} = \sum_{i=1}^n(-1)^{i+j}a_{ij}\det\mathbf A_{(i,j)}$;
    4. swapping two rows multiplies $\det\mathbf A$ by $-1$, multiplying one row by $c$ multiplies it by $c$, and adding a multiple of one row to another leaves it unchanged; by (1), the same holds for columns;
    5. $\mathbf A$ is invertible if and only if $\det\mathbf A \ne 0$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    For $n = 2$, (1), (3), and (4) are checked by expanding both sides, and (2) by
    $\det\Big(\begin{bmatrix} a & b \\ c & d\end{bmatrix}\begin{bmatrix} p & q \\ r & s\end{bmatrix}\Big) = (ap + br)(cq + ds) - (aq + bs)(cp + dr) = (ad - bc)(ps - qr)$.
    (5) for $n = 2$ is the next lemma. For general $n$, see [Axler (2024), *Linear Algebra Done Right*, 4th ed., Chapter 9](https://linear.axler.net/) or [Wikipedia: Leibniz formula for determinants](https://en.wikipedia.org/wiki/Leibniz_formula_for_determinants). $\blacksquare$
    ///

    /// important | 📐 **Lemma (Inverse of a 2 × 2 Matrix)**
        attrs: {class: no-icon}
    $\mathbf A = \begin{bmatrix} a & b \\ c & d\end{bmatrix}$ is invertible if and only if $ad - bc \ne 0$, and then
    $$\mathbf A^{-1} = \frac{1}{ad - bc}\begin{bmatrix} d & -b \\ -c & a\end{bmatrix}.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Let $\mathbf A' := \begin{bmatrix} d & -b \\ -c & a\end{bmatrix}$. Multiplying out gives $\mathbf A\mathbf A' = \mathbf A'\mathbf A = (ad - bc)\mathbf I$. If $ad - bc \ne 0$, then $(ad - bc)^{-1}\mathbf A'$ is an inverse. If $ad - bc = 0$ and $\mathbf A$ had an inverse, then $\mathbf A' = \mathbf A'\mathbf A\mathbf A^{-1} = \mathbf 0\,\mathbf A^{-1} = \mathbf 0$, so $a = b = c = d = 0$ and $\mathbf A = \mathbf 0$; but $\mathbf 0\,\mathbf B = \mathbf 0 \ne \mathbf I$ for every $\mathbf B$, a contradiction. $\blacksquare$
    ///

    For the $2\times 2$ covariance matrix above, with $\sigma_x, \sigma_y > 0$ and $|\rho| < 1$,
    $$\begin{bmatrix} \sigma_x^2 & \rho\sigma_x\sigma_y \\ \rho\sigma_x\sigma_y & \sigma_y^2\end{bmatrix}^{-1} = \frac{1}{\sigma_x^2\sigma_y^2(1 - \rho^2)}\begin{bmatrix} \sigma_y^2 & -\rho\sigma_x\sigma_y \\ -\rho\sigma_x\sigma_y & \sigma_x^2\end{bmatrix},$$
    the matrix that appears in the exponent of the bivariate normal density.

    /// important | 📐 **Corollary (Consequences)**
        attrs: {class: no-icon}
    For $\mathbf A, \mathbf V \in \mathbb R^{n\times n}$ and $c \in \mathbb R$:

    1. if $\mathbf A$ is invertible, $\det(\mathbf A^{-1}) = 1/\det\mathbf A$;
    2. $\det(c\mathbf A) = c^n\det\mathbf A$;
    3. if $\mathbf V$ is invertible, $\det(\mathbf V\mathbf A\mathbf V^{-1}) = \det\mathbf A$;
    4. if $\mathbf A$ is upper triangular, $\det\mathbf A = a_{11}\cdots a_{nn}$;
    5. $\det\mathbf A \ne 0$ is an eighth equivalent condition in the Invertible Matrix Theorem.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    (1) $\det\mathbf A\det\mathbf A^{-1} = \det(\mathbf A\mathbf A^{-1}) = \det\mathbf I = 1$. (2) Multiply each of the $n$ rows by $c$, using property 4. (3) $\det\mathbf V\det\mathbf A\det\mathbf V^{-1} = \det\mathbf A$ by (1). (4) $\mathbf A^\top$ is lower triangular with the same diagonal; use property 1. (5) is property 5. $\blacksquare$
    ///

    /// tip | **A small determinant does not mean "almost singular"**
        attrs: {class: no-icon}
    $\det(0.1\,\mathbf I_{20}) = 10^{-20}$, yet $0.1\,\mathbf I_{20}$ is perfectly easy to invert. The determinant scales with the units of every row, so it is a poor numerical test of near-singularity. Use the eigenvalues of a symmetric matrix (below) or `np.linalg.cond` instead.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Trace

    For a 3-D position error $\mathbf e$ with mean $\mathbf 0$ and covariance matrix $\mathbf P$ ([Chapter 12](ch12_vectors_matrices_covariance.md)), the diagonal entries $p_{11}, p_{22}, p_{33}$ are the variances of the East, North, and Up errors. By linearity of expectation ([Chapter 6](ch6_expectation_and_variance.md)), their sum is the mean squared distance between estimate and truth: $p_{11} + p_{22} + p_{33} = \mathbb E[e_1^2 + e_2^2 + e_3^2] = \mathbb E\|\mathbf e\|^2$. [Chapter 13](ch13_kalman_filter.md) chooses the Kalman gain to make this sum as small as possible.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Trace**</u>

    The trace of a square matrix $\mathbf A \in \mathbb R^{n\times n}$ is the sum of its diagonal entries,
    $$\operatorname{tr}\mathbf A := \sum_{i=1}^n a_{ii}.$$
    ///

    Directly from the definition, $\operatorname{tr}(\mathbf A + \mathbf B) = \operatorname{tr}\mathbf A + \operatorname{tr}\mathbf B$, $\operatorname{tr}(c\mathbf A) = c\operatorname{tr}\mathbf A$, and $\operatorname{tr}\mathbf A^\top = \operatorname{tr}\mathbf A$.

    /// important | 📐 **Theorem (Cyclic Property of the Trace)**
        attrs: {class: no-icon}
    For $\mathbf A \in \mathbb R^{m\times n}$ and $\mathbf B \in \mathbb R^{n\times m}$, $\operatorname{tr}(\mathbf A\mathbf B) = \operatorname{tr}(\mathbf B\mathbf A)$. Consequently, whenever the products are defined,
    $$\operatorname{tr}(\mathbf A\mathbf B\mathbf C) = \operatorname{tr}(\mathbf B\mathbf C\mathbf A) = \operatorname{tr}(\mathbf C\mathbf A\mathbf B).$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    $\operatorname{tr}(\mathbf A\mathbf B) = \sum_{i=1}^m\sum_{j=1}^n a_{ij}b_{ji} = \sum_{j=1}^n\sum_{i=1}^m b_{ji}a_{ij} = \operatorname{tr}(\mathbf B\mathbf A)$, exchanging two finite sums. For three factors, apply this to the two factors $\mathbf A$ and $\mathbf B\mathbf C$, then to $\mathbf B$ and $\mathbf C\mathbf A$. $\blacksquare$
    ///

    Note that $\mathbf A\mathbf B$ is $m\times m$ while $\mathbf B\mathbf A$ is $n\times n$. For a vector $\mathbf x \in \mathbb R^n$, the $n\times n$ outer product and the $1\times 1$ inner product have the same trace: $\operatorname{tr}(\mathbf x\mathbf x^\top) = \operatorname{tr}(\mathbf x^\top\mathbf x) = \|\mathbf x\|^2$.

    Only *cyclic* reorderings are allowed. With $\mathbf A = \begin{bmatrix} 0 & 1 \\ 0 & 0\end{bmatrix}$, $\mathbf B = \begin{bmatrix} 0 & 0 \\ 1 & 0\end{bmatrix}$, and $\mathbf C = \begin{bmatrix} 1 & 0 \\ 0 & 0\end{bmatrix}$, we get $\mathbf A\mathbf B\mathbf C = \mathbf C$, so $\operatorname{tr}(\mathbf A\mathbf B\mathbf C) = 1$, but $\mathbf A\mathbf C = \mathbf 0$, so $\operatorname{tr}(\mathbf A\mathbf C\mathbf B) = 0$.

    /// important | 📐 **Corollary (Traces of Quadratic Forms and Similar Matrices)**
        attrs: {class: no-icon}
    1. For $\mathbf A \in \mathbb R^{n\times n}$ and $\mathbf x, \mathbf y \in \mathbb R^n$, $\mathbf x^\top\mathbf A\mathbf y = \operatorname{tr}(\mathbf A\mathbf y\mathbf x^\top)$; in particular $\mathbf x^\top\mathbf A\mathbf x = \operatorname{tr}(\mathbf A\mathbf x\mathbf x^\top)$.
    2. If $\mathbf V$ is invertible, $\operatorname{tr}(\mathbf V\mathbf A\mathbf V^{-1}) = \operatorname{tr}\mathbf A$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    (1) A $1\times 1$ matrix equals its trace, and $\operatorname{tr}(\mathbf x^\top(\mathbf A\mathbf y)) = \operatorname{tr}((\mathbf A\mathbf y)\mathbf x^\top)$ by the cyclic property with factors $\mathbf x^\top \in \mathbb R^{1\times n}$ and $\mathbf A\mathbf y \in \mathbb R^{n\times 1}$. (2) $\operatorname{tr}(\mathbf V(\mathbf A\mathbf V^{-1})) = \operatorname{tr}(\mathbf A\mathbf V^{-1}\mathbf V) = \operatorname{tr}\mathbf A$. $\blacksquare$
    ///

    Part 1 is how [Chapter 12](ch12_vectors_matrices_covariance.md) computes the expected value of a quadratic form $\mathbf x^\top\mathbf A\mathbf x$: the trace moves the random vector into one outer product.

    ### The Frobenius norm

    Viewing $\mathbf A \in \mathbb R^{m\times n}$ as a list of $mn$ numbers gives it a length, the **Frobenius norm**
    $$\|\mathbf A\|_F := \Big(\sum_{i=1}^m\sum_{j=1}^n a_{ij}^2\Big)^{1/2}.$$
    Since $[\mathbf A^\top\mathbf A]_{jj} = \sum_i a_{ij}^2$, we have $\|\mathbf A\|_F^2 = \operatorname{tr}(\mathbf A^\top\mathbf A)$, and every entry satisfies $|a_{ij}| \le \|\mathbf A\|_F$.

    /// important | 📐 **Lemma (Submultiplicativity)**
        attrs: {class: no-icon}
    For $\mathbf A \in \mathbb R^{m\times n}$ and $\mathbf B \in \mathbb R^{n\times p}$, $\|\mathbf A\mathbf B\|_F \le \|\mathbf A\|_F\,\|\mathbf B\|_F$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Let $\mathbf r_i := (a_{i1}, \ldots, a_{in})$ be the $i$-th row of $\mathbf A$ and $\mathbf b_k$ the $k$-th column of $\mathbf B$. Then $[\mathbf A\mathbf B]_{ik} = \mathbf r_i\cdot\mathbf b_k$, so by Cauchy–Schwarz $[\mathbf A\mathbf B]_{ik}^2 \le \|\mathbf r_i\|^2\|\mathbf b_k\|^2$. Summing over $i$ and $k$ gives $\|\mathbf A\mathbf B\|_F^2 \le \big(\sum_i\|\mathbf r_i\|^2\big)\big(\sum_k\|\mathbf b_k\|^2\big) = \|\mathbf A\|_F^2\|\mathbf B\|_F^2$; take square roots. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Orthogonal Matrices

    Turning an IMU changes the coordinates of every vector it measures, but not lengths or angles. The rotation matrix $\mathbf R(\theta)$ from Matrices and Linear Maps has columns $(\cos\theta, \sin\theta)$ and $(-\sin\theta, \cos\theta)$. Each has norm $1$, because $\cos^2\theta + \sin^2\theta = 1$, and their dot product is $-\cos\theta\sin\theta + \sin\theta\cos\theta = 0$. Since $[\mathbf A^\top\mathbf A]_{ij}$ is the dot product of columns $i$ and $j$ of $\mathbf A$, this says exactly that $\mathbf R(\theta)^\top\mathbf R(\theta) = \mathbf I$.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Orthogonal matrix**</u>

    A square matrix $\mathbf Q \in \mathbb R^{n\times n}$ is orthogonal if $\mathbf Q^\top\mathbf Q = \mathbf I$.
    ///

    Equivalently, the columns of $\mathbf Q$ are **orthonormal**: each has norm $1$ and any two different columns are orthogonal.

    /// important | 📐 **Theorem (Properties of Orthogonal Matrices)**
        attrs: {class: no-icon}
    Let $\mathbf Q, \mathbf Q' \in \mathbb R^{n\times n}$ be orthogonal. Then:

    1. $\mathbf Q$ is invertible with $\mathbf Q^{-1} = \mathbf Q^\top$; in particular $\mathbf Q\mathbf Q^\top = \mathbf I$, so the rows are orthonormal too;
    2. $\mathbf Q^\top$ and $\mathbf Q\mathbf Q'$ are orthogonal;
    3. $\det\mathbf Q = \pm 1$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    (1) $\mathbf Q^\top$ is a one-sided inverse, hence the inverse, by the Invertible Matrix Theorem. (2) $(\mathbf Q^\top)^\top\mathbf Q^\top = \mathbf Q\mathbf Q^\top = \mathbf I$ by (1), and $(\mathbf Q\mathbf Q')^\top\mathbf Q\mathbf Q' = \mathbf Q'^\top\mathbf Q^\top\mathbf Q\mathbf Q' = \mathbf Q'^\top\mathbf Q' = \mathbf I$. (3) $1 = \det\mathbf I = \det(\mathbf Q^\top\mathbf Q) = \det\mathbf Q^\top\det\mathbf Q = (\det\mathbf Q)^2$ by properties 1 and 2 of the determinant. $\blacksquare$
    ///

    /// important | 📐 **Theorem (Orthogonal Matrices Preserve Geometry)**
        attrs: {class: no-icon}
    For $\mathbf Q \in \mathbb R^{n\times n}$ the following are equivalent:

    1. $\mathbf Q$ is orthogonal;
    2. $\mathbf Q\mathbf x\cdot\mathbf Q\mathbf y = \mathbf x\cdot\mathbf y$ for all $\mathbf x, \mathbf y \in \mathbb R^n$ (dot products, hence angles, are preserved);
    3. $\|\mathbf Q\mathbf x\| = \|\mathbf x\|$ for all $\mathbf x \in \mathbb R^n$ (lengths are preserved).
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    (1 ⇒ 2) $\mathbf Q\mathbf x\cdot\mathbf Q\mathbf y = \mathbf x^\top\mathbf Q^\top\mathbf Q\mathbf y = \mathbf x^\top\mathbf y$. (2 ⇒ 3) Take $\mathbf y = \mathbf x$ and square roots. (3 ⇒ 2) Expanding with the dot product rules gives the polarization identity $\mathbf x\cdot\mathbf y = \tfrac14\big(\|\mathbf x + \mathbf y\|^2 - \|\mathbf x - \mathbf y\|^2\big)$; apply it to $\mathbf Q\mathbf x, \mathbf Q\mathbf y$ and use $\mathbf Q\mathbf x \pm \mathbf Q\mathbf y = \mathbf Q(\mathbf x \pm \mathbf y)$. (2 ⇒ 1) $[\mathbf Q^\top\mathbf Q]_{ij} = \mathbf Q\mathbf e_i\cdot\mathbf Q\mathbf e_j = \mathbf e_i\cdot\mathbf e_j = \delta_{ij}$. $\blacksquare$
    ///

    **Examples.** $\mathbf R(\theta)$ has determinant $+1$. The mirror $\operatorname{diag}(1, -1)$ is orthogonal with determinant $-1$: it preserves lengths but flips orientation (a counterclockwise turn becomes clockwise). A **permutation matrix**, whose columns are $\mathbf e_1, \ldots, \mathbf e_n$ in some order, is orthogonal. The orthogonal matrices with determinant $+1$ are exactly the rotation matrices of [Chapter 17](ch17_rotations.md), which form the {term}`special orthogonal group`.

    Orthogonal changes of coordinates do not change the mean squared error. If an error vector $\mathbf e$ with covariance $\mathbf P$ is expressed in rotated coordinates $\mathbf Q\mathbf e$, its covariance becomes $\mathbf Q\mathbf P\mathbf Q^\top$ ([Chapter 12](ch12_vectors_matrices_covariance.md)), and $\operatorname{tr}(\mathbf Q\mathbf P\mathbf Q^\top) = \operatorname{tr}(\mathbf P\mathbf Q^\top\mathbf Q) = \operatorname{tr}\mathbf P$.

    /// caution | ⚠️ **Assumptions and Failure Modes**
        attrs: {class: no-icon}
    In floating-point arithmetic, a product of many orthogonal matrices (for example, an attitude updated 100 times per second) slowly stops being orthogonal: rounding makes $\mathbf Q^\top\mathbf Q$ drift away from $\mathbf I$, so lengths are no longer preserved. Attitude code therefore re-orthonormalizes periodically; [Chapter 18](ch18_quaternions.md) shows the quaternion version of this fix.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Eigenvalues and Eigenvectors

    Most vectors change direction under the covariance-like matrix $\boldsymbol\Sigma = \begin{bmatrix} 2 & 1 \\ 1 & 2\end{bmatrix}$, but two directions do not:

    $$\boldsymbol\Sigma\begin{bmatrix} 1 \\ 1\end{bmatrix} = \begin{bmatrix} 3 \\ 3\end{bmatrix} = 3\begin{bmatrix} 1 \\ 1\end{bmatrix}, \qquad \boldsymbol\Sigma\begin{bmatrix} 1 \\ -1\end{bmatrix} = \begin{bmatrix} 1 \\ -1\end{bmatrix} = 1\begin{bmatrix} 1 \\ -1\end{bmatrix}.$$

    Along $(1, 1)$, $\boldsymbol\Sigma$ stretches by $3$; along the perpendicular direction $(1, -1)$ it changes nothing. In [Chapter 12](ch12_vectors_matrices_covariance.md) these become the axes of a confidence ellipse. By contrast, the quarter-turn $\mathbf R(90°) = \begin{bmatrix} 0 & -1 \\ 1 & 0\end{bmatrix}$ turns every nonzero vector by a right angle, so it keeps no real direction fixed. Yet $\mathbf R(90°)^2 = -\mathbf I$: in some sense it "multiplies by a square root of $-1$". Complex numbers make this precise, and they guarantee that every square matrix has at least one eigenvalue, which the spectral theorem in the next section needs.

    ### Complex numbers (just enough)

    The set of **complex numbers** is $\mathbb C := \mathbb R^2$ with addition $(a, b) + (c, d) := (a + c, b + d)$ and multiplication $(a, b)(c, d) := (ac - bd, ad + bc)$. We identify each $a \in \mathbb R$ with $(a, 0)$ (this respects both operations) and write $i := (0, 1)$, so that $(a, b) = a + bi$ and $i^2 = -1$. With these operations $\mathbb C$ is a {term}`field`; checking the field axioms is routine ([Wikipedia: Complex number](https://en.wikipedia.org/wiki/Complex_number)). The **conjugate** of $z = a + bi$ is $\bar z := a - bi$, and direct computation gives

    $$\overline{z + w} = \bar z + \bar w, \qquad \overline{zw} = \bar z\,\bar w, \qquad z\bar z = a^2 + b^2.$$

    So $z\bar z$ is a real number $\ge 0$ that is $0$ only for $z = 0$, and $z$ is real exactly when $\bar z = z$.

    Vectors and matrices with complex entries ($\mathbb C^n$, $\mathbb C^{n\times n}$) are defined as before with $\mathbb C$ in place of $\mathbb R$. Everything from Matrices and Linear Maps through Determinants that does not mention order, norms, or dot products used only the field axioms, so it holds verbatim over $\mathbb C$; in particular the Invertible Matrix Theorem and the properties of the determinant do. Conjugation of vectors and matrices acts entrywise, so $\overline{\mathbf A\mathbf v} = \bar{\mathbf A}\,\bar{\mathbf v}$. For $\mathbf v \in \mathbb C^n$, the number $\bar{\mathbf v}^\top\mathbf v = \sum_i\bar v_iv_i$ is real and $\ge 0$, and it is $0$ only for $\mathbf v = \mathbf 0$.

    ### Definitions

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Eigenvalue**</u>

    A number $\lambda \in \mathbb C$ is an eigenvalue of a square matrix $\mathbf A \in \mathbb C^{n\times n}$ (for example, $\mathbf A \in \mathbb R^{n\times n}$) if $\mathbf A\mathbf v = \lambda\mathbf v$ for some nonzero $\mathbf v \in \mathbb C^n$.
    ///

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Eigenvector**</u>

    A vector $\mathbf v \in \mathbb C^n$ is an eigenvector of a square matrix $\mathbf A \in \mathbb C^{n\times n}$ if $\mathbf v \ne \mathbf 0$ and $\mathbf A\mathbf v = \lambda\mathbf v$ for some $\lambda \in \mathbb C$, which is then called the eigenvalue of $\mathbf v$.
    ///

    Every nonzero multiple of an eigenvector is an eigenvector for the same eigenvalue, so it is the *direction* that matters.

    /// important | 📐 **Lemma (Characteristic Equation)**
        attrs: {class: no-icon}
    $\lambda \in \mathbb C$ is an eigenvalue of $\mathbf A \in \mathbb C^{n\times n}$ if and only if $\det(\lambda\mathbf I - \mathbf A) = 0$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    $\lambda$ is an eigenvalue $\iff$ $(\lambda\mathbf I - \mathbf A)\mathbf v = \mathbf 0$ for some $\mathbf v \ne \mathbf 0$ $\iff$ $\lambda\mathbf I - \mathbf A$ is not invertible (Invertible Matrix Theorem, 1 ⇔ 2) $\iff$ $\det(\lambda\mathbf I - \mathbf A) = 0$ (property 5 of the determinant). $\blacksquare$
    ///

    The function $p_{\mathbf A}(\lambda) := \det(\lambda\mathbf I - \mathbf A)$ is the **characteristic polynomial** of $\mathbf A$. For $n = 2$ we can compute it directly:

    $$p_{\mathbf A}(\lambda) = \det\begin{bmatrix} \lambda - a & -b \\ -c & \lambda - d\end{bmatrix} = \lambda^2 - (a + d)\lambda + (ad - bc) = \lambda^2 - (\operatorname{tr}\mathbf A)\lambda + \det\mathbf A,$$

    so the quadratic formula gives the eigenvalues $\lambda = \tfrac12\operatorname{tr}\mathbf A \pm \sqrt{\tfrac14(\operatorname{tr}\mathbf A)^2 - \det\mathbf A}$, where a negative radicand $-s$ has the square roots $\pm i\sqrt s$. For general $n$ we state the analogous facts.

    /// important | 📐 **Theorem (Characteristic Polynomial; Fundamental Theorem of Algebra)**
        attrs: {class: no-icon}
    1. For $\mathbf A \in \mathbb C^{n\times n}$, $p_{\mathbf A}$ is a polynomial of degree $n$ of the form $p_{\mathbf A}(\lambda) = \lambda^n - (\operatorname{tr}\mathbf A)\lambda^{n-1} + \cdots + (-1)^n\det\mathbf A$.
    2. Every polynomial $c_n\lambda^n + \cdots + c_1\lambda + c_0$ with complex coefficients, $n \ge 1$, and $c_n \ne 0$ factors as $c_n(\lambda - \lambda_1)\cdots(\lambda - \lambda_n)$ for some $\lambda_1, \ldots, \lambda_n \in \mathbb C$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    (1) follows by induction on $n$ from the first-row expansion (the constant term is $p_{\mathbf A}(0) = \det(-\mathbf A) = (-1)^n\det\mathbf A$); see [Wikipedia: Characteristic polynomial](https://en.wikipedia.org/wiki/Characteristic_polynomial). (2) is the fundamental theorem of algebra, whose proofs use analysis; see [Wikipedia: Fundamental theorem of algebra](https://en.wikipedia.org/wiki/Fundamental_theorem_of_algebra). Neither is proved here. $\blacksquare$
    ///

    /// important | 📐 **Corollary (Every Square Matrix Has an Eigenvalue)**
        attrs: {class: no-icon}
    Every $\mathbf A \in \mathbb C^{n\times n}$ has at least one and at most $n$ distinct eigenvalues. Listing them with multiplicity as $\lambda_1, \ldots, \lambda_n$, so that $p_{\mathbf A}(\lambda) = (\lambda - \lambda_1)\cdots(\lambda - \lambda_n)$,
    $$\operatorname{tr}\mathbf A = \lambda_1 + \cdots + \lambda_n, \qquad \det\mathbf A = \lambda_1\cdots\lambda_n.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    By the theorem, $p_{\mathbf A}(\lambda) = (\lambda - \lambda_1)\cdots(\lambda - \lambda_n)$. A product in a field is $0$ exactly when a factor is, so the roots of $p_{\mathbf A}$, which are the eigenvalues by the lemma, are exactly $\lambda_1, \ldots, \lambda_n$. Multiplying out gives $\lambda^n - (\lambda_1 + \cdots + \lambda_n)\lambda^{n-1} + \cdots + (-1)^n\lambda_1\cdots\lambda_n$; compare coefficients with part 1 of the theorem. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Examples.**

    1. $\boldsymbol\Sigma = \begin{bmatrix} 2 & 1 \\ 1 & 2\end{bmatrix}$: $p(\lambda) = \lambda^2 - 4\lambda + 3 = (\lambda - 1)(\lambda - 3)$. Indeed $\operatorname{tr}\boldsymbol\Sigma = 4 = 1 + 3$ and $\det\boldsymbol\Sigma = 3 = 1\cdot 3$.
    2. The rotation $\mathbf R(\theta)$: $p(\lambda) = \lambda^2 - 2\cos\theta\,\lambda + 1$, so $\lambda = \cos\theta \pm i\sin\theta$, with eigenvectors $(1, \mp i)$. The eigenvalues are real only when $\sin\theta = 0$, i.e. when $\mathbf R(\theta) = \pm\mathbf I$.
    3. The cart matrix $\mathbf F = \begin{bmatrix} 1 & \Delta t \\ 0 & 1\end{bmatrix}$: $p(\lambda) = (\lambda - 1)^2$, so $1$ is the only eigenvalue, with multiplicity $2$. But $(\mathbf F - \mathbf I)\mathbf v = (\Delta t\,v_2, 0)$ vanishes only when $v_2 = 0$, so every eigenvector is a multiple of $\mathbf e_1$: there is only one eigenvector direction.

    The last example uses a general shortcut: if $\mathbf A$ is triangular, so is $\lambda\mathbf I - \mathbf A$, so $p_{\mathbf A}(\lambda) = (\lambda - a_{11})\cdots(\lambda - a_{nn})$ and **the eigenvalues of a triangular matrix are its diagonal entries.**

    /// important | 📐 **Theorem (Diagonalization)**
        attrs: {class: no-icon}
    Suppose $\mathbf A \in \mathbb C^{n\times n}$ has eigenvectors $\mathbf v_1, \ldots, \mathbf v_n$ (with eigenvalues $\lambda_1, \ldots, \lambda_n$) that form a linearly independent list. Let $\mathbf V := [\mathbf v_1\ \cdots\ \mathbf v_n]$ and $\boldsymbol\Lambda := \operatorname{diag}(\lambda_1, \ldots, \lambda_n)$. Then $\mathbf V$ is invertible, and for every $k \in \mathbb N$,
    $$\mathbf A = \mathbf V\boldsymbol\Lambda\mathbf V^{-1}, \qquad \mathbf A^k = \mathbf V\boldsymbol\Lambda^k\mathbf V^{-1} = \mathbf V\operatorname{diag}(\lambda_1^k, \ldots, \lambda_n^k)\mathbf V^{-1}.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    $\mathbf V$ is invertible by the Invertible Matrix Theorem (3 ⇒ 1). Column by column, $\mathbf A\mathbf V = [\mathbf A\mathbf v_1\ \cdots\ \mathbf A\mathbf v_n] = [\lambda_1\mathbf v_1\ \cdots\ \lambda_n\mathbf v_n] = \mathbf V\boldsymbol\Lambda$; multiply on the right by $\mathbf V^{-1}$. For powers, induct on $k$: $\mathbf A^{k+1} = \mathbf V\boldsymbol\Lambda^k\mathbf V^{-1}\mathbf V\boldsymbol\Lambda\mathbf V^{-1} = \mathbf V\boldsymbol\Lambda^{k+1}\mathbf V^{-1}$, and powers of a diagonal matrix are computed entrywise. $\blacksquare$
    ///

    A matrix of this form is called **diagonalizable**. In the coordinates given by the eigenvectors it acts on each coordinate separately, multiplying the $i$-th one by $\lambda_i$ at every step; so in $\mathbf x_k = \mathbf A^k\mathbf x_0$ a component dies out if $|\lambda_i| < 1$ and grows if $|\lambda_i| > 1$. This is why the eigenvalues of the matrix that propagates a filter's error decide whether old errors are forgotten. The cart matrix $\mathbf F$ is *not* diagonalizable, because any two of its eigenvectors are multiples of $\mathbf e_1$ and hence dependent. The next section shows that this cannot happen for symmetric matrices.

    Eigenvalues also describe rotations: [Chapter 17](ch17_rotations.md) shows that every 3-D rotation matrix has the eigenvalue $1$, and an eigenvector for it is the rotation axis.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Explore: a 2 × 2 matrix acting on the plane

    The sliders set the entries of $\mathbf A = \begin{bmatrix} a & b \\ c & d\end{bmatrix}$. The gray unit square and dashed unit circle are mapped to the blue parallelogram (spanned by the columns $\mathbf A\mathbf e_1$ and $\mathbf A\mathbf e_2$) and the orange ellipse. When the eigenvalues are real, the dotted black lines are the eigenvector directions, and each red arrow is $\mathbf A\mathbf v = \lambda\mathbf v$ for a unit eigenvector $\mathbf v$: it stays on its line. Things to try:

    - Set $b = c$. The eigenvector lines become perpendicular (the spectral theorem, next section) and lie along the axes of the ellipse.
    - Set $a = d = 0.7$, $b = -0.7$, $c = 0.7$ (a rotation by 45° with a slight shrink). The eigenvalues become complex and no direction is kept.
    - Set $a = d = 1$, $c = 0$, and $b \ne 0$ (the cart's shear). Only one eigenvector direction remains.
    - Make $\det\mathbf A < 0$. The parallelogram is flipped: the dot marking the image of the corner $(1, 1)$ is now on the other side of $\mathbf A\mathbf e_1$.
    - Set all four entries to $1$. Then $\det\mathbf A = 0$ and the plane collapses onto a line.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    eig_a = mo.ui.slider(-2.0, 2.0, 0.1, value=1.5, label=r"$a$", show_value=True)
    eig_b = mo.ui.slider(-2.0, 2.0, 0.1, value=0.5, label=r"$b$", show_value=True)
    eig_c = mo.ui.slider(-2.0, 2.0, 0.1, value=0.3, label=r"$c$", show_value=True)
    eig_d = mo.ui.slider(-2.0, 2.0, 0.1, value=1.0, label=r"$d$", show_value=True)
    return eig_a, eig_b, eig_c, eig_d


@app.cell(hide_code=True)
def _(eig_a, eig_b, eig_c, eig_d, graphic, mo, np, plt):
    _A = np.array([[eig_a.value, eig_b.value], [eig_c.value, eig_d.value]])
    _t = np.linspace(0.0, 2.0 * np.pi, 361)
    _circle = np.vstack([np.cos(_t), np.sin(_t)])
    _square = np.array([[0.0, 1.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 1.0, 0.0]])
    _img_circle = _A @ _circle
    _img_square = _A @ _square

    _fig, _ax = plt.subplots(figsize=(6, 6))
    _ax.fill(_square[0], _square[1], color="0.85", zorder=1, label="unit square")
    _ax.plot(_circle[0], _circle[1], color="0.55", linestyle="--", linewidth=1, label="unit circle")
    _ax.fill(_img_square[0], _img_square[1], color="C0", alpha=0.3, zorder=2, label="image of the square")
    _ax.plot(_img_circle[0], _img_circle[1], color="C1", linewidth=2, label="image of the circle")
    _ax.plot(_img_square[0, 2], _img_square[1, 2], "o", color="C0", zorder=4)
    for _j in range(2):
        _ax.annotate("", xy=_A[:, _j], xytext=(0.0, 0.0),
                     arrowprops=dict(arrowstyle="->", color="C0", lw=2), zorder=3)
        _ax.text(1.08 * _A[0, _j], 1.08 * _A[1, _j], rf"$\mathbf{{A}}\mathbf{{e}}_{_j + 1}$", color="C0")

    _tr = _A[0, 0] + _A[1, 1]
    _det = _A[0, 0] * _A[1, 1] - _A[0, 1] * _A[1, 0]
    _disc = (_tr / 2) ** 2 - _det
    if _disc >= 0:
        _vals, _vecs = np.linalg.eig(_A)
        _vals, _vecs = _vals.real, _vecs.real
        for _k in range(2):
            _v = _vecs[:, _k] / np.linalg.norm(_vecs[:, _k])
            _ax.plot([-6 * _v[0], 6 * _v[0]], [-6 * _v[1], 6 * _v[1]], color="k", linestyle=":",
                     linewidth=1.2, label="eigenvector directions" if _k == 0 else None)
            _ax.annotate("", xy=_vals[_k] * _v, xytext=(0.0, 0.0),
                         arrowprops=dict(arrowstyle="->", color="red", lw=1.5), zorder=5)
        _eig_text = rf"$\lambda_1 = {_vals[0]:.3f}$ and $\lambda_2 = {_vals[1]:.3f}$ (real)"
    else:
        _eig_text = rf"$\lambda = {_tr / 2:.3f} \pm {np.sqrt(-_disc):.3f}\,i$ (complex: no real eigenvector)"

    _ax.set_xlim(-4.5, 4.5)
    _ax.set_ylim(-4.5, 4.5)
    _ax.set_aspect("equal")
    _ax.set_xlabel(r"$x_1$")
    _ax.set_ylabel(r"$x_2$")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.legend(loc="upper left", fontsize=8)
    _ax.set_title(r"The unit square and circle under $\mathbf{A}$", style="italic")
    _plot = graphic(_fig)
    plt.close(_fig)

    _info = mo.md(
        rf"$\det\mathbf A = {_det:.3f}$ (signed area of the blue parallelogram), "
        rf"$\operatorname{{tr}}\mathbf A = {_tr:.3f}$, eigenvalues {_eig_text}."
    )
    mo.vstack([mo.hstack([eig_a, eig_b, eig_c, eig_d]), _plot, _info])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Symmetric and Positive Definite Matrices

    Covariance matrices ([Chapter 12](ch12_vectors_matrices_covariance.md)) have two special properties: they equal their own transpose, and the "variance in every direction" they assign is nonnegative. This section shows what these properties buy: perpendicular eigenvectors, real positive eigenvalues, and invertibility.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Symmetric matrix**</u>

    A square matrix $\mathbf A \in \mathbb R^{n\times n}$ is symmetric if $\mathbf A^\top = \mathbf A$, i.e. $a_{ij} = a_{ji}$ for all $i, j$.
    ///

    For any $\mathbf M \in \mathbb R^{m\times n}$, the matrices $\mathbf M^\top\mathbf M$ and $\mathbf M\mathbf M^\top$ are symmetric, because $(\mathbf M^\top\mathbf M)^\top = \mathbf M^\top(\mathbf M^\top)^\top = \mathbf M^\top\mathbf M$. Similarly, if $\mathbf P$ and $\mathbf Q$ are symmetric, so is the predicted covariance $\mathbf F\mathbf P\mathbf F^\top + \mathbf Q$. The inverse of an invertible symmetric matrix is symmetric: $(\mathbf A^{-1})^\top = (\mathbf A^\top)^{-1} = \mathbf A^{-1}$.

    /// important | 📐 **Theorem (Symmetric Matrices Have Real Eigenvalues)**
        attrs: {class: no-icon}
    Every eigenvalue $\lambda$ of a symmetric $\mathbf A \in \mathbb R^{n\times n}$ is real, and has a real eigenvector $\mathbf v \in \mathbb R^n$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Let $\mathbf A\mathbf v = \lambda\mathbf v$ with $\mathbf v \in \mathbb C^n$ nonzero, and put $s := \bar{\mathbf v}^\top\mathbf A\mathbf v \in \mathbb C$. Since $\mathbf A$ is real and symmetric, and a $1\times 1$ matrix equals its transpose,
    $$\bar s = \mathbf v^\top\mathbf A\bar{\mathbf v} = (\mathbf v^\top\mathbf A\bar{\mathbf v})^\top = \bar{\mathbf v}^\top\mathbf A^\top\mathbf v = \bar{\mathbf v}^\top\mathbf A\mathbf v = s,$$
    so $s$ is real. Also $s = \bar{\mathbf v}^\top(\lambda\mathbf v) = \lambda\,\bar{\mathbf v}^\top\mathbf v$, where $\bar{\mathbf v}^\top\mathbf v$ is real and positive. Hence $\lambda = s/(\bar{\mathbf v}^\top\mathbf v)$ is real. Then $\lambda\mathbf I - \mathbf A$ is a real matrix with determinant $0$, so by the Invertible Matrix Theorem over $\mathbb R$ some real $\mathbf w \ne \mathbf 0$ has $(\lambda\mathbf I - \mathbf A)\mathbf w = \mathbf 0$. $\blacksquare$
    ///

    /// important | 📐 **Lemma (Eigenvectors of Distinct Eigenvalues Are Orthogonal)**
        attrs: {class: no-icon}
    If $\mathbf A \in \mathbb R^{n\times n}$ is symmetric, $\mathbf A\mathbf u = \lambda\mathbf u$ and $\mathbf A\mathbf v = \mu\mathbf v$ with $\mathbf u, \mathbf v \in \mathbb R^n$ and $\lambda \ne \mu$, then $\mathbf u\cdot\mathbf v = 0$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    By the transpose rules, $\lambda\,(\mathbf u\cdot\mathbf v) = (\mathbf A\mathbf u)\cdot\mathbf v = \mathbf u\cdot(\mathbf A^\top\mathbf v) = \mathbf u\cdot(\mathbf A\mathbf v) = \mu\,(\mathbf u\cdot\mathbf v)$. So $(\lambda - \mu)(\mathbf u\cdot\mathbf v) = 0$, and $\lambda - \mu \ne 0$. $\blacksquare$
    ///

    To handle repeated eigenvalues as well, we need one tool: an orthogonal matrix with a prescribed first column.

    /// important | 📐 **Lemma (Householder Reflection)**
        attrs: {class: no-icon}
    For every unit vector $\mathbf q \in \mathbb R^n$ there is a symmetric orthogonal $\mathbf H \in \mathbb R^{n\times n}$ with $\mathbf H\mathbf e_1 = \mathbf q$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    If $\mathbf q = \mathbf e_1$, take $\mathbf H = \mathbf I$. Otherwise $\|\mathbf e_1 - \mathbf q\|^2 = \|\mathbf e_1\|^2 - 2\,\mathbf e_1\cdot\mathbf q + \|\mathbf q\|^2 = 2 - 2q_1 > 0$. Let $\mathbf u := (\mathbf e_1 - \mathbf q)/\|\mathbf e_1 - \mathbf q\|$ and $\mathbf H := \mathbf I - 2\mathbf u\mathbf u^\top$. Then $\mathbf H^\top = \mathbf H$, and since $\mathbf u^\top\mathbf u = 1$,
    $$\mathbf H^\top\mathbf H = \mathbf I - 4\mathbf u\mathbf u^\top + 4\mathbf u(\mathbf u^\top\mathbf u)\mathbf u^\top = \mathbf I.$$
    Finally, $\mathbf u^\top\mathbf e_1 = (1 - q_1)/\|\mathbf e_1 - \mathbf q\|$, so
    $$\mathbf H\mathbf e_1 = \mathbf e_1 - 2\mathbf u(\mathbf u^\top\mathbf e_1) = \mathbf e_1 - \frac{2(1 - q_1)}{2 - 2q_1}(\mathbf e_1 - \mathbf q) = \mathbf q. \qquad\blacksquare$$
    ///

    Geometrically, $\mathbf H$ is the mirror through the plane perpendicular to $\mathbf e_1 - \mathbf q$, which swaps $\mathbf e_1$ and $\mathbf q$.

    /// important | 📐 **Theorem (Spectral Theorem)**
        attrs: {class: no-icon}
    For every symmetric $\mathbf A \in \mathbb R^{n\times n}$ there are an orthogonal $\mathbf Q \in \mathbb R^{n\times n}$ and a real diagonal $\boldsymbol\Lambda = \operatorname{diag}(\lambda_1, \ldots, \lambda_n)$ with
    $$\mathbf A = \mathbf Q\boldsymbol\Lambda\mathbf Q^\top.$$
    The columns $\mathbf q_1, \ldots, \mathbf q_n$ of $\mathbf Q$ are orthonormal eigenvectors, $\mathbf A\mathbf q_i = \lambda_i\mathbf q_i$, and $\lambda_1, \ldots, \lambda_n$ are the eigenvalues of $\mathbf A$ listed with multiplicity.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Induction on $n$. For $n = 1$ take $\mathbf Q = [1]$ and $\boldsymbol\Lambda = \mathbf A$. Let $n \ge 2$. By the Corollary (Every Square Matrix Has an Eigenvalue) and the theorem on real eigenvalues, $\mathbf A$ has a real eigenvalue $\lambda_1$ with a real eigenvector, which we scale to a unit vector $\mathbf q_1$. Take $\mathbf H$ from the Householder lemma with $\mathbf H\mathbf e_1 = \mathbf q_1$, and let $\mathbf B := \mathbf H^\top\mathbf A\mathbf H$. Then $\mathbf B$ is symmetric, and its first column is
    $$\mathbf B\mathbf e_1 = \mathbf H^\top\mathbf A\mathbf q_1 = \lambda_1\mathbf H^\top\mathbf q_1 = \lambda_1\mathbf H^\top\mathbf H\mathbf e_1 = \lambda_1\mathbf e_1.$$
    By symmetry its first row is $\lambda_1\mathbf e_1^\top$, so $\mathbf B = \begin{bmatrix} \lambda_1 & \mathbf 0^\top \\ \mathbf 0 & \mathbf C\end{bmatrix}$ with $\mathbf C \in \mathbb R^{(n-1)\times(n-1)}$ symmetric. By the induction hypothesis, $\mathbf C = \mathbf Q_2\boldsymbol\Lambda_2\mathbf Q_2^\top$ with $\mathbf Q_2$ orthogonal and $\boldsymbol\Lambda_2$ real diagonal. Let $\mathbf U := \begin{bmatrix} 1 & \mathbf 0^\top \\ \mathbf 0 & \mathbf Q_2\end{bmatrix}$; block multiplication and the block transpose rule give $\mathbf U^\top\mathbf U = \mathbf I$ and
    $$\mathbf U^\top\mathbf B\mathbf U = \begin{bmatrix} \lambda_1 & \mathbf 0^\top \\ \mathbf 0 & \mathbf Q_2^\top\mathbf C\mathbf Q_2\end{bmatrix} = \begin{bmatrix} \lambda_1 & \mathbf 0^\top \\ \mathbf 0 & \boldsymbol\Lambda_2\end{bmatrix} =: \boldsymbol\Lambda.$$
    So $\mathbf Q := \mathbf H\mathbf U$ is orthogonal (a product of orthogonal matrices) and $\mathbf Q^\top\mathbf A\mathbf Q = \mathbf U^\top\mathbf B\mathbf U = \boldsymbol\Lambda$; multiplying by $\mathbf Q$ on the left and $\mathbf Q^\top$ on the right gives $\mathbf A = \mathbf Q\boldsymbol\Lambda\mathbf Q^\top$.

    Then $\mathbf A\mathbf Q = \mathbf Q\boldsymbol\Lambda$, whose $i$-th column reads $\mathbf A\mathbf q_i = \lambda_i\mathbf q_i$. Finally, $p_{\mathbf A}(\lambda) = \det\big(\mathbf Q(\lambda\mathbf I - \boldsymbol\Lambda)\mathbf Q^\top\big) = \det(\lambda\mathbf I - \boldsymbol\Lambda) = (\lambda - \lambda_1)\cdots(\lambda - \lambda_n)$, because $\det\mathbf Q\det\mathbf Q^\top = \det(\mathbf Q\mathbf Q^\top) = 1$. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Writing a product column-by-row, $\mathbf M\mathbf N = \sum_j \mathbf m_j\mathbf n_j^\top$, where $\mathbf m_j$ is the $j$-th column of $\mathbf M$ and $\mathbf n_j^\top$ the $j$-th row of $\mathbf N$ (compare entries: both are $\sum_j m_{ij}n_{jk}$). With $\mathbf M = \mathbf Q\boldsymbol\Lambda$ and $\mathbf N = \mathbf Q^\top$ this turns the spectral theorem into

    $$\mathbf A = \sum_{i=1}^n \lambda_i\,\mathbf q_i\mathbf q_i^\top,$$

    a sum of stretches by $\lambda_i$ along perpendicular directions $\mathbf q_i$. It also gives $\operatorname{tr}\mathbf A = \operatorname{tr}(\boldsymbol\Lambda\mathbf Q^\top\mathbf Q) = \lambda_1 + \cdots + \lambda_n$ and $\det\mathbf A = \det\boldsymbol\Lambda = \lambda_1\cdots\lambda_n$ without the characteristic polynomial.

    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    A symmetric matrix is a stretch along perpendicular axes: in the orthonormal coordinates given by its eigenvectors it is simply $\operatorname{diag}(\lambda_1, \ldots, \lambda_n)$.
    ///

    **Example ($2\times 2$ symmetric matrices).** For $\mathbf A = \begin{bmatrix} a & b \\ b & d\end{bmatrix}$, the characteristic polynomial $\lambda^2 - (a + d)\lambda + (ad - b^2)$ has discriminant $(a + d)^2 - 4(ad - b^2) = (a - d)^2 + 4b^2 \ge 0$, which confirms directly that both eigenvalues are real:

    $$\lambda_\pm = \frac{a + d}{2} \pm r, \qquad r := \sqrt{\Big(\frac{a - d}{2}\Big)^2 + b^2}.$$

    If $r > 0$, let $\varphi$ be half the polar angle of the point $\big(\tfrac{a - d}{2}, b\big)$, so that $\tfrac{a - d}{2} = r\cos 2\varphi$ and $b = r\sin 2\varphi$ (in code, `phi = 0.5 * np.arctan2(2 * b, a - d)`). Then

    $$\mathbf A = \frac{a + d}{2}\,\mathbf I + r\begin{bmatrix} \cos 2\varphi & \sin 2\varphi \\ \sin 2\varphi & -\cos 2\varphi\end{bmatrix},$$

    and the angle-difference formulas $\cos(2\varphi - \varphi) = \cos 2\varphi\cos\varphi + \sin 2\varphi\sin\varphi$ and $\sin(2\varphi - \varphi) = \sin 2\varphi\cos\varphi - \cos 2\varphi\sin\varphi$ give

    $$\mathbf A\begin{bmatrix} \cos\varphi \\ \sin\varphi\end{bmatrix} = \lambda_+\begin{bmatrix} \cos\varphi \\ \sin\varphi\end{bmatrix}, \qquad \mathbf A\begin{bmatrix} -\sin\varphi \\ \cos\varphi\end{bmatrix} = \lambda_-\begin{bmatrix} -\sin\varphi \\ \cos\varphi\end{bmatrix}.$$

    So $\mathbf Q = \mathbf R(\varphi)$: the eigenvectors are the perpendicular directions at angles $\varphi$ and $\varphi + 90°$. If $r = 0$, then $\mathbf A = a\mathbf I$ and every nonzero vector is an eigenvector. For $\boldsymbol\Sigma = \begin{bmatrix} 2 & 1 \\ 1 & 2\end{bmatrix}$: $r = 1$, $\varphi = 45°$, and $\lambda_\pm = 3, 1$, as found at the start of the previous section. [Chapter 12](ch12_vectors_matrices_covariance.md) draws confidence ellipses with exactly these axes.

    ### Positive definite matrices

    For a covariance matrix $\boldsymbol\Sigma$ and a direction $\mathbf w$, the number $\mathbf w^\top\boldsymbol\Sigma\mathbf w$ is the variance of the combination $\mathbf w^\top\mathbf x$ of the random entries ([Chapter 12](ch12_vectors_matrices_covariance.md)), so it can never be negative. Numbers of the form $\mathbf x^\top\mathbf A\mathbf x = \sum_{i,j}a_{ij}x_ix_j$ are called **quadratic forms**. For $\boldsymbol\Sigma = \begin{bmatrix} 2 & 1 \\ 1 & 2\end{bmatrix}$,
    $$\mathbf x^\top\boldsymbol\Sigma\mathbf x = 2x_1^2 + 2x_1x_2 + 2x_2^2 = x_1^2 + x_2^2 + (x_1 + x_2)^2 > 0 \quad\text{for } \mathbf x \ne \mathbf 0,$$
    whereas $\begin{bmatrix} 1 & 2 \\ 2 & 1\end{bmatrix}$ gives $1 - 4 + 1 = -2$ at $\mathbf x = (1, -1)$, so it cannot be a covariance matrix (it would need a correlation coefficient of $2$).

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Positive definite**</u>

    A symmetric matrix $\mathbf A \in \mathbb R^{n\times n}$ is positive definite if $\mathbf x^\top\mathbf A\mathbf x > 0$ for every nonzero $\mathbf x \in \mathbb R^n$.
    ///

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Positive semidefinite**</u>

    A symmetric matrix $\mathbf A \in \mathbb R^{n\times n}$ is positive semidefinite if $\mathbf x^\top\mathbf A\mathbf x \ge 0$ for every $\mathbf x \in \mathbb R^n$.
    ///

    In this book, positive (semi)definite matrices are symmetric by definition; some texts drop that requirement.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// important | 📐 **Theorem (Definiteness and Eigenvalues)**
        attrs: {class: no-icon}
    A symmetric $\mathbf A \in \mathbb R^{n\times n}$ is positive definite if and only if all its eigenvalues are $> 0$, and positive semidefinite if and only if all its eigenvalues are $\ge 0$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Write $\mathbf A = \mathbf Q\boldsymbol\Lambda\mathbf Q^\top$ (spectral theorem). For $\mathbf x \in \mathbb R^n$ put $\mathbf y := \mathbf Q^\top\mathbf x$; since $\mathbf Q^\top$ is invertible, $\mathbf y = \mathbf 0$ exactly when $\mathbf x = \mathbf 0$. Then
    $$\mathbf x^\top\mathbf A\mathbf x = (\mathbf Q^\top\mathbf x)^\top\boldsymbol\Lambda(\mathbf Q^\top\mathbf x) = \mathbf y^\top\boldsymbol\Lambda\mathbf y = \sum_{i=1}^n\lambda_iy_i^2.$$
    If every $\lambda_i > 0$ and $\mathbf x \ne \mathbf 0$, some $y_i \ne 0$ and the sum is positive. Conversely, $\mathbf x = \mathbf q_i$ gives $\mathbf q_i^\top\mathbf A\mathbf q_i = \lambda_i\,\mathbf q_i^\top\mathbf q_i = \lambda_i$, so positive definiteness forces $\lambda_i > 0$. The semidefinite case is identical with $\ge$. $\blacksquare$
    ///

    /// important | 📐 **Corollary (Consequences of Definiteness)**
        attrs: {class: no-icon}
    Let $\mathbf A = \mathbf Q\boldsymbol\Lambda\mathbf Q^\top$ be positive definite. Then $\det\mathbf A > 0$, so $\mathbf A$ is invertible; $\mathbf A^{-1} = \mathbf Q\boldsymbol\Lambda^{-1}\mathbf Q^\top$ is positive definite; and every diagonal entry $a_{ii} = \mathbf e_i^\top\mathbf A\mathbf e_i$ is positive. If $\mathbf A$ is only positive semidefinite, then $\det\mathbf A \ge 0$ and $a_{ii} \ge 0$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    $\det\mathbf A = \lambda_1\cdots\lambda_n$, and $(\mathbf Q\boldsymbol\Lambda\mathbf Q^\top)(\mathbf Q\boldsymbol\Lambda^{-1}\mathbf Q^\top) = \mathbf I$. The matrix $\mathbf Q\boldsymbol\Lambda^{-1}\mathbf Q^\top$ is symmetric, and the computation in the previous proof, with $1/\lambda_i > 0$ in place of $\lambda_i$, shows it is positive definite. The diagonal entries are quadratic forms at $\mathbf e_i \ne \mathbf 0$. $\blacksquare$
    ///

    /// important | 📐 **Lemma (Building Positive Definite Matrices)**
        attrs: {class: no-icon}
    1. If $\mathbf A \in \mathbb R^{n\times n}$ is positive semidefinite and $\mathbf M \in \mathbb R^{m\times n}$, then $\mathbf M\mathbf A\mathbf M^\top$ is positive semidefinite. In particular, $\mathbf M\mathbf M^\top$ is.
    2. If $\mathbf A$ is positive definite and $\mathbf C \in \mathbb R^{n\times n}$ is invertible, then $\mathbf C^\top\mathbf A\mathbf C$ is positive definite.
    3. If $\mathbf A$ is positive semidefinite and $\mathbf B$ is positive definite, then $\mathbf A + \mathbf B$ is positive definite; a sum of positive semidefinite matrices is positive semidefinite.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    All three matrices are symmetric by the transpose rules. (1) $\mathbf x^\top\mathbf M\mathbf A\mathbf M^\top\mathbf x = (\mathbf M^\top\mathbf x)^\top\mathbf A(\mathbf M^\top\mathbf x) \ge 0$; for $\mathbf M\mathbf M^\top$ take $\mathbf A = \mathbf I$. (2) For $\mathbf x \ne \mathbf 0$, $\mathbf C\mathbf x \ne \mathbf 0$ (Invertible Matrix Theorem), so $\mathbf x^\top\mathbf C^\top\mathbf A\mathbf C\mathbf x = (\mathbf C\mathbf x)^\top\mathbf A(\mathbf C\mathbf x) > 0$. (3) $\mathbf x^\top(\mathbf A + \mathbf B)\mathbf x = \mathbf x^\top\mathbf A\mathbf x + \mathbf x^\top\mathbf B\mathbf x$. $\blacksquare$
    ///

    **Why the Kalman gain always exists.** In [Chapter 13](ch13_kalman_filter.md), if $\mathbf P$ and $\mathbf Q$ are positive semidefinite, then so is the predicted covariance $\mathbf F\mathbf P\mathbf F^\top + \mathbf Q$ (parts 1 and 3). If moreover the measurement noise covariance $\mathbf R$ is positive definite, then the innovation covariance $\mathbf S = \mathbf H\mathbf P^-\mathbf H^\top + \mathbf R$ is positive definite (parts 1 and 3), hence invertible, so $\mathbf K = \mathbf P^-\mathbf H^\top\mathbf S^{-1}$ is defined. A perfect sensor ($\mathbf R$ only semidefinite) can make $\mathbf S$ singular.

    /// important | 📐 **Theorem (2 × 2 Test)**
        attrs: {class: no-icon}
    $\mathbf A = \begin{bmatrix} a & b \\ b & d\end{bmatrix}$ is positive definite if and only if $a > 0$ and $ad - b^2 > 0$. In particular, the covariance matrix $\begin{bmatrix} \sigma_x^2 & \rho\sigma_x\sigma_y \\ \rho\sigma_x\sigma_y & \sigma_y^2\end{bmatrix}$ with $\sigma_x, \sigma_y > 0$ is positive definite if and only if $|\rho| < 1$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    ($\Rightarrow$) $a = \mathbf e_1^\top\mathbf A\mathbf e_1 > 0$ and $ad - b^2 = \det\mathbf A > 0$ by the previous corollary. ($\Leftarrow$) $\lambda_1\lambda_2 = \det\mathbf A > 0$, so the eigenvalues have the same sign. From $ad > b^2 \ge 0$ and $a > 0$ we get $d > 0$, so $\lambda_1 + \lambda_2 = \operatorname{tr}\mathbf A = a + d > 0$. Hence both are positive. For the covariance matrix, $a = \sigma_x^2 > 0$ and $\det = \sigma_x^2\sigma_y^2(1 - \rho^2)$. $\blacksquare$
    ///

    For $n\times n$ matrices the analogous test is Sylvester's criterion: $\mathbf A$ is positive definite if and only if the determinants of its upper-left $k\times k$ submatrices are positive for $k = 1, \ldots, n$ ([Wikipedia: Sylvester's criterion](https://en.wikipedia.org/wiki/Sylvester%27s_criterion)). In practice, the Cholesky algorithm of the next section is the fastest test.

    ### Matrix square roots

    If $\mathbf A = \mathbf Q\boldsymbol\Lambda\mathbf Q^\top$ is positive semidefinite, then $\mathbf A^{1/2} := \mathbf Q\operatorname{diag}(\sqrt{\lambda_1}, \ldots, \sqrt{\lambda_n})\mathbf Q^\top$ is symmetric, positive semidefinite (its eigenvalues are $\sqrt{\lambda_i} \ge 0$), and satisfies $\mathbf A^{1/2}\mathbf A^{1/2} = \mathbf Q\boldsymbol\Lambda\mathbf Q^\top = \mathbf A$. It does not depend on which spectral decomposition is used, because $\mathbf A$ has exactly one positive semidefinite square root ([Wikipedia: Square root of a matrix](https://en.wikipedia.org/wiki/Square_root_of_a_matrix)). Filtering uses the word "square root" more loosely: *any* $\mathbf S$ with $\mathbf S\mathbf S^\top = \mathbf A$ will do, for example to scale sigma points ([Chapter 16](ch16_unscented_kalman_filter.md)). $\mathbf A^{1/2}$ is one such $\mathbf S$; the next section builds a cheaper, triangular one.

    /// caution | ⚠️ **Assumptions and Failure Modes**
        attrs: {class: no-icon}
    - **Symmetry is essential.** $\begin{bmatrix} 1 & 4 \\ 0 & 1\end{bmatrix}$ has both eigenvalues equal to $1$, yet $\mathbf x = (1, -1)$ gives $\mathbf x^\top\mathbf A\mathbf x = -2$. A quadratic form only sees the symmetric part $\tfrac12(\mathbf A + \mathbf A^\top) = \begin{bmatrix} 1 & 2 \\ 2 & 1\end{bmatrix}$, whose eigenvalues are $3$ and $-1$. Without symmetry the spectral theorem also fails: the cart matrix $\mathbf F$ is not even diagonalizable.
    - **Rounding.** A covariance matrix computed in floating point can become slightly non-symmetric or even acquire a tiny negative eigenvalue. Filters guard against this by symmetrizing, $\mathbf P \leftarrow \tfrac12(\mathbf P + \mathbf P^\top)$, and by update formulas that preserve definiteness ([Chapter 13](ch13_kalman_filter.md), [Chapter 14](ch14_kalman_filters_in_practice.md)).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cholesky Decomposition

    To simulate two correlated sensor errors with standard deviations $\sigma_x, \sigma_y$ and correlation coefficient $\rho$, start from two uncorrelated noises $w_1, w_2$ with variance $1$ and mix them:

    $$\begin{bmatrix} x \\ y\end{bmatrix} = \underbrace{\begin{bmatrix} \sigma_x & 0 \\ \rho\sigma_y & \sigma_y\sqrt{1 - \rho^2}\end{bmatrix}}_{\mathbf L}\begin{bmatrix} w_1 \\ w_2\end{bmatrix}.$$

    [Chapter 12](ch12_vectors_matrices_covariance.md) shows that $\mathbf L\mathbf w$ has covariance matrix $\mathbf L\mathbf L^\top$, and multiplying out,

    $$\mathbf L\mathbf L^\top = \begin{bmatrix} \sigma_x^2 & \rho\sigma_x\sigma_y \\ \rho\sigma_x\sigma_y & \rho^2\sigma_y^2 + \sigma_y^2(1 - \rho^2)\end{bmatrix} = \begin{bmatrix} \sigma_x^2 & \rho\sigma_x\sigma_y \\ \rho\sigma_x\sigma_y & \sigma_y^2\end{bmatrix},$$

    exactly the covariance we wanted. For $|\rho| < 1$, the factor $\mathbf L$ is lower triangular with positive diagonal entries. Every positive definite matrix has exactly one factor of this kind.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Cholesky decomposition**</u>

    The Cholesky decomposition of a positive definite matrix $\mathbf A \in \mathbb R^{n\times n}$ is the factorization $\mathbf A = \mathbf L\mathbf L^\top$ in which $\mathbf L \in \mathbb R^{n\times n}$ is lower triangular with positive diagonal entries. The matrix $\mathbf L$ is the Cholesky factor of $\mathbf A$.
    ///

    /// important | 📐 **Theorem (Existence and Uniqueness of the Cholesky Factor)**
        attrs: {class: no-icon}
    A symmetric matrix $\mathbf A \in \mathbb R^{n\times n}$ is positive definite if and only if $\mathbf A = \mathbf L\mathbf L^\top$ for some lower triangular $\mathbf L$ with positive diagonal entries. This $\mathbf L$ is unique.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    ($\Leftarrow$) $\det\mathbf L = l_{11}\cdots l_{nn} > 0$, so $\mathbf L^\top$ is invertible, and $\mathbf L\mathbf L^\top = (\mathbf L^\top)^\top\mathbf I\,\mathbf L^\top$ is positive definite by part 2 of the Lemma (Building Positive Definite Matrices).

    ($\Rightarrow$, with uniqueness) Induction on $n$. For $n = 1$, $\mathbf A = [a]$ with $a = \mathbf e_1^\top\mathbf A\mathbf e_1 > 0$, and $l^2 = a$, $l > 0$ holds exactly for $l = \sqrt a$. Let $n \ge 2$ and partition
    $$\mathbf A = \begin{bmatrix} a & \mathbf b^\top \\ \mathbf b & \mathbf C\end{bmatrix}, \qquad \mathbf L = \begin{bmatrix} l & \mathbf 0^\top \\ \mathbf l & \mathbf M\end{bmatrix},$$
    with $a, l \in \mathbb R$, $\mathbf b, \mathbf l \in \mathbb R^{n-1}$, and $\mathbf C, \mathbf M \in \mathbb R^{(n-1)\times(n-1)}$; every lower triangular $\mathbf L$ with positive diagonal has this form with $l > 0$ and $\mathbf M$ lower triangular with positive diagonal. By block multiplication,
    $$\mathbf L\mathbf L^\top = \begin{bmatrix} l^2 & l\,\mathbf l^\top \\ l\,\mathbf l & \mathbf l\mathbf l^\top + \mathbf M\mathbf M^\top\end{bmatrix},$$
    so $\mathbf A = \mathbf L\mathbf L^\top$ holds if and only if $l^2 = a$, $l\,\mathbf l = \mathbf b$, and $\mathbf M\mathbf M^\top = \mathbf C - \mathbf l\mathbf l^\top$. Since $a > 0$, these force $l = \sqrt a$ and $\mathbf l = \mathbf b/\sqrt a$, and leave
    $$\mathbf M\mathbf M^\top = \mathbf A' := \mathbf C - \frac{\mathbf b\mathbf b^\top}{a}.$$
    $\mathbf A'$ is symmetric. It is positive definite: for $\mathbf y \ne \mathbf 0$ in $\mathbb R^{n-1}$, let $\mathbf x := (-\mathbf b^\top\mathbf y/a,\ \mathbf y) \ne \mathbf 0$; block multiplication gives
    $$0 < \mathbf x^\top\mathbf A\mathbf x = a\,x_1^2 + 2x_1\,\mathbf b^\top\mathbf y + \mathbf y^\top\mathbf C\mathbf y = \frac{(\mathbf b^\top\mathbf y)^2}{a} - \frac{2(\mathbf b^\top\mathbf y)^2}{a} + \mathbf y^\top\mathbf C\mathbf y = \mathbf y^\top\mathbf A'\mathbf y.$$
    By the induction hypothesis there is exactly one admissible $\mathbf M$, hence exactly one $\mathbf L$. $\blacksquare$
    ///

    The matrix $\mathbf A'$ is the Schur complement of $a$ in $\mathbf A$ (see the next section): Cholesky's algorithm repeatedly takes Schur complements.

    ### The algorithm

    Unrolling the induction gives explicit formulas. For $i \ge j$, entry $(i, j)$ of $\mathbf L\mathbf L^\top$ is $\sum_k l_{ik}l_{jk}$, and $l_{jk} = 0$ for $k > j$, so $\mathbf A = \mathbf L\mathbf L^\top$ says $a_{ij} = \sum_{k=1}^{j}l_{ik}l_{jk}$. Solving for the term $k = j$, column by column for $j = 1, \ldots, n$:

    $$l_{jj} = \sqrt{a_{jj} - \sum_{k<j}l_{jk}^2}, \qquad l_{ij} = \frac{1}{l_{jj}}\Big(a_{ij} - \sum_{k<j}l_{ik}l_{jk}\Big) \quad (i > j).$$

    Each right-hand side uses only entries already computed. If $\mathbf A$ is positive definite, its Cholesky factor exists and satisfies these equations, so the algorithm reproduces it, and each radicand equals $l_{jj}^2 > 0$. Conversely, if some radicand is $\le 0$, no Cholesky factor exists and $\mathbf A$ is not positive definite. This makes the algorithm the cheapest practical test of positive definiteness; it takes about $n^3/6$ multiplications and additions each. It reads only the lower triangle of $\mathbf A$, so apply it only to symmetric matrices.
    """)
    return


@app.cell
def _(np):
    # jb: echo=true
    def cholesky(A):
        """Lower-triangular L with positive diagonal such that L @ L.T == A.

        Raises ValueError if the symmetric matrix A is not positive definite.
        """
        A = np.asarray(A, dtype=float)
        n = A.shape[0]
        L = np.zeros((n, n))
        for j in range(n):
            radicand = A[j, j] - L[j, :j] @ L[j, :j]
            if radicand <= 0:
                raise ValueError("matrix is not positive definite")
            L[j, j] = np.sqrt(radicand)
            for i in range(j + 1, n):
                L[i, j] = (A[i, j] - L[i, :j] @ L[j, :j]) / L[j, j]
        return L

    return (cholesky,)


@app.cell
def _(cholesky, mo, np):
    # jb: echo=true
    A_chol = np.array([[4.0, 2.0, -2.0],
                       [2.0, 10.0, 2.0],
                       [-2.0, 2.0, 6.0]])
    L_chol = cholesky(A_chol)

    try:
        cholesky([[1.0, 2.0], [2.0, 1.0]])
        indefinite_result = "accepted (unexpected)"
    except ValueError as err:
        indefinite_result = f"rejected: {err}"

    mo.plain_text(
        f"L =\n{L_chol}\n"
        f"L @ L.T == A:                {np.allclose(L_chol @ L_chol.T, A_chol)}\n"
        f"agrees with numpy:           {np.allclose(L_chol, np.linalg.cholesky(A_chol))}\n"
        f"det A = (l11 l22 l33)^2:     {np.prod(np.diag(L_chol)) ** 2:.1f}\n"
        f"[[1, 2], [2, 1]] is {indefinite_result}"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The exact factor of the $3\times 3$ example is $\mathbf L = \begin{bmatrix} 2 & 0 & 0 \\ 1 & 3 & 0 \\ -1 & 1 & 2\end{bmatrix}$, so $\det\mathbf A = (\det\mathbf L)^2 = (2\cdot 3\cdot 2)^2 = 144$, as computed under Determinants. Once $\mathbf L$ is known, a system $\mathbf A\mathbf x = \mathbf b$ is solved by two triangular solves, $\mathbf L\mathbf y = \mathbf b$ and then $\mathbf L^\top\mathbf x = \mathbf y$, each of which is just substitution from the top (or bottom) row.

    ### Square roots and ellipses

    The Cholesky factor and the symmetric square root $\mathbf A^{1/2}$ are different matrices with the same "square" $\mathbf S\mathbf S^\top = \mathbf A$. What they share is the ellipse they draw.

    /// important | 📐 **Lemma (Square Roots Map the Unit Sphere onto the Same Ellipsoid)**
        attrs: {class: no-icon}
    Let $\mathbf A \in \mathbb R^{n\times n}$ be positive definite and $\mathbf S \in \mathbb R^{n\times n}$ satisfy $\mathbf S\mathbf S^\top = \mathbf A$. Then $\mathbf S$ is invertible, and $\mathbf x \mapsto \mathbf S\mathbf x$ maps the unit sphere $\{\mathbf x : \|\mathbf x\| = 1\}$ onto the ellipsoid $E_{\mathbf A} := \{\mathbf y : \mathbf y^\top\mathbf A^{-1}\mathbf y = 1\}$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    $(\det\mathbf S)^2 = \det\mathbf S\det\mathbf S^\top = \det\mathbf A > 0$, so $\mathbf S$ is invertible, and $\mathbf A^{-1} = (\mathbf S\mathbf S^\top)^{-1} = \mathbf S^{-\top}\mathbf S^{-1}$. For $\mathbf y = \mathbf S\mathbf x$,
    $$\mathbf y^\top\mathbf A^{-1}\mathbf y = \mathbf x^\top\mathbf S^\top\mathbf S^{-\top}\mathbf S^{-1}\mathbf S\mathbf x = \|\mathbf x\|^2,$$
    so unit vectors land on $E_{\mathbf A}$; and every $\mathbf y \in E_{\mathbf A}$ is $\mathbf S(\mathbf S^{-1}\mathbf y)$ with $\|\mathbf S^{-1}\mathbf y\|^2 = \mathbf y^\top\mathbf A^{-1}\mathbf y = 1$. $\blacksquare$
    ///

    In the eigenvector coordinates $\mathbf z = \mathbf Q^\top\mathbf y$ of $\mathbf A = \mathbf Q\boldsymbol\Lambda\mathbf Q^\top$, the equation of $E_{\mathbf A}$ reads $\sum_i z_i^2/\lambda_i = 1$: an ellipse (for $n = 2$) with semi-axes $\sqrt{\lambda_i}$ along the eigenvectors. When $\mathbf A$ is a covariance matrix, $E_{\mathbf A}$ is the one-standard-deviation {term}`confidence ellipse` of [Chapter 12](ch12_vectors_matrices_covariance.md). The unscented transform of [Chapter 16](ch16_unscented_kalman_filter.md) places its sigma points at the mean plus and minus (scaled) columns of a square root $\mathbf S$; by the lemma, those points lie on this ellipse whichever square root is used.

    ### Explore: two square roots, one ellipse

    The sliders set a $2\times 2$ covariance matrix $\mathbf A$. The red arrows are the columns of the Cholesky factor $\mathbf L$ (images of $\mathbf e_1, \mathbf e_2$), and the blue arrows are the columns of $\mathbf A^{1/2}$. Both maps carry the dashed unit circle onto the same orange ellipse, but they send $\mathbf e_1$ and $\mathbf e_2$ to different points on it. The gray dots are $300$ samples $\mathbf L\mathbf w$, where $\mathbf w$ has two independent standard normal entries;[^normal-informal] they spread out in the shape of the ellipse. As $|\rho| \to 1$, the ellipse collapses toward a line and the second diagonal entry $\sigma_y\sqrt{1 - \rho^2}$ of $\mathbf L$ goes to $0$.

    [^normal-informal]: Standard normal random variables are defined in [Chapter 5](ch5_random_variables.md); here they only produce a cloud whose covariance is $\mathbf A$ ([Chapter 12](ch12_vectors_matrices_covariance.md)).
    """)
    return


@app.cell
def _(np):
    # jb: include=false
    chol_samples_w = np.random.default_rng(12).standard_normal((2, 300))
    return (chol_samples_w,)


@app.cell(hide_code=True)
def _(mo):
    chol_sx = mo.ui.slider(0.2, 2.0, 0.05, value=1.5, label=r"$\sigma_x$", show_value=True)
    chol_sy = mo.ui.slider(0.2, 2.0, 0.05, value=1.0, label=r"$\sigma_y$", show_value=True)
    chol_rho = mo.ui.slider(-0.95, 0.95, 0.05, value=0.6, label=r"$\rho$", show_value=True)
    return chol_rho, chol_sx, chol_sy


@app.cell(hide_code=True)
def _(chol_rho, chol_samples_w, chol_sx, chol_sy, cholesky, graphic, mo, np, plt):
    _sx, _sy, _rho = chol_sx.value, chol_sy.value, chol_rho.value
    _A = np.array([[_sx**2, _rho * _sx * _sy], [_rho * _sx * _sy, _sy**2]])
    _L = cholesky(_A)
    _lam, _Q = np.linalg.eigh(_A)
    _root = _Q @ np.diag(np.sqrt(_lam)) @ _Q.T

    _t = np.linspace(0.0, 2.0 * np.pi, 361)
    _circle = np.vstack([np.cos(_t), np.sin(_t)])
    _cloud = _L @ chol_samples_w

    _fig, _ax = plt.subplots(figsize=(6, 6))
    _ax.scatter(_cloud[0], _cloud[1], s=6, color="0.6", alpha=0.6, label=r"samples $\mathbf{L}\mathbf{w}$")
    _ax.plot(_circle[0], _circle[1], color="0.55", linestyle="--", linewidth=1, label="unit circle")
    _ax.plot(*(_L @ _circle), color="C1", linewidth=3, label=r"image under $\mathbf{L}$")
    _ax.plot(*(_root @ _circle), color="k", linestyle=":", linewidth=1.5, label=r"image under $\mathbf{A}^{1/2}$")
    for _j in range(2):
        _ax.annotate("", xy=_L[:, _j], xytext=(0.0, 0.0),
                     arrowprops=dict(arrowstyle="->", color="red", lw=2))
        _ax.annotate("", xy=_root[:, _j], xytext=(0.0, 0.0),
                     arrowprops=dict(arrowstyle="->", color="C0", lw=2))
        _ax.text(*(1.1 * _L[:, _j]), rf"$\mathbf{{L}}\mathbf{{e}}_{_j + 1}$", color="red")
        _ax.text(*(1.1 * _root[:, _j]), rf"$\mathbf{{A}}^{{1/2}}\mathbf{{e}}_{_j + 1}$", color="C0")
    _ax.set_xlim(-4.5, 4.5)
    _ax.set_ylim(-4.5, 4.5)
    _ax.set_aspect("equal")
    _ax.set_xlabel(r"$x$ (units of $\sigma$)")
    _ax.set_ylabel(r"$y$ (units of $\sigma$)")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.legend(loc="upper left", fontsize=8)
    _ax.set_title("Cholesky factor and symmetric square root", style="italic")
    _plot = graphic(_fig)
    plt.close(_fig)

    _info = mo.md(
        rf"$\mathbf L = \begin{{bmatrix}} {_L[0, 0]:.3f} & 0 \\ {_L[1, 0]:.3f} & {_L[1, 1]:.3f} \end{{bmatrix}}$, "
        rf"$\quad\mathbf A^{{1/2}} = \begin{{bmatrix}} {_root[0, 0]:.3f} & {_root[0, 1]:.3f} \\ {_root[1, 0]:.3f} & {_root[1, 1]:.3f} \end{{bmatrix}}$, "
        rf"$\quad\mathbf L\mathbf L^\top = \mathbf A^{{1/2}}\mathbf A^{{1/2}} = \mathbf A$ up to rounding: "
        rf"{np.allclose(_L @ _L.T, _A) and np.allclose(_root @ _root, _A)}."
    )
    mo.vstack([mo.hstack([chol_sx, chol_sy, chol_rho]), _plot, _info])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
        attrs: {class: no-icon}
    - **Positive definiteness is required.** A singular positive semidefinite matrix (for example a covariance with $|\rho| = 1$, or with a state that is known exactly) produces a zero radicand, and the plain algorithm divides by zero. Variants with pivoting handle the semidefinite case.
    - **Rounding can break it.** A covariance matrix that should be positive definite but has a tiny negative eigenvalue after rounding makes the algorithm fail. This is a common way for an unscented Kalman filter to crash ([Chapter 16](ch16_unscented_kalman_filter.md)), and a reason to symmetrize and to use numerically careful updates ([Chapter 14](ch14_kalman_filters_in_practice.md)).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Block Matrices and the Schur Complement

    Under Matrix Multiplication we multiplied block matrices; here we invert them. The motivating example is the scalar Kalman update in disguise. Treat the true weight $x$ as random with variance $P^-$ about the prediction (the Bayesian view of [Chapter 8](ch8_bayesian_view.md)), and let $z = x + v$ with measurement noise $v$ of variance $R$, uncorrelated with $x$. Then the pair $(x, z)$ has covariance matrix ([Chapter 12](ch12_vectors_matrices_covariance.md))

    $$\boldsymbol\Sigma = \begin{bmatrix} P^- & P^- \\ P^- & P^- + R\end{bmatrix}.$$

    The number "top-left entry minus off-diagonal times (bottom-right)$^{-1}$ times off-diagonal",

    $$P^- - P^-(P^- + R)^{-1}P^- = \frac{P^-R}{P^- + R},$$

    is exactly the updated error variance of [Chapter 7](ch7_optimal_alpha.md). [Chapter 12](ch12_vectors_matrices_covariance.md) proves that it is the variance of $x$ once $z$ is known. For matrices, this number becomes the Schur complement.

    Throughout this section, $\mathbf M = \begin{bmatrix} \mathbf A & \mathbf B \\ \mathbf C & \mathbf D\end{bmatrix}$ with square blocks $\mathbf A \in \mathbb R^{p\times p}$ and $\mathbf D \in \mathbb R^{q\times q}$ (so $\mathbf B \in \mathbb R^{p\times q}$ and $\mathbf C \in \mathbb R^{q\times p}$), and $\mathbf I$ and $\mathbf 0$ denote identity and zero blocks of the appropriate sizes.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Schur complement**</u>

    Let $\mathbf M = \begin{bmatrix} \mathbf A & \mathbf B \\ \mathbf C & \mathbf D\end{bmatrix}$ be a block matrix with square diagonal blocks $\mathbf A$ and $\mathbf D$. If $\mathbf A$ is invertible, the Schur complement of $\mathbf A$ in $\mathbf M$ is $\mathbf M/\mathbf A := \mathbf D - \mathbf C\mathbf A^{-1}\mathbf B$. If $\mathbf D$ is invertible, the Schur complement of $\mathbf D$ in $\mathbf M$ is $\mathbf M/\mathbf D := \mathbf A - \mathbf B\mathbf D^{-1}\mathbf C$.
    ///

    In the example, $\boldsymbol\Sigma/(P^- + R) = P^-R/(P^- + R)$. For the general $2\times 2$ covariance matrix with standard deviations $\sigma_x, \sigma_y$ and correlation $\rho$, the Schur complement of $\sigma_y^2$ is $\sigma_x^2 - \rho^2\sigma_x^2\sigma_y^2/\sigma_y^2 = \sigma_x^2(1 - \rho^2)$: knowing $y$ shrinks the variance of $x$ by the factor $1 - \rho^2$.

    /// important | 📐 **Lemma (Unit Block-Triangular Matrices)**
        attrs: {class: no-icon}
    For all $\mathbf X \in \mathbb R^{q\times p}$ and $\mathbf Y \in \mathbb R^{p\times q}$, the matrices $\begin{bmatrix} \mathbf I & \mathbf 0 \\ \mathbf X & \mathbf I\end{bmatrix}$ and $\begin{bmatrix} \mathbf I & \mathbf Y \\ \mathbf 0 & \mathbf I\end{bmatrix}$ have determinant $1$ and inverses $\begin{bmatrix} \mathbf I & \mathbf 0 \\ -\mathbf X & \mathbf I\end{bmatrix}$ and $\begin{bmatrix} \mathbf I & -\mathbf Y \\ \mathbf 0 & \mathbf I\end{bmatrix}$. Also, $\det\begin{bmatrix} \mathbf A & \mathbf 0 \\ \mathbf 0 & \mathbf D\end{bmatrix} = \det\mathbf A\,\det\mathbf D$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    The first matrix is lower triangular with ones on the diagonal and the second is upper triangular with ones on the diagonal, so both determinants are $1$ (Lemma (Triangular Determinants) and Corollary (Consequences), part 4). Block multiplication gives $\begin{bmatrix} \mathbf I & \mathbf 0 \\ \mathbf X & \mathbf I\end{bmatrix}\begin{bmatrix} \mathbf I & \mathbf 0 \\ -\mathbf X & \mathbf I\end{bmatrix} = \begin{bmatrix} \mathbf I & \mathbf 0 \\ \mathbf X - \mathbf X & \mathbf I\end{bmatrix} = \mathbf I$, and similarly for the other products. For the block-diagonal matrix, block multiplication gives $\begin{bmatrix} \mathbf A & \mathbf 0 \\ \mathbf 0 & \mathbf D\end{bmatrix} = \begin{bmatrix} \mathbf A & \mathbf 0 \\ \mathbf 0 & \mathbf I_q\end{bmatrix}\begin{bmatrix} \mathbf I_p & \mathbf 0 \\ \mathbf 0 & \mathbf D\end{bmatrix}$. Expanding the second factor along its first row (whose only nonzero entry is the $1$ in position $(1, 1)$) removes one row and column of $\mathbf I_p$; after $p$ steps we get $\det\mathbf D$. Expanding the first factor along its last row (property 3) likewise gives $\det\mathbf A$. Now use property 2. $\blacksquare$
    ///

    /// important | 📐 **Theorem (Block Inverse via the Schur Complement)**
        attrs: {class: no-icon}
    Suppose $\mathbf A$ is invertible and let $\mathbf S := \mathbf M/\mathbf A = \mathbf D - \mathbf C\mathbf A^{-1}\mathbf B$. Then
    $$\mathbf M = \begin{bmatrix} \mathbf I & \mathbf 0 \\ \mathbf C\mathbf A^{-1} & \mathbf I\end{bmatrix}\begin{bmatrix} \mathbf A & \mathbf 0 \\ \mathbf 0 & \mathbf S\end{bmatrix}\begin{bmatrix} \mathbf I & \mathbf A^{-1}\mathbf B \\ \mathbf 0 & \mathbf I\end{bmatrix}$$
    and $\det\mathbf M = \det\mathbf A\,\det\mathbf S$. Hence $\mathbf M$ is invertible if and only if $\mathbf S$ is, and then
    $$\mathbf M^{-1} = \begin{bmatrix} \mathbf A^{-1} + \mathbf A^{-1}\mathbf B\mathbf S^{-1}\mathbf C\mathbf A^{-1} & -\mathbf A^{-1}\mathbf B\mathbf S^{-1} \\ -\mathbf S^{-1}\mathbf C\mathbf A^{-1} & \mathbf S^{-1}\end{bmatrix}.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Block multiplication: the last two factors multiply to $\begin{bmatrix} \mathbf A & \mathbf B \\ \mathbf 0 & \mathbf S\end{bmatrix}$, and multiplying by the first factor gives $\begin{bmatrix} \mathbf A & \mathbf B \\ \mathbf C\mathbf A^{-1}\mathbf A & \mathbf C\mathbf A^{-1}\mathbf B + \mathbf S\end{bmatrix} = \mathbf M$. By the lemma and property 2 of the determinant, $\det\mathbf M = 1\cdot\det\mathbf A\det\mathbf S\cdot 1$, and since $\det\mathbf A \ne 0$, $\det\mathbf M \ne 0 \iff \det\mathbf S \ne 0$ (property 5). If $\mathbf S$ is invertible, the middle factor has inverse $\begin{bmatrix} \mathbf A^{-1} & \mathbf 0 \\ \mathbf 0 & \mathbf S^{-1}\end{bmatrix}$, and by the inverse rules
    $$\mathbf M^{-1} = \begin{bmatrix} \mathbf I & -\mathbf A^{-1}\mathbf B \\ \mathbf 0 & \mathbf I\end{bmatrix}\begin{bmatrix} \mathbf A^{-1} & \mathbf 0 \\ \mathbf 0 & \mathbf S^{-1}\end{bmatrix}\begin{bmatrix} \mathbf I & \mathbf 0 \\ -\mathbf C\mathbf A^{-1} & \mathbf I\end{bmatrix},$$
    which multiplies out to the stated formula. $\blacksquare$
    ///

    /// important | 📐 **Corollary (Using the Other Schur Complement)**
        attrs: {class: no-icon}
    If $\mathbf D$ and $\mathbf T := \mathbf M/\mathbf D = \mathbf A - \mathbf B\mathbf D^{-1}\mathbf C$ are invertible, then $\mathbf M$ is invertible and
    $$\mathbf M^{-1} = \begin{bmatrix} \mathbf T^{-1} & -\mathbf T^{-1}\mathbf B\mathbf D^{-1} \\ -\mathbf D^{-1}\mathbf C\mathbf T^{-1} & \mathbf D^{-1} + \mathbf D^{-1}\mathbf C\mathbf T^{-1}\mathbf B\mathbf D^{-1}\end{bmatrix}.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Multiply $\mathbf M$ by the claimed inverse, block by block. Top left: $\mathbf A\mathbf T^{-1} - \mathbf B\mathbf D^{-1}\mathbf C\mathbf T^{-1} = \mathbf T\mathbf T^{-1} = \mathbf I$. Top right: $-\mathbf A\mathbf T^{-1}\mathbf B\mathbf D^{-1} + \mathbf B\mathbf D^{-1} + \mathbf B\mathbf D^{-1}\mathbf C\mathbf T^{-1}\mathbf B\mathbf D^{-1} = -\mathbf T\mathbf T^{-1}\mathbf B\mathbf D^{-1} + \mathbf B\mathbf D^{-1} = \mathbf 0$. Bottom left: $\mathbf C\mathbf T^{-1} - \mathbf D\mathbf D^{-1}\mathbf C\mathbf T^{-1} = \mathbf 0$. Bottom right: $-\mathbf C\mathbf T^{-1}\mathbf B\mathbf D^{-1} + \mathbf I + \mathbf C\mathbf T^{-1}\mathbf B\mathbf D^{-1} = \mathbf I$. A one-sided inverse of a square matrix is its inverse (Invertible Matrix Theorem). $\blacksquare$
    ///

    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    The bottom-right block of $\mathbf M^{-1}$ is $(\mathbf M/\mathbf A)^{-1}$ and the top-left block is $(\mathbf M/\mathbf D)^{-1}$. Taking a Schur complement is what "eliminating" a block of variables does to a matrix; in [Chapter 12](ch12_vectors_matrices_covariance.md), conditioning a Gaussian on some of its entries leaves a Schur complement as the new covariance.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The matrix inversion lemma

    /// important | 📐 **Theorem (Matrix Inversion Lemma)**
        attrs: {class: no-icon}
    Let $\mathbf A \in \mathbb R^{n\times n}$ and $\mathbf C \in \mathbb R^{k\times k}$ be invertible, $\mathbf U \in \mathbb R^{n\times k}$, and $\mathbf V \in \mathbb R^{k\times n}$. If $\mathbf W := \mathbf C^{-1} + \mathbf V\mathbf A^{-1}\mathbf U$ is invertible, then $\mathbf A + \mathbf U\mathbf C\mathbf V$ is invertible and
    $$(\mathbf A + \mathbf U\mathbf C\mathbf V)^{-1} = \mathbf A^{-1} - \mathbf A^{-1}\mathbf U\,\mathbf W^{-1}\mathbf V\mathbf A^{-1}.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Multiply, using $\mathbf U + \mathbf U\mathbf C\mathbf V\mathbf A^{-1}\mathbf U = \mathbf U\mathbf C(\mathbf C^{-1} + \mathbf V\mathbf A^{-1}\mathbf U) = \mathbf U\mathbf C\mathbf W$:
    $$\begin{aligned}
    (\mathbf A + \mathbf U\mathbf C\mathbf V)(\mathbf A^{-1} - \mathbf A^{-1}\mathbf U\mathbf W^{-1}\mathbf V\mathbf A^{-1})
    &= \mathbf I + \mathbf U\mathbf C\mathbf V\mathbf A^{-1} - (\mathbf U + \mathbf U\mathbf C\mathbf V\mathbf A^{-1}\mathbf U)\mathbf W^{-1}\mathbf V\mathbf A^{-1} \\
    &= \mathbf I + \mathbf U\mathbf C\mathbf V\mathbf A^{-1} - \mathbf U\mathbf C\mathbf W\mathbf W^{-1}\mathbf V\mathbf A^{-1} = \mathbf I.
    \end{aligned}$$
    A one-sided inverse of a square matrix is its inverse. $\blacksquare$
    ///

    The identity is not a lucky guess: for $\mathbf M = \begin{bmatrix} \mathbf A & -\mathbf U \\ \mathbf V & \mathbf C^{-1}\end{bmatrix}$, the top-left block of $\mathbf M^{-1}$ is $(\mathbf M/\mathbf C^{-1})^{-1} = (\mathbf A + \mathbf U\mathbf C\mathbf V)^{-1}$ by the corollary, and also $\mathbf A^{-1} - \mathbf A^{-1}\mathbf U\mathbf W^{-1}\mathbf V\mathbf A^{-1}$ by the theorem, since $\mathbf M/\mathbf A = \mathbf W$. The lemma equates the two. It pays off when $k \ll n$: the right side inverts only the $k\times k$ matrix $\mathbf W$.

    **Example (the information form of the Kalman update).** Let $\mathbf P^- \in \mathbb R^{n\times n}$ and $\mathbf R \in \mathbb R^{m\times m}$ be positive definite, $\mathbf H \in \mathbb R^{m\times n}$, $\mathbf S := \mathbf H\mathbf P^-\mathbf H^\top + \mathbf R$, and $\mathbf K := \mathbf P^-\mathbf H^\top\mathbf S^{-1}$ (the {term}`Kalman gain` of [Chapter 13](ch13_kalman_filter.md)). The lemma with $\mathbf A = (\mathbf P^-)^{-1}$, $\mathbf U = \mathbf H^\top$, $\mathbf C = \mathbf R^{-1}$, $\mathbf V = \mathbf H$ (so $\mathbf W = \mathbf S$, invertible as shown under Symmetric and Positive Definite Matrices) gives
    $$\big((\mathbf P^-)^{-1} + \mathbf H^\top\mathbf R^{-1}\mathbf H\big)^{-1} = \mathbf P^- - \mathbf P^-\mathbf H^\top\mathbf S^{-1}\mathbf H\mathbf P^- = (\mathbf I - \mathbf K\mathbf H)\mathbf P^-.$$
    For $n = m = 1$ and $\mathbf H = [1]$ this is $1/P = 1/P^- + 1/R$, the formula of [Chapter 7](ch7_optimal_alpha.md): inverse variances (information) add.

    /// important | 📐 **Lemma (Schur Complements of Positive Definite Matrices)**
        attrs: {class: no-icon}
    Let $\mathbf M = \begin{bmatrix} \mathbf A & \mathbf B \\ \mathbf B^\top & \mathbf D\end{bmatrix}$ be symmetric with $\mathbf A$ positive definite. Then $\mathbf M/\mathbf A = \mathbf D - \mathbf B^\top\mathbf A^{-1}\mathbf B$ is symmetric, and $\mathbf M$ is positive definite (semidefinite) if and only if $\mathbf M/\mathbf A$ is positive definite (semidefinite).
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    $\mathbf A^{-1}$ is symmetric, so $(\mathbf B^\top\mathbf A^{-1}\mathbf B)^\top = \mathbf B^\top\mathbf A^{-1}\mathbf B$ and $\mathbf S := \mathbf M/\mathbf A$ is symmetric. With $\mathbf C = \mathbf B^\top$, the first factor in the theorem is the transpose of the last one, $\mathbf U := \begin{bmatrix} \mathbf I & \mathbf A^{-1}\mathbf B \\ \mathbf 0 & \mathbf I\end{bmatrix}$, so $\mathbf M = \mathbf U^\top\begin{bmatrix} \mathbf A & \mathbf 0 \\ \mathbf 0 & \mathbf S\end{bmatrix}\mathbf U$. For $\mathbf x \in \mathbb R^{p+q}$ write $\mathbf U\mathbf x = (\mathbf y, \mathbf w)$; block multiplication gives
    $$\mathbf x^\top\mathbf M\mathbf x = \mathbf y^\top\mathbf A\mathbf y + \mathbf w^\top\mathbf S\mathbf w.$$
    Since $\mathbf U$ is invertible, $(\mathbf y, \mathbf w)$ runs over all of $\mathbb R^{p+q}$, and is nonzero exactly when $\mathbf x$ is. If $\mathbf S$ is positive definite and $(\mathbf y, \mathbf w) \ne \mathbf 0$, then either $\mathbf w \ne \mathbf 0$ (second term positive) or $\mathbf y \ne \mathbf 0$ (first term positive), and the other term is $\ge 0$. Conversely, choosing $\mathbf y = \mathbf 0$ shows that $\mathbf M$ positive definite forces $\mathbf w^\top\mathbf S\mathbf w > 0$ for $\mathbf w \ne \mathbf 0$. The semidefinite case is the same with $\ge$. $\blacksquare$
    ///

    So the conditional covariance of [Chapter 12](ch12_vectors_matrices_covariance.md), a Schur complement of a covariance matrix, is again a valid covariance matrix.

    /// caution | ⚠️ **Assumptions and Failure Modes**
        attrs: {class: no-icon}
    - **The pivot block must be invertible.** $\mathbf M = \begin{bmatrix} 0 & 1 \\ 1 & 0\end{bmatrix}$ is invertible, but its top-left block $0$ is not, so $\mathbf M/\mathbf A$ is undefined; use the other Schur complement (here $\mathbf D = 0$ fails too, and neither formula applies even though $\mathbf M^{-1} = \mathbf M$).
    - **The matrix inversion lemma needs $\mathbf W$ invertible.** In the Kalman example this is guaranteed by $\mathbf R$ being positive definite. With a perfect sensor ($\mathbf R$ singular) the information form breaks down, although the covariance form $(\mathbf I - \mathbf K\mathbf H)\mathbf P^-$ may still make sense.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cross Products and Skew-Symmetric Matrices

    A wheel spins about the vertical axis at $\boldsymbol\omega = (0, 0, 1)$ rad/s (counterclockwise seen from above, in East-North-Up coordinates). A point on its rim at $\mathbf r = (1, 0, 0)$ m (due East of the hub) moves North at $1$ m/s, perpendicular to both the axis and the radius. The velocity is the cross product $\boldsymbol\omega\times\mathbf r = (0, 1, 0)$ m/s. Cross products appear wherever rotation does: gyroscope kinematics, lever arms, and the attitude error models of Chapters 17–21.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Cross product**</u>

    The cross product of $\mathbf a, \mathbf b \in \mathbb R^3$ is the vector
    $$\mathbf a\times\mathbf b := (a_2b_3 - a_3b_2,\ a_3b_1 - a_1b_3,\ a_1b_2 - a_2b_1) \in \mathbb R^3.$$
    ///

    Check: $(0, 0, 1)\times(1, 0, 0) = (0\cdot 0 - 1\cdot 0,\ 1\cdot 1 - 0\cdot 0,\ 0\cdot 0 - 0\cdot 1) = (0, 1, 0)$. The formula is unchanged if all indices are shifted cyclically $1 \to 2 \to 3 \to 1$; we call this **cyclic symmetry** and use it to prove one component of an identity and conclude the other two.

    For fixed $\mathbf a$, each entry of $\mathbf a\times\mathbf b$ is a linear combination of $b_1, b_2, b_3$, so $\mathbf b \mapsto \mathbf a\times\mathbf b$ is linear and therefore given by a matrix ("Matrices Are Linear Maps"). Its columns are $\mathbf a\times\mathbf e_1 = (0, a_3, -a_2)$, $\mathbf a\times\mathbf e_2 = (-a_3, 0, a_1)$, and $\mathbf a\times\mathbf e_3 = (a_2, -a_1, 0)$:

    $$[\mathbf a]_\times := \begin{bmatrix} 0 & -a_3 & a_2 \\ a_3 & 0 & -a_1 \\ -a_2 & a_1 & 0\end{bmatrix}, \qquad [\mathbf a]_\times\mathbf b = \mathbf a\times\mathbf b.$$

    This matrix equals minus its transpose.

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Skew-symmetric matrix**</u>

    A square matrix $\mathbf W \in \mathbb R^{n\times n}$ is skew-symmetric if $\mathbf W^\top = -\mathbf W$, i.e. $w_{ij} = -w_{ji}$ for all $i, j$.
    ///

    Taking $i = j$ shows that the diagonal of a skew-symmetric matrix is zero. A $3\times 3$ skew-symmetric matrix is therefore determined by the three entries $w_{32}, w_{13}, w_{21}$ below and above the diagonal, which gives:

    /// important | 📐 **Lemma (Skew-Symmetric Matrices in 3-D)**
        attrs: {class: no-icon}
    For every $\mathbf a \in \mathbb R^3$, $[\mathbf a]_\times$ is skew-symmetric, and every skew-symmetric $\mathbf W \in \mathbb R^{3\times 3}$ equals $[\mathbf w]_\times$ for exactly one $\mathbf w \in \mathbb R^3$, namely $\mathbf w = (w_{32}, w_{13}, w_{21})$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    The first claim is visible in the matrix. If $\mathbf W$ is skew-symmetric, its diagonal is zero and $w_{23} = -w_{32}$, $w_{31} = -w_{13}$, $w_{12} = -w_{21}$, so $\mathbf W = [(w_{32}, w_{13}, w_{21})]_\times$ entry by entry. If $[\mathbf w]_\times = [\mathbf w']_\times$, then comparing entries $(3,2)$, $(1,3)$, $(2,1)$ gives $\mathbf w = \mathbf w'$. $\blacksquare$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// important | 📐 **Theorem (Cross Product Identities)**
        attrs: {class: no-icon}
    For all $\mathbf a, \mathbf b, \mathbf c \in \mathbb R^3$ and $s \in \mathbb R$:

    1. $(\mathbf a + s\mathbf b)\times\mathbf c = \mathbf a\times\mathbf c + s\,(\mathbf b\times\mathbf c)$ and $\mathbf a\times(\mathbf b + s\mathbf c) = \mathbf a\times\mathbf b + s\,(\mathbf a\times\mathbf c)$;
    2. $\mathbf a\times\mathbf b = -\,\mathbf b\times\mathbf a$; in particular $\mathbf a\times\mathbf a = \mathbf 0$;
    3. (triple product) $\mathbf a\cdot(\mathbf b\times\mathbf c) = \det[\mathbf a\ \mathbf b\ \mathbf c] = \mathbf b\cdot(\mathbf c\times\mathbf a) = \mathbf c\cdot(\mathbf a\times\mathbf b)$, where $[\mathbf a\ \mathbf b\ \mathbf c]$ is the matrix with these columns; in particular $\mathbf a\times\mathbf b$ is orthogonal to $\mathbf a$ and to $\mathbf b$;
    4. (triple-product expansion) $\mathbf a\times(\mathbf b\times\mathbf c) = \mathbf b\,(\mathbf a\cdot\mathbf c) - \mathbf c\,(\mathbf a\cdot\mathbf b)$; in matrix form, $[\mathbf a]_\times^2 = \mathbf a\mathbf a^\top - \|\mathbf a\|^2\mathbf I$;
    5. (Lagrange's identity) $\|\mathbf a\times\mathbf b\|^2 = \|\mathbf a\|^2\|\mathbf b\|^2 - (\mathbf a\cdot\mathbf b)^2$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    (1) The second identity is linearity of $\mathbf b \mapsto [\mathbf a]_\times\mathbf b$; the first holds because $[\mathbf a]_\times$ depends linearly on $\mathbf a$ (each entry is $0$ or $\pm a_i$). (2) Each component changes sign when $\mathbf a$ and $\mathbf b$ are swapped; then $\mathbf a\times\mathbf a = -\,\mathbf a\times\mathbf a$.

    (3) Expanding gives the same six terms for all four expressions, $a_1b_2c_3 - a_1b_3c_2 + a_2b_3c_1 - a_2b_1c_3 + a_3b_1c_2 - a_3b_2c_1$ (for the determinant use the $3\times 3$ formula under Determinants). Then $\mathbf a\cdot(\mathbf a\times\mathbf b) = \mathbf b\cdot(\mathbf a\times\mathbf a) = 0$ and $\mathbf b\cdot(\mathbf a\times\mathbf b) = \mathbf a\cdot(\mathbf b\times\mathbf b) = 0$ by the cyclic equalities and (2).

    (4) First component: $a_2(b_1c_2 - b_2c_1) - a_3(b_3c_1 - b_1c_3) = b_1(a_2c_2 + a_3c_3) - c_1(a_2b_2 + a_3b_3) = b_1(\mathbf a\cdot\mathbf c) - c_1(\mathbf a\cdot\mathbf b)$, after adding and subtracting $a_1b_1c_1$. The other components follow by cyclic symmetry. For the matrix form, $[\mathbf a]_\times^2\mathbf b = \mathbf a\times(\mathbf a\times\mathbf b) = \mathbf a(\mathbf a\cdot\mathbf b) - \mathbf b\|\mathbf a\|^2 = (\mathbf a\mathbf a^\top - \|\mathbf a\|^2\mathbf I)\mathbf b$ for every $\mathbf b$, and a matrix is determined by its action ("Matrices Are Linear Maps").

    (5) By (3) with the three vectors $\mathbf a\times\mathbf b$, $\mathbf a$, $\mathbf b$, then (4):
    $\|\mathbf a\times\mathbf b\|^2 = (\mathbf a\times\mathbf b)\cdot(\mathbf a\times\mathbf b) = \mathbf a\cdot\big(\mathbf b\times(\mathbf a\times\mathbf b)\big) = \mathbf a\cdot\big(\mathbf a\|\mathbf b\|^2 - \mathbf b(\mathbf b\cdot\mathbf a)\big) = \|\mathbf a\|^2\|\mathbf b\|^2 - (\mathbf a\cdot\mathbf b)^2$. $\blacksquare$
    ///

    By (5) and the angle $\vartheta \in [0, \pi]$ between $\mathbf a$ and $\mathbf b$ (Cauchy–Schwarz), $\|\mathbf a\times\mathbf b\| = \|\mathbf a\|\|\mathbf b\|\sin\vartheta$: the area of the parallelogram they span. By (3), $\mathbf a\times\mathbf b$ is perpendicular to both; its direction follows the right-hand rule. In the wheel example, $\|\boldsymbol\omega\times\mathbf r\| = 1\cdot 1\cdot\sin 90° = 1$ m/s.

    /// important | 📐 **Theorem (Rotations Respect Cross Products)**
        attrs: {class: no-icon}
    If $\mathbf Q \in \mathbb R^{3\times 3}$ is orthogonal with $\det\mathbf Q = 1$, then for all $\mathbf a, \mathbf b \in \mathbb R^3$
    $$\mathbf Q(\mathbf a\times\mathbf b) = (\mathbf Q\mathbf a)\times(\mathbf Q\mathbf b), \qquad\text{equivalently}\qquad \mathbf Q[\mathbf a]_\times\mathbf Q^\top = [\mathbf Q\mathbf a]_\times.$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    For every $\mathbf c \in \mathbb R^3$, using the triple product, the column view of products ($[\mathbf c\ \ \mathbf Q\mathbf a\ \ \mathbf Q\mathbf b] = \mathbf Q[\mathbf Q^\top\mathbf c\ \ \mathbf a\ \ \mathbf b]$, since $\mathbf Q\mathbf Q^\top = \mathbf I$), and property 2 of the determinant:
    $$\mathbf c\cdot(\mathbf Q\mathbf a\times\mathbf Q\mathbf b) = \det\big(\mathbf Q[\mathbf Q^\top\mathbf c\ \ \mathbf a\ \ \mathbf b]\big) = \det\mathbf Q\,(\mathbf Q^\top\mathbf c)\cdot(\mathbf a\times\mathbf b) = \mathbf c\cdot\mathbf Q(\mathbf a\times\mathbf b),$$
    where the last step uses $\det\mathbf Q = 1$ and transpose rule 4. Taking $\mathbf c = \mathbf e_i$ for $i = 1, 2, 3$ shows that the two vectors have the same entries. For the matrix form, $\mathbf Q[\mathbf a]_\times\mathbf Q^\top\mathbf b = \mathbf Q\big(\mathbf a\times\mathbf Q^\top\mathbf b\big) = \mathbf Q\mathbf a\times\mathbf Q\mathbf Q^\top\mathbf b = [\mathbf Q\mathbf a]_\times\mathbf b$ for every $\mathbf b$. $\blacksquare$
    ///

    If $\det\mathbf Q = -1$ (a reflection), the same computation gives $\mathbf Q(\mathbf a\times\mathbf b) = -(\mathbf Q\mathbf a)\times(\mathbf Q\mathbf b)$: mirrors reverse handedness. This is why every frame in this book is right-handed (East-North-Up, Forward-Left-Up), and why mixing in a left-handed frame silently flips the sign of every cross product.

    The code below implements $[\mathbf a]_\times$ and checks the identities numerically for one random pair of vectors.
    """)
    return


@app.cell
def _(np):
    # jb: echo=true
    def skew(a):
        """The cross-product matrix [a]_x, so that skew(a) @ b == np.cross(a, b)."""
        return np.array([[0.0, -a[2], a[1]],
                         [a[2], 0.0, -a[0]],
                         [-a[1], a[0], 0.0]])

    return (skew,)


@app.cell
def _(mo, np, skew):
    # jb: echo=true
    rng_cross = np.random.default_rng(3)
    a_vec, b_vec = rng_cross.standard_normal(3), rng_cross.standard_normal(3)

    mo.plain_text(
        f"[a]x b == a x b:             {np.allclose(skew(a_vec) @ b_vec, np.cross(a_vec, b_vec))}\n"
        f"[a]x is skew-symmetric:      {np.allclose(skew(a_vec).T, -skew(a_vec))}\n"
        f"[a]x^2 == a a^T - |a|^2 I:   "
        f"{np.allclose(skew(a_vec) @ skew(a_vec), np.outer(a_vec, a_vec) - (a_vec @ a_vec) * np.eye(3))}\n"
        f"a . (a x b) == 0:            {np.isclose(a_vec @ np.cross(a_vec, b_vec), 0.0)}"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Matrix Exponential

    The scalar model $\dot x = ax$ has the solution $x(t) = e^{at}x(0)$, so its exact discretization is $x_k = e^{a\Delta t}x_{k-1}$ ([Chapter 10](ch10_process_models.md)). A cart moving at constant velocity obeys the vector equation

    $$\frac{d}{dt}\begin{bmatrix} p \\ v\end{bmatrix} = \begin{bmatrix} v \\ 0\end{bmatrix} = \underbrace{\begin{bmatrix} 0 & 1 \\ 0 & 0\end{bmatrix}}_{\mathbf A}\begin{bmatrix} p \\ v\end{bmatrix},$$

    and we would like to write its solution as "$e^{t\mathbf A}$ times the initial state". Taking the exponential series of [Appendix C: Exponential and Logarithm](appendix_c_calculus.md) and replacing powers of $a$ by powers of $\mathbf A$ does exactly that. Here $\mathbf A^2 = \mathbf 0$, so the series stops after two terms:

    $$\mathbf I + t\mathbf A = \begin{bmatrix} 1 & t \\ 0 & 1\end{bmatrix},$$

    which for $t = \Delta t$ is the cart matrix $\mathbf F$ we have used all along. A sequence of matrices $\mathbf M_N$ **converges** to $\mathbf M$ if every entry converges, $[\mathbf M_N]_{ij} \to [\mathbf M]_{ij}$ ([Appendix C: Sequences and Limits](appendix_c_calculus.md)).

    /// important | 📐 **Lemma (Convergence of the Exponential Series)**
        attrs: {class: no-icon}
    For every $\mathbf A \in \mathbb R^{n\times n}$ and all $i, j$, the series $\sum_{k=0}^\infty [\mathbf A^k]_{ij}/k!$ converges absolutely. Moreover $|[\mathbf A^k]_{ij}| \le \|\mathbf A\|_F^k$ for $k \ge 1$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    By submultiplicativity and induction on $k$, $\|\mathbf A^k\|_F \le \|\mathbf A\|_F^k$ for $k \ge 1$, and every entry is bounded by the Frobenius norm. So the terms are bounded in absolute value by $\|\mathbf A\|_F^k/k!$ for $k \ge 1$ (and by $1$ for $k = 0$). The series $\sum_k\|\mathbf A\|_F^k/k!$ converges (to $e^{\|\mathbf A\|_F}$; [Appendix C: Exponential and Logarithm](appendix_c_calculus.md)), so the Comparison Test ([Appendix C: Series](appendix_c_calculus.md)) gives absolute convergence. $\blacksquare$
    ///

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Matrix exponential**</u>

    The matrix exponential of $\mathbf A \in \mathbb R^{n\times n}$ is the matrix $\exp(\mathbf A) \in \mathbb R^{n\times n}$ whose $(i, j)$ entry is $\sum_{k=0}^\infty [\mathbf A^k]_{ij}/k!$. We write
    $$\exp(\mathbf A) = \sum_{k=0}^\infty\frac{\mathbf A^k}{k!} = \mathbf I + \mathbf A + \frac{\mathbf A^2}{2!} + \cdots,$$
    and also $e^{\mathbf A}$.
    ///

    Entrywise limits pass through fixed matrices: if $\mathbf M_N \to \mathbf M$, then $\mathbf B\mathbf M_N \to \mathbf B\mathbf M$, $\mathbf M_N\mathbf B \to \mathbf M\mathbf B$, and $\mathbf M_N^\top \to \mathbf M^\top$, because each entry of $\mathbf B\mathbf M_N$ is a fixed finite linear combination of entries of $\mathbf M_N$ (limit laws, [Appendix C: Sequences and Limits](appendix_c_calculus.md)). We use this freely below.

    /// important | 📐 **Theorem (Properties of the Matrix Exponential)**
        attrs: {class: no-icon}
    For $\mathbf A, \mathbf B \in \mathbb R^{n\times n}$ and $s, t \in \mathbb R$:

    1. $\exp(\mathbf 0) = \mathbf I$, $\ \exp\big(\operatorname{diag}(d_1, \ldots, d_n)\big) = \operatorname{diag}(e^{d_1}, \ldots, e^{d_n})$, and $\exp(\mathbf A^\top) = \exp(\mathbf A)^\top$;
    2. if $\mathbf V$ is invertible, $\exp(\mathbf V\mathbf A\mathbf V^{-1}) = \mathbf V\exp(\mathbf A)\mathbf V^{-1}$;
    3. if $\mathbf A\mathbf B = \mathbf B\mathbf A$, then $\exp(\mathbf A + \mathbf B) = \exp(\mathbf A)\exp(\mathbf B)$;
    4. $\exp(\mathbf A)$ is invertible with $\exp(\mathbf A)^{-1} = \exp(-\mathbf A)$, and $\exp\big((s + t)\mathbf A\big) = \exp(s\mathbf A)\exp(t\mathbf A)$;
    5. $t \mapsto \exp(t\mathbf A)$ is differentiable (entry by entry) with $\dfrac{d}{dt}\exp(t\mathbf A) = \mathbf A\exp(t\mathbf A) = \exp(t\mathbf A)\mathbf A$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    (1) $\mathbf 0^k = \mathbf 0$ for $k \ge 1$; powers of a diagonal matrix are diagonal with entries $d_i^k$; and $(\mathbf A^\top)^k = (\mathbf A^k)^\top$ by the transpose rules and induction. Pass to the limit of the partial sums.

    (2) $(\mathbf V\mathbf A\mathbf V^{-1})^k = \mathbf V\mathbf A^k\mathbf V^{-1}$ by induction (the inner $\mathbf V^{-1}\mathbf V$ cancel), so the partial sums are $\mathbf V\big(\sum_{k\le N}\mathbf A^k/k!\big)\mathbf V^{-1}$; pass to the limit.

    (3) Because $\mathbf A$ and $\mathbf B$ commute, the binomial theorem $(\mathbf A + \mathbf B)^m = \sum_{k=0}^m\binom{m}{k}\mathbf A^k\mathbf B^{m-k}$ holds (its usual induction proof uses only distributivity, associativity, and $\mathbf A\mathbf B = \mathbf B\mathbf A$). Fix $i, j$. For each $l$, the product $[\exp\mathbf A]_{il}[\exp\mathbf B]_{lj}$ of two absolutely convergent series equals, by the Cauchy Product ([Appendix C: Series](appendix_c_calculus.md)), $\sum_{m=0}^\infty\sum_{k=0}^m [\mathbf A^k]_{il}[\mathbf B^{m-k}]_{lj}/\big(k!\,(m-k)!\big)$. Summing over the finitely many $l$ inside the limit,
    $$[\exp\mathbf A\exp\mathbf B]_{ij} = \sum_{m=0}^\infty\frac{1}{m!}\sum_{k=0}^m\binom{m}{k}[\mathbf A^k\mathbf B^{m-k}]_{ij} = \sum_{m=0}^\infty\frac{[(\mathbf A + \mathbf B)^m]_{ij}}{m!} = [\exp(\mathbf A + \mathbf B)]_{ij}.$$

    (4) $\mathbf A$ and $-\mathbf A$ commute, so by (3) and (1), $\exp(\mathbf A)\exp(-\mathbf A) = \exp(\mathbf 0) = \mathbf I$, and likewise in the other order. $s\mathbf A$ and $t\mathbf A$ commute.

    (5) For $0 < |h| \le 1$, every entry of $\big(\exp(h\mathbf A) - \mathbf I\big)/h - \mathbf A = \sum_{k\ge 2}h^{k-1}\mathbf A^k/k!$ is at most $\sum_{k\ge 2}|h|^{k-1}\|\mathbf A\|_F^k/k! \le |h|\,e^{\|\mathbf A\|_F}$ in absolute value, which tends to $0$ as $h \to 0$. By (4), $\big(\exp((t + h)\mathbf A) - \exp(t\mathbf A)\big)/h = \exp(t\mathbf A)\big(\exp(h\mathbf A) - \mathbf I\big)/h \to \exp(t\mathbf A)\mathbf A$ ([Appendix C: Limits of Functions and Continuity](appendix_c_calculus.md)). Finally $\mathbf A$ commutes with every partial sum of $\exp(t\mathbf A)$, hence with $\exp(t\mathbf A)$. $\blacksquare$
    ///

    **Commuting matters.** For $\mathbf A = \begin{bmatrix} 0 & 1 \\ 0 & 0\end{bmatrix}$ and $\mathbf B = \begin{bmatrix} 0 & 0 \\ 1 & 0\end{bmatrix}$ (which do not commute), $\exp(\mathbf A)\exp(\mathbf B) = \begin{bmatrix} 1 & 1 \\ 0 & 1\end{bmatrix}\begin{bmatrix} 1 & 0 \\ 1 & 1\end{bmatrix} = \begin{bmatrix} 2 & 1 \\ 1 & 1\end{bmatrix}$. But $\mathbf J := \mathbf A + \mathbf B = \begin{bmatrix} 0 & 1 \\ 1 & 0\end{bmatrix}$ has $\mathbf J^2 = \mathbf I$, so grouping even and odd powers gives $\exp(\mathbf J) = \big(\sum_m\tfrac{1}{(2m)!}\big)\mathbf I + \big(\sum_m\tfrac{1}{(2m+1)!}\big)\mathbf J \approx \begin{bmatrix} 1.543 & 1.175 \\ 1.175 & 1.543\end{bmatrix}$, a different matrix.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Linear differential equations

    /// important | 📐 **Theorem (Solution of $\dot{\mathbf x} = \mathbf A\mathbf x$)**
        attrs: {class: no-icon}
    For $\mathbf A \in \mathbb R^{n\times n}$ and $\mathbf x_0 \in \mathbb R^n$, the function $\mathbf x(t) := \exp(t\mathbf A)\mathbf x_0$ satisfies $\dot{\mathbf x}(t) = \mathbf A\mathbf x(t)$ for all $t \in \mathbb R$ and $\mathbf x(0) = \mathbf x_0$, and it is the only differentiable function with these two properties. Consequently, for every $\Delta t$,
    $$\mathbf x(t + \Delta t) = \exp(\Delta t\,\mathbf A)\,\mathbf x(t).$$
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Property 5 gives $\dot{\mathbf x} = \mathbf A\exp(t\mathbf A)\mathbf x_0 = \mathbf A\mathbf x$, and property 1 gives $\mathbf x(0) = \mathbf x_0$. Uniqueness: let $\mathbf y$ be another such function and $\mathbf g(t) := \exp(-t\mathbf A)\mathbf y(t)$. By the product rule, applied entry by entry ([Appendix C: Derivatives](appendix_c_calculus.md)), and property 5 for $-\mathbf A$,
    $$\dot{\mathbf g} = -\mathbf A\exp(-t\mathbf A)\mathbf y + \exp(-t\mathbf A)\mathbf A\mathbf y = -\exp(-t\mathbf A)\mathbf A\mathbf y + \exp(-t\mathbf A)\mathbf A\mathbf y = \mathbf 0.$$
    A function with zero derivative everywhere is constant ([Appendix C: The Mean Value Theorem and Extrema](appendix_c_calculus.md)), so $\mathbf g(t) = \mathbf g(0) = \mathbf x_0$, and by property 4, $\mathbf y(t) = \exp(t\mathbf A)\mathbf g(t) = \mathbf x(t)$. The last claim is property 4: $\exp\big((t + \Delta t)\mathbf A\big)\mathbf x_0 = \exp(\Delta t\,\mathbf A)\exp(t\mathbf A)\mathbf x_0$. $\blacksquare$
    ///

    So the exact discrete-time transition matrix of a linear continuous-time model is $\mathbf F = \exp(\mathbf A\Delta t)$; for $n = 1$ this is the $e^{a\Delta t}$ of [Chapter 10](ch10_process_models.md), and for the cart it is $\begin{bmatrix} 1 & \Delta t \\ 0 & 1\end{bmatrix}$.

    **Example (an integral for the process noise).** Integrals of matrix-valued functions are taken entry by entry. When the cart's acceleration is white noise of intensity $q$, [Chapter 14](ch14_kalman_filters_in_practice.md) discretizes it with an integral of the form $\mathbf Q = \int_0^{\Delta t}\exp(\mathbf A\tau)\,\mathbf g\,q\,\mathbf g^\top\exp(\mathbf A\tau)^\top\,d\tau$ with $\mathbf g = (0, 1)$. Here $\exp(\mathbf A\tau)\mathbf g = (\tau, 1)$, so the integrand is $q\begin{bmatrix} \tau^2 & \tau \\ \tau & 1\end{bmatrix}$ and
    $$\mathbf Q = q\begin{bmatrix} \Delta t^3/3 & \Delta t^2/2 \\ \Delta t^2/2 & \Delta t\end{bmatrix}.$$

    ### Exponentials of skew-symmetric matrices

    /// important | 📐 **Theorem (Exponentials of Skew-Symmetric Matrices Are Rotations)**
        attrs: {class: no-icon}
    If $\mathbf K \in \mathbb R^{n\times n}$ is skew-symmetric, then $\exp(\mathbf K)$ is orthogonal and $\det\exp(\mathbf K) = 1$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    By properties 1 and 4, $\exp(\mathbf K)^\top\exp(\mathbf K) = \exp(\mathbf K^\top)\exp(\mathbf K) = \exp(-\mathbf K)\exp(\mathbf K) = \mathbf I$. The same holds for $t\mathbf K$, which is also skew-symmetric, so $f(t) := \det\exp(t\mathbf K) \in \{-1, 1\}$ for every $t$. The determinant is a polynomial in the entries (by its recursive definition), and the entries of $\exp(t\mathbf K)$ are differentiable, hence continuous, in $t$ (property 5); so $f$ is continuous. Since $f(0) = \det\mathbf I = 1$, if $f(1)$ were $-1$ the intermediate value theorem ([Appendix C: Limits of Functions and Continuity](appendix_c_calculus.md)) would give a $t$ with $f(t) = 0$, which is impossible. So $f(1) = 1$. $\blacksquare$
    ///

    For $n = 3$ every skew-symmetric matrix is $[\boldsymbol\theta]_\times$ for some $\boldsymbol\theta \in \mathbb R^3$, and $\exp([\boldsymbol\theta]_\times)$ is the rotation by the angle $\|\boldsymbol\theta\|$ about the axis $\boldsymbol\theta$; [Chapter 17](ch17_rotations.md) derives its closed form (Rodrigues' formula). With a constant body rate $\boldsymbol\omega$, property 5 shows that $\mathbf R(t) = \mathbf R(0)\exp(t[\boldsymbol\omega]_\times)$ solves the attitude kinematics $\dot{\mathbf R} = \mathbf R[\boldsymbol\omega]_\times$ used from Chapter 17 on.

    The code below sums the series directly and checks these facts.
    """)
    return


@app.cell
def _(np):
    # jb: echo=true
    def expm_series(A, terms=30):
        """Partial sum I + A + A^2/2! + ... + A^(terms-1)/(terms-1)! of the exponential series.

        Fine for moderate ||A||_F; production code (scipy.linalg.expm) adds
        "scaling and squaring" so that large matrices are handled accurately.
        """
        A = np.asarray(A, dtype=float)
        term = np.eye(A.shape[0])
        total = term.copy()
        for k in range(1, terms):
            term = term @ A / k
            total = total + term
        return total

    return (expm_series,)


@app.cell
def _(expm_series, mo, np, skew):
    # jb: echo=true
    dt_demo = 0.1                                       # s
    A_cart = np.array([[0.0, 1.0], [0.0, 0.0]])         # d/dt (p, v) = (v, 0)
    B_other = np.array([[0.0, 0.0], [1.0, 0.0]])        # does not commute with A_cart

    omega_demo = np.array([0.3, -0.2, 0.9])             # constant body rate, rad/s
    R_demo = expm_series(skew(omega_demo) * 1.0)        # attitude change over 1 s

    mo.plain_text(
        f"exp(A dt) for the cart =\n{expm_series(A_cart * dt_demo)}\n"
        f"R^T R == I:                     {np.allclose(R_demo.T @ R_demo, np.eye(3))}\n"
        f"det R:                          {np.linalg.det(R_demo):.12f}\n"
        f"R omega == omega (axis fixed):  {np.allclose(R_demo @ omega_demo, omega_demo)}\n"
        f"exp(A + B) == exp(A) exp(B):    "
        f"{np.allclose(expm_series(A_cart + B_other), expm_series(A_cart) @ expm_series(B_other))}"
        f"   (A and B do not commute)"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
        attrs: {class: no-icon}
    - **Non-commuting exponents.** $\exp(\mathbf A + \mathbf B) \ne \exp(\mathbf A)\exp(\mathbf B)$ in general. In particular, a time-varying model $\dot{\mathbf x} = \mathbf A(t)\mathbf x$ is *not* solved by $\exp\big(\int\mathbf A(t)\,dt\big)$ unless the matrices $\mathbf A(t)$ commute. For attitude, this means a body whose rotation axis keeps changing (such as a swinging foot) cannot be integrated by exponentiating the summed gyro angles; filters exponentiate one short step at a time.
    - **Truncation.** Keeping only $\mathbf I + \mathbf K$ for a skew-symmetric $\mathbf K$ (a first-order, or Euler, step) gives $(\mathbf I + \mathbf K)^\top(\mathbf I + \mathbf K) = \mathbf I - \mathbf K^2$. For $\mathbf K = [\mathbf a]_\times$, $-\mathbf K^2 = \|\mathbf a\|^2\mathbf I - \mathbf a\mathbf a^\top$ is positive semidefinite, so every step slightly *stretches* vectors perpendicular to $\mathbf a$. Repeated over many steps, the attitude matrix drifts away from orthogonality ([Chapter 18](ch18_quaternions.md)).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Derivatives with Respect to Matrices

    [Chapter 13](ch13_kalman_filter.md) chooses the gain $\mathbf K$ to minimize $\operatorname{tr}\mathbf P(\mathbf K)$, a real-valued function of a matrix variable. In the scalar case ([Chapter 7](ch7_optimal_alpha.md)) we completed the square. For matrices we can do the same (the last theorem below), or we can set the partial derivative with respect to every entry to zero, which is how the formula is usually found.

    For $f : \mathbb R^{m\times n} \to \mathbb R$, regard $\mathbf X$ as the point $(x_{11}, x_{12}, \ldots, x_{mn}) \in \mathbb R^{mn}$. The **derivative of $f$ with respect to $\mathbf X$** is the $m\times n$ matrix of partial derivatives ([Appendix C: Functions of Several Variables](appendix_c_calculus.md))

    $$\frac{\partial f}{\partial\mathbf X} := \begin{bmatrix} \partial f/\partial x_{11} & \cdots & \partial f/\partial x_{1n} \\ \vdots & & \vdots \\ \partial f/\partial x_{m1} & \cdots & \partial f/\partial x_{mn}\end{bmatrix},$$

    when they all exist. It has the same shape as $\mathbf X$. Some texts use the transpose instead, so compare conventions before copying formulas ([Wikipedia: Matrix calculus](https://en.wikipedia.org/wiki/Matrix_calculus)). For example, $f(\mathbf X) = x_{11}^2 + 3x_{12}x_{21}$ on $\mathbb R^{2\times 2}$ has $\partial f/\partial\mathbf X = \begin{bmatrix} 2x_{11} & 3x_{21} \\ 3x_{12} & 0\end{bmatrix}$.

    /// important | 📐 **Theorem (Trace Derivatives)**
        attrs: {class: no-icon}
    For $\mathbf X \in \mathbb R^{m\times n}$:

    1. $\dfrac{\partial\operatorname{tr}(\mathbf A\mathbf X)}{\partial\mathbf X} = \mathbf A^\top$ for every $\mathbf A \in \mathbb R^{n\times m}$;
    2. $\dfrac{\partial\operatorname{tr}(\mathbf X\mathbf M^\top)}{\partial\mathbf X} = \dfrac{\partial\operatorname{tr}(\mathbf M\mathbf X^\top)}{\partial\mathbf X} = \mathbf M$ for every $\mathbf M \in \mathbb R^{m\times n}$;
    3. $\dfrac{\partial\operatorname{tr}(\mathbf X\mathbf A\mathbf X^\top)}{\partial\mathbf X} = \mathbf X(\mathbf A + \mathbf A^\top)$ for every $\mathbf A \in \mathbb R^{n\times n}$, which is $2\mathbf X\mathbf A$ if $\mathbf A$ is symmetric.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    (1) $\operatorname{tr}(\mathbf A\mathbf X) = \sum_{i=1}^n\sum_{k=1}^m a_{ik}x_{ki}$. Exactly one term contains $x_{pq}$, namely the one with $k = p$ and $i = q$, and it equals $a_{qp}x_{pq}$. So $\partial\operatorname{tr}(\mathbf A\mathbf X)/\partial x_{pq} = a_{qp} = [\mathbf A^\top]_{pq}$.

    (2) By the cyclic property, $\operatorname{tr}(\mathbf X\mathbf M^\top) = \operatorname{tr}(\mathbf M^\top\mathbf X)$, so (1) with $\mathbf A = \mathbf M^\top$ gives $\mathbf M$. Also $\operatorname{tr}(\mathbf M\mathbf X^\top) = \operatorname{tr}\big((\mathbf X\mathbf M^\top)^\top\big) = \operatorname{tr}(\mathbf X\mathbf M^\top)$.

    (3) $\operatorname{tr}(\mathbf X\mathbf A\mathbf X^\top) = \sum_{i=1}^m\sum_{k=1}^n\sum_{l=1}^n x_{ik}a_{kl}x_{il}$. By the product rule, $\partial(x_{ik}x_{il})/\partial x_{pq} = \delta_{ip}\delta_{kq}\,x_{il} + x_{ik}\,\delta_{ip}\delta_{lq}$. Summing,
    $$\frac{\partial\operatorname{tr}(\mathbf X\mathbf A\mathbf X^\top)}{\partial x_{pq}} = \sum_{l=1}^n a_{ql}x_{pl} + \sum_{k=1}^n x_{pk}a_{kq} = [\mathbf X\mathbf A^\top]_{pq} + [\mathbf X\mathbf A]_{pq}. \qquad\blacksquare$$
    ///

    With $m = n = 1$ these reduce to $\tfrac{d}{dx}(ax) = a$ and $\tfrac{d}{dx}(ax^2) = 2ax$.

    /// important | 📐 **Lemma (First-Order Condition)**
        attrs: {class: no-icon}
    If $f : \mathbb R^{m\times n} \to \mathbb R$ has a minimum at $\mathbf X_\star$ and all partial derivatives of $f$ exist at $\mathbf X_\star$, then $\dfrac{\partial f}{\partial\mathbf X}(\mathbf X_\star) = \mathbf 0$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    Fix $(p, q)$ and let $\mathbf E_{pq} := \mathbf e_p\mathbf e_q^\top$, the matrix with a single $1$ in position $(p, q)$. The one-variable function $g(t) := f(\mathbf X_\star + t\mathbf E_{pq})$ has a minimum at $t = 0$, where its derivative is $\partial f/\partial x_{pq}(\mathbf X_\star)$. A differentiable function has zero derivative at an interior minimum ([Appendix C: The Mean Value Theorem and Extrema](appendix_c_calculus.md)). $\blacksquare$
    ///

    A zero derivative is necessary for a minimum, not sufficient. For the quadratic functions that appear in filtering, completing the square settles the question, and says more.

    /// important | 📐 **Theorem (Completing the Square for Matrices)**
        attrs: {class: no-icon}
    Let $\mathbf S \in \mathbb R^{n\times n}$ be positive definite, $\mathbf M \in \mathbb R^{m\times n}$, and $\mathbf C \in \mathbb R^{m\times m}$. For $\mathbf X \in \mathbb R^{m\times n}$ define
    $$f(\mathbf X) := \mathbf C - \mathbf X\mathbf M^\top - \mathbf M\mathbf X^\top + \mathbf X\mathbf S\mathbf X^\top, \qquad \mathbf X_\star := \mathbf M\mathbf S^{-1}.$$
    Then $f(\mathbf X) = f(\mathbf X_\star) + (\mathbf X - \mathbf X_\star)\mathbf S(\mathbf X - \mathbf X_\star)^\top$ for every $\mathbf X$, with $f(\mathbf X_\star) = \mathbf C - \mathbf M\mathbf S^{-1}\mathbf M^\top$. Consequently:

    1. $f(\mathbf X) - f(\mathbf X_\star)$ is positive semidefinite: $\mathbf w^\top f(\mathbf X)\mathbf w \ge \mathbf w^\top f(\mathbf X_\star)\mathbf w$ for every $\mathbf w \in \mathbb R^m$;
    2. $\operatorname{tr}f(\mathbf X) \ge \operatorname{tr}f(\mathbf X_\star)$, with equality only for $\mathbf X = \mathbf X_\star$;
    3. $\mathbf X_\star$ is the only zero of $\partial\operatorname{tr}f/\partial\mathbf X = 2\mathbf X\mathbf S - 2\mathbf M$.
    ///

    /// admonition | ✍️ **Proof**
        attrs: {class: no-icon}
    $\mathbf S^{-1}$ is symmetric, so $\mathbf X_\star\mathbf S = \mathbf M$, $\mathbf S\mathbf X_\star^\top = (\mathbf X_\star\mathbf S)^\top = \mathbf M^\top$, and $\mathbf X_\star\mathbf S\mathbf X_\star^\top = \mathbf M\mathbf S^{-1}\mathbf M^\top$. Expanding,
    $$(\mathbf X - \mathbf X_\star)\mathbf S(\mathbf X - \mathbf X_\star)^\top = \mathbf X\mathbf S\mathbf X^\top - \mathbf X\mathbf M^\top - \mathbf M\mathbf X^\top + \mathbf M\mathbf S^{-1}\mathbf M^\top = f(\mathbf X) - \big(\mathbf C - \mathbf M\mathbf S^{-1}\mathbf M^\top\big).$$
    At $\mathbf X = \mathbf X_\star$ the left side is $\mathbf 0$, so $f(\mathbf X_\star) = \mathbf C - \mathbf M\mathbf S^{-1}\mathbf M^\top$, and the identity follows.

    (1) $(\mathbf X - \mathbf X_\star)\mathbf S(\mathbf X - \mathbf X_\star)^\top$ is positive semidefinite by the Lemma (Building Positive Definite Matrices). (2) Let $\mathbf Y := \mathbf X - \mathbf X_\star$ with rows $\mathbf y_1^\top, \ldots, \mathbf y_m^\top$. Then $\operatorname{tr}(\mathbf Y\mathbf S\mathbf Y^\top) = \sum_i\mathbf y_i^\top\mathbf S\mathbf y_i \ge 0$, with equality only if every $\mathbf y_i = \mathbf 0$. (3) $\operatorname{tr}(\mathbf M\mathbf X^\top) = \operatorname{tr}(\mathbf X\mathbf M^\top)$, so $\operatorname{tr}f(\mathbf X) = \operatorname{tr}\mathbf C - 2\operatorname{tr}(\mathbf X\mathbf M^\top) + \operatorname{tr}(\mathbf X\mathbf S\mathbf X^\top)$, whose derivative is $-2\mathbf M + 2\mathbf X\mathbf S$ by the Trace Derivatives theorem. It vanishes exactly when $\mathbf X = \mathbf M\mathbf S^{-1}$. $\blacksquare$
    ///

    **Example (the Kalman gain).** With $\mathbf C = \mathbf P^-$, $\mathbf M = \mathbf P^-\mathbf H^\top$, and $\mathbf S = \mathbf H\mathbf P^-\mathbf H^\top + \mathbf R$ (so $\mathbf X\mathbf M^\top = \mathbf K\mathbf H\mathbf P^-$, since $\mathbf P^-$ is symmetric), $f(\mathbf K) = \mathbf P^- - \mathbf K\mathbf H\mathbf P^- - \mathbf P^-\mathbf H^\top\mathbf K^\top + \mathbf K\mathbf S\mathbf K^\top$ is the error covariance after an update with an arbitrary gain $\mathbf K$ ([Chapter 13](ch13_kalman_filter.md) derives this). The theorem gives the minimizer $\mathbf K_\star = \mathbf P^-\mathbf H^\top\mathbf S^{-1}$ and the minimum $f(\mathbf K_\star) = (\mathbf I - \mathbf K_\star\mathbf H)\mathbf P^-$. For $m = n = 1$, $f(k) = P^- - 2kP^-h + k^2(h^2P^- + R)$ is minimized at $k_\star = P^-h/(h^2P^- + R)$, the gain of [Chapter 11](ch11_measurement_functions.md).

    Part 1 resolves the unit problem raised under Vectors: the same $\mathbf K_\star$ minimizes $\mathbf w^\top f(\mathbf K)\mathbf w$, the error variance of every combination $\mathbf w^\top\mathbf e$, and hence also $\operatorname{tr}\big(\mathbf D f(\mathbf K)\mathbf D\big)$ for every diagonal rescaling $\mathbf D$ of the units. Minimizing the trace is a convenient way to find a gain that is optimal in every direction at once.

    /// caution | ⚠️ **Assumptions and Failure Modes**
        attrs: {class: no-icon}
    - **$\mathbf S$ must be positive definite.** If $\mathbf S$ has a negative eigenvalue, $\operatorname{tr}f$ is unbounded below and has no minimum; if $\mathbf S$ is only semidefinite and singular, $\mathbf M\mathbf S^{-1}$ is undefined and the minimizer, if any, is not unique. In the Kalman filter, $\mathbf R$ positive definite guarantees that $\mathbf S$ is positive definite.
    - **Layout conventions.** Formulas such as $\partial\operatorname{tr}(\mathbf A\mathbf X)/\partial\mathbf X = \mathbf A^\top$ hold for the "same shape as $\mathbf X$" convention used here; in the transposed convention the right side becomes $\mathbf A$.
    ///

    The code below checks the trace derivatives against finite differences.
    """)
    return


@app.cell
def _(mo, np):
    # jb: echo=true
    def numerical_gradient(f, X, h=1e-6):
        """Central-difference approximation of the matrix of partial derivatives df/dX."""
        G = np.zeros_like(X)
        for p in range(X.shape[0]):
            for q in range(X.shape[1]):
                E = np.zeros_like(X)
                E[p, q] = h
                G[p, q] = (f(X + E) - f(X - E)) / (2 * h)
        return G


    rng_grad = np.random.default_rng(7)
    X_grad = rng_grad.standard_normal((2, 3))
    A_grad = rng_grad.standard_normal((3, 2))   # for tr(A X)
    B_grad = rng_grad.standard_normal((3, 3))   # for tr(X B X^T); not symmetric

    grad_linear = numerical_gradient(lambda X: np.trace(A_grad @ X), X_grad)
    grad_quadratic = numerical_gradient(lambda X: np.trace(X @ B_grad @ X.T), X_grad)
    mo.plain_text(
        f"d tr(A X)/dX     == A^T:          {np.allclose(grad_linear, A_grad.T)}\n"
        f"d tr(X B X^T)/dX == X (B + B^T):  {np.allclose(grad_quadratic, X_grad @ (B_grad + B_grad.T))}"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - A vector in $\mathbb R^n$ is a function $\{1, \ldots, n\} \to \mathbb R$. The dot product gives lengths and angles, and Cauchy–Schwarz bounds it.
    - A matrix is a linear map whose $j$-th column is the image of $\mathbf e_j$. Multiplication is composition, so it is associative but not commutative. Transposes and inverses reverse products: $(\mathbf A\mathbf B)^\top = \mathbf B^\top\mathbf A^\top$, $(\mathbf A\mathbf B)^{-1} = \mathbf B^{-1}\mathbf A^{-1}$.
    - A square matrix is invertible if and only if $\mathbf A\mathbf x = \mathbf 0$ only for $\mathbf x = \mathbf 0$, if and only if it has rank $n$, if and only if $\det\mathbf A \ne 0$; a one-sided inverse is two-sided.
    - $\operatorname{tr}(\mathbf A\mathbf B) = \operatorname{tr}(\mathbf B\mathbf A)$, and the trace of an error covariance is the mean squared error.
    - Orthogonal matrices preserve lengths and angles and have determinant $\pm 1$; those with determinant $+1$ are rotations.
    - Eigenvalues are the roots of $\det(\lambda\mathbf I - \mathbf A)$. A symmetric matrix is $\mathbf Q\boldsymbol\Lambda\mathbf Q^\top$ with $\mathbf Q$ orthogonal and $\boldsymbol\Lambda$ real diagonal (spectral theorem). It is positive definite exactly when its eigenvalues are positive, and $\mathbf H\mathbf P\mathbf H^\top + \mathbf R$ is positive definite whenever $\mathbf R$ is.
    - Every positive definite matrix has exactly one Cholesky factor, computed in about $n^3/6$ steps; every square root maps the unit sphere onto the same covariance ellipsoid.
    - Schur complements give block inverses and the matrix inversion lemma, and (in Chapter 12) the covariance of a conditioned Gaussian.
    - $[\mathbf a]_\times\mathbf b = \mathbf a\times\mathbf b$, and rotations respect cross products.
    - $\exp(\mathbf A) = \sum_k\mathbf A^k/k!$ solves $\dot{\mathbf x} = \mathbf A\mathbf x$, so $\mathbf F = \exp(\mathbf A\Delta t)$; exponentials of skew-symmetric matrices are rotations.
    - $\partial\operatorname{tr}(\mathbf A\mathbf X)/\partial\mathbf X = \mathbf A^\top$ and $\partial\operatorname{tr}(\mathbf X\mathbf A\mathbf X^\top)/\partial\mathbf X = \mathbf X(\mathbf A + \mathbf A^\top)$; completing the square shows that $\mathbf M\mathbf S^{-1}$ minimizes the Kalman-type quadratic in every direction at once.

    ## What's Next

    This appendix has no successor of its own: return to the chapter that sent you here. If you are reading in order, continue with [Chapter 12](ch12_vectors_matrices_covariance.md), which turns these facts about matrices into facts about uncertainty: random vectors, covariance matrices, the multivariate normal distribution, and the Schur-complement formula for conditioning that is the Kalman update in disguise.
    """)
    return


if __name__ == "__main__":
    app.run()
