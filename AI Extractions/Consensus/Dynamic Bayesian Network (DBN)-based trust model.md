A Dynamic Bayesian Network (DBN) is a probabilistic graphical model that represents sequences of variables and their temporal dependencies, allowing the modeling of how states evolve over time. **It extends Bayesian networks by incorporating time as a dimension, making it suitable for dynamic systems where variables change and influence each other across time steps.**

A DBN-based trust model applies this framework to represent and infer trust as a dynamic, evolving state influenced by observed behaviors and interactions. For example, in human-multi-robot teams, a DBN-based trust model uses robot performance as input to infer human trust states and predict human interventions, capturing how trust changes with ongoing experience (Mahani et al., 2020). 

In multi-agent systems, DBNs combine personalized criteria with multiple observations to evaluate the trustworthiness of agent groups dynamically, improving accuracy over static models (Nguyen & Bai, 2018). 

Other applications include dispersed computing environments where DBN-based models update comprehensive trust values by integrating historical and current interactions while filtering out malicious behavior (Hui et al., 2023).

Overall, DBN-based trust models provide a flexible probabilistic approach to continuously update and predict trust in complex, time-varying contexts (Mahani et al., 2020; Nguyen & Bai, 2018; Hui et al., 2023).

> [!NOTE] DBN vs. POMDP?
> While **DBNs** are excellent at _estimating_ a state (e.g., "how much does the user trust me?"), **POMDPs** (Partially Observable Markov Decision Processes) are gaining traction because they go a step further: they **decide what to do** about it.
> 
> 
[[CC-POMCP|see  **Cost-Constrained POMCP (CC-POMCP)**]]
## References

Mahani, M., Jiang, L., & Wang, Y. (2020). A Bayesian Trust Inference Model for Human-Multi-Robot Teams. _International Journal of Social Robotics_, 13, 1951 - 1965. [https://doi.org/10.1007/s12369-020-00705-1](https://doi.org/10.1007/s12369-020-00705-1)

Nguyen, T., & Bai, Q. (2018). A Dynamic Bayesian Network approach for agent group trust evaluation. _Comput. Hum. Behav._, 89, 237-245. [https://doi.org/10.1016/j.chb.2018.07.028](https://doi.org/10.1016/j.chb.2018.07.028)

Hui, H., Gong, Z., An, J., & Qi, J. (2023). A dynamic Bayesian-based comprehensive trust evaluation model for dispersed computing environment. _China Communications_, 20, 278-288. [https://doi.org/10.23919/jcc.2023.02.018](https://doi.org/10.23919/jcc.2023.02.018)