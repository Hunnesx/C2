import numpy as np

def wellenlaenge(n, laser, s, x):
    return(n * laser * s / x)*10**(-3)
def wellenlaenge_error(n, laser, s, x, s_error, x_error):
    return np.sqrt((n * laser * s_error / x) ** 2 + (n * laser * s * x_error / x ** 2) ** 2)*10**(-3)
def schallgeschwindigkeit(f, lambda_):
    return f * lambda_
def schallgeschwindigkeit_error(f, lambda_, f_error, lambda_error):
    return np.sqrt((f_error * lambda_) ** 2 + (f * lambda_error) ** 2)

s_error = 1.0
x_error = 0.10
s = 2851.5
n = 1
frequenzen = [3, 5, 7, 9, 11, 12]

all_v = []
all_v_err = []

# --- helper to collect and print ---
def process(label, laser, x_list):
    for i in range(len(frequenzen)):
        lam     = wellenlaenge(n, laser, s, x_list[i])
        lam_err = wellenlaenge_error(n, laser, s, x_list[i], s_error, x_error)
        v       = schallgeschwindigkeit(frequenzen[i], lam)
        v_err   = schallgeschwindigkeit_error(frequenzen[i], lam, 1, lam_err)
        all_v.append(v)
        all_v_err.append(v_err)
        print(f"{label}: n={n}, f={frequenzen[i]}, lambda={lam:.4f} +/- {lam_err:.4f} µm")
        print(f"{label}: n={n}, f={frequenzen[i]}, v={v:.4f} +/- {v_err:.4f} m/s")
        print("-----------------------------")

process("Rot",  650,   [2.5, 6, 8, 12, 14, 16])
print("\n")
process("Gruen", 532.0, [4.5, 6, 8, 9, 11, 13])
print("\n")
process("Blau", 405,   [3, 4, 5.5, 7, 9, 11])

# --- Mean over all 18 values ---
all_v     = np.array(all_v)
all_v_err = np.array(all_v_err)

mean_v     = np.mean(all_v)
mean_v_err = np.sqrt(np.sum(all_v_err**2)) / len(all_v_err)   # Gaussian error of the mean

print(f"\n{'='*45}")
print(f"Mittlere Schallgeschwindigkeit (alle Farben & Frequenzen):")
print(f"  v_mean = {mean_v:.2f} +/- {mean_v_err:.2f} m/s")
print(f"{'='*45}")