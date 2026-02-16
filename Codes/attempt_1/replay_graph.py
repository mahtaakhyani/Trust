import numpy as np
import matplotlib.pyplot as plt
import os

# Change this to the .npz file you want to inspect
npz_path = os.path.join("Codes/attempt_1/graphs", "2026-02-12_22-02-02.npz")

data = np.load(npz_path)
t = data["t"]

series_names = ["trust", "anxiety", "kp", "kd", "effort", "error", "angle"]
colors = {
    "trust": "skyblue",
    "anxiety": "salmon",
    "kp": "dimgray",
    "kd": "dimgray",
    "effort": "blue",
    "error": "red",
    "angle": "purple",
}
styles = {
    "trust": "-",
    "anxiety": "-",
    "kp": "--",
    "kd": ":",
    "effort": "-",
    "error": "-",
    "angle": "-",
}

plt.figure(figsize=(8, 4))
ax = plt.gca()
for name in series_names:
    ax.plot(t, data[name], color=colors[name], linestyle=styles[name], label=name)

ax.set_title("Replay (raw data)")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Value")
ax.grid(True, alpha=0.2)
ax.legend(loc="upper left", fontsize=8)

plt.show()