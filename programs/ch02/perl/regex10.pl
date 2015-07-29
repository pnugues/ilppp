# Differences between single and double quotes
$pattern = 'aaa\tbbb';
print $pattern, "\n";

$pattern2 = "ccc\t" . $pattern;

print $pattern2 . "\n";

# Variable substitution
$pattern3 = "my";
$pattern4 = "${pattern3} string\n";
print $pattern4;

# Metacharacters, specifically { and } [ and ]
$pattern5 = "my string";
$width = 10;
$line = <>;
if ($line =~ m/(.{0,$width}$pattern5.{0,$width})/) {
    print $1, "\n";
}

$regex = "(\w+)";
print $regex, "\n";
