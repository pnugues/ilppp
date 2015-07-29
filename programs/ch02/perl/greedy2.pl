$text = <>;
while ($line = <>) { 
    $text .= $line;
}
if ($text =~ m/(.+?)/) {
    print "$1\n"; #$1 holds the match
}


