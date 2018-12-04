#!/usr/bin/python

import tensorflow as tf
import numpy as np
import codecs
import json

vocab_filename = 'vocab.json'
model_filename = 'best.hdf5'
sample_text_size = 3000
temperature = 0.8

with codecs.open(vocab_filename, 'r', encoding='utf-8') as f:
    vocab = json.loads(f.read())

num_classes = len(vocab)+1

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)

model = tf.keras.models.load_model(model_filename)

model.summary()

input_shape = model.input_shape

#print input_shape

data = np.random.randint(num_classes,high=None, size=input_shape)

predictions = []

model.reset_states()

for i in range(sample_text_size):
#    print data[0]
    probabilities = model.predict_on_batch(data)
    index = int(abs(np.random.normal(0.0, temperature)))
    
#    print probabilities[0]
    ps=np.flip(np.argsort(probabilities[0]));
#    print ps
    prediction = ps[index]
#    print prediction
    data[0] = np.roll(data[0],-1)
    data[0][-1]=prediction
    predictions.append(prediction)

#print predictions

#print vocab
inv_vocab = {v: k for k, v in vocab.iteritems()}
inv_vocab[0] = ''

text = map(lambda x: inv_vocab[x], predictions)

text = ''.join(text)

print text

