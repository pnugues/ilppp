"""
Quoting metachars in character classes
"""
__author__ = "Pierre Nugues"

import re
import sys

for line in sys.stdin:
    m = re.search(r'[a\t$1^d]', line)
    #m = re.search(r'[\\\^\$1\]\-a]', line)
    if m:
        print("Not a metachar: ", line, end="")