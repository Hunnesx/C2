import numpy as np

#Data from excel sheet 2
kFilter =  2.073 #mV
Fensterglas = 0.0420 #mV
Siliziumwafer = (0.965 + 0.966)/2 #mV
NaCl = 1.515 #mV
vernickelt = -0.005 #mV

#def transmittance and error in percentage

def transmittance(U):
    return (U-vernickelt)/kFilter * 100
def transmittance_error(U, errU=0.01):
    return errU/kFilter * 100

#returing transmittance and error for all 4 materials
materials = {'Fensterglas': Fensterglas, 'Siliziumwafer': Siliziumwafer, 'NaCl': NaCl, 'vernickelt': vernickelt}
results = {}
for name, U in materials.items():
    T = transmittance(U)
    dT = transmittance_error(U)
    results[name] = (T, dT)
    print(f"{name}: Transmittance = {T:.3f} ± {dT:.3f}")

##wellenlänge maximale spektrale intensität

b = 2897.771955 #\mu m * K
T_77 = 77 + 273.15 #K
T_20 = 20 + 273.15 #K
lambda_max_77 = b / T_77 #\mu m
lambda_max_20 = b / T_20 #\mu m
d_lambda_max_77 =  lambda_max_77*(b / T_77**2) * 0.1 #\mu m
d_lambda_max_20 =  lambda_max_20*(b / T_20**2) * 0.1 #\mu m
print(f"Wellenlänge der maximalen spektralen Intensität bei 77°C: {lambda_max_77:.3f} ± {d_lambda_max_77:.3f} μm")
print(f"Wellenlänge der maximalen spektralen Intensität bei 20°C: {lambda_max_20:.3f} ± {d_lambda_max_20:.3f} μm")
