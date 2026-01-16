# Mathematical Model: Anxiety Accumulation in Human-Robot Interaction

## Abstract

This document proposes a formal computational framework for modeling **anxiety accumulation** in human-robot interaction (HRI), with specific application to wearable robotics and prosthetic systems. While existing literature addresses stress models in biology and trust models in HRI separately, we synthesize neurobiological (allostatic load), psychological (negativity bias), and computational (Bayesian inference) principles into a unified predictive model. The proposed framework aims to explain the compounding effect of robot errors on user anxiety and provides a foundation for adaptive robot control systems that account for user affective state.

**Keywords**: Human-robot interaction, anxiety modeling, allostatic load, trust dynamics, wearable robotics, computational psychiatry

---

## 1. The Anxiety Accumulation Formula

### 1.1 Core Formulation

In a dynamic HRI environment, we model the user's anxiety level at time $t$ as a cumulative function of past aversive events, each weighted by severity and decaying exponentially over time:

$$
A(t) = A_{\text{baseline}} + \sum_{i=1}^{n} w_i \cdot E_i \cdot e^{-\lambda(t - t_i)}
$$

Where each component represents a distinct psychological or physiological process validated in prior literature.

### 1.2 Parameter Definitions and Empirical Grounding

| Parameter | Definition | Empirical Basis | Impact on Wearable Robotics |
|-----------|------------|-----------------|------------------------------|
| $A(t)$ | **Instantaneous anxiety** at time $t$ | State anxiety (STAI-S) [1] | Determines real-time trust and safety perception |
| $A_{\text{baseline}}$ | **Trait anxiety** (individual resting state) | Trait anxiety (STAI-T) [1]; HRV baseline [2] | Higher baseline predicts faster trust decay [3] |
| $E_i$ | **Event magnitude** (severity of error $i$) | Subjective threat rating; kinematic deviation [4] | Larger errors (e.g., 15° overshoot) produce stronger responses |
| $w_i$ | **Negativity weight** (loss aversion factor) | Prospect theory [5]; negativity bias [6] | Failures weighted ~2× more than successes [5] |
| $\lambda$ | **Decay constant** (recovery rate) | Cortisol decay kinetics [7]; HRV recovery [2] | Smaller $\lambda$ → prolonged anxiety (slower washout) |
| $t - t_i$ | **Temporal gap** since event $i$ | Time elapsed in seconds/minutes | Events within decay window compound non-linearly |
| $n$ | **Number of accumulated events** | Count of errors within memory window | More events → higher cumulative load [8] |

**Key assumptions:**
1. Events are **independent** in magnitude but **dependent** in timing (compounding effect)
2. Decay follows **first-order kinetics** (exponential), consistent with stress hormone dynamics [7]
3. The model operates on a timescale of **minutes to hours**, not milliseconds (not suitable for startle responses)

---

## 2. Theoretical Foundations

### 2.1 The Leaky Integrator Model (Temporal Decay)

The exponential decay term $e^{-\lambda(t - t_i)}$ originates from **leaky integrator** models in computational neuroscience and decision theory [9,10].

**Neurobiological interpretation:**
- Represents the time course of stress hormone clearance (cortisol half-life ~60-90 min [7])
- Models the decay of sympathetic nervous system activation (heart rate, skin conductance recovery [2])
- Captures the "washout period" observed in psychophysiological experiments [11]

**Mathematical properties:**
- At $t = t_i$: full impact ($e^0 = 1$)
- At $t = t_i + \frac{1}{\lambda}$: 37% of original impact remains
- At $t = t_i + \frac{3}{\lambda}$: ~5% remains (practical washout threshold)

**Empirical calibration:**
For typical stress responses, $\lambda \approx 0.01$ to $0.02 \text{ min}^{-1}$, corresponding to decay half-lives of 30-70 minutes [7,11].

### 2.2 Allostatic Load (Cumulative Stress)

The summation operator ($\sum_{i=1}^{n}$) implements the principle of **allostatic load** [8]: the cumulative physiological cost of repeated adaptation to stressors.

**Key principle**: Stressors that occur before previous stressors have fully resolved produce **non-linear** increases in total load:

$$
A(t_2) > A(t_1) + E_2 \quad \text{if } t_2 - t_1 < \frac{3}{\lambda}
$$

