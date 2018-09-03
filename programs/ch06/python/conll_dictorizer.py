# coding=utf-8
"""
CoNLL 2009 file readers and writers for the parts of speech.
Version with a class modeled as a vectorizer
"""
__author__ = "Pierre Nugues"

import regex as re


def save(file, corpus_dict, column_names):
    """
    Saves the corpus in a file
    :param file:
    :param corpus_dict:
    :param column_names:
    :return:
    """
    with open(file, 'w') as f_out:
        for sentence in corpus_dict:
            sentence_lst = []
            for row in sentence:
                items = map(lambda x: row.get(x, '_'), column_names)
                sentence_lst += '\t'.join(items) + '\n'
            sentence_lst += '\n'
            f_out.write(''.join(sentence_lst))


class Token(dict):
    pass


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
    train_dict = conll_dict.transform(train)

    print(train_dict[0])
    print(train_dict[0][0])
    print(type(train_dict[0][0]))
    print(train_dict[0][0]['form'])
    print(train_dict[1])
    tok = Token({'id': '1', 'form': 'La', 'lemma': 'el', 'cpos': 'd', 'pos': 'da', 'feats': 'num=s|gen=f'})
    print(tok['form'])
    print('form' in tok)

    save('out', train_dict, column_names)

    tok_dict = {'id': '1', 'form': 'La', 'lemma': 'el', 'cpos': 'd', 'pos': 'da', 'feats': 'num=s|gen=f'}
    tok_dict2 = {'id': '1', 'form': 'La', 'lemma': 'el', 'cpos': 'd', 'pos': 'da', 'feats': 'num=s|gen=f'}

    tok_set = set(tok_dict)
    print(tok_set)

    tok_set = tok_set.union(tok_dict2)
    print(tok_set)

    print(tok.keys())

    # exit()
    word_set = set()
    word_set = set(tok_dict.values())
    print(list(word_set))

    word_set = set()
    word_set = set(tok.values())
    print(list(word_set))

    word_set = set()
    word_set.update(tok.values())
    print(list(word_set))

    word_set = set()
    print("Tok val", tok.values())
    word_set = word_set.union(set(tok.values()))
    print(list(word_set))
