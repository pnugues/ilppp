from baseline_post import Baseline
from best_first import BestFirst
from beam_search import BeamSearch
from viterbi import Viterbi

from counts import Counts
from confusion_matrix import ConfusionMatrix
from tqdm import tqdm
import conll


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

    print('Baseline')
    tagger = Baseline(counts)

    test_sentences = conll.read_sentences(test_file)
    formatted_test_corpus = [conll.split_rows(sentence, column_names)
                             for sentence in test_sentences]

    for sentence in tqdm(formatted_test_corpus):
        tagger.tag(sentence)

    cm = ConfusionMatrix(formatted_test_corpus, POS_key)
    cm.compute_matrix()
    print("Accuracy: ", cm.compute_accuracy())

    print('Best first')
    tagger = BestFirst(counts)

    test_sentences = conll.read_sentences(test_file)
    formatted_test_corpus = [conll.split_rows(sentence, column_names)
                             for sentence in test_sentences]

    for sentence in tqdm(formatted_test_corpus):
        tagger.tag(sentence)

    cm = ConfusionMatrix(formatted_test_corpus, POS_key)
    cm.compute_matrix()
    print("Accuracy: ", cm.compute_accuracy())

    print('Beam search')
    tagger = BeamSearch(counts, 4)

    test_sentences = conll.read_sentences(test_file)
    formatted_test_corpus = [conll.split_rows(sentence, column_names)
                             for sentence in test_sentences]

    for sentence in tqdm(formatted_test_corpus):
        tagger.tag(sentence)

    cm = ConfusionMatrix(formatted_test_corpus, POS_key)
    cm.compute_matrix()
    print("Accuracy: ", cm.compute_accuracy())

    print('Viterbi')
    tagger = Viterbi(counts)

    test_sentences = conll.read_sentences(test_file)
    formatted_test_corpus = [conll.split_rows(sentence, column_names)
                             for sentence in test_sentences]

    for sentence in tqdm(formatted_test_corpus):
        tagger.tag(sentence)

    cm = ConfusionMatrix(formatted_test_corpus, POS_key)
    cm.compute_matrix()
    print("Accuracy: ", cm.compute_accuracy())
    cm.print()