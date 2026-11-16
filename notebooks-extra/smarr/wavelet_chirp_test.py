import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from typing import Iterable
    from ssqueezepy import Wavelet, cwt, imshow
    import numpy as np
    import matplotlib.pyplot as plt
    from ssqueezepy.experimental import scale_to_freq
    from scipy.signal import chirp

    return Iterable, Wavelet, chirp, cwt, imshow, np, plt, scale_to_freq


@app.cell
def _(Iterable, Wavelet, cwt, imshow, np, scale_to_freq):
    def morse_cwt_by_period(
        x: Iterable[float],
        sample_freq: float, # Hz
        beta=5,
        gamma=3,
        wavelets_per_octave=32,
    ):
        duration = len(x) / sample_freq
        time_vector = np.linspace(0, duration, int(sample_freq * duration), endpoint=False)
        wavelet = Wavelet(('gmw', {'beta': beta, 'gamma': gamma}))

        Wx, scales = cwt(
            x,
            wavelet,
            scales='log',
            t=time_vector,
            nv=wavelets_per_octave
        )

        freqs = scale_to_freq(scales, wavelet, len(x), fs=sample_freq)
        periods = 1 / freqs

        # Flip to put longer periods at top
        print(Wx.shape)
        Wx_flipped = np.flipud(Wx)
        periods_flipped = periods[::-1]

        ikw = dict(abs=1, xticks=time_vector, xlabel="Time", ylabel="Period")
        imshow(Wx_flipped, **ikw, yticks=periods_flipped)

    return (morse_cwt_by_period,)


@app.cell
def _(chirp, np):
    def make_chirp(start_freq, end_freq, duration, fs=1):
        """
        Generates a linear chirp signal using scipy.signal.chirp.

        Args:
            start_freq (float): Starting frequency in Hz.
            end_freq (float): Ending frequency in Hz.
            duration (float): Duration of the signal in seconds.
            fs (int, optional): Sample rate in Hz. Defaults to 1.

        Returns:
            tuple: (t, signal)  
                t (np.ndarray): The time vector.  
                signal (np.ndarray): The generated chirp signal.
        """
        t = np.linspace(0, duration, int(fs * duration), endpoint=False)
        signal = chirp(t, f0=start_freq, t1=duration, f1=end_freq, method='linear')
    
        return t, signal

    return (make_chirp,)


@app.cell
def _(make_chirp, plt):
    duration = 10.0  # 10 seconds
    sample_freq = 100  # 100 Hz sampling rate
    start_freq = 0.1  # Start at 0.1 Hz (10 second period)
    end_freq = 2.0   # End at 2 Hz (0.5 second period)

    # Generate the chirp signal
    t, chirp_signal = make_chirp(start_freq, end_freq, duration, fs=sample_freq)

    # Plot the original signal
    plt.figure()
    plt.plot(t, chirp_signal)
    plt.title('Test Chirp Signal (0.1 Hz to 2 Hz)')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()
    # Apply wavelet transform
    # plt.figure(figsize=(12, 8))
    return chirp_signal, duration, sample_freq


@app.cell
def _(chirp_signal, duration, morse_cwt_by_period, plt, sample_freq):
    plt.figure()
    morse_cwt_by_period(chirp_signal, sample_freq, duration)
    return


if __name__ == "__main__":
    app.run()
