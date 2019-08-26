#!/usr/bin/env python3

from datetime import datetime
import csv
import re
import gzip
from collections import Counter


def stat(filename, col):
    c = Counter()
    with gzip.open(filename, 'rt') if filename.endswith('gz') else open(filename, 'rt') as csvinput:
        reader = csv.reader(csvinput)
        row = next(reader)
        for row in reader:
            value = row[col]
            c[value] += 1
    return c


def ss(name, c):
    s = sum(c.values())
    n = len(c)
    print('\n###\n{}: {} total, {} unique, {} frac (total/unique)'.format(name, s, n, s/n))
    # print('\n', c.most_common(10))
    print('most  common: ', c.most_common(10))
    print('least common: ', c.most_common()[:-10:-1])
    c2 = Counter()
    for x in c.items():
        c2[x[1]] += 1
    print('\n{} numbers: {} different numbers, {} unique numbers'.format(name, sum(c2.values()), len(c2)))
    print('most  common: ', c2.most_common(10))
    print('least common: ', c2.most_common()[:-10:-1])
    # print(c2)


def empty_field_stat(filename):
    print('file: {}'.format(filename))
    ci = Counter()
    cd = Counter()
    with gzip.open(filename, 'rt') if filename.endswith('gz') else open(filename, 'rt') as csvinput:
        reader = csv.reader(csvinput)
        header = next(reader)
        for row in reader:
            for i in range(len(row)):
                if row[i] == '':
                    ci[i] += 1
        for i in range(len(header)):
            if ci[i] > 0:
                cd[header[i]] = ci[i]
    print('empty indexes ', ci)
    print('empty fields  ', cd)


# ct = stat('../data/original-data/troll-tweets.csv.gz', 1)
# ce = stat('..data/original-data/election_day_tweets_expanded.csv.gz', 21)
#
# ss('troll', ct)
# ss('elect', ce)

empty_field_stat('../data/original-data/election_day_tweets.csv.gz')
empty_field_stat('../data/original-data/troll-tweets.csv.gz')
empty_field_stat('../data/original-improved/trolls-all.csv')

# print('troll {} total, {} unique'.format(sum(c.values()), len(c)))
# print('\n', c.most_common(40))
# print('\nleast common:', c.most_common()[:-40:-1])
