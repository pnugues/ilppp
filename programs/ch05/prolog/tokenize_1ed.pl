% Author: Pierre Nugues
% 2002
% This file contains two tokenizing programs:
% tokenize_line/1 reads characters from the keyboard until 
% it reaches an eof or a new line.
% tokenize_file/2 read characters from a file given in argument
% They use the Latin 1 code plus some Windows extensions.


% tokenize_line(-TokenList)
%  Tokenizes the current input: reads a line of text
%  and breaks it into a list of atomic terms.
tokenize_line(TokenList) :-
	read_line(CharList),
	!,
	tokenize(CharList, TokenList).

% read_line(-Line)
%  Reads characters from the keyboard until 
%  it reaches an eof or a new line.
read_line([Char | List]) :-
	get0(Char),
	Char =\= -1,
	Char =\= 10,
	!,
	read_line(List).
read_line([]).

% tokenize_file(+File, -TokenList)
%  Tokenizes File: reads all the lines of the text
%  and breaks them into a list of atomic terms.
tokenize_file(File, TokenList) :-
	see(File),
	read_list(CharList),
	seen,
	!,
	tokenize(CharList, TokenList).

% read_list(-List)
%  Reads characters from the the input 
%  it reaches an eof.
read_list([Char | List]) :-
	get0(Char),
	Char =\= -1,
	!,
	read_list(List).
read_list([]).

% tokenize(+Chars, -Tokens)
%  breaks a list of characters into a list of tokens.
%  It uses blanks/2 that removes the blank characters from
%  the head of the list and token/3 that builds one
%  token from the characters of the head of the list.
tokenize([], []) :- !.
tokenize(Chars, Tokens) :-
	blanks(Chars, RemainingChars),
	tokenize(RemainingChars, Tokens),
	!.
tokenize(Chars, [Token | Tokens]) :-
	token(Chars, Token, RemainingChars),
	tokenize(RemainingChars, Tokens).

% blanks(+Chars, -RemainingChars)
%  Removes the blank characters from the head of the list of Chars
%  RemainingChars contains the rest of the list.
blanks([Char1, Char2 | Chars], [Char2 | Chars]) :-
	Char1 =< 32,
	Char2 > 32,
	!.
blanks([], []) :- !.
blanks([Char | Chars], RemainingChars) :-
	Char =< 32,
	blanks(Chars, RemainingChars).

% token(+Chars, -Token, -RemainingChars)
%  Builds one token from the characters of the head of the list.
%  Token is the built token and RemainingChars is the rest of the list
token(Chars, Token, RemainingChars) :-
	alphanumeric_token(Chars, TokenChars, RemainingChars),
	name(Token, TokenChars),
	!.
token(Chars, Token, RemainingChars) :-
	others(Chars, TokenChar, RemainingChars),
	name(Token, [TokenChar]).


% alphanumeric_token(+Chars, -TokenChars, -RemainingChars)
%  Returns the characters of the first token on the head
%  of the list.
alphanumeric_token([Char1, Char2 | Chars], [Char1], [Char2 | Chars]) :-
	alphanumeric(Char1),
	\+ alphanumeric(Char2),
	!.
alphanumeric_token([], [], []) :- !.
alphanumeric_token([Char | Chars], [Char | TokenChars], RemainingChars) :-
	alphanumeric(Char),
	!,
	alphanumeric_token(Chars, TokenChars, RemainingChars).

% alphanumeric(+Char)
%  Checks whether Char is alphanumeric. There are several
%  cases:
%  Lower-case letters without accent
alphanumeric(Char) :-
	97 =< Char,
	Char =< 122,
	!.
%  Upper-case letters without accent
alphanumeric(Char) :-
	65 =< Char,
	Char =< 90,
	!.
%  Accented characters. The values 215 and 247 correspond to
%  the multiplication and division: × ÷
alphanumeric(Char) :-
	192 =< Char,
	Char =< 255,
	Char =\= 215,
	Char =\= 247,
	!.
%  Digits
alphanumeric(Char) :- 
	48 =< Char,
	Char =< 57,
	!.
%  The oe, OE, and Y" letters
alphanumeric(Char) :-
	(Char =:= 140 ;  Char =:= 156 ; Char =:= 159),
	!.

others([Char | Chars], Char, Chars).
