% Author: Pierre Nugues
% read_file(+File, -CharList)
read_file(File, CharList) :-
	open(File, read, Stream),
	read_list(Stream, CharList),
	close(Stream),
	!.

% read_list(+Stream, -List)
%  Reads characters from the the input
%  it reaches an eof.
read_list(Stream, [Char | List]) :-
	get_char(Stream, Char),
	Char \== end_of_file,
	!,
	read_list(Stream, List).
read_list(_, []).
