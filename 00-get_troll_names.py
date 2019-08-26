#!/usr/bin/env python3

from datetime import datetime
import csv
import re
import gzip
from collections import Counter

users = set()
ids = set()
names = set()

n = 0


with open('../data/original-data/trolls.csv', 'rt') as csvinput:
    reader = csv.reader(csvinput)
    row = next(reader)
    for row in reader:
        id, name = row[0], row[8].lower()
        new_row = (id, name)
        users.add(new_row)
        ids.add(id)
        names.add(name)
        n += 1

# print('users: {} added, new size = {}'.format(n, len(users)))
print('trolls: {} added, new size = {} ids, {} names, {} tuples'.format(n, len(ids), len(names), len(users)))

# with gzip.open('../data/original-data/troll-tweets.csv.gz', 'rt') as csvinput:
#     reader = csv.reader(csvinput)
#     row = next(reader)
#     for row in reader:
#         id, name = row[0], row[1].lower()
#         new_row = (id, name)
#         users.add(new_row)
#         ids.add(id)
#         names.add(name)
#         n += 1

# print('users: {} added, new size = {}'.format(n, len(users)))
# print('troll-tweets: {} added, new size = {} ids, {} names, {} tuples'.format(n, len(ids), len(names), len(users)))
if '' in ids:
    ids.remove('')
if '' in names:
    names.remove('')
if ('', '') in users:
    users.remove(('', ''))
print('removed empty entries, new size = {} ids, {} names, {} tuples'.format(n, len(ids), len(names), len(users)))

with open('../data/original-improved/troll-id.csv', 'wt') as csvoutput:
    writer = csv.writer(csvoutput, lineterminator='\n')
    writer.writerow(['id'])
    for r in ids:
        writer.writerow([r])
with open('../data/original-improved/troll-names.csv', 'wt') as csvoutput:
    writer = csv.writer(csvoutput, lineterminator='\n')
    writer.writerow(['name'])
    for r in names:
        writer.writerow([r])

with open('../data/original-improved/trolls-all.csv', 'wt') as csvoutput:
    writer = csv.writer(csvoutput, lineterminator='\n')
    writer.writerow(['id', 'name'])
    for r in users:
        writer.writerow([r[0], r[1]])

# umap = {}
# for x in users:
#     if