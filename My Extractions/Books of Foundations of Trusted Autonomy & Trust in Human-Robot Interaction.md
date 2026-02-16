# Foundations of Trusted Autonomy [(Lewis et al., 2018)](https://doi.org/10.1007/978-3-319-64816-3_8)

- Understanding and replicating the human motivational subsystem can be highly beneficial to building autonomous intelligent agents and systems, because of its power, flexibility, and adaptability [(Sun, 2009)](https://doi.org/10.1007/s12559-009-9003-1).

- McDougall [(McDougall, 1936)](https://archive.org/details/introductiontoso00mcdo) proposed a framework that was concerned with “**instincts**”.  
  Instincts, in our framework, refer to (more or less) evolutionarily hard-wired (i.e., innate) behavior patterns or routines that can be relatively easily triggered by pertinent stimuli in pertinent situations. #cognitive/instincts_model
- Some of these primary drives are approach-oriented, while others are avoidance-oriented. This distinction has been argued by many (e.g., [(Clark & Watson, 1999)](https://psycnet.apa.org/record/1999-04371-012), [(Gray & McNaughton, 2000)](https://global.oup.com/academic/product/the-neuropsychology-of-anxiety-9780198522713), [(Smillie et al., 2006)](https://doi.org/10.1207/s15327957pspr1004_3)).  
  The approach system is sensitive to cues signaling rewards, and results in active approach.  
  The avoidance system is sensitive to cues of punishment, and results in avoidance, characterized by **anxiety or fear**. #reward_signals #punishment_cues #cognitive/anxiety #cognitive/fear ^tr-spfecqi79

- the core drive module determines drive strengths (using neural networks) based roughly on:  
  **ds_d = gain_d . stimulus_d . deficit_d + baseline_d**

  where ds_d is the strength of drive d, gain_d is the gain for drive d, stimulus_d is a value representing how pertinent the current situation is to drive d, def icit_d indicates the perceived deficit in relation to drive d (which represents an individual’s internal inclination toward activating drive d), and baseline_d is the baseline strength of drive d. The justifications for this may be found in the literature [(Sun, 2016)](https://global.oup.com/academic/product/anatomy-of-the-mind-9780190200527), [(Toates, 1986)](https://www.cambridge.org/core/books/motivational-systems/8E3E98B35F2C5E0C5E1C9F6C8E9E2A9E), [(Tyrrell, 1993)](https://www.cs.toronto.edu/~tyrrell/thesis/thesis.html). #computational_cognitive_architecture #formula

- The afore-discussed motivational representations and their resulting dynamics help to make a computational cognitive architecture more complete and functioning in a more psychologically realistic way. I believe that this constitutes a requisite step forward in making computational cognitive architectures more realistic models of the human mind taking into considerations all of its complexity and intricacy, especially in terms of its complex motivational dynamics. It is highly relevant to building truly autonomous and trust-worthy computational agents capable of functioning in complex, uncertain, and unpredictable environments. Note that what I emphasize here is human-like full autonomy and human-like trust.

- These studies help introduce the idea of “inverse trust”. The inverse trust problem is defined in [(Floyd et al., 2014)](https://doi.org/10.1007/978-3-319-09144-0_50) as determining how “an autonomous agent can modify it’s behavior in an attempt to increase the trust a human operator will have in it”. In this paper, the authors base this measure largely on the number of times the automation is interrupted by a human operator, and uses this to evaluate the autonomous agent’s assessment of change in the operator’s trust level. Instead of determining an absolute numerical value of trust, the authors choose to have the automation estimate changes in the human’s trust level. This is followed in [(Mittu, 2016)](https://doi.org/10.1007/978-1-4899-7668-0) by studies in simulation validating their inverse trust model.
---
# Trust in Human-Robot Interaction [Link](https://www.sciencedirect.com/book/edited-volume/9780128194720/trust-in-human-robot-interaction)

- In the automation literature, such worry is tied to the performance of the system; and this worry can be alleviated, and allows for trust (Schaefer, Chen, Szalma, & Hancock, 2016). 

	- Sheridan and Parasuraman (2005) reviewed research in human automation interaction and offered two sets of features of trust. One set comes from the system’s lower-level reliability of performance, while the other comes from the system’s higher-level ability.

	- Ideally, trust in a system is grounded in an accurate conception of the system’s ability and reliability [(Malle & Ullman, 2021)](https://doi.org/10.1016/B978-0-12-819472-0.00001-0). #trust_factors/robot_factors/ability #trust_factors/robot_factors/reliability ^tr-j1qd1s6ia

	- Because **errors** reveal a system’s performance quality, they have been a particular focus in human-automation work. 
		- For example, Madhavan, Wiegmann, and Lacson (2006) showed that trust in an automated decision aid declined when the user observed system errors. 
		- However, not all errors were treated the same way: when a system made errors on **easy trials** rather than difficult trials, users **mistrusted the system far more**. People potentially use task difficulty as a diagnostic indicator: failing to complete easy trials shows low **ability** [(Malle & Ullman, 2021)](https://doi.org/10.1016/B978-0-12-819472-0.00001-0). #trust_factors/robot_factors/error #trust_factors/environmental_factors/task_difficulty 
	  
	- A recent review of 127 empirical studies on human trust in automation  [(Hoff & Bashir, 2015)](https://psycnet.apa.org/record/2015-11688-001)  identified numerous factors that affect trust, including culture, personality, task characteristics, workload, self-confidence, and more;  ^9d0c16
		- but the object of the trust itself—the automation system— was described only in terms of its **performance**: its **reliability**, **predictability**, and **error-proneness** [(Malle & Ullman, 2021)](https://doi.org/10.1016/B978-0-12-819472-0.00001-0). 
		- #trust_factors/robot_factors/performance #trust_factors/robot_factors/predictability  
	- In sum, **in the literature on trust in automation, the primary focus is on appropriately matching a person’s expectations for a system with information about the performance of the system.** 
	 These systems are motiveless, and users are not concerned about being betrayed, exploited, or deceived by the system. Trust here is the expectation that a system will perform a task as intended and expected, and the only worries that arise concern the system’s reliability and ability #trust_factors/robot_factors/matching_expectations  ^perf ^tr-1xjotqi2t

- Much of the extant work on human-robot trust focuses on the **reliability** and **ability** characteristics of robotic systems, so trust in intelligent robots is considered along the same factors seen in the broader human automation literature  [(Yanco et al., 2016); summarized in (Malle & Ullman, 2021)](https://doi.org/10.1016/B978-0-12-819472-0.00001-0)
- For example, [(Hancock et al., 2011)](https://doi.org/10.1177/0018720811417254) conducted a metaanalysis of factors that prior research has identified as influencing trust in human-robot interaction. The authors collated 21 studies and found that factors related to the robot—specifically, **robot performance (such as reliability)—had the strongest association with trust**. Human-related factors (e.g., attitudes and comfort with robots) and environmental factors (e.g., culture and physical environment) contributed relatively less.  
  

- **Performance-based trust** centers around the robot being trusted to be **reliable**, **capable**, and **competent**.

	- Performance-based trust may also depend on the robot’s **transparency**, **responsiveness**, and **predictability**. Relation-based trust, on the other hand, implies that a robot is trusted as a social agent  
	  [(Law & Scheutz, 2021)](https://doi.org/10.1016/B978-0-12-819472-0.00002-2).

	- [(Xu & Howard, 2018)](https://doi.org/10.1109/ROMAN.2018.8525669) found that a robot who gave a **first impression** of being faulty was trusted less. ^init

- **Human factors** that contribute toward trust include personal characteristics that affect the trustor’s judgment toward the trustee  
  [(Hancock et al., 2011)](https://doi.org/10.1177/0018720811417254);  
  [(Szalma & Taylor, 2011)](https://doi.org/10.1037/a0024170).

- A robot displaying **unconditional and consistent behavior** improves trust  
  [(Parks et al., 1996); cited in (Malle & Ullman, 2021)](https://doi.org/10.1016/B978-0-12-819472-0.00001-0). #trust_factors/robot_factors/consistent_behavior ^tr-k7451rcdc

- Robot **transparency** affects trust and utility  
  [(Lyons, 2013; Wortham & Theodorou, 2017); summarized in (Malle & Ullman, 2021)](https://doi.org/10.1016/B978-0-12-819472-0.00001-0).

- **Trust is a purely subjective quality** characterizing the relationship between two parties.
#trust_definition 
- **Psychological trust** consists of multiple factors at cognitive, emotional, and behavioral levels  #psychological_trust
  [(PytlikZillig & Kimbrough, 2016)](https://doi.org/10.1007/s11238-016-9569-3).

- Studies of neuroimaging and neuropsychological have shown that a favorable assessment of trust will lead to **less activation in the amygdala region**  ^amyg0
- #measures/objective_measures/brain_scan
  [(Rilling & Sanfey, 2011); summarized in (Mee et al., 2006)](https://doi.org/10.1016/j.jpsychires.2006.03.003).
- #trust_bio/amygdala
	- ##### Amygdala
		- The amygdala functions to code the emotional salience of information (Aggleton, 2000).
		- amygdala activity correlates with the subjective evaluation of trustworthiness of social stimuli (Rule et al., 2013). ^amygdala1
		- Rule and colleagues (2013) recently reported that amygdala activity increases when making judgments related to trustworthiness and distrustworthiness. ^amygdala2
		- Furthermore, individuals with amygdala damage display abnormal trustworthiness evaluations of faces (Adolphs et al., 1998) and altered trust based decision making (Koscik and Tranel, 2011).  ^amygdala3
		- **Together, these findings indicate that amygdala structure may be a neural construct associated with individual differences in the tendency to trust and distrust.** 
		^amygdala4

		[DOI](https://www.sciencedirect.com/science/article/abs/pii/S1053811914009902#:~:text=https%3A//doi.org/10.1016/j.neuroimage.2014.11.060) 
		- #important #trust_factors/human_factors/traits/amygdala_structure
	- ##### Anterior Insula
		- The anterior insula is involved in emotional awareness and the subjective experience of emotions (Gu et al., 2013).
		- In terms of trust, anterior insula activity is associated with trustworthiness decisions of faces (Kragel et al., 2014, Winston et al., 2002) and with trust based decisions during economic scenarios (Aimone et al., 2014, van den Bos et al., 2009). 
		- Additionally, empirical evidence indicates that the anterior insula codes both trust (Killgore et al., 2013) and distrust (Winston et al., 2002) evaluations of faces.
		#trust_bio/insula
		- **individual differences in the tendency to trust (self-report and behaviorally) would be associated with gray matter volume within the vmPFC, amygdala and anterior insula.** #trust_factors/human_factors/traits/insula_structure
		[DOI](https://www.sciencedirect.com/science/article/abs/pii/S1053811914009902#:~:text=https%3A//doi.org/10.1016/j.neuroimage.2014.11.060) ^tr-5xflpo6il


- Basic personality tendencies relevant to trust include **Conscientiousness**, **Agreeableness**, **Emotional Stability**, **Adaptability**, and **Integrity**  [(Christian et al., 2010)](https://doi.org/10.1177/0146167209359702).
#trust_factors/human_factors/traits/emotional_stability
#trust_factors/human_factors/traits/adaptability
#trust_factors/human_factors/traits/integrity
#trust_factors/human_factors/traits/conscientiousness
#trust_factors/human_factors/traits/agreeableness
## Chapter 4
- Given that trust has a neurological basis, **there is a need for “ground truth” to link physiological measurements to a trustor’s actual feelings of trust by combining physiological with subjective measurements in the form of big data.** This enables determining a fixed reference point in the analysis of trust. However, time is important when associating physiological measurements to subjective trust since human trust is dynamic with ever-changing quality.
	#measures/objective_measures/physiological_measures
	^ground
- To avoid information loss, it is critical to pause the interaction so that subjects could score the current trust attribute before progressing to the next attribute in the dialogue. ^tr-1ctkhxj8m

## Chapter 5
- A user’s trust in robots and robotic environments can also play a critical role in safe and effective human-robot interaction performance.

- **Working memory** involves maintaining and processing information during complex cognitive tasks, and individual differences in working memory capacity predict performance on a wide range of real-world tasks (Engle, 2002).
	- An individual worker’s working memory is likely to be **negatively associated with trust** in robots. One study, in which researchers investigated the **effect of working memory on trust in automation**, supported this relationship and found that inferior working memory was associated with more trust in automation (Rovira et al., 2017). This study further suggested that participants with lower working memory calibrate trust inappropriately and rely on the automation even when it fails (Rovira et al., 2017).
	#trust_factors/human_factors/working_memory
- Similar relationships have been observed with **attentional capacity** (Chen & Barnes, 2012; Parasuraman & Manzey, 2010). Studies demonstrated that individuals with **lower attentional resources showed increased reliance on automation** (Chen & Barnes, 2012), and operators increased their reliance on automation when less attentional resources were available due to the task complexity (Parasuraman & Manzey, 2010), even when doing so could result in undesirable performance.
- Increased trust in the automated system is likely a strategy that operators adopt to deal with complex information while **conserving cognitive resources** (Chen & Barnes, 2012). ^res
- 
#trust_factors/human_factors/attentional_capacity
#cognitive/cognitive_reserve ^tr-g7d0kunsi

- Given the dynamic nature of the trust calibration process, **individual differences in the changes of trust over time can be large**. Studies found that while trust changes substantially for some people, for other people, it changes relatively little (Lee & Moray, 1994; Lee & See, 2004).
	#Time/trust_dynamics_over_time
- Similar to the roles of human-related factors in the **initial level of trust**, various individual characteristics and differences can influence the **evolution of trust**.

- As individuals vary in learning processes ( Jonassen & Grabowski, 2012), individual **differences in learning ability** would have impacts on the acquisition of knowledge and skills related to working with robots, which results in varying change rates in individuals’ trust in robots. ^learning

#trust_factors/human_factors/learning_ability 
## Chapter 6
- Trust can be defined as “**a person’s calculated exposure to risk of damage from the activities of influential others**” (Hancock et al., 2011).
#trust_definition
### Human-related antecedents of trust
- Early studies in human-robot interaction (HRI) often focused on characteristics related to the robot. However, the rise in human-centered thinking has led to a more frequent measurement of human characteristics in HRI experimentation. Such investigations look to topics such as **personality**, **age**, **attitudes toward automation** and robots, **culture**, and **self perception**.
#trust_factors/human_factors/traits/personality
#trust_factors/human_factors/traits/age 
#trust_factors/human_factors/traits/attitude_toward_robots
#trust_factors/human_factors/traits/culture
#trust_factors/human_factors/traits/self_perception
- a positive relationship between participants’ **extroversion** and their ratings of robot anthropomorphism exists (Kaplan, Sanders, & Hancock, 2018). These findings suggest that personality can influence participants’ perceptions of a robot’s characteristics. ^tr-bbm8243qw

- Several studies show **age** as a precursor to trust, specifically, younger participants are much more likely to trust robots than their older counterparts (Erebak & Turgut, 2018; Heerink, 2011; Schaefer, 2013; Scopelliti, Giuliani, & Fornara, 2005)

- there is a positive relationship between trust and a user’s expertise or **prior experience** (Hancock et al., 2020; Heerink, 2011; Sanders et al., 2017; Schaefer, 2013). This suggests that trust is emerging, uniquely, from each interaction as it is built on the experiences of the previous encounter.

### Robot-related antecedents of trust
#### Performance-based factors
- Robot-related antecedents of trust are broadly categorized into **performance-based factors** (how well the robot functions) and **attribute based factors** (how the robot looks, feels, and behaves). Overall, robot related antecedents, specifically **those related to reliable performance, have generally been found to be most closely related to trust development**.
	- **Reliability is one specific facet of performance**, related to the consistent nature of that performance (Stowers et al., 2017).
		- Closely related to reliability is **predictability**. Predictability here represents a measure of how clear a robot’s intentions and future actions are to its operator (Dragan, Lee, & Srinivasa, 2013). This trait is also positively related to trust, with more predictable behavior on the part of the robot leading to higher trust on the part of the user (Biros, Daly, & Gunsch, 2004).
			- The issue of robot intention is closely allied to another factor, which is **transparency**. Transparency refers to the amount of information that a robot shares with its operator (see Lyons & Havig, 2014)
			#trust_factors/robot_factors/reliability 
		    #trust_factors/robot_factors/performance 
			#trust_factors/robot_factors/transparency
### Time
- When the time is taken into account in human-robot trust, it is generally in the form of shared tenure or prior experience, and *not as a moderating influencer that affects all of the other antecedents*.
#trust_factors/time
- Yet, time is little accounted for in previous models of human-robot trust, and when it has been, it is generally in the form of shared tenure or prior experience, and not as a moderating influencer that affects all of the other antecedents. 
	- Further, as trust is generally measured at the end of an interaction, there is not much empirical evidence to permit elucidation of the profile of the dynamic nature of trust. While the evidence that trust evolves with time is clear, it is often treated as a stable and unchanging trait.
	
- **The human-related antecedent of prior experience with robots has a clear and linear relationship with time.** Experience only increases, though at different rates, and the later the individual is surveyed, the higher their experience with robots will necessarily be. 
	- Other factors are not so clearly related. A person’s culture does not change but how that culture affects their trust in a robot may vary based on any current cultural phenomenon such as movies, accidents, or military involvement.
	- Each antecedent of trust changes differently based on **both the time of the interaction and the time of trust measurement**. Thus, time moderates the relationships between these antecedents and trust
	
- In one study, researchers found that one robot’s good performance increased the level of trust that people felt toward a different robot viewed later (De Bruijn, 2013) ^tr-20c0rnxfj

- Researchers found that **trust increased overall** across trials. However, **decreases in robot reliability** caused corresponding decreases in trust that **slowly recovered as reliability improved** (Desai et al., 2013). ^96b7a4
	- Low reliability has a negative impact on trust **but a stronger one at the beginning of an interaction**.
	
- Perhaps it is important to view **time** not simply as a fourth and equivalent antecedent of trust but as a **pre-precursor or a super-moderator, that is, something that affects all of the other moderators and sub-moderators before trust calibration even begins**.



---

# References

- Christian, M. S., Miller, C. T., & McCord, D. M. (2010).  
  *The effects of stereotype threat on performance in a social judgment task.*  
  **Personality and Social Psychology Bulletin, 36**(3), 379–392.  
  https://doi.org/10.1177/0146167209359702

- Clark, L. A., & Watson, D. (1999).  
  *Temperament: A [[new]] paradigm for trait psychology.*  
  In **Handbook of Personality: Theory and Research** (pp. 399–423).  
  https://psycnet.apa.org/record/1999-04371-012

- Gray, J. A., & McNaughton, N. (2000).  
  *The Neuropsychology of Anxiety: An Enquiry into the Function of the Septo-Hippocampal System.*  
  Oxford University Press.  
  https://global.oup.com/academic/product/the-neuropsychology-of-anxiety-9780198522713

- Hancock, P. A., Billings, D. R., Schaefer, K. E., Chen, J. Y. C., de Visser, E. J., & Parasuraman, R. (2011).  
  *A meta-analysis of factors affecting trust in human–robot interaction.*  
  **Human Factors, 53**(5), 517–527.  
  https://doi.org/10.1177/0018720811417254

- Law, T., & Scheutz, M. (2021).  
  *Trust: Recent concepts and evaluations in human–robot interaction.*  
  In C. S. Nam & J. B. Lyons (Eds.), **Trust in Human-Robot Interaction** (pp. 27–57). Academic Press.  
  https://doi.org/10.1016/B978-0-12-819472-0.00002-2

- Lewis, M., Sycara, K., & Walker, P. (2018).  
  *The role of trust in human–robot interaction.*  
  In H. Abbass et al. (Eds.), **Foundations of Trusted Autonomy** (Vol. 117). Springer.  
  https://doi.org/10.1007/978-3-319-64816-3_8

- Malle, B. F., & Ullman, D. (2021).  
  *A multidimensional conception and measure of human–robot trust.*  
  In C. S. Nam & J. B. Lyons (Eds.), **Trust in Human-Robot Interaction** (pp. 3–25). Academic Press.  
  https://doi.org/10.1016/B978-0-12-819472-0.00001-0

- McDougall, W. (1936).  
  *An Introduction to Social Psychology.* Methuen & Co.  
  https://archive.org/details/introductiontoso00mcdo

- Mee, S., Bunney, B. G., Reist, C., Potkin, S. G., & Bunney, W. E. (2006).  
  *Psychological pain: A review of evidence.*  
  **Journal of Psychiatric Research, 40**(8), 680–690.  
  https://doi.org/10.1016/j.jpsychires.2006.03.003

- Smillie, L. D., Pickering, A. D., & Jackson, C. J. (2006).  
  *The [[new]] reinforcement sensitivity theory: Implications for personality measurement.*  
  **Personality and Social Psychology Review, 10**(4), 320–335.  
  https://doi.org/10.1207/s15327957pspr1004_3

- Sun, R. (2009).  
  *Motivational representations within a computational cognitive architecture.*  
  **Cognitive Computation, 1**(1), 91–103.  
  https://doi.org/10.1007/s12559-009-9003-1

- Sun, R. (2016).  
  *Anatomy of the Mind: Exploring Psychological Mechanisms and Processes with the CLARION Cognitive Architecture.*  
  Oxford University Press.  
  https://global.oup.com/academic/product/anatomy-of-the-mind-9780190200527

- Szalma, J. L., & Taylor, G. S. (2011).  
  *Individual differences in response to automation: The five factor model of personality.*  
  **Journal of Experimental Psychology: Applied, 17**(2), 71–96.  
  https://doi.org/10.1037/a0024170

- Toates, F. M. (1986).  
  *Motivational Systems.* Cambridge University Press.  
  https://www.cambridge.org/core/books/motivational-systems/8E3E98B35F2C5E0C5E1C9F6C8E9E2A9E

- Tyrrell, T. (1993).  
  *Computational mechanisms for action selection.*  
  Oxford University.  
  https://www.cs.toronto.edu/~tyrrell/thesis/thesis.html

- Xu, J., & Howard, A. (2018).  
  *The impact of first impressions on human–robot trust during problem-solving scenarios.*  
  **RO-MAN 2018**, IEEE.  
  https://doi.org/10.1109/ROMAN.2018.8525669

- Haas, B. W., Ishak, A., Anderson, I. W., & Filkowski, M. M. (2015). *The tendency to trust is reflected in human brain structure*. **_NeuroImage_**, _107_, 175-181. 
  https://doi.org/10.1016/j.neuroimage.2014.11.060

- Floyd, M., Drinkwater, M., & Aha, D. (2014). _Adapting Autonomous Behavior Using an Inverse Trust Estimation_. 728–742. https://doi.org/10.1007/978-3-319-09144-0_50

- Mittu, R. (2016). _Robust Intelligence and Trust in Autonomous Systems_. https://doi.org/10.1007/978-1-4899-7668-0