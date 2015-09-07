% Author Pierre Nugues
% Converter of brackets in IOB2 tags

% convert_brackets_to_iob2(+Pairs) converts a bracketed chunk list
% into IOB2 annotated chunks
% +Label is the chunk type and +Tokens is a list of pairs (Word, POS)
convert_brackets_to_iob2([[Label, Tokens] | Rest]) :-
	write_group(Tokens, Label, 'B'),
	!,
	convert_brackets_to_iob2(Rest).
convert_brackets_to_iob2([(Word, Tag) | Rest]) :-
	write(Word), write(' '), write(Tag), write(' O'), nl, 
	!,
	convert_brackets_to_iob2(Rest).
convert_brackets_to_iob2([]) :-
	nl.

write_group([(Word, Tag) | Rest], Label, IB) :-
	write(Word), write(' '), write(Tag), write(' '), 
	write(IB), write('-'), write(Label), nl,
	!,
	write_group(Rest, Label, 'I').
write_group([], _, _).

% Start this to see a conversion example.
test_conversion_iob2 :-
	Sentence = [['NP', [('He', 'PRP')]], ['VP', [(reckons, 'VBZ')]], ['NP', [(the, 'DT'), (current, 'JJ'), (account, 'NN'), (deficit, 'NN')]], ['VP', [(will, 'MD'), (narrow, 'VB')]], ['PP', [(to, 'TO')]], ['NP', [(only,  'RB'), ('#', '#'), (1.8, 'CD'), (billion, 'CD')]], ['PP', [(in, 'IN')]], ['NP', [('September', 'NNP')]]],
	write('Bracketed groups:'), nl,
	write(Sentence), nl, nl,
	write('Tagged groups:'), nl,
	convert_brackets_to_iob2(Sentence).


