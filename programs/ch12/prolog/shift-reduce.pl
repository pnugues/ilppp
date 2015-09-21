% Author: Pierre Nugues

% Shift reduce
%?- shift_reduce([the, waiter, brought, the, meal], [s]).
% yes
% ?- shift_reduce([the, waiter, brought, the, meal], [np, vp]).
% yes

% shift_reduce(+Sentence, ?Category)
shift_reduce(Sentence, Category) :-
	shift_reduce(Sentence, [], Category).

% shift_reduce(+Sentence, +Stack, ?Category)
shift_reduce([], Category, Category).
shift_reduce(Sentence, Stack, Category) :-
	reduce(Stack, ReducedStack),
	write('Reduce: '), write(ReducedStack), nl,
	shift_reduce(Sentence, ReducedStack, Category).
shift_reduce(Sentence, Stack, Category) :-
	shift(Sentence, Stack, NewSentence, NewStack),
	write('Shift: '), write(NewStack), nl,	
	shift_reduce(NewSentence, NewStack, Category).

% shift(+Sentence, +Stack, -NewSentence, -NewStack),
shift([First | Rest], Stack, Rest, NewStack) :-
	append(Stack, [First], NewStack).

/*
It is possible to implement a reversed stack. See code here
shift([First | RestSentence], Stack, RestSentence, [First | Stack]).
*/

%reduce(+Stack, -NewStack)
reduce(Stack, NewStack) :-
	match_rule(Stack, NewStack).
reduce(Stack, NewStack) :-
	match_word(Stack, NewStack).

match_rule(Stack, ReducedStack) :-
	rule(Head, Expansion),
	append(StackBottom, Expansion, Stack),
	append(StackBottom, [Head], ReducedStack).

match_word(Stack, NewStack) :-
	append(StackBottom, Word, Stack),
	word(POS, Word),
	append(StackBottom, [POS], NewStack).
/*
It is possible to implement a reversed stack. See code here
match_rule(Stack, [Head | RestStack]) :-
	rule(Head, Expansion),
	reverse(Expansion, ExpansionRev),
	append(ExpansionRev, RestStack, Stack).

match_word([Word | Stack], [POS | Stack]) :-
	word(POS, [Word]).
*/

rule(s, [np, vp]).
rule(np, [d, n]).
rule(vp, [v]).
rule(vp, [v, np]).

word(d, [the]).
word(n, [waiter]).
word(n, [meal]).
word(n, [cat]).
word(v, [brought]).
word(v, [slept]).


