"""Appendix B.
"""
__author__ = "Pierre Nugues"

"""zip and iterators"""
latin_alphabet = 'abcdefghijklmnopqrstuvwxyz'
len(latin_alphabet)  # 26
greek_alphabet = 'αβγδεζηθικλμνξοπρστυφχψω'
len(greek_alphabet)  # 24
cyrillic_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
len(cyrillic_alphabet)  # 33

la_gr = zip(latin_alphabet[:3], greek_alphabet[:3])
la_gr_cy = zip(latin_alphabet[:3], greek_alphabet[:3],
               cyrillic_alphabet[0:3])

la_gr.__next__()  # ('a', 'α')
la_gr.__next__()  # ('b', 'β')
la_gr.__next__()  # ('c', 'γ')
try:
    la_gr.__next__()
except:
    pass

la_gr_cy_list = list(la_gr_cy)

la_gr_cy_list  # [('a', 'α', 'а'), ('b', 'β', 'б'), ('c', 'γ', 'в')]
la_gr_cy_list  # [('a', 'α', 'а'), ('b', 'β', 'б'), ('c', 'γ', 'в')]

la_gr_cy_list = list(la_gr_cy)  # []

la_gr_cy = zip(latin_alphabet[:3], greek_alphabet[:3],
               cyrillic_alphabet[0:3])
list(zip(*la_gr_cy))  # [('a', 'b', 'c'), ('α', 'β', 'γ'), ('а', 'б', 'в')]
