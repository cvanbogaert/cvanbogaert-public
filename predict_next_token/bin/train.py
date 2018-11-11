import tensorflow as tf
import keras_preprocessing.text as kpt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import codecs

#tf.enable_eager_execution()

#source text file information
encoding = 'utf-8'
fname = 'holmes_canon.txt'
origin = 'https://sherlock-holm.es/stories/plain-text/cnus.txt'

#how to tokenize the text
char_level = True
max_tokens = 10000000

#how to split the tokens into training and validation data
validation_split = 0.2

#how to arrange the tokens into batches of sequences and targets
timesteps = 256
batch_size = 256
#shuffle_size = 1000

#how to build the model
embedding_size = 16
units = 256
dropout = 0.2

#how to train the model
optimizer='adam'
num_validation_steps=1
device = '/gpu:1'
model_filename='pnt.h5'
checkpoint_filename='pnt_checkpoint.h5'
num_epochs = 250

#how to do the text sample
epochs_per_sample = 10
sample_text_size = 1000
temperature=0.1



#fetch the file
filename = tf.keras.utils.get_file(fname,origin)
with codecs.open(filename,encoding=encoding) as file:
    text = file.read()

#tokenize the text
t = kpt.Tokenizer(char_level=char_level)
t.fit_on_texts([text])
tokens = t.texts_to_sequences([text])[0]
tokens = tokens[:max_tokens]

vocab=t.word_index
vocab_size = len(vocab)

#divide the tokens into training and validation sets
num_tokens=len(tokens)
num_validation_tokens = int(num_tokens*validation_split)
num_training_tokens = num_tokens-num_validation_tokens

training_tokens = tokens[:num_training_tokens]
validation_tokens = tokens[num_training_tokens:]

def dataset_from_tokens(tokens,timesteps,batch_size):
    
    num_tokens = len(tokens)
    stride_size = timesteps+1
    num_strides = num_tokens/stride_size
    num_take_tokens = num_strides*stride_size+1
    shuffle_size = num_strides
    
    dataset = tf.data.Dataset.from_tensor_slices(tokens)
    dataset = dataset.take(num_take_tokens)
    dataset = dataset.repeat()
    dataset = dataset.batch(stride_size)
    dataset = dataset.map(lambda x: [x[:-1],x[-1]])
    dataset = dataset.shuffle(shuffle_size)
    dataset = dataset.batch(batch_size)
    
    return dataset,num_strides

def generate_text(model,timesteps,t,text_size):
    
    vocab=t.word_index
    vocab_size = len(vocab)
    
    inv_vocab = {v: k for k, v in vocab.iteritems()}
    inv_vocab[0] = '\0'
    indexes = np.random.randint(vocab_size,size=timesteps).reshape(1,timesteps)
    predictions = []
    probability_history = []
    
    while len(predictions) < text_size:
        probabilities=model.predict(indexes)[0]

        shape = probabilities.shape
        noise = np.random.normal(loc=0.0, scale=temperature, size=shape)
        probabilities+=noise

        prediction = probabilities.argmax()
        indexes[0,:-1] = indexes[0,1:]; indexes[0,-1] = prediction
        predictions.append(prediction)
        probability_history.append(probabilities)
    
    tokens = map(lambda x: inv_vocab[x], predictions)
    string = ''.join(tokens)
    
    probability_history=np.asarray(probability_history)
    return string,probability_history

class My_Callback(tf.keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        return
    def on_train_end(self, logs={}):
        return
    def on_epoch_begin(self, epoch, logs={}):
        if epoch % epochs_per_sample == 0:
            text,probability_history = generate_text(self.model,timesteps,t,sample_text_size)
            print text
            cmap = plt.cm.hot
	    norm = plt.Normalize(vmin=probability_history.min(), vmax=probability_history.max())
            image = cmap(norm(probability_history))
            plt.imsave('test.png', image)
        return
    def on_epoch_end(self, epoch, logs={}):
        return
    def on_batch_begin(self, batch, logs={}):
        return 
    def on_batch_end(self, batch, logs={}):
        return

with tf.device(device):
    
    training_dataset,training_strides = dataset_from_tokens(training_tokens,timesteps,batch_size)
    validation_dataset,validation_strides = dataset_from_tokens(validation_tokens,timesteps,batch_size)

    steps_per_epoch=int(training_strides/batch_size)
    
    model = tf.keras.models.Sequential()

    model.add(tf.keras.layers.Embedding(vocab_size+1,embedding_size,input_length=timesteps))
    model.add(tf.keras.layers.CuDNNLSTM(units,return_sequences=True))
    model.add(tf.keras.layers.Dropout(dropout)) 
    model.add(tf.keras.layers.CuDNNLSTM(units,return_sequences=True))
    model.add(tf.keras.layers.Dropout(dropout))
    model.add(tf.keras.layers.CuDNNLSTM(units))
    model.add(tf.keras.layers.Dense(vocab_size+1,activation=tf.keras.activations.softmax))

    model.compile(optimizer=optimizer,
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.summary()
    
    callbacks = [My_Callback(),
                tf.keras.callbacks.ModelCheckpoint(checkpoint_filename),
                tf.keras.callbacks.TensorBoard(log_dir='logs',
			histogram_freq=1,
			batch_size=batch_size,
			write_graph=True,
			write_grads=True,
			write_images=True,
			embeddings_freq=0,
			embeddings_layer_names=None,
			embeddings_metadata=None,
			embeddings_data=None)]
          
    score = model.evaluate(validation_dataset,steps=num_validation_steps)
    print score
    
    history = model.fit(training_dataset,
                        epochs=num_epochs,
                        steps_per_epoch=steps_per_epoch,
                        validation_data=validation_dataset,
                        validation_steps=num_validation_steps,
                        callbacks=callbacks)
    
    print history
    
    model.save(model_filename)
    
