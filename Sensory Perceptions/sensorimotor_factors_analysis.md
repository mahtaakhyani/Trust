## TL;DR

Sensory precision (especially proprioception), prior expectations/attention, motor noise, and cognitive traits drive individual differences in sensorimotor perception. Aging reduces sensory precision and increases reliance on priors; no single perfect model exists, with Bayesian, predictive coding, and optimal control approaches leading.

----

## Key individual factors

The literature groups determinants of sensorimotor perception into physical (sensory and motor) and psychological (prior, attention, cognitive) categories and shows they interact to shape perceptual outcomes. Multiple studies emphasize that reduced sensory precision (notably proprioception) and altered priors/attention are central to between-person differences in perception.

- **Sensory precision** Proprioceptive and other sensory acuities strongly modulate body perception and multisensory integration; age-related reductions in proprioceptive ability explain increased distortions in body metrics and ownership in older adults [1].  
- **Motor noise and control** Motor response variability and noise influence visuomotor corrections and are modeled as increased endogenous noise in older adults, producing slower corrective responses despite unchanged response onset latency [2].  
- **Prior expectations** The strength and variance of priors bias perception; flatter or weaker priors account for individual differences in motion perception and are implemented in Bayesian models of perception [3].  
- **Attention and precision weighting** Top‑down allocation of expected precision (attention) changes the relative influence of modalities (vision vs proprioception) in both perception and action under conflict [4].  
- **Cognitive and trait factors** Working memory, past responses, and trait measures (e.g., autistic traits) modulate how sensory evidence and priors are combined across individuals [3] [5].  
- **Multisensory causal inference** Beliefs about a common cause (causal inference) determine cue combination weights and differ across development and individuals [6].

References in this section support the categorical roles above and their interactions [1] [2] [3] [4] [6] [7] [5].

----

## Age and gender effects

Empirical work quantifies several age-related changes in sensorimotor perception while the literature provides little direct evidence for gender effects in the supplied corpus. Older adults show systematic increases in sensory noise, altered cue weighting, and greater reliance on predictive signals, whereas gender-specific quantitative effects are not reported in the provided studies.

- **Increased reliance on predictive signals** Older adults show larger motion‑induced position shifts (MIPS); the mean MIPS was reported as 2.87 times larger in older compared with younger adults, and sensory noise (not propagation noise) was identified as significantly larger in the older group [8].  
- **Proprioceptive decline drives body misperception** Age-related higher distortions in perceived arm dimensions and stronger illusory ownership toward a virtual hand are explained by reduced proprioceptive abilities in older participants [1].  
- **Slower corrective responses with preserved onset latency** Cross‑correlation analyses found no age‑related increase in response latency at perturbation onset, but a substantial slowing of the response itself; this pattern was fit by an optimal‑control style model in which increased endogenous noise causes adaptation manifesting as slower responses [2].  
- **Altered cue‑history influences** Bayesian modeling indicates that while older and younger adults can show comparable immediate cue biases, older adults’ after‑effects are sometimes driven more by their previous responses (behavioral history) than by prior sensory information [5].  
- **Gender evidence insufficient** The supplied papers do not report gender‑specific effect sizes or correlations for sensorimotor perception; therefore evidence for gender influences is insufficient.

Each quantitative claim above is supported by the cited empirical reports [1] [8] [2] [5].

----

## Statistical relationships reported

Empirical and modeling studies report several statistical and model‑based relationships, but many do not publish a comprehensive set of correlation coefficients or regression parameter estimates in their abstracts; detailed numerical relationships are sometimes confined to full texts. The supplied studies nonetheless provide a few explicit quantitative findings and indicate analytic approaches used to relate factors to perception.

