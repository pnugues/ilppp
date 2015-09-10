"""
Concordance program to find all the concordances
of a pattern surrounded by width characters.
Usage: python concord.py file pattern width
"""
__author__ = "Pierre Nugues"

import re
import sys

[file_name, pattern, width] = sys.argv[1:]
try:
    file = open(file_name)
except:
    print("Could not open file", file_name)
    exit(0)

text = file.read()

# Let spaces match across _and print_ newlines
pattern = re.sub(" ", r"\\s+", pattern)
text = re.sub(r"\s+", " ", text)  # Uncomment this to match/print newlines as spaces
pattern = "(.{{0,{width}}}{pattern}.{{0,{width}}})".format(pattern=pattern, width=width)
for match in re.finditer(pattern, text):
    print(match.group(1))
# print the string with 0..width characters on either side
