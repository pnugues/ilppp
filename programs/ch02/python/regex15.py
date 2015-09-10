"""
A Perl regex that does not in Python
"""
__author__ = "Pierre Nugues"

import re

match = re.search(".X(.+)+X", "bbbbXcXaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
print(match.group(1))
