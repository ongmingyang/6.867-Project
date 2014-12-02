import csv
from dateutil.parser import parse
from math import log

'''
I have no idea what I am doing
'''

dow = {}
positive_counts = {}
negative_counts = {}
gains = {}
predict_rate = {}
goods = bads = 0
# We will store predictions in memory- this is ok as the file is small
with open("dow_2007.txt") as f:
  for line in f:
    k = line.rstrip().split(",")
    d = parse(k[0]).date().strftime('%Y%m%d')
    y = int(k[1])

    if y == 1: goods += 1 # total 144
    else: bads += 1 # total 107

    dow[d] = y

with open("output3/matrix.csv") as csvfile:
  # Read first row, get words
  words = csvfile.readline().rstrip().split(",")

  # Initialize to 0
  for i in xrange(1, len(words)):
    positive_counts[words[i]] = 0
    negative_counts[words[i]] = 0

  # Generator expression to read entires that belong also in dow
  entries = csv.reader(row for row in csvfile if row[0:8] in dow)

  for entry in entries:
    for i in xrange(1,len(entry)):
      if int(entry[i]) != 0 and dow[entry[0]] == 1:
        positive_counts[words[i]] += 1
      if int(entry[i]) == 0 and dow[entry[0]] != 1:
        negative_counts[words[i]] += 1

def entropy(goods, bads):
  # Include laplace correction term?
  g = float(goods+0.01)/(goods+bads)
  b = float(bads+0.01)/(goods+bads)
  return - g*log(g,2) - b*log(b,2)

prior_entropy = entropy(goods, bads)
g = float(goods)/(goods+bads)
b = float(bads)/(goods+bads)

for i in xrange(1, len(words)):
  word = words[i]
  p = positive_counts[word]
  n = negative_counts[word]
  #print p,n
  gains[word] = prior_entropy - g * entropy(p, goods-p) - b * entropy(n, bads-n)
  predict_rate[word] = (p,n)

gain_order = sorted([(k,v) for (k,v) in gains.iteritems()], key=lambda tup: tup[1])
prob = lambda tup: g * tup[1][0]/goods + b * tup[1][1]/bads
predict_order = sorted([(k,v,prob((k,v))) for (k,v) in predict_rate.iteritems()], key=prob, reverse=True)

for i in xrange(0,20):
  output = ' & '.join(map(str, predict_order[i])).replace(',',' &').replace('(', '').replace(')', '')
  print output + ' \\\ '
  #print predict_order[i], gains[predict_order[i][0]]
  #print gain_order[i], predict_rate[gain_order[i][0]]
