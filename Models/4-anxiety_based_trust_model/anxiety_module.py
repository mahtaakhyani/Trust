'''
This module models the anxiety accumulation and decay over time. 

It takes these variables as input to initiate an Anxiety class instance:
    1. Anxiety baseline (A_baseline) -> individual's baseline anxiety
    2. Negativity Bias (W_i) -> negative events are weighted 2-3x more heavily than positive events 
        where:
            - For errors/failures: w_err ≈ 2 to 3
            - For successes: w_succ ≈ 0.5 to 1
            - For neutral events: w_neut ≈ 0
    
It takes these variables to update the Anxiety class instance:
    1. Time of the signal (t)
    2. Signal impact aka "Surprise" (S_i) -> S_i = E_i * U_i * R_i 
        where:
            - E_i: Objective kinematic error magnitude (e.g., degrees of angular deviation, cm of position error)
                * Magnitude is captured through:
                    Crest factor = signal's peak amplitude/root mean square (RMS) value of the signal
            - U_i: Unexpectedness factor
                * Unexpectedness is measured through:
                    Kurtosis formula
            - R_i: Contextual criticality/risk factor
    3. Decay constant (Lambda) -> how fast the effect of the signal naturally decays in time for the user (loss is faster than gain)
    

The model is built upon the following phrases:
    * Anxiety decay expression: e^{-lambda*(t - t_i)} (Leacky integrator model)
    * The perceived strength of the stressor: w_i * S_i * R_i
    * The non-linearity expression of the cumulative physiological cost of the stressors: ∑_i=1^n

Full model:
        A(t) = A_baseline + ∑_i [(w_i * E_i * U_i * R_i) * e^{-lambda * (t - t_i)}]
        

This module also keeps a history of all the anxiety levels and stressors. 

'''
import numpy as np
from scipy.interpolate import PchipInterpolator
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from itertools import count
from adjustText import adjust_text

from motion_types import *
from surprise_handler import *



W_BASE = 1.0  # population-level negativity bias constant
ALPHA = 0.4   # sensitivity of negativity bias to baseline
BETA = 0.3    # sensitivity of decay rate to baseline
_id_counter = count(1)

