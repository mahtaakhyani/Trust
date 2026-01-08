
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import config as cfg


TRUST_SCALE = cfg.TRUST_SCALE
FEATURE_WEIGHTS = cfg.FEATURE_WEIGHTS
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
    
    
    def trust_transition(self):
        # Row order: [Conscientiousness, Agreeableness, Extraversion, Openness, Neuroticism]
        # Column order: [TimingDelay, WalkingSymmetry, Balance, MetabolicCost]
        trust_transition = np.array([
            [-0.08,  0.04,  0.05,  0.03],   # Conscientiousness
            [-0.06,  0.05,  0.06,  0.04],   # Agreeableness
            [-0.10,  0.02,  0.03,  0.01],   # Extraversion
            [-0.09,  0.01,  0.02,  0.00],   # Openness
            [-0.15, -0.02, -0.03, -0.01]    # Neuroticism
        ])

        # Example: compute trust change for a user with trait vector T
        # (e.g., T = [1, 0.5, -0.2, 0, -0.8] where each entry is a standardized trait score)
        T = np.array([1.0, 0.5, -0.2, 0.0, -0.8])
        delta_trust = T @ trust_transition   # shape (4,) → change per feature
        print("Δtrust per feature:", delta_trust)
        
        traits = ["Conscientiousness", "Agreeableness",
          "Extraversion", "Openness", "Neuroticism"]
        features = ["Timing Delay", "Walking Symmetry", "Balance", "Metabolic Cost"]

        # -------------------------------------------------
        # 2️⃣  Plot a grouped bar chart (one group per trait)
        # -------------------------------------------------
        x = np.arange(len(traits))                 # the label locations
        width = 0.18                               # width of each bar

        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot each feature as its own set of bars
        for i, (feature, color) in enumerate(zip(features,
                                                ["#d62728", "#2ca02c", "#1f77b4", "#ff7f0e"])):
            ax.bar(x + i*width - 1.5*width,          # shift each bar within the group
                trust_transition[:, i],
                width,
                label=feature,
                color=color)

        # -------------------------------------------------
        # 3️⃣  Beautify the figure
        # -------------------------------------------------
        ax.set_ylabel("Δ Trust (per unit change in feature)")
        ax.set_title("Effect of Robot Action Features on Trust by Personality Trait")
        ax.set_xticks(x)
        ax.set_xticklabels(traits, rotation=15, ha="right")
        ax.axhline(0, color="gray", linewidth=0.8)   # zero line for reference
        ax.legend(title="Feature", loc="upper right")
        ax.grid(axis="y", linestyle="--", alpha=0.6)

        plt.tight_layout()
        plt.show()
            
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
    




# ============================================================================
# Display all transition parameters
# ============================================================================
print("="*80)
print("TRANSITION PARAMETERS MATRIX")
print("="*80)
print("\n1. FEATURE WEIGHTS (Performance Calculation)")
print("-" * 80)
for key, value in FEATURE_WEIGHTS.items():
    print(f"  {key:30s}: {value}")

print("\n2. PERSONALITY TRAIT PARAMETERS")
print("-" * 80)
trait_params_df = pd.DataFrame(TRAIT_PARAMETERS).T
print(trait_params_df.to_string())

print("\n3. BASE PARAMETERS")
print("-" * 80)
print(f"  {'Base Trust Level':30s}: {BASE_TRUST_LEVEL}")
print(f"  {'Base Error Impact':30s}: {BASE_ERROR_IMPACT}")

# Convert to numpy matrix format for direct access
print("\n" + "="*80)
print("NUMPY MATRIX REPRESENTATION")
print("="*80)

# Create structured arrays for each parameter type
traits_list = ['conscientiousness', 'agreeableness', 'extraversion', 'openness', 'neuroticism']
trait_params_df = pd.DataFrame(TRAIT_PARAMETERS).T
# Extract all unique parameter names
all_param_names = set()
for trait_params in TRAIT_PARAMETERS.values():
    all_param_names.update(trait_params.keys())
all_param_names = sorted(all_param_names)

# Create personality parameter matrix: [trait, parameter]
personality_matrix = np.zeros((len(traits_list), len(all_param_names)))

for i, trait in enumerate(traits_list):
    for j, param in enumerate(all_param_names):
        personality_matrix[i, j] = TRAIT_PARAMETERS[trait].get(param, 0.0)

print("\nPersonality Parameters Matrix Shape:", personality_matrix.shape)
print("Rows (traits):", traits_list)
print("Columns (parameters):", all_param_names)
print("\nMatrix:")
print(personality_matrix)

