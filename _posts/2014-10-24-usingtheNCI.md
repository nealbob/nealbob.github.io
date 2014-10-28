---
layout: post
title: How to use the ANU supercomputer
excerpt: "Everything I've learnt so far about how to use the NCI"
modified: 2014-10-24
tags: [NCI, ANU, Python]
comments: true
---

Here's what I've learnt so far trying to get my code running on ANU's [National Computational Infrastructure](http://nci.org.au). The NCI website provides a lot information on all of this (see the [raijin user guide](http://nci.org.au/services-support/getting-help/raijin-user-guide/)), but I've found it can be a bit opaque. Luckily the help desk staff are very responsive if you ever get stuck (help@nf.nci.org.au).

# What is the NCI?

The NCI houses raijin a 60,000 CPU core supercomputer - the largest in the Southern Hemisphere - and its located at the ANU next to South oval. 

<figure>
	<img src="http://nealbob.github.io/images/nci.jpg">
</figure>

# Applying for time on raijin

For ANU Phd students the first step is to apply for a startup grant. This is a small allocation of time (1000 core hours) to do initial testing: learn how to use the system and give you an idea of how many core hours you will need for your main application. <br><br> To apply go [here](http://nci.org.au/access/user-registration/application-form-resource/), fill in the form and get your supervisor to sign (technically the application comes from them not you) then email it to the help desk (or just walk it over its not that far!). The application process was a bit confusing at times, but a few emails to the help desk got it done. <br><br> Full applications open in November for computing time the next year. The minimum request on raijin is 20,000 core hours, which is fairly large: equivalent to about 4000 hours or 20 weeks time on an i7 desktop or around $5000 worth on a commercial service like [multyvac](http://www.multyvac.com/). 

# Logging in

Once you're approved you'll receive a username and project code via email and a temporary password via sms.

You login online via ssh (if your on windows or mac you will need an ssh client, see the [user guide](http://nci.org.au/services-support/getting-help/raijin-user-guide/)), on linux just open the terminal and type 

{% highlight bash %}
ssh -l username raijin.nci.org.au
{% endhighlight %}

You'll get a warning about connecting for the first time, just type yes, then enter your password and your in.

{% highlight bash %}
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
{% endhighlight %}

# First steps

So now you are in a command line linux environment on a single raijin node (with 16 cores). You should have a prompt that looks like this

{% highlight bash %}
[username@raijin4 ~]$
{% endhighlight %}

First lets reset our password

{% highlight bash %}
[username@raijin4 ~]$ passwd
{% endhighlight %}

We begin in our home folder, which is on the filesystem at /home/unigrp/username (where unigrp is the last three digits of your username). Here you can install all your code and any dependencies. Any changes you make will be saved when you log out. Your home folder has a capacity of 2 Gb. You can check how much you have used with `lquota`.

{% highlight bash %}
[username@raijin4 ~]$ lquota
--------------------------------------------------------------
          fs  Usage  Quota  Limit   iUsage    iQuota   iLimit
--------------------------------------------------------------
ndh401  home  383MB 2000MB 2000MB     5449         0    88000 
   fr3 short   28kB 72.0GB  144GB        7    164000   328000 
--------------------------------------------------------------
{% endhighlight %}

Next we can check our account status

{% highlight bash %}
[username@raijin4 ~]$ nci_account

Usage Report: Project=projectcode Compute Period=2014.q4 (01/10/2014-31/12/2014)
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


Usage Report: Project=projectcode Storage Period=2014.10 (01/10/2014-31/12/2014)
========================================================================
-------------------------------------------------------------------------------------------------
System    StoragePt             Grant       Usage       Avail      iGrant      iUsage      iAvail
-------------------------------------------------------------------------------------------------
dmf       massdata            20.00GB      0.00GB     20.00GB     100.00K       0.00K     100.00K
raijin    short               72.00GB      0.00GB     72.00GB     164.00K       0.01K     163.99K
-------------------------------------------------------------------------------------------------
Total                         92.00GB      0.00GB     92.00GB     264.00K       0.01K     263.99K
{% endhighlight %}

You should see your 1000 hour allocation. Note that these interactive sessions don't count towards your quota. 

# Installing software

raijin has just about all the software you might need already installed (see the [list](http://nci.org.au/nci-systems/national-facility/peak-system/raijin/application-software/)). You just need to make it available to your profile with the `module` command. To view the list of all software type

{% highlight bash %}
[username@raijin4 ~] module avail
{% endhighlight %}

To load Python (with `numpy`, `scipy` and `matplotlib`) you type

{% highlight bash %}
[username@raijin4 ~] module load python/2.7.3
[username@raijin4 ~] module load python/2.7.3-matplotlib
{% endhighlight %}

To use Cython I also needed to replace the default intel C compiler with gcc

{% highlight bash %}
[username@raijin4 ~] module unload intel-cc
[username@raijin4 ~] module load gcc/4.9.0
{% endhighlight %}

You can then add these commands to your `.profile` file, to make sure they are executed on login. I used vim to edit these text files

{% highlight bash %}
[username@raijin4 ~] vim .profile
{% endhighlight %}

# Installing your code and dependencies

An easy way to load your code is via [github](https://github.com) (which is like dropbox for code). Once you've learnt github, and have your code in a github repository [like this](https://github.com/nealbob/regrivermod), you can clone it directly onto your profile.

{% highlight bash %}
[username@raijin4 ~] git clone git://github.com/nealbob/regrivermod.git ~/Model
{% endhighlight %}

Too easy. I also needed to compile my code, which once I loaded `gcc` worked just like it does on my local machine. 

Next I needed to install a number of other Python packages not included on raijin by default (`cython`, `pandas`, `scikit-learn`). First create a folder to hold them

{% highlight bash %}
[username@raijin4 ~] mkdir packages
{% endhighlight %}

To install python packages I can use `easy_install`. You just need to tell `easy_install` to install locally, for example

{% highlight bash %}
[username@raijin4 ~] easy_install --install-dir=~/packages pandas
{% endhighlight %}

Next you need to add ~/packages to your PYTHONPATH environment variable so Python can find it

{% highlight bash %}
[username@raijin4 ~] export PYTHONPATH=~/packages:$PYTHONPATH
{% endhighlight %}

Its best to make this change permanent by adding it to your `.bashrc` file.

# Data storage

The first place to store large data files is in your 'short' folder, located at /short/projectcode/username. As we saw from the `nci_account` output, you get 72 Gb on short and 20 on massdata. <br> <br> To transfer data files between raijin and your local computer you can use `rsync`. For example, to transfer a file from your short folder to you local machine, naviagate to the local folder you want to hold the file then type

{% highlight bash %}
[username@raijin4 ~] rsync  -e "ssh -c arcfour" username@r-dm.nci.org.au:/short/projectcode/username/filename 
{% endhighlight %}

For longer term storage, the user guide recommends massdata because it's backed up.

# Running jobs

Just to check that it works I can run my code interactively 

{% highlight bash %}
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
{% endhighlight %}

Horah it works! To run larger jobs across multiple nodes we need to use the [PBS job scheduling system](http://nci.org.au/services-support/getting-help/pbspro-commands/). To run the above job using PBS we type


{% highlight bash %}
[username@raijin1 Model]$ qsub jobscript
{% endhighlight %}

where jobscript is a text file that contains the following

{% highlight bash %}
#!/bin/bash
#PBS -P projectcode 
#PBS -q express
#PBS -l walltime=60
#PBS -l mem=500MB
#PBS -l ncpus=8
#PBS -l wd
module load python/2.7.3
module load python/2.7.3-matplotlib
python test.py
{% endhighlight %}

All of the lines beginning with `#PBS` are job scheduling options. `-P projectcode` just tells the system which project to charge the time against. `-q express` sets the type of 'queue' to join, either `express` (for testing), `normal`, or `copyq` (for data intensive jobs) - see the [user guide](http://nci.org.au/services-support/getting-help/raijin-user-guide/). `-l wd` just tells the system to start the job from the current directory. 

`-l walltime=60` is the expected running time of the job in seconds (best to allow slightly longer than you expect).  For large jobs you can specify the time in hours:minutes:seconds format.   `-l ncpus=8` sets the number of cpus the job requires, if greater than 16 (one node) this needs to be in multiples of 16. `-l mem=500Mb` is the amount of memory required for the job - your job won't run if you don't allow enough memory.

Next we need to repeat our `module load` statements. While all the changes we've made to our home folder  will be available to the job, anything we've added to `.profile` needs to be repeated. Finally, we add our job command. 

So after submitting we get the uninspiring response

{% highlight bash %}
jobid.r-man2
{% endhighlight %}

where `jobid` is some number. We can query the status of the job with 

{% highlight bash %}
[username@raijin1 Model]$ qstat -s jobid
qstat: 7516166.r-man2 Job has finished, use -x or -H to obtain historical job information
[username@raijin1 Model]$ qstat -s jobid -x

r-man2: 
                                                            Req'd  Req'd   Elap
Job ID          Username Queue    Jobname    SessID NDS TSK Memory Time  S Time
--------------- -------- -------- ---------- ------ --- --- ------ ----- - -----
jobid.r-man2   username express- jobscript   27544  --   8  500mb 00:01 F 00:00
   Job run at Tue Oct 28 at 08:58 on (r102:jobfs_local=102400kb:mem=512000...
{% endhighlight %}

Now if the job worked as planned we should find a `jobscript.ojobid` text file has been created with all of the output (if not you might find a `jobscript.ejobid` file with an error message). To view any of these files use the `cat` command

{% highlight bash %}
[username@raijin1 Model]$ cat jobscript.ojobid

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
Solve time: 3.24676513672
Running simulation for 500000 periods...
Simulation time: 0.89
Summary stats time 1.6745159626
Data stacking time: 1.70569396019
Storage mean: 697642.617942
Inflow mean: 693752.110128
Withdrawal mean: 520867.804524
Welfare mean: 186632658.338
======================================================================================
			Resource Usage on 2014-10-28 08:59:26.639311:
	JobId:  jobid.r-man2  
	Project: projectcode 
	Exit Status: 0 (Linux Signal 0)
	Service Units: 0.04
	NCPUs Requested: 8				NCPUs Used: 8
							CPU Time Used: 00:00:36
	Memory Requested: 500mb 			Memory Used: 56mb
							Vmem Used: 531mb
	Walltime requested: 00:01:00 			Walltime Used: 00:00:20
	jobfs request: 100mb				jobfs used: 1mb
======================================================================================
{% endhighlight %}

Great so it worked, and we have this resource usage info at the end, which is a good way to work out the CPU / memory requirements of your jobs.


