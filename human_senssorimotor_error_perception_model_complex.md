# Human Perceptual-Sensorimotor Model for Wearable Robotics

## Model Overview

The proposed model for human perception of wearable robot action errors is:

$$E_{\text{human}}(t) = g(t) \cdot \log\left(1 + \frac{|A(t)|}{A_{\text{ref}}}\right) \cdot K_{\text{time}}(\omega, \Delta t(t), \mathcal{C})$$
where:
$$        ( A ) = \text{Action error magnitude}$$
$$ (A_{\text{ref}}) = \text{Reference action magnitude representing expected or baseline assistance} $$
$$\text{(e.g., nominal torque, predicted effort). Sets Weber-scale sensitivity (≈ detection at 10–20\% of} (A_{\text{ref}})).$$

$$        ( \Delta t ) = \text{Temporal error between expected and actual robot action
(e.g., control delay or phase shift)}$$
$$        (\mathcal{C}) = \text{Task context indicator (e.g., discrete event vs rhythmic locomotion)} $$
$$ (\omega) = \text{Task angular frequency }(\omega = 2\pi / T)$$
$$ ((T) = \text{cycle period, e.g., stride duration)}$$
$$(g(t)) = \text{Adaptation gain capturing habituation over repetition or exposure}$$
$$(e.g., (g(t)=g_0 e^{-t/\tau_{\text{adapt}}})).
\text{ Modulates perceived salience, not physical error.}$$

and $K_{\text{time}}$ is context-dependent:
- **Event-based**: $K_{\text{time}} = \sigma(\beta(|\Delta t| - t_0))$
- **Rhythmic**: $K_{\text{time}} = \frac{1}{2}(1 - \cos(\omega\Delta t - \phi_{\text{pref}}))$
where 
$$(\phi_{\text{pref}}) = \text{Preferred assistance phase (task- and movement-phase dependent)} $$
$$ ( \beta ) = \text{Individual sharpness (age, training, pathology)}$$

$$( \sigma ) = sigmoid $$
$$(t_0) = \text{Temporal tolerance window / JND (typically a few percent of task period)} $$
* **Temporal tolerance** is the maximum timing mismatch a human can experience before noticing that an action is “off”. (**JND** stands for *Just Noticeable Difference*.)


## Strengths: What the Model Captures

### 1. Weber-Law Scaling for Force/Torque Perception

**Model Component**: $\log(1 + |A(t)|/A_{\text{ref}})$

**Evidence**: The logarithmic scaling aligns with psychophysical findings on torque perception. Welker et al. [1] demonstrated that humans exhibit Weber-law behavior in wrist torque discrimination, with just-noticeable differences (JNDs) ranging from **7.5% to 22.9%** of the reference torque depending on limb state and movement context. The model's use of relative scaling ($|A|/A_{\text{ref}}$) correctly captures this proportional sensitivity rather than absolute thresholds [1].

**Validation**: The 10-20% detection threshold range mentioned in the model parameters is empirically supported across multiple studies of haptic perception in physical human-robot interaction [1, 4].

---

### 2. Context-Dependent Temporal Sensitivity

**Model Component**: Dual temporal kernels for event-based vs. rhythmic tasks

**Evidence**: 

- **Event-based sigmoid**: The sigmoid function $\sigma(\beta(|\Delta t| - t_0))$ appropriately models the sharp perceptual transition around temporal tolerance windows. This aligns with psychometric functions used in temporal discrimination tasks [3, 5].

- **Rhythmic cosine kernel**: For cyclic tasks like walking, Peng et al. [5] found that actuation timing perception in powered ankle exoskeletons is **phase-dependent**, with detection rates varying systematically across the gait cycle. The cosine term $(1 - \cos(\omega\Delta t - \phi_{\text{pref}}))$ captures this periodic sensitivity, where certain phases (e.g., push-off) show heightened sensitivity to timing errors [5].

**Temporal tolerance windows**: Studies report temporal JNDs of approximately **3-8% of the gait cycle** for ankle exoskeleton timing perception [5], supporting the model's $t_0$ parameter as a small fraction of task period.

---

### 3. Adaptation and Habituation Dynamics

**Model Component**: $g(t) = g_0 e^{-t/\tau_{\text{adapt}}}$

**Evidence**: The exponential decay function captures sensory adaptation effects documented in haptic perception. Moaed and Engeberg [4] demonstrated that multichannel sensorimotor integration involves adaptive mechanisms where repeated exposure to stimuli reduces perceptual salience over time. While specific time constants $\tau_{\text{adapt}}$ for exoskeleton habituation require further empirical characterization, the exponential form is consistent with classical adaptation models in psychophysics [4].

---

### 4. Multiplicative Structure

**Model Component**: Multiplication of magnitude and temporal terms