# Feature weights as vector
feature_weight_vector = np.array([
    FEATURE_WEIGHTS['walking_symmetry'],
    FEATURE_WEIGHTS['balance'],
    FEATURE_WEIGHTS['metabolic_cost']
])
print("\n\nFeature Weight Vector:", feature_weight_vector)
print("(Order: walking_symmetry, balance, metabolic_cost)")

timing_weight_vector = np.array(FEATURE_WEIGHTS['timing_vs_performance'])
print("\nTiming vs Performance Weights:", timing_weight_vector)
print("(Order: timing, performance)")

# ============================================================================
# TRUST CALCULATION FUNCTION (using the matrices above)
# ============================================================================

def calculate_trust_effect(trait_name, trait_score, action_features):
    """
    Calculate trust effect using the transition matrices defined above.
    
    Parameters:
    - trait_name: one of ['conscientiousness', 'agreeableness', 'extraversion', 'openness', 'neuroticism']
    - trait_score: 0-100 score for that trait
    - action_features: dict with keys ['timing_delay', 'walking_symmetry', 'balance', 'metabolic_cost']
    
    Returns:
    - trust_level: predicted trust level (1-7 Likert scale)
    """
    
    # Get trait parameters
    params = TRAIT_PARAMETERS[trait_name]
    trait_normalized = trait_score / 100
    
    # Calculate performance quality using FEATURE_WEIGHTS
    performance_components = np.array([
        100 - action_features['walking_symmetry'],  # Lower error = better
        100 - action_features['balance'],           # Lower error = better
        action_features['metabolic_cost']           # Higher benefit = better
    ])
    performance_quality = np.dot(performance_components, feature_weight_vector) / 100
    
    # Calculate timing quality
    timing_quality = (100 - action_features['timing_delay']) / 100
    
    # Overall robot quality using timing_vs_performance weights
    quality_components = np.array([timing_quality, performance_quality])
    robot_quality = np.dot(quality_components, timing_weight_vector)
    
    # Error magnitude (inverse of quality)
    error_magnitude = 1 - robot_quality
    
    # Apply trait-specific trust modulation
    trust_delta = 0
    
    if trait_name in ['conscientiousness', 'agreeableness', 'extraversion', 'openness']:
        # Protective traits reduce trust loss
        protection_factor = trait_normalized ** params['protection_exponent']
        trust_delta = -error_magnitude * BASE_ERROR_IMPACT * (1 - protection_factor * params['protection_strength'])
        
        # Additional bonuses
        if 'performance_bonus' in params and params['performance_bonus'] > 0:
            trust_delta += robot_quality * params['performance_bonus'] * trait_normalized
        
        if 'baseline_trust_boost' in params:
            trust_delta += trait_normalized * params['baseline_trust_boost']
        
        if 'engagement_bonus' in params:
            trust_delta += trait_normalized * params['engagement_bonus'] * robot_quality
        
        if 'timing_tolerance' in params:
            timing_tolerance = trait_normalized * params['timing_tolerance']
            trust_delta += timing_tolerance * (action_features['timing_delay'] / 100) * params['novelty_bonus']
    
    elif trait_name == 'neuroticism':
        # Neuroticism amplifies distrust
        anxiety_amplification = trait_normalized ** params['anxiety_exponent']
        trust_delta = -error_magnitude * BASE_ERROR_IMPACT * (1 + anxiety_amplification * params['distrust_amplification'])
        
        # Extra sensitivity to timing
        trust_delta -= (action_features['timing_delay'] / 100) * trait_normalized * params['timing_sensitivity']
    
    # Calculate final trust level
    trust_level = BASE_TRUST_LEVEL + trust_delta
    
    # Constrain to Likert 1-7 scale
    trust_level = np.clip(trust_level, 1, 7)
    
    return trust_level


# ============================================================================
# Generate complete transition tensor
# ============================================================================

trait_scores = np.linspace(0, 100, 11)
timing_delay = np.linspace(0, 100, 11)
walking_symmetry = np.linspace(0, 100, 11)
balance = np.linspace(0, 100, 11)
metabolic_cost_levels = np.linspace(0, 100, 11)

# Full 6D tensor: [trait, trait_score, timing, symmetry, balance, metabolic_cost]
print("\n" + "="*80)
print("GENERATING FULL TRANSITION TENSOR")
print("="*80)

trust_tensor = np.zeros((5, 11, 11, 11, 11, 11))

