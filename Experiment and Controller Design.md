### Hypothesis
1. Anxiety levels and trust levels show almost the same dynamic, regardless of other non-anxiety-related trust factors introduced in the literature.
2. All the trust factors in wearable robots root back to anxiety. Thus, trust in wearable robots can be safely defined, measured, and controlled through anxiety as its proxy.
3. Sensory signals (and cognitive trust) are the core driving signals of trust in wearable robots.

### ⚠ Critical Questions to answer in the first place
1. How to create anxiety, as a sense of *future threat*, not just instant fear ([[Anxiety Definition#^7f3c4d]])?
	-  [**Potential Method**](https://share.google/aimode/N9wiP7sFSBvayslCm) 
		1. **The Baseline Test:** 
			Testing biomarkers before encountering the robot. If they are already elevated just from having the device strapped to you, you are measuring the "hidden state" of anxiety.
		
		2. **The Persistence Test:** 
		   If the biomarkers remain high for the entire duration of the second wear—rather than spiking only during certain movements—it indicates a generalized state of anxiety rather than a specific reaction to the robot's physical performance.

> [!NOTE]
> if the discomfort is driven by **anxiety** (the "hidden state"), your body would likely show heightened biomarkers the next day—even if the robot functions perfectly. 
This is known as **anticipatory anxiety**. While the initial failure caused an acute **stress response**, the memory of that failure creates an internal "threat cue". When you put the robot back on, your brain anticipates another failure, triggering the same physiological "fight-or-flight" biomarkers.

2. Any kind of anxiety inducing stimuli in long term can be judged as "trust loss". how can i prove it was due to anxiety, not sth else?
	- **[Potential methods](https://share.google/aimode/uyZWnSoelqNsoMqHB)**:
		1. Give the user a neutral task (like a simple reaction time game on a tablet) while they are wearing the robot, versus while they are not. If their performance drops or their "stress biomarkers" stay high during the _neutral_ task, it proves they are in a state of **anxious hyper-vigilance**. *Trust loss in the robot shouldn't interfere with their ability to perform an unrelated task.*
		2. Biomarker "Signature" Differentiation: 
		   Anxiety and Trust loss have slightly different physiological "signatures": 
		   **Anxiety Signature:** Characterized by **Lowered Heart Rate Variability (HRV)** and increased **Phasic Skin Conductance** (frequent micro-sweats). This indicates a nervous system that is "locked" in a defensive state. 
		   **Trust Loss (Cognitive):** Often shows up as **increased Mental Workload** biomarkers (like Pupil Dilation or specific EEG bands) because the user is "monitoring" the robot more closely, but they may not show the same "fear-based" heart rate spikes

### Designing and Evaluation of the Experiment
1. **Creating a scenario/setup**
	1. **Task**
		1. what is the setup or task?
	2. **Subject group**
		1. who are our subject group? 
			1. what are the individual factors that affect the response of individuals to external stimuli? (age, health, gender, baseline anxiety level, personality, etc.)
			2. how far i want to take these factors into account/ cancel them in the first place? (limit the subject group to least individual factors)
				1. do the people with those factors shape the majority or minority of the users of the exoskeletons? (e.g., if elderly or health patients use this more than young healthy subjects, how do they react to that kind of stimuli?)
	3. **Stimulation**
		1. finding a definite "anxiety stimulant"
			1. gathering stimulants that are proven to induce anxiety (preferably, anxiety only) and NOT just instant fear/stress
				1. “oddball” tactile events:
					- **Types of Deviance:**
					    - **Spatial:** Stimulation shifts from one location (e.g., left hand) to another (e.g., right hand).
					    - **Intensity/Quality:** A vibration changes in intensity (high vs. low) or texture.
					    - **Omission:** An expected stimulus does not occur, which still produces a "surprising" brain response.
		2. making sure they only, or at least dominantly stimulate anxiety
		3. frequency of stimulation
		4. variation in types of stimuli or same?
		   
2. **Measurement**
		1. what factors to measure to demonstrate the effect (i.e., anxiety and trust level)?
			1. what are the most suitable measures to use for each of the factors of trust/anxiety?
				1. objective measures: 
					1. [***Empatica E4**](https://www.empatica.com/research/e4/) wristband (~1000$) is a commercially available wearable device that records:
						1. photoplethysmography (PPG)-derived interbeat intervals (IBIs)* 
						2. *heart rate (HR), 
						3. temperature, 
						4. electrodermal activity (EDA), 
						5. movement.*
					2. **EEG** 
						1.  [MindWave Mobile](https://www.amazon.com/NeuroSky-MindWave-Mobile-Brainwave-Starter/dp/B07CXN8NKX) found from [DOI](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7428822&casa_token=YZYCHG6hol8AAAAA:exd3WRud7LwA5sj9squjYD00zWvXknTHq67AmOOZOq0HmzQWJ7RDXWTPSMVgPxefxWnuIiz8r4A&tag=1)
						2. [UMind Mirror](https://www.indiegogo.com/en/projects/umindmirror/umind-mirror-smart-eeg-brainwave-wearable-for-you) 
							The UMind Mirror development SDK provides complete access to developers, supporting drivers, APIs, and analysis tools for EEG research applications. This means that developers can create potential applications, such as improving focus, meditation, stress therapy, fitness tracking, mind-controlled computing, interactive television, gaming and entertainment, and smart home integration.
					3. EDA
				2. subjective measures
		2. how the measured values are going to be combined to make sense
		3. frequency of each of the measurements
			1. is it possible to measure it that frequent?
			2. is it ok to measure it that unfrequent?
		
4. **Find the dynamic of anxiety $\propto$ trust**


### Utilizing this Dynamic
1. Are we going to use anxiety as the control signal or feedback? (Is the robot going to adapt its behavior based on anxiety level, or create or reduce anxiety stimulants to maintain trust/anxiety on a certain level?)




- Let's focus on Polyvagal theory only, 