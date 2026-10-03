---
abbreviations:
  iff: if and only if
  diff: null
numbering:
  equations: false
title: "Drafting"
---

```{marimo-config}
:pyproject:
    requires-python = ">=3.13"
    dependencies = [
        "matplotlib==3.11.1",
        "numpy==2.5.2",
        "pandas==3.0.5",
        "schemdraw[matplotlib,svgmath]==0.23",
    ]
```

<!---->

```{marimo} python
:hide-code: true
:name: imports
:include: false
import marimo as mo
import numpy as np
import pandas as pd
import matplotlib
import schemdraw
from schemdraw import flow
from textwrap import dedent
import matplotlib.pyplot as plt
```

```{marimo} python
:hide-code: true
:name: display_format
:include: false
plt.style.use('default')
def graphic(x):
    return mo.Html(
        dedent(f'''\
        <style>
            .dark .graphic {{ 
                filter: invert(1) hue-rotate(180deg); 
            }}
        </style>
        <div class="graphic">
            {mo.as_html(x)}
        </div>
        ''')
    )
```

lorem ipsum dolor sit amet consectetuer adipiscing elit sed diam nonummy nib