This "compounding effect" explains why a second robot error occurring within the decay window (e.g., 60 min) is experienced as more severe than the same error in isolation.

**Empirical support:**
- Repeated stressors produce elevated cortisol responses compared to single stressors [8,12]
- Cumulative daily stress predicts HRV suppression better than single-event stress [13]
- In HRI, rapid successive failures produce steeper trust decline than temporally separated failures [14]

### 2.3 Negativity Bias (Asymmetric Weighting)

The parameter $w_i$ implements **loss aversion** from prospect theory [5] and **negativity bias** from affective neuroscience [6].

**Core finding**: Negative events (losses, threats, errors) have approximately **twice the psychological impact** of equivalent positive events (gains, safety signals, successes) [5,15].

**Model implementation:**
- For robot **errors**: $w_{\text{error}} \approx 2.0$ to $3.0$
- For robot **successes**: $w_{\text{success}} \approx 0.5$ to $1.0$
- For **neutral** events: $w_{\text{neutral}} = 0$

**Neural basis**: 
- Amygdala responses to negative stimuli are faster and stronger than to positive stimuli [16]
- Loss-related activations in anterior insula exceed gain-related activations [17]

**HRI implications**: A single robot failure may require **multiple** successful interactions to restore baseline trust—a phenomenon observed empirically [3,14].

### 2.4 Bayesian Trust Dynamics

Trust ($T$) in the robot is inversely related to the **perceived volatility** (variance) of its performance [18,19]:

$$
T(t) \propto \frac{1}{1 + \sigma^2_{\text{performance}}(t)}
$$

Where performance variance is estimated over a sliding temporal window:

$$
\sigma^2_{\text{performance}}(t) = \int_{t - \tau}^{t} \left[ \text{Actual}(s) - \text{Expected}(s) \right]^2 ds
$$

**Key insight**: Trust collapses non-linearly when multiple errors ($E_i$) occur within the integration window $\tau$ [18].

**Connection to anxiety**: High $A(t)$ increases the **precision** (inverse variance) assigned to prediction errors, making the user hyper-sensitive to small deviations [20,21].

---

## 3. Individual Differences: Resilience and Vulnerability

### 3.1 The Precision-Weighting Framework

Individual differences in anxiety response are formalized in computational psychiatry as differences in **prior precision** ($\pi$) and **learning rates** ($\alpha$) [20,21,22].

| Cognitive Parameter | High Trait Anxiety / Low Resilience | Low Trait Anxiety / High Resilience |
|---------------------|--------------------------------------|--------------------------------------|
| **Learning rate** ($\alpha$) for negative events | High (~0.7-0.9): Single error drastically shifts beliefs | Low (~0.2-0.4): Multiple errors needed to update priors |
| **Decay constant** ($\lambda$) | Small (~0.008 min⁻¹): 90+ min recovery | Large (~0.02 min⁻¹): 30-50 min recovery |
| **Prior precision** ($\pi_{\text{threat}}$) | High: Expect things to go wrong | Low: Expect stability |
| **Negativity weight** ($w$) | Large (~2.5-3.0): Amplified threat response | Moderate (~1.5-2.0): Balanced response |
| **Baseline anxiety** ($A_{\text{baseline}}$) | Elevated (STAI-T > 45) [1] | Low (STAI-T < 35) [1] |

**Neurobiological correlates:**
- High trait anxiety → reduced prefrontal cortex inhibition of amygdala [23]
- Low resilience → blunted HRV and prolonged cortisol elevation [2,13]
- Anxiety disorders → impaired safety learning (extinction deficits) [24,25]

### 3.2 Developmental and Age-Related Differences

**Youth (adolescents, 12-18 years):**
- **Higher learning rate** ($\alpha$): More plastic trust models; rapid adaptation but also rapid trust loss [26]
- **Lower baseline anxiety** ($A_{\text{baseline}}$): On average, unless clinical anxiety is present [1]
- **Faster decay** ($\lambda$): Shorter physiological memory of stressors [27]

**Young adults (20-35 years):**
- **More stable priors**: Less affected by single errors but slower to re-learn trust once broken [28]
- **Intermediate decay rates**: Cortisol recovery ~60-90 min [7]

**Older adults (>60 years):**
- **Reduced learning rates**: More reliance on established priors [29]
- **Slower decay** (in some individuals): Prolonged stress responses [30]

