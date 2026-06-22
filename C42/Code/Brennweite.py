from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline

# ------------------------------------------------------------------
# Daten einlesen
# ------------------------------------------------------------------
base_path = Path.cwd()
data_path = base_path / "C42" / "Data" / "42_Messwerte.xlsx"
img_path = base_path.parent / "C2-Praktikum" / "C42" / "Images"

# Ensure the image directory exists
img_path.mkdir(parents=True, exist_ok=True)

Data = pd.read_excel(
    data_path, sheet_name="2.3 Brennweitenbestimmung", engine="openpyxl"
)

# Extract and sort data (CubicSpline requires strictly increasing x-values)
x_data = Data["x/cm"].to_numpy()
y_data = Data["I/mA"].to_numpy()

sort_indices = np.argsort(x_data)
x_data = x_data[sort_indices]
y_data = y_data[sort_indices]

# Define Given Uncertainties
sigma_x = 1.0  # cm
sigma_I = 0.01  # mA

# ------------------------------------------------------------------
# Smooth Fit (Cubic Spline) & Maximum Detection
# ------------------------------------------------------------------
# Create the nominal spline function
cs = CubicSpline(x_data, y_data)

# Generate a high-resolution x-axis for a perfectly smooth curve
x_smooth = np.linspace(x_data.min(), x_data.max(), 1000)
y_smooth = cs(x_smooth)

# Find the nominal maximum of the smooth curve
max_idx = np.argmax(y_smooth)
x_max = x_smooth[max_idx]
y_max = y_smooth[max_idx]

# ------------------------------------------------------------------
# Monte Carlo Error Propagation for the Maximum (Calculated behind the scenes)
# ------------------------------------------------------------------
n_simulations = 1000
mc_x_max = []
mc_y_max = []

# Seed the generator for reproducibility
rng = np.random.default_rng(42)

for _ in range(n_simulations):
    # Perturb the data points within their Gaussian distributions
    x_perturbed = x_data + rng.normal(0, sigma_x, size=x_data.shape)
    y_perturbed = y_data + rng.normal(0, sigma_I, size=y_data.shape)

    # Spline requires strictly increasing x values, re-sort every iteration
    sort_idx = np.argsort(x_perturbed)
    x_pert_sorted = x_perturbed[sort_idx]
    y_pert_sorted = y_perturbed[sort_idx]

    try:
        # Fit spline to perturbed data
        cs_pert = CubicSpline(x_pert_sorted, y_pert_sorted)
        x_smooth_pert = np.linspace(
            x_pert_sorted.min(), x_pert_sorted.max(), 1000
        )
        y_smooth_pert = cs_pert(x_smooth_pert)

        # Extract the maximum of this simulation
        idx_pert = np.argmax(y_smooth_pert)
        mc_x_max.append(x_smooth_pert[idx_pert])
        mc_y_max.append(y_smooth_pert[idx_pert])
    except ValueError:
        continue

# Calculate standard deviations (uncertainties) of the maximum coordinates
sigma_x_max = np.std(mc_x_max)
sigma_y_max = np.std(mc_y_max)

print("--- Result with Propagated Uncertainties ---")
print(f"Calculated Maximum x: {x_max:.3f} ± {sigma_x_max:.3f} cm")
print(f"Calculated Maximum I: {y_max:.3f} ± {sigma_y_max:.3f} mA")

# ------------------------------------------------------------------
# Plotting (Clean Plot - No Errors)
# ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6), dpi=150)

# Plot original data points as a clean scatter plot (no error bars)
ax.scatter(
    x_data, y_data, marker="x", color="red", s=50, label="Data", zorder=3
)

# Plot the smooth fit line
ax.plot(
    x_smooth,
    y_smooth,
    color="black",
    linewidth=2,
    label="Smooth Fit (Spline)",
    zorder=2,
)


# Highlight the single maximum point (no error bars)
ax.plot(
    x_max,
    y_max,
    marker="v",
    markersize=10,
    color="forestgreen",
    label=f"Maximum ({x_max:.2f} ± {sigma_x_max:.2f}) cm",
    zorder=4,
)

# Axis styling
ax.set_xlabel("x / cm", fontsize=12)
ax.set_ylabel("I / mA", fontsize=12)
ax.set_title("Brennweitenbestimmung", fontsize=14, pad=15)

# Grid and Ticks
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())

ax.legend(loc="best", frameon=True)

plt.tight_layout()

# Save and show
plt.savefig(img_path / "brennweite_fit_clean.png")
plt.show()

g = 80 #cm
sigma_g  = 2

b = x_max - g #cm
sigma_b = np.sqrt((sigma_x_max)**2 + (sigma_g)**2)

f = (g * b)/(g + b)
sigma_f = (f) * np.sqrt((sigma_g / g**2) ** 2 + (sigma_b / b**2) ** 2)
print(f"f = ({f:.3f} ± {sigma_f:.3f}) cm")