print("Computing trust values for all combinations...")
print(f"Dimensions: {trust_tensor.shape}")
print(f"Total combinations: {np.prod(trust_tensor.shape):,}")

for t_idx, trait in enumerate(traits_list):
    for ts_idx, ts_val in enumerate(trait_scores):
        for td_idx, td_val in enumerate(timing_delay):
            for ws_idx, ws_val in enumerate(walking_symmetry):
                for b_idx, b_val in enumerate(balance):
                    for mc_idx, mc_val in enumerate(metabolic_cost_levels):
                        action_feat = {
                            'timing_delay': td_val,
                            'walking_symmetry': ws_val,
                            'balance': b_val,
                            'metabolic_cost': mc_val
                        }
                        trust = calculate_trust_effect(trait, ts_val, action_feat)
                        trust_tensor[t_idx, ts_idx, td_idx, ws_idx, b_idx, mc_idx] = trust

print(f"\nTensor shape: {trust_tensor.shape}")
print(f"Trust range: [{trust_tensor.min():.3f}, {trust_tensor.max():.3f}]")
print(f"Mean trust: {trust_tensor.mean():.3f}")
print(f"Std trust: {trust_tensor.std():.3f}")

# ============================================================================
# SAMPLE PREDICTIONS
# ============================================================================

print("\n" + "="*80)
print("SAMPLE TRUST PREDICTIONS")
print("="*80)

scenarios = [
    {
        'name': 'Perfect Robot Performance',
        'timing_delay': 0,
        'walking_symmetry': 0,
        'balance': 0,
        'metabolic_cost': 80
    },
    {
        'name': 'Moderate Robot Errors',
        'timing_delay': 40,
        'walking_symmetry': 30,
        'balance': 25,
        'metabolic_cost': 50
    },
    {
        'name': 'Severe Robot Failures',
        'timing_delay': 80,
        'walking_symmetry': 70,
        'balance': 75,
        'metabolic_cost': 20
    }
]

for scenario in scenarios:
    print(f"\n{scenario['name']}:")
    print(f"  Timing delay: {scenario['timing_delay']}%, Symmetry error: {scenario['walking_symmetry']}%")
    print(f"  Balance error: {scenario['balance']}%, Metabolic benefit: {scenario['metabolic_cost']}%")
    print(f"\n  Trust levels by personality (Low/Medium/High trait scores):")
    
    for trait in traits_list:
        trust_low = calculate_trust_effect(trait, 20, scenario)
        trust_med = calculate_trust_effect(trait, 50, scenario)
        trust_high = calculate_trust_effect(trait, 80, scenario)
        
        print(f"    {trait:18s}: Low={trust_low:.2f}, Med={trust_med:.2f}, High={trust_high:.2f}")

# ============================================================================
# VISUALIZATIONS
# ============================================================================

print("\n" + "="*80)
print("GENERATING VISUALIZATIONS")
print("="*80)

fig = plt.figure(figsize=(18, 12))

for idx, trait in enumerate(traits_list):
    ax = fig.add_subplot(2, 3, idx+1, projection='3d')
    
    trait_grid = np.linspace(0, 100, 30)
    error_grid = np.linspace(0, 100, 30)
    T, E = np.meshgrid(trait_grid, error_grid)
    
    Z = np.zeros_like(T)
    for i in range(len(error_grid)):
        for j in range(len(trait_grid)):
            combined_error = error_grid[i]
            action_feat = {
                'timing_delay': combined_error * 0.4,
                'walking_symmetry': combined_error * 0.35,
                'balance': combined_error * 0.35,
                'metabolic_cost': max(0, 70 - combined_error * 0.5)
            }
            Z[i, j] = calculate_trust_effect(trait, trait_grid[j], action_feat)
    
    surf = ax.plot_surface(T, E, Z, cmap='RdYlGn', alpha=0.8, edgecolor='none')
    
    ax.set_xlabel('Trait Score', fontsize=9)
    ax.set_ylabel('Error Magnitude', fontsize=9)
    ax.set_zlabel('Trust Level', fontsize=9)
    ax.set_title(trait.capitalize(), fontsize=11, fontweight='bold')
    ax.set_zlim(1, 7)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('trust_surfaces_by_trait.png', dpi=150, bbox_inches='tight')
print("\nVisualization saved as 'trust_surfaces_by_trait.png'")

print("\n" + "="*80)
print("COMPLETE!")
print("="*80)
print("\nYou can now modify the transition parameters at the top of the code")
print("and rerun to see how different weights affect trust predictions.")