**Important caveat**: These are population-level trends with substantial individual variation. Personalized calibration of model parameters is essential for real-world HRI systems [31].

---

## 4. Mechanisms of Threat History Effects

### 4.1 Sensitization and Fear Generalization

Repeated exposure to unpredictable robot errors produces two maladaptive changes:

**A. Sensitization** [32,33]:
- **Definition**: Increased responsivity to a stimulus following repeated exposure
- **Neural mechanism**: Long-term potentiation (LTP) in lateral amygdala strengthens threat pathways [32]
- **Behavioral outcome**: Lower threshold for anxiety response to subsequent errors

**B. Fear Generalization** [34,35]:
- **Definition**: Extension of threat response to stimuli that resemble, but are not identical to, the original threat
- **Neural mechanism**: Reduced hippocampal pattern separation; overgeneralized amygdala activation [34]
- **HRI outcome**: User becomes anxious about robot behaviors that are objectively safe but perceptually similar to past errors

### 4.2 Safety Signal Blunting

A history of unpredictable threats impairs the **ventromedial prefrontal cortex (vmPFC)**, the brain region responsible for signaling safety and inhibiting amygdala responses [24,36].

**Consequence**: Even when the robot performs flawlessly, the user's brain struggles to "believe" in safety.

**Formal model**: Safety signal efficacy decays as a function of threat history:

$$
S_{\text{efficacy}}(t) = S_{\text{max}} \cdot e^{-\gamma \cdot \sum_{i=1}^{n} E_i}
$$

Where $\gamma$ is the **safety-erosion coefficient** (higher in individuals with trauma history or anxiety disorders) [24,37].

**Clinical relevance**: This mechanism underlies the observation that individuals with PTSD or panic disorder show impaired fear extinction and persistent hypervigilance [24,36].

---

## 5. Physiological Validation: Neuroception and HRV

### 5.1 Neuroception: Subconscious Threat Detection

**Neuroception** [38] refers to the autonomic nervous system's rapid, pre-conscious evaluation of safety vs. threat, mediated by:
- Amygdala (threat detection)
- Ventral vagal complex (social engagement, safety)
- Dorsal vagal complex (shutdown, freeze)

**Model correspondence**: $A(t)$ can be interpreted as the output of the neuroceptive system, determining which autonomic state is activated [38].

### 5.2 Heart Rate Variability as an Objective Index

**Heart rate variability (HRV)**, specifically high-frequency HRV (HF-HRV, 0.15-0.4 Hz), reflects parasympathetic (vagal) tone and is the gold-standard physiological index of stress regulation [2,13].

**Empirical relationship**:
$$
\text{HRV}(t) \propto \frac{1}{1 + A(t)}
$$

**Key findings:**
- High $A(t)$ → Low HRV → Reduced capacity for flexible social engagement [2]
- HRV predicts trust in automation better than self-report measures [39]
- HRV recovery time correlates with $\lambda$ (decay constant) [13]

**Practical application**: Real-time HRV monitoring can provide continuous estimates of $A(t)$, enabling adaptive robot behavior [40].

---

## 6. Model Limitations and Future Directions

### 6.1 Current Limitations

1. **Lack of direct empirical validation**: The specific functional form (exponential decay summation) has not been tested against real HRI data
2. **Simplified error representation**: $E_i$ is treated as a scalar, but errors have multidimensional features (timing, predictability, controllability)
3. **Linear summation assumption**: May not capture non-linear interactions between error types
4. **Static parameters**: $\lambda$, $w$, and $A_{\text{baseline}}$ likely vary dynamically with context and learning
5. **No explicit safety signal term**: The model currently only accumulates negative events

### 6.2 Recommended Extensions

1. **Empirical calibration**: Fit model to longitudinal HRI data with concurrent HRV/cortisol measurements
2. **Add safety signal term**: 
   $$A(t) = A_{\text{baseline}} + \sum_{i=1}^{n} w_i \cdot E_i \cdot e^{-\lambda(t - t_i)} - \sum_{j=1}^{m} w_j^+ \cdot S_j \cdot e^{-\lambda^+(t - t_j)}$$
