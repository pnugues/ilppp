"""
Elementary tokenizer
Usage: python tokenize_simple.py < corpus.txt
"""
__author__ = "Pierre Nugues"

import sys
import regex as re


def simple_tokenizer(text):
    one_token_per_line = re.sub('\s+', '\n', text)
    print(one_token_per_line, end='')


def simple_tokenizer_punc(text):
    spaced_tokens = re.sub('([\p{S}\p{P}])', r' \1 ', text)
    one_token_per_line = re.sub('\s+', '\n', spaced_tokens)
    print(one_token_per_line, end='')


if __name__ == '__main__':
    mode = 'WORD_ONLY'
    # mode = 'WORD_PUNC'
    text = sys.stdin.read()
    if mode == 'WORD_ONLY':
        simple_tokenizer(text)
    if mode == 'WORD_PUNC':
        simple_tokenizer_punc(text)
