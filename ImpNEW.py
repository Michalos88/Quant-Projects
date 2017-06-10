# Implicit Finite Difference method to calculate values for Call and Put European options.
# Written by: Michal Lyskawinski
# 10/31/2016

from math import *

# Initialize parameters
K = 100
S = 100
r = 0.06
sig = 0.2
T = 1
N = 3
Nj = 3
div = 0.03  # In percentage
dx = 0.2
option = 'Call'

# Precompute constants
dt = T/N
nu = r - div - 0.5*(sig**2)
edx = exp(dx)
pu = 0.5*dt*((sig/dx)**2 + nu/dx)
pm = 1.0 - dt*(sig/dx)**2 - r*dt
pd = 0.5*dt*((sig/dx)**2 - nu/dx)


# print("dt=",dt)
# print("nu=",nu)
# print("edx=",edx)
# print("pu=",pu)
# print("pm=",pm)
# print("pd=",pd)

#Initialise arrays for asset prices(St) and option values(C)
St = [0 for i in range(2*Nj+1)]
C = [[0 for i in range(2*Nj+1)] for j in range(N+1)]


# Initialize asset prices at maturity
St[0] = S*exp(-Nj*dx)
for j in range(1, 2*Nj+1):
    St[j] = St[j-1]*edx

# Initialize option values at maturity
for j in range(0,2*Nj+1):
    if option == 'Call':
        C[0][j] = max(0, St[j] - K)
    elif option == 'Put':
        C[0][j] = max(0, K - St[j])
    else:
        break

# Compute derivative BC's
if option == 'Call':
    lambdaL = 0.0
    lambdaU = St[1] - St[0]
elif option == 'Put':
    lambdaL = -1*(St[1]-St[0])
    lambdaU = 0.0

def solve_implicit_tridiagonal_system(C,pu,pm,pd,lambdaL,lambdaU):
    # Substituting BC's at j=0 in j=1
    pmp = [0 for i in range(2 * Nj)]
    pp = [0 for i in range(2 * Nj)]
    pmp[1] = pm + pd
    pp[1] = C[0][1] + pd * lambdaL

    # eliminating upper diagonal
    for j in range(2, 2 * Nj+1-1):
        pmp[j] = pm - pu * pd / pmp[j - 1]
        pp[j] = C[0][j] - pp[j - 1] * pd / pmp[j - 1]

    # Using other BC's
    C[1][2 * Nj] = (pp[2 * Nj - 1] + pmp[2 * Nj - 1] * lambdaU) / (pu + pmp[2 * Nj - 1])
    C[1][2 * Nj - 1] = C[1][2 * Nj] - lambdaU

    # Back - substitution
    for j in range(2 * Nj+1-2, 0, -1):
        C[1][j] = (pp[j] - pu * C[1][j + 1]) / pmp[j]

    return


for i in range(2*N+1-1,Nj,-1):
    solve_implicit_tridiagonal_system(C,pu,pm,pd,lambdaL,lambdaU)
    # In case of american:
    for j in range(0,2*Nj+1):
        # if option == 'Call':
        #    C[0][j] = max(C[1][j],St[j] - K)
        # elif option == 'Put':
        #    C[0][j] = max(C[1][j],K - St[j])
     C[0][j] = C[1][j]


print(C)
print(C[0][Nj])






# Nj = 2Nj for array, 2Nj +1 for range
# -Nj = 0
# 0 = (if exen 6/2 =3 , if odd 7/2 = 3.5 + 0.5





