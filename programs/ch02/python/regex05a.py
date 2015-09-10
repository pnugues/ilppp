"""
Match variables inside m//
"""
__author__ = "Pierre Nugues"

import re
import sys

pattern = re.compile(r'(.)\1\1')
for line in sys.stdin:
    m = pattern.search(line)
    if m:
        line = pattern.sub('***', line)
        print(m.group(1))
        print(line, end='')
