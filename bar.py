#!/usr/bin/python
import os, csv
from pdb import set_trace as debug

'''
This file combines the lexeme frequencies
of articles written on the same day
'''

def main():
  for root, dirs, files in os.walk("output"):
    dirs.sort()
    dic = {}
    for files in sorted(files):
      path_to_file = os.path.join(root, files)
      with open(path_to_file) as csvfile:
        entries = csv.reader(row for row in csvfile if not row.startswith("#"))
        for row in entries:
          if row[0] in dic:
            dic[row[0]] = (row[1], int(dic[row[0]][1]) + int(row[2]))
          else:
            dic[row[0]] = (row[1], row[2])

    path_to_write = "{0}/0.csv".format(root.replace("output","output2"))
    print path_to_write
    with open(path_to_write, 'w') as f:
      f.write("# Lexeme, Part of Speech, Frequency\n")
      for key, value in dic.iteritems():
        stringy = "{0}, {1}, {2}\n".format(key, value[0], value[1])
        f.write(stringy)

main()
