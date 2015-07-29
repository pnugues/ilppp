# This must be run with the command:
# perl -CS prog.pl <inputfile
# Detecting nonASCII, Greek, Greek blocks
use utf8; # To use UTF-8 characters in the program
use charnames ':full'; # To uses Unicode names

while ($line = <>) {
    if ($line =~ m/^\p{IsASCII}+$/) {
		print "line is ASCII: ", $line;
    }
    if ($line =~ m/\P{IsASCII}/) {
		print "line contains NonASCII: ", $line;
    }
    if ($line =~ m/\P{InBasic_Latin}/) {
		print "line contains non basic Latin: ", $line;
    }
    if ($line =~ m/^\p{InGreek_and_Coptic}+$/) {
		print "Line is in Greek and Coptic block: ", $line;
    }
    if ($line =~ m/^\p{Greek}+$/) {
		print "Line is Greek script: ", $line;
    }
    if ($line =~ m/\x{03B1}/) {
		print "Line contains alpha (code point): ", $line;
    }
    if ($line =~ m/\N{GREEK SMALL LETTER ALPHA}/) {
		print "Line contains alpha (Unicode name): ", $line;
    }
    if ($line =~ m/α/) {
		print "Line contains alpha (Direct char input): ", $line;
    }
    if ($line =~ m/\N{LATIN SMALL LETTER A}/) {
		print "Line contains a: ", $line;
    }
    if ($line =~ m/\N{LATIN SMALL LETTER O WITH DIAERESIS}/) {
		print "Line contains ö: ", $line;
    }
}
