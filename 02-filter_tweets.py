#!/usr/bin/env python3

from datetime import datetime
import csv
import re
import gzip
from collections import Counter
import random
import numpy

# uids = {}

def  process_text(text):
    # substitute urls
    text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', 'xxURLxx', text)
    #
    text = text.replace('\'', '')
    return text


def simple_XX(filename, n_from_troll, n_from_not):
    tweets = [[], []]
    with gzip.open(filename, 'rt') as csvinput:
        reader = csv.reader(csvinput)
        next(reader)  # skip header
        # rows = [_ for _ in reader]
        for x in reader:
            tweets[0].append(x) if x[0] == '0' else tweets[1].append(x)
    # random.sample(rows)
    if len(tweets[0]) < n_from_not:
        raise Exception('not enough not troll tweets')
    if len(tweets[1]) < n_from_troll:
        raise Exception('not enough troll tweets')
    numpy.random.shuffle(tweets[0])
    numpy.random.shuffle(tweets[1])
    return tweets[0][:n_from_not], tweets[1][:n_from_troll]


def per_user(filename, tweets_per_user, not_troll_tweets_total):
    uids = Counter()
    stat = Counter()
    tweets = []

    with gzip.open(filename, 'rt') as csvinput:
        reader = csv.reader(csvinput)
        next(reader)  # skip header
        for row in reader:
            id = row[1]
            if tweets_per_user is not None:
                if id in uids:
                    if uids[id] >= tweets_per_user:
                        continue
                    else:
                        uids[id] += 1
                else:
                    uids[id] = 1
            troll = row[0]
            if troll == '1':
                stat['troll'] += 1
            else:
                if not_troll_tweets_total is not None and stat['not_troll'] > not_troll_tweets_total:
                    continue
                stat['not_troll'] += 1
            name = row[2]
            text = row[3]
            tweets.append((troll, text))
    print(stat)
    return tweets


def write_tweets(filename, tweets):
    with gzip.open(filename, 'wt') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        writer.writerow(['is_troll', 'text'])
        for r in tweets:
            r[1] = process_text(r[1])
            writer.writerow(r)


# def write_dataset

# tweets = per_user('../data/original-improved/all-tweets-marked.csv.gz', )
tweets = simple_XX('../data/original-improved/all-tweets-marked.csv.gz', 5000, 5000)
# tweets[0] += tweets[1]
# for t in tweets[0]:
#     x = []
write_tweets('../data/original-improved/5k-each.csv.gz', [[x[0], x[3]] for x in tweets[0] + tweets[1]])

