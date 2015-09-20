% Author: Pierre Nugues
% Compositional rules to build a semantic representation of
% I would like to hear something composed by Mozart

s(Sem) --> np(Sub), vp(Sub^Sem).

npx(SemNP) --> pro(SemNP).
npx(SemNP) --> noun(SemNP).
npx(SemNP) --> det, noun(SemNP).


np(SemNP) --> npx(SemVP^SemNP), vp_passive(SemVP).
np(SemNP) --> npx(SemNP).

verb_group(SemVG) --> verb(SemVG).
verb_group(SemVG) --> aux(SemAux), verb(SemVG).

vp(SemVP) --> verb_group(SemVP).
vp(SemVP) --> verb_group(Obj^SemVP), np(Obj).
vp(Subject^SemVP) --> verb_group(SemInf^Subject^SemVP), vp_inf(Subject^SemInf).
vp_passive(SemVP) --> verb(Sub^SemVP), [by], np(Sub).

vp_inf(SemVP) --> [to], vp(SemVP).

verb(Obj^Sub^like(Sub, Obj)) --> [like].
verb(Obj^Sub^hear(Sub, Obj)) --> [hear].
verb(Sub^Obj^compose(Sub, Obj)) --> [composed].


aux(would) --> [would].

pro('I') --> ['I'].
pro(something) --> [something].
pro(Modifier^something(Modifier)) --> [something].

noun(N) --> proper_noun(N).

proper_noun('Mozart') --> ['Mozart'].

det --> [some].

val1(Sem) :- s(Sem, ['I', like, something], []).
val2(Sem) :- s(Sem, ['I', would, like, something], []).
val3(Sem) :- s(Sem, ['I', would, like, to, hear, something], []).
val4(Sem) :- s(Sem, ['I', would, like, to, hear, something, composed, by, 'Mozart'], []).


