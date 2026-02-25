import csv
import matplotlib.pyplot as plt
import os

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ACCEL_FILE = os.path.join(SCRIPT_DIR, "Accel first walk.csv")
ROTATION_FILE = os.path.join(SCRIPT_DIR, "rotation first walk.csv")


def load_csv(filepath):
    """Load CSV and return dict of lists: time_s, x, y, z."""
    time_s, x, y, z = [], [], [], []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            time_s.append(float(row["datetime"]))
            x.append(float(row["x"]))
            y.append(float(row["y"]))
            z.append(float(row["z"]))
    return time_s, x, y, z


# --- Load Data ---
a_t, a_x, a_y, a_z = load_csv(ACCEL_FILE)
r_t, r_x, r_y, r_z = load_csv(ROTATION_FILE)

# Convert timestamps to seconds from first sample
t0 = a_t[0]
a_t = [t - t0 for t in a_t]
r_t = [t - t0 for t in r_t]

# --- Styling ---
plt.style.use("dark_background")
COLORS = {"x": "#FF6B6B", "y": "#4ECDC4", "z": "#FFD93D"}

# --- Create Figure ---
fig, (ax_accel, ax_rot) = plt.subplots(
    2, 1, figsize=(14, 8), sharex=True,
    gridspec_kw={"hspace": 0.12},
)
fig.canvas.manager.set_window_title("Crutch Sensor Data")
fig.suptitle("Crutch Sensor Data", fontsize=16, fontweight="bold", y=0.97)

# --- Acceleration ---
for vals, label in ((a_x, "X"), (a_y, "Y"), (a_z, "Z")):
    ax_accel.plot(a_t, vals, label=label, color=COLORS[label.lower()], lw=0.7, alpha=0.9)
ax_accel.set_ylabel("Acceleration (m/s²)", fontsize=11)
ax_accel.set_title("Linear Acceleration", fontsize=12, pad=6, color="#AAAAAA")
ax_accel.legend(loc="upper right", fontsize=9, framealpha=0.4)
ax_accel.grid(True, alpha=0.15)
ax_accel.axhline(0, color="white", lw=0.3, alpha=0.3)

# --- Rotation ---
for vals, label in ((r_x, "X"), (r_y, "Y"), (r_z, "Z")):
    ax_rot.plot(r_t, vals, label=label, color=COLORS[label.lower()], lw=0.7, alpha=0.9)
ax_rot.set_ylabel("Rotation Rate (rad/s)", fontsize=11)
ax_rot.set_xlabel("Time (s)", fontsize=11)
ax_rot.set_title("Rotation Rate", fontsize=12, pad=6, color="#AAAAAA")
ax_rot.legend(loc="upper right", fontsize=9, framealpha=0.4)
ax_rot.grid(True, alpha=0.15)
ax_rot.axhline(0, color="white", lw=0.3, alpha=0.3)

# --- Instruction ---
fig.text(0.5, 0.005,
         "Toolbar: 🔍 Zoom  ·  ✋ Pan  ·  Scroll to zoom  ·  Home to reset",
         ha="center", fontsize=9, color="#888888", style="italic")

plt.tight_layout(rect=[0, 0.025, 1, 0.95])


# --- Scroll-to-zoom ---
def on_scroll(event):
    if event.inaxes is None:
        return
    ax = event.inaxes
    factor = 0.8 if event.button == "up" else 1.25
    xl = ax.get_xlim()
    yl = ax.get_ylim()
    xd, yd = event.xdata, event.ydata
    ax.set_xlim([xd - (xd - xl[0]) * factor, xd + (xl[1] - xd) * factor])
    ax.set_ylim([yd - (yd - yl[0]) * factor, yd + (yl[1] - yd) * factor])
    for other in (ax_accel, ax_rot):
        if other is not ax:
            other.set_xlim(ax.get_xlim())
    fig.canvas.draw_idle()


fig.canvas.mpl_connect("scroll_event", on_scroll)
plt.show()
