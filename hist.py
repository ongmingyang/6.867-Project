import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as p

with open("output3/hist.csv") as csvfile:
  entries = csv.reader(row for row in csvfile if not row.startswith("#"))
  data = [int(v[1]) for v in entries]

p.hist(data, bins=50, log=True)
p.savefig('hist.eps')
p.clf()
p.plot(data, range(len(data)))
p.yscale('log')
p.savefig('freq.eps')
