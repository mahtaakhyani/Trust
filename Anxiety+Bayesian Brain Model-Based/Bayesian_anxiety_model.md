# Bayesian Brain Theory: Anxiety as Precision-Weighting in Robotic Embodiment

## Introduction

In the Bayesian Brain framework, specifically within the Free Energy Principle and predictive processing accounts, anxiety can be conceptualized as the pathological over-weighting of sensory prediction errors [1,2]. This computational model provides a mechanistic explanation for why an anxious user of a robotic prosthetic or avatar cannot easily "ignore" minor kinematic irregularities (jitters, latency) that a calm user would naturally filter out through sensory attenuation [3,4].



---

## 1. The Bayesian Inference Framework

### 1.1 Core Formulation

The brain continuously estimates the state of an embodied agent (e.g., a robotic limb, $x$) by integrating two sources of information:

- **Prior belief** ($x_{\text{prior}}$): The internal generative model based on learned body schema
- **Sensory likelihood** ($x_{\text{sensory}}$): Current sensory observations (proprioceptive, visual, haptic)

Each information source is weighted by its **precision** ($\pi$), defined as the inverse of uncertainty (variance):

$$
\pi = \frac{1}{\sigma^2}
$$

The posterior estimate combines these sources according to their relative precision:

$$
x_{\text{posterior}} = \frac{\pi_{\text{prior}} \cdot x_{\text{prior}} + \pi_{\text{sensory}} \cdot x_{\text{sensory}}}{\pi_{\text{prior}} + \pi_{\text{sensory}}}
$$

This is the standard precision-weighted Bayesian fusion rule [5].

### 1.2 The Computational Role of Anxiety

Within predictive processing frameworks, anxiety is hypothesized to modulate the precision afforded to prediction errors—the mismatch between predicted and observed sensory signals [1,6]. Formally, we can model anxiety $A(t)$ as a gain parameter that amplifies sensory precision:

$$
\pi_{\text{sensory}}(t) = \pi_{\text{baseline}} \cdot [1 + \beta \cdot A(t)]
$$

Where:
- $\pi_{\text{baseline}}$: Baseline sensory precision in the absence of anxiety
- $\beta$: Sensitivity coefficient (individual difference parameter)
- $A(t)$: Time-varying anxiety level (derived from accumulated prediction errors or threat signals)

**Important caveat**: The parameters $\beta$ and $A(t)$ are theoretical constructs that capture computational principles. They are not directly observable neural quantities, though they may map onto neuromodulatory tone (see Section 3.2) [7,8].

---

## 2. Hyper-Reflexivity and Gamma Bias in Robotic Embodiment

### 2.1 Precision Escalation and Sensory Dominance

As anxiety increases ($A(t) \uparrow$), the brain assigns disproportionately high precision to sensory signals from the robotic system. In the Bayesian posterior equation, this forces the system to "trust" noisy, volatile sensory likelihoods more than stable internal priors [3,9].

**Mechanistic sequence**:

1. **Minor kinematic anomaly**: A small robotic jitter or latency creates a sensory prediction error ($\text{PE}$):
   $$
   \text{PE}(t) = x_{\text{sensory}}(t) - x_{\text{predicted}}(t)
   $$

2. **Precision amplification**: Because $\pi_{\text{sensory}}$ is elevated by anxiety, this $\text{PE}$ is weighted heavily in the posterior estimate, even if objectively small.

3. **Active inference response**: To minimize prediction error under high sensory precision, the brain issues corrective motor commands or attentional shifts [10].

### 2.2 Gamma Bias and Muscle Spindle Sensitivity

In biological motor control, **gamma bias** refers to the increased gain of muscle spindle afferents via gamma motor neuron activity [11]. In the context of robotic prosthetics or teleoperation, an analogous phenomenon occurs: heightened anxiety increases the sensitivity to proprioceptive-like feedback signals from the device.

Empirical observations suggest a **20-40% increase in stretch reflex sensitivity** during anxiety states, though this specific range requires further validation in robotic embodiment contexts [12]. This hyper-reflexivity manifests as:

- Exaggerated corrective movements in response to minor device perturbations
- Reduced tolerance for sensory noise or latency
- Disrupted sense of agency ("the robot feels less like 'me'") [13]

---

## 3. Dynamic Asymmetries in Precision

### 3.1 Learning-Rate Asymmetry and Precision Hysteresis

Standard Bayesian updating assumes symmetric learning rates: precision increases and decreases at comparable rates depending on prediction error magnitude. However, **anxiety dynamics exhibit precision hysteresis**: sensory precision increases rapidly following unexpected sensory input but decays slowly during stable, error-free periods [14,15].

