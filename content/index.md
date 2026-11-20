---
title: Home
# marimo-version: 0.25.1
abbreviations:
  hover over terms: like this
numbering:
  equations: false
---

```{marimo} python
:hide-code: true
:name: imports
:include: false

import marimo as mo
```

It's impossible to measure anything in the real world with 100% precision. Whether it's a bathroom scale measuring your weight, a car spedometer measuring wheel rotation, a pacemaker measuring heart beats, or an airplane measuring flight trajectory, there will always be some uncertainty. Signal filters are used to reduce this uncertainty and make better estimates of the true values we are trying to measure.

Humans generally have intuition on handling imperfect data: when making hard decisions, they consult multiple people (a type of social measurement) and decide based on a combination of the input received and their understanding of the situation. They understand that some input is more trustworthy and should be more heavily considered than others. Moreover, most people understand that getting more input can lead to better understanding even if no single piece of input is perfect.

By combining multiple measurements and knowledge about what's being measured, signal filters can follow a somewhat analogous process to estimate some unknown quantity. To see what this might look like, you can skip ahead to the [Introduction](/ch01-recursive-average) where we walk through some examples.
  
## Preface

My goal for this project was to write an intuitive (and mostly rigorous) guide to kalman filtering.
  
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
  
### My Approach

Proofs have long been my favorite type of writing. In highschool, I would regularly spend hours on the [AoPS TeXeR](https://artofproblemsolving.com/texer), drafting proofs for my homework problems. It was often a [type 2](https://www.rei.com/blog/climb/fun-scale) experience, but something about the rigor was satisfying. It was like building a puzzle, where the pieces were made of language and the language was precisely defined.

Here is a favorite definition, both because of its utility, and because of my penchant for self-referential ideas[^self-referential-ideas]:

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Definition
: (Of a term) a set of requirements which are necessary and sufficient to be in the category labeled by the term.
:::
::::

[^self-referential-ideas]: It's always quite beautiful when a self-referential idea can remain nevertheless usesful, rather than collapsing under the weight of its own circular reasoning.
  
In other words, if you have a set of requirements which are necessary and sufficient[^iff] to meet the category of *any* term, then you have a definition of that term (the set of requirements for the term "definition" has only one element, as do many other definitions) *and* any definition of any term must be a set of requirements which are necessary and sufficient for membership of that term's category.
  
In my pursuit of a middle ground between the accessible writing of introductory blog posts and the academically dense writing of engineering textbooks, I've come to the following conclusion: all rigor in my writing must be in the form of precisely defined language. Outside of this, the only goal is to be maximally informative to as many readers as possible.

To quote Hormozi:

> Words matter because they affect how we think. How we think affects what we do. And if words have us thinking the wrong way, then we will probably do the wrong stuff. I hate doing the wrong stuff. So to do the right stuff more and the wrong stuff less, it's best we know what words mean and use them.
>
> – $100M Leads
  
In this spirit, I will frequently include definition cards for words (like for "definition" above) whenever I think their technical use contains important specificity often missing from colloquial usage. After establishing definitions, the way to be accessible to the most readers is to be clear about the key points that I'm communicating and to provide a complete path for understanding the organizational hierarchy of concepts these key points are built on.
  
:::{tip icon=false} **Tips for reading online**
As you have likely already figured out if you are reading this on a computer with a cursor, you can hover over terms with a dotted underline to view information about them. The information may be a {term}`definition` or a [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia) preview. If they are blue, you may also click on these terms to navigate to the source link as normal.
:::