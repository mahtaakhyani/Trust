# Defining Anxiety as the Proxy of Trust

## Wearable Robotics & Human-Robot Interaction

---

## The Problem: Trust is Hard to Measure
**Trust in robotics:**

- Trust has a neurological basis, requiring combination of physiological with subjective measurements in the form of big data to build a ground truth of trust [1]
- Embodiment is highlighted as the future measurement system of wearable robot's success criteria [2], but there are few studies that connect physiological signals to embodiment in real time.

**But anxiety has:**

- Decades of research
- Well-defined biomarkers
- Established physiological signals
- Proven measurement protocols

**Opportunity:** Use anxiety as a measurable proxy for trust in wearable robots

---

## What is Anxiety?

**Cognitive-Affective-Physiological Response System**

> "Not just a raw emotion, but a complex, future-oriented state resulting from an individual's evaluation of their relationship with their environment"

### Two Critical Appraisal Dimensions

- **Control:** Can I influence the consequences?
- **Power:** Do I have sufficient ability to change outcomes?

**Key distinction:** Anxiety = future threat, not instant fear

---

## The Neurological Foundation
---
### Neuroception (Polyvagal Theory)

- Brain's **automatic** detection of safety/threat
- **Without conscious awareness**
- Triggers physiological arousal or calmness from subtle cues

### Interoceptive Perception

- Detecting internal bodily signals (heartbeat, breathing)
- **Conscious awareness** of bodily states

### The Anxiety Mechanism
> **Anxiety is driven by:**
> 
>neuroceptive models $\not\equiv$ interoception

---

## Predictability: The Common Thread

### Brain Theory

Brain minimizes surprise/unpredictability

### Trust Literature

Automation systems defined by:

- Reliability
- **Predictability** ← central factor
- Error-proneness

### Exoskeleton Trust Dimensions

Purpose, Process, Performance → all converge on **predictability**

**When systems act consistently and transparently, trust increases**

---

## The Anxiety-Trust Connection

### Why Anxiety Affects Trust So Powerfully

**Attention narrowing:**

- High anxiety → focus on threat stimuli only
- Reduces processing of safety/non-threat cues
- Makes trust harder to gain, easier to lose

**Trust dynamics:**

- More affected by negative events than positive
- Affected by mismatches with expectations (not just errors)


---

## Safety-Seeking Behavior Spiral

```
High Anxiety
    ↓
Reduced safety processing
    ↓
Safety-seeking behaviors:
  • Robot avoidance
  • Demanding transparency
  • Hypervigilance
    ↓
Harder to regain trust
    ↓
System must constantly adapt
```

---

**Implication:** 

Anxiety is the dominant factor driving trust dynamics 

and the controller requires constant updating based on anxiety levels

---

## Anxiety Disrupts Motor Control

**In wearable robots:**

- Impairs automatic motor processes
- Yields rigid OR overly variable movements
- Reduces trust in sensory feedback
- Increases conscious monitoring (mental effort)
---
![[CBT fig. 1.1..png]]
---
### Yerkes-Dodson Principle

- Moderate anxiety → enhanced error awareness → better learning
- Excessive anxiety → disrupted predictive coding → impaired performance

**Anxiety × Motor interaction = Critical design consideration**

---
## Core Hypothesis

### Three Key Claims

1. **Anxiety and trust dynamics are mirror images**
    
    - Show nearly identical temporal patterns
    - Independent of non-anxiety trust factors
2. **All trust factors root back to anxiety**
    
    - Trust can be safely defined, measured, and controlled through anxiety
3. **Sensory signals drive trust**
    
    - Physiological (neuroception) + cognitive signals are core drivers
    - Not just subjective evaluations

---


## Critical Experimental Questions

### Q1: How to Create Anxiety (Not Just Fear)?

**Two-Test Method:**

1. **Baseline Test**
    
    - Measure biomarkers before robot encounter
    - Elevated levels = "hidden state" anxiety
2. **Persistence Test**
    
    - Biomarkers remain high throughout second wear?
    - → Generalized anxiety, not situational stress

**Key indicator:** Anticipatory anxiety from threat memory

---

## Critical Experimental Questions (cont.)

### Q2: Prove It's Anxiety, Not Something Else

**Method 1: Neutral Task Performance**

- User performs unrelated task (e.g., reaction time game)
- While wearing vs. not wearing robot
- Performance drop + elevated biomarkers = anxious hypervigilance
- Trust loss alone shouldn't affect unrelated tasks
---

**Method 2: Biomarker Signature Differentiation**


|Anxiety Signature|Trust Loss Signature|
|---|---|
|Lowered HRV|Increased pupil dilation|
|Increased phasic EDA|Specific EEG bands|
|Fear-based HR spikes|Mental workload markers|
|Defensive state|Monitoring state|

---
Common Features of Anxiety

