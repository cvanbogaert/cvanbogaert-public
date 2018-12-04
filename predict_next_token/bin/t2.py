import tensorflow as tf
from tensorflow.keras.layers import InputLayer, Embedding, CuDNNLSTM, LSTM, Dense, Dropout
import numpy as np
import time
import codecs
import keras_preprocessing.text as kpt
import json

batch_size = 256
num_units = 256
num_layers = 2
dropout = 0.5
num_timesteps = 8
embedding_size = 16
validation_split = 0.25

# source text file information
encoding = 'utf-8'
#fname = 'holmes_canon.txt'
#origin = 'https://sherlock-holm.es/stories/plain-text/cnus.txt'

# how to tokenize the text
char_level = True
vocab_filename = 'vocab.json'

# fetch the file
#filename = tf.keras.utils.get_file(fname, origin)

filename = '/media/cvanbogaert/data/OANC-GrAF/subset.txt'

with codecs.open(filename, encoding=encoding) as file:
    text = file.read()

# tokenize the text
t = kpt.Tokenizer(char_level=char_level)
t.fit_on_texts([text])
tokens = np.array(t.texts_to_sequences([text])[0])

vocab = t.word_index
num_classes = len(vocab)+1

with codecs.open(vocab_filename, 'w', encoding='utf-8') as f:
    f.write(json.dumps(vocab, sort_keys=True, indent=4))


class CategoricalSequenceFromTokens(tf.keras.utils.Sequence):

    def __init__(self, tokens, batch_size, num_timesteps, num_classes):
        self.tokens = tokens
        self.batch_size = batch_size
        self.num_timesteps = num_timesteps
        self.num_classes = num_classes

        self.num_tokens = len(self.tokens)
#        self.num_batches = int(self.num_tokens/self.num_timesteps)
        self.num_batches = self.num_tokens

        self.base_times = np.random.randint(
            self.num_tokens, high=None, size=self.batch_size)

#        self.on_epoch_end()

    def __len__(self):
        return self.num_batches

    def __getitem__(self, index):

        #        ts = self.base_times + (index * self.num_timesteps)
        ts = self.base_times + index

        data_x = np.array([self.tokens.take(range(
            tx, tx+self.num_timesteps), mode='wrap') for tx in ts])
        data_y = np.array(
            [self.tokens.take((tx+self.num_timesteps), mode='wrap') for tx in ts])
        
        return data_x, data_y

    def on_epoch_end(self):
        self.base_times = np.random.randint(
            self.num_tokens, high=None, size=self.batch_size)

# divide the tokens into training and validation sets
num_tokens = len(tokens)
num_validation_tokens = int(num_tokens * validation_split)
num_training_tokens = num_tokens - num_validation_tokens

training_tokens = tokens[:num_training_tokens]
validation_tokens = tokens[num_training_tokens:]

data_train = CategoricalSequenceFromTokens(
    training_tokens, batch_size, num_timesteps, num_classes)
data_val = CategoricalSequenceFromTokens(
    validation_tokens, batch_size, num_timesteps, num_classes)

# model


def build_model(batch_size, num_classes, num_units, num_layers, dropout, num_timesteps, embedding_size):

    model = tf.keras.models.Sequential()

    model.add(Embedding(num_classes, embedding_size, batch_size=batch_size,
                        input_length=num_timesteps))
    if dropout > 0.0:
        model.add(Dropout(dropout))
    for i in range(num_layers-1):
        model.add(CuDNNLSTM(num_units, stateful=True,
                            return_sequences=True))
    model.add(CuDNNLSTM(num_units, stateful=True))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam', metrics=['accuracy'])

    return model


config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)

model = build_model(batch_size, num_classes, num_units,
                    num_layers, dropout, num_timesteps, embedding_size)
model.summary()


class my_callback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        self.model.reset_states()
# training

callbacks = [
    tf.keras.callbacks.TensorBoard(
        log_dir='logs' + '/' + str(time.time()),
        histogram_freq=0,
        batch_size=batch_size,
        write_graph=True,
        write_grads=True,
        write_images=True),
     tf.keras.callbacks.ModelCheckpoint(
         'best.hdf5',
         monitor='val_acc',
         save_best_only=True, save_weights_only=False),
    my_callback()
]

history = model.fit_generator(generator=data_train,
                              validation_data=data_val,
                              callbacks=callbacks,
                              epochs=5000,
                              steps_per_epoch=3000,
                              validation_steps=3000,
                              shuffle=False, verbose=1)
