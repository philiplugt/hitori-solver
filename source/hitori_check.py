
from copy import deepcopy

# Rule 3 - All white cells form one touching group
def test_white_connected(puzzle):
    if total_white_cells(puzzle) == touch(first_white(puzzle), deepcopy(puzzle), 1):
        return True
    else:
        return False


# Count all white cells irrespective of touching
def total_white_cells(puzzle):
    count = 0
    for i in puzzle:
        for j in i:
            if j != 0:  
                count = count + 1
    return count


# Recursive touch method to check if all white cells are connected, sets checked locations 
# to -1 and counts them during backtracking
def touch(start, puzzle, tcount):
    size = len(puzzle)
    if start is None:
        return 0 # No white cells, so don't search
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


# Location of first white cell to count from
def first_white(puzzle):
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if puzzle[i][j] != 0:
                return [i, j]
    return None


# Rule 2 - No black cells are touching, diagonal is allowed, label black as 0
def test_adjacent_black(puzzle):
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if puzzle[i][j] == 0:
                if not valid_black(puzzle, i, j):
                    return False
    return True


# Check if cell is allowed to be black, regardless of whether it is black or white
def valid_black(puzzle, i, j):
    if i-1 >= 0:
        if puzzle[i-1][j] == 0:
            return False
    if i+1 < len(puzzle):
        if puzzle[i+1][j] == 0:
            return False
    if j-1 >= 0:
        if puzzle[i][j-1] == 0:
            return False
    if j+1 < len(puzzle):
        if puzzle[i][j+1] == 0:
            return False
    return True


# Rule 1 - No duplicate numbers in rows and columns for white cells
def test_duplicate_number(puzzle):
    size = len(puzzle)
    pcol = list(zip(*puzzle)) # Invert puzzle to get columns
    for i in range(size):
        for j in range(size):
            if puzzle[i][j] != 0:
                if is_duplicate(puzzle, pcol, i, j):
                   return False
    return True 


# Marks numbers that are unique (they occur once in their row or column)
# 0 is uncertain, 1 must be white
def unique_values(puzzle):
    size = len(puzzle)
    pcol = list(zip(*puzzle)) # Invert puzzle to get columns
    binaryboard = [[0 for i in puzzle] for j in puzzle]
    for i in range(size):
        for j in range(size):
            if puzzle[i][j] != 0:
                if not is_duplicate(puzzle, pcol, i, j):
                    binaryboard[i][j] = 1;
    return binaryboard


# Check if a number is a duplicate within its row or column
def is_duplicate(puzzle, pcol, i, j):
    if puzzle[i].count(puzzle[i][j]) > 1 or pcol[j].count(puzzle[i][j]) > 1:
        return True
    return False


# Forward checking - If a cell is turned black adjust the domains of adjacent cells
# by removing 'B' from the domain
def fc_black(domain, i, j):
    size = len(domain)
    if i-1 >= 0:
        domain[i-1][j] = domain[i-1][j].replace('B', '')
    if i+1 < size:
        domain[i+1][j] = domain[i+1][j].replace('B', '')
    if j-1 >= 0:
        domain[i][j-1] = domain[i][j-1].replace('B', '')
    if j+1 < size:
        domain[i][j+1] = domain[i][j+1].replace('B', '')
    return domain


# Forward checking - If a cell is turned white adjust the domains of all the cells with
# a duplicate value in the row and colum by removing 'W'
def fc_white(puzzle, domain, i, j):
    size = len(domain)
    k = 1
    while i-k >= 0:
        if puzzle[i-k][j] == puzzle[i][j]: 
            domain[i-k][j] = domain[i-k][j].replace('W', '')
        k += 1
    k = 1
    while i+k < size:
        if puzzle[i+k][j] == puzzle[i][j]: 
            domain[i+k][j] = domain[i+k][j].replace('W', '')
        k += 1
    k = 1
    while j-k >= 0:
        if puzzle[i][j-k] == puzzle[i][j]: 
            domain[i][j-k] = domain[i][j-k].replace('W', '')
        k += 1
    k = 1
    while j+k < size:
        if puzzle[i][j+k] == puzzle[i][j]: 
            domain[i][j+k] = domain[i][j+k].replace('W', '')
        k += 1
    return domain


if __name__ == '__main__':
    # Do nothing for now
    pass

    
