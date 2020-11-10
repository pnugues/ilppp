import regex as re
import conll
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier


def char2tag(sent_dict):
    for word in sent_dict:
        if len(word['FORM']) == 1:
            word['CHAR_TAGS'] = 'S'
        elif len(word['FORM']) == 2:
            word['CHAR_TAGS'] = 'BE'
        else:
            word['CHAR_TAGS'] = 'B' + (len(word['FORM']) - 2) * 'I' + 'E'
    return sent_dict


def tokens2seq(sent_text, sent_dict):
    sent_seg_seq = ''
    for word in sent_dict:
        m = re.search(re.escape(word['FORM']), sent_text)
        sent_seg_seq += 'X' * m.start()
        sent_seg_seq += word['CHAR_TAGS']
        sent_text = sent_text[m.end():]
    return sent_seg_seq


def extract_features(sentences, w_size=5):
    bos = '▶' * int(w_size / 2)
    eos = '◀' * int(w_size / 2)
    X = []
    for sentence in sentences:
        sentence = bos + sentence + eos
        for i in range(len(sentence[:-w_size + 1])):
            X.append(list(sentence[i:i + w_size]))
    return X


def dictorize(X_feat_symb):
    X_dict = []
    w_size = len(X_feat_symb[0])
    feat_keys = ['feat' + str(i) for i in range(w_size)]
    for x in X_feat_symb:
        X_dict.append({k: v for k, v in zip(feat_keys, x)})
    return X_dict


def seq2tokens(sentence, seg_sequence):
    pat = '(BI*E)|S'
    tokens_inx = []
    for m in re.finditer(pat, seg_sequence):
        tokens_inx.append((m.start(), m.end()))
    tokens = []
    for inx_pair in tokens_inx:
        tokens += [sentence[inx_pair[0]:inx_pair[1]]]
    return tokens


def run_exam():
    sent_text = 'You really got me thinking, I enjoy reading this blog.'
    sent_seg_seq = 'BIEXBIIIIEXBIEXBEXBIIIIIIESXSXBIIIEXBIIIIIEXBIIEXBIIES'
    sent_dict = [{'ID': '1', 'FORM': 'You'},
                 {'ID': '2', 'FORM': 'really'},
                 {'ID': '3', 'FORM': 'got'},
                 {'ID': '4', 'FORM': 'me'},
                 {'ID': '5', 'FORM': 'thinking'},
                 {'ID': '6', 'FORM': ','},
                 {'ID': '7', 'FORM': 'I'},
                 {'ID': '8', 'FORM': 'enjoy'},
                 {'ID': '9', 'FORM': 'reading'},
                 {'ID': '10', 'FORM': 'this'},
                 {'ID': '11', 'FORM': 'blog'},
                 {'ID': '12', 'FORM': '.'}]

    char2tag(sent_dict)
    print('Formatted sentence:')
    print('\t', sent_dict)
    sent_tok_seq = tokens2seq(sent_text, sent_dict)
    print('Sentence and aligned token segmentation:')
    print('\t', sent_text)
    print('\t', sent_tok_seq)
    if len(sent_tok_seq) == len(sent_text):
        print('Aligned sequences')
    if sent_tok_seq == sent_seg_seq:
        print('Equal gold and system')
    X_symb = extract_features([sent_text])
    print(X_symb)
    print(len(X_symb))
    X_dict = dictorize(X_symb)
    print(X_dict)
    print(len(X_dict))
    print(len(sent_tok_seq))


if __name__ == '__main__':
    column_names = ['ID', 'FORM', 'LEMMA', 'UPOS',
                    'XPOS', 'FEATS', 'HEAD', 'DEPREL', 'DEPS', 'MISC']
    base_path = '/Users/pierre/Documents/Cours/EDAN20/corpus/ud-treebanks-v2.6/'
    train_file = base_path + 'UD_English-EWT/en_ewt-ud-train.conllu'
    dev_file = base_path + 'UD_English-EWT/en_ewt-ud-dev.conllu'
    test_file = base_path + 'UD_English-EWT/en_ewt-ud-test.conllu'

    train_sentences = conll.read_sentences(train_file)
    formatted_train_corpus = [conll.split_rows(sentence, column_names)
                              for sentence in train_sentences]
    train_sent_texts = [conll.get_text(sentence)
                        for sentence in train_sentences]
    test_sentences = conll.read_sentences(test_file)
    formatted_test_corpus = [conll.split_rows(sentence, column_names)
                              for sentence in test_sentences]
    test_sent_texts = [conll.get_text(sentence)
                        for sentence in test_sentences]

    # Training a model
    X_symb_seq = []
    Y_symb_seq = []
    for sent_text, sent_dict in zip(train_sent_texts, formatted_train_corpus):
        sent_dict = conll.purge_non_int_ID(sent_dict)
        sent_dict = char2tag(sent_dict)
        sent_tok_seq = tokens2seq(sent_text, sent_dict)
        # Useless instruction
        X_symb_seq.append(sent_text)
        Y_symb_seq.append(sent_tok_seq)
    print('Input seqs:\t', len(X_symb_seq))
    print('Output seqs:\t', len(Y_symb_seq))
    print(X_symb_seq[:2])
    print(Y_symb_seq[:2])

    X_feat_symb = extract_features(X_symb_seq)
    y = list(''.join(Y_symb_seq))
    print('# feature vectors:', len(X_feat_symb))
    print('# output tags:', len(y))
    for i in range(3):
        print('x:', X_feat_symb[i], 'y:', y[i])
    # run_exam()

    X_dict = dictorize(X_feat_symb)
    print(X_dict[:2])
    vectorizer = DictVectorizer()
    vectorizer.fit(X_dict)
    X = vectorizer.transform(X_dict)
    print(X[:2])

    #lr = LogisticRegression(n_jobs=12, verbose=True)
    lr = MLPClassifier(verbose=True)
    lr.fit(X, y)
    y_pred = lr.predict(X)
    print('Train acc.', accuracy_score(y, y_pred))

    # Testing the model
    X_symb_seq_test = []
    Y_symb_seq_test = []
    for sent_text, sent_dict in zip(test_sent_texts, formatted_test_corpus):
        sent_dict = conll.purge_non_int_ID(sent_dict)
        sent_dict = char2tag(sent_dict)
        sent_tok_seq = tokens2seq(sent_text, sent_dict)
        X_symb_seq_test.append(sent_text)
        Y_symb_seq_test.append(sent_tok_seq)

    X_feat_symb_test = extract_features(X_symb_seq_test)
    y_test = list(''.join(Y_symb_seq_test))

    X_dict_test = dictorize(X_feat_symb_test)
    X_test = vectorizer.transform(X_dict_test)
    y_pred_test = lr.predict(X_test)
    print('Test acc.', accuracy_score(y_test, y_pred_test))

    # Applying the model
    print('Applying the model to a sentence')
    # test_sentence = 'Bush earned 340 points in 1969-1970.'
    test_sentence = 'Tinnitus is a common consequence of damage to the auditory periphery, affecting around 5–12% of the population and inducing intolerable discomfort. Today, no treatment exists to cure tinnitus.'
    test_features_symb = extract_features([test_sentence])
    test_features_dict = dictorize(test_features_symb)
    X_test = vectorizer.transform(test_features_dict)
    y_test = lr.predict(X_test)
    seg_sequence = ''.join(y_test)
    print(test_sentence)
    print(seg_sequence)
    tokens = seq2tokens(test_sentence, seg_sequence)
    print(tokens)
