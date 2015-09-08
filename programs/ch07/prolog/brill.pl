t1(L) :- tag([the/art, holy/adj, see/verb], L).
%L = [the/art, holy/adj, see/noun]

t2(L) :-  tag(['I'/pro, want/verb, to/to, table/noun, a/art, proposal/noun], L).

% tag(+InitialTaggedText, -TaggedText)
% Implementation of Brill's algorithm

tag(InitialTaggedText, TaggedText) :-
	bagof(alter(FromPOS, ToPOS, Condition),
		alter(FromPOS, ToPOS, Condition), Rules),
	forall(Rules, InitialTaggedText, TaggedText).

% Collect all the rules and apply them sequentially

forall([Rule | Rules], Text, TaggedText) :-
	apply(Rule, Text, AlteredText),
	forall(Rules, AlteredText, TaggedText).
forall([], TaggedText, TaggedText).

%Apply prevtag template
apply(alter(FromPOS, ToPOS, prevtag(POS)),
		[PrevWord/POS, Word/FromPOS | RemainingText],
		[PrevWord/POS, Word/ToPOS | RemainingText1] ) :-
	!,
	apply(alter(FromPOS, ToPOS, prevtag(POS)),
		[Word/ToPOS | RemainingText],
		[Word/ToPOS | RemainingText1] ).
apply(alter(FromPOS, ToPOS, prevtag(POS)),
		[X, Y | RemainingText], [X, Y | RemainingText1] ) :-
	apply(alter(FromPOS, ToPOS, prevtag(POS)),
		[Y| RemainingText], [Y | RemainingText1] ).
apply(alter(_, _, prevtag(_)), [X], [X]).

%The ordered contextual rules
alter(verb, noun, prevtag(adj)).
alter(noun, verb, prevtag(to)).
