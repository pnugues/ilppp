:- encoding(utf8).
% The rules to parse:
%	The waiter brought the meal
%	The waiter brought the meal to the table
%	The waiter brought the meal of the day

% You should consult this file and then query the interpreter
% with a sentence:
% ?-s([the, waiter, brought, the, meal, to, the, table], []).
% yes.
% or use it as a generator:
% ?-s(L, []).

% It would be a good idea to trace the execution


s --> np, vp.
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

