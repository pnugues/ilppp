__author__ = 'Pierre Nugues'


class Preprocessor:

    def __init__(self, column_names):
        self.column_names = column_names

    def make_conll_sentence(self, sent_string):
        word_list = sent_string.strip().split()

        conll_sentence = []
        for inx, word in enumerate(word_list, 1):
            word_row = {key: '_' for key in self.column_names}
            word_row['ID'] = str(inx)
            word_row['FORM'] = word
            conll_sentence += [word_row]
        return conll_sentence

    def pad(self, sentence):
        bos_pad = {key: '<s>' for key in self.column_names}
        eos_pad = {key: '</s>' for key in self.column_names}
        bos_pad['ID'] = '0'
        inx_end = str((len(sentence) - 1))
        sentence[-1]['ID'] = inx_end
        sentence = [bos_pad] + sentence + [eos_pad]
        return sentence