- **Explicit effect size** The factor 2.87× larger mean MIPS in older adults is an explicitly reported group effect size for position bias [8].  
- **Cross‑correlation outcome** Cross‑correlation analyses revealed unchanged latency to response onset but slower response dynamics with age, a pattern reproduced in model fits that parameterize noise intensity and effort willingness [2].  
- **Latent factor relationships** Bayesian structural equation modeling (BSEM) separated **sensory capability** and **information integration** as independent latent factors explaining cognitive status in older adults, indicating separable pathways linking sensory acuity and integration to behavior [7].  
- **Model prediction of individual differences** A quantitative Bayesian model combining sensory thresholds and autistic‑trait scores predicted individual differences in motion perception phenomena, indicating joint contributions of sensitivity and priors to perceptual variance [3].  
- **Insufficient evidence for many coefficients** Specific Pearson/Spearman correlation coefficients, regression β weights, full reported model fits, and numerical parameter estimates for most factor–perception relationships are not available in the provided abstracts; therefore many precise statistical coefficients cannot be listed here (insufficient evidence).

Where explicit statistics are reported above, the originating studies are cited immediately after the claims [8] [2] [7] [3].

----

## Computational models and formulas

Several computational frameworks are used across the supplied literature to formalize sensorimotor perception: Bayesian (including Bayesian causal inference), predictive coding / active inference, and quadratic optimal control. The papers cite or implement these frameworks, but full numeric parameter sets and some closed‑form parameter values are not consistently reported in the provided abstracts.

Table summarizing model forms and reported quantities

| **Model** | **Representative equation or form** | **Key parameters or gains reported** | **Primary references** |
|---|---:|---|---|
| **Bayesian perceptual model** | Posterior ∝ Likelihood × Prior (P(s|o) ∝ P(o|s) P(s)) — cue weights follow reliability weighting | Individual differences explained by sensory thresholds and prior variance; specific numeric prior variances not shown in abstracts | [3] [6] |
| **Bayesian causal inference** | Weighted averaging conditional on causal hypothesis with P(C=1|data) modulating fusion vs segregation | Model used to capture visuotactile localization and development; specific β or σ values not in abstracts | [6] |
| **Predictive coding / active inference** | Precision‑weighted prediction error drives updates: minimize Σ precision × (observation − prediction)^2 | Expected precision (attention) modulates influence of vision vs proprioception; precision allocation effects reported qualitatively | [4] [8] |
| **Optimal control (quadratic cost)** | Minimize J = E[Σ_t (x_t'Qx_t + u_t'Ru_t)] under noisy dynamics; behavior modeled as optimal controller under increased noise | Model parameters described conceptually: latency, effort cost, noise intensity/bandwidth; numeric parameter values not provided in abstracts | [2] |
| **Neural population tuning model** | Prior sharpening implemented as response suppression across tuning curves, leading to reduced population variance | Prior‑dependent tuning sharpening reported to explain pursuit biases; numeric gain values not listed in abstracts | [9] |

Notes on formulas and parameters
- The general Bayes form and causal‑inference architectures are explicitly applied to multisensory localization and developmental comparisons in the cited works [6] [3].  
- Active inference / predictive coding formulations emphasize precision (inverse variance) as a multiplicative weight on prediction errors; increasing expected precision for a modality increases its influence on perception/action [4] [8].  
- The optimal‑control approach used to model age effects assumes quadratic optimality and parameterizes behavior by latency, willingness to expend effort, and noise terms; the model reproduced qualitative group differences but the abstracts do not report fitted numerical parameter values for these terms [2].  
- Several studies implement these frameworks quantitatively (model fitting, BSEM), but full regression coefficients, exact prior variances, or gain‑parameter point estimates are generally reported in full articles rather than in the provided abstracts (insufficient evidence for many numeric parameter values).

For readers seeking explicit equations and parameter estimates, the cited papers implement these frameworks and contain the detailed mathematical derivations and fits [3] [6] [4] [8] [2] [9].

----

## Unified framework and hierarchy

No single perfect or universally accepted model is endorsed in the supplied literature; instead, complementary frameworks dominate and empirical work points to a hierarchical role of sensory precision with modulatory roles for priors, attention, and cognitive factors. The literature converges on a set of leading computational theories rather than a unified formalism.

