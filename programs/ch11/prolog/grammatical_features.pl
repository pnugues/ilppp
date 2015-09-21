% Author: Pierre Nugues
:- op(600, xfy, ':').

np(gend:G, num:N, case:C, pers:P, det:D) -->
	det(gend:G, num:N, case:C, pers:P, det:D),
	adj(gend:G, num:N, case:C, pers:P, det:D),
	n(gend:G, num:N, case:C, pers:P).
det(gend:masc, num:sg, case:nom, pers:3, det:def) --> [der].
det(gend:masc, num:sg, case:gen, pers:3, det:def) --> [des].
det(gend:masc, num:sg, case:dat, pers:3, det:def) --> [dem].
det(gend:masc, num:sg, case:acc, pers:3, det:def) --> [den].

adj(gend:masc, num:sg, case:nom, pers:3, det:def) --> [kleine].
adj(gend:masc, num:sg, case:gen, pers:3, det:def) --> [kleinen].
adj(gend:masc, num:sg, case:dat, pers:3, det:def) --> [kleinen].
adj(gend:masc, num:sg, case:acc, pers:3, det:def) --> [kleinen].

n(gend:masc, num:sg, case:nom, pers:3) --> ['Ober'].
n(gend:masc, num:sg, case:gen, pers:3) --> ['Obers'].
n(gend:masc, num:sg, case:dat, pers:3) --> ['Ober'].
n(gend:masc, num:sg, case:acc, pers:3) --> ['Ober'].



