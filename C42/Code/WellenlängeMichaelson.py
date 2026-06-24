import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 2.5 Bestimmung der Wellenlänge mit dem Michelson-Interferometer
# ============================================================

# Nummern der Maxima
i = np.array([
    1, 2, 3, 4, 5, 6, 7, 8, 9
])

# Positionen der Maxima in cm
x = np.array([
    0.50, 2.20, 3.80, 5.30, 7.10,
    8.60, 10.20, 12.00, 13.70
])

# Fehler jeder Längenmessung
dx_pos = 0.1  # cm

# ============================================================
# Abstände benachbarter Maxima
# ============================================================

dx = np.diff(x)

# Fehler eines Abstandes
d_dx = np.sqrt(dx_pos**2 + dx_pos**2)

# Mittelwert der Maxima-Abstände
dx_mean = np.mean(dx)

# Fehler des Mittelwerts
d_dx_mean = d_dx / np.sqrt(len(dx))

# Beim Michelson-Interferometer gilt:
# lambda = 2 * mittlerer Abstand der Maxima
lam = 2 * dx_mean

# Fehler der Wellenlänge
dlam = 2 * d_dx_mean

print("2.5 Michelson-Interferometer")
print(f"Mittelwert Δx = ({dx_mean:.4f} ± {d_dx_mean:.4f}) cm")
print(f"Wellenlänge λ = ({lam:.4f} ± {dlam:.4f}) cm")

# ============================================================
# Plot 1: Maximapositionen
# ============================================================

plt.figure(figsize=(7,4))

plt.errorbar(
    i,
    x,
    yerr=dx_pos,
    fmt="o",
    capsize=3,
    label="Messwerte"
)

plt.plot(i, x)

plt.xlabel("Maximum")
plt.ylabel("Spiegelposition x / cm")

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
# Plot 2: Abstände der Maxima
# ============================================================

plt.figure(figsize=(7,4))

plt.errorbar(
    np.arange(1, len(dx)+1),
    dx,
    yerr=d_dx,
    fmt="o",
    capsize=3,
    label="Maxima-Abstände"
)

plt.axhline(
    dx_mean,
    linestyle="--",
    label=fr"$\overline{{\Delta x}} = {dx_mean:.3f}$ cm"
)

plt.xlabel("Intervallnummer")
plt.ylabel(r"Abstand $\Delta x$ / cm")

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