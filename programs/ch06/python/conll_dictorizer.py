# coding=utf-8
"""
CoNLL 2009 file readers and writers for the parts of speech.
Version with a class modeled as a vectorizer
"""
__author__ = "Pierre Nugues"

import regex as re


def save(file, formatted_corpus, column_names):
    """
    Saves the corpus in a file
    :param file:
    :param formatted_corpus:
    :param column_names:
    :return:
    """
    with open(file, 'w') as f_out:
        for sentence in formatted_corpus:
            sentence_lst = []
            for row in sentence:
                items = map(lambda x: row.get(x, '_'), column_names)
                sentence_lst += '\t'.join(items) + '\n'
            sentence_lst += '\n'
            f_out.write(''.join(sentence_lst))


class Token:

    def __init__(self, token):
        self._content = token
        self.keys = token.keys()
        self.get = token.get

    def __contains__(self, item):
        return item in self.keys

    def __getitem__(self, item):
        return self._content[item]

    def __setitem__(self, item, value):
        self._content[item] = value

    def __repr__(self):
        return str(self._content)


class CoNLLDictorizer:

    def __init__(self, column_names, sent_sep='\n\n', col_sep=' +'):
        self.column_names = column_names
        self.sent_sep = sent_sep
        self.col_sep = col_sep

    def fit(self):
        pass

    def transform(self, corpus):
        corpus = corpus.strip()
        sentences = re.split(self.sent_sep, corpus)
        return list(map(self._split_in_words, sentences))

    def fit_transform(self, corpus):
        return self.transform(corpus)

    def _split_in_words(self, sentence):
        rows = re.split('\n', sentence)
        return [Token(dict(zip(self.column_names,
                               re.split(self.col_sep, row))))
                for row in rows]


if __name__ == '__main__':
    train_file = 'test.txt'

    column_names = ['id', 'form', 'lemma', 'cpos', 'pos', 'feats']
    train = open(train_file).read().strip()
    conll_dict = CoNLLDictorizer(column_names, col_sep='\t')
    X_dict = conll_dict.transform(train)

    print(X_dict[0])
    print(X_dict[0][0])
    print(type(X_dict[0][0]))
    print(X_dict[0][0]['form'])
    print(X_dict[1])
    tok = Token({'id': '1', 'form': 'La', 'lemma': 'el', 'cpos': 'd', 'pos': 'da', 'feats': 'num=s|gen=f'})
    print(tok['form'])
    print('form' in tok)

    save('out', X_dict, column_names)
