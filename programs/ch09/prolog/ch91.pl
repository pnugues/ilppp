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


