---
layout: page
title: Code
tags: [about]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
---

I code mostly in Python, following the lead of [John Stachurski](http://johnstachurski.net/). His [quantecon](http://quant-econ.net/) site with Tom Sargent for a great introduction to Python for economists. <br> <br> Python is a joy to use, but it's a bit slow. Here I rely on [Cython](http://cython.org/), which is basically a Python to C translator. When I get a chance I will put up some posts, describing how I use Cython.

econlearn
---------

``econlearn`` is a python [machine learning](http://en.wikipedia.org/wiki/Machine_learning) toolkit I developed as part of my thesis. `econlearn` provides some [reinforcement learning](http://en.wikipedia.org/wiki/Reinforcement_learning) (i.e., approximate dynamic programming) and [supervised learning](http://en.wikipedia.org/wiki/Supervised_learning) (i.e., non-parametric regression) algorithms suited to economic problems. That is noisy problems, requiring large sample sizes, but involving relatively few dimensions. In particular, ``econlearn`` implements a batch version of [Q-learning](http://en.wikipedia.org/wiki/Q-learning) using [tilecoding](http://en.wikipedia.org/wiki/Cerebellar_Model_Articulation_Controller) for function approximation. <br> <br> All the code for my thesis is available on [github](https://github.com/nealbob/regrivermod). Eventually, I will create a standalone version of ``econlearn`` with documentation so that it can easily be used by others (I promise).
