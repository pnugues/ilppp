"""
Implementation of a simple feed forward neural network
with embeddings

"""
__author__ = "Pierre Nugues"

import sys
import os
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from keras import models, layers, callbacks
import matplotlib.pyplot as plt
from context_dictorizer import ContextDictorizer
import datasets

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')))

from ch06.python.conll_dictorizer import CoNLLDictorizer

CORPUS = 'EWT'  # 'EWT' or 'PTB'
MINI_CORPUS = False
OPTIMIZER = 'nadam'
EMBEDDING_DIM = 100
W_SIZE = 2
BATCH_SIZE = 128
EPOCHS = 100
VILDE = False  # The computing machine

config = {'Corpus': CORPUS, 'Mini corpus': MINI_CORPUS,
          'Optimizer': OPTIMIZER, 'Embedding dim': EMBEDDING_DIM,
          'Context size': W_SIZE, 'Batch size': BATCH_SIZE, 'Epochs': EPOCHS}


def predict_sentence(sent_dict, model, context_dictorizer,
                     dict_vect, word2idx, idx2pos):
    X_dict, y = context_dictorizer.transform([sent_dict],
                                             training_step=False)
    for x_dict in X_dict:
        for word in x_dict:
            x_dict[word] = word2idx.get(x_dict[word], 1)
    X = dict_vect.transform(X_dict)

    y_prob = model.predict(X)
    y_pred = y_prob.argmax(axis=-1)
    y_pred_cat = [idx2pos[i] for i in y_pred]
    for row, y_pred in zip(sent_dict, y_pred_cat):
        row['ppos'] = y_pred
    return sent_dict


def sentence_to_conll(sentence):
    """
    Convert a sentence to a CoNLL dict
    :param sentence:
    :return:
    """
    column_names = ['id', 'form']
    sentence = list(enumerate(sentence.split(), start=1))
    conll_cols = ''
    for tuple in sentence:
        conll_cols += str(tuple[0]) + '\t' + tuple[1] + '\n'

    conll_dict = CoNLLDictorizer(column_names)
    sent_dict = conll_dict.transform(conll_cols)
    return sent_dict[0]


