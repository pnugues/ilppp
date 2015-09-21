% Author: Pierre Nugues

% Nivre's parser to parse manually-annotated graphs (gold standard) 
% and produce an action sequence or
% produce a graph from an action sequence
% Author: Pierre Nugues 
% Complement to the book:
% Language processing using Perl and Prolog, Springer, 2006
% Two ways to use the program: 
% ?- nivre_parser(+Sentence, -Actions, +Graph) 
% ?- nivre_parser(+Sentence, +Actions, -Graph) 
% Example: 
% ?- words_0(S), deprel_0(G), nivre_parser(S, A, G).
% or 
% ?- words_0(S), nivre_parser(S, [sh, sh, la, sh, la, ra], G).

% Nivre's Dependency Shift reduce
% We store the words as 
% [w(id='0', form='ROOT', postag='ROOT'), w([id='1', form='ƒktenskapet', postag='NN']), w(), ...]
% We store the dependency arcs as d(Head, Dependent, Function).
% [w([id='1', form='ƒktenskapet', postag='NN', head=4, deprel='SS']), ...]

% nivre_parser(+Sentence, ?Operations, ?RefGraph)
% Generates the operation sequence from the graph and the graph
% from the operation sequence
% Two ways to use the program: 
% ?- nivre_parser(+Sentence, -Actions, +Graph) 
% ?- nivre_parser(+Sentence, +Actions, -Graph) 
nivre_parser(Sentence, Ops, RefGraph) :-
	nivre_parser(Sentence, [], Ops, [], RefGraph).
nivre_parser(_, [fail], _).

% Auxiliary predicate.
% nivre_parser(+Words, +Stack, -Ops, +CurGraph, +RefGraph)
% the mode corresponds to the gold-standard parsing
nivre_parser([], _, [], CurGraph, RefGraph) :-
	nonvar(RefGraph),
	!,
	subset(RefGraph, CurGraph),
	subset(CurGraph, RefGraph).
% nivre_parser(+Words, +Stack, +Ops, +CurGraph, -RefGraph)
% the mode corresponds to the transition list input
nivre_parser([], _, [], Graph, Graph).
nivre_parser(Words, Stack, [Op | Ops], Graph, RefGraph) :-
	oracle(Words, Stack, RefGraph, Op),
	execute_action(Op, Words, NWords, Stack, NStack, Graph, NGraph),
	nivre_parser(NWords, NStack, Ops, NGraph, RefGraph).

% execute_action(+Op, +Words, -NewWords, +Stack, -NewStack, +Graph, NewGraph)
% Executes the operation and produces a new parser state
execute_action(la, Words, Words, Stack, NStack, Graph, NGraph) :-
	left_arc(Words, Stack, NStack, Graph, NGraph).
execute_action(ra, Words, NWords, Stack, NStack, Graph, NGraph) :-
	right_arc(Words, NWords, Stack, NStack, Graph, NGraph).
execute_action(re, Words, Words, Stack, NStack, Graph, Graph) :-
	reduce(Stack, NStack, Graph).
execute_action(sh, Words, NWords, Stack, NStack, Graph, Graph) :-
	shift(Words, NWords, Stack, NStack).
execute_action(Op, _, _, _, _, _, _) :-
	\+ member(Op, [la, ra, re, sh]),
	write('Illegal action. Returning'), nl.

% oracle(+Words, +Stack, +Graph, -Operation)
% Predicts the next transition from the 
% manually-annoted graph
oracle(_, _, _, Op) :-
	nonvar(Op),
	!.
oracle([W | _], [T | _], Graph, la) :-
	T = w([id=IDT, form=FORMT, postag=POST | _]),
	W = w([id=IDW | _]),
	member(w([id=IDT, form=FORMT, postag=POST, head=IDW | _]), Graph),
	!.
oracle([W | _], [T | _], Graph, ra) :-
	T = w([id=IDT | _]),
	W = w([id=IDW, form=FORMW, postag=POSW | _]),
	member(w([id=IDW, form=FORMW, postag=POSW, head=IDT | _]), Graph),
	!.
oracle([W | _], [_ |Stack], Graph, re) :-
	member(K, Stack),
	K = w([id=IDK, form=FORMK, postag=POSK | _]),
	W = w([id=IDW, form=FORMW, postag=POSW | _]),
	(   
	member(w([id=IDK, form=FORMK, postag=POSK, head=IDW | _]), Graph)
	;
	member(w([id=IDW, form=FORMW, postag=POSW, head=IDK | _]), Graph)
	),
	!.
oracle(_, _, _, sh).

% left_arc(+Words, +Stack, -NewStack, +Graph, -NewGraph)
left_arc([W | _], [T | Stack], Stack, Graph, [w([id=IDT, form=FORMT, postag=POST, head=IDW, deprel=_]) | Graph]) :-
	W = w([id=IDW | _]),
	T = w([id=IDT, form=FORMT, postag=POST | _]),
	\+ member(w([id=IDT, form=FORMT | _]), Graph).

% right_arc(+Words, -NewWords, +Stack, -NewStack, +Graph, -NewGraph)
right_arc([W | Words], Words, [T | Stack], [W, T | Stack], Graph, [w([id=IDW, form=FORMW, postag=POSW, head=IDT, deprel=_]) | Graph]) :-
	W = w([id=IDW, form=FORMW, postag=POSW | _]),
	T = w([id=IDT | _]),
	\+ member(w([id=IDW, form=FORMW | _]), Graph).

% reduce(+Stack, -NewStack, +Graph)
reduce([T | Stack], Stack, Graph) :-
	T = w([id=IDT, form=FORMT | _]),
	member(w([id=IDT, form=FORMT | _]), Graph).

% shift(+Words, -NewWords, +Stack, -NewStack)
shift([First | Words], Words, Stack, [First | Stack]).


	
	

