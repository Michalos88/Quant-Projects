# Michal Lyskawinski
# Date: 11/28/2016
# CIR Model

from math import *
from scipy.stats import norm,chi2

# interest rate parameters:
rzero = 0.04
rbar = 0.05
a = 1.5
sigma = 0.1

# Option parameters:        European Call
OM = 2  # Option Maturity in years
OBM = 6  # Option's Bond Maturity in years
K = 0.73

# Bond parameters:
BM = 2 # Bond Maturity in years


def PDB(r,M):
    P = exp(-r*M)
    return P



# Pure discount Bond price calculations:
def PBond(M,a,sigma,rbar,rzero):
    phi1 = sqrt(a ** 2 + 2 * sigma ** 2)
    phi2 = (a + phi1) / 2
    phi3 = (2 * a * rbar) / sigma ** 2
    B = (PDB(-phi1,M)-1)/(phi2*(PDB(-phi1,M)-1)+phi1)
    A = ((phi1*PDB(-phi2,M))/(phi2*(PDB(-phi1,M)-1)+phi1))**phi3
    P = A*PDB(B,rzero)
    return P

print('Price of the bond =',PBond(BM,a,sigma,rbar,rzero))

def B(M,a,sigma):
    phi1 = sqrt(a ** 2 + 2 * sigma ** 2)
    phi2 = (a + phi1) / 2
    B = (PDB(-phi1,M)-1)/(phi2*(PDB(-phi1,M)-1)+phi1)
    return B

def A(M,a,sigma,rbar):
    phi1 = sqrt(a ** 2 + 2 * sigma ** 2)
    phi2 = (a + phi1) / 2
    phi3 = (2 * a * rbar) / sigma ** 2
    A = ((phi1 * PDB(-phi2, M)) / (phi2 * (PDB(-phi1, M) - 1) + phi1)) ** phi3
    return A

sigmaR = ((sigma*sqrt(rzero))/BM)*B(BM,a,sigma) # volatility of the one-year spot rate
POB = PBond(OBM,a,sigma,rbar,rzero)
PO = PBond(OM,a,sigma,rbar,rzero)

theta = sqrt((a**2) + 2*(sigma**2))
phi = (2*theta)/((sigma**2)*(PDB(-theta,OM)-1))
Y = (a+theta)/sigma**2
BOB = B(OBM-OM,a,sigma)
AOB = A(OBM-OM,a,sigma,rbar)

d1 = 2*rzero*(phi+Y+BOB)
d2 = (4*a*rbar)/sigma**2
d3 = (2*(phi**2)*rzero*PDB(-theta,OM))/(phi+Y+BOB)
d4 = 2*rzero*(phi+Y)
d5 = (2*(phi**2)*rzero*PDB(-theta,OM))/(phi+Y)

C = POB*chi2.cdf(d1,d2,d3)-K*PO*chi2.cdf(d4,d2,d5)
print(C)

