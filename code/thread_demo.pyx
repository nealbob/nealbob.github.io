#cython: boundscheck=False, wraparound=False, nonecheck=False

from cython.parallel import prange
import numpy as np
from math import exp
from libc.math cimport exp as c_exp

cdef extern from "vfastexp.h":
    double c_exp_approx "EXP" (double)

cdef extern from "fastonebigheader.h":
    double c_exp_approx2 "fastexp" (double)

cdef inline double rbf(double r, double theta):

    return c_exp(-(r * theta)**2)

def rbf_network_multi(double[:, :] X, double[:] beta, double theta):

    cdef int N = X.shape[0]
    cdef int D = X.shape[1]
    cdef double[:] Y = np.zeros(N)
    cdef int i, j, d
    cdef double r = 0

    for i in prange(N, nogil=True):
        for j in range(N):
            r = 0
            for d in range(D):
                r += (X[j, d] - X[i, d])**2 
            r = r**0.5
            Y[i] += beta[j] * c_exp(-(r * theta)**2)

    return np.array(Y)

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
                r += (X[j, d] - X[i, d])**2 
            r = r**0.5
            Y[i] += beta[j] * c_exp(-(r * theta)**2)

    return np.array(Y)

def c_array_f_multi(double[:] X):

    cdef int N = X.shape[0]
    cdef double[:] Y = np.zeros(N)
    cdef int i

    for i in prange(N, nogil=True):
        if X[i] > 0.5:
            Y[i] = c_exp(X[i])
        else:
            Y[i] = 0

    return Y

cdef inline double f(double X) nogil:
    if X > 0.5:
        return c_exp(X)
    else:
        return 0

def c_array_f_multithread2(double[:] X):

    cdef int N = X.shape[0]
    cdef double[:] Y = np.zeros(N)
    cdef int i

    for i in prange(N, nogil=True):
        Y[i] = f(X[i])
    return Y

def c_array_f_multi_sum(double[:] X):

    cdef int N = X.shape[0]
    cdef double Ysum = 0
    cdef int i

    for i in prange(N, nogil=True):
        Ysum += f(X[i])
    return Ysum

def c_array_f(double[:] X):

    cdef int N = X.shape[0]
    cdef double[:] Y = np.zeros(N)
    cdef int i

    for i in range(N):
        if X[i] > 0.5:
            Y[i] = c_exp(X[i])
        else:
            Y[i] = 0

    return Y

def array_f(X):
    
    Y = np.zeros(X.shape)
    
    index = X > 0.5
    Y[index] = np.exp(X[index])

    return Y

def array_f_sum(X):
    
    Y = np.zeros(X.shape)
    
    index = X > 0.5
    Y[index] = np.exp(X[index])

    return np.sum(Y)
