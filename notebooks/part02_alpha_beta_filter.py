# /// script
# dependencies = [
#     "marimo>=0.9.0",
#     "matplotlib>=3.10.0",
#     "numpy>=2.1.0",
#     "pandas>=2.2.3",
#     "schemdraw[matplotlib,svgmath]==0.23",
# ]
# requires-python = ">=3.13"
# ///

import marimo

__generated_with = "0.25.0"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # The Alpha-Beta Filter
    """)
    return


@app.cell(hide_code=True)
def imports():
    # jb: include=false

    import marimo as mo
    import schemdraw
    from schemdraw import flow
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from textwrap import dedent

    return dedent, mo, np, pd, plt


@app.cell(hide_code=True)
def display_funcs(dedent, mo):
    # jb: include=false

    def admonition(
        value: str,
        title: str = "<b>Key Idea</b>",
        color: str = "GoldenRod",
        icon_str='<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="color-mix(in srgb, GoldenRod 70%, currentColor 30%)" d="M8.308 13.308q.538-.539.538-1.308t-.538-1.308T7 10.154t-1.308.538T5.154 12t.538 1.308T7 13.846t1.308-.538M7 16.73q-2 0-3.366-1.366Q2.27 14 2.27 12t1.366-3.366T7 7.27q1.698 0 2.941.958t1.593 2.273h9.049l1.494 1.494l-2.48 2.635l-1.828-1.379l-1.827 1.442l-1.557-1.192h-2.85q-.356 1.339-1.608 2.285T7 16.73"></path></svg>',
    ):
        # Parse LaTeX & Markdown first into a rendered Marimo HTML element
        content = mo.md(value) if isinstance(value, str) else value
        title_content = mo.md(title) if isinstance(title, str) and title else None

        title_html = ""
        if title_content:
            title_html = f"""
            <div style="
                display: flex;
                align-items: center;
                font-weight: bold;
                margin-bottom: 8px;
            ">
                <div style="
                    flex-shrink: 0;
                    margin-right: 8px;
                    font-size: 1.5em;
                    display: flex;
                ">
                    {icon_str}
                </div>
                <div style="color:color-mix(in srgb, {color} 70%, currentColor 30%)">{title_content.text}</div>
            </div>
            """

        # Build body HTML using content.text (already parsed by KaTeX)
        body_html = f"""
        <div style="display: flex; align-items: flex-start;">
            {f"" if title else f'<div style="flex-shrink: 0; margin-right: 12px; font-size: 1.5em; display: flex; padding-top: 2px;">{icon_str}</div>'}
            <div style="flex-grow: 1; overflow-wrap: anywhere;">
                {content.text}
            </div>
        </div>
        """

        return mo.Html(f"""
        <div style="
            display: flex;
            flex-direction: column;
            padding: 16px;
            margin: 16px 0;
            border-left: 4px solid {color};
            background-color: color-mix(in srgb, {color} 10%, transparent);
            border-radius: 0 6px 6px 0;
        ">
            {title_html}
            {body_html}
        </div>
        """)

    def key_idea(
        value: str,
        title="<b>Key Idea</b>",
        color="GoldenRod",
    ):
        icon_str = '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="color-mix(in srgb, GoldenRod 70%, currentColor 30%)" d="M8.308 13.308q.538-.539.538-1.308t-.538-1.308T7 10.154t-1.308.538T5.154 12t.538 1.308T7 13.846t1.308-.538M7 16.73q-2 0-3.366-1.366Q2.27 14 2.27 12t1.366-3.366T7 7.27q1.698 0 2.941.958t1.593 2.273h9.049l1.494 1.494l-2.48 2.635l-1.828-1.379l-1.827 1.442l-1.557-1.192h-2.85q-.356 1.339-1.608 2.285T7 16.73"></path></svg>'
        return admonition(value=value, title=title, color=color, icon_str=icon_str)

    def glossary_def(
        value: str,
        title="<b>Definition</b>",
        color="cornflowerblue",
    ):
        icon_str = '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="color-mix(in srgb, cornflowerblue 70%, currentColor 30%)" d="M4.385 14.09h.779l.555-1.534h2.87l.561 1.535h.792l-2.31-6.143h-.957zm1.62-2.267l1.124-3.06h.05l1.123 3.06zm7.88-2.23v-.931q.805-.408 1.725-.612t1.89-.204q.554 0 1.064.071q.509.072 1.052.202v.908q-.524-.167-1.02-.232q-.498-.064-1.096-.064q-.97 0-1.892.218q-.924.218-1.724.643m0 5.462v-.97q.768-.407 1.717-.611t1.899-.204q.554 0 1.064.072q.509.07 1.052.201v.908q-.524-.167-1.02-.232q-.498-.064-1.096-.064q-.97 0-1.892.235q-.924.234-1.724.665m0-2.712v-.969q.806-.408 1.726-.611t1.89-.204q.554 0 1.063.07q.51.072 1.052.203v.908q-.523-.168-1.02-.232q-.497-.065-1.095-.065q-.97 0-1.892.238q-.924.237-1.724.662M12.5 17.32q1.216-.678 2.453-.98t2.547-.3q.9 0 1.618.111t1.267.296q.23.096.423-.029t.192-.394V7.008q0-.173-.096-.308q-.096-.134-.327-.23q-.825-.293-1.501-.4T17.5 5.961q-1.31 0-2.613.386q-1.304.387-2.387 1.16zm-.5 1.45q-1.22-.834-2.62-1.282T6.5 17.04q-.78 0-1.534.13q-.753.131-1.466.42q-.544.217-1.022-.131T2 16.496V6.831q0-.371.195-.689t.547-.442q.881-.388 1.833-.563T6.5 4.962q1.47 0 2.866.423q1.398.423 2.634 1.23q1.237-.807 2.634-1.23t2.866-.423q.973 0 1.925.175t1.833.563q.352.125.547.442t.195.689v9.665q0 .614-.516.943q-.517.328-1.1.111q-.693-.27-1.418-.39q-.724-.121-1.466-.121q-1.48 0-2.88.448T12 18.769"></path></svg>'
        return admonition(
            value=value, title=title, color=color, icon_str=icon_str
        )

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

    return (graphic,)


@app.cell(hide_code=True)
def math_funcs(np):
    # jb: include=false

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

    return ema, gaussian_noise


@app.cell(hide_code=True)
def nutrition_funcs():
    # jb: include=false

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
    return activity_lvl_dict, kcal_per_lb, mifflin_st_jeor, sex_dict


@app.cell(hide_code=True)
def biometrics(
    activity_lvl_dict,
    ema,
    gaussian_noise,
    kcal_per_lb,
    mifflin_st_jeor,
    np,
):
    # jb: include=false

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
    return (
        age,
        height_cm,
        measurements,
        sex,
        target_kcal_per_day,
        target_lbs_per_week,
        total_days,
        weight,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the last section, we used the EMA equation

    $$\hat{x}_k = \hat{x}_{k-1} + \alpha (z_k - \hat{x}_{k-1})$$

    to estimate your weight with the assumption that your true weight did not change between measurements. That assumption let us use $\alpha$ to pick an $\hat x_k$ bewteen $\hat x_{k-1}$ and $z_k$, because without noise, those values *should* have both been equal to $x_k$. Therefore, by combining the two, we increased the chance that the noise would "cancel itself out".

    In this section, we build an algorithm that works without this assumption—that is, an algorithm for when we expect the value to change over time. This means we can no longer assume that, without noise, $\hat x_{k-1}$ would equal $x_k$. The only thing we can still be sure of is that *if there was no noise*, then we would have

    $$\begin{align*}
    \hat x_{k-1} &= x_{k-1}, \\
    z_k &= x_k.
    \end{align*}$$

    You might ask, "well of course if there were no imperfections then our measurement and estimate would be perfect, but how is that useful?" In order for this be useful, we need an expresion in terms of $\hat x_{k-1}$ that—without noise—would be equal to $x_k$, that way we can use our same strategy with $\alpha$ to choose a value between the expression and $z_k$. By letting $\Delta x_k$ represent the change in value arriving at step $k$: $(x_k - x_{k-1})$, we can say that *if there was no noise*, then we would have

    $$\hat x_{k-1} + \Delta x_k = z_k = x_k.$$

    Therefore, we can substitute $\hat x_{k-1}$ for $(\hat x_{k-1} + \Delta x_k)$ in our EMA equation to get

    $$\hat{x}_k = (\hat x_{k-1} + \Delta x_k) + \alpha (z_k - (\hat x_{k-1} + \Delta x_k)).$$

    We are now much closer to running our filter just like in the last section. However, we must first figure out how to estimate the delta. To see how this plays out, let's walk through an example.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Estimating the Rate of Change
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Imagine that after the scale measures you at 154.95 lbs, you decide to bulk up and start eating more. Then, we weigh you again every day. You track your caloric intake and then use the Mifflin-St Jeor equation[^mifflin-st-jeor], an activity multiplier[^activity-multiplier], and the Wishnofsky approximation[^wishnofsky] to estimate how much weight you will likely gain with your new diet [@wishnofsky1958].

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
    """)
    return


