% Author: Pierre Nugues

% Getting the syntactic struture from a parse
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

