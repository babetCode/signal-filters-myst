# title

yo wussup

```{marimo} python
import marimo as mo

slider = mo.ui.slider(start=1, stop=10, label="items")
slider
```

```{marimo} python
mo.md(f"The slider is set to **{slider.value}**.")
```