---
title: The Alpha-Beta Filter
marimo-version: 0.25.1
---

```{marimo-config}
---
pyproject: |-
  dependencies = [
      "marimo>=0.9.0",
      "matplotlib>=3.10.0",
      "numpy>=2.1.0",
      "pandas>=2.2.3",
      "schemdraw[matplotlib,svgmath]==0.23",
  ]
  requires-python = ">=3.13"
---
```

<!-- jb-frontmatter
numbering:
  equations: false
-->

```{marimo} python
:hide-code: true
:name: imports
:include: false

import marimo as mo
import schemdraw
from schemdraw import flow
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from textwrap import dedent
```

```{marimo} python
:hide-code: true
:name: display_format
:include: false

plt.style.use('default')
schemdraw.use("svg")
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

```{marimo} python
:hide-code: true
:name: math_funcs
:include: false

def gaussian_noise(
    mean=0.,
    std_dev=1.,
    Hz=1.,
    duration_sec=10.,
    seed=1,
):
    rng = np.random.default_rng(seed=seed)

    n = int(Hz * duration_sec)
    measurements = rng.normal(
        loc=mean,
        scale=std_dev,
        size=n,
    )
    return measurements

def cumulative_average(measurements):
    x_k_minus_one = 0
    output = []
    for k, z in enumerate(measurements, start=1):
        x_k = x_k_minus_one + (1/k)*(z - x_k_minus_one)
        output.append(x_k)
        x_k_minus_one = x_k
    return output

def ema(alpha, measurements):
    x_k_minus_one = 0
    ema_output = []
    for k, z in enumerate(measurements, start=1):
        if k == 1:
            x_k_minus_one = z
        x_k = x_k_minus_one + alpha*(z - x_k_minus_one)
        ema_output.append(x_k)
        x_k_minus_one = x_k
    return ema_output
```

```{marimo} python
:hide-code: true
:name: nutrition_funcs
:include: false

def mifflin_st_jeor(
    age = 25,
    height_cm = 175,
    weight = 154.88,
    sex = "M",
    unit = "lbs",
):
    if unit == "lbs":
        weight = weight * 0.45359237

    bmr = 10*weight + 6.25*height_cm -5*age
    if sex.lower() == "m":
        return  bmr + 5

    elif sex.lower() == "f":
        return bmr - 161

    else:
        return -1

activity_lvl_dict = {
    "light": 1.2,  # light walking, biking, or chores
    "moderate": 1.5,  # regular lifting, running, or active work
    "high": 1.9,  # Professional athletes or military training
}
sex_dict = {
    "M": "male",
    "F": "female",
}
kcal_per_lb = 3500
```

```{marimo} python
:hide-code: true
:name: biometrics
:include: false

age = 23
height_cm = 175
sex = "M"
activity_lvl = "moderate"
target_lbs_per_week = 1.4

total_days = 28
weight = np.linspace(start=155, stop=155+target_lbs_per_week*4, num=total_days, endpoint=False)
noise = np.array(
    [
        ema(
            0.05,
            gaussian_noise(
                mean=0.0, std_dev=1.0, Hz=10, duration_sec=3, seed=i
            ),
        )[-1]
        for i in range(1, 29)
    ]
)
measurements = np.round(weight + noise, 2)
start_weight = measurements[0]

bmr = mifflin_st_jeor(age, height_cm, start_weight, sex)
tdee = bmr * activity_lvl_dict[activity_lvl]

target_kcal_per_day = tdee + (kcal_per_lb * target_lbs_per_week / 7)
guess_kcal_per_day = 2800
```

In the last section, we used the EMA equation

$$\hat{x}_k = \hat{x}_{k-1} + \alpha (z_k - \hat{x}_{k-1})$$

to estimate your weight with the assumption that your true weight did not change between measurements. That assumption let us use $\alpha$ to pick an $\hat x_k$ bewteen $\hat x_{k-1}$ and $z_k$, because without noise, those values *should* have both been equal to $x_k$. Therefore, by combining the two, we increased the chance that the noise would "cancel itself out".

In this section, we build an algorithm that works without this assumption—that is, an algorithm for when we expect the value to change over time. This means we can no longer assume that, without noise, $\hat x_{k-1}$ would equal $x_k$. The only thing we can still be sure of is that *if there was no noise*, then we would have

$$\begin{align*}
\hat x_{k-1} &= x_{k-1}, \\
z_k &= x_k.
\end{align*}$$

You might say, "well of course if there were no imperfections then our estimate and measurement would be perfect, but how is that useful?" In order for this be useful, we need an expresion in terms of $\hat x_{k-1}$ that—without noise—would be equal to $x_k$, that way we can use our same strategy with $\alpha$ to choose a value between the expression and $z_k$. By letting $\Delta x_k$ represent the change in value arriving at step $k$: $(x_k - x_{k-1})$, we can say that *if there was no noise*, then we would have

$$\hat x_{k-1} + \Delta x_k = z_k = x_k$$

(we don't know what $\Delta x_k$ is yet, but we'll figure out how to deal with that later). Therefore, we can substitute $(\hat x_{k-1} + \Delta x_k)$ in place of $\hat x_{k-1}$ in our EMA equation to get

$$\hat{x}_k = (\hat x_{k-1} + \Delta x_k) + \alpha (z_k - (\hat x_{k-1} + \Delta x_k)).$$

Here, the $(\hat x_{k-1} + \Delta x_k)$ term is called the **prior** (often denoted $\hat x_k^-$), because it represents our estimate for time $k$ *prior* to getting the measurement $z_k$. Using this notation, we can rewrite our equation as

$$\hat{x}_k = \hat x_k^- + \alpha (z_k - \hat x_k^-).$$

This is starting to look quite similar to our filter in the last section.
<!---->
:::{attention icon=false} 🗝️ **Key Idea**
If we can get an expresion in terms of $\hat x_{k-1}$ that—without noise—would be equal to $x_k$, then we can combine them (with some weighting $\alpha$) to increase the probablity that the noise cancels out.
:::
<!---->
However, we must first figure out how to estimate $\Delta x_k$. To see how this plays out, let's walk through an example.
<!---->
## Estimating the Rate of Change
<!---->
Imagine that after the scale measures you at 154.95 lbs, you decide to start eating more in order to bulk up. Then, we weigh you again every day. We also use the Mifflin-St Jeor equation[^mifflin-st-jeor], an activity multiplier[^activity-multiplier], and the Wishnofsky approximation[^wishnofsky] to estimate how much weight you will likely gain given your new diet [@wishnofsky1958].

[^mifflin-st-jeor]:
    The Mifflin-St Jeor equation estimates basal metabolic rate (BMR):
    $$\text{BMR} = 10(\text{weight}) + 6.25(\text{height}) - 5(\text{age}) + (\text{plus 5 for men, minus 161 for women}).$$

[^wishnofsky]:
    Max Wishnofsky's 1958 paper Caloric Equivalents of Gained or Lost Weight calculates:
    $$3,500\text{ kcal}\approx 1 \text{{ lb.}}$$

[^activity-multiplier]:
    Total daily energy expenditure (TDEE) is commonly calculated by multiplying BMR my some activity multiplier. For moderate activity, this value is about 1.5:
    $$\text{TDEE} \approx 1.5 (\text{BMR}).$$
    This means if your daily energy intake (DEI) is equal to TDEE, then then you will be in energy balance, and maintain a constant weight. Therefore, we have:
    $$\text{pounds gained per day} \approx (\text{DEI} - \text{{TDEE}})/3,500.$$

```{marimo} python
:hide-code: true

