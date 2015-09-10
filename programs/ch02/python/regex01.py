"""
The m// match operator
"""
__author__ = "Pierre Nugues"

import re
import sys

for line in sys.stdin:
    if re.search('ab+c', line):
        print('-> ' + line, end='')
