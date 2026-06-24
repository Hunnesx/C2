import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 2.7 Polarisation von Mikrowellen
# Polarplot wie in der Abbildung
# ============================================================

# Winkel in Grad
theta_deg = np.array([
    0, 10, 20, 30, 40,
    50, 60, 70, 80,
    90, 100, 110, 120,
    130, 140, 150, 160,
    170, 180
])

# Normalisierte Intensitäten
I = np.array([
    0.264, 0.248, 0.218,0.196, 0.209, 0.275, 0.337, 0.424,
    0.47, 0.486, 0.478, 0.435, 0.354, 0.284, 0.232, 0.215,
    0.222, 0.254, 0.266
])

# Umrechnung in Radiant
theta = np.deg2rad(theta_deg)

# ============================================================
# Plot
# ============================================================

fig = plt.figure(figsize=(11,7))

ax = fig.add_subplot(111, projection='polar')

# Nur Halbkreis
ax.set_thetamin(0)
ax.set_thetamax(180)

# 0° rechts
ax.set_theta_zero_location("E")

# mathematisch positiver Drehsinn
ax.set_theta_direction(1)

# Radius
ax.set_ylim(0, 1.0)

# Winkelgitter
ax.set_thetagrids(
    [0, 30, 60, 90, 120, 150, 180],
    fontsize=18
)

# Radiale Ticks
ax.set_rticks([0.2, 0.4, 0.6, 0.8])

ax.set_rlabel_position(0)

# Größe radialer Labels
for label in ax.get_yticklabels():
    label.set_fontsize(16)

# Grid
ax.grid(
    True,
    linestyle='--',
    linewidth=1.2,
    alpha=0.6
)

# Datenlinie
ax.plot(
    theta,
    I,
    color='red',
    linewidth=2,
    marker='x',
    markersize=12,
    markeredgewidth=2.5,
    label='transmitted intensity'
)

# Titel
plt.title(
    "2.7 Polarisation von Mikrowellen",
    fontsize=34,
    pad=40
)

# y-Label links
fig.text(
    0.06,
    0.38,
    "normalised intensity",
    rotation=90,
    fontsize=28,
    va='center'
)

# Legende
plt.legend(
    loc='upper right',
    bbox_to_anchor=(1.12, 1.12),
    frameon=True,
    edgecolor='black',
    fancybox=False,
    fontsize=18
)

plt.tight_layout()

plt.show()