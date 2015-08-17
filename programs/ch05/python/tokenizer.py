import sys
import re

import regex


def tokenize(text):
    # words = re.split("[\s\-,;:!?.’\'«»()–...&‘’“”*—]+", text)
    # words = re.split("[^a-zåàâäæçéèêëîïôöœßùûüÿA-ZÅÀÂÄÆÇÉÈÊËÎÏÔÖŒÙÛÜŸ’\-]+", text)
    # words = re.split("\W+", text)
    words = regex.split("[^\p{L}]+", text)
    words.remove('')
    return words


def tokenize2(text):
    text = re.sub("[^a-zåàâäæçéèêëîïôöœßùûüÿA-ZÅÀÂÄÆÇÉÈÊËÎÏÔÖŒÙÛÜŸ’'()\-,.?!:;]+", "\n", text)
    text = re.sub("([,.?!:;)('-])", r"\n\1\n", text)
    text = re.sub(r"\n+", "\n", text)
    return text


if __name__ == '__main__':
    text = sys.stdin.read()
    words = tokenize(text)
    for word in words:
        print(word)
    text = tokenize2(text)
    print(text)