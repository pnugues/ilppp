% Author Pierre Nugues
% CoNLL 200 reader.

% next_sentence_conll(+Type, -Pairs) reads the CONLL formatted files and
% returns a list of pairs or triples with
% the word and its part of speech if Type = wordpos
% the POS and chunk type if Type = poschunk
% the word, the POS, and the chunk type if Type = all
next_sentence_conll(poschunk, [(T2, T3) | Tail]) :-
	read_line(CharList),
	CharList \= [],
	split_list_to_atoms(32, [_, T2, T3 | _], CharList, []),
	!,
	next_sentence_conll(poschunk, Tail).
next_sentence_conll(poschunk,[]).

next_sentence_conll(wordpos, [(T1, T2) | Tail]) :-
	read_line(CharList),
	CharList \= [],
	split_list_to_atoms(32, [T1, T2 | _], CharList, []),
	!,
	next_sentence_conll(wordpos, Tail).
next_sentence_conll(wordpos,[]).

next_sentence_conll(all, [(T1, T2, T3) | Tail]) :-
	read_line(CharList),
	CharList \= [],
	split_list_to_atoms(32, [T1, T2, T3 | _], CharList, []),
	!,
	next_sentence_conll(all, Tail).
next_sentence_conll(all,[]).


write_sentence(S) :-
	member(P, S),
	write(P),
	nl,
	fail.
write_sentence(_) :-
	nl.

% read_line/2 reads one line in a file
read_line([Char | List]) :-
	get0(Char),
	Char =\= -1,
	Char =\= 10,
	!,
	read_line(List).
read_line([]).

% split_list_to_atoms(+Sep, +Codes) splits a sequence of +Codes
% separated by +Sep into tokens and turns them into Prolog atoms
% Sep is normally 32.
split_list_to_atoms(Sep, [A | Rest]) --> 
	excluding(L, Sep), 
	[Sep], 
	{atom_codes(A, L), !}, 
	split_list_to_atoms(Sep, Rest).
split_list_to_atoms(Sep, [A]) --> 
	excluding(L, Sep), 
	{atom_codes(A, L), !}.

% This rules describes a token that does not contain a Sep
% character
excluding([C | Cs], Sep) --> [C], { C \== Sep }, excluding(Cs, Sep).
excluding([C], Sep) --> [C], { C \== Sep }.
