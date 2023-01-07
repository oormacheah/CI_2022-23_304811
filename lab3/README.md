# Lab 3 - Policy Search for Nim game

This laboratory consists of implementing 4 different agents for playing the Nim game.
* Task3.1: An agent using fixed rules
* Task3.2: An agent using evolved rules
* Task3.3: An agent using minmax
* Task3.4: An agent using reinforcement learning

## Approaches

### Task 3.1
My personal approach. This strategy is by no means attempting to compete with nim-sum. As a matter of fact, it is unable to beat it. It works as follows. 
* The ply will be done on the shortest active row.
* Consider the number of active rows. 
  * It this number is odd, the ply will be to either take all the remaining elements of the or, if there is a K that doesn't allow to remove all, take just K (the maximum) elements of this row. 
  * If the number of active rows is even, the same logic holds, but the attempt will be to leave 1 element in the row, instead of 0. If the K again doesn't allow this, just take K elements.

This strategy performs better than "gabriele" and "pure_random".

### Task 3.2
