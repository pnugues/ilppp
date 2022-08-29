"""
The m// match operator
"""
__author__ = "Pierre Nugues"

import regex as re
import sys

for line in sys.stdin:
    if re.search('ab*c', line):  # m/ab*c/
        print('-> ' + line, end='')
