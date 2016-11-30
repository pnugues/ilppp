"""
Graph utilities for projectivity
"""
__author__ = "Pierre Nugues"
import conll


def all_children_in_graph(word, graph, sentence):
    """
    Boolean that returns true if word in sentence has
    has all its children in an incomplete graph (graph).
    Normally word is the first or second word in the stack
    :param word:
    :param graph:
    :param sentence:
    :return:
    """
    left_children, right_children = get_children(word, sentence)
    for child in left_children + right_children:
        if not child['id'] in graph['heads']:
            return False
    return True


def get_children(current_word, sentence):
    """
    Returns the lists of sorted left
    and right children (modifiers) of a word
    :param current_word:
    :param sentence:
    :return:
    """
    left_children = []
    right_children = []
    for word in sentence:
        if word['head'] == current_word['id']:
            if int(word['id']) < int(current_word['id']):
                left_children.append(word)
            if int(word['id']) > int(current_word['id']):
                right_children.append(word)
    return left_children, right_children


def inorder(current_word, sentence, projective_order):
    """
    In-order traversal of a dependency graph
    :param current_word:
    :param sentence:
    :param projective_order: Returns the projective order
    :return:
    """
    if current_word == []:
        return
    left_children, right_children = get_children(current_word, sentence)
    for word in left_children:
        inorder(word, sentence, projective_order)
    print(current_word['id'], end=' ', flush=True)
    projective_order.append(current_word['id'])
    for word in right_children:
        inorder(word, sentence, projective_order)


def print_sentence(sentence):
    for word in sentence:
        print(word['form'], end=' ', flush=True)
    print()


def connected(word, head, sentence):
    """
    Succeeds if word is connected to head and returns the chain
    of words
    :param word:
    :param head:
    :param sentence:
    :return:
    """
    chain = [word]
    current_word = word
    while True:
        if current_word['head'] == head['id']:
            chain.append(head)
            return chain
        else:
            # next head. We assume one head
            head_inx = int(current_word['head'])
            current_word = sentence[head_inx]
            # No cycle or we have reached the ROOT
            if current_word in chain:
                return False
            else:
                chain.append(current_word)


def nonprojective_links(sentence):
    """
    Finds the nonprojective links
    :param sentence:
    :return:
    """
    np_links = []
    for word in sentence:
        # words between id and head
        id_min = min(int(word['id']), int(word['head']))
        id_max = max(int(word['id']), int(word['head']))
        id_head = int(word['head'])
        # The words in between
        for i in range(id_min + 1, id_max):
            # Are they all connected?
            if not connected(sentence[i], sentence[id_head], sentence):
                np_links.append(word)
                break
    return np_links


if __name__ == '__main__':
    train_file = '../../../corpus/conllx/sv/swedish_talbanken05_train.conll'
    # train_file = 'test_x'
    # test_file = '../../../corpus/conllx/sv/swedish_talbanken05_test.conll'
    test_file = '../../../corpus/conllx/sv/swedish_talbanken05_test_blind.conll'

    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats',
                         'head', 'deprel', 'phead', 'pdeprel']
    column_names_2006_test = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats']

    sentences = conll.read_sentences(train_file)
    formatted_corpus = conll.split_rows(sentences, column_names_2006)
    # print(formatted_corpus[0])

    for sentence in formatted_corpus:
        if sentence[1]['form'] == 'Vad' and sentence[2]['form'] == 'beror':
            print_sentence(sentence)
            print(sentence)
            np_links = nonprojective_links(sentence)
            print("nonprojective Links", np_links)

            projective_order = []
            inorder(sentence[0], sentence, projective_order)
            print(projective_order)
