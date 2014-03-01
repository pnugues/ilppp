# More default variables: $&, $`, and $'

$line = "Tell me, O muse, of that ingenious hero
  who travelled far and wide after he had sacked 
  the famous town of Troy.";
$line =~ m/,.*,/;

print "Last match: ", $&, "\n";
print "Before: ", $`, "\n";
print "After: ", $', "\n";
