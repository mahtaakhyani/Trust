from token import OP
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

TRUST_SCALE = 7

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
        self.trust_level=trust_level if trust_level else np.random.randint(0, TRUST_SCALE)
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
    
    
    def trust_to_observation(self):
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
    
    
    def plot_trait_observations_correlation_matrix(self) -> None:
        '''
            Plot the correlation matrix of Trait vs Observation 
            (How possible it is to see an observation from a specific trait)
        '''
        df = pd.DataFrame(
            self.trait_correlation_matrix,
            index=[keys for keys in self.observations],
            columns=self.personality_traits
        )

        # Plot
        plt.figure()
        plt.imshow(df.values)
        plt.xticks(range(len(self.personality_traits)), 
                   ['Agreeableness', 
                              'Openness', 
                              'Conscientiousness', 
                              'Extraversion', 
                              'Neuroticism'], 
                   rotation=45)
        plt.yticks(range(len(self.observations)), self.observations)
        plt.colorbar(label="Likelihood / Correlation Strength")
        plt.title("Observation vs Personality Trait Correlation Matrix")
        plt.tight_layout()
        plt.show()
        
    
    def generate_random_personality(self, scale=40) -> np.array:
        '''
            Based on Big Five Inventory (BFI-10/44) assesment of 
            The Five-Factor Model (FFM) - the most widely accepted 
            psychological framework for categorizing human personality
        '''
        Agreeableness = np.random.randint(0, scale) # (Positive Correlation):
            # strongest predictor of trust. High scorers naturally view others as honest and well-intentioned (Highly agreeable individuals have a higher "propensity to trust" machines)
        Openness = np.random.randint(0, scale) # (Positive Correlation):
            # Individuals high in openness generally show higher robot acceptance and are more willing to perform tasks alongside them. Conversely, low openness is a predictor of "technology anxiety" and higher initial skepticism.
        Conscientiousness = np.random.randint(0, scale) # (Reliability-Focused): 
            # This trait is a positive predictor of primary trust appraisal. Highly conscientious people often trust robots more when the robot demonstrates high performance and reliability.
        Extraversion = np.random.randint(0, scale) # (Social Trust):
            # Extraverts tend to have a higher willingness to trust and engage with robots, particularly those with human-like (anthropomorphic) features. Research also shows a "personality matching" effect: extraverts prefer robots with "extroverted" characteristics (e.g., louder voices or faster speech), which enhances their perceived trust and likability of the machine.
        Neuroticism = np.random.randint(0, scale) # (Negative Correlation): 
            # This trait is strongly associated with a negative attitude toward robots and higher levels of anticipated stress during interaction. Highly neurotic individuals are less likely to perceive robots as "likable" and often struggle to form a stable trust dynamic due to heightened sensitivity to potential robot errors.
            
        personality_traits = np.array([Agreeableness, 
                              Openness, 
                              Conscientiousness, 
                              Extraversion, 
                              Neuroticism])
        
        return personality_traits
    
    
    