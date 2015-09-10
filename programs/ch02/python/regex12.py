"""
Detecting nonASCII, Greek, Greek blocks
This must be run with the command:
python3 regex12.py <../test.txt
"""
__author__ = "Pierre Nugues"

import sys
import regex

for line in sys.stdin:
    # if  regex.search(r"^\p{IsASCII}+$", line):
    #        print("line is ASCII: ", line, end="")
    #    if regex.search(r"\P{IsASCII}", line):
    #        print("line contains NonASCII: ", line, end="")
    if regex.search(r"\P{InBasic_Latin}", line):
        print("line contains non basic Latin: ", line, end="")
    if regex.search(r"^\p{InGreek_and_Coptic}+$", line):
        print("Line is in Greek and Coptic block: ", line, end="")
    if regex.search(r"^\p{Greek}+$", line):
        print("Line is Greek script: ", line, end="")
    if regex.search(r"\u03B1", line):
        print("Line contains alpha (code point): ", line, end="")
    if regex.search(r'\N{GREEK SMALL LETTER ALPHA}', line):
        print("Line contains alpha (Unicode name): ", line, end="")
    if regex.search("α", line):
        print("Line contains alpha (Direct char input): ", line, end="")
    if regex.search(r"\N{LATIN SMALL LETTER A}", line):
        print("Line contains a: ", line, end="")
    if regex.search(r"\N{LATIN SMALL LETTER O WITH DIAERESIS}", line):
        print("Line contains ö: ", line, end="")
