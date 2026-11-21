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
  
## Motivation

My goal for this project was to write an intuitive (and mostly rigorous) guide to kalman filtering. I was inspired by [Kalman and Bayesian Filters in Python](https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python), a fantastic book by Roger Labbe. However, I wanted to do a couple things differently:

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
  
## Guiding Principles

In my pursuit of a middle ground between introduction and textbook, I've made the following notes-to-self:

- I like accessible writing because it's faster to read and can be understood with minimal prerequisite knowlege (so more people can get something out of it).
- I like textbook writing because it uses well defined language and provides a more complete understanding of material (so those who have the prerequisite knowlege can get the most out of it).

Therefore, my favorite writing (where the most people can get the most out of it) should:

1. Be concise and fast to read
2. Require minimal prerequiste knowlege
3. Use well defined language
4. Provide a complete understanding
  
### Concision

- Establish the key concept and its purpose up-front.
- Then, *only* include other concepts which are necessary for understanding the organizational hierarchy which the key concept is built on.
- Do so in as few words as possible while still being clear.
  
### Prerequisites

- Assume minimal knowlege from the reader; it preferable to build all concepts from the ground up.
- When a concept is not worth building from the ground-up in the book, link to an external resource that does.
  
### Definitions

- Provide precise definitions whenever a word's intended meaning is different or more specific than its colloquial one.
- Define each word before it is used and only use it with exactly that meaning afterwards.
- Each definition of a word is a set of requirements which are necessary and sufficient to be in the category labeled by the word:

::::{admonition icon=false} 📖 **Definition**
:::{glossary}
Definition
: (Of a word or symbol) a set of requirements which are necessary and sufficient to be in the category labeled by the word or symbol.
:::
::::
  
### Understanding

- Order concepts by dependency so that nothing is used before it is introduced.
- When possible, start with a concrete example, then generalize; intuition makes formalism feel motivated rather than arbitrary.
- Justify steps rather than asserting them. Include a derivation when possible and link to one when it isn't.
- Make examples interactive, so readers can change an input and see the result.
- State assumptions and say what happens when they fail; a complete understanding includes knowing where a result stops being true.
  
:::{tip icon=false} **Tips for reading online**
As you have likely already figured out if you are reading this on a computer with a cursor, you can hover over terms with a dotted underline to view information about them. The information may be a {term}`definition` or a [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia) preview. If they are blue, you may also click on these terms to navigate to the source link as normal.
:::