Formally:

$$
\frac{d\pi_{\text{sensory}}}{dt}\Bigg|_{\text{prediction error}} \gg \left|\frac{d\pi_{\text{sensory}}}{dt}\right|\Bigg|_{\text{error-free}}
$$

This asymmetry explains the persistence of anxious states even after the robotic system resumes stable, predictable behavior—a phenomenon observed clinically and in human-robot interaction studies [16].

### 3.2 Mechanisms Supporting Asymmetric Precision Dynamics

Several neurobiologically plausible mechanisms can account for this asymmetry:

#### A. Biased Volatility Inference
Following a prediction error, the brain may infer that the environment (or the robot) has become more volatile. Under hierarchical Bayesian models like the Hierarchical Gaussian Filter (HGF), this inferred volatility maintains elevated sensory precision even during subsequent stable periods [17].

#### B. Neuromodulatory Hysteresis
Precision is neurally implemented via gain control mediated by:
- **Norepinephrine (NE)**: Signals unexpected uncertainty and arousal [8]
- **Acetylcholine (ACh)**: Signals expected uncertainty and promotes learning [8]

These neuromodulatory systems increase rapidly in response to threat or error but decay slowly, producing prolonged sensory amplification even after the triggering event has resolved [7,8].

#### C. Meta-Prior on Safety
Safety expectations operate as higher-order priors in a hierarchical generative model. These meta-priors update more slowly than sensorimotor priors, delaying the re-establishment of trust in the robotic system [18,19].

#### D. Asymmetric Cost Function
From an evolutionary perspective, the cost of false negatives (failing to detect a genuine threat) far exceeds the cost of false positives (over-reacting to a benign event). This asymmetry rationally biases the system toward maintaining elevated vigilance [20].

### 3.3 Interpretation of Extended Recovery Periods

In experimental and clinical contexts, a **washout period** (e.g., 60-90 minutes) is often required before anxious participants return to baseline sensory integration patterns [16,21]. In Bayesian terms, this reflects:

- Slow decay of elevated sensory precision ($\pi_{\text{sensory}}$)
- Gradual reinstatement of the prior belief in bodily control ($\pi_{\text{prior}}$)
- Persistent inference of environmental volatility

This is **not** due to continued sensory prediction errors, but rather to the sluggish dynamics of higher-level inference about safety and controllability [17,18].

---

## 4. Summary Table: Bayesian Parameters of Anxiety

| **Parameter**                          | **Healthy State**                     | **Anxious State** ($A(t) \gg 0$)       |
|----------------------------------------|---------------------------------------|----------------------------------------|
| Sensory Precision ($\pi_{\text{sensory}}$) | Moderate (Filtered)                  | High (Amplified)                       |
| Prior Precision ($\pi_{\text{prior}}$)     | High (Stable Body Schema)            | Low (Fragile Sense of Embodiment)      |
| Prediction Error Sensitivity           | Low (Errors attenuated)              | High (Hyper-vigilant)                  |
| Causal Inference                       | "The robot is part of me"            | "The robot is an external, unpredictable object" |
| Volatility Estimate ($\sigma_{\text{vol}}$) | Low                                  | High (Environment perceived as unstable) |
| Learning Rate (Precision Update)       | Symmetric                            | Asymmetric (Fast ↑, Slow ↓)            |

---

## 5. References

[1] Feldman, H., & Friston, K. J. (2010). Attention, uncertainty, and free-energy. *Frontiers in Human Neuroscience*, *4*, 215. https://doi.org/10.3389/fnhum.2010.00215

[2] Clark, A. (2013). Whatever next? Predictive brains, situated agents, and the future of cognitive science. *Behavioral and Brain Sciences*, *36*(3), 181-204. https://doi.org/10.1017/S0140525X12000477

[3] Edwards, M. J., Adams, R. A., Brown, H., Pareés, I., & Friston, K. J. (2012). A Bayesian account of 'hysteria'. *Brain*, *135*(11), 3495-3512. https://doi.org/10.1093/brain/aws129

[4] Brown, H., Adams, R. A., Parees, I., Edwards, M., & Friston, K. (2013). Active inference, sensory attenuation and illusions. *Cognitive Processing*, *14*(4), 411-427. https://doi.org/10.1007/s10339-013-0571-3

[5] Knill, D. C., & Pouget, A. (2004). The Bayesian brain: The role of uncertainty in neural coding and computation. *Trends in Neurosciences*, *27*(12), 712-719. https://doi.org/10.1016/j.tins.2004.10.007

