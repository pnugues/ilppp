"""Appendix B.
"""
__author__ = "Pierre Nugues"

"""First loop"""

for i in [1, 2, 3, 4, 5, 6]:
    print(i)
print('Done')

"""Loop with a condition"""

for i in [1, 2, 3, 4, 5, 6]:
    if i % 2 == 0:
        print('Even:', i)
    else:
        print('Odd:', i)
print('Done')

"""Strings"""

"""String with a new line"""
iliad = """Sing, O goddess, the anger of Achilles son of Peleus,
that brought countless ills upon the Achaeans."""
print(iliad, '\n')

"""String with a continuation"""
iliad2 = 'Sing, O goddess, the anger of Achilles son of \
Peleus, that brought countless ills upon the Achaeans.'
print(iliad2, '\n')

alphabet = 'abcdefghijklmnopqrstuvwxyz'
alphabet[0]  # 'a'
alphabet[1]  # 'b'
alphabet[25]  # 'z'

alphabet[-1]  # the last character of a string: 'z'
alphabet[-2]  # the second last: 'y'
alphabet[-26]  # 'a'

try:
    alphabet[27]
except:
    pass

len(alphabet)  # 26

try:
    alphabet[0] = 'b'  # throws an error
except:
    pass

'abc' + 'def'  # 'abcdef'
'abc' * 3  # 'abcabcabc'

# join()
''.join(['abc', 'def', 'ghi'])  # equivalent to a +:
# 'abcdefghi'
' '.join(['abc', 'def', 'ghi'])  # places a space between the
# elements: 'abc def ghi'
', '.join(['abc', 'def', 'ghi'])  # 'abc, def, ghi'

# upper() and lower()
accented_e = 'eéèêë'
accented_e.upper()  # 'EÉÈÊË'
accented_E = 'EÉÈÊË'
accented_E.lower()  # 'eéèêë'

alphabet.find('def')  # 3
alphabet.find('é')  # -1
alphabet.replace('abc', 'αβγ')  # 'αβγdefghijklmnopqrstuvwxyz'

text_vowels = ''
for i in iliad:
    if i in 'aeiou':
        text_vowels = text_vowels + i
print(text_vowels)  # 'ioeeaeoieooeeuaououeiuoeaea'

# Slices
alphabet[0:3]  # the three first letters of the alphabet: 'abc'
alphabet[:3]  # equivalent to alphabet[0:3]
alphabet[3:6]  # substring from index 3 to index 5: 'def'
alphabet[-3:]  # the three last letters of the alphabet: 'xyz'
alphabet[10:-10]  # 'klmnop'
alphabet[:]  # all the letters: 'a...z'

i = 10
alphabet[:i] + alphabet[i:]

# Slices with a step
alphabet[0::2]  # acegikmoqzuwy

# Special characters
'Python\'s strings'  # "Python's strings"
"Python's strings"  # "Python's strings"

'\N{COMMERCIAL AT}'  # '@'
'\x40'  # '@'
'\u0152'  # 'Œ'

r'\N{COMMERCIAL AT}'  # '\\N{COMMERCIAL AT}'
r'\x40'  # '\\x40'
r'\u0152'  # '\\u0152'

# Formatting string
begin = 'my'
'{} string {}'.format(begin, 'is empty')
# 'my string is empty'

begin = 'my'
'{1} string {0}'.format('is empty', begin)
# 'my string is empty'

"""Data types"""

type(alphabet)  # <class 'str'>
type(12)  # <class 'int'>
type('12')  # <class 'str'>
type(12.0)  # <class 'float'>
type(True)  # <class 'bool'>
type(1 < 2)  # <class 'bool'>
type(None)  # <class 'NoneType'>

# Type conversions
int('12')  # 12
str(12)  # '12'
try:
    int('12.0')  # ValueError
except:
    pass
try:
    int(alphabet)  # ValueError
except:
    pass
int(True)  # 1
int(False)  # 0
bool(7)  # True
bool(0)  # False
bool(None)  # False

"""Data structures"""

# Lists
list1 = []  # An empty list
list1 = list()  # Another way to create an empty list
list2 = [1, 2, 3]  # List containing 1, 2, and 3

