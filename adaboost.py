import csv
import numpy as np
import matplotlib.pyplot as plt
from pdb import set_trace as debug

from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

# Get decision stump indices
stumps = ["scotland", "violent", "feb", "advised", "youth", "chronicle", "ambition", "contemporary", "shared", "semiconductor", "cdos", "financi", "kurdish", "mukasey", "astrazeneca", "oat", "avandia", "myanmar", "glaxo", "tiffani"]
stump_indices = []
with open("output3/hist.csv") as csvfile:
  entries = csv.reader(row for row in csvfile if not row.startswith("#"))
  i = 0
  for row in entries:
    word = row[0].strip()
    if word in stumps:
      stump_indices.append(i)
    i += 1

# load data from csv files
data = np.loadtxt('processed_matrix.csv', delimiter=",")

# Truncate data to only include relevant stumps
stump_indices.append(-1)
data = data[:, stump_indices]

# use deep copy here to make cvxopt happy
x = data[:, 1:-1].copy()
y = data[:, -1:].copy()

indices = range(len(x))
test_indices = indices[::3]
train_indices = [i for i in indices if i not in test_indices]

x_train = np.ceil(x[train_indices])
y_train = y[train_indices]
x_test = np.ceil(x[test_indices])
y_test = y[test_indices]

#ada=AdaBoostClassifier(DecisionTreeClassifier(max_depth=1), n_estimators=25) 
ada=AdaBoostClassifier() 
ada.fit(x_train,y_train.ravel())

score = ada.staged_score(x_test, y_test.ravel())
for stage in score:
  print stage
