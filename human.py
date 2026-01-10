
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
    
    
    def trait_trust_to_observation(self) -> np.array[tuple[int, int, int], float]:
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
    
    def compute_sharpness_beta(self,
                                scale=40,
                                beta_min=5.0,
                                beta_max=40.0,
                                confidence_weight=1.0,
                                ):
        """
        Map Big Five personality traits to perceptual sharpness (beta).
        
        Weights prioritize temporal error detection evidence where available,
        falling back to general cognitive sharpness evidence when temporal data
        is insufficient. Confidence weighting scales contributions based on
        evidence quality.

        Parameters
        ----------
        scale : int
            Maximum trait score (used for normalization).
        beta_min : float
            Lower bound on sharpness.
        beta_max : float
            Upper bound on sharpness.
        confidence_weight : float, default=1.0
            Multiplier for confidence-based weighting (0.0-1.0).
            Reduces weight of lower-confidence associations when < 1.0.

        Returns
        -------
        beta : float
            Individual sharpness parameter for perceived_error().
        """

        A, O, C, E, N = self.personality_traits / scale  # normalize to [0,1]

        # Base weights reflect evidence hierarchy from temporal_sharpness_bigFive_mapping.md
        # Temporal error detection evidence is prioritized; general sharpness used as fallback
        
        # Openness: 0.48
        # TEMPORAL EVIDENCE: Moderate confidence - most direct link to temporal error detection
        # via cognitive ability pathway. Higher temporal discrimination correlates with
        # psychometric intelligence, which is positively associated with Openness.
        # Weight reflects primary driver status with moderate confidence.
        w_openness = 0.48
        
        # Conscientiousness: 0.15
        # TEMPORAL EVIDENCE: Insufficient - no direct empirical evidence for temporal mapping.
        # GENERAL SHARPNESS: Positive association - predicts better cognitive performance
        # and slower decline, but this relates to maintenance over time rather than
        # moment-to-moment temporal precision. Reduced weight reflects lack of temporal evidence.
        w_conscientiousness = 0.15
        
        # Extraversion: 0.05
        # TEMPORAL EVIDENCE: Insufficient - no direct temporal sensitivity measurements.
        # GENERAL SHARPNESS: Modest, domain-specific positive links (speed-attention-executive,
        # verbal fluency) but weaker for complex reasoning. Minimal weight reflects
        # insufficient temporal evidence and modest general effects.
        w_extraversion = 0.05
        
        # Agreeableness: 0.02
        # TEMPORAL EVIDENCE: Insufficient - no data linking temporal discrimination to Agreeableness.
        # GENERAL SHARPNESS: Weak to mixed positive links, small effect sizes, facet-dependent.
        # Minimal weight reflects weakest evidence base among all traits.
        w_agreeableness = 0.02
        
        # Neuroticism: -0.30
        # TEMPORAL EVIDENCE: Low-moderate confidence, indirect mapping via cognitive ability.
        # Temporal discrimination correlates with intelligence, which shows negative
        # associations with Neuroticism. However, evidence is indirect and tentative.
        # Reduced magnitude reflects lower confidence and indirect pathway.
        w_neuroticism = -0.30
        
        # Apply confidence weighting to lower-confidence associations
        # Openness (moderate confidence) and Neuroticism (low-moderate) are scaled down
        # when confidence_weight < 1.0
        w_openness_conf = w_openness * (0.7 + 0.3 * confidence_weight)  # moderate confidence
        w_neuroticism_conf = w_neuroticism * (0.5 + 0.5 * confidence_weight)  # low-moderate confidence
        w_conscientiousness_conf = w_conscientiousness * confidence_weight  # insufficient temporal evidence
        w_extraversion_conf = w_extraversion * confidence_weight  # insufficient temporal evidence
        w_agreeableness_conf = w_agreeableness * confidence_weight  # insufficient temporal evidence
        
        # Weighted sharpness score
        # Weights sum to ~1.0 when confidence_weight=1.0, allowing natural scaling
        sharpness_score = (
            w_openness_conf * O +
            w_conscientiousness_conf * C +
            w_extraversion_conf * E +
            w_agreeableness_conf * A +
            w_neuroticism_conf * N
        )

        # Clamp latent score to [0,1]
        sharpness_score = np.clip(sharpness_score, 0.0, 1.0)

        # Map to usable beta range
        beta = beta_min + sharpness_score * (beta_max - beta_min)

        return beta


    def percieved_error(self,
                            A,
                            dt,
                            A_ref=0.1, # ~10% deviation = perceptual threshold (Weber-like)
                            context="event",
                            omega=2*np.pi,
                            beta=20.0,
                            t0=0.05,
                            phi_pref=0.0,
                            g=1.0,
                        ):
        """
        Human-perceived error salience model.
        The model is fully described in "human_senssorimotor_error_perception_model_complex.md"

        Parameters
        ----------
        A : float or ndarray
            Action error magnitude (force/torque deviation).
        dt : float or ndarray
            Timing error (seconds).
        A_ref : float
            Reference / expected action magnitude (Weber scale).
        context : {"rhythmic", "event"}
            Task type.
        omega : float
            Task angular frequency (rad/s), used for rhythmic tasks.
        beta : float
            Individual sharpness (age, training, pathology).
        t0 : float
            Temporal tolerance / JND (seconds).
        phi_pref : float
            Preferred phase for assistance (rad).
        g : float
            Adaptation gain (0–1).

        Returns
        -------
        E : float or ndarray
            Perceived error salience (unitless).
        """
        # Weber-scaled magnitude term
        mag = np.log1p(np.abs(A) / A_ref)

        # Temporal kernel
        if context == "event":
            K = 1.0 / (1.0 + np.exp(-beta * (np.abs(dt) - t0)))
        elif context == "rhythmic":
            phi = omega * dt
            K = 0.5 * (1.0 - np.cos(phi - phi_pref))
        else:
            raise ValueError("context must be 'event' or 'rhythmic'")

        return g * mag * K

    def calculate_trust_loss(self, trait, action):
        '''
            Calculates trust loss for each personality trait based on their current trust level.
            
            The current function is defined based on "BigFivePersonalityTraits_to_Trust.PDF" results,
            but the scores are entirely estimated values and not supported by experiment.
        '''
        normalized_trust_level = self.trust_level / TRUST_SCALE  # Normalize to 0-1 scale
        
        # Higher trait scores provide protection against trust loss except neuroticism (Negative Correlation)
        if trait == 'neuroticism':
            protection_factor = 1 - normalized_trust_level  # Higher neuroticism = less protection
        else:
            protection_factor = normalized_trust_level  # Higher trait = more protection
    

         # Calculate weighted error based on trait sensitivity
        weighted_error = (action.performance.performance_error * trait_weights[trait]['performance'] + 
                        action.norm_delay * trait_weights[trait]['timing'])
        
        
Human().plot_trait_trust_observations_correlation_matrix()