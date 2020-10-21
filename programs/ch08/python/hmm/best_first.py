__author__ = 'Pierre Nugues'

import math
from tqdm import tqdm

import conll
from confusion_matrix import ConfusionMatrix
from pos_tagger import POSTagger
from counts import Counts
from preprocessor import Preprocessor
from hmm_prob import HMMProb


class BestFirst(POSTagger):

    def __init__(self, counts, use_trigrams=True):
        self.cnts = counts
        self.word_POS_cnts = counts.word_POS_cnts
        self.unk_POS_cnts = counts.unk_POS_cnts
        self.use_trigrams = use_trigrams

    def tag(self, sentence):
        logprob = math.log10(1.0)
        prev_prev_POS = '<s>'
        prev_POS = '<s>'
        hmm_prob = HMMProb(self.cnts)
        for word in sentence:
            pos_cnt_for_word = self.word_POS_cnts.get(word.get('FORM'))
            cur_POS = None
            if pos_cnt_for_word:
                pos_candidates = pos_cnt_for_word.keys()
            else:
                # New version: all the POS are possible:
                # pos_tagset = POS_cnt.keys();
                # Only observed unknown POS are possible
                pos_candidates = self.unk_POS_cnts.keys()

            max_pos_prob = 0.0
            prev_bigram = (prev_prev_POS, prev_POS)
            for POS in pos_candidates:
                if self.use_trigrams:
                    pos_prob = hmm_prob.compute_tri(
                        word.get('FORM'), prev_bigram, POS)
                else:
                    pos_prob = hmm_prob.compute_bi(
                        word.get('FORM'), prev_POS, POS)
                if max_pos_prob < pos_prob:
                    max_pos_prob = pos_prob
                    cur_POS = POS
                # print("\t" + POS)
                # print(freq + "\t" + self.word_cnt.get(word['FORM])

            logprob += math.log10(max_pos_prob)
            word['PPOS'] = cur_POS
            prev_prev_POS = prev_POS
            prev_POS = cur_POS
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
    dev_sentences = conll.read_sentences(dev_file)
    formatted_dev_corpus = [conll.split_rows(sentence, column_names)
                            for sentence in dev_sentences]

    POS_distr_unk = counts.unk_word_POS_distr(formatted_dev_corpus)
    print('POS distribution of unknown words:', POS_distr_unk)

    nbest = BestFirst(counts)

    preprocessor = Preprocessor(column_names)
    sentence = preprocessor.make_conll_sentence('That round table might collapse')
    # sentence = preprocessor.pad(sentence)
    print(sentence)
    logprob, sentence = nbest.tag(sentence)
    print(logprob, sentence)

    test_sentences = conll.read_sentences(test_file)
    formatted_test_corpus = [conll.split_rows(sentence, column_names)
                             for sentence in test_sentences]

    for sentence in tqdm(formatted_test_corpus):
        nbest.tag(sentence)

    cm = ConfusionMatrix(formatted_test_corpus, POS_key)
    cm.compute_matrix()
    cm.print()
    print("Accuracy: ", cm.compute_accuracy())
