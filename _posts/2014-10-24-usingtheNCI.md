---
layout: post
title: How to use the ANU supercomputer
excerpt: "Everything I've learnt so far about how to use the NCI"
modified: 2014-10-24
tags: [NCI, ANU, Python]
comments: true
---

Here's what Ive learnt so far trying to get my code running on the ANUs [National Computing Infrastructure](nci.org.au). The NCI website provides a lot information on all of this (see the [raijin user guide](http://nci.org.au/services-support/getting-help/raijin-user-guide/)), but I've found it can be a bit opaque and incomplete. Luckily the help desk staff are very responsive if you ever get stuck (help@nf.nci.org.au).

# What is the NCI?

The NCI houses raijin a 60,000 CPU core supercomputer - the largest in the Southern hemisphere. Its located at the ANU a short walk from the Crawford School. 

# Applying for time on rajin

For ANU Phds the first step is applying for a startup grant. This is a small allocation of time (1000 core hours) to do do initial testing: learn how to use the system and give you an idea of how many core hours you will need for you main application.

To apply go here, you need to fill in the form and get your supervisor to sign (technically the application comes from them not you) then email it to the help desk (or just walk it over its not that far!). The application process was a bit confusing at times, but a few emails to the help desk got it done.

Full applications open in November for computing time the next year, the form is here. The minimum computing time request on raijin is 20,000 core hours, which is fairly large: equivalent to about 4000 hours or 20 weeks time on an i7 desktop or around $5000 worth on a commercial service like [multyvac](. 

# Logging in

Once you are approved you will receive a username via email and a temporary password via sms.

You login via ssh (if your on windows or mac you will need an ssh client, see the [user guide](http://nci.org.au/services-support/getting-help/raijin-user-guide/)), on linux just type 

    ssh -l username raijin.nci.org.au

You'll get a warning about connecting for the first time, just type yes, then enter your password and your in

# First steps

So now you are in a command line linux environment on a single raijin node (with 16 cores).  Each users gets there own profile to modify: install your code and any dependencies, store results etc. Any changes you make here will be stored when you log out. Your profile is located on the system at /home/username.

First lets reset our password

    passwd

Next we can check our account status


So we can see our 1000 hour allocation is still intact, plus nearly 100GB in storage. Note that these interactive sessions don't count towards your quota.

# Installing software

raijin has just about all the software you might need already installed (see the list ). You just need to make it available to your profile with the `module` command. To install Python (with numpy, scipy and matplotlib) you type


To use Cython I also needed to replace the default intel C compiler with gcc

You can then add these commands to your .profile file, to make sure they are executed on login.

I used vim to edit these text files

vim .profile

# Installing your code and dependencies

An easy way to load your code is via github (which is like dropbox for code). If you have your code in a git hub repository, you can clone it directly onto your profile.


Too easy. I also need to compile my code, which once I installed gcc worked just like it does on my local machine. 

Next I needed to install a number of other Python packages not included on raijin by default (cython, pandas, scikit-learn). First create a folder to hold them


Now raijin doesn't have `pip` but it does have `easy_install`. You just need to tell `easy_install` to install locally, for example

Next you need to add ~\packages to your PYTHONPATH so Python can find it

Its best to make this permanent by adding it to your .bashrc file.

So now I have two directories in my profile `Model` and `packages`.

# Running jobs

Just to check that it works I can run my code interactively 


Horah it works! To run larger jobs across multiple nodes we need to use the PBS job scheduling system (I haven't tried this yet).


