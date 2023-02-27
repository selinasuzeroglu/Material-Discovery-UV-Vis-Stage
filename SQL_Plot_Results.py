import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
from Snapshot import sample_list

image_index = 0
def fire_results():
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

    def plotting():

        fig, (ax1, ax2) = plt.subplots(2)

        ax1.plot(wavelength_transmission, transmission)
        ax1.set_title('Transmission')

        ax2.plot(wavelength_reflection, reflection)
        ax2.set_title('Reflection')

        custom_ylim = (0, 100)
        plt.setp((ax1, ax2), ylim=custom_ylim)

        global image_index
        collection_name = sample_list[image_index]
        plt.savefig(f'{collection_name}')
        plt.show(block=False)

        image_index += 1

    return plotting()
    cnxn.close()


