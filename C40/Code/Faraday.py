import numpy as np
import matplotlib.pyplot as plt

# Messwerte
x_mm = np.array([
    0, 2, 4, 6, 8, 10, 12, 14, 16,
    18, 20, 22, 24, 26, 28, 30, 32, 34
])

B_mT = np.array([
    -5.7, -9.2, -18.4, -35.7, -60.4,
    -79.7, -90.9, -95.0, -96.0,
    -96.1, -96.0, -95.1, -90.7,
    -77.4, -52.7, -30.4, -15.1, -7.2
])

# ---------------------------------------------------
# Effektives Magnetfeld durch Integration bestimmen
# ---------------------------------------------------

# Länge des Glaskörpers in mm
l_mm = 30

# Numerische Integration mit Trapezregel
integral = np.trapz(B_mT, x_mm)

# Effektives Feld
B_eff = integral / l_mm

# Maximales Feld
B_max = np.min(B_mT)

# Faktor alpha
alpha = B_eff / B_max

print("Integral ∫B(x)dx =", integral, "mT·mm")
print("Effektives Feld B_eff =", B_eff, "mT")
print("Maximales Feld B_max =", B_max, "mT")
print("alpha =", alpha)

# ---------------------------------------------------
# Plot
# ---------------------------------------------------

plt.figure(figsize=(8,5))

plt.plot(
    x_mm,
    B_mT,
    'o-',
    label='Messwerte'
)

# horizontale Linie für B_eff
plt.axhline(
    B_eff,
    color='red',
    linestyle='--',
    label=fr'$B_{{eff}}={B_eff:.2f}\,$ mT'
)

plt.xlabel('x / mm')
plt.ylabel('B(x) / mT')

plt.title('Magnetische Flussdichte entlang des Glaskörpers')

plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()