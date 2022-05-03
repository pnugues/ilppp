% Author: Pierre Nugues
% 2002--2010
% This file contains a program to compute the entropy and cross entropy
% Typical usage:
e(E):-
	read_file('../../corpus/Salammbo/salammbo_wikisource.txt', L),
	clean_text(L, CL),
	entropy(CL, E).

ce1(CE) :-
	read_file('../../corpus/Salammbo/salammbo_wikisource.txt', L1),
	clean_text(L1, CL1),
	read_file('../../corpus/Salammbo/salammbo_wikisource.txt', L2),
	clean_text(L2, CL2),
	cross_entropy(CL1, CL2, CE).
ce2(CE) :-
	read_file('../../corpus/Salammbo/salammbo_train_wikisource.txt', L1),
	clean_text(L1, CL1),
	read_file('../../corpus/Salammbo/salammbo_train_wikisource.txt', L2),
	clean_text(L2, CL2),
	cross_entropy(CL1, CL2, CE).
ce3(CE) :-
	read_file('../../corpus/Salammbo/salammbo_ch15.txt', L1),
	clean_text(L1, CL1),
	read_file('../../corpus/Salammbo/salammbo_ch15.txt', L2),
	clean_text(L2, CL2),
	cross_entropy(CL1, CL2, CE).

ce4(CE) :-
	read_file('../../corpus/Salammbo/salammbo_train_wikisource.txt', L1),
	clean_text(L1, CL1),
	read_file('../../corpus/Salammbo/salammbo_ch15.txt', L2),
	clean_text(L2, CL2),
	cross_entropy(CL1, CL2, CE).

ce5(CE) :-
	read_file('../../corpus/notredame.txt', L1),
	clean_text(L1, CL1),
	read_file('../../corpus/notredame.txt', L2),
	clean_text(L2, CL2),
	cross_entropy(CL1, CL2, CE).
ce6(CE) :-
	read_file('../../corpus/Salammbo/salammbo_train_wikisource.txt', L1),
	clean_text(L1, CL1),
	read_file('../../corpus/notredame.txt', L2),
	clean_text(L2, CL2),
	cross_entropy(CL1, CL2, CE).
ce7(CE) :-
	read_file('../../corpus/iliad.mb.txt', L1),
	clean_text(L1, CL1),
	read_file('../../corpus/iliad.mb.txt', L2),
	clean_text(L2, CL2),
	cross_entropy(CL1, CL2, CE).
ce8(CE) :-
	read_file('../../corpus/Salammbo/salammbo_train.txt', L1),
	clean_text(L1, CL1),
	read_file('../../corpus/iliad.mb.txt', L2),
	clean_text(L2, CL2),
	cross_entropy(CL1, CL2, CE).
ce9(CE) :-
	read_file('../../corpus/1984/1984.txt', L1),
	clean_text(L1, CL1),
	read_file('../../corpus/1984/1984.txt', L2),
	clean_text(L2, CL2),
	cross_entropy(CL1, CL2, CE).
ce10(CE) :-
	read_file('../../corpus/Salammbo/salammbo_train_wikisource.txt', L1),
	clean_text(L1, CL1),
	read_file('../../corpus/1984/1984.txt', L2),
	clean_text(L2, CL2),
	cross_entropy(CL1, CL2, CE).

base_folder('../../corpus/Salammbo/') :- !.
%base_folder('') :- !.
salammbo_files(['salammbo_wikisource.txt']) :- !.
%salammbo_files(['salammbo_ch01.txt', 'salammbo_ch02.txt', 'salammbo_ch03.txt', 'salammbo_ch04.txt', 'salammbo_ch05.txt', 'salammbo_ch06.txt', 'salammbo_ch07.txt', 'salammbo_ch08.txt', 'salammbo_ch09.txt', 'salammbo_ch10.txt', 'salammbo_ch11.txt', 'salammbo_ch12.txt', 'salammbo_ch13.txt', 'salammbo_ch14.txt', 'salammbo_ch15.txt', 'salammbo_en_ch01.txt', 'salammbo_en_ch02.txt', 'salammbo_en_ch03.txt', 'salammbo_en_ch04.txt', 'salammbo_en_ch05.txt', 'salammbo_en_ch06.txt', 'salammbo_en_ch07.txt', 'salammbo_en_ch08.txt', 'salammbo_en_ch09.txt', 'salammbo_en_ch10.txt', 'salammbo_en_ch11.txt', 'salammbo_en_ch12.txt', 'salammbo_en_ch13.txt', 'salammbo_en_ch14.txt', 'salammbo_en_ch15.txt']) :- !.

