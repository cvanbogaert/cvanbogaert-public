#!/usr/bin/python

import tensorflow as tf
import keras_preprocessing.text as kpt
import numpy as np
import codecs
import json
import os
import itertools
import time
import csv
import math

# source text file information
encoding = 'utf-8'
fname = 'holmes_canon.txt'
origin = 'https://sherlock-holm.es/stories/plain-text/cnus.txt'

# how to tokenize the text
char_level = True
vocab_filename = 'vocab.json'

# how to split the tokens into training and validation data
validation_split = 0.2

# how to arrange the tokens into batches of sequences and targets

batch_size = 256
shuffle_size = 1000
# how to build the model
embedding_size = 16

# how to train the model
optimizer = 'adam'
num_validation_steps = 5
model_filename = 'pnt.h5'
best_checkpoint_filename = 'best.ckpt'
last_checkpoint_filename = 'last.ckpt'
num_epochs = 1000000
steps_per_epoch = 50
logdir = 'logs'
patience = 100
num_final_validation_steps = 50
stats_filename = 'stats.csv'
# grid
units_grid = [1, 2, 4, 8, 16, 32, 64, 128, 256]
timesteps_grid = [1, 2, 4, 8, 16, 32, 64, 128, 256]
#dropout_grid = [0.0,0.01,0.02,0.05,0.1,0.2,0.5]
#layers_grid = [1,2,3,4,5,6,7,8]

dropout_grid = [0.0]
layers_grid = [4,8,16]


def dataset_from_tokens(tokens, timesteps, batch_size):

    num_tokens = len(tokens)
    stride_size = timesteps + 1
    num_strides = num_tokens / stride_size
    num_take_tokens = num_strides * stride_size + 1

    dataset = tf.data.Dataset.from_tensor_slices(tokens)
    dataset = dataset.take(num_take_tokens)
    dataset = dataset.repeat()
    dataset = dataset.batch(stride_size)
    dataset = dataset.map(lambda x: [x[:-1], x[-1]])
    dataset = dataset.shuffle(shuffle_size)
    dataset = dataset.batch(batch_size)

    return dataset, num_strides


# fetch the file
filename = tf.keras.utils.get_file(fname, origin)
with codecs.open(filename, encoding=encoding) as file:
    text = file.read()

# tokenize the text
t = kpt.Tokenizer(char_level=char_level)
t.fit_on_texts([text])
tokens = t.texts_to_sequences([text])[0]

vocab = t.word_index
vocab_size = len(vocab)

# divide the tokens into training and validation sets
num_tokens = len(tokens)
num_validation_tokens = int(num_tokens * validation_split)
num_training_tokens = num_tokens - num_validation_tokens

training_tokens = tokens[:num_training_tokens]
validation_tokens = tokens[num_training_tokens:]

i = itertools.product(units_grid, timesteps_grid, dropout_grid, layers_grid)
i = sorted(i, key=sum)

fieldnames = [
    'units',
    'timesteps',
    'dropout',
    'layers',
    'num_epochs_completed',
    'final_val_loss',
    'final_val_acc',
    'duration']


with open(stats_filename, 'a') as f:
    writer = csv.writer(f)
    writer.writerow(fieldnames)

for units, timesteps, dropout, exp_layers in i:
    
    layers = int(math.log(exp_layers,2))

    basedir = '_'.join(
        (str(units),
         str(timesteps),
         str(dropout),
         str(layers)))

    if os.path.exists(basedir):
        continue
       
    basedir = basedir + '/'
    os.mkdir(basedir)

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True

    session = tf.Session(config=config)

    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            basedir + best_checkpoint_filename,
            monitor='val_loss',
            save_best_only=True),
        tf.keras.callbacks.ModelCheckpoint(
            basedir + last_checkpoint_filename),
        tf.keras.callbacks.TensorBoard(
            log_dir=basedir + logdir,
            histogram_freq=0,
            batch_size=batch_size,
            write_graph=True,
            write_grads=True,
            write_images=True),
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=patience,
            mode='auto'
        )]

    with codecs.open(basedir + vocab_filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(vocab, sort_keys=True, indent=4))

    model = tf.keras.models.Sequential()

    model.add(
        tf.keras.layers.Embedding(
            vocab_size,
            embedding_size,
            input_length=timesteps))

    model.add(tf.keras.layers.Dropout(dropout))
    for x in range(layers - 1):
        model.add(tf.keras.layers.CuDNNLSTM(units, return_sequences=True))
    model.add(tf.keras.layers.CuDNNLSTM(units))
    model.add(tf.keras.layers.Dropout(dropout))
    model.add(
        tf.keras.layers.Dense(
            vocab_size,
            activation=tf.keras.activations.softmax))

    model.compile(optimizer=optimizer,
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    print model.summary()

    training_dataset, training_strides = dataset_from_tokens(
        training_tokens, timesteps, batch_size)
    validation_dataset, validation_strides = dataset_from_tokens(
        validation_tokens, timesteps, batch_size)

    start = time.time()
    history = model.fit(training_dataset,
                        epochs=num_epochs,
                        steps_per_epoch=steps_per_epoch,
                        validation_data=validation_dataset,
                        validation_steps=num_validation_steps,
                        callbacks=callbacks)

    end = time.time()
    duration = end - start

    num_epochs_completed = len(history.history['acc'])

    final_val_loss, final_val_acc, = model.evaluate(
        validation_dataset,
        steps=num_final_validation_steps)

    fields = [
        units,
        timesteps,
        dropout,
        layers,
        num_epochs_completed,
        final_val_loss,
        final_val_acc,
        duration]

    with open(stats_filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

    tf.keras.backend.clear_session()
    session.close()
