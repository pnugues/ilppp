__author__ = 'Pierre Nugues'

import math
from tqdm import tqdm

import conll
from confusion_matrix import ConfusionMatrix
from pos_tagger import POSTagger
from counts import Counts
from preprocessor import Preprocessor


class Baseline(POSTagger):

    def __init__(self, cnt):
        self.word_cnt = cnt.word_cnts
        self.word_POS_cnts = cnt.word_POS_cnts
        self.unk_POS_cnts = cnt.unk_POS_cnts

    # Applies arg max ∏ P(t_i | w_i)
    # Equivalent to arg max ∏ P(w_i | t_i) ∏ P(t_i)
    def tag(self, sentence):
        logprob = math.log10(1.0)
        default_POS = max(self.unk_POS_cnts, key=self.unk_POS_cnts.get)
        default_POS_prob = self.unk_POS_cnts[default_POS] / \
                           sum(self.unk_POS_cnts.values())
        default_POS_logprob = math.log10(default_POS_prob)
        for word in sentence:
            if word['FORM'] in self.word_cnt:
                POS_cands = self.word_POS_cnts.get(word['FORM'])
                # Selects the highest freq. and then the POS tag in alphabetical order
                POS = min(POS_cands, key=lambda x: (-POS_cands[x], x))
                logprob += math.log10(POS_cands[POS] / sum(POS_cands.values()))
            else:
                POS = default_POS
                logprob += default_POS_logprob
            word['PPOS'] = POS
        return logprob, sentence


if __name__ == '__main__':
    corpus = 'CoNLL2009'
    if corpus == 'CoNLL2009':
        column_names = ['ID', 'FORM', 'LEMMA', 'PLEMMA', 'POS', 'PPOS']
        POS_key = 'POS'
        base_path = '/Users/pierre/Documents/Cours/EDA171/programs/pos_tagging/corpus/en/'
        train_file = base_path + 'CoNLL2009-ST-English-train-pos.txt'
        dev_file = base_path + 'CoNLL2009-ST-English-development-pos.txt'
        test_file = base_path + 'CoNLL2009-ST-test-words-pos.txt'
    elif corpus == 'CoNLL-U':
        column_names = ['ID', 'FORM', 'LEMMA', 'UPOS',
                        'XPOS', 'FEATS', 'HEAD', 'DEPREL', 'DEPS', 'MISC']
        POS_key = 'UPOS'
        base_path = '/Users/pierre/Documents/Cours/EDAN20/corpus/ud-treebanks-v2.6/'
        train_file = base_path + 'UD_English-EWT/en_ewt-ud-train.conllu'
        dev_file = base_path + 'UD_English-EWT/en_ewt-ud-dev.conllu'
        test_file = base_path + 'UD_English-EWT/en_ewt-ud-test.conllu'

    train_sentences = conll.read_sentences(train_file)
    formatted_train_corpus = [conll.split_rows(sentence, column_names)
                              for sentence in train_sentences]

    counts = Counts(formatted_train_corpus, column_names, POS_key)
    counts.count_all()
    # counts.print_stats()

    dev_sentences = conll.read_sentences(dev_file)
    formatted_dev_corpus = [conll.split_rows(sentence, column_names)
                            for sentence in dev_sentences]

    POS_distr_unk = counts.unk_word_POS_distr(formatted_dev_corpus)
    print('POS distribution of unknown words:', POS_distr_unk)
    bl_tagger = Baseline(counts)

    preprocessor = Preprocessor(column_names)
    sentence = preprocessor.make_conll_sentence('That round table might collapse')
    # sentence = tester.pad(sentence)
    print(sentence)
    logprob, sentence = bl_tagger.tag(sentence)
    print(logprob, sentence)

    test_sentences = conll.read_sentences(test_file)
    formatted_test_corpus = [conll.split_rows(sentence, column_names)
                             for sentence in test_sentences]

    for sentence in tqdm(formatted_test_corpus):
        bl_tagger.tag(sentence)

    cm = ConfusionMatrix(formatted_test_corpus, POS_key)
    cm.compute_matrix()
    cm.print()
    print("Accuracy: ", cm.compute_accuracy())
