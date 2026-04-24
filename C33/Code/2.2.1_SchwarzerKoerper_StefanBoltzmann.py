from matplotlib import ticker
import numpy as np
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from scipy.optimize import curve_fit

#Import data from path
base_path = Path.cwd()

data_path = base_path / 'C33' / 'Data' / 'Versuch_33.xlsx'
img_path = base_path.parent / 'C2-Praktikum' / 'C33' /  'Images'
Data = pd.read_excel(data_path, sheet_name='schwarze Körper SBG', engine='openpyxl')

#pick out data from excel sheet 3

Spannung = np.array([[x, y] for x, y in zip(Data['Spannung in mV'].tolist(), Data['Temperatur in °C'].tolist())])

##Errors
errT = 0.1 #Temperatur in °C
errU = 0.1 #Spannung in mV

def model(T, a, b):
    return a * T**4 + b

##plot data as U(T) for all 4 surfaces in 4 different plots
###def plot
def plot_and_fit(data, name, errU=0.1, errT=0.1):
    U = data[:, 0]
    T_C = data[:, 1]

    # convert to Kelvin
    T_K = T_C + 273.15
    T4 = T_K**4

    # linear fit: U = a * x + b
    #coeffs = np.polyfit(T_K, U, 1)
    #fit = np.poly1d(coeffs)

    #x_fit = np.linspace(T_K.min(), T_K.max(), 200)

    # quadratic fit: U = a*T^2 + b*T + c
    coeffs = np.polyfit(T_K, U, 2)
    fit = np.poly1d(coeffs)

    x_fit = np.linspace(T_K.min(), T_K.max(), 200)

    ###params, _ = curve_fit(model, T_K, U)
    ###x_fit = np.linspace(T_K.min(), T_K.max(), 200)

    # --- plot U(T)
    plt.figure()
    plt.errorbar(T_K, U, xerr=errT, yerr=errU, fmt='x', label='data', color='black', capsize=4)
    #plt.plot(T_K, fit(T_K), label=f'fit: U = {coeffs[0]:.3e} T + {coeffs[1]:.3e}', color='black')
    plt.plot(x_fit, fit(x_fit), label=f'U = {coeffs[0]:.3e} T² + {coeffs[1]:.3e} T + {coeffs[2]:.3e}', color='black')
    ###plt.plot(x_fit, model(x_fit, *params), label=f'U = {params[0]:.3e} T⁴ + {params[1]:.3e}', color='black')
    plt.xlabel("T [K]")
    plt.ylabel("U [mV]")
    plt.title(f"{name} - U(T)")
    plt.legend()
    plt.grid(False)
    plt.gca().yaxis.set_minor_locator(AutoMinorLocator(4))
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator(4))
    plt.tick_params(axis='both', which='minor', direction='in', right=True, top=True)
    plt.tick_params(axis='both', which='major', direction='in', right=True, top=True, length=5)
    plt.tight_layout()
    plt.savefig(img_path / f"{name}_U_T.png")
    plt.show()


    # linear fit: U = a * x + b
    coeffs2 = np.polyfit(T4, U, 1)
    fit2 = np.poly1d(coeffs2)

    x_fit2 = np.linspace(T4.min(), T4.max(), 200)
    

    # --- plot U(T^4)
    plt.figure()
    plt.errorbar(T4, U, xerr=4*T_K**3*errT, yerr=errU, fmt='x', label='data', color='black', capsize=4)
    plt.plot(x_fit2, fit2(x_fit2), label=f'fit: U = {coeffs2[0]:.3e} T⁴ + {coeffs2[1]:.3e}', color='black')
    plt.xlabel("T⁴ [K⁴]")
    plt.ylabel("U [mV]")
    plt.title(f"{name} - U(T⁴)")
    plt.legend()
    plt.grid(False)
    plt.gca().yaxis.set_minor_locator(AutoMinorLocator(4))
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator(4))
    plt.tick_params(axis='both', which='minor', direction='in', right=True, top=True)
    plt.tick_params(axis='both', which='major', direction='in', right=True, top=True, length=5)
    plt.tight_layout()
    plt.savefig(img_path / f"{name}_U_T4.png")
    plt.show()

plot_and_fit(Spannung, "Black body  - Stefan-Boltzmann law", errU, errT)