import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import scipy
from sklearn import svm
from db import Soldier
from operator import itemgetter
import math

win_samples = []
loss_samples = []
for row in Soldier.select_all_match_stats():
    if row[18] > 1: # Bug in data gathering. Player has played more than 1 game between checks.
        continue
    elif row[19] == 0:
        loss_samples.append([row[4], row[3]])
    elif row[19] == 1:
        win_samples.append([row[4], row[3]])

win_samples = np.array(win_samples)
loss_samples = np.array(loss_samples)

fig = plt.figure()

plt.scatter(win_samples[:,0],win_samples[:,1], marker='+')
plt.scatter(loss_samples[:,0],loss_samples[:,1], c= 'green', marker='o')

X = np.concatenate((win_samples,loss_samples), axis = 0)
Y = np.array([1]*len(win_samples) + [0]*len(loss_samples))

#print max(X,key=itemgetter(1))[0]
#max =  np.amax(X)
#max = int(math.ceil(1.05 * max))


C = 1.0  # SVM regularization parameter
clf = svm.SVC(kernel = 'linear',  gamma=0.7, C=C )
clf.fit(X,Y)

w = clf.coef_[0]
a = -w[0] / w[1]
xx = np.linspace(0, 62)
yy = a * xx - (clf.intercept_[0]) / w[1]
#yy = np.linspace(0,75)

plt.ylabel("Kills")
plt.xlabel("Finishing blows")
#plt.axis('equal')
plt.plot(xx, yy, 'k-')

plt.xlim([0,60])
plt.ylim([0,60])

fig.savefig('lin.png')
print "Coefficients=%s" %clf.coef_
