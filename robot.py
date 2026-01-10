from pydantic import BaseModel, ValidationError, confloat, conint
import numpy as np
import logging
import config as cfg

FEATURE_WEIGHTS = cfg.FEATURE_WEIGHTS

# Configure logging 
logging.basicConfig(level=logging.DEBUG)

class Action:
    '''
        The action of the robot with its properties and factors.
        The features of an action includes: 
            - timing delay: how the robot does its action on a WRONG TIMING (makes unpredictability)
            - performance: how GOOD the robot does its job (relates to ability/usability)
        
        Attributes
        ----------
        timing_delay : float
            Temporal offset (in seconds, normalized to [0, 1]) that makes the
            action more or less predictable. Higher values mean higher
            unpredictability (aside from the performance score).
        performance : FunctionalPerformance
            Object describing the functional quality of the action based on
            walking symmetry, balance, and metabolic cost.
        
        Properties
        ----------
        norm_delay : float
            Returns the normalized delay value used in error computations.
            
        action_error : float
            Overall error of the action that combines performance error and
            timing delay into a single value in the range [0, 1], where
            0 represents a perfect action and 1 the worst possible action.
        
        Methods
        -------
        __init__() -> None
            Initializes the action with a random functional performance and
            zero timing delay.
        set_timing_delay(delay: float = 0) -> None
            Sets and clips the timing delay to [0, 1] and clears any
            manually assigned action error.
        set_performance(**kwargs) -> None
            Updates the underlying `FunctionalPerformance` instance and clears
            any manually assigned action error.
        action_error(value: float) -> None
            Setter that allows manually specifying the overall action error in
            [0, 1]; this stored value is then returned by the `action_error`
            property.
        
    '''
    
    def __init__(self) -> None:
        # Initial random performance for the action
        self.performance = FunctionalPerformance.generate_random_performance()
        # The level of unpredictability of an action (aside from how good/bad the performance is)
        self.timing_delay: float = 0.0
        
    @property
    def norm_delay(self) -> float:
        '''
            Normalize delay to 0-1 range
        '''
        return self.timing_delay
        
    def set_timing_delay(self, delay=0) -> None:
        '''
            Adding a delay to the action (making the action unpredictable)
            If the delay is too much, the delay is clipped to less than a sec to reserve the effect of a delay on trust.
            (Preventing re-fit on the undelayed expected time)
            
        '''
        self.timing_delay = np.clip(delay, 0, 1)
        # Clear manual action_error setting when delay is updated
        if hasattr(self, '_manual_action_error'):
            delattr(self, '_manual_action_error')
        
    def set_performance(self, **kwargs):
        '''
            Setting Performance of the action to the desired values
        '''
        
        self.performance.update_performance(**kwargs)
        # Clear manual action_error setting when performance is updated
        if hasattr(self, '_manual_action_error'):
            delattr(self, '_manual_action_error')

    @property
    def action_error(self) -> float:
        # If manually set, return the stored value
        if hasattr(self, '_manual_action_error'):
            return self._manual_action_error
        
        performance_error = self.performance.performance_error
        # Calculate overall action quality (combines performance and timing)
        action_error = (performance_error + self.norm_delay + (performance_error * self.norm_delay)) / 3  # 0=perfect, 1=worst
        
        return action_error
    
    @action_error.setter
    def action_error(self, value: float) -> None:
        '''
            Manually set action error. This will automatically adjust
            the performance error and timing delay to achieve the desired error.
            Value should be between 0 (perfect) and 1 (worst).
        '''
        value = np.clip(value, 0.0, 1.0)
        self._manual_action_error = value

        
        
