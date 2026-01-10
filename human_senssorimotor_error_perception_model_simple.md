# Human Sensorimotor Error Perception Model (Event-Based Tasks)

The proposed model:  
$$ E_{human} = |A| \cdot \sigma\left(\beta(|\Delta t| - t_0)\right) $$
Where: 
$$        ( A ) = \text{action error magnitude}$$
$$        ( \Delta t ) = \text{delay relative to human motor intent}$$
$$        ( \sigma ) = sigmoid $$
$$ ( t_0 ) = \text{temporal tolerance window}$$
$$       ( \beta ) = \text{sharpnes (individual-dependent)}$$

quantifies human perceptual error based on **action error magnitude** and **delay relative to motor intent** using a sigmoid function. This model aligns with the concept of human perceptual–sensorimotor modeling by capturing how humans perceive discrepancies in wearable robot actions. 

## Research Backup
Research highlights that human sensorimotor systems rely on prediction and error signals to adapt to robotic assistance, with models often emphasizing the minimization of prediction errors and the integration of sensory feedback to maintain embodiment and trust in wearable devices  (*Oliver et al., 2021; Xia et al., 2024; Chang et al., 2025*). 

The temporal tolerance window \(**t_0** \) and sharpness parameter \( **beta** \) reflect individual differences in sensitivity to timing errors, consistent with findings that human perception of robotic action errors depends on temporal and force mismatches  (*Chang et al., 2025; Ehrlich & Cheng, 2018*). 

While most existing models focus on control-theoretic or computational frameworks, some studies incorporate perceptual and cognitive aspects, such as error-related potentials (ErrPs) measured via EEG, to assess how humans detect and respond to robot errors in real time  (*Ehrlich & Cheng, 2018*). The sigmoid function in the model effectively represents a nonlinear perceptual threshold, which is supported by evidence that human sensorimotor error detection is not linear but involves thresholding and saturation effects  (*Saygin et al., 2011; Ehrlich & Cheng, 2018*). 


## Conclusion
Overall, this simple model captures key elements of human perceptual–sensorimotor response to wearable robot action errors, though further validation with neurophysiological data and adaptation to individual variability would enhance its applicability  (*Oliver et al., 2021; Ehrlich & Cheng, 2018*).


 
## References
 
Oliver, G., Lanillos, P., & Cheng, G. (2021). An Empirical Study of Active Inference on a Humanoid Robot. *IEEE Transactions on Cognitive and Developmental Systems*, 14, 462-471. https://doi.org/10.1109/tcds.2021.3049907
 
Xia, H., Zhang, Y., Rajabi, N., Taleb, F., Yang, Q., Kragic, D., & Li, Z. (2024). Shaping high-performance wearable robots for human motor and sensory reconstruction and enhancement. *Nature Communications*, 15. https://doi.org/10.1038/s41467-024-46249-0
 
Chang, E., Torres, W., & Stuart, H. (2025). Error recovery in wearable robotic Co-Grasping: the role of human-led correction. *Frontiers in Robotics and AI*, 12. https://doi.org/10.3389/frobt.2025.1598296
 
Saygin, A., Chaminade, T., Ishiguro, H., Driver, J., & Frith, C. (2011). The thing that should not be: predictive coding and the uncanny valley in perceiving human and humanoid robot actions. *Social Cognitive and Affective Neuroscience*, 7, 413 - 422. https://doi.org/10.1093/scan/nsr025
 
Ehrlich, S., & Cheng, G. (2018). A Feasibility Study for Validating Robot Actions Using EEG-Based Error-Related Potentials. *International Journal of Social Robotics*, 11, 271 - 283. https://doi.org/10.1007/s12369-018-0501-8
 


