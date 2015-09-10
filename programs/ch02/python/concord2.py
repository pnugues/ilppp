"""
Concordances where the right context uses a lookahead
This is to avoid advancing the matching start index past a concordance
if the distance between two concordances is less than the context size,
for instance less than 20 characters apart
python3 concord2.py helenus.txt 'Helenus' 20
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
pattern = "(.{{0,{width}}})({pattern})(?=(.{{0,{width}}}))".format(pattern=pattern, width=width)
for match in re.finditer(pattern, text):
    print(match.group(1), match.group(2), match.group(3))
# print the string with 0..width characters on either side
