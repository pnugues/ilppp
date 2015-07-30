"""
Match variables inside s//
"""

import sys
import re

for line in sys.stdin:
    result = re.subn(r'(.)\1\1', '***', line)
    # Number of matches
    if result[1] != 0:
        # Subst. result
        print(result[0], end='')
