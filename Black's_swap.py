# Michal Lyskawinski
# Date: 11/28/2016
# Black's Model
# Price a one year option which exercise into a new two year semi-
# annual payer swap. The strike price of the option is 6% and the
# forward swap rate volatility is 10%.

from math import *
from scipy.stats import norm

# Parameters for option
K = 0.06  # Strike in %
r = 0.04  # Term structure of interest rate is flat at r
M1 = 1.00  # Maturity of the option in years

# Parameters for the swap
FSRvol = 0.1  # forward swap rate volatility
M3 = 3.00  # # Maturity of the swap
dt = 0.5  # Reset period

# Precompute Constants:
N = (M3-M1)/dt  # Number of reset periods of the swap


def PDBprice(r,M):
    P = exp(-r*M)
    return P

# Under our term structure assumptions the relevant bond prices are given
M1pdb = PDBprice(r,M1)
M3pdb = PDBprice(r,M3)

Mpdb = []
FBP = []  # forward bond prices
y = []
for i in range(1,int(N)):
    M = i*dt+M1
    pdb = PDBprice(r,M)
    Mpdb.append(pdb)
    FBP1 = pdb / M1pdb
    FBP.append(FBP1)


FBP2 = M3pdb/M1pdb

Rfswap = ((1-FBP2)/(sum(FBP)+FBP2))*2

d1 = (1 / (FSRvol * sqrt(M1))) * ((log(Rfswap / K)) + ((FSRvol ** 2) / 2) * M1)
d2 = d1 - FSRvol * sqrt(M1)

# for i in range(1,int(N)):
#     x = 1/((1+Rfswap)**N)
#     y.append(x)



C = dt*(sum(Mpdb)+M3pdb)*(Rfswap*norm.cdf(d1) - K*norm.cdf(d2))  # *(sum(y))

print(C)