
def load_puzzle(puzzle):
    for row in puzzle:
        assert len(row) == len(puzzle[0]), 'Usage: Puzzle should be size N x M'

    domain = [['BW' for cell in row] for row in puzzle]
    edges = []
    for i in range(len(puzzle)):
        edges_row = []
        for j in range(len(puzzle[i])):
            edges_cell = []
            u, d, l, r = i-1, i+1, j-1, j+1
            if u >= 0:
                edges_cell.append([u, j])
            if d < len(puzzle):
                edges_cell.append([d, j])
            if l >= 0:
                edges_cell.append([i, l])
            if r < len(puzzle[i]):
                edges_cell.append([i, r])
            edges_row.append(edges_cell)
        edges.append(edges_row)
    state =  {
        'puzzle': puzzle, 
        'domain': unique_white_cells(puzzle, domain),
        'edges': edges
    }
    return state


def copy(state):
    puzzle = [row[:] for row in state['puzzle']]
    domain = [row[:] for row in state['domain']]
    new_state =  {
        'puzzle': puzzle, 
        'domain': unique_white_cells(puzzle, domain),
        'edges': state['edges']
    }
    return new_state


# General test - No solution if there are still unset cells
def check_solution(state):
    return domain_complete(state['domain']) and test_duplicate_number(state['puzzle'])


def domain_complete(domain):
    for i in domain:
        for j in i:
            if len(j) != 1:
                return False
    return True


# Rule 1 - No duplicate numbers in rows and columns for white cells
def test_duplicate_number(puzzle):
    transpose = list(zip(*puzzle)) # Invert to get columns
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j] != 'B':
                if has_duplicates(puzzle[i], transpose[j], puzzle[i][j]):
                    return False
    return True


# Check if a number is a duplicate within its row or column
def has_duplicates(row, col, value):
    if row.count(value) > 1 or col.count(value) > 1:
        return True
    return False


# Marks numbers that are unique (they occur once in their row or column)
# a number is uncertain, V must be white
def unique_white_cells(puzzle, domain):
    transpose = list(zip(*puzzle))
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if (not has_duplicates(puzzle[i], transpose[j], puzzle[i][j])
                and puzzle[i][j] != 'B'):
                domain[i][j] = 'V'
    return domain


# Rule 2 - No black cells are touching, diagonal is allowed, label black as 'B'
# Check if cell is allowed to be black, regardless of whether it is black or white
def black_allowed(state, i, j):
    for i2, j2 in state['edges'][i][j]:
        if state['puzzle'][i2][j2] == 'B':
            return False
    return True


# Rule 3 - All white cells form one touching group
def test_white_connected(grid, edges):
    visited = [[False for cell in row] for row in grid]
    node = first_white(grid)
    if total_white_cells(grid) == touch(node, visited, grid, edges, 1):
        return True
    return False


# Count all white cells irrespective of touching
def total_white_cells(grid):
    count = 0
    for i in grid:
        for j in i:
            if j != 'B':  
                count = count + 1
    return count


# Recursive touch method to check if all white cells are connected, sets checked locations 
# to 'C' and counts them during backtracking
def touch(node, visited, grid, edges, count):
    if node is None:
        return 0 # No white cells, so don't search
    else:
        i, j = node
        visited[i][j] = True
        for i2, j2 in edges[i][j]:
            if grid[i2][j2] != 'B' and not visited[i2][j2]:
                count = touch([i2, j2], visited, grid, edges, count) + 1
        return count


# Location of first white cell to count from
def first_white(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != 'B':
                return [i, j]
    return None


# Forward checking - If a cell is turned black adjust the domains of adjacent cells
# by removing 'B' from the domain
def fc_black(state, i, j):
    for i2, j2 in state['edges'][i][j]:
        state['domain'][i2][j2] = state['domain'][i2][j2].replace('B', '')
        if state['domain'][i2][j2] == '':
            return None
    return state


# Forward checking - If a cell is turned white adjust the domains of all the cells with
# a duplicate value in the row and colum by removing 'W'
def fc_white(state, i, j):
    size = len(state['puzzle'])
    k = 1
    while i-k >= 0:
        if state['puzzle'][i-k][j] == state['puzzle'][i][j]: 
            state['domain'][i-k][j] = state['domain'][i-k][j].replace('W', '')
            if state['domain'][i-k][j] == '':
                return None
        k += 1
    k = 1
    while i+k < size:
        if state['puzzle'][i+k][j] == state['puzzle'][i][j]: 
            state['domain'][i+k][j] = state['domain'][i+k][j].replace('W', '')
            if state['domain'][i+k][j] == '':
                return None
        k += 1
    k = 1
    while j-k >= 0:
        if state['puzzle'][i][j-k] == state['puzzle'][i][j]: 
            state['domain'][i][j-k] = state['domain'][i][j-k].replace('W', '')
            if state['domain'][i][j-k] == '':
                return None
        k += 1
    k = 1
    while j+k < size:
        if state['puzzle'][i][j+k] == state['puzzle'][i][j]: 
            state['domain'][i][j+k] = state['domain'][i][j+k].replace('W', '')
            if state['domain'][i][j+k] == '':
                return None
        k += 1
    return state


def cell_surrounded(state, i, j):
    count = 0
    for i2, j2 in state['edges'][i][j]:
        if state['domain'][i2][j2] == 'B':
            count += 1

    if count == len(state['edges'][i][j])-1:
        for i2, j2 in state['edges'][i][j]:
            if state['domain'][i2][j2] != 'B':
                state['domain'][i2][j2] = state['domain'][i2][j2].replace('B', '')
                state['domain'][i][j] = state['domain'][i][j].replace('B', '')
                if state['domain'][i2][j2] == '' or state['domain'][i][j] == '':
                    return None
    return state

