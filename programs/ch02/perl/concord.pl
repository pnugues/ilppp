# Concordance program slightly modified from Doug Cooper. 
# In CORPORA Mailing list archive 
use utf8;
#binmode(STDOUT, ":encoding(UTF-8)");
#binmode(STDIN, ":encoding(UTF-8)");
#use open IO => ':utf8';

($file_name, $pattern, $width) = @ARGV;

open(FILE, "$file_name") || die "Could not open file $file_name.";

while ($line = <FILE>) {
	$text .= $line;
}
$pattern =~ s/ /\\s+/g; # Let spaces match across _and print_ newlines
$text =~ s/\s+/ /g; # Uncomment this to match/print newlines as spaces
while ($text =~ m/(.{0,$width}$pattern.{0,$width})/g ) {
	print "$1\n"; #$1 holds the match
	# print the string with 0..width
	# characters on either side
}

