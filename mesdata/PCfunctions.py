import numpy as np
import math
from scipy.stats import norm

"""Conversion funciton between ITgrade and Symtolerance - Input Should be in millimeters"""
	
def dimItg2Symtol(Dim, ITG):

	# Calculates the symmetric Symtolerances from IT-grade
	if Dim  <= 500:
		symtol = (10**(0.2*(ITG-1)))*(0.45*(Dim**(1./3.))+(0.001*Dim))/1000/2
	else:
		symtol = 10**(0.2*(ITG-1))*(0.004*Dim+2.1)/1000/2
	return symtol

def dimSymtol2Itg(Dim, Symtol):

	# IT-grade from symmetric Symtolerance

	if Dim <= 500:
		Itg =5*np.log10(2*Symtol*1000/(0.45*Dim**(1./3.)+Dim*0.001))+1	
	else:
		Itg =5*np.log10(2*Symtol*1000/(0.004*Dim+2.1))+1
	return Itg


def stdMeanshiftCpk2Symtol(std,meanshift, cpk):

	# Calculates the symmetric Symtolerance from cpk
	symtol = abs(meanshift) + 3 * std * cpk
	return symtol

def UslLsl2SymTol(USL, LSL):
	
	# Calculates symmetric tolerance width

	symtol = (USL-LSL)/2.0

	return symtol

def c4stdCorrectionFactor(n):
	
	return math.sqrt( 2.0 / (n-1)) * math.gamma(n/2.0) / math.gamma((n-1)/2.0)

def list2cdf (input_data):

	# recieves a list of data, returns a normal distribution fit

	mean = np.mean(input_data)
	std = np.std(input_data, ddof=1)

	minpos = mean - 3*std
	maxpos = mean + 3*std
	x = np.linspace(minpos,maxpos,100).tolist()
	cdf = [norm.cdf(x[i], loc=mean, scale=std) for i in range(100)]

	return (x, cdf)