import pyodbc
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter


cnxn_str = ("Driver={SQL Server};"
            "Server=MU00195249\ZEISSSQL;"
            "Database=InProcess;"
            "Trusted_Connection=yes;"
            "UID=sa;"
            "PWD=ZeissSql2015!;")
cnxn = pyodbc.connect(cnxn_str)

spectrum = '''SELECT * FROM InProcess.dbo.VSpectra'''
data = pd.read_sql(spectrum, cnxn)

result_name = data.ResultName.str.split(";", expand=True, )
wavelengths = data.Wavelengths.str.split(";", expand=True, )
values = data.Values.str.split(";", expand=True, )


class InProcessData:

    def __init__(self, result, column):
        self.column = column
        self.result = result

    def get_data(self):
        transposed_data = self.column.transpose()
        result_name.rename(columns={0: 'ResultName'}, inplace=True)
        result_index = result_name[result_name['ResultName'] == self.result].index.values
        recent_data_index = max(result_index)
        transposed_data = transposed_data.iloc[:, recent_data_index]
        return transposed_data.to_numpy().astype(float)


transmission = InProcessData('Transmission', values).get_data()
reflection = InProcessData('Reflection', values).get_data()
absorbance = InProcessData('Spectrum', values).get_data()
wavelength_transmission = InProcessData('Transmission', wavelengths).get_data()
wavelength_reflection = InProcessData('Reflection', wavelengths).get_data()


def get_energy(λ):  # λ = Wavelengths
    energy = (6.626070e-34 * 299792458) / (λ * 1e-9) * 6.242e18  # get Energy in eV
    return energy


# def get_absorbance():  # R = Reflection
#     R = reflection
#     absorbance = np.log(1 / R)
#     return absorbance


def get_alpha():  # A = Absorbance, d = thickness of the sample (in cm)
    d = 0.37  # estimated sample thickness
    A = absorbance
    absorption_coefficient = A / d
    return absorption_coefficient


def get_ordinate(E, a, r):  # E = Energy, a = Absorption Coefficient, r = power factor of the transition mode
    x = E*a
    if (x > 0).any():
        y = x**(1/r)
        return y
    else:
        return 0


Energy = get_energy(wavelength_reflection)
AbsorptionCoefficient = get_alpha()

r_direct = 1/2
r_indirect = 2


tauc_spectrum = np.zeros((len(reflection), 2))
tauc_spectrum[:, 0] = Energy  # hv on x-axis
tauc_spectrum[:, 1] = get_ordinate(Energy, AbsorptionCoefficient, r_indirect)  # (hv*a)**(1/r) on y-axis


# Calculation:

# Transform Tauc plot to interpolation function
y = interp1d(tauc_spectrum[:, 0], savgol_filter(tauc_spectrum[:, 1], 51, 3))
x = np.linspace(tauc_spectrum[0, 0], tauc_spectrum[-1:, 0], 5000).squeeze()


# Calculate 1st derivative along Tauc plot
dy = np.diff(y(x), 1)
dx = np.diff(x, 1)

y_1d = interp1d(x[:-1], dy / dx)


# Calculate 2nd derivative along Tauc plot
d2y = np.diff(y(x), 2)
dx2 = 0.0001
y_2d = interp1d(x[:-2], d2y / dx2)

# Find point in Tauc plot where 2nd derivative == 0 and gradient is at a maximum
gradmax = 0.
for i in range(2, len(x[:-2])):
    grad = y_1d(x[:-2])[i]
    if grad > gradmax:
        gradmax = grad
    if np.allclose([y_2d(x[:-2])[i]], [0.], atol=0.001) and y(x)[i] > 0.1 * np.amax(
            tauc_spectrum[:, 1]) and grad >= gradmax:
        x_0 = x[i]
        y_0 = y(x)[i]

# Calculate extrapolation line
m = y_1d(x_0)
c = y_0 - m * x_0

# Calculate optical gap from extrapolation line
x_cross = (0 - c) / m
gap = x_cross

# Plot Tauc plot, extrapolation line and point equal to optical gap
plt.xlabel(r'$ h \nu$ (eV)')
plt.ylabel(r'$( \alpha h \nu )^{1/r}$ $(cm^{-1})$')
plt.figtext(0.15, 0.8, 'Optical Gap = ' + str(x_cross)[:4] + ' eV')

plt.plot(tauc_spectrum[:, 0], tauc_spectrum[:, 1], '-',
         [(0 - c) / m, (0.7 * np.amax(tauc_spectrum[:, 1]) - c) / m], [0, 0.7 * np.amax(tauc_spectrum[:, 1])], '--',
         tauc_spectrum[:, 0], np.zeros(len(tauc_spectrum)), '-',
         x_cross, 0, 'o', )

plt.show()