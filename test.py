import human as hm
import robot as rb
import logging

# Configure logging 
logging.basicConfig(level=logging.DEBUG)

# ---- Human ----
def test_plot_trait_observations_correlation_matrix():
    try:
        human = hm.Human()
        human.plot_trait_observations_correlation_matrix()
        logging.info("Plotting trait vs observation correlation matrix successful \n --------")
        
    except:
        logging.error("Plotting trait vs observation correlation matrix failed. \n --------")


# ---- Robot ---- 
def test_update_performance_function():
    try: 
        FP = rb.FunctionalPerformance(walking_symmetry=50, balance=0.5, metabolic_cost=30)
        FP.update_performance(walking_symmetry=270, balance=1)
        print(FP.walking_symmetry, FP.balance, FP.metabolic_cost)
        logging.info("Performance update test successful \n --------")
    except:
        logging.error("Performance update test failed \n --------")
        
        
def test_set_action():
    try:
        action = rb.Action()
        action.set_performance(walking_symmetry=20, balance=1)
        print(f'Action Performance: {action.performance}')
        print(f'Performance Error: {action.performance.performance_error:4f}')
        action.set_timing_delay(delay=0.2)
        print(f'Action Error with {action.timing_delay} delay: {action.action_error:4f}')
        print("------- \n Setting action performance error to 0 (Perfect) \n --------")
        action.performance.performance_error = 0
        action.set_timing_delay(delay=0) # minimum delay possible
        print(f'Performance Error: {action.performance.performance_error:4f}')
        action.set_timing_delay(delay=0.2)
        print(f'Action Error with {action.timing_delay} delay: {action.action_error:4f}')
        action.set_timing_delay(delay=0.7)
        print(f'Action Error with {action.timing_delay} delay: {action.action_error:4f}')
        action.set_timing_delay(delay=1.0) # maximum delay possible
        print(f'Action Error with {action.timing_delay} delay: {action.action_error:4f}')
        print((action.performance.__list_features__()))
        logging.info("Action set test successful \n --------")
    except Exception as e:
        logging.error(f"Action performance set test failed with error \n {e} \n --------")


if __name__=="__main__":
    # test_plot_trait_observations_correlation_matrix()
    test_set_action()
    # test_update_performance_function()
    logging.info("All tests done.")