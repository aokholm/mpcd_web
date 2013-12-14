'''
Created on Dec 14, 2013

@author: aokholmRetina
'''
from scipy.stats import norm
import numpy as np
from mesdata.PCfunctions import c4stdCorrectionFactor


def list2cdf (input_data):

    # recieves a list of data, returns a normal distribution fit

    mean = np.mean(input_data)
    std = np.std(input_data, ddof=1) / c4stdCorrectionFactor(len(input_data))

    minpos = mean - 3*std
    maxpos = mean + 3*std
    x = np.linspace(minpos,maxpos,100).tolist()
    cdf = [norm.cdf(x[i], loc=mean, scale=std) for i in range(100)]

    return (x, cdf)