# Match variables inside m//

while ($line = <>) {
    if ($new = ($line =~ s/(.)\1\1/***/rg)) {
	print $new, "\n"; 
    } 
}
