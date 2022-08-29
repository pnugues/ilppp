"""
Match variables inside m//
"""
__author__ = "Pierre Nugues"

import re
import sys

for line in sys.stdin:
    line = re.sub(r'\$ *([0-9]+)\.?([0-9]*)', r'\1 dollars and \2 cents', line)
    print(line, end='')
