# /// script
# dependencies = [
#     "marimo>=0.9.0",
#     "matplotlib==3.11.1",
#     "numpy==2.5.2",
#     "pandas==3.0.5",
#     "schemdraw[matplotlib,svgmath]==0.23",
# ]
# requires-python = ">=3.13"
# ///

import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Introduction
    """)
    return


@app.cell(hide_code=True)
def imports():
    # jb: include=false
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib
    import schemdraw
    from schemdraw import flow
    from textwrap import dedent
    import matplotlib.pyplot as plt

    return dedent, flow, mo, np, pd, plt, schemdraw


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

    return glossary_def, graphic, key_idea


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

    return cumulative_average, ema, gaussian_noise


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It's impossible to measure anything in the real world with 100% precision. However, by combining multiple measurements and knowledge about what's being measured, it is possible to make better estimates. This is what signal filters do.

    Humans generally have intuition on handling imperfect data: when making hard decisions, they consult multiple people (a type of social measurement) and decide based on a combination of the input received and their understanding of the situation. Moreover, most understand that getting more input can lead to better understanding even if no single piece of input is perfect.

    Signal filters follow a somewhat analogous process of using a variety of measurements to estimate some unknown quantity. For example, when weighing an object with an imprecise scale, a filter might be used to combine multiple different measurements and make a better estimate of the object's actual weight. The crucial point here is that having more measurements allows us to achieve better estimates *even if none of the measurements are 100% correct*.
    """)
    return


@app.cell(hide_code=True)
def _(key_idea):
    key_idea(value="Having more measurements allows for better estimates <i>even if none of the measurements are 100% correct.</i>")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To see what this might look like, let's walk through a simple example.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Recursive Averaging
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Imagine we are building a digital bathroom scale to measure your body weight. When you step on the scale, a sensor—called a strain gauge load cell[^loadcell]—underneath the platform measures your downward force. The loadcell outputs an analog voltage that is then converted to a digital measurement with an analog-to-digital converter (ADC). A typical ADC such as the HX711 will sample the voltage signal between 10-80 Hz [@avia_hx711_datasheet]. Since we could represent both the output from the loadcell and the output from the ADC as funtions over time, they are both {term}`signal`s.

    [^loadcell]: A strain gauge load cell is an electronic component that converts force into proportional resistance change using metal foil grids (called strain gauges) which change resistance under load (increasing under tension and decreasing under compression). They are used in almost all digital bathroom scales because they are thin, accurate (relatively), mass-producible, and have no moving parts to wear out.
    """)
    return


@app.cell(hide_code=True)
def _(glossary_def):
    glossary_def(value="<b>Signal:</b> Any function that represents how a quantity varies over time or space.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Because nobody stands perfectly still, your constant weight shifts on the scale will introduce **noise** to the measurements (and even if you were still, there would still be thermal noise in the load cell).
    """)
    return


@app.cell(hide_code=True)
def _(glossary_def):
    glossary_def(value="<b>Noise:</b> Any unwanted or random component added to a signal that degrades or obscures the information it carries.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Since the stream of measurements from the ADC will constantly fluctuate, we can never know your true weight with 100% precision (remember, it's impossible to measure anything with 100% precision). Instead, we must attempt to remove the noise from this signal to make our best estimate. Hence, the term **filter**.
    """)
    return


@app.cell(hide_code=True)
def _(glossary_def):
    glossary_def(value="<b>Filter:</b> Any algorithm that selectively modifies or removes noise from a signal.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here is the setup we are working with at this point, where each arrow is annotated with the result or output of the prior box:
    """)
    return


