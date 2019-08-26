#!/usr/bin/env python3

from __future__ import absolute_import, division, print_function

from datetime import datetime
import csv
import re
import gzip
from collections import Counter
from gensim.models import doc2vec
from collections import namedtuple
# from os.path import basename
import os
import sys

# https://github.com/tensorflow/tensorflow/issues/19584
# https://www.tensorflow.org/get_started/eager

import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow.contrib.eager as tfe


# _train_dataset_fp = '../data/dataset-02-1.csv'
# _test_fp =          '../data/dataset-02-0.csv'
# _num_epochs = 10
# _epoch_verb = 2


def parse_csv(line):
    #example_defaults = [[0]] + [[0.]] * 100  # sets field types
    example_defaults = [[0.]] * 100 + [[0]] # sets field types
    #print(example_defaults)
    parsed_line = tf.decode_csv(line, example_defaults)
    # First 4 fields are features, combine into single tensor
    features = tf.reshape(parsed_line[:-1], shape=(100,))
    # Last field is the label
    label = tf.reshape(parsed_line[-1], shape=())
    return features, label


tf.enable_eager_execution()
print("TensorFlow version: {}".format(tf.VERSION))
print("Eager execution: {}".format(tf.executing_eagerly()))


def loss(model, x, y):
    y_ = model(x)
    return tf.losses.sparse_softmax_cross_entropy(labels=y, logits=y_)


def grad(model, inputs, targets):
    with tf.GradientTape() as tape:
        loss_value = loss(model, inputs, targets)
    return tape.gradient(loss_value, model.variables)


### TRAIN ###
def train(train_dataset_fp, num_epochs, epoch_verb):
    # train_dataset_fp = tf.keras.utils.get_file('../data/dataset-00-0.csv', origin='../data/dataset-00-0.csv')
    # train_dataset_fp = open('../data/dataset-00-0.csv', 'rt')
    # with open('../data/dataset-00-0.csv', 'rt') as file:
    #    train_dataset_fp = ''.join(file.readlines())
    train_dataset = tf.data.TextLineDataset(train_dataset_fp, compression_type='GZIP')
    train_dataset = train_dataset.skip(1)  # skip the first header row
    train_dataset = train_dataset.map(parse_csv)  # parse each row
    train_dataset = train_dataset.shuffle(buffer_size=1000)  # randomize
    train_dataset = train_dataset.batch(32)

    # View a single example entry from a batch
    features, label = iter(train_dataset).next()
    print("example features:", features[0])
    print("example label:", label[0])

    # example features: tf.Tensor([6.  2.7 5.1 1.6], shape=(4,), dtype=float32)
    # example label: tf.Tensor(1, shape=(), dtype=int32)

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, activation="relu", input_shape=(100,)),  # input shape required
        tf.keras.layers.Dense(10, activation="relu"),
        tf.keras.layers.Dense(3)
    ])

    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.05)

    ## Note: Rerunning this cell uses the same model variables

    # keep results for plotting
    train_loss_results = []
    train_accuracy_results = []

    for epoch in range(num_epochs):
        epoch_loss_avg = tfe.metrics.Mean()
        epoch_accuracy = tfe.metrics.Accuracy()

        # Training loop - using batches of 32
        for x, y in train_dataset:
            # Optimize the model
            grads = grad(model, x, y)
            optimizer.apply_gradients(zip(grads, model.variables),
                                      global_step=tf.train.get_or_create_global_step())

            # Track progress
            epoch_loss_avg(loss(model, x, y))  # add current batch loss
            # compare predicted label to actual label
            epoch_accuracy(tf.argmax(model(x), axis=1, output_type=tf.int32), y)

        # end epoch
        train_loss_results.append(epoch_loss_avg.result())
        train_accuracy_results.append(epoch_accuracy.result())

        if epoch % epoch_verb == 0:
            print("Epoch {:03d}: Loss: {:.3f}, Accuracy: {:.3%}".format(epoch,
                                                                        epoch_loss_avg.result(),
                                                                        epoch_accuracy.result()))
    return model


### TEST ###
def test(model, test_fp):
    test_dataset = tf.data.TextLineDataset(test_fp, compression_type='GZIP')
    test_dataset = test_dataset.skip(1)  # skip header row
    test_dataset = test_dataset.map(parse_csv)  # parse each row with the funcition created earlier
    test_dataset = test_dataset.shuffle(1000)  # randomize
    test_dataset = test_dataset.batch(32)  # use the same batch size as the training set

    test_accuracy = tfe.metrics.Accuracy()
    cc = Counter()

    for (x, y) in test_dataset:
        prediction = tf.argmax(model(x), axis=1, output_type=tf.int32)
        test_accuracy(prediction, y)
        #print(prediction, y)
        cc['TP'] += int(tf.count_nonzero(prediction * y))
        cc['TN'] += int(tf.count_nonzero((prediction - 1) * (y - 1)))
        cc['FP'] += int(tf.count_nonzero(prediction * (y - 1)))
        cc['FN'] += int(tf.count_nonzero((prediction - 1) * y))

    print("Test set accuracy: {:.3%}".format(test_accuracy.result()))
    print('c: tp.tn {}.{}  fp.fn {}.{} '.format(cc['TP'], cc['TN'], cc['FP'], cc['FN']))
    #print('c: ', cc)
    #print("Test set precision: {:.3%}".format(test_p.result()))
    #print("Test set recall: {:.3%}".format(test_r.result()))


def main():
    if len(sys.argv) != 4:
        print('train test epochs')
        exit(1)
    train_dataset_fp, test_fp, num_epochs = sys.argv[1:]
    num_epochs = int(num_epochs)
    print('Train data: {}\nTest data:  {}\nEpochs: {}'.format(train_dataset_fp, test_fp, num_epochs))
    model = train(train_dataset_fp, num_epochs, num_epochs // 15 + 1)
    test(model, test_fp)


main()
