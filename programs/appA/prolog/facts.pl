character(priam, iliad). 
character(hecuba, iliad). 
character(achilles, iliad). 
character(agamemnon, iliad). 
character(patroclus, iliad). 
character(hector, iliad). 
character(andromache, iliad). 
character(rhesus, iliad). 
character(ulysses, iliad). 
character(menelaus, iliad). 
character(helen, iliad). 
 
character(ulysses, odyssey). 
character(penelope, odyssey). 
character(telemachus, odyssey). 
character(laertes, odyssey). 
character(nestor, odyssey). 
character(menelaus, odyssey). 
character(helen, odyssey). 
character(hermione, odyssey). 


% Male characters        
male(priam).              
male(achilles).           
male(agamemnon).         
male(patroclus).         
male(hector). 
male(rhesus). 
male(ulysses). 
male(menelaus). 
male(telemachus). 
male(laertes). 
male(nestor). 

% Female characters 
female(hecuba).
female(andromache).
female(helen). 
female(penelope). 


% Fathers                     
father(priam, hector).         
father(laertes,ulysses).       
father(atreus,menelaus).      
father(menelaus, hermione). 
father(ulysses, telemachus). 

% Mothers 
mother(hecuba, hector).
mother(penelope,telemachus).
mother(helen, hermione). 


king(ulysses, ithaca, achaean). 
king(menelaus, sparta, achaean). 
king(nestor, pylos, achaean). 
king(agamemnon, argos, achaean). 
king(priam, troy, trojan). 
king(rhesus, thrace, trojan). 

character(priam, iliad, king(troy, trojan)). 
character(ulysses, iliad, king(ithaca, achaean)). 
character(menelaus, iliad, king(sparta, achaean)). 


son(X, Y) :- father(Y, X), male(X). 
son(X, Y) :- mother(Y, X), male(X).

parent(X, Y) :- mother(X, Y). 
parent(X, Y) :- father(X, Y). 

ancestor(X, Y) :- parent(X, Y). 
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y). 

p(X) :- q(X), r(X). 

q(a).
q(b).

r(b).
r(c).

