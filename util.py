#!/usr/bin/env python3

from datetime import datetime
import csv
import re
import gzip
from collections import Counter


def get_header(filename):
    print('file: {}'.format(filename))
    with gzip.open(filename, 'rt') if filename.endswith('gz') else open(filename, 'rt') as csvinput:
        reader = csv.reader(csvinput)
        return next(reader)


def get_data(filename, drop_row=None):
    print('file: {}'.format(filename))
    with gzip.open(filename, 'rt') if filename.endswith('gz') else open(filename, 'rt') as csvinput:
        reader = csv.reader(csvinput)
        header = next(reader)
        if type(drop_row) is int:
            del header[drop_row]
        rows = []
        for row in reader:
            if type(drop_row) is int:
                del row[drop_row]
            rows.append(row)
    return header, rows


def write_rows(filename, rows):
    with gzip.open(filename, 'wt') if filename.endswith('gz') else open(filename, 'wt') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        writer.writerows(rows)


_, rows = get_data('tf_is_fun/troll_estimator/dataset-04-0.csv.gz')
header = [str(x) for x in range(100)] + ['is_troll']
# print(header, len(data))
write_rows('tf_is_fun/troll_estimator/dataset-04-0-.csv.gz', [header] + rows)
