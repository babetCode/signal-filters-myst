import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import pandas as pd
    from pathlib import Path

    # Get the directory where the current script is located
    data_dir = Path(__file__).parent.parent.parent / "assets/smarr"

    df_dict = {
        'fLA': pd.read_csv(data_dir / 'micedata-FemAct.csv'),
        'fCBT': pd.read_csv(data_dir / 'micedata-FemTemp.csv'),
        'mLA': pd.read_csv(data_dir / 'micedata-MaleAct.csv'),
        'mCBT': pd.read_csv(data_dir / 'micedata-MaleTemp.csv')
    }
    df_dict
    return df_dict, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Raw Data

    First I'll plot the temperatuere data.
    """)
    return


@app.cell
def _(df_dict):
    import numpy as np
    import matplotlib.pyplot as plt

    def plot_raw_temp(data, columns, title, color='blue'):
        fig, ax = plt.subplots(figsize=(12, 6))
    
        for col in columns:
            ax.plot(data['time (min)'], data[col], label=col, alpha=0.5)
    
        ax.set_xlabel('Time (min)')
        ax.set_ylabel('Temperature (°C)')
        ax.set_title(title)
        ax.legend(bbox_to_anchor=(1.0, 1), loc='upper left')
        ax.grid(True, alpha=0.3)

        xticks = np.arange(0, max(data['time (min)']) + 1, 1440)
        ax.set_xticks(xticks)
    
        plt.tight_layout()
        plt.show()

    # Plot female temperatures
    fem_data_columns = [f'fem{n}' for n in range(1, 15)]
    plot_raw_temp(df_dict['fCBT'], fem_data_columns, 'Female Temperature Data - All Traces')

    # Plot male temperatures
    male_data_columns = [f'male{n}' for n in range(1, 7)]
    plot_raw_temp(df_dict['mCBT'], male_data_columns, 'Male Temperature Data - All Traces')
    return fem_data_columns, male_data_columns, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The [first linked paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC5301430/#:~:text=For%20CBT%2C%20values,were%20not%20inflated.) explains that:
    > *For CBT, values below 35 °C were set to 35 °C to remove the result of a few rare device malfunctions and all values more than three standard deviations from the mean were set to three standard deviations from the mean. For LA, the correction to three standard deviations was only applied in the positive direction so that erroneously high values were corrected while activity counts of “0” were not inflated.*

    <!-- Similarly, the [second linked paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC9308033/#:~:text=For%20CBT%2C%20outlier,were%20not%20inflated.) explains that:
    > *For CBT, outlier values below 35 were set to 35, and all points greater than 3 standard deviations (SD) of the mean were set to three SD from the mean (plus or minus, as appropriate). For activity, the correction was only applied in the positive direction so that activity counts of “0” were not inflated.* -->

    Based on the cuttofs in the male data, it appears these corrections have already been applied. This can be quicky verified as well:
    """)
    return


@app.cell
def _(df_dict):
    # Check Female Temperature data
    fem_temp_data = df_dict['fCBT'].drop(columns=['time (min)'])
    fem_low_values = (fem_temp_data < 35).any().any()
    print(f'fCBT has values < 35: {fem_low_values}')

    # Check Male Temperature data  
    male_temp_data = df_dict['mCBT'].drop(columns=['time (min)'])
    male_low_values = (male_temp_data < 35).any().any()
    print(f'mCBT has values < 35: {male_low_values}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, look at the activity data.
    """)
    return


@app.cell
def _(df_dict, fem_data_columns, male_data_columns, np, plt):
    # Plot female activity traces in a grid
    fig, axes = plt.subplots(5, 3, figsize=(15, 18), sharey=True)
    axes = axes.flatten()
    # fem_data_columns = [f'fem{n}' for n in range(1, 15)]
    time_data = df_dict['fLA']['time (min)']

    for i, col in enumerate(fem_data_columns):
        axes[i].plot(time_data, df_dict['fLA'][col], linewidth=0.8)
        axes[i].set_title(f'{col}', fontsize=10)
        axes[i].grid(True, alpha=0.3)
    
        # Set x-axis ticks every 1440 minutes (24 hours)
        axes[i].set_xticks(np.arange(0, max(time_data) + 1, 1440))
        axes[i].set_xlabel('Time (min)', fontsize=9)
    
        if i % 3 == 0:  # Left column
            axes[i].set_ylabel('Activity\n(events/min)', fontsize=9)

    # Hide the last empty subplot (index 14)
    axes[14].set_visible(False)

    plt.suptitle('Female Locomotor Activity - Individual Traces', fontsize=14, y=0.995)
    plt.tight_layout()
    plt.show()

    # Plot male activity traces in a grid
    fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharey=True)
    axes = axes.flatten()

    # male_data_columns = [f'male{n}' for n in range(1, 7)]
    time_data = df_dict['mLA']['time (min)']

    for i, col in enumerate(male_data_columns):
        axes[i].plot(time_data, df_dict['mLA'][col], linewidth=0.8)
        axes[i].set_title(f'{col}', fontsize=10)
        axes[i].grid(True, alpha=0.3)
    
        # Set x-axis ticks every 1440 minutes (24 hours)
        axes[i].set_xticks(np.arange(0, max(time_data) + 1, 1440))
        axes[i].set_xlabel('Time (min)', fontsize=9)
    
        if i % 3 == 0:  # Left column
            axes[i].set_ylabel('Activity\n(events/min)', fontsize=9)

    plt.suptitle('Male Locomotor Activity - Individual Traces', fontsize=14, y=0.98)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The [paper also explains that](https://pmc.ncbi.nlm.nih.gov/articles/PMC5301430/#:~:text=For%20LA%2C%20the%20correction%20to%20three%20standard%20deviations%20was%20only%20applied%20in%20the%20positive%20direction%20so%20that%20erroneously%20high%20values%20were%20corrected%20while%20activity%20counts%20of%20%E2%80%9C0%E2%80%9D%20were%20not%20inflated.):

    > *For LA, the correction to three standard deviations was only applied in the positive direction so that erroneously high values were corrected while activity counts of “0” were not inflated.*

    The peaks on many of these plot look chopped off. While the original mean and standard deviation can't be calculated from chopped data, I'll assume this was already corrected as well.

    Next, [the paper says](https://pmc.ncbi.nlm.nih.gov/articles/PMC5301430/#:~:text=Daily%20range%20for,modality%E2%80%99s%20daily%20range.):

    > *Daily range for each modality was defined as (max-min) per mouse per day. Median 4-day windows (i.e., cycles in females) were generated for each animal by taking the average of the three repeated cycles, followed by taking the average of these 4-day windows across individuals of the same sex. Inter-animal variability was defined as the population range for each modality's daily range.*

    From the plots above, the data begins right as CBT and LA increase, so it's reasonable to assume the data has also been aligned to the beginning of a day.

    Since the data is already cleaned, I can move to creating the four day averages described.

    ### Four Day Averages
    """)
    return