| Physiological symptoms                   | Cognitive symptoms                                    |
| ---------------------------------------- | ----------------------------------------------------- |
| (1) Increased heart rate, palpitations   | (1) Fear of losing control, being unable to cope      |
| (2) Shortness of breath, rapid breathing | (2) Fear of physical injury or death                  |
| (3) Chest pain or pressure               | (3) Fear of "going crazy"                             |
| (4) Choking sensation                    | (4) Fear of negative evaluation by others             |
| (5) Dizzy, lightheaded                   | (5) Frightening thoughts, images, or memories         |
| (6) Sweaty, hot flashes, chills          | (6) Perceptions of unreality or detachment            |
| (7) Nausea, upset stomach, diarrhea      | (7) Poor concentration, confusion, distractible       |
| (8) Trembling, shaking                   | (8) Narrowing of attention, hypervigilance for threat |
| (9) Tingling or numbness in arms, legs   | (9) Poor memory                                       |
| (10) Weakness, unsteady, faintness       | (10) Difficulty in reasoning, loss of objectivity     |
| (11) Tense muscles, rigidity             |                                                       |
| (12) Dry mouth                           |                                                       |

---


| Behavioral symptoms                             | Affective symptoms                                      |
|-------------------------------------------------|---------------------------------------------------------|
| (1) Avoidance of threat cues or situations      | (1) Nervous, tense, wound-up                            |
| (2) Escape, flight                              | (2) Frightened, fearful, terrified                      |
| (3) Pursuit of safety, reassurance              | (3) Edgy, jumpy, jittery                                |
| (4) Restlessness, agitation, pacing             | (4) Impatient, frustrated                               |
| (5) Hyperventilation                            |                                                         |
| (6) Freezing, motionless                        |                                                         |
| (7) Difficulty speaking                         |                                                         |

---

## Experimental Design Components

### 1. Task Setup

- What scenario/context?

### 2. Subject Selection

- Age, health, gender, baseline anxiety
- Individual response variation
- Target user demographics (elderly? patients? athletes?)

---

### 3. Anxiety Stimulation

**Oddball tactile events:**

- Spatial deviance (location shifts)
- Intensity/quality changes
- Omission (expected stimulus missing)

**Requirements:**

- Induce anxiety specifically (not just fear/stress)
- Controlled frequency
- Stimulus variation strategy

---

## Measurement Strategy

### Objective Measures

**Empatica E4 Wristband (~$1000)**

- PPG-derived IBIs
- Heart rate
- Temperature
- Electrodermal activity (EDA)
- Movement

**EEG Options**

 **NeuroSky MindWave Mobile (~130$)**
---

 
**UMind Mirror (300$)**
- 1 in diameter - weighing less than a US quarter
- development SDK provides complete access to developers, supporting drivers, APIs, and analysis tools for EEG research applications 
- AI EEG analysis
- a meditation report of the brain relaxation state
- measures activity in all cortical lobes of the brain
- 10 hours full charge
---

### Subjective Measures

Self-report scales, questionnaires

**Integration:** How to combine multi-modal signals into meaningful metrics?

---

## Finding the Anxiety ∝ Trust Dynamic

### Analysis Goals

1. Demonstrate temporal correlation
2. Show causal relationship
3. Quantify the proportional relationship
4. Account for individual differences

### Measurement Frequency

- Real-time continuous monitoring?
- Event-triggered sampling?
- Balance feasibility vs. granularity

---

## Utilizing This Dynamic

### Control vs. Feedback?

**Option A: Anxiety as Feedback Signal**

- Robot adapts behavior based on detected anxiety
- Reduces anxiety-inducing stimuli
- Increases predictability/transparency

**Option B: Anxiety as Control Signal**

- Maintain optimal anxiety level (Yerkes-Dodson zone)
- Create/reduce stimuli strategically
- Balance challenge and safety

**Design question:** Which approach for which context?

---

## Key Takeaways

1. **Anxiety has the neurological grounding while trust is context-dependant**
    
2. **Predictability is the common denominator** across trust factors
    
3. **Neuroception + interoception mismatch** drives anxiety and trust loss
    
4. **Anxiety can be measured objectively** with established biomarkers
    
5. **Trust dynamics mirror anxiety dynamics** in wearable HRI
    
6. **Managing anxiety = managing trust** in wearable robots
    


---

## Conclusion
By treating anxiety as the physiological substrate of trust, we can:

- Ground trust research in neuroscience
- Enable real-time measurement
- Create adaptive systems
- Improve long-term human-robot relationships

**The path to trust runs through the autonomic nervous system**

---
## References
1. [[Books of Foundations of Trusted Autonomy & Trust in Human-Robot Interaction#^ground]]
2. [[Embodiment for Robotic Lower-LimbExoskeletons A Narrative Review]]
3. [[Cognitive Therapy of Anxiety Disorders#^692901]]
4. [Klaus et. al., 2022](https://doi.org/10.3389/fpsyg.2022.857419)
5. [[A predictive processing perspective of disrupted motor control under anxiety#^de0b99]]
6. [[Books of Foundations of Trusted Autonomy & Trust in Human-Robot Interaction#^9d0c16]]
7. [[Measuring trust in real time.pdf]]
8. [[Exoskeleton Trust Predictability Dimensions]]
9. [[Do you feel safe with your robot? Factors influencing perceived safety in human-robot interaction based on subjective and objective measures 1#^48fe5e]]
10. [[perceived_risk_and_safety#^3b72f7]]
11. [Rubagotti et al. (2022)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11076167/#R72)
12. [[Polyvagal Theory]]
13. [[Perception vs Neuroception Anxiety#3.2 Interoceptive Perception Conscious Awareness & Anxiety Maintenance]]