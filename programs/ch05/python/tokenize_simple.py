"""
Elementary tokenizer
Usage: python tokenize_simple.py < corpus.txt
"""
__author__ = "Pierre Nugues"

import sys
import re

text = sys.stdin.read()
text = re.sub("\s+", "\n", text)
print(text, end='')
