# Set Covering problem    

## Approach
The problem was tackled by re-adapting the given search algorithms and utils for performing a search among the possible solutions.
The class State was modified in order to keep both a list of lists and a set representing the set coverage of such state. The method covers() was used for indicating wether a given list is a subset of the covered set. In order to improve memory efficiency, after a solution state has been found, it won't be explored for further nodes. Another optimization is that a node won't be considered an available action if the next list is a subset of the already coverered set (this avoids repetition and lists that don't expand the covered set). The \_\_init\_\_() method stores the list of lists **sorted** such that another State with the same list of lists in different order is not considered nor stored in the frontier, improving the memory efficiency significantly. 

Removing the list duplicates before deploying the search algorithm is useful since, even though a state won't analyze a repeated list, different paths will eventually reach duplicate lists at least once.
***
## Breadth-First and Depth-First
Depth-First finds a solution first, as expected, but traversing all the possible paths (even with the optimizations) is an extremely expensive task. For N=10 and further, the algorithm doesn't end.

## A*
A first attempt was made by choosing h(.) as the number of total elements to a given state, giving priority to short-length lists. This is sub-optimal since shorter lists will require more nodes to be explored before reaching a full set covering.

A second idea consists in a heuristic function h(.) that gives priority directly considering the "bloat". For this purpose, a Counter object will used. Given a state, the function creates a Counter for it. Then, it will return the bloat. This approach yields good solutions but it is quite slow. Below are the results:

