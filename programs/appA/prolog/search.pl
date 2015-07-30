link(r1, r2). link(r1, r3). link(r1, r4). link(r1, r5). link(r2, r6). link(r2, r7). link(r3, r6). link(r3, r7). link(r4, r7). link(r4, r8). link(r6, r9).

s(X, Y) :- link(X, Y).
s(X, Y) :- link(Y, X).


goal(X) :- minautor(X).

minautor(r8).

%% depth_first_search(+Node, -Path)
depth_first_search(Node, Path) :-
	depth_first_search(Node, [], Path).

%% depth_first_search(+Node, +CurrentPath, -FinalPath)
depth_first_search(Node, Path, [Node | Path]) :-
	goal(Node).
depth_first_search(Node, Path, FinalPath) :-
	s(Node, Node1),
	\+ member(Node1, Path),
	depth_first_search(Node1, [Node | Path], FinalPath).


%% breadth_first_search(+Node, -Path)
breadth_first_search(Node, Path) :-
	bf_search_aux([[Node]], Path).

bf_search_aux([[Node | Path] | _], [Node | Path]) :- 
	goal(Node).
bf_search_aux([CurrentPath | NextPaths], FinalPath) :-
	expand(CurrentPath, ExpandedPaths),
	append(NextPaths, ExpandedPaths, NewPaths),
	bf_search_aux(NewPaths, FinalPath).


expand([Node | Path], ExpandedPaths) :-
	bagof([Node1, Node | Path],
	      (s(Node, Node1), \+ member(Node1, Path)),
	      ExpandedPaths),
	!.
expand(_, []).
