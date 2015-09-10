"""
The m// match operator and s/// substitution operator
"""
__author__ = "Pierre Nugues"

import re
import sys

for line in sys.stdin:
    if re.search('ab+c', line):
        print("Old: " + line, end='')
        # Replaces all the occurrences
        line = re.sub('ab+c', 'ABC', line)
        # Replaces the first occurrence
        # line = re.sub('ab+c', 'ABC', line, 1)
        print("New: " + line, end='')