list2[1]  # 2
list2[1] = 8
list2  # [1, 8, 3]
try:
    list2[4]  # Index error
except:
    pass

var1 = 3.14
var2 = 'my string'
list3 = [1, var1, 'Prolog', var2]
list3  # [1, 3.14, 'Prolog', 'my string']

list3[1:3]  # [3.14, 'Prolog']
list3[1:3] = [2.72, 'Perl', 'Python']
list3  # [1, 2.72, 'Perl', 'Python', 'my string']

list4 = [list2, list3]
# [[1, 8, 3], [1, 2.72, 'Perl', 'Python', 'my string']]

list4[0][1]  # 8
list4[1][3]  # 'Python'

list5 = list2
[v1, v2, v3] = list5

# List operations and functions
list2  # [1, 8, 3]
list3[:-1]  # [1, 2.72, 'Perl', 'Python']
[1, 2, 3] + ['a', 'b']  # [1, 2, 3, 'a', 'b']
list2[:2] + list3[2:-1]  # [1, 8, 'Perl', 'Python']
list2 * 2  # [1, 8, 3, 1, 8, 3]
[0.0] * 4  # Initializes a list of four 0.0s
# [0.0, 0.0, 0.0, 0.0]


list2  # [1, 8, 3]
list2[1] = 2  # [1, 2, 3]
len(list2)  # 3
list2.extend([4, 5])  # [1, 2, 3, 4, 5]
list2.append(6)  # [1, 2, 3, 4, 5, 6]
list2.append([7, 8])  # [1, 2, 3, 4, 5, 6, [7, 8]]
list2.pop(-1)  # [1, 2, 3, 4, 5, 6]
list2.remove(1)  # [2, 3, 4, 5, 6]
list2.insert(0, 'a')  # ['a', 2, 3, 4, 5, 6]

# Tuples
tuple1 = ()  # An empty tuple
tuple1 = tuple()  # Another way to create an empty tuple
tuple2 = (1, 2, 3, 4)
tuple2[3]  # 4
tuple2[1:4]  # (2, 3, 4)
try:
    tuple2[3] = 8  # Type error: Tuples are immutable
except:
    pass

list6 = ['a', 'b', 'c']
tuple3 = tuple(list6)  # conversion to a tuple: ('a', 'b', 'c')
type(tuple3)  # <class 'tuple'>
list7 = list(tuple2)  # [1, 2, 3, 4]

tuple4 = (tuple2, list6)  # ((1, 2, 3, 4), ['a', 'b', 'c'])
tuple4[0]  # (1, 2, 3, 4),
tuple4[1]  # ['a', 'b', 'c']
tuple4[0][2]  # 3
tuple4[1][1]  # 'b'
tuple4[1][1] = 'β'  # ((1, 2, 3, 4), ['a', 'β', 'c'])

# Sets
set1 = set()  # An empty set
set2 = {'a', 'b', 'c', 'c', 'b'}  # {'a', 'b', 'c'}
set2.add('d')  # {'a', 'b', 'c', 'd'}
set2.remove('a')  # {'b', 'c', 'd'}

list8 = ['a', 'b', 'c', 'c', 'b']
set3 = set(list8)  # {'a', 'b', 'c'}
iliad_chars = set(iliad.lower())
# The set of unique characters of the iliad string

print(sorted(iliad_chars))

"""
sort() calls the underlying operating system.
This means that it produces different results on different systems.
It does not work properly on OSX.
"""
import locale

loc = locale.getlocale()
locale.setlocale(locale.LC_ALL, loc)
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
accented = 'aàeéèêëiîïoôöuûüαβγ'
print("Without locale:", sorted(accented))
print("With locale:", sorted(accented, key=locale.strxfrm))

set2.intersection(set3)  # {'c', 'b'}
set2.union(set3)  # {'d', 'b', 'a', 'c'}
set2.symmetric_difference(set3)  # {'a', 'd'}
set2.issubset(set3)  # False
iliad_chars.intersection(set(alphabet))
# characters of the iliad string that are letters:
# {'a', 's', 'g', 'p', 'u', 'h', 'c', 'l', 'i',
#  'd', 'o', 'e', 'b', 't', 'f', 'r', 'n'}


