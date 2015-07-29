use utf8;
binmode(STDOUT, ":encoding(UTF-8)");
binmode(STDIN, ":encoding(UTF-8)");

$text = <>;
while ($line = <>) { 
   $text .= $line;
}

$text =~ tr/a-zåàâäæçéèêëîïôöœßùûüÿA-ZÅÀÂÄÆÇÉÈÊËÎÏÔÖŒÙÛÜŸ'()\-,.?!:;/\n/cs;
   # The dash character must be quoted
$text =~ s/([,.?!:;()'\-])/\n$1\n/g;
$text =~ s/\n+/\n/g;
print $text;