class FunctionalPerformance(BaseModel):
    '''
        Performance of an action of the robot.
        
        This class models how well a robot action supports the human user, based on
        biomechanical and energetic indicators.
        
        Attributes
        ----------
        walking_symmetry : int
            Symmetry Index (0–100). `0` represents perfect gait symmetry; higher
            values indicate increasing asymmetry between limbs.
        balance : float
            Balance / stability score (0–100). Lower values correspond to more
            stable and harmonic gait; higher values indicate greater instability
            or fall risk.
        metabolic_cost : float
            Percentage (0–100) of reduced energy consumption. Higher values
            represent better energetic assistance from the robot.
        
        Properties
        ----------
        performance_error : float
            Aggregate performance error in the range [0, 1], computed from
            `walking_symmetry`, `balance`, and `metabolic_cost` using
            `FEATURE_WEIGHTS`. Lower values indicate better overall performance.
        
        Methods
        -------
        update_performance(**kwargs) -> FunctionalPerformance
            Returns an updated instance with new performance values while
            enforcing validation and resetting any manually set performance
            error.
        generate_random_performance() -> FunctionalPerformance
            Create a random, but bounded, performance profile (useful for
            initialization).
        __list_features__() -> list
            Return the names of all exposed performance features.
        
        Notes
        -----
        The `performance_error` property can be set manually; when set, its
        value is stored and returned directly instead of being re-computed from
        the underlying features until those features are updated again.
    '''
    
    # https://share.google/aimode/EoTIzF1skNEHB46n6
    walking_symmetry : conint(ge=0, le=100) # Symmetry Index (SI): The most common method. 
        # 0% represents perfect symmetry.
        # Values above 0% indicate increasing asymmetry
        # SI = (XR - XL)/0.5(XR + XL)*100
        # Using absolute value for our case (since only the performance is important not the direction)
    balance: confloat(ge=0, le=100) # 0 represents perfect stability and values approaching 100 indicate high instability or fall risk
        # Based on "φ-bonacci index" (a quantitative biomechanical metric used to measure how closely a person's walking pattern aligns with a "harmonic" or ideal model based on the golden ratio (φ ≈ 1.618))
    metabolic_cost: confloat(ge=0, le=100) # percentage of reduced energy consumption
    
    # Prevent accidental out-of-range values during training
    class ConfigDict:
        validate_assignment = True
        
    @property
    def performance_error(self) -> float:
        '''
            Calculate performance error on demand
        '''
        # If manually set, return the stored value
        if hasattr(self, '_manual_performance_error'):
            return self._manual_performance_error
        return self._calculate_performance_error()
    
    @performance_error.setter
    def performance_error(self, value: float) -> None:
        '''
            Manually set performance error. This will automatically adjust
            the underlying performance metrics to achieve the desired error.
            Value should be between 0 (perfect) and 1 (worst).
        '''
        value = np.clip(value, 0.0, 1.0)
        self._manual_performance_error = value
        
        # Back-calculate performance metrics
        self.walking_symmetry = int(value * 100)
        self.balance = value * 100.0
        self.metabolic_cost = (1.0 - value) * 100.0
    
    def update_performance(self, **kwargs) -> FunctionalPerformance:
        '''
            Set new values for the action's performance
            (Change how an action affects the user)
        '''
        try:
            updated = self.model_copy(update=kwargs)
            self.__dict__.update(updated.__dict__)
            # Clear manual error setting when metrics are updated
            if hasattr(self, '_manual_performance_error'):
                delattr(self, '_manual_performance_error')
            logging.info("Performance updated.")
            
        except ValidationError:
            logging.error("Performance factor values out of range. Performance not updated.")
        
        return self
    
    def _calculate_performance_error(self) -> float:
        '''
            Performance error is sensed only after accumulation.
        '''
        # Normalize performance metrics to 0-1 scale (lower is better for errors)
        norm_symmetry = self.walking_symmetry / 100  # Higher values = worse performance
        norm_balance = self.balance / 100            # Higher values = worse performance
        norm_metabolic = 1 - (self.metabolic_cost / 100)  # Convert to error metric (higher = worse)
        performance_error = (
        FEATURE_WEIGHTS['walking_symmetry'] * norm_symmetry +
        FEATURE_WEIGHTS['balance'] * norm_balance +
        FEATURE_WEIGHTS['metabolic_cost'] * norm_metabolic
        )
        
        return performance_error
        
    @staticmethod
    def generate_random_performance():
        '''
            Define a random performance 
            (mostly used for initial action definition)
        '''
        
        random_performance = FunctionalPerformance(walking_symmetry=np.random.randint(0,100), 
                                                   balance=np.random.randint(0,100), 
                                                   metabolic_cost=np.random.randint(0,100))
        return random_performance
    
    def __list_features__(self) -> list:
        '''
        Return a list of all the performance features
        '''
        features = [attr for attr in vars(self) 
    if not attr.startswith('_') and not callable(getattr(self, attr))]
        
        return features
 
