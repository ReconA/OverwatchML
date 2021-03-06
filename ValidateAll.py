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
        loss_samples.append(row[3:17])
    elif row[19] == 1:
        win_samples.append(row[3:17])

win_samples = np.array(win_samples)
loss_samples = np.array(loss_samples)


X = np.concatenate((win_samples,loss_samples), axis = 0)
Y = np.array([1]*len(win_samples) + [0]*len(loss_samples))

clf = svm.SVC(kernel='linear', C=1)
scores = cross_val_score(clf, X, Y, cv=10)
print scores
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


