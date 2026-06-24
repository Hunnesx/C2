import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ============================================================
# 2.6 Totalreflexion und Tunneleffekt
# ============================================================

# Abstand der beiden Paraffinprismen in cm
d = np.array([
    15.35, 15.00, 14.50, 14.00, 13.50,
    13.00, 12.50, 12.00, 11.50
])

# Transmission Stellung A in mA
I_A = np.array([
    0.295, 0.261, 0.211, 0.136, 0.100,
    0.086, 0.076, 0.072, 0.073
])

# Reflexion Stellung B in mA
I_B = np.array([
    0.180, 0.195, 0.198, 0.200, 0.202,
    0.203, 0.206, 0.208, 0.198
])

# Fehler
dd = 0.1       # cm
dI_A = 0.001   # mA
dI_B = 0.001   # mA

# ============================================================
# Exponentieller Fit für Transmission
# ============================================================

def expo(x, I0, delta):
    return I0 * np.exp(-x / delta)

popt, pcov = curve_fit(
    expo,
    d,
    I_A,
    sigma=np.full_like(I_A, dI_A),
    absolute_sigma=True,
    maxfev=10000
)

I0, delta = popt
dI0, ddelta = np.sqrt(np.diag(pcov))

print("2.6 Totalreflexion und Tunneleffekt")
print(f"I0 = ({I0:.4f} ± {dI0:.4f}) mA")
print(f"delta = ({delta:.4f} ± {ddelta:.4f}) cm")

# Werte für Fitkurve
d_fit = np.linspace(min(d), max(d), 500)
I_fit = expo(d_fit, I0, delta)

# ============================================================
# Plot 1: Transmission halblogarithmisch
# ============================================================

plt.figure(figsize=(7,4))

plt.errorbar(
    d,
    I_A,
    xerr=dd,
    yerr=dI_A,
    fmt="o",
    capsize=3,
    label="Transmission"
)

plt.semilogy(
    d_fit,
    I_fit,
    "-",
    label="exponentieller Fit"
)

plt.yscale("log")

plt.xlabel("Abstand d / cm")
plt.ylabel("Transmittierte Intensität / mA")

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
# Plot 2: Reflexion linear
# ============================================================

plt.figure(figsize=(7,4))

plt.errorbar(
    d,
    I_B,
    xerr=dd,
    yerr=dI_B,
    fmt="o",
    capsize=3,
    label="Reflexion"
)

plt.plot(d, I_B)

plt.xlabel("Abstand d / cm")
plt.ylabel("Reflektierte Intensität / mA")

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
# Plot 3: Transmission und Reflexion zusammen linear
# ============================================================

plt.figure(figsize=(7,4))

plt.errorbar(
    d,
    I_A,
    xerr=dd,
    yerr=dI_A,
    fmt="o",
    capsize=3,
    label="Transmission"
)

plt.errorbar(
    d,
    I_B,
    xerr=dd,
    yerr=dI_B,
    fmt="s",
    capsize=3,
    label="Reflexion"
)

plt.xlabel("Abstand d / cm")
plt.ylabel("Intensität / mA")

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