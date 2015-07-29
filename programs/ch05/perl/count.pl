use utf8;
binmode(STDOUT, ":encoding(UTF-8)");
binmode(STDIN, ":encoding(UTF-8)");

$text = <>;
while ($line = <>) { 
	$text .= $line;
}
$text =~ tr/a-zåàâäæçéèêëîïôöœßùûüÿA-ZÅÀÂÄÆÇÉÈÊËÎÏÔÖŒÙÛÜŸ/\n/cs;
@words = split(/\n/, $text);
for ($i = 0; $i <= $#words; $i++) {
	if (!exists($frequency{$words[$i]})) {
		$frequency{$words[$i]} = 1;
	} else {
		$frequency{$words[$i]}++;
	}
}
foreach $word (sort keys %frequency){
	print "$frequency{$word} $word\n";
}
