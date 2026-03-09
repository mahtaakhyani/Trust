## System Structure

![[system_diagram.svg|697]]
---

## Anxiety Module

It takes these variables as input to initiate an Anxiety class instance:

1. Anxiety baseline ($A_\text{baseline}$) -> individual's baseline anxiety

2. Negativity Bias ($W_i$) -> negative events are weighted 2-3x more heavily than positive events

where:

- For errors/failures: $w_e$ ≈ 2 to 3

- For successes: $w_s$ ≈ 0.5 to 1

- For neutral events: $w_n$ ≈ 0

It takes these variables to update the Anxiety class instance:

1. Time of the signal (t)

2. Signal impact aka "Surprise" ($S_i$): 
					 $S_i = E_i * U_i * R_i$

where:

- $E_i$: Objective kinematic error **magnitude** (e.g., degrees of angular deviation, cm of position error)
	* Magnitude is captured through **jerk** of the specific event
	
- $U_i$: Unexpectedness factor
	* Unexpectedness is measured through: Kurtosis formula?

- R_i: Contextual criticality/risk factor

3. Decay constant ($\lambda$) →  how fast the effect of the signal naturally decays in time for the user (loss is faster than gain, riskier events is slower)

  

The model is built upon the following phrases:

* Anxiety decay expression: e^{-lambda*(t - t_i)} (Leacky integrator model)

* The perceived strength of the stressor: w_i * S_i * R_i

* The non-linearity expression of the cumulative physiological cost of the stressors: ∑_i=1^n

  

Full model:

$A(t) = A_\text{baseline} + ∑_i [(w_i \cdot E_i \cdot U_i \cdot R_i) \cdot e^{-\lambda \cdot (t - t_i)}]$

  

This module also keeps a history of all the anxiety levels and stressors.
---

## Anxiety Model

![[system_diagram.svg|697]]

---
## Experiments

**1. Fixed vs. Adaptive Assistance**
- Fixed: constant 75% assistance under mismatch
- Adaptive: POMDP reduces assistance when anxiety high → restores agency
- Expected: lower mean anxiety, minor tracking error increase

**2. Immunization Protocol**
- Trained group: brief *escapable* failures before the main test
- Both groups face the same large uncontrollable perturbation
- Expected:  lower peak anxiety,  faster recovery in trained group

**3. Sensitivity Analysis**
- Vary decay rate, assistance thresholds, mismatch type
- Confirm robustness to parameter changes

---
## References

[1] Diab, M., & Demiris, Y. (2025). TICK: A knowledge processing infrastructure for cognitive trust in human–robot interaction. *International Journal of Social Robotics, 17*, 2905–2937. https://doi.org/10.1007/s12369-024-01206-1

[2] Raju H, Tadi P. Neuroanatomy, Somatosensory Cortex. [Updated 2022 Nov 7]. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing; 2025 Jan-. Available from: https://www.ncbi.nlm.nih.gov/books/NBK555915/

[3] Bertuccelli, M., Tortora, S., Pasinato, M., Trombin, E., Tasinazzo, W., Baba, A., Bisiacchi, P., Sparacino, G., Menegatti, E., & Del Felice, A. (2025). Quantitative assessment of human-exoskeleton integration through a neurophysiological marker of embodiment. _Scientific Reports_, _16_(1), 3111. https://doi.org/10.1038/s41598-025-33046-y

[4] Anke Hua, Cédrick T. Bonnet, Cédrick T Bonnet, Jian Wang. Sensorimotor mismatch disrupts motor automaticity and increases anxiety during a goal-directed balance task. Frontiers in Human Neuroscience, 2025, 19, ⟨10.3389/fnhum.2025.1632265⟩. ⟨hal-05321803⟩

[5] Bertuccelli, M., Tortora, S., Trombin, E., Negri, L., Bisiacchi, P., Menegatti, E., & Del Felice, A. (2025). Human–robot interactions: A pilot study of psychoaffective and cognitive factors to boost the acceptance and usability of assistive wearable devices. *Multimodal Technologies and Interaction, 9*, 5. https://doi.org/10.3390/mti9010005

[6] Smoak, M. A., Galvan, K. J., Calvo, D. E., Powers, R. E., & Moschak, T. M. (2024). Prelimbic cortex activity predicts anxiety-like behavior in the elevated plus maze. *bioRxiv*. https://doi.org/10.1101/2024.12.26.630448

[7] Stirling, L., Wu, M. I., & Peng, X. (2024). Measuring trust for exoskeleton systems. In *Proceedings of Taking a Closer Look: Refining Trust and Its Impact in HRI Workshop (HRI ’24)*. (arXiv:2407.07200)

[8] Hybart, R. L., & Ferris, D. P. (2023). Embodiment for robotic lower-limb exoskeletons: A narrative review. *IEEE Transactions on Neural Systems and Rehabilitation Engineering, 31*, 657–668. https://doi.org/10.1109/TNSRE.2022.3229563

