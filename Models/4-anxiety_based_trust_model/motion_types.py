import numpy as np
from scipy.stats import kurtosis
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import logging
from surprise_handler import *

# Basic configuration to output INFO level messages or higher to the console
logging.basicConfig(level=logging.INFO)


# ---------------------------------------- CREATING EVENTS --------------------------------------------------
# Different events are shaped by different jerk vlaues. 
# In the following functions a set of "events" as an array of accel data are defined accordingly 
# as modules to be imported into the timelines.
# -----------------------------------------------------------------------------------------------------------

class CreateMotion:
    LAG = 0.01
    BURST_FREQ = 50.0
    BURST_DURATION = 0.1
    STOP_DURATION = 0.01
    IMPULE_MAGNITUDE = 10.0
    
    def motion(
        self,
        t,
        start_time,
        motion_type="smooth",
        freq=2.0,
        amplitude=1.0,
        duration=0.02,
        lag=None,
        burst_freq=None,
        burst_start_time=None,
        impulse_magnitude=None,
    ):
        """
        Generate simple motion profiles on a shared time base.
        """
        handlers = {
            "smooth": self._smooth_motion,
            "lag": self._lag_motion,
            "vibration": self._vibration_motion,
            "sudden_stop": self._sudden_stop_motion,
        }
        
        try:
            return handlers[motion_type](
                t=t,
                start_time=start_time,
                motion_type=motion_type,
                freq=freq,
                amplitude=amplitude,
                lag=lag,
                burst_freq=burst_freq,
                burst_start_time=burst_start_time,
                duration=duration,
                impulse_magnitude=impulse_magnitude,
            )
        except KeyError:
            raise ValueError(f"Unknown motion_type: {motion_type!r}") from None

    def _smooth_motion(self, *, t, freq=2, amplitude=1, **_):
        return amplitude * np.sin(2 * np.pi * freq * t)

    def _lag_motion(self, *, t, freq, amplitude, lag, **_):
        if lag is None:
            logging.warning(
                f"Lagged motion: No lag defined. Using default lag {self.LAG}"
            )
            lag = self.LAG
        
        return amplitude * np.sin(2 * np.pi * freq * (t - lag))

    def _vibration_motion(
        self, *, t, burst_start_time, burst_freq, duration, amplitude, **_):
        if burst_freq is None:
            logging.warning(
                f"Vibration motion: No burst_freq defined. Using default burst_freq {self.BURST_FREQ}"
            )
            burst_freq = self.BURST_FREQ

        if duration is None:
            logging.warning(
                f"Vibration motion: No duration defined. Using default duration {self.BURST_DURATION}"
            )
            duration = self.BURST_DURATION

        delta = np.zeros_like(t)
        mask = (t >= burst_start_time) & (t <= burst_start_time + duration)
        local_t = t[mask] - burst_start_time
        delta[mask] = amplitude * np.sin(2 * np.pi * burst_freq * local_t)
        return delta

    def _sudden_stop_motion(
        self, *, t, start_time, duration, impulse_magnitude, **_):
        if duration is None:
            logging.warning(
                f"Stop motion: No duration defined. Using default duration {self.STOP_DURATION}"
            )
            duration = self.STOP_DURATION

        if impulse_magnitude is None:
            logging.warning(
                f"Stop motion: No impulse_magnitude defined. Using default impulse_magnitude {self.IMPULE_MAGNITUDE}"
            )
            impulse_magnitude = self.IMPULE_MAGNITUDE

        delta = np.zeros_like(t)
        mask = (t >= start_time) & (t <= start_time + duration)
        delta[mask] = impulse_magnitude
        return delta
            
        

    def add_gaussian_noise(self, signal, std=0.05, rng=None):
        """
        Add zero-mean Gaussian noise to a signal.

        Parameters
        ----------
        signal : ndarray
            Input signal.
        std : float
            Standard deviation of the noise.
        rng : np.random.Generator | None
            Optional NumPy random generator for reproducibility.
        """
        if rng is None:
            rng = np.random.default_rng()
        return signal + rng.normal(0.0, std, size=signal.shape)



def plot_sample_stressors(data, fs=1000, ax=None, show=True):
    """
    Plot all sample stressor acceleration traces against time.

    Parameters
    ----------
    data : dict[str, np.ndarray]
        Output from `sample_stressors()`, mapping condition name -> acceleration array.
    fs : int, optional
        Sampling frequency in Hz (default 1000, matching `sample_stressors`).
    ax : matplotlib.axes.Axes, optional
        Existing axis to draw on. If None, a new figure and axis are created.
    show : bool, optional
        Whether to call `plt.show()` at the end (default True).
    """
    if not data:
        raise ValueError("`data` is empty. Pass the dict returned by `sample_stressors()`.")

    # Assume all traces have the same length
    n_samples = len(next(iter(data.values())))
    t = np.arange(n_samples) / fs

    created_fig = False
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
        created_fig = True

    for label, accel in data.items():
        ax.plot(t, accel, label=label, linewidth=1.0)

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Acceleration (a.u.)")
    ax.set_title("Sample Stressor Accelerations Over Time")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", fontsize=8)

    # Highlight key event windows used when generating the signals
    ax.axvspan(0.45, 0.55, color="orange", alpha=0.1, label="_vibration_window")
    ax.axvspan(0.50, 0.51, color="red", alpha=0.1, label="_sudden_stop_window")

    if show and created_fig:
        plt.tight_layout()
        plt.show()

    return ax


