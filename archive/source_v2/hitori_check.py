"""
Author: Philip van der Lugt
Date: m1.d5.y13
Class: Artificial Intelligence

Brute force and intelligent solver for Hitori puzzles.
"""

from copy import deepcopy

# Checks if game is solved (valid state if solved)
# No adjacent black is not used here, because it is already checked in 
# generate state
def check_for_validity(puzzle):
    if no_duplicate_number(puzzle): # and no_adjacent_black(puzzle) and all_white_connected(puzzle) 
        return True # True - then state is valid
    else:
        return False # False - then state is not valid

#####################################################################
# Rule 1 - All non-black values are connected                       #
# Check using 2 methods of counting white values,                   #
# if the numbers match then it all white values are connected       #
#####################################################################
def all_white_connected(puzzle):
    if number_of_white(puzzle) == touch(first_white(puzzle), deepcopy(puzzle), 1):
        return True
    else:
        return False 

# Returns the total number of white cells regardless of whether isolated or not
def number_of_white(puzzle):
    count = len(puzzle) * len(puzzle) # Total possible positions
    for i in range(len(puzzle)):
    	# Whites can have any value except 0, so count 
    	# all 0's and subtract from total possible positions
        count = count - puzzle[i].count(0) 
    return count

# Returns the location of the first white cell, this is used as a starting
# point for searches
def first_white(puzzle):
    ps = range(len(puzzle)) # Puzzle size range
    for i in ps:
        for j in ps:
            if puzzle[i][j] != 0:
                return [i, j]
    return [-1,-1] # No white cells 

# Recursive touch method to check if all whites are connected, sets checked locations to -1
# and counts them during backtracking
def touch(start, puzzle, tcount):
    size = len(puzzle)
    if start[0] == -1 and start[1] == -1:
        return 0 # No white cells so don't search
    else:
        puzzle[start[0]][start[1]] = -1
        if start[0]+1 < size:
            if puzzle[start[0]+1][start[1]] != 0 and puzzle[start[0]+1][start[1]] != -1:
                tcount = touch([start[0]+1, start[1]], puzzle, tcount) + 1
        if start[0]-1 >= 0:
            if puzzle[start[0]-1][start[1]] != 0 and puzzle[start[0]-1][start[1]] != -1:
                tcount = touch([start[0]-1, start[1]], puzzle, tcount) + 1
        if start[1]+1 < size:
            if puzzle[start[0]][start[1]+1] != 0 and puzzle[start[0]][start[1]+1] != -1:
                tcount = touch([start[0], start[1]+1], puzzle, tcount) + 1
        if start[1]-1 >= 0:
            if puzzle[start[0]][start[1]-1] != 0 and puzzle[start[0]][start[1]-1] != -1:
                tcount = touch([start[0], start[1]-1], puzzle, tcount) + 1
        return tcount

#####################################################################
# Rule 2 - No black cells are connecting                            #
# Test rows and columns, so that no black values are adjacent       #
# 0 used to represent black values, diagonal connection is allowed  #
#####################################################################
def no_adjacent_black_test(puzzle): # Rule 2
    ps = range(len(puzzle)) # Puzzle size range
    for i in ps:
        for j in ps:
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

# Same as method above but more efficient for single locations
def no_adjacent_black(puzzle, i, j): # Only for individual squares
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


#####################################################################
#                                                                   #
# Rule 3 - No duplicate numbers in rows or columns for white cells  #
#                                                                   #
#####################################################################
def no_duplicate_number(puzzle):
    zipped = list(zip(*puzzle)) # Generate columns
    ps = range(len(puzzle)) # Puzzle size range
    # Test rows and columns
    for i in ps:
        for j in ps:
            if puzzle[i][j] != 0 and zipped[j][i] != 0:
                if puzzle[i].count(puzzle[i][j]) > 1: 
                    return False
                if zipped[j].count(zipped[j][i]) > 1:
                    return False             
    return True

# Marks values that have no duplicates in rows or columns
def some_duplicates(puzzle):
    zipped = list(zip(*puzzle)) # Generate columns
    ps = range(len(puzzle)) # Puzzle size range
    binaryboard = [[0 for i in ps] for j in ps]
    
    # Test rows and columns
    for i in ps:
        for j in ps:
            if puzzle[i][j] != 0 and zipped[j][i] != 0:
                if puzzle[i].count(puzzle[i][j]) == 1 and zipped[j].count(zipped[j][i]) == 1:
                    binaryboard[i][j] = 1
    return binaryboard

# Check number if it has a duplicate to be marked black immediately
def has_duplicate(puzzle, i, j):
    zipped = list(zip(*puzzle)) # Generate columns
    ps = range(len(puzzle)) # Puzzle size range
    
    # Test rows and columns
    if puzzle[i].count(puzzle[i][j]) > 1 and zipped[j].count(zipped[j][i]) > 1:
        return True
    return False

if __name__ == '__main__':
    print("Nothing to test")