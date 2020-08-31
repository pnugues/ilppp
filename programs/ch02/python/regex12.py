"""
Detecting nonASCII, Greek, Greek blocks
This must be run with the command:
python3 regex12.py <../test.txt
"""
__author__ = 'Pierre Nugues'

import sys
import regex as re

for line in sys.stdin:
    print("Line:", line, end='')
    if re.search(r'[\p{IsAlpha}\p{Nd}]+', line):
        print('\tline is Alpha num')
    """
    # Does not work in Python
    if re.search(r'^\p{IsASCII}+$', line):
        print('\tline is ASCII')
    if re.search(r'\P{IsASCII}', line):
        print('\tline contains NonASCII')
    """
    if re.search(r'^\p{InBasic_Latin}+$', line):
        print('\tline is basic Latin')
    if re.search(r'\P{InBasic_Latin}', line):
        print('\tline contains non basic Latin')
    if re.search(r'^\p{InGreek_and_Coptic}+$', line):
        print('\tLine is in Greek and Coptic block')
    if re.search(r'^\p{Greek}+$', line):
        print('\tLine is Greek script')
    if re.search(r'\u03B1', line):
        print('\tLine contains alpha (code point)')
    if re.search(r'\N{GREEK SMALL LETTER ALPHA}', line):
        print('\tLine contains alpha (Unicode name)')
    if re.search('α', line):
        print('\tLine contains alpha (Direct char input)')
    if re.search(r'\N{LATIN SMALL LETTER A}', line):
        print('\tLine contains letter a')
    if re.search(r'\N{LATIN SMALL LETTER O WITH DIAERESIS}', line):
        print('\tLine contains letter ö')
