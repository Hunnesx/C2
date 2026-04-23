import numpy as np
from pathlib import Path
import pandas as pd
 

 ##import data from path
base_path = Path.cwd()

data_path = base_path / 'C33' / 'Data' / 'Versuch_33.xlsx'
img_path = base_path.parent / 'Images'
Data = pd.read_excel(data_path, sheet_name='Stefan-Boltzmann Gesetz', engine='openpyxl')

 ##pick out data
SeiteSchwarz = np.array([[x, y] for x, y in zip(Data['schwarz Spannung in mV'].tolist(), Data['Temperatur in °C'].tolist())])
SeiteWeiss = np.array([[x, y] for x, y in zip(Data['weiß Spannung in mV'].tolist(), Data['Temperatur in °C'].tolist())])
SeiteNickelPoliert = np.array([[x, y] for x, y in zip(Data['vernickelt (poliert) Spannung in mV'].tolist(), Data['Temperatur in °C'].tolist())])
SeiteNickelMatt = np.array([[x, y] for x, y in zip(Data['vernickelt (matt) Spannung in mV'].tolist(), Data['Temperatur in °C'].tolist())])  
print(SeiteNickelMatt)