---
title: Preface
# marimo-version: 0.25.1
abbreviations:
  hover over terms: like this
numbering:
  equations: false
---

```{marimo-config}
:eval: false
---
width: medium
---
```

```{marimo} python
:hide-code: true
:name: imports
:include: false

import marimo as mo
```

It's impossible to measure anything in the real world with 100% precision. However, by combining multiple measurements and knowledge about what's being measured, it is possible to make better estimates. This is what signal filters do.

Humans generally have intuition on handling imperfect data: when making hard decisions, they consult multiple people (a type of social measurement) and decide based on a combination of the input received and their understanding of the situation. Moreover, most understand that getting more input can lead to better understanding even if no single piece of input is perfect.

Signal filters follow a somewhat analogous process of using a variety of measurements to estimate some unknown quantity. For example, when weighing an object with an imprecise scale, a filter might be used to combine multiple different measurements and make a better estimate of the object's actual weight. The crucial point here is that having more measurements allows us to achieve better estimates *even if none of the measurements are 100% correct*.

:::{attention icon=false} 🗝️ **Key Idea**
Having more measurements allows for better estimates *even if none of the measurements are 100% correct.*
:::

To see what this might look like, skip ahead to the [Introduction](/part01-recursive-average) where we walk through one of the simplest ways to combine measurements: a recursive average.
  
## Tips for Reading Online
  
If you are reading this on a computer with a cursor, you can hover over terms&nbsp;with a dotted underline to view information about them. The information may be a {term}`definition` or a [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia) preview. If they are blue, you may also click on these terms to navigate to the source link as normal.
  
## Motivation

My goal for this project was to write an intuitive (and mostly rigorous) introduction to kalman filtering.

I was inspired by [Kalman and Bayesian Filters in Python](https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python), a fantastic book by Roger Labbe. However, I wanted to do a couple things differently:

1. His book is written as a collection of `.ipynb` files, so to read it you can:
    - Downoad the notebooks from github, set up a conda environment, run a local jupyter server, read the book from the local server (this is the recommended way).[^running-kbfp-locally].
    - Read a copy of the files hosted on nbviewer.org (this is usually slow or inaccessible due to rate limiting).
    - Read the PDF export of the book from Labbe's google drive (which loses all interactivity and sometimes does not exactly match the notebook source)[^kbfp-clone-repo].

2. The book makes complex concepts very intuitive to understand, but sometimes forgoes precision in favor of simplicity. His goal was to make a simplified, introductory text, as he states in his preface: "If you are a hobbyist this book should provide everything you need. If you are serious about Kalman filters you’ll need more."

By using [jupyter-book-marimo](https://github.com/marimo-team/jupyter-book-marimo) to publish content to the web, I can get the best of both worlds: interactive code in the browser without any downloads or configuration on the user end. My goal in writing this is to bridge the gap between introduction and textbook, so that I can be accessible to more readers will still using precise language.

[^running-kbfp-locally]: At the time of Labbe's writing, this was the best option available for reactive notebooks. However, he also notes in his documentation, "this is admittedly a somewhat cumbersome interface to a book."

[^kbfp-clone-repo]: To get around this, I have also created a [fork of his book](https://github.com/babetCode/Kalman-and-Bayesian-Filters-in-Python) on github which
    - Includes a `pyproject.toml` file, so that if you have [uv](https://docs.astral.sh/uv/) installed you can run the book immediately with a single command.
    - Publishes the `.ipynb` files to a [jupyter-book](https://jupyterbook.org/) so that you can read on the web without downloading (not interactive, but I prefer it to the PDF).