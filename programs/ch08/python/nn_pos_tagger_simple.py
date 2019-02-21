"""
Implementation of a simple feed forward neural network
"""
__author__ = "Pierre Nugues"

import sys
import os
import time
import datasets
from context_dictorizer import ContextDictorizer
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction import DictVectorizer
from keras import models, layers, callbacks
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')))

from ch06.python.conll_dictorizer import CoNLLDictorizer

OPTIMIZER = 'rmsprop'
SCALER = True
NUM_LAYERS = 1  # 1 --> one layer, 2 --> two layers
DROPOUT = 0.0  # Dropout between the two layers
BATCH_SIZE = 128
EPOCHS = 100
MINI_CORPUS = False
CORPUS = 'EWT'  # 'EWT' or 'PTB'
SAVE_MODEL = False
VILDE = False  # The computing machine

config = {'Optimizer': OPTIMIZER, 'Scaler': SCALER, 'Layers': NUM_LAYERS,
          'Dropout': DROPOUT, 'Batch size': BATCH_SIZE, 'Epochs': EPOCHS,
          'Corpus': CORPUS, 'Mini corpus': MINI_CORPUS}


def predict_sentence(sent_dict, model, context_dictorizer,
                     dict_vect, scaler, idx2pos):
    """
    Prediction of parts of speech
    :param sentence: A list of words
    :param dict_vect:
    :param model:
    :param idx2pos:
    :return:
    """
    X_dict, y = context_dictorizer.transform([sent_dict],
                                             training_step=False)
    X_num = dict_vect.transform(X_dict)
    if scaler:
        X = scaler.transform(X_num)
    else:
        X = X_num
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


def build_model(input_dim,
                output_dim,
                num_layers=1,
                dropout=0.0,
                optimizer='rmsprop'):
    model = models.Sequential()
    if num_layers == 1:
        model.add(layers.Dense(output_dim,
                               input_dim=input_dim,
                               activation='softmax'))
    else:
        model.add(layers.Dense(output_dim,
                               input_dim=input_dim,
                               activation='relu'))
        model.add(layers.Dropout(dropout))
        model.add(layers.Dense(output_dim,
                               activation='softmax'))

    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer=optimizer,
                  metrics=['accuracy'])
    model.summary()
    return model


def main():
    start_time = time.perf_counter()

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

    # Convert the corpus in a dictionary
    conll_dict = CoNLLDictorizer(column_names)
    train_dict = conll_dict.transform(train_sentences)
    dev_dict = conll_dict.transform(dev_sentences)
    if MINI_CORPUS:
        train_dict = train_dict[:len(train_dict) // 10]
    test_dict = conll_dict.transform(test_sentences)

    # Extract the context and dictorize it
    context_dictorizer = ContextDictorizer()
    context_dictorizer.fit(train_dict)
    X_dict_train, y_cat_train = context_dictorizer.transform(train_dict)
    X_dict_dev, y_cat_dev = context_dictorizer.transform(dev_dict)

    # Transform the X symbols into numbers
    dict_vectorizer = DictVectorizer()
    X_num_train = dict_vectorizer.fit_transform(X_dict_train)
    X_num_dev = dict_vectorizer.transform(X_dict_dev)

    scaler = None
    if SCALER:
        # Standardize X_num
        scaler = StandardScaler(with_mean=False)
        X = scaler.fit_transform(X_num_train)
        X_dev = scaler.transform(X_num_dev)
    else:
        X = X_num_train
        X_dev = X_num_dev

    # Vectorizing y
    # The POS and the number of different POS
    pos_list = sorted(set(y_cat_train))
    NB_CLASSES = len(pos_list)

    # We build a part-of-speech index.
    idx2pos = dict(enumerate(pos_list))
    pos2idx = {v: k for k, v in idx2pos.items()}

    # We encode y. We assign unknown parts of speech to 0 in the test set
    y = [pos2idx[i] for i in y_cat_train]
    y_dev = [pos2idx.get(i, 0) for i in y_cat_dev]

    # The tagger
    np.random.seed(0)
    model = build_model(X.shape[1],
                        NB_CLASSES,
                        num_layers=NUM_LAYERS,
                        dropout=DROPOUT)

    # Callback to stop when the validation score does not increase
    # and keep the best model
    callback_lists = [
        callbacks.EarlyStopping(
            monitor='val_acc',
            patience=2,
            restore_best_weights=True
        )
    ]
    # Fitting the model
    history = model.fit(X, y,
                        epochs=EPOCHS,
                        batch_size=BATCH_SIZE,
                        callbacks=callback_lists,
                        validation_data=(X_dev, y_dev))
    if SAVE_MODEL:
        model.save(config + '.h5')

    # Formatting the test set
    X_test_dict, y_test_cat = context_dictorizer.transform(test_dict)

    # We transform the symbols into numbers
    X_test_num = dict_vectorizer.transform(X_test_dict)
    if scaler:
        X_test = scaler.transform(X_test_num)
    else:
        X_test = X_test_num
    y_test = [pos2idx.get(i, 0) for i in y_test_cat]

    # Evaluate the model
    test_loss, test_acc = model.evaluate(X_test, y_test)

    print('Configuration', config)
    print('Loss:', test_loss)
    print('Accuracy:', test_acc)
    print('Time:', (time.perf_counter() - start_time) / 60)

    # Evaluation on the test set
    total = 0
    correct = 0
    print('#Sentences', len(test_dict))
    for sentence in test_dict:
        y_pred = predict_sentence(sentence,
                                  model,
                                  context_dictorizer,
                                  dict_vectorizer,
                                  scaler,
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
        y_test_pred_cat = predict_sentence(sent_dict,
                                           model,
                                           context_dictorizer,
                                           dict_vectorizer,
                                           scaler,
                                           idx2pos)
        print([y['form'] for y in y_test_pred_cat])
        print([y['ppos'] for y in y_test_pred_cat])

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
