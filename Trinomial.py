# Trinomial tree to calculate values for Call and Put European options.
# Written by: Michal Lyskawinski
# 10/31/2016
from math import *

# Initialize parameters
S = 150
r = 0.06
sig = 0.3
T = 1
K = 150
N = 3

div = 0.03  # In percentage
dx = 0.2
option = 'Call'

edx = exp(dx)

#  Compute asset prices at maturity
St = [0 for i in range(2*N+1)]
St[0] = S*exp(-N*dx)
for j in range(1, 2*N+1):
    St[j] = St[j - 1] * edx

#  Compute option values at maturity
C = [[0 for i in range(2*N+1)] for j in range(N+1)]
for j in range(0, 2*N+1):
    if option == 'Call':
        C[N][j] = max(0, St[j]-K)
    elif option == 'Put':
        C[N][j] = max(0, K - St[j])


#  Stepping backwards in time
dt = T/N
disc = exp(-r*dt)
nu = r-div-0.5*sig**2
pu = 0.5*(((sig**2*dt+nu**2*dt**2)/(dx**2))+nu*dt/dx)
pm = 1 - ((sig**2*dt+nu**2*dt**2)/dx**2)
pd = 0.5*(((sig**2*dt+nu**2*dt**2)/dx**2) - nu*dt/dx)
TNar = 0
for i in range(N-1,-1,-1):
    for j in range(TNar,2*N-TNar):
        C[i][j] = disc * (pu * C[i+1][j + 1] + pm * C[i + 1][j] + pd * C[i + 1][j - 1])
        #C[i][j] = disc * (pu * C[i][j + 1] + pm * C[i + 1][j + 1] + pd * C[i + 1][j -1])
print(C)
print(C[0][3])