- **No perfect unified model** Papers apply and compare Bayesian causal inference, predictive coding/active inference, and optimal control to different tasks and populations; none of the provided studies claim a single complete unifying model that subsumes all phenomena [6] [4] [2] [3].  
- **Leading theories** Bayesian cue combination and Bayesian causal inference explain multisensory weighting and developmental patterns, predictive coding / active inference formalize precision‑weighting and attention effects, and optimal control captures action under noise and effort tradeoffs [6] [4] [2] [3].  
- **Hierarchy of influence (evidence‑based ordering)**  
  - **Primary factors** Sensory precision (especially proprioception and sensory noise) emerges repeatedly as the dominant determinant of altered perception, particularly with aging [1] [8] [7].  
  - **Secondary factors** Priors and their variance (expectation strength) shift biases and can compensate for noisy sensory signals, acting together with sensory precision [3] [9].  
  - **Modulatory factors** Attention/precision allocation, motor costs/effort tradeoffs, and cognitive/trait variables (memory, prior responses, autistic traits) modulate how primary and secondary factors are combined into perception and action [4] [2] [5] [7].  
- **Limits of ordering** Although multiple studies support the primacy of sensory precision and the modulatory role of priors/attention, the supplied corpus does not provide a single statistical ranking with full quantitative inter‑factor weights across tasks and populations; therefore a strict, universally applicable ordering with exact numerical weights is not available (insufficient evidence).

The leading computational theories and the empirical hierarchy above are supported by the cited modeling and experimental studies in the supplied literature [1] [8] [2] [3] [4] [6] [7] [5] [9].

## References
[1]
G. Powell, Z. Meredith, R. McMillin, and T. C. Freeman, “Bayesian Models of Individual Differences: Combining Autistic Traits and Sensory Thresholds to Predict Motion Perception,” Psychological Science, vol. 27, no. 12, pp. 1562–1572, Oct. 2016, doi: 10.1177/0956797616665351.

[2]
G. Risso et al., “Proprioception Impacts Body Perception in Healthy Aging: Insights from a Psychophysical and Computational Approach,” July 2024, doi: 10.1101/2024.07.23.604821.

[3]
E. Verhaar, W. P. Medendorp, S. Hunnius, and J. C. Stapel, “Bayesian causal inference in visuotactile integration in children and adults,” Developmental Science, Nov. 2021, doi: 10.1111/DESC.13184.

[4]
J. Lee, A. A. Yayna, and S. Adduri, “Prior expectation enhances sensorimotor behavior by modulating population tuning and subspace activity in sensory cortex,” Science Advances, vol. 9, no. 27, July 2023, doi: 10.1126/sciadv.adg4156.

[5]
J. Park, S. Kim, H. Kim, and J. Lee, “Prior expectation enhances sensorimotor behavior by modulating population tuning and subspace activity in sensory cortex,” bioRxiv, vol. 9, Dec. 2022, doi: 10.1101/2022.12.04.516847.

[6]
M. Sherback, F. J. Valero-Cuevas, and R. D’Andrea, “Slower Visuomotor Corrections with Unchanged Latency are Consistent with Optimal Adaptation to Increased Endogenous Noise in the Elderly,” PLOS Computational Biology, vol. 6, no. 3, Mar. 2010, doi: 10.1371/JOURNAL.PCBI.1000708.

[7]
J. Misselhorn et al., “Sensory capability and information integration independently explain the cognitive status of healthy older adults.,” Scientific Reports, vol. 10, no. 1, p. 22437, Dec. 2020, doi: 10.1038/S41598-020-80069-8.

[8]
J. Limanowski and K. J. Friston, “Active inference under intersensory conflict: Simulation and empirical results,” bioRxiv, p. 795419, Oct. 2019, doi: 10.1101/795419.

[9]
H.-J. Jeon, Y. Yun, and O.-S. Kwon, “Integration of Position and Predictive Motion Signals in Aging Vision,” Scientific Reports, vol. 10, no. 1, p. 8783, May 2020, doi: 10.1038/S41598-020-65568-Y.