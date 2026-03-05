> The definition of Trust can be understood as follows: trust is characterized as an event (e) wherein a minimum of two agents are involved, identified as the trustor (y) and trustee (z), engaging in a specific task or sub-task (t) that necessitates their interaction (p). 
> The dynamics of trust are influenced by social attributes (s), which encompass factors that impact trust, such as the inference of human intention (i), the agent’s capability in a given situation (re), vulnerability (v), and risk (r). 
> The outcome of trust manifests as either an act of trust or an act of distrust, resulting in subsequent actions. #trust_definition 

[[TICK- A Knowledge Processing Infrastructure for Cognitive Trust in Human–Robot Interaction.pdf#page=9&selection=140,0,154,7|TICK- A Knowledge Processing Infrastructure for Cognitive Trust in Human–Robot Interaction, page 9]]

> We present a proposed definition for the concept of Threat as follows: “A threat is an event that encompasses objects capable of causing harm or posing danger, thereby potentially rendering an agent vulnerable.” #threat 
[[TICK- A Knowledge Processing Infrastructure for Cognitive Trust in Human–Robot Interaction.pdf#page=9&selection=360,0,366,31|TICK- A Knowledge Processing Infrastructure for Cognitive Trust in Human–Robot Interaction, page 9]]

> *Risk in the TICK is defined as a **probabilistic value** that has the potential to result in loss or harm due to the exploitation of vulnerability by a threat event. The assessment of risk takes into account both the threat event and the vulnerability of an agent.* #risk #threat #necessities/vulnerable_settings 
[[TICK- A Knowledge Processing Infrastructure for Cognitive Trust in Human–Robot Interaction.pdf#page=10&selection=187,0,193,13|TICK- A Knowledge Processing Infrastructure for Cognitive Trust in Human–Robot Interaction, page 10]]


- **Prior Experiences Storage**: They have used "episodic memory" storing context of the situation. Each context includes info about the participants, the utilized object for the task, the action performed by the robot, and human's reaction + reasoned (processed) info about each feature of the model (evaluated risk, robot reliability, human intention, ...) [[TICK- A Knowledge Processing Infrastructure for Cognitive Trust in Human–Robot Interaction.pdf#page=12&selection=31,0,47,10|TICK- A Knowledge Processing Infrastructure for Cognitive Trust in Human–Robot Interaction, page 12]]


> **Fig. 7** The flow of information between the knowledge acquisition’s modules to build understandable knowledge of the working domain including the current scene of the robot

[[TICK- A Knowledge Processing Infrastructure for Cognitive Trust in Human–Robot Interaction.pdf#page=15&selection=4,0,7,29|TICK- A Knowledge Processing Infrastructure for Cognitive Trust in Human–Robot Interaction, page 15]]

> The user’s perception of the available technical information significantly contributes to their trust in the system.

[[TICK- A Knowledge Processing Infrastructure for Cognitive Trust in Human–Robot Interaction.pdf#page=20&selection=170,11,172,4|TICK- A Knowledge Processing Infrastructure for Cognitive Trust in Human–Robot Interaction, page 20]]


#### **Everything about this Section is IMPORTANT:** 
> 4.6 Trust Estimation
[[TICK- A Knowledge Processing Infrastructure for Cognitive Trust in Human–Robot Interaction.pdf#page=20&selection=14,0,14,19|TICK- A Knowledge Processing Infrastructure for Cognitive Trust in Human–Robot Interaction, page 20]]

Steps: 
1. identify key features impacting trust
2. normalizing them
3. linking them to their respecting definitions (like "risk")

**T = h × pt f** (h=performance, pt f = perceived trust factor)
	**h measured by**: 
		1. robot self-assessment 
		2. **behavioural** measures (**the level of engagement** in general, as an example how much they listen to robot's suggestions in higher risk situations or keeping distance with the robot)
		3. **performance** indicators [4] (**number of errors** made ≠ success rate → based on human **satisfaction** at the end of the experiment)
	**pt f shows:**
		4. Situation analysis, 
		5. Reliability, Vulnerability, 
		6. Risk analysis, 
		7. Intention
		8. Explainability

$h = \sum_{i=1}^{n} ux_{i} + f(sa, bm, pi)$ 
[link to formula]([[TICK- A Knowledge Processing Infrastructure for Cognitive Trust in Human–Robot Interaction.pdf#page=20&selection=90,0,90,1|TICK- A Knowledge Processing Infrastructure for Cognitive Trust in Human–Robot Interaction, page 20]])

$ptf = f(ux_r, fu, rf, os)$
*Each value is between [0,1].*
		
		
$NormalizedValue = \frac {x-\mu}\sigma$
	
	
	
	