% Author: Pierre Nugues
% Program to count the frequencies of word in a file

:- ['read_file.pl'].
:- ['tokenize.pl'].
:- ['count_duplicates.pl'].

count_unigrams(File, UnigramList) :-
    read_file(File, CharacterList), 
    tokenize(CharacterList, TokenList), 
    msort(TokenList, OrderedTokens), %quicksort 
    count_duplicates(OrderedTokens, UnigramList).
