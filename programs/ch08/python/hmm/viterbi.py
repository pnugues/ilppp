__author__ = 'Pierre Nugues'

import math
from tqdm import tqdm

import conll
from confusion_matrix import ConfusionMatrix
from pos_tagger import POSTagger
from counts import Counts
from preprocessor import Preprocessor
from hmm_prob import HMMProb


class Viterbi(POSTagger):

    def __init__(self, counts, use_trigrams=True):
        self.cnts = counts
        self.word_cnts = counts.word_cnts
        self.POS_cnts = counts.POS_cnts
        self.word_POS_cnts = counts.word_POS_cnts
        self.unk_POS_cnts = counts.unk_POS_cnts
        self.use_trigrams = use_trigrams

    def tag(self, sentence):
        rows = len(self.POS_cnts)
        table = self.create_table(sentence)
        # self.print_matrix(sentence, table)
        max = -math.inf
        inx_max = 0
        for i in range(rows):
            (table[i][-1]).sort(key=lambda x: -x.get('logprob'))
            if max < (table[i][-1])[0]['logprob']:
                max = (table[i][-1])[0]['logprob']
                inx_max = i
        POS_path = table[inx_max][-1][0]['path'][1:]
        # print(POS_path)
        for i in range(len(sentence)):
            sentence[i]['PPOS'] = POS_path[i]
        return max, sentence

    def create_table(self, sentence):
        table = []
        POS_list = sorted(list(self.POS_cnts.keys()))
        # Init col 1
        # We fill the first column: P(<s>) = 1 and P(Other) = 0
        for POS in POS_list:
            cell = []
            if POS == '<s>':
                start = [{'path': ['<s>'], 'logprob': 0.0}]
                cell.append(start)
            else:
                start = [{'path': [POS], 'logprob': -math.inf}]
                cell.append(start)
            table.append(cell)
        for inx_word, word in enumerate(sentence, 1):  # The words after <s>
            form = word['FORM']
            if form in self.word_cnts:
                pos_candidates = list(self.word_POS_cnts[form].keys())
            else:
                # Unknown words: Observed unknown words in the dev set
                pos_candidates = list(self.unk_POS_cnts.keys())
            for inx_POS, POS in enumerate(POS_list):  # For each word, we fill the current column
                if POS in pos_candidates:
                    if self.use_trigrams:
                        self.fill_cell_trigram(table, form, POS, inx_POS, inx_word)
                    else:
                        self.fill_cell_bigram(table, form, POS, inx_POS, inx_word)
                else:
                    # table[i][j] = 0.0;
                    POS_path = [{'path': [], 'logprob': -math.inf}]
                    table[inx_POS].append(POS_path)
        return table

    def fill_cell_bigram(self, table, form, POS, inx_POS, inx_word):
        rows = len(self.POS_cnts)
        hmm_prob = HMMProb(self.cnts)
        POS_paths = []
        # For each current word, we scan the previous column (col - 1)
        # to get the bigrams and the probability of the path so far.
        for k in range(rows):
            prev_paths_in_cell = table[k][inx_word - 1]
            # Normally one list. This could be expanded to have an NBest search.
            best_path_in_cell = prev_paths_in_cell[0]
            prev_prob = best_path_in_cell['logprob']
            if prev_prob != -math.inf:
                prev_POS = best_path_in_cell['path'][-1]
                prob_term = hmm_prob.compute_bi(form, prev_POS, POS)
                logprob = prev_prob + math.log10(prob_term)
                POS_path = {'path': list(best_path_in_cell['path'] + [POS]), 'logprob': logprob}
                POS_paths.append(POS_path)
        table[inx_POS].append(POS_paths)
        # We sort each cell and we keep the best
        table[inx_POS][inx_word] = sorted(table[inx_POS][inx_word], key=lambda x: -x.get('logprob'))[:1]

    def fill_cell_trigram(self, table, form, POS, inx_POS, inx_word):
        rows = len(self.POS_cnts)
        hmm_prob = HMMProb(self.cnts)
        POS_paths = []
        # For each current word, we scan the previous column (col - 1)
        # to get the bigrams and the probability of the path so far.
        for k in range(rows):
            prev_paths_in_cell = table[k][inx_word - 1]
            # Normally one list for bigrams and more for trigrams.
            # This could be expanded to have an NBest search.
            prev_prob = prev_paths_in_cell[0]['logprob']
            if prev_prob != -math.inf:
                best_path_for_cell = []
                for prev_path in prev_paths_in_cell:
                    prev_bigram = tuple(prev_path['path'][-2:])
                    if len(prev_bigram) < 2:
                        prev_bigram = ('<s>', prev_bigram[0])
                    prob_term = hmm_prob.compute_tri(form, prev_bigram, POS)
                    logprob = prev_path['logprob'] + math.log10(prob_term)
                    POS_path = {'path': list(prev_path['path'] + [POS]), 'logprob': logprob}
                    best_path_for_cell.append(POS_path)
                # We take the max of each previous cell and we forget the rest
                best_path_for_cell = sorted(best_path_for_cell, key=lambda x: -x.get('logprob'))[:1]
                POS_paths += best_path_for_cell
        table[inx_POS].append(POS_paths)
        # print(table[inx_POS][inx_word])
        table[inx_POS][inx_word] = sorted(table[inx_POS][inx_word], key=lambda x: -x.get('logprob'))

    def print_matrix(self, sentence, table):
        for word in sentence:  # range(cols):
            print(word['FORM'], end='\t')
        print()
        for i, row in enumerate(table):
            for j, word in enumerate(row):
                print(table[i][j], end='\t')
            print()


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

    tagger = Viterbi(counts)

    preprocessor = Preprocessor(column_names)
    sentence = preprocessor.make_conll_sentence('That round table might collapse')
    # sentence = preprocessor.pad(sentence)
    # sentence = sentence[1:]
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
