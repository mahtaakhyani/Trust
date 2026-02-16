
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import config as cfg
import robot as rb

plt.set_loglevel("warning") 

TRUST_SCALE = cfg.TRUST_SCALE
TRAIT_PARAMETERS = cfg.TRAIT_PARAMETERS
BASE_ERROR_IMPACT = cfg.BASE_ERROR_IMPACT
BASE_TRUST_LEVEL = cfg.BASE_TRUST_LEVEL


class Human:
    def __init__(self, age=25,
                 gender='male', 
                 anxiety_level=0.5, 
                 personality_traits=[], 
                 trust_level=None) -> None:
        self.age=age
        self.gender=gender
        self.anxiety_level=anxiety_level
        self.personality_traits=personality_traits if personality_traits else self.generate_random_personality()
        # T_dispositional: baseline propensity to trust
        self.T_dispositional = self._compute_dispositional_trust()
        
        # T_situational: context/environment (you don't have this yet)
        self.T_situational = 0.0
        
        # T_learned: dynamic component (what you're trying to model)
        self.T_learned = 0.0
        
        # Total trust
        self.trust_level = self.T_dispositional + self.T_situational + self.T_learned
        
        self.trust_level=trust_level if trust_level else np.random.randint(0, TRUST_SCALE)
        # State tracking
        self.fatigue_level = 0.0  # Increases over time
        self.cognitive_load = 0.5  # Task difficulty
        
        self.observations = self.set_default_observation()
        # Manually defined likelihood-style correlations between personality traits and observations
        # Rows = observations, Columns = traits
        # Values reflect how likely each observation is given high trait levels
        self.trait_correlation_matrix = np.array([
            # Agr   Open  Cons  Extra Neuro
            [-0.6, -0.4, -0.3, -0.2,  0.7],  # Hesitation
            [-0.7, -0.5, -0.4, -0.3,  0.6],  # Refused to Do Task
            [-0.3, -0.2, -0.6, -0.1,  0.5],  # Delayed Weight Transfer
            [ 0.5,  0.3,  0.6,  0.2, -0.5],  # Reduced Monitoring
            [-0.4, -0.3, -0.5, -0.2,  0.6],  # Increased Monitoring

            [ 0.4,  0.2,  0.3,  0.1, -0.7],  # Reduced Heart Rate
            [ 0.3,  0.1,  0.2,  0.0, -0.8],  # Reduced Palm Sweat
            [ 0.2,  0.1,  0.4, -0.1, -0.6],  # Reduced Co-contraction

            [-0.2, -0.3, -0.1, -0.4,  0.8],  # Increased Heart Rate
            [-0.1, -0.4, -0.1, -0.2,  0.9],  # Increased Palm Sweat
            [-0.3, -0.2, -0.4, -0.1,  0.7],  # Increased Co-contraction
        ])
        
    def set_default_observation(self):
        '''
            Define the initial default observation dictionary
        '''
        observations = {
            # --- trust in the robot's performance ---
            'hesitation':False, # Boolean for simplicity
            'refused_to_do_task':False,
            'delayed_weight_transfer':False,
            'reduced_monitoring_counts': False, # how many times the user monitors or looks at the robot during tasks
            # --- distrust in the robot's performance ---
            'increased_monitoring_counts': False, 
            # ---- Signs of relaxation ---
            'reduced_heart_rate':False, # change of heart rate after robot's action
            'reduced_palm_sweat': False,
            'reduced_cocontraction':False, # Muscle stiffening is an unconscious distrust response.
            # ---- Signs of anxiety ---
            'increased_heart_rate':False, 
            'increased_palm_sweat': False,
            'increased_cocontraction':False 
        }
        
        
        return observations
    
    def _compute_dispositional_trust(self):
        """Baseline propensity from personality"""
        A, O, C, E, N = self.personality_traits / 40
        
        # Evidence from your own document:
        # - Agreeableness: strongest predictor (r ≈ 0.35)
        # - Neuroticism: negative (r ≈ -0.30)
        # - Openness: positive for tech acceptance
        
        T_base = (
            0.40 * A +      # Strongest predictor
            0.20 * O +      # Tech acceptance
            0.15 * C +      # Reliability focus
            0.10 * E +      # Social trust
            -0.35 * N       # Anxiety/distrust
        )
        
        # Scale to your TRUST_SCALE (e.g., 0-10)
        return T_base * TRUST_SCALE * 0.5  # Start at ~50% of max
    
    def trait_trust_to_observation(self) -> np.array([tuple[int, int, int], float]):
        ''' 
        How likely observation i is for someone with trait k, at trust level t+1
                - Positive = more likely at high trust
                - Negative = more likely at low trust
        '''
        trust_sensitivity = np.array([
            -0.6,  # Hesitation
            -0.7,  # Refused Task
            -0.5,  # Delayed Weight Transfer
            0.6,  # Reduced Monitoring
            -0.6,  # Increased Monitoring

            0.7,  # Reduced Heart Rate
            0.6,  # Reduced Palm Sweat
            0.5,  # Reduced Co-contraction

            -0.8,  # Increased Heart Rate
            -0.9,  # Increased Palm Sweat
            -0.7   # Increased Co-contraction
        ])
        
        # Initialize tensor: trust × observation × trait
        trait_trust_observation_tensor = np.zeros((TRUST_SCALE, 
                                                   len(self.observations), 
                                                   len(self.personality_traits)))

        for t_idx, trust in enumerate(TRUST_SCALE):
            # Normalize trust to [-1, 1] with 4 as neutral
            trust_norm = (trust - 4) / 3  

            for obs_idx in range(len(self.observations)):
                modulation = 1 + trust_norm * trust_sensitivity[obs_idx]
                trait_trust_observation_tensor[t_idx, obs_idx, :] = (
                    self.trait_correlation_matrix[obs_idx, :] * modulation
                )
                
        return trait_trust_observation_tensor
              
    def plot_trait_trust_observations_correlation_matrix(self) -> None:
        '''
            Plot the correlation matrix of Trait vs Observation 
            (How possible it is to see an observation from a specific trait)
        '''
        # Automatically extract trait names from `generate_random_personality`
        # Filter out non-trait locals like 'self', 'scale', and the final 'personality_traits' array
        trait_names = [
            var
            for var in self.generate_random_personality.__code__.co_varnames
            if var not in ["self", "scale", "personality_traits"]
        ]

        df = pd.DataFrame(
            self.trait_correlation_matrix,
            index=list(self.observations.keys()),
            columns=trait_names,
        )

        # Plot
        plt.figure()
        plt.imshow(df.values, aspect="auto")

        # Center tick labels on the middle of each square
        x_positions = np.arange(df.shape[1])
        y_positions = np.arange(df.shape[0])

        plt.xticks(x_positions, df.columns, rotation=45, ha="right")
        plt.yticks(y_positions, df.index)
        plt.colorbar(label="Likelihood / Correlation Strength")
        plt.title("Observation vs Personality Trait Correlation Matrix")
        plt.tight_layout()
        
        plt.savefig('Observation vs Personality Trait Correlation Matrix.png')
         
    def generate_random_personality(self, scale=40) -> np.array:
        '''
            Generate a combination of random scores in each of the five personality traits.
            Based on Big Five Inventory (BFI-10/44) assesment of 
            The Five-Factor Model (FFM) - the most widely accepted 
            psychological framework for categorizing human personality
        '''
        Agreeableness = np.random.randint(0, scale) # (Positive Correlation):
            # strongest predictor of trust. High scorers naturally view others as honest and well-intentioned 
            # (Highly agreeable individuals have a higher "propensity to trust" machines)
        Openness = np.random.randint(0, scale) # (Positive Correlation):
            # Individuals high in openness generally show higher robot acceptance and are more willing to perform 
            # tasks alongside them. Conversely, low openness is a predictor of "technology anxiety" and higher initial skepticism.
        Conscientiousness = np.random.randint(0, scale) # (Reliability-Focused): 
            # This trait is a positive predictor of primary trust appraisal. Highly conscientious people often 
            # trust robots more when the robot demonstrates high performance and reliability.
        Extraversion = np.random.randint(0, scale) # (Social Trust):
            # Extraverts tend to have a higher willingness to trust and engage with robots, particularly those with 
            # human-like (anthropomorphic) features. Research also shows a "personality matching" effect: 
            # extraverts prefer robots with "extroverted" characteristics (e.g., louder voices or faster speech), 
            # which enhances their perceived trust and likability of the machine.
        Neuroticism = np.random.randint(0, scale) # (Negative Correlation): 
            # This trait is strongly associated with a negative attitude toward robots and higher levels of anticipated stress 
            # during interaction. Highly neurotic individuals are less likely to perceive robots as "likable" and often 
            # struggle to form a stable trust dynamic due to heightened sensitivity to potential robot errors.
        personality_traits = np.array([Agreeableness,
                              Openness,
                              Conscientiousness,
                              Extraversion,
                              Neuroticism])
        
        return personality_traits
    

    def compute_temporal_tolerance(self, t0_min=0.03, t0_max=0.10, age_ref=25):
        """
        Calculate temporal tolerance (t0) based on age.
        
        Older adults have wider Temporal Binding Window (TBW) and increased
        tolerance for timing errors, while younger users are more sensitive.
        
        Parameters
        ----------
        t0_min : float, default=0.03
            Minimum temporal tolerance for young adults (seconds).
        t0_max : float, default=0.10
            Maximum temporal tolerance for older adults (seconds).
        age_ref : int, default=25
            Reference age where t0 = t0_min (years).
        
        Returns
        -------
        t0 : float
            Temporal tolerance window (seconds).
        """
        # Linear increase: t0 increases with age beyond reference
        # Based on "age in error perception.md" - older adults have wider TBW
        age_factor = max(0, (self.age - age_ref) / 60.0)  # normalize to ~85 years
        return t0_min + age_factor * (t0_max - t0_min)



    """Asymmetric trust learning with personality modulation"""
    
    A, O, C, E, N = self.personality_traits / 40
    
    # Learning rates depend on personality
    # High N → faster loss, slower recovery
    # High A → faster recovery
    alpha_loss = 0.2 + 0.5 * N  # Range: 0.2-0.7
    alpha_gain = 0.03 + 0.12 * A  # Range: 0.03-0.15
    
    # Risk amplifies loss
    alpha_loss *= (1 + risk_level)
    
    # Error threshold for trust loss
    error_threshold = 0.2 - 0.1 * C  # Conscientious people more tolerant
    
    if perceived_error > error_threshold:
        # Trust LOSS: fast, nonlinear
        # Use exponential: small errors → small loss, large errors → catastrophic
        loss_magnitude = 1 - np.exp(-3 * perceived_error)
        delta = -alpha_loss * loss_magnitude * TRUST_SCALE
        
    else:
        # Trust GAIN: slow, requires sustained good performance
        # Diminishing returns as trust approaches maximum
        room_to_grow = 1 - (self.T_learned / (TRUST_SCALE - self.T_dispositional))
        gain_magnitude = action_quality * room_to_grow
        delta = alpha_gain * gain_magnitude * TRUST_SCALE
    
    return delta