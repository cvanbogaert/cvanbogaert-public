#!/usr/bin/python

import tensorflow as tf
import codecs
import keras_preprocessing.text as kpt


model_filename = 'best.ckpt'

# source text file information
encoding = 'utf-8'
fname = 'holmes_canon.txt'
origin = 'https://sherlock-holm.es/stories/plain-text/cnus.txt'

# how to tokenize the text
char_level = True

# how to split the tokens into training and validation data
validation_split = 0.2

# how to arrange the tokens into batches of sequences and targets
timesteps = 256
batch_size = 256

num_validation_steps = 50

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

validation_tokens = tokens[num_training_tokens:]


def dataset_from_tokens(tokens, timesteps, batch_size):

    num_tokens = len(tokens)
    stride_size = timesteps + 1
    num_strides = num_tokens / stride_size
    num_take_tokens = num_strides * stride_size + 1
    shuffle_size = num_strides

    dataset = tf.data.Dataset.from_tensor_slices(tokens)
    dataset = dataset.take(num_take_tokens)
    dataset = dataset.repeat()
    dataset = dataset.batch(stride_size)
    dataset = dataset.map(lambda x: [x[:-1], x[-1]])
    dataset = dataset.shuffle(shuffle_size)
    dataset = dataset.batch(batch_size)

    return dataset


validation_dataset = dataset_from_tokens(
    validation_tokens, timesteps, batch_size)

model = tf.keras.models.load_model(model_filename)

score = model.evaluate(validation_dataset, steps=num_validation_steps)

print score
