

# General test - No solution if there are still unset cells
def domain_complete(domain, smart=False):
    for i in range(len(domain)):
        for j in range(len(domain[i])):
            if smart:
                if len(domain[i][j]) != 1:
                    return False
            else:
                if domain[i][j] == '.':
                    return False
    return True


# Rule 1 - No duplicate numbers in rows and columns for white cells
def test_duplicate_number(puzzle):
    identity = list(zip(*puzzle)) # Invert to get columns
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j] != 'B':
                if has_duplicates(puzzle[i], identity[j], puzzle[i][j]):
                    return False
    return True


# Check if a number is a duplicate within its row or column
def has_duplicates(row, col, value):
    if row.count(value) > 1 or col.count(value) > 1:
        return True
    return False


# Marks numbers that are unique (they occur once in their row or column)
# a number is uncertain, V must be white
def unique_white_cells(puzzle, smart=False):
    domain = [row[:] for row in puzzle]
    identity = list(zip(*domain)) # Invert domain to get columns
    for i in range(len(domain)):
        for j in range(len(domain[i])):
            if not has_duplicates(domain[i], identity[j], domain[i][j]):
                domain[i][j] = 'V'
    for i in range(len(domain)):
        for j in range(len(domain[i])):
            if domain[i][j] != 'V':
                if smart:
                    domain[i][j] = 'BW'
                else:
                    domain[i][j] = '.'
    return domain


# Rule 2 - No black cells are touching, diagonal is allowed, label black as 'B'
def test_adjacent_black(puzzle):
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j] == 'B' and not black_allowed(puzzle, i, j):
                return False
    return True


# Check if cell is allowed to be black, regardless of whether it is black or white
def black_allowed(puzzle, i, j):
    u, d, l, r = i-1, i+1, j-1, j+1 # Up, down, left, and right of position
    if u >= 0 and puzzle[u][j] == 'B':
        return False
    if d < len(puzzle) and puzzle[d][j] == 'B':
        return False
    if l >= 0 and puzzle[i][l] == 'B':
        return False
    if r < len(puzzle[i]) and puzzle[i][r] == 'B':
        return False
    return True


# Rule 3 - All white cells form one touching group
def test_white_connected(puzzle):
    if total_white_cells(puzzle) == touch(first_white(puzzle), [row[:] for row in puzzle], 1):
        return True
    return False


# Count all white cells irrespective of touching
def total_white_cells(puzzle):
    count = 0
    for i in puzzle:
        for j in i:
            if j != 'B':  
                count = count + 1
    return count


# Recursive touch method to check if all white cells are connected, sets checked locations 
# to 'C' and counts them during backtracking
def touch(start, puzzle, count):
    size = len(puzzle)
    if start is None:
        return 0 # No white cells, so don't search
    else:
        i, j = start
        u, d, l, r = i-1, i+1, j-1, j+1 # Up, down, left, and right of position
        puzzle[i][j] = 'C'
        if u >= 0 and puzzle[u][j] != 'B' and puzzle[u][j] != 'C':
                count = touch([u, j], puzzle, count) + 1
        if d < size and puzzle[d][j] != 'B' and puzzle[d][j] != 'C':
                count = touch([d, j], puzzle, count) + 1
        if l >= 0 and puzzle[i][l] != 'B' and puzzle[i][l] != 'C':
                count = touch([i, l], puzzle, count) + 1
        if r < size and puzzle[i][r] != 'B' and puzzle[i][r] != 'C':
                count = touch([i, r], puzzle, count) + 1 
        return count


# Location of first white cell to count from
def first_white(puzzle):
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j] != 'B':
                return [i, j]
    return None


# Forward checking - If a cell is turned black adjust the domains of adjacent cells
# by removing 'B' from the domain
def fc_black(domain, adjacent_cells):
    for x, y in adjacent_cells:
        domain[x][y] = domain[x][y].replace('B', '')
        if domain[x][y] == '':
            return None
    return domain


# Forward checking - If a cell is turned white adjust the domains of all the cells with
# a duplicate value in the row and colum by removing 'W'
def fc_white(puzzle, domain, i, j):
    size = len(puzzle)
    k = 1
    while i-k >= 0:
        if puzzle[i-k][j] == puzzle[i][j]: 
            domain[i-k][j] = domain[i-k][j].replace('W', '')
            if domain[i-k][j] == '':
                return None
        k += 1
    k = 1
    while i+k < size:
        if puzzle[i+k][j] == puzzle[i][j]: 
            domain[i+k][j] = domain[i+k][j].replace('W', '')
            if domain[i+k][j] == '':
                return None
        k += 1
    k = 1
    while j-k >= 0:
        if puzzle[i][j-k] == puzzle[i][j]: 
            domain[i][j-k] = domain[i][j-k].replace('W', '')
            if domain[i][j-k] == '':
                return None
        k += 1
    k = 1
    while j+k < size:
        if puzzle[i][j+k] == puzzle[i][j]: 
            domain[i][j+k] = domain[i][j+k].replace('W', '')
            if domain[i][j+k] == '':
                return None
        k += 1
    return domain


# Extra rules
def cell_surrounded(domain, i, j):
    u, d, l, r = i-1, i+1, j-1, j+1 # Up, down, left, and right of position

    # Check if coordinates are within array bounds
    adjacent_cells = []
    if u >= 0:
        adjacent_cells.append([u, j])
    if d < len(domain):
        adjacent_cells.append([d, j])
    if l >= 0:
        adjacent_cells.append([i, l])
    if r < len(domain[i]):
        adjacent_cells.append([i, r])

    count = 0
    for x, y in adjacent_cells:
        if domain[x][y] == 'B':
            count += 1

    if count == len(adjacent_cells)-1:
        for x, y in adjacent_cells:
            if domain[x][y] != 'B':
                domain[x][y] = domain[x][y].replace('B', '')
                domain[i][j] = domain[i][j].replace('B', '')
                if domain[x][y] == '' or domain[i][j] == '':
                    return None
    return domain