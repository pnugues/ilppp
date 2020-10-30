__author__ = 'Pierre Nugues'


class ConfusionMatrix:

    def __init__(self, sentences, POS_key, relative_freqs=True):
        self.sentences = sentences
        self.conf_matrix = {}
        self.POS_key = POS_key
        self.relative_freqs = relative_freqs

    def compute_accuracy(self):
        correct = 0
        error = 0
        for sentence in self.sentences:
            for word in sentence:
                if word[self.POS_key] == word['PPOS']:
                    correct += 1
                else:
                    error += 1
        return correct / (correct + error)

    def compute_matrix(self):
        for sentence in self.sentences:
            for word in sentence:
                if word[self.POS_key] in self.conf_matrix:
                    if word['PPOS'] in self.conf_matrix[word[self.POS_key]]:
                        self.conf_matrix[word[self.POS_key]][word['PPOS']] += 1
                    else:
                        self.conf_matrix[word[self.POS_key]][word['PPOS']] = 1
                else:
                    self.conf_matrix[word[self.POS_key]] = {}
                    self.conf_matrix[word[self.POS_key]][word['PPOS']] = 1
        if self.relative_freqs:
            for key1 in self.conf_matrix:
                POS_count = sum(self.conf_matrix[key1][key2] for key2 in self.conf_matrix[key1])
                if POS_count == 0:
                    continue
                for key2 in self.conf_matrix[key1]:
                    self.conf_matrix[key1][key2] /= POS_count

    def print(self):
        print('\t')
        for pos in sorted(self.conf_matrix):
            print(pos, end='\t')
        print('\n')
        for pos in sorted(self.conf_matrix):
            print(pos, end='\t')
            for ppos in sorted(self.conf_matrix):
                if self.conf_matrix[pos].get(ppos) is None:
                    if self.relative_freqs:
                        print('{:.2f}'.format(0.0), end='\t')
                    else:
                        print('0', end='\t')
                else:
                    if self.relative_freqs:
                        print('{:.2f}'.format(self.conf_matrix[pos][ppos] * 100), end='\t')
                    else:
                        print(self.conf_matrix[pos][ppos], end='\t')
            print('\n')