3. **Hierarchical Bayesian implementation**: Estimate individual-level parameters ($\lambda_k$, $w_k$) within a population distribution [41]
4. **Context-dependent weighting**: Incorporate task criticality, user expertise, and environmental factors
5. **Model comparison**: Test against existing HRI trust models [3,14,18] using model selection criteria (AIC, BIC)

---

## 7. Conclusions

We have presented a formal computational model of anxiety accumulation in HRI that synthesizes principles from:
- **Computational neuroscience**: Leaky integrator dynamics, Bayesian inference
- **Stress physiology**: Allostatic load, cortisol kinetics, HRV
- **Behavioral economics**: Loss aversion, negativity bias
- **Clinical psychology**: Fear conditioning, safety learning deficits

**Key contributions:**
1. Explicit mathematical formalization of the "compounding effect" of robot errors
2. Integration of individual differences (trait anxiety, resilience) into model parameters
3. Connection to objective physiological measures (HRV) for real-time validation
4. Foundation for adaptive robot control systems that account for user affective state

**Next steps**: Empirical validation in controlled HRI experiments with wearable robotics, followed by implementation in adaptive control algorithms.

---

## References

[1] Spielberger, C. D. (1983). *Manual for the State-Trait Anxiety Inventory (STAI)*. Palo Alto, CA: Consulting Psychologists Press.

[2] Thayer, J. F., & Lane, R. D. (2009). Claude Bernard and the heart-brain connection: Further elaboration of a model of neurovisceral integration. *Neuroscience & Biobehavioral Reviews*, *33*(2), 81-88. https://doi.org/10.1016/j.neubiorev.2008.08.004

[3] Lee, J. D., & See, K. A. (2004). Trust in automation: Designing for appropriate reliance. *Human Factors*, *46*(1), 50-80. https://doi.org/10.1518/hfes.46.1.50_30392

[4] Ajoudani, A., et al. (2018). Progress and prospects of the human-robot collaboration. *Autonomous Robots*, *42*(5), 957-975. https://doi.org/10.1007/s10514-017-9677-2

[5] Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, *47*(2), 263-291. https://doi.org/10.2307/1914185

[6] Rozin, P., & Royzman, E. B. (2001). Negativity bias, negativity dominance, and contagion. *Personality and Social Psychology Review*, *5*(4), 296-320. https://doi.org/10.1207/S15327957PSPR0504_2

[7] Kirschbaum, C., & Hellhammer, D. H. (1994). Salivary cortisol in psychoneuroendocrine research: Recent developments and applications. *Psychoneuroendocrinology*, *19*(4), 313-333. https://doi.org/10.1016/0306-4530(94)90013-2

[8] McEwen, B. S. (1998). Protective and damaging effects of stress mediators. *New England Journal of Medicine*, *338*(3), 171-179. https://doi.org/10.1056/NEJM199801153380307

[9] Busemeyer, J. R., & Townsend, J. T. (1993). Decision field theory: A dynamic-cognitive approach to decision making. *Psychological Review*, *100*(3), 432-459. https://doi.org/10.1037/0033-295X.100.3.432

[10] Usher, M., & McClelland, J. L. (2001). The time course of perceptual choice: The leaky, competing accumulator model. *Psychological Review*, *108*(3), 550-592. https://doi.org/10.1037/0033-295X.108.3.550

[11] Grillon, C., Baas, J. P., Lissek, S., Smith, K., & Milstein, J. (2004). Anxious responses to predictable and unpredictable aversive events. *Behavioral Neuroscience*, *118*(5), 916-924. https://doi.org/10.1037/0735-7044.118.5.916

[12] Schlotz, W., Hellhammer, J., Schulz, P., & Stone, A. A. (2004). Perceived work overload and chronic worrying predict weekend-weekday differences in the cortisol awakening response. *Psychosomatic Medicine*, *66*(2), 207-214. https://doi.org/10.1097/01.psy.0000116715.78238.56

[13] Thayer, J. F., Åhs, F., Fredrikson, M., Sollers III, J. J., & Wager, T. D. (2012). A meta-analysis of heart rate variability and neuroimaging studies: Implications for heart rate variability as a marker of stress and health. *Neuroscience & Biobehavioral Reviews*, *36*(2), 747-756. https://doi.org/10.1016/j.neubiorev.2011.11.009

