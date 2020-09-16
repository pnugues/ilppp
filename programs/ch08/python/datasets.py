"""
Functions to load CoNLL datasets.
Some of the corpora are available from github.
For some others, you need to obtain them from LDC or other sources
and store them in your computer. You will have to edit the paths.
"""
__author__ = "Pierre Nugues"

import sys, os
import numpy as np
from os.path import join, dirname
from urllib.request import urlopen

sys.path.append(join(dirname(__file__), '..', '..'))

from ch06.python.conll_dictorizer import CoNLLDictorizer


def load_conll2009_pos(BASE_DIR='/Users/pierre/Documents/Cours/EDAN20/corpus/conll2009/'):
    """
    The CoNLL English corpus up to the parts of speech
    :param BASE_DIR:
    :return:
    """
    train_file = BASE_DIR + 'en/CoNLL2009-ST-English-train-pos.txt'
    dev_file = BASE_DIR + 'en/CoNLL2009-ST-English-development-pos.txt'
    test_file = BASE_DIR + 'en/CoNLL2009-ST-test-words-pos.txt'
    test2_file = join(dirname(__file__), 'simple_pos_test.txt')

    column_names = ['ID', 'FORM', 'LEMMA', 'PLEMMA', 'POS', 'PPOS']

    column_names = list(map(str.lower, column_names))
    train_sentences = open(train_file).read().strip()
    dev_sentences = open(dev_file).read().strip()
    test_sentences = open(test_file).read().strip()
    test2_sentences = open(test2_file).read().strip()
    return train_sentences, dev_sentences, test_sentences, column_names


def load_conll2003_en(BASE_DIR='/Users/pierre/Projets/Corpora/CoNLL2003/'):
    """
    CoNLL 2003
    Source: https://www.clips.uantwerpen.be/conll2003/ner/
    :param BASE_DIR:
    :return:
    """
    train_file = BASE_DIR + 'NER-data/eng.train'
    dev_file = BASE_DIR + 'NER-data/eng.valid'
    test_file = BASE_DIR + 'NER-data/eng.test'

    column_names = ['FORM', 'PPOS', 'PCHUNK', 'NER']

    column_names = list(map(str.lower, column_names))
    train_sentences = open(train_file).read().strip()
    dev_sentences = open(dev_file).read().strip()
    test_sentences = open(test_file).read().strip()
    return train_sentences, dev_sentences, test_sentences, column_names


def load_ud_en_ewt(url='https://raw.githubusercontent.com/UniversalDependencies/UD_English-EWT/master/'):
    """
    The English Web treebank from github
    Source: https://universaldependencies.org/
    :param url:
    :return:
    """
    train_file = url + 'en_ewt-ud-train.conllu'
    dev_file = url + 'en_ewt-ud-dev.conllu'
    test_file = url + 'en_ewt-ud-test.conllu'

    column_names = ['ID', 'FORM', 'LEMMA', 'UPOS', 'XPOS',
                    'FEATS', 'HEAD', 'DEPREL', 'HEAD', 'DEPS', 'MISC']

    column_names = list(map(str.lower, column_names))
    train_sentences = urlopen(train_file).read().decode('utf-8').strip()
    dev_sentences = urlopen(dev_file).read().decode('utf-8').strip()
    test_sentences = urlopen(test_file).read().decode('utf-8').strip()
    return train_sentences, dev_sentences, test_sentences, column_names


def load_ud_sv_talbanken(url='https://raw.githubusercontent.com/UniversalDependencies/UD_Swedish-Talbanken/master/'):
    """
    The Swedish talbanken from the Universal Dependency corpus.
    Changed column name UPOS to POS
    Source: https://universaldependencies.org/
    :param url:
    :return:
    """
    train_file = url + 'sv_talbanken-ud-train.conllu'
    dev_file = url + 'sv_talbanken-ud-dev.conllu'
    test_file = url + 'sv_talbanken-ud-test.conllu'

    column_names = ['ID', 'FORM', 'LEMMA', 'UPOS', 'XPOS',
                    'FEATS', 'HEAD', 'DEPREL', 'HEAD', 'DEPS', 'MISC']

    column_names = list(map(str.lower, column_names))
    train_sentences = urlopen(train_file).read().decode('utf-8').strip()
    dev_sentences = urlopen(dev_file).read().decode('utf-8').strip()
    test_sentences = urlopen(test_file).read().decode('utf-8').strip()
    return train_sentences, dev_sentences, test_sentences, column_names


