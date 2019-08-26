#!/usr/bin/env python3

from datetime import datetime
import csv
import re
import gzip
from collections import Counter

import os

import numpy
from gensim.models import doc2vec
from collections import namedtuple


bm = True


def build_model(doc):
    docs = []
    analyzedDocument = namedtuple('AnalyzedDocument', 'words tags')
    for i, text in enumerate(doc):
        # print(i, " ", text)
        words = re.findall(r'[#@]?[\w\'`]+', text.lower())
        # words = text.lower().split()
        tags = [i]
        # print(analyzedDocument(words, tags))
        docs.append(analyzedDocument(words, tags))
    model = doc2vec.Doc2Vec(docs, vector_size=100, window=300, min_count=1, workers=4)
    model.save('tweets_model')
    print('model saved')
    return model


def load_model():
    return doc2vec.Doc2Vec.load('tweets_model')



def generate(filename, bm):
    # uids = {}
    uids = Counter()
    stat = Counter()
    tweets = []

    all = []
    doc = []
    with gzip.open(filename, 'rt') if filename.endswith('gz') else open(filename, 'rt') as csvinput:
        reader = csv.reader(csvinput)
        next(reader)  # skip header
        for row in reader:
            all.append(row)
            doc.append(row[1])

    print('document loaded')

    if bm:
        model = build_model(doc)
        print('model built')
    else:
        model = load_model()
        print('model loaded')

    header = ['is_troll']
    # row.extend([x for x in range(100)])
    header.extend(list(range(0, 100)))
    rows = []
    for i in range(len(all)):
        rx = []
        rx.extend(model.docvecs[i])
        rx.append(all[i][0])
        rows.append(rx)
    #rows = [[all[i][0]] + model.docvecs[i] for i in range(len(all))]
    return header, rows


def write(filename, header, rows):
    with gzip.open(filename, 'wt') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        writer.writerow(header)
        writer.writerows(rows)


def write_split(filename, header, rows, frac=0.8):
    base, ext = os.path.splitext(filename)
    out1 = base + '-0.csv'
    out2 = base + '-1.csv'
    tweets = [[], []]
    with gzip.open(filename + '.gz', 'wt') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        writer.writerow(header)
        writer.writerows(rows)
    for x in rows:
        tweets[0].append(x) if x[0] == '0' else tweets[1].append(x)
    numpy.random.shuffle(tweets[0])
    numpy.random.shuffle(tweets[1])
    n0 = int(len(tweets[0]) * frac)
    n1 = int(len(tweets[1]) * frac)
    train = tweets[0][:n0] + tweets[1][:n1]
    test = tweets[0][n0:] + tweets[1][n1:]
    numpy.random.shuffle(train)
    numpy.random.shuffle(test)
    with open(out1, 'wt') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        writer.writerow(header)
        writer.writerows(train)
    with open(out2, 'wt') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        writer.writerow(header)
        writer.writerows(test)



# row = list(range(0, 101))
# all.append(row)
# for i in range(count):
#     row = [i]
#     row.extend(model.docvecs[i])
#     all.append(row)


h, r = generate('../data/original-improved/5k-each.csv.gz', True)
# write('../data/dataset-04.csv.gz')
write_split('../data/dataset-04.csv', h, r)

