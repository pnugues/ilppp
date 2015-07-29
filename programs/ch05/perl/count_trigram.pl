$text = <>;
while ($line = <>) { 
   $text .= $line;
}
$text =~ tr/a-zåàâäæçéèêëîïôöœßùûüÿA-ZÅÀÂÄÆÇÉÈÊËÎÏÔÖŒÙÛÜ/\n/cs;

@words = split(/\n/, $text);
for ($i = 0; $i < $#words - 2; $i++) {
	$trigrams[$i] = $words[$i] . " " . $words[$i + 1] . " " . $words[$i + 2];
}
	
for ($i = 0; $i < $#words - 2; $i++) {
	if (!exists($frequency_trigrams{$trigrams[$i]})) {
		$frequency_trigrams{$trigrams[$i]} = 1;
	} else {
       		$frequency_trigrams{$trigrams[$i]}++;
	}
}
foreach $trigram (sort keys %frequency_trigrams ){
	print $frequency_trigrams{$trigram}, " ", $trigram, "\n";
}

