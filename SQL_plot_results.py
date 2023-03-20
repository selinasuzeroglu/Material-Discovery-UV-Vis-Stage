import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
from Snapshot import sample_list
from SQL_get_data import InProcessData, result_name, product_name, timestamp, wavelengths, values

image_index = 0

"""Get all SQL data from SQL_get_data. Here we choose get_recent_data(), because we want most recent data results
after every measurement run (these data results resemble just measured spectra).  """


def fire_results():  # connecting to SQL, selecting most recent measurement results and subsequently plotting
    # transmission and reflection spectra measured by Zeiss.
    cnxn_str = ("Driver={SQL Server};"
                "Server=MU00195249\ZEISSSQL;"
                "Database=InProcess;"
                "Trusted_Connection=yes;"
                "UID=sa;"
                "PWD=ZeissSql2015!;")
    cnxn = pyodbc.connect(cnxn_str)

    transmission = InProcessData('Transmission', values, timestamp).get_recent_data()
    reflection = InProcessData('Reflection', values, timestamp).get_recent_data()
    wavelength_transmission = InProcessData('Transmission', wavelengths, timestamp).get_recent_data()
    wavelength_reflection = InProcessData('Reflection', wavelengths, timestamp).get_recent_data()

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
        plt.savefig(f'C:\\Users\\ssuz0008\\OneDrive - Monash University\\Plots\\{collection_name}')
        # change folder direction
        plt.show(block=False)

        image_index += 1

    return plotting()
    cnxn.close()

