#!/usr/bin/python
import os, csv
from pdb import set_trace as debug

'''
This file standardizes the length of the
lexeme vector and combines the results into
a single csv file
'''

# Globals
threshold = 300 # drops all entries in the dictionary that appears fewer than `threshold` times in total
path_to_histogram = "output3/hist.csv"
path_to_matrix = "output3/matrix.csv"

def clean_dict(dic):
  for key in dic.keys():
    dic[key] = 0

def main():
  # Massive global dictionary object
  dic = {}

  # First iteration of dirtree to get features
  for root, dirs, files in os.walk("output2"):
    for files in files:
      path_to_file = os.path.join(root, files)
      with open(path_to_file) as csvfile:
        entries = csv.reader(row for row in csvfile if not row.startswith("#"))
        for row in entries:
          if row[0] in dic:
            dic[row[0]] += int(row[2])
          else:
            dic[row[0]] = int(row[2])

  print len(dic)
  with open(path_to_histogram, 'w') as f:
    f.write("# Word: frequency\n# This list is sorted from highest to lowest frequency\n")
    for key in sorted(dic, cmp=lambda x,y: cmp(dic[x], dic[y]), reverse=True):
      f.write("{0}, {1}\n".format(key, dic[key]))

  # Begin pruning dictionary for feature matrix
  dic_order = sorted([(k,v) for (k,v) in dic.iteritems() if v > threshold], key=lambda tup: tup[1], reverse=True)
  pruned_dic = {k:0 for (k,v) in dic_order}
  print len(pruned_dic)

  # Second iteration of dirtree to get frequencies of vectors
  with open(path_to_matrix, 'w') as f:
    # Write words in row
    f.write("# [Date]") 
    for tup in dic_order:
      f.write(", {0}".format(tup[0]))
    f.write("\n")

    # Write frequencies into each row for each day in year
    for root, dirs, files in os.walk("output2"):
      dirs.sort()
      for files in sorted(files):

        # Clear dictionary, add date in first column
        clean_dict(pruned_dic)
        path_to_file = os.path.join(root, files)
        print path_to_file
        f.write("{0}".format(root[-8:])) # This gets the date if I'm not wrong

        # Ok, start populating dictionary
        with open(path_to_file) as csvfile:
          entries = csv.reader(row for row in csvfile if not row.startswith("#"))
          for row in entries:
            if row[0] in pruned_dic:
              pruned_dic[row[0]] += int(row[2])

        # Write row
        for tup in dic_order:
          f.write(", {0}".format(pruned_dic[tup[0]]))
        f.write("\n")

main()
