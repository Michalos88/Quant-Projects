from math import *


# Initialize parameters
S = 214.95
r = 0.06
sigma = 0.37
T = (20/365)
N = 100
option = 'Call'

def euro(S,r,sigma,K,N,option):
    # Compute more constants
    v = r-0.5*sigma**2
    deltaT = T/N
    disc = exp(-r*deltaT)
    dxu = sqrt((sigma**2)*deltaT+(v*deltaT)**2)
    dxd = -dxu
    #  p = (exp(r*deltaT)-d)/(u-d) # probability of going up
    pu = 0.5+0.5*((v*deltaT)/dxu)
    pd = 1-pu

    # Initialize arrays
    St = [0]*(N+1)
    C = [0]*(N+1)

    # Initialize asset prices at maturity N
    St[0] = S*exp(N*dxd)
    for j in range(1,N):
        St[j] = St[j-1]*exp(dxu-dxd)

    # Initialize option values at maturity
    for j in range(0, N):
        if option == 'Call':
            C[j] = max(0.0, St[j] - K)
        elif option == 'Put':
            C[j] = max(0.0, K - St[j])

    # Step back through the tree
    for i in range(N-1, 0):
        for j in range(0, i):
            C[j] = disc*(pu*C[j+1]+pd*C[j])
    if option == 'Call':
        return C[int(N/2)]
    elif option == 'Put':
        return C[int(N/2)]

Ks = [70,115,120,121,123,125,126,129,130,141]
for i in Ks:
    print('For K=',i,'OptionV =',euro(S,r,sigma,i,N,option))
