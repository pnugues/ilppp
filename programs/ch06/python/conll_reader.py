# coding=utf-8
"""
CoNLL 2009 file readers and writers for the parts of speech.
Version with a class modeled as a vectorizer
"""
__author__ = "Pierre Nugues"


def save(file, formatted_corpus, column_names):
    """
    Saves the corpus in a file
    :param file:
    :param formatted_corpus:
    :param column_names:
    :return:
    """
    f_out = open(file, 'w')
    for sentence in formatted_corpus:
        for row in sentence:
            for col in column_names[:-1]:
                if col in row.keys():
                    f_out.write(row[col] + '\t')
                else:
                    f_out.write('_\t')
            col = column_names[-1]
            if col in row.keys():
                f_out.write(row[col] + '\n')
            else:
                f_out.write('_\n')
        f_out.write('\n')
    f_out.close()


class Token:

    def __init__(self, token):
        self._content = token
        self.keys = token.keys

    def __getitem__(self, item):
        return self._content[item]

    def __repr__(self):
        return str(self._content)


class CoNLLDictorizer:

    def __init__(self, column_names, sent_sep='\n\n', col_sep=' '):
        self.column_names = column_names
        self.sent_sep = sent_sep
        self.col_sep = col_sep

    def fit(self):
        pass

    def transform(self, corpus):
        corpus = corpus.strip()
        sentences = corpus.split(self.sent_sep)
        return list(map(self._split_in_words, sentences))

    def fit_transform(self, corpus):
        return self.transform(corpus)

    def _split_in_words(self, sentence):
        rows = sentence.split('\n')
        return [Token(dict(zip(self.column_names,
                               row.split(self.col_sep))))
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

    save('out', X_dict, column_names)
