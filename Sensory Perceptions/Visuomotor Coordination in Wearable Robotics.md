# Visuomotor Coordination in Wearable Robotics

This report explores how **visuomotor coordination—the brain's ability to synchronize movement with visual perception**—influences the design, adaptation, and performance metrics of wearable robotic systems.

---
## Questions
→ Does visuomotor affect the content of designing controllers for wearable robots?

→ Do difficulties in an individual's visuomotor change how the robot should help or adapt?

→ Do differences in individuals' visuomotor levels change the definition of performance in wearable robots?

## 1. Impact on Controller Design
Visuomotor coordination is a primary driver in the development of **biomimetic controllers**. Engineers use models of human gaze-motor coupling to ensure that the robot does not interfere with the user's natural movement intent.

* **Shared Control & Gaze Integration:** Modern controllers increasingly incorporate eye-gaze tracking to predict user intent. By understanding the "visuomotor lead time" (the temporal gap between visual fixation and motor execution), controllers can pre-activate motors, reducing perceived system latency.
* **Trajectory Constraints:** Designing controllers that enforce specific kinematic pathways improves task precision, provided these pathways align with the user’s internal visuomotor models.
* **Claim:** Visuomotor principles are used to estimate parameters for "intention-detection" algorithms, shifting robot control from purely reactive to predictive.
* **Citations:** * Lukic, L. (2015). *Visuomotor Coordination in Reach-to-Grasp Tasks: From Humans to Humanoids*. EPFL Thesis.
    * Masia, L., et al. (2020). Intention-Detection Strategies for Upper Limb Exosuits. *IEEE BIOROB*.

---

## 2. Adaptation to Individual Visuomotor Difficulties
When an individual has visuomotor deficits (due to stroke or neurodegenerative conditions), the robot must transition from a passive assistant to an **active guide**.

* **Personalization of Assistance:** Research suggests that "one-size-fits-all" controllers can hinder neuroplasticity. For users with high visuomotor error, robots must provide **"error augmentation"** (exaggerating mistakes to help the brain notice them) or **"haptic guidance"** (physically guiding the limb).
* **Visual Biofeedback:** In users with slow adaptation rates, adding secondary visual aids (e.g., augmented reality displays) can "bypass" damaged natural visuomotor pathways to accelerate the learning of robot-assisted movement.
* **Claim:** Robots must adapt by modulating "Assistance-as-Needed" (AAN) gains based on the user's specific rate of visuomotor adaptation, as rigid constraints can impede the acquisition of new motor skills.
* **Citations:** * Schiele, A., & van der Helm, F. C. (2006). Kinematic design to improve ergonomics. *IEEE Transactions*.
    * Cazarez, M. (2021). *The Effect of Stance Visual Feedback on Exoskeleton Adaptation*. eScholarship.

---

## 3. Redefining "Performance" in Wearable Robots
The definition of "performance" is shifting from purely mechanical metrics to **human-machine fluency**.

* **Skill-Normalized Performance:** Performance is increasingly defined by the robot's ability to bridge the **"skill gap."** If a robot provides more benefit to a user with lower visuomotor skill than to an expert, its "performance" is considered higher for that specific context.
* **Co-Adaptation as Success:** "Expert" performance is reached when the user’s visuomotor system has fully "internalized" the robot’s physics. This is measured by the stability of movement trajectories and a decrease in visual attention (cognitive load).
* **Claim:** Visuomotor skill level is a predictor of learning capacity; therefore, robot performance is defined by the speed of the user’s "proprioceptive recalibration" and the reduction in visual error-correction effort.
* **Citations:** * Beckerle, P., et al. (2017). Human-robot integration: From biology to technology. *Science Robotics*.
    * Ruttle, J. (2021). *Factors impacting the time course of visuomotor reach adaptation*. YorkSpace.

---

## Reference

* **Beckerle, P., et al. (2017).** Human-robot integration: From biology to technology. *Science Robotics*, 2(10). doi:10.1126/scirobotics.aan4441.
* **Casadio, M., et al. (2014).** Characterizing the human-robot haptic dyad in robot therapy. *International Journal of Intelligent Computing and Cybernetics*.
* **Cazarez, M. (2021).** *The Effect of Stance Visual Feedback on Exoskeleton Adaptation*. University of California, Irvine.
* **Cressman, E. K., & Henriques, D. Y. (2010).** Reach adaptation and proprioceptive recalibration. *Journal of Neurophysiology*, 103(4), 1888-1895.
* **Krakauer, J. W. (2006).** Motor learning: Stages of learning and regional brain involvement. *The Neuroscientist*, 12(1), 84-90.
* **Lukic, L. (2015).** *Visuomotor Coordination in Reach-to-Grasp Tasks: From Humans to Humanoids*. EPFL Thesis.
* **Masia, L., et al. (2020).** Intention-Detection Strategies for Upper Limb Exosuits: Model-Based Myoelectric vs Dynamic-Based Control. *IEEE BIOROB*.
* **Ruttle, J. (2021).** *Factors impacting the time course of visuomotor reach adaptation*. York University.
* **Schiele, A., & van der Helm, F. C. (2006).** Kinematic design to improve ergonomics in human-machine interaction. *IEEE Transactions on Neural Systems and Rehabilitation Engineering*, 14(4), 456-469.