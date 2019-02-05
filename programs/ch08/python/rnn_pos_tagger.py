"""
__author__ = "Pierre Nugues"
"""
import sys
import os
import time
import numpy as np
from keras import models, layers, callbacks
from keras.utils import to_categorical
from keras.preprocessing.sequence import pad_sequences
from keras.initializers import Constant
import matplotlib.pyplot as plt
import datasets

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')))

from ch06.python.conll_dictorizer import CoNLLDictorizer

TYPE = 'LSTM'  # 'RNN'  # or 'LSTM'
OPTIMIZER = 'rmsprop'
EMBEDDING_DIM = 100
EMBEDDING_INIT = 4  # Glove
EMBEDDING_INITIALIZER = False
BATCH_SIZE = 128
EPOCHS = 100
UNIT_MULTIPLIER = 4
INPUT_DROPOUT = 0.2
DROPOUT = 0.0
RECURRENT_DROPOUT = 0.2
OUTPUT_DROPOUT = 0.0
PATIENCE = 4
CORPUS = 'EWT'  # or 'PTB'
VILDE = True  # The computing machine

if EMBEDDING_INIT != 4:
    EMBEDDING_INITIALIZER = True

config = {'Type': TYPE, 'Optimizer': OPTIMIZER, 'Embedding dim': EMBEDDING_DIM,
          'Unit multiplier': UNIT_MULTIPLIER, 'Input dropout': INPUT_DROPOUT,
          'Internal dropout': DROPOUT,
          'Recurrent dropout': RECURRENT_DROPOUT, 'Output dropout': OUTPUT_DROPOUT,
          'Embedding init': EMBEDDING_INIT, 'Batch size': BATCH_SIZE,
          'Epochs': EPOCHS, 'Corpus': CORPUS}


def build_sequences(corpus_dict,
                    key_x='form',
                    key_y='pos',
                    tolower=True):
    """
    Creates sequences from a list of dictionaries
    :param corpus_dict:
    :param key_x:
    :param key_y:
    :return:
    """
    X = []
    Y = []
    for sentence in corpus_dict:
        x = [word[key_x] for word in sentence]
        y = [word[key_y] for word in sentence]
        if tolower:
            x = list(map(str.lower, x))
        X += [x]
        Y += [y]
    return X, Y


def to_index(X, idx):
    """
    Convert the word lists (or POS lists) to indexes
    :param X: List of word (or POS) lists
    :param idx: word to number dictionary
    :return:
    """
    X_idx = []
    for x in X:
        # We map the unknown symbols to one
        x_idx = list(map(lambda x: idx.get(x, 1), x))
        X_idx += [x_idx]
    return X_idx


def predict_wordlist(x, model, word2idx, idx2pos):
    x_idx = to_index([x], word2idx)
    y_idx_pred_prob = model.predict(np.array(x_idx))
    # Select the highest prob
    y_idx = np.argmax(y_idx_pred_prob, axis=-1)[0]
    # Convert to POS idx to symbols
    y_pred = list(map(idx2pos.get, y_idx))
    return y_pred


def predict_sentence(sentence, model, word2idx, idx2pos, verbose=False):
    # Predict one sentence
    wordlist = sentence.split()
    poslist = predict_wordlist(wordlist, model, word2idx, idx2pos)
    return poslist


def predict_padded_testset(X_test_cat, model, word2idx, idx2pos):
    # We evaluate on all the test corpus
    X_test_idx = to_index(X_test_cat, word2idx)
    X_test_padded = pad_sequences(X_test_idx)
    Y_test_pred_padded_vect = model.predict(X_test_padded)

    # Remove padding
    Y_test_pred_vect = []
    for sent_nbr, sent_pos_predictions in enumerate(Y_test_pred_padded_vect):
        Y_test_pred_vect += [sent_pos_predictions[-len(X_test_cat[sent_nbr]):]]

    # Convert to POS idx to symbols
    Y_test_pred = []
    for y_test_pred_vect in Y_test_pred_vect:
        pos_idx = np.argmax(y_test_pred_vect, axis=-1)
        pos_cat = list(map(idx2pos.get, pos_idx))
        Y_test_pred += [pos_cat]
    return Y_test_pred


def eval(X_test_cat, Y_test_cat, Y_test_pred, word2idx):
    total, correct, total_ukn, correct_ukn = 0, 0, 0, 0
    for id_s, x_test_cat in enumerate(X_test_cat):
        for id_w, word in enumerate(x_test_cat):
            total += 1
            if Y_test_pred[id_s][id_w] == Y_test_cat[id_s][id_w]:
                correct += 1
            # The word is not in the dictionary
            if word not in word2idx:
                total_ukn += 1
                if Y_test_pred[id_s][id_w] == Y_test_cat[id_s][id_w]:
                    correct_ukn += 1
    return total, correct, total_ukn, correct_ukn


