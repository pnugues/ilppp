"""
Detecting nonASCII
https://pypi.python.org/pypi/regex
We need to use the regex module
"""
__author__ = "Pierre Nugues"

import sys
import regex

for line in sys.stdin:
    if regex.search(r"[^\u0000-\u007f]", line):
        # if regex.search(r"[^\x00-\x7f]", line):
        #    if regex.search(r"^[^\x00-\x7f]+$", line):
        #    if regex.search(r"^\p{IsLatin}+$", line):
        print("NonASCII: ", line, end='')
    else:
        print('ASCII: ', line, end='')
