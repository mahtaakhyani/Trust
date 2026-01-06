from pydantic import BaseModel, ValidationError, confloat, conint
import numpy as np
import logging

# Configure logging 
logging.basicConfig(level=logging.DEBUG)

class Action:
    '''
        The action of the robot with its properties and factors.
        The features of an action includes: 
            - timing delay: how the robot does its action on a WRONG TIMING (makes unpredictability)
            - performance: how GOOD the robot does its job (relates to ability/usability)
    '''
    
    def __init__(self) -> None:
        self.performance = FunctionalPerformance.generate_random_performance()
        self.timing_delay: int # the level of unpredictability of an action (aside from the performance - or how good/bad was the action)
        
    def set_timing_delay(self, delay=0) -> None:
        '''
            Adding a delay to the action (making the action unpredictable)
            If the delay is too much, the delay is clipped to less than a sec to reserve the effect of a delay on trust.
            (Preventing re-fit on the undelayed expected time)
            
        '''
        self.timing_delay = np.clip(delay, 0, 1)
        
    def set_performance(self, **kwargs):
        '''
            Setting Performance of the action to the desired values
        '''
        
        self.performance = self.performance.update_performance(**kwargs)


        
        
class FunctionalPerformance(BaseModel):
    '''
        Performance of an action of the robot
        
        Performance is defined based on these factors:
            - walking symmetry: It calculates the difference between the two limbs as a percentage of their average.
            - balance: Assess balance by evaluating the consistency, symmetry, and self-similarity of a user's gait
            - metabolic_cost: how much the robot can reduce the energy a person consumes during walking or running
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
        
        
    def mean_performance(self):
        '''
            Return an overall value of performance
            (The average of all the factors of performance)
        '''
        return np.mean([self.walking_symmetry, self.balance, self.metabolic_cost])
    
    def update_performance(self, **kwargs): 
        '''
            Set new values for the action's performance
            (Change how an action affects the user)
        '''
        try:
            updated = self.model_copy(update=kwargs)
            self.__dict__.update(updated.__dict__)
            logging.info("Performance updated.")
            
        except ValidationError:
            logging.error("Performance factor values out of range. Performance not updated.")
        
        return self
        
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
 
 
