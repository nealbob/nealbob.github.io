---
layout: page
title: Code
tags: [about]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
---
As an economist I'm a bit of a frustrated engineer and computer programmer. 

For my thesis I've learnt to code in Python. [John Stachurski](http://johnstachurski.net/) and Thomas Sargent's [quant-econ](http://quant-econ.net/) site provides a great introduction to Python for economists. Python is a joy to use, but it's a bit slow. Here I rely on [Cython](http://cython.org/) which is basically a Python to C translator, see [this post]({% post_url 2014-10-30-cython1 %}).

Recently I've been working on adapting some machine learning methods to economic problems...

econlearn
---------

``econlearn`` is a python [machine learning](http://en.wikipedia.org/wiki/Machine_learning) toolkit I developed as part of my thesis. `econlearn` provides some [reinforcement learning](http://en.wikipedia.org/wiki/Reinforcement_learning) (i.e., approximate dynamic programming) and [supervised learning](http://en.wikipedia.org/wiki/Supervised_learning) (i.e., non-parametric regression) algorithms suited to economic problems. That is noisy problems, requiring large sample sizes, but involving relatively few dimensions. In particular, it implements a batch version of [Q-learning](http://en.wikipedia.org/wiki/Q-learning) using [tilecoding](http://en.wikipedia.org/wiki/Cerebellar_Model_Articulation_Controller) for function approximation. 

All the code for my thesis is available on [github](https://github.com/nealbob/regrivermod). Eventually, I will create a standalone version of ``econlearn`` with documentation so that it can easily be used by others (I promise).
