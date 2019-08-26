#!/usr/bin/env python3

from datetime import datetime
import csv
import re
import gzip
from collections import Counter


def load_set(file, set):
    with gzip.open(file, 'rt') if file.endswith('gz') else open(file, 'rt') as csvinput:
        reader = csv.reader(csvinput)
        next(reader)  # omit header
        for row in reader:
            set.add(row[0])


def read_tweets(file, tweets, ids, names, rid, rname, rtext):
    nt = 0
    nn = 0
    with gzip.open(file, 'rt') if file.endswith('gz') else open(file, 'rt') as csvinput:
        reader = csv.reader(csvinput)
        next(reader)  # skip header
        for row in reader:
            id = row[rid]
            name = row[rname]
            text = row[rtext]
            if text == '':
                continue
            if id in ids or name in names:
                troll = 1
                nt += 1
            else:
                troll = 0
                nn += 1
            tweets.append((troll, id, name, text))
    return nn, nt


def read_and_combine(file, user_map, ids, names, rid, rname, rtext):
    with gzip.open(file, 'rt') if file.endswith('gz') else open(file, 'rt') as csvinput:
        reader = csv.reader(csvinput)
        next(reader)  # skip header
        for row in reader:
            id = row[rid]
            name = row[rname]
            text = row[rtext]
            if id in ids or name in names:
                troll = 1
                nt += 1
            else:
                troll = 0
                nn += 1
            tweets.append((troll, id, name, text))


# users = set()
ids = set()
names = set()
tweets = []
# 393 ids, 454 names
load_set('../data/original-improved/troll-id.csv', ids)
load_set('../data/original-improved/troll-names.csv', names)
print('loaded trolls: {} ids, {} names'.format(len(ids), len(names)))

ret = read_tweets('../data/original-data/election_day_tweets.csv.gz', tweets, ids, names, 10, 23, 0)
print('loaded tweets: {} not, {} from trolls'.format(ret[0], ret[1]))

ret = read_tweets('../data/original-data/troll-tweets.csv.gz', tweets, ids, names, 0, 1, 7)
print('loaded tweets: {} not, {} from trolls'.format(ret[0], ret[1]))

with gzip.open('../data/original-improved/all-tweets-marked.csv.gz', 'wt') as csvoutput:
    writer = csv.writer(csvoutput, lineterminator='\n')
    writer.writerow(['is_troll', 'id', 'name', 'text'])
    for r in tweets:
        writer.writerow(r)


# print('users: {} added, new size = {}'.format(n, len(users)))
# print('troll-tweets: {} added, new size = {} ids, {} names'.format(n, len(ids), len(names)))


# with open('../data/original-improved/troll-names.csv', 'wt') as csvoutput:
#     writer = csv.writer(csvoutput, lineterminator='\n')
#     writer.writerow(['name'])
#     for r in names:
#         writer.writerow([r])
#
