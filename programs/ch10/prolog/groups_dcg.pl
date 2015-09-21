% Author: Pierre Nugues

% Multiword and group detector

% Test with:
test_multiword(Out) :-
	multiword_detector(['M.', 'Dupont', was, given, 500,
			    euros, in, front, of, the, casino], Out).

la_times(L) :-
	group_detector([critics, question, the, ability, of, a, relatively, small, group, of, big, integrated, prime, contractors, to, maintain, the, intellectual, diversity, that, formerly, provided, the, pentagon, with, innovative, weapons, with, fewer, design, staffs, working, on, military, problems, the, solutions, are, likely, to, be, less, varied], L).

la_times_2(S) :-
	la_times(L),
	modifier_detector(L, S).


% Multiwords
multiword(give_up) -->
	[give, up].
multiword(['<ENAMEX>', 'Helmut', 'Kohl', '</ENAMEX>']) -->
	['Helmut', 'Kohl'].
multiword(['<ENAMEX>', 'M.', Name, '</ENAMEX>']) -->
	['M.'], [Name],
	{
	atom_codes(Name, [Initial | _]),
	Initial >= 65, % must be an upper-case letter
	Initial =< 90
	}.
multiword(['<NUMEX>', Value, euros, '</NUMEX>']) -->
	[Value], [euros],
	{
	number(Value)
	}.
multiword(['<NUMEX>', '$', Value, '</NUMEX>']) -->
	['$'], [Value],
	{
	number(Value)
	}.

multiword(in_front_of) --> [in, front, of].
multiword(in_front) --> [in, front].


word_stream_multiword(Beginning, Multiword, End) -->
	beginning(Beginning),
	multiword(Multiword),
	end(End).

% This predicate detects the multiwords and don't remove the remaining words
multiword_detector(In, Out) :-
	word_stream_multiword(Beginning, Multiword, End, In, []),
	!,
	multiword_detector(End, Rest),
	append(Beginning, [Multiword], Head),
	append(Head, Rest, Out).
multiword_detector(End, End).

/*
% This predicate detects the multiwords and remves the remaining words
multiword_detector(In, [MultiWord | Out]) :-
	word_stream_multiword(_, MultiWord, End, In, []),
	multiword_detector(End, Out).
multiword_detector(_, []).
*/


%%%%%
% Noun groups

% First nominal expressions
nominal([NOUN | NOM]) --> noun(NOUN), nominal(NOM).
nominal([N]) --> noun(N).

% Nouns divide into common and proper nouns
noun(N) --> common_noun(N).
noun(N) --> proper_noun(N).

% noun_group(-NounGroup)
% detects a list of words making a noun group and
% unifies NounGroup with it
noun_group([D | N]) --> det(D), nominal(N).
noun_group(N) --> nominal(N).
noun_group([PRO]) --> pronoun(PRO).
noun_group(NG) -->
	adj_group(AG), nominal(NOM),
	{append(AG, NOM, NG)}.
noun_group(NG) -->
	det(D), adj_group(AG), nominal(NOM),
	{append([D | AG], NOM, NG)}.


% adj_group(-AdjGroup)
% detects a list of words making an adjective
% group and unifies AdjGroup with it

adj_group_x([RB, A]) --> adv(RB), adj(A).
adj_group_x([A]) --> adj(A).

adj_group(AG) --> adj_group_x(AG).
adj_group(AG) -->
	adj_group_x(AGX),
	adj_group(AGR),
	{append(AGX, AGR, AG)}.


verb_group([V]) --> tensed_verb(V).
verb_group([RB, V]) --> adv(RB), tensed_verb(V).


verb_group([AUX, V]) --> aux(AUX), past_participle(V).
verb_group([AUX, G]) --> aux(AUX), gerund(G).
verb_group([MOD, I]) --> modal(MOD), infinitive(I).
verb_group([to, I]) --> [to], infinitive(I).

verb_group([AUX, RB, V]) -->
	aux(AUX), adv(RB), past_participle(V).
