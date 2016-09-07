"""
CoNLL 2000 file reader
"""
__author__ = "Pierre Nugues"


def read_sentences(file):
    """
    Creates a list of sentences from the corpus
    Each sentence is a string
    :param file:
    :return:
    """
    f = open(file).read().strip()
    sentences = f.split('\n\n')
    return sentences


def split_rows(sentences, column_names):
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
    formatted_corpus = split_rows(sentences, column_names)
    print(formatted_corpus)
