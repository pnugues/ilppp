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