**Rationale**: The multiplicative structure implies that both magnitude and timing errors must be present for maximal perceived error. This is mechanistically reasonable: a large force error delivered at the expected time may be less disruptive than a moderate error delivered at an unexpected time. However, direct empirical validation of this interaction term is limited in the current literature.

---

## Limitations: What the Model Does Not Consider

### 1. **Directional Asymmetry**

The model uses $|A(t)|$, ignoring the sign of the error. Welker et al. [1] found **significant asymmetries** between flexion and extension torque perception, with different JND values depending on torque direction. Resistive forces (opposing movement) may be perceived differently than assistive forces (aiding movement), but current evidence is task-specific and inconsistent [1].

**Impact**: For applications requiring directional sensitivity (e.g., distinguishing over-assistance from under-assistance), the model may need separate terms for positive and negative errors.

---

### 2. **Movement Phase Effects**

While the rhythmic kernel captures periodic sensitivity, it does not explicitly model how perception varies across movement phases (acceleration, steady-state, deceleration). Peng et al. [5] showed that timing perception differs between stance and swing phases of gait, suggesting that $\phi_{\text{pref}}$ and $\beta$ may need to be phase-dependent functions rather than constants.

---

### 3. **Multi-Modal Sensory Integration**

The model treats perception as a single channel. In reality, humans integrate proprioceptive, visual, vestibular, and tactile cues. Moaed and Engeberg [4] demonstrated that multichannel sensory feedback significantly affects perception of robotic assistance. The model does not account for:
- Visual feedback of robot state
- Vestibular contributions during balance-critical tasks
- Cross-modal suppression or enhancement effects

---

### 4. **Predictability and Learning**

The adaptation term $g(t)$ captures passive habituation but does not model:
- **Predictive error cancellation**: Humans learn to anticipate regular robot behaviors and may perceptually suppress expected errors
- **Attention and cognitive load**: Detection thresholds increase under dual-task conditions
- **Trust dynamics**: Repeated errors may increase vigilance rather than decrease salience

---

### 5. **Task-Specific Parameters**

The model requires empirical tuning of:
- $A_{\text{ref}}$: Reference magnitude (context-dependent)
- $t_0$: Temporal tolerance (varies with task frequency)
- $\beta$: Individual sharpness (age, training, pathology)
- $\phi_{\text{pref}}$: Preferred phase (task and joint-specific)
- $\tau_{\text{adapt}}$: Adaptation time constant (limited data)

Current literature provides partial guidance [1, 5], but comprehensive parameter databases across tasks and populations are lacking.

---

## Conclusion

The proposed model is **sufficiently good** as a compact perceptual-sensorimotor model for wearable robotics. It incorporates the three most critical empirically-validated features:

1. **Weber-law magnitude scaling** (10-20% JNDs) [1]
2. **Context-dependent temporal kernels** (event vs. rhythmic) [5]
3. **Adaptation dynamics** (habituation) [4]

The multiplicative structure is mechanistically plausible, though direct validation is needed. Key limitations include the absence of directional asymmetry, multi-modal integration, and predictive learning effects. For applications requiring these features, the model can be extended with directional terms, phase-dependent parameters, or cognitive state variables.

For initial controller design, human-in-the-loop optimization, and comfort-based tuning of wearable robots, this model provides a practical, theoretically-grounded framework.

---

## References

[1] Welker, C. G., Collins, S. H., & Okamura, A. M. (2022). Human Perception of Wrist Flexion and Extension Torque During Upper and Lower Extremity Movement. *IEEE Transactions on Haptics*, 15(4), 717-728. https://doi.org/10.1109/TOH.2022.3219031

[2] Moaed, A., & Engeberg, E. D. (2024). Multichannel Sensorimotor Integration with a Dexterous Artificial Hand. *Robotics*, 13(7), 97. https://doi.org/10.3390/robotics13070097

[3] Clark, J. P., & O'Malley, M. K. (2023). Defining Allowable Stimulus Ranges for Position and Force Controlled Cutaneous Cues. *IEEE Transactions on Haptics*, 16(2), 234-245. https://doi.org/10.1109/TOH.2023.3286306

[4] Moaed, A., & Engeberg, E. D. (2024). Multichannel Sensorimotor Integration with a Dexterous Artificial Hand. *Robotics*, 13(7), 97. https://doi.org/10.3390/robotics13070097

[5] Peng, X., Acosta-Sojo, Y., Wu, M. I., et al. (2022). Actuation Timing Perception of a Powered Ankle Exoskeleton and Its Associated Ankle Angle Changes During Walking. *IEEE Transactions on Neural Systems and Rehabilitation Engineering*, 30, 1-12. https://doi.org/10.1109/TNSRE.2022.3162213
