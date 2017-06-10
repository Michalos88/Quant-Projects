# Michal Lyskawinski
# Date: 11/28/2016
# Hull-White Model

from math import *
from scipy.stats import norm

# interest rate parameters:
r = 0.04
r1 = 0.04
sigma = 0.01
a = 0.1

# Option parameters:        European Call
OM = 2  # Option Maturity in years
OBM = 6  # Option's Bond Maturity in years
K = 0.73

# Bond parameters:
T = 1  # Bond Maturity in years
s = 2
t = 0 # Present time
dt = 0.1


def PDB(r,M):
    P = exp(-r*M)
    return P

# Pricing the Bond:
P5 = PDB(r,s)
P1 = PDB(r,T)
dB = (1/a)*(1-PDB(a,s-T))
Slope = (log(PDB(r,T+dt))-log(PDB(r,T-dt)))/(2*dt)
lnA = log(P5/P1) - dB*(Slope)
BP = exp(lnA)*PDB(r1,dB)

print('Price of the bond =',BP)

# Pricing the European Option:
PO = PDB(r,OM)
POB = PDB(r,OBM)
# K = POB/PO  # If no K
sigmaP = sqrt((sigma**2/(2*a**3))*(1-PDB(2*a,OM))*(1-PDB(a,OBM-OM))**2)
d1 = ((log((POB)/(K*P1)))/(sigmaP)) + (sigmaP*0.5)
d2 = d1 - sigmaP
c = POB*norm.cdf(d1) - K*PO*norm.cdf(d2)  # call
p = PO*K*norm.cdf(-d2) - POB*norm.cdf(-d1)  # put

print('Price of the European Call =',c)



