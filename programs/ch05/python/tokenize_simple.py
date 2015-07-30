import sys
import re

text = sys.stdin.read()
text = re.sub("\s+", "\n", text)
print(text, end='')
