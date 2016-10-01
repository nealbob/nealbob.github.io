import econlearn
import numpy as np
import sklearn
from matplotlib import pyplot as plt

X = np.random.rand(100)
Y = np.maximum(X - 0.5, 0) + np.random.normal(scale=0.1, size=100)
Xt = np.arange(min(X), max(X), 0.001)
Nt = Xt.shape[0]
folder = '/home/nealbob/Dropbox/Presentations/ML/'

def plot_line(X, Y, Xt, Yt, name):

    plt.scatter(X, Y, marker="+")
    plt.xlim(0,1)
    plt.ylim(-0.2,0.8)
    Y_act = np.maximum(Xt - 0.5, 0)
    plt.plot(Xt, Y_act, color="blue", linewidth="0.3")
    plt.plot(Xt, Yt, color="g", linewidth="2.5")
    plt.savefig(folder + name, dpi=200)
    plt.show()


plt.scatter(X, Y, marker="+")
plt.xlim(0,1)
plt.ylim(-0.2,0.8)
plt.savefig(folder + "data.png", dpi=200)
plt.show()

plt.scatter(X, Y, marker="+")
plt.xlim(0,1)
plt.ylim(-0.2,0.8)
Yt = np.maximum(Xt - 0.5, 0)
plt.plot(Xt, Yt, color="blue", linewidth="0.3")
plt.savefig(folder + "datamodel.png", dpi=200)
plt.show()

ols = sklearn.linear_model.LinearRegression(fit_intercept=True)
ols.fit(X.reshape([100,1]), Y)
Yt = ols.predict(Xt.reshape([Nt,1])) 
plot_line(X, Y, Xt, Yt, 'linear.png')

tile = econlearn.TilecodeRegressor(1, [4], 1)
tile.fit(X, Y)
Yt = tile.predict(Xt)
plot_line(X, Y, Xt, Yt, 'bias.png')

tile = econlearn.TilecodeRegressor(1, [40], 1)
tile.fit(X, Y)
Yt = tile.predict(Xt)
plot_line(X, Y, Xt, Yt, 'noise.png')

Y_act = np.maximum(X - 0.5, 0)
ols.fit(Y_act.reshape([100,1]), Y) 
Yt = np.maximum(Xt - 0.5, 0) 
Yt = ols.predict(Yt.reshape([Nt,1]))
plot_line(X, Y, Xt, Yt, 'true.png')

R2 = np.zeros(30)
CV = np.zeros(30)
for i in range(30):
    for j in range(1000):
        Xtemp = np.random.rand(100)
        Ytemp = np.maximum(Xtemp - 0.5, 0) + np.random.normal(scale=0.1, size=100)
        Xtest = np.random.rand(1000)
        Ytest = np.maximum(Xtest - 0.5, 0) + np.random.normal(scale=0.1, size=1000)
        
        tile = econlearn.TilecodeRegressor(1, [i+1], 1)
        tile.fit(Xtemp, Ytemp, score=True)
        R2[i] += (tile.tile.R2)*0.001
        Ytt = tile.predict(Xtest)

        ss_res = np.dot((Ytest - Ytt),(Ytest - Ytt))
        ymean = np.mean(Ytest)
        ss_tot = np.dot((Ytest-ymean),(Ytest-ymean))
        CV[i] += (1-ss_res/ss_tot)*0.001


plt.plot(range(1,31), CV, label="out-of-sample fit")
plt.plot(range(1,31), R2, label="in-sample fit")
plt.xlabel("number of bins")
plt.ylabel("$R^2$")
plt.legend()
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
plt.ylim(0,1)
plt.xlim(0,30)
plt.savefig(folder + 'performance.png', dpi=200)
imax = np.where(CV == np.max(CV))
imax[0][0] = imax[0][0] + 1
plt.scatter(imax, np.array(CV[imax]))
plt.ylim(0,1)
plt.xlim(0,30)
plt.savefig(folder + 'maxperformance.png', dpi=200)
plt.show()

tile = econlearn.TilecodeRegressor(1, [imax[0][0]], 1)
tile.fit(X, Y)
Yt = tile.predict(Xt)
plot_line(X, Y, Xt, Yt, 'good.png')

tile = econlearn.TilecodeRegressor(1, [3], 80)
tile.fit(X, Y, method="SGD", n_iters=30, eta=0.15)
Yt = tile.predict(Xt)
plot_line(X, Y, Xt, Yt, 'ensemble.png')

CV_OLS = np.zeros(30)
CV_ML = np.zeros(30)
CV_ML2 = np.zeros(30)
CV_ACT = np.zeros(30)
sample = np.zeros(30)
for i in range(30):
    N = 8 + 5*i
    sample[i] = N
    for j in range(200):
        X = np.random.rand(N)
        Y = np.maximum(X - 0.5, 0) + np.random.normal(scale=0.1, size=N)
        Xtest = np.random.rand(1000)
        Ytest = np.maximum(Xtest - 0.5, 0) + np.random.normal(scale=0.1, size=1000)
        
        #tile = econlearn.TilecodeRegressor(1, [8], 1)
        #tile.fit(X, Y)
        #Yt = tile.predict(Xtest)
        #ss_res = np.dot((Ytest - Yt),(Ytest - Yt))
        #ymean = np.mean(Ytest)
        #ss_tot = np.dot((Ytest-ymean),(Ytest-ymean))
        #CV_ML[i] += (1-ss_res/ss_tot)*(1/200.0)
        
        tile = econlearn.TilecodeRegressor(1, [3], 80)
        tile.fit(X, Y, method="SGD", n_iters=30, eta=0.15)
        Yt = tile.predict(Xtest)
        ss_res = np.dot((Ytest - Yt),(Ytest - Yt))
        ymean = np.mean(Ytest)
        ss_tot = np.dot((Ytest-ymean),(Ytest-ymean))
        CV_ML2[i] += (1-ss_res/ss_tot)*(1/200.0)

        ols.fit(X.reshape([N,1]), Y)
        Yt = ols.predict(Xtest.reshape([1000,1])) 
        ss_res = np.dot((Ytest - Yt),(Ytest - Yt))
        ymean = np.mean(Ytest)
        ss_tot = np.dot((Ytest-ymean),(Ytest-ymean))
        CV_OLS[i] += (1-ss_res/ss_tot)*(1/200.0)
        
        Y_act = np.maximum(X - 0.5, 0)
        ols.fit(Y_act.reshape([N,1]), Y) 
        X_act = np.maximum(Xtest - 0.5, 0)
        Yt = ols.predict(X_act.reshape([1000,1])) 
        ss_res = np.dot((Ytest - Yt),(Ytest - Yt))
        ymean = np.mean(Ytest)
        ss_tot = np.dot((Ytest-ymean),(Ytest-ymean))
        CV_ACT[i] += (1-ss_res/ss_tot)*(1/200.0)

plt.plot(sample, CV_OLS, color="blue", label="OLS: linear")
plt.plot(sample, CV_ACT, color="blue", linestyle="dashed", label="OLS: true")
plt.xlabel("sample size")
plt.ylabel("out-of-sample $R^2$")
plt.ylim(0,0.9)
#plt.plot(sample, CV_ML, color="green", linestyle="dashed", label="ML: step function")
plt.plot(sample, CV_ML2, color="green", label="ML")
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=3, mode="expand", borderaxespad=0.)
plt.savefig(folder + 'samplesize2.png', dpi=200)
plt.show()
