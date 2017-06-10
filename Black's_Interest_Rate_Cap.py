# Michal Lyskawinski
# Date: 11/28/2016
# Black's Model
# Price an interest rate cap at 4.7%. Assume that the cap is for a
# two year period, the reset frequency is four months. Assume that
# the volatility of the forward rate is 9%. The principal of the swap
# is 1 million (you may want to use software for this). Please note
# that a caplet and a cap are two different things.

from math import exp, log, sqrt
from scipy.stats import norm

# General Parameters
r = 0.04  # Flat term structure

# Parameters for option
L = 1*10**6  # Principal
rc = 0.047  # Cap rate
fr = 4  # Reset frequency in months
VFIR = 0.09  # Volatility of future interest rate
M = 24  # Maturity in months

# Precompute constants
dt = 1/M


def PDBprice(r,M):
    P = exp(-r*M)
    return P

Ccap = []

for i in range(1,int(M/fr)):
    m2 = (i+1)*fr*dt
    m1 = i*fr*dt
    Opdb = PDBprice(r, m1)
    d1 = (1 / (VFIR * sqrt(m1))) * ((log(r / rc)) + ((VFIR ** 2) / 2) * m1)
    d2 = d1 - VFIR * sqrt(m1)
    Ccaplet = Opdb*(r*norm.cdf(d1) - rc*norm.cdf(d2))*dt*L
    Ccap.append(Ccaplet)

C = sum(Ccap)
print(C)

# We assume for our analysis that there is no caplet over the first cap period as the interest rate applicable to the period is known at time t0