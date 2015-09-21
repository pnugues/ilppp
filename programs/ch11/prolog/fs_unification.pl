% Author: Pierre Nugues
:- op(600, xfx, ':').

unif(FStr, FStr) :-
	!.
unif([F1:V1 | Rest1], [F1:V2 | Rest2]) :-
	!,
	unif(V1, V2),
	unif(Rest1, Rest2).
unif([F1:V1 | Rest1], [F2:V2 | Rest2]) :-
	F1 \= F2,
	unif(Rest1, [F2:V2 | Rest3]),
	unif(Rest2, [F1:V1 | Rest3]).

