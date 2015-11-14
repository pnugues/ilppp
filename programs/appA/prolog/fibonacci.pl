% Fibonacci numbers defined as:
% fibonacci(n) = fibonacci(n- 1) + fibonacci(n - 2)
% with fibonacci(1) = 1 and fibonacci(2) = 1
% Author Pierre Nugues
:- dynamic fibonacci/2.

fibonacci(1, 1).
fibonacci(2, 1).
fibonacci(M, N) :-
	M > 2,
	M1 is M - 1, fibonacci(M1, N1),
	M2 is M - 2, fibonacci(M2, N2),
	N is N1 + N2,
	asserta((fibonacci(M, N) :- !)).
