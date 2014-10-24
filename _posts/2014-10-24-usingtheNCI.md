---
layout: post
title: How to use the ANU supercomputer
excerpt: "Everything I've learnt so far about how to use the NCI"
modified: 2014-10-24
tags: [NCI, ANU, Python]
comments: true
---

Here's what Ive learnt so far trying to get my code running on the ANUs [National Computing Infrastructure](http://nci.org.au). The NCI website provides a lot information on all of this (see the [raijin user guide](http://nci.org.au/services-support/getting-help/raijin-user-guide/)), but I've found it can be a bit opaque and incomplete. Luckily the help desk staff are very responsive if you ever get stuck (help@nf.nci.org.au).

# What is the NCI?

The NCI houses raijin a 60,000 CPU core supercomputer - the largest in the Southern hemisphere. Its located at the ANU a short walk from the Crawford School. 

<figure>
	<img src="http://nealbob.github.io/images/nci.jpg">
</figure>

# Applying for time on raijin

For ANU Phd students the first step is to apply for a startup grant. This is a small allocation of time (1000 core hours) to do do initial testing: learn how to use the system and give you an idea of how many core hours you will need for you main application. <br><br>

To apply go [here](http://nci.org.au/access/user-registration/application-form-resource/), fill in the form and get your supervisor to sign (technically the application comes from them not you) then email it to the help desk (or just walk it over its not that far!). The application process was a bit confusing at times, but a few emails to the help desk got it done. <br><br>

Full applications open in November for computing time the next year, the form is here. The minimum computing time request on raijin is 20,000 core hours, which is fairly large: equivalent to about 4000 hours or 20 weeks time on an i7 desktop or around $5000 worth on a commercial service like [multyvac](http://www.multyvac.com/). 

# Logging in

Once your'e approved you will receive a username via email and a temporary password via sms.

You login via ssh (if your on windows or mac you will need an ssh client, see the [user guide](http://nci.org.au/services-support/getting-help/raijin-user-guide/)), on linux just type 

    ssh -l username raijin.nci.org.au

You'll get a warning about connecting for the first time, just type yes, then enter your password and your in.


    ###############################################################################
    #                            NCI National Facility                            #
    #      This service is for authorised clients only. It is a criminal          #
    #      offence to:                                                            #
    #                - Obtain access to data without permission                   #
    #                - Damage, delete, alter or insert data without permission    #
    #      Use of this system requires acceptance of the Conditions of Use        #
    #      published at http://nci.org.au/conditions/                             #
    ###############################################################################
    |                  Welcome to the NCI National Facility!                      |
    |        raijin.nci.org.au - 57472 processor InfiniBand x86_64 cluster        |
    |     Assistance: help@nci.org.au     Information: http://nci.org.au          |
    ===============================================================================

# First steps

So now you are in a command line linux environment on a single raijin node (with 16 cores). You should have a prompt that looks like this

    [username@raijin4 ~]$

Each users gets there own profile to play with, here you can install your code and any dependencies and store your input and output files. Any changes you make here will be saved when you log out. Your profile is located on the system at /home/username.

First lets reset our password

    [username@raijin4 ~]$ passwd

Next we can check our account status

    [username@raijin4 ~]$ nci_account

    Usage Report: Project=fr3 Compute Period=2014.q4 (01/10/2014-31/12/2014)
    ========================================================================

    Total Grant: 1000.00 SU
    Total Used:   0.00 SU
    Total Avail: 1000.00 SU
    Bonus Used:   0.00 SU

    -------------------------------------------------------------------------------------------------------------
    System      Queue  Charge         Usage         Usage       SU used   Reserved SU    Pending SU      Total SU
                       Weight     (CPU Hrs)    (Walltime)                   (Running)      (Queued)     Committed
    raijin      copyq     1.0          0.00          0.00          0.00          0.00          0.00          0.00
    raijin    express     3.0          0.00          0.00          0.00          0.00          0.00          0.00
    raijin    hugemem     1.0          0.00          0.00          0.00          0.00          0.00          0.00
    raijin     normal     1.0          0.00          0.00          0.00          0.00          0.00          0.00
    -------------------------------------------------------------------------------------------------------------
    Overall                            0.00          0.00          0.00          0.00          0.00          0.00


    Usage Report: Project=fr3 Storage Period=2014.10 (01/10/2014-31/12/2014)
    ========================================================================
    -------------------------------------------------------------------------------------------------
    System    StoragePt             Grant       Usage       Avail      iGrant      iUsage      iAvail
    -------------------------------------------------------------------------------------------------
    dmf       massdata            20.00GB      0.00GB     20.00GB     100.00K       0.00K     100.00K
    raijin    short               72.00GB      0.00GB     72.00GB     164.00K       0.01K     163.99K
    -------------------------------------------------------------------------------------------------
    Total                         92.00GB      0.00GB     92.00GB     264.00K       0.01K     263.99K

So you should see your 1000 hour allocation, plus nearly 100GB in storage. Note that these interactive sessions don't count towards your quota.

# Installing software

raijin has just about all the software you might need already installed (see the [list](http://nci.org.au/nci-systems/national-facility/peak-system/raijin/application-software/)). You just need to make it available to your profile with the `module` command. To view the list of all software type

    module avail

To install Python (with `numpy`, `scipy` and `matplotlib`) you type

    module load python/2.7.3
    module load python/2.7.3-matplotlib

To use Cython I also needed to replace the default intel C compiler with gcc

    module unload intel-cc
    module load gcc/4.9.0

You can then add these commands to your `.profile` file, to make sure they are executed on login. I used vim to edit these text files

    vim .profile

# Installing your code and dependencies

An easy way to load your code is via [github](https://github.com) (which is like dropbox for code). Once you've learnt github, and have your code in a github repository [like this](https://github.com/nealbob/regrivermod), you can clone it directly onto your profile.

    git clone git://github.com/nealbob/regrivermod.git ~/Model

Too easy. I also needed to compile my code, which once I installed `gcc` worked just like it does on my local machine. 

Next I needed to install a number of other Python packages not included on raijin by default (cython, pandas, scikit-learn). First create a folder to hold them

    mkdir packages

For this I can use `easy_install`. You just need to tell `easy_install` to install locally, for example

    easy_install --install-dir=~/packages pandas

Next you need to add ~/packages to your PYTHONPATH environment variable so Python can find it

    export PYTHONPATH=~/packages:$PYTHONPATH

Its best to make this change permanent by adding it to your `.bashrc` file.

# Running jobs

Just to check that it works I can run my code interactively 

    [username@raijin4 ~]$ cd Model
    [username@raijin4 Model]$ python test.py

     --- Main parameters --- 

    Inflow to capacity: 0.708747484611
    Coefficient of variation: 0.7
    Proportion of high demand: 0.234622818122
    Target water price: 10.0
    Transaction cost: 55.0
    High user inflow share: 0.469245636245
    Land: 4833.896933
    High Land: 0.0655588606907

    Decentralised storage model with 100 users. 

    Solving the planner's problem...
    PI Iteration: 1, Error: 100.0, PE Iterations: 68
    PI Iteration: 2, Error: 0.0102, PE Iterations: 11
    PI Iteration: 3, Error: 0.0014, PE Iterations: 2
    PI Iteration: 4, Error: 0.001, PE Iterations: 1
    Solve time: 11.7644062042
    Running simulation for 500000 periods...
    Simulation time: 5.42
    Summary stats time 1.61270594597
    Data stacking time: 1.63947796822
    Storage mean: 698008.184127
    Inflow mean: 694593.226731
    Withdrawal mean: 520950.115529
    Welfare mean: 186576969.954

Horah it works! To run larger jobs across multiple nodes we need to use the PBS job scheduling system (I haven't tried this yet).


