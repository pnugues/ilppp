# coding=utf-8
"""
IOB to IOBES converter
"""
__author__ = "Pierre Nugues"

import sys
import copy
from os.path import join, dirname

sys.path.append(join(dirname(__file__), '..', '..'))

from ch06.python.conll_dictorizer import CoNLLDictorizer
from ch08.python.datasets import load_conll2003_en

VILDE = False
CONVERSION = 'RESULTS2IOB'  # 'RESULTS2IOB' 'IOB2IOBES' 'IOBES2IOB'

"""
From IOB to IOBES
"""


def I2S(sentence_iob, sentence_iobes, tag='chunk'):
    """
    The pattern it matches:
    O or I-Y or B-Y or start
    I-X -> S-X
    O or I-Y or B-Y or B-X or end
    :param sentence_iob:
    :param sentence_iobes:
    :param tag:
    :return:
    """
    if len(sentence_iob) == 1:
        if sentence_iob[0][tag][0] == 'I':
            sentence_iobes[0][tag] = 'S' + sentence_iob[0][tag][1:]
        return sentence_iobes

    if sentence_iob[0][tag][0] == 'I':
        if sentence_iob[1][tag][0] in ['B', 'O']:
            sentence_iobes[0][tag] = 'S' + sentence_iob[0][tag][1:]
        elif sentence_iob[1][tag][1:] != sentence_iob[0][tag][1:]:
            sentence_iobes[0][tag] = 'S' + sentence_iob[0][tag][1:]
    if sentence_iob[-1][tag][0] == 'I':
        if sentence_iob[-2][tag][1:] != sentence_iob[-1][tag][1:]:
            sentence_iobes[-1][tag] = 'S' + sentence_iob[-1][tag][1:]
    if len(sentence_iob) == 2:
        return sentence_iobes

    for i, word in enumerate(sentence_iob[1:-1], start=1):
        if (word[tag][0] == 'I' and
                sentence_iob[i - 1][tag][1:] != word[tag][1:] and
                (sentence_iob[i + 1][tag][0] == 'B'
                 or sentence_iob[i + 1][tag][1:] != word[tag][1:])):
            sentence_iobes[i][tag] = 'S' + word[tag][1:]
    return sentence_iobes


def I2B(sentence_iob, sentence_iobes, tag='chunk'):
    """
    The pattern it matches:
    O or I-Y or B-Y or start
    I-X -> B-X
    I-X
    :param sentence_iob:
    :param sentence_iobes:
    :param tag:
    :return:
    """
    if len(sentence_iob) == 1:
        return sentence_iobes

    if sentence_iob[0][tag][0] == 'I':
        if sentence_iob[0][tag] == sentence_iob[1][tag]:
            sentence_iobes[0][tag] = 'B' + sentence_iob[0][tag][1:]
    if len(sentence_iob) == 2:
        return sentence_iobes

    for i, word in enumerate(sentence_iob[1:-1], start=1):
        if (word[tag][0] == 'I' and
                sentence_iob[i - 1][tag][1:] != word[tag][1:] and
                sentence_iob[i + 1][tag] == word[tag]):
            sentence_iobes[i][tag] = 'B' + word[tag][1:]
    return sentence_iobes


def I2E(sentence_iob, sentence_iobes, tag='chunk'):
    """
    The pattern it matches:
    I-X or B-X
    I-X -> E-X
    I-Y or B or O or end
    :param sentence_iob:
    :param sentence_iobes:
    :param tag:
    :return:
    """
    if len(sentence_iob) == 1:
        return sentence_iobes

    if sentence_iob[-1][tag][0] == 'I':
        if sentence_iob[-2][tag][1:] == sentence_iob[-1][tag][1:]:
            sentence_iobes[-1][tag] = 'E' + sentence_iob[-1][tag][1:]
    if len(sentence_iob) == 2:
        return sentence_iobes

    for i, word in enumerate(sentence_iob[1:-1], start=1):
        if (word[tag][0] == 'I' and
                sentence_iob[i - 1][tag][1:] == word[tag][1:] and
                (sentence_iob[i + 1][tag][0] == 'B'
                 or sentence_iob[i + 1][tag][1:] != word[tag][1:])):
            sentence_iobes[i][tag] = 'E' + word[tag][1:]
    return sentence_iobes


