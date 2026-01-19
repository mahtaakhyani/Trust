## Anxiety in the Bayesian Brain and the Free Energy Principle (FEP)

In the context of the Bayesian Brain and the Free Energy Principle (FEP), researchers such as Friston, Clark, and Edwards describe anxiety as a failure in the brain's *inference engine* to properly manage uncertainty. While the 2012 collaboration by these authors (notably Edwards et al., 2012) primarily focused on functional “hysterical” symptoms, the broader framework applies to anxiety through the following mechanisms.

---

## 1. Learned Uncertainty

Anxiety is conceptualized as **learned uncertainty**, where a biological system that has faced persistent uncertainty in the past *expects* uncertainty in the future, regardless of whether it actually exists. This creates a state where the brain is constantly anticipating high-surprise outcomes.

---

## 2. Aberrant Encoding of Precision

The FEP suggests that the brain balances its internal prior beliefs (expectations) against sensory evidence (bottom-up signals). In anxious states, there is an **aberrant encoding of precision**—the mathematical confidence assigned to these signals:

- **Over-precision of Threat**  
  The brain may assign too much *weight* or precision to sensory signals that suggest threat.

- **Precision and Attention**  
  Anxiety is seen as a disruption in the neuromodulatory mechanisms (such as dopamine or norepinephrine) that regulate attention and the gain of neurons reporting prediction errors.

---

## 3. Failure of Active Inference

To minimize free energy (surprise), the brain uses **active inference**: changing its environment or its perception to match its internal model.

- **Uncertainty about Action**  
  In anxiety, there is *discerned uncertainty* about whether any action will successfully minimize future uncertainty.

- **Maladaptive Cycles**  
  This leads to a breakdown where the system cannot find *attractor states* (homeostasis), resulting in persistent free energy that manifests as psychological distress.

---

## 4. Hierarchical Prediction Errors

The brain is a hierarchical prediction machine. Anxiety occurs when high-level predictions (e.g., *“I am in danger”*) dominate the hierarchy, forcing the system to interpret even neutral sensory data as evidence of threat in order to minimize prediction error within that specific (though flawed) model.

---

## The Mathematical Framework of Anxiety

While the seminal 2012 paper by Edwards et al. primarily provides a conceptual hierarchical Bayesian model for functional symptoms, subsequent research has formalized these mechanics.

---

## 1. Variational Free Energy ($F$)

Anxiety is modeled as the persistent inability to minimize **Variational Free Energy**, which serves as an upper bound on surprise (surprisal):

$$
F \ge -\ln p(o)
$$

The standard decomposition is:

$$
F
= \underbrace{D_{\mathrm{KL}}\!\left[q(s)\,\|\,p(s)\right]}_{\text{Complexity}}
- \underbrace{\mathbb{E}_{q(s)}\!\left[\ln p(o \mid s)\right]}_{\text{Accuracy}}
$$

**Anxiety application**  
In anxiety, the *complexity* term is inflated because threat-related priors $p(s)$ are rigid and resistant to updating, even when observations $o$ indicate safety.

---

## 2. Precision-Weighted Prediction Error (PWPE)

Prediction errors are weighted by their expected precision:

$$
\Delta q \propto \Pi \, \epsilon
$$

where:

- $\epsilon = o - \hat{o}$ is the prediction error  
- $\Pi = \Sigma^{-1}$ is precision (inverse variance)

**Anxiety modeling**

- Hyper-precision: $\Pi \uparrow$ on threat-related priors  
- Hypo-precision: $\Pi \downarrow$ on sensory evidence of safety  

This imbalance prevents corrective updating and stabilizes anxiety.

---

## 3. Expected Free Energy ($G$) and Action

Expected Free Energy governs policy selection under active inference:

$$
G(\pi)
\approx
\sum_{\tau}
\mathbb{E}_{q(o_\tau, s_\tau \mid \pi)}
\left[
\ln q(s_\tau \mid \pi)
-
\ln p(o_\tau, s_\tau)
\right]
$$

**Anxiety application**  
When no policy $\pi$ sufficiently reduces ambiguity and risk, the agent experiences persistent learned uncertainty—failure to reach a homeostatic attractor.

---

## Key Papers for the Mathematics

- **Edwards et al. (2012)** — Precision-weighting in functional symptoms  
- **Friston (2010)** — Formal derivation of the Free Energy Principle  
- **Ramstead et al. (2022)** — Anxiety as expected future uncertainty  

---

## Anxiety as Accumulated Free Energy

Anxiety is not a scalar but an accumulation of unresolved surprise over time.

---

## 1. Core Anxiety Accumulation

Anxiety level $A(t)$ is modeled as the integral of the rate of change of free energy:

$$
A(t)
=
\int_0^t \frac{dF}{d\tau} \, d\tau
+
A_{\text{prior}}
$$

- $\frac{dF}{d\tau} > 0$ → anxiety accumulates  
- $\frac{dF}{d\tau} < 0$ → anxiety dissipates  

---

## 2. Precision-Weighted Accumulation

The intensity of accumulation scales with precision:

$$
A \propto \Pi \, (o - \hat{o})^2
$$

- High $\Pi$ → rapid escalation  
- Learned uncertainty → elevated baseline precision  

---

## 3. Anticipatory Anxiety (Future Free Energy)

Generalized anxiety corresponds to Expected Free Energy:

$$
G = \text{Risk} + \text{Ambiguity}
$$

- **Risk**: divergence from preferred outcomes  
- **Ambiguity**: uncertainty about state–action mappings  

---

## Summary of the Anxiety State Model

| Term | Mathematical Meaning | Clinical Manifestation |
|-----|----------------------|------------------------|
| $F$ | Immediate surprise | Acute stress / panic |
| $\Pi \epsilon$ | Gain on prediction error | Hypervigilance |
| $\int dF/dt$ | Accumulation | Sustained anxiety |
| $G$ | Future surprise | Worry / apprehension |

---

## Dynamic Anxiety Accumulation Model

The full dynamical system is:

$$
\frac{dA(t)}{dt}
=
\Pi(t)\, S(t)
-
\alpha A(t)
$$

where:

- $S(t) = -\ln p(o_t)$ is surprisal  
- $\Pi(t)$ is time-varying precision  
- $\alpha$ is the regulatory decay rate  

---

### Integrated Solution

$$
A(t)
=
A(0) e^{-\alpha t}
+
\int_0^t
e^{-\alpha (t-\tau)}
\, \Pi(\tau)\, S(\tau)
\, d\tau
$$

---

## Feedback Loop

Precision is often a function of anxiety itself:

$$
\Pi = \Pi(A)
$$

This yields a positive feedback loop:

1. Surprise $\uparrow \Rightarrow A \uparrow$  
2. Anxiety $\uparrow \Rightarrow \Pi \uparrow$  
3. Precision $\uparrow \Rightarrow$ future surprise amplified  

This mechanism explains the nonlinear escalation and persistence of anxiety.
