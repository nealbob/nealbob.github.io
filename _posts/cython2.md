---
layout: post
title: Fast simulation models in Cython
excerpt: "A simple example showing some more advanced Cython techniques"
modified: 2014-10-24
tags: [Python, Cython, multiprocessing, OpenMP]
comments: true
---

One of the great things about Cython is its ability to handle large complex pieces of code.  Within Cython we can easily define nested class and function definitions without returning to Python. Cython then presents an alternative to fast object orientate languages like C++ or Java for coding large complex simulation models.

Below we show how to simulate a stochastic consumption-saving model in Cython. While this is a contrived example hopefully it shows how Cython's object orientated syntax could be used to code more complex models, such as those encountered in agent based computational economics.

# A consumption saving model

Consider a simple one sector stochastic consumption-production-saving model

<div>$$  max_{\{c_t\}_{t=0}^\infty} E[\sum_{t=0}^\infty \beta^tU(c_t)]  $$</div>
subject to
<div>$$  k_{t+1} = (1- \delta)k_t - c_t + \z_t k_t^{alpha} $$</div>
<div>$$  z_{t+1} = \rho z_t + \epsilon_{t+1} $$</div>
<div>$$  \epsilon_{t+1} \sim N(0, \sigma^2) $$</div>
<div>$$  U(c_t) = {c_t^{1 - \phi} \over  1 - \phi} $$</div>


Within Python, multiple processes can be managed the `multiprocessing` module.  Python doesn't allow for threading based parallelization, due to the Global Interpreter Lock (GIL). However, multi-threading can be achieved with Cython via OpenMP (a threading platform for C). 

# Processes in Python



# Threads in Cython 



