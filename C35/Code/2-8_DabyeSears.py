import numpy as np

def wellenlaenge(n, laser, s, x):
    return(n * laser * s / x)*10**(-3)

def wellenlaenge_error(n, laser, s, x, s_error, x_error):
    return np.sqrt((n * laser * s_error / x) ** 2 + (n * laser * s * x_error / x ** 2) ** 2)*10**(-3)

def schallgeschwindigkeit(f, lambda_):
    return f * lambda_

def schallgeschwindigkeit_error(f, lambda_, f_error, lambda_error):
    return np.sqrt((f_error * lambda_) ** 2 + (f * lambda_error) ** 2)

s_error = 1.0 #mm
x_error = 0.10 #mm

s = 2851.5 #mm
n = 1
frequenzen = [3, 5, 7, 9, 11, 12]

#laser rot
laser_rot = 632.8 #nm
x_rot = [2.5, 6, 8, 12, 14, 16] #mm

for i in range(len(frequenzen)):
    print(f"Rot: n={n}, f={frequenzen[i]}, lambda={wellenlaenge(n, laser_rot, s, x_rot[i])} +/- {wellenlaenge_error(n, laser_rot, s, x_rot[i], s_error, x_error)} mu m")
    print(f"Rot: n={n}, f={frequenzen[i]}, v={schallgeschwindigkeit(frequenzen[i], wellenlaenge(n, laser_rot, s, x_rot[i]))} +/- {schallgeschwindigkeit_error(frequenzen[i], wellenlaenge(n, laser_rot, s, x_rot[i]), 1, wellenlaenge_error(n, laser_rot, s, x_rot[i], s_error, x_error))} m/s")
    print("-----------------------------")

print("\n\n")

#laser gruen
laser_gruen = 532.0 #nm
x_gruen = [4.5, 6, 8, 9, 11, 13] #mm

for i in range(len(frequenzen)):
    print(f"Gruen: n={n}, f={frequenzen[i]}, lambda={wellenlaenge(n, laser_gruen, s, x_gruen[i])} +/- {wellenlaenge_error(n, laser_gruen, s, x_gruen[i], s_error, x_error)} mu m")
    print(f"Gruen: n={n}, f={frequenzen[i]}, v={schallgeschwindigkeit(frequenzen[i], wellenlaenge(n, laser_gruen, s, x_gruen[i]))} +/- {schallgeschwindigkeit_error(frequenzen[i], wellenlaenge(n, laser_gruen, s, x_gruen[i]), 1, wellenlaenge_error(n, laser_gruen, s, x_gruen[i], s_error, x_error))} m/s")
    print("-----------------------------")

print("\n\n")

#laser blau
laser_blau = 488.0 #nm
x_blau = [3, 4, 5.5, 7, 9, 11] #mm

for i in range(len(frequenzen)):
    print(f"Blau: n={n}, f={frequenzen[i]}, lambda={wellenlaenge(n, laser_blau, s, x_blau[i])} +/- {wellenlaenge_error(n, laser_blau, s, x_blau[i], s_error, x_error)} mu m")
    print(f"Blau: n={n}, f={frequenzen[i]}, v={schallgeschwindigkeit(frequenzen[i], wellenlaenge(n, laser_blau, s, x_blau[i]))} +/- {schallgeschwindigkeit_error(frequenzen[i], wellenlaenge(n, laser_blau, s, x_blau[i]), 1, wellenlaenge_error(n, laser_blau, s, x_blau[i], s_error, x_error))} m/s")
    print("-----------------------------")
