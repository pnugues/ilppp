"""
m// and match variables
"""

import re
import sys

for line in sys.stdin:
    matches = re.findall(r"\$ *([0-9]+)\.?([0-9]*)", line)
    if matches:
        for match in matches:
            print("Dollars: ", match[0], " Cents: ", match[1], "\n", end="")
