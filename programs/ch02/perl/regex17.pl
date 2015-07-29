use POSIX qw(locale_h);
use locale;

setlocale(LC_ALL, "fr_FR.UTF-8");
@list = ("a", "A", "b", "B");
@list_sorted = sort(@list);
print @list_sorted, "\n";