# Dictionaries
wordcount = {}  # We create an empty dictionary
wordcount = dict()  # Another way to create a dictionary
wordcount['a'] = 21  # The key 'a' has value 21
wordcount['And'] = 10  # 'And' has value 10
wordcount['the'] = 18

wordcount['a']  # 21
wordcount['And']  # 10

'And' in wordcount  # True
'is' in wordcount  # False

try:
    wordcount['is']  # Key error
except:
    pass

wordcount.get('And')  # 10
wordcount.get('is', 0)  # 0
wordcount.get('is')  # None

wordcount.keys()  # dict_keys(['the', 'a', 'And'])
wordcount.values()  # dict_values([18, 21, 10])
wordcount.items()  # dict_items([('the', 18), ('a', 21),
# ('And', 10)])

my_dict = {}
my_dict[('And', 'the')] = 3  # OK, we use a tuple
try:
    my_dict[['And', 'the']] = 3  # Type error:
    # unhashable type: 'list'
except:
    pass

letter_count = {}
for letter in iliad.lower():
    if letter in alphabet:
        if letter in letter_count:
            letter_count[letter] += 1
        else:
            letter_count[letter] = 1

print('Iliad')
print(letter_count)

for letter in sorted(letter_count.keys()):
    print(letter, letter_count[letter])
print('---')
for letter in sorted(letter_count.keys(),
                     key=letter_count.get, reverse=True):
    print(letter, letter_count[letter])

"""Control structures"""

# Conditionals
char = '.'
digits = '0123456789'
punctuation = '.,;:?!'
if char in alphabet:
    print('Letter')
elif char in digits:
    print('Number')
elif char in punctuation:
    print('Punctuation')
else:
    print('Other')

# For in loop
sum = 0
for i in range(100):
    sum += i
print(sum)  # Sum of integers from 0 to 99: 4950
# Using the built-in sum() function,
# sum(range(100)) would produce the same result.

list10 = list(range(5))  # [0, 1, 2, 3, 4]

for inx, letter in enumerate(alphabet):
    print(inx, letter)

# While loop
sum, i = 0, 0
while i < 100:
    sum += i
    i += 1
print(sum)

sum, i = 0, 0
while True:
    sum += i
    i += 1
    if i >= 100:
        break
print(sum)

"""
Exceptions
"""
try:
    int(alphabet)
    int('12.0')
except:
    pass
print('Cleared the exception!')

try:
    int(alphabet)
    int('12.0')
except ValueError:
    print('Caught a value error!')
except TypeError:
    print('Caught a type error!')

"""
Functions
"""


def count_letters(text, lc=True):
    letter_count = {}
    if lc:
        text = text.lower()
    for letter in text:
        if letter.lower() in alphabet:
            if letter in letter_count:
                letter_count[letter] += 1
            else:
                letter_count[letter] = 1
    return letter_count


"""Comprehensions and Generators"""

# Comprehensions
word = 'acress'
splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
deletes = [a + b[1:] for a, b in splits if b]

print(splits, deletes)

splits = []
for i in range(len(word) + 1):
    splits.append((word[:i], word[i:]))

deletes = []
for a, b in splits:
    if b:
        deletes.append(a + b[1:])

print(splits, deletes)

# Generators
splits_generator = ((word[:i], word[i:])
                    for i in range(len(word) + 1))
for i in splits_generator: print(i)


# Generators using a function
def splits_generator_function():
    for i in range(len(word) + 1):
        yield (word[:i], word[i:])


splits_generator = splits_generator_function()
for i in splits_generator: print(i)

""" Modules"""
import math

math.sqrt(2)  # 1.4142135623730951
math.sin(math.pi / 2)  # 1.0
math.log(8, 2)  # 3.0

import statistics as stats

stats.mean([1, 2, 3, 4, 5])  # 3.0
stats.stdev([1, 2, 3, 4, 5])  # 1.5811388300841898

if __name__ == '__main__':
    print("Running the program")
    # Other statements
else:
    print("Importing the program")
    # Other statements

