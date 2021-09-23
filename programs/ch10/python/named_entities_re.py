"""
Detecting named entities with regular expressions
"""
__author__ = "Pierre Nugues"

import regex as re

input_string = 'M. Dupont was given 500 euros in front of the casino'
# input_string = open('/Users/pierre/Documents/Cours/Spelling corrector in Prolog/Norvig/big.txt').read()

ne_pairs = {
    'in front of': [
        'in_front_of'
    ],
    'in front': [
        'in_front'
    ],
    'give up': [
        'give_up'
    ],
    'M\. (\p{Lu}\p{L}+)': [
        r'<ENAMEX> M. \1 </ENAMEX>'
    ],
    '(\p{N}+) euros': [
        r'<NUMEX> \1 euros </NUMEX>'
    ]
}

re_union = '|'.join(ne for ne in ne_pairs.keys())

output_string = ''
start_span = 0
for match in re.finditer(re_union, input_string):
    for key in ne_pairs:
        ne_match = re.match(key, match.group())
        if ne_match:
            transduced_string = re.sub(
                key,
                ne_pairs[key][0],
                match.group(), count=1)
            output_string += \
                input_string[start_span:match.span()[0]] + \
                transduced_string
            start_span = match.span()[1]
            break

output_string += input_string[start_span:]
print('Input:', input_string)
print('Output:', output_string)
