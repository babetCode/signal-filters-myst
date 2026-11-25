# /// script
# dependencies = [
#     "marimo>=0.25.1",
#     "matplotlib==3.11.2",
#     "numpy==2.5.3",
#     "schemdraw==0.23",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(app_title="Introduction", css_file="notebook-styles.css")


@app.cell
def frontmatter(mo):
    mo.md(r"""
    <!-- jb-frontmatter
    subtitle: "Building Intuition"
    abbreviations:
      ADC: analog-to-digital converter
      AHRS: attitude and heading reference system
      BMR: basal metabolic rate
      DEI: daily energy intake
      EMA: exponential moving average
      IMU: inertial measurement unit
      SPS: samples per second
      TDEE: total daily energy expenditure
    numbering:
      equations: false
    -->
    """)
    return


@app.cell
def imports():
    # jb: include=false
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import schemdraw
    from schemdraw import flow
    from textwrap import dedent
    from pathlib import Path

    return Path, dedent, flow, mo, np, plt, schemdraw


@app.cell
def display_settings(dedent, mo, plt, schemdraw):
    # jb: include=false
    plt.style.use("default")
    plt.rcParams["svg.hashsalt"] = "introduction_v2"  # reproducible SVG ids
    schemdraw.use("svg")

    def graphic(x):
        return mo.Html(dedent(f'''\
            <div class="graphic">
                {mo.as_html(x)}
            </div>
            '''))

    return (graphic,)


