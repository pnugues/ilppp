
% edit_distance(+Source, +Target, -Edits, ?Cost).
edit_distance(Source, Target, Edits, Cost) :-
	edit_distance(Source, Target, Edits, 0, Cost).

edit_distance([], [], [], Cost, Cost).
edit_distance(Source, Target, [EditOp | Edits], Cost, FinalCost) :-
	edit_operation(Source, Target, NewSource, NewTarget, EditOp, CostOp),
	Cost1 is Cost + CostOp,
	edit_distance(NewSource, NewTarget, Edits, Cost1, FinalCost).


% edit_operation carries out one edit operation
% between a source string and a target string.
edit_operation([Char | Source], [Char | Target], Source, Target, ident, 0).
edit_operation([SChar | Source], [TChar | Target], Source, Target, sub(SChar,TChar), 2) :-
	SChar \= TChar.
edit_operation([SChar | Source], Target, Source, Target, del(SChar), 1).
edit_operation(Source, [TChar | Target], Source, Target, ins(TChar), 1).


% min_edit(+Source, +Target, -Cost).
min_edit(Source, Target, Cost) :-
	min_edit_matrix(Source, Target, Matrix),
	append(_, [LastCol], Matrix),
	append(_, [Cost], LastCol).
	
% min_edit(+Source, +Target, -Matrix).
min_edit_matrix(Source, Target, Matrix) :-
	length(Source, SLength),
	length(Target, TLength),
	IMax is SLength + 1,
	JMax is TLength + 1,
	first_column(IMax, FirstCol),
	double_loop(Source, Target, 0, JMax, FirstCol, Matrix).

double_loop(_, [], _, _, L, [L]) :- !.
double_loop(Source, [TChar | Target], J, JMax, PrevCol, [PrevCol | LList]) :-
	J < JMax,
	J1 is J + 1,
	distance(Source, TChar, PrevCol, [J1 | NextCol]),
	double_loop(Source, Target, J1, JMax, [J1 | NextCol], LList).


distance([Char], Char, [Sub, Del], [Ins, New]) :-
	Temp is min(Sub, Del + 1),
	New is min(Temp, Ins + 1).
distance([SChar], TChar, [Sub, Del], [Ins, New]) :-
	SChar \= TChar,
	Temp is min(Sub + 2, Del + 1),
	New is min(Temp, Ins + 1).
distance([Char | Source], Char, [Sub, Del | PrevCol], [Ins, New | NextCol]) :-
	Temp is min(Sub, Del + 1),
	New is min(Temp, Ins + 1),
	distance(Source, Char, [Del | PrevCol], [New | NextCol]).
distance([SChar | Source], TChar, [Sub, Del | PrevCol], [Ins, New | NextCol]) :-
	SChar \= TChar,
	Temp is min(Sub + 2, Del + 1),
	New is min(Temp, Ins + 1),
	distance(Source, TChar, [Del | PrevCol], [New | NextCol]).

first_column(IMax, FirstCol) :-
	loop(0, IMax, FirstCol).

loop(Max, Max, []) :- !.
loop(I, Max, [I | List]) :-
	I < Max,
	I1 is I + 1,
	loop(I1, Max, List).
