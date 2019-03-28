# CMPT317
Repository for Introduction to Artificial Intelligence

### Assignment 2 - Calculating Machine
This assignment built a calculating machine - that is, it started with two key inputs: a target integer and an array of integers. The goal was to use the commands 'multiply', 'add', 'subtract', 'divide', and 'oo-operation (nop)' to calculate the target using only the array of integers using several AI hill-climbing algorithms. I am quite happy with this project, and scored very well.

a2q1 (Assignment_2-1) utilized Random Guessing, and took a random state each iteration. It remembered the best state from each of its iterations, and after an allotted amount of time, terminated and returned its closest guess to the target. This one was the most fun, but only because of how ridiculous I think random guessing is.

a2q2 did Random Search. This would take in a randomized initial array, and  then mutate one of the array values. If the mutation was better (closer to the target), it became the new best guess.

a2q3 was an actual Hill-climbing Search. It acted similarly to Random Search, except it took the *best* operator to mutate by.

q4 did Random-Restart Hill-climbing search, and q5 used Stochastic Hill-climbing search.

### Assignment 3 - The Constraint Satisfaction Problem (CSPs)
For this assignment, I implemented the Constraint Satisfaction Program augmented with Forward Checking. As input, this program takes examples_size3.txt and examples_size5.txt, both provided. These text files contain unfinished Latin Squares, which are solved by the program. It is kind of slow, entirely the fault of the depth-first search. A lot of deepcopies occur, though this is an easily solvable problem. For example, I could substitute a fair portion of the program with numPy's.

### Assignement 4 - Minimax Search
This assignment revolved around a board game styled off the N-Queens program. The object of the game was to be the last player to put a piece (a queen) on the board, and therefore minimize the amount of queens the other player can play. The project uses a variety of Minimax algorithms, some with Alpha-Beta Pruning, some with Depth-Cutoff. There is also a large number of tests for the code present. Overall, it demonstrates a fine understanding of minimax and testing practices.

This program takes a multidimensional array as output, as seen in the test code at the bottom.

I don't think the project works perfectly, though it was graded very well, but the general concepts of Minimax Search, Alpha-Beta Pruning, Depth-Cuttoff with Minimax, et. al. are there. As well, organization could be improved for this project, but I preferred it this way to ease actually handing it in.


