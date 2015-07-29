# This must be run with the command:
# perl -CS prog.pl
# Printing Unicode names, 
use charnames ':full'; # To use Unicode names

# Unicode names
print "\N{LATIN CAPITAL LIGATURE OE}, \N{LATIN CAPITAL LETTER O WITH DIAERESIS}, \N{LATIN SMALL LETTER O WITH DIAERESIS}, \x{0152}, \x{00D6}", " \077 " , "\x40\n";
print "\N{LATIN CAPITAL LIGATURE OE}, \N{LATIN CAPITAL LETTER O WITH DIAERESIS}, \N{LATIN SMALL LETTER O WITH DIAERESIS}, \x{0152}, \x{00D6}", " \077 " , "\x40\n";
print "\N{LATIN CAPITAL LIGATURE OE}\n";
print "\N{LATIN SMALL LETTER O WITH DIAERESIS}\n";
print "\N{LATIN CAPITAL LIGATURE OE}, \N{LATIN SMALL LETTER O WITH DIAERESIS}\n";
print "\N{LATIN SMALL LETTER O WITH DIAERESIS}\n";
