import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ==================================================
# Fehler
# ==================================================

dB_mT = 0.1
dI_A = 0.005
dtheta_deg = 0.05
dx_mm = 0.5

l_glass_mm = 30
dl_glass_mm = 0.5

l_glass_m = l_glass_mm / 1000
dl_glass_m = dl_glass_mm / 1000


# ==================================================
# Hilfsfunktionen
# ==================================================

def linear(x, a, b):
    return a * x + b


def fit_linear(x, y, yerr):
    popt, pcov = curve_fit(
        linear,
        x,
        y,
        sigma=yerr,
        absolute_sigma=True
    )
    a, b = popt
    da, db = np.sqrt(np.diag(pcov))
    return a, b, da, db


# ==================================================
# 1. Magnetfeldprofil B(x)
# ==================================================

x_mm = np.array([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34])

B_x_mT = np.array([
    -5.7, -9.2, -18.4, -35.7, -60.4, -79.7,
    -90.9, -95.0, -96.0, -96.1, -96.0, -95.1,
    -90.7, -77.4, -52.7, -30.4, -15.1, -7.2
])

xerr = np.full_like(x_mm, dx_mm, dtype=float)
Berr = np.full_like(B_x_mT, dB_mT, dtype=float)

integral_B = np.trapezoid(B_x_mT, x_mm)
B_eff_profile = integral_B / l_glass_mm
B_max_profile = np.min(B_x_mT)
alpha = B_eff_profile / B_max_profile

# grobe Unsicherheit von B_eff
d_integral_B = np.sqrt(np.sum((dB_mT * np.diff(x_mm, prepend=x_mm[0]))**2))
dB_eff_profile = abs(B_eff_profile) * np.sqrt(
    (d_integral_B / abs(integral_B))**2 + (dl_glass_mm / l_glass_mm)**2
)

dalpha = abs(alpha) * np.sqrt(
    (dB_eff_profile / abs(B_eff_profile))**2 + (dB_mT / abs(B_max_profile))**2
)

print("1. Magnetfeldprofil")
print(f"Integral ∫B(x) dx = {integral_B:.3f} mT mm")
print(f"B_eff = ({B_eff_profile:.3f} ± {dB_eff_profile:.3f}) mT")
print(f"B_max = ({B_max_profile:.3f} ± {dB_mT:.3f}) mT")
print(f"alpha = {alpha:.5f} ± {dalpha:.5f}")

