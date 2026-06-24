from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
from scipy.signal import find_peaks

# -----------------------------------------------------------
# Daten einlesen
# -----------------------------------------------------------
base_path = Path.cwd()
data_path = base_path / "C42" / "Data" / "42_Messwerte.xlsx"
img_path = base_path.parent / 'C2-Praktikum' / 'C42' / 'Images'

# Ordner erstellen, falls er noch nicht existiert
img_path.mkdir(parents=True, exist_ok=True)

Data = pd.read_excel(
    data_path,
    sheet_name="2.8 Gitterkonstante",
    engine="openpyxl"
)

# Daten für 100 säubern und extrahieren
Data100 = Data[['Winkel teta /°', 'I (100)/mA']].dropna()
theta100 = Data100['Winkel teta /°'].to_numpy()
I100 = Data100['I (100)/mA'].to_numpy()

# Daten für 110 säubern und extrahieren
Data110 = Data[['Winkel teta /°', 'I (110)/mA']].dropna()
theta110 = Data110['Winkel teta /°'].to_numpy()
I110 = Data110['I (110)/mA'].to_numpy()

#------------------------------------------------------------
# Fehlerdefinition
#------------------------------------------------------------
errThe = 1       # Fehler des Winkels Theta
errInt = 0.01    # Fehler der Intensität I

# -----------------------------------------------------------
# Spline-Interpolation für glatte Kurven
# -----------------------------------------------------------
theta_fine = np.linspace(theta100.min(), theta100.max(), 1000)

cs100 = CubicSpline(theta100, I100)
cs110 = CubicSpline(theta110, I110)

I100_smooth = cs100(theta_fine)
I110_smooth = cs110(theta_fine)

# -----------------------------------------------------------
# Peaks finden
# -----------------------------------------------------------
peaks100, _ = find_peaks(I100_smooth, prominence=0.05)
peaks110, _ = find_peaks(I110_smooth, prominence=0.05)

# -----------------------------------------------------------
# Plot 100
# -----------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))

# Messpunkte mit Fehlerbalken
ax.errorbar(theta100, I100, xerr=errThe, yerr=errInt, fmt='x', 
            capsize=4, color='black', label='Data (100)')

# Geglättete Kurve
ax.plot(theta_fine, I100_smooth, '-', lw=2, label='Spline (100)', color='red')

# NUR das zweite Maximum auswählen (Index 1)
if len(peaks100) >= 2:
    idx_100 = peaks100[1]
    peak_x_100 = theta_fine[idx_100]
    peak_y_100 = I100_smooth[idx_100]
    
    # Vertikale Linie durch das Maximum ziehen
    ax.vlines(x=peak_x_100, ymin=0, ymax=4, color='royalblue', 
              linestyle='--', lw=1.5, label='Peak position')

    # Zweites Maximum markieren
    ax.plot(peak_x_100, peak_y_100, 'x', ms=10, mew=2,
            label='Main maximum (100)', color='royalblue')

    # Nur das zweite Maximum beschriften
    ax.annotate(f'{peak_x_100:.1f}°',
                (peak_x_100, peak_y_100),
                textcoords="offset points",
                xytext=(0, 8),
                ha='center')
else:
    print("Warnung: Es wurden nicht genügend Peaks gefunden, um das zweite Maximum anzuzeigen.")

# Formatierung Plot 100
ax.set_xlabel(r'Angle of incidence $\theta$ / °')
ax.set_ylabel('Intensity I / mA')
ax.set_xlim(theta100.min(), theta100.max())
ax.set_ylim(0, 0.33)
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.legend()

plt.tick_params(axis='both', which='minor', direction='in', right=True, top=True)
plt.tick_params(axis='both', which='major', direction='in', right=True, top=True, length=5)

plt.tight_layout()
plt.savefig(img_path / 'Gitterkonstante100.png', bbox_inches='tight')
plt.show()

# -----------------------------------------------------------
# Plot 110
# -----------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))

# Messpunkte mit Fehlerbalken für 110
ax.errorbar(theta110, I110, xerr=errThe, yerr=errInt, fmt='x', 
            capsize=3, color='black', label='Data (110)')

# Geglättete Kurve
ax.plot(theta_fine, I110_smooth, '-', lw=2, label='Spline (110)', color='red')

