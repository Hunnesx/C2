import numpy as np
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from scipy.optimize import curve_fit

# --- paths ---
base_path = Path.cwd()
data_path = base_path / 'Data' / 'Versuch_33.xlsx'
img_path = base_path.parent / 'C33' / 'Images'

# --- load data ---
Data = pd.read_excel(
    data_path,
    sheet_name='Stefan-Boltzmann Gesetz',
    engine='openpyxl'
)

# --- extract datasets ---
SeiteSchwarz = np.array(list(zip(Data['schwarz Spannung in mV'], Data['Temperatur in °C'])))
SeiteWeiss = np.array(list(zip(Data['weiß Spannung in mV'], Data['Temperatur in °C'])))
SeiteNickelPoliert = np.array(list(zip(Data['vernickelt (poliert) Spannung in mV'], Data['Temperatur in °C'])))
SeiteNickelMatt = np.array(list(zip(Data['vernickelt (matt) Spannung in mV'], Data['Temperatur in °C'])))

datasets = [
    (SeiteSchwarz, "black"),
    (SeiteWeiss, "white"),
    (SeiteNickelPoliert, "nickel polished"),
    (SeiteNickelMatt, "nickel matt")
]

# --- constants ---
T0_K = 20 + 273.15
errT = 0.1
errU = 0.1

# --- model ---
def model(T, A, b):
    return A * (T**b - T0_K**b)

# --- plotting ---

colors = ["black", "tab:red", "tab:blue", "tab:green"]

plt.figure(figsize=(8, 6))

b_values = []

for (data, label), color in zip(datasets, colors):
    U = data[:, 0]
    T_K = data[:, 1] + 273.15

    # --- fit ---
    popt, pcov = curve_fit(model, T_K, U, p0=[1e-10, 4])
    A_fit, b_fit = popt

    # --- GAUSS ERROR (standard deviation from covariance matrix) ---
    b_err = np.sqrt(pcov[1, 1])

    print(f"{label}:")
    print(f"  A = {A_fit:.3e}")
    print(f"  b = {b_fit:.4f} ± {b_err:.4f}\n")

    # --- data (same color) ---
    plt.errorbar(
        T_K, U,
        xerr=errT, yerr=errU,
        fmt='x',
        capsize=3,
        color=color,
        label=f"{label} data"
    )

    # --- fit (same color) ---
    T_fit = np.linspace(min(T_K), max(T_K), 300)
    plt.plot(
        T_fit,
        model(T_fit, *popt),
        color=color,
        label=(
            f"{label} fit:\n"
            f"$b = {b_fit:.3f} \\pm {b_err:.3f}$"
    )   )

# --- styling ---
plt.xlabel("temperature T [K]")
plt.ylabel("U [mV]")
plt.title("U(T) - dependency and individual fits: U = A(T^b - T0^b)")
plt.legend()
plt.grid(False)

plt.gca().xaxis.set_minor_locator(AutoMinorLocator(4))
plt.gca().yaxis.set_minor_locator(AutoMinorLocator(4))

plt.tick_params(axis='both', which='major', direction='in', top=True, right=True)
plt.tick_params(axis='both', which='minor', direction='in', top=True, right=True)

plt.tight_layout()
plt.savefig(img_path / "individual_fits_U(T).png")
plt.show()

# --- summary output ---
print("Summary of exponents:")
for i, b in enumerate(b_values, start=1):
    print(f"b{i} = {b:.4f}")