[14] Desai, M., Kaniarasu, P., Medvedev, M., Steinfeld, A., & Yanco, H. (2013). Impact of robot failures and feedback on real-time trust. In *Proceedings of the 8th ACM/IEEE International Conference on Human-Robot Interaction* (pp. 251-258). https://doi.org/10.1109/HRI.2013.6483596

[15] Baumeister, R. F., Bratslavsky, E., Finkenauer, C., & Vohs, K. D. (2001). Bad is stronger than good. *Review of General Psychology*, *5*(4), 323-370. https://doi.org/10.1037/1089-2680.5.4.323

[16] LeDoux, J. E. (2000). Emotion circuits in the brain. *Annual Review of Neuroscience*, *23*(1), 155-184. https://doi.org/10.1146/annurev.neuro.23.1.155

[17] Paulus, M. P., & Stein, M. B. (2006). An insular view of anxiety. *Biological Psychiatry*, *60*(4), 383-387. https://doi.org/10.1016/j.biopsych.2006.03.042

[18] Hancock, P. A., Billings, D. R., Schaefer, K. E., Chen, J. Y., De Visser, E. J., & Parasuraman, R. (2011). A meta-analysis of factors affecting trust in human-robot interaction. *Human Factors*, *53*(5), 517-527. https://doi.org/10.1177/0018720811417254

[19] Körber, M. (2019). Theoretical considerations and development of a questionnaire to measure trust in automation. In *Proceedings of the 20th Congress of the International Ergonomics Association* (pp. 13-30). Springer. https://doi.org/10.1007/978-3-319-96074-6_2

[20] Feldman, H., & Friston, K. J. (2010). Attention, uncertainty, and free-energy. *Frontiers in Human Neuroscience*, *4*, 215. https://doi.org/10.3389/fnhum.2010.00215

[21] Bishop, S. J. (2007). Neurocognitive mechanisms of anxiety: An integrative account. *Trends in Cognitive Sciences*, *11*(7), 307-316. https://doi.org/10.1016/j.tics.2007.05.008

[22] Browning, M., Behrens, T. E., Jocham, G., O'Reilly, J. X., & Bishop, S. J. (2015). Anxious individuals have difficulty learning the causal statistics of aversive environments. *Nature Neuroscience*, *18*(4), 590-596. https://doi.org/10.1038/nn.3961

[23] Etkin, A., & Wager, T. D. (2007). Functional neuroimaging of anxiety: A meta-analysis of emotional processing in PTSD, social anxiety disorder, and specific phobia. *American Journal of Psychiatry*, *164*(10), 1476-1488. https://doi.org/10.1176/appi.ajp.2007.07030504

[24] Jovanovic, T., Kazama, A., Bachevalier, J., & Davis, M. (2012). Impaired safety signal learning may be a biomarker of PTSD. *Neuropharmacology*, *62*(2), 695-704. https://doi.org/10.1016/j.neuropharm.2011.02.023

[25] Lonsdorf, T. B., Menz, M. M., Andreatta, M., Fullana, M. A., Golkar, A., Haaker, J., ... & Merz, C. J. (2017). Don't fear 'fear conditioning': Methodological considerations for the design and analysis of studies on human fear acquisition, extinction, and return of fear. *Neuroscience & Biobehavioral Reviews*, *77*, 247-285. https://doi.org/10.1016/j.neubiorev.2017.02.026

[26] Somerville, L. H., Jones, R. M., & Casey, B. J. (2010). A time of change: Behavioral and neural correlates of adolescent sensitivity to appetitive and aversive environmental cues. *Brain and Cognition*, *72*(1), 124-133. https://doi.org/10.1016/j.bandc.2009.07.003

[27] Gunnar, M. R., Wewerka, S., Frenn, K., Long, J. D., & Griggs, C. (2009). Developmental changes in hypothalamus-pituitary-adrenal activity over the transition to adolescence: Normative changes and associations with puberty. *Development and Psychopathology*, *21*(1), 69-85. https://doi.org/10.1017/S0954579409000054

[28] Mata, R., Josef, A. K., Samanez-Larkin, G. R., & Hertwig, R. (2011). Age differences in risky choice: A meta-analysis. *Annals of the New York Academy of Sciences*, *1235*(1), 18-29. https://doi.org/10.1111/j.1749-6632.2011.06200.x

