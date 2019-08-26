#!/usr/bin/env python3

#  from wikidataintegrator import wdi_core
# my_first_wikidata_item = wdi_core.WDItemEngine(wd_item_id='Q5')
# /Users/maggiemoheb/Desktop/Masters/2nd semester/Privacy Enhancement Technologies

# # to check successful installation and retrieval of the data, you can print the json representation of the item
# print(my_first_wikidata_item.get_wd_json_representation())

import gzip

from gensim.models import doc2vec
from collections import namedtuple
import csv

# combine texts

doc1 = []
with open('data/1-troll-tweets.csv', 'rt') as csvinput:
    with gzip.open('/data/0-election_day_tweets_output.csv.gz', 'rt') as csvinput2:
        reader = csv.reader(csvinput)
        reader2 = csv.reader(csvinput2)
        all = []
        row = next(reader)
        row.append('tweet_vec')
        count = 0
        all.append(row)
        for row in reader:
            doc1.append(row[7])
            count = count + 1
        for row in reader2:
            doc1.append(row[0])
            count = count + 1

# Load data
# doc1 = ["This is a sentence", "This is another sentence"]

# Transform data (you can add more data preprocessing steps) 
# texts -> tags

docs = []
analyzedDocument = namedtuple('AnalyzedDocument', 'words tags')
for i, text in enumerate(doc1):
    # print(i, " ", text)
    words = text.lower().split()
    tags = [i]
    # print(analyzedDocument(words, tags))
    docs.append(analyzedDocument(words, tags))

# Train model (set min_count = 1, if you want the model to work with the provided example data set)

model = doc2vec.Doc2Vec(docs, vector_size=100, window=300, min_count=1, workers=4)

# Get the vectors
# print(model.docvecs[0])
# model.docvecs[1]

# print(model.docvecs)
model.save('tweets_model')

model = doc2vec.Doc2Vec.load('tweets_model')

all = []
row = list(range(0, 101))
all.append(row)
for i in range(count):
    row = [i + 1]
    row.extend(model.docvecs[i])
    all.append(row)
with open('tweets_output.csv', 'wt') as csvoutput:
    writer = csv.writer(csvoutput, lineterminator='\n')
    writer.writerows(all)