class AnxietyModel:
    def __init__(self, A_baseline, negativity_weight=2):
        self.A_baseline = A_baseline
        self.negativity_weight = negativity_weight
        self.stressor_history = []
        self.anxiety_history = [self.Anxiety(level=self.A_baseline, time=0)]
        self.current_anxiety_level = self.A_baseline
        
        # Use a consistent time base and sampling rate for motion and surprise
        self.motion = MotionHandler()
        self.surprise = SurpriseFactorsHandler(sampling_frequency=self.motion.fs)
        
        
    @dataclass
    class Stressor:
        accel_data: list = field(default_factory = [])
        id: int = field(default_factory= lambda: next(_id_counter))
        motion_type: str = field(default_factory = '')
        time: float = field(default=0.0)
        duration: float = field(default=0.0)
        magnitude: float = field(default=1.0)
        unexpectedness: float = field(default=1.0)
        risk_factor: float = field(default=1.0)
        surprise: float = field(default=1.0)
        decay: float = field(default=0.3)
        
        
    @dataclass
    class Anxiety:
        level: float
        time: float
        stressor: object = None
    



    def add_stressor(self,
                    motion_type: str,
                    freq: float,
                    amplitude: float,
                    risk_factor: float,
                    duration: float,
                    decay: float = 0.02,
                    start_time: float | None = None,
                    lag: float | None = None,
                    burst_start_time: float | None = None,
                    burst_freq: float | None = None,
                    impulse_magnitude: float | None = None,
                    ):
        if not start_time:
            start_time = duration * 0.45
        if burst_start_time and start_time:
            start_time = burst_start_time
        # Use provided burst_start_time when available, otherwise align with start_time
        if burst_start_time is None and start_time:
            burst_start_time = start_time

        # Map high-level motion labels to underlying generator types
        motion_map = {
            # "mild vibration": "vibration",
            "strong vibration": "vibration",
            # "phase_lag": "lag",
            "sudden stop": "sudden_stop",
            # "event": "vibration",
        }
        generator_motion_type = motion_map.get(motion_type, motion_type)


        motion_delta = self.motion.motion.motion(
            t=self.motion.t,
            start_time=start_time,
            motion_type=generator_motion_type,
            freq=freq,
            amplitude=amplitude,
            lag=lag,
            burst_freq=burst_freq,
            burst_start_time=burst_start_time,
            duration=duration,
            impulse_magnitude=impulse_magnitude,
        )

        # Convert event time (seconds) to sample index on the shared timeline
        accel_data=self.motion.baseline_motion + motion_delta
        event_index = int(np.argmax(np.abs(accel_data)))
        crest, kurt, surprise, jerk = self.surprise.event_handler(
            event_time_index=event_index,
            accel_data=accel_data,
            duration=duration,
        )
        event_time = start_time
        stressor = self.Stressor(
            motion_type=motion_type,
            time=event_time,
            duration=duration,
            magnitude=jerk,
            unexpectedness=kurt,
            risk_factor=risk_factor,
            surprise=surprise,
            decay=decay,
            accel_data=accel_data
        )
        self.stressor_history.append(stressor)
        self._update_anxiety_over_interval(stressor)

        return stressor
        


    @staticmethod
    def _leaky_integrator_interval_contribution(
        *, time: float, start: float, end: float, decay: float, intensity: float
    ) -> float:
        """
        Contribution of a constant-intensity stressor active on [start, end].

        This matches a leaky integrator driven by constant input during the event:
        - For time in [start, end], anxiety ramps up toward a steady-state.
        - For time > end, contribution decays exponentially from the end level.
        """
        if intensity == 0.0 or time < start:
            return 0.0

        if decay <= 0:
            # No decay: contribution is proportional to elapsed active time.
            return intensity * (min(time, end) - start)

        if time <= end:
            return (intensity / decay) * (1.0 - np.exp(-decay * (time - start)))

        active_area = (intensity / decay) * (1.0 - np.exp(-decay * (end - start)))
        return active_area * np.exp(-decay * (time - end))

    def _stressor_contribution(self, time: float, stressor) -> float:
        if time < stressor.time:
            return 0.0
        intensity = float(self.negativity_weight) * float(stressor.surprise)
        # Impulse: full intensity at t_i, then decay from event end
        t_end = stressor.time + stressor.duration
        return intensity * np.exp(-stressor.decay * (time - t_end))

    def _update_anxiety(self, time: float, stressor) -> float:
        A = self.A_baseline + sum(
            self._stressor_contribution(time, s) for s in self.stressor_history
        )
        self.anxiety_history.append(self.Anxiety(level=A, time=time, stressor=stressor))
        self.current_anxiety_level = A
        return A

    def _update_anxiety_over_interval(self, stressor) -> None:
        """
        Log anxiety continuously while the stressor is active (plus endpoint).
        """
        start = float(stressor.time)
        end = start + float(stressor.duration)
        dt = 1.0 / float(self.motion.fs)
        times = np.arange(start, end + 0.5 * dt, dt)
        for t in times:
            self._update_anxiety(float(t), stressor)
        
    def get_anxiety_at(self, time: float) -> float:
        """Evaluate A(t) at any time without logging."""
        A = self.A_baseline + sum(
            self._stressor_contribution(time, s)
            * np.exp(-s.decay * (time - (s.time + float(s.duration))))
            for s in self.stressor_history
            if time >= s.time  # ← don't contribute before event starts
        )
        A = min(A, 80)
        
        return A
        
    def compute_tonic_envelope(self, time): # WRONGGGGGGGG FUNCTION/ACCUMULATION WATEVER
        if not self.anxiety_history:
            return np.full_like(time, fill_value=self.A_baseline, dtype=float)

        hist_times = np.array([a.time for a in self.anxiety_history], dtype=float)
        hist_levels = np.array([a.level for a in self.anxiety_history], dtype=float)

        anchor_times: list[float] = []
        anchor_values: list[float] = []

        for s in self.stressor_history:
            idx = int(np.searchsorted(hist_times, s.time))
            pre_idx = max(0, idx - 3)
            baseline_val = float(hist_levels[pre_idx]) if idx > 0 else float(self.A_baseline)

            end = min(len(hist_levels), idx + 30)
            if idx >= end:
                continue
            window = hist_levels[idx:end]
            if window.size == 0:
                continue

            peak_val = float(np.max(window))
            midpoint = 0.5 * (peak_val + baseline_val)
            anchor_times.append(float(s.time))
            anchor_values.append(midpoint)

        if len(anchor_times) < 2:
            return np.full_like(time, fill_value=self.A_baseline, dtype=float)

        # Add decay anchors AFTER last event, sampled from the actual anxiety curve
        last_t = anchor_times[-1]
        for dt_offset in [15, 40, 80, 150]:
            t_sample = last_t + dt_offset
            if t_sample < float(time[-1]):
                idx = int(np.searchsorted(hist_times, t_sample))
                if idx < len(hist_levels):
                    anchor_times.append(t_sample)
                    anchor_values.append(float(hist_levels[idx]))

        # Boundary anchors
        anchor_times = [float(time[0])] + anchor_times + [float(time[-1])]
        anchor_values = [float(self.A_baseline)] + anchor_values + [float(self.A_baseline)]

        interp = PchipInterpolator(anchor_times, anchor_values, extrapolate=False)
        tonic = interp(time)
        tonic = np.where(np.isnan(tonic), self.A_baseline, tonic)
        return tonic
    