def plot_sample_stressor_jerks(
    data,
    fs=1000,
    ax=None,
    show=True,
    window_size=11,
    poly_order=3):
    """
    Plot jerk (first derivative of acceleration) for each sample stressor.

    Parameters
    ----------
    data : dict[str, np.ndarray]
        Dict mapping condition name -> acceleration array (e.g., from `generate_all_events()`).
    fs : int, optional
        Sampling frequency in Hz (default 1000).
    ax : matplotlib.axes.Axes, optional
        Existing axis to draw on. If None, a new figure and axis are created.
    show : bool, optional
        Whether to call `plt.show()` at the end (default True).
    window_size : int, optional
        Window size for the Savitzky-Golay filter used in `calculate_jerk`.
    poly_order : int, optional
        Polynomial order for the Savitzky-Golay filter in `calculate_jerk`.
    """
    if not data:
        raise ValueError("`data` is empty. Pass the dict returned by the event generator.")

    n_samples = len(next(iter(data.values())))
    t = np.arange(n_samples) / fs
    dt = 1.0 / fs
    motion = CreateMotion()

    created_fig = False
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
        created_fig = True

    for label, accel in data.items():
        jerk = motion.calculate_jerk(
            accel,
            dt=dt,
            window_size=window_size,
            poly_order=poly_order,
        )
        t_jerk = t[: len(jerk)]
        ax.plot(t_jerk, jerk, label=label, linewidth=1.0)

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Jerk (a.u.)")
    ax.set_title("Sample Stressor Jerks Over Time (Smoothed)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", fontsize=8)

    # Highlight the same key event windows as in the acceleration plot
    ax.axvspan(0.45, 0.55, color="orange", alpha=0.1, label="_vibration_window")
    ax.axvspan(0.50, 0.51, color="red", alpha=0.1, label="_sudden_stop_window")

    if show and created_fig:
        plt.tight_layout()
        plt.show()

    return ax


def generate_event_example_signals(
    duration=10.0,
    fs=1000,
    noise_std=0.05,
    seed=0,
    motion_freq=2.0,
    motion_amplitude=1.0,
    window_size=11,
    poly_order=3,):
    """
    Generate example signals on a single global timeline.

    This is meant for quick demos and plotting. It instantiates:
    - Smooth baseline motion
    - 3 phase-lag variants (low/mid/high)
    - Baseline + vibration burst delta
    - Baseline + sudden stop delta

    Returns
    -------
    t : ndarray
        Global time vector (seconds).
    signals : dict[str, ndarray]
        Mapping label -> acceleration trace.
    jerks : dict[str, ndarray]
        Mapping label -> jerk trace computed from each acceleration trace.
    """
    if duration <= 0:
        raise ValueError("`duration` must be > 0.")
    if fs <= 0:
        raise ValueError("`fs` must be > 0.")

    n = int(round(duration * fs))
    t = np.arange(n) / fs
    print(t)
    rng = np.random.default_rng(seed)
    motion = CreateMotion()
    surprise_handler = SurpriseFactorsHandler(sampling_frequency=fs)

    baseline = motion.motion(
        t=t,
        start_time=0.0,
        motion_type="smooth",
        freq=motion_freq,
        amplitude=motion_amplitude,
    )

    lag_low = motion.motion(
        t=t,
        start_time=0.0,
        motion_type="lag",
        freq=motion_freq,
        amplitude=motion_amplitude,
        lag=0.010,
    )
    lag_mid = motion.motion(
        t=t,
        start_time=0.0,
        motion_type="lag",
        freq=motion_freq,
        amplitude=motion_amplitude,
        lag=0.050,
    )
    lag_high = motion.motion(
        t=t,
        start_time=0.0,
        motion_type="lag",
        freq=motion_freq,
        amplitude=motion_amplitude,
        lag=0.150,
    )

    vib_delta = motion.motion(
        t=t,
        start_time=duration * 0.45,
        motion_type="vibration",
        burst_start_time=duration * 0.45,
        burst_freq=50.0,
        duration=0.10,
        amplitude=0.5,
    )
    vib = baseline + vib_delta

    stop_delta = motion.motion(
        t=t,
        start_time=duration * 0.50,
        motion_type="sudden_stop",
        duration=0.01,
        impulse_magnitude=10.0,
    )
    stop = baseline + stop_delta

    # signals = {
    #     "Smooth": add_gaussian_noise(baseline, std=noise_std, rng=rng),
    #     "Lag_Low": add_gaussian_noise(lag_low, std=noise_std, rng=rng),
    #     "Lag_Mid": add_gaussian_noise(lag_mid, std=noise_std, rng=rng),
    #     "Lag_High": add_gaussian_noise(lag_high, std=noise_std, rng=rng),
    #     "Vibration_Burst": add_gaussian_noise(vib, std=noise_std, rng=rng),
    #     "Sudden_Stop": add_gaussian_noise(stop, std=noise_std, rng=rng),
    # }
    signals = {
        "Lag_Low": lag_low,
        "Lag_Mid": lag_mid,
        "Lag_High": lag_high,
        "vibration_Burst": vib,
        "sudden_stop": stop,
        "Smooth": baseline,
    }



    crests: dict[str, float] = {}
    kurts: dict[str, float] = {}
    surprises: dict[str, float] = {}
    jerks: dict[str, float] = {}

    for label, accel in signals.items():
        # Use the point of maximum absolute acceleration as the event index
        event_index = int(np.argmax(np.abs(accel)))
        crest, kurt, surprise_value, jerk = surprise_handler.event_handler(
            event_time_index=event_index,
            accel_data=accel,
            duration=accel.duration
        )
        crests[label] = crest
        kurts[label] = kurt
        surprises[label] = surprise_value
        jerks[label] = jerk

    return t, signals, jerks, crests, kurts, surprises


