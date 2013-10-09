import numpy as np


"""Conversion funciton between ITgrade and Tolerance - Input Should be in millimeters"""
	
def itg2tol(Dim, ITG):

	# Calculates the symmetric tolerances from IT-grade
	if Dim  <= 500:
		Tol = (10**(0.2*(ITG-1)))*(0.45*(Dim**(1./3.))+(0.001*Dim))/1000/2
	else:
		Tol = 10**(0.2*(ITG-1))*(0.004*Dim+2.1)/1000/2
	return Tol

def tol2itg(Dim, Tol):

	# IT-grade from symmetric Tolerance

	if Dim <= 500:
		Itg =5*np.log10(2*Tol*1000/(0.45*Dim**(1./3.)+Dim*0.001))+1	
	else:
		Itg =5*np.log10(2*Tol*1000/(0.004*Dim+2.1))+1
	return Itg


def stdbias2tol(std,bias, cpk):

	# Calculates a tolerance from cpk

	tol = bias + 3 * std * cpk

	return tol

def stdbias2itg(dim,std,bias,cpk):

	# Calculates a IT grade from bias, stadard deviation and cpk-value

	tol = stdbias2tol(std,bias,cpk)

	itg = tol2itg(dim,tol)

	return itg