plt.figure(figsize=(8, 5))
plt.errorbar(
    x_mm, B_x_mT,
    xerr=xerr,
    yerr=Berr,
    fmt="x",
    capsize=3,
    label="Messwerte"
)
plt.plot(x_mm, B_x_mT, "-", alpha=0.7)
plt.axhline(B_eff_profile, linestyle="--", label=f"B_eff = {B_eff_profile:.2f} mT")
plt.xlabel("x / mm")
plt.ylabel("B(x) / mT")
plt.title("Magnetfeldprofil B(x)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# ==================================================
# 2. Kalibrierung B_eff(I)
# ==================================================

I_cal = np.array([
    -0.495, -0.804, -1.103, -1.398, -1.702, -2.016,
    -2.303, -2.604, -2.907,
     0.509,  0.808,  1.097,  1.407,  1.705,  2.013,
     2.306,  2.606,  2.899
])

B_eff_cal_mT = np.array([
    -23.71, -38.00, -52.06, -65.77, -77.66,
    -94.19, -106.88, -120.37, -133.06,
     22.84,  37.27,  50.98,  65.41,  79.25,
     94.26, 106.88, 120.44, 132.55
])

Ierr_cal = np.full_like(I_cal, dI_A, dtype=float)
Berr_cal = np.full_like(B_eff_cal_mT, dB_mT, dtype=float)

a_B, b_B, da_B, db_B = fit_linear(I_cal, B_eff_cal_mT, Berr_cal)

I_fit = np.linspace(min(I_cal), max(I_cal), 300)
B_fit = linear(I_fit, a_B, b_B)

print("\n2. Kalibrierung B_eff(I)")
print(f"B_eff(I) = ({a_B:.3f} ± {da_B:.3f}) mT/A * I + ({b_B:.3f} ± {db_B:.3f}) mT")

plt.figure(figsize=(8, 5))
plt.errorbar(
    I_cal, B_eff_cal_mT,
    xerr=Ierr_cal,
    yerr=Berr_cal,
    fmt="x",
    capsize=3,
    label="data"
)
plt.plot(I_fit, B_fit, "-", label=f"Fit: B_eff = {a_B:.3f} I {b_B:+.3f}")
plt.xlabel("I [A]")
plt.ylabel("B_eff [mT]")
plt.tick_params(
    axis='both',      # x- und y-Achse
    which='both',     # major + minor ticks
    direction='in',   # nach innen
    top=True,
    right=True
)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# ==================================================
# 3. Faraday-Daten
# ==================================================

I_400_560 = np.array([
     0.507,  0.803,  1.108,  1.398,  1.703,  2.007,
     2.302,  2.603,  2.918,
    -0.497, -0.795, -1.111, -1.406, -1.700, -2.007,
    -2.306, -2.601, -2.894
])

theta_400_560 = np.array([
     0.5, 1.0, 1.5, 2.0, 2.5, 3.0,
     3.5, 4.0, 4.5,
    -0.5, -1.0, -1.5, -2.0, -2.5, -3.0,
    -3.5, -4.0, -4.5
])

I_360_460 = np.array([
    -0.514, -0.810, -1.091, -1.413, -1.714, -2.012,
    -2.312, -2.608, -2.884,
     0.496,  0.808,  1.110,  1.410,  1.723,  2.014,
     2.314,  2.613,  2.871
])

theta_360_460 = np.array([
     0.0, -1.0, -1.5, -2.0, -2.5, -3.0,
    -5.0, -6.5, -7.5,
     0.5,  1.0,  1.5,  2.0,  2.5,  3.0,
     3.5,  4.5,  5.5
])

I_560_630 = np.array([
     0.495,  0.825,  1.106,  1.410,  1.710,  2.009,
     2.312,  2.621,  2.888,
    -0.497, -0.815, -1.104, -1.415, -1.730, -2.011,
    -2.326, -2.591, -2.926
])

theta_560_630 = np.array([
     0.5, 1.0, 1.5, 2.0, 2.0, 2.5,
     2.5, 3.0, 3.0,
    -0.5, -0.5, -1.0, -1.5, -2.0, -2.0,
    -2.5, -2.5, -3.0
])


def faraday_auswertung(I, theta_deg, name):
    B_eff = linear(I, a_B, b_B)

    dB_eff = np.sqrt((I * da_B)**2 + db_B**2 + (a_B * dI_A)**2)

    theta_err = np.full_like(theta_deg, dtheta_deg, dtype=float)

    m, c, dm, dc = fit_linear(B_eff, theta_deg, theta_err)

    B_plot = np.linspace(min(B_eff), max(B_eff), 300)
    theta_plot = linear(B_plot, m, c)

    V = m * np.pi / 180 * 1000 / l_glass_m

    dV = abs(V) * np.sqrt(
        (dm / abs(m))**2 + (dl_glass_m / l_glass_m)**2
    )

    print(f"\n3. Faraday-Auswertung {name}")
    print(f"Steigung m = ({m:.5f} ± {dm:.5f}) °/mT")
    print(f"Achsenabschnitt b = ({c:.5f} ± {dc:.5f}) °")
    print(f"Verdet-Konstante V = ({V:.2f} ± {dV:.2f}) rad/(T m)")

    plt.figure(figsize=(8, 5))
    plt.errorbar(
        B_eff, theta_deg,
        xerr=dB_eff,
        yerr=theta_err,
        fmt="x",
        capsize=3,
        label="data"
    )
    plt.plot(B_plot, theta_plot, "-", label=f"Fit")
    plt.xlabel("B_eff [mT]")
    plt.ylabel("Drehwinkel θ [°]")
    plt.tick_params(
    axis='both',      # x- und y-Achse
    which='both',     # major + minor ticks
    direction='in',   # nach innen
    top=True,
    right=True
)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return m, dm, c, dc, V, dV


m_400, dm_400, b_400, db_400, V_400, dV_400 = faraday_auswertung(
    I_400_560, theta_400_560, "400–560 nm"
)

m_360, dm_360, b_360, db_360, V_360, dV_360 = faraday_auswertung(
    I_360_460, theta_360_460, "360–460 nm"
)

m_560, dm_560, b_560, db_560, V_560, dV_560 = faraday_auswertung(
    I_560_630, theta_560_630, "560–630 nm"
)


# ==================================================
# 4. Dispersionsplot V(lambda)
# ==================================================

lambda_nm = np.array([410, 480, 595])
dlambda_nm = np.array([50, 80, 35])

V_values = np.array([V_360, V_400, V_560])
dV_values = np.array([dV_360, dV_400, dV_560])

plt.figure(figsize=(8, 5))
plt.errorbar(
    lambda_nm,
    V_values,
    xerr=dlambda_nm,
    yerr=dV_values,
    fmt="x",
    capsize=3,
    label="verdet constants"
)

plt.xlabel("wavelength λ [nm]")
plt.ylabel("verdet constan V [rad/(T m)]")

plt.grid(True)
plt.legend()
plt.tick_params(
    axis='both',      # x- und y-Achse
    which='both',     # major + minor ticks
    direction='in',   # nach innen
    top=True,
    right=True
)
plt.tight_layout()
plt.show()


# ==================================================
# 5. Zusammenfassung
# ==================================================

print("\nZusammenfassung")
print("--------------------------------------------------------------------------")
print("Filterbereich | lambda / nm | m / °mT^-1        | V / rad(Tm)^-1")
print("--------------------------------------------------------------------------")
print(f"360–460 nm    | 410 ± 50    | {m_360:.5f} ± {dm_360:.5f} | {V_360:.2f} ± {dV_360:.2f}")
print(f"400–560 nm    | 480 ± 80    | {m_400:.5f} ± {dm_400:.5f} | {V_400:.2f} ± {dV_400:.2f}")
print(f"560–630 nm    | 595 ± 35    | {m_560:.5f} ± {dm_560:.5f} | {V_560:.2f} ± {dV_560:.2f}")
print("--------------------------------------------------------------------------")