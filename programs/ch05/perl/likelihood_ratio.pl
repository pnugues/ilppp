$text = <>;
while ($line = <>) { 
    $text .= $line;
}
$text =~ tr/a-zåàâäæçéèêëîïôöœßùûüÿA-ZÅÀÂÄÆÇÉÈÊËÎÏÔÖŒÙÛÜŸ/\n/cs;

@words = split(/\n/, $text);
for ($i = 0; $i < $#words; $i++) {
    $bigrams[$i] = $words[$i] . " " . $words[$i + 1];
}
for ($i = 0; $i <= $#words; $i++) {
    $frequency{$words[$i]}++;
}
for ($i = 0; $i < $#words; $i++) {
    $frequency_bigrams{$bigrams[$i]}++;
}

for ($i = 0; $i < $#words; $i++) {
    $p = $frequency{$words[$i + 1]}/$#words;
    $p1 = $frequency_bigrams{$bigrams[$i]}/$frequency{$words[$i]};
    $p2= ($frequency{$words[$i + 1]} - $frequency_bigrams{$bigrams[$i]})/($#words - $frequency{$words[$i]});
    if (($p1 != 1) && ($p2 != 0)) {
	$likelihood_ratio{$bigrams[$i]} = 2*(
	    $frequency_bigrams{$bigrams[$i]} * log($p1) + ($frequency{$words[$i]} - $frequency_bigrams{$bigrams[$i]}) * log(1 - $p1) 
	     + ($frequency{$words[$i + 1]} - $frequency_bigrams{$bigrams[$i]}) * log($p2) + ($#words - $frequency{$words[$i]} - $frequency{$words[$i + 1]} + $frequency_bigrams{$bigrams[$i]}) * log(1 - $p2) 
	     - $frequency_bigrams{$bigrams[$i]} * log($p) - ($frequency{$words[$i]} - $frequency_bigrams{$bigrams[$i]}) * log(1 - $p)
              - ($frequency{$words[$i + 1]} - $frequency_bigrams{$bigrams[$i]}) * log($p) - ($#words - $frequency{$words[$i]} - $frequency{$words[$i + 1]} + $frequency_bigrams{$bigrams[$i]}) * log(1 - $p));
    }
}

foreach $bigram (keys %likelihood_ratio ){
	@bigram_array = split(/ /, $bigram);
	print $likelihood_ratio{$bigram}, " ", $bigram, "\t", $frequency_bigrams{$bigram}, "\t", $frequency{$bigram_array[0]}, "\t", $frequency{$bigram_array[1]}, "\n";
}
