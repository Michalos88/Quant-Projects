# Michal Lyskawinski
# Date: 11/28/2016
# Ho-Lee Model

from math import *
from scipy.stats import norm

# interest rate parameters:
r = 0.04
r1 = 0.04
sigma = 0.01

# Option parameters:        European Call
OM = 2  # Option Maturity in years
OBM = 6  # Option's Bond Maturity in years
K = 0.73

# Bond parameters:
T = 1
s = 2  # Bond Maturity in years
t = 0  # Present time
dB = s - T  # difference
dt = 0.1

def PDB(r,M):
    P = exp(-r*M)
    return P

# Pricing the Bond:
P5 = PDB(r,s)
P1 = PDB(r,T)
Slope = (log(PDB(r,T+dt))-log(PDB(r,T-dt)))/(2*dt)
lnA = log(P5/P1) - dB*(Slope) - 0.5*(sigma**2)*(T-t)*dB**2
BP = exp(lnA)*PDB(r1,dB)

print('Price of the bond =',BP)

# Pricing the European Call Option:
PO = PDB(r,OM)
POB = PDB(r,OBM)
#  K = POB/PO  # If no K
sigmaP = sigma*(dB)*sqrt(T-t)
d1 = ((log((POB)/(K*P1)))/(sigmaP)) + (sigmaP*0.5)
d2 = d1 - sigmaP
c = POB*norm.cdf(d1) - K*PO*norm.cdf(d2)  # call
p = PO*K*norm.cdf(-d2) - POB*norm.cdf(-d1)  # put
print('Price of the European Call =',c)



