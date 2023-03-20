import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
from SQL_get_data import InProcessData, values, timestamp, wavelengths


transmission = InProcessData('Transmission', values, timestamp).get_recent_data()
reflection = InProcessData('Reflection', values, timestamp).get_recent_data()
recent_absorbance = InProcessData('Spectrum', values, timestamp).get_recent_data()
wavelength_transmission = InProcessData('Transmission', wavelengths, timestamp).get_recent_data()
wavelength_reflection = InProcessData('Reflection', wavelengths, timestamp).get_recent_data()


def tauc_plot(absorbance):

    global x_0, y_0
    z = absorbance

    def get_energy(λ):  # λ = Wavelengths
        energy = (6.626070e-34 * 299792458) / (λ * 1e-9) * 6.242e18  # get Energy in eV
        return energy

    # def get_absorbance():  # R = Reflection
    #     R = reflection
    #     absorbance = np.log(1 / R)
    #     return absorbance

    def get_alpha():  # A = Absorbance, d = thickness of the sample (in cm)
        d = 2.2  # estimated sample thickness
        absorption_coefficient = z / d
        return absorption_coefficient

    def get_ordinate(E, a, r):  # E = Energy, a = Absorption Coefficient, r = power factor of the transition mode
        y = E * a ** (1 / r)
        return y

    energy = get_energy(wavelength_reflection)
    absorption_coefficient = get_alpha()

    r_direct = 1 / 2
    r_indirect = 2

    tauc_spectrum = np.zeros((len(reflection), 2))
    tauc_spectrum[:, 0] = energy  # hv on x-axis
    unnormalized_ordinate = get_ordinate(energy, absorption_coefficient, r_indirect) # (hv*a)**(1/r) on y-axis
    tauc_spectrum[:, 1] = unnormalized_ordinate/max(unnormalized_ordinate)

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
    for i in x:
        if (2 < i < 4).all():
            grad = y_1d(i)
            if grad > gradmax:
                gradmax = grad
            if np.allclose([y_2d(i)], [0.], atol=0.001) and y(i) > 0.1 * np.amax(
                    tauc_spectrum[:, 1]) and grad >= gradmax:
                x_0 = i
                y_0 = y(i)

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
    plt.savefig('P1_absorbance')
    plt.show(block=False)


# Data from run on 09/03/2023:
M1_absorbance = InProcessData('Spectrum', values, '2023-03-09 02:35:47.600').get_data_from_timestamp()
M2_absorbance = InProcessData('Spectrum', values, '2023-03-09 02:40:15.337').get_data_from_timestamp()
M3_absorbance = InProcessData('Spectrum', values, '2023-03-09 02:41:14.620').get_data_from_timestamp()
P1_absorbance = InProcessData('Spectrum', values, '2023-03-09 06:04:44.637').get_data_from_timestamp()


tauc_plot(P1_absorbance)