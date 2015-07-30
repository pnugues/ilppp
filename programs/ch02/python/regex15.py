import re

match = re.search(".X(.+)+X", "bbbbXcXaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
print(match.group(1))
