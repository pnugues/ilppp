# Concordance program slightly modified from Doug Cooper. 
# In CORPORA Mailing list archive
# Concordances where the right context uses a lookahead
# This is to avoid advancing the matching start index past a concordance
# if the distance between two concordances is less than the context size,
# for instance less than 20 characters apart
# Program modified after a bug reported by Tel Monks
use utf8;
#binmode(STDOUT, ":encoding(UTF-8)");
#binmode(STDIN, ":encoding(UTF-8)");
#use open IO => ':utf8';
# use with:
# perl -w concord_perl2.pl helenus.txt 'Helenus' 20

($file_name, $pattern, $width) = @ARGV;

open(FILE, "$file_name") || die "Could not open file $file_name.";

while ($line = <FILE>) {
	$text .= $line;
}
$pattern =~ s/ /\\s+/g; # Let spaces match across _and print_ newlines
$text =~ s/\s+/ /g; # Uncomment this to match/print newlines as spaces
while ($text =~ m/(.{0,$width})($pattern)(?=(.{0,$width}))/g ) {
	print "$1$2$3\n"; #$1 holds the match
	# print the string with 0..width
	# characters on either side
}