@app.cell
def _(df_dict, np, pd, plt):
    min_4_days = 5760

    def process_df(df):
        remove_time_col = list(df.columns)[1:]
        data_df = df[remove_time_col].copy()

        top_half = data_df.iloc[:min_4_days].values
        bottom_half = data_df.iloc[min_4_days:].values

        averaged_halves = (top_half + bottom_half) / 2

        final_result_array = averaged_halves.mean(axis=1)

        return final_result_array

    processed_dict = {'time (min)': np.arange(1, 5761)}

    for name, df in df_dict.items():
        four_day_average = process_df(df)
        processed_dict[name] = four_day_average

    processed_df = pd.DataFrame(processed_dict)

    time = processed_df['time (min)']

    # Temperature plot
    plt.figure(figsize=(12, 5))
    plt.plot(time, processed_df['fCBT'], label='Female CBT', color='C0', linewidth=1.5, alpha=0.8)
    plt.plot(time, processed_df['mCBT'], label='Male CBT', color='C1', linewidth=1.5, alpha=0.8)
    plt.ylabel('Temperature (°C)')
    plt.title('Four-day averages: Temperature')
    plt.legend()
    plt.grid(True, which='both', axis='x', linestyle=':', linewidth=0.5)
    plt.xticks(np.arange(0, max(time) + 1, 1440))
    plt.tight_layout()
    plt.show()

    # Activity plot
    plt.figure(figsize=(12, 5))
    plt.plot(time, processed_df['fLA'], label='Female LA', color='C2', linewidth=1)
    plt.plot(time, processed_df['mLA'], label='Male LA', color='C3', linewidth=1, alpha=0.8)
    plt.xlabel('Time (min)')
    plt.ylabel('Activity (events per minute)')
    plt.title('Four-day averages: Activity')
    plt.legend()
    plt.grid(True, which='both', axis='x', linestyle=':', linewidth=0.5)
    plt.xticks(np.arange(0, max(time) + 1, 1440))
    plt.tight_layout()
    plt.show()
    return (processed_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For wavelet transforms, I'll use ssqueezepy.

    ### Wavelet Analysis
    """)
    return


@app.cell
def _(np, plt, processed_df):
    from ssqueezepy import Wavelet, cwt, imshow
    from ssqueezepy.experimental import scale_to_freq
    from matplotlib.colors import LinearSegmentedColormap

    def morse_cwt(
        x,
        beta=5,
        gamma=3,
        scale_type='log',
        sample_rate=60,
        wavelets_per_octave=32
    ):
        x = np.asarray(x)
        num_samples = len(x)

        wavelet = Wavelet(('gmw', {'beta': beta, 'gamma': gamma}))

        Wx, scales = cwt(
            x,
            wavelet,
            scales=scale_type,
            fs=sample_rate,
            nv=wavelets_per_octave
        )

        freqs = scale_to_freq(scales, wavelet, num_samples, fs=sample_rate)

        t = np.linspace(0., num_samples/sample_rate, num_samples)

        return Wx, freqs, t

    def plot_scalogram(W, freqs, t, title):
        periods = 1 / freqs # Convert frequency to period
        W_flipped = np.flipud(W)
        periods_flipped = periods[::-1]

        # Make scalogram
        fig, ax = plt.subplots(figsize=(10, 6))
        imshow_kwargs = dict(
            abs=1, xticks=t, xlabel="Time", ylabel="Period", 
            title=title
        )

        colors = ['cyan', 'blue', 'red', 'white']
        positions = [0, 0.1, 0.5, 1.0]
        n_bins = 256
        custom_cmap = LinearSegmentedColormap.from_list(
            'cyan_blue_red_white', 
            list(zip(positions, colors)), 
            N=n_bins
        )

        imshow(W_flipped, **imshow_kwargs, yticks=periods_flipped, ax=ax, show=0, cmap=custom_cmap)

        im = ax.get_images()[0]
        cbar = plt.colorbar(im, ax=ax, orientation='horizontal', pad=0.1, shrink=0.8)
        cbar.set_label('Magnitude')

        plt.tight_layout()
        plt.show()

    for _col in ['fLA', 'fCBT', 'mLA', 'mCBT']:
        W, freqs, t = morse_cwt(processed_df[_col].to_numpy())
        plot_scalogram(W, freqs, t, _col)
    return


if __name__ == "__main__":
    app.run()
