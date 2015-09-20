% Author: Pierre Nugues
% read_line(-Line)
%  Reads characters from the keyboard until
%  it reaches an eof or a new line.
read_line([Char | List]) :-
	get_char(Char),
	Char \== end_of_file,
	Char \== '\n',
	!,
	read_line(List).
read_line([]).

