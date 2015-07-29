$text = <>;
while ($line = <>) { 
    $text .= $line;
}
while ($text =~ m/\<b\>(.*?)\<\/b\>/mg ) {
    print "$1\n"; #$1 holds the match
}