@app.cell
def data(Path, np):
    # jb: include=false
    IMAGES_DIR = Path(__file__).parent.parent / "notebooks" / "public"
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # Bathroom scale: constant true weight, HX711 at 10 SPS, 3 s of data, sigma = 1 lb
    true_weight = 155.0  # lb
    _sps = 10  # samples per second
    _k = np.arange(1, 3 * _sps + 1)  # k = 1, ..., 30
    scale_t = _k / _sps  # time of measurement k, in seconds
    scale_z = np.round(true_weight + np.random.default_rng(1).normal(0.0, 1.0, _k.size), 2)

    # Bulking: 28 daily weigh-ins, true gain 0.2 lb/day, daily reading noise sigma = 1 lb
    bulk_rate = 0.2  # lb/day (1.4 lb/week)
    bulk_days = np.arange(1, 29)
    bulk_x = true_weight + bulk_rate * (bulk_days - 1)
    bulk_z = np.round(bulk_x + np.random.default_rng(2).normal(0.0, 1.0, bulk_days.size), 1)
    return (
        IMAGES_DIR,
        bulk_days,
        bulk_rate,
        bulk_x,
        bulk_z,
        scale_t,
        scale_z,
        true_weight,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Every time we want to know a real-world value, we must measure it. Since our measurements always have limited precision, we can often combine multiple measurements to get a better estimate of the real-world value. This chapter turns that idea into a sequence of simple filters, each a small improvement on the last. By the end, we will have the basic structure of the Kalman filter, which the rest of the book builds on.

    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    More measurements can allow for better estimates, even if *none* of the measurements are 100% precise.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This can work for all sorts of measurements, from speedometers, to pacemakers, to AHRS. To see how this might work, imagine that we are building a digital bathroom scale to measure your body weight. Body weight provides a simple example because:

    1. We can assume your weight does not change over short periods of time (a few seconds).
    2. Your weight can be represented by a single number.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Measurements and Definitions

    When you step on a bathroom scale, a sensor called a strain gauge load cell[^loadcell] underneath the platform measures your downward force. The load cell outputs an analog voltage that is then converted to a sequence of digital measurements by an ADC. A typical ADC for scales, the HX711, converts the voltage to a 24-bit number either 10 or 80 times per second (10 or 80 SPS), selected by one of its pins [@avia_hx711_datasheet]. Since the output from the load cell and the output from the ADC can both be represented as functions[^informal-function] of time, we call both of them **signals**.

    [^loadcell]: A strain gauge load cell is an electronic component that converts force into a proportional change in resistance, using metal foil grids (called strain gauges) whose resistance changes under load: it increases under tension and decreases under compression. Load cells are used in almost all digital bathroom scales because they are thin, relatively accurate, mass-producible, and have no moving parts to wear out.

    [^informal-function]: Used informally here: a function assigns to each input exactly one output. Functions are defined precisely in [Chapter 2](ch2_axioms_of_set_theory_v2.md).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Signal**</u>

    A {term}`function` whose domain is a set of times (or positions) and whose value at each time (or position) is the value of some quantity, such as a voltage, a force, or a weight, at that time (or position).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this book, time is counted in **steps** $k = 1, 2, 3, \ldots$, one per measurement, and $k = 0$ stands for the starting point before any measurement has been taken. We write

    - $z_k$ for the **measurement** at step $k$ (for the scale, the $k$-th reading from the ADC, converted to pounds), and
    - $x_k$ for the **true value** at step $k$ (your true weight at the time of the $k$-th measurement).

    Both $k \mapsto z_k$ and $k \mapsto x_k$ are signals whose domain is the set of steps. We can observe every $z_k$, but we can never observe any $x_k$ directly, and that is the whole problem.

    Because nobody stands perfectly still, the force on the platform fluctuates as your weight shifts, so the measurements differ from your true weight. Even if you stood perfectly still, electrical fluctuations in the load cell and the ADC would remain. We call these differences **noise**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Noise**</u>

    The difference between a measured {term}`signal` and the true signal it represents. For measurements $z_k$ of true values $x_k$, the noise at step $k$ is $z_k - x_k$.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Like the true value, the noise can never be observed directly, since computing $z_k - x_k$ would require knowing $x_k$. To reason about how large it tends to be, [Chapter 5](ch5_random_variables_v2.md) will model it as random.

    Since the stream of measurements from the ADC constantly fluctuates, we can never know your true weight with 100% precision (remember, it's impossible to measure anything with 100% precision). The best we can do is to compute an **estimate** of it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Estimate**</u>

    A value that is computed from measurements (and from assumptions fixed in advance, such as "the weight does not change") and is used in place of an unknown true value. We write $\hat x_k$ ("x hat") for the estimate of $x_k$ computed after the measurement $z_k$ has been incorporated.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The **error** of an estimate is $\hat x_k - x_k$: positive when we overestimate and negative when we underestimate. Like the noise, it can never be computed, because $x_k$ is unknown; our goal is to keep it small. [Chapter 6](ch6_expectation_and_variance_v2.md) treats the rule that produces estimates as a mathematical object of its own (an *estimator*), and [Chapter 7](ch7_optimal_alpha_v2.md) gives the error a symbol and measures "small" precisely.

    To keep the error small, we must remove as much of the noise as we can, hence the term **filter**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Filter**</u>

    An algorithm that maps a sequence of measurements $z_1, z_2, z_3, \ldots$ to a sequence of {term}`estimates <estimate>` $\hat x_1, \hat x_2, \hat x_3, \ldots$ in such a way that each estimate $\hat x_k$ is computed from $z_1, \ldots, z_k$ only (together with choices fixed in advance, such as a starting value).
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Requiring each $\hat x_k$ to use only the measurements received so far means that a filter can run in real time, producing each estimate as soon as its measurement arrives. An algorithm that may also use later measurements $z_{k+1}, z_{k+2}, \ldots$ to estimate $x_k$ is called a *smoother* instead.

    In general, a filter used to estimate a real-world value receives a sequence[^informal-sequence] of digital measurements and outputs a sequence of estimates:

    [^informal-sequence]: Used informally here: a list $z_1, z_2, z_3, \ldots$ indexed by the steps. Sequences are defined precisely in [Chapter 3](ch3_sets_for_probability_v2.md).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/intro_filter_diagram_v2.svg" class="graphic" alt="Flow diagram: a real-world value is measured by a measurement device, producing a sequence of digital measurements, which a filter turns into an estimate of the real-world value." />
    """)
    return


@app.cell(hide_code=True)
def make_filter_diagram(IMAGES_DIR, flow, schemdraw):
    # jb: include=false
    with schemdraw.Drawing(show=False) as _d:
        _d.config(fontsize=12)

        flow.Start().label("Real-world value\nwe want to know").drop("S")
        flow.Arrow().down(1)
        flow.RoundBox().label("Measurement device")
        flow.Arrow().down(1)
        flow.RoundBox().label("Sequence of digital\nmeasurements").drop("E")
        flow.Line().right(1)
        flow.Line().up(4)
        flow.Arrow().right(1.5)
        flow.RoundBox().label("Filter removes noise\nfrom the measurements").drop("S")
        flow.Arrow().down(1)
        flow.Terminal().label("Estimate of the real-world value")

    _d.save(IMAGES_DIR / "intro_filter_diagram_v2.svg")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For our particular example of a scale measuring weight, this sequence looks like the following (each arrow is labeled with the output of the box before it):
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/intro_scale_diagram_v2.svg" class="graphic" alt="Flow diagram: force on the platform tenses and compresses strain gauges; the load cell outputs a continuous analog voltage; the ADC samples it into a sequence of digital measurements; the filter turns these into a weight estimate, shown as the scale reading." />
    """)
    return


@app.cell(hide_code=True)
def make_scale_diagram(IMAGES_DIR, flow, schemdraw):
    # jb: include=false
    with schemdraw.Drawing(show=False) as _d:
        _d.config(fontsize=12)

        flow.Start().label("Force is applied to\nthe scale's platform").drop("S")
        flow.Arrow().down(1).label(
            "Tensed/compressed\nstrain gauges", loc="bottom"
        )
        flow.RoundBox().label(
            "Load cell measures force\nvia strain gauge resistance"
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

    _d.save(IMAGES_DIR / "intro_scale_diagram_v2.svg")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Averaging Measurements

    We have yet to explain *how* a filter could remove noise, but we're getting there. Imagine you step on the scale and the first 10 measurements look like this:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/intro_weight_measurements_fig_v2.svg" class="graphic" alt="Ten weight measurements taken 0.1 s apart, scattered between about 153.7 and 155.9 lb." />
    """)
    return


@app.cell(hide_code=True)
def make_weight_measurements_fig(
    IMAGES_DIR,
    np,
    plt,
    scale_t,
    scale_z,
    true_weight,
):
    # jb: include=false
    _fig, _ax = plt.subplots(figsize=(7, 4))
    _ax.plot(
        scale_t[:10], scale_z[:10], "o",
        markerfacecolor="none", markeredgecolor="black", label="Measurement $z_k$",
    )
    _ax.set(
        xlabel="Time (s)",
        ylabel="Weight (lb)",
        xticks=scale_t[:10],
        ylim=(true_weight - 3, true_weight + 3),
        yticks=np.arange(true_weight - 3, true_weight + 4, 1),
    )
    _ax.legend(loc="upper right")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.set_title("Weight Measurements at 10 SPS", style="italic")
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "intro_weight_measurements_fig_v2.svg", metadata={"Date": None})
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can immediately tell that you're in the mid-150s, but we're not sure exactly where. The fluctuations look random[^informal-random]: some readings are too high and others too low. We will make two assumptions about the noise:

    1. **Zero mean:** if the same measurement could be repeated many times, its noise would average out to 0 lb[^zero-mean]. In other words, the scale does not systematically read too high or too low.
    2. **Unrelated noise:** the noise in one measurement tells us nothing about the noise in any other[^unrelated].

    Under these assumptions, averaging measurements makes the noise cancel out in a precise sense. The average of $k$ measurements is centered on the true value, just like a single measurement, but the variance[^informal-variance] of its noise (roughly, the average squared size of the noise) is $1/k$ times as large. Since the typical size of the noise is the square root of its variance, the typical error shrinks like $1/\sqrt{k}$: if a single measurement typically misses by about 1 lb, as our simulated scale does, then the average of 30 measurements typically misses by only about $1/\sqrt{30} \approx 0.18$ lb.

    [^informal-random]: Used informally here: we cannot predict the next fluctuation. Randomness is made precise by probability spaces in [Chapter 4](ch4_probability_spaces_v2.md) and random variables in [Chapter 5](ch5_random_variables_v2.md).

    [^zero-mean]: The mean (or *expected value*) is defined in [Chapter 6](ch6_expectation_and_variance_v2.md). This is an assumption about the *mean* of the noise, not its median: the noise may be negative more often than positive, as long as its positive values are correspondingly larger, so that it still averages out to zero.

    [^unrelated]: [Chapter 5](ch5_random_variables_v2.md) makes this precise as *independence*, and [Chapter 6](ch6_expectation_and_variance_v2.md) shows that the weaker condition of being *uncorrelated* is enough for the variance result. We also assume every measurement is equally noisy, which is reasonable for repeated readings from the same scale.

    [^informal-variance]: Used informally here. Variance is defined in [Chapter 6](ch6_expectation_and_variance_v2.md), which also proves the result quoted here: the average of $k$ measurements whose noise has mean zero and variance $\sigma^2$, and is uncorrelated between measurements, has mean equal to the true value and variance $\sigma^2/k$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    If the noise has mean zero and the noise in different measurements is unrelated, then the error of the average of $k$ measurements also has mean zero, and its variance is $1/k$ times the variance of a single measurement's noise.
    ///

    /// caution | ⚠️ **Assumptions and Failure Modes**
        attrs: {class: no-icon}
    Averaging relies on three assumptions, and each one can fail:

    - **The true value is constant.** If it changes while we average (you are still stepping onto the platform, or you pick up a cat), the average mixes old and new values and lags behind the truth. Most of the rest of this chapter deals with this failure.
    - **The noise has mean zero.** If every reading is 2 lb too high because the scale is miscalibrated, then so is the average of any number of readings: averaging cannot remove an error that every measurement shares. [Chapter 11](ch11_measurement_functions_v2.md) treats such sensor bias.
    - **The noise in different measurements is unrelated.** If you sway slowly back and forth, neighboring readings err in the same direction, and averaging $k$ of them reduces the variance by much less than a factor of $k$.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The most basic way to combine measurements is by averaging them. For example, if we only had the first two measurements, our estimate would be
    """)
    return


@app.cell(hide_code=True)
def _(mo, scale_z):
    mo.md(rf"""
    $$({scale_z[0]:.2f} + {scale_z[1]:.2f})/2 = {(scale_z[0] + scale_z[1]) / 2:.2f}\text{{ lb}}.$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    After the third, we would have
    """)
    return


@app.cell(hide_code=True)
def _(mo, scale_z):
    mo.md(rf"""
    $$({scale_z[0]:.2f} + {scale_z[1]:.2f} + {scale_z[2]:.2f})/3 = {(scale_z[0] + scale_z[1] + scale_z[2]) / 3:.2f}\text{{ lb}},$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    and so on. Under the assumptions above, the more measurements we average, the smaller the variance of our estimate's error.

    This seems like a good strategy, but our list of measurements grows quickly, and a scale's microcontroller may have only 64 of its 256 bytes of data memory available for data processing [@holtek_ht45f75_data_sheet]. With each measurement stored as a 32-bit integer (4 bytes), 64 bytes hold only 16 measurements, so at 10 SPS the memory would be full within 1.6 seconds.

    We don't actually need the whole list, though. The average only needs two numbers: the running sum $z_1 + z_2 + \cdots + z_k$ and the count $k$. But the sum has a different problem: it grows without bound. The HX711 reports each measurement as a 24-bit signed integer, which can be as large as $2^{23}$ in magnitude, while a 32-bit signed integer can hold numbers only up to about $2^{31}$ in magnitude. Since $2^{31}/2^{23} = 256$, a sum of more than 256 full-scale measurements can overflow: after about 26 seconds at 10 SPS, or about 3 seconds at 80 SPS. (Low-cost microcontrollers often lack floating-point hardware, so integer arithmetic is the natural choice.) Instead, we will store two different numbers: the count and the previous *average*, which can never grow larger than the measurements themselves.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A Recursive Average

    Let our measurements be denoted $z_1, z_2, z_3, \ldots$, so that after $k$ measurements, we have $z_1, z_2, \ldots, z_k$. After $k-1$ measurements, our average is

    $$\bar{x}_{k-1} = \frac{z_1 + z_2 + \cdots + z_{k-1}}{k-1},$$

    and after $k$ measurements it is

    $$\bar{x}_k = \frac{z_1 + z_2 + \cdots + z_{k-1} + z_k}{k}.$$

    Here $\bar{x}_k$ is pronounced "x bar", where the bar is statistical notation for an average; it is our estimate, $\hat x_k = \bar x_k$. Multiplying the first equation by $k-1$ shows that $z_1 + \cdots + z_{k-1} = (k-1)\bar x_{k-1}$. Substituting this into the second equation, we can calculate each $\bar{x}_k$ from just the number of measurements ($k$), the previous average ($\bar{x}_{k-1}$), and the new measurement ($z_k$): for every $k \ge 2$,

    $$\bar{x}_k = \frac{(k-1)\bar{x}_{k-1} + z_k}{k} = \frac{k\bar x_{k-1} - \bar x_{k-1} + z_k}{k} = \bar{x}_{k-1} + \frac{1}{k}(z_k - \bar{x}_{k-1}).$$

    For $k = 1$ the same formula gives $\bar x_1 = \bar x_0 + (z_1 - \bar x_0) = z_1$ whatever starting value $\bar x_0$ we choose, so it holds for every $k \ge 1$. By writing each estimate in terms of the previous estimate, a weighting term[^weighting-term], and the new measurement, we can run this algorithm while storing only two numbers, $k$ and $\bar x_{k-1}$.

    [^weighting-term]: We are using $\frac{1}{k}$ as our weighting here, but we will soon see other options.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The recursive form has a useful interpretation. Before $z_k$ arrives, our best guess for $x_k$ is $\bar x_{k-1}$: we assumed your weight does not change, so our estimate of $x_{k-1}$ is also our guess for $x_k$. A guess made *before* the measurement is called a **prediction**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Prediction**</u>

    An {term}`estimate` of $x_k$ that is formed before the measurement $z_k$ is incorporated, that is, computed from $z_1, \ldots, z_{k-1}$ only (together with choices fixed in advance). We write it $\hat x_k^-$, where the minus sign means "before $z_k$".
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The difference between what we measure and what we predicted is the part of $z_k$ that the prediction did not anticipate: the new information the measurement brings. It is therefore called the **innovation**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Innovation**</u>

    The difference $\tilde y_k = z_k - \hat x_k^-$ between the measurement $z_k$ and the {term}`prediction` $\hat x_k^-$ of $x_k$.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With the prediction $\hat x_k^- = \hat x_{k-1}$, the recursive average becomes

    $$\hat x_k = \hat x_k^- + \frac{1}{k}\,\tilde y_k:$$

    the new estimate is the prediction plus a weight times the innovation. Compared with storing a running sum, this form has three advantages:

    1. **Bounded magnitude.** Rearranged, $\bar x_k = \left(1 - \frac1k\right)\bar x_{k-1} + \frac1k z_k$. This is a weighted combination of $\bar x_{k-1}$ and $z_k$ whose weights lie between 0 and 1 and add up to 1, so $\bar x_k$ lies between $\bar x_{k-1}$ and $z_k$. Starting from $\bar x_1 = z_1$ and repeating this argument one step at a time (a proof by induction, [Chapter 2](ch2_axioms_of_set_theory_v2.md)) shows that every $\bar x_k$ lies between the smallest and the largest measurement so far. The stored estimate therefore fits in any number format that can hold one measurement, and the innovation $z_k - \bar x_{k-1}$, a difference of two such numbers, needs just one extra bit[^fixed-point].
    2. **An estimate at every step.** The stored number *is* the current estimate, ready to display after every measurement with no extra work.
    3. **A structure that generalizes.** *Prediction + weight × innovation* is the shape of every filter we build in this book, up to and including the Kalman filter. Only the prediction and the weight will change.

    [^fixed-point]: In integer arithmetic, dividing by $k$ rounds the result. Storing the estimate with a few extra fractional bits (fixed-point arithmetic) keeps this rounding error small.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    We avoid storing every measurement, and keep every stored number bounded, by writing each estimate in terms of the previous one: the new estimate is the prediction plus a weight times the innovation.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This can be implemented in Python as:
    """)
    return


@app.cell
def _(np):
    # jb: echo=true
    def cumulative_average(measurements):
        """Return the recursive averages x̂_1, ..., x̂_k of the measurements z_1, ..., z_k."""
        x_hat = 0.0  # x̂_0: any value works, because the first step gives x̂_1 = z_1
        estimates = []
        for k, z in enumerate(measurements, start=1):
            x_pred = x_hat  # prediction: the weight is assumed constant
            x_hat = x_pred + (1 / k) * (z - x_pred)  # prediction + weight × innovation
            estimates.append(x_hat)
        return np.array(estimates)

    return (cumulative_average,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Over 3 seconds, this looks like:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/intro_cumulative_avg_fig_v2.svg" class="graphic" alt="Thirty weight measurements over 3 seconds with their cumulative average, which settles close to the true weight of 155 lb." />
    """)
    return


@app.cell(hide_code=True)
def make_cumulative_avg_fig(
    IMAGES_DIR,
    cumulative_average,
    np,
    plt,
    scale_t,
    scale_z,
    true_weight,
):
    # jb: include=false
    _fig, _ax = plt.subplots(figsize=(7, 4))
    _ax.axhline(true_weight, color="black", linewidth=1.2, label="True weight $x_k$")
    _ax.plot(
        scale_t, scale_z, "o",
        markerfacecolor="none", markeredgecolor="black", label="Measurement $z_k$",
    )
    _ax.plot(
        scale_t, cumulative_average(scale_z), color="C1", marker=".",
        label=r"Cumulative average $\hat{x}_k$",
    )
    _ax.set(
        xlabel="Time (s)",
        ylabel="Weight (lb)",
        xticks=np.arange(0, 3.01, 0.2),
        ylim=(true_weight - 3, true_weight + 3),
        yticks=np.arange(true_weight - 3, true_weight + 4, 1),
    )
    _ax.tick_params(axis="x", labelrotation=45)
    _ax.legend(loc="upper right")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.set_title("Weight Measurements & Cumulative Average at 10 SPS", style="italic")
    _fig.tight_layout()
    _fig.savefig(IMAGES_DIR / "intro_cumulative_avg_fig_v2.svg", metadata={"Date": None})
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As desired, the estimates (orange) have quickly stabilized relative to the measurements (circles), and they stay close to the true weight (black line), which the filter never sees. This is a reasonable algorithm for a scale, but real scales face one more complication.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exponential Moving Average

    Currently, our formula is

    $$\hat{x}_k = \hat{x}_{k-1} + \frac{1}{k}(z_k - \hat{x}_{k-1}),$$

    where the $\frac 1k$ term ensures that as each new measurement is added, all the measurements stay weighted equally. If your weight really is constant, that is exactly right: [Chapter 7](ch7_optimal_alpha_v2.md) proves that, under the assumptions above, no other choice of weights in this recursive form gives an error with smaller variance. On a real scale, however, "constant" only holds approximately: the reading ramps up while you step on, you shift your weight, or you pick up your cat. After $k$ measurements, a new measurement gets a weight of only $\frac1k$, so the longer the cumulative average runs, the more slowly it responds to any real change.

    In practice, we therefore care more about recent measurements than old ones, and rather than using a weight that decreases as $k$ grows, it's common to use a constant weight $\alpha$:

    $$\hat{x}_k = \hat{x}_{k-1} + \alpha (z_k - \hat{x}_{k-1}).$$

    This equation is called the EMA.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// note | 📖 **Definition**
        attrs: {class: no-icon}
    <u>**Exponential moving average**</u>

    A {term}`filter` that, for a constant $\alpha$ with $0 < \alpha < 1$ (the *smoothing factor*), starts from an initial value $\hat x_0$ and computes each estimate as $\hat x_k = \hat x_{k-1} + \alpha(z_k - \hat x_{k-1})$ for $k = 1, 2, 3, \ldots$
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The prediction is still $\hat x_k^- = \hat x_{k-1}$, because we still assume the true value does not change, so the EMA again has the form *prediction + weight × innovation*, with the constant weight $\alpha$ in place of $\frac1k$. Rearranged into its more common form, it reads

    $$\hat{x}_k = \alpha z_k + (1-\alpha) \hat x_{k-1},$$

    so $z_k$ has a weight of $\alpha$ and $\hat x_{k-1}$ has a weight of $1-\alpha$[^ema]. As $\alpha$ goes to $0$, $\hat x_k$ goes to $\hat{x}_{k-1}$, and as $\alpha$ goes to $1$, $\hat x_k$ goes to $z_k$. In other words, each estimate is some value between the previous estimate $\hat{x}_{k-1}$ and the new measurement $z_k$. With a smaller $\alpha$ (closer to $0$), we stay closer to the previous estimate. With a larger $\alpha$ (closer to $1$), we move closer to the new measurement.

    Choosing $\alpha$ is therefore a trade-off between noise and lag:

    - A **small** $\alpha$ spreads the weight over many past measurements, so more noise is averaged away, but the EMA responds slowly to real changes: it *lags* behind them.
    - A **large** $\alpha$ responds quickly to real changes, but it averages over fewer measurements, so more noise gets through.

    [Chapter 6](ch6_expectation_and_variance_v2.md) quantifies both sides of this trade-off and finds the $\alpha$ that balances them when the true value changes at a constant rate.

    [^ema]: The exponential moving average gets its name from the weights it gives to past measurements. Substituting $\hat x_{k-1} = \alpha z_{k-1} + (1-\alpha)\hat x_{k-2}$ into $\hat x_k = \alpha z_k + (1-\alpha)\hat x_{k-1}$, then substituting for $\hat x_{k-2}$ in the same way, and so on down to $\hat x_0$ (formally, a proof by induction) gives
        $$\hat x_k = \sum_{n=0}^{k-1} \alpha(1-\alpha)^n z_{k-n} + (1-\alpha)^k\,\hat x_0.$$
        Each measurement is multiplied by $\alpha$ when it arrives and by $(1-\alpha)$ at every step afterward, so the measurement from $n$ steps ago, $z_{k-n}$ with $0 \le n \le k-1$, has weight $\alpha(1-\alpha)^n$: the weights decay exponentially with age. By the formula for a geometric sum ([Appendix C: Series](appendix_c_calculus_v2.md)), these weights add up to $1 - (1-\alpha)^k$, and the initial value $\hat x_0$ gets the remaining $(1-\alpha)^k$. With first-measurement initialization ($\hat x_0 = z_1$, described below), $z_1$ appears twice, and its total weight is $\alpha(1-\alpha)^{k-1} + (1-\alpha)^k = (1-\alpha)^{k-1}$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    Each estimate is chosen to be some value between the previous estimate $\hat{x}_{k-1}$ and the new measurement $z_k$. With a smaller $\alpha$ (closer to $0$), we choose closer to $\hat x_{k-1}$, which averages away more noise but responds more slowly to real changes. With a larger $\alpha$ (closer to $1$), we choose closer to $z_k$, which responds faster but lets more noise through.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Initialization

    One additional consideration with EMA filters is initialization. The cumulative average returns the first measurement as its first estimate no matter what $\bar x_0$ is, because its first weight is $\frac11 = 1$. The EMA's weight is $\alpha < 1$, so we must give it a starting value $\hat x_0$ to combine with the first measurement. There are three common approaches:

    1. *First-measurement initialization:* We set $\hat x_0 = z_1$ as soon as we get the first measurement, ensuring that the first estimate equals the first measurement, $\hat x_1 = z_1$. This is the most common approach and the one we use here.
    2. *Zero initialization:* We set $\hat x_0 = 0$, so that the first estimate is $\hat x_1 = \alpha z_1$. This is fast and simple, but the filter takes some time to stabilize, especially with low $\alpha$ values: since each step multiplies the weight of $\hat x_0$ by $1-\alpha$, it still carries a weight of $(1-\alpha)^k$ after $k$ steps. With $\alpha = 0.1$, that is about 10% after 22 measurements, enough to pull a 155 lb reading down by about 15 lb, so the beginning of the filtered signal may need to be cropped out.
    3. *Calibration-period initialization:* We reserve some period of time at the beginning of data collection for calibration, during which we average the measurements. Then we set $\hat x_0$ equal to that average and begin filtering with our EMA. This is less computationally efficient and is more common in economic forecasting and stock predictions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Implementation

    Our EMA with first-measurement initialization can be implemented in Python as:
    """)
    return


@app.cell
def _(np):
    # jb: echo=true
    def ema(measurements, alpha):
        """Return the EMA estimates x̂_1, ..., x̂_k, with first-measurement initialization."""
        x_hat = measurements[0]  # x̂_0 = z_1, so that x̂_1 = z_1
        estimates = []
        for z in measurements:
            x_pred = x_hat  # prediction: the weight is assumed constant
            x_hat = x_pred + alpha * (z - x_pred)  # prediction + α × innovation
            estimates.append(x_hat)
        return np.array(estimates)

    return (ema,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Use the slider to choose $\alpha$; the cumulative average (gray, dashed) is shown for comparison. Then tick the box to pick up a 10 lb cat halfway through, so that the true value is no longer constant.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    ema_alpha = mo.ui.slider(
        start=0.05, stop=0.95, step=0.05, value=0.1, label=r"$\alpha$", show_value=True
    )
    ema_cat = mo.ui.checkbox(value=False, label="Pick up a 10 lb cat at 1.5 s")
    return ema_alpha, ema_cat


@app.cell(hide_code=True)
def ema_fig_interactive(
    cumulative_average,
    ema,
    ema_alpha,
    ema_cat,
    graphic,
    mo,
    np,
    plt,
    scale_t,
    scale_z,
    true_weight,
):
    _cat = np.where(scale_t > 1.5, 10.0, 0.0) if ema_cat.value else np.zeros_like(scale_t)
    ema_truth = true_weight + _cat
    _z = scale_z + _cat
    ema_estimates = ema(_z, ema_alpha.value)
    ema_averages = cumulative_average(_z)

    _fig, _ax = plt.subplots(figsize=(7, 4.2))
    _ax.plot(scale_t, ema_truth, color="black", linewidth=1.2, label="True value $x_k$")
    _ax.plot(
        scale_t, _z, "o",
        markerfacecolor="none", markeredgecolor="black", label="Measurement $z_k$",
    )
    _ax.plot(scale_t, ema_averages, "--", color="0.5", label="Cumulative average")
    _ax.plot(
        scale_t, ema_estimates, color="C1", marker=".",
        label=rf"EMA $\hat{{x}}_k$, $\alpha = {ema_alpha.value:.2f}$",
    )
    _top = true_weight + (14 if ema_cat.value else 3)
    _ax.set(
        xlabel="Time (s)",
        ylabel="Weight (lb)",
        xticks=np.arange(0, 3.01, 0.2),
        ylim=(true_weight - 3, _top),
    )
    _ax.tick_params(axis="x", labelrotation=45)
    _ax.legend(loc="upper left", fontsize="small")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.set_title(
        rf"Weight Measurements & EMA with $\alpha = {ema_alpha.value:.2f}$", style="italic"
    )
    _fig.tight_layout()
    _out = graphic(_fig)
    plt.close(_fig)

    mo.vstack([mo.hstack([ema_alpha, ema_cat], justify="start", gap=2), _out])
    return ema_averages, ema_estimates, ema_truth


@app.cell(hide_code=True)
def _(ema_averages, ema_estimates, ema_truth, mo, scale_t):
    mo.md(rf"""
    After {scale_t[-1]:.0f} seconds, the EMA reads {ema_estimates[-1]:.2f} lb and the cumulative average reads {ema_averages[-1]:.2f} lb, while the true value is {ema_truth[-1]:.0f} lb.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Without the cat, the EMA has no advantage: for a constant weight, the cumulative average has the smallest error variance (Chapter 7 proves this), and larger values of $\alpha$ visibly let more noise through. With the cat, the cumulative average is still about halfway between the old and new values at the end, because the 15 measurements taken before the cat still make up half of its average, while the EMA closes most of the gap, and closes it faster the larger $\alpha$ is. We have now built a simple filter of the kind found in many digital scales and other embedded devices.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The EMA works because we've assumed that your true weight changes little between measurements: in a world with no noise, all of our measurements and estimates would equal the same true value $x_k$. Combining them therefore averages the noise, and under the zero-mean and unrelated-noise assumptions, this shrinks its variance. [Chapter 6](ch6_expectation_and_variance_v2.md) shows that for a constant true value, the variance of the EMA's error approaches $\frac{\alpha}{2-\alpha}$ times the variance of a single measurement's noise: about $0.05$ times for $\alpha = 0.1$. Unlike the variance of the cumulative average, which keeps shrinking like $\frac1k$, the variance of the EMA stops shrinking. That is the price of its constant attention to recent measurements.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    We can use the EMA equation

    $$\hat{x}_k = \hat{x}_{k-1} + \alpha (z_k - \hat{x}_{k-1})$$

    to estimate a real-world value with the assumption that it changes little between measurements. If we expect noisier measurements, we should pick a smaller $\alpha$; if we expect the true value to change faster, we should pick a larger one.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If we expect our real-world value to change *steadily* between measurements, we will have to update our filtering strategy.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Alpha-Beta Filter

    ### Predicting the Change

    Our EMA relied on the assumption that your true weight does not change between measurements, which is what made the previous estimate $\hat x_{k-1}$ a sensible prediction of $x_k$. If we *do* expect the true value to change, then even a perfect previous estimate, $\hat x_{k-1} = x_{k-1}$, would miss $x_k$ by the change $x_k - x_{k-1}$.

    So we predict the change, too. Let $\Delta x_k$ be the change we *expect* from step $k-1$ to step $k$, and predict

    $$\hat x_k^- = \hat x_{k-1} + \Delta x_k.$$

    In a world with no noise, where $\hat x_{k-1} = x_{k-1}$, $z_k = x_k$, and the actual change $x_k - x_{k-1}$ is exactly the expected change $\Delta x_k$, this prediction would be exactly right:

    $$\hat x_k^- = x_{k-1} + (x_k - x_{k-1}) = x_k = z_k.$$

    You might say, "Well, of course if there were no imperfections then our estimates and measurements would be perfect, but how is that useful?" It tells us that $\hat x_k^-$ and $z_k$ are two attempts at the same number, $x_k$, each spoiled only by noise. So we can use the same strategy as the EMA, and choose a value between them with a weight $\alpha$:

    $$\hat{x}_k = \hat x_k^- + \alpha (z_k - \hat x_k^-) = \hat x_k^- + \alpha\,\tilde y_k.$$

    We will call this the *alpha filter*. It has exactly the form of the EMA, *prediction + weight × innovation*, but with a better prediction. (With $\Delta x_k = 0$, it *is* the EMA.)

    Notice the difference between the *expected* change $\Delta x_k$, which we choose before seeing $z_k$, and the *actual* change $x_k - x_{k-1}$, which we never observe. In reality the two differ: your weight changes from day to day in ways no diet plan predicts. The gap $(x_k - x_{k-1}) - \Delta x_k$ between the actual and the expected change is called *process noise*[^informal-process-noise], because it is noise in the process we are measuring rather than in the measurement. It makes the prediction $\hat x_k^-$ noisy even when $\hat x_{k-1}$ is perfect, which is one more reason to combine the prediction with the measurement instead of trusting either one alone.

    [^informal-process-noise]: Used informally here. {term}`Process noise` is defined precisely in [Chapter 9](ch9_noise_levels_v2.md), which also shows how to choose $\alpha$ when both kinds of noise are present.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// attention | 🗝️ **Key Idea**
        attrs: {class: no-icon}
    If we can predict $x_k$ from $\hat x_{k-1}$ with a prediction that would be exactly right without noise, then we can combine the prediction with the measurement, using some weight $\alpha$, so that part of the noise in each averages out.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Step-by-Step Example

    As an example, imagine that after weighing yourself on your bathroom scale, you decide to start eating more in order to bulk up. You start weighing yourself every morning for four weeks to track your weight gain. For our EMA, we had 10 measurements per second. Here, we are only taking one measurement per day, and each daily reading is off by about 1 lb in either direction because of the water and food in your body[^daily-noise]:

    [^daily-noise]: Each daily reading is itself the output of the scale's own filter, so the scale's electrical noise is small. What remains is mostly real day-to-day variation in the water and food in your body. Since we want to track the slow trend in your weight, we treat that variation as noise: the "true value" $x_k$ is the trend.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <img src="public/intro_alpha_beta_weight_measurements_fig_v2.svg" class="graphic" alt="Twenty-eight daily weigh-ins that scatter by about a pound around a slowly rising trend, from about 155 lb to about 160 lb." />
    """)
    return


@app.cell(hide_code=True)
def make_alpha_beta_weight_measurements_fig(
    IMAGES_DIR,
    bulk_days,
    bulk_z,
    np,
    plt,
):
    # jb: include=false
    _fig, _ax = plt.subplots(figsize=(7, 4))
    _ax.plot(
        bulk_days, bulk_z, "o",
        markerfacecolor="none", markeredgecolor="black", label="Measurement $z_k$",
    )
    _ax.set(
        xlabel="Time (days)",
        ylabel="Weight (lb)",
        xticks=bulk_days,
        ylim=(np.floor(bulk_z.min()) - 1, np.ceil(bulk_z.max()) + 1),
    )
    _ax.tick_params(axis="x", labelrotation=45)
    _ax.legend(loc="upper left")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.set_title("Bulking Daily Weigh-Ins", style="italic")
    _fig.tight_layout()
    _fig.savefig(
        IMAGES_DIR / "intro_alpha_beta_weight_measurements_fig_v2.svg", metadata={"Date": None}
    )
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    How fast should we expect your weight to change? An energy-balance estimate[^delta-prediction] predicts that if you eat about 3,230 kcal per day, you will gain about 0.2 lb per day (1.4 lb per week). So we choose the same expected change every day, $\Delta x_k = 0.2$ lb, together with the weight $\alpha = 0.2$.

    [^delta-prediction]: For our example person, a moderately active 23-year-old man who is 175 cm tall and weighs 155 lb (70.3 kg), a realistic weight gain rate can be obtained with the following strategy:
        - Use the Mifflin–St Jeor estimate for BMR:
          $$\text{BMR} \approx 10(\text{weight in kg}) + 6.25(\text{height in cm}) - 5(\text{age in years}) + 5 \approx 1{,}687\text{ kcal/day}.$$
          (For women, the final $+5$ is replaced by $-161$.)
        - TDEE is commonly estimated by multiplying BMR by some activity multiplier. For moderate activity, 1.5 is used:
          $$\text{TDEE} \approx 1.5\,\text{BMR} \approx 2{,}530\text{ kcal/day}.$$
        - Estimate the energy balance from DEI and TDEE:
          $$\text{Energy Balance} = \text{DEI} - \text{TDEE}.$$
        - Max Wishnofsky's 1958 paper, *Caloric Equivalents of Gained or Lost Weight*, estimates that $3{,}500\text{ kcal} \approx 1\text{ lb}$ of body weight [@wishnofsky1958].
        - Estimate the weight gain:
          $$\text{Weight Gain (lb/day)} = \frac{\text{Energy Balance}}{3{,}500}.$$
          Gaining 0.2 lb per day therefore takes a surplus of $0.2 \times 3{,}500 = 700$ kcal per day, that is, a DEI of about $2{,}530 + 700 = 3{,}230$ kcal per day.

        All of these are rough population averages, so your true rate may well differ from the prediction; the rest of this section shows what happens when $\Delta x_k$ is wrong. Also, TDEE grows with body weight, so the same intake produces slightly less gain as you grow; [Chapter 10](ch10_process_models_v2.md) builds this into the prediction.
    """)
    return


@app.cell
def step_example(bulk_z):
    # jb: include=false
    # Hand computation of the first three days with alpha = 0.2 and expected change 0.2 lb/day
    _alpha, _dx = 0.2, 0.2
    ex_z = bulk_z[:3]
    ex_pred2 = ex_z[0] + _dx
    ex_innov2 = ex_z[1] - ex_pred2
    ex_est2 = ex_pred2 + _alpha * ex_innov2
    ex_pred3 = ex_est2 + _dx
    ex_innov3 = ex_z[2] - ex_pred3
    ex_est3 = ex_pred3 + _alpha * ex_innov3
    return ex_est2, ex_est3, ex_innov2, ex_innov3, ex_pred2, ex_pred3, ex_z


@app.cell(hide_code=True)
def _(
    ex_est2,
    ex_est3,
    ex_innov2,
    ex_innov3,
    ex_pred2,
    ex_pred3,
    ex_z,
    mo,
):
    mo.md(rf"""
    **Day 1:** The scale reads $z_1 = {ex_z[0]:.1f}$ lb. Using first-measurement initialization, we set our first estimate

    $$\hat x_1 = z_1 = {ex_z[0]:.1f}\text{{ lb}}.$$

    **Day 2:**

    - <u>Prediction Step</u>

      First we predict $x_2$ by adding the expected change to our previous estimate:

      $$\hat x^-_2 = \hat x_1 + \Delta x_2 = {ex_z[0]:.1f} + 0.2 = {ex_pred2:.2f}\text{{ lb}}.$$

    - <u>Measurement Update Step</u>

      Next, we use the measurement to update this prediction. The scale reads $z_2 = {ex_z[1]:.1f}$ lb, so the innovation is $\tilde y_2 = z_2 - \hat x^-_2 = {ex_innov2:.2f}$ lb, and our second estimate is

      $$\hat x_2 = \hat x^-_2 + \alpha\tilde y_2 = {ex_pred2:.2f} + 0.2\,({ex_innov2:.2f}) = {ex_est2:.2f}\text{{ lb}}.$$

    **Day 3:**

    - <u>Prediction Step</u>

      $$\hat x^-_3 = \hat x_2 + \Delta x_3 = {ex_est2:.2f} + 0.2 = {ex_pred3:.2f}\text{{ lb}}.$$

    - <u>Measurement Update Step</u>

      The scale reads $z_3 = {ex_z[2]:.1f}$ lb, so $\tilde y_3 = {ex_innov3:.2f}$ lb and

      $$\hat x_3 = \hat x^-_3 + \alpha\tilde y_3 = {ex_pred3:.2f} + 0.2\,({ex_innov3:.2f}) = {ex_est3:.2f}\text{{ lb}}.$$

    And then we continue in this fashion, repeating the prediction step and then the measurement update step for each of our future measurements.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The Alpha Filter in Code

    In code, this could look like:
    """)
    return


@app.cell
def _(np):
    # jb: echo=true
    def alpha_filter(measurements, alpha, delta_x):
        """Alpha filter with first-measurement initialization and a constant expected change.

        Returns arrays of the predictions x̂_k^- and the estimates x̂_k, one entry per
        measurement (there is no prediction for k = 1, so that entry is NaN).
        """
        x_hat = measurements[0]  # x̂_1 = z_1
        predictions, estimates = [np.nan], [x_hat]
        for z in measurements[1:]:
            # Prediction step
            x_pred = x_hat + delta_x
            # Measurement update step
            x_hat = x_pred + alpha * (z - x_pred)
            predictions.append(x_pred)
            estimates.append(x_hat)
        return np.array(predictions), np.array(estimates)

    return (alpha_filter,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's run this filter on all 28 days of measurements. In this simulation, the true weight (black line) rises by exactly 0.2 lb per day, so $\Delta x = 0.2$ lb/day is the correct expected change. Use the sliders to change $\alpha$ and the expected change $\Delta x$, which is the same for every day.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    af_alpha = mo.ui.slider(
        start=0.05, stop=1.0, step=0.05, value=0.2, label=r"$\alpha$", show_value=True
    )
    af_dx = mo.ui.slider(
        start=-0.4, stop=1.0, step=0.05, value=0.2,
        label=r"$\Delta x$ (lb/day)", show_value=True,
    )
    return af_alpha, af_dx


@app.cell(hide_code=True)
def alpha_filter_fig_interactive(
    af_alpha,
    af_dx,
    alpha_filter,
    bulk_days,
    bulk_x,
    bulk_z,
    graphic,
    mo,
    np,
    plt,
):
    _pred, af_estimates = alpha_filter(bulk_z, af_alpha.value, af_dx.value)

    _fig, _ax = plt.subplots(figsize=(7, 4.2))
    _ax.plot(bulk_days, bulk_x, color="black", linewidth=1.2, label="True weight $x_k$")
    _ax.plot(
        bulk_days, bulk_z, "o",
        markerfacecolor="none", markeredgecolor="black", label="Measurement $z_k$",
    )
    _ax.plot(
        bulk_days, _pred, ":", color="red", marker="d", markersize=4,
        label=r"Prediction $\hat{x}_k^-$",
    )
    _ax.plot(bulk_days, af_estimates, color="C1", marker=".", label=r"Estimate $\hat{x}_k$")
    _lo = min(151.0, np.nanmin([_pred, af_estimates]) - 0.5)
    _hi = max(166.0, np.nanmax([_pred, af_estimates]) + 0.5)
    _ax.set(xlabel="Time (days)", ylabel="Weight (lb)", ylim=(_lo, _hi))
    _ax.legend(loc="upper left", fontsize="small")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.set_title(
        rf"Alpha Filter with $\alpha = {af_alpha.value:.2f}$, $\Delta x = {af_dx.value:.2f}$ lb/day",
        style="italic",
    )
    _fig.tight_layout()
    _out = graphic(_fig)
    plt.close(_fig)

    mo.vstack([mo.hstack([af_alpha, af_dx], justify="start", gap=2), _out])
    return (af_estimates,)


@app.cell(hide_code=True)
def _(af_alpha, af_dx, af_estimates, bulk_rate, bulk_x, mo, np):
    _offset = (1 - af_alpha.value) / af_alpha.value * (af_dx.value - bulk_rate)
    _last_week = np.mean(af_estimates[-7:] - bulk_x[-7:])
    mo.md(rf"""
    With $\alpha = {af_alpha.value:.2f}$ and $\Delta x = {af_dx.value:.2f}$ lb/day, the estimates over the last week are on average {_last_week:+.2f} lb away from the true weight. The noise-free calculation below predicts a steady offset of {_offset:+.2f} lb.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Unsurprisingly, this works quite well when our value of $\Delta x$ is correct. When $\Delta x$ is wrong, however, the estimates drift away from the true weight until they settle at a constant offset. Try $\Delta x = 1$ lb/day, the kind of rate a careless diet calculation might suggest, or $\Delta x = 0$, which turns the alpha filter back into the EMA.

    We can compute this offset. Suppose there is no noise, the true weight changes by the same amount $c$ every step, and our constant expected change $\Delta x$ is wrong by $d = \Delta x - c$. Write $e_k = \hat x_k - x_k$ for the error at step $k$. Since $z_k = x_k$,

    $$e_k = \hat x_k^- + \alpha(x_k - \hat x_k^-) - x_k = (1-\alpha)(\hat x_k^- - x_k) = (1-\alpha)(\hat x_{k-1} + \Delta x - x_{k-1} - c) = (1-\alpha)(e_{k-1} + d).$$

    The number $e^* = \frac{1-\alpha}{\alpha}\,d$ satisfies the same equation, $e^* = (1-\alpha)(e^* + d)$, as you can check by expanding the right-hand side. Subtracting the two equations gives $e_k - e^* = (1-\alpha)(e_{k-1} - e^*)$, so each step multiplies the distance from $e^*$ by $1-\alpha$, and

    $$e_k - e^* = (1-\alpha)^{k-1}(e_1 - e^*).$$

    Since $0 \le 1-\alpha < 1$, the right-hand side shrinks toward 0 as $k$ grows, so the error settles at

    $$e^* = \frac{1-\alpha}{\alpha}\,(\Delta x - c).$$

    (With noise, the errors fluctuate around this value.) Two consequences stand out. First, the offset is proportional to the error in $\Delta x$, so a wrong $\Delta x$ never washes out. Second, it grows as $\alpha$ shrinks, so the small $\alpha$ we want for averaging away noise makes the offset worse. For the EMA ($\Delta x = 0$), the offset is $-\frac{1-\alpha}{\alpha}c$: the EMA lags behind a steadily rising weight by $\frac{1-\alpha}{\alpha}$ steps' worth of change, which is the lag from the noise-versus-lag trade-off above.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Beta Weighting Term

    To fix this, we want some way to correct $\Delta x$ in addition to correcting our estimate. The innovations tell us how. If $\Delta x$ is too small, the measurements keep coming in above our predictions, so the innovations $\tilde y_k = z_k - \hat x_k^-$ are positive more often than not; if $\Delta x$ is too large, they are mostly negative. So, just as we correct the prediction of $x_k$ by $\alpha$ times the innovation, we can correct the expected change by a second weight $\beta$ times the innovation. Since the expected change is now estimated from the data, we give it a hat, $\widehat{\Delta x}_k$, and each step becomes:

    - **Prediction step:** $\hat x_k^- = \hat x_{k-1} + \widehat{\Delta x}_k$.
    - **Measurement update step:** with the innovation $\tilde y_k = z_k - \hat x_k^-$,

      $$\hat x_k = \hat x_k^- + \alpha\,\tilde y_k, \qquad \widehat{\Delta x}_{k+1} = \widehat{\Delta x}_k + \beta\,\tilde y_k.$$

    Here $\widehat{\Delta x}_{k+1}$ is our estimate of the change from step $k$ to step $k+1$, made after seeing $z_k$, and one step is one day ($\Delta t = 1$ day)[^beta-conventions]. This is the **alpha-beta filter**[^informal-alpha-beta]. We start it with first-measurement initialization, $\hat x_1 = z_1$, and an initial guess $\widehat{\Delta x}_2$ for the first day's change. With $\beta = 0$, it never changes $\widehat{\Delta x}$, and it is the alpha filter again.

    [^beta-conventions]: Other texts write the update of the change differently. Some track a rate per unit time, $\hat v_k = \widehat{\Delta x}_k/\Delta t$, and so scale $\beta$ by $1/\Delta t$: $\hat v_{k+1} = \hat v_k + \frac{\beta}{\Delta t}\,\tilde y_k$. Others update from the change in the estimate, $\widehat{\Delta x}_{k+1} = \widehat{\Delta x}_k + \beta'\big[(\hat x_k - \hat x_{k-1}) - \widehat{\Delta x}_k\big]$. Since $\hat x_k - \hat x_{k-1} = \widehat{\Delta x}_k + \alpha\tilde y_k$, the bracket equals $\alpha\tilde y_k$, so this is our form with $\beta = \alpha\beta'$.

    [^informal-alpha-beta]: [Chapter 13](ch13_kalman_filter_v2.md) defines the {term}`alpha-beta filter` formally and shows how to choose its weights α and β as those of a steady-state Kalman filter.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Why does this fix the offset? Repeat the noise-free calculation with a true change of $c$ per step. Write $e_k = \hat x_k - x_k$ for the error in the estimate and $d_k = \widehat{\Delta x}_{k+1} - c$ for the error in the expected change. The prediction misses by $\hat x_k^- - x_k = e_{k-1} + d_{k-1}$, so the innovation is $\tilde y_k = x_k - \hat x_k^- = -(e_{k-1} + d_{k-1})$, and the two update equations become

    $$e_k = (1-\alpha)(e_{k-1} + d_{k-1}), \qquad d_k = d_{k-1} - \beta\,(e_{k-1} + d_{k-1}).$$

    If the errors settle at constant values $e$ and $d$, the second equation gives $\beta(e + d) = 0$. So, if $\beta > 0$, then $e + d = 0$, and the first equation gives $e = (1-\alpha) \cdot 0 = 0$, and hence $d = 0$. Unlike the alpha filter, the only place the alpha-beta filter can settle is at *zero* error, whatever the initial guess $\widehat{\Delta x}_2$. Whether the errors actually get there depends on the weights: if they are too large, each correction overshoots by more than the last, and the errors grow without bound. For all weights with $0 < \alpha \le 1$ and $0 < \beta < 2$, which includes every setting of the sliders below except $\beta = 0$, the errors do shrink to zero[^ab-stability].

    [^ab-stability]: Together, the two error equations say that each step multiplies the pair $(e_{k-1}, d_{k-1})$ by a fixed matrix ([Appendix D: Matrices and Linear Maps](appendix_d_linear_algebra_v2.md)), and the errors shrink to zero from every starting point exactly when both roots of $\lambda^2 - (2 - \alpha - \beta)\lambda + (1 - \alpha) = 0$, the eigenvalues of that matrix ([Appendix D: Eigenvalues and Eigenvectors](appendix_d_linear_algebra_v2.md)), have magnitude less than 1. The [Jury stability criterion](https://en.wikipedia.org/wiki/Jury_stability_criterion) shows that this happens exactly when $0 < \alpha < 2$ and $0 < \beta < 4 - 2\alpha$. See also [Wikipedia: Alpha beta filter](https://en.wikipedia.org/wiki/Alpha_beta_filter).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The Alpha-Beta Filter in Code

    In code, the alpha-beta filter needs only a few more lines than the alpha filter:
    """)
    return


@app.cell
def _(np):
    # jb: echo=true
    def alpha_beta_filter(measurements, alpha, beta, delta_x_initial):
        """Alpha-beta filter with first-measurement initialization.

        Returns arrays of the predictions x̂_k^-, the estimates x̂_k, and the expected
        changes Δx̂_(k+1), one entry per measurement (there is no prediction for k = 1,
        so that entry is NaN).
        """
        x_hat = measurements[0]  # x̂_1 = z_1
        delta_x_hat = delta_x_initial  # Δx̂_2: initial guess for the change from step 1 to 2
        predictions, estimates, changes = [np.nan], [x_hat], [delta_x_hat]
        for z in measurements[1:]:
            # Prediction step
            x_pred = x_hat + delta_x_hat
            # Measurement update step
            innovation = z - x_pred
            x_hat = x_pred + alpha * innovation
            delta_x_hat = delta_x_hat + beta * innovation
            predictions.append(x_pred)
            estimates.append(x_hat)
            changes.append(delta_x_hat)
        return np.array(predictions), np.array(estimates), np.array(changes)

    return (alpha_beta_filter,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Try it on the same 28 days of data. The initial guess starts at $\widehat{\Delta x}_2 = 0$ ("I have no idea how fast I'm gaining"). Watch the lower panel, where $\beta$ pulls the expected change toward the true 0.2 lb/day. Then set $\beta = 0$ to get the alpha filter back, with its offset, or start from the careless guess of 1 lb/day.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    ab_alpha = mo.ui.slider(
        start=0.05, stop=1.0, step=0.05, value=0.3, label=r"$\alpha$", show_value=True
    )
    ab_beta = mo.ui.slider(
        start=0.0, stop=0.3, step=0.01, value=0.03, label=r"$\beta$", show_value=True
    )
    ab_dx0 = mo.ui.slider(
        start=-0.4, stop=1.0, step=0.05, value=0.0,
        label=r"Initial $\widehat{\Delta x}_2$ (lb/day)", show_value=True,
    )
    return ab_alpha, ab_beta, ab_dx0


@app.cell(hide_code=True)
def alpha_beta_fig_interactive(
    ab_alpha,
    ab_beta,
    ab_dx0,
    alpha_beta_filter,
    bulk_days,
    bulk_rate,
    bulk_x,
    bulk_z,
    graphic,
    mo,
    np,
    plt,
):
    _pred, ab_estimates, ab_changes = alpha_beta_filter(
        bulk_z, ab_alpha.value, ab_beta.value, ab_dx0.value
    )

    _fig, (_ax, _ax_rate) = plt.subplots(
        2, 1, figsize=(7, 6), sharex=True, gridspec_kw={"height_ratios": [2, 1]}
    )
    _ax.plot(bulk_days, bulk_x, color="black", linewidth=1.2, label="True weight $x_k$")
    _ax.plot(
        bulk_days, bulk_z, "o",
        markerfacecolor="none", markeredgecolor="black", label="Measurement $z_k$",
    )
    _ax.plot(
        bulk_days, _pred, ":", color="red", marker="d", markersize=4,
        label=r"Prediction $\hat{x}_k^-$",
    )
    _ax.plot(bulk_days, ab_estimates, color="C1", marker=".", label=r"Estimate $\hat{x}_k$")
    _lo = min(151.0, np.nanmin([_pred, ab_estimates]) - 0.5)
    _hi = max(166.0, np.nanmax([_pred, ab_estimates]) + 0.5)
    _ax.set(ylabel="Weight (lb)", ylim=(_lo, _hi))
    _ax.legend(loc="upper left", fontsize="small")
    _ax.grid(visible=True, alpha=0.9, linewidth=0.4)
    _ax.set_title(
        rf"Alpha-Beta Filter with $\alpha = {ab_alpha.value:.2f}$, $\beta = {ab_beta.value:.2f}$",
        style="italic",
    )

    _ax_rate.axhline(bulk_rate, color="black", linewidth=1.2, label="True change per day")
    _ax_rate.plot(
        bulk_days, ab_changes, color="C1", marker=".",
        label=r"Expected change $\widehat{\Delta x}_{k+1}$",
    )
    _ax_rate.set(
        xlabel="Time (days)",
        ylabel="Change (lb/day)",
        ylim=(min(-0.5, ab_changes.min() - 0.1), max(1.1, ab_changes.max() + 0.1)),
    )
    _ax_rate.legend(loc="upper right", fontsize="small")
    _ax_rate.grid(visible=True, alpha=0.9, linewidth=0.4)
    _fig.tight_layout()
    _out = graphic(_fig)
    plt.close(_fig)

    mo.vstack([mo.hstack([ab_alpha, ab_beta, ab_dx0], justify="start", gap=2), _out])
    return ab_changes, ab_estimates


@app.cell(hide_code=True)
def _(ab_changes, ab_estimates, bulk_rate, bulk_x, mo):
    mo.md(rf"""
    After 28 days, the alpha-beta filter estimates the change per day as {ab_changes[-1]:.3f} lb/day (true: {bulk_rate:.3f} lb/day) and your weight as {ab_estimates[-1]:.2f} lb (true: {bulk_x[-1]:.2f} lb).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// caution | ⚠️ **Assumptions and Failure Modes**
        attrs: {class: no-icon}
    - **Alpha filter: the expected change is right.** If $\Delta x$ is wrong by $d$ at every step, the estimates settle at an offset of $\frac{1-\alpha}{\alpha}\,d$, as computed above.
    - **Alpha-beta filter: the change per step is (nearly) constant.** The filter learns a single rate. If the rate itself changes, say because you switch diets halfway through, the estimates lag behind until $\widehat{\Delta x}$ catches up, and the smaller $\beta$ is, the longer that takes.
    - **Weights in the stable range.** If $\alpha$ or $\beta$ is too large, each correction overshoots, and the errors grow instead of shrinking.
    - **Measurement noise, as before:** zero mean and unrelated from one measurement to the next. Water weight that persists for several days violates the second assumption, and the filters will partly mistake it for a real change.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    Our goal when designing a signal filter is to estimate the true values $x_k$ from noisy measurements $z_k$. If the noise has mean zero and is unrelated from one measurement to the next, then combining measurements reduces the variance of the noise in our estimate. Every filter in this chapter does this recursively: it forms a {term}`prediction` $\hat x_k^-$ of $x_k$, compares it with the measurement to get the {term}`innovation` $\tilde y_k = z_k - \hat x_k^-$, and adds a weighted share of the innovation to the prediction:

    $$\hat{x}_k = \hat x_k^- + \alpha (z_k - \hat x_k^-).$$

    | Filter | Prediction $\hat x_k^-$ | Weights |
    |---|---|---|
    | Cumulative average | $\hat x_{k-1}$ | $\frac1k$ |
    | Exponential moving average | $\hat x_{k-1}$ | $\alpha$ |
    | Alpha filter | $\hat x_{k-1} + \Delta x_k$ | $\alpha$ |
    | Alpha-beta filter | $\hat x_{k-1} + \widehat{\Delta x}_k$ | $\alpha$ for the estimate, $\beta$ for the expected change: $\widehat{\Delta x}_{k+1} = \widehat{\Delta x}_k + \beta\,\tilde y_k$ |

    Smaller weights average away more noise but respond more slowly to real changes. The second weight $\beta$ corrects the expected change using the same innovations, which removes the steady offset that a wrong expected change causes in the alpha filter.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What's Next

    So far we have chosen $\alpha$ (and $\beta$) by feel. Because both the prediction $\hat x_k^-$ and the measurement $z_k$ are noisy values, a natural question becomes:

    > Given some amounts of noise in our prediction ($\hat x_k^-$) and measurement ($z_k$), what value of $\alpha$ should we pick?

    **Part 1: Choosing α** is dedicated to answering this question. Since modeling noise relies on probability, probability is built on set theory, and set theory is built on logic, we introduce these topics along the way: logic in [Chapter 1](ch1_language_of_logic_v2.md), sets in [Chapters 2](ch2_axioms_of_set_theory_v2.md) and [3](ch3_sets_for_probability_v2.md), and probability in [Chapters 4](ch4_probability_spaces_v2.md) through [6](ch6_expectation_and_variance_v2.md). [Chapter 7](ch7_optimal_alpha_v2.md) then answers the question, and proves along the way that the cumulative average's $\frac1k$ was optimal all along. [Chapter 8](ch8_bayesian_view_v2.md) reinterprets the answer using Bayes' theorem.

    Once we know the optimal $\alpha$ for given levels of noise in $\hat x_k^-$ and $z_k$, the remaining parts answer the following questions.

    **Part 2: The Scalar Kalman Filter** ([Chapters 9](ch9_noise_levels_v2.md) through [11](ch11_measurement_functions_v2.md))

    > How do we determine the levels of noise in $\hat x_k^-$ and $z_k$?

    (Spoiler: $z_k$ will be pretty simple, but $\hat x_k^-$ will take a bit more work. The answer is the Kalman filter, and [Chapter 9](ch9_noise_levels_v2.md) shows that in the long run it becomes an EMA, which finally tells us how to choose the EMA's $\alpha$.)

    > What is the best way to calculate $\hat x_k^-$?

    (There are endless ways to do this, and we will not cover them all. [Chapter 10](ch10_process_models_v2.md) shows how to build a model of how the true value changes, and how to judge whether it is a good one.)

    > What if my sensor doesn't measure the real-world value I want to know?

    (Time for measurement functions in [Chapter 11](ch11_measurement_functions_v2.md)!)

    **Part 3: State Vectors** ([Chapters 12](ch12_vectors_matrices_covariance_v2.md) through [14](ch14_kalman_filters_in_practice_v2.md))

    > What if my real-world value can't be represented as a scalar?

    (Time for state vectors! The alpha-beta filter already tracks two numbers, a weight and its change per day. [Chapter 13](ch13_kalman_filter_v2.md) shows that it is a special case of the multivariate Kalman filter, and [Chapter 14](ch14_kalman_filters_in_practice_v2.md) covers tuning, sensor fusion, and checking that a filter is working.)

    **Part 4: Nonlinearity** ([Chapters 15](ch15_extended_kalman_filter_v2.md) and [16](ch16_unscented_kalman_filter_v2.md))

    > What if I expect my real-world value to change in super weird, nonlinear ways?

    (Linear approximation techniques in the extended Kalman filter, then sigma points in the unscented Kalman filter.)

    **Part 5: Orientation** ([Chapters 17](ch17_rotations_v2.md) through [19](ch19_ahrs_v2.md))

    > What if I need to avoid singularities in my state representation?

    (Quaternion time! We represent orientation with rotation matrices and quaternions, then build an AHRS that fuses gyroscopes, accelerometers, and magnetometers.)

    **Part 6: Inertial Navigation for Gait** ([Chapters 20](ch20_strapdown_inertial_navigation_v2.md) and [21](ch21_zero_velocity_updates_v2.md))

    > Can a single IMU strapped to a shoe measure how someone walks?

    (We put everything together: we integrate the IMU's measurements to track the foot, and correct the resulting drift every time the foot is flat on the ground, to measure stride length, cadence, and gait speed.)

    **Optional appendices.** Four appendices build foundational material from the ground up: [Appendix A: Formal Logic](appendix_a_formal_logic_v2.md), [Appendix B: Constructing the Number Systems](appendix_b_number_systems_v2.md), [Appendix C: Calculus](appendix_c_calculus_v2.md), and [Appendix D: Linear Algebra](appendix_d_linear_algebra_v2.md). You don't need to read them front to back. Every chapter after this one opens with a Prerequisites box that lists exactly which appendix sections it relies on, so read a section when a chapter points to it and the material is new to you. In particular, if they are unfamiliar, read Appendix C's sections on sequences and series before Chapter 4, and Appendix D before Part 3.

    We begin with [Chapter 1: Language of Logic](ch1_language_of_logic_v2.md).
    """)
    return


if __name__ == "__main__":
    app.run()
