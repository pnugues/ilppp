% Author Pierre Nugues
% Rules describing noun groups

% noun_group(-NounGroup)
% detects a list of words making a noun group and 
% unifies NounGroup with it
noun_group([D | N]) --> det(D), nominal(N).
noun_group(N) --> nominal(N).

noun_group([PN]) --> proper_noun(PN).
noun_group([PRO]) --> pronoun(PRO).

noun_group(NG) -->
	det(D), adj_group(AG), nominal(NOM),
	{append([D | AG], NOM, NG)}.
noun_group(NG) -->
	adj_group(AG), nominal(NOM),
	{append(AG, NOM, NG)}.

% Nominal expressions
nominal([NOUN | NOM]) --> noun(NOUN), nominal(NOM).
nominal([N]) --> noun(N).

% Nouns divide into common and proper nouns
noun(N) --> common_noun(N).
noun(N) --> proper_noun(N).

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


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% The POS rules

det(Pair) --> [Pair], { Pair = (_, 'DT') }.

common_noun(Pair) --> [Pair], { Pair = (_, 'NN') }.

proper_noun(Pair) --> [Pair], { Pair = (_, 'NNP') }.

pronoun(Pair) --> [Pair], { Pair = (_, 'PRP') }.

adv(Pair) --> [Pair], { Pair = (_, 'RB') }.

adj(Pair) --> [Pair], { Pair = (_, 'JJ') }.

adj(A) --> past_participle(A).
adj(A) --> gerund(A).


past_participle(Pair) --> [Pair], { Pair = (_, 'VBN') }.

gerund(Pair) --> [Pair], { Pair = (_, 'VBG') }.
