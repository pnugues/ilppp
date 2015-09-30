# The \b class

while ($line = <>) {
    if ($line =~ m/(\bact\b)/) {
	    print "Word: ", $1;
    }
}
