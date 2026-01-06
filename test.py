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
        
        
def test_action_set_performance():
    try:
        action = rb.Action()
        print(action.performance)
        action.set_performance(walking_symmetry=20, balance=1)
        print(action.performance.mean_performance())
        logging.info("Action performance set test successful \n --------")
    except:
        logging.error("Action performance set test failed \n --------")


if __name__=="__main__":
    test_plot_trait_observations_correlation_matrix()
    test_action_set_performance()
    test_update_performance_function()
    
    logging.info("All tests done.")