% Author: Pierre Nugues
% 2013
% This file contains two tokenizing programs that use a DCG grammar:
% tokenize_line/1 reads characters from the keyboard until
% it reaches an eof or a new line.
% tokenize_file/2 read characters from a file given in argument
% They use UTF-8.

% Usage example:
% tokenize_file('../../corpus/Salammbo/salammbo.txt', L), msort(L, LS), write(LS), length(LS, N).

:- ['../../appA/prolog/read_line.pl'].
:- ['../../appA/prolog/read_file.pl'].

tokenize_line(TokenList) :-
	read_line(CharList),
	tokens(TokenList, CharList, []).

tokenize_file(File, TokenList) :-
	read_file(File, CharList),
	tokens(TokenList, CharList, []).


tokens(Tokens) --> blank, !, tokens(Tokens).
tokens([FirstT | Tokens]) --> token(FirstT), !, tokens(Tokens).
tokens([]) --> [].

% A blank is a white space or a control character
blank --> [B], {char_type(B, cntrl), !}.
blank --> [B], {char_type(B, space), !}.

% A token is a sequence of alphanumeric characters
% or another symbol

token(Word) -->
  alphanumerics(List), {atom_chars(Word, List), !}.
token(Symbol) -->
  other(CSymbol), {atom_chars(Symbol, [CSymbol]), !}.

% A sequence of alphanumerics is an alphanumeric
% character followed by the rest of alphanumerics
% or a single alphanumeric character.
alphanumerics([L | LS]) -->
  alphanumeric(L), alphanumerics(LS).
alphanumerics([L]) --> alphanumeric(L).

% Here comes the definition of alphanumeric
% characters: digits and letters.
alphanumeric(D) --> [D], { char_type(D, alnum), !}.

% All other symbols come here
other(Symbol) --> [Symbol], !.


sentences([S | RS]) -->
  words_of_a_sentence(S),
  sentences(RS).
% The last sentence (punctuated)
sentences([S]) --> words_of_a_sentence(S).
% Last sentence (no final punctuation)
sentences([S]) --> words_without_punctuation(S).

words_of_a_sentence([P]) -->
  end_punctuation(P).
words_of_a_sentence([W | RS]) -->
  word(W),
  words_of_a_sentence(RS).

words_without_punctuation([W | RS]) -->
  word(W),
  words_without_punctuation(RS).
words_without_punctuation([W]) --> [W].

word(W) --> [W].

end_punctuation(P) --> [P], {end_punctuation(P), !}.

end_punctuation(P) :-
  member(P, ['.', ';', ':', '?', '!']).
