# Demonstration of using cython to evaluate a radial basis function network
#
# Neal Hughes

import numpy as np
from math import exp

def rbf_network(X, beta, theta):

    N = X.shape[0]
    D = X.shape[1]
    Y = np.zeros(N)

    for i in range(N):
        for j in range(N):
            r = 0
            for d in range(D):
                r += (X[j, d] - X[i, d]) ** 2
            r = r**0.5
            Y[i] += beta[j] * exp(-(r * theta)**2)

    return Y

D = 5
N = 1000
X = np.array([np.random.rand(N) for d in range(D)]).T
beta = np.random.rand(N)
theta = 10

%timeit rbf_network(X, beta, theta)
"""
from scipy.interpolate import Rbf

Xtuple = tuple([X[:, i] for i in range(D)])

rbf = Rbf(X[:,0], X[:,1], X[:,2], X[:,3], X[:, 4], np.random.rand(N))

%timeit rbf(Xtuple)

from fastloop import rbf_network as rbf_fast

%timeit rbf_fast(X, beta, theta)
"""
