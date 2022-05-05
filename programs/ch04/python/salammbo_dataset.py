"""
Character frequencies by chapter from Salammbô in French and English
"""
__author__ = 'Pierre Nugues'

import regex as re

base_folder = '../../corpus/Salammbo/'
salammbo_files_fr = ['salammbo_ch01.txt', 'salammbo_ch02.txt', 'salammbo_ch03.txt', 'salammbo_ch04.txt',
                     'salammbo_ch05.txt', 'salammbo_ch06.txt', 'salammbo_ch07.txt', 'salammbo_ch08.txt',
                     'salammbo_ch09.txt', 'salammbo_ch10.txt', 'salammbo_ch11.txt', 'salammbo_ch12.txt',
                     'salammbo_ch13.txt', 'salammbo_ch14.txt', 'salammbo_ch15.txt']
salammbo_files_en = ['salammbo_en_ch01.txt',
                     'salammbo_en_ch02.txt', 'salammbo_en_ch03.txt', 'salammbo_en_ch04.txt', 'salammbo_en_ch05.txt',
                     'salammbo_en_ch06.txt', 'salammbo_en_ch07.txt', 'salammbo_en_ch08.txt', 'salammbo_en_ch09.txt',
                     'salammbo_en_ch10.txt', 'salammbo_en_ch11.txt', 'salammbo_en_ch12.txt', 'salammbo_en_ch13.txt',
                     'salammbo_en_ch14.txt', 'salammbo_en_ch15.txt']

salammbo_files_fr = [base_folder + file for file in salammbo_files_fr]
salammbo_files_en = [base_folder + file for file in salammbo_files_en]
salammbo_files = salammbo_files_fr + salammbo_files_en


def count_chars(text: str) -> dict[str, int]:
    char_counts = {}
    for char in text:
        char_counts[char] = char_counts.get(char, 0) + 1
    return char_counts


def count_chars_by_chap(char_count_by_chap, files, lang):
    char_count_by_chap[lang] = dict()
    for i, file in enumerate(files, start=1):
        text = open(file).read().strip()
        text = re.sub(r'\s+', ' ', text)
        char_counts = count_chars(text.upper())
        char_count_by_chap[lang][i] = char_counts
    return char_count_by_chap


char_count_by_chap = dict()
char_count_by_chap = count_chars_by_chap(char_count_by_chap,
                                         salammbo_files_fr,
                                         'fr')
char_count_by_chap = count_chars_by_chap(char_count_by_chap,
                                         salammbo_files_en,
                                         'en')

# We compute the sum of all uppercase chars for Salammbô in French
char_counts = dict()
char_counts['fr'] = dict()
for chap in char_count_by_chap['fr'].keys():
    for char in char_count_by_chap['fr'][chap]:
        char_counts['fr'][char] = char_counts['fr'].get(char, 0) + char_count_by_chap['fr'][chap][char]

print('Frequencies of characters. Letters set in uppercase')
print('Full text in French')
for char in sorted(char_counts['fr']):
    print(char, char_counts['fr'][char])
print()

the_char = 'A'
# the_char = 'E'
print('Frequencies by chapter and by language')
for lang in ['fr', 'en']:
    print(lang)
    print('{:4}\t{:6}\t{}{}'.format('chap', '#chars', '#', the_char))
    for i, chap in enumerate(char_count_by_chap[lang], start=1):
        print('{:4}\t{:6}\t{}'.format(i, sum(char_count_by_chap[lang][chap].values()),
              char_count_by_chap[lang][chap][the_char]))
    print()
