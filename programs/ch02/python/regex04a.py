"""
The tr/// operator with modifiers
tr///d
"""

import sys

translation_dict = str.maketrans('', '', 'AEIOUaeiou')
for line in sys.stdin:
    print(line.translate(translation_dict), end='')
