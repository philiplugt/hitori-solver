"""
Author: Philip van der Lugt
Date: m1.d5.y13
Class: Artificial Intelligence

Brute force and intelligent (forward checking/minimum remaining values) solver for Hitori puzzles.
"""

# Standard
from __future__ import division
from collections import deque
from copy import deepcopy
from time import perf_counter

# Own
from hitori_check import no_duplicate_number
from hitori_check import no_adjacent_black
from hitori_check import no_adjacent_black_test
from hitori_check import all_white_connected
from hitori_check import some_duplicates
from hitori_check import has_duplicate

"""
Hitori is a Japanese puzzle game, which consists of a 
n-by-n grid of numbers with numbers ranging from 1-n.

The game has three conditions that must be met in order
to win
1. White values (non-black values) not be isolated (all connected)
2. Black values (0 used for us) cannont be adjacent (vertically and horizontally) to each other
3. There must be no duplicate numbers in the rows or columns
"""

# Main method, set up the puzzles
# Any test scripts should run solve_hitori function
def main():
    # Bruteforce method on
    bruteforce = True   
    
    # Sample puzzles
    puzzle1 = [2, 1], [1, 1] # Simple case, solved if last 1 set to 0
    puzzle2 = [1, 2, 3], [1, 1, 3], [2, 3, 3] # Solvable
    puzzle3 = [1, 2, 3], [2, 2, 3], [1, 1, 3] # Unsolvable
    puzzle4 = [3, 3, 1, 2], [4, 3, 2, 3], [3, 4, 1, 1], [1, 2, 3, 4]
    puzzle5X = [5, 5, 3, 3, 4], [1, 4, 3, 2, 5], [4, 5, 5, 4, 3], [3, 1, 5, 5, 4], [5, 4, 1, 4, 5]
    puzzle5Y = [0, 5, 0, 3, 4], [1, 4, 3, 2, 5], [4, 5, 5, 4, 3], [3, 1, 5, 5, 4], [5, 4, 1, 4, 5]
    puzzle6  = [5, 5, 4, 4, 2], [5, 1, 3, 4, 1], [2, 3, 3, 1, 1], [3, 4, 1, 2, 5], [1, 1, 4, 5, 5]
    puzzle7 = [3, 2, 5, 4, 5], [2, 3, 4, 3, 5], [4, 3, 2, 4, 4], [1, 3, 3, 5, 5], [5, 4, 1, 2, 3]

    # Change name to insert puzzle
    solve_hitori(puzzle7, bruteforce)

# Main solver function to select which method to use
def solve_hitori(puzzle, boo):
    if boo:
        hitori_method_bf(puzzle)
    else:
        hitori_method_ai(puzzle)

# Brute force solver
def hitori_method_bf(puzzle):
    # Start clock plus opening comments
    tstart = perf_counter()
    print("HITORI SOLVER - Bruteforce")
    print("")
    print("Puzzle to solve: ")
    display(puzzle)
    print("")
    print("Solving...")
    print("")
    
    # Create puzzle for comparison and check if initial configuration is a solution 
    next_state = deepcopy(puzzle)
    the_queue = deque()
    the_queue.append(next_state)
    visited_q = deque()

    # Create board with as many known answers as possible
    blackboard = some_duplicates(next_state)
    display(blackboard)

    # Counter for puzzles searched
    iter = 1;
    checked = 1;
    solution_found = False

    # Breadth first search of the puzzle
    while len(the_queue) != 0:
        # print len(the_queue)
        next_state = the_queue.popleft()
        blackboard = some_duplicates(next_state)
        if no_duplicate_number(next_state):
            solution_found = True
            break
        # Generates the next step state, one step is marking a 
        # value as invalid (black), so in this case setting it 
        # to 0, then generates a queue with all the possible next step states
        ps = range(len(next_state))
        for i in ps:
            for j in ps:
                if (next_state[i][j] != 0) and blackboard[i][j] != 1: 
                    # Check predetermined correct values
                    newobj = deepcopy(next_state)
                    newobj[i][j] = 0
                    if no_adjacent_black(newobj, i, j) and all_white_connected(newobj): 
                        # Remove obviously bad states
                        iter = iter + 1
                        the_queue.append(newobj)
                        # print str(iter)
    
    if solution_found:
        print("Solution found! It took " + str(iter) + " iteration(s):")
        display(next_state)
    else:
        print("No solution found after " + str(iter) + " iteration(s)")

    # Clock time plus closing comments
    tend = perf_counter()
    print("")
    print("Elapsed time: " + str(tend - tstart) + " seconds")
    print("")

# AI solver
def solve_hitori_ai(puzzle):
    # Start clock plus opening comments
    tstart = perf_counter()
    print("HITORI SOLVER - Forward Checking")
    print("")
    print("Puzzle to solve: ")
    display(puzzle)
    print("")
    print("Solving...")
    print("")

    # ENTER SOLVER HERE

    # Clock time plus closing comments
    tend = perf_counter()
    print("")
    print("Elapsed time: " + str(tend - tstart) + " seconds")
    print("")

# Print out the puzzle board
def display(x):
    for i in x:
        print(i)

if __name__ == '__main__':
    main()