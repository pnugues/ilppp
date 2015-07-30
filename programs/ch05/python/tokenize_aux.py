import sys
import re
import regex

text = sys.stdin.read()
# words = re.split("[\s\-,;:!?.’\'«»()–...&‘’“”*—]+", text)
# words = re.split("[^a-zåàâäæçéèêëîïôöœßùûüÿA-ZÅÀÂÄÆÇÉÈÊËÎÏÔÖŒÙÛÜŸ’\-]+", text)
# words = re.split("\W+", text)
words = regex.split("[^\p{L}]+", text)
for word in words:
    print(word)
