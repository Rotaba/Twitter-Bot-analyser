#!/usr/bin/env python3

from datetime import datetime
import csv
import re
import gzip
from collections import Counter

c = Counter()  # hashtags

with gzip.open('data/0-election_day_tweets_expanded.csv.gz', 'rt') as csvoutput:
    reader = csv.reader(csvoutput)

    row = next(reader)

    for row in reader:
      hashtags = row[35]
      hashtags = re.findall(r'\'([\w`]+)\'', hashtags)
      # print(hashtags)
      for word in hashtags:
        c[word] += 1

print('{} total, {} unique'.format(sum(c.values()), len(c)))

print('\n', c.most_common(40))

print('\nleast common:', c.most_common()[:-40:-1])

