import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd

#1MHz
# c = 2.619   # mm/µs
# c_err = 0.032   # mm/µs
# delta_t = 0.769230 

#2MHz
c = 2.667
c_err = 0.033   # mm/µs
delta_t = 1.2727272727

# #4MHz
# c = 2.746
# c_err = 0.052   # mm/µs
# delta_t = 1.27692307 

# gemessene Zeitdifferenzen zwischen Sendeimpuls und Echo in µs
# Beispielwerte ersetzen!
# delta_t = np.array([
#     14.5669291339,   # Bohrung 9.1
#     15.905511811,   # Bohrung 9.2       
# ])

# Fehler der Zeitmessung in µs
delta_t_err = 0.1

# Namen der Messpunkte
namen = "Differenz"

# Reflexionsmessung: Schall läuft hin und zurück
# Tiefe = c * delta_t / 2
tiefe = c * delta_t / 2

# # Fehlerfortpflanzung
# tiefe_err = 0.5 * np.sqrt(
#     (delta_t * c_err) ** 2 +
#     (c * delta_t_err) ** 2
# )

tiefe_err =  tiefe * np.sqrt((delta_t_err/delta_t) ** 2 + (c_err/c) ** 2)


# =========================
# Ausgabe als Tabelle
# =========================


print(f"Messpunkt: {namen}")
print(f"delta_t [µs]: {delta_t}")
print(f"Tiefe t_i [mm]: {tiefe}")
print(f"Fehler Tiefe [mm]: {tiefe_err}")


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

