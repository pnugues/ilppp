Apply automata to a string with OpenFst
Pierre Nugues

1. Install OpenFst from this site: http://openfst.org

2. Compile the two automata (Figs. 2.1 and 2.2) using these commands:
$ fstcompile --isymbols=symbols.txt --osymbols=symbols.txt --acceptor fsa1.fst fsa1.bin 
$ fstcompile --isymbols=symbols.txt --osymbols=symbols.txt --acceptor fsa2.fst fsa2.bin

3. Compile the chains:
$ fstcompile --isymbols=symbols.txt --osymbols=symbols.txt --acceptor input1.fst input1.bin
$ fstcompile --isymbols=symbols.txt --osymbols=symbols.txt --acceptor input2.fst input2.bin

4. Apply the automata to the strings using:
$ fstcompose input1.bin fsa1.bin | fstprint --acceptor --isymbols=symbols.txt
$ fstcompose input2.bin fsa1.bin | fstprint --acceptor --isymbols=symbols.txt

5. Generate random strings using:
$ fstrandgen fsa1.bin | fstprint --isymbols=symbols.txt --acceptor