"""
CoNLL 2000 file reader
Author: Pierre Nugues
"""


def read_sentences(file):
    """
    Creates a list of sentences from the corpus
    Each sentence is a string
    :param file:
    :return:
    """
    f = open(file).read()
    sentences = f.split('\n\n')
    # Remove the empty strings
    sentences = filter(None, sentences)
    return sentences


def split_rows(sentences):
    """
    Creates a list of sentence where each sentence is a list of lines
    Each line is a list of columns
    :param sentences:
    :return:
    """
    new_sentences = []
    for sentence in sentences:
        rows = sentence.split('\n')
        sentence = [row.split() for row in rows]
        new_sentences.append(sentence)
    return new_sentences


def split_rows_dict(sentences, column_names):
    """
    Creates a list of sentence where each sentence is a list of lines
    Each line is a dictionary of columns
    :param sentences:
    :param column_names:
    :return:
    """
    new_sentences = []
    for sentence in sentences:
        rows = sentence.split('\n')
        sentence = [dict(zip(column_names, row.split())) for row in rows]
        new_sentences.append(sentence)
    return new_sentences


if __name__ == '__main__':
    train_file = '../../corpus/conll2000/train.txt'
    # train_file = 'test_x'
    test_file = '../../corpus/conll2000/test.txt'
    column_names = ['form', 'pos', 'chunk']

    sentences = read_sentences(train_file)
    formatted_corpus = split_rows(sentences)
    print(formatted_corpus)
