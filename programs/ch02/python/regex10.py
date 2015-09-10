"""
Program to extract the left and right context of a match
"""
__author__ = "Pierre Nugues"

import re
import sys

string = "my string"
width = 10

# pattern = (.{0,width}string.{0,width})
# pattern = (.{0,10}my string.{0,10})
pattern = "(.{{0,{1}}}{0}.{{0,{1}}})".format(string, width)
for line in sys.stdin:
    match = re.search(pattern, line)
    if match:
        print(match.group(1))
