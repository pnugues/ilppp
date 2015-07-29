# The m// match operator and s/// substitution operator

while ($line = <>) {
    if ($line =~ m/ab+c/) {
	print "Old: ", $line;
	$line =~ s/ab+c/ABC/g;
	print "New: ", $line;
    }
}
