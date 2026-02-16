# Cognitive and Affective Trust in Wearable Robots

Trust in wearable robots (e.g., exoskeletons) has both **cognitive** (rational, competence-based) and **affective** (emotional, relational) components. Recent work in HRI and exoskeletons shows these layers can be influenced differently and often need distinct design strategies.

### Conceptualizations of Trust (incl. Wearables)

Wearable exoskeleton work emphasizes specifying **dimensions and sub-dimensions of trust** (e.g., predictability, supportiveness, error history) tailored to tightly coupled human–robot movement ([[#^88d9b7|Stirling et al., 2024]]). Broader theory distinguishes **multidimensional trust** (goal‑ and context‑specific) and argues that “do you trust the robot?” is too simplistic ([[#^f73670 |Kopp, 2024; Miller et al., 2021]]). Meta-analyses and reviews converge on three antecedent groups: **human**, **robot**, and **context** factors ([[#^1c6960 |Campagna & Rehm, 2024; Hancock et al., 2020]]).
#trust_factors/robot_factors/predictability #trust_factors/robot_factors/supportiveness #trust_factors/robot_factors/error 
### Cognitive vs Affective Trust: Evidence and Mechanisms ^tr-xls7v89f1

Studies explicitly separating trust types show:
#trust_factors/robot_factors/competence #trust_factors/robot_factors/performance #trust_factors/robot_factors/reliability 
- **Cognitive trust** is strongly shaped by **competence and performance reliability**; high‑competence robots yield more reliance and higher cognitive trust than low‑competence baselines ([[#^425177|Manor et al., 2025; Manor et al., 2024]]). ^cog
- **Affective trust** depends more on **social presence, attentiveness, emotional expression, promises, and aesthetics** than on raw performance ([[#^9fa605|Song et al., 2023]]; [[#^51495a|Cominelli et al., 2021]]; [[#^9603a4|Pinney et al., 2022]]; [[#^425177|Manor et al., 2024]]).
- Robot performance can raise cognitive but not affective trust, suggesting affective trust needs specific socio‑emotional cues ([[#^425177|Manor et al., 2024]]), while **attentive behavior** (turning, orienting, “being there”) boosts _both_ affective and cognitive trust even in simple non‑humanoid robots ([[#^425177|Manor et al., 2024]]). ^tr-oed161vai

### Wearable Robots and Psycho‑Affective Factors

For lower-limb exoskeletons, **anxiety, cognitive reserve, and identification with the device** **predict workload** and **perceived usability**, indicating that affective and cognitive user states shape acceptance and “bonding” with the wearable ([[Human–Robot Interactions A Pilot Study of Psychoaffective and Cognitive Factors to Boost the Acceptance and Usability of Assistive Wearable Devices|Bertuccelli et al., 2025]]). ^y

Trust-related dimensions for exoskeletons such as **predictability** and **supportiveness** degrade with controller errors, directly targeting cognitive trust in safety and performance ([[#^88d9b7|Stirling et al., 2024]]). #robot/lower_limb #cognitive/anxiety #cognitive/cognitive_reserve #trust_factors/robot_factors/predictability  #trust_factors/robot_factors/supportiveness 
### Methods to Assess Trust Layers ^tr-fqizb0v7w

Questionnaires are still dominant, but work is moving to **behavioral, physiological, and real‑time models** (e.g., heart rate, skin temperature, Bayesian and reinforcement‑learning based trust models) to capture dynamic, layered trust, including affect-influenced components ([[#^1c6960|Campagna & Rehm, 2024]]; [[#^422ac7|Alzahrani, 2025]]; [[#^b4dc12|Guo & Yang, 2020]]; [[#^8fe166|Miller et al., 2021]]). #measures/subjective_measures 

### Summary

Current research suggests that for wearable robots, **cognitive trust** is built primarily via consistent, transparent performance and error handling, while **affective trust** requires deliberate socio‑emotional design (attentiveness, expressive cues, aesthetics) and management of anxiety and identification. 
**Effective exoskeleton and wearable-robot design likely needs to engineer and measure both layers explicitly, using multidimensional and dynamic assessment rather than a single global “trust” score.**
#trust_definition/affective_trust
#trust_definition/cognitive_trust

## References

Stirling, L., Wu, M., & Peng, X. (2024). [[Measuring Trust for Exoskeleton Systems]]. _ArXiv_, abs/2407.07200. [https://doi.org/10.48550/arxiv.2407.07200](https://doi.org/10.48550/arxiv.2407.07200) ^88d9b7

Song, Y., Tao, D., & Luximon, Y. (2023). In robot we trust? The effect of emotional expressions and contextual cues on anthropomorphic trustworthiness.. _Applied ergonomics_, 109, 103967. [https://doi.org/10.1016/j.apergo.2023.103967](https://doi.org/10.1016/j.apergo.2023.103967) ^9fa605

Cominelli, L., Feri, F., Garofalo, R., Giannetti, C., Meléndez-Jiménez, M., Greco, A., Nardelli, M., Scilingo, E., & Kirchkamp, O. (2021). Promises and trust in human–robot interaction. _Scientific Reports_, 11. [https://doi.org/10.1038/s41598-021-88622-9](https://doi.org/10.1038/s41598-021-88622-9) ^51495a

Kopp, T. (2024). Facets of Trust and Distrust in Collaborative Robots at the Workplace: Towards a Multidimensional and Relational Conceptualisation. _International Journal of Social Robotics_, 16, 1445 - 1462. [https://doi.org/10.1007/s12369-023-01082-1](https://doi.org/10.1007/s12369-023-01082-1) ^f73670

Campagna, G., & Rehm, M. (2024). A Systematic Review of Trust Assessments in Human–Robot Interaction. _ACM Transactions on Human-Robot Interaction_, 14, 1 - 35. [https://doi.org/10.1145/3706123](https://doi.org/10.1145/3706123) ^1c6960

Alzahrani, A. (2025). Measuring Human’s Trust in Robots in Real-time During Human-Robot Interaction. **. [https://doi.org/10.23889/suthesis.69777](https://doi.org/10.23889/suthesis.69777) ^422ac7

Manor, A., Parush, A., & Erel, H. (2025). Trust Interplay: Robot Performance Influences Cognitive But Not Affective Trust. _2025 20th ACM/IEEE International Conference on Human-Robot Interaction (HRI)_, 1483-1487. [https://doi.org/10.1109/hri61500.2025.10974010](https://doi.org/10.1109/hri61500.2025.10974010) ^425177

Guo, Y., & Yang, X. (2020). Modeling and Predicting Trust Dynamics in Human–Robot Teaming: A Bayesian Inference Approach. _International Journal of Social Robotics_, 13, 1899 - 1909. [https://doi.org/10.1007/s12369-020-00703-3](https://doi.org/10.1007/s12369-020-00703-3) ^b4dc12

Bertuccelli, M., Tortora, S., Trombin, E., Negri, L., Bisiacchi, P., Menegatti, E., & Del Felice, A. (2025). Human-Robot Interactions: A Pilot Study of Psychoaffective and Cognitive Factors to Boost the Acceptance and Usability of Assistive Wearable Devices. _Multimodal Technol. Interact._, 9, 5. [https://doi.org/10.3390/mti9010005](https://doi.org/10.3390/mti9010005) ^d62b40

Miller, L., Kraus, J., Babel, F., & Baumann, M. (2021). More Than a Feeling—Interrelation of Trust Layers in Human-Robot Interaction and the Role of User Dispositions and State Anxiety. _Frontiers in Psychology_, 12. [https://doi.org/10.3389/fpsyg.2021.592711](https://doi.org/10.3389/fpsyg.2021.592711) ^8fe166

Pinney, J., Carroll, F., & Newbury, P. (2022). Human-robot interaction: the impact of robotic aesthetics on anticipated human trust. _PeerJ Computer Science_, 8. [https://doi.org/10.7717/peerj-cs.837](https://doi.org/10.7717/peerj-cs.837) ^9603a4

Hancock, P., Kessler, T., Kaplan, A., Brill, J., & Szalma, J. (2020). Evolving Trust in Robots: Specification Through Sequential and Comparative Meta-Analyses. _Human Factors: The Journal of Human Factors and Ergonomics Society_, 63, 1196 - 1229. [https://doi.org/10.1177/0018720820922080](https://doi.org/10.1177/0018720820922080)

Manor, A., Parush, A., & Erel, H. (2024). Attentiveness: A Key Factor in Fostering Affective and Cognitive Trust with Non-Humanoid Robots. _2024 33rd IEEE International Conference on Robot and Human Interactive Communication (ROMAN)_, 469-476. [https://doi.org/10.1109/ro-man60168.2024.10731320](https://doi.org/10.1109/ro-man60168.2024.10731320)


---
