import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# ==========================
# Pfade
# ==========================
base_path = Path.cwd()

data_path = base_path / 'C40' / 'Data' / '40_Messdaten.xlsx'
img_path = base_path.parent / 'C2-Praktikum' / 'C40' / 'Images'

# ==========================
# Excel-Datei einlesen
# ==========================
Data = pd.read_excel(
    data_path,
    sheet_name='2.1 Malussche Gesetz',
    engine='openpyxl'
)

# ==========================
# Daten bereinigen
# ==========================
theta_deg = pd.to_numeric(
    Data["teta /in°"],
    errors="coerce"
)

I = pd.to_numeric(
    Data["I /gemessen in mA mit Agilent 34405A"],
    errors="coerce"
)

mask = theta_deg.notna() & I.notna()

theta_deg = theta_deg[mask]
I = I[mask]

# ==========================
# Fitfunktion
# ==========================
def malus(theta_deg, A, theta0, B):
    theta_rad = np.radians(theta_deg - theta0)
    return A * np.cos(theta_rad)**2 + B

# ==========================
# Fit durchführen
# ==========================
p0 = [
    I.max() - I.min(),  # A
    0,                  # theta0
    I.min()             # B
]

params, cov = curve_fit(
    malus,
    theta_deg,
    I,
    p0=p0
)

A_fit, theta0_fit, B_fit = params

print("Fitparameter:")
print(f"A      = {A_fit:.4f} mA")
print(f"theta0 = {theta0_fit:.2f}°")
print(f"B      = {B_fit:.4f} mA")

# ==========================
# Fitkurve erzeugen
# ==========================
theta_fit_deg = np.linspace(0, 360, 1000)
I_fit = malus(theta_fit_deg, *params)

# ==========================
# Polarplot
# ==========================
import matplotlib.cm as cm
import matplotlib.colors as mcolors

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='polar')

# --- Colormap setup ---
cmap = cm.plasma
I_min = min(I.min(), I_fit.min())
I_max = max(I.max(), I_fit.max())
norm = mcolors.Normalize(vmin=I_min, vmax=I_max)

# --- Messwerte: color by intensity ---
sc = ax.scatter(
    np.radians(theta_deg),
    I,
    c=I,
    cmap=cmap,
    norm=norm,
    s=60,
    marker='x',
    linewidths=1.5,
    zorder=5,
    label='Data'
)

# --- Fit: colored line segments by intensity ---
theta_fit_rad = np.radians(theta_fit_deg)
for i in range(len(theta_fit_rad) - 1):
    ax.plot(
        theta_fit_rad[i:i+2],
        I_fit[i:i+2],
        color=cmap(norm(I_fit[i])),
        linewidth=2.5
    )

# --- Theoretical Malus curve: I_max * cos²(θ) ---
I_max_data = I.max()
I_theo = I_max_data * np.cos(theta_fit_rad)**2
ax.plot(
    theta_fit_rad,
    I_theo,
    color='grey',
    linewidth=1.5,
    linestyle='--',
    zorder=3,
    label='Theory'
)

# Dummy line for legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color=cmap(0.8), linewidth=2.5, label='Fit: A cos²(θ - θ₀) + B'),
    Line2D([0], [0], color='grey', linewidth=1.5, linestyle='--', label='Theory: I_max cos²(θ)'),
    Line2D([0], [0], marker='x', color=cmap(0.8), markerfacecolor=cmap(0.8),
           markersize=8, linestyle='None', label='Data')
]
ax.set_theta_zero_location('E')
ax.set_theta_direction(1)
ax.legend(handles=legend_elements, loc='upper right')

# Colorbar
sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, pad=0.1, shrink=0.7)
cbar.set_label('Intensity I (mA)')

plt.tight_layout()

# ==========================
# Speichern
# ==========================
img_path.mkdir(parents=True, exist_ok=True)

save_file = img_path / 'Malus_Fit_Polarplot.png'
plt.savefig(save_file, dpi=300, bbox_inches='tight')

plt.show()