import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# print("Skript startet")
# def absorption_fit(d, A_gemessen, main_dB, out_dB, korrigieren=True):
#     d = np.array(d, dtype=float)
#     A_gemessen = np.array(A_gemessen, dtype=float)
#     main_dB = np.array(main_dB, dtype=float)
#     out_dB = np.array(out_dB, dtype=float)

#     if korrigieren:
#         A = A_gemessen * 10 ** (-(main_dB + out_dB) / 20)
#     else:
#         A = A_gemessen

#     def model(d, A0, lamb):
#         return A0 * np.exp(-2 * lamb * d)

#     popt, pcov = curve_fit(model, d, A, p0=[A[0], 0.1])
#     A0, lamb = popt

#     d_fit = np.linspace(min(d), max(d), 300)
#     A_fit = model(d_fit, A0, lamb)

#     plt.scatter(d, A, label="Messwerte")
#     plt.plot(d_fit, A_fit, label=f"Fit: λ = {lamb:.4f} 1/cm")
#     plt.xlabel("Dicke d [cm]")
#     plt.ylabel("Amplitude korrigiert [a.u.]")
#     plt.title("Absorption Ultraschall in PVC")
#     plt.grid(True)
#     plt.legend()
#     plt.show()

#     print("A0 =", A0)
#     print("lambda =", lamb, "1/cm")


# # =========================
# # HIER DEINE WERTE EINTRAGEN
# # =========================
# if __name__ == "__main__":
#     d = [120.76, 80.81, 41.30]
#     A = [0.125, 0.3958, 0.620]
#     main = [35, 35, 20]
#     out = [10, 5, 0]

#     absorption_fit(d, A, main, out, korrigieren=True)

print("Skript2 startet")
def absorption_fit(d, A_gemessen, main_dB, out_dB,
                   d_err=0.1, A_err=0.001,
                   korrigieren=True):

    d = np.array(d, dtype=float)
    A_gemessen = np.array(A_gemessen, dtype=float)

    main_dB = np.array(main_dB, dtype=float)
    out_dB = np.array(out_dB, dtype=float)

    # Verstärkungskorrektur
    if korrigieren:
        A = A_gemessen * 10 ** (-(main_dB + out_dB) / 20)
    else:
        A = A_gemessen

    # Fehler der Amplitude
    A_sigma = np.ones_like(A) * A_err

    # Modellfunktion
    def model(d, A0, lamb):
        return A0 * np.exp(-2 * lamb * d)

    # gewichteter Fit
    popt, pcov = curve_fit(
        model,
        d,
        A,
        sigma=A_sigma,
        absolute_sigma=True,
        p0=[A[0], 0.1]
    )

    A0, lamb = popt

    # Fehler aus Kovarianzmatrix
    A0_err, lamb_err = np.sqrt(np.diag(pcov))

    # Plot
    d_fit = np.linspace(min(d), max(d), 300)
    A_fit = model(d_fit, A0, lamb)

    plt.figure(figsize=(7,5))

    plt.errorbar(
        d, A,
        xerr=d_err,
        yerr=A_sigma,
        fmt='o',
        capsize=4,
        label='Messwerte'
    )

    plt.plot(
        d_fit,
        A_fit,
        label=f'Fit: λ = {lamb:.4f} ± {lamb_err:.4f} 1/cm'
    )

    plt.xlabel("Dicke d [cm]")
    plt.ylabel("korrigierte Amplitude")
    plt.title("Absorption in PVC")
    plt.grid(True)
    plt.legend()
    plt.show()

    print(f"A0 = {A0:.5f} ± {A0_err:.5f}")
    print(f"λ = {lamb:.5f} ± {lamb_err:.5f} 1/cm")


# =========================
# DEINE WERTE
# =========================

d = [120.76, 80.81, 41.30]

#1MHz
# A = [0.125, 0.3958, 0.620]
# main = [35, 35, 20]
# out = [10, 5, 0]

#2MHz
A = [0.01581, 0.16440677, 0.57627]
main = [0, 35, 25]
out = [25, 10, 0]

absorption_fit(
    d,
    A,
    main,
    out,
    d_err=0.1,
    A_err=0.01,
    korrigieren=True
)
