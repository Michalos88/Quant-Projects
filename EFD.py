# Explicit Finite Difference method to calculate values for Call and Put European options.
# Written by: Michal Lyskawinski
# 10/31/2016
from math import *
import numpy as np

S = 100
r = 0.06
sig = 0.2
T = 1
K = 100
N = 3
Nj = 3
div = 0.03  # In percentage
dx = 0.2
option = 'Call'

# Precompute constants
nu = r - div - 0.5 * (sig ** 2)
dt=T/N
edx = exp(dx)
pu = 0.5 * dt * ((sig / dx) ** 2 + nu / dx)
pm = 1.0 - dt * (sig / dx) ** 2 - r * dt
pd = 0.5 * dt * ((sig / dx) ** 2 - nu / dx)

# Initialise arrays
St = []
C = []

# Initialise asset prices at maturity
S0= float (S*(exp(N*dx)))
St.append(S0)
for j in range (1,2*N+1):
    Sa = St[j-1]/edx
    St.append(Sa)

# Initialise option values at maturity
for j in range (0,2*N+1):
    if option == 'Call':
        Max = max(0,St[j] - K)
        C.append(Max)
    elif option == 'Put':
        Max = max(0, K-St[j])
        C.append(Max)

# Initialise payoff matrix
P = np.zeros(shape=((2*N)+1,(1*N)+1))
for i in range (0,2*N+1):
    P[i,N] = C[i]

# Step back through lattice
for i in range (N-1,-1, -1):
    for j in range (N-i,(2*N)):
        P[j,i]= (pu*P[j+1,i+1]+pm*P[j,i+1]+pd*P[j-1,i+1])

    # Boundary conditions:
    for j in range (N-i-1,-1,-1):
        P[j,i]= P[j+1,i] + St[j] - St[j+1]

    for j in range (2*N,2*N-1,-1):
        P[j,i]= P[j-1,i]


print(P)
print('The value of European',option,'option is',P[int(N),0])



