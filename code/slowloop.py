# Demonstration of using cython to evaluate a radial basis function network
#
# Neal Hughes

import numpy as np
from math import exp


def rbf_network(X, c, beta, theta):

    N = X.shape[0]
    M = c.shape[0]
    D = X.shape[1]
    Y = np.zeros(N)

    for i in range(N):
        for j in range(M):
            r = 0
            for d in range(D):
                r += (c[j, d] - X[i, d]) ** 2
            Y[i] += beta[j] * exp(-(r * theta)**2)

    return Y

D = 5
N = 200000
M = 100
X = np.array([np.random.rand(N) for d in range(D)]).T
c = np.array([np.random.rand(M) for d in range(D)]).T
beta = np.random.rand(M)
theta = 10

%timeit rbf_network(X, c, beta, theta)

from scipy.interpolate import Rbf

ctuple = tuple([c[:, i] for i in range(D)])
Xtuple = tuple([X[:, i] for i in range(D)])

rbf = Rbf(ctuple, np.random.rand(M))

%timeit rbf(Xtuple)

from fastloop import rbf_network

%timeit rbf_network(X, c, beta, theta)

