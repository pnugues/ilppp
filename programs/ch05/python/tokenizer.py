"""
Tokenizers
Usage: python tokenizer.py < corpus.txt
"""
__author__ = "Pierre Nugues"

import sys
import regex as re

text = """Tell me, O muse, of that ingenious hero who
travelled far and wide after he had sacked the famous
town of Troy."""


def tokenize(text):
    """uses the nonletters to break the text into words
    returns a list of words"""
    # words = re.split(r'[\s\-,;:!?.’\'«»()–...&‘’“”*—]+', text)
    # words = re.split(r'[^a-zåàâäæçéèêëîïôöœßùûüÿA-ZÅÀÂÄÆÇÉÈÊËÎÏÔÖŒÙÛÜŸ’\-]+', text)
    # words = re.split(r'\W+', text)
    words = re.split(r'\P{L}+', text)
    words.remove('')
    return words


def tokenize2(text):
    """uses the letters to break the text into words
    returns a list of words"""
    # words = re.findall(r'[a-zåàâäæçéèêëîïôöœßùûüÿA-ZÅÀÂÄÆÇÉÈÊËÎÏÔÖŒÙÛÜŸ’\-]+', text)
    # words = re.findall(r'\w+', text)
    words = re.findall(r'\p{L}+', text)
    return words


def tokenize3(text):
    """uses the punctuation and nonletters to break the text into words
    returns a list of words"""
    # text = re.sub(r'[^a-zåàâäæçéèêëîïôöœßùûüÿA-ZÅÀÂÄÆÇÉÈÊËÎÏÔÖŒÙÛÜŸ’'()\-,.?!:;]+', '\n', text)
    # text = re.sub(r'([,.?!:;)('-])', r'\n\1\n', text)
    text = re.sub(r'[^\p{L}\p{P}]+', '\n', text)
    text = re.sub(r'(\p{P})', r'\n\1\n', text)
    text = re.sub(r'\n+', '\n', text)
    return text.split()


def tokenize4(text):
    """uses the punctuation and symbols to break the text into words
    returns a list of words"""
    spaced_tokens = re.sub(r'([\p{S}\p{P}])', r' \1 ', text)
    one_token_per_line = re.sub(r'\s+', '\n', spaced_tokens)
    tokens = one_token_per_line.split()
    return tokens


if __name__ == '__main__':
    text = sys.stdin.read()
    """words = tokenize(text)
    for word in words:
        print(word)
    words = tokenize2(text)
    print(words)"""
    words = tokenize4(text)
    print(words)
