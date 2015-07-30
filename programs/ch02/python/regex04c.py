"""
The tr/// operator with modifiers
tr///cs
"""

import re
import sys


def squeeze(char, line):
    pattern = re.escape(char) + '{2,}'
    return re.sub(pattern, char, line)


for line in sys.stdin:
    line = re.sub('[^AEIOUaeiou\n]', '$', line)
    line = squeeze('$', line)
    print(line, end='')
