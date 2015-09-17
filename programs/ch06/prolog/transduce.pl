/*
 * Author: Pierre Nugues
 */

% Run with transduce(1, F, [c,h,a,n,t,e,r,+|U], S), write(S).

%transduce(+Start, ?Final, ?Underlying, ?Surface).

% arc(Start, End, UnderlyingChar, SurfaceChar)
%  describes the automaton
arc(1, 1, C, C) :- letter(C).
arc(1, 2, e, 0).
arc(2, 3, r, 0).
arc(3, 4, +, 0).
arc(4, 5, e, e).
arc(5, 6, r, r).
arc(6, 7, a, a).
arc(7, 8, i, i).
arc(7, 9, s, s).
arc(6, 10, e, e).
arc(10, 11, z, z).
arc(6, 12, o, o).
arc(12, 13, n, n).
arc(13, 14, s, s).
arc(13, 15, t, t).


% final_state(S)
%  gives the stop condition
final_state(7).
final_state(8).
final_state(9).
final_state(11).
final_state(14).
final_state(15).


% letter(+L)
%  describes letters
letter(L) :-
	nonvar(L),
	char_type(L, alpha).

% transduce(+Start, ?Final, ?UnderlyingString, ?SurfaceString)
%  describes the transducer. The first and second rules include
%  mute transitions and enable to remove 0s

transduce(Start, Final, [U | UnderlyingString], SurfaceString) :-
	arc(Start, Next, U, 0),
	transduce(Next, Final, UnderlyingString, SurfaceString).
transduce(Start, Final, UnderlyingString, [S | SurfaceString]) :-
	arc(Start, Next, 0, S),
	transduce(Next, Final, UnderlyingString, SurfaceString).
transduce(Start, Final, [U | UnderlyingString], [S | SurfaceString]) :-
	arc(Start, Next, U, S),
	U \== 0,
	S \== 0,
	transduce(Next, Final, UnderlyingString, SurfaceString).
transduce(Final, Final, [], []) :-
	final_state(Final).

