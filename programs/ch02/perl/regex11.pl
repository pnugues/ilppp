# Detecting nonASCII

while ($line = <>) {
    if ($line =~ m/[^\x00-\x7f]/) {
		print "NonASCII: ", $line;
    }
}
