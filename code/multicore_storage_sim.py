import numpy as np
from matplotlib import pyplot as plt
import time
from multiprocessing import Process
from multiprocessing.queues import Queue

def retry_on_eintr(function, *args, **kw):
    while True:
        try:
            return function(*args, **kw)
        except IOError, e:            
            if e.errno == errno.EINTR:
                continue
            else:
                raise    

class RetryQueue(Queue):
    """Queue which will retry if interrupted with EINTR."""

    def get(self, block=True, timeout=None):
        return retry_on_eintr(Queue.get, self, block, timeout)

def simulate(K, mu, sig, Sbar, T, multi=False, que=0, jobno=0):
    
    np.random.seed(jobno)

    S = np.zeros(T+1)
    W = np.zeros(T+1)
    I = np.zeros(T+1)
    S[0] = K

    for t in range(T):
        W[t] = min(S[t], Sbar)    
        I[t+1] = max(np.random.normal(mu, sig), 0)
        S[t+1] = min(S[t] - W[t] + I[t+1], K)

    if multi:
        que.put(S)
    else:
        return S

def multi_sim(CORES=2, T=100):
    
    results = []
    ques = [Queue() for i in range(CORES)]
    args = [(100, 70, 70, 70, int(T/CORES), True, ques[i], i) for i in range(CORES)]
    jobs = [Process(target=simulate, args=(a)) for a in args]
    for j in jobs: j.start()
    for q in ques: results.append(q.get())
    for j in jobs: j.join()
    S = np.hstack(results)

    return S



"""
### Sample size
T = 1000000

# Single core run ==================================

tic = time.time()

S = simulate(100, 70, 70, 70, T)

toc = time.time()
print 'Single core run time: ' + str(round(toc - tic,3))

plt.plot(S[0:100])
plt.show()

# Multi core run ==================================

tic = time.time()

CORES = 2
results = []
ques = [Queue() for i in range(CORES)]
args = [(100, 70, 70, 70, int(T/CORES), True, ques[i], i) for i in range(CORES)]
jobs = [Process(target=simulate, args=(a)) for a in args]
for j in jobs: j.start()
for q in ques: results.append(q.get())
for j in jobs: j.join()
S = np.hstack(results)

toc = time.time()
print 'Multi-core run time: ' + str(toc - tic)

plt.plot(S[0:100])
plt.show()

print S.shape

plt.scatter(results[0], results[1])
plt.show()
"""
