import re
import sys

text = sys.stdin.read()
for match in re.finditer(r"<b>(.*?)</b>", text):
    print(match.group(1))
