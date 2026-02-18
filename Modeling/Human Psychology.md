# ACT-R
ACT-R, as a useful and well-known cognitive architecture, is a theory for simulating and understanding human cognition.
![[Pasted image 20260218205640.png]]

# [ACT-RΦ](https://www.researchgate.net/publication/259172584_ACT-RPH_A_cognitive_architecture_with_physiology_and_affect) 
[[ACognitiveArchitecturewithPhysiologyandAffect_BICA-63.pdf]]
- An extension that adds a **Physiology Module** to standard [ACT-R](https://act-r.psy.cmu.edu/), allowing the model to simulate things like stress, fatigue, and arousal levels.

## How ACT-RΦ Works

- **Affective Modules**: It introduces new modules like **SEEKING** and **Affective-Associations** to represent emotions and motivations.
  ![[Pasted image 20260218205940.png]]
  (Some key brain areas from the SEEKING, incentive salience, and ACT-R theories)


- **Physio Module**: This module connects ACT-R to **HumMod**, a highly detailed simulation of human physiology.
- **Bidirectional Influence**:
    - **Mind to Body**: A model’s "thoughts" or production rules can trigger physiological changes (e.g., increasing heart rate due to a stressful task).
    - **Body to Mind**: Changes in the body (like fatigue or high adrenaline) can automatically adjust cognitive parameters, such as making memory retrieval harder or increasing the "noise" in decision-making.

# A diagram of the ACT-R Φ subsystems
![[Pasted image 20260218210046.png]]
![[Screenshot 2026-02-18 at 9.04.38 PM.png]]
(source of this figure: [[1023Towards_Adding_A_Physiological_Substrate_to_ACT-R_DancyRB_Final.pdf]], [link](https://act-r.psy.cmu.edu/wordpress/wp-content/uploads/2012/12/1023Towards_Adding_A_Physiological_Substrate_to_ACT-R_DancyRB_Final.pdf))

# Where to Access the Code
**Official ACT-R Lisp Source**:  [Carnegie Mellon University ACT-R Software Page](http://act-r.psy.cmu.edu/software/).

**Official ACT-R Phi Source:** https://github.com/cld5070/act-r_phi
