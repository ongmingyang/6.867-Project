import csv, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as p

articles_per_day = True

if articles_per_day:
  data = []
  for root, dirs, files in os.walk("text", topdown=False): 
    for dr in dirs:
      data.append(len([0 for f in os.listdir(os.path.join("text", dr))]))

  p.hist(data, bins=50)
  p.savefig('hist_articles.eps')
else:
  with open("output3/hist.csv") as csvfile:
    entries = csv.reader(row for row in csvfile if not row.startswith("#"))
    data = [int(v[1]) for v in entries]

  p.hist(data, bins=50, log=True)
  p.savefig('hist.eps')
  p.clf()
  p.plot(data, range(len(data)))
  p.yscale('log')
  p.savefig('freq.eps')
