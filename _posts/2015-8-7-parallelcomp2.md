---
layout: post
title: Parallel computing in Cython - threads
excerpt: "How to run multiple threads in Cython"
modified: 2015-8-7
tags: [Cython, Python, prange, thread, OpenMP]
comments: true
---

One of the cool things about [Cython]({% post_url 2014-10-30-cython1 %}) is that it supports multi-threaded code, via the C library [OpenMP](https://en.wikipedia.org/wiki/OpenMP). 

While Python allows for message passing (i.e., multiple processes) shared memory (i.e., multi-threading) is not possible due to the [Global Interpreter Lock](https://en.wikipedia.org/wiki/Global_Interpreter_Lock) (see this [earlier post]({% post_url 2014-12-5-parallelcomp %})). 
 
Relative to message passing, multi-threading is fast (and has lower memory requirements). The catch is that you can run into concurrency problems: where the different threads need to access the same memory locations at the same time.  As such, multi-threading is best suited to performing large numbers of simple calculations. In particular, where the order in which the calculations are executed doesn't matter.  

# A simple Cython example

The perfect use case is applying a function element wise over a large array. Lets say we want to apply the function \\( f\\) below to some array \\( X\\) 


<div>$$  f(x) = \begin{cases} e^x & \mbox{if } x > 0.5 \\
         0 & \mbox{if } otherwise \end{cases} $$</div>

Below I have a Python version and a Cython version of \\( f\\) in the file thread_demo.pyx

{% highlight cython %}
import numpy as np
from math import exp 
from libc.math cimport exp as c_exp

def array_f(X):
    
    Y = np.zeros(X.shape)
    index = X > 0.5
    Y[index] = np.exp(X[index])

    return Y

def c_array_f(double[:] X):

    cdef int N = X.shape[0]
    cdef double[:] Y = np.zeros(N)
    cdef int i

    for i in range(N):
            if X[i,j] > 0.5:
                Y[i,j] = c_exp(X[i,j])
            else:
                Y[i,j] = 0

    return Y
{% endhighlight %}

Next we compile this file with a standard `setup.py` (like we did [here]({% post_url 2014-10-30-cython1 %})). Now lets test these functions in IPython:

{% highlight python %}
from thread_demo import *
X = -1 + 2*np.random.rand(10000000) 
%timeit array_f(X)
1 loops, best of 3: 222 ms per loop
%timeit c_array_f(X)
10 loops, best of 3: 87.5 ms per loop
{% endhighlight %}

In this case, the Cython version is not dramatically faster than Python, because our function is simple enough to 'vectorise' via `numpy`. 

Now to create a multi-threaded version of `c_array_f` we just need to replace `range()` in the loop with the multi-treaded version `prange()` from `cython.parallel`:

{% highlight cython %}
from cython.parallel import prange

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
{% endhighlight %}

Too easy. This tells the compiler to run the loop across multiple CPU cores. In this case, we have no concurrency problems: the order in which the loop is executed doesn't matter. Now we just need to make a few changes to our `setup.py` file, in order to compile our code with the OpemMP:

{% highlight python %}
from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules=[
    Extension("thread_demo",
              ["thread_demo.pyx"],
              libraries=["m"],
              extra_compile_args = ["-O3", "-ffast-math", "-march=native", "-fopenmp" ],
              extra_link_args=['-fopenmp']
              ) 
]

setup( 
  name = "thread_demo",
  cmdclass = {"build_ext": build_ext},
  ext_modules = ext_modules
)
{% endhighlight %}

Now lets give it a go

{% highlight python %}
%timeit c_array_f_multi(X)
10 loops, best of 3: 22.4 ms per loop
{% endhighlight %}

So with four cores we get just under a 4 times speed up.  

# A few more details

Now so far I've glossed over many important details. Here are some basic things to consider (for a full explanation see the [documentation](http://docs.cython.org/src/userguide/parallelism.html)

Firstly, notice the `nogil` argument in `prange(N, nogil=True)`. In order to run multi-threaded code we need to turn off the GIL. This means that you can't have Python code inside your multi-threaded loop, or compilation will fail. It also means that any functions called inside the loop need to be defined nogil, for example:

{% highlight cython %}
cdef inline double f(double X) nogil:
    if X > 0.5:
        return c_exp(X)
    else:
        return 0

def c_array_f_multi(double[:] X):

    cdef int N = X.shape[0]
    cdef double[:] Y = np.zeros(N)
    cdef int i

    for i in prange(N, nogil=True):
        Y[i] = f(X[i])
    return Y
{% endhighlight %}

`prange()` takes a few other arguments including `num_threads`, which will default to the number of cores on your system. Then there is the `schedule` argument which has to do with load balancing. The simplest option here is 'static' which just breaks the loop into equal chunks. This is fine if all steps in the loop compute in around the same time, if not one thread may finish before the others leaving resources idle. In this case, you might try 'dynamic' (see the [docs](http://docs.cython.org/src/userguide/parallelism.html) for detail).

The other key issue is how your variables are handled in memory: that is, which variables are shared between threads and which are private or local. With multi-threading this can very quickly get complex. The good thing with Cython is that all of this detail is - in true Python style - magically inferred from your code. 

The basic idea is that variables that are only read are shared, while variables assigned to are thread private. An important special case are 'reduction' variables. `cython.parallel` will take any variable with an in-place operator (i.e., `+=') as a reduction, which means that the thread local values are combined after all threads have completed to give you a final value. This is useful if you need to compute a sum:

{% highlight cython %}
 def c_array_f_multi_sum(double[:] X):

    cdef int N = X.shape[0]
    cdef double Ysum = 0
    cdef int i

    for i in prange(N, nogil=True):
        Ysum += f(X[i])
    return Ysum

def array_f_sum(X):
    
    Y = np.zeros(X.shape)
    
    index = X > 0.5
    Y[index] = np.exp(X[index])

    return np.sum(Y)
{% endhighlight %}


{% highlight python %}
from thread_demo import *
X = -1 + 2*np.random.rand(10000000) 
array_f_sum(X)
5349424.6891543046
c_array_f_multi_sum(X)
5349424.689154312
{% endhighlight %}

This gives us the correct answer. Note that if we instead put `Ysum = Ysum + f(X[i])` we would have got a compiler error.

# Radial Basis Function (RBF) example 

Recall the problem of evaluating a RBF approximation scheme from this [post]({% post_url 2014-10-30-cython1 %}), well here is a multi-threaded version:

{% highlight cython %}
def rbf_network_multithread(double[:, :] X,  double[:] beta, double theta):

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

    return Y
{% endhighlight %}

{% highlight python %}
D = 5
N = 1000
X = np.array([np.random.rand(N) for d in range(D)]).T
beta = np.random.rand(N)
theta = 10
%timeit rbf_network(X, beta, theta)
10 loops, best of 3: 45.2 ms per loop
%timeit rbf_network_multi(X, beta, theta)
100 loops, best of 3: 8.67 ms per loop
{% endhighlight %}

For some reason this achieves a better than 4 times speed up!

# Bottom line

Of course, the real challenge is in identifying / producing code segments that are suited to multi-threading. In many cases, blindly running a loop in parallel will either fail or lead to a decrease in performance if the threads get in each others way.  But for simple applications at least, running multiple threads in Cython is as simple as adding `prange()` to your loops.  
