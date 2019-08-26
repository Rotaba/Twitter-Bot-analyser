#!/usr/bin/env python3

from datetime import datetime
import csv
import re
import gzip
from collections import Counter

import sys
from gensim.models import doc2vec
from collections import namedtuple
# from os.path import basename
import os


def split_dataset(file, col, frac):
    # base = basename(file)
    # base, ext = os.path.splitext(file)
    if file.endswith('.csv.gz'):
        base, ext = file[:-7], file[-7:]
    else:
        base, ext = os.path.splitext(file)
    out1 = base + '-0.csv'
    out2 = base + '-1.csv'
    print(out1, out2)
    data = []
    c = Counter()
    with gzip.open(file, 'rt') if ext.endswith('gz') else open(file, 'rt') as csvinput:
        reader = csv.reader(csvinput)
        head = next(reader)
        for row in reader:
            data.append(row)
            c[row[col]] += 1
    print(c)
    cn = Counter()
    c1 = Counter()
    c2 = Counter()
    # value = c.most_common(1)[0]
    d1 = []
    d2 = []
    for d in data:
        v = d[col]
        cn[v] += 1
        d = d[2:] + [d[1]]
        if cn[v] < c[v] * frac:
            c1[v] += 1
            d1.append(d)
        else:
            c2[v] += 1
            d2.append(d)
    print(c1, c2)
    # with gzip.open(out1, 'rt') if ext.endswith('gz') else open(file, 'rt') as csvinput:
    with open(out1, 'wt') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        writer.writerow(head)
        # writer.writerow([len(d1), 100, 'not-troll', 'troll'])
        # writer.writerow([str(_) for _ in range(100)] + ['troll'])
        writer.writerows(d1)
    with open(out2, 'wt') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        writer.writerow(head)
        # writer.writerow([str(_) for _ in range(100)] + ['troll'])
        writer.writerows(d2)


def main():
    if len(sys.argv) != 2:
        print('1 mandatory parameter: filename to split')
        return
    split_dataset(sys.argv[1], 1, 0.8)


main()

