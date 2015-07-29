$text = <>; 
while ($line = <>) {  
    $text .= $line; 
} 
$text =~ s/\s+/\n/g; 
print $text; 
