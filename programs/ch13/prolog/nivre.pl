% Author: Pierre Nugues

% Nivre's Dependency Shift reduce

test1(G) :-
	shift_reduce([w(the, 1), w(waiter, 2), w(brought, 3), w(the, 4), w(meal, 5)], G).
test2(G) :-
	shift_reduce([w(the, 1), w(waiter, 2), w(brought, 3), w(the, 4), w(meal, 5), w(of, 6), w(the, 7), w(day, 8)], G).
test3(G) :-
	shift_reduce([w(the, 1), w(waiter, 2), w(brought, 3), w(the, 4), w(meal, 5), w(of, 6), w(the, 7), w(day, 8)], G), member(d(_, _, pmod), G), member(d(_, _, pcomp), G).
test4(G) :-
	shift_reduce([w(the, 1), w(waiter, 2), w(brought, 3), w(the, 4), w(meal, 5), w(to, 6), w(the, 7), w(table, 8)], G), member(d(_,_,adv), G), member(d(_, _, pcomp), G).
test_sve(G) :-
	shift_reduce([w('på', 1), w('60-talet', 2), w('målade', 3), w(han, 4), w(tavlor, 5)], G).
% We store the dependency arcs as d(Head, Dependent, Function).

% shift_reduce(+Sentence, -Graph)
shift_reduce(Sentence, Graph) :-
	shift_reduce(Sentence, [], [], Graph).

% shift_reduce(+Words, +Stack, +CurrentGraph, -FinalGraph)
shift_reduce([], _, Graph, Graph).
shift_reduce(Words, Stack, Graph, FinalGraph) :-
	left_arc(Words, Stack, NewStack, Graph, NewGraph),
	write('left arc'), nl,
	shift_reduce(Words, NewStack, NewGraph, FinalGraph).
shift_reduce(Words, Stack, Graph, FinalGraph) :-
	right_arc(Words, NewWords, Stack, NewStack, Graph, NewGraph),
	write('right arc'), nl,
	shift_reduce(NewWords, NewStack, NewGraph, FinalGraph).
shift_reduce(Words, Stack, Graph, FinalGraph) :-
	reduce(Stack, NewStack, Graph),
	write(reduce), nl,
	shift_reduce(Words, NewStack, Graph, FinalGraph).
shift_reduce(Words, Stack, Graph, FinalGraph) :-
	shift(Words, NewWords, Stack, NewStack),
	write(shift),nl,
	shift_reduce(NewWords, NewStack, Graph, FinalGraph).





% left_arc(+WordList, +Stack, -NewStack, +Graph, -NewGraph)
left_arc([w(First, PosF) | _], [w(Top, PosT) | Stack], Stack, Graph, [d(w(First, PosF), w(Top, PosT), Function) | Graph]) :-
	word(First, FirstPOS),
	word(Top, TopPOS),
	drule(FirstPOS, TopPOS, Function, left),
	\+ member(d(_, w(Top, PosT), _), Graph).

% right_arc(+WordList, -NewWordList, +Stack, -NewStack, +Graph, -NewGraph)
right_arc([w(First, PosF) | Words], Words, [w(Top, PosT) | Stack], [w(First, PosF), w(Top, PosT) | Stack], Graph, [d(w(Top, PosT), w(First, PosF), Function) | Graph]) :-
	word(First, FirstPOS),
	word(Top, TopPOS),
	drule(TopPOS, FirstPOS, Function, right),
	\+ member(d(_, w(First, PosF), _), Graph).

% reduce(+Stack, -NewStack, +Graph)
reduce([w(Top, PosT) | Stack], Stack, Graph) :-
	member(d(_, w(Top, PosT), _), Graph).

% shift(+WordList, -NewWordList, +Stack, -NewStack)
shift([First | Words], Words, Stack, [First | Stack]).

/*
% Rules for English 
%drule(+HeadPOS, +DependentPOS, +Function, +Direction)
drule(noun, determiner, determinative, left).
drule(noun, adjective, attribute, left).
drule(verb, noun, subject, left).
drule(verb, pronoun, subject, left).
drule(verb, noun, object, right).
drule(verb, pronoun, object, right).
drule(verb, prep, adv, _).
drule(noun, prep, pmod, right).
drule(prep, noun, pcomp, right).

%word(+Word, +PartOfSpeech)
word(waiter, noun).
word(meal, noun).
word(day, noun).
word(table, noun).
word(the, determiner).
word(a, determiner).
word(brought, verb).
word(ran, verb).
word(of, prep).
word(to, prep).
*/


% Rules for Swedish 
%drule(+HeadPOS, +DependentPOS, +Function, +Direction)
drule(noun, determiner, determinative, left).
drule(noun, adjective, attribute, left).
drule(verb, noun, subject, _).
drule(verb, pronoun, subject, _).
drule(verb, noun, object, right).
drule(verb, pronoun, object, right).
drule(verb, prep, adv, _).
drule(prep, noun, pcomp, right).


%word(+Word, +PartOfSpeech)
word('på', prep).
word(han, pronoun).
word(målade, verb).
word('60-talet', noun).
word(tavlor, noun).
