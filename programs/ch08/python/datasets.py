"""
Program to load CoNLL datasets
"""
import sys, os
import numpy as np
from os.path import join, dirname
from urllib.request import urlopen

sys.path.append(join(dirname(__file__), '..', '..'))

from ch06.python.conll_dictorizer import CoNLLDictorizer


def load_conll2009_pos(BASE_DIR='/Users/pierre/Documents/Cours/EDAN20/corpus/conll2009/'):
    train_file = BASE_DIR + 'en/CoNLL2009-ST-English-train-pos.txt'
    dev_file = BASE_DIR + 'en/CoNLL2009-ST-English-development-pos.txt'
    test_file = BASE_DIR + 'en/CoNLL2009-ST-test-words-pos.txt'
    test2_file = join(dirname(__file__), 'simple_pos_test.txt')

    column_names = ['id', 'form', 'lemma', 'plemma', 'pos', 'ppos']

    train_sentences = open(train_file).read().strip()
    dev_sentences = open(dev_file).read().strip()
    test_sentences = open(test_file).read().strip()
    test2_sentences = open(test2_file).read().strip()
    return train_sentences, dev_sentences, test_sentences, column_names


def load_conll2003_en(BASE_DIR='/Users/pierre/Projets/Corpora/CoNLL2003/'):
    train_file = BASE_DIR + 'NER-data/eng.train'
    dev_file = BASE_DIR + 'NER-data/eng.valid'
    test_file = BASE_DIR + 'NER-data/eng.test'

    column_names = ['form', 'ppos', 'pchunk', 'ner']

    train_sentences = open(train_file).read().strip()
    dev_sentences = open(dev_file).read().strip()
    test_sentences = open(test_file).read().strip()
    return train_sentences, dev_sentences, test_sentences, column_names


def load_ud_en_ewt(BASE_DIR='/Users/pierre/Documents/Cours/EDAN20/corpus/ud-treebanks-v2.3/UD_English-EWT/'):
    train_file = BASE_DIR + 'en_ewt-ud-train.conllu'
    dev_file = BASE_DIR + 'en_ewt-ud-dev.conllu'
    test_file = BASE_DIR + 'en_ewt-ud-test.conllu'

    column_names = ['ID', 'FORM', 'LEMMA', 'UPOS', 'XPOS',
                    'FEATS', 'HEAD', 'DEPREL', 'HEAD', 'DEPS', 'MISC']

    column_names = list(map(str.lower, column_names))
    train_sentences = open(train_file).read().strip()
    dev_sentences = open(dev_file).read().strip()
    test_sentences = open(test_file).read().strip()
    return train_sentences, dev_sentences, test_sentences, column_names


def load_internet_ud_en_ewt(url='https://raw.githubusercontent.com/UniversalDependencies/UD_English-EWT/master/'):
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


def load_internet_ud_en_talbanken(url=
                                  'https://raw.githubusercontent.com/UniversalDependencies/UD_Swedish-Talbanken/master/'):
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


def load_suc_3(BASE_DIR='/Users/pierre/Projets/Corpora/svenska/SUC3.0/corpus/conll/'):
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


def load_embeddings(BASE_DIR='/Users/pierre/Documents/Cours/EDAN20/corpus/'):
    """
    Return the embeddings in the from of a dictionary
    :param file:
    :return:
    """
    file = BASE_DIR + 'glove.6B.100d.txt'
    glove = open(file)
    embeddings_dict = {}
    for line in glove:
        values = line.strip().split()
        word = values[0]
        embeddings_dict[word] = np.array(values[1:])
    glove.close()
    return embeddings_dict


if __name__ == '__main__':
    train_sentences, dev_sentences, test_sentences, column_names = load_internet_ud_en_talbanken()
    conll_dict = CoNLLDictorizer(column_names, col_sep='\t')
    train_dict = conll_dict.transform(train_sentences)
    print(train_dict[0])
    print(train_dict[1])

    train_sentences, dev_sentences, test_sentences, column_names = load_conll2009_pos()
    conll_dict = CoNLLDictorizer(column_names, col_sep='\t')
    train_dict = conll_dict.transform(train_sentences)
    print(train_dict[0])
    print(train_dict[1])

    train_sentences, dev_sentences, test_sentences, column_names = load_conll2003_en()
    conll_dict = CoNLLDictorizer(column_names, col_sep=' ')
    train_dict = conll_dict.transform(train_sentences)
    print(train_dict[0])
    print(train_dict[1])

    train_sentences, dev_sentences, test_sentences, column_names = load_ud_en_ewt()
    conll_dict = CoNLLDictorizer(column_names, col_sep='\t')
    train_dict = conll_dict.transform(train_sentences)
    print(train_dict[0])
    print(train_dict[1])

    train_sentences, dev_sentences, test_sentences, column_names = load_internet_ud_en_ewt()
    conll_dict = CoNLLDictorizer(column_names, col_sep='\t')
    train_dict = conll_dict.transform(train_sentences)
    print(train_dict[0])
    print(train_dict[1])

    train_sentences, dev_sentences, test_sentences, column_names = load_suc_3()
    conll_dict = CoNLLDictorizer(column_names, col_sep='\t')
    train_dict = conll_dict.transform(train_sentences)
    print(train_dict[0])
    print(train_dict[1])

    embeddings_dict = load_embeddings()
    print(embeddings_dict['table'])
