from math import *
from scipy.stats import norm
import openpyxl

# Opening the data file
wb = openpyxl.load_workbook('Data2.xlsx')
sheet1 = wb.get_sheet_by_name('SPY1118')

# Initializing arrays for variables
K = [0]*500  # Array of strike prices
BS = [0]*500  # Array of BSM prices
EU = [0]*500
AM = [0]*500


# Initializing constants:

T = (24/365)  # Time to maturity
S = 214.95  # Underlying asset price
r = 0.4  # interest rate
tol = 10**-6  # tolerance
A = 107  # starting row in excel
sigma = 0.3 # Implied volatility   Call
N = 100
option = 'Put'

# Calculating option value using BSM:
def CBS(S, K, T, r, sigma, option):
    # Calculations for the solution to BSM equation
    dplus = (1 / (sigma * sqrt(T))) * ((log(S / K)) + (r + (sigma ** 2) / 2) * T)
    dminus = (1 / (sigma * sqrt(T))) * ((log(S / K)) + (r - (sigma ** 2) / 2) * T)

    # Calculating price of Call and Put
    if option == 'Call':
        return S * norm.cdf(dplus) - K * exp(-r * T) * norm.cdf(dminus)
    elif option == 'Put':
        return K * exp(-r * T) * norm.cdf(-dminus) - S * norm.cdf(-dplus)

# Calculating option value using binomial for european:
def euro(S, r, sigma, K, N, option):
            # Compute more constants
            v = r - 0.5 * sigma ** 2
            deltaT = T / N
            disc = exp(-r * deltaT)
            dxu = sqrt((sigma ** 2) * deltaT + (v * deltaT) ** 2)
            dxd = -dxu
            #  p = (exp(r*deltaT)-d)/(u-d) # probability of going up
            pu = 0.5 + 0.5 * ((v * deltaT) / dxu)
            pd = 1 - pu

            # Initialize arrays
            St = [0] * (N + 1)
            C = [0] * (N + 1)

            # Initialize asset prices at maturity N
            St[0] = S * exp(N * dxd)
            for j in range(1, N):
                St[j] = St[j - 1] * exp(dxu - dxd)

            # Initialize option values at maturity
            for j in range(0, N):
                if option == 'Call':
                    C[j] = max(0.0, St[j] - K)
                elif option == 'Put':
                    C[j] = max(0.0, K - St[j])

            # Step back through the tree
            for i in range(N - 1, 0):
                for j in range(0, i):
                    C[j] = disc * (pu * C[j + 1] + pd * C[j])
            if option == 'Call':
                return C[51]
            elif option == 'Put':
                return C[0]

def american(S, r, sigma, T, K, N, option):
    dt = T / N
    u = exp(sigma * sqrt(dt))
    d = 1 / u
    p = (exp(r * dt) - d) / (u - d)
    disc = exp(-r * dt)

    St = [0] * (N + 1)
    C = [0] * (N + 1)

    St[0] = S * d ** N
    for j in range(1, N):
        St[j] = St[j - 1] * (u / d)

    for j in range(0, N):
        if option == 'Put':
            C[j] = max(0.0, K - St[j])
        elif option == 'Call':
            C[j] = max(0.0, St[j] - K)
        else:
            break

    for i in range(N - 1, 0):
        for j in range(0, i):
            C[j] = disc * (p * C[j + 1] + (1 - p) * C[j])
            St[j] = (St[j]) / d
            if option == 'Put':
                C[j] = max(C[j], K - St[j])
            elif option == 'Call':
                C[j] = max(C[j], St[j] - K)
            next(j)
        next(i)
    if option == 'Call':
        return C[52]
    elif option == 'Put':
        return C[0]


## Calculating option value using Binomial Theorem:

# Loop for finding values for each row
while A < 211:
    A=A+1

    K[A] = float(sheet1.cell(row=(A), column=1).value)
    BS[A]= CBS(S,K[A],T,r,sigma,option)
    EU[A]= euro(S, r, sigma, K[A], N, option)
    AM[A]= american(S, r, sigma, T, K[A], N, option)


print(BS)
print(EU)
print(AM)

