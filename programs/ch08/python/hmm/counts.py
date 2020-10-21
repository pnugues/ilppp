import conll
from confusion_matrix import ConfusionMatrix
from hmm_prob import HMMProb


class Counts:

    def __init__(self, sentences, column_names, POS_key='POS'):
        self.sentences = sentences
        self.sentence_cnt = len(sentences)
        self.column_names = column_names
        self.POS_key = POS_key
        self.POS_cnts = {}
        self.word_cnts = {}
        self.POS_bigram_cnts = {}
        self.POS_trigram_cnts = {}
        self.word_POS_cnts = {}
        self.unk_POS_cnts = {}
        self.token_cnt = 0
        self.POS_set = set()

    def pad(self):
        bos_pad = {key: '<s>' for key in self.column_names}
        eos_pad = {key: '</s>' for key in self.column_names}
        bos_pad['ID'] = '0'
        self.sentences = [[dict(bos_pad)] + sentence + [dict(eos_pad)]
                          for sentence in self.sentences]
        for sentence in self.sentences:
            inx_end = str((len(sentence) - 1))
            sentence[-1]['ID'] = inx_end
        return self.sentences

    def count_words(self):
        self.token_cnt = 0
        for sentence in self.sentences:
            for word in sentence:
                self.token_cnt += 1
                if word['FORM'] in self.word_cnts:
                    self.word_cnts[word['FORM']] += 1
                else:
                    self.word_cnts[word['FORM']] = 1
        return self.word_cnts

    def unique_POS(self):
        for sentence in self.sentences:
            for word in sentence:
                self.POS_set.add(word[self.POS_key])
        return self.POS_set

    def count_POS(self):
        token_cnt = 0
        for sentence in self.sentences:
            for word in sentence:
                token_cnt += 1
                if word[self.POS_key] in self.POS_cnts:
                    self.POS_cnts[word[self.POS_key]] += 1
                else:
                    self.POS_cnts[word[self.POS_key]] = 1
        return self.POS_cnts

    def count_POS_bigram(self):
        for sentence in self.sentences:
            for inx in range(len(sentence) - 1):
                POS_bigram = (sentence[inx][self.POS_key],
                              sentence[inx + 1][self.POS_key])
                if POS_bigram in self.POS_bigram_cnts:
                    self.POS_bigram_cnts[POS_bigram] += 1
                else:
                    self.POS_bigram_cnts[POS_bigram] = 1
        return self.POS_bigram_cnts

    def count_POS_trigram(self):
        for sentence in self.sentences:
            for inx in range(len(sentence) - 2):
                POS_trigram = (sentence[inx][self.POS_key], sentence[inx + 1][self.POS_key],
                               sentence[inx + 2][self.POS_key])
                if POS_trigram in self.POS_trigram_cnts:
                    self.POS_trigram_cnts[POS_trigram] += 1
                else:
                    self.POS_trigram_cnts[POS_trigram] = 1
        return self.POS_trigram_cnts

    def count_word_POS(self):
        for sentence in self.sentences:
            for word in sentence:
                if word['FORM'] not in self.word_POS_cnts:
                    self.word_POS_cnts[word['FORM']] = {}
                    self.word_POS_cnts[word['FORM']][word[self.POS_key]] = 1
                elif word[self.POS_key] not in self.word_POS_cnts[word['FORM']]:
                    self.word_POS_cnts[word['FORM']][word[self.POS_key]] = 1
                else:
                    self.word_POS_cnts[word['FORM']][word[self.POS_key]] += 1
        return self.word_POS_cnts

    def unk_word_POS_distr(self, sentences):
        for sentence in sentences:
            for word in sentence:
                if word['FORM'] not in self.word_POS_cnts:
                    if word[self.POS_key] in self.unk_POS_cnts:
                        self.unk_POS_cnts[word[self.POS_key]] += 1
                    else:
                        self.unk_POS_cnts[word[self.POS_key]] = 1
        return self.unk_POS_cnts

    def count_all(self):
        self.pad()
        self.count_POS()
        self.unique_POS()
        self.count_words()
        self.count_word_POS()
        self.count_POS_bigram()
        self.count_POS_trigram()

    def print_stats(self):
        print("Token count:\t {} \tSentence count:\t {}".format(
            self.token_cnt, self.sentence_cnt))
        print("\t", self.word_cnts)
        print("\tUnique tokens:\t", len(self.word_cnts))

        print("\tUnique POS:\t", len(self.POS_set))
        print("\t", self.POS_set)

        print("\tUnique word/POS pairs:\t", len(self.word_POS_cnts))
        print("\t", self.word_POS_cnts)

        print("\tUnique POS bigrams:\t", len(self.POS_bigram_cnts))
        print("\t", self.POS_bigram_cnts)

        print("\tUnique POS trigrams:\t", len(self.POS_trigram_cnts))
        print("\t", self.POS_trigram_cnts)

    def print_debug(self):
        print("That round table might collapse")
        sentence = ['<s>', 'That', 'round', 'table',
                    'might', 'collapse', 'sssss', '</s>']
        print('POS distribution:')
        for word in sentence:
            print('\t {}:\t {}'.format(word, self.word_POS_cnts.get(word, 0)))

    def print_debug_ngrams(self):
        bigrams = [("<s>", "DT"), ("DT", "JJ"), ("VB", "</s>"), ("NNP", "NIL")]
        print('\nBigram counts:')
        for bigram in bigrams:
            print('\t {}:\t {}'.format(bigram, self.POS_bigram_cnts.get(bigram, 0)))

        trigrams = [("<s>", "DT", "NN")]
        print('\nTrigram counts:')
        for trigram in trigrams:
            print('\t {}:\t {}'.format(
                trigram, self.POS_trigram_cnts.get(trigram, 0)))


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
    formatted_corpus = [conll.split_rows(sentence, column_names)
                        for sentence in train_sentences]
    # print(formatted_corpus[0])

    counts = Counts(formatted_corpus, column_names, POS_key)
    counts.count_all()
    # counts.print_stats()
    counts.print_debug()
    # print(counts.sentences[0])
    # exit()
    if corpus == 'CoNLL2009':
        cm = ConfusionMatrix(formatted_corpus, POS_key)
        cm.compute_matrix()
        cm.print()
        print("Accuracy: ", cm.compute_accuracy())

    dev_sentences = conll.read_sentences(dev_file)
    formatted_dev_corpus = [conll.split_rows(sentence, column_names)
                            for sentence in dev_sentences]

    POS_distr_unk = counts.unk_word_POS_distr(formatted_dev_corpus)
    print('POS distribution of unknown words:', POS_distr_unk)

    hmm_prob = HMMProb(counts)
    if corpus == 'CoNLL2009':
        print("prob: ", hmm_prob.compute_tri("tabl", ("<s>", "DT"), "NN"))
    elif corpus == 'CoNLL-U':
        print("prob: ", hmm_prob.compute_tri("tabl", ("<s>", "DET"), "NOUN"))
    # tabl is UKN. It can only have a possible POS: NN, NNS, NNP, etc, not DT