def B2S(sentence_iob, sentence_iobes, tag='chunk'):
    """
    The pattern it matches:
    B-X -> S-X
    O or I-Y or B-X or end
    :param sentence_iob:
    :param sentence_iobes:
    :param tag:
    :return:
    """
    if len(sentence_iob) == 1:
        return sentence_iobes

    if sentence_iob[-1][tag][0] == 'B':
        sentence_iobes[-1][tag] = 'S' + sentence_iob[-1][tag][1:]
    if len(sentence_iob) == 2:
        return sentence_iobes

    for i, word in enumerate(sentence_iob[1:-1], start=1):
        if (word[tag][0] == 'B' and
                (sentence_iob[i + 1][tag][0] == 'B'
                 or sentence_iob[i + 1][tag][1:] != word[tag][1:])):
            sentence_iobes[i][tag] = 'S' + word[tag][1:]
    return sentence_iobes


def iob2iobes(sentence_iob):
    """
    Conversion from IOB (CoNLL 2003) to IOBES
    :param sentence_iob:
    :return:
    """
    sentence_iobes = copy.deepcopy(sentence_iob)
    for tag in ['chunk', 'ner']:
        sentence_iobes = I2S(sentence_iob, sentence_iobes, tag)
        sentence_iobes = I2B(sentence_iob, sentence_iobes, tag)
        sentence_iobes = I2E(sentence_iob, sentence_iobes, tag)
        sentence_iobes = B2S(sentence_iob, sentence_iobes, tag)
    return sentence_iobes


def iob_corpus2iobes(iob_sentences, conll_dict):
    iob_dict = conll_dict.transform(iob_sentences)
    iobes_dict = []
    for sentence in iob_dict:
        new_sentence = iob2iobes(sentence)
        iobes_dict.append(new_sentence)
    return iobes_dict


"""
From IOBES to IOB
"""


def E2I(sentence_iobes, sentence_iob, tag='chunk'):
    """
    The pattern always matches:
    E-X -> I-X
    :param sentence_iob:
    :param sentence_iobes:
    :param tag:
    :return:
    """
    for word_iobes, word_iob in zip(sentence_iobes[1:], sentence_iob[1:]):
        if word_iobes[tag][0] == 'E':
            word_iob[tag] = 'I' + word_iobes[tag][1:]
    return sentence_iob


def B2I(sentence_iobes, sentence_iob, tag='chunk'):
    """
    The pattern it matches:
    -Y
    B-X -> I-X
    :param sentence_iob:
    :param sentence_iobes:
    :param tag:
    :return:
    """
    if sentence_iobes[0][tag][0] == 'B':
        sentence_iob[0][tag] = 'I' + sentence_iob[0][tag][1:]
    if len(sentence_iobes) == 1:
        return sentence_iob

    for i, word in enumerate(sentence_iobes[1:], start=1):
        if (word[tag][0] == 'B' and
                sentence_iobes[i - 1][tag][1:] != word[tag][1:]):
            sentence_iob[i][tag] = 'I' + word[tag][1:]
    return sentence_iob


def S2B(sentence_iobes, sentence_iob, tag='chunk'):
    """
    The pattern it matches:
    -X
    S-X -> B-X
    :param sentence_iobes:
    :param sentence_iob:
    :param tag:
    :return:
    """
    if len(sentence_iobes) == 1:
        return sentence_iob

    for i, word in enumerate(sentence_iobes[1:], start=1):
        if (word[tag][0] == 'S' and
                sentence_iobes[i - 1][tag][1:] == word[tag][1:]):
            sentence_iob[i][tag] = 'B' + word[tag][1:]
    return sentence_iob


def S2I(sentence_iobes, sentence_iob, tag='chunk'):
    """
    The pattern it matches:
    -Y
    S-X -> I-X
    :param sentence_iob:
    :param sentence_iobes:
    :param tag:
    :return:
    """
    if sentence_iobes[0][tag][0] == 'S':
        sentence_iob[0][tag] = 'I' + sentence_iobes[0][tag][1:]
    if len(sentence_iobes) == 1:
        return sentence_iob

    for i, word in enumerate(sentence_iobes[1:], start=1):
        if (word[tag][0] == 'S' and
                sentence_iobes[i - 1][tag][1:] != word[tag][1:]):
            sentence_iob[i][tag] = 'I' + word[tag][1:]
    return sentence_iob


