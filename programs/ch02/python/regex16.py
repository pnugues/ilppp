"""
The \b class
"""
__author__ = "Pierre Nugues"

import re
import sys

for line in sys.stdin:
    m = re.search(r'(\bact\b)', line)
    if m:
        print('Word: ' + m.group(1))