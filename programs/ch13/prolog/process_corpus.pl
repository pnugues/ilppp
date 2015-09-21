% Utilities to preprocess a CoNLL file before it is parsed
% Author: Pierre Nugues

% To load a corpus and extract the action list
% 1. Load the corpus file with the corpus/1 predicate
% 2. Call corpus(Corpus), parse_gold_corpus(Corpus).
% To extract features and write them in File, use instead:
% corpus(Corpus), parse_gold_corpus_feat(Corpus, File)
% The Corpus fact is created from a CoNLL formatted file using 
% conll_reader.pl

:- ['../../ch11/prolog/nonprojective_links'].
:- ['nivre_ref'].

% Gold standard parsing of a hand-annotated corpus
% Prints the transition sequences
parse_gold_corpus(Corpus) :-
	parse_gold_corpus(Corpus, 0).

parse_gold_corpus([], _).
parse_gold_corpus([X | L], N) :-
	N1 is N + 1,
	write(N), write(': '),
	parse_gold(X, A),
	extract_nonproj(X, NP),
%	write(X), nl,
	write('Nonprojective links: '), write(NP), nl,
	write('Parsing operations: '), write(A), nl,
	!,
	parse_gold_corpus(L, N1).

% Gold standard parsing of a hand-annotated corpus
parse_gold_corpus_feat(Corpus, File) :-
	open(File, write, Stream, [encoding(utf8)]),
	parse_gold_corpus_feat(Corpus, 0, Stream),
	close(Stream).

parse_gold_corpus_feat([], _, _).
parse_gold_corpus_feat([X | L], N, Stream) :-
	N1 is N + 1,
	write(N), write(': '),
	parse_gold_feat(X, A, F),
	extract_nonproj(X, NP),
%	write(X), nl,
	write('Nonprojective links: '), write(NP), nl,
	write('Parsing operations: '), write(A), nl,
	write_features(NP, F, Stream),
	!,
	parse_gold_corpus_feat(L, N1, Stream).

% parse_gold(+X, -A) extracts actions from a gold-standard graph
% Then checks that applying the actions produces the same graph.
parse_gold(X, A) :-
	make_word(X, W),
	make_graph(X, G),
	nivre_parser([w([id=0, form=root, postag='ROOT']) | W], A, G),
	nivre_parser([w([id=0, form=root, postag='ROOT']) | W], A, GP),
	(   
	  subset(GP, G),
	  subset(G, GP)
	;
	  write('Different graphs'), nl
	).

% extract_feats(+X, -Actions, -Features) extracts transitions and 
% features from a gold-standard graph
% Then checks that applying the actions produces the same graph.
parse_gold_feat(X, A, F) :-
	make_word(X, W),
	make_graph(X, G),
	nivre_parser([w([id=0, form=root, postag='ROOT']) | W], A, F, G).
	
% extract_nonproj(+X, -NP)  extracts nonprojective links from a 
% gold-standard graph
extract_nonproj(X, NP) :-
	make_graph(X, G),
	nonproj_links(G, NP).

% make_graph(+G, -SG) extracts a subset of the graph. It sets aside
% a couple of columns from the CoNLL format.
make_graph([], []).
make_graph([w(X) | L], [w([id=ID, form=FORM, postag=POSTAG, head=HEAD, deprel=DEPREL]) | WL]) :-
	member(id=ID, X),
	member(form=FORM, X),
	member(postag=POSTAG, X),
	member(head=HEAD, X),
	member(deprel=DEPREL, X),
	make_graph(L, WL).

% Formats the words as a subset of the CoNLL 2006 format
% make_word(+W, -FormattedWord)
make_word([], []).
make_word([w(X) | L], [w([id=ID, form=FORM, postag=POSTAG]) | WL]) :-
	member(id=ID, X),
	member(form=FORM, X),
	member(postag=POSTAG, X),
	make_word(L, WL).

equal_pos([]).
equal_pos([w(X) | L]) :-
	member(cpostag=C, X),
	member(postag=C, X),
	!,
	equal_pos(L).
equal_pos([w(X) | L]) :-
	write(X), nl,
	equal_pos(L).
	  
% Write the features extracted from gold-standard parsing
% When the graph is projective
% write_features(+NonprojectiveLinks, +Features, +Stream)
write_features(NP, _, _) :-
	NP \= [].
write_features([], [], _).
write_features([], [[T, S0, S1, W0, W1, W2, LA, RA, RE, LMS] | Feats], Stream) :-
	write(Stream, S0),
	write(Stream, '\t'),
	write(Stream, S1),
	write(Stream, '\t'),
	write(Stream, W0),
	write(Stream, '\t'),
	write(Stream, W1),
	write(Stream, '\t'),
	write(Stream, W2),
	write(Stream, '\t'),
	write(Stream, LA),
	write(Stream, '\t'),
	write(Stream, RA),
	write(Stream, '\t'),
	write(Stream, RE),
	write(Stream, '\t'),
	write(Stream, LMS),
	write(Stream, '\t'),
	write(Stream, T),
	write(Stream, '\n'),
	write_features([], Feats, Stream).

