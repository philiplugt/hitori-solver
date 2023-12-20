"""
Author: Philip van der Lugt
Date: m1.d5.y13
Class: Artificial Intelligence

Brute force and intelligent solver for Hitori puzzles.

2020-04-12 Update:
Run with Python 2.7

This was a project an AI class I took. I failed it, I think.

So, this is the original hitori brute force checker, I never implemented the smart 
alas. But, the brute force solution is still pretty terrible time-wise. Main reason
is that the brute force solution does not check for obvious incorrect states early. Which
causes needlessly main iterations to be wasted on already incorrect answers.

In retrospect I shouldn't be so hard on myself. This project was technically my
first python program... I literally had to learn python on the fly.

"""

from collections import deque
import copy
from time import time

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
def main():
    print "~ Hitori Solver"
    print ""
    
    # Bruteforce method on
    bruteforce = True   
    
    # Sample puzzles
    puzzle1 = [2, 1], [1, 1] # Simple case, solved if last 1 set to 0
    puzzle2 = [1, 2, 3], [1, 1, 3], [2, 3, 3] # Solvable
    puzzle2a = [1, 2, 0], [0, 1, 3], [2, 3, 0] # Solvable
    puzzle3 = [1, 2, 3], [2, 2, 3], [1, 1, 3] # Unsolvable
    
    # Added 2021-04-12
    #puzzle4 = [3, 3, 1, 2], [4, 3, 2, 3], [3, 4, 1, 1], [1, 2, 3, 4]
    #puzzle5 = [5, 5, 3, 3, 4], [1, 4, 3, 2, 5], [4, 5, 5, 4, 3], [3, 1, 5, 5, 4], [5, 4, 1, 4, 5]
    #puzzle7 = [3, 2, 5, 4, 5], [2, 3, 4, 3, 5], [4, 3, 2, 4, 4], [1, 3, 3, 5, 5], [5, 4, 1, 2, 3]
    
    # Change name to insert puzzle
    print "Puzzle to solve:"
    display(puzzle5)
    tstart = time()
    solve_hitori(puzzle5, bruteforce)
    tend = time()
    print("")
    print("Elapsed time: " + str(tend - tstart) + " seconds")
    print("")

# Print out the puzzle board
def display(x):
    for i in x:
        print(i)
    print ""

# Main solver function to select which method to use
def solve_hitori(puzzle, b):
    if (bool(b)):
        hitori_method_bf(puzzle)
    else:
        hitori_method_ai(puzzle)

# Brute force solver
def hitori_method_bf(puzzle):
    print "~ Bruteforce Solution"
    print ""
    print "Iteration(s):"
   
    #print check_for_validity(puzzle)
    
   	# Create puzzle for comparison and check if initial configuration is a solution 
    endpuzzle = copy.deepcopy(puzzle)
    init_q = deque()
    init_q.append(puzzle)

    iter = 1; # Counter for puzzles searched
    no_solution = False

    # Create queues filled with puzzle lists
    while check_for_validity(endpuzzle) == False:
	    next_q = bf_next(init_q)
	    if len(next_q) == 0: # No solution if there is no next_q (all spaces filled with 0's)
                             # WARNING: THESE PUZZLES ARE EXTREMELY SLOW TO COMPUTE
	    	no_solution = True;
	    	break
	    iter = iter + len(next_q)
	    for i in range(len(next_q)):
	        if check_for_validity(next_q[i]):
	            endpuzzle = copy.deepcopy(next_q[i])
	    init_q.clear()
	    init_q = copy.deepcopy(next_q)    
    
    if not no_solution:
        print "Solution found after " + str(iter) + " iteration(s):"
        display(endpuzzle)
    else:
    	print "No solution found!"

# Based on the previous puzzle creates a new queue of puzzles for the next iteration
def bf_next(init_q):
    some_q = deque()
    for i in range(len(init_q)):
	    gs = generate_state(init_q.pop())
	    for i in range(len(gs)):
	        some_q.append(gs[i])
    #display(some_q)
    return some_q
	

