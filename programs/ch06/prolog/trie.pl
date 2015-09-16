/*
 * Author Pierre Nugues
 */

/*
 * To build a trie, use the predicates
 * ?- make_wordlist('file.txt', WL), make_trie(WL, Trie).
 */

/* The file:
aaa
aab
abce
should produce the trie:
[a, [a, [a], [b]], [b, [c, [e]]]].
*/
% letter_tree([[a, [a, [a], [b]], [b, [c, [e]]]]]).

:- dynamic letter_tree/1.

make_wordlist(File, WordList) :-
    read_file(File, LChars),
    get_word(LChars, WordLChars, RestLChars),
    atom_chars(Word, WordLChars),
    make_wordlist(RestLChars, [Word], WordListR),
    reverse(WordListR, WordList).

make_wordlist([], WordList, WordList) :- !.
make_wordlist(LChars, WordList, FinalWordList) :-
    get_word(LChars, WordLChars, RestLChars),
    atom_chars(Word, WordLChars),
    make_wordlist(RestLChars, [Word | WordList], FinalWordList).

% make_trie(+WordList, -Trie)
make_trie([Word | WordList], Trie) :-
	make_trielist(Word, Word, WordTrie),
	make_trie(WordList, [WordTrie], Trie).

% make_trie(+WordList, -Trie, -FinalTrie)
make_trie([], T, T) :- !.
make_trie([Word | WordList], Trie, FinalTrie) :-
        insert_word_in_trie(Word, Word, Trie, NewTrie),
	make_trie(WordList, NewTrie, FinalTrie).

%Inserts a word in a trie
%The Leaf argument contains the type of the word in the
%insert_word_in_trie(+Word, +Leaf, +Trie, -NewTrie)
insert_word_in_trie(Word, Leaf, Trie, NewTrie) :-
	make_trielist(Word, Leaf, WordTrie),
	insert_wordtrie_in_trie(WordTrie, Trie, NewTrie).

%Inserts a word trie in a trie
%insert_wordtrie_in_trie(+WordTrie, +Trie, -NewTrie)
insert_wordtrie_in_trie([H | [T]], [[H, Leaf | BT] | LT], [[H, Leaf | NB] | LT]) :-
	atom(Leaf),
        !,
	insert_wordtrie_in_trie(T, BT, NB).
% Traverses a segment shared between the trie and the word
% and encounters a leaf. It assumes that the leaf is an atom.

insert_wordtrie_in_trie([H | [T]], [[H | BT] | LT], [[H | NB] | LT]) :-
        !,
	insert_wordtrie_in_trie(T, BT, NB).
% Traverses a segment shared between the trie and the word

insert_wordtrie_in_trie([H | T], [[HT | BT] | LT], [[HT | BT] | NB]) :-
        !,
	insert_wordtrie_in_trie([H | T], LT, NB).
% Traverses a non-shared segment

insert_wordtrie_in_trie(RW, RT, NB) :-
	append(RT, [RW], NB),
        !.
% Appends the remaining part of the word to the trie

%make_trielist(+Word, +Leave, -WordTtrie)
% Creates the trie for a single word.
%Leaf contains the type of the word
make_trielist(Word, Leaf, WordTrie) :-
        atom_chars(Word, CharList),
	make_trielist_aux(CharList, Leaf, WordTrie).

make_trielist_aux([X], Leaf, [X, Leaf]) :- !.
make_trielist_aux([X | L], Leaf, [X | [LS]]) :-
	make_trielist_aux(L, Leaf, LS).

% Checks if a word is in a trie
% is_word_in_trie(+WordChars, +Trie, -Lex)
is_word_in_trie([H | T], Trie, Lex) :-
        member([H | Branches], Trie),
        is_word_in_trie(T, Branches, Lex).
is_word_in_trie([], Trie, LexList) :-
        findall(Lex, (member(Lex, Trie), atom(Lex)), LexList),
        LexList \= [].
% We assume that the word type is an atom

/*
is_word_in_trie([], [Lex | _], Lex) :-
        \+ is_list(Lex).
is_word_in_trie([H | T], [[H | BT] | _], Lex) :-
	is_word_in_trie(T, BT, Lex).
is_word_in_trie([H | T], [[HT | _] | LT], Lex) :-
        H \= HT,
	is_word_in_trie([H | T], LT, Lex).
is_word_in_trie([H | T], [HeadTrie | RestTrie], Lex) :-
        \+ is_list(HeadTrie), % If it's not a list, just skip it. It's category information
	is_word_in_trie([H | T], RestTrie, Lex).

*/


read_file(File, L) :-
	see(File),
	read_file_aux([], LR),
	reverse(LR, L),
	seen,
        !.

read_file_aux(L, RL) :-
	get0(X),
	X =\= -1,
	!,
	atom_codes(C, [X]),
	read_file_aux([C | L], RL).
read_file_aux(L, L).

get_word(['\n' | L], [], L) :- !.
get_word([], [], []) :- !.
get_word([X | L], [X | W], RL) :-
	letter(X),
	get_word(L, W, RL),
        !.

letter(_) :- !.
%letter(X) :- member(X, [`a`, `b`, `c`, `d`, `e`, `f`, `g`, `h`, `i`, `j`, `k`, `l`, `m`, `n`, `o`, `p`, `q`, `r`, `s`, `t`, `u`, `v`, `w`, `x`, `y`, `z`]).


%member_trie(+Word, +Trie) answers yer or fails when Word is not a member
% of the Trie
member_trie(Word, Trie, Type) :-
    atom_chars(Word, LWord),
    is_word_in_trie(LWord, Trie, Type).


%find_differences(+WordList, +Trie, +ListOfDifferences)
find_differences([], _, []) :- !.
find_differences([Word | RestWords], Trie, Diff) :-
    member_trie(Word, Trie, _),
    !,
    find_differences(RestWords, Trie, Diff).
find_differences([Word | RestWords], Trie, [Word | Diff]) :-
    !,
    find_differences(RestWords, Trie, Diff).
