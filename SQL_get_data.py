import pyodbc
import pandas as pd


"""" After Zeiss measurements are finished, InProcess sends the data results to SQL (for storing and processing 
information in a relational database). Using pyodbc, you can directly access SQL (line 8 - 14) and query desired data 
results through SQL commands (line 16-17). Printing line 17 shows a table containing all objects from the 
DataBaseObject (DBO) 'VSpectra' which is the location of our data results storage. 
"""""

cnxn_str = ("Driver={SQL Server};"
            "Server=MU00195249\ZEISSSQL;"
            "Database=InProcess;"
            "Trusted_Connection=yes;"
            "UID=sa;"
            "PWD=ZeissSql2015!;")
cnxn = pyodbc.connect(cnxn_str)

spectrum = '''SELECT * FROM InProcess.dbo.VSpectra'''
data = pd.read_sql(spectrum, cnxn)


"""selecting individual columns from the SQL data results table. 
For columns 'Wavelengths' and 'Values' str.split() command is needed because all the resulting data points 
(f.e. 225.00nm, 225.50nm, etc.) from one measurement are stored within the same column and row, only separated by 
semikola."""

result_name = data.ResultName
product_name = data.ProductName
timestamp = data.Timestamp
wavelengths = data.Wavelengths.str.split(";", expand=True, )
values = data.Values.str.split(";", expand=True, )


class InProcessData:
    def __init__(self, result_class, column, timestamp):
        self.result = result_class
        self.column = column
        self.timestamp = timestamp

    def get_data_from_timestamp(self):  # choose this function if you want to get timestamp and result specific data
        result_index = result_name[result_name == self.result].index.values  # select indices which include desired
        # result_name
        timestamp_index = timestamp[timestamp == self.timestamp].index.values  # select indices which include desired
        # timestamp
        data_index = list(set(timestamp_index).intersection(result_index))  # select indices with desired timestamp AND
        # result_name, f.e. 'Transmission' at '2022-12-01 23:09:58.853'
        transposed_data = self.column.transpose()  # transposing data from row to column
        desired_data = transposed_data.iloc[:, data_index]  # select data according to predefined index
        return desired_data.to_numpy().astype(float).flatten()

    def get_recent_data(self):
        result_index = result_name[result_name == self.result].index.values  # select indices which include desired
        # result_name
        recent_data_index = max(result_index)  # select most recent data result, which is resembled by highest index
        # number from all indices resembling preselected result_name
        transposed_data = self.column.transpose()  # transposing data from row to column
        desired_data = transposed_data.iloc[:, recent_data_index]  # select data according to predefined index
        return desired_data.to_numpy().astype(float).flatten()

    def get_data_from_index(self, index):
        transposed_data = self.column.transpose()
        desired_data = transposed_data.iloc[:, index]  # select data from desired index
        return desired_data.to_numpy().astype(float).flatten()


def joining_data(product_table, result_table):  # creates table with data results and according wavelengths
    value_column = InProcessData(product_table, result_table, values).get_recent_data()
    wavelength_column = InProcessData(product_table, result_table, wavelengths).get_recent_data()
    table = [wavelength_column, value_column]
    results = pd.concat(table, axis=1, join="inner")
    print(results)

cnxn.close()


