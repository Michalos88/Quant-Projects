# Monte Carlo Valuation of a European Option in a Black-Scholes World
# With implementation of Antithetic and Delta-based control variate method
# by Michal Lyskawinski
# 10/31/2016

from math import *
import numpy as np
import random
from scipy.stats import norm

# Computation of Black-Scholes
def CBS(S, K, T, r, sigma,t, option):

    t2t = T-t # time to maturity
    # Calculations for the solution to BSM equation
    dplus = (1 / (sigma * sqrt(t2t))) * ((log(S / K)) + (r + ((sigma ** 2) / 2)) * t2t)
    dminus = (1 / (sigma * sqrt(t2t))) * ((log(S / K)) + (r - (sigma ** 2) / 2) * t2t)

    # Calculating price of Call and Put
    if option == 'Call':
        return S * norm.cdf(dplus) - K * exp(-r * t2t) * norm.cdf(dminus)
    elif option == 'Put':
        return K * exp(-r * t2t) * norm.cdf(-dminus) - S * norm.cdf(-dplus)


# Initialize parameters
S = 100
r = 0.06
sig = 0.2
T = 1
K = 100
N = 10
M = 100
div = 0.03  # In percentage
option = 'Put'

# Precompute constants
dt = T/N
nu = r - div - 0.5*(sig**2)
nudt = nu*dt
sigsdt = sig*sqrt(dt)
erddt = exp((r-div)*dt)
beta1 = -1

sum_CT = 0
sum_CT2 = 0

for j in range(1,M): # For each simulation
    St1 = S
    St2 = S
    cv1 = 0
    cv2 = 0

    for i in range(1,N): # For each time step
        t = (i - 1) * dt
        delta1 = CBS(St1, K, T, r, sig, t, option)
        delta2 = CBS(St2, K, T, r, sig, t, option)
        eps = np.random.normal(0, 1)
        Stn1 = St1 * exp(nudt + sigsdt * eps)
        Stn2 = St2 * exp(nudt + sigsdt * (-eps))
        cv1a = cv1 + delta1 * (Stn1 - St1 * erddt)
        cv2a = cv2 + delta2 * (Stn2 - St2 * erddt)
        St1 = Stn1
        St2 = Stn2

    if option == 'Call':
        CT = 0.5*(max(0, St1 - K) + beta1*cv1a + max(0, St2 - K) + beta1*cv2a)
        sum_CT = sum_CT + CT
        sum_CT2 = sum_CT2 + CT*CT
    elif option == 'Put':
        CT = 0.5*(max(0, K - St1) + beta1*cv1a + max(0, K - St2) + beta1*cv2a)
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





