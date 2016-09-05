Apply transducers to a verb with OpenFst
Pierre Nugues

1. Install OpenFst from this site: http://openfst.org

2. Compile the transducer (Fig. 6.8) using this command:
$ fstcompile --isymbols=symbols.txt --osymbols=symbols.txt first_group_future.fst first_group_future.bin

3. Compile the conjugated verb:
$ fstcompile --isymbols=symbols.txt --acceptor rêver+era.fst rêver+era.bin

4. Apply the transducer to the verb using:
$ fstcompose rêver+era.bin first_group_future.bin | fstprint --isymbols=symbols.txt --osymbols=symbols.txt

5. Project the output:
$ fstcompose rêver+era.bin first_group_future.bin | fstproject --project_output | fstprint --isymbols=symbols.txt --osymbols=symbols.txt

6. Remove the epsilons:
$ fstcompose rêver+era.bin first_group_future.bin | fstproject --project_output | fstrmepsilon | fstprint --isymbols=symbols.txt --osymbols=symbols.txt
