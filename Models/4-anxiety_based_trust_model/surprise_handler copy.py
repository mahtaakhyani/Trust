import numpy as np
from scipy.stats import kurtosis
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import logging


# Basic configuration to output INFO level messages or higher to the console
logging.basicConfig(level=logging.INFO)


# ----------------------------------- CALCULATE SURPRISE FACTOR S_i -----------------------------------------

SAMPLING_FREQ = 100
class SurpriseFactorsHandler:

    def __init__(self, sampling_frequency=SAMPLING_FREQ):  # (e.g., 100Hz)
        '''
            Initiating the vars that are unique to each experiment setup, but not the same among all setups
        '''
        self.sampling_frequency = sampling_frequency
        self.threshold=-8.0
        self.k=0.5
        self.accel_data = np.array([])
        self.event_segment = np.array([])
    
    def event_handler(self, event_time_index, accel_data, duration):
        self.accel_data = accel_data # update accel history based on the latest recieved data
        self._calculate_event_segment(event_time_index)
        if len(self.event_segment) == 0:
            return 0.0, 0.0, 0.0, 0.0
        
        crest = self.calculate_crest()
        kurt = self.calculate_kurt(fisher=True, bias=False)
        ldlj = self.calculate_ldlj(duration)
        jerk_effect = 1 / (1 + np.exp(self.k * (ldlj - self.threshold)))

        surprise = kurt * jerk_effect
        return crest, kurt, surprise, jerk_effect
        
        
    def _calculate_event_segment(self, event_time_index):
        half_window = 0.025 * self.sampling_frequency  # 2.5 samples at 100Hz
        start = max(0, int(event_time_index - half_window))
        end = min(len(self.accel_data), int(event_time_index + half_window))

        # 1. Crop the event
        event_segment = np.array(self.accel_data[start:end])

        # # Ensure the window has a minimum number of samples to be statistically valid
        # if len(event_segment) < int(0.05 * self.sampling_frequency):
        #     self.event_segment = np.array([])
        #     return  # invalid event window
        
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
                Kurtosis for normal walking ≈ 3 (or 0 if using "excess kurtosis", aka., fisher=True)
                Kurtosis for abnormal signal ≈ 10, 20, 100, etc.
        '''
        k = kurtosis(self.event_segment, fisher=fisher, bias=bias)
        return abs(k)



    def calculate_jerk(self, dt=0.001, window_size=11, poly_order=3):
        """
        Calculate jerk on the current event window.
        
        Parameters:
        dt (float): Time interval between samples (e.g., 0.001 for 1000Hz).
        window_size (int): Number of samples for the smoothing window (must be odd, a window of 11 covers 11 milliseconds).
        poly_order (int): The order of the polynomial to fit (3 is standard for jerk).
        
        Returns:
        float: Peak absolute jerk over the event window.
        """
        
        accel = np.asarray(self.event_segment)
        n = accel.size
        if n == 0:
            return 0.0

        # Savitzky–Golay requires: window_length odd, <= n, and poly_order < window_length
        wl = int(window_size)
        if wl % 2 == 0:
            wl -= 1
        wl = min(wl, n if n % 2 == 1 else n - 1)
        min_wl = poly_order + 2  # strictly > poly_order, keep it odd below
        if min_wl % 2 == 0:
            min_wl += 1
        if wl < max(3, min_wl):
            # Too few samples for a stable SG derivative; return zeros matching shape.
            return 0.0

        jerk = savgol_filter(
            accel,
            window_length=wl,
            polyorder=poly_order,
            deriv=1,
            delta=dt,
        )
        return float(np.max(np.abs(jerk)))

    def _calculate_jerk_signal(self, dt: float, window_size: int = 11, poly_order: int = 3) -> np.ndarray:
        """
        Return jerk signal over the event window (same length as event).
        """
        accel = np.asarray(self.event_segment, dtype=float)
        n = accel.size
        if n < 2:
            return np.zeros(n, dtype=float)

        wl = int(window_size)
        if wl % 2 == 0:
            wl -= 1
        wl = min(wl, n if n % 2 == 1 else n - 1)
        min_wl = poly_order + 2
        if min_wl % 2 == 0:
            min_wl += 1

        if wl >= max(3, min_wl):
            return savgol_filter(
                accel,
                window_length=wl,
                polyorder=poly_order,
                deriv=1,
                delta=dt,
            ).astype(float, copy=False)

        # Too few samples for stable SG derivative.
        return np.gradient(accel, dt).astype(float, copy=False)



    def calculate_ldlj(self, duration):
        """
        Calculates the Log Dimensionless Jerk (LDLJ) for a given motion profile.
        Higher (less negative) = Smoother
        Lower (more negative) = Jerkier/More impulsive
        """
        duration = 1
        if duration <= 0.0 or len(self.event_segment) < 2:
            return 0.0

        dt = 1.0 / float(self.sampling_frequency)
        # 1. Calculate jerk signal (derivative of acceleration)
        jerk = self._calculate_jerk_signal(dt=dt)
        
        # 2. Calculate Peak Velocity (integral of acceleration) for normalization
        # If velocity is constant before the stop, use the peak magnitude.
        v_peak = np.max(np.abs(np.cumsum(self.event_segment) * dt))
        if v_peak == 0: v_peak = 1e-6 # Avoid division by zero
        
        # 3. Calculate Dimensionless Jerk (DJ)
        # Integral of squared jerk * (Duration^3 / Peak_Velocity^2)
        msj_integral = float(np.trapezoid(jerk**2, dx=dt))
        dj = msj_integral * (duration**3 / (v_peak**2))
        
        # 4. Logarithmic scale
        # We use -ln(DJ) so that smoother movements have higher values
        if not np.isfinite(dj) or dj <= 0.0:
            return 0.0
        return float(-np.log(dj))