[6] Paulus, M. P., & Stein, M. B. (2006). An insular view of anxiety. *Biological Psychiatry*, *60*(4), 383-387. https://doi.org/10.1016/j.biopsych.2006.03.042

[7] Yu, A. J., & Dayan, P. (2005). Uncertainty, neuromodulation, and attention. *Neuron*, *46*(4), 681-692. https://doi.org/10.1016/j.neuron.2005.04.026

[8] Dayan, P., & Yu, A. J. (2006). Phasic norepinephrine: A neural interrupt signal for unexpected events. *Network: Computation in Neural Systems*, *17*(4), 335-350. https://doi.org/10.1080/09548980601004024

[9] Friston, K. J., Stephan, K. E., Montague, R., & Dolan, R. J. (2014). Computational psychiatry: The brain as a phantastic organ. *The Lancet Psychiatry*, *1*(2), 148-158. https://doi.org/10.1016/S2215-0366(14)70275-5

[10] Friston, K. J., Daunizeau, J., Kilner, J., & Kiebel, S. J. (2010). Action and behavior: A free-energy formulation. *Biological Cybernetics*, *102*(3), 227-260. https://doi.org/10.1007/s00422-010-0364-z

[11] Prochazka, A., Clarac, F., Loeb, G. E., Rothwell, J. C., & Wolpaw, J. R. (2000). What do reflex and voluntary mean? Modern views on an ancient debate. *Experimental Brain Research*, *130*(4), 417-432. https://doi.org/10.1007/s002210050045

[12] Davis, M., Walker, D. L., Miles, L., & Grillon, C. (2010). Phasic vs sustained fear in rats and humans: Role of the extended amygdala in fear vs anxiety. *Neuropsychopharmacology*, *35*(1), 105-135. https://doi.org/10.1038/npp.2009.109

[13] Tsakiris, M., Hesse, M. D., Boy, C., Haggard, P., & Fink, G. R. (2007). Neural signatures of body ownership: A sensory network for bodily self-consciousness. *Cerebral Cortex*, *17*(10), 2235-2244. https://doi.org/10.1093/cercor/bhl131

[14] Browning, M., Behrens, T. E., Jocham, G., O'Reilly, J. X., & Bishop, S. J. (2015). Anxious individuals have difficulty learning the causal statistics of aversive environments. *Nature Neuroscience*, *18*(4), 590-596. https://doi.org/10.1038/nn.3961

[15] Aylward, J., Valton, V., Ahn, W. Y., Bond, R. L., Dayan, P., Roiser, J. P., & Robinson, O. J. (2019). Altered learning under uncertainty in unmedicated mood and anxiety disorders. *Nature Human Behaviour*, *3*(10), 1116-1123. https://doi.org/10.1038/s41562-019-0628-0

[16] Grillon, C. (2002). Startle reactivity and anxiety disorders: Aversive conditioning, context, and neurobiology. *Biological Psychiatry*, *52*(10), 958-975. https://doi.org/10.1016/S0006-3223(02)01665-7

[17] Mathys, C., Daunizeau, J., Friston, K. J., & Stephan, K. E. (2011). A Bayesian foundation for individual learning under uncertainty. *Frontiers in Human Neuroscience*, *5*, 39. https://doi.org/10.3389/fnhum.2011.00039

[18] Lonsdorf, T. B., Menz, M. M., Andreatta, M., Fullana, M. A., Golkar, A., Haaker, J., ... & Merz, C. J. (2017). Don't fear 'fear conditioning': Methodological considerations for the design and analysis of studies on human fear acquisition, extinction, and return of fear. *Neuroscience & Biobehavioral Reviews*, *77*, 247-285. https://doi.org/10.1016/j.neubiorev.2017.02.026

[19] Dunsmoor, J. E., Niv, Y., Daw, N., & Phelps, E. A. (2015). Rethinking extinction. *Neuron*, *88*(1), 47-63. https://doi.org/10.1016/j.neuron.2015.09.028

[20] Bach, D. R., & Dolan, R. J. (2012). Knowing how much you don't know: A neural organization of uncertainty estimates. *Nature Reviews Neuroscience*, *13*(8), 572-586. https://doi.org/10.1038/nrn3289

[21] Grillon, C., Baas, J. P., Lissek, S., Smith, K., & Milstein, J. (2004). Anxious responses to predictable and unpredictable aversive events. *Behavioral Neuroscience*, *118*(5), 916-924. https://doi.org/10.1037/0735-7044.118.5.916
