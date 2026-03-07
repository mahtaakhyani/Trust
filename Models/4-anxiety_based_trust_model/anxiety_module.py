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
                    start_time: float,
                    freq: float,
                    amplitude: float,
                    lag: float,
                    burst_start_time: float,
                    burst_freq: float,
                    impulse_magnitude: float,
                    duration: float,
                    risk_factor: float):
        
        if not start_time:
            start_time = duration * 0.45

        # Map high-level motion labels to underlying generator types
        motion_map = {
            "mild vibration": "vibration",
            "strong vibration": "vibration",
            "phase_lag": "lag",
            "sudden stop": "sudden_stop",
            "event": "vibration",
        }
        generator_motion_type = motion_map.get(motion_type, motion_type)

        # Use provided burst_start_time when available, otherwise align with start_time
        if burst_start_time is None:
            burst_start_time = start_time

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

        event_time = start_time
        stressor = self.Stressor(
            motion_type=motion_type,
            time=event_time,
            duration=duration,
            magnitude=crest,
            unexpectedness=kurt,
            risk_factor=risk_factor,
            surprise=surprise,
            decay=0.02,
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
        
        
        
        
        

def test(A_baseline=0.1):
    model = AnxietyModel(A_baseline)
    
    model.add_stressor(
        motion_type='mild vibration',
        start_time=20.0,
        freq=2.0,
        amplitude=2.0,
        lag=0.0,
        burst_start_time=20.0,
        burst_freq=50.0,
        impulse_magnitude=0.0,
        duration=0.10,
        risk_factor=1.0,
    )
    model.add_stressor(
        motion_type='strong vibration',
        start_time=20.0,
        freq=2.0,
        amplitude=5.0,
        lag=0.0,
        burst_start_time=20.0,
        burst_freq=50.0,
        impulse_magnitude=0.0,
        duration=0.10,
        risk_factor=1.0,
    )
    model.add_stressor(
        motion_type='phase_lag',
        start_time=40.0,
        freq=2.0,
        amplitude=3.0,
        lag=0.05,
        burst_start_time=40.0,
        burst_freq=50.0,
        impulse_magnitude=0.0,
        duration=0.10,
        risk_factor=1.0,
    )
    model.add_stressor(
        motion_type='sudden stop',
        start_time=60.0,
        freq=2.0,
        amplitude=2.0,
        lag=0.0,
        burst_start_time=60.0,
        burst_freq=50.0,
        impulse_magnitude=10.0,
        duration=0.01,
        risk_factor=3.0,
    )

    time = np.linspace(0, 100, 100)
    anxiety_values = [model.get_anxiety_at(t) for t in time]

    return time, anxiety_values


fig, axes = plt.subplots(1, 3, figsize=(15, 4))

baselines = [20, 30, 40]
colors = ['steelblue', 'darkorange', 'seagreen']
stressor_events = [
    dict(time=20, magnitude=5, risk_factor=1.0),
    dict(time=40, magnitude=3, risk_factor=1.0),
    dict(time=60, magnitude=7, risk_factor=2.0),
]

for ax, A_baseline, color in zip(axes, baselines, colors):
    time, anxiety_values = test(A_baseline)
    ax.plot(time, anxiety_values, color=color)
    ax.set_xlabel('Time (s)')
    ax.set_title(f'Baseline STAI-S = {A_baseline}')

    # Get the model to access stressor objects with all properties
    model = AnxietyModel(A_baseline)
    for ev in stressor_events:
        s = model.add_stressor(
            motion_type='event',
            start_time=ev["time"],
            freq=2.0,
            amplitude=ev["magnitude"],
            lag=0.0,
            burst_start_time=ev["time"],
            burst_freq=50.0,
            impulse_magnitude=0.0,
            duration=0.10,
            risk_factor=ev["risk_factor"],
        )
        ax.axvline(x=s.time, color='red', linestyle='--', alpha=0.4, linewidth=0.8)

        label = (
            f"t={s.time}\n"
            f"mag={s.magnitude}\n"
            f"risk={s.risk_factor}\n"
            f"unexpect={s.unexpectedness}\n"
            f"decay={s.decay}"
        )
        ax.text(
            s.time + 5, ax.get_ylim()[1] * 0.98,
            label,
            fontsize=6.5,
            verticalalignment='top',
            color='red',
            alpha=0.8,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='red', alpha=0.5)
        )

axes[0].set_ylabel('Anxiety (STAI-S)')
plt.tight_layout()
plt.show()