% compute_freqs_all_files(+Letter), where Letter is 'A' or 'E' in the book examples
compute_freqs_all_files(Letter) :-
	salammbo_files(SalammboFiles),
	base_folder(BF),
	apply_files(Letter, SalammboFiles, BF),
	!.

apply_files(_, [], _).
apply_files(Letter, [File | Files], BF) :-
	compute_freqs(Letter, File, BF),
	apply_files(Letter, Files, BF).

compute_freqs(Letter, File, BF):-
	concat(BF, File, Path),
	read_normalize_file(Path, CharList),
	char_frequencies(CharList, CharFreqs),
%	write(CharFreqs), nl,
	length(CharList, N),
	write(File), nl,
	member([Letter, P, F], CharFreqs),
	write('\tTotal chars: '), write(N), nl,
	write('\tFrequency '), write(Letter), write(': '), write(F), nl,
	write('\t'), write(' & '), write(N), write(' & '), write(F),nl,
	write('\tProbability '), write(Letter), write(': '), write(P), nl.


read_normalize_file(File, CharListUpper) :-
	read_file(File, CharListIn),
	atom_chars(Atom, CharListIn),
	normalize_space(chars(CharList), Atom),
	to_upper_case(CharList, CharListUpper).

% char_frequencies(+CharList, -Freqs)
%  computes the symbol probabilities and frequencies in a list.
char_frequencies(CharList, Freqs) :-
	sort(CharList, SymbolList),
	probabilities(CharList, SymbolList, Freqs).

% read_file(+File, -CharList)
read_file(File, CharList) :-
	open(File, read, Stream),
	read_list(Stream, CharList),
	close(Stream),
	!.

% read_list(+Stream, -List)
%  Reads characters from the the input
%  it reaches an eof.
read_list(Stream, [Char | List]) :-
	get_char(Stream, Char),
	Char \== end_of_file,
	!,
	read_list(Stream, List).
read_list(_, []).


% entropy(+CharList, -Entropy)
%  computes the entropy probability of all the symbols in a list.
entropy(CharList, Entropy) :-
	sort(CharList, SymbolList),
	probabilities(CharList, SymbolList, ProbList),
	entropy(ProbList, 0.0, Entropy).

%cross_entropy(+ModelList, +CharList, -Entropy)
%  computes the entropy probability of all the symbols in a list.
cross_entropy(ModelList, CharList, Entropy) :-
	sort(ModelList, SymbolList1),
	sort(CharList, SymbolList2),
	append(SymbolList1, SymbolList2, USortedSymbols),
	sort(USortedSymbols, SymbolList),
	probabilities(ModelList, SymbolList, ModelProbList),
	probabilities(CharList, SymbolList, TestProbList),
	write(ModelProbList), nl,
	write(TestProbList), nl,
	cross_entropy(ModelProbList, TestProbList, 0.0, Entropy).


% probabilities(+CharList, +SymbolList, -Probs)
%  computes the probabilities of all the symbols in a list.
probabilities(CharList, SymbolList, ProbList) :-
	length(CharList, TotalCount),
	count_symbols(SymbolList, CharList, TotalCount, ProbList).


% count_symbols(+SymbolSet, +List, +TotalCount, -FinalCount)
%  counts the frequency of all the symbols in a set.
count_symbols([], _, _, []).
count_symbols([Symbol | SymbolSet], CharList, TotalCount, [[Symbol, Prob, Freq] | FreqList]) :-
	count_symbol(Symbol, CharList, 0, Freq),
	Prob is Freq / TotalCount,
%	write(Symbol), write(': '), write(Freq), nl,
	count_symbols(SymbolSet, CharList, TotalCount, FreqList).


