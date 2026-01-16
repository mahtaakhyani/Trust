# Bayesian Brain Theory: Anxiety as Precision-Weighting

In the Bayesian Brain framework (specifically the **Free Energy Principle**), anxiety is defined as the **over-weighting of sensory prediction errors**. This model explains why an anxious user cannot *ignore* minor robotic jitters that a calm user would naturally filter out.

---

## 1. The Bayesian Inference Framework

The brain estimates the state of the robot (x) by combining a **Prior** (internal model) and a **Likelihood** (sensory data). Each is weighted by its **Precision** (\pi), defined as the inverse of uncertainty:

[
\pi = \frac{1}{\sigma^2}
]

[
x_{\text{posterior}} =
\frac{\pi_{\text{prior}} \cdot x_{\text{prior}} + \pi_{\text{sensory}} \cdot x_{\text{sensory}}}
{\pi_{\text{prior}} + \pi_{\text{sensory}}}
]

---

### The Role of Anxiety (A(t))

In this model, **anxiety acts as a multiplier on the precision of sensory prediction errors** (\pi_{\text{sensory}}):

[
\pi_{\text{sensory}}(t) =
\pi_{\text{baseline}} \cdot \left[1 + \beta \cdot A(t)\right]
]

Where:

* (\beta) — sensitivity coefficient
* (A(t)) — anxiety value from the Anxiety Accumulation Formula

---

## 2. Hyper-Reflexivity and Gamma Bias

As (A(t)) increases, the brain assigns **high precision** to the robot’s sensory signals. Mathematically, this forces the brain to *trust noisy likelihoods more than its own stable prior*.

**Process breakdown:**

1. **Prediction Error Spike**
   A small robot jerk creates a prediction error ((PE)).

2. **Precision Scaling**
   Because the user is anxious, the brain weights this (PE) extremely heavily.

3. **Haptic Hyper-reflexivity**
   The brain demands an immediate motor correction.
   This manifests as the **20–40% increase in stretch-signal sensitivity (Gamma Bias)** discussed previously.

---

## 3. Trust as “Model Evidence”

In Bayesian terms, **trust** is the degree to which the brain’s internal model successfully predicts the robot’s behavior.

* **Trusting state**

  * Low prediction error
  * High prior precision
  * The robot is *part of the self*

* **Anxious / Distrusting state**

  * High prediction error
  * High sensory precision
  * The robot is an *external threat* that must be monitored

---

### The “90-Minute Washout” in Bayesian Terms

During the 90-minute recovery window, the brain’s **uncertainty estimate remains high**. Even if the robot performs perfectly, the brain’s **learning rate** is biased toward expecting another error. This prevents re-establishing a high-precision *safety prior*.

---

## 4. Scientific Origins & Citations

* **Feldman, H., & Friston, K. J. (2010)**
  *Attention, uncertainty, and free-energy.*
  *Frontiers in Human Neuroscience.*
  **Origin:** Defines attention (and by extension anxiety) as optimization of synaptic gain (precision).

* **Edwards, M. J., et al. (2012)**
  *A Bayesian account of “hysteria” and functional sensorimotor symptoms.*
  *Brain.*
  **Origin:** Models how over-precision on sensory input produces hyper-sensitivity and abnormal motor responses.

* **Friston, K. J., et al. (2014)**
  *The computational anatomy of psychosis.*
  *Frontiers in Psychiatry.*
  **Origin:** Describes Bayesian phase transitions where excessive error precision collapses prior models (trust).

* **Powers, A. R., et al. (2017)**
  *Pavlovian conditioning–induced hallucinations and abnormal perception.*
  *Science.*
  **Origin:** Demonstrates how priors and likelihoods are reweighted under volatility and uncertainty.

---

## 5. Summary Table: Bayesian Parameters of Anxiety

| Parameter                    | Healthy State             | Anxious State (A(t) \gg 0)        |
| ---------------------------- | ------------------------- | --------------------------------- |
| Sensory Precision (\pi_s)    | Moderate (filtered)       | High (amplified)                  |
| Prior Precision (\pi_p)      | High (stable body schema) | Low (fragile identity)            |
| Prediction Error Sensitivity | Low                       | High (hyper-vigilant)             |
| Causal Inference             | “The robot is me.”        | “The robot is an external force.” |
