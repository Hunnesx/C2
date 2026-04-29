import numpy as np
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from scipy.optimize import curve_fit

# --- paths ---
base_path = Path.cwd()
data_path = base_path / 'C33' / 'Data' / 'Versuch_33.xlsx'
img_path = base_path.parent / 'C2-Praktikum' / 'C33' / 'Images'

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
# --- colors (same mapping as before) ---
colors = ["black", "tab:red", "tab:blue", "tab:green"]

T0_K = 20 + 273.15


# --- linear model for U(T^4) ---
def linear_model(T4, a, c):
    return a * T4 + c

plt.figure(figsize=(8, 6))

for (data, label), color in zip(datasets, colors):
    U = data[:, 0]
    T_K = data[:, 1] + 273.15
    T4 = T_K**4 - T0_K**4

    errT = 0.1
    errU = 0.00025 * U + 0.00008 * 100

    # --- fit ---
    popt, _ = curve_fit(linear_model, T4, U)
    a_fit, c_fit = popt

    print(f"{label}: a = {a_fit:.3e}, c = {c_fit:.3e}")

    # --- data ---
    plt.errorbar(
        T4, U,
        xerr=4 * T_K**3 * errT,
        yerr=errU,
        fmt='x',
        capsize=3,
        color=color,
        label=f"{label} data"
    )

    # --- fit line ---
    T4_fit = np.linspace(min(T4), max(T4), 300)
    plt.plot(
        T4_fit,
        linear_model(T4_fit, *popt),
        color=color,
        label=f"{label} fit (linear in $T^4$)"
    )

# --- styling ---
plt.xlabel(r"$temperature \, T^4 - T_0^4 \, [K^4]$")
plt.ylabel("U [mV]")
plt.title("U(T^4) - dependency (Stefan Boltzmann Law) with linear fits")

plt.legend()
plt.grid(False)

plt.gca().xaxis.set_minor_locator(AutoMinorLocator(4))
plt.gca().yaxis.set_minor_locator(AutoMinorLocator(4))

plt.tick_params(axis='both', which='major', direction='in', top=True, right=True)
plt.tick_params(axis='both', which='minor', direction='in', top=True, right=True)

plt.tight_layout()
plt.savefig(img_path / "individual_fits_U(T4).png")
plt.show()