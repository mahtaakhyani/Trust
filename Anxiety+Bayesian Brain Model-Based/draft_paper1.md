# Convergent Models of Anxiety Accumulation in Human-Robot Interaction: Derivation from Biological Time Constants and the Free Energy Principle

## Abstract

We present a unified computational model of anxiety accumulation in human-robot interaction (HRI) derived through two independent approaches: (1) empirical synthesis of stress physiology, behavioral economics, and fear conditioning literature, and (2) formal derivation from the Free Energy Principle (FEP) and active inference framework. Both derivations converge on an identical mathematical structure—a precision-weighted, temporally discounted accumulation of surprise—providing mutual validation of the model's theoretical foundations. The model predicts that anxiety at time $t$ follows:

$$A(t) = A_{\text{baseline}} + \sum_{i=1}^{n} w_i \cdot S_i \cdot e^{-\lambda(t-t_i)}$$

where robot errors accumulate as surprise events ($S_i$), weighted by negativity bias ($w_i$), and decay exponentially with physiologically-grounded time constants ($\lambda \approx 0.01$ min⁻¹). We demonstrate that empirically-derived parameters (negativity weights, decay rates) have direct interpretations as precision ratios and temporal discounting in Bayesian inference. This convergence suggests the model captures fundamental principles of affective dynamics rather than arbitrary curve-fitting. We discuss applications to adaptive robot control, individual difference modeling, and testable predictions that differentiate the mechanisms underlying the unified model.

**Keywords**: Human-robot interaction, anxiety modeling, Free Energy Principle, allostatic load, Bayesian inference, predictive processing, computational psychiatry

---

## 1. Introduction

### 1.1 The Challenge of Modeling Affective Dynamics in HRI

As robotic systems become increasingly integrated into domains requiring extended human interaction—wearable prosthetics, assistive robotics, teleoperation, and collaborative manipulation—understanding user affective state has become critical for system design and safety [1,2]. A central challenge is modeling how users respond to robot errors: while a single minor deviation may be tolerated, repeated or unexpected failures often produce disproportionate anxiety responses that persist long after the triggering event [3,4].

Existing HRI trust models [5,6] typically treat each error as an independent event, failing to capture the compounding effect observed empirically: a second error occurring within minutes of the first produces anxiety levels exceeding the simple sum of individual responses [7]. This non-linear accumulation suggests that anxiety has intrinsic temporal dynamics shaped by both immediate events and longer-term physiological recovery processes.

### 1.2 Two Approaches to Understanding Anxiety

Anxiety can be understood from two complementary perspectives:

**Empirical/mechanistic perspective**: Anxiety is a physiological state characterized by measurable biomarkers—elevated cortisol, reduced heart rate variability (HRV), increased muscle tension—each with known temporal dynamics [8,9]. From this view, anxiety accumulation reflects the superposition of stress responses that decay according to biological time constants.

**Computational/normative perspective**: Anxiety is a consequence of Bayesian inference under uncertainty [10,11]. The brain continuously predicts sensory inputs and updates beliefs based on prediction errors. Anxiety emerges when the system assigns aberrantly high precision (inverse variance) to threat-related predictions, amplifying the impact of unexpected aversive events [12,13].

### 1.3 Contribution and Structure

This paper demonstrates that these two perspectives, developed independently, converge on an identical mathematical model of anxiety accumulation. We:

1. **Derive the model from empirical observations** (Section 2): Using established findings from stress physiology, behavioral economics, and fear conditioning, we construct a model based on measurable biological parameters.

2. **Derive the model from theoretical principles** (Section 3): Starting from the Free Energy Principle and active inference framework, we show that anxiety accumulation follows necessarily from optimal Bayesian inference in volatile environments.

3. **Show formal equivalence** (Section 4): We demonstrate that the empirically-derived parameters (negativity weights, decay constants, surprise) have direct interpretations as computational quantities (precision ratios, temporal discounting, Bayesian surprise).

4. **Identify testable predictions** (Section 5): We leverage the convergence to generate predictions that can differentiate between alternative mechanisms and validate the model's deeper claims.

This convergent derivation approach provides stronger evidence than either derivation alone: the model is not an ad hoc fit to data, nor is it untethered mathematical abstraction, but rather an inevitable consequence of both empirical constraints and normative principles.

---

## 2. Part I: Bottom-Up Derivation from Biological First Principles

### 2.1 Starting Assumptions

We begin with four empirically-grounded claims about anxiety dynamics, each supported by extensive literature:

**Claim 1**: Stressful events accumulate over time rather than being processed independently.  
**Claim 2**: The impact of past events decays exponentially with physiological time constants.  
**Claim 3**: Negative events are weighted more heavily than positive events.  
**Claim 4**: Unexpectedness amplifies the psychological impact of events.

We now formalize each claim mathematically.

---

### 2.2 Claim 1: Allostatic Load and Event Accumulation

**Empirical Basis**: McEwen's allostatic load theory [14] demonstrates that repeated stressors produce cumulative physiological "wear and tear" that exceeds the sum of individual responses. Schlotz et al. [15] showed that daily stressors accumulate to predict weekend cortisol levels, and Thayer et al. [16] demonstrated cumulative effects on HRV suppression.

**Mathematical Formulation**: Anxiety at time $t$ depends on all past events, not just the most recent:

$$A(t) = A_{\text{baseline}} + f(\text{event history})$$

where $A_{\text{baseline}}$ represents trait anxiety (individual resting state, measured by STAI-T [17]) and $f$ is a yet-to-be-determined accumulation function.

**Key insight**: The summation operator $\sum$ will naturally emerge from the requirement that multiple events contribute additively to total load.

---

### 2.3 Claim 2: Exponential Decay Following Biological Time Constants

**Empirical Basis**: 

- **Cortisol clearance**: Salivary cortisol follows first-order decay kinetics with half-lives of 60-90 minutes in response to acute stressors [18,19].
- **HRV recovery**: High-frequency HRV returns to baseline with time constants of 30-70 minutes following stress induction [16,20].
- **Subjective anxiety**: Self-reported state anxiety (STAI-S) decays exponentially following laboratory stressors, with recovery periods of 45-90 minutes [21].