# Checks board if game is solved    
def check_for_validity(puzzle):
    #print all_white_connected(puzzle)
    #print no_adjacent_black(puzzle)
    #print no_duplicate_number(puzzle)
    if all_white_connected(puzzle) and no_adjacent_black(puzzle) and no_duplicate_number(puzzle):
        return True
    else:
        return False

# All white values are connected with the 2 methods of counting the number of white values match
def all_white_connected(puzzle):
    #print touch(first_white(puzzle), puzzle)
    if number_of_white(puzzle) == number_of_neg(touch(first_white(puzzle), copy.deepcopy(puzzle))):
        return True
    else:
        return False 

# Returns number of white cells to check if there are isolated cases
def number_of_white(puzzle):
    count = len(puzzle) * len(puzzle) # Total possible white
    for i in range(len(puzzle)):
        count = count - puzzle[i].count(0)
    return count    

# Counts the number of negative locations
def number_of_neg(puzzle):
    count = 0
    for i in range(len(puzzle)):
        count = count + puzzle[i].count(-1)
    return count

# Recursive touch method to check if all whites are connected, sets checked locations to -1
def touch(start, puzzle):
    puzzle[start[0]][start[1]] = -1
    if start[0]+1 < len(puzzle):
        if puzzle[start[0]+1][start[1]] != 0 and puzzle[start[0]+1][start[1]] != -1:
            touch([start[0]+1, start[1]], puzzle)
    if start[0]-1 >= 0:
        if puzzle[start[0]-1][start[1]] != 0 and puzzle[start[0]-1][start[1]] != -1:
            touch([start[0]-1, start[1]], puzzle)
    if start[1]+1 < len(puzzle):
        if puzzle[start[0]][start[1]+1] != 0 and puzzle[start[0]][start[1]+1] != -1:
            touch([start[0], start[1]+1], puzzle)
    if start[1]-1 >= 0:
        if puzzle[start[0]][start[1]-1] != 0 and puzzle[start[0]][start[1]-1] != -1:
            touch([start[0], start[1]-1], puzzle)
    return puzzle

# Returns the location of the first white cell, this is used as a starting
# point for searches
def first_white(puzzle):
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if puzzle[i][j] != 0:
                return [i, j]
    return [-1,-1] # No white cells

 # Test rows and columns, so that no black values
 # are adjacent (0 represent black values)
def no_adjacent_black(puzzle): # Rule 2
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if puzzle[i][j] == 0:
                if i+1 < len(puzzle):
                    if (puzzle[(i+1)][j] == 0):
                        return False
                if i-1 >= 0:
                    if (puzzle[(i-1)][j] == 0):
                        return False
                if j+1 < len(puzzle):
                    if (puzzle[i][(j+1)] == 0):
                        return False
                if j-1 >= 0:
                    if (puzzle[i][(j-1)] == 0):
                        return False  
    return True
    

# Checks for duplicate numbers in rows and columns
def no_duplicate_number(puzzle):
    ndn = True
    zipped = zip(*puzzle) # Generate columns
    
    # Test rows and columns
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if puzzle[i][j] != 0:
                if puzzle[i].count(puzzle[i][j]) > 1:
                    ndn = False
    for i in range(len(zipped)):
        for j in range(len(zipped)):
            if zipped[i][j] != 0:
                if zipped[i].count(zipped[i][j]) > 1:
                    ndn = False                
    return ndn
    

# Generates the next step state, one step is marking a value as invalid
# So in this case setting it to 0, then generates a queue with all the possible next step states
def generate_state(puzzle):
    d = deque()
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            newobj = copy.deepcopy(puzzle)
            newobj[i][j] = 0
            if (puzzle[i][j] != 0):
                d.append(newobj)
    return d


# AI solver
def solve_hitori_ai(puzzle):
    print "Intelligent Solution"

if __name__ == '__main__':
    main()