verb_group([AUX1, AUX2, V]) -->
	aux(AUX1), aux(AUX2), past_participle(V).
verb_group([MOD, AUX, V]) -->
	modal(MOD), aux(AUX), past_participle(V).
verb_group([AUX]) -->
	aux(AUX).

group(NG) -->
	noun_group(Group),
	{append(['<NG>' | Group], ['</NG>'], NG)}.
group(VG) -->
	verb_group(Group),
	{append(['<VG>' | Group], ['</VG>'], VG)}.


det(the) --> [the].
det(a) --> [a].

common_noun(critics) --> [critics].
common_noun(ability) --> [ability].
common_noun(group) --> [group].
common_noun(contractors) --> [contractors].
common_noun(diversity) --> [diversity].
common_noun(weapons) --> [weapons].
common_noun(design) --> [design].
common_noun(staffs) --> [staffs].
common_noun(problems) --> [problems].
common_noun(solutions) --> [solutions].
common_noun(chancellor) --> [chancellor].

proper_noun(pentagon) --> [pentagon].

adv(relatively) --> [relatively].
adv(formerly) --> [formerly].
adv(likely) --> [likely].
adv(less) --> [less].

adj(small) --> [small].
adj(big) --> [big].
adj(prime) --> [prime].
adj(intellectual) --> [intellectual].
adj(innovative) --> [innovative].
adj(military) --> [military].
adj(fewer) --> [fewer].

adj(A) --> past_participle(A).
adj(A) --> gerund(A).


infinitive(be) --> [be].
infinitive(maintain) -->	[maintain].

tensed_verb(question) -->	[question].
tensed_verb(provided) -->	[provided].

past_participle(integrated) -->		[integrated].
past_participle(varied) -->	[varied].

gerund(doing) --> [doing].

modal(can) --> [can].

aux(are) --> [are].

prep(of) --> [of].
prep(with) --> [with].

relative_pronoun(that) --> [that].

pronoun(it) --> [it].

word_stream_group(Beginning, Group, End) -->
	beginning(Beginning),
	group(Group),
	end(End).


group_detector(In, Out) :-
	word_stream_group(Beginning, Group, End, In, []),
	group_detector(End, Rest),
	append(Beginning, [Group], Head),
	append(Head, Rest, Out).
group_detector(End, End).

ng(['<NG>'| NG]) --> [['<NG>'| NG]].
vg(['<VG>'| VG]) --> [['<VG>'| VG]].

prep_group([P | [NG]]) -->
	prep(P), ng(NG).

% Relative clause: The relative pronoun is the subject
relative_clause(RC) -->
	relative_pronoun(R),
	vg(VG),
	ng(NG),
	{append([R | [VG]], [NG], RC)}.

% Relative clause: The relative pronoun is the object
relative_clause(RC) -->
	relative_pronoun(R),
	ng(NG),
	vg(VG),
	{append([R | [NG]], [VG], RC)}.

infinitive_clause([['<VG>', to | VG], NG]) -->
	vg(['<VG>', to | VG]),
	ng(NG).
infinitive_clause([['<VG>', to | VG]]) -->
	vg(['<VG>', to | VG]).

modifier(MOD) -->
    prep_group(PG),
	{append(['<PG>' | PG], ['</PG>'], MOD)}.
modifier(MOD) -->
	relative_clause(RC),
	{append(['<RC>' | RC], ['</RC>'], MOD)}.
modifier(MOD) -->
	infinitive_clause(IC),
	{append(['<IC>' | IC], ['</IC>'], MOD)}.

modifier_detector(In, Out) :-
	word_stream_modifier(Beginning, Group, End, In, []),
	modifier_detector(End, Rest),
	append(Beginning, [Group], Head),
	append(Head, Rest, Out).
modifier_detector(End, End).

word_stream_modifier(Beginning, Group, End) -->
	beginning(Beginning),
	modifier(Group),
	end(End).


beginning(X, Y, Z) :- append(X, Z, Y).

end(X, Y, Z) :- append(X, Z, Y).