**Mathematical Formulation**: The impact of an event occurring at time $t_i$ decays exponentially:

$$\text{Impact}(t) \propto e^{-\lambda(t - t_i)}$$

where $\lambda$ is the decay rate constant. Empirically, $\lambda \approx 0.01 \text{ to } 0.02 \text{ min}^{-1}$, corresponding to half-lives of:

$$t_{1/2} = \frac{\ln 2}{\lambda} \approx 35\text{ to }70 \text{ min}$$

**Physical interpretation**: At time $t = t_i + \frac{1}{\lambda}$, approximately 37% of the original impact remains. By $t = t_i + \frac{3}{\lambda}$ (roughly 150-300 minutes for typical $\lambda$), the impact has decayed to ~5% of its original magnitude, representing practical washout.

**Combining Claims 1 and 2**: The accumulation function becomes:

$$f(\text{event history}) = \sum_{i=1}^{n} g(E_i) \cdot e^{-\lambda(t - t_i)}$$

where $g(E_i)$ represents the initial impact of event $i$ with magnitude $E_i$, and the sum accounts for all $n$ events within the effective memory window.

---

### 2.4 Claim 3: Negativity Bias and Loss Aversion

**Empirical Basis**:

- **Prospect theory** [22]: Losses loom larger than gains, with a typical loss aversion coefficient of $\lambda_{\text{loss}} \approx 2-2.5$.
- **Negativity bias** [23]: Across multiple psychological domains, negative events are weighted 2-3× more heavily than positive events of equivalent objective magnitude.
- **Neural asymmetry** [24,25]: Amygdala responses to threat-related stimuli are faster, stronger, and more persistent than responses to safety or reward signals. Loss-related activations in anterior insula exceed gain-related activations by a factor of ~2.

**HRI-specific evidence**: In human-automation interaction, Desai et al. [26] demonstrated that a single robot failure requires 3-5 successful interactions to restore baseline trust, suggesting $w_{\text{error}} \approx 3-5$ times $w_{\text{success}}$.

**Mathematical Formulation**: The initial impact of an event depends on its valence:

$$g(E_i) = w_i \cdot E_i$$

where:
- For errors/failures: $w_{\text{error}} \approx 2.0$ to $3.0$
- For successes: $w_{\text{success}} \approx 0.5$ to $1.0$
- For neutral events: $w_{\text{neutral}} = 0$

**Updated model**:

$$f(\text{event history}) = \sum_{i=1}^{n} w_i \cdot E_i \cdot e^{-\lambda(t - t_i)}$$

---

### 2.5 Claim 4: The Role of Surprise and Predictability

**Empirical Basis**:

- **Predictable vs. unpredictable stress** [27]: Grillon (2002) demonstrated that unpredictable shocks produce greater startle responses and sustained anxiety compared to predictable shocks of equal intensity and frequency.
- **Controllability** [28]: Perceived controllability (a form of predictability) is one of the strongest moderators of stress responses; uncontrollable stressors produce more persistent cortisol elevation and HRV suppression.
- **Expectancy violation** [29]: Events that violate established expectations produce larger P300 ERP components and stronger amygdala activation than expected events.

**Conceptual insight**: An error of magnitude 5 occurring after 30 minutes of flawless performance is psychologically more impactful than the same error occurring in a context of frequent, ongoing errors.

**Mathematical Formulation**: We decompose event magnitude into objective severity and subjective surprise:

$$E_i \rightarrow S_i = E_i \cdot U_i \cdot C_i$$

where:
- $E_i$: Objective kinematic error magnitude (e.g., degrees of angular deviation, cm of position error)
- $U_i$: Unexpectedness factor (depends on recent error history)
- $C_i$: Contextual criticality (task importance, social context)

**Modeling unexpectedness**: We define unexpectedness based on temporal proximity to previous errors:

$$U_i = 1 + \beta \cdot \exp\left(-\frac{t_i - t_{i-1}}{\tau_{\text{expect}}}\right)$$

where:
- $\beta \approx 0.5$ to $1.0$ (calibrated from predictability experiments)
- $\tau_{\text{expect}} \approx 30$ to $60$ seconds (expectation window)

**Interpretation**:
- If error $i$ occurs shortly after error $i-1$ (within $\tau_{\text{expect}}$), the exponent is large, so $U_i \approx 1 + \beta$ (moderately unexpected, user is already vigilant)
- If error $i$ occurs long after the previous error (beyond 3-5× $\tau_{\text{expect}}$), the exponent is near zero, so $U_i \approx 1$ (baseline unexpectedness, user had relaxed)

**Note on first events**: For the first error ($i=1$), we set $U_1 = 1$ (no prior history to violate).

---

### 2.6 The Complete Empirical Model

Integrating all four claims, we arrive at:

$$\boxed{A(t) = A_{\text{baseline}} + \sum_{i=1}^{n} w_i \cdot S_i \cdot e^{-\lambda(t-t_i)}}$$

where surprise $S_i = E_i \cdot U_i \cdot C_i$.

**Expanding fully**:

$$A(t) = A_{\text{baseline}} + \sum_{i=1}^{n} w_i \cdot E_i \cdot U_i \cdot C_i \cdot e^{-\lambda(t-t_i)}$$

### 2.7 Parameter Summary (Empirical Derivation)

| Parameter | Empirical Basis | Typical Range | Measurement Method |
|-----------|-----------------|---------------|-------------------|
| $A_{\text{baseline}}$ | Trait anxiety (STAI-T) | 20-60 (AU) | STAI-T questionnaire [17] |
| $\lambda$ | Cortisol/HRV decay rate | 0.008-0.02 min⁻¹ | Fit to physiological recovery curves [18,20] |
| $w_i$ | Negativity bias | 2.0-3.0 (errors) | Behavioral trust experiments [22,23,26] |
| $E_i$ | Kinematic error magnitude | 0-10 (normalized) | Direct measurement (degrees, cm) |
| $U_i$ | Unexpectedness | 1.0-2.0 | Derived from inter-event intervals [27] |
| $C_i$ | Task criticality | 0.5-2.0 | Task analysis / user ratings |

---

## 3. Part II: Top-Down Derivation from the Free Energy Principle

### 3.1 The Free Energy Principle: Core Concepts

