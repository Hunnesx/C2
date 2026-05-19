import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd


# =========================
# Eingaben
# =========================

# Schallgeschwindigkeit in Polyacryl, z.B. in mm/us
c = 2.619   # mm/µs

# Fehler der Schallgeschwindigkeit, falls bekannt
c_err = 0.032   # mm/µs

# gemessene Zeitdifferenzen zwischen Sendeimpuls und Echo in µs
# Beispielwerte ersetzen!
delta_t = np.array([
    5.825242718,   # Bohrung 1
    11.6058394161,   # Bohrung 2
    17.5735294118,   # Bohrung 3
    23.3576642336,   # Bohrung 4
    29.4890510949,   # Bohrung 5
    35.1824817518,   # Bohrung 6
    40.5109489051,   # Bohrung 7
    46.0583941606,   # Bohrung 8
    14.5669291339,   # Bohrung 9.1
    15.905511811,   # Bohrung 9.2       
    41.5048543689,   # Bohrung 10 
])

# Fehler der Zeitmessung in µs
delta_t_err = 0.1

# Namen der Messpunkte
namen = [
    "Bohrung 1",
    "Bohrung 2",
    "Bohrung 3",
    "Bohrung 4",
    "Bohrung 5",
    "Bohrung 6",
    "Bohrung 7",
    "Bohrung 8",
    "Bohrung 9.1",
    "Bohrung 9.2",
    "Bohrung 10",
]


# =========================
# Berechnung
# =========================

# Reflexionsmessung: Schall läuft hin und zurück
# Tiefe = c * delta_t / 2
tiefe = c * delta_t / 2

# Fehlerfortpflanzung
# tiefe_err = 0.5 * np.sqrt(
#     (delta_t * c_err) ** 2 +
#     (c * delta_t_err) ** 2
# )
tiefe_err =  tiefe * np.sqrt(
    (delta_t_err/delta_t) ** 2 +
    (c_err/c) ** 2
)


# =========================
# Ausgabe als Tabelle
# =========================

df = pd.DataFrame({
    "Messpunkt": namen,
    "delta_t [µs]": delta_t,
    "Tiefe t_i [mm]": tiefe,
    "Fehler Tiefe [mm]": tiefe_err
})

print(df.to_string(index=False))


# =========================
# Gesamtmaß des Blocks
# =========================

delta_t_ges = 55.0      # µs, Beispielwert ersetzen
delta_t_ges_err = 0.1   # µs

t_ges = c * delta_t_ges / 2

t_ges_err = 0.5 * np.sqrt(
    (delta_t_ges * c_err) ** 2 +
    (c * delta_t_ges_err) ** 2
)

print()
# print(f"Gesamtdicke des Blocks: {t_ges:.2f} ± {t_ges_err:.2f} mm")