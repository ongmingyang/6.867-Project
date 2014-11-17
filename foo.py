#!/usr/bin/python
import psycopg2, os
from nltk.corpus import wordnet as wn
from nltk import pos_tag as pos
from pdb import set_trace as debug

'''
This file parses each corpus by
1) Removing stems from words, reducing
  them into their root lexemes
2) Removing stop words
3) Tagging the part of speech
'''

def pg_connect(f):
  with psycopg2.connect("dbname='ml' user='mingy' password='{0}'".format(os.environ['PG_PASSWORD'])) as conn:
    with conn.cursor() as cur:
      return f(cur)

def parse_file(path_to_file, cur):
  # Write from txt file in text to csv file in output
  path_to_write = path_to_file.replace('text','output').replace('txt','csv')
  print path_to_write

  # Skip if file is already written to output or is empty
  if os.path.isfile(path_to_write): return
  if os.path.getsize(path_to_file) <= 1: return

  with open(path_to_file) as f:
    thing = f.readlines()
  thing = ' '.join(thing[0].split())
  # Yay sql injection
  cur.execute("""SELECT to_tsvector('public.english', '{0}')""".format(thing))
  rows = cur.fetchall()

  # Do some cleaning up
  # Dimensionality reduction with hypernyms?
  string = rows[0][0]
  words = string.split(' ')
  vector = {}
  for word in words:
    [key, locations] = word.split(':')
    key = key.strip("'")
    locations = locations.count(',') + 1
    parts_of_speech = pos([key])[0][1]
    vector[key] = (parts_of_speech, locations)

  with open(path_to_write, 'w') as f:
    f.write("# Lexeme, Part of Speech, Frequency\n")
    for key, value in vector.iteritems():
      stringy = "{0}, {1}, {2}\n".format(key, value[0], value[1])
      f.write(stringy)

@pg_connect
def main(cur):
  for root, dirs, files in os.walk("text"):
    dirs.sort()
    for name in sorted(files):
      path_to_file = os.path.join(root, name)
      parse_file(path_to_file, cur)
