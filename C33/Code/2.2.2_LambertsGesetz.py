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
Spannung = np.array([
    [x, y] for x, y in zip(
        Data['Spannung in mV'].tolist(),
        Data['Winkel'].tolist()
    )
])

# --- Linear model U = a*cos(phi) + b ---
def linear_model(cos_phi, a, b):
    return a * cos_phi + b

plt.figure(figsize=(8, 6))

for (data, label) in zip([Spannung], ['Lambert-Gesetz']):
    U = data[:, 0]
    phi_deg = data[:, 1]  # ✅ FIXED: no +273.15
    cos_phi = np.cos(np.radians(phi_deg))

    # --- Errors ---
    errU = errU = 0.00025 * U + 0.00008 * 100  # mV
    errW = 0.1  # degrees (not used in fit here)
    
    # --- Fit ---
    popt, pcov = curve_fit(
        linear_model,
        cos_phi,
        U,
        sigma=np.full_like(U, errU, dtype=float),
        absolute_sigma=True
    )
    
    a_fit, b_fit = popt
    a_err, b_err = np.sqrt(np.diag(pcov))
    
    # --- Fit line ---
    cos_phi_fit = np.linspace(min(cos_phi), max(cos_phi), 300)
    
    # --- Lambert's law (ideal, no offset) ---
    U_lambert = a_fit * cos_phi_fit + b_fit - 0.025  # scale to fit data range
    
    print(f"{label}:")
    print(f"  a = {a_fit:.3e} ± {a_err:.3e}")
    print(f"  b = {b_fit:.3e} ± {b_err:.3e}")
    
    # --- Plot data ---
    plt.errorbar(
    cos_phi,
    U,
    yerr=errU,
    fmt='x',
    capsize=3,
    label="Data",
    color='black'
)

# --- Fit line ---
plt.plot(
    cos_phi_fit,
    linear_model(cos_phi_fit, *popt),
    label="Fit: $U = a \\cos(\\phi) + b$",
    color='red'
)

# --- Lambert (ideal, no offset) ---
plt.plot(
    cos_phi_fit,
    U_lambert,
    linestyle='--',
    color='blue',
    label=r'Lambert (ideal): $U \propto \cos(\phi)$'
)

# --- Styling ---
plt.xlabel(r"$\cos(\phi)$")  
plt.ylabel("U [mV]")
plt.title(r"$U(\cos(\phi))$ - Lambert's Law with linear fit")

plt.legend()
plt.grid(False)

ax = plt.gca()
ax.xaxis.set_minor_locator(AutoMinorLocator(4))
ax.yaxis.set_minor_locator(AutoMinorLocator(4))

plt.tick_params(axis='both', which='major', direction='in', top=True, right=True)
plt.tick_params(axis='both', which='minor', direction='in', top=True, right=True)

plt.tight_layout()

# --- Save ---
plt.savefig(img_path / "individual_fits_U_cos_phi.png")

plt.show()