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
	$mutual_info{$bigrams[$i]} = log(($#words + 1) * $frequency_bigrams{$bigrams[$i]}/($frequency{$words[$i]} * $frequency{$words[$i + 1]}))/log(2);
}

foreach $bigram (keys %mutual_info){
	@bigram_array = split(/ /, $bigram);
	print $mutual_info{$bigram}, " ", $bigram, "\t", $frequency_bigrams{$bigram}, "\t", $frequency{$bigram_array[0]}, "\t", $frequency{$bigram_array[1]}, "\n";
}