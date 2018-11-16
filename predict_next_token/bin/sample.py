#!/usr/bin/python

import tensorflow as tf
import numpy as np
import codecs
import json

vocab_filename = 'vocab.json'
model_filename = 'best.ckpt'
sample_text_size = 1000
temperature = 0.075


with codecs.open(vocab_filename, 'r', encoding='utf-8') as f:
    vocab = json.loads(f.read())

model = tf.keras.models.load_model(model_filename)


def generate_text(model, vocab, text_size, temperature):

    vocab_size = len(vocab)

    token_from_index = {v: k for k, v in vocab.iteritems()}
    token_from_index[0] = '\0'

    # starting values

    model_input_shape = np.asarray(model.input_shape)

    model_input_shape[0] = 1

    input_data = np.random.randint(vocab_size, size=model_input_shape)

    predictions = []

    while len(predictions) < text_size:
        probabilities = model.predict(input_data)[0]

        shape = probabilities.shape
        noise = np.random.normal(loc=0.0, scale=temperature, size=shape)
        probabilities += noise

        prediction = probabilities.argmax()
        input_data[0, :-1] = input_data[0, 1:]
        input_data[0, -1] = prediction
        predictions.append(prediction)

    tokens = map(lambda x: token_from_index[x], predictions)
    string = ''.join(tokens)

    return string


text = generate_text(model, vocab, sample_text_size, temperature)

print text
