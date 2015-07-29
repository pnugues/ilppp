use utf8;
binmode(STDOUT, ":encoding(UTF-8)");
binmode(STDIN, ":encoding(UTF-8)");

$text = <>;
while ($line = <>) { 
   $text .= $line;
}
# The next line is a very primitive tokenizer
$text =~ tr/a-zåàâäæçéèêëîïôöœßùûüÿA-ZÅÀÂÄÆÇÉÈÊËÎÏÔÖŒÙÛÜŸ/\n/cs;

@words = split(/\n/, $text);
for ($i = 0; $i < $#words; $i++) {
	$bigrams[$i] = $words[$i] . " " . $words[$i + 1];
}
for ($i = 0; $i < $#words; $i++) {
	if (!exists($frequency_bigrams{$bigrams[$i]})) {
		$frequency_bigrams{$bigrams[$i]} = 1;
	} else {
		$frequency_bigrams{$bigrams[$i]}++;
	}
}
foreach $bigram (sort keys %frequency_bigrams){
	print "$frequency_bigrams{$bigram} $bigram \n";
}
