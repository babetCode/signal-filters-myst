# v2 Style Guide and Chapter Plan

This file is the shared reference for the `*.py` notebooks: the book structure, file conventions, notation, glossary-term allocation, running examples, and a brief for every chapter. Conventions marked **(proposed)** are new in v2 and have not been decided by the author yet. They are written so that a single regex can change them later.

`sync_notebooks.py` only converts `*.py` files, so this markdown file is never exported.

---

## 1. Book structure

### Main path

| File | Title | Subtitle |
|---|---|---|
| `index.py` | Home | |
| `introduction.py` | Introduction | Building Intuition |
| **Part 1: Choosing α** | | |
| `ch1_language_of_logic.py` | Language of Logic | From Statements to Proofs |
| `ch2_axioms_of_set_theory.py` | Axioms of Set Theory | From Axioms to Natural Numbers |
| `ch3_sets_for_probability.py` | Sets for Probability | Complements, Preimages, and Infinity |
| `ch4_probability_spaces.py` | Probability Spaces | Measuring Uncertainty |
| `ch5_random_variables.py` | Random Variables | From Outcomes to Numbers |
| `ch6_expectation_and_variance.py` | Expectation and Variance | Why Averaging Works |
| `ch7_optimal_alpha.py` | The Optimal α | Combining Two Noisy Estimates |
| `ch8_bayesian_view.py` | The Bayesian View | Priors, Likelihoods, and Posteriors |
| **Part 2: The Scalar Kalman Filter** | | |
| `ch9_noise_levels.py` | Noise Levels | The Scalar Kalman Filter |
| `ch10_process_models.py` | Process Models | Predicting the Next State |
| `ch11_measurement_functions.py` | Measurement Functions | When Sensors Measure Something Else |
| **Part 3: State Vectors** | | |
| `ch12_vectors_matrices_covariance.py` | Vectors, Matrices, and Covariance | Uncertainty in Many Dimensions |
| `ch13_kalman_filter.py` | The Kalman Filter | The Multivariate Filter |
| `ch14_kalman_filters_in_practice.py` | Kalman Filters in Practice | Tuning, Fusion, and Consistency |
| **Part 4: Nonlinearity** | | |
| `ch15_extended_kalman_filter.py` | The Extended Kalman Filter | Linearization |
| `ch16_unscented_kalman_filter.py` | The Unscented Kalman Filter | Sigma Points |
| **Part 5: Orientation** | | |
| `ch17_rotations.py` | Rotations | Frames, Matrices, and Singularities |
| `ch18_quaternions.py` | Quaternions | Singularity-Free Attitude |
| `ch19_ahrs.py` | Attitude and Heading Reference Systems | Fusing Gyroscopes, Accelerometers, and Magnetometers |
| **Part 6: Inertial Navigation for Gait** | | |
| `ch20_strapdown_inertial_navigation.py` | Strapdown Inertial Navigation | Dead Reckoning a Walking Foot |
| `ch21_zero_velocity_updates.py` | Zero-Velocity Updates | Gait Analysis with a Foot-Mounted IMU |

### Optional appendices (ground-up foundations)

| File | Title | Needed by |
|---|---|---|
| `appendix_a_formal_logic.py` | Appendix A: Formal Logic | Deepens Ch 1–2; nothing on the main path depends on it |
| `appendix_b_number_systems.py` | Appendix B: Constructing the Number Systems | Ch 3 uses its result (ℝ is a complete ordered field) |
| `appendix_c_calculus.py` | Appendix C: Calculus | Sequences/series before Ch 4; integrals before Ch 5; ODEs in Ch 10; Jacobians in Ch 15 |
| `appendix_d_linear_algebra.py` | Appendix D: Linear Algebra | All of Part 3 onward |

The main path never sacrifices precision: every definition is precise and every result is proven or explicitly cited. The appendices hold *foundational* material that a reader may already know. A main-path chapter that relies on an appendix result says so in its Prerequisites box and links to the section by name.

### Fixed appendix section names (`##` headings; link to these by name)

- **Appendix A:** Formal Syntax · Formal Semantics · Theories and Logical Consequence · Formal Proofs · Extension by Definitions · The Metatheory
- **Appendix B:** Arithmetic on the Natural Numbers · Equivalence Relations and Quotients · The Integers · The Rational Numbers · Incompleteness of the Rationals · The Real Numbers · Uniqueness of the Real Numbers
- **Appendix C:** Sequences and Limits · Series · Limits of Functions and Continuity · Derivatives · The Mean Value Theorem and Extrema · Taylor's Theorem · The Riemann Integral · The Fundamental Theorem of Calculus · Exponential and Logarithm · Improper Integrals · Functions of Several Variables · Multiple Integrals · Linear Differential Equations
- **Appendix D:** Vectors · Matrices and Linear Maps · Matrix Multiplication · Transpose, Identity, and Inverse · Linear Independence, Basis, and Rank · Determinants · Trace · Orthogonal Matrices · Eigenvalues and Eigenvectors · Symmetric and Positive Definite Matrices · Cholesky Decomposition · Block Matrices and the Schur Complement · Cross Products and Skew-Symmetric Matrices · The Matrix Exponential · Derivatives with Respect to Matrices

---

## 2. File conventions

### Skeleton (copy exactly)

```python
# /// script
# dependencies = [
#     "marimo>=0.25.1",
#     "matplotlib==3.11.2",
#     "numpy==2.5.3",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="The Optimal α", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "Combining Two Noisy Estimates"
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
    Prose goes here. One `mo.md` cell per subsection.
    """)
    return


if __name__ == "__main__":
    app.run()
```

- Only list dependencies the notebook actually imports. Allowed: `marimo>=0.25.1`, `matplotlib==3.11.2`, `numpy==2.5.3`, `pandas==3.0.6`, `schemdraw==0.23`, `scipy==1.18.1`.
- Keep `css_file="notebook-styles.css"`; the sync script comments it out.
- **LaTeX macros:** if a chapter uses custom macros (only Ch 1, Ch 2, Ch 3, Appendix A, and Appendix B use `\existsin`, `\forallin`, `\existssubseteq`, `\forallsubseteq`), define them in **both** places. That means the frontmatter `math:` block (for MyST) and an `include=false` cell that calls `mo.latex(...)` then `mo.output.clear()` (for the marimo editor, kept for development). Copy the exact pattern from `notebooks/ch1_language_of_logic.py`. Other chapters write `\operatorname{Var}`, `\mathbb E`, etc. explicitly; there are no new macros.

### Cells

