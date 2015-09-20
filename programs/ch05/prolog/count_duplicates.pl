% Author: Pierre Nugues
% count_duplicates(+OrderedList, -CountedList) counts items of
% an ordered list. The result is a list of [N, Item] elements
count_duplicates(OrderedList, CountedList) :- 
	count_duplicates(OrderedList, 1, [], CountedListRev), 
	reverse(CountedListRev, CountedList). 
 
count_duplicates([X, X | Ordered], N, Counting, Counted) :- 
	N1 is N + 1, 
	!, 
	count_duplicates([X | Ordered], N1, Counting, Counted). 
count_duplicates([X | Ordered], N, Counting, Counted) :- 
	!, 
	count_duplicates(Ordered, 1, [[N, X] | Counting], Counted). 
count_duplicates([], _, L, L). 
