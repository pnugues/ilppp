% Author Pierre Nugues
% Reads, tokenizes, and counts the words of a file

% nwords(+File, -WordFrequencies)
nwords(File, WordCounts) :-
    read_file_to_codes(File, Codes, []),
    maplist(char_code, Chars, Codes),
    words(Words, Chars, []),
    maplist(downcase_atom, Words, LCWords),
    count_occurrences(LCWords, WordCounts).

% Returns a list of words from a list of characters
words(Words) --> blank, !, words(Words).
words([Word | Words]) --> word(Word), !, words(Words).
words([]) --> [].

word(Word) --> letters([Char | Chars]), {atom_chars(Word, [Char | Chars])}.

letters([L | Ls]) --> letter(L), !, letters(Ls).
letters([]) --> [].

letter(Char) --> [Char], {char_type(Char, alpha)}.

blank --> [Char], {\+ char_type(Char, alpha)}.

count_occurrences(Text, Occs):-
    findall(freq(W, Cnt), (bagof(true, member(W, Text), Ws), length(Ws, Cnt)), Occs).
