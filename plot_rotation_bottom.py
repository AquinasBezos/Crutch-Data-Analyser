import csv
import matplotlib.pyplot as plt
import os

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(SCRIPT_DIR, "rotation bottom crutch .csv")


def load_csv(filepath):
    """Load CSV and return lists: time_s, x, y, z, magnitude."""
    time_s, x, y, z, mag = [], [], [], [], []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            time_s.append(float(row["datetime"]))
            x.append(float(row["x"]))
            y.append(float(row["y"]))
            z.append(float(row["z"]))
            mag.append(float(row["magnitude"]))
    return time_s, x, y, z, mag


# --- Load Data ---
t, rx, ry, rz, rmag = load_csv(CSV_FILE)

# Convert to seconds from start
t0 = t[0]
t = [ti - t0 for ti in t]

# --- Styling ---
plt.style.use("dark_background")
COLORS = {"x": "#FF6B6B", "y": "#4ECDC4", "z": "#FFD93D", "mag": "#C084FC"}

# --- Create Figure: 2 subplots ---
# Top: individual x, y, z axes    Bottom: magnitude
fig, (ax_xyz, ax_mag) = plt.subplots(
    2, 1, figsize=(14, 8), sharex=True,
    gridspec_kw={"hspace": 0.12, "height_ratios": [2, 1]},
)
fig.canvas.manager.set_window_title("Rotation — Bottom Crutch")
fig.suptitle("Rotation Rate — Bottom Crutch", fontsize=16, fontweight="bold", y=0.97)

# --- X / Y / Z ---
for vals, label in ((rx, "X"), (ry, "Y"), (rz, "Z")):
    ax_xyz.plot(t, vals, label=label, color=COLORS[label.lower()], lw=0.7, alpha=0.9)
ax_xyz.set_ylabel("Rotation Rate (rad/s)", fontsize=11)
ax_xyz.set_title("X / Y / Z Components", fontsize=12, pad=6, color="#AAAAAA")
ax_xyz.legend(loc="upper right", fontsize=9, framealpha=0.4)
ax_xyz.grid(True, alpha=0.15)
ax_xyz.axhline(0, color="white", lw=0.3, alpha=0.3)

# --- Magnitude ---
ax_mag.plot(t, rmag, label="Magnitude", color=COLORS["mag"], lw=0.8, alpha=0.9)
ax_mag.set_ylabel("Magnitude (rad/s)", fontsize=11)
ax_mag.set_xlabel("Time (s)", fontsize=11)
ax_mag.set_title("Total Magnitude", fontsize=12, pad=6, color="#AAAAAA")
ax_mag.legend(loc="upper right", fontsize=9, framealpha=0.4)
ax_mag.grid(True, alpha=0.15)

# --- Help text ---
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
    for other in (ax_xyz, ax_mag):
        if other is not ax:
            other.set_xlim(ax.get_xlim())
    fig.canvas.draw_idle()


fig.canvas.mpl_connect("scroll_event", on_scroll)
plt.show()
