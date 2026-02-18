
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
    def __init__(self, 
                 anxiety_level=0.5,
                 trust_level=None) -> None:
        
        self.anxiety_level=anxiety_level      
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

        }
        
        
        return observations
       
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
    

    def anxiety_updater(self) -> ?:
        pass