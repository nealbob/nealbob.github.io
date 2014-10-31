#cython: boundscheck=False, wraparound=False, nonecheck=False

from cython.parallel import prange
import numpy as np
#from math import exp
from libc.math cimport exp as c_exp

cdef extern from "vfastexp.h":
    double c_exp_approx "EXP" (double)

cdef extern from "fastonebigheader.h":
    double c_exp_approx2 "fastexp" (double)

cdef inline double rbf(double r, double theta):

    return c_exp(-(r * theta)**2)


def rbf_network(double[:, :] X,  double[:] beta, double theta):

    cdef int N = X.shape[0]
    cdef int D = X.shape[1]
    cdef double[:] Y = np.zeros(N)
    cdef int i, j, d
    cdef double r = 0

    for i in range(N):
        for j in range(N):
            r = 0
            for d in range(D):
                r += (X[j, d] - X[i, d]) ** 2
            Y[i] += beta[j] * c_exp_approx(-(r * theta)**2)

    return Y
