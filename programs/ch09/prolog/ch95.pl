s(Sem) --> np(Sub), vp(Sub^Sem).

npx(SemNP) --> pro(SemNP).
npx(SemNP) --> noun(SemNP).
npx(SemNP) --> det, noun(SemNP).

np(SemNP) --> npx(SemNP).

verb_group(SemVG) --> verb(SemVG).
verb_group(SemVG) --> aux(SemAux), verb(SemVG).

vp(SemVP) --> verb_group(SemVP).
vp(SemVP) --> verb_group(Obj^SemVP), np(Obj).

verb(Obj^Sub^like(Sub, Obj)) --> [like].
verb(Obj^Sub^hear(Sub, Obj)) --> [hear].

aux(would) --> [would].

pro('I') --> ['I'].
pro(something) --> [something].

noun(N) --> proper_noun(N).

proper_noun('Mozart') --> ['Mozart'].

det --> [some].

val_sem_1(Sem) :- s(Sem, ['I', would, like, some, 'Mozart'], []).

