'''
Created on Dec 14, 2013

@author: aokholmRetina
'''
from scipy.stats import norm
import numpy as np
from mesdata.PCfunctions import meanStd
from scipy.special import erfcinv

def list2cdf (input_data):
    # recieves a list of data, returns a normal distribution fit

    (mean, std) = meanStd(input_data)

    minpos = mean - 3*std
    maxpos = mean + 3*std
    x = np.linspace(minpos,maxpos,100).tolist()
    cdf = [norm.cdf(x[i], loc=mean, scale=std) for i in range(100)]
    return (x, cdf)

def list2cdfNinety(input_data):
    # recieves a list of data, returns a normal distribution fit
    (mean, std) = meanStd(input_data)

    minpos = mean - 3*std
    maxpos = mean + 3*std
    x = np.linspace(minpos,maxpos,100).tolist()
    cdf = [norm.cdf(x[i], loc=mean, scale=std) for i in range(100)]
    ninety = norm.ppf(0.9, loc=mean, scale=std)
    
    return (x, cdf, ninety)

def wilson (cdf,n,alpha):
    
    phat = []
    xc = []
    wsi_up = []
    wsi_lo = []
    halfwidth = [] 
    z = np.sqrt(2)*erfcinv(alpha)
    den = 1+(z**2/float(n))
     
    for i in range(len(cdf)):
        phat.append(cdf[i]/n)
        xc.append((phat[i] + (z**2)/float(2*n))/den)        
        halfwidth.append((z*np.sqrt((phat[i]*(1-phat[i])/n) + (z**2 /(4*(n**2)))))/den)
        wsi_up.append(xc[i]+halfwidth[i])
        wsi_lo.append(xc[i]-halfwidth[i])
    
    return (wsi_up, wsi_lo)