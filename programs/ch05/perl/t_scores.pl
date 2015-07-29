use utf8;
binmode(STDOUT, ":encoding(UTF-8)");
binmode(STDIN, ":encoding(UTF-8)");

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
	$t_scores{$bigrams[$i]} = ($frequency_bigrams{$bigrams[$i]} - $frequency{$words[$i]} * $frequency{$words[$i + 1]}/($#words + 1))/sqrt($frequency_bigrams{$bigrams[$i]});
}

foreach $bigram (keys %t_scores ){
	@bigram_array = split(/ /, $bigram);
	print $t_scores{$bigram}, " ", $bigram, "\t", $frequency_bigrams{$bigram}, "\t", $frequency{$bigram_array[0]}, "\t", $frequency{$bigram_array[1]}, "\n";
}