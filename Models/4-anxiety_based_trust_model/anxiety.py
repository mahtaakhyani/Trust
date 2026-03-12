from motion_types import CreateMotion
from sklearn.metrics import mean_squared_error
import numpy as np

class Anxiety:
    def __init__(self, a_baseline):
        self.A_baseline = a_baseline
        
    
    def instantaneous_anxiety(self, beta, mismatch):
        A = self.A_baseline + beta*mismatch
        
        return A
    
    def predictive_model(self, t):
        create_motion = CreateMotion() 
        motion_model = np.array(create_motion._smooth_motion(t=t))
        
        return motion_model
        
    def calculate_mismatch(self, signal, t):
        expected_signal = self.predictive_model(t)
        mse = mean_squared_error(expected_signal, np.array(signal))
        
        return mse
        
        

def test():
    a = Anxiety(20)
    t = np.arange(10)
    motion = CreateMotion()
    baseline = motion.motion(
        t=t,
        start_time=0.0,
        motion_type="smooth",
        freq=2,
        amplitude=1,
    )
    vib_delta = motion.motion(
        t=t,
        start_time=10,
        motion_type="vibration",
        burst_start_time=10,
        burst_freq=50.0,
        duration=0.10,
        amplitude=0.5,
    )
    vib = baseline + vib_delta
    
    mismatch = a.calculate_mismatch(vib, t)
    print(mismatch)
    
    
test()