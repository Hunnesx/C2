from matplotlib import ticker
import numpy as np
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from scipy.optimize import curve_fit

# --- Import data ---
base_path = Path.cwd()
data_path = base_path / 'C33' / 'Data' / 'Versuch_33(1).xlsx'

img_path = base_path.parent / 'C2-Praktikum' / 'C33' / 'Images'


Data = pd.read_excel(
    data_path,
    sheet_name='Lambert-Gesetz',
    engine='openpyxl'
)

# --- Extract data ---
U = np.array(Data['Spannung in mV'].tolist())
phi = np.array(Data['Winkel'].tolist())

# --- Sort by angle (important for plotting & fitting) ---
sort_idx = np.argsort(phi)
phi = phi[sort_idx]
U = U[sort_idx]

# --- Normalize voltage to U(phi=0) = 1 ---
# Find value closest to phi = 0
idx0 = np.argmin(np.abs(phi))
U0 = U[idx0]
U_norm = U / U0

# --- Restrict to range 0° to 50° ---
mask = (phi >= 0) & (phi <= 50)
phi = phi[mask]
U_norm = U_norm[mask]

# --- Fit function ---
def fit_func(phi, a, b, c, d):
    return a * np.cos(np.deg2rad(b * phi) + c) + d
    # note: convert degrees → radians inside cos

# --- Initial guesses (important for convergence) ---
p0 = [0.5, 1.0, 0.0, 0.5]

# --- Fit ---
params, cov = curve_fit(fit_func, phi, U_norm, p0=p0)
a, b, c, d = params

print(f"Fit parameters:")
print(f"a = {a}")
print(f"b = {b}")
print(f"c = {c}")
print(f"d = {d}")

# --- Generate smooth curve for plotting ---
phi_fit = np.linspace(0, 50, 500)
U_fit = fit_func(phi_fit, *params)

# --- Lambert's law (normalized) ---
I_lambert = np.cos(np.deg2rad(phi_fit))

# --- Plot ---
plt.figure(figsize=(8,6))

plt.errorbar(phi, U_norm, yerr=0.00025 * U + 0.00008 * 100/U0, fmt='o', label='Data', capsize=3, color='black')
plt.plot(phi_fit, U_fit, 
         label=f'Fit: U = {a:.2f} cos({b:.2f} $\phi$ + {c:.2f}) + {d:.2f}', 
         color='red')

plt.plot(phi_fit, I_lambert, 
         linestyle='--', 
         label=r'Lambert: $I = \cos(\phi)$',
         color='blue')

plt.xlabel(r'$\phi$ (degrees)')
plt.ylabel(r'$U(\phi)$ (normalized)')
plt.title('Normalized Voltage U($\phi$) with fit: $U = a \cos(b \phi + c) + d$')

plt.legend()
plt.grid(False)
plt.gca().xaxis.set_minor_locator(AutoMinorLocator())
plt.gca().yaxis.set_minor_locator(AutoMinorLocator())

plt.tick_params(axis='both', which='major', direction='in', top=True, right=True)
plt.tick_params(axis='both', which='minor', direction='in', top=True, right=True)

plt.tight_layout()
plt.savefig(img_path / "lambert_U_phi.png")
plt.show()