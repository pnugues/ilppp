# The tr/// operator with modifiers

while ($line = <>) {
#    $line =~ tr/AEIOUaeiou//d;
    $line =~ tr/AEIOUaeiou/$/cs;
    print $line;
}
