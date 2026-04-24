import numpy as np

#Data from excel sheet 2
kFilter =  2.073 #mV
Fensterglas = 0.420 #mV
Siliziumwafer = (0.965 + 0.966)/2 #mV
NaCl = 1.515 #mV
vernickelt = -0.005 #mV

#def transmittance and error in percentage

def transmittance(U):
    return (U-vernickelt)/kFilter * 100
def transmittance_error(U, errU=0.1):
    return errU/kFilter * 100

#returing transmittance and error for all 4 materials
materials = {'Fensterglas': Fensterglas, 'Siliziumwafer': Siliziumwafer, 'NaCl': NaCl, 'vernickelt': vernickelt}
results = {}
for name, U in materials.items():
    T = transmittance(U)
    dT = transmittance_error(U)
    results[name] = (T, dT)
    print(f"{name}: Transmittance = {T:.3f} ± {dT:.3f}")
