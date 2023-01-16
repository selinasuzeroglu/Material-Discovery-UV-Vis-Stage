import matplotlib.pyplot as plt
import pyodbc
import pandas as pd
import numpy as np


import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import os
import sys
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt

cnxn_str = ("Driver={SQL Server};"
            "Server=MU00195249\ZEISSSQL;"
            "Database=InProcess;"
            "Trusted_Connection=yes;"
            "UID=sa;"
            "PWD=ZeissSql2015!;")

cnxn = pyodbc.connect(cnxn_str)

cursor = cnxn.cursor()


sql_command = """CREATE TABLE table12 (
       [Time_v] VARCHAR(max),
	   [Time_w] VARCHAR(max),
	   ResultName_v VARCHAR(max),
	   ResultName_w VARCHAR(max),
	   [Value] VARCHAR(max),
	   [Wavelength] VARCHAR(max)
)
;"""
cursor.execute(sql_command)

sql_command = """DECLARE @RowNo_w int =1;
DECLARE @RowNo_v int =1;
WITH cte_split_w(ROWNO_w, [Timestamp_w], ResultName_w, split_wavelengths, [Wavelengths]) AS
(

   -- anchor member
   SELECT 
       @RowNo_w as ROWNO_w,
	   [Timestamp],
       ResultName,
	   LEFT([Wavelengths], CHARINDEX(';', [Wavelengths] + ';') - 1),
	   STUFF([Wavelengths], 1, CHARINDEX(';', [Wavelengths] + ';'), '')
   FROM InProcess.dbo.VSpectra



   UNION ALL

   -- recursive member 
   SELECT
        ROWNO_w+1,
		[Timestamp_w],
        ResultName_w,
        LEFT([Wavelengths], CHARINDEX(';', [Wavelengths] + ';') - 1),
        STUFF([Wavelengths], 1, CHARINDEX(';', [Wavelengths] + ';'), '')
    FROM cte_split_w
	WHERE split_wavelengths > ''

)
,

cte_split_v(ROWNO_v, [Timestamp_v], ResultName_v, split_values, [Values]) AS
(

   -- anchor member
   SELECT
       @RowNo_v as ROWNO_v,
	   [Timestamp],
       VSpectra.ResultName,
	   LEFT(CONVERT(VARCHAR(MAX), [Values]), CHARINDEX(';', CONVERT(VARCHAR(MAX), [Values]) + ';') - 1),
	   STUFF(CONVERT(VARCHAR(MAX), [Values]), 1, CHARINDEX(';', CONVERT(VARCHAR(MAX), [Values]) + ';'), '')
   FROM InProcess.dbo.VSpectra


   UNION ALL

   -- recursive member 
   SELECT
        ROWNO_v+1,
		[Timestamp_v],
        ResultName_v,
		LEFT(CONVERT(VARCHAR(MAX), [Values]), CHARINDEX(';', CONVERT(VARCHAR(MAX), [Values]) + ';') - 1),
	   STUFF(CONVERT(VARCHAR(MAX), [Values]), 1, CHARINDEX(';', CONVERT(VARCHAR(MAX), [Values]) + ';'), '')
    FROM cte_split_v
	WHERE CONVERT(VARCHAR(MAX), [split_values]) <> ''
)

INSERT INTO table12
SELECT cte_split_v.Timestamp_v,
       cte_split_w.Timestamp_w,
       cte_split_v.ResultName_v, 
	   cte_split_w.ResultName_w,
       cte_split_v.split_values,
	   cte_split_w.split_wavelengths
FROM cte_split_v INNER JOIN cte_split_w on ROWNO_v=ROWNO_w
WHERE split_values <> ''
AND split_wavelengths <> ''
AND [Timestamp_v]='2022-10-20 03:12:29.253'
AND [Timestamp_w]=[Timestamp_v]
AND ResultName_v='Transmission of Sample'
AND ResultName_v=ResultName_w
ORDER BY split_wavelengths
option (maxrecursion 0);
"""

cursor.execute(sql_command)

#data from SQL
data = pd.read_sql('SELECT [Value], [Wavelength] FROM table12',cnxn)



spectrum = data.to_numpy().astype(float)

try:
    r = float(sys.argv[1])
    #d = float(sys.argv[2])
    imgfile = sys.argv[2]
    dpi = int(sys.argv[3])
    # d = float(sys.argv[4])
except Exception as e:
    print('input format: taucauto.py r imgfile dpi')
    print('r : tauc plot exponent value')
    print('imgfile : image file type/extension')
    print('dpi : image quality (dpi)')
    exit()

λ = spectrum[:, 0]
A = spectrum[:, 1] # Absorbance has to be put in spectrum: right now value = transmission

def GetHv(x):
    return (6.626070e-34 * 299792458) / (x * 1e-9) * 6.242e18

#def GetAlpha(A, d):  #=a  unnecessary because of linear relation
 #   return (A/d)

def GetOrdinate(hv,a,r):
    return (hv*a)**(1/r)


tauc_spectrum = np.zeros((len(spectrum),2))
tauc_spectrum[:, 0] = GetHv(λ)
tauc_spectrum[:, 1] = GetOrdinate(GetHv(λ), A, r)


