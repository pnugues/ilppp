% Author: Pierre Nugues
% Reading and converting the CONLL 2006 and 2007 files into a Prolog fact
% corpus([[w(id=1, form=...), w(id=2, ], ..., [...]].


convert_file(FileIn, FileOut) :-
	open(FileIn, read, StreamIn, [encoding(utf8)]),
	open(FileOut, write, StreamOut, [encoding(utf8)]),
%	set_stream(StreamOut, representation_errors(xml)),
	write(StreamOut, ':- encoding(utf8).\n'),
	write(StreamOut, 'corpus(['),
	read_sentences(StreamIn, StreamOut),
	write(StreamOut, ']).\n'),
	close(StreamIn),
	close(StreamOut),
	!.

read_sentences(StreamIn, StreamOut) :-
	\+ at_end_of_stream(StreamIn),
	read_sentence(StreamIn, StreamOut, S),
	writeq(StreamOut, S), 
	(  
	  at_end_of_stream(StreamIn)
	;
	  write(StreamOut, ', ')
	),
	!,
	read_sentences(StreamIn, StreamOut).
read_sentences(_, _).

read_sentence(StreamIn, StreamOut, [ParsedLine | L]) :-
	  get_char(StreamIn, Cur),
	  Cur \== '\n',	
	  read_line(StreamIn, Cur, S),
	  line(ParsedLine, S, []),
	  !,
	  read_sentence(StreamIn, StreamOut, L).
read_sentence(_, _, []).

read_line(StreamIn, Prev, [Prev | L]) :-
	  Prev \== '\n',	
	  get_char(StreamIn, Cur),
	  !,
	  read_line(StreamIn, Cur, L).
read_line(_, _, []).



/*
line(w(ID, FORM, LEMMA, CPOSTAG, POSTAG, FEATS, HEAD, DEPREL, PHEAD, PDEPREL)) -->
*/
line(w([id=ID, form=FORM, lemma=LEMMA, cpostag=CPOSTAG, postag=POSTAG, feats=FEATS, head=HEAD, deprel=DEPREL, phead=PHEAD, pdeprel=PDEPREL])) -->
	id(ID),
	['\t'],
	form(FORM),
	['\t'],
	lemma(LEMMA),
	['\t'],
	cpostag(CPOSTAG),
	['\t'],
	postag(POSTAG),
	['\t'],
	feats(FEATS),
	['\t'],
	head(HEAD),
	['\t'],
	deprel(DEPREL),
	['\t'],
	phead(PHEAD),
	['\t'],
	pdeprel(PDEPREL).

id(W) --> alphanum(L), {number_chars(W, L), !}.
form(W) --> alphanum(L), {atom_chars(W, L), !}.
lemma(W) --> alphanum(L), {atom_chars(W, L), !}.
cpostag(W) --> alphanum(L), {atom_chars(W, L), !}.
postag(W) --> alphanum(L), {atom_chars(W, L), !}.
feats(W) --> alphanum(L), {atom_chars(W, L), !}.
head(W) --> alphanum(L), {number_chars(W, L), !}.
deprel(W) --> alphanum(L), {atom_chars(W, L), !}.
phead('_') --> alphanum(['_']), {!}.
phead(W) --> alphanum(L), {number_chars(W, L), !}.
pdeprel(W) --> alphanum(L), {atom_chars(W, L), !}.

alphanum([C | R]) -->
	[C],
	{C \== '\n', C \== '\t'},
	alphanum(R).
alphanum([]) --> [].
