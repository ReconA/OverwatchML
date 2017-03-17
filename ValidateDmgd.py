import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import scipy
from sklearn import svm
from db import Soldier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

win_samples = []
loss_samples = []
for row in Soldier.select_all_match_stats():
    if row[18] > 1: # Bug in data gathering. Player has played more than 1 game between checks.
        continue
    elif row[19] == 0:
        loss_samples.append([row[8], row[12]])
    elif row[19] == 1:
        win_samples.append([row[8], row[12]])

win_samples = np.array(win_samples)
loss_samples = np.array(loss_samples)

fig = plt.figure()

plt.scatter(win_samples[:,0],win_samples[:,1], marker='+')
plt.scatter(loss_samples[:,0],loss_samples[:,1], c= 'green', marker='o')

X = np.concatenate((win_samples,loss_samples), axis = 0)
Y = np.array([1]*len(win_samples) + [0]*len(loss_samples))

clf = svm.SVC(kernel='linear', C=1)
scores = cross_val_score(clf, X, Y, cv=10)
print scores
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


