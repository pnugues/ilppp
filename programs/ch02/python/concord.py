"""
Concordance program to find all the concordances
of a pattern surrounded by width characters.
Usage: python concord.py file pattern width
"""
__author__ = "Pierre Nugues"

import regex as re
import sys

[file_name, pattern, width] = sys.argv[1:]
try:
    text = open(file_name).read()
except:
    print('Could not open file', file_name)
    exit(0)

# spaces match tabs and newlines
pattern = re.sub(' ', '\\s+', pattern)
# Replaces newlines with spaces in the text
text = re.sub('\s+', ' ', text)
concordance = ('(.{{0,{width}}}{pattern}.{{0,{width}}})'
               .format(pattern=pattern, width=width))
for match in re.finditer(concordance, text):
    print(match.group(1))
# print the string with 0..width characters on either side