- **Prose:** `@app.cell(hide_code=True)` + `def _(mo):` + `mo.md(r""" ... """)`. Content is indented 4 spaces inside the string; marimo dedents it on export.
- **Setup or figure-generating cells nobody should see:** first line `# jb: include=false`.
- **Code the reader should read** (reference implementations such as `kalman_filter(...)`) **(proposed):** a normal `@app.cell` whose first line is `# jb: echo=true`. The real executed code is then shown on the site. Do not duplicate it in a ```` ```python ```` block in markdown.
- **Interactive widgets:** define the UI element in its own cell, which may be `hide_code=True`. Read `.value` in a *different* cell, and display element and figure together with `mo.vstack([slider, graphic(fig)])` or `mo.hstack`.
- **marimo rules:**
  - Every global name is defined in exactly one cell.
  - Use `_`-prefixed names for cell-local variables (e.g. `_fig, _ax`).
  - The function signature must list every global the cell reads, and `return (a, b)` must list every global other cells use.
  - Use raw strings for anything with backslashes.
  - In `rf"""` strings, double literal braces (`{{ }}`), and remember that LaTeX braces count. Prefer small separate `mo.md(rf"...")` cells for dynamic numbers.
- **Computed markdown:** an `mo.md` cell whose text depends on other variables (an `rf"""` string with live values) is exported as a marimo code cell and rendered by marimo, not MyST. Inside such cells, `{term}` references, `[@cite]` citations, footnotes, and relative `.md` links will not work on the site. Keep computed cells to plain text and math, and put those features in static `mo.md(r"""...""")` cells whose only parameter is `mo`.
- **Determinism:** `rng = np.random.default_rng(<fixed seed>)`. Keep each notebook's runtime under about 20 s: vectorize, keep Monte Carlo sizes modest.
- **Never** call `eval`/`exec` on user input.

### Figures

- **Interactive figures:** render inline: build the matplotlib figure and output `graphic(fig)`.
- **Static figures and diagrams:** follow the existing convention.
  - An `include=false` cell saves an SVG to `Path(__file__).parent / "public" / "<chapter>_<name>.svg"`, e.g. `ch7_gain_curve.svg`. Start each name with the chapter, so no notebook overwrites another's figure in `public/`.
  - A separate `hide_code=True` markdown cell shows it with `<img src="public/ch7_gain_curve.svg" class="graphic" alt="..." />`.
- **Plot style:** default matplotlib style; axis labels with units; `ax.grid(visible=True, alpha=0.9, linewidth=0.4)`; italic titles (`style='italic'`).
- **Colour roles:**
  - measurements: hollow black circles, or C0 for dense streams
  - estimates: C1
  - truth: black solid line
  - predictions: red dotted
  - ±2σ bands: shaded C1 with alpha 0.2

### Admonitions (exact format; the sync regexes depend on it)

**Definition** (established). This becomes a MyST glossary entry, so `{term}` references work book-wide. The `<u>**Term**</u>` line must come immediately after the `attrs` line:

```
/// note | 📖 **Definition**
    attrs: {class: no-icon}
<u>**Covariance**</u>

The covariance of random variables $X$ and $Y$ with finite variances is
$$\operatorname{Cov}(X, Y) := \mathbb E\big[(X - \mathbb E X)(Y - \mathbb E Y)\big].$$
///
```

**Key Idea** (established): `/// attention | 🗝️ **Key Idea**` + `attrs: {class: no-icon}`.

**Tip** (established): `/// tip | **Title**` + `attrs: {class: no-icon}`.

**Theorem, Lemma, Corollary** **(proposed):**

```
/// important | 📐 **Theorem (Optimal Gain)**
    attrs: {class: no-icon}
Statement...
///

/// admonition | ✍️ **Proof**
    attrs: {class: no-icon}
Proof text... $\blacksquare$
///
```

Use the label `Theorem` for main results, `Lemma` for helper results, and `Corollary` for immediate consequences. **Do not use "Proposition" as a label**, because "statement" is the logic term and "proposition" would be ambiguous. When a proof is not given, the proof box says so and links to one.

**Prerequisites** **(proposed):** at the very top of every main-path chapter after the Introduction, list exactly what the chapter uses, with links:

```
/// seealso | 🔗 **Prerequisites**
    attrs: {class: no-icon}
- [Chapter 6](ch6_expectation_and_variance.md): variance of a weighted sum.
- [Appendix C: Derivatives](appendix_c_calculus.md) (optional; only for the alternative derivation).
///
```

