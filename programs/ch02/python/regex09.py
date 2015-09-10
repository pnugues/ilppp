"""
Program to extract the context of a match:
before the match, the matched pattern, and after the match
"""
__author__ = "Pierre Nugues"

import re

line = "Tell me, O muse, of that ingenious hero who travelled far and wide after he had sacked the famous town of Troy."

match = re.search(",.*,", line)

print("First match: ", line[match.start():match.end()])
print("Before: ", line[:match.start()])
print("After: ", line[match.end():])