# Erstes/Haupt-Maximum auswählen und verarbeiten (Index 0)
if len(peaks110) >= 1:
    idx_110 = peaks110[0]
    peak_x_110 = theta_fine[idx_110]
    peak_y_110 = I110_smooth[idx_110]
    
    # Vertikale Linie durch das Maximum ziehen
    ax.vlines(x=peak_x_110, ymin=0, ymax=4, color='royalblue', 
              linestyle='--', lw=1.5, label='Peak position')

    # Peaks markieren
    ax.plot(peak_x_110, peak_y_110, 'x', ms=10, mew=2,
            label='Maximum (110)', color='royalblue')

    # Peak-Winkel beschriften
    ax.annotate(f'{peak_x_110:.1f}°',
                (peak_x_110, peak_y_110),
                textcoords="offset points",
                xytext=(0, 8),
                ha='center')
else:
    print("Warnung: Es wurden keine Peaks für Plot 110 gefunden.")
    
# Formatierung Plot 110
ax.set_xlabel(r'Angle of incidence $\theta$ / °')
ax.set_ylabel('Intensity I / mA')
ax.set_xlim(theta110.min(), theta110.max())
ax.set_ylim(0, 0.33)
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.legend()

plt.tick_params(axis='both', which='minor', direction='in', right=True, top=True)
plt.tick_params(axis='both', which='major', direction='in', right=True, top=True, length=5)

plt.tight_layout()
plt.savefig(img_path / 'Gitterkonstante110.png', bbox_inches='tight')
plt.show()

#--------------------------------------
# Berechnung von der Gitterkonstante (Relative Fehlerfortpflanzung)
#--------------------------------------

# Wellenlänge
wavelength = 3.262  # cm
n = 1
errWave = 0.013      # cm Unsicherheit der Wellenlänge

# 100-Seite
if len(peaks100) >= 2:
    theta_peak_100 = theta_fine[peaks100[1]]
    d100 = n * wavelength / (2 * np.sin(np.deg2rad(theta_peak_100)))
    
    # 1. Relativer Fehler der Wellenlänge (Spezialfall für Quotienten)
    rel_err_wave = errWave / wavelength
    
    # 2. Relativer Fehler des Winkels (über die Ableitung des Sinus)
    # cot(theta) = cos(theta) / sin(theta)
    cot_theta_100 = np.cos(np.deg2rad(theta_peak_100)) / np.sin(np.deg2rad(theta_peak_100))
    rel_err_theta_100 = cot_theta_100 * np.deg2rad(errThe)
    
    # 3. Geometrische Addition der relativen Fehlerquadrate (Spezialfall 3)
    rel_err_d100 = np.sqrt(rel_err_wave**2 + rel_err_theta_100**2)
    
    # Absoluten Fehler berechnen: Delta d = d * (Delta d / d)
    err_d100 = d100 * rel_err_d100
    
    print(f"Gitterkonstante d100 = ({d100:.4f} ± {err_d100:.4f}) cm bei theta = {theta_peak_100:.2f}°")
else:
    print("Warnung: Nicht genügend Peaks gefunden, um die Gitterkonstante für 100 zu berechnen.")

# 110-Seite
if len(peaks110) >= 1:
    theta_peak_110 = theta_fine[peaks110[0]]
    d110 = n * wavelength / (2 * np.sin(np.deg2rad(theta_peak_110))) * np.sqrt(2)
    
    # 1. Relativer Fehler der Wellenlänge
    rel_err_wave = errWave / wavelength
    
    # 2. Relativer Fehler des Winkels
    cot_theta_110 = np.cos(np.deg2rad(theta_peak_110)) / np.sin(np.deg2rad(theta_peak_110))
    rel_err_theta_110 = cot_theta_110 * np.deg2rad(errThe)
    
    # 3. Geometrische Addition der relativen Fehlerquadrate
    rel_err_d110 = np.sqrt(rel_err_wave**2 + rel_err_theta_110**2)
    
    # Absoluten Fehler berechnen
    err_d110 = d110 * rel_err_d110
    
    print(f"Gitterkonstante d110 = ({d110:.4f} ± {err_d110:.4f}) cm bei theta = {theta_peak_110:.2f}°")
else:
    print("Warnung: Nicht genügend Peaks gefunden, um die Gitterkonstante für 110 zu berechnen.")