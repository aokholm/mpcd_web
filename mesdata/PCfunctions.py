import numpy as np


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

def dimStdMeanshiftCpk2Itg(dim,std,meanshift,cpk):

	# Calculates a IT grade from meanshift, stadard deviation and cpk-value

	symtol = stdMeanshiftCpk2Symtol(std,meanshift,cpk)

	itg = dimSymtol2Itg(dim,symtol)

	return itg

def upperLowerTol2SymTol(upper, lower):
	
	# Calculates symmetric tolerance width

	tol_spec = (upper-lower)/2.0

	return tol_spec