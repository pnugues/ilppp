# The m// match operator

while ($line = <>) {
    if ($line =~ m/ab+c/) {
        print $line;
    }
}
