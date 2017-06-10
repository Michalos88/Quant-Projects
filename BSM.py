#  Only using toolbox functions for normal CDF calculation and mathematical tools
from math import *
from scipy.stats import norm

# Input Parameters


sigma = 3

T = 0.5
S = 187.85
r = 0.05
K = 80
# Calculations for the solution to BSM equation
dplus = (1/(sigma*sqrt(T)))*((log(S/K))+(r+(sigma**2)/2)*T)
dminus = (1/(sigma*sqrt(T)))*((log(S/K))+(r-(sigma**2)/2)*T)

# Calculating price of Call and Put
Call = S*norm.cdf(dplus) - K*exp(-r*T)*norm.cdf(dminus)
Put = K*exp(-r*T)*norm.cdf(-dminus)-S*norm.cdf(-dplus)

# Printing the values of call an put options
print("The Price of the Call option is %s" % round(Call, 2))
print("The Price of the Put option is %s" % round(Put,  2))