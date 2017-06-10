
from math import *

# Initialize parameters
S = 150
r = 0.06
sigma = 0.3
T = 1
K = 150
N = 100
option = 'Put'

def american(S,r,sigma,T,K,N,option):
    dt = T/N
    u = exp(sigma * sqrt(dt))
    d = 1/u
    p = (exp(r*dt)-d)/(u-d)
    disc = exp(-r*dt)

    St = [0]*(N+1)
    C = [0]*(N+1)

    St[0] = S*d**N
    for j in range(1, N):
        St[j] = St[j-1]*(u/d)

    for j in range(0, N):
        if option == 'Put':
            C[j] = max(0.0, K - St[j])
        elif option == 'Call':
            C[j] = max(0.0, St[j] - K)
        else:
            break

    for i in range(N-1, 0):
        for j in range(0, i):
            C[j] = disc*(p*C[j+1]+(1-p)*C[j])
            St[j] = (St[j])/d
            if option == 'Put':
                C[j] = max(C[j], K - St[j])
            elif option == 'Call':
                C[j] = max(C[j], St[j] - K)
            next(j)
        next(i)
    if option =='Call':
        return C[52]
    elif option =='Put':
        return C[0]

print(american(S,r,sigma,T,K,N,option))