@app.cell(hide_code=True)
def _(flow, graphic, schemdraw):
    schemdraw.use("svg")

    with schemdraw.Drawing(show=False) as _d:
        _d.config(fontsize=12)

        flow.Start().label("Force is applied to\nthe scale's platform").drop("S")
        flow.Arrow().down(1).label(
            "Tensed/compressed\nstrain gaugues", loc="bottom"
        )
        flow.RoundBox().label(
            "Loadcell measures force\nvia strain gauge resistance"
        )
        flow.Arrow().down(1).label(
            "Continuous\nanalog voltage", loc="bottom"
        )
        flow.RoundBox().label("ADC samples\nthe voltage signal")
        flow.Line().down(1).label(
            "Sequence of digital\nmeasurements", loc="bottom", ofst=(0, 0.25)
        )
        flow.Line().right(3.5)
        flow.Line().up(5)
        flow.Arrow().right(1)
        flow.RoundBox().label("Filter removes\nnoise from the\nmeasurements").drop("S")
        flow.Arrow().down(1).label("Weight estimate", loc="bottom")
        flow.Terminal().label("Scale reading")

    graphic(_d)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Imagine you step on the scale and the first 10 digital measurements look like this:
    """)
    return


@app.cell(hide_code=True)
def _(gaussian_noise, graphic, np, pd, plt):
    weight = 155
    Hz = 10
    dur = 3
    noise = gaussian_noise(
        mean=0.,
        std_dev=1.,
        Hz=Hz,
        duration_sec=dur,
    ).round(2)
    measurements = noise + weight
    ten_measurements = measurements[:10]

    ten_measurements_df = pd.DataFrame(
        {
            "time_s": np.arange(.1, 1.1, .1),
            "weight_lbs": ten_measurements,
        }
    )

    with plt.style.context("default"):
        _fig, _ax = plt.subplots()

        ten_measurements_df.plot(
            x="time_s",
            y="weight_lbs",
            ax=_ax,
            legend=False,
            xlabel="Time (s)",
            ylabel="Weight (lbs.)",
            ylim=(weight-3, weight+3),
            xticks=ten_measurements_df["time_s"],
            yticks=np.arange(weight-3, weight+4, 1),
        )

        _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
        _ax.set_title("Weight Measurements at 10 Hz Sample Rate", style='italic')

    graphic(_fig)
    return dur, measurements, ten_measurements, weight


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can immediately tell that you're in the mid 150's, but we're not sure exactly where. Since the fluctuations are generally random, it is reasonable to assume each measurement is just as likely to be too high as it is to be too low[^mean-noise]. Therefore, we can get a better estimate of the person's true weight by combining many measurements, in hopes of the noise canceling itself out.

    [^mean-noise]: More specifically, we assume that the mean of the noise is 0, which means our logic still holds even if the median skews too big or too small.
    """)
    return


@app.cell(hide_code=True)
def _(key_idea):
    key_idea(
        r"Because we assume that the noise is random and has a mean of 0, we combine multiple measurements to increase the probability that the noise cancels out."
    )
    return


@app.cell(hide_code=True)
def _(mo, ten_measurements):
    mo.md(rf"""
    The most basic way to combine measurements is by averaging them. For example, if we only had the two measurements our estimate would be

    $$({ten_measurements[0]}+{ten_measurements[1]})/2={round(.5*(ten_measurements[0]+ten_measurements[1]), 2)}\text{{ lbs.}}$$

    After the third, we would have

    $$({ten_measurements[0]}+{ten_measurements[1]}+{ten_measurements[2]})/3={(ten_measurements[0]+ten_measurements[1]+ten_measurements[2])/3:.2f} \text{{ lbs.}},$$

    and so on. In general, the more measurements we continue to average, the better we expect our estimate to get.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This seems like a good strategy, but our list of measurements is growing quite quickly and many scales have only 64 out of 256 bytes of memory available for data processing [@holtek_ht45f75_data_sheet]. At this rate, with each number stored as a 32-bit integer (4 bytes), our memory would be completely full within about 1.6 seconds. We can fix this by using a recursive average to store only two values: the number of measurements, and the previous average.

    Let our measurements be denoted $z_1$, $z_2$, $z_3$, etc..., so that after $k$ measurements, we have $z_1$, $z_2$, ..., $z_k$. This means that after
    $k-1$ measurements, our average will be

    $$\bar{x}_{k-1} = \frac{z_1 + z_2 + \cdot\cdot\cdot + z_{k-1}}{k-1},$$

    and after $k$ measurements it will be

    $$\bar{x}_k = \frac{z_1 + z_2 + \cdot\cdot\cdot + z_{k-1} + z_k}{k}.$$

    Now we can calculate each $\bar{x}_k$ (pronounced "x bar", where the bar is statistical notation for an average) in terms of the number of measurements ($k$) and the previous average ($\bar{x}_{k-1}$) by seeing that

    $$\bar{x}_k = \frac{\bar{x}_{k-1}(k-1) + z_k}{k} = \bar{x}_{k-1} + \frac{1}{k}(z_k - \bar{x}_{k-1}).$$

    By writing each estimate in terms of the previous estimate, a weighting term ($1/k$ in this example), and the new measurement, we can allow this algorithm to run on our scale's limited memory.
    """)
    return


