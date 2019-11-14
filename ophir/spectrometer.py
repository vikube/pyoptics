import pandas as pd
import re
import numpy as np


def load_spectrum(filename, wlmin=None, wlmax=None):
    """
    Load spectral data captured by Ophir's spectrometer. The header lines are detected using a phrase "Begin Spectral Data". The first column of the data is assumed to be wavelength.
    :param filename: filepath to the file to be loaded
    :param wlmin: min value of wavelength to filter when loaded
    :param wlmax: max value of wavelength to filter when loaded
    :return:
    """
    # eliminate metadata at the beginning
    with open(filename, 'r') as f:
        count = 0
        while re.search("Begin Spectral Data", f.readline()) is None:
            count += 1

    data = pd.read_csv(filename, sep="\t", skiprows=count, header=None)

    if wlmin is None:
        wlmin = data[0].min()

    if wlmax is None:
        wlmax = data[0].max()

    data = data.loc[data[0].between(wlmin, wlmax)]

    return data