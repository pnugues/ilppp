% Author: Pierre Nugues
% Detector of nonprojective links. 
% To run the detector, type:
% deprel_2(Graph), nonproj_links(Graph, NPLinks).

% Loads examples of dependency graphs
:- [dgraph_examples].

% nonproj_links(+DepGraph, -NPL) returns nonprojective 
% links, where DepGraph is the set of dependency 
% relations and NPL, the nonprojective links.
% Links are encoded as 
% w([id=ID, form=FORM, postag=POSTAG, head=HEAD, deprel=DEPREL])
nonproj_links(DepGraph, NPL) :-
	nonproj_links(DepGraph, DepGraph, NPL).

nonproj_links(_, [], []).
nonproj_links(DepGraph, [Arc | T], NPL) :-
	range(Arc, MIN, MAX),
	proj_in_range(DepGraph, Arc, MIN, MAX),
	!,
	nonproj_links(DepGraph, T, NPL).
nonproj_links(DepGraph, [Arc | T], [Arc | NPL]) :-
	!,
	nonproj_links(DepGraph, T, NPL).


% range(+Arc, -MIN, +MAX) finds the range of Arc
range(w(Arc), MIN, MAX) :-
	member(id=DepPos, Arc),
	member(head=HeadPos, Arc),
	MIN is min(DepPos, HeadPos),
	MAX is max(DepPos, HeadPos).


% proj_in_range(+DepGraph, +Arc, +MIN, +MAX) succeeds 
% if all the arcs inside Arc are transitively  
% connected to its head or fails otherwise
proj_in_range(DepGraph, Arc, MIN, MAX) :-
	findall(w([id=DepPos, form=Dep, postag=POS, head=HeadPos]),
		(member(w([id=DepPos, form=Dep, postag=POS, head=HeadPos | _]), DepGraph),
		 DepPos > MIN, 
		 DepPos < MAX
		), 
		InRange),
	head_chains(DepGraph, InRange, Arc).


% head_chains(+DepGraph, +ArcsInRange, +Arc) succeeds
% if all the arcs in ArcsInRange are transitively
% connected to Arc
head_chains(_, [], _).
head_chains(DepGraph, [w([id=DepPosIR, form=DepIR, postag=POSIR, head=HeadPosIR]) | T], w([id=DepPos, form=Dep, postag=POS, head=HeadPos | _])) :-
	!,
	chain(DepGraph, w([id=DepPosIR, form=DepIR, postag=POSIR, head=HeadPosIR]), w([id=HeadPos, form=_, postag=_, head=_])),
	head_chains(DepGraph, T, w([id=DepPos, form=Dep, postag=POS, head=HeadPos | _])).


% chains(+DepGraph, +Arc, +Head) succeeds
% if Arc is transitively connected to Head
chain(_, w([id=_, form=_, postag=_, head=HeadPos]), w([id=HeadPos, form=_, postag=_, head=_])) :- !.
chain(DepGraph, w([id=_, form=_, postag=_, head=HeadPosIR]), w([id=HeadPos, form=_, postag=_, head=_])) :-
	member(w([id=HeadPosIR, form=HeadIR, postag=HeadPOS, head=HHPosIR | _]), DepGraph),
	chain(DepGraph, w([id=HeadPosIR, form=HeadIR, postag=HeadPOS, head=HHPosIR]), w([id=HeadPos, form=_, postag=_, head=_])).
