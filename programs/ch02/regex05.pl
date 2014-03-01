# Match variables inside m//

while ($line = <>) {
    if ($line =~ s/(.)\1\1/***/g) {
	print $line, "\n"; 
    } 
}
