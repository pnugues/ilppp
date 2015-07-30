% concordance(+Pattern, +List, +Span, -Line) 
% finds Pattern in List and displays the Line
% where it appears within Span characters
% surrounding it
:- use_module(library(lists)).

concord :-
    read_file('../../corpus/Selma.txt', L),
    normalize(L, L2),
    concordance('Helen', L2, 30, C),
    write(C), nl, 
    fail.

% concordance(+Pattern, +List, +Span, -Line) 
% finds Pattern in List and displays the Line
% where it appears within Span characters
% surrounding it

concordance(Pattern, List, Span, Line) :-
	atom_chars(Pattern, LPattern),
	prepend(LPattern, Span, LeftPattern),
	append(_, Rest, List),
	append(LeftPattern, End, Rest),
	prefix(End, Span, Suffix),
	append(LeftPattern, Suffix, LLine),
	atom_chars(Line, LLine).

% prefix(+List. +Span, -Prefix) extracts the prefix of
% List with up to Span characters
% The second rule is to check the case there are 
% less than Span character in List

prefix(List, Span, Prefix) :-
	append(Prefix, _, List),
	length(Prefix, Span),
	!.
prefix(Prefix, Span, Prefix) :-
	length(Prefix, L),
	L < Span.

% suffix(+List. +Span, -Suffix) extracts the suffix of
% List with up to Span characters

suffix(List, Span, Suffix) :-
	append(_, Suffix, List),
	length(Suffix, Span),
	!.
suffix(Suffix, Span, Suffix) :-
	length(Suffix, L),
	L < Span.


prepend(Pattern, Span, List) :-
	prepend(Pattern, Span, Pattern, List).

prepend(_, 0, List, List) :- !.
prepend(Pattern, Span, List, FList) :-
	Span1 is Span - 1,
	prepend(Pattern, Span1, [_ | List], FList).


% normalize(+List, -NormalizedList) 
% replaces contiguous white spaces with one blank

normalize([C1, C2 | L1], [' ' | L2]) :-
    char_type(C1, space),
    char_type(C2, space),
    !,
    normalize([C2 | L1], [' ' | L2]).
normalize([C1 | L1], [' ' | L2]) :-
    char_type(C1, space),
    !,
    normalize(L1, L2).
normalize([C1 | L1], [C1 | L2]) :-
    \+ char_type(C1, space),
    !,
    normalize(L1, L2).
normalize([], []).


read_file(FileName, CharList) :- 
	open(FileName, read, Stream, [encoding(utf8)]), 
	read_list(Stream, CharList), 
	close(Stream).
	
read_list(Stream, [C | L]) :- 
	get_char(Stream, C), 
	C \== end_of_file, % end of file 
	!, 
	read_list(Stream, L).
read_list(_, []).


