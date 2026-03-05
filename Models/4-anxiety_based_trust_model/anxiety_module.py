'''
This module models the anxiety accumulation and decay over time. 

It takes these variables as input to initiate an Anxiety class instance:
    1. Anxiety baseline (A_baseline) -> individual's baseline anxiety
    2. Decay constant (Lambda) -> how fast the anxiety naturally decays in time for the user
    3. Negativity Bias (W_i) -> how strongly the user perceives the stressor
    
It takes these variables to update the Anxiety class instance:
    1. Time of the stressor signal (t)
    2. Stressor true magnitude (S_i) -> not the perceived value
    3. Stressor risk factor (R_i) -> how risky the stressor is
    

The model is built upon the following phrases:
    * Anxiety decay expression: e^{-lambda*(t - t_i)} (Leacky integrator model)
    * The perceived strength of the stressor: w_i * S_i * R_i
    * The non-linearity expression of the cumulative physiological cost of the stressors: ∑_i=1^n

Overall model:
        A(t) = A_baseline + ∑_i [(w_i * S_i * R_i) * e^{-lambda * (t - t_i)}]
        
To map the model onto standard STAI-S measurement scale:
        A(t) = 20 + [(A(t) - A_min)/(A_max - A_min)] * 60
    
    Where:
        - A_min = A_baseline (resting, no stressors) → maps to STAI-S = 20
        - A_max = theoretical ceiling (all stressors firing at once) → maps to STAI-S = 80

This module also keeps a history of all the anxiety levels and stressors. 

'''
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from itertools import count



W_BASE = 1.0  # population-level negativity bias constant
ALPHA = 0.4   # sensitivity of negativity bias to baseline
BETA = 0.3    # sensitivity of decay rate to baseline
_id_counter = count(1)

class AnxietyModel:
    def __init__(self, A_baseline, lambda_decay):
        self.A_baseline = A_baseline
        self.lambda_decay = lambda_decay * (1 - BETA * A_baseline)
        self.negativity_weight = W_BASE * (1 + ALPHA * A_baseline)
        self.stressor_history = []
        self.anxiety_history = []
        self.current_anxiety_level = self.A_baseline
        
        
    @dataclass
    class Stressor:
        id: int = field(default_factory= lambda: next(_id_counter))
        time: float = field(default=0.0)
        magnitude: float = field(default=0.0)
        risk_factor: float = field(default=1.0)
        
    @dataclass
    class Anxiety:
        level: int
        time: float
        stressor: Stressor
    

    def add_stressor(self, time: float, magnitude: float, risk_factor: float):
        stressor = self.Stressor(time=time, magnitude=magnitude, risk_factor=risk_factor)
        self.stressor_history.append(stressor)
        self._update_anxiety(time, stressor)
        


    def _update_anxiety(self, time: float, stressor) -> float:
        A = self.A_baseline + sum(
            self.negativity_weight * s.magnitude * s.risk_factor * np.exp(-self.lambda_decay * (time - s.time))
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
            self.negativity_weight * s.magnitude * s.risk_factor * np.exp(-self.lambda_decay * (time - s.time))
            for s in self.stressor_history
            if s.time <= time
        )
        return A


def test(A_baseline=0.1, lambda_decay=0.35):
    model = AnxietyModel(A_baseline, lambda_decay) # individual factors

    model.add_stressor(time=20, magnitude=0.5, risk_factor=1.0) # event factors
    model.add_stressor(time=40, magnitude=0.3, risk_factor=1.0)
    model.add_stressor(time=60, magnitude=0.7, risk_factor=2.0)

    time = np.linspace(0, 100, 1000)
    anxiety_values = [model.get_anxiety_at(t) for t in time]

    # STAI-S scaling
    A_min = model.A_baseline
    A_max = max(anxiety_values)
    stai_values = [20 + ((a - A_min) / (A_max - A_min)) * 60 for a in anxiety_values]

    return time, stai_values

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes[0].set_xlabel('Time (min)')
axes[1].set_xlabel('Time (min)')
axes[2].set_xlabel('Time (min)')
axes[0].set_ylim(20, 80)
axes[1].set_ylim(20, 80)
axes[2].set_ylim(20, 80)
axes[0].set_title('Anxiety Accumulation and Decay')
axes[1].set_title('Anxiety Accumulation and Decay')
axes[2].set_title('Anxiety Accumulation and Decay')

time, stai = test(A_baseline=0.1, lambda_decay=0.35)
axes[0].set_ylabel('Anxiety (STAI-S) - decay = 0.35, baseline = 0.1')
axes[0].plot(time, stai)

time, stai = test(A_baseline=0.4, lambda_decay=0.35)
axes[1].set_ylabel('Anxiety (STAI-S) - decay = 0.35, baseline = 0.1')
axes[1].plot(time, stai)

time, stai = test(A_baseline=0.1, lambda_decay=0.7)
axes[2].set_ylabel('Anxiety (STAI-S) - decay = 0.7, baseline = 0.1')
axes[2].plot(time, stai)

plt.tight_layout()
plt.show()