% count_symbol(+Symbol, +List, +CurrentCount, -FinalCount)
%  counts the frequency of a given symbol in a list
count_symbol(_, [], Count, Count).
count_symbol(Char, [Char | List], N, Count) :-
	!,
	N1 is N + 1,
	count_symbol(Char, List, N1, Count).
count_symbol(Char, [_ | List], N, Count) :-
	count_symbol(Char, List, N, Count).


% entropy(+ProbList, +CurrentEntropy, -Entropy)
%  computes the entropy of a list of symbols/probability
entropy([], Entropy, Entropy).
entropy([[_, Prob, _] | RestCount], Acc, Entropy) :-
	(   Prob =\= 0.0,
	    Ent is -Prob*(log(Prob)/log(2))
	;
	     Ent is 0
	),
	Acc1 is Ent + Acc,
	entropy(RestCount, Acc1, Entropy).

% cross_entropy(+ModelProbList, +TestProbList, +CurrentEntropy, -Entropy)
%  computes the entropy of a list of symbols/probability
cross_entropy([], [], Entropy, Entropy).
cross_entropy([[_, Model, _] | RestCountModel], [[_, Test, _] | RestCountTest], Acc, Entropy) :-
	(   Model =\= 0.0,
	    Ent is -Test*(log(Model)/log(2))
	;
	     Ent is 0
	),
	Acc1 is Ent + Acc,
	cross_entropy(RestCountModel, RestCountTest, Acc1, Entropy).


% clean_text(+DirtyList, -CleanList) removes the non-printable chars
clean_text([], []).
clean_text([Char | InList], [Char | OutList]) :-
	name(Char, [UNICODE]),
	UNICODE >= 32,
	!,
	clean_text(InList, OutList).
clean_text([_ | InList], OutList) :-
	clean_text(InList, OutList).

% to_lower_case(+InList, -OutList) sets the Input list into lower
%  case letters. For French only.
%  This predicate is no longer necessary.
%  Use upcase_atom/2 and downcase_atom instead
to_lower_case([], []).
to_lower_case([Char | InList], [LCChar | OutList]) :-
	downcase_atom(Char, LCChar),
	to_lower_case(InList, OutList).

% to_upper_case(+InList, -OutList) sets the Input list into upper
%  case letters. For French only.
to_upper_case([], []).
to_upper_case([Char | InList], [UCChar | OutList]) :-
	upcase_atom(Char, UCChar),
	to_upper_case(InList, OutList).

/*
accented('À', à).
accented('Â', â).
accented('Ä', ä).
accented('Å', å).
accented('Æ', æ).
accented('Ç', ç).
accented('É', é).
accented('È', è).
accented('Ê', ê).
accented('Ë', ë).
accented('Î', î).
accented('Ï', ï).
accented('Ô', ô).
accented('Ö', ö).
accented('Œ', 'œ').
accented('Ù', ù).
accented('Û', û).
accented('Ü', ü).
accented('Ÿ', ÿ).
*/

% Dead code from here.
% Could not compute the entropy of Selma because of insufficient memory heap
%
count_duplicates([], CountedList, CountedList).
count_duplicates([Char | SortedChars], CountedList, FinalCounted) :-
	count_duplicates([Char | SortedChars], Char, 0, Count, RestChars),
	!,
	count_duplicates(RestChars, [[Char, Count] | CountedList], FinalCounted).

count_duplicates([X], X, N, Count, []) :-
	Count is N + 1.
count_duplicates([X, Y | Rest], X, N, Count, Rest) :-
	Y \== X,
	Count is N + 1.
count_duplicates([X, X | Rest], X, N, Count, RestChars) :-
	N1 is N + 1,
	!,
	count_duplicates([X | Rest], X, N1, Count, RestChars).

 %	tokenize(CharList, TokenList).

count_chars([], HashTable, HashTable).
count_chars([Char | CharList], HashTable, FinalTable):-
	increment_char(Char, HashTable, NewHashTable),
	count_chars(CharList, NewHashTable, FinalTable).

increment_char(Char, HashTable, [[Char, N1] | NewHashTable]) :-
	member([Char, N], HashTable),
	!,
	N1 is N + 1,
	subtract(HashTable, [Char, N], NewHashTable).
increment_char(Char, HashTable, [[Char, 1] | HashTable]).

