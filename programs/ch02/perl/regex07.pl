# m// and match variables

while ($line = <>) {
    while ($line =~ m/\$ *([0-9]+)\.?([0-9]*)/g) { 
	print "Dollars: ", $1, " Cents: ", $2, "\n"; 
    } 
}
