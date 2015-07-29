% Author: Pierre Nugues
% 2012
% This file contains two tokenizing programs:
% tokenize_line/1 reads characters from the keyboard until
% it reaches an eof or a new line.
% tokenize_file/2 read characters from a file given in argument

% Same as tokenize_opt. Should be better but in fact slower
:- ['read_file.pl'].
:- ['read_line.pl'].

% tokenize_line(-TokenList)
%  Tokenizes the current input: reads a line of text
%  and breaks it into a list of atomic terms.
tokenize_line(TokenList) :-
	read_line(CharList),
	!,
	tokenize(CharList, TokenList).


% tokenize_file(+File, -TokenList)
%  Tokenizes File: reads all the lines of the text
%  and breaks them into a list of atomic terms.
tokenize_file(File, TokenList) :-
	read_file(File, CharCodes),
	!,
	tokenize(CharCodes, TokenList).

% tokenize(+CharCodes, -Tokens)
%  breaks a list of character codes into a list of tokens.
tokenize([], []).
tokenize([CharCode | RestCodes], Tokens) :- % a blank
	char_type(CharCode, space),
	!,
	tokenize(RestCodes, Tokens).
tokenize([CharCode | CharCodes], [Word | Tokens]) :- % an alphanumical
	char_type(CharCode, alnum),
	!,
	make_word([CharCode | CharCodes], alnum, WordCodes, RestCodes),
	atom_codes(Word, WordCodes),
	tokenize(RestCodes, Tokens).
tokenize([CharCode | CharCodes], [Char | Tokens]) :- % other
	!,
	atom_codes(Char, [CharCode]),
	tokenize(CharCodes, Tokens).

% make_word(+CharCodes, +Type, -WordCodes, -RestCodes)
make_word([CharCode1, CharCode2 | CharCodes], alnum, [CharCode1 | WordCodes], RestCodes) :-
	char_type(CharCode2, alnum),
	!,
	make_word([CharCode2 | CharCodes], alnum, WordCodes, RestCodes).
make_word([CharCode | RestCodes], alnum, [CharCode] , RestCodes).

