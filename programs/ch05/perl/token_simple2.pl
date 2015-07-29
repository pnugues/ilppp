$text = <>; 
while ($line = <>) {  
  $text .= $line; 
} 
# Separate the punctuation from the words
$text =~ s/([,;:?!#$%&\-\/\\])/ $1 /g;
# Separate the dots
$text =~ s/\./ . /g;
# Separate the brackets
$text =~ s/(["\(\)\[\]{}\<\>])/ $1 /g;
# Left and back quotes
$text =~ s/(``|`|''|')/ $1 /g;
# Remove leading spaces
$text =~ s/^ *//g;
# Tokenize according to white spaces
$text =~ s/\s+/\n/g; 
print $text; 