def load_ud_fr_gsd(url='https://raw.githubusercontent.com/UniversalDependencies/UD_French-GSD/master/'):
    """
    French Universal Dependency corpus.
    Changed column name UPOS to POS
    :param url:
    :return:
    """
    train_file = url + 'fr_gsd-ud-train.conllu'
    dev_file = url + 'fr_gsd-ud-dev.conllu'
    test_file = url + 'fr_gsd-ud-test.conllu'

    column_names = ['ID', 'FORM', 'LEMMA', 'UPOS', 'XPOS',
                    'FEATS', 'HEAD', 'DEPREL', 'HEAD', 'DEPS', 'MISC']

    column_names = list(map(str.lower, column_names))
    train_sentences = urlopen(train_file).read().decode('utf-8').strip()
    dev_sentences = urlopen(dev_file).read().decode('utf-8').strip()
    test_sentences = urlopen(test_file).read().decode('utf-8').strip()
    return train_sentences, dev_sentences, test_sentences, column_names


def load_suc_3(BASE_DIR='/Users/pierre/Projets/Corpora/svenska/SUC3.0/corpus/conll/'):
    """
    The Swedish SUC corpus
    Source: https://spraakbanken.gu.se/swe/resurs/suc3
    :param BASE_DIR:
    :return:
    """
    train_file = BASE_DIR + 'suc-train.conll'
    dev_file = BASE_DIR + 'suc-dev.conll'
    test_file = BASE_DIR + 'suc-test.conll'

    column_names = ['ID', 'FORM', 'LEMMA', 'POS', 'XPOS', 'FEATS',
                    'HEAD', 'DEPREL', 'CHUNK_TAG', 'CHUNK_TYPE',
                    'NER_TAG', 'NER_TYPE', 'SENT_TOK_ID']

    column_names = list(map(str.lower, column_names))
    train_sentences = open(train_file).read().strip()
    dev_sentences = open(dev_file).read().strip()
    test_sentences = open(test_file).read().strip()
    return train_sentences, dev_sentences, test_sentences, column_names


def load_glove_vectors(BASE_DIR='/Users/pierre/Documents/Cours/EDAN20/corpus/'):
    """
    Return the Glove embeddings in the from of a dictionary
    Source: https://nlp.stanford.edu/projects/glove/
    :param file:
    :return:
    """
    fname = BASE_DIR + 'glove.6B.100d.txt'
    fobj = open(fname, encoding='utf8')
    embeddings_dict = {}
    for line in fobj:
        values = line.strip().split()
        word = values[0]
        embeddings_dict[word] = np.array(values[1:]).astype(np.float32)
    fobj.close()
    return embeddings_dict


def load_fasttext_vectors(BASE_DIR='/Users/pierre/Documents/Cours/EDAN20/corpus/', lc=True):
    """
    Returns the Fasttext embeddings
    Source: https://fasttext.cc/docs/en/english-vectors.html
    :param BASE_DIR:
    :param lc:
    :return:
    """
    fname = BASE_DIR + 'wiki-news-300d-1M-subword.vec'
    fobj = open(fname)
    n, d = map(int, fobj.readline().split())
    # print(n, d)
    embeddings_dict = {}
    for line in fobj:
        values = line.strip().split()
        word = values[0]
        if lc:
            word = word.lower()
            if word in embeddings_dict:
                continue
        embeddings_dict[word] = np.array(values[1:]).astype(np.float32)
    return embeddings_dict


if __name__ == '__main__':
    train_sentences, dev_sentences, test_sentences, column_names = load_conll2009_pos()
    conll_dict = CoNLLDictorizer(column_names)
    train_dict = conll_dict.transform(train_sentences)
    print(train_dict[0])
    print(train_dict[1])

    train_sentences, dev_sentences, test_sentences, column_names = load_conll2003_en()
    conll_dict = CoNLLDictorizer(column_names, col_sep=' ')
    train_dict = conll_dict.transform(train_sentences)
    print(train_dict[0])
    print(train_dict[1])

    train_sentences, dev_sentences, test_sentences, column_names = load_ud_en_ewt()
    conll_dict = CoNLLDictorizer(column_names)
    train_dict = conll_dict.transform(train_sentences)
    print(train_dict[0])
    print(train_dict[1])

    train_sentences, dev_sentences, test_sentences, column_names = load_suc_3()
    conll_dict = CoNLLDictorizer(column_names, col_sep='\t')
    train_dict = conll_dict.transform(train_sentences)
    print(train_dict[0])
    print(train_dict[1])

    embeddings_dict = load_glove_vectors()
    print(embeddings_dict['table'])

    embeddings_dict = load_fasttext_vectors()
    print(embeddings_dict['table'])
