$$
\tilde{T}_t = \tilde{T}_{t-1} - \ln(A_t)
$$
$$
\text{trust}_t = T_{\max}\cdot \frac{1}{1 + \exp(-\lambda(\tilde{T}_t - T_0))}
$$
where:

$$
A_t = A_{\text{init}}
+ \ln\!\big(1 + \text{temporal\ tolerance}\big)\cdot \big(\text{prediction} - \text{perceived data}\big)\ \cdot \ \frac{1}{\sigma^2}
\cdot {k_\tau}\ dt+\int_{\tau = 0}^{\tau = t} A_{\tau}\ e^{-\frac{1}{k_\tau}\,\tau} \ d\tau
$$

$$
\text{perceived data}_t = \text{real data }_t \cdot \pi \cdot \text{anxiety level}_t
$$

$$
\text{predicted data}_t = \gamma_t \cdot \text{perceived data}_{t−1}​+(1−\gamma) \cdot \text{predicted data}_{t−1}​
$$
$$
\gamma_t
========

\gamma_{\max}
\cdot
\exp!\Big(-\frac{(A_t - A^*)^2}{2\sigma_A^2}\Big)
\cdot
\frac{c}{k_t + c}
\cdot
\frac{1}{1 + \beta \cdot \text{age}}
$$
$$\pi ={\frac{1}{(1 + \ \beta\  \cdot\  \text{age})}}\ + \alpha \cdot \text{anxiety level }$$
where:
- $A = \text{anxiety level}$
- $\sigma^2 = \text{varience of prediction errors}$
- ${k}$ = Contextual criticality factor (depends on how threatening an event has been at ${\tau}$ = t)


- $\pi=$ Precision factor based on individual traits
- $
\text{temporal tolerance} \rightarrow \text{Reduced by 20-40\% after each threatning signal during the cortisol washout window (≈60-90mins)}
$



* $A^*$ = optimal anxiety for adaptation (task-dependent)
* $\sigma_A$ = width of tolerance window
* $\gamma_{\max} < 1$
* $T_{\max}$ = 7 (Trust scale/embodiment ceiling)
* $T_0$ = 5 (midpoint/ when robot starts to feel “natural”)
* $\lambda$ = sharpness of saturation

- $c$ = constant (e.g., 1)
- $\alpha$ = anxiety sensitivity parameter (based on personality traits)
- $\beta$ = age sensitivity parameter