from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from db import Soldier

target = []
data   = []
for row in Soldier.select_all_match_stats():
    if row[19] == 0 or row[19] == 1:
        target.append(row[19])
        data.append([row[3], row[8], row[12]])


logistic = LogisticRegression()
logistic.fit(data,target)

print "Used %s data points" %len(data)
print "Coefficients=%s" % logistic.coef_