def iobes2iob(sentence_iobes):
    """
    Conversion from IOB (CoNLL 2003) to IOBES
    :param sentence_iob:
    :return:
    """
    sentence_iob = copy.deepcopy(sentence_iobes)
    for tag in ['chunk', 'ner']:
        sentence_iob = E2I(sentence_iobes, sentence_iob, tag)
        sentence_iob = S2I(sentence_iobes, sentence_iob, tag)
        sentence_iob = B2I(sentence_iobes, sentence_iob, tag)
        sentence_iob = S2B(sentence_iobes, sentence_iob, tag)
    return sentence_iob


def iobes_corpus2iob(iobes_sentences, conll_dict):
    iobes_dict = conll_dict.transform(iobes_sentences)
    iob_dict = []
    for sentence in iobes_dict:
        new_sentence = iobes2iob(sentence)
        iob_dict.append(new_sentence)
    return iob_dict


def serialize_conll(corpus_dict, column_names):
    corpus = ''
    for sentence in corpus_dict:
        sentence_str = ''
        for row in sentence:
            items = map(lambda x: row.get(x, '_'), column_names)
            sentence_str += ' '.join(items) + '\n'
        sentence_str += '\n'
        corpus += sentence_str
    return corpus


def convert_corpus(corpus_str, conll_dict, direction='iob2iobes'):
    column_names = conll_dict.column_names
    if direction == 'iob2iobes':
        corpus_dict_iobes = iob_corpus2iobes(corpus_str, conll_dict)
        corpus_iobes = serialize_conll(corpus_dict_iobes, column_names)
        return corpus_iobes
    else:
        corpus_dict_iob = iobes_corpus2iob(corpus_str, conll_dict)
        corpus_iob = serialize_conll(corpus_dict_iob, column_names)
        return corpus_iob


def save(file, corpus):
    """
    Saves the corpus in a file
    :param file:
    :param corpus_dict:
    :param column_names:
    :return:
    """
    with open(file, 'w') as f_out:
        f_out.write(corpus)


if __name__ == '__main__':
    if CONVERSION == 'IOB2IOBES':
        # Conversion from IOB to IOBES
        if VILDE:
            train_sentences, dev_sentences, test_sentences, column_names = load_conll2003_en(
                BASE_DIR='/home/pierre/Cours/EDAN20/corpus/CoNLL2003/')
        else:
            train_sentences, dev_sentences, test_sentences, column_names = load_conll2003_en()
        column_names = ['form', 'pos', 'chunk', 'ner']
        conll_dict = CoNLLDictorizer(column_names, col_sep=' +')
        train_iobes = convert_corpus(train_sentences, conll_dict, direction='iob2iobes')
        dev_iobes = convert_corpus(dev_sentences, conll_dict, direction='iob2iobes')
        test_iobes = convert_corpus(test_sentences, conll_dict, direction='iob2iobes')

        save('NER-data/eng.train', train_iobes)
        save('NER-data/eng.valid', dev_iobes)
        save('NER-data/eng.test', test_iobes)

    if CONVERSION == 'IOBES2IOB':
        # Conversion from IOBES to IOB
        column_names = ['form', 'pos', 'chunk', 'ner']
        conll_dict = CoNLLDictorizer(column_names, col_sep=' +')
        train_iobes, dev_iobes, test_iobes, column_names = load_conll2003_en('./')
        train_iob = convert_corpus(train_iobes, conll_dict, direction='iobes2iob')
        dev_iob = convert_corpus(dev_iobes, conll_dict, direction='iobes2iob')
        test_iob = convert_corpus(test_iobes, conll_dict, direction='iobes2iob')

        save('train_iob.txt', train_iob)
        save('dev_iob.txt', dev_iob)
        save('test_iob.txt', test_iob)

    if CONVERSION == 'RESULTS2IOB':
        column_names = ['form', 'chunk', 'ner']
        conll_dict = CoNLLDictorizer(column_names, col_sep=' +')
        # test_results = 'test_ARCH9.out'
        # test_results_iobes = open(test_results).read().strip()
        test_results_iobes = sys.stdin.read().strip()
        test_results_iob = convert_corpus(test_results_iobes, conll_dict, direction='iobes2iob')
        sys.stdout.write(test_results_iob)
