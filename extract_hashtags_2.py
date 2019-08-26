#!/usr/bin/env python3

from datetime import datetime
import csv
import re
import gzip
from collections import Counter

# ch = Counter()  # hashtags
# nh = 0
# nt = 0
# cu = Counter()  # users
# c.update()


def load_set(file):
    with gzip.open(file, 'rt') if file.endswith('gz') else open(file, 'rt') as csvinput:
        reader = csv.reader(csvinput)
        header = next(reader)  # omit header
        rows = [_ for _ in reader]
        return rows, header


data, header = load_set('../data/original-improved/all-tweets-marked.csv.gz')
hm = {}
hh = []
hn = 0
hl = []
for row in data:
    text = row[3]
    # remove urls
    text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)  # , flags=re.MULTILINE)
    # split words
    text_arr = re.findall(r'[#@]?[\w\'`]+', text)
    # text_arr = re.findall(r'\w+', text)
    # print(text_arr)
    hashtags = set()
    mentions = 0
    for word in text_arr:
        if word[0] == '#':
            m = re.match(r'#(\w+)', word)
            if m is None:
                print(word)
                continue
            h = m.group(1).lower()
            if h in hm:
                n = hm[h]
            else:
                n = hn
                hm[h] = hn
                hh.append(h)
                hn += 1
            # hashtags.append(n)
            hashtags.add(n)
        # elif word[0] == '@':
        #     mentions = mentions + 1
        #     elif
    # hashtags = hashtags.sort()
    hl.append(hashtags)

file = '../data/original-improved/all-with-tags.csv.gz'
ct = len(data)
cc = 0
with gzip.open(file, 'wt') if file.endswith('gz') else open(file, 'wt') as csvoutput:
    writer = csv.writer(csvoutput)
    for i in range(hn):
        header.append('#' + hh[i])

    print('hlen = {}'.format(len(header)))
    l = len(header)
    writer.writerow(header)

    for row, hashtags in zip(data, hl):
        cc += 1
        if cc % 100 == 1:
            print('{} of {} rows processing'.format(cc, ct), end='\r')
        for i in range(hn):
            if i in hashtags:
                row.append(1)
            else:
                row.append(0)
        writer.writerow(row)

        if len(row) != l:
            print('{} = {}'.format(row[3], len(row)))
        del row