start_time = time.perf_counter()
print('Starting:', config)

# Loading the corpus
if CORPUS == 'EWT':
    train_sentences, dev_sentences, test_sentences, column_names = \
        datasets.load_ud_en_ewt()
else:  # PTB
    if VILDE:
        train_sentences, dev_sentences, test_sentences, column_names = \
            datasets.load_conll2009_pos(
                BASE_DIR='/home/pierre/Cours/EDAN20/corpus/conll2009/')
    else:
        train_sentences, dev_sentences, test_sentences, column_names = \
            datasets.load_conll2009_pos()

conll_dict = CoNLLDictorizer(column_names)
train_dict = conll_dict.transform(train_sentences)
dev_dict = conll_dict.transform(dev_sentences)
test_dict = conll_dict.transform(test_sentences)

X_train_cat, Y_train_cat = build_sequences(train_dict)
X_dev_cat, Y_dev_cat = build_sequences(dev_dict)
print('First sentence, words', X_train_cat[0])
print('First sentence, POS', Y_train_cat[0])

# We collect the words, parts of speech and we create the indices
vocabulary_words = sorted(set([word
                               for sentence in X_train_cat
                               for word in sentence]))
print('#', len(vocabulary_words), 'words')

# If we use an embedding matrix, we collect the words in the file
if EMBEDDING_INIT == 4:
    if VILDE:
        embeddings_dict = datasets.load_embeddings(
            BASE_DIR='/home/pierre/Cours/EDAN20/corpus/')
    else:
        embeddings_dict = datasets.load_embeddings()
    embeddings_words = embeddings_dict.keys()
    print('Words in GloVe:', len(embeddings_dict.keys()))
    vocabulary_words = sorted(set(vocabulary_words +
                                  list(embeddings_words)))
    print('# unique words in the vocabulary: embeddings and corpus:',
          len(vocabulary_words))

pos = sorted(set([pos
                  for sentence in Y_train_cat
                  for pos in sentence]))
NB_CLASSES = len(pos)
print('#', NB_CLASSES, 'Parts of speech:', pos)

# We create the indexes
# We start at two to make provision for
# the padding symbol 0 in RNN and LSTMs and unknown words, 1
idx2word = dict(enumerate(vocabulary_words, start=2))
idx2pos = dict(enumerate(pos, start=1))
word2idx = {v: k for k, v in idx2word.items()}
pos2idx = {v: k for k, v in idx2pos.items()}
print('word index:', list(word2idx.items())[:10])
print('POS index:', list(pos2idx.items())[:10])

# We create the parallel sequences of indexes
X_train_idx = to_index(X_train_cat, word2idx)
Y_train_idx = to_index(Y_train_cat, pos2idx)
X_dev_idx = to_index(X_dev_cat, word2idx)
Y_dev_idx = to_index(Y_dev_cat, pos2idx)
print('First sentences, word indices', X_train_idx[:3])
print('First sentences, POS indices', Y_train_idx[:3])

X_train = pad_sequences(X_train_idx)
Y_train = pad_sequences(Y_train_idx)
X_dev = pad_sequences(X_dev_idx)
Y_dev = pad_sequences(Y_dev_idx)
print('Padded X:', X_train[0])
print('Padded Y:', Y_train[0])

# The number of POS classes, and 0 (padding symbol)
Y_train = to_categorical(Y_train, num_classes=len(pos) + 1)
Y_dev = to_categorical(Y_dev, num_classes=len(pos) + 1)
print('Padded categorical Y:', Y_train[0])

np.random.seed(1234567)
if EMBEDDING_INIT == 1:
    # One hot encoding: very large matrix
    EMBEDDING_DIM = len(vocabulary_words) + 2
    embedding_matrix = np.eye(len(vocabulary_words) + 2)
    embed_init = 'identity'
elif EMBEDDING_INIT == 2:  # Embeddings with a random init
    embed_init = 'uniform'
elif EMBEDDING_INIT == 3:  # Embeddings with a zero init
    embed_init = 'zeros'
elif EMBEDDING_INIT == 4:  # GloVe
    EMBEDDING_DIM = 100
    embedding_matrix = np.random.uniform(-0.05, 0.05,
                                         (len(vocabulary_words) + 2,
                                          EMBEDDING_DIM)
                                         ).astype(np.float32)
    # We initialize the matrix with embeddings
    for word in vocabulary_words:
        if word in embeddings_dict:
            # If the words are in the embeddings,
            # we fill them with a value
            embedding_matrix[word2idx[word]] = embeddings_dict[word]
    if EMBEDDING_INITIALIZER:
        embed_init = Constant(embedding_matrix)

    # print('Embedding:', embedding_matrix)
    print('Shape of embedding matrix:', embedding_matrix.shape)
    print('Embedding of table', embedding_matrix[word2idx['table']])
    print('Embedding of the padding symbol, idx 0, random numbers', embedding_matrix[0])

