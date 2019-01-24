# CMPT317
Repository for Introduction to Artificial Intelligence

### Assignment 2 - Calculating Machine
This assignment built a calculating machine - that is, it started with two
key inputs: a target integer and an array of integers. The goal was to use
the commands 'multiply', 'add', 'subtract', 'divide', and 'oo-operation (nop)'
to calculate the target using only the array of integers using several AI
hill-climbing algorithms.

a2q1 utilized Random Guessing, and took a random state each iteration. It 
remembered the best state from each of its iterations, and after an allotted
amount of time, terminated and returned its closest guess to the target.
This one was the most fun, but only because of how ridiculous I think
random guessing is.

a2q2 did Random Search. This would take in a randomized initial array, and 
then mutate one of the array values. If the mutation was better (closer to
the target), it became the new best guess.

a2q3 was an actual Hill-climbing Search. It acted similarly to Random Search,
except it took the *best* operator to mutate by.




### Assignement 4 - Minimax Search
This assignment revolved around a board game styled off the N-Queens program. 
The object of the game was to be the last player to put a piece (a queen) on 
the board, and therefore minimize the amount of queens the other player can 
play. The project uses a variety of Minimax algorithms, some with Alpha-Beta 
Pruning, some with Depth-Cutoff. There is also a large number of tests for 
the code present. Overall, it demonstrates a fine understanding of minimax 
and testing practices.

This program takes a multidimensional array as output, as seen in the test
code at the bottom.

I don't think the project works perfectly, though it was graded very well, but the 
general concepts of Minimax Search, Alpha-Beta Pruning, Depth-Cuttoff with Minimax, 
et. al. are there. As well, organization could be improved for this project, but I
preferred it this way to ease actually handing it in.


