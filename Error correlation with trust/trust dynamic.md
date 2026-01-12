# Trust Dynamics in Physical Human-Robot Interaction (pHRI)

In physical human-robot interaction (pHRI), the correlation between perceived error and user trust is **not strictly linear**. While initial trust often scales with perceived reliability, the relationship is dynamic and evolves non-linearly over time, influenced by the timing of errors and user expectations.

---

## 1. Dynamics of the Relationship

- **Non-Linear Decay**  
  Trust is highly sensitive to early interactions. Errors occurring at the beginning of an interaction have a disproportionately large negative impact on trust compared to errors occurring after a period of stable performance.

- **Trust Recovery**  
  The relationship is asymmetrical; trust is *easy to lose and difficult to gain*. Recovery following an error often requires more stable cycles than the single error that caused the drop, and the rate of recovery can depend on the user's initial framing of the robot's functionality.

- **Age as a Moderator**  
  For older adults, trust can be more resilient to performance errors because they often evaluate robots based on non-performance factors (e.g., social cues or perceived helpfulness) rather than strictly tracking mechanical errors.

---

## 2. Mathematical Modeling of Trust

Mathematical frameworks typically model trust (\(T\)) as a **dynamic state value**, often bounded between \(0\) (complete distrust) and \(1\) (complete trust).

### A. Three-Layered Model
A widely used framework (2026 update) models trust as a sum of three components:


$$T(t) = T_{dispositional} + T_{situational}(t) + T_{learned}(t)$$



- \(T_{dispositional}\): A constant representing the user's baseline tendency to trust technology.  
- \(T_{situational}\): Contextual variables such as task risk and environmental uncertainty.  
- \(T_{learned}\): The dynamic component that updates based on experience.

---

### B. Dynamic Update Rule
Learned trust is often updated iteratively using a performance-based feedback loop:

$$T_{t+1} = T_{t} + \alpha (P_{t} - E_{t})$$

Where:  
- \(T_{t+1}\): Updated trust level  
- \(\alpha\): A learning rate (often asymmetrical, higher for errors than for successes)  
- \(P_{t}\): Actual performance (1 for success, 0 for error)  
- \(E_{t}\): Expected performance  

---

### C. Probabilistic Models
Advanced models like **OPTIMo** use Bayesian estimation to calculate trust based on failure rates (\(f\)) and task interventions (\(i\)):

$$T \approx P(\text{Success} \mid f, i, \text{Performance History})
$$

This approach accounts for the ambiguity and risk inherent in pHRI.

---

## References
- Ahmad, M. I., & Robinson, S. (2026). *Modelling Human Trust in Robots During Repeated Interactions*  
- Washburn, A., Adeleye, A., An, T., & Riek, L. D. (2025). *Robot Errors in Proximate HRI: Framing Affects Perceived Reliability and Trust*  
- Wald, S., Puthuveetil, K., & Erickson, Z. (2024). *Do Mistakes Matter? Comparing Trust Responses of Different Age Groups*  
- Rezaei Khavas, Z., Ahmadzadeh, R., & Robinette, P. (2020). *Modeling Trust in Human-Robot Interaction: A Survey*

