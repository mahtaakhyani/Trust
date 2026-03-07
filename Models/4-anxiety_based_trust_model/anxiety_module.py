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
    2. Signal impact aka "Surprise" (S_i) -> S_i = E_i * U_i * C_i 
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
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from itertools import count

from utils import *



W_BASE = 1.0  # population-level negativity bias constant
ALPHA = 0.4   # sensitivity of negativity bias to baseline
BETA = 0.3    # sensitivity of decay rate to baseline
_id_counter = count(1)

class AnxietyModel:
    def __init__(self, A_baseline, negativity_weight=2):
        self.A_baseline = A_baseline
        self.negativity_weight = negativity_weight
        self.stressor_history = []
        self.anxiety_history = []
        self.current_anxiety_level = self.A_baseline
        
        # Use a consistent time base and sampling rate for motion and surprise
        self.motion = MotionHandler()
        self.surprise = SurpriseFactorsHandler(sampling_frequency=self.motion.fs)
        
        
    @dataclass
    class Stressor:
        accel_data: list
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
        level: int
        time: float
        stressor: object
    



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
            "mild vibration": "vibration",
            "strong vibration": "vibration",
            "phase_lag": "lag",
            "sudden stop": "sudden_stop",
            "event": "vibration",
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
        event_index = int(start_time * self.surprise.sampling_frequency)
        crest, kurt, surprise = self.surprise.event_handler(
            event_time_index=event_index,
            accel_data=self.motion.baseline_motion + motion_delta,
        )
        accel_data=self.motion.baseline_motion + motion_delta
        event_time = start_time
        stressor = self.Stressor(
            motion_type=motion_type,
            time=event_time,
            duration=duration,
            magnitude=crest,
            unexpectedness=kurt,
            risk_factor=risk_factor,
            surprise=surprise,
            decay=decay,
            accel_data=accel_data
        )
        self.stressor_history.append(stressor)
        self._update_anxiety(event_time, stressor)

        return stressor
        


    def _update_anxiety(self, time: float, stressor) -> float:
            
            A = self.A_baseline + sum(
                self.negativity_weight * s.surprise * np.exp(-s.decay * (time - s.time))
                for s in self.stressor_history
                if s.time <= time
            )

            self.anxiety_history.append(
                self.Anxiety(level=A, time=time, stressor=stressor)
            )
            self.current_anxiety_level = A
            return A
        
    def get_anxiety_at(self, time: float) -> float:
        """Evaluate A(t) at any time without logging."""
        A = self.A_baseline + sum(
            self.negativity_weight * s.surprise * np.exp(-s.decay * (time - s.time))
            for s in self.stressor_history
            if s.time <= time
        )
        return A
        

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
    
    model.add_stressor(
        motion_type='mild vibration',
        freq=2.0,
        amplitude=2.0,
        lag=0.0,
        burst_start_time=20.0,
        burst_freq=50.0,
        impulse_magnitude=0.0,
        duration=0.10,
        risk_factor=1.0,
        decay=0.3
    )
    model.add_stressor(
        motion_type='strong vibration',
        freq=2.0,
        amplitude=15.0,
        lag=0.0,
        burst_start_time=100.0,
        burst_freq=50.0,
        impulse_magnitude=0.0,
        duration=0.50,
        risk_factor=1.0,
    )
    model.add_stressor(
        motion_type='phase_lag',
        start_time=300.0,
        freq=2.0,
        amplitude=1.0,
        lag=0.05,
        duration=0.2,
        risk_factor=2.0,
    )
    model.add_stressor(
        motion_type='sudden stop',
        start_time=600.0,
        freq=2.0,
        amplitude=2.0,
        lag=0.0,
        burst_start_time=60.0,
        burst_freq=50.0,
        impulse_magnitude=10.0,
        duration=0.01,
        risk_factor=4.0,
        decay=0.01,
    )

    time = np.linspace(0, 1000, 1000)
    anxiety_values = [model.get_anxiety_at(t) for t in time]

    return model, time, anxiety_values


fig, ax = plt.subplots(1, 1, figsize=(15, 8))

model, time, anxiety_values = test()
ax.plot(time, anxiety_values)
ax.set_xlabel('Time (s)')
from adjustText import adjust_text
# Get the model to access stressor objects with all properties
model, time, anxiety_values = test()
texts =[]
for idx, s in enumerate(model.stressor_history):

    ax.axvline(x=s.time, color='red', linestyle='--', alpha=0.4, linewidth=0.8)

    label = (
        f"type={s.motion_type}\n"
        f"t={s.time}\n"
        f"mag={s.magnitude}\n"
        f"risk={s.risk_factor}\n"
        f"unexpect={s.unexpectedness}\n"
        f"duration={s.duration}\n"
        f"surprise={s.surprise}\n"
        f"decay={s.decay}\n"
        f"jerk={CreateMotion().calculate_jerk(s.accel_data)[0]:4f}"
        
    )
    # Place labels at different vertical positions in axes coordinates
    # so that annotation boxes for multiple stressors do not overlap.
    y_frac = 0.95 - idx * 0.15
    if y_frac < 0.15:
        y_frac = 0.15

    t = ax.text(
        s.time,
        y_frac,
        label,
        fontsize=6.5,
        verticalalignment='top',
        horizontalalignment='left',
        transform=ax.get_xaxis_transform(),
        color='red',
        alpha=0.8,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='red', alpha=0.5)
    )
    texts.append(t)
adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red'))
ax.set_ylabel('Anxiety (STAI-S)')
plt.tight_layout()
plt.show()
