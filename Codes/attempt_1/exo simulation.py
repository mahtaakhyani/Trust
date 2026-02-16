import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np
import os
from datetime import datetime
import time

# --- 1. THE STABLE CONTROLLER ---
class PDController:
    def __init__(self, kp=1.2, kd=0.3):
        self.kp, self.kd = kp, kd
        self.prev_error = 0

    def calculate(self, target, current, trust, anxiety, dt=0.03):
        # ERROR: Target (1.8) - Current (1.5) = +0.3 (NEEDS UPWARD FORCE)
        error = target - current
        derivative = (error - self.prev_error) / dt
        self.prev_error = error
        
        # Trust scales the response; Anxiety adds jitter
        noise = np.random.normal(0, anxiety * 0.05)
        eff_trust = np.clip(trust + noise, 0, 1.2)
        
        # PD Law: If error is +, output is + (Upward)
        return eff_trust * (self.kp * error + self.kd * derivative)

# --- 2. SETUP ---
L1, L2 = 1.0, 1.0
TARGET_Y = 1.85 
START_TIME = time.time()
state = {'hip_y': 1.85, 'auto': True, 'dragging': False, 'v': 0.0}
ctrl = PDController(kp=1.5, kd=0.4) # Stronger defaults to fight gravity

# Figure and axes layout: main view on the left, live trends on the right
fig = plt.figure(figsize=(11, 6.5))
gs = fig.add_gridspec(
    1,
    2,
    width_ratios=[1.2, 1.0],
    left=0.30,
    right=0.98,
    bottom=0.12,
    top=0.9,
    wspace=0.35,
)
ax = fig.add_subplot(gs[0, 0])          # main exoskeleton view
ax_trend = fig.add_subplot(gs[0, 1])    # live trends view

# Sliders (fixed on the left side of the figure)
slider_positions = [0.8, 0.7, 0.6, 0.5, 0.35, 0.25]
s_ax = [fig.add_axes([0.04, y, 0.18, 0.035]) for y in slider_positions]
labels = ['Trust', 'Anxiety', 'Kp', 'Kd', 'Effort', 'Sensor Error']
inits = [1.0, 0.1, 1.5, 0.4, 0.4, 0.0]
colors = ['skyblue', 'salmon', 'gray', 'gray', 'blue', 'red']

# Sensor Error: Positive = Too High, Negative = Too Low
sliders = [
    Slider(ax_slider, label, -1.5, 2.5 if 'K' in label else 1.5, valinit=init, color=color)
    for ax_slider, label, init, color in zip(s_ax, labels, inits, colors)
]
s_trust, s_anxiety, s_kp, s_kd, s_effort, s_sensor_err = sliders

# Make slider labels more compact to avoid overlap
for slider in sliders:
    slider.label.set_fontsize(8)

# Interaction
def on_press(event): 
    if event.inaxes == s_sensor_err.ax: state['dragging'] = True
def on_release(event): 
    state['dragging'] = False

fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)

# Mode Button
ax_btn = plt.axes([0.05, 0.85, 0.2, 0.05])
btn = Button(ax_btn, 'Mode: AUTO', color='lime')

def toggle(event):
    state['auto'] = not state['auto']
    btn.label.set_text(f"Mode: {'AUTO' if state['auto'] else 'MANUAL'}")
    btn.color = 'lime' if state['auto'] else 'yellow'
    # In AUTO mode, only Trust and Anxiety are locked; gains remain tunable
    for s in [s_trust, s_anxiety]:
        s.set_active(not state['auto'])
        s.poly.set_alpha(1.0 if not state['auto'] else 0.2)

btn.on_clicked(toggle)
for s in [s_trust, s_anxiety]:
    s.set_active(False)
    s.poly.set_alpha(0.2)

# --- Live trends setup ---
history = {
    't': [],
    'trust': [],
    'anxiety': [],
    'kp': [],
    'kd': [],
    'effort': [],
    'error': [],
    'angle': [],
}

# Scale factors to fit everything on the same axes
scales = {
    'trust': 1.0 / 1.5,
    'anxiety': 1.0 / 1.5,
    'kp': 1.0 / 2.5,
    'kd': 1.0 / 2.5,
    'effort': 1.0 / 1.5,
    'error': 1.0 / 1.5,
    'angle': 1.0 / 180.0,  # degrees -> roughly [-1, 1] range
}

