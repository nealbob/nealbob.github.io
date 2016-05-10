---
layout: post
title: Machine learning for ~~dummies~~ economists
excerpt: "A simplistic introduction to machine learning"
modified: 2014-10-24
tags: [Machine learning, econometrics]
comments: true
---

In a recent article Hal Varian had this to say about machine learning:

>I believe that these methods have a lot to offer and should be more widely known and used by economists.  In fact, my standard advice to graduate students these days is: go to the computer science department and take a class in machine learning.

So what is machine learning? Machine learning (ML) is a sub-field of computer science concerned with algorithms that 'learn' from data. ML has its origins in artificial intelligence (AI). The basic goal of ML is to enable computers to make good predictions or decisions on the basis of observed data, without relying on human instructions. 

So what does all this have to do with economics? Well ML is also closely related to statistics. In fact, a large branch of ML (known as supervised learning) is concerned with regression problems. Another part of ML (known as reinforcement learning) is concerned with optimal behaviour in stochastic environments. Two things economists are big fans of. 

# Machine learning in action

Machine learning is everywhere. Whenever an app or a web site does something that seems a little too 'clever' or too like 'magic' its probably machine learning. A good example is google photos. Lying behind google photos are some high end ML algorithms that can interpret photos. So you upload some photos off your camera (with no identifying text or file names) and google photos can tell what's in them: allowing you to search your library.




So how do you get a computer to see images. While the specific algorithm is rather complicated, the basic idea is simple: its just a big regression problem. You take a large database of images each with labels (provided by a human). This is the training data: an X matrix containing photo data and vector Y containing labels. Then once you have the function f, you can use it to predict the contents of other unlabeled images.

# Supervised learning versus econometrics

Supervised learning involves a very different approach to regression than econometrics  (for a detailed comparison read Leo Brieman's "Statistical modelling: the two cultures", seriously its awesome).

Econometrics
------------

With econometrics we begin by inventing a statistical model, often something like this:

Once we have a model we can estimate the parameters by optimisation (i.e., OLS). Of course the problem is how do you pick the right model?. In economics we don't tend to have much to go on, so we just 'make it up'.  Invariably the model will be wrong: its just a matter of how much. 

Econometrics
------------

 

# Processes in Python



# Threads in Cython 



