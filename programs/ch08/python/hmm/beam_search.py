__author__ = 'Pierre Nugues'

import math
from tqdm import tqdm
import copy

import conll
from confusion_matrix import ConfusionMatrix
from pos_tagger import POSTagger
from counts import Counts
from preprocessor import Preprocessor
from hmm_prob import HMMProb


class BeamSearch(POSTagger):

    def __init__(self, counts, beam_size, use_trigram=True):
        self.cnts = counts
        self.word_POS_cnts = counts.word_POS_cnts
        self.unk_POS_cnts = counts.unk_POS_cnts
        self.beam_size = beam_size
        self.use_trigrams = use_trigram

    def tag(self, sentence):
        paths = self.generate_paths(sentence)
        best_path = paths[0]['path'][1:]
        logprob = paths[0]['logprob']

        for word, POS in zip(sentence, best_path):
            word['PPOS'] = POS
        return logprob, sentence

    def count_paths(self, sentence):
        path_cnt = 1
        for word in sentence:
            if word['FORM'] in self.word_POS_cnts:
                path_cnt *= len(self.word_POS_cnts[word['FORM']])
            else:
                path_cnt *= len(self.unk_POS_cnts.keys())
        return path_cnt

    def generate_paths(self, sentence):
        paths = []
        start = {'path': ['<s>'], 'logprob': 0.0}
        paths.append(start)
        for word in sentence:
            form = word['FORM']
            paths = self.expand_paths(paths, form)
            paths.sort(key=lambda x: -x.get('logprob'))
            paths = paths[:self.beam_size]
        return paths

    def expand_paths(self, paths, form):
        """
        We create as many new paths as we have possible POSs for the form. 
        We expand the POS paths with one POS:
        If for has three POS: POS1, POS2, POS3
        We create path + POS1, path + POS2, path + POS3
        """
        word_POS_cnt = self.word_POS_cnts.get(form)
        hmm_prob = HMMProb(self.cnts)
        if word_POS_cnt:
            pos_candidates = word_POS_cnt.keys()
        else:
            # Unknown words: either NN or all the possible POS
            # The latter has better results with beamSize large.
            # posSet = posFreqs.keySet();
            # Only observed unknown POS are possible
            pos_candidates = self.unk_POS_cnts.keys()
        new_paths = []
        for path in paths:
            for pos in pos_candidates:
                new_path = copy.deepcopy(path)
                new_path['path'].append(pos)
                if self.use_trigrams:
                    prev_bigram = tuple(path['path'][-2:])
                    if len(prev_bigram) < 2:
                        prev_bigram = ('<s>', prev_bigram[0])
                    prob_term = hmm_prob.compute_tri(form, prev_bigram, pos)
                else:
                    prev_pos = path['path'][-1]
                    prob_term = hmm_prob.compute_bi(form, prev_pos, pos)
                new_path['logprob'] += math.log10(prob_term)
                new_paths.append(new_path)
        return new_paths


if __name__ == '__main__':
    corpus = 'CoNLL-U'
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

    tagger = BeamSearch(counts, 4)

    preprocessor = Preprocessor(column_names)
    sentence = preprocessor.make_conll_sentence('That round table might collapse')
    # sentence = tester.pad(sentence)
    print(sentence)
    logprob, sentence = tagger.tag(sentence)
    print(logprob, sentence)

    test_sentences = conll.read_sentences(test_file)
    formatted_test_corpus = [conll.split_rows(sentence, column_names)
                             for sentence in test_sentences]

    for sentence in tqdm(formatted_test_corpus):
        tagger.tag(sentence)

    cm = ConfusionMatrix(formatted_test_corpus, POS_key)
    cm.compute_matrix()
    cm.print()
    print("Accuracy: ", cm.compute_accuracy())
