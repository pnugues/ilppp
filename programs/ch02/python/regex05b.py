"""
Match variables inside m//
"""
__author__ = "Pierre Nugues"

import sys
import re

for line in sys.stdin:
    m = re.search(r'(.)\1\1', line)
    if m:
        line = re.sub(r'(.)\1\1', '***', line)
        print(m.group(1))
        print(line, end='')
