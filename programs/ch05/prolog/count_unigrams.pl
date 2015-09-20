% Author: Pierre Nugues
% Program to count the frequencies of words in a file

:- ['../../appA/prolog/read_file.pl'].
:- ['tokenize.pl'].
:- ['count_duplicates.pl'].

count_unigrams(File, UnigramList) :-
    read_file(File, CharacterList), 
    tokenize(CharacterList, TokenList), 
    msort(TokenList, OrderedTokens), %quicksort 
    count_duplicates(OrderedTokens, UnigramList).
