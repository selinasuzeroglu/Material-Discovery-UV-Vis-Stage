import pandas as pd

import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import os
import sys
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt



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