The Free Energy Principle (FEP) [30,31] proposes that biological systems minimize **variational free energy** ($F$), an information-theoretic quantity that upper-bounds surprise. Formally:

$$F = \mathbb{E}_{q(s)}[\ln q(s) - \ln p(o,s)] \geq -\ln p(o) = \text{Surprise}$$

where:
- $o$: Sensory observations (e.g., proprioceptive feedback from robot)
- $s$: Hidden states of the world (e.g., robot configuration, safety status)
- $q(s)$: Brain's approximate posterior belief about states
- $p(o,s)$: True generative model (joint probability of observations and states)

**Key insight**: The brain cannot directly access surprise ($-\ln p(o)$) because it requires knowing the true distribution $p(o)$. Instead, it minimizes free energy $F$, which can be computed from internal beliefs $q(s)$.

### 3.2 Decomposition of Free Energy

Free energy decomposes into two competing objectives:

$$F = \underbrace{D_{\text{KL}}[q(s) || p(s)]}_{\text{Complexity}} - \underbrace{\mathbb{E}_{q(s)}[\ln p(o|s)]}_{\text{Accuracy}}$$

- **Accuracy**: How well do my beliefs explain current observations?
- **Complexity**: How much do my beliefs deviate from my priors?

**Healthy inference**: Balance accuracy and complexity—update beliefs to fit observations while maintaining reasonable priors.

**Anxious inference**: Over-weight accuracy (sensory evidence) at the expense of complexity (deviation from stable priors). This manifests as over-fitting to noisy or threatening observations.

---

### 3.3 Precision-Weighted Prediction Errors

In hierarchical predictive processing [32,33], the brain encodes beliefs as probability distributions with associated **precision** (inverse variance):

$$\pi = \frac{1}{\sigma^2}$$

Prediction errors (mismatches between predicted and observed sensory signals) are weighted by their expected precision:

$$\Delta q \propto \pi \cdot \epsilon$$

where $\epsilon = o - \hat{o}$ is the prediction error.

**Anxiety as aberrant precision**: Computational psychiatry models [12,34,35] propose that anxiety arises from misallocated precision:

- **Hyper-precision on threat signals**: $\pi_{\text{threat}} \gg \pi_{\text{baseline}}$
- **Hypo-precision on safety signals**: $\pi_{\text{safety}} \ll \pi_{\text{baseline}}$

This creates a state where the brain over-reacts to minor errors (high precision amplifies small prediction errors) and under-responds to corrective evidence (low precision attenuates safety signals).

---

### 3.4 Anxiety as Accumulated Free Energy

Under active inference [36,37], anxiety is formalized as the **rate of change of free energy** that cannot be resolved through action or perceptual updating:

$$\frac{dA}{dt} = \frac{dF}{dt}\bigg|_{\text{unresolved}}$$

When the system successfully minimizes free energy (accurate predictions, successful actions), $\frac{dF}{dt} < 0$ and anxiety dissipates. When free energy accumulates faster than it can be minimized, anxiety increases.

**Temporal integration**: Anxiety at time $t$ is the cumulative unresolved free energy:

$$A(t) = \int_0^t \frac{dF}{d\tau} \, d\tau + A_0$$

For a system with exponential forgetting (temporal discounting of past observations), this becomes:

$$A(t) = A_0 e^{-\alpha t} + \int_0^t e^{-\alpha(t-\tau)} \frac{dF}{d\tau} d\tau$$

