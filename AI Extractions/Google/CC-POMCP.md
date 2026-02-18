We have:
1. POMDP
2. CPOMDP (Constrained POMDP)
3. POMCP (Partially Observable Monte Carlo Planning)

Current research actually combines them into **Cost-Constrained POMCP (CC-POMCP)**. It uses the **speed** of POMCP's simulations to solve the **safety** requirements of a CPOMDP. This is the "gold standard" for real-time human-robot trust. [1]


While **CC-POMCP** is a high-performance algorithm in the broader field of AI planning, its direct application to **Trust in Human-Robot Interaction (HRI)** is currently rare in published literature. Instead, most pioneering "Trust-Aware" research relies on standard **Trust-POMDP** frameworks.
In these models:
- **The Objective** is usually a single weighted reward function: 
	$R = TaskPerformance +  \omega .Trust$`
- **Trust Calibration** is the goal, where the robot might intentionally fail or choose low-risk tasks to manage human expectations.

## Why not used in HRI trust papers a lot?

1. *CC-POMCP requires a strict cost limit* (e.g., "Cost must be <10"). In HRI, it is psychologically difficult to define a hard numerical "red line" for trust.
2. *CC-POMCP relies on a "black-box simulator" of the environment.* While we can simulate robot physics easily, simulating **human psychological trust** accurately enough for thousands of Monte Carlo rollouts is still an active area of research.
3. *Many current trust experiments involve relatively simple tasks (like table-clearing or object-carrying)*. Standard POMDP solvers are sufficient for these "small-scale" state spaces, so the heavy computational power of CC-POMCP isn't yet a necessity.

## Where the Field is Moving

The transition toward **Constrained** models is beginning in **Safety-Critical HRI** (e.g., medical robotics or autonomous driving), where "Safety" is the hard constraint and "Trust" is the secondary reward. 

As HRI moves from simple lab tasks to complex, long-term deployments, **algorithms like CC-POMCP will likely become the standard for preventing "trust-breaking" actions while optimizing efficiency.**
[2]

> [!NOTE] Idea
> The "red line" in the anxiety research can definitely be the "threat" cues. Any error that has the potential to be interpreted as a threat, should be the red line - at least at first in in the interaction. The foundation is important.
> #idea


# Code-like logic example of how a CC-POMCP makes a decision [3]

In a **CC-POMCP** (Cost-Constrained POMCP) framework, the robot uses a **Lagrangian** multiplier ($\gamma$ ) to balance rewards (task speed) against costs (trust violation).
Instead of a single "score," the robot maintains two separate values for every action: Q_R (expected reward) and Q_C (expected cost).

The core logic follows an "interleaved" optimization: it searches for the best actions using **Monte Carlo Tree Search (MCTS)** and simultaneously updates how "strict" it should be about trust.

```python
# CC-POMCP Main Decision Loop
def get_best_action(current_belief):
    # 1. Update the 'strictness' parameter (Lagrangian Multiplier lambda)
    # If past simulations showed trust violation > threshold, increase lambda
    lambda_multiplier = update_lagrangian(current_belief, threshold=0.4)

    for simulation in range(NUM_SIMULATIONS):
        # 2. Monte Carlo Tree Search (MCTS)
        # Select actions that maximize: Reward - (lambda * Cost)
        simulate_future_trajectories(current_belief, lambda_multiplier)

    # 3. Final Selection
    # Pick the action that maximizes the combined 'Lagrangian' value
    return argmax(Q_reward(action) - lambda_multiplier * Q_cost(action))

# The Robot's "Inner Thoughts" during MCTS Simulation:
def simulate_step(state, action):
    # What happens if I move fast?
    new_state, reward, cost = simulator.step(state, action)
    
    # Reward is high (Task completion), but Cost is also high (Human trust drops)
    # The solver balances these based on the current 'strictness' (lambda)
    return reward, cost


```


Key Equations in the Tree

The robot selects actions within the search tree using a modified **UCB1** rule:  

![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)

- $\gamma$ → 0 : The robot ignores trust and rushes the task.
- $\gamma$ → $\infty$ The robot becomes paralyzed by fear of losing trust and never acts.
- **Dual Ascent:** CC-POMCP automatically finds the "just right" 
 to stay safe while being as fast as possible.
     
#models/ccpomdp #models/pomdp #models/cpomdp #models/pomcp
# References
[1](https://share.google/aimode/5Rd2qoBBrNoFc7b85)
[2](https://share.google/aimode/prcWtSdVddH0QZ3HS)
[3](https://share.google/aimode/XH07JvNCemagx3qFu)