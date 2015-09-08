:- encoding(utf8).
% The rules to parse:
% 	The waiter brought the meal
% 	The waiter brought the meal to the table
% 	The waiter brought the meal of the day

% You should consult this file and then query the interpreter
% with a sentence:
% ?-s([the, waiter, brought, the, meal, to, the, table], []).
% yes.
% or use it as a generator:
% ?-s(L, []).

% It would be a good idea to trace the execution


s --> np, vp.
np --> det, noun.
np --> np, pp.
vp --> verb, np.
vp --> verb, np, pp.
pp --> prep, np.


det --> [the].
det --> [a].
noun --> [waiter].
noun --> [meal].
noun --> [table].
noun --> [day].
verb --> [brought].
prep --> [to].
prep --> [of].


% Some rules to remove left recursion

npx --> det, noun.
np --> npx.
np --> npx, pp.

% Using variables to check gender agreement

np(Gender) --> det(Gender), noun(Gender).
det(m) --> [le].
det(f) --> [la].
noun(m) --> [garçon].
noun(f) --> [fille].

% Getting the syntactic struture
% The query
% ?- s(S, L, []). will result in:
% S = s(np(det(the), noun(waiter)), 
%          vp(verb(bring), np(det(the), noun(waiter)))),
%    L = [the, waiter, brought, the, waiter] ;
% and so on if you make the parser fail with ;

s(s(NP, VP)) --> np(NP), vp(VP).
np(np(D, N)) --> det(D), noun(N).
vp(vp(V, NP)) -->  verb(V), np(NP).

det(det(the)) --> [the].
det(det(a)) --> [a].
noun(noun(waiter)) --> [waiter].
noun(noun(meal)) --> [meal].
noun(noun(table)) --> [table].
noun(noun(tray)) --> [tray].
verb(verb(bring)) --> [brought].

% Getting the semantic structure
% The query ?- s(Semantics, [the, patron, ordered, a, meal], []).
% will result in 
% 	Semantics = ordered(patron, meal)

s(Semantics) --> np(Subject), vp(Subject^Semantics).
np(X) --> det, noun(X).
vp(Subject^Predicate) --> verb(Subject^Predicate).
vp(Subject^Predicate) --> verb(Object^Subject^Predicate), np(Object).
noun(waiter) --> [waiter].
noun(patron) --> [patron].
noun(meal) --> [meal].
verb(X^rushed(X)) --> [rushed].
verb(Y^X^ordered(X, Y)) --> [ordered].
verb(Y^X^brought(X, Y)) --> [brought].
det --> [a].
det --> [the].