[29] Eppinger, B., Hämmerer, D., & Li, S. C. (2011). Neuromodulation of reward-based learning and decision making in human aging. *Annals of the New York Academy of Sciences*, *1235*(1), 1-17. https://doi.org/10.1111/j.1749-6632.2011.06230.x

[30] Otte, C., Hart, S., Neylan, T. C., Marmar, C. R., Yaffe, K., & Mohr, D. C. (2005). A meta-analysis of cortisol response to challenge in human aging: Importance of gender. *Psychoneuroendocrinology*, *30*(1), 80-91. https://doi.org/10.1016/j.psyneuen.2004.06.002

[31] Chen, J. Y., & Barnes, M. J. (2014). Human-agent teaming for multirobot control: A review of human factors issues. *IEEE Transactions on Human-Machine Systems*, *44*(1), 13-29. https://doi.org/10.1109/THMS.2013.2293535

[32] Rogan, M. T., Stäubli, U. V., & LeDoux, J. E. (1997). Fear conditioning induces associative long-term potentiation in the amygdala. *Nature*, *390*(6660), 604-607. https://doi.org/10.1038/37601

[33] Grillon, C., & Baas, J. (2003). A review of the modulation of the startle reflex by affective states and its application in psychiatry. *Clinical Neurophysiology*, *114*(9), 1557-1579. https://doi.org/10.1016/S1388-2457(03)00202-5

[34] Lissek, S., et al. (2010). Overgeneralization of conditioned fear as a pathogenic marker of panic disorder. *American Journal of Psychiatry*, *167*(1), 47-55. https://doi.org/10.1176/appi.ajp.2009.09030410

[35] Dunsmoor, J. E., & Paz, R. (2015). Fear generalization and anxiety: Behavioral and neural mechanisms. *Biological Psychiatry*, *78*(5), 336-343. https://doi.org/10.1016/j.biopsych.2015.04.010

[36] Milad, M. R., & Quirk, G. J. (2012). Fear extinction as a model for translational neuroscience: Ten years of progress. *Annual Review of Psychology*, *63*, 129-151. https://doi.org/10.1146/annurev.psych.121208.131631

[37] Liberzon, I., & Abelson, J. L. (2016). Context processing and the neurobiology of post-traumatic stress disorder. *Neuron*, *92*(1), 14-30. https://doi.org/10.1016/j.neuron.2016.09.039

[38] Porges, S. W. (2004). Neuroception: A subconscious system for detecting threats and safety. *Zero to Three*, *24*(5), 19-24.

[39] Reinerman-Jones, L., Matthews, G., Barber, D. J., & Abich IV, J. (2014). Psychophysiological metrics for workload are demand-sensitive but multifactorial. In *Proceedings of the Human Factors and Ergonomics Society Annual Meeting* (Vol. 58, pp. 974-978). https://doi.org/10.1177/1541931214581204

[40] Liu, P., Galla, S., & Sarkar, N. (2016). Human-robot relationship state estimation using physiological signals. In *2016 IEEE International Conference on Automation Science and Engineering* (pp. 274-279). https://doi.org/10.1109/COASE.2016.7743408

[41] Gelman, A., & Hill, J. (2006). *Data analysis using regression and multilevel/hierarchical models*. Cambridge University Press. https://doi.org/10.1017/CBO9780511790942

---

## Appendix: Notation Summary

| Symbol | Meaning | Units |
|--------|---------|-------|
| $A(t)$ | Instantaneous anxiety at time $t$ | Arbitrary units (AU) or STAI-S score |
| $A_{\text{baseline}}$ | Trait anxiety (resting state) | STAI-T score |
| $E_i$ | Magnitude of error event $i$ | Subjective units (e.g., 0-10 scale) |
| $w_i$ | Weighting factor for event $i$ | Dimensionless (typically 1.5-3.0) |
| $\lambda$ | Decay rate constant | min⁻¹ (typical range: 0.008-0.02) |
| $t_i$ | Time of occurrence of event $i$ | Minutes or seconds |
| $T(t)$ | Trust level at time $t$ | 0-1 scale or Likert scale |
| $\sigma^2$ | Variance (uncertainty) | Units² of measured variable |
| $\pi$ | Precision (inverse variance) | 1/Units² |
| $\alpha$ | Learning rate | Dimensionless (0-1) |
| $\tau$ | Integration time window | Minutes |
| HRV | Heart rate variability | ms² (HF-HRV power) |

