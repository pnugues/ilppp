% Author: Pierre Nugues
% 2002
% This file contains two tokenizing programs that use a DCG grammar:
% tokenize_line/1 reads characters from the keyboard until 
% it reaches an eof or a new line.
% tokenize_file/2 read characters from a file given in argument
% They use the Latin 1 code plus some Windows extensions.
% NE MARCHE PLUS AVEC UTF8

tokenize_line(TokenList) :-
	read_line(CharList),
	!,
	tokens(TokenList, CharList, []).

read_line([Char | List]) :-
	get0(Char),
	Char =\= -1,
	Char =\= 10,
	!,
	read_line(List).
read_line([]).


tokenize_file(File, TokenList) :-
	see(File),
	read_list(CharList),
	seen,
	!,
	tokens(TokenList, CharList, []).

read_list([Char | List]) :-
	get0(Char),
	Char =\= -1,
	!,
	read_list(List).
read_list([]).


tokens(Tokens) --> blank, tokens(Tokens), {!}.
tokens([FirstT | Tokens]) --> token(FirstT), tokens(Tokens), {!}.
tokens([]) --> [].

% A blank is a white space or a control character
blank --> [B], {B =< 32, !}.

% A token is a sequence of alphanumeric characters 
% or another symbol

token(Word) --> alphanumerics(List), {name(Word, List), !}.
token(Symbol) --> other(CSymbol), {name(Symbol, [CSymbol]), !}.

% A sequence of alphanumerics is an alphanumeric character 
% followed by the rest of alphanumerics or a 
% single alphanumeric character.

alphanumerics([L | LS]) --> alphanumeric(L), alphanumerics(LS).
alphanumerics([L]) --> alphanumeric(L).


% Here comes the definition of alphanumeric characters: digits,
% upper-case letters without accent, lower-case letters without 
% accent, and accented characters. Here we only consider
% letters comtained in the Latin 1 charset, OE, and oe.

% lower-case letters without accent
alphanumeric(L) --> [L], {97 =< L, L =< 122, !}.

% upper-case letters without accent
alphanumeric(L) --> [L], {65 =< L, L =< 90, !}.

% accented characters. The values 215 and 247 correspond to
% the multiplication and division: × ÷
alphanumeric(L) --> [L], {192 =< L, L =< 255, L =\= 215, L =\= 247, !}.

% digits
alphanumeric(D) --> [D], {48 =< D, D =< 57, !}.

% The oe, OE, and Y with umlaut letters
alphanumeric(D) --> [D], {D =:= 140, ! ;  D =:= 156, ! ; D =:= 159, !}.

%All other symbols come here
other(Symbol) --> [Symbol], {!}.