class MotionHandler:
    def __init__(
        self,
        t=100.0,
        fs=100,
        motion_freq=2.0,
        motion_amplitude=1.0,
    ):
        """
        Create a shared motion time base.

        Parameters
        ----------
        t : float | array-like
            If scalar, interpreted as duration in seconds. If array-like,
            interpreted as an explicit time vector (in seconds).
        fs : int
            Sampling frequency in Hz for the internal time base.
        """
        self.fs = fs
        self.motion_freq = motion_freq
        self.motion_amplitude = motion_amplitude

        if np.isscalar(t):
            duration = float(t)
            n = int(round(duration * fs))
            self.t = np.arange(n) / fs  # seconds
        else:
            self.t = np.asarray(t)

        self.motion = CreateMotion()
        self.baseline_motion = self.motion.motion(
            t=self.t,
            start_time=0.0,
            motion_type="smooth",
            freq=motion_freq,
            amplitude=motion_amplitude,
        )
        
        
        
        
        

def test(A_baseline=20):
    model = AnxietyModel(A_baseline)
    
    # model.add_stressor(
    #     motion_type='mild vibration',
    #     freq=2.0,
    #     amplitude=2.0,
    #     lag=0.0,
    #     burst_start_time=20.0,
    #     burst_freq=50.0,
    #     impulse_magnitude=0.0,
    #     duration=0.10,
    #     risk_factor=1.0,
    #     decay=0.3
    # )
    model.add_stressor(
        motion_type='strong vibration',
        freq=2.0,
        amplitude=15.0,
        lag=0.0,
        burst_start_time=10.0,
        burst_freq=50.0,
        impulse_magnitude=0.0,
        duration=0.01,
        risk_factor=1.0,
        decay=0.9
    )

    # model.add_stressor(
    #     motion_type='phase_lag',
    #     start_time=300.0,
    #     freq=2.0,
    #     amplitude=1.0,
    #     lag=0.05,
    #     duration=0.2,
    #     risk_factor=2.0,
    # )
    model.add_stressor(
        motion_type='sudden stop',
        freq=2.0,
        amplitude=2.0,
        lag=0.0,
        burst_start_time=60.0,
        burst_freq=50.0,
        impulse_magnitude=10.0,
        duration=0.01,
        risk_factor=2.0,
        decay=0.1,
    )
    model.add_stressor(
        motion_type='sudden stop',
        freq=2.0,
        amplitude=2.0,
        lag=0.0,
        burst_start_time=70.0,
        burst_freq=50.0,
        impulse_magnitude=10.0,
        duration=0.01,
        risk_factor=4.0,
        decay=0.05,
    )
    model.add_stressor(
        motion_type='sudden stop',
        freq=2.0,
        amplitude=2.0,
        lag=0.0,
        burst_start_time=80.0,
        burst_freq=50.0,
        impulse_magnitude=10.0,
        duration=0.01,
        risk_factor=4.0,
        decay=0.03,
    )
    model.add_stressor(
        motion_type='sudden stop',
        freq=2.0,
        amplitude=2.0,
        lag=0.0,
        burst_start_time=90.0,
        burst_freq=50.0,
        impulse_magnitude=10.0,
        duration=0.01,
        risk_factor=4.0,
        decay=0.01,
    )

    time = np.linspace(0, 300, 300)
    anxiety_values = [model.get_anxiety_at(t) for t in time]
    # Compute tonic envelope over the full time vector
    tonic_values = model.compute_tonic_envelope(time)
    return model, time, anxiety_values, tonic_values


if __name__ == "__main__":
    # Single plot: anxiety (solid) and tonic envelope (dashed)
    fig, ax = plt.subplots(1, 1, figsize=(15, 8))

    model, time, anxiety_values, tonic_values = test()
    ax.plot(time, anxiety_values, label="Anxiety")
    ax.plot(time, tonic_values, linestyle="--", color="orange", label="Tonic envelope")

    texts = []
    for idx, s in enumerate(model.stressor_history):
        ax.axvline(x=s.time, color="red", linestyle="--", alpha=0.4, linewidth=0.8)

        jerk_value = float(s.magnitude)
        label = (
            f"type={s.motion_type}\n"
            f"t={s.time}\n"
            f"mag={s.magnitude}\n"
            f"risk={s.risk_factor}\n"
            f"unexpect={s.unexpectedness}\n"
            f"duration={s.duration}\n"
            f"surprise={s.surprise}\n"
            f"decay={s.decay}\n"
            f"jerk={jerk_value}"
        )

        y_frac = max(0.15, 0.95 - idx * 0.15)
        t = ax.text(
            s.time,
            y_frac,
            label,
            fontsize=6.5,
            verticalalignment="top",
            horizontalalignment="left",
            transform=ax.get_xaxis_transform(),
            color="red",
            alpha=0.8,
            bbox=dict(
                boxstyle="round,pad=0.2",
                facecolor="white",
                edgecolor="red",
                alpha=0.5,
            ),
        )
        texts.append(t)

    adjust_text(texts, arrowprops=dict(arrowstyle="->", color="red"))
    ax.set_ylabel("Anxiety (STAI-S)")
    ax.set_xlabel("Time (s)")
    ax.legend(loc="upper right")
    plt.tight_layout()
    plt.show()
