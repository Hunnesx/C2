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

# --- Errors ---
errU = 0.1  # mV
errW = 0.1  # degrees (not used in fit here)

# --- Linear model U = a*cos(phi) + b ---
def linear_model(cos_phi, a, b):
    return a * cos_phi + b

plt.figure(figsize=(8, 6))

for (data, label) in zip([Spannung], ['Lambert-Gesetz']):
    U = data[:, 0]
    phi_deg = data[:, 1]  # ✅ FIXED: no +273.15

    # convert to cos(phi)
    cos_phi = np.cos(np.deg2rad(phi_deg))

    # --- Fit ---
    popt, pcov = curve_fit(
        linear_model,
        cos_phi,
        U,
        sigma=np.full_like(U, errU),  # include y-error
        absolute_sigma=True
    )

    a_fit, b_fit = popt
    a_err, b_err = np.sqrt(np.diag(pcov))

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
        label=f"Data",
        color='black'
    )

    # --- Fit line ---
    cos_phi_fit = np.linspace(min(cos_phi), max(cos_phi), 300)
    plt.plot(
        cos_phi_fit,
        linear_model(cos_phi_fit, *popt),
        label= "Lambert's Law (linear fit in $\cos(\phi)$)",
        color='red'
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