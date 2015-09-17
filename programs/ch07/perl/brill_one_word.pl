# Programme montrant Brill avec le mot den
# Le corpus est talbanken.txt
# Une expression régulière utile pour trouver les cas correspondant à une règle
# .+\tden\tdt.+\n.+\tpp\t

$line_prev = <>;
$line = <>;
$pronoun_count = 0;
$det_count = 0;
$vb_count_pos = 0;
$pp_count_pos = 0;
$vb_count_neg = 0;
$pp_count_neg = 0;

while ($line_next = <>) {
    if ($line =~ m/den\tpn/i) {
	$pronoun_count = $pronoun_count + 1;
	if ($line_prev =~ m/\tvb\t/) {
	    $vb_count_pos = $vb_count_pos + 1;
	}
	if ($line_next =~ m/\tpp\t/) {
	    $pp_count_pos = $pp_count_pos + 1;
	}
    }
    if ($line =~ m/den\tdt/i) {
	$det_count = $det_count + 1;
	if ($line_prev =~ m/\tvb\t/) {
	    $vb_count_neg = $vb_count_neg + 1;
	}
	if ($line_next =~ m/\tpp\t/) {
	    $pp_count_neg = $pp_count_neg + 1;
	}
    }
    $line_prev = $line;
    $line = $line_next;
}
print "Pronoun count: ", $pronoun_count, "\n";
print "Det count: ", $det_count, "\n";
print "Verb count positive: ", $vb_count_pos, "\n";
print "Prep count positive: ", $pp_count_pos, "\n";
print "Verb count negative: ", $vb_count_neg, "\n";
print "Prep count negative: ", $pp_count_neg, "\n";