ax_trend.set_title("Live Trends", pad=6)
ax_trend.set_xlabel("Time (s)")
ax_trend.set_ylabel("Scaled value")
ax_trend.set_ylim(-1.1, 1.1)
ax_trend.grid(True, alpha=0.2)
ax_trend.tick_params(labelsize=8)

ax.set_title("Exoskeleton View", pad=6)
ax.tick_params(labelsize=8)

lines = {}
lines['trust'], = ax_trend.plot([], [], color=colors[0], label='Trust')
lines['anxiety'], = ax_trend.plot([], [], color=colors[1], label='Anxiety')
lines['kp'], = ax_trend.plot([], [], color='dimgray', linestyle='--', label='Kp')
lines['kd'], = ax_trend.plot([], [], color='dimgray', linestyle=':', label='Kd')
lines['effort'], = ax_trend.plot([], [], color=colors[4], label='Effort')
lines['error'], = ax_trend.plot([], [], color=colors[5], label='Error')
lines['angle'], = ax_trend.plot([], [], color='purple', label='Joint angle')

ax_trend.legend(loc='upper left', fontsize=8, framealpha=0.8)

scale_info = "\n".join([
    f"Trust×{scales['trust']:.2f}",
    f"Anxiety×{scales['anxiety']:.2f}",
    f"Kp×{scales['kp']:.2f}",
    f"Kd×{scales['kd']:.2f}",
    f"Effort×{scales['effort']:.2f}",
    f"Error×{scales['error']:.2f}",
    f"Angle×{scales['angle']:.3f}",
])
ax_trend.text(
    0.99,
    0.01,
    scale_info,
    transform=ax_trend.transAxes,
    ha='right',
    va='bottom',
    fontsize=7,
    bbox=dict(boxstyle='round', facecolor='white', alpha=0.7, edgecolor='none'),
)

# Let Matplotlib optimize layout for all texts, but keep room on the left for sliders
fig.tight_layout(rect=[0.29, 0.08, 0.98, 0.95])

# --- 3. MAIN LOOP ---
plt.ion()
while plt.fignum_exists(fig.number):
    dt = 0.03
    
    if state['auto']:
        ctrl.kp, ctrl.kd = s_kp.val, s_kd.val
        
        # If user is dragging slider, we bypass the real position
        if state['dragging']:
            current_pos = TARGET_Y - s_sensor_err.val
        else:
            current_pos = state['hip_y']
            s_sensor_err.set_val(TARGET_Y - current_pos) # Update slider for visual feedback
            
        # 1. Calculate Torque (Upward is Positive)
        torque = ctrl.calculate(TARGET_Y, current_pos, s_trust.val, s_anxiety.val, dt)
        
        # 2. Physics: Velocity = Torque + Effort - Gravity (0.5)
        # We use a velocity-based update for smoothness
        state['v'] = (torque + s_effort.val - 0.5) 
        state['hip_y'] += state['v'] * dt * 2
        
    else:
        # MANUAL MODE: Direct kinematic control
        state['hip_y'] = TARGET_Y - s_sensor_err.val
        state['v'] = 0
        ctrl.prev_error = s_sensor_err.val

    # Hard Safety Limits
    state['hip_y'] = np.clip(state['hip_y'], 0.1, 1.98)

    # --- Draw ---
    ax.clear()
    # Slightly smaller view window so annotations fit more comfortably
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(0, 2.7)
    ax.grid(True, alpha=0.2)
    ax.set_ylabel("Height (Meters)"); ax.set_xlabel("Lateral (Meters)")
    
    # Inverse Kinematics
    ky = state['hip_y'] / 2.0
    kx = np.sqrt(max(0, L1**2 - (state['hip_y'] - ky)**2))
    
    # Body
    ax.plot([0, kx, 0], [0, ky, state['hip_y']], color='navy', lw=16, solid_capstyle='round')
    ax.scatter([0, kx, 0], [0, ky, state['hip_y']], s=700, c='black', zorder=3)
    ax.add_patch(plt.Rectangle((-0.2, state['hip_y']), 0.4, 0.4, color='gray', alpha=0.3))
    
    # Visual Feedback
    ax.axhline(y=TARGET_Y, color='red', ls='--', alpha=0.5)
    # Place time inside the axes using relative coordinates so it never clips
    ax.text(
        0.02,
        0.95,
        f"TIME: {time.time()-START_TIME:.1f}s",
        transform=ax.transAxes,
        weight='bold',
        fontsize=10,
        va='top',
    )
    # Color text red if falling, green if stable
    err_color = 'red' if abs(s_sensor_err.val) > 0.05 else 'green'
    ax.text(0.1, state['hip_y'], f"ERROR: {s_sensor_err.val:+.2f}m", color=err_color, weight='bold')

    # Joint angle at the knee (degrees)
    v1 = np.array([0 - kx, 0 - ky])               # knee -> ankle
    v2 = np.array([0 - kx, state['hip_y'] - ky])  # knee -> hip
    cosang = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-9)
    angle_deg = np.degrees(np.arccos(np.clip(cosang, -1.0, 1.0)))

    # Update live history
    t_now = time.time() - START_TIME
    history['t'].append(t_now)
    history['trust'].append(s_trust.val)
    history['anxiety'].append(s_anxiety.val)
    history['kp'].append(s_kp.val)
    history['kd'].append(s_kd.val)
    history['effort'].append(s_effort.val)
    history['error'].append(s_sensor_err.val)
    history['angle'].append(angle_deg)

    # Update trend lines (scaled)
    if history['t']:
        t_data = history['t']
        for key in ['trust', 'anxiety', 'kp', 'kd', 'effort', 'error', 'angle']:
            scaled_values = np.array(history[key]) * scales[key]
            lines[key].set_data(t_data, scaled_values)

        t_last = t_data[-1]
        t_first = max(0.0, t_last - 10.0)
        ax_trend.set_xlim(t_first, max(10.0, t_last))
    
    plt.pause(0.01)