mo.md(rf"""
For example, imagine you are a {height_cm} cm, {age} year old {sex_dict[sex]}, you eat {target_kcal_per_day:.0f} kcal/day, and you have a moderate activity level. This means you will likely gain about {target_lbs_per_week/7:.1f} lbs./day, meaning we have $\Delta x_k = {target_lbs_per_week/7:.1f}$. Applying this filter over 4 weeks of measurements looks like:
""")
```

```{marimo} python
:hide-code: true
:name: alpha_delta_sliders
:include: false

def alpha_delta(alpha, delta, measurements):
    x_k_minus_one = 0
    ema_output = []
    for k, z in enumerate(measurements, start=1):
        if k == 1:
            x_k_minus_one = z - delta
        x_k = x_k_minus_one + delta + alpha*(z - x_k_minus_one - delta)
        ema_output.append(x_k)
        x_k_minus_one = x_k
    return ema_output

alpha_slider = mo.ui.slider(start=0, stop=1, step=.05, value=0.05, label=r"$\alpha$")
delta_slider = mo.ui.slider(start=-1, stop=1, step=.1, value=round(target_lbs_per_week/7, 1), label=r"$\Delta x$")
```

```{marimo} python
:hide-code: true
:name: alpha_delta_fig

_alpha_delta_weight = alpha_delta(alpha_slider.value, delta_slider.value, measurements)

_measurements_df = pd.DataFrame({
    "day": np.arange(1, total_days+1, 1),
    "weight_lbs": measurements,
    "alpha_delta_weight": _alpha_delta_weight,
})

_fig, _ax = plt.subplots()

_measurements_df.plot(
    x="day",
    y=["weight_lbs", "alpha_delta_weight"],
    ax=_ax,
    xlabel="Time (s)",
    ylabel="Weight (lbs.)",
    ylim=(np.min(weight)-3, np.max(weight)+3),
    xticks=_measurements_df["day"],
    yticks=np.arange(np.min(weight)-3, np.max(weight)+4, 1),
    rot=45,
)
_ax.legend(["Measurement", "Filtered"])
_ax.grid(visible=True, alpha=0.9, linewidth=0.4)
_ax.set_title(f"Bulking Daily Weigh-Ins with $\\alpha = {alpha_slider.value:.2f}$ and $\\Delta x = {delta_slider.value}$", style='italic')

mo.vstack([
    alpha_slider,
    delta_slider,
    graphic(_fig)
])
```

```{marimo} python
:hide-code: true

mo.md(rf"""
This looks really good when $\Delta x \approx {target_lbs_per_week/7:.1f}$, but only because we've used the same Mifflin-St Jeor equation to simulate the data and also to predict your weight gain. When we adjust $\Delta x$, we see our filter starts to drift (especially when $\alpha$ is small).
""")
```

In the real world, the value we plug in for $\Delta x_k$ won't be perfect, so we may want it to adjust, based on the measuremnts we're getting. For example, if we had initially set $\Delta x_k = 0.4$, then after the first three measurements we might think everything was fine, but after the 4th and 5th measurements, we may wonder if we overestimated your calorie consumption.

In general, we expect each measurement to equal the previous estimate plus your rate of weight gain times the time step. Expressed as an equation, we expect

$$z_k = \Delta x_k$$

```{marimo} python
:hide-code: true

# TODO Make interactive graph the visualizes predicted as well as measurement and estimate (which are already shown).

# TODO clarify the difference between $\delta x$ and $\beta$.

# TODO consider replacing nutrition footnotes with glossary.
```