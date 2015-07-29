($source, $target) = @ARGV;

$length_s = length($source);
$length_t = length($target);

# Initialize first row and column
for ($i = 0; $i <= $length_s; $i++) {
    $table[$i][0] = $i;
}
for ($j = 0; $j <= $length_t; $j++) {
    $table[0][$j] = $j;
}

# Get the characters. Start index is 0
@source = split(//, $source);
@target = split(//, $target);

# Fills the table. Start index of rows and columns is 1
for ($i = 1; $i <= $length_s; $i++) {
    for ($j = 1; $j <= $length_t; $j++) {
	# Is it a copy or a substitution?
	$cost = ($source[$i - 1] eq $target[$j - 1]) ? 0 : 2;
	# Computes the minimum
	$min = $table[$i-1][$j-1] + $cost;
	if ($min > $table[$i][$j-1] + 1) {
	    $min = $table[$i][$j-1] + 1;
	}
	if ($min > $table[$i-1][$j] + 1) {
	    $min = $table[$i-1][$j] + 1;
	}
	$table[$i][$j] = $min;
    }
}

for ($j = 0; $j <= $length_t; $j++) {
    for ($i = 0; $i <= $length_s; $i++) {
	print $table[$i][$j], " ";
    }
    print "\n";
}
print "Minimum distance: ", $table[$length_s][$length_t], "\n";


