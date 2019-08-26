#!/usr/bin/env python3

from datetime import datetime
import csv
import re
import gzip
from collections import Counter

ch = Counter()  # hashtags
nh = 0
nt = 0
cu = Counter()  # users
# c.update()

with gzip.open('data/0-election_day_tweets.csv.gz', 'r') as csvinput:
  with gzip.open('data/0-election_day_tweets_expanded.csv.gz', 'wt') as csvoutput:
    writer = csv.writer(csvoutput, lineterminator='\n')
    reader = csv.reader(csvinput)

    row = next(reader)
    row.append('created_str')
    row.append('hashtags')
    row.append('mentions')
    writer.writerow(row)

    for row in reader:
      nt += 1
      cu.update([row[10]])
      convdate = row[1]
      a = datetime.strptime(convdate, "%Y-%m-%d %H:%M:%S")
      b = datetime(1970, 1, 1)
      row.append(int((a - b).total_seconds()) * 1000)

      text = row[0]
      # remove urls
      text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)  # , flags=re.MULTILINE)
      # split words
      text_arr = re.findall(r'[#@]?[\w\'`]+', text)
      # text_arr = re.findall(r'\w+', text)
      # print(text_arr)
      hashtags = []
      mentions = 0
      for word in text_arr:
        if word[0] == '#':
          m = re.match(r'#(\w+)', word)
          if m is None:
            print(word)
            continue
          h = m.group(1).lower()
          # print(word, h)
          ch.update([h])
          hashtags.append(h)
          nh += 1
        elif word[0] == '@':
          mentions = mentions + 1
        # elif
      row.append(hashtags)
      row.append(mentions)
      writer.writerow(row)
      # all.append(row)

    # writer.writerows(all)

print('{} unique / {} total hashtags / {}'.format(len(ch), nh, nh / len(ch)))
print('{} users / {} tweets / {}'.format(len(cu), nt, nt / len(cu)))

# print(cu)
# print(ch)