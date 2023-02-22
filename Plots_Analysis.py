import pyodbc
import pandas as pd
import math
import numpy as np

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
wavelength_transmission = InProcessData('Transmission', wavelengths).get_data()
wavelength_reflection = InProcessData('Reflection', wavelengths).get_data()


def get_energy(λ):  # get Energy in eV
    energy = (6.626070e-34 * 299792458) / (λ * 1e-9) * 6.242e18
    return energy


def get_alpha(A, d):  # A = Absorbance, d = thickness of the sample (in cm)
    absorption_coefficient = A / d
    return absorption_coefficient


def get_absorbance(R):  # R = Reflection
    absorbance = math.log(1 / R)
    return absorbance


def get_ordinate(E, a, r):  # E = Energy, a = Absorption Coefficient, r = power factor of the transition mode
    y = (E*a)**(1/r)
    return y


tauc_spectrum = np.zeros((len(spectrum),2))
tauc_spectrum[:, 0] = get_energy()
tauc_spectrum[:, 1] = get_ordinate()