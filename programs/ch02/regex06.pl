# Match variables inside m//

while ($line = <>) {
    $line =~ s/\$ *([0-9]+)\.?([0-9]*)/$1 dollars and $2 cents/g;
    print $line, "\n"; 
}
