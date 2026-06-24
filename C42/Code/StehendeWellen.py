import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 2.4 Bestimmung der Wellenlänge mit stehenden Wellen
# ============================================================

# Knotennummern
i = np.array([
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31
])

# Knotenpositionen in cm
x = np.array([
    55.15, 56.80, 58.30, 59.95, 61.60,
    63.35, 64.95, 66.60, 68.25, 69.75,
    71.45, 73.00, 74.65, 76.35, 77.90,
    79.50, 81.10, 82.75, 84.40, 86.00,
    87.60, 89.20, 90.80, 92.40, 93.95,
    95.60, 97.20, 98.95, 100.60, 102.30,
    104.00
])

# Fehler jeder Positionsmessung
dx_pos = 0.1  # cm

# ============================================================
# Knotenabstände
# ============================================================

dx = np.diff(x)

# Fehler jedes Abstandes
d_dx = np.sqrt(dx_pos**2 + dx_pos**2)

# Mittelwert
dx_mean = np.mean(dx)

# Fehler des Mittelwerts
d_dx_mean = d_dx / np.sqrt(len(dx))

# Wellenlänge
lam = 2 * dx_mean

# Fehler der Wellenlänge
dlam = 2 * d_dx_mean

print("2.4 Stehende Welle")
print(f"Mittelwert Δx = ({dx_mean:.4f} ± {d_dx_mean:.4f}) cm")
print(f"Wellenlänge λ = ({lam:.4f} ± {dlam:.4f}) cm")

# ============================================================
# Plot 1: Knotenpositionen
# ============================================================

plt.figure(figsize=(7,4))

plt.errorbar(
    i,
    x,
    yerr=dx_pos,
    fmt='o',
    capsize=3,
    label='Messwerte'
)

plt.plot(i, x)

plt.xlabel("Knotennummer")
plt.ylabel("Position x / cm")

plt.tick_params(
    direction="in",
    top=True,
    right=True,
    which="both"
)

plt.minorticks_on()

plt.legend()
plt.tight_layout()


plt.show()

# ============================================================
# Plot 2: Knotenabstände
# ============================================================

plt.figure(figsize=(7,4))

plt.errorbar(
    np.arange(1, len(dx)+1),
    dx,
    yerr=d_dx,
    fmt='o',
    capsize=3,
    label='Knotenabstände'
)

plt.axhline(
    dx_mean,
    linestyle="--",
    label=fr"$\overline{{\Delta x}} = {dx_mean:.3f}$ cm"
)

plt.xlabel("Intervallnummer")
plt.ylabel(r"$\Delta x$ / cm")

plt.tick_params(
    direction="in",
    top=True,
    right=True,
    which="both"
)

plt.minorticks_on()

plt.legend()
plt.tight_layout()

plt.show()