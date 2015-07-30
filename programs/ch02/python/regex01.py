"""
The m// match operator
"""

import re
import sys

for line in sys.stdin:
    if re.search('ab+c', line):
        print('-> ' + line, end='')
