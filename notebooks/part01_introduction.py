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

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="Introduction")


@app.cell(hide_code=True)
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    numbering:
      equations: false
    -->
    """)
    return


@app.cell(hide_code=True)
def imports():
    # jb: include=false
    import marimo as mo
    import numpy as np
    import pandas as pd
    import schemdraw
    from schemdraw import flow
    from textwrap import dedent
    import matplotlib.pyplot as plt

    return dedent, flow, mo, np, pd, plt, schemdraw


@app.cell(hide_code=True)
def display_format(dedent, mo, plt, schemdraw):
    # jb: include=false
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

    return cumulative_average, ema, gaussian_noise


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It's impossibles to measure anything in the real world with 100% precision. However, by combining multiple measurements and knowledge about what's being measured, it is possible to make better estimates. This is what signal filters do.

    Humans generally have intuition on handling imperfect data: when making hard decisions, they consult multiple people (a type of social measurement) and decide based on a combination of the input received and their understanding of the situation. Moreover, most understand that getting more input can lead to better understanding even if no single piece of input is perfect.

    Signal filters follow a somewhat analogous process of using a variety of measurements to estimate some unknown quantity. For example, when weighing an object with an imprecise scale, a filter might be used to combine multiple different measurements and make a better estimate of the object's actual weight. The crucial point here is that having more measurements allows us to achieve better estimates *even if none of the measurements are 100% correct*.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    :::{attention icon=false} 🗝️ **Key Idea**
    Having more measurements allows for better estimates *even if none of the measurements are 100% correct.*
    :::
    """)
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
    Imagine we are building a digital bathroom scale to measure your body weight. When you step on the scale, a sensor—called a strain gauge load cell[^loadcell]—underneath the platform measures your downward force. The loadcell outputs an analog voltage that is then converted to a digital measurement with an analog-to-digital converter (ADC). A typical ADC such as the HX711 will sample the voltage signal between 10-80 Hz [@avia_hx711_datasheet]. Since we could represent both the output from the loadcell and the output from the ADC as funtions over time, they are both **signals**.

    [^loadcell]: A strain gauge load cell is an electronic component that converts force into proportional resistance change using metal foil grids (called strain gauges) which change resistance under load (increasing under tension and decreasing under compression). They are used in almost all digital bathroom scales because they are thin, accurate (relatively), mass-producible, and have no moving parts to wear out.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ::::{admonition icon=false} 📖 **Definition**
    :::{glossary}
    Signal
    : Any {term}`function` that represents how a quantity varies over time or space.
    :::
    ::::
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Because nobody stands perfectly still, your constant weight shifts on the scale will introduce **noise** to the measurements (and even if you were still, there would still be thermal noise in the load cell).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ::::{admonition icon=false} 📖 **Definition**
    :::{glossary}
    Noise
    : Any unwanted or random component added to a {term}`signal` that degrades or obscures the information it carries.
    :::
    ::::
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Since the stream of measurements from the ADC will constantly fluctuate, we can never know your true weight with 100% precision (remember, it's impossible to measure anything with 100% precision). Instead, we must attempt to remove the noise from this signal to make our best estimate. Hence, the term **filter**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ::::{admonition icon=false} 📖 **Definition**
    :::{glossary}
    Filter
    : Any algorithm that selectively modifies or removes noise from a {term}`signal`.
    :::
    ::::
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here is the setup we are working with at this point, where each arrow is annotated with the result or output of the prior box:
    """)
    return


@app.cell(hide_code=True)
def scale_diagram(flow, graphic, schemdraw):
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
def measurements_fig(gaussian_noise, graphic, np, pd, plt):
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
def _(mo):
    mo.md(r"""
    :::{attention icon=false} 🗝️ **Key Idea**
    Because we assume that the noise is random and has a mean of 0, we combine multiple measurements to increase the probability that the noise cancels out.
    :::
    """)
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
def _(mo):
    mo.md(r"""
    :::{attention icon=false} 🗝️ **Key Idea**
    We avoid storing a list of all measurements by writing each estimate in terms of the previous one.
    :::
    """)
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
def cumulative_avg_fig(
    cumulative_average,
    dur,
    graphic,
    measurements,
    np,
    pd,
    plt,
    weight,
):
    _measurements_df = pd.DataFrame({
        "time_s": np.arange(.1, dur+.1, .1),
        "weight_lbs": measurements,
        "cumulative_avg_weight": cumulative_average(measurements),
    })

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
def _(mo):
    mo.md(r"""
    :::{attention icon=false} 🗝️ **Key Idea**
    Each estimate is chosen to be some value between the previous estimate $\hat{x}_{k-1}$ and the new measurement $z_k$. With a smaller $\alpha$ (closer to $0$) we choose closer to $\hat x_{k-1}$. With a larger $\alpha$ (closer to $1$) we choose closer to $z_k$.
    :::
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    One additional consideration with EMA filters is initialization: our cummulative average simply returns the first measurement as the first estimate, but the EMA takes a weighted combination of each measurement with the previous estimate, so we must give it some initial value to use when calculating the first estimate. There are three common approaches to this.

    1. *First measurement initialization:* We set $\hat x_{0}$ equal to the first measurement as soon as we get it, ensuring the first estimate equals the first measurement. This is the most common and will be used here.
    2. *Zero initialization:* We set $\hat x_{0} = 0$, so that the first estimate will be $\alpha$ times the first measurement. This is extremely fast and simple, but the filtered will take some time to stabilize, especially with low $\alpha$ values, so the begining of the begining of the filtered signal may need to be cropped out.
    3. *Callibration period initialization:* We reserve some period of time at the begining of data collection for callibration, during which we average the measurements, then we set $\hat x_0$ equal to the average and begin filtering with our EMA. This is less computationally efficient and is more common in economic forecasting and stock predictions.

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
def ema_alpha_slider(mo):
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
def filter_diagram(flow, graphic, schemdraw):
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
