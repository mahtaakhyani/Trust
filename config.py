import numpy as np

# ================================================================================
# TRUST PARAMETERS
# ================================================================================
TRUST_SCALE = 7
# Base error impact (before personality modulation)
BASE_ERROR_IMPACT = 2.5  # Maximum trust loss from errors
BASE_TRUST_LEVEL = 4.0   # Neutral starting trust (on 1-7 scale)



# ================================================================================
# TRANSITION PARAMETERS MATRIX
# ================================================================================
# < All transition weights in one place - these define how features map to trust >
# --------------------------------------------------------------------------------
T0 = 0.05  # temporal tolerance (JND) in seconds
STRIDE_TIME = 1.0      # seconds
OMEGA = 2 * np.pi / STRIDE_TIME # task angular frequency (Interpretation: Normal walking cadence. Adjust if cadence changes)
PHI_PREF = 0.0 # preferred assistance phase
# Interpretation:
# Assistance aligned with expected phase
# Shift only if you have phase-specific actuation

g = 1.0 # perceptual gain
# ===================================
# Overall Performance Features Matrix
# ===================================
# Feature weights: How each performance metric contributes to overall quality
# -----------------------------------
FEATURE_WEIGHTS = {
    'walking_symmetry': 0.4,  # Weight for symmetry in performance error calculation
    'balance': 0.5,           # balance is felt faster
    'metabolic_cost': 0.3,    # metabolic cost is slowest
}

# =====================================
# Personality Trait Transition Parameters
# Structure: [trait_name] -> {parameter_name: value}
# =====================================
TRAIT_SCALE = 40 # Maximum trait score (used for normalization)

# temporal sensitivity (Sharpness) -> (sigmoid slope )
# -----------------
BETA_MIN = 5.0 # Lower bound on sharpness
BETA_MAX = 40.0 # Upper bound on sharpness


TRAIT_PARAMETERS = {
    'conscientiousness': {
        'protection_exponent': 1.5,      # Nonlinearity of protective effect
        'protection_strength': 0.6,      # How much it reduces trust loss (0-1)
        'performance_bonus': 0.8,        # Boost from good performance
        'performance_scaling': 1.0,      # Scaling with trait level
    },
    'agreeableness': {
        'protection_exponent': 1.2,      # Nonlinearity of protective effect
        'protection_strength': 0.7,      # How much it reduces trust loss (0-1)
        'baseline_trust_boost': 0.5,     # Unconditional trust increase
        'performance_bonus': 0.0,        # (No special performance bonus)
    },
    'extraversion': {
        'protection_exponent': 1.3,      # Nonlinearity of protective effect
        'protection_strength': 0.4,      # How much it reduces trust loss (0-1)
        'engagement_bonus': 0.3,         # Boost from social engagement
        'quality_interaction': 1.0,      # Multiplied by robot_quality
    },
    'openness': {
        'protection_exponent': 1.1,      # Nonlinearity of protective effect
        'protection_strength': 0.3,      # How much it reduces trust loss (0-1)
        'timing_tolerance': 0.4,         # Tolerance for timing unpredictability
        'novelty_bonus': 0.5,            # Bonus when timing is imperfect
    },
    'neuroticism': {
        'anxiety_exponent': 1.4,         # Nonlinearity of anxiety amplification
        'distrust_amplification': 0.8,   # How much it increases trust loss (0-1)
        'timing_sensitivity': 0.6,       # Extra sensitivity to timing issues
        'performance_bonus': 0.0,        # (No performance bonus)
    }
}
