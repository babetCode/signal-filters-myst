# /// script
# dependencies = [
#     "marimo>=0.25.1",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="Home", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    abbreviations:
      hover over terms: like this
    numbering:
      equations: false
    -->
    """)
    return


@app.cell
def imports():
    # jb: include=false
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It's impossible to measure anything in the real world with 100% precision. Whether it's a bathroom scale measuring your weight, a car speedometer measuring wheel rotation, a pacemaker measuring heart beats, or an airplane measuring flight trajectory, there will always be some uncertainty. Signal filters are used to reduce this uncertainty and make better estimates of the true values we are trying to measure.

    Humans generally have intuition on handling imperfect data: when making hard decisions, they consult multiple people (a type of social measurement) and decide based on a combination of the input received and their understanding of the situation. They understand that some input is more trustworthy and should be more heavily considered than others. Moreover, most people understand that getting more input can lead to better understanding even if no single piece of input is perfect.

    By combining multiple measurements and knowledge about what's being measured, signal filters can follow a somewhat analogous process to estimate some unknown quantity. To see what this might look like, you can skip ahead to the [Introduction](introduction.md) where we walk through some examples.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Motivation

    My goal for this project was to write an intuitive (and mostly rigorous) guide to Kalman filtering. I was inspired by [Kalman and Bayesian Filters in Python](https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python), a fantastic book by Roger Labbe. However, I wanted to do a couple of things differently:

    1. His book is written as a collection of `.ipynb` files, so to read it you can:
        - Download the notebooks from GitHub, set up a conda environment, run a local Jupyter server, and read the book from the local server (this is the recommended way)[^running-kbfp-locally].
        - Read a copy of the files hosted on nbviewer.org (this is usually slow or inaccessible due to rate limiting).
        - Read the PDF export of the book from Labbe's Google Drive (which loses all interactivity and sometimes does not exactly match the notebook source)[^kbfp-clone-repo].

    2. His book makes complex concepts very intuitive to understand, but sometimes forgoes precision in favor of simplicity. His goal was to make a simplified, introductory text, as he states in his preface: "If you are a hobbyist this book should provide everything you need. If you are serious about Kalman filters you’ll need more."

    By using [jupyter-book-marimo](https://github.com/marimo-team/jupyter-book-marimo) to publish content to the web, I can get the best of both worlds: interactive code in the browser without any downloads or configuration on the user end. My goal in writing this is to bridge the gap between introduction and textbook, so that it can be accessible to more readers while still using precise language.

    [^running-kbfp-locally]: At the time of Labbe's writing, this was the best option available for reactive notebooks. However, he also notes in his documentation, "this is admittedly a somewhat cumbersome interface to a book."

    [^kbfp-clone-repo]: To get around this, I have also created a [fork of his book](https://github.com/babetCode/Kalman-and-Bayesian-Filters-in-Python) on GitHub which
        - Includes a `pyproject.toml` file, so that if you have [uv](https://docs.astral.sh/uv/) installed you can run the book immediately with a single command.
        - Publishes the `.ipynb` files to a [jupyter-book](https://jupyterbook.org/) so that you can read on the web without downloading (not interactive, but I prefer it to the PDF).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Guiding Principles

    In my pursuit of a middle ground between introduction and textbook, I've made the following notes-to-self:

    - I like accessible writing because it's faster to read and can be understood with minimal prerequisite knowledge (so more people can get something out of it).
    - I like textbook writing because it uses well defined language and provides a more complete understanding of material (so those who have the prerequisite knowledge can get the most out of it).

    Therefore, my favorite writing (where the most people can get the most out of it) should:

    1. Be concise and fast to read
    2. Require minimal prerequisite knowledge
    3. Use well defined language
    4. Provide a complete understanding
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Concision

    - Establish the key concept and its purpose up-front.
    - Then, *only* include other concepts which are necessary for understanding the organizational hierarchy which the key concept is built on.
    - Do so in as few words as possible while still being clear.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Prerequisites

    - Assume minimal knowledge from the reader; it is preferable to build all concepts from the ground up.
    - When a concept is not worth building from the ground up in the book, link to an external resource that does.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Definitions

    - Provide precise definitions whenever a word's intended meaning is different or more specific than its colloquial one.
    - Define each word before it is used and only use it with exactly that meaning afterwards.
    - Each definition of a word is a set of requirements which are necessary and sufficient[^necessary-sufficient] to be in the category labeled by the word:

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Definition**</u>
    (Of a word or symbol) a set of requirements which are necessary and sufficient to be in the category labeled by the word or symbol.
    ///

    [^necessary-sufficient]: Used informally here; *necessary* and *sufficient* conditions are made precise in [Chapter 1](ch1_language_of_logic.md).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Understanding

    - Order concepts by dependency so that nothing is used before it is introduced.
    - When possible, start with a concrete example, then generalize; intuition makes formalism feel motivated rather than arbitrary.
    - Justify steps rather than asserting them. Include a derivation when possible and link to one when it isn't.
    - Make examples interactive, so readers can change an input and see the result.
    - State assumptions and say what happens when they fail; a complete understanding includes knowing where a result stops being true.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## How This Book Is Organized

    The [Introduction](introduction.md) builds one idea through a sequence of simple examples: a filter forms a *prediction* of the true value, compares it with a new *measurement*, and moves its estimate toward the measurement by some weight, called α. Every filter we build in this book, up to and including the Kalman filter, has that shape. The rest of the book is organized into six parts, each answering one question about it:

    | Part | Chapters | Question it answers |
    |---|---|---|
    | Part 1: Choosing α | [1](ch1_language_of_logic.md)–[8](ch8_bayesian_view.md) | Given how noisy a prediction and a measurement are, how much weight should each get? |
    | Part 2: The Scalar Kalman Filter | [9](ch9_noise_levels.md)–[11](ch11_measurement_functions.md) | How noisy are the prediction and the measurement, how should we predict, and what if the sensor measures something other than what we want to know? |
    | Part 3: State Vectors | [12](ch12_vectors_matrices_covariance.md)–[14](ch14_kalman_filters_in_practice.md) | What if what we want to know can't be represented by a single number? |
    | Part 4: Nonlinearity | [15](ch15_extended_kalman_filter.md)–[16](ch16_unscented_kalman_filter.md) | What if it changes, or is measured, in nonlinear ways? |
    | Part 5: Orientation | [17](ch17_rotations.md)–[19](ch19_ahrs.md) | How do we represent and estimate which way something is pointing, without singularities? |
    | Part 6: Inertial Navigation for Gait | [20](ch20_strapdown_inertial_navigation.md)–[21](ch21_zero_velocity_updates.md) | How can a motion sensor strapped to a shoe measure how someone walks? |

    Part 1 is the longest, because its answer ([Chapter 7](ch7_optimal_alpha.md)) is a statement about probabilities, and we want to prove it rather than ask you to take it on faith. So Part 1 first builds the mathematics that statement depends on, in dependency order: logic ([Chapter 1](ch1_language_of_logic.md)), sets ([Chapters 2](ch2_axioms_of_set_theory.md) and [3](ch3_sets_for_probability.md)), and probability ([Chapters 4](ch4_probability_spaces.md)–[6](ch6_expectation_and_variance.md)). If you are already comfortable with this material, skim it and start at Chapter 7. Every chapter after the Introduction opens with a **Prerequisites** box listing exactly what it uses, with links, so you can always find your way back.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Optional Appendices

    The appendices build foundational material from the ground up that many readers will already know. You don't need to read them front to back: read a section when a Prerequisites box points to it and the material is new to you.

    | Appendix | What it covers | When to read it |
    |---|---|---|
    | [Appendix A: Formal Logic](appendix_a_formal_logic.md) | Formal syntax, semantics, and proofs | Any time after Chapter 2, if you are curious; it deepens Chapters 1–2, and nothing on the main path depends on it |
    | [Appendix B: Constructing the Number Systems](appendix_b_number_systems.md) | The integers, rational numbers, and real numbers, built from the natural numbers | Before or alongside Chapter 3, which uses its main result |
    | [Appendix C: Calculus](appendix_c_calculus.md) | Limits, series, derivatives, integrals, and differential equations | Sequences and series before Chapter 4; integrals before Chapter 5; differential equations for Chapter 10; Jacobians for Chapter 15 |
    | [Appendix D: Linear Algebra](appendix_d_linear_algebra.md) | Vectors, matrices, eigenvalues, and derivatives with respect to matrices | Before Part 3 |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// tip | **Tips for reading online**
        attrs: {class: no-icon}
    As you have likely already figured out if you are reading this on a computer with a cursor, you can hover over terms with a dotted underline to view information about them. The information may be a {term}`definition` or a [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia) preview. If they are blue, you may also click on these terms to navigate to the source link as normal.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Feedback

    If you have any questions, comments, or think you've found an error in this book, I'd love to know!

    [adrienbabet1@gmail.com](mailto:adrienbabet1@gmail.com)
    """)
    return


if __name__ == "__main__":
    app.run()
