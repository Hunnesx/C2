import pandas as pd
import numpy as np
from pathlib import Path

# ==========================
# Pfade
# ==========================
base_path = Path.cwd()
data_path = base_path / 'C40' / 'Data' / '40_Messdaten.xlsx'

# ==========================
# Excel-Datei einlesen
# ==========================
Data = pd.read_excel(
    data_path,
    sheet_name='2.4 Halbschattenwinkel',
    engine='openpyxl'
)

Psi_L = pd.to_numeric(
    Data["heller Punkt (rechts oben)"],
    errors="coerce"
).dropna()

Psi_R = pd.to_numeric(
    Data["anders"],
    errors="coerce"
).dropna()

# ==========================
# Halbschattenwinkel berechnen
# ==========================
# Each pair gives one half-shadow angle
Psi_values = np.abs(Psi_L.values - Psi_R.values)

# Mean and standard deviation
Psi_mean = np.mean(Psi_values)
Psi_std  = np.std(Psi_values, ddof=1)          # sample std (N-1)
Psi_sem  = Psi_std / np.sqrt(len(Psi_values)-1)  # std of the mean

# ==========================
# Ausgabe
# ==========================
print("Individual half-shadow angles Ψ:")
for i, psi in enumerate(Psi_values, 1):
    print(f"  Measurement {i}: Ψ = {psi:.3f}°")

print(f"\nNumber of measurements : n  = {len(Psi_values)}")
print(f"Mean half-shadow angle : Ψ  = {Psi_mean:.3f}°")
print(f"Standard deviation     : σΨ = {Psi_std:.3f}°")
print(f"Std of the mean        : σΨ̄ = {Psi_sem:.3f}°")