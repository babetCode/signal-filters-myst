import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="Home")


@app.cell(hide_code=True)
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


@app.cell(hide_code=True)
def imports():
    # jb: include=false
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It's impossible to measure anything in the real world with 100% precision. However, by combining multiple measurements and knowledge about what's being measured, it is possible to make better estimates. This is what signal filters do.

    Humans generally have intuition on handling imperfect data: when making hard decisions, they consult multiple people (a type of social measurement) and decide based on a combination of the input received and their understanding of the situation. Moreover, most understand that getting more input can lead to better understanding even if no single piece of input is perfect.

    Signal filters follow a somewhat analogous process of using a variety of measurements to estimate some unknown quantity. For example, when weighing an object with an imprecise scale, a filter might be used to combine multiple different measurements and make a better estimate of the object's actual weight. The crucial point here is that having more measurements allows us to achieve better estimates *even if none of the measurements are 100% correct*.

    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    Having more measurements allows for better estimates *even if none of the measurements are 100% correct.*
    ///

    To see what this might look like, skip ahead to [chapter 1](/ch01-recursive-average) where we walk through one of the simplest ways to combine measurements: a recursive average.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Tips for Reading Online
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If you are reading this on a computer with a cursor, you can hover over terms&nbsp;with a dotted underline to view information about them. The information may be a {term}`definition` or a [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia) preview. If they are blue, you may also click on these terms to navigate to the source link as normal.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Preface

    My goal for this project was to write an intuitive (and mostly rigorous) introduction to kalman filtering.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Motivation

    I was inspired by [Kalman and Bayesian Filters in Python](https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python), a fantastic book by Roger Labbe. However, I wanted to do a couple things differently:

    1. His book is written as a collection of `.ipynb` files, so to read it you can:
        - Downoad the notebooks from github, set up a conda environment, run a local jupyter server, read the book from the local server (this is the recommended way).[^running-kbfp-locally].
        - Read a copy of the files hosted on nbviewer.org (this is usually slow or inaccessible due to rate limiting).
        - Read the PDF export of the book from Labbe's google drive (which loses all interactivity and sometimes does not exactly match the notebook source)[^kbfp-clone-repo].

    2. His book makes complex concepts very intuitive to understand, but sometimes forgoes precision in favor of simplicity. His goal was to make a simplified, introductory text, as he states in his preface: "If you are a hobbyist this book should provide everything you need. If you are serious about Kalman filters you’ll need more."

    By using [jupyter-book-marimo](https://github.com/marimo-team/jupyter-book-marimo) to publish content to the web, I can get the best of both worlds: interactive code in the browser without any downloads or configuration on the user end. My goal in writing this is to bridge the gap between introduction and textbook, so that I can be accessible to more readers will still using precise language.

    [^running-kbfp-locally]: At the time of Labbe's writing, this was the best option available for reactive notebooks. However, he also notes in his documentation, "this is admittedly a somewhat cumbersome interface to a book."

    [^kbfp-clone-repo]: To get around this, I have also created a [fork of his book](https://github.com/babetCode/Kalman-and-Bayesian-Filters-in-Python) on github which
        - Includes a `pyproject.toml` file, so that if you have [uv](https://docs.astral.sh/uv/) installed you can run the book immediately with a single command.
        - Publishes the `.ipynb` files to a [jupyter-book](https://jupyterbook.org/) so that you can read on the web without downloading (not interactive, but I prefer it to the PDF).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Writing Philosophy

    Proofs have long been my favorite type of writing. In highschool, I would regularly spend hours on the [AoPS TeXeR](https://artofproblemsolving.com/texer), drafting proofs for my homework problems. It was often a [type 2](https://www.rei.com/blog/climb/fun-scale) experience, but something about the rigor was satisfying. It was like building a puzzle, where the pieces were made of language and the language was precisely defined.

    Here is my favorite definition, both because of its utility, and because of my penchant for self-referential ideas[^self-referential-ideas]:

    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Definition**</u>
    (Of a term) a set of requirements which are necessary and sufficient to be in the category labeled by the term.
    ///

    [^self-referential-ideas]: It's always quite beautiful when a self-referential idea can remain nevertheless usesful, rather than collapsing under the weight of its own circular reasoning.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In other words, if you have a set of requirements which are necessary and sufficient[^iff] to meet the category of *any* term, then you have a definition of that term (the set of requirements for the term "definition" has only one element, as do many other definitions) *and* any definition of any term must be a set of requirements which are necessary and sufficient for memebership of that term's category.

    [^iff]: The phrase "necessary and sufficient" means the same thing as "if and only if":

        | English phrase | Logical meaning |
        |:------:|:----------------------------:|
        | $A$ if $B$ | $B \rightarrow A$ |
        | $A$ only if $B$ | $\neg B \rightarrow \neg A$ |
        | $A$ necessary for $B$ | $\neg A \rightarrow \neg B$ |
        | $A$ suffucient for $B$ | $A \rightarrow B$ |

        So by [contrapositive](https://en.wikipedia.org/wiki/Contraposition) equivalence:
        - "$A$ if $B$" is equivalent to "$A$ necessary for $B$".
        - "$A$ only if $B$" is equivalent to "$A$ sufficient for $B$".

        Note: It is important to remember that "if $A$ then $B$" means the same thing as "$B$ if $A$", and *not* the same as "$A$ if $B$". This is because in english the word "if" applies to whatever is to the right of it, so we flip the order of the variables in the sentence to preserve this relationship.
    """)
    return


@app.cell(hide_code=True)
def def_draft(mo):
    mo.md(r"""
    <!-- You may dismiss this as overly constraining:

    *But words often have different meanings based on context! If I wait 5 hours at the doctor's office, we would agree this is a "long" wait. If the doctor says my new-born child will live a "long" life, then 5 hours would be quite dissapointing. Doesn't that mean the definition of "long" is actually more fluid and context based, rather than a strict set of requirements?*

    Not so fast! This just means that "5 hours" is not the correct requirement for the term "long". Something like "lasting over a greater period of time than usual" would work for both our scenarios. Furthermore, we can make requirements that have multiple ways of being satisfied, i.e. "Adjective: lasting over a greater period of time, or greater distance than usual OR Verb: to have a deep desire for something".

    In general, if a word takes on different meanings based on context, then   -->
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In my pursuit of a middle ground between the accessible writing of introductory blog posts and the academically dense writing of engineering textbooks, I've come to the following conclusion: all rigor in my writing must be in the form of precisely defined language. Outside of this, the only goal is to be maximally informative to as many readers as possible[^footnotes].

    To quote Alex Hormozi:

    > Words matter because they affect how we think. How we think affects what we do. And if words have us thinking the wrong way, then we will probably do the wrong stuff. I hate doing the wrong stuff. So to do the right stuff more and the wrong stuff less, it's best we know what words mean and use them.
    >
    > – $100M Leads (p. 41)

    [^footnotes]: Plus some footnotes when the rabbit-hole of curiosity gets the best of me.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    After establishing definitions, the way to be accessible to the most readers is to be clear about the key points that I'm communicating and to provide a complete path for understanding the organizational hierarchy of concepts these key points are built on:

    > If we think about learning as a bridge, every step is needed, right? You can't skip a step to get across, you have to have every single foundational piece. And so the more general skills you have, the more gaps you can fill when someone provides incomplete information... All of us provide incomplete information, right? Otherwise, we'd literally have to start at zero and start at goooo gaga and then go all the way to coding AI, right? It's just we don't have the time to do it.
    >
    > – $100M Virtual Implementation Workshop (9:58)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    After a couple chapters for developing general intuition and language for signals, we will define zero using set theory (as well as discussing the structure of language), then use these foundations to build up to coding signal filters.
    """)
    return


if __name__ == "__main__":
    app.run()