**Assumptions and failure modes** **(proposed):** every major result gets one of these, stating its assumptions and what happens when each fails (the index's Understanding principle):

```
/// caution | ⚠️ **Assumptions and Failure Modes**
    attrs: {class: no-icon}
...
///
```

- Never nest admonitions.
- Do not use the hidden `:::{div}` heading trick.
- Footnotes (`[^name]`) must be defined in the same `mo.md` cell that references them.

### Links, terms, citations

- **Cross-chapter links:** use relative file links such as `[Chapter 7](ch7_optimal_alpha.md)` or `[Appendix D: Trace](appendix_d_linear_algebra.md)`. Do not use heading anchors or `(label)=` targets.
- **Glossary references:** use `{term}`variance`` or `{term}`variances <variance>``. Only reference terms that exist in the allocation table (§4) or that you define yourself.
- **Words used before their formal definition:** mark the first informal use with a footnote such as `[^informal-probability]: Used informally here; defined precisely in [Chapter 4](ch4_probability_spaces.md).`
- **Citations:**
  - Cite every published work (book, paper, preprint, datasheet) by its `content/refs.bib` key, not with an inline link to the work. Use whichever form reads best in the sentence:
    - `[@kalman1960]` renders as (Kalman, 1960). This is the usual form.
    - `@kalman1960` renders as Kalman (1960). Use it when the authors are part of the sentence.
    - `[@barshalom2002, Ch. 5]` or `@barshalom2002 [Ch. 5]` points to a chapter or section, and `[see @kalman1960]` adds a lead-in.
    - `[@godel1938; @cohen1963]` cites several works together.
  - Add a missing work to `content/refs.bib` before citing it, and leave the other entries as they are. Name the key after the first author and year (`kalman1960`); datasheets and undated works take a descriptive key (`avia_hx711_datasheet`).
  - Take an entry's details from its DOI record or publisher, never from memory. Give the `doi` if there is one, otherwise a `url`.
- **Web links:** use an inline markdown link for web resources that are not published works (Wikipedia, software and project websites). Only link URLs you are confident are correct.

### Writing principles (from `index.py`; non-negotiable)

1. **Concision, as the author defines it:** first include everything in the dependency hierarchy the key concept is built on, with complete understanding and precise definitions. Only then use as few words as possible. Never trade precision or completeness for brevity.
2. Define every word before it is used, and use it only with that meaning afterwards. A glossary definition must be a necessary-and-sufficient test.
3. Order concepts by dependency; nothing is used before it is introduced.
4. Start with a concrete example, then generalize.
5. Justify every step. Prove when possible; otherwise state precisely and link to a proof.
6. Give every chapter at least one meaningful interactive element.
7. State assumptions, and what happens when they fail.
8. Open each chapter with its key concept and why it matters for filtering. Close it with a short **Summary** and a **What's Next** paragraph linking to the next chapter.
9. Spell-check. Use American spelling. Use "Fraenkel", not "Frankel". AHRS = *attitude and heading reference system*.

---

## 3. Global notation

| Symbol | Meaning | Introduced |
|---|---|---|
| $k \in \mathbb N$ | time step; measurements start at $k = 1$; $k = 0$ is the initial condition | Intro |
| $x_k$ | true value (state) at step $k$ (scalar in Parts 1–2) | Intro |
| $z_k$ | measurement at step $k$ | Intro |
| $\hat x_k$ | estimate after incorporating $z_k$ | Intro |
| $\hat x_k^-$ | prediction: estimate of $x_k$ before $z_k$ is incorporated (**not** called "prior" until Ch 8) | Intro |
| $\tilde y_k := z_k - \hat x_k^-$ (later $z_k - h\hat x_k^-$, $\mathbf z_k - \mathbf H\hat{\mathbf x}_k^-$) | innovation | Intro |
| $\alpha$, later $K_k$ | gain; Ch 7 shows the optimal α and renames it $K_k$ | Intro / Ch 7 |
| $\Delta x_k$ | predicted change from step $k-1$ to $k$ | Intro |
| $e_k := \hat x_k - x_k$, $e_k^- := \hat x_k^- - x_k$ | estimation and prediction errors | Ch 7 |
| $v_k := z_k - x_k$ (or $z_k - h x_k$), $R$ | measurement noise and its variance | Ch 5 / Ch 7 |
| $w_k$, $Q$ | process noise and its variance | Ch 9 |
| $P_k$, $P_k^-$ | error variances of $\hat x_k$ and $\hat x_k^-$ | Ch 7 |
| $S_k$ | innovation variance (covariance) | Ch 9 |
| $(\Omega, \mathcal F, \mathbb P)$ | probability space; $\mathbb P$ is blackboard bold to avoid clashing with $P_k$ | Ch 4 |
| $\mathbb E$, $\operatorname{Var}$, $\operatorname{Cov}$ | expectation, variance, covariance | Ch 6 |
| $X, Y, Z$ | random variables are uppercase in Ch 4–6; Ch 7 explicitly switches to the filtering convention of lowercase $x_k, z_k, v_k$ for random quantities | Ch 5 / Ch 7 |
| $F_X$, $f_X$, $p_X$ | CDF, PDF, PMF of $X$ | Ch 5 |
| $\mathcal N(\mu, \sigma^2)$, $\mathcal N(\boldsymbol\mu, \boldsymbol\Sigma)$ | normal distribution | Ch 5 / Ch 12 |
| $\mathbb N = \{0, 1, 2, \ldots\}$, $\mathbb N^+ := \mathbb N \setminus \{0\}$ | natural numbers | Ch 2 / Ch 3 |
| $A^c := \Omega \setminus A$ | complement relative to an ambient set | Ch 3 |
| $f[A]$, $f^{-1}[B]$ | image and preimage of sets; square brackets distinguish them from $f(a)$ and the inverse function | Ch 3 |
| bold lowercase / bold uppercase | vectors / matrices (Part 3 on); scalars stay plain | Ch 12 |
| $\mathbf x_k, \mathbf P_k, \mathbf F, \mathbf B, \mathbf u_k, \mathbf H, \mathbf Q, \mathbf R, \mathbf K_k, \mathbf S_k, \mathbf I$ | KF quantities (Part 3) | Ch 13 |
| $f(\cdot)$, $h(\cdot)$, $\mathbf F_k = \partial f/\partial \mathbf x$, $\mathbf H_k = \partial h/\partial \mathbf x$ | nonlinear process and measurement functions and their Jacobians | Ch 15 |
| $\alpha_{\text{UT}}, \beta_{\text{UT}}, \kappa, \lambda$ | unscented-transform parameters (subscripted so they don't clash with gains α, β) | Ch 16 |
| $\Delta t$ | sample period | Ch 10 |
| $[\mathbf a]_\times$ | skew-symmetric (cross-product) matrix: $[\mathbf a]_\times \mathbf b = \mathbf a \times \mathbf b$ | App D / Ch 17 |

### Orientation conventions (Ch 17–21; must be identical in every chapter)

- **Navigation frame $n$:** local-level ENU: $x$ = East, $y$ = North, $z$ = Up. Gravity $\mathbf g^n = [0, 0, -g]^\top$ with $g = 9.81\ \text{m/s}^2$.
- **Body frame $b$:** FLU: $x$ = forward, $y$ = left, $z$ = up. At zero attitude the body frame coincides with ENU, facing East.
- $\mathbf R^n_b$ maps body coordinates to navigation coordinates: $\mathbf v^n = \mathbf R^n_b \mathbf v^b$.
- **Euler angles, ZYX (yaw–pitch–roll):** $\mathbf R^n_b = \mathbf R_z(\psi)\,\mathbf R_y(\theta)\,\mathbf R_x(\phi)$, with roll φ, pitch θ, yaw ψ. Elementary rotations are active and right-handed.
- **Quaternions:** Hamilton convention, scalar-first, $q = [q_w, q_x, q_y, q_z]$; product $\otimes$. $q^n_b$ rotates body to nav: $[0, \mathbf v^n] = q^n_b \otimes [0, \mathbf v^b] \otimes (q^n_b)^*$. Mention that the JPL convention differs.
- **Kinematics:**
  - $\dot{\mathbf R}^n_b = \mathbf R^n_b [\boldsymbol\omega^b]_\times$
  - $\dot q = \tfrac12\, q \otimes [0, \boldsymbol\omega^b]$
  - $\boldsymbol\omega^b$ is the body angular rate relative to the navigation frame (Earth rotation is neglected; say so).
- **Specific force:** $\mathbf f^b = (\mathbf R^n_b)^\top(\mathbf a^n - \mathbf g^n)$. At rest and level it reads $[0, 0, +g]$.
- **IMU models:**
  - $\boldsymbol\omega_m = \boldsymbol\omega^b + \mathbf b_g + \mathbf n_g$
  - $\mathbf f_m = \mathbf f^b + \mathbf b_a + \mathbf n_a$
  - Magnetometer: $\mathbf m_m = (\mathbf R^n_b)^\top \mathbf m^n + \mathbf n_m$, with $\mathbf m^n = [0, 22, -42]^\top\ \mu\text{T}$ (points North and down).
- **Error-state attitude convention** (Ch 19 and Ch 21): right/body-frame perturbation, $q = \hat q \otimes \delta q(\delta\boldsymbol\theta)$, $\mathbf R = \hat{\mathbf R}\,\operatorname{Exp}(\delta\boldsymbol\theta) \approx \hat{\mathbf R}(\mathbf I + [\delta\boldsymbol\theta]_\times)$.
- **Default IMU parameters:**
  - 100 Hz
  - gyro white-noise σ = 0.01 rad/s, gyro bias 0.01 rad/s per axis (constant or slow random walk)
  - accelerometer white-noise σ = 0.05 m/s², accelerometer bias 0.05 m/s² per axis
  - magnetometer noise σ = 0.5 μT

---

## 4. Glossary-term allocation

Each term is defined **exactly once**, in the chapter listed. Other chapters reference it with `{term}`. A writer who needs a term not listed here defines it in their own chapter after grepping `notebooks/*.py` for `<u>**Term**</u>` to make sure nobody else did.

- **Index:** Definition
- **Introduction:** Signal, Noise, Filter, Estimate, Prediction, Innovation, Exponential moving average
- **Ch 1:** Statement, Truth table, Tautology, Logically equivalent, Predicate, Quantifier, Necessary condition, Sufficient condition, Axiom, Theorem, Lemma, Corollary, Proof, Counterexample
- **Ch 2:** Subset, Empty set, Union, Intersection, Set difference, Power set, Ordered pair, Cartesian product, Relation, Function, Domain, Codomain, Range, Successor, Inductive set, Natural numbers
- **Ch 3:** Complement, Disjoint, Partition, Indexed family, Sequence, Image, Preimage, Injective, Surjective, Bijective, Composition, Inverse function, Equinumerous, Finite, Countable, Uncountable, Field, Ordered field, Upper bound, Supremum, Infimum, Complete ordered field, Absolute value, Interval, Extended real numbers
- **Ch 4:** Sample space, Outcome, Event, Sigma-algebra, Generated sigma-algebra, Borel sigma-algebra, Probability measure, Probability space, Conditional probability, Independent events, Almost surely
- **Ch 5:** Random variable, Distribution, Cumulative distribution function, Discrete random variable, Probability mass function, Continuous random variable, Probability density function, Uniform distribution, Normal distribution, Joint distribution, Joint density, Marginal density, Independent random variables, Independent and identically distributed, Stochastic process, Measurement noise
- **Ch 6:** Expected value, Variance, Standard deviation, Covariance, Correlation coefficient, Uncorrelated, Estimator, Estimator bias, Unbiased, Mean squared error, Sample mean
- **Ch 7:** Estimation error, Error variance, Gain, Optimal gain
- **Ch 8:** Conditional density, Prior, Likelihood, Posterior, Evidence, Minimum mean squared error estimator, Maximum a posteriori estimate, Bayes filter
- **Ch 9:** Sample variance, Quantization, Process noise, Random walk, White noise, Kalman filter, Steady-state gain, Innovation variance, Normalized innovation squared, Chi-squared distribution, Filter consistency
- **Ch 10:** System, System state, Process model, Control input, Deterministic, Linear system, Discretization, Autocorrelation
- **Ch 11:** Measurement model, Measurement function, Calibration, Least squares, Sensor bias
- **Ch 12:** Random vector, Mean vector, Covariance matrix, Cross-covariance matrix, Multivariate normal distribution, Mahalanobis distance, Confidence ellipse
- **Ch 13:** State-space model, State transition matrix, Measurement matrix, Process noise covariance, Measurement noise covariance, Kalman gain, Innovation covariance, Joseph form, Observability, Alpha-beta filter
- **Ch 14:** Normalized estimation error squared, Gating, Sensor fusion, Filter divergence, Sequential update
- **Ch 15:** Nonlinear system, Linearization, Extended Kalman filter
- **Ch 16:** Sigma points, Unscented transform, Unscented Kalman filter, Particle filter
- **Ch 17:** Reference frame, Rotation matrix, Special orthogonal group, Euler angles, Gimbal lock, Axis-angle representation, Rotation vector, Angular velocity
- **Ch 18:** Quaternion, Quaternion conjugate, Unit quaternion, Hamilton product, Double cover
- **Ch 19:** Inertial measurement unit, Gyroscope, Accelerometer, Specific force, Magnetometer, Attitude, Heading, Complementary filter, Error-state Kalman filter
- **Ch 20:** Strapdown inertial navigation, Dead reckoning, Drift, Gait cycle, Stance phase, Swing phase, Stride, Zero-velocity detector
- **Ch 21:** Zero-velocity update, Pseudo-measurement, Zero angular rate update, Stride length, Cadence, Gait speed, Foot clearance
- **App A:** Formula, Free variable, Bound variable, Sentence, Structure, Model, Theory, Logical consequence, Formal proof, Operation, Term, Conservative extension
- **App B:** Equivalence relation, Equivalence class, Quotient set, Integers, Rational numbers, Dedekind cut
- **App C:** Limit of a sequence, Convergent, Cauchy sequence, Series, Limit of a function, Continuous, Derivative, Differentiable, Riemann sum, Riemann integral, Antiderivative, Exponential function, Natural logarithm, Improper integral, Taylor polynomial, Partial derivative, Gradient, Jacobian, Differential equation
- **App D:** Vector, Dot product, Norm, Matrix, Linear map, Matrix product, Transpose, Identity matrix, Invertible matrix, Linear independence, Basis, Rank, Determinant, Trace, Orthogonal matrix, Eigenvalue, Eigenvector, Symmetric matrix, Positive definite, Positive semidefinite, Cholesky decomposition, Schur complement, Cross product, Skew-symmetric matrix, Matrix exponential

---

## 5. Running examples and canonical numbers

- **Bathroom scale (Intro, Ch 5–9):**
  - true weight 155 lb, constant while standing
  - HX711 at 10 samples/s (it supports 10 or 80 SPS)
  - measurement noise σ = 1 lb (R = 1 lb²), Gaussian, seed 1
  - 3 s of data: 30 samples
- **Bulking (Intro, Ch 9, 10, 13):**
  - 28 daily weigh-ins, starting at 155 lb
  - true gain 1.4 lb/week (0.2 lb/day)
  - daily reading noise σ = 1 lb (water and food fluctuations dominate)
  - person: age 23, height 175 cm, male, activity multiplier 1.5 (moderate)
  - Mifflin–St Jeor BMR; 3500 kcal per lb [@wishnofsky1958]
  - In Ch 10, TDEE is linear in weight, so the model is $x_k = a x_{k-1} + b u_k + c$ with $u_k$ = daily energy intake.
  - Canonical data (used by the Introduction; reuse it verbatim): `k = np.arange(1, 29); x_true = 155 + 0.2*(k-1); z = np.round(x_true + np.random.default_rng(2).normal(0, 1, 28), 1)`. Chapters that need a different truth (e.g. Ch 13's diet change) still use seed 2 for the measurement noise.
- **Load-cell counts (Ch 11):**
  - raw counts $z = h x + c + v$ with $h = 20{,}000$ counts/lb and offset $c = 85{,}000$ counts
  - noise σ = 20,000 counts (= 1 lb)
  - calibration plates: 0, 45, 90, 135 lb
- **1-D cart (Ch 14):** a position sensor at 10 Hz (σ = 0.5 m) plus an accelerometer at 100 Hz used as the control input; foreshadows Part 6.
- **Pendulum (Ch 15–16):**
  - $L = 1$ m, $g = 9.81$, light damping $c = 0.1\ \text{s}^{-1}$
  - state $[\theta, \omega]$; Δt = 0.01 s; dynamics integrated with RK4 for truth
  - measurement: horizontal bob position $L\sin\theta$ at 20 Hz, σ = 0.05 m
- **IMU (Ch 19–21):** see the default parameters in §3. The gait simulator is written in Ch 20 and copied verbatim into Ch 21 (notebooks are self-contained).

---

## 6. Chapter briefs

Each brief lists required content in dependency order. Writers may add material that serves the key concept, but must not drop required items. Where the author's existing notebooks already contain good material, reuse and improve it rather than rewriting from scratch:

- `notebooks/introduction.py`
- `notebooks/index.py`
- `notebooks/ch1_language_of_logic.py`
- `notebooks/ch2_axioms.py`
- `notebooks/ch3_numbers_probabilities.py`

### index

- Fix typos: speedometer, Download, prerequisite, knowledge, "it is preferable", "so that it can be accessible", "Kalman".
- Link to `introduction.md`.
- Remove the unused `base64`/`reveal_btn` code.
- Leave the guiding principles' wording unchanged except for typos.
- Add a short **How This Book Is Organized** section: the parts, the optional appendices, and when to read them. It can be a small table of what each part answers, mirroring the questions in the Introduction's What's Next section.

### introduction

Fix every issue from the review:

1. HX711 samples at 10 **or** 80 SPS.
2. Correct the memory motivation. A running sum and a count are also only two numbers. The real advantages of the recursive form are bounded magnitude (no overflow in fixed-width integers), an estimate available at every step, and the *prediction + gain × innovation* structure that generalizes to the Kalman filter.
3. Introduce $x_k$, $z_k$, $\hat x_k$ up front. Name the error and the innovation.
4. Replace every "increase the probability that the noise cancels out" with variance language, informal and marked, with a forward link to the σ²/k theorem in Ch 6.
5. State the zero-mean noise assumption directly in the text. Replace the placeholder `[test]` link with a link to Ch 6.
6. Motivate the EMA honestly. For a truly constant weight the 1/k average is better (proved optimal in Ch 7). The EMA is used because "constant" only holds approximately: the person shifts, steps on, and so on. State the lag-versus-noise trade-off, with a forward link to Ch 6.
7. Correct the EMA footnote weights: $n$ runs over $0 \le n \le k-1$; with first-measurement initialization, $z_1$ has weight $(1-\alpha)^{k-1}$.
8. Soften the "millions of scales" claim.
9. Rename "prior" to **prediction**, defined as the estimate of $x_k$ formed before $z_k$ is incorporated. "Prior" is reserved for Ch 8.
10. Distinguish the *expected* change $\Delta x_k$ from the *actual* change. Name the gap informally as process noise, with a forward link to Ch 9.
11. Make the alpha-filter simulation consistent and interactive. Truth rises at a known slope; sliders for α and $\Delta x$ show both the correct-Δx case and drift when Δx is wrong.
12. Switch the alpha-beta filter to the **standard form**: $\hat x_k = \hat x_k^- + \alpha\tilde y_k$, $\widehat{\Delta x}_{k+1} = \widehat{\Delta x}_k + \beta\,\tilde y_k$ (Δt = 1 day). Add a footnote noting that other texts scale β by $1/\Delta t$, or update from $\hat x_k - \hat x_{k-1}$, which is equivalent to $\beta = \alpha\beta'$. Finish the section with a working implementation, shown via `echo=true`, and an interactive plot on the 28-day bulking data with sliders for α, β, and the initial Δx. Delete the unused variables and dead cells.
13. Update the Summary to include β. Rewrite What's Next to describe the parts and the optional appendices, and remove "once I've finished".
14. Fix typos throughout. AHRS = attitude and heading reference system.
15. Make the `{term}`function`` link resolve to Ch 2's Function definition.
16. Write precise glossary definitions, flagged as informal where they rely on later concepts:
    - **Signal:** a function whose domain is a set of times (or positions) and whose values are the quantity being represented.
    - **Noise:** the difference between a measured signal and the true signal it represents; formalized in Ch 5.
    - **Filter:** an algorithm that maps a sequence of measurements to a sequence of estimates.
    - **Estimate**, **Prediction**, **Innovation**, **Exponential moving average.**

Keep the existing diagrams. Regenerate them, and fix "gauges".

### ch1_language_of_logic (main path; working logic, not formal grammar)

Goal: the reader can read and write precise mathematical statements and proofs. Reuse the good parts of the existing ch1 (the metalanguage/syntax/semantics distinction, truth tables), but move the formal grammar to Appendix A. Required content, in order:

- Why precision matters for filtering.
- Statements and truth values.
- Connectives ¬ ∧ ∨ → ↔ with truth tables. Explain vacuous truth for the conditional with an everyday example.
- Necessary and sufficient conditions. Tie them to the index's definition of "Definition".
- Tautologies and logical equivalence: double negation, De Morgan, contrapositive versus converse, distributive laws. Prove with truth tables.
- Predicates and variables.
- Quantifiers ∀, ∃: order matters, negating quantified statements, bounded quantifiers (with the `\existsin` macros), unique existence ∃!.
- The notation `:=` for definitions of objects and `:⟺` for definitions of properties.
- Axioms, definitions, theorems, lemmas, corollaries, and what a proof is. Proofs here are rigorous informal arguments that could be formalized; link to Appendix A.
- Proof techniques, each with a tiny example:
  - direct proof
  - contrapositive
  - contradiction
  - cases
  - proving ∃ by example
  - disproving ∀ by counterexample
  - proving ↔ in two directions
  - (induction comes in Ch 2)
- A filtering example of a direct proof: if $0 \le \alpha \le 1$ then $\hat x_k$ lies between $\hat x_{k-1}$ and $z_k$.
- **Interactive:** a truth-table generator for a chosen or typed formula in P, Q, R. Use a small safe parser, never `eval`.

### appendix_a_formal_logic

- The full formal treatment: the existing ch1 syntax and semantics content (symbols, formulas, free and bound variables, sentences, substitution, abbreviations table, structures, truth clauses), with the fixes from the review:
  - the garbled "structure" sentence
  - the list/paragraph blank lines
  - the wrong cross-reference
  - the *theory* versus *structure* distinction for axioms
- Models and satisfaction ⊨. Theories and logical consequence.
- A concrete deductive system: logical axioms + modus ponens + generalization (Enderton-style), with a short worked formal derivation.
- Soundness and completeness (Gödel 1929), stated with links.
- Extension by Definitions: move the existing ch2 "Defined Terms" material here (operations, terms, unpacking, provisos, conservative extension), with its fixes.
- The Metatheory:
  - the intended "structure of all sets" is a proper class
  - the metatheory is informal/naive set theory
  - Gödel's second incompleteness theorem means ZFC cannot prove its own consistency, so we assume it
- **Interactive:** e.g. a free/bound-variable highlighter for a small set of formulas, or a structure checker on a finite domain where the reader edits a small ∈-relation.

### ch2_axioms_of_set_theory

- Set and membership as primitive notions; explain why there is no glossary entry.
- For each ZFC axiom, in this order: the axiom in words, then symbols, then what it lets us build. Define each operation **immediately** after the axiom that justifies it, so nothing is used before it is defined.
  1. Extensionality: uniqueness, which justifies naming sets. Give a one-paragraph explanation and link to Appendix A: Extension by Definitions.
  2. Empty Set.
  3. Pairing, and singletons.
  4. Union, with binary ∪ defined right here.
  5. Separation:
     - set-builder notation
     - binary ∩
     - general $\bigcap A := \{x \in \bigcup A : \forall a \in A\,(x \in a)\}$ with the proviso $A \ne \emptyset$, explaining why
     - set difference
  6. Power Set.
  7. Replacement, and $\{f(x) : x \in A\}$ notation (the existing set-builder material, cleaned up).
  8. Infinity (using succ, now definable).
  9. Regularity: one paragraph, plus the proof that $x \notin x$.
  10. Choice: motivate it with a forward link to the Vitali set in Ch 4.
- **Building blocks** under their own `##` heading:
  - ordered pairs, with a *full* proof of the characteristic property (case split)
  - Cartesian product: $\{a\},\{a,b\} \subseteq X\cup Y$, so $(a,b) \in \mathcal P(\mathcal P(X\cup Y))$; fix the old subset/element error and the "B ∈ Y" typo
  - relations
  - functions: domain, codomain, range, $f: X \to Y$, $Y^X$, the proviso on function application
- **Natural Numbers** under their own `##` heading:
  - successor, inductive sets (defined once), ℕ
  - Theorem (Induction), with proof
  - Lemma: every natural number is transitive. Theorem: succ is injective, with proof. 0 is not a successor.
  - The Recursion Theorem, with a polished proof, plus the parameterized variant $h(n+1) = g(n, h(n))$. Explicitly connect it to the filter recursion $\hat x_k = g(k, \hat x_{k-1})$.
  - Arithmetic and order on ℕ defined by recursion. Properties are proven in Appendix B.
- **Interactive:** e.g. a von Neumann numeral explorer (slider n, showing the nested-brace form and its elements), or a power-set builder.

### appendix_b_number_systems

Move the existing ch2 ℕ-arithmetic-to-ℝ material here, fixed:

- Delete the duplicate Integers section.
- Equivalence relations and quotients, and the well-definedness lemma.
- Prove associativity and commutativity of + on ℕ fully; other ℕ properties can be proven or sketched with links.
- ℤ and ℚ, keeping the existing compatibility checks.
- Incompleteness of ℚ, with a *full* proof that $\{q : q < 0 \lor q^2 < 2\}$ has no supremum in ℚ.
- ℝ via Dedekind cuts: order, least-upper-bound property, arithmetic.
- The theorem that ℝ is a complete ordered field.
- Uniqueness up to isomorphism, stated with a link.
- The identification remark.
- **Interactive:** a √2 cut explorer (rationals in the cut versus out, for a chosen denominator bound).

### ch3_sets_for_probability

Prerequisites box: Ch 2. Also: Appendix C: Sequences and Limits and Series **must** be read before Ch 4.

- Complement and De Morgan's laws, finite and indexed, with proofs.
- Disjoint, pairwise disjoint, partitions.
- Indexed families, sequences, indexed ∪ and ∩ via Replacement and Union.
- Finite sums Σ defined by recursion.
- Image and preimage:
  - Lemma: preimage preserves ∪, ∩, complement, with proof
  - counterexample showing image does not preserve ∩
  - remark: this is why random variables are defined with preimages
- Injective, surjective, bijective; composition; inverse functions.
- Equinumerous, finite, countable, uncountable:
  - ℕ×ℕ countable (explicit pairing bijection), ℤ and ℚ countable
  - countable unions of countable sets are countable; flag that this uses countable choice
  - Cantor's theorem (no surjection $X \to \mathcal P(X)$)
- ℝ as a complete ordered field:
  - the axioms
  - a pointer to the Appendix B construction and uniqueness
  - Archimedean property and density of ℚ, proven from the least-upper-bound property
  - absolute value and the triangle inequality
  - intervals
- ℝ is uncountable, by the nested-interval proof using only the least-upper-bound property.
- Extended reals $[0, \infty]$ and their arithmetic conventions, needed for measures.
- **Interactive:** e.g. Cantor zig-zag enumeration of ℚ⁺ (slider for how many terms), or a preimage explorer.

### ch4_probability_spaces

Reuse and improve the existing `ch3_numbers_probabilities.py` material (coin toss, random rational, random number in [0,1]).

- Motivation: a scale reading displayed to 0.1 lb.
- Sample space, outcome, event.
- σ-algebra:
  - a finite example
  - Lemma: an intersection of σ-algebras is a σ-algebra
  - generated σ-algebra, Borel σ-algebra
- Kolmogorov's axioms; probability measure and probability space.
- Consequences, all with proofs: $\mathbb P(\emptyset)=0$, finite additivity, complement rule, monotonicity, union bound, two-set inclusion–exclusion, continuity from below and above (uses App C limits).
- Why not every subset can be an event: a full Vitali-set proof using Choice, translation invariance mod 1, and countable additivity.
- Existence of Lebesgue measure on the Borel sets, stated precisely with a link (Carathéodory).
- Almost surely.
- Conditional probability, the law of total probability, Bayes' theorem for events, all with proofs. Reuse the three-card-monte example.
- Independence of events, pairwise versus mutual, with a counterexample.
- **Interactive:** simulated coin/die relative frequencies with a slider for n. Label it an experiment whose convergence is *proven* in Ch 6.

### ch5_random_variables

- Random variable as a measurable function $\Omega \to \mathbb R$, with the Borel σ-algebra on ℝ; uses Ch 3's preimage lemma. Example: scale noise.
- Distribution as the push-forward measure.
- CDF, with its properties and proofs.
- Discrete random variables and PMFs.
- Continuous random variables and PDFs, via the Riemann integral of App C. Note the Lebesgue generalization with a link.
- Uniform distribution. Normal distribution: $\int e^{-x^2/2}dx = \sqrt{2\pi}$ via App C: Multiple Integrals.
- Functions of a random variable: the PDF of $aX+b$, with proof; quantization noise as a uniform distribution.
- Joint distributions, joint density, marginal density.
- Independent random variables (factorization), i.i.d.
- Sums of independent random variables: convolution, proven for the discrete case and stated for densities.
- Stochastic processes; a signal as a stochastic process, connecting back to the Introduction's Signal definition.
- The measurement-noise model $z_k = x_k + v_k$, $v_k$ i.i.d. $\mathcal N(0, \sigma^2)$, as an *assumption*, with failure modes: quantization, outliers, drift, correlated noise.
- **Interactive:** histogram of simulated scale noise versus the normal PDF, with sliders for μ, σ, and n.

### ch6_expectation_and_variance

- Expected value (discrete sum / continuous integral, existence via absolute convergence); the general Lebesgue definition linked.
- LOTUS: proven for discrete, stated for continuous.
- Linearity: proven for discrete and for joint densities.
- Independence implies $\mathbb E[XY] = \mathbb E X\,\mathbb E Y$.
- Variance, standard deviation; $\operatorname{Var}(aX+b)$.
- Covariance and correlation; uncorrelated does not imply independent (counterexample).
- Variance of sums.
- Estimator, estimator bias, unbiased, mean squared error; prove MSE = bias² + variance.
- Sample mean: unbiased, variance σ²/k (this retroactively justifies the Introduction).
- Markov and Chebyshev inequalities, and the weak law of large numbers, all with proofs.
- **EMA analysis**, the key payoff:
  - With first-measurement initialization and constant $x$, the EMA is unbiased with exact variance $\sigma^2\big[(1-\alpha)^{2(k-1)} + \alpha^2\tfrac{1-(1-\alpha)^{2(k-1)}}{1-(1-\alpha)^2}\big] \to \sigma^2\tfrac{\alpha}{2-\alpha}$.
  - For a ramp $x_k = ck$, the noise-free steady-state lag is $e = -c\tfrac{1-\alpha}{\alpha}$.
  - Therefore $\text{MSE}(\alpha) \approx c^2(1-\alpha)^2/\alpha^2 + \sigma^2\alpha/(2-\alpha)$, which has an interior optimum.
- **Interactive:** α slider showing bias², variance, and MSE curves, plus a Monte Carlo check.

### ch7_optimal_alpha (the centerpiece of Part 1)

- Switch to the filtering convention: lowercase random quantities, explicitly announced.
- Setup: $\hat x^- = x + e^-$, $z = x + v$, $\mathbb E e^- = \mathbb E v = 0$, $\operatorname{Var} = P^-, R$, uncorrelated (independence is not needed).
- For every α the estimator is unbiased.
- Error variance $P(\alpha) = (1-\alpha)^2P^- + \alpha^2R$. Complete the square (no calculus needed): $\alpha^* = P^-/(P^-+R)$, $P = (1-\alpha^*)P^- = P^-R/(P^-+R)$, $1/P = 1/P^- + 1/R$. Prove $P < \min(P^-, R)$. Cover the limiting cases.
- **Theorem:** for a constant $x$ with first-measurement initialization, the optimal gains are exactly $1/k$ and $P_k = R/k$ (by induction). The Introduction's cumulative average was optimal.
- Assumptions and failure modes:
  - correlated errors: derive the general $\alpha^* = (P^- - c)/(P^- + R - 2c)$, and show overconfidence if correlation is ignored
  - bias
  - mis-specified variances: still unbiased; compute the actual variance with the wrong α
  - "optimal" means among linear combinations; Ch 8 covers optimality among all estimators
- Rename α to the gain $K_k$.
- **Interactive:**
  - sliders for $P^-$ and $R$, showing α*, P, and the two Gaussians combining
  - a Monte Carlo histogram check
  - a sequential constant-weight demo comparing 1/k with an EMA

### ch8_bayesian_view

- Conditional densities; Bayes' theorem for densities.
- Formal Prior, Likelihood, Posterior, Evidence. Remark that this is the term the Introduction deliberately avoided.
- Gaussian prior × Gaussian likelihood gives a Gaussian posterior with exactly Ch 7's mean and variance, proven by completing the square.
- MMSE estimator: $\mathbb E[X \mid Z]$ minimizes $\mathbb E[(X-g(Z))^2]$, proven for densities. For jointly Gaussian variables it is linear, so Ch 7's estimator is optimal among *all* estimators under Gaussian assumptions.
- MAP estimate.
- A non-Gaussian counterexample where the best linear estimator is not the MMSE (e.g. outlier-mixture noise), made interactive.
- The central limit theorem, stated precisely with a link, plus an interactive demo (sums of uniforms).
- Bayes filter recursion: predict (Chapman–Kolmogorov / convolution) and update (Bayes).
- **Interactive:** a discrete histogram (grid) Bayes filter on the scale example, showing it matches the Kalman result for Gaussians.

### ch9_noise_levels

- Estimating R:
  - sample variance, with a proof of Bessel's correction
  - datasheets
  - quantization variance Δ²/12, with proof
  - Allan variance pointer
- Process noise and the random-walk model $x_k = x_{k-1} + \Delta x_k + w_k$; prove $P_k^- = P_{k-1} + Q$.
- White noise.
- **The scalar Kalman filter:** the predict/update algorithm as an `echo=true` implementation. Define the Kalman filter.
- Q = 0 recovers 1/k (Ch 7).
- Steady state: derive $p = (Q + \sqrt{Q^2 + 4QR})/2$, $K_\infty = p/(p+R)$. **Theorem:** the steady-state KF is exactly an EMA with α = K∞. This answers the Introduction's EMA question.
- Innovations: mean 0, variance $S_k = P_k^- + R$, uncorrelated over time (prove what is provable).
- NIS and the χ² distribution (1 degree of freedom, mean 1); a filter-consistency test; mis-tuning demo.
- **Interactive:**
  - Q and R sliders on scale data where the person shifts weight
  - the same on the bulking data
  - an NIS histogram

### ch10_process_models

- System, system state, process model, deterministic versus stochastic, control input, linear system.
- Scalar linear model $x_k = a x_{k-1} + b u_k + w_k$; prove $\hat x^- = a\hat x + bu$, $P^- = a^2P + Q$.
- The bulking energy-balance model, linear because TDEE is linear in weight (derive $a$ and $b$). KF with this model versus the random-walk model on data with varying daily intake (logging error becomes process noise).
- Continuous-time models and discretization: exact $e^{a\Delta t}$ versus Euler, with a link to App C: Linear Differential Equations.
- Rate models: alpha-beta needs two numbers, which motivates Part 3.
- Model mismatch; validation via innovation autocorrelation (whiteness).
- "There is no best model": how to evaluate one.
- **Interactive:** a model-choice toggle and a noise slider.

### ch11_measurement_functions

- Measurement model $z = hx + c + v$ with HX711 counts.
- Calibration by least squares from known plates: derive the normal equations for a line fit, using App C partial derivatives or completing the square.
- Filtering counts directly: derive the gain $K = P^-h/(h^2P^- + R)$ and the innovation $z - (h\hat x^- + c)$.
- Sensor bias; drifting tare offset as a second unknown.
- Observability intuition: one measurement cannot separate $x$ and $c$; an empty-platform reading helps. This motivates state vectors.
- Measuring a different quantity than desired in general; a nonlinear $h$ preview, forward-linked to Ch 15.
- **Interactive:** calibration-plate noise slider; filtering in counts.

### ch12_vectors_matrices_covariance

- A short recap list of the linear-algebra facts used, each linked to its App D section.
- Random vectors, mean vector.
- Covariance matrix: symmetric and positive semidefinite, with proof.
- $\operatorname{Cov}(\mathbf A\mathbf x + \mathbf b) = \mathbf A\boldsymbol\Sigma\mathbf A^\top$, with proof.
- Cross-covariance.
- Multivariate normal: the PDF; affine transformations, proven for invertible $\mathbf A$ via App C change of variables, otherwise cited; marginals.
- **Conditioning a joint Gaussian** via the Schur complement, derived. This is the Kalman update in disguise.
- Confidence ellipses via eigendecomposition; Mahalanobis distance and χ².
- **Interactive:** ellipse with σx, σy, ρ sliders and a sample cloud.

### ch13_kalman_filter

- State-space model with $\mathbf F, \mathbf B, \mathbf H, \mathbf Q, \mathbf R$ and stated assumptions.
- Predict equations, with proof.
- Update for an arbitrary gain: the Joseph form $\mathbf P = (\mathbf I-\mathbf K\mathbf H)\mathbf P^-(\mathbf I-\mathbf K\mathbf H)^\top + \mathbf K\mathbf R\mathbf K^\top$, with proof.
- Minimize the trace (App D: Derivatives with Respect to Matrices): $\mathbf K = \mathbf P^-\mathbf H^\top\mathbf S^{-1}$, and the simplified $\mathbf P = (\mathbf I-\mathbf K\mathbf H)\mathbf P^-$. Note this is valid only at the optimal gain, which is why the Joseph form exists.
- Cross-check: the same result follows from Ch 12 Gaussian conditioning.
- `echo=true` NumPy implementation.
- Two-state bulking [weight, rate] with a diet change mid-way.
- **Alpha-beta revisited:** the steady-state KF gains $[\alpha, \beta/\Delta t]^\top$. Compute them by iterating the Riccati equation, and compare with Kalata's tracking-index relations (with a citation).
- Observability: rank test, with the tare-offset example from Ch 11.
- **Interactive:** σ_a and R sliders.

### ch14_kalman_filters_in_practice

- Initialization (large $\mathbf P_0$).
- Choosing Q: piecewise-constant versus continuous white-noise acceleration; discretize via the integral (App C/D).
- Sequential updates, missing measurements, multi-rate operation.
- Sensor fusion on the 1-D cart: position at 10 Hz, accelerometer at 100 Hz as control input.
- Outlier gating via NIS thresholds.
- NEES/NIS Monte Carlo consistency tests.
- Numerical stability: symmetrize, Joseph form, square-root filters mentioned.
- A divergence demo where Q is too small during a maneuver.
- RTS smoother mentioned with a link.
- **Interactive:** Q, R, and dropout-rate sliders.

### ch15_extended_kalman_filter

- Nonlinear systems.
- How a Gaussian transforms through a nonlinearity: Monte Carlo versus linearized mean and variance, interactive.
- Linearization via Jacobians (App C).
- The EKF algorithm.
- Pendulum example: derive $f$, $h$, and their Jacobians; `echo=true` implementation; numerical Jacobian check.
- Failure modes: large initial error, strong nonlinearity, bad Jacobians. Mention the iterated EKF.
- **Interactive:** initial-error and noise sliders.

### ch16_unscented_kalman_filter

- The unscented transform: sigma points; Merwe scaled weights ($\alpha_{\text{UT}}, \beta_{\text{UT}}, \kappa, \lambda$); matrix square root via Cholesky (App D).
- Accuracy statement: mean and covariance correct to second order; cite a source, then demonstrate.
- The UKF algorithm on the same pendulum, compared with the EKF.
- Particle filters: the idea, with a link to Labbe's book.
- When to choose which filter.
- **Interactive:** UT versus linearization versus Monte Carlo for a chosen nonlinearity and spread.

### ch17_rotations

Use the §3 conventions throughout.

- Reference frames.
- Rotation matrices and SO(3): orthogonal with determinant +1, with proofs of the key properties; passive versus active, stated explicitly; composition order.
- Elementary rotations and ZYX Euler angles, to and from matrices (atan2).
- **Gimbal lock:** derive the Euler-rate equation $\dot{\boldsymbol\Theta} = \mathbf E(\phi,\theta)\boldsymbol\omega$ and show that $\mathbf E$ is singular at θ = ±90°. Show two different angle triples giving the same matrix.
- Axis-angle representation and Rodrigues' formula, with proof.
- Rotation vector; exp/log maps (matrix exponential of a skew matrix).
- Angular velocity: derive $\dot{\mathbf R} = \mathbf R[\boldsymbol\omega]_\times$ from $\mathbf R^\top\mathbf R = \mathbf I$.
- Small-angle approximation.
- Why every three-parameter representation has singularities: state it and link to the topological argument.
- **Interactive:** 3-D axes with yaw, pitch, and roll sliders showing gimbal lock.

### ch18_quaternions

- ℍ and the Hamilton product: non-commutative; associativity proven or cited.
- Scalar–vector form; conjugate; norm (multiplicative, with proof); inverse.
- Unit quaternions; rotation $q\,v\,q^*$, with proof that it is a rotation and the axis-angle form $[\cos\tfrac\theta2, \sin\tfrac\theta2\mathbf u]$.
- Double cover.
- Conversions to and from $\mathbf R$, axis-angle, and Euler angles; composition order.
- Kinematics $\dot q = \tfrac12 q\otimes[0,\boldsymbol\omega]$, derived.
- Exact discrete integration with the exponential map for constant ω; a normalization-drift demo.
- Slerp (optional).
- Note the Hamilton versus JPL conventions.
- **Interactive:** a rotating body with live quaternion components; gimbal lock avoided.

### ch19_ahrs

- IMU sensors and their models (§3); specific force.
- Tilt from the accelerometer (derive roll and pitch for FLU/ENU); tilt-compensated heading from the magnetometer.
- Gyro integration drift.
- **Complementary filter:**
  - scalar pitch first; show it is *exactly* the Introduction's alpha filter with $\Delta x_k = \omega_k\Delta t$
  - frequency interpretation; time constant $\tau = \Delta t(1-\alpha)/\alpha$
- **Error-state (multiplicative) EKF:**
  - nominal $\hat q$, $\hat{\mathbf b}_g$; error state $[\delta\boldsymbol\theta, \delta\mathbf b_g]$
  - right-perturbation convention
  - derive the error dynamics, propagation, and the accelerometer-gravity and magnetometer updates
  - reset step
- Simulation with synthetic motion and linear accelerations.
- Failure modes: linear acceleration (adaptive R or gating on $|\mathbf f| \approx g$), magnetic disturbances, unobservable yaw without a magnetometer.
- Mahony and Madgwick filters, linked.
- **Interactive:** sliders for α, gyro bias, and linear-acceleration magnitude.

### ch20_strapdown_inertial_navigation

- Strapdown mechanization: attitude update (Ch 18), $\dot{\mathbf v}^n = \mathbf R^n_b\mathbf f^b + \mathbf g^n$, $\dot{\mathbf p}^n = \mathbf v^n$; discrete implementation at 100 Hz.
- Error growth, derived:
  - accelerometer bias gives a $\tfrac12 b t^2$ position error
  - tilt error δθ gives about $\tfrac12 g\,\delta\theta\,t^2$
  - gyro bias gives about $\tfrac16 g\,b_g t^3$
- **Interactive** drift demo.
- Why consumer IMUs cannot navigate freely for more than seconds.
- Gait: the gait cycle (heel strike, foot flat, heel off, toe off, swing); stance ≈ 60%; the foot is stationary at foot-flat.
- **Synthetic gait simulator**, a reusable function:
  - stance/swing timing
  - forward displacement via a minimum-jerk profile
  - clearance bump
  - foot pitch during swing
  - optional turns
  - true $\boldsymbol\omega^b$ and $\mathbf f^b$ from the analytic trajectory
  - noise and bias added per §3
- Zero-velocity detectors: acceleration-magnitude and gyro thresholds, and the SHOE/GLRT statistic [@skog2010]. Evaluate them on the synthetic data.
- Dead reckoning without ZUPT diverges (demo).

### ch21_zero_velocity_updates

- ZUPT as a pseudo-measurement $\mathbf v^n = \mathbf 0$.
- Error-state EKF with 15 states $[\delta\mathbf p, \delta\mathbf v, \delta\boldsymbol\theta, \delta\mathbf b_a, \delta\mathbf b_g]$:
  - derive the linearized INS error model in the §3 convention
  - continuous $\mathbf F$, discretization $\mathbf I + \mathbf F\Delta t$, $\mathbf Q$
  - $\mathbf H = [\mathbf 0\ \mathbf I\ \mathbf 0\ \mathbf 0\ \mathbf 0]$
  - update, feedback, and reset
- Results on the Ch 20 synthetic gait (simulator copied verbatim): with versus without ZUPT.
- Observability: yaw and z-gyro bias are unobservable from ZUPT, which causes heading drift. ZARU for gyro bias. Heading aids: magnetometer, heuristic drift elimination.
- Gait parameters per stride:
  - stride length
  - stride time
  - cadence
  - gait speed
  - foot clearance
  - turning angle
- A table comparing estimates with ground truth.
- Failure modes: running (short stance), stairs, detector thresholds, saturation.
- Further reading, as citations: [@foxlin2005], [@skog2010], [@nilsson2012] (OpenShoe), [@jimenez2009].
- **Interactive:** detector-threshold and noise sliders, plus a trajectory plot.

### appendix_c_calculus

Sections as listed in §1. Rigorous ε definitions. Prove:

- limit laws
- monotone convergence (from the least-upper-bound property)
- geometric series
- derivative rules
- Rolle's theorem and the MVT; EVT (prove via Bolzano–Weierstrass, or cite)
- Taylor's theorem with the Lagrange remainder
- both parts of the FTC
- integration by parts and substitution

Also:

- exp defined as a power series, with its key properties (prove or cite $e^{a+b}=e^ae^b$); ln as its inverse
- improper integrals
- multivariable: partial derivatives, gradient, Jacobian (arranged as an array; forward link to App D for matrices), the chain rule stated, first-order Taylor
- Fubini and polar change of variables stated precisely with links, then the Gaussian integral proved from them
- linear ODEs $\dot x = ax + bu$: integrating-factor solution and exact discretization
- **Interactive:** ε–N visualizer, Riemann-sum slider, Taylor-degree slider, linearization of sin.

### appendix_d_linear_algebra

Sections as listed in §1:

- vectors in ℝⁿ as functions $\{1..n\} \to \mathbb R$ (Ch 3), dot product, norm
- matrices as linear maps; multiplication as composition
- transpose, identity, inverse
- linear independence, basis, rank (brief)
- determinants: 2×2 and 3×3; general properties stated, with links
- trace, with the cyclic property proven
- orthogonal matrices
- eigenvalues and eigenvectors
- the spectral theorem: stated; proven for 2×2 or linked
- positive (semi)definite matrices
- Cholesky decomposition (existence for PD, with an algorithm)
- block matrices, the Schur complement, and the matrix inversion lemma (with proof)
- cross product and skew-symmetric matrices
- the matrix exponential (series, key properties)
- trace derivatives $\partial\operatorname{tr}(\mathbf{AX})/\partial\mathbf X$ and $\partial\operatorname{tr}(\mathbf X\mathbf A\mathbf X^\top)/\partial\mathbf X$, with proofs
- **Interactive:** a 2×2 matrix acting on the unit square and circle, with eigenvectors shown.

---

## 7. Verification (every notebook)

Run:

```
"%TEMP%/sigfilt-venv/Scripts/python" "%TEMP%/sfcheck/verify_nb.py" notebooks/<file>.py
```

From Git Bash, the same command is `"$TEMP/sigfilt-venv/Scripts/python" "$TEMP/sfcheck/verify_nb.py" notebooks/<file>.py`.

The script:

- executes the notebook
- runs `marimo check`
- exports to MyST into `%TEMP%/sfcheck/out/` (never into the repo)
- flags malformed admonitions and `{term}` references or duplicate definitions

Fix the notebook until it reports `[RUN] ok`, `[CHECK] ok`, and `[EXPORT] ok`. Unresolved `{term}` references are fine only if the allocation table assigns the term to another chapter. Running a notebook writes its SVGs into `notebooks/public/`; that is expected.

Do not modify any file other than your assigned `*.py` files and their `public/*.svg` outputs, except to add citation entries to `content/refs.bib`. In particular, leave the rest of `content/` (including `myst.yml`), `scripts/`, and other notebooks untouched.
