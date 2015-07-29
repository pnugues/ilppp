# Match variables inside m//

while ($line = <>) {
    $nbr = ($line =~ s/(.)\1\1/***/g);
    print $line, "\n"; 
    print $nbr, " substitutions\n";
}
