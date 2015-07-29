# Quoting metachars in character classes

while ($line = <>) {
    if ($line =~ m/[a\t$1^d]/) {
#    if ($line =~ m/[\\\^\$1\]\-a]/) {
		print "no metachar: ", $line;
    }
}
