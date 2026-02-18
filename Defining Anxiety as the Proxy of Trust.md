Given that trust has a neurological basis, we must combine physiological with subjective measurements in the form of big data to build a ground truth of trust ([[Books of Foundations of Trusted Autonomy & Trust in Human-Robot Interaction#^ground]]). 
While embodiment is highlighted as the future measurement system of wearable robot's success criteria ([[Embodiment for Robotic Lower-LimbExoskeletons A Narrative Review]]), there are few studies that connect physiological signals to embodiment. On the contrary, anxiety has been studied for decades with a wide variety of different objective and subjective measurement systems and well-defined biomarkers. That makes anxiety an excellent measurable criteria of success for wearable robots.

### Anxiety Definition
Anxiety is a complex cognitive, affective, physiological and behavioral response system (i.e., threat mode) ([[Cognitive Therapy of Anxiety Disorders#^692901]]). In Relational or Appraisal-based definition of anxiety, anxiety is defined as *"not just a raw emotion, but a complex, future-oriented state resulting from an individual's evaluation of their relationship with their environment"* ([Klaus et. al., 2022](https://doi.org/10.3389/fpsyg.2022.857419)). Two major appraisal criteria central to this process are **control** (whether one can influence the consequences) and **power** (whether one has sufficient ability to change outcomes).

### Predictability
Many theories, such as brain theory, define the level of surprise or unpredictability as the variable that the brain tries to minimize ([[A predictive processing perspective of disrupted motor control under anxiety#^de0b99]]).  
In trust literature, the object of the trust itself—the automation system— is described only in terms of its **reliability**, **predictability**, and **error-proneness**, as the defining factors of its performance ([[Books of Foundations of Trusted Autonomy & Trust in Human-Robot Interaction#^9d0c16]]).  
According to [[Measuring trust in real time.pdf|Stirling et al. (2024)]], trust in exoskeletons can be grouped into **purpose, process, and performance** dimensions, covering factors such as safety, reliability, dependability, accessibility, integrity, understandability, and familiarity. Despite their variety, these dimensions all converge on the deeper principle of **predictability**—users must be able to anticipate the system’s behavior and outcomes. When the exoskeleton acts consistently, transparently, and in alignment with user intentions, predictability is reinforced, making it the central foundation of trust in such systems [[Exoskeleton Trust Predictability Dimensions]].

### Safety and Risk
Perceived safety - which is different from physical safety - is crucial for long-term human-robot interaction and user acceptance especially in vulnerable settings such as healthcare domains ([[Do you feel safe with your robot? Factors influencing perceived safety in human-robot interaction based on subjective and objective measures 1#^48fe5e]]). In the context of HRI, “perceived safety” refers to the user’s perception of danger and the level of comfort when interacting with a robot ([[perceived_risk_and_safety#^3b72f7]]). [Rubagotti et al. (2022)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11076167/#R72) mentions how **trust**, **comfort**, **fear**, **anxiety**, and **surprise** affect perceived safety ([[perceived_risk_and_safety#^395243]]). However, these factors all have bidirectional effects and hard to keep track of all separately. This highlights the necessity of going back a step to the roots of all these factors to find the most prominent factor and focus on manipulating that factor for building trust in HRI.

## Psychological Aspects


### Going back to the roots: Physiology, sympathetic nervous system, introception, and neuroception
Neuroception, term from Polyvagal's theory ([[Polyvagal Theory]]), refers to the brain’s automatic detection of safety or threat without conscious awareness ([[Perception vs Neuroception Anxiety#3.1 Neuroception Unconscious Threat Detection & Anxiety Initiation]]) while Interoceptive perception involves detecting and interpreting internal bodily signals (e.g., heartbeat, breathing) ([[Perception vs Neuroception Anxiety#3.2 Interoceptive Perception Conscious Awareness & Anxiety Maintenance]]). 
Subtle cues can trigger physiological arousal or calmness **even when not consciously perceived**. [[Perception vs Neuroception Anxiety#3.1 Neuroception Unconscious Threat Detection & Anxiety Initiation]].  
In theories such as predictive processing anxiety can be defined as the negative cognitive and physiological response to threat cues ([[A predictive processing perspective of disrupted motor control under anxiety#^tr-5mh5poqjy]]). 
From a biological aspect, ongoing anxiety is driven by discrepancies between predicted **bodily states (neuroceptive models)** and **actual sensations (perceived interoception)**. ([[Perception vs Neuroception Anxiety#3.3 Neural Substrates Insula & Predictive Coding]]). That fits well with Bayesian Brain theory in neuroscience, built upon Free Energy Principle, suggesting the brain uses probabilistic, internal models to interpret uncertain sensory data and update beliefs.

Consequently, we can assume that the internal model defined in FEP, is constantly under the fundamental influence of neuroceptive models (as the internal model of the brain) and perceived introception (sensory data), all of which driving **anxiety** when encountering a surprise (i.e., unpredictability, or mismatch between the neuroception and introception).

Advanced appraisal activates specific brain areas—the medial prefrontal cortex and anterior cingulate cortex (ACC) —when we anticipate something anxiety-provoking.
Interestingly, individual differences in the tendency to trust (self-report and behaviorally) would be associated with gray matter volume within the vmPFC (a specific subregion of prefrontal cortex), amygdala and anterior insula ([[Books of Foundations of Trusted Autonomy & Trust in Human-Robot Interaction#^tr-5xflpo6il]]).

Overall schematics:
![[Pasted image 20260216235126.png]]

![[Pasted image 20260216234840.png]]

[Based on this](https://www.google.com/search?q=&sourceid=chrome&ie=UTF-8&udm=50&aep=48&cud=0&qsubts=1771249052245&source=chrome.crn.obic&mstk=AUtExfCQZBLpJBLj2E2vd1CsdEF7DSUJwXKesNxNbArSA5r_YzQzhT2c8P46gXnEmWLdHil3SJNzlFdxxOQa0laI3Mh_PsJphp0PYox2Z63ZUG-RDcIPyJ1HYPvtYSkq07x5XajIpGqtVxCWZFTAql-U8PmHNofb7Qzio8--0YsCrcxjdoEAW6HiS2Xhy9ntkfGg6E2p9hAmLdE5hBvVMj4MeNHfOHtEyPxR46O7D2eXR-b1zfZZLY7ldW7u2kqOjGl3WdTCEw87X6MFQzEJGhJiS76VZzzJkD90ASGY8apHpwXbyCp95d9xVQhBJbcYxq9F4mZbgiljoDShLA&csuir=1&mtid=nx2TaZjdOLKFwbkP9eOs4QI&lns_mode=cvst) 
(so, any trust, moves from the filter of subconscious first. so, if a threat signal, we lose our shot at developing trust at first, especially if minimum priors exist. but if safety signals keep coming, making heavier cognitive safety in the cortex, then it will eventually volume down the neuro and interoception [](https://www.google.com/search?q=can+we+trust+something+that+neuroception%2Binteroception+of+our+body+detect+as+threat+%28but+may+or+may+not+the+cortex+see+it+that+way%29&sourceid=chrome&ie=UTF-8&udm=50&aep=48&cud=0&qsubts=1771253548070&source=chrome.crn.obic&mstk=AUtExfBT4GpZw8FP30t-HBy6LEbxdvelkbFG8zNvscTK4gYyuI2-5jgc0F_dCDDp7J2qOxC7xsg6tk7XLEJVqdNfcPOeYHrmxiOnnwDp9qkIt5dgzuX5Tx0yNYeZhWsUv-xPu8IZVUGQGik-lkcmSoY19dFMJWt_fjfdfr0drDbTqCLs9uXf3gzOKh8upTpHNVHnMxmaHmrXFzpKi82V_GiSBh0cXj8uRiZBd6BrAnvJi649nMBqiW3HoXIACTQXJrpti4xjB_IPhTwd9buBNd3B2Ti68t4Ranb-_lk&csuir=1&mtid=Zy-Tab65GdOawbkPhc6ryAo))

#### How does this relate to trust?
As referenced in trust in HRI literature, trust is usually easy to lose and difficult to gain, especially when the situation is unfamiliar and fewer priors exist [Kopp, T, 2024](https://doi.org/10.1007/s12369-023-01082-1). Trust is constantly updated based on new observations that may or may not match the prior expectations. 

The higher the anxiety level, the more one's attention will become narrowly focused on a restricted range of mood-congruent stimuli, thereby causing a reduction in attentional resources remaining to process cues of nonthreat or safety ([[Cognitive Therapy of Anxiety Disorders#^bd3657]]). Trust dynamic is similarly much more affected by negative and more important, rather than positive or simpler events [Kopp, T, 2024](https://doi.org/10.1007/s12369-023-01082-1). As mentioned before, anxiety is driven by the mismatch between introception and neuroception. This fits well on the trust dynamic described in  [Kopp, T, 2024](https://doi.org/10.1007/s12369-023-01082-1), as the trust is affected by an event that is not necessarily an error or failure, but could be as simple as a mismatch of the event with the user's mental model and expectations. That being said, we can conclude that a dominant factor of the dynamic of trust is indeed anxiety, as it both affects our cognitive perception and sensory input precision to start with.

Additionally, the diminishing processing of safety due to state anxiety, causes the individuals to engage in safety-seeking behavior ([[Cognitive Therapy of Anxiety Disorders#^bd3657]]), in HRI settings this can induce behaviors in the user such as avoiding the robot, or requiring higher degrees of transparency, making it even more difficult to maintain or regain the previous higher trust level in an HRI settings, as it should constantly update its performance factors, such as level of explanation, or safety perception factors based on the user's anxiety levels.







### The effect of anxiety on other factors
As for the wearable robot settings, anxiety disrupts automatic motor control processes ([[Sensorimotor mismatch disrupts motor automaticity and increases anxiety during a goal-directedbalance task#^tr-yhrnpu7f1]], which can yield either **rigid or overly variable movements** and reduced trust in sensory feedback ([Harris et al., 2023](app://obsidian.md/index.html#^be6a7d); [Nieuwenhuys & Oudejans, 2017](app://obsidian.md/index.html#^bfab18))([[Anxiety and Proprioception#^tr-5uaqwduya]]). This is possibly due to anxiety impairing the unconscious, reflexive control processes that normally regulate coordinated movement, increasing mental effort and conscious movement monitoring ([[Sensorimotor mismatch disrupts motor automaticity and increases anxiety during a goal-directedbalance task#^tr-yhrnpu7f1]]). 





This anxiety-motor interaction aligns with the Yerkes- Dodson principle that moderate anxiety might enhance error awareness, potentially benefiting learning, while excessive anxiety could disrupt predictive coding and impair performance. Thus, anxiety induced by sensorimotor mismatch could functionally resemble maladaptive error amplification when it exceeds an individual’s challenge threshold ([[Sensorimotor mismatch disrupts motor automaticity and increases anxiety during a goal-directedbalance task#^6c32b9]]). 