"""Basic File Input/Output"""

try:
    f_iliad = open('../../corpus/iliad.mb.txt', 'r')  # We open a file and we get a file object
    iliad_txt = f_iliad.read()  # We read all the file
    f_iliad.close()  # We close the file
    iliad_stats = count_letters(iliad_txt)  # We count the letters
    with open('iliad_stats.txt', 'w') as f:
        f.write(str(iliad_stats))
    # We automatically close the file
except:
    pass

odyssey = """Tell me, O Muse, of that many-sided hero who
traveled far and wide after he had sacked the famous town
of Troy."""
print('Start')
od = count_letters(odyssey)
for letter in sorted(od.keys()):
    print(letter, od[letter])

print('----')
od = count_letters(odyssey, False)
for letter in sorted(od.keys()):
    print(letter, od[letter])

"""Classes and Objects"""


class Text:
    """Text class to hold and process text"""

    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self, text=None):
        """The constructor called when an object
        is created"""

        self.content = text
        self.length = len(text)
        self.letter_counts = {}

    def count_letters(self, lc=True):
        """Function to count the letters of a text"""

        letter_counts = {}
        if lc:
            text = self.content.lower()
        else:
            text = self.content
        for letter in text:
            if letter.lower() in self.alphabet:
                if letter in letter_counts:
                    letter_counts[letter] += 1
                else:
                    letter_counts[letter] = 1
        self.letter_counts = letter_counts
        return letter_counts


txt = Text("""Tell me, O Muse, of that many-sided hero who
traveled far and wide after he had sacked the famous town
of Troy.""")
print(type(txt))
print(txt.length)
print(txt.content)

print(txt.count_letters())
print(txt.count_letters(False))

txt.my_var = 'a'
txt.content = open('../../corpus/iliad.mb.txt', 'r').read()
print(txt.count_letters())
print(txt.my_var)


class Word(Text):
    def __init__(self, word=None):
        super().__init__(word)
        self.part_of_speech = None

    def annotate(self, part_of_speech):
        self.part_of_speech = part_of_speech


word = Word('Muse')
print(word.length)
print(word.count_letters(lc=False))
word.annotate('Noun')
print(word.part_of_speech)

"""Functional Programming"""

text_lengths = map(len, [iliad, odyssey])
print(list(text_lengths))  # [100, 111]


def file_length(file):
    return len(open(file).read())


print(file_length('../../corpus/iliad.mb.txt'))

files = ['../../corpus/iliad.mb.txt', '../../corpus/odyssey.mb.txt']

text_lengths = map(lambda x: len(open(x).read()), files)
print(list(text_lengths))  # [807502, 610502]

text_lengths = (
    map(lambda x: (open(x).read(), len(open(x).read())),
        files))
text_lengths = list(text_lengths)
print([text_lengths[0][1], text_lengths[1][1]])  # [807502, 610502]

text_lengths = (
    map(lambda x: (x, len(x)),
        map(lambda x: open(x).read(), files)))
text_lengths = list(text_lengths)
print([text_lengths[0][1], text_lengths[1][1]])  # [807502, 610502]

import functools

char_count = functools.reduce(
    lambda x, y: x[1] + y[1],
    map(lambda x: (x, len(x)),
        map(lambda x: open(x).read(), files)))

print(char_count)

iliad = """Sing, O goddess, the anger of Achilles son of
Peleus, that brought countless ills upon the Achaeans."""
print(iliad)

iliad = 'Sing, O goddess, the anger of Achilles son of \
Peleus, that brought countless ills upon the Achaeans.'
print(iliad)

print(''.join(filter(lambda x: x in 'aeiou', iliad)))

''.join(filter(lambda x: x in 'aeiou',
               open('../../corpus/iliad.mb.txt').read()))

map(lambda y:
    ''.join(filter(lambda x: x in 'aeiou',
                   open(y).read())),
    files)

print(list(map(len,
               map(lambda y:
                   ''.join(filter(lambda x: x in 'aeiou',
                                  open(y).read())),
                   files))))

# print(list(map(lambda x: x if x in 'aeiuo' else '', map(lambda x: open(x).read(), files))))