@app.cell(hide_code=True)
def _(key_idea):
    key_idea(
        "We avoid storing a list of all measurements by writing each estimate in terms of the previous one."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This can be implemented in python as

    ```py
    def cumulative_average(measurements):
        x_k_minus_one = 0
        output = []
        for k, z in enumerate(measurements, start=1):
            x_k = x_k_minus_one + (1/k)*(z - x_k_minus_one)
            output.append(x_k)
            x_k_minus_one = x_k
        return output
    ```
    """)
    return


@app.cell(hide_code=True)
def _(dur, mo):
    mo.md(rf"""
    Over {dur} seconds, this looks like:
    """)
    return


@app.cell(hide_code=True)
def _(cumulative_average, dur, graphic, measurements, np, pd, plt, weight):
    _measurements_df = pd.DataFrame({
        "time_s": np.arange(.1, dur+.1, .1),
        "weight_lbs": measurements,
        "cumulative_avg_weight": cumulative_average(measurements),
    })

    with plt.style.context("default"):
        _fig, _ax = plt.subplots()

        _measurements_df.plot(
            x="time_s",
            y=["weight_lbs", "cumulative_avg_weight"],
            ax=_ax,
            xlabel="Time (s)",
            ylabel="Weight (lbs.)",
            ylim=(weight-3, weight+3),
            xticks=np.arange(0, dur+.1, .2),
            yticks=np.arange(weight-3, weight+4, 1),
            rot=45,
        )
        _ax.legend(["Measurement", "Cumulative Avg"])
        _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
        _ax.set_title("Weight Measurements & Cumulative Average at 10 Hz", style='italic')

    graphic(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As desired, we can see that the orange line of averages has quickly stabalized relative to the blue measurements. While this is very close to the algorithm that real scales use, we still need one tweak.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exponential Moving Average
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Currently, our formula is

    $$\bar{x}_k = \bar{x}_{k-1} + \frac{1}{k}(z_k - \bar{x}_{k-1}),$$

    where the $\frac 1k$ term ensures that as each new measurement is added, all the measurements stay weighted equally. In practice, we tend to care more about recent measurements than past ones, so rather than using a term that decreases as $k$ grows, we use a constant smoothing factor $\alpha$:

    $$\hat{x}_k = \hat{x}_{k-1} + \alpha (z_k - \hat{x}_{k-1}).$$

    Note that we have also substituted "$\bar x$" with "$\hat x$" (pronounced "x hat"), where the hat indicates an estimated value, rather than an average. This new equation is called the exponential moving average (EMA)[^ema]. Importantly, $z_k$ has a weighting of $\alpha$, and $\hat x_{k-1}$ has a weighting of $(1-\alpha)$, so that as $\alpha$ goes to $0$, the function goes to $\hat{x}_{k-1}$, and as $\alpha$ goes to $1$, the function goes to $z_k$. In other words, each estimate is chosen to be some value between the previous estimate $\hat{x}_{k-1}$ and the new measurement $z_k$. With a smaller $\alpha$ (closer to $0$) we go closer to the prior estimate. With a larger $\alpha$ (closer to $1$) we go closer to our new measurement.

    [^ema]: The exponential moving average gets its name because each term $z_{k-n}$ is weighted by a factor of $\alpha(1-\alpha)^n$, where $k$ is the number of measurements and $n\le k$. This is clearer when the equation is rearranged into its more common form: $\hat{x}_k = \alpha z_k + (1-\alpha) \hat x_{k-1}$, and we can see that each measurement is multiplied by $\alpha$ when initially taken, and then by $(1-\alpha)$ at every iteration afterwards.
    """)
    return


