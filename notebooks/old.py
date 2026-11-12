import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    # jb: include=false

    _foobar = 0

    mo.md(r"""
    > If we think about learning as a bridge, every step is needed, right? You can't skip a step to get across, you have to have every single foundational piece. And so the more general skills you have, the more gaps you can fill when someone provides incomplete information... All of us provide incomplete information, right? Otherwise, we'd literally have to start at zero and start at goooo gaga and then go all the way to coding AI, right? It's just we don't have the time to do it.
    >
    > – Alex Hormozi, $100M Virtual Implementation Workshop ([9:58](https://www.youtube.com/watch?v=eV3BTnlc_tI&list=PLCGQSFOSt3B0&t=9m58s))

    After developing some general intuition for filters, we will define zero using set theory and discussing the structure of mathematical language. Then we will use these foundations to build up to coding signal filters.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You may dismiss this as overly constraining:

    *But words often have different meanings based on context! If I wait 5 hours at the doctor's office, we would agree this is a "long" wait. If the doctor says my new-born child will live a "long" life, then 5 hours would be quite dissapointing. Doesn't that mean the definition of "long" is actually more fluid and context based, rather than a strict set of requirements?*

    Not so fast! This just means that "5 hours" is not the correct requirement for the term "long". Something like "lasting over a greater period of time than usual" would work for both our scenarios. Furthermore, we can make requirements that have multiple ways of being satisfied, i.e. "Adjective: lasting over a greater period of time, or greater distance than usual OR Verb: to have a deep desire for something".

    In general, if a word takes on different meanings based on context, then
    """)
    return


if __name__ == "__main__":
    app.run()
