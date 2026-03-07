import numpy as np
from scipy.stats import kurtosis
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import logging


# Basic configuration to output INFO level messages or higher to the console
logging.basicConfig(level=logging.INFO)


# ----------------------------------- CALCULATE SURPRISE FACTOR S_i -----------------------------------------


class SurpriseFactorsHandler:

    def __init__(self, sampling_frequency=100):  # (e.g., 100Hz)
        '''
            Initiating the vars that are unique to each experiment setup, but not the same among all setups
        '''
        self.sampling_frequency = sampling_frequency
        self.accel_data = np.array([])
        self.event_segment = np.array([])
    
    def event_handler(self, event_time_index, accel_data):
        self.accel_data = accel_data # update accel history based on the latest recieved data
        self._calculate_event_segment(event_time_index)
        crest = self.calculate_crest()
        kurt = self.calculate_kurt(fisher=True, bias=False)
        surprise = crest * abs(kurt)
        
        return crest, kurt, surprise
        
        
    def _calculate_event_segment(self, event_time_index):
        half_window = int(0.1 * self.sampling_frequency)  # 100ms before and 100ms after
        start = max(0, event_time_index - half_window)
        end = min(len(self.accel_data), event_time_index + half_window)

        # 1. Crop the event
        event_segment = np.array(self.accel_data[start:end])

        # 2. Remove DC Offset
        self.event_segment = event_segment - np.mean(event_segment)
        
        
        
    def calculate_crest(self):
        '''
            Calculates Crest Factor as the event's Magnitude.
            
            This factor is used as the common language for comparison 
            between different types of events (lag, vibration, etc.)
        '''
            
        peak = np.max(np.abs(self.event_segment))
        rms = np.sqrt(np.mean(self.event_segment**2)) + 1e-9
        crest_factor = peak / rms
        
        return crest_factor

        
        

    def calculate_kurt(self, fisher, bias):
        '''
            Kurtosis is used to measure the unexpectedness of an event.
            
            Higher values indicate extreme outliers/shocks:
                Kurtosis for normal walking ≈ 3 (or 0 if using "excess kurtosis", aka., fisher=False)
                Kurtosis for abnormal signal ≈ 10, 20, 100, etc.
        '''
        return kurtosis(a=self.event_segment, fisher=fisher, bias=bias)




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
        lag=None,
        burst_freq=None,
        burst_start_time=None,
        duration=None,
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

    def _smooth_motion(self, *, t, freq, amplitude, **_):
        return amplitude * np.sin(2 * np.pi * freq * t)

    def _lag_motion(self, *, t, freq, amplitude, lag, **_):
        if lag is None:
            logging.warning(
                f"Lagged motion: No lag defined. Using default lag {self.LAG}"
            )
            lag = self.LAG

        return amplitude * np.sin(2 * np.pi * freq * (t - lag))

    def _vibration_motion(
        self, *, t, burst_start_time, burst_freq, duration, amplitude, **_
    ):
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
        self, *, t, start_time, duration, impulse_magnitude, **_
    ):
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


    def calculate_jerk(self, accel_data, dt=0.001, window_size=11, poly_order=3):
        """
        Calculates jerk from acceleration data.
        
        Parameters:
        accel_data (ndarray): Array of acceleration values (m/s^2).
        dt (float): Time interval between samples (e.g., 0.001 for 1000Hz).
        window_size (int): Number of samples for the smoothing window (must be odd, a window of 11 covers 11 milliseconds).
        poly_order (int): The order of the polynomial to fit (3 is standard for jerk).
        
        Returns:
        ndarray: The calculated jerk (m/s^3).
        """
        
        # 1. Finite Difference Method (Raw/Noisy)
        # jerk_raw = np.diff(accel_data) / dt
        
        # 2. Savitzky-Golay Method (Recommended for Research)
        # This applies a smoothing filter and takes the 1st derivative of acceleration (jerk)
        # deriv=1 means we take the first derivative of the input (acceleration)
        jerk_filtered = savgol_filter(accel_data, window_length=window_size,
                                    polyorder=poly_order, deriv=1, delta=dt)
        
        return jerk_filtered




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
        ax.plot(t, jerk, label=label, linewidth=1.0)

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
    rng = np.random.default_rng(seed)
    motion = CreateMotion()

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
        "Vibration_Burst": vib,
        "Sudden_Stop": stop,
        "Smooth": baseline,
    }

    dt = 1.0 / fs
    jerks = {
        label: motion.calculate_jerk(
            accel,
            dt=dt,
            window_size=window_size,
            poly_order=poly_order,
        )
        for label, accel in signals.items()
    }

    return t, signals, jerks


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

    Produces a 2-row plot:
    - Top: acceleration for all event examples
    - Bottom: jerk (smoothed derivative) for all event examples
    """
    t, signals, jerks = generate_event_example_signals(
        duration=duration,
        fs=fs,
        noise_std=noise_std,
        seed=seed,
        window_size=window_size,
        poly_order=poly_order,
    )

    fig, (ax_accel, ax_jerk) = plt.subplots(
        2,
        1,
        figsize=(12, 7),
        sharex=True,
        gridspec_kw={"height_ratios": [2, 1]},
    )

    for label, accel in signals.items():
        ax_accel.plot(t, accel, label=label, linewidth=1.0)
        jerk = jerks[label]
        ax_jerk.plot(t, jerk, label=label, linewidth=1.0)

    vib_start = duration * 0.45
    vib_end = vib_start + 0.10
    stop_start = duration * 0.50
    stop_end = stop_start + 0.01

    for ax in (ax_accel, ax_jerk):
        ax.axvspan(vib_start, vib_end, color="black", alpha=0.08, label="_vibration_window")
        ax.axvspan(stop_start, stop_end, color="red", alpha=0.08, label="_sudden_stop_window")
        ax.grid(True, alpha=0.25)

    ax_accel.set_title("Event examples on a global timeline")
    ax_accel.set_ylabel("Acceleration (a.u.)")
    ax_jerk.set_ylabel("Jerk (a.u.)")
    ax_jerk.set_xlabel("Time (s)")

    ax_accel.legend(loc="upper right", fontsize=8)

    plt.tight_layout()
    if show:
        plt.show()

    return fig, (ax_accel, ax_jerk), (t, signals, jerks)



plot_event_examples(duration=10.0, fs=1000, noise_std=0.05, seed=0)
