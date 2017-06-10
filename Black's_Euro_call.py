# Michal Lyskawinski
# Date: 11/28/2016
# Black's Model
# Assume that the forward bond price volatility is 7%. Price a two
# year European call option with strike 0.8 on a seven-year pure
# discount bond.

from math import exp, log, sqrt
from scipy.stats import norm

# Parameters for option
OM = 2  # Maturity of the option in years
Or = 0.04  # Term structure of interest rate
K = 0.8  # Strike

# Parameters for the bond
Br = 0.04
BM = 7  # Maturity pure discount bond in years
FBPV = 0.07  # Forward bond price volatility

def PDBprice(r,M):
    P = exp(-r*M)
    return P

Bpdb = PDBprice(Br, BM)
Opdb = PDBprice(Or, OM)

Pf = Bpdb/Opdb

d1 = (1/(FBPV*sqrt(OM)))*((log(Pf/K))+((FBPV**2)/2)*OM)
d2 = d1 - FBPV*sqrt(OM)

C = Opdb*(Pf*norm.cdf(d1) - K*norm.cdf(d2))

print(C)
