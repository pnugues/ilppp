:- [tokenize_dcg].
% % A simplified version of the ELIZA program
% %

% The main loop reads the input and calls process/1
% It stops when the input is the word bye.

eliza :-
	write('Hello, I am ELIZA. How can I help you?'), nl,
	repeat,
	write('> '),
	tokenize_line(In),
	process(In).


% process/1 accepts the userís utterance. It either terminates
% or tries to find a template matching to the userís
% utterance

process([bye | _]) :-
	write('ELIZA: bye'), nl, !.
process(In) :-
	utterance(Out, In, []),
	!,
	write('ELIZA: '), write_answer(Out),
	fail.

% utterance is a DCG rule describing a set of templates

utterance(['Why', aren, '''', t, you | Y]) -->
	['I', am, not], end(Y).
utterance(['How', long, have, you, been | Y]) -->
	['I', am], end(Y).
utterance(['Why', do, you, like | Y]) -->
	['I', like], end(Y).
utterance(['Do', you, often, think, of | Y]) -->
	beginning(_), ['I', remember], end(Y).
utterance(['Please', tell, me, more, about, your, X, .]) -->
	beginning(_), [X], end(_), {important(X)}.
utterance(['Why', are, so, negative, '?']) -->
	[no].
utterance(['Tell', me, more, .]) -->
	[_].
utterance(['Please', go, on, .]) -->
	beginning(_).

% The Prolog clauses beginning/3 qnd end/3
% to link the pieces of the utterance

beginning(X, Y, Z) :- append(X, Z, Y).

end(X, Y, Z) :- append(X, Z, Y).

% The Freudian facts
important(father).
important(mother).
important(brother).
important(sister).

% write_answer/1 prints the content of the list containing
% Eliza's answer.

write_answer([Head | Tail]) :-
	write(Head), write(' '),
	write_answer(Tail).
write_answer([]) :- nl.


