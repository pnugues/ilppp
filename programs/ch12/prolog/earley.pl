% Author: Pierre Nugues

% The Earley chart parser.

e(Chart) :- parse([the, meal, of, the, day], np, Chart).
g(Chart) :- parse([the, waiter, brought, the, meal, of, the, day], s, Chart).

% arc(No, LHS, RHS, B, E).

parse(Words, Category, FinalChart) :-
	expand_chart([[arc(start, ['.', Category], 0, 0), 0, []]], [], Chart),
	earley_parser(Words, 0, FinalPos, Chart, FinalChart),
	member([arc(start, [Category, '.'], 0, FinalPos), _, _], FinalChart).

expand_chart([], Chart, Chart).
expand_chart([[Entry, Cnt, Crea] | Entries], Chart, NewChart) :-
	\+ member([Entry, _, _], Chart),
	!,
	length(Chart, Cnt),
	expand_chart(Entries, [[Entry, Cnt, Crea] | Chart], NewChart).
expand_chart([_ | Entries], Chart, NewChart) :-
	expand_chart(Entries, Chart, NewChart).

earley_parser([], FinalNode, FinalNode, Chart, Chart) :- !.
earley_parser(Words, Pos, FinalPos, Chart, FinalChart) :-
	predictor(Pos, Chart, PredChart),
	NextPos is Pos + 1,
	scanner(Words, RestWords, Pos, NextPos, PredChart, ScanChart),
	completer(NextPos, ScanChart, CompChart),
	!,
	earley_parser(RestWords, NextPos, FinalPos, CompChart, FinalChart).

predictor(CurPos, Chart, PredChart) :-
	findall(
	[arc(CAT, ['.' | RHS], CurPos, CurPos), X, []],
	(
		member([arc(LHS, ACTIVE_RHS, InitPos, CurPos), _, _], Chart),
		append(B, ['.', CAT | E], ACTIVE_RHS),
		rule(CAT, RHS),
		\+ member([arc(CAT, ['.' | RHS], CurPos, CurPos), _, _], Chart)
	),
	NewChartEntries),
	NewChartEntries \== [],
	write('predictor: '), write(NewChartEntries), nl,
	expand_chart(NewChartEntries, Chart, NewChart),
	predictor(CurPos, NewChart, PredChart),
	!.
predictor(_, Chart, Chart).

scanner([Word | RestWords], RestWords, CurPos, NextPos, Chart, ScaChart) :-
	findall(
	[arc(CAT, [Word, '.'], CurPos, NextPos), X, []],
	(
		word(CAT, [Word]),
		once((member([arc(LHS, ACTIVE_RHS, InitPos, CurPos), _, _], Chart),
		append(B, ['.', CAT | E], ACTIVE_RHS)))
	),
	NewChartEntries),
	NewChartEntries \== [],
	write('scanner: '), write(NewChartEntries), nl,
	expand_chart(NewChartEntries, Chart, ScaChart),
	!.
scanner(Words, Words, CurPos, NextPos, Chart, ScaChart) :-
	findall(
	[arc(CAT, [[], '.'], CurPos, NextPos), X, []],
	(
		word(CAT, []),
		once((member([arc(LHS, ACTIVE_RHS, InitPos, CurPos), _, _], Chart),
		append(B, ['.', CAT | E], ACTIVE_RHS)))
	),
	NewChartEntries),
	NewChartEntries \== [],
	write('scanner: '), write(NewChartEntries), nl,
	expand_chart(NewChartEntries, Chart, ScaChart),
	!.

%scanner(_, _, _).


completer(CurPos, Chart, CompChart) :-
	findall(
	[arc(LHS2, RHS3, PrevPos, CurPos), X, [Cnt | Prev]],
	(
		member([arc(LHS, COMPLETE_RHS, InitPos, CurPos), Cnt, _], Chart),
		append(_, ['.'], COMPLETE_RHS),
		member([arc(LHS2, RHS2, PrevPos, InitPos), _, Prev], Chart),
		append(B, ['.', LHS | E], RHS2),
		append(B, [LHS, '.' | E], RHS3),
		\+ member([arc(LHS2, RHS3, PrevPos, CurPos), _, _], Chart)
	),
	CompletedChartEntries),
	CompletedChartEntries \== [],
	write('completer: '), write(CompletedChartEntries), nl,
	expand_chart(CompletedChartEntries, Chart, NewChart),
	completer(CurPos, NewChart, CompChart),
	!.
completer(_, Chart, Chart).



rule(s, [np, vp]).
rule(np, [d, n]).
rule(np, [d, a, n]).
rule(np, [np, pp]).
rule(vp, [v, np, pp]).
rule(vp, [v]).
rule(vp, [v, np]).
rule(pp, [prep, np]).

word(n, [cat]).
word(v, [brought]).
word(v, [slept]).
word(d, [the]).
word(d, []).
word(n, [waiter]).
word(n, [meal]).
word(n, [day]).
word(prep, [of]).
