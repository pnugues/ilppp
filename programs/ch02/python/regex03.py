"""
The tr/// translate operator
"""

import sys

letters = 'abcdefghijklmnopqrstuwvxyzäåö'
translation_dict = str.maketrans(letters, letters.upper())
for line in sys.stdin:
    print(line.translate(translation_dict), end='')
    # Equivalent to line.upper()