where $\alpha$ is the temporal decay rate (inverse of the brain's effective memory window for affective states).

---

### 3.5 Precision-Weighted Surprise

The rate of free energy change is proportional to **precision-weighted surprise**:

$$\frac{dF}{dt} \propto \Pi(t) \cdot S(t)$$

where:
- $S(t) = -\ln p(o_t | s_t)$: Bayesian surprise (negative log-likelihood of current observation)
- $\Pi(t)$: Time-varying precision encoding confidence in sensory channels

Substituting into the integral:

$$A(t) = A_0 e^{-\alpha t} + \int_0^t e^{-\alpha(t-\tau)} \Pi(\tau) S(\tau) d\tau$$

**This is the continuous-time FEP anxiety model.**

---

### 3.6 Discretization for Event-Based HRI

In robotic systems, errors occur as **discrete events** at specific times $\{t_1, t_2, ..., t_n\}$ rather than continuous fluctuations. We discretize the integral using Riemann approximation:

$$\int_0^t e^{-\alpha(t-\tau)} \Pi(\tau) S(\tau) d\tau \approx \sum_{i=1}^n e^{-\alpha(t-t_i)} \Pi_i S_i \Delta t_i$$

For point events (Dirac delta functions in time), $\Delta t_i \to 1$ and we obtain:

$$A(t) = A_0 e^{-\alpha t} + \sum_{i=1}^n \Pi_i S_i e^{-\alpha(t-t_i)}$$

**Steady-state assumption**: For ongoing interactions where the system has reached dynamic equilibrium, the initial transient $A_0 e^{-\alpha t}$ decays to negligible levels. Replacing $A_0$ with the steady-state baseline $A_{\text{baseline}}$:

$$\boxed{A(t) = A_{\text{baseline}} + \sum_{i=1}^n \Pi_i S_i e^{-\alpha(t-t_i)}}$$

---

### 3.7 Operationalizing Precision for Robot Errors

**Theoretical definition**: Precision $\Pi_i$ represents the inverse variance assigned to prediction errors:

$$\Pi_i = \frac{1}{\sigma_i^2}$$

**Anxiety-dependent precision**: In anxious states, precision is amplified [12,34]:

$$\Pi_i = \Pi_{\text{baseline}} \cdot [1 + \beta \cdot A(t_i^-)]$$

where $A(t_i^-)$ is anxiety just before event $i$, creating a positive feedback loop.

**Simplified approximation**: For initial model validation, we approximate anxiety-dependent precision as a **constant weighting factor**:

$$\Pi_i \approx w_i$$

where $w_i$ captures the average precision amplification for errors vs. neutral/positive events:

$$w_{\text{error}} = \frac{\Pi_{\text{error}}}{\Pi_{\text{neutral}}} \approx 2-3$$

**Future work**: Section 5 discusses testing the full dynamic precision model.

---

### 3.8 Operationalizing Surprise for Robot Errors

**Theoretical definition**: Bayesian surprise is the negative log-probability of an observation:

$$S_i = -\ln p(o_i | s_i, \text{history})$$

**Decomposition**: Probability depends on both magnitude and expectation:

$$p(o_i) \approx p(E_i) \cdot p(\text{unexpected}) \cdot p(\text{context})$$

Taking negative logarithms (sum of independent factors):

$$S_i = -\ln p(E_i) - \ln p(\text{unexpected}) - \ln p(\text{context})$$

**Operational form**: Approximating log-probabilities with normalized scores:

$$S_i \approx E_i \cdot U_i \cdot C_i$$

where:
- $E_i$: Error magnitude (high magnitude → low probability → high surprise)
- $U_i$: Unexpectedness (violated prediction → low probability → high surprise)
- $C_i$: Contextual criticality (amplifies functional significance of surprise)

This is the same decomposition derived empirically in Section 2.5.

---

### 3.9 The Complete Theoretical Model

Combining discretization (3.6), precision approximation (3.7), and surprise operationalization (3.8):

$$\boxed{A(t) = A_{\text{baseline}} + \sum_{i=1}^n w_i \cdot S_i \cdot e^{-\alpha(t-t_i)}}$$

where $S_i = E_i \cdot U_i \cdot C_i$ and $\alpha = \lambda$ (we use $\lambda$ for consistency with the empirical derivation).

**This is identical to the empirical model (Section 2.6).**

---

### 3.10 Parameter Summary (Theoretical Derivation)

| Parameter | FEP Interpretation | Computational Role |
|-----------|-------------------|-------------------|
| $A_{\text{baseline}}$ | Prior expected free energy | Baseline homeostatic set-point |
| $\lambda$ | Temporal precision decay rate | Inverse of affective memory window |
| $w_i$ | Precision ratio $\Pi_{\text{threat}}/\Pi_{\text{neutral}}$ | Gain on prediction errors |
| $S_i$ | Bayesian surprise $-\ln p(o_i)$ | Information content of observation |
| $U_i$ | Expectation violation | Inferred volatility component |
| $C_i$ | Contextual precision modulation | Task-dependent gain |

---

## 4. Part III: Convergence Analysis and Unification

### 4.1 Structural Equivalence

The two derivations produce the same functional form:

**Empirical model** (from biology):
$$A(t) = A_{\text{baseline}} + \sum_{i=1}^n w_i \cdot E_i \cdot U_i \cdot C_i \cdot e^{-\lambda(t-t_i)}$$

**Theoretical model** (from FEP):
$$A(t) = A_{\text{baseline}} + \sum_{i=1}^n w_i \cdot E_i \cdot U_i \cdot C_i \cdot e^{-\lambda(t-t_i)}$$

**These are identical.**

### 4.2 Parameter Mapping

Each parameter has dual interpretations:

| Component | Empirical Interpretation | FEP Interpretation | Mutual Constraint |
|-----------|-------------------------|-------------------|-------------------|
| **$A_{\text{baseline}}$** | Trait anxiety (STAI-T) | Prior expected free energy | Individual difference parameter measurable via questionnaire and computable via hierarchical priors |
| **$\lambda$** | Cortisol/HRV decay rate (0.01-0.02 min⁻¹) | Inverse temporal precision | Must match physiological time constants (~60-90 min half-life) |
| **$w_i$** | Negativity bias (~2-3 for errors) | Precision ratio $\Pi_{\text{threat}}/\Pi_{\text{neutral}}$ | Should emerge from optimal inference under asymmetric costs (false negatives >> false positives) |
| **$E_i$** | Kinematic error magnitude | Component of $-\ln p(o)$ | Directly observable; higher magnitude → lower probability |
| **$U_i$** | Expectation violation | Inferred volatility | Computable from inter-event statistics or explicit Bayesian volatility estimation |
| **$C_i$** | Task criticality | Context-dependent precision modulation | Task analysis or learned from outcomes |

### 4.3 Why the Convergence Matters

The fact that independent derivations yield identical mathematics is not coincidental—it suggests the model captures **fundamental constraints** on affective dynamics:

1. **Biological constraints**: Physiological recovery processes have intrinsic time constants that must be respected.

2. **Computational constraints**: Optimal inference under uncertainty necessitates precision-weighting and temporal integration.

3. **Evolutionary constraints**: Negativity bias and loss aversion are adaptations to asymmetric survival costs.

The model sits at the intersection of these constraints, making it **mechanistically grounded, normatively justified, and evolutionarily plausible**.

### 4.4 Testable Predictions from the Unified Model

The convergence enables strong predictions:

#### **Prediction 1: Negativity weight equals optimal precision ratio**

From empirical data: $w_{\text{error}} \approx 2-3$

From FEP: Under optimal inference with asymmetric costs (false negative cost = $C_{FN}$, false positive cost = $C_{FP}$), the precision ratio should be:

$$w_{\text{optimal}} = \sqrt{\frac{C_{FN}}{C_{FP}}}$$

If $C_{FN} \approx 4-9 \times C_{FP}$ (plausible for HRI safety), then $w_{\text{optimal}} \approx 2-3$. ✓

**Test**: Manipulate perceived costs experimentally and measure resulting $w_i$ from behavioral data.

#### **Prediction 2: Decay rate matches temporal credit assignment**

From empirical data: $\lambda \approx 0.01-0.02$ min⁻¹ (cortisol kinetics)

From FEP: Temporal discounting in Bayesian filtering should match the timescale over which past observations remain informative for predicting future states.

**Test**: Measure how long error patterns remain predictive of subsequent errors. This should match $1/\lambda$ (~50-100 min).

#### **Prediction 3: Individual differences in $\lambda$ correlate with HRV recovery**

From empirical data: Lower $\lambda$ → slower anxiety decay

From FEP: Lower $\lambda$ → longer memory window for integrating surprise

**Test**: Measure HRV recovery half-life and estimate $\lambda$ from behavioral trust dynamics. These should correlate ($r > 0.6$).

#### **Prediction 4: Predictability reduces $U_i$ and thereby $S_i$**

From empirical data: Unpredictable shocks produce more anxiety [27]

From FEP: Predictable errors have higher $p(\text{error})$, thus lower surprise $S = -\ln p(\text{error})$

**Test**: Present identical errors in predictable vs. unpredictable sequences. Predictable sequences should produce lower total $A(t)$ due to reduced $U_i$.

#### **Prediction 5: Anxiety amplifies sensory precision (dynamic $w_i$)**

From empirical data: Anxious individuals show hyper-reflexivity [38]

From FEP: $w_i = w_{\text{baseline}} \cdot [1 + \beta A(t_i^-)]$ creates positive feedback

**Test**: Induce anxiety experimentally (via unpredictable errors), then present identical test error. The same error should produce larger $\Delta A$ when occurring in high-anxiety vs. low-anxiety states.

---

## 5. Part IV: Empirical Validation Strategy

### 5.1 Experimental Design

#### **Phase 1: Parameter Estimation**

**Participants**: 60 adults (balanced for trait anxiety: 20 low STAI-T <35, 20 medium 35-45, 20 high >45)

**Task**: Teleoperation of a robotic arm for object manipulation (pick-and-place)

**Error injection protocol**:
- **Predictable condition**: Small kinematic errors (5° overshoot) every 60 seconds
- **Unpredictable condition**: Same errors at random intervals (30-120 sec)
- **Magnitude variation**: Errors of 2°, 5°, 10°, 15° to calibrate $E_i$ scaling

**Measures**:
- **Continuous**: HRV (5-min RMSSD), skin conductance
- **Discrete**: STAI-S every 10 minutes, trust ratings after each trial
- **Behavioral**: Error correction time, movement smoothness

**Model fitting**: Use non-linear least squares to estimate $\{A_{\text{baseline}}, \lambda, w_i, \beta\}$ per participant, minimizing:

$$\text{SSE} = \sum_t [A_{\text{observed}}(t) - A_{\text{model}}(t)]^2$$

where $A_{\text{observed}}$ is the normalized composite of HRV, STAI-S, and skin conductance.

#### **Phase 2: Validation Against Novel Sequences**

Using parameters estimated in Phase 1, predict responses to new error sequences not seen during calibration:

- Mixed magnitude sequences (varying $E_i$)
- Clustered vs. distributed errors (testing exponential decay)
- Context switches (manipulating $C_i$ via task instructions)

**Success criterion**: $R^2 > 0.6$ between predicted and observed anxiety trajectories.

#### **Phase 3: Intervention Testing**

Test model-informed adaptive control:

**Baseline controller**: Standard impedance control (no anxiety model)

**Adaptive controller**: Use real-time HRV to estimate $A(t)$, then:
- If $A(t) > A_{\text{threshold}}$: Increase assistance, reduce autonomy
- Enforce minimum inter-error interval: $\Delta t > 3/\lambda$ (~150-300 min)

**Prediction**: Adaptive controller should reduce cumulative anxiety by ~30-40% compared to baseline.

---

### 5.2 Predicted Results

#### **Result 1: Exponential decay fit**

**Prediction**: Single-error responses should decay as $A(t) = A_{\text{peak}} e^{-\lambda t}$ with $\lambda \approx 0.01-0.02$ min⁻¹.

**Alternative hypothesis**: If anxiety were a step function (no decay), $\lambda \approx 0$. If immediate forgetting, $\lambda > 0.1$ min⁻¹.

**Statistical test**: Fit both exponential and linear decay models; exponential should have AIC at least 10 points lower.

#### **Result 2: Non-linear accumulation**

**Prediction**: Two errors separated by $\Delta t = 30$ min (within decay window) should produce:

$$A_{\text{peak2}} > A_{\text{peak1}} + \Delta A_{\text{isolated}}$$

**Quantification**: For $\lambda = 0.015$ min⁻¹, at $\Delta t = 30$ min:

$$e^{-\lambda \cdot 30} = e^{-0.45} \approx 0.64$$

So 64% of the first error's impact remains, creating ~1.6× the response of an isolated error.

**Statistical test**: Paired t-test comparing second-error responses in clustered vs. isolated conditions.

#### **Result 3: Negativity asymmetry**

**Prediction**: $w_{\text{error}} / w_{\text{success}} \approx 2-3$

**Measurement**: Inject both errors (negative events) and successful assists (positive events) of equivalent kinematic magnitude. Fit separate weights.

**Statistical test**: Likelihood ratio test comparing model with $w_{\text{error}} = w_{\text{success}}$ vs. $w_{\text{error}} \neq w_{\text{success}}$.

#### **Result 4: Individual differences in $\lambda$ correlate with HRV recovery**

**Prediction**: Participants with slower HRV recovery (measured independently) should show lower $\lambda$ in anxiety model.

**Statistical test**: Pearson correlation between HRV recovery half-life and $1/\lambda$, predicted $r > 0.6$.

---

### 5.3 Model Comparison

We compare the unified model against existing HRI trust models:

| Model | Structure | Parameters | Predictions |
|-------|-----------|------------|-------------|
| **Lee & See (2004)** [5] | Bayesian belief updating | Initial trust, learning rate | No temporal decay; each error independent |
| **Hancock et al. (2011)** [6] | Meta-analysis factors | Multiple static factors | No dynamics; only cross-sectional |
| **Desai et al. (2013)** [26] | Exponential trust decay | Trust baseline, decay rate | Captures decay but not accumulation |
| **Unified model (ours)** | Precision-weighted accumulation | $A_{\text{baseline}}, \lambda, w_i, U_i$ | Accumulation + decay + surprise |

**Key differentiator**: Only the unified model predicts that **error timing matters** (errors within $3/\lambda$ compound non-linearly).

**Quantitative test**: Compare AIC/BIC across models when fitted to the same data. Unified model should outperform by $\Delta \text{AIC} > 20$.

---

## 6. Part V: Applications to Adaptive HRI

### 6.1 Real-Time Anxiety Estimation

**Challenge**: The model requires knowing $A(t)$, but directly measuring anxiety continuously is impractical.

**Solution**: Use HRV as a proxy:

$$\text{HRV}(t) \approx \frac{\text{HRV}_{\text{max}}}{1 + k \cdot A(t)}$$

Invert to estimate anxiety:

$$\hat{A}(t) = \frac{1}{k}\left(\frac{\text{HRV}_{\text{max}}}{\text{HRV}(t)} - 1\right)$$

Calibrate $k$ and $\text{HRV}_{\text{max}}$ per user during a baseline period.

**Implementation**: 
- Measure HRV with chest strap or wrist sensor
- Compute 5-minute rolling RMSSD
- Update $\hat{A}(t)$ every 30 seconds

### 6.2 Adaptive Control Strategies

#### **Strategy 1: Error Spacing**

**Principle**: Prevent accumulation by ensuring errors are spaced beyond the decay window.


#### **Strategy 2: Anxiety-Dependent Autonomy**

**Principle**: Reduce robot autonomy when $A(t)$ is elevated.


#### **Strategy 3: Predictability Enhancement**

**Principle**: Reduce surprise ($U_i$) by making robot behavior more predictable.

**Implementation**:
- Provide advance warnings before autonomous actions
- Use consistent movement patterns
- Display confidence indicators

**Prediction**: Should reduce $U_i$ by ~30-50%, thereby reducing total anxiety accumulation.

### 6.3 Personalization

**Challenge**: Parameters vary across individuals (different $\lambda$, $w_i$, $A_{\text{baseline}}$).

**Solution**: Hierarchical Bayesian calibration [39]:

1. **Population priors**: $\lambda \sim \mathcal{N}(0.015, 0.005)$, $w_i \sim \mathcal{N}(2.5, 0.5)$
2. **Individual posteriors**: Update using first 10-20 minutes of interaction
3. **Adaptive updating**: Continue refining estimates over long-term use

**Software architecture**:
```
User Profile {
    A_baseline: float  // from STAI-T or learned
    lambda: float      // from HRV recovery or learned
    w_error: float     // from behavioral responses
    beta: float        // unexpectedness sensitivity
}
```

---

## 7. Discussion

### 7.1 Theoretical Implications

The convergence of empirical and theoretical derivations has several implications:

#### **7.1.1 Anxiety as Bounded Inference**

The model reveals anxiety not as irrational excess but as **inference under constraints**:
- Finite memory (exponential decay)
- Asymmetric costs (negativity bias)
- Noisy observations (surprise weighting)

From this view, anxious responses are adaptive in genuinely volatile environments but maladaptive when environmental stability is misestimated.

#### **7.1.2 The Curse of Precision**

The positive feedback loop ($w_i$ depends on $A(t)$, which depends on $w_i$) explains the "runaway" nature of anxiety disorders: once initiated, hyper-precision becomes self-perpetuating. This suggests interventions should target precision calibration rather than simply providing safety signals.

#### **7.1.3 Temporal Scale Separation**

The model operates on timescales of **minutes to hours** (matching cortisol/HRV dynamics), distinct from:
- **Millisecond-scale**: Startle reflexes, orienting responses
- **Day-scale**: Mood, depression

This middle timescale is precisely where HRI unfolds, making the model ecologically appropriate.

### 7.2 Practical Implications for HRI Design

#### **7.2.1 Error Tolerance is Time-Dependent**

A robot that makes 10 small errors over 5 hours is vastly preferable to one that makes the same 10 errors in 30 minutes. Current HRI metrics (e.g., "total error count") miss this critical temporal structure.

**Design guideline**: Budget errors over time, not just in total count.

#### **7.2.2 Predictability > Perfection**

A robot with consistent 5° errors is less anxiety-inducing than one that is usually perfect but occasionally makes 5° errors. The latter has higher surprise ($U_i$).

**Design guideline**: Prioritize consistent, predictable behavior over maximizing peak performance.

#### **7.2.3 Recovery Periods are Non-Negotiable**

Users need ~90-150 minutes (3/$\lambda$) to fully recover from significant errors. Continuous operation without recovery periods will inexorably accumulate anxiety.

**Design guideline**: Enforce mandatory rest periods or handoff to backup systems.

### 7.3 Limitations and Future Directions

#### **7.3.1 Current Limitations**

1. **Static parameters**: We assume $\lambda$, $w_i$ are constant, but they likely adapt with learning and context.

2. **Simplified surprise**: The $U_i$ model captures temporal unexpectedness but not other forms (e.g., violations of semantic expectations).

3. **No explicit safety signals**: The model accumulates negative events but doesn't explicitly represent positive evidence that reduces anxiety.

4. **Individual differences**: While we account for trait anxiety ($A_{\text{baseline}}$), the model doesn't capture other relevant factors (neuroticism, previous trauma, domain expertise).

#### **7.3.2 Recommended Extensions**

**Extension 1: Dynamic precision with hierarchical volatility estimation**

Replace static $w_i$ with:

$$w_i(t) = w_{\text{baseline}} \cdot [1 + \beta \cdot A(t_i^-)] \cdot [1 + \gamma \cdot \hat{\omega}(t)]$$

where $\hat{\omega}(t)$ is estimated environmental volatility from a Hierarchical Gaussian Filter [40].

**Extension 2: Safety signal integration**

Add an antagonistic term:

$$A(t) = A_{\text{baseline}} + \sum_i w_i^- S_i^- e^{-\lambda(t-t_i)} - \sum_j w_j^+ S_j^+ e^{-\lambda^+(t-t_j)}$$

where $S_j^+$ are positive safety signals (successful interactions, explicit reassurance).

**Hypothesis**: $\lambda^+ < \lambda^-$ (safety signals decay faster than threat signals), explaining the asymmetry observed in fear extinction [41].

**Extension 3: Meta-learning of $\lambda$**

Model $\lambda$ as adapting based on environmental statistics:

$$\frac{d\lambda}{dt} = \eta \left(\lambda_{\text{optimal}}(\omega) - \lambda(t)\right)$$

In stable environments, $\lambda$ should increase (faster forgetting). In volatile environments, $\lambda$ should decrease (longer memory).

**Extension 4: Multi-modal fusion**

Integrate multiple physiological signals:

$$A(t) = \text{fusion}(\text{HRV}(t), \text{EDA}(t), \text{EMG}(t), \text{pupil}(t))$$

Using Kalman filtering or learned weights to combine modalities.

### 7.4 Broader Implications

#### **7.4.1 Computational Psychiatry**

The model provides a **mechanistic bridge** between:
- Clinical measures (STAI, GAD-7)
- Physiological biomarkers (HRV, cortisol)
- Computational constructs (precision, free energy)

This could enable:
- Objective anxiety phenotyping
- Personalized intervention timing
- Computational treatment targets (e.g., precision reweighting via neurofeedback)

#### **7.4.2 Human-AI Interaction Beyond Robotics**

The model generalizes to any human-AI system where:
- Errors occur discretely
- Users form expectations
- Trust/anxiety evolves dynamically

Applications include:
- Autonomous vehicles (unexpected maneuvers)
- Medical AI (diagnostic errors)
- Conversational agents (misunderstandings)

#### **7.4.3 Quantitative Ethics**

By formalizing the psychological cost of robot errors, the model enables **ethical cost-benefit analysis**:

- What is the anxiety cost of deploying a 95% accurate vs. 99% accurate system?
- How much does error clustering increase total harm beyond simple error counts?
- What recovery time is ethically required after serious errors?

These become answerable quantitative questions rather than vague ethical appeals.

---

## 8. Conclusion

We have presented a unified computational model of anxiety accumulation in human-robot interaction, derived independently from:

1. **Biological time constants** (cortisol decay, HRV recovery)
2. **Behavioral economics** (loss aversion, negativity bias)
3. **Fear conditioning** (predictability, expectancy violation)
4. **Free Energy Principle** (precision-weighted Bayesian surprise)

The convergence of these derivations on an identical mathematical structure—precision-weighted, temporally discounted accumulation of surprise—provides strong evidence that the model captures fundamental principles of affective dynamics.

**Key contributions**:

- **Mechanistic grounding**: Every parameter has both empirical measurement methods and theoretical interpretation
- **Testable predictions**: The model generates specific, falsifiable predictions about error timing, individual differences, and intervention efficacy
- **Practical applicability**: Real-time anxiety estimation and adaptive control strategies
- **Theoretical unification**: Bridges computational psychiatry, stress physiology, and HRI

The model's dual derivation exemplifies mature computational neuroscience: neither pure data-fitting nor untethered theory, but the convergence of empirical constraint and normative principle. This approach not only validates the specific model but also demonstrates a methodology for developing scientifically rigorous affective computing systems.

Future work will empirically validate the model's parameters, test its predictive power against alternative frameworks, and extend it to incorporate dynamic precision, hierarchical volatility estimation, and safety signal integration. The ultimate goal is adaptive robotic systems that don't merely react to user state but anticipate and prevent anxiety accumulation through principled, computationally grounded design.

---

## References

[1] Ajoudani, A., Zanchettin, A. M., Ivaldi, S., Albu-Schäffer, A., Kosuge, K., & Khatib, O. (2018). Progress and prospects of the human-robot collaboration. *Autonomous Robots*, *42*(5), 957-975.

[2] Beckerle, P., Salvietti, G., Unal, R., Prattichizzo, D., Rossi, S., Castellini, C., ... & Bianchi, M. (2017). A human-robot interaction perspective on assistive and rehabilitation robotics. *Frontiers in Neurorobotics*, *11*, 24.

[3] Desai, M., Kaniarasu, P., Medvedev, M., Steinfeld, A., & Yanco, H. (2013). Impact of robot failures and feedback on real-time trust. In *Proceedings of the 8th ACM/IEEE International Conference on Human-Robot Interaction* (pp. 251-258).

[4] Robinette, P., Li, W., Allen, R., Howard, A. M., & Wagner, A. R. (2016). Overtrust of robots in emergency evacuation scenarios. In *2016 11th ACM/IEEE International Conference on Human-Robot Interaction* (pp. 101-108).

[5] Lee, J. D., & See, K. A. (2004). Trust in automation: Designing for appropriate reliance. *Human Factors*, *46*(1), 50-80.

[6] Hancock, P. A., Billings, D. R., Schaefer, K. E., Chen, J. Y., De Visser, E. J., & Parasuraman, R. (2011). A meta-analysis of factors affecting trust in human-robot interaction. *Human Factors*, *53*(5), 517-527.

[7] Liu, P., Galla, S., & Sarkar, N. (2016). Human-robot relationship state estimation using physiological signals. In *2016 IEEE International Conference on Automation Science and Engineering* (pp. 274-279).

[8] McEwen, B. S. (1998). Protective and damaging effects of stress mediators. *New England Journal of Medicine*, *338*(3), 171-179.

[9] Thayer, J. F., & Lane, R. D. (2009). Claude Bernard and the heart-brain connection: Further elaboration of a model of neurovisceral integration. *Neuroscience & Biobehavioral Reviews*, *33*(2), 81-88.

[10] Friston, K. (2010). The free-energy principle: A unified brain theory? *Nature Reviews Neuroscience*, *11*(2), 127-138.

[11] Clark, A. (2013). Whatever next? Predictive brains, situated agents, and the future of cognitive science. *Behavioral and Brain Sciences*, *36*(3), 181-204.

[12] Feldman, H., & Friston, K. J. (2010). Attention, uncertainty, and free-energy. *Frontiers in Human Neuroscience*, *4*, 215.

[13] Paulus, M. P., & Stein, M. B. (2006). An insular view of anxiety. *Biological Psychiatry*, *60*(4), 383-387.

[14] McEwen, B. S., & Stellar, E. (1993). Stress and the individual: Mechanisms leading to disease. *Archives of Internal Medicine*, *153*(18), 2093-2101.

[15] Schlotz, W., Hellhammer, J., Schulz, P., & Stone, A. A. (2004). Perceived work overload and chronic worrying predict weekend-weekday differences in the cortisol awakening response. *Psychosomatic Medicine*, *66*(2), 207-214.

[16] Thayer, J. F., Åhs, F., Fredrikson, M., Sollers III, J. J., & Wager, T. D. (2012). A meta-analysis of heart rate variability and neuroimaging studies: Implications for heart rate variability as a marker of stress and health. *Neuroscience & Biobehavioral Reviews*, *36*(2), 747-756.

[17] Spielberger, C. D. (1983). *Manual for the State-Trait Anxiety Inventory (STAI)*. Palo Alto, CA: Consulting Psychologists Press.

[18] Kirschbaum, C., & Hellhammer, D. H. (1994). Salivary cortisol in psychoneuroendocrine research: Recent developments and applications. *Psychoneuroendocrinology*, *19*(4), 313-333.

[19] Dickerson, S. S., & Kemeny, M. E. (2004). Acute stressors and cortisol responses: A theoretical integration and synthesis of laboratory research. *Psychological Bulletin*, *130*(3), 355-391.

[20] Houtveen, J. H., Rietveld, S., & de Geus, E. J. (2002). Contribution of tonic vagal modulation of heart rate, central respiratory drive, respiratory depth, and respiratory frequency to respiratory sinus arrhythmia during mental stress and physical exercise. *Psychophysiology*, *39*(4), 427-436.

[21] Grillon, C., Baas, J. P., Lissek, S., Smith, K., & Milstein, J. (2004). Anxious responses to predictable and unpredictable aversive events. *Behavioral Neuroscience*, *118*(5), 916-924.

[22] Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, *47*(2), 263-291.

[23] Baumeister, R. F., Bratslavsky, E., Finkenauer, C., & Vohs, K. D. (2001). Bad is stronger than good. *Review of General Psychology*, *5*(4), 323-370.

[24] LeDoux, J. E. (2000). Emotion circuits in the brain. *Annual Review of Neuroscience*, *23*(1), 155-184.

[25] Paulus, M. P., Rogalsky, C., Simmons, A., Feinstein, J. S., & Stein, M. B. (2003). Increased activation in the right insula during risk-taking decision making is related to harm avoidance and neuroticism. *NeuroImage*, *19*(4), 1439-1448.

[26] Desai, M., Stubbs, K., Steinfeld, A., & Yanco, H. (2009). Creating trustworthy robots: Lessons and inspirations from automated systems. In *Proceedings of the AISB Convention: New Frontiers in Human-Robot Interaction*.

[27] Grillon, C. (2002). Startle reactivity and anxiety disorders: Aversive conditioning, context, and neurobiology. *Biological Psychiatry*, *52*(10), 958-975.

[28] Maier, S. F., & Seligman, M. E. (2016). Learned helplessness at fifty: Insights from neuroscience. *Psychological Review*, *123*(4), 349-367.

[29] Donchin, E., & Coles, M. G. (1988). Is the P300 component a manifestation of context updating? *Behavioral and Brain Sciences*, *11*(3), 357-374.

[30] Friston, K., Kilner, J., & Harrison, L. (2006). A free energy principle for the brain. *Journal of Physiology-Paris*, *100*(1-3), 70-87.

[31] Friston, K. J., Daunizeau, J., Kilner, J., & Kiebel, S. J. (2010). Action and behavior: A free-energy formulation. *Biological Cybernetics*, *102*(3), 227-260.

[32] Rao, R. P., & Ballard, D. H. (1999). Predictive coding in the visual cortex: A functional interpretation of some extra-classical receptive-field effects. *Nature Neuroscience*, *2*(1), 79-87.

[33] Friston, K. (2005). A theory of cortical responses. *Philosophical Transactions of the Royal Society B: Biological Sciences*, *360*(1456), 815-836.

[34] Bishop, S. J. (2007). Neurocognitive mechanisms of anxiety: An integrative account. *Trends in Cognitive Sciences*, *11*(7), 307-316.

[35] Browning, M., Behrens, T. E., Jocham, G., O'Reilly, J. X., & Bishop, S. J. (2015). Anxious individuals have difficulty learning the causal statistics of aversive environments. *Nature Neuroscience*, *18*(4), 590-596.

[36] Friston, K. J., Daunizeau, J., & Kiebel, S. J. (2009). Reinforcement learning or active inference? *PloS One*, *4*(7), e6421.

[37] Friston, K., FitzGerald, T., Rigoli, F., Schwartenbeck, P., & Pezzulo, G. (2017). Active inference: A process theory. *Neural Computation*, *29*(1), 1-49.

[38] Davis, M., Walker, D. L., Miles, L., & Grillon, C. (2010). Phasic vs sustained fear in rats and humans: Role of the extended amygdala in fear vs anxiety. *Neuropsychopharmacology*, *35*(1), 105-135.

[39] Gelman, A., & Hill, J. (2006). *Data analysis using regression and multilevel/hierarchical models*. Cambridge University Press.

[40] Mathys, C., Daunizeau, J., Friston, K. J., & Stephan, K. E. (2011). A Bayesian foundation for individual learning under uncertainty. *Frontiers in Human Neuroscience*, *5*, 39.

[41] Lonsdorf, T. B., Menz, M. M., Andreatta, M., Fullana, M. A., Golkar, A., Haaker, J., ... & Merz, C. J. (2017). Don't fear 'fear conditioning': Methodological considerations for the design and analysis of studies on human fear acquisition, extinction, and return of fear. *Neuroscience & Biobehavioral Reviews*, *77*, 247-285.

---

## Appendix A: Notation Summary

| Symbol | Definition | Units | Typical Range |
|--------|------------|-------|---------------|
| $A(t)$ | Anxiety level at time $t$ | Arbitrary units (AU) or normalized STAI-S | 0-100 |
| $A_{\text{baseline}}$ | Trait anxiety (resting state) | STAI-T score | 20-60 |
| $\lambda$ | Decay rate constant | min⁻¹ | 0.008-0.02 |
| $w_i$ | Weighting factor for event $i$ | Dimensionless | 0.5-3.0 |
| $S_i$ | Surprise (total impact) of event $i$ | AU | 0-10 |
| $E_i$ | Error magnitude (objective) | Degrees, cm, or normalized | 0-10 |
| $U_i$ | Unexpectedness factor | Dimensionless | 1.0-2.0 |
| $C_i$ | Contextual criticality | Dimensionless | 0.5-2.0 |
| $t_i$ | Time of event $i$ | Minutes or seconds | - |
| $\Pi$ | Precision (FEP) | 1/variance | - |
| $F$ | Variational free energy | Nats or bits | - |
| $\beta$ | Unexpectedness sensitivity | Dimensionless | 0.5-1.0 |
| $\tau_{\text{expect}}$ | Expectation time window | Seconds | 30-60 |

---