@app.cell(hide_code=True)
def _(
    age,
    height_cm,
    mo,
    sex,
    sex_dict,
    target_kcal_per_day,
    target_lbs_per_week,
):
    mo.md(rf"""
    For example, imagine you are a {height_cm} cm, {age} year old {sex_dict[sex]}, you eat {target_kcal_per_day:.0f} kcal/day, and you have a moderate activity level. This means you will likely gain about {target_lbs_per_week/7:.1f} lbs./day, meaning we have $\Delta x_k = {target_lbs_per_week/7:.1f}$. Applying this filter over 4 weeks of measurements looks like:
    """)
    return


@app.function(hide_code=True)
# jb: include=false
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


@app.cell(hide_code=True)
def _(mo, target_lbs_per_week):
    # jb: include=false
    alpha_slider = mo.ui.slider(start=0, stop=1, step=.05, value=0.05, label=r"$\alpha$")
    delta_slider = mo.ui.slider(start=-1, stop=1, step=.1, value=round(target_lbs_per_week/7, 1), label=r"$\Delta x$")
    return alpha_slider, delta_slider


@app.cell(hide_code=True)
def _(
    alpha_slider,
    delta_slider,
    graphic,
    measurements,
    mo,
    np,
    pd,
    plt,
    total_days,
    weight,
):
    _alpha_delta_weight = alpha_delta(alpha_slider.value, delta_slider.value, measurements)

    _measurements_df = pd.DataFrame({
        "day": np.arange(1, total_days+1, 1),
        "weight_lbs": measurements,
        "alpha_delta_weight": _alpha_delta_weight,
    })

    with plt.style.context("default"):
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
    return


@app.cell(hide_code=True)
def _(mo, target_lbs_per_week):
    mo.md(rf"""
    This looks really good when $\Delta x \approx {target_lbs_per_week/7:.1f}$, but only because we've used the same Mifflin-St Jeor equation to simulate the data and also to predict your weight gain. When we adjust $\Delta x$, we see our filter starts to drift (especially when $\alpha$ is small). In the real world, the value we plug in for $\Delta x_k$ won't be perfect.
    """)
    return


@app.cell(hide_code=True)
def _():
    # TODO Make interactive graph the visualizes predicted as well as measurement and estimate (which are already shown).

    # TODO clarify the difference between $\delta x$ and $\beta$.

    # TODO consider replacing nutrition footnotes with glossary.
    return


if __name__ == "__main__":
    app.run()
