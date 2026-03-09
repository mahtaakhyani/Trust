# Motion Types Reference

This module defines four motion types for generating acceleration profiles: smooth (sinusoidal baseline), lag (phase-shifted sinusoid), vibration (short burst of high-frequency oscillation), and sudden_stop (constant impulse). Each type uses simple formulas—sinusoids or step functions—parameterized by frequency, amplitude, duration, and timing. Variables include time `t`, frequency `freq`, amplitude, and type-specific parameters such as `lag`, `burst_freq`, and `impulse_magnitude`. Class constants provide fallback defaults when parameters are omitted. Default values are chosen for typical stressor experiments (e.g., 2 Hz baseline, 50 Hz vibration burst, 10 ms stop impulse).

---

## Motion Types


| Type          | Description                                 |
| ------------- | ------------------------------------------- |
| `smooth`      | Sinusoidal baseline motion                  |
| `lag`         | Phase-lagged sinusoid (delayed smooth)      |
| `vibration`   | Short burst of high-frequency oscillation   |
| `sudden_stop` | Constant impulse (step) over a brief window |


---

## Formulas


| Type            | Formula                                                                                                                             |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **smooth**      | a(t) = A \cdot \sin(2\pi f \cdot t)                                                                                                 |
| **lag**         | a(t) = A \cdot \sin(2\pi f \cdot (t - \tau))                                                                                        |
| **vibration**   | a(t) = A \cdot \sin(2\pi f_{\text{burst}} \cdot (t - t_{\text{start}})) for t \in [t_{\text{start}}, t_{\text{start}} + d] , else 0 |
| **sudden_stop** | a(t) = M for t \in [t_{\text{start}}, t_{\text{start}} + d] , else 0                                                                |


---

## Variables


| Symbol           | Name                              | Unit | Description                                          |
| ---------------- | --------------------------------- | ---- | ---------------------------------------------------- |
| t                | `t`                               | s    | Time vector                                          |
| f                | `freq`                            | Hz   | Base frequency                                       |
| A                | `amplitude`                       | a.u. | Amplitude                                            |
| \tau             | `lag`                             | s    | Phase lag (lag type only)                            |
| t_{\text{start}} | `start_time` / `burst_start_time` | s    | Start of event                                       |
| f_{\text{burst}} | `burst_freq`                      | Hz   | Vibration frequency (vibration only)                 |
| d                | `duration`                        | s    | Event duration                                       |
| M                | `impulse_magnitude`               | a.u. | Constant acceleration during stop (sudden_stop only) |


---

## Class Constants (CreateMotion)


| Constant           | Default | Used when                             |
| ------------------ | ------- | ------------------------------------- |
| `LAG`              | 0.01    | `lag` not provided                    |
| `BURST_FREQ`       | 50.0    | `burst_freq` not provided             |
| `BURST_DURATION`   | 0.1     | `duration` not provided (vibration)   |
| `STOP_DURATION`    | 0.01    | `duration` not provided (sudden_stop) |
| `IMPULE_MAGNITUDE` | 10.0    | `impulse_magnitude` not provided      |


---

## Default Values (motion method)


| Parameter           | Default                        |
| ------------------- | ------------------------------ |
| `motion_type`       | `"smooth"`                     |
| `freq`              | 2.0                            |
| `amplitude`         | 1.0                            |
| `duration`          | 0.02                           |
| `lag`               | None → uses `LAG`              |
| `burst_freq`        | None → uses `BURST_FREQ`       |
| `burst_start_time`  | None                           |
| `impulse_magnitude` | None → uses `IMPULE_MAGNITUDE` |


---

## Example Usage (generate_event_example_signals)


| Condition       | Type                   | Key parameters                                    |
| --------------- | ---------------------- | ------------------------------------------------- |
| Smooth          | smooth                 | `freq=2.0`, `amplitude=1.0`                       |
| Lag_Low         | lag                    | `lag=0.010`                                       |
| Lag_Mid         | lag                    | `lag=0.050`                                       |
| Lag_High        | lag                    | `lag=0.150`                                       |
| Vibration_Burst | baseline + vibration   | `burst_freq=50`, `duration=0.10`, `amplitude=0.5` |
| Sudden_Stop     | baseline + sudden_stop | `duration=0.01`, `impulse_magnitude=10.0`         |