def main():
    # Loading the embeddings
    if VILDE:
        embeddings_dict = datasets.load_glove_vectors(
            BASE_DIR='/home/pierre/Cours/EDAN20/corpus/')
    else:
        embeddings_dict = datasets.load_glove_vectors()
    print('Embeddings table:', embeddings_dict['table'])

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
    if MINI_CORPUS:
        train_dict = train_dict[:len(train_dict) // 15]
    test_dict = conll_dict.transform(test_sentences)
    print('First sentence, train:', train_dict[0])

    context_dictorizer = ContextDictorizer()
    context_dictorizer.fit(train_dict)
    X_dict_train, y_cat_train = context_dictorizer.transform(train_dict)
    X_dict_dev, y_cat_dev = context_dictorizer.transform(dev_dict)

    corpus_words = [value for x in X_dict_train
                    for value in x.values()]
    corpus_words = sorted(set(corpus_words))
    print('# unique words seen in training corpus:', len(corpus_words))

    embeddings_words = embeddings_dict.keys()
    print('Words in GloVe:', len(embeddings_dict.keys()))
    vocabulary_words = set(corpus_words + list(embeddings_words))

    # We start at 1, 0 is the unknown word
    idx2word = dict(enumerate(vocabulary_words, start=1))
    word2idx = {v: k for k, v in idx2word.items()}
    cnt_uniq = len(vocabulary_words) + 1
    print('# unique words in the vocabulary: embeddings and corpus:',
          len(vocabulary_words) + 1)

    for x_dict in X_dict_train:
        for word in x_dict:
            x_dict[word] = word2idx[x_dict[word]]
    for x_dict in X_dict_dev:
        for word in x_dict:
            x_dict[word] = word2idx.get(x_dict[word], 0)

    np.random.seed(0)
    dict_vectorizer = DictVectorizer(sparse=False)
    X = dict_vectorizer.fit_transform(X_dict_train)
    X_dev = dict_vectorizer.transform(X_dict_dev)

    print('X shape', X.shape)
    print('First line of X:', X[0])

    # The POS and the number of different POS
    pos_list = sorted(set(y_cat_train))
    NB_CLASSES = len(pos_list)

    # We build a part-of-speech index.
    idx2pos = dict(enumerate(pos_list))
    pos2idx = {v: k for k, v in idx2pos.items()}

    # We encode y
    y = [pos2idx[i] for i in y_cat_train]
    print(y_cat_train[:10])
    y_dev = [pos2idx[i] for i in y_cat_dev]

    embedding_matrix = np.random.random((cnt_uniq,
                                         EMBEDDING_DIM))
    # Same init as with Keras (-0.05, 0.05)
    # embedding_matrix = (embedding_matrix - 0.5) / 10.0

    for word in vocabulary_words:
        if word in embeddings_dict:
            # If the words are in the pretrained embeddings,
            # we fill them with this embedding value
            embedding_matrix[word2idx[word]] = embeddings_dict[word]

    model = models.Sequential()
    model.add(layers.Embedding(cnt_uniq, EMBEDDING_DIM,
                               weights=[embedding_matrix],
                               trainable=True,
                               input_length=2 * W_SIZE + 1))
    model.add(layers.Flatten())
    model.add(layers.Dense(NB_CLASSES, activation='softmax'))
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer=OPTIMIZER,
                  metrics=['accuracy'])
    model.summary()

    # Fitting the model
    callback_lists = [
        callbacks.EarlyStopping(
            monitor='val_acc',
            patience=2,
            restore_best_weights=True
        )
    ]
    # Callback to stop when the validation score does not increase
    # and keep the best model
    history = model.fit(X, y,
                        epochs=EPOCHS,
                        batch_size=BATCH_SIZE,
                        callbacks=callback_lists,
                        validation_data=(X_dev, y_dev))

    X_test_dict, y_test_cat = context_dictorizer.transform(test_dict)
    for x_dict_test in X_test_dict:
        for word in x_dict_test:
            x_dict_test[word] = word2idx.get(x_dict_test[word], 0)

    # We transform the symbols into numbers
    X_test = dict_vectorizer.transform(X_test_dict)
    y_test = [pos2idx.get(i, 0) for i in y_test_cat]

    test_loss, test_acc = model.evaluate(X_test, y_test)
    print('Configuration:', config)
    print('Loss:', test_loss)
    print('Accuracy:', test_acc)

    # Evaluation on the test set
    total = 0
    correct = 0
    print('#Sentences', len(test_dict))
    for sentence in test_dict:
        y_pred = predict_sentence(sentence,
                                  model,
                                  context_dictorizer,
                                  dict_vectorizer,
                                  word2idx,
                                  idx2pos)
        for y in y_pred:
            total += 1
            if y['pos'] == y['ppos']:
                correct += 1
    print('total %d, correct %d, accuracy %f' % (total, correct, correct / total))

    # Tag some sentences
    sentences = ['That round table might collapse .',
                 'The man can learn well .',
                 'The man can swim .',
                 'The man can simwo .',
                 'that round table might collapsex']

    for sentence in sentences:
        sent_dict = sentence_to_conll(sentence.lower())
        sent_dict = predict_sentence(sent_dict,
                                     model,
                                     context_dictorizer,
                                     dict_vectorizer,
                                     word2idx,
                                     idx2pos)
        print([word['form'] for word in sent_dict])
        print([word['ppos'] for word in sent_dict])

    # Show the training curves
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    acc = history.history['acc']
    val_acc = history.history['val_acc']

    epochs = range(1, len(acc) + 1)
    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.figure()
    plt.plot(epochs, acc, 'bo', label='Training acc')
    plt.plot(epochs, val_acc, 'b', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
