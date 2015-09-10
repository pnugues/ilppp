"""
The tr/// operator with modifiers
tr///d
"""
__author__ = "Pierre Nugues"

import re
import sys

for line in sys.stdin:
    line = re.sub('[AEIOUaeiou]', '', line)
    print(line, end='')