@app.cell(hide_code=True)
def _(key_idea):
    key_idea(
        value=r"Each estimate is chosen to be some value between the previous estimate $\hat{x}_{k-1}$ and the new measurement \(z_k\). With a smaller $\alpha$ (closer to $0$) we choose closer to $\hat x_{k-1}$. With a larger $\alpha$ (closer to $1$) we choose closer to $z_k$."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    One additional consideration with EMA filters is initialization: our cummulative average simply returns the first measurement as the first estimate, but the EMA takes a weighted combination of each measurement with the previous estimate, so we must give it some initial value to use when calculating the first estimate. There are three common approaches to this.

    1. **First measurement initialization:** We set $\hat x_{0}$ equal to the first measurement as soon as we get it, ensuring the first estimate equals the first measurement. This is the most common and will be used here.
    2. **Zero initialization:** We set $\hat x_{0} = 0$, so that the first estimate will be $\alpha$ times the first measurement. This is extremely fast and simple, but the filtered will take some time to stabilize, especially with low $\alpha$ values, so the begining of the begining of the filtered signal may need to be cropped out.
    3. **Callibration period initialization:** We reserve some period of time at the begining of data collection for callibration, during which we average the measurements, then we set $\hat x_0$ equal to the average and begin filtering with our EMA. This is less computationally efficient and is more common in economic forecasting and stock predictions.

    Our first measurement initialization EMA can be implemented in python as:

    ```python
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
    """)
    return


@app.cell(hide_code=True)
def _(alpha_slider, mo):
    mo.md(rf"""
    By setting $\alpha = {alpha_slider.value}$, we get:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # jb: include=false
    alpha_slider = mo.ui.slider(start=0, stop=1, step=.05, value=0.05, label="$\\alpha$")
    return (alpha_slider,)


@app.cell(hide_code=True)
def _(alpha_slider, dur, ema, graphic, measurements, mo, np, pd, plt, weight):
    ema_weight = ema(alpha_slider.value, measurements)

    _measurements_df = pd.DataFrame({
        "time_s": np.arange(.1, dur+.1, .1),
        "weight_lbs": measurements,
        "ema_weight": ema_weight,
    })

    with plt.style.context("default"):
        _fig, _ax = plt.subplots()

        _measurements_df.plot(
            x="time_s",
            y=["weight_lbs", "ema_weight"],
            ax=_ax,
            xlabel="Time (s)",
            ylabel="Weight (lbs.)",
            ylim=(weight-3, weight+3),
            xticks=np.arange(0, dur+.1, .2),
            yticks=np.arange(weight-3, weight+4, 1),
            rot=45,
        )
        _ax.legend(["Measurement", "EMA"])
        _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
        _ax.set_title(f"Weight Measurements & EMA with $\\alpha = {alpha_slider.value:.2f}$", style='italic')

    mo.vstack([
        alpha_slider,
        graphic(_fig),
    ])
    return (ema_weight,)


@app.cell(hide_code=True)
def _(dur, ema_weight, mo):
    mo.md(rf"""
    where our EMA settles on ${ema_weight[-1]:.2f}$ lbs. after {dur} seconds. We have now built a filter algorithm used in the real world by millions of digital bathroom scales.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this section, we saw how to use the EMA equation

    $$\hat{x}_k = \hat{x}_{k-1} + \alpha (z_k - \hat{x}_{k-1})$$

    to estimate your weight with the assumption that your true weight does not change between measurements. In other words, in a perfect world with no noise, all of our measurements and estimates are equal (since they all equal your true weight). This assumption lets us use $\alpha$ to choose an $\hat x_k$ bewteen $\hat x_{k-1}$ and $z_k$, because without noise, these values *should* both equal $x_k$ (where the lack of hat denotes the true value at the time of the $k$-th measuremnt). Therefore, by combining the two, we increase the probability that the noise "cancels itself out", leaving us with a better estimate $\hat x_k$.

    However, we've barely scatched the surface of signal filtering. In the coming sections, we will discuss:

    - Using $\alpha$ along with a second variable $\beta$ to estimate a value that is changing
    - Using Bayesian updates to filter
    - Estimating a real-world value represented by multiple variables
    - System dynamics and signal classifications

    Throughout all these topics, the general framework of real world value, noisy measurement, filter, and estimate will remain the same.
    """)
    return


@app.cell(hide_code=True)
def _(flow, graphic, schemdraw):
    with schemdraw.Drawing(show=False) as _d:
        _d.config(fontsize=12)

        flow.Start().label("Real-world value\nwe want to know").drop("S")
        flow.Arrow().down(1)
        flow.RoundBox().label(
            "Measurement device"
        )
        flow.Arrow().down(1)
        flow.RoundBox().label("Sequence of digital\nmeasurements").drop("E")
        flow.Line().right(1)
        flow.Line().up(4)
        flow.Arrow().right(1.5)
        flow.RoundBox().label("Filter removes noise\nfrom the measurements").drop("S")
        flow.Arrow().down(1)
        flow.Terminal().label("Estimate of the real-world value")

    graphic(_d)
    return


if __name__ == "__main__":
    app.run()
