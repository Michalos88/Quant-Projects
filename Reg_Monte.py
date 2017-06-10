# Monte Carlo Valuation of a European Option in a Black-Scholes World
# by Michal Lyskawinski
# 10/31/2016

from math import *
import numpy as np
# Initialize parameters
S = 100
r = 0.06
sig = 0.2
T = 1
K = 100
N = 300
M = 100
div = 0.03  # In percentage
option = 'Put'

# Precompute constants
dt = T/N
nu = r - div - 0.5*(sig**2)
nudt = nu*dt
sigsdt = sig*sqrt(dt)
lnS = log(S)

sum_CT = 0
sum_CT2 = 0

for j in range(1,M): # For each simulation
    lnST = lnS

    for i in range(1,N):
        eps = np.random.normal(0, 1)
        lnST = lnST + nudt + sigsdt*eps

    St = exp(lnST)
    if option == 'Call':
        CT = max(0, St - K)
        sum_CT = sum_CT + CT
        sum_CT2 = sum_CT2 + CT*CT
    elif option == 'Put':
        CT = max(0, K - St)
        sum_CT = sum_CT + CT
        sum_CT2 = sum_CT2 + CT * CT
    else:
        break


Value = sum_CT/M*exp(-r*T)
SD = sqrt((sum_CT2 - sum_CT*sum_CT/M)*exp(-2*r*T)/(M-1))
SE = SD/sqrt(M)


print('The Value of European',option,'Option is',Value)
print('The Standard Deviation of this Option is',SD)
print('The Standard Error in this case is',SE)





