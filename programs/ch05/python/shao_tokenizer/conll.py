# coding=utf-8
"""
CoNLL 2009 file readers and writers for the parts of speech.
"""
__author__ = "Pierre Nugues"

import regex as re


def read_sentences(file):
    """
    Creates a list of sentences from the corpus
    Each sentence is a string
    :param file: The input file
    :return: a list of sentences
    """
    f = open(file, encoding='utf-8').read().strip()
    sentences = re.split('\n\s*\n', f)
    return sentences


def split_rows(sentence, column_names):
    """
    Breaks a sentence in a list of lines: The words.
    Each line is a dictionary of columns
    :param sentence:
    :param column_names:
    :return: A list of dictionaries
    """
    rows = sentence.strip().split('\n')
    word_list = [dict(zip(column_names, row.strip().split()))
                 for row in rows if row[0] != '#']
    return word_list

def purge_non_int_ID(sent_dict):
    return [row for row in sent_dict if row['ID'].isdigit()]


def get_text(sentence):
    rows = sentence.strip().split('\n')
    for row in rows:
        if row.startswith('# text ='):
            m = re.match('# text = ', row)
            return row[m.end():].strip()


def save(file, formatted_corpus, column_names):
    """
    Saves the corpus in a file
    :param self:
    :param file:
    :param formatted_corpus:
    :param column_names:
    :return:
    """
    f_out = open(file, 'w')
    for sentence in formatted_corpus:
        for row in sentence:
            # print(row, flush=True)
            for col in column_names[:-1]:
                if col in row:
                    f_out.write(row[col] + '\t')
                else:
                    f_out.write('_\t')
            col = column_names[-1]
            if col in row:
                f_out.write(row[col] + '\n')
            else:
                f_out.write('_\n')
        f_out.write('\n')
    f_out.close()


def evaluate(sentences, gold, system):
    """
    Computes the accuracy
    :param sentences:
    :param gold:
    :param system:
    :return:
    """
    bad = 0
    good = 0
    for sentence in sentences:
        for word in sentence:
            if word[gold] == word[system]:
                good += 1
            else:
                bad += 1
    return good, bad
