#!/usr/bin/python

import tensorflow as tf
import numpy as np
import codecs
import json

vocab_filename = 'vocab.json'
model_filename = 'best.hdf5'
sample_text_size = 1000
temperature = 0.04

with codecs.open(vocab_filename, 'r', encoding='utf-8') as f:
    vocab = json.loads(f.read())

num_classes = len(vocab)+1

model = tf.keras.models.load_model(model_filename)

model.summary()

input_shape = model.batch_input_shape

print input_shape

data = np.random.randint(num_classes,high=None,size=input_shape)

print data

p = model.predict(data)

print p