[9] Harris, D., Wilkinson, S., & Ellmers, T. (2023). From fear of falling to choking under pressure: A predictive processing perspective of disrupted motor control under anxiety. _Neuroscience & Biobehavioral Reviews_, _148_, 105115. https://doi.org/10.1016/j.neubiorev.2023.105115

[10] McGovern, H. T., Foe, A. D., Biddell, H., Leptourgos, P., Corlett, P., Bandara, K., & Hutchinson, B. T. (2022). Learned uncertainty: The free energy principle in anxiety. _Frontiers in Psychology_, _13_, 943785. https://doi.org/10.3389/fpsyg.2022.943785

[11] McGovern, H. T., De Foe, A., Biddell, H., Leptourgos, P., Corlett, P., Bandara, K., & Hutchinson, B. T. (2022). Learned uncertainty: The free energy principle in anxiety. _Frontiers in Psychology_, _13_, 943785. https://doi.org/10.3389/fpsyg.2022.943785

[12] Law, T., & Scheutz, M. (2021). Trust: Recent concepts and evaluations in human–robot interaction. In C. S. Nam & J. B. Lyons (Eds.), *Trust in Human–Robot Interaction* (pp. 27–57). Academic Press. https://doi.org/10.1016/B978-0-12-819472-0.00002-2

[13] Pynadath, D. V., Wang, N., & Kamireddy, S. (2019). A Markovian method for predicting trust behavior in human-agent interaction. In *Proceedings of the 7th International Conference on Human-Agent Interaction (HAI ’19)*. https://doi.org/10.1145/3349537.3351905

[14] Li X, Zhang M, Li K, Zou F, Wang Y, Wu X, Zhang H. The Altered Somatic Brain Network in State Anxiety. Front Psychiatry. 2019 Jul 1;10:465. doi: 10.3389/fpsyt.2019.00465. PMID: 31312147; PMCID: PMC6613038.

[15] Lewis, M., Sycara, K., & Walker, P. (2018). The role of trust in human–robot interaction. In H. Abbass et al. (Eds.), *Foundations of Trusted Autonomy* (Vol. 117). Springer. https://doi.org/10.1007/978-3-319-64816-3_8

[16] Cornwell, B. R., Garrido, M. I., Overstreet, C., Pine, D. S., & Grillon, C. (2017). The un-predictive brain under threat: A neuro-computational account of anxious hypervigilance. _Biological Psychiatry_, _82_(6), 447. https://doi.org/10.1016/j.biopsych.2017.06.031

[17] Maier, S. F., & Seligman, M. E. P. (2016). Learned helplessness at fifty: Insights from neuroscience. *Psychological Review*. https://doi.org/10.1037/rev0000033

[18] Haas, B. W., Ishak, A., Anderson, I. W., & Filkowski, M. M. (2015). The tendency to trust is reflected in human brain structure. *NeuroImage, 107*, 175–181. https://doi.org/10.1016/j.neuroimage.2014.11.060

[19] Hoff, K. A., & Bashir, M. (2015). Trust in automation: Integrating empirical evidence on factors that influence trust. *Human Factors, 57*(3), 407–434. https://doi.org/10.1177/0018720814547570

[20] Eysenck, M. W. (2013). _Anxiety: The cognitive perspective_. Psychology Press. https://doi.org/10.4324/9780203775677

[21] Grupe, D. W., & Nitschke, J. B. (2013). Uncertainty and anticipation in anxiety: An integrated neurobiological and psychological perspective. _Nature Reviews Neuroscience, 14_(7), 488–501. [https://doi.org/10.1038/nrn3524](https://psycnet.apa.org/doi/10.1038/nrn3524)

[22] Kilteni, Konstantina & Groten, Raphaela & Slater, Mel. (2012). The Sense of Embodiment in Virtual Reality. Presence Teleoperators &amp Virtual Environments. 21. 10.1162/PRES_a_00124. 

[23] Clark, D. A., & Beck, A. T. (2009). _Cognitive therapy of anxiety disorders: Science and practice_. Guilford Press.

[24] Bar-Haim, Y., Lamy, D., Pergamin, L., Bakermans-Kranenburg, M. J., & van IJzendoorn, M. H. (2007). Threat-related attentional bias in anxious and nonanxious individuals: A meta-analytic study. *Psychological Bulletin*.

[25] Corcoran, K. A., & Quirk, G. J. (2007). Activity in prelimbic cortex is necessary for the expression of learned, but not innate, fears. *The Journal of Neuroscience*. https://doi.org/10.1523/JNEUROSCI.5327-06.2007

[26] Kalisch, R., Wiech, K., Critchley, H. D., & Dolan, R. J. (2006). Levels of appraisal: A medial prefrontal role in high-level appraisal of emotional material. *NeuroImage*. https://doi.org/10.1016/j.neuroimage.2005.11.011

[27] Condé F, Maire-Lepoivre E, Audinat E, Crépel F. Afferent connections of the medial frontal cortex of the rat. II. Cortical and subcortical afferents. J Comp Neurol. 1995 Feb 20;352(4):567-93. doi: 10.1002/cne.903520407. PMID: 7722001.



