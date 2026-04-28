import numpy as np
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from scipy.optimize import curve_fit

# --- paths ---
base_path = Path.cwd()
data_path = base_path / 'C33' / 'Data' / 'Versuch_33(1).xlsx'
img_path = base_path.parent / 'C2-Praktikum' / 'C33' / 'Images'

# --- load data ---
Data = pd.read_excel(
    data_path,
    sheet_name='schwarze Körper SBG',
    engine='openpyxl'
)

# --- extract data ---
U = np.array(Data['Spannung in mV'])
T_K = np.array(Data['Temperatur in °C']) + 273.15

# --- constants ---
T0_K = 293.15  # 20°C

# --- errors ---
errT = 0.1
errU = 0.1

def model(T, A, b):
    return A * (T**b - T0_K**b)

# --- fit ---
popt, pcov = curve_fit(model, T_K, U, p0=[1e-10, 4])
A_fit, b_fit = popt

# --- parameter error ---
b_err = np.sqrt(pcov[1, 1])

print("Fit results:")
print(f"A = {A_fit:.3e}")
print(f"b = {b_fit:.4f} ± {b_err:.4f}")

# --- plotting ---
plt.figure(figsize=(8, 6))

# data
plt.errorbar(
    T_K, U,
    xerr=errT, yerr=errU,
    fmt='x',
    capsize=3,
    label="data"
)

# fit curve
T_fit = np.linspace(min(T_K), max(T_K), 300)
plt.plot(
    T_fit,
    model(T_fit, *popt),
    label=f"fit: b = {b_fit:.3f} ± {b_err:.3f}"
)

# --- styling ---
plt.xlabel("temperature T [K]")
plt.ylabel("U [mV]")
plt.title("U(T) fit: U = A(T^b - T0^b)")
plt.legend()
plt.grid(False)

plt.gca().xaxis.set_minor_locator(AutoMinorLocator(4))
plt.gca().yaxis.set_minor_locator(AutoMinorLocator(4))

plt.tick_params(axis='both', which='major', direction='in', top=True, right=True)
plt.tick_params(axis='both', which='minor', direction='in', top=True, right=True)

plt.tight_layout()
plt.savefig(img_path / "fit_U_T_blackbody.png")
plt.show()


#lin fit
X = T_K**4 - T0_K**4

coeffs = np.polyfit(X, U, 1)
A_lin = coeffs[0]
offset = coeffs[1]

print("\nLinear fit (recommended):")
print(f"A = {A_lin:.3e}")
print(f"offset = {offset:.3e}")

# plot linear fit
plt.figure(figsize=(8, 6))

plt.errorbar(
    X, U,
    xerr=4*T_K**3*errT,
    yerr=errU,
    fmt='x',
    capsize=3,
    label='data',
    color='black'
)

x_fit = np.linspace(min(X), max(X), 300)
plt.plot(x_fit, A_lin * x_fit + offset,
         label=f'U = {A_lin:.3e}·(T⁴-T₀⁴) + {offset:.2e}', color='red')

plt.xlabel("T⁴ - T₀⁴ [K⁴]")
plt.ylabel("U [mV]")
plt.title("U(T^4) linear fit")
plt.legend()

plt.gca().xaxis.set_minor_locator(AutoMinorLocator(4))
plt.gca().yaxis.set_minor_locator(AutoMinorLocator(4))
plt.tick_params(axis='both', which='both', direction='in', top=True, right=True)

plt.tight_layout()
plt.savefig(img_path / "fit_U_T4_Blackbody.png")
plt.show()