% Author Pierre Nugues
% Chunking program (imcomplete)

:- [conll_io].
:- [brackets_to_iob2].
:- [ng].

% tag_complete_file(+InputFile, +OutputFile)
% tags the complete input file and writes it in the output file
tag_complete_file(Input, Output) :-
	see(Input),
	open(Output, write, OutStream),
	current_output(StdOut),
	process_all_sentences(OutStream, StdOut),
	seen,
	close(OutStream).

% process_all_sentences/2 applies the group_detector to
% all the sentences and converts the brackets annotation into the
% IOB2 style
process_all_sentences(OutStream, StdOut) :-
	next_sentence_conll(wordpos, Tokens), % Tokens are pairs (Word, POS)
	Tokens \= [],
	group_detector(Tokens, TaggedTokens),
	set_output(OutStream),
	convert_brackets_to_iob2(TaggedTokens),
	set_output(StdOut),
	%write(TaggedTokens), nl,
	!,
	process_all_sentences(OutStream, StdOut).
process_all_sentences(_, _).

% The group detector that is in the book
group_detector(In, Out) :-
	word_stream_group(Beginning, Group, End, In, []),
	group_detector(End, Rest),
	append(Beginning, [Group], Head),
	append(Head, Rest, Out).
group_detector(End, End).

word_stream_group(Beginning, Group, End) -->
	beginning(Beginning),
	group(Group),
	end(End).

beginning(X, Y, Z) :- append(X, Z, Y).

end(X, Y, Z) :- append(X, Z, Y).

group(['NP', Group]) --> noun_group(Group).
