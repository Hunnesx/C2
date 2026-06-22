from matplotlib import ticker
import numpy as np
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

# ------------------------------------------------------------------
# Daten einlesen
# ------------------------------------------------------------------
base_path = Path.cwd()
data_path = base_path / 'C42' / 'Data' / '42_Messwerte.xlsx'
img_path = base_path.parent / 'C2-Praktikum' / 'C42' / 'Images'
Data = pd.read_excel(data_path, sheet_name='2.2 Winkelverteilung', engine='openpyxl')
WinkelStromstaerke = np.array(
    [[x, y] for x, y in zip(Data['Winkel /°'], Data['I/mA'])]
)
winkel = WinkelStromstaerke[:, 0]
I = WinkelStromstaerke[:, 1]

# ------------------------------------------------------------------
# NaNs entfernen und nach Winkel sortieren
# ------------------------------------------------------------------
mask = ~np.isnan(winkel) & ~np.isnan(I)
winkel = winkel[mask]
I = I[mask]
sort_idx = np.argsort(winkel)
winkel = winkel[sort_idx]
I = I[sort_idx]

# ------------------------------------------------------------------
# Normierung
# ------------------------------------------------------------------
I_abs = np.abs(I)
I_max = np.max(I_abs)
I_norm = I_abs / I_max
I_half = 0.5

# ------------------------------------------------------------------
# Halbwertswinkel bestimmen
# ------------------------------------------------------------------
max_index = np.argmax(I_norm)

left_idx = np.where(I_norm[:max_index] <= I_half)[0]
if len(left_idx) > 0:
    i1 = left_idx[-1]
    i2 = i1 + 1
    theta_left = np.interp(I_half, [I_norm[i1], I_norm[i2]], [winkel[i1], winkel[i2]])
else:
    theta_left = np.nan

right_idx = np.where(I_norm[max_index:] <= I_half)[0]
if len(right_idx) > 0:
    i2 = max_index + right_idx[0]
    i1 = i2 - 1
    theta_right = np.interp(I_half, [I_norm[i2], I_norm[i1]], [winkel[i2], winkel[i1]])
else:
    theta_right = np.nan

halbwertswinkel = theta_right - theta_left

print(f"Linker Halbwertspunkt: {theta_left:.2f}°")
print(f"Rechter Halbwertspunkt: {theta_right:.2f}°")
print(f"Halbwertswinkel: {halbwertswinkel:.2f}°")

# ==================================================================
# >>> HIER DEN NEUEN FEHLERRECHNUNGS-BLOCK EINFÜGEN <
# ==================================================================
sigma_theta = 2
sigma_I = 0.01
sigma_I_norm = sigma_I / I_max

def f_interp(I1, I2, theta1, theta2, I_half):
    return theta1 + (I_half - I1) * (theta2 - theta1) / (I2 - I1)

def interp_with_error(i1, i2, I_half, sigma_theta, sigma_I_norm):
    I1, I2 = I_norm[i1], I_norm[i2]
    theta1, theta2 = winkel[i1], winkel[i2]
    theta_val = f_interp(I1, I2, theta1, theta2, I_half)
    eps = 1e-6
    dtheta_dI1 = (f_interp(I1 + eps, I2, theta1, theta2, I_half)
                  - f_interp(I1 - eps, I2, theta1, theta2, I_half)) / (2 * eps)
    dtheta_dI2 = (f_interp(I1, I2 + eps, theta1, theta2, I_half)
                  - f_interp(I1, I2 - eps, theta1, theta2, I_half)) / (2 * eps)
    dtheta_dtheta1 = (f_interp(I1, I2, theta1 + eps, theta2, I_half)
                      - f_interp(I1, I2, theta1 - eps, theta2, I_half)) / (2 * eps)
    dtheta_dtheta2 = (f_interp(I1, I2, theta1, theta2 + eps, I_half)
                      - f_interp(I1, I2, theta1, theta2 - eps, I_half)) / (2 * eps)
    sigma_val = np.sqrt(
        (dtheta_dI1 * sigma_I_norm) ** 2 +
        (dtheta_dI2 * sigma_I_norm) ** 2 +
        (dtheta_dtheta1 * sigma_theta) ** 2 +
        (dtheta_dtheta2 * sigma_theta) ** 2
    )
    return theta_val, sigma_val

theta_left, sigma_theta_left = interp_with_error(
    left_idx[-1], left_idx[-1] + 1, I_half, sigma_theta, sigma_I_norm
)

i2_r = max_index + right_idx[0]
i1_r = i2_r - 1
theta_right, sigma_theta_right = interp_with_error(
    i2_r, i1_r, I_half, sigma_theta, sigma_I_norm
)

halbwertswinkel = theta_right - theta_left
sigma_halbwertswinkel = np.sqrt(sigma_theta_left**2 + sigma_theta_right**2)

print(f"Linker Halbwertspunkt:  ({theta_left:.2f} ± {sigma_theta_left:.2f})°")
print(f"Rechter Halbwertspunkt: ({theta_right:.2f} ± {sigma_theta_right:.2f})°")
print(f"Halbwertswinkel:        ({halbwertswinkel:.2f} ± {sigma_halbwertswinkel:.2f})°")
# ==================================================================
# >>> ENDE DES NEUEN BLOCKS <
# ==================================================================

# ------------------------------------------------------------------
# Polardiagramm
# ------------------------------------------------------------------
winkel_rad = np.deg2rad(winkel)
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
ax.plot(winkel_rad, I_norm, 'x-', label='Angular distribution of radiation characteristics')
ax.fill(winkel_rad, I_norm, alpha=0.2)
ax.plot(np.linspace(0, 2*np.pi, 200), np.ones(200) * I_half, '--', label='Halfvalues (0.5)')

ax.errorbar(np.deg2rad(theta_left), I_half,
            xerr=np.deg2rad(sigma_theta_left), fmt='ro', capsize=3)
ax.errorbar(np.deg2rad(theta_right), I_half,
            xerr=np.deg2rad(sigma_theta_right), fmt='ro', capsize=3)

ax.set_theta_zero_location('E')
ax.set_theta_direction(-1)
ax.set_thetamin(-30)
ax.set_thetamax(30)
ax.set_thetagrids(np.arange(-30, 30, 10))
ax.set_rgrids(np.arange(0, 1.1, 0.1))
ax.set_rlabel_position(135)
ax.legend(loc='lower right')
plt.tight_layout()
plt.savefig(img_path / 'Winkelverteilung_Polar.pdf', bbox_inches='tight')
plt.show()