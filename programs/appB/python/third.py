"""Appendix B.
"""
__author__ = "Pierre Nugues"

alphabet = 'abcdefghijklmnopqrstuvwxyz'
try:
    int(alphabet)
    int('12.0')
except:
    pass
print('Cleared the exception')
# int(alphabet)
# int(12.0)
# print('Cleared the exception')

if __name__ == '__main__':
    print('Running the program')
else:
    print('Importing the program')
