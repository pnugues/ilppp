% Author: Pierre Nugues
% 2013
% This file contains two tokenizing programs that use a DCG grammar:
% tokenize_line/1 reads characters from the keyboard until 
% it reaches an eof or a new line.
% tokenize_file/2 read characters from a file given in argument
% They use UTF-8.

% Usage example:
% tokenize_file('../corpus/Salammbo/salammbo.txt', L), msort(L, LS), write(LS), length(LS, N).

tokenize_line(TokenList) :-
	read_line(CharList),
	!,
	tokens(TokenList, CharList, []).

read_line([Char | List]) :-
	get_code(Char),
	Char =\= -1,
	Char =\= 10,
	!,
	read_line(List).
read_line([]).


tokenize_file(File, TokenList) :-
	open(File, read, Stream),
	read_list(Stream, CharList),
	close(Stream),
	!,
	tokens(TokenList, CharList, []).

read_list(Stream, [Char | List]) :-
	get_code(Stream, Char),
	Char =\= -1,
	!,
	read_list(Stream, List).
read_list(_, []).


tokens(Tokens) --> blank, {!}, tokens(Tokens). 
tokens([FirstT | Tokens]) --> 
  token(FirstT), {!}, tokens(Tokens). 
tokens([]) --> []. 
 
% A blank is a white space or a control character 
blank --> [B], {B =< 32, !}. 
 
% A token is a sequence of alphanumeric characters  
% or another symbol 
 
token(Word) --> 
  alphanumerics(List), {atom_codes(Word, List), !}. 
token(Symbol) --> 
  other(CSymbol), {atom_codes(Symbol, [CSymbol]), !}. 
 
% A sequence of alphanumerics is an alphanumeric  
% character followed by the rest of alphanumerics   
% or a single alphanumeric character. 
 
alphanumerics([L | LS]) --> 
  alphanumeric(L), alphanumerics(LS). 
alphanumerics([L]) --> alphanumeric(L). 
 
% Here comes the definition of alphanumeric  
% characters: digits, uppercase letters without   
% accent, lowercase letters without accent,   
% and accented characters. Here we only consider 
% letters common in French, German, and Swedish 
 
% digits 
alphanumeric(D) --> [D], { 48 =< D, D =< 57, !}. 
 
% uppercase letters without accent 
alphanumeric(L) --> [L], {65 =< L, L =< 90, !}. 
 
% lowercase letters without accent 
alphanumeric(L) --> [L], {97 =< L, L =< 122, !}. 
 
% accented characters 
alphanumeric(L) -->
  [L], {atom_codes(A, [L]), accented(A), !}. 
 
accented(L) :- 
  member(L, 
    ['à', 'â', 'ä', 'å', 'æ', 'ç', 'é', 'è', 'ê', 'ë',  
    'î', 'ï', 'ô', 'ö', 'œ', 'ù', 'û', 'ü', 'ÿ',
    'À', 'Â', 'Ä', 'Å', 'Æ', 'Ç', 'É', 'È', 'Ê', 'Ë', 
    'Î', 'Ï', 'Ô', 'Ö', 'Œ', 'Ù', 'Û', 'Ü', 'Ÿ']).
 
% All other symbols come here 
other(Symbol) --> [Symbol], {!}. 


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