def plot_event_examples(
    duration=10.0,
    fs=1000,
    noise_std=0.05,
    seed=0,
    window_size=11,
    poly_order=3,
    show=True,):
    """
    Generate and plot example event signals (acceleration + jerk).

    Produces two figures (separate windows):
    - Figure 1: acceleration for all event examples
    - Figure 2: jerk (smoothed derivative) per condition, one subplot each
    """
    t, signals, jerks, crests, kurts, surprises = generate_event_example_signals(
        duration=duration,
        fs=fs,
        noise_std=noise_std,
        seed=seed,
        window_size=window_size,
        poly_order=poly_order,
    )

    vib_start = duration * 0.45
    vib_end = vib_start + 0.10
    stop_start = duration * 0.50
    stop_end = stop_start + 0.01

    # Figure 1: acceleration
    fig_accel, ax_accel = plt.subplots(figsize=(12, 4))
    for label, accel in signals.items():
        ax_accel.plot(t, accel, label=label, linewidth=1.0)
    ax_accel.set_title("Event examples on a global timeline")
    ax_accel.set_ylabel("Acceleration (a.u.)")
    ax_accel.axvspan(vib_start, vib_end, color="black", alpha=0.08, label="_vibration_window")
    ax_accel.axvspan(stop_start, stop_end, color="red", alpha=0.08, label="_sudden_stop_window")
    ax_accel.grid(True, alpha=0.25)
    ax_accel.legend(loc="upper right", fontsize=8)

    # Figure 2: jerk subplots (separate window)
    n_conditions = len(signals)
    fig_jerk, ax_jerks = plt.subplots(
        n_conditions,
        1,
        figsize=(12, 2 * n_conditions),
        sharex=True,
        squeeze=True,
    )
    ax_jerks = np.atleast_1d(ax_jerks)
    for ax_jerk, (label, jerk) in zip(ax_jerks, jerks.items(), strict=True):
        t_jerk = t[: len(jerk)]
        ax_jerk.plot(t_jerk, jerk, linewidth=1.0)
        ax_jerk.set_ylabel(f"{label}\nJerk (a.u.)", fontsize=9)
        ax_jerk.axvspan(vib_start, vib_end, color="black", alpha=0.08)
        ax_jerk.axvspan(stop_start, stop_end, color="red", alpha=0.08)
        ax_jerk.grid(True, alpha=0.25)
    ax_jerks[-1].set_xlabel("Time (s)")

    plt.figure(fig_accel.number)
    plt.tight_layout()
    plt.figure(fig_jerk.number)
    plt.tight_layout()
    if show:
        plt.show()

    return (fig_accel, fig_jerk), (ax_accel, ax_jerks), (t, signals, jerks, crests, kurts, surprises)

# t, signals, jerks, crests, kurts, surprises = generate_event_example_signals()

# plt.figure()
# plt.bar(crests.keys(), crests.values())
# plt.title("Crest factor per condition")

# plt.figure()
# plt.bar(kurts.keys(), kurts.values())
# plt.title("Kurtosis per condition")

# plt.figure()
# plt.bar(surprises.keys(), surprises.values())
# plt.title("Surprise per condition")
# plt.show()

# plot_event_examples(duration=10.0, fs=1000, noise_std=0.05, seed=0)
