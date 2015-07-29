% The start state
start(q0).

% The final states
final(q2).

transition(q0, a, q1).
transition(q1, b, q1).
transition(q1, c, q2).

accept(Symbols) :-
	start(StartState),
	accept(Symbols, StartState).

accept([], State) :-
	final(State).
accept([Symbol | Symbols], State) :-
	transition(State, Symbol, NextState),
	accept(Symbols, NextState).
