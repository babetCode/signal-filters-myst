# Introduction

My goal for this project is an interactive, introduction to signal filtering. I was inspired by *Kalman and Bayesian Filters in Python*, an introductory textbook written using Jupyter Notebook by Roger Labbe. To run his book, he recommends to downoad the notebooks from github, set up a conda environment, and run a local jupyter server. When Labbe wrote it, this was the best option for reactive notebooks. However, <u><a href="https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python#downloading-and-running-the-book" target="_blank">he also notes</a></u> "This is admittedly a somewhat cumbersome interface to a book."

Now, <u><a href="https://marimo.io/" target="_blank">marimo</a></u> and <u><a href="https://docs.astral.sh/uv/" target="_blank">uv</a></u> offer much easier sharing and dependency management. My goal here is to adapt what I have learned from Labbe's work and make it more easily shareable with modern tools. [test](https://example.com)

To view Labbe's original book, see

- <u><a href="https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python" target="_blank">github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python</a></u>, or 
-  <u><a href="https://github.com/babetCode/Kalman-and-Bayesian-Filters-in-Python" target="_blank">github.com/babetCode/Kalman-and-Bayesian-Filters-in-Python</a></u> to run with uv.

<!-- ```{marimo} python
import marimo as mo

slider = mo.ui.slider(start=1, stop=10, label="items")
slider
```

```{marimo} python
mo.md(f"The slider is set to **{slider.value}**.")
``` -->