# --- 4. SAVE TRENDS GRAPH ON CLOSE ---
# Save the complete history (entire run) as an SVG in ./graphs when the window is closed.
graphs_dir = os.path.join(os.getcwd(), "graphs")
os.makedirs(graphs_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"{timestamp}.svg"
save_path = os.path.join(graphs_dir, filename)

if history['t']:
    # Recreate a clean trends-only figure using the full stored history.
    fig_trend, ax_trend_save = plt.subplots(figsize=(6, 4))
    ax_trend_save.set_title("Live Trends (Full Run)")
    ax_trend_save.set_xlabel("Time (s)")
    ax_trend_save.set_ylabel("Scaled value")
    ax_trend_save.set_ylim(-1.1, 1.1)
    ax_trend_save.grid(True, alpha=0.2)

    t_data = history['t']
    t_first = t_data[0]
    t_last = t_data[-1]
    ax_trend_save.set_xlim(t_first, max(10.0, t_last))

    # Plot each scaled series, keeping colors consistent with the UI.
    series_colors = {
        'trust': 'skyblue',
        'anxiety': 'salmon',
        'kp': 'dimgray',
        'kd': 'dimgray',
        'effort': 'blue',
        'error': 'red',
        'angle': 'purple',
    }
    series_styles = {
        'trust': '-',
        'anxiety': '-',
        'kp': '--',
        'kd': ':',
        'effort': '-',
        'error': '-',
        'angle': '-',
    }

    for key in ['trust', 'anxiety', 'kp', 'kd', 'effort', 'error', 'angle']:
        scaled_values = np.array(history[key]) * scales[key]
        ax_trend_save.plot(
            t_data,
            scaled_values,
            color=series_colors[key],
            linestyle=series_styles[key],
            label=key.capitalize() if key != 'kd' else 'Kd',
        )

    ax_trend_save.legend(loc='upper left', fontsize=8, framealpha=0.8)

    scale_info = "\n".join([
        f"Trust×{scales['trust']:.2f}",
        f"Anxiety×{scales['anxiety']:.2f}",
        f"Kp×{scales['kp']:.2f}",
        f"Kd×{scales['kd']:.2f}",
        f"Effort×{scales['effort']:.2f}",
        f"Error×{scales['error']:.2f}",
        f"Angle×{scales['angle']:.3f}",
    ])
    ax_trend_save.text(
        0.99,
        0.01,
        scale_info,
        transform=ax_trend_save.transAxes,
        ha='right',
        va='bottom',
        fontsize=7,
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.7, edgecolor='none'),
    )

    fig_trend.tight_layout()
    fig_trend.savefig(save_path, format="svg")