model = models.Sequential()
if not EMBEDDING_INITIALIZER:  # We use the weights
    model.add(layers.Embedding(len(vocabulary_words) + 2,
                               EMBEDDING_DIM,
                               weights=[embedding_matrix],
                               trainable=True,
                               mask_zero=True))
else:
    model.add(layers.Embedding(len(vocabulary_words) + 2,
                               EMBEDDING_DIM,
                               embeddings_initializer=embed_init,
                               trainable=True,
                               mask_zero=True))
model.add(layers.Dropout(INPUT_DROPOUT))
if TYPE == 'RNN':
    model.add(layers.Bidirectional(
        layers.SimpleRNN(UNIT_MULTIPLIER * (NB_CLASSES + 1),
                         return_sequences=True,
                         dropout=DROPOUT,
                         recurrent_dropout=RECURRENT_DROPOUT)))
else:
    model.add(layers.Bidirectional(
        layers.LSTM(UNIT_MULTIPLIER * (NB_CLASSES + 1),
                    return_sequences=True,
                    dropout=DROPOUT,
                    recurrent_dropout=RECURRENT_DROPOUT)))
model.add(layers.Dropout(OUTPUT_DROPOUT))
model.add(layers.Dense(NB_CLASSES + 1, activation='softmax'))
model.compile(loss='categorical_crossentropy',
              optimizer=OPTIMIZER,
              metrics=['acc'])
model.summary()

# Callback to stop when the validation score does not increase
# and keep the best model
callback_lists = [
    callbacks.EarlyStopping(
        monitor='val_acc',
        patience=PATIENCE,
        restore_best_weights=True
    )
]
# Fitting the model
history = model.fit(X_train, Y_train,
                    epochs=EPOCHS,
                    batch_size=BATCH_SIZE,
                    callbacks=callback_lists,
                    validation_data=(X_dev, Y_dev))

# In X_dict, we replace the words with their index
X_test_cat, Y_test_cat = build_sequences(test_dict)

# We create the parallel sequences of indexes
X_test_idx = to_index(X_test_cat, word2idx)
Y_test_idx = to_index(Y_test_cat, pos2idx)
print('X[0] test idx', X_test_idx[0])
print('Y[0] test idx', Y_test_idx[0])

X_test_padded = pad_sequences(X_test_idx)
Y_test_padded = pad_sequences(Y_test_idx)
print('X[0] test idx padded', X_test_padded[0])
print('Y[0] test idx padded', Y_test_padded[0])

# One extra symbol for 0 (padding)
Y_test_padded_vectorized = to_categorical(Y_test_padded,
                                          num_classes=len(pos) + 1)
print('Y[0] test idx padded vectorized', Y_test_padded_vectorized[0])

print(X_test_padded.shape)
print(Y_test_padded_vectorized.shape)

# Evaluates the model
test_loss, test_acc = model.evaluate(X_test_padded,
                                     Y_test_padded_vectorized)
print('Batch evaluation')
print('Configuration', config)
print('Loss:', test_loss)
print('Accuracy:', test_acc)
print('Time:', (time.perf_counter() - start_time) / 60)

print('Evaluation of padded sentences')
Y_test_pred = predict_padded_testset(X_test_cat, model, word2idx, idx2pos)
total, correct, total_ukn, correct_ukn = eval(X_test_cat, Y_test_cat, Y_test_pred, word2idx)
print('total %d, correct %d, accuracy %f' % (total, correct, correct / total))
if total_ukn != 0:
    print('total unknown %d, correct %d, accuracy %f' % (total_ukn, correct_ukn, correct_ukn / total_ukn))

print('Evaluation of individual sentences')
Y_test_pred = [predict_wordlist(x, model, word2idx, idx2pos)
               for x in X_test_cat]
total, correct, total_ukn, correct_ukn = eval(X_test_cat, Y_test_cat, Y_test_pred, word2idx)
print('total %d, correct %d, accuracy %f' % (total, correct, correct / total))
if total_ukn != 0:
    print('total unknown %d, correct %d, accuracy %f' % (total_ukn, correct_ukn, correct_ukn / total_ukn))

# Tagging a few sentences
sentences = ['That round table might collapse .',
             'The man can learn well .',
             'The man can swim .',
             'The man can simwo .',
             'that round table might collapsex', ]
for sentence in sentences:
    y_test_pred_cat = predict_sentence(sentence.lower(), model, word2idx, idx2pos)
    print(sentence)
    print(y_test_pred_cat)

# Show the training curves
loss = history.history['loss']
val_loss = history.history['val_loss']
acc = history.history['acc']
val_acc = history.history['val_acc']

epochs = range(1, len(acc) + 1)
plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.plot('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

plt.clf()

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.show()
