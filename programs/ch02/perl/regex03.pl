# The tr/// translate operator

while ($line = <>) {
    $line =~ tr/a-zäåö/A-ZÄÅÖ/;
    print $line;
}
