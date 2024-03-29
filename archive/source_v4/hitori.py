
# Python imports
from time import perf_counter

# Hitori check imports
from hitori_check import (
    domain_complete,
    test_duplicate_number, 
    test_adjacent_black, 
    test_white_connected, 
    black_allowed, 
    unique_white_cells,  
    fc_black, 
    fc_white,
    cell_surrounded)


# Main method of solver
def solve_hitori(puzzle, method=False):
    if method:
        solve_brute(puzzle, "Brute Force")
    else:
        solve_smart(puzzle, "Smart")


# Wrapper for timing solvers
def timeit(func):
    def inner(*args, **kwargs):
        # Print introductory text for solver
        puzzle, mode = args

        print_start_text(puzzle, mode)
        timer_start = perf_counter()

        idx, solution = func(puzzle)
        print_solution(idx, solution, len(puzzle[len(puzzle[0])-1]))

        # Calculate and print time taken
        timer_end = perf_counter()
        time = timer_end - timer_start
        print_end_text(time)
    return inner

# Takes in a puzzle and attempts to solve it using the brute force method
# also known as a Generate and Test algorithm
@timeit
def solve_brute(puzzle):

    def check_solution(state, domain):
        return (domain_complete(domain) and test_duplicate_number(state))

    idx = 0
    initial_node = [0, 0]
    nodes = [initial_node]
    intial_state = [row[:] for row in puzzle]
    stack = [intial_state]
    initial_domain = unique_white_cells(puzzle)
    domains = [initial_domain]

    while nodes:
        i, j = nodes.pop()
        state = stack.pop()
        domain = domains.pop()

        if check_solution(state, domain):
            return idx, state
        else:
            # List of coordinates adjacent to current position
            u, d, l, r = i-1, i+1, j-1, j+1

            # Check if coordinates are within array bounds
            adjacent_cells = []
            if u >= 0:
                adjacent_cells.append([u, j])
            if d < len(state):
                adjacent_cells.append([d, j])
            if l >= 0:
                adjacent_cells.append([i, l])
            if r < len(state[i]):
                adjacent_cells.append([i, r])

            # Label cell as B (black) or W (white) if not yet labeled
            if domain[i][j] not in 'BW':
                if state[i][j] != 'B':
                    new_state_white = [row[:] for row in state]
                    new_domain_white = [row[:] for row in domain]
                    new_domain_white[i][j] = 'W'
                    idx += 1

                    for xy in adjacent_cells:                
                        nodes.append(xy)
                        stack.append(new_state_white)
                        domains.append(new_domain_white)

                # Black label is only given if conditions are met
                if domain[i][j] == '.' and black_allowed(domain, i, j):
                    new_state_black = [row[:] for row in state]
                    new_state_black[i][j] = 'B'
                    new_domain_black = [row[:] for row in domain]
                    new_domain_black[i][j] = 'B'
                    idx += 1

                    if test_white_connected(new_domain_black):
                        for xy in adjacent_cells:                
                            nodes.append(xy)
                            stack.append(new_state_black)
                            domains.append(new_domain_black)
    return idx, None


# Takes in a puzzle and attemps to solve it using the smart method
@timeit
def solve_smart(puzzle):

    def check_solution(state, domain):
        return (domain_complete(domain, True) and test_duplicate_number(state))

    matrix = []
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            matrix.append([i, j])

    idx = 0
    iterr = [0]
    initial_node = [0, 0]
    nodes = [initial_node]
    intial_state = [row[:] for row in puzzle]
    stack = [intial_state]
    initial_domain = unique_white_cells(puzzle, True)
    domains = [initial_domain]
    initial_visited = [[False] * len(puzzle[0])] * len(puzzle)
    visited_list = [initial_visited]

    while nodes:
        index = iterr.pop()
        i, j = nodes.pop()
        state = stack.pop()
        domain = domains.pop()
        visited = visited_list.pop()

        domain = cell_surrounded(domain, i, j)
        if not domain:
            continue

        if check_solution(state, domain):
            return idx, state
        else:
            # List of coordinates adjacent to current position
            u, d, l, r = i-1, i+1, j-1, j+1

            # Check if coordinates are within array bounds
            adjacent_cells = []
            if u >= 0 and not visited[u][j]:
                adjacent_cells.append([u, j])
            if d < len(state) and not visited[d][j]:
                adjacent_cells.append([d, j])
            if l >= 0 and not visited[i][l]:
                adjacent_cells.append([i, l])
            if r < len(state[i]) and not visited[i][r]:
                adjacent_cells.append([i, r])

            # Label cell as B (black) or W (white) if not yet labeled
            for d in domain[i][j]:


                # Unique white (V) cells are final, thus proceed to the next node
                if d == 'V' :
                    new_visited_unique = [row[:] for row in visited]
                    new_visited_unique[i][j] = True
                    
                    if index+1 < len(matrix):
                        iterr.append(index+1)
                        nodes.append(matrix[index+1])
                        stack.append(state)
                        domains.append(domain)
                        visited_list.append(new_visited_unique)
                    else:
                        iterr.append(index)
                        nodes.append(matrix[index])
                        stack.append(state)
                        domains.append(domain)
                        visited_list.append(new_visited_unique)

                if d == 'W':
                    new_state_white = [row[:] for row in state]
                    new_domain_white = [row[:] for row in domain]
                    new_domain_white[i][j] = 'W'
                    new_visited_white = [row[:] for row in visited]
                    new_visited_white[i][j] = True
                    idx += 1

                    # Forward check for Rule 1
                    new_domain_white = fc_white(new_state_white, new_domain_white, i, j)
                    if not new_domain_white:
                        continue

                    # MRV, add the smallest domains to the stack last so they get handled first
                    if index+1 < len(matrix):
                        iterr.append(index+1)
                        nodes.append(matrix[index+1])
                        stack.append(new_state_white)
                        domains.append(new_domain_white)
                        visited_list.append(new_visited_white)
                    else:
                        iterr.append(index)
                        nodes.append(matrix[index])
                        stack.append(new_state_white)
                        domains.append(new_domain_white)
                        visited_list.append(new_visited_white)

                # Black label is only given if conditions are met
                if d == 'B' and black_allowed(state, i, j):
                    new_state_black = [row[:] for row in state]
                    new_state_black[i][j] = 'B'
                    new_domain_black = [row[:] for row in domain]
                    new_domain_black[i][j] = 'B'
                    new_visited_black = [row[:] for row in visited]
                    new_visited_black[i][j] = True
                    idx += 1

                    if test_white_connected(new_domain_black):
                        # Forward check for Rule 2
                        new_domain_black = fc_black(new_domain_black, adjacent_cells)
                        if not new_domain_black:
                            continue

                        if index+1 < len(matrix):
                            iterr.append(index+1)
                            nodes.append(matrix[index+1])
                            stack.append(new_state_black)
                            domains.append(new_domain_black)
                            visited_list.append(new_visited_black)
                        else:
                            iterr.append(index)
                            nodes.append(matrix[index])
                            stack.append(new_state_black)
                            domains.append(new_domain_black)
                            visited_list.append(new_visited_black)
    return idx, None


# Prints a 2d array for display
def display(x):
    # Get the size of the largest digits, to determine width for printing grid
    big = 0
    for i in x:
        for j in i:
            big = max(big, len(str(j)))
    digits = big

    start_bar = "─" * (len(x[0]) * 2 + 1) + "─" * (len(x[0]) * (digits-1))
    end_bar = "─" * (len(x[len(x)-1]) * 2 + 1) + "─" * (len(x[len(x)-1]) * (digits-1))
    print(f"  ┌{start_bar}┐")
    for i in x:
        print("  │ ", end="")
        for j in i: 
            if isinstance(j, int):
                char = f"{str(j).rjust(digits)} "
            elif j == "B":
                char = "█ ".rjust(digits+1)
            else:
                char = f"{j} ".rjust(digits+1)
            print(char, end="")
        print("│")
    print(f"  └{end_bar}┘")


# Checks to see if coordinate on grid is within bounds
def coord_within_bounds(i, j, size):
    return 0 <= i < size and 0 <= j < size


def print_start_text(puzzle, mode):
    print(f"  Hitori Solver - {mode}")
    print("")
    print("  Initial puzzle state:")
    print("")
    display(puzzle)
    print("")
    print("  Start solving... (this might take a moment)")


def print_end_text(time):
    print("")
    print(f"  Elapsed time: {str(time)} seconds")
    print("")


def print_filler_text(width):
    print("")
    bars = "-" * (width * 2 + 3)
    print(f"  {bars}")
    print("")


def print_solution(states, solution, puzzle_length):
    if solution:
        print_filler_text(len(solution[0]))
        print(f"  Solution found! It took {str(states)} iteration(s):")
        print("")
        display(solution)
    else:
        print_filler_text(puzzle_length)
        print(f"  No solution found after {str(states)} iteration(s)")


if __name__ == "__main__":

    # Sample puzzles
    puzzle1 = [2, 1], [1, 1] # Simple case, solved if last 1 set to 0
    puzzle2 = [1, 2, 3], [1, 1, 3], [2, 3, 3] # Solvable
    puzzle3 = [1, 2, 3], [2, 2, 3], [1, 1, 3] # Unsolvable
    puzzle4 = [3, 3, 1, 2], [4, 3, 2, 3], [3, 4, 1, 1], [1, 2, 3, 4]
    puzzle5 = [5, 5, 3, 3, 4], [1, 4, 3, 2, 5], [4, 5, 5, 4, 3], [3, 1, 5, 5, 4], [5, 4, 1, 4, 5]
    puzzle5a = ['B', 5, 'B', 3, 4], [1, 4, 3, 2, 5], [4, 5, 5, 4, 3], [3, 1, 5, 5, 4], [5, 4, 1, 4, 5]
    puzzle6 = [5, 5, 4, 4, 2], [5, 1, 3, 4, 1], [2, 3, 3, 1, 1], [3, 4, 1, 2, 5], [1, 1, 4, 5, 5]
    puzzle6a = ['B', 5, 4, 'B', 2], [5, 3, 3, 4, 1], [2, 3, 'B', 1, 'B'], [3, 4, 1, 2, 5], ['B', 1, 'B', 5, 5]
    puzzle7 = [3, 2, 5, 4, 5], [2, 3, 4, 3, 5], [4, 3, 2, 4, 4], [1, 3, 3, 5, 5], [5, 4, 1, 2, 3]
    puzzle8 = [
        [4, 8, 1, 6, 3, 2, 5, 7],
        [3, 6, 7, 2, 1, 6, 5, 4],
        [2, 3, 4, 8, 2, 8, 6, 1],
        [4, 1, 6, 5, 7, 7, 3, 5],
        [7, 2, 3, 1, 8, 5, 1, 2],
        [3, 5, 6, 7, 3, 1, 8, 4],
        [6, 4, 2, 3, 5, 4, 7, 8],
        [8, 7, 1, 4, 2, 3, 5, 6],
    ]

    puzzle9 = [
        [3, 2, 4, 1, 3, 1],
        [2, 1, 1, 4, 1, 3],
        [1, 3, 3, 5, 6, 2],
        [6, 3, 1, 1, 5, 1],
        [3, 5, 4, 1, 4, 6],
        [4, 1, 6, 3, 1, 2],
    ]

    puzzle10 = [
        [1, 2, 5, 1, 4],
        [2, 4, 3, 2, 4],
        [4, 1, 2, 5, 3],
        [3, 5, 4, 1, 2],
        [2, 3, 2, 4, 5],
    ]

    puzzle11 = [
        [ 2,  9,  3,  2,  8,  5,  4,  7,  3, 10,  8, 11],
        [ 2,  7, 10,  6,  7,  4,  1, 10,  1,  9,  8, 12],
        [11,  6, 12, 11,  5,  4,  2, 12,  4,  6,  1,  1],
        [ 4, 10,  2, 11,  9,  6, 12,  4,  7,  5,  5,  1],
        [ 6, 12,  4, 12, 10,  1,  2,  5,  3, 11,  2,  3],
        [ 9,  4,  4,  5,  7,  6,  6, 12,  7,  2, 12,  9],
        [ 4,  2,  8,  4,  3, 10,  7,  2, 11, 12,  9,  5],
        [10, 10,  7,  9,  4,  1, 11,  2,  9,  1, 12,  7],
        [ 5,  1,  8,  4,  4, 12,  8, 10,  2,  5, 10,  3],
        [ 5,  3, 11,  9, 12,  9, 10,  1,  2,  4,  5,  2],
        [ 9,  6, 10, 12,  2,  9,  1,  1,  5, 12, 11,  4],
        [10, 11, 11, 10,  3,  2,  5,  8,  9,  3,  2,  7],
    ]

    puzzle12 = [
        [ 7, 15, 11, 11,  5,  3, 13,  1,  6, 13, 17,  5, 18, 12,  7, 14, 16,  8,  4,  6],
        [ 1, 16,  9,  7,  8, 19,  2, 14, 13,  2, 20,  4, 12, 10,  5,  8, 15, 16,  6,  5],
        [20,  1,  1, 11,  7, 13,  3,  5,  8,  9, 15, 10, 13, 16, 11,  3,  6,  4, 15,  6],
        [ 8,  6, 13,  3, 15,  4, 17, 19, 10,  4, 18,  8,  2,  8,  7,  5, 20, 10, 10,  7],
        [ 4, 11, 17, 15,  1, 12, 19, 13, 10, 16,  6,  5, 16, 19,  2,  3,  7, 15, 14,  1],
        [18,  8,  2,  1, 19,  1, 16, 20,  4,  6, 11, 17, 10, 13, 17,  7, 12, 12,  1, 14],
        [17,  8,  6, 10, 18,  5, 19, 17,  3, 17,  1,  5,  7,  2, 13,  4,  8, 14, 16,  5],
        [ 5, 13, 18, 11,  9, 15,  7, 11, 19,  1,  4, 14,  7,  6,  9,  2,  6, 16,  4,  3],
        [ 8, 18,  3,  1,  1, 14,  7,  2, 13, 12,  2, 20, 10, 10,  6, 13,  4, 15, 19, 15],
        [15,  9, 14, 19,  2, 10,  9, 16,  6, 14,  7,  1,  3, 14, 17,  2, 13,  5, 15, 12],
        [19,  2, 12, 20, 12,  6, 10,  7, 18, 16,  5, 11,  8, 14, 19, 14,  1, 13, 17,  4],
        [ 2, 16,  4, 10, 17,  1,  1,  8,  3, 15, 14, 16, 10,  5, 10,  9,  9, 20, 17, 19],
        [13, 18,  1,  4, 16,  8, 18, 12, 15,  7, 11,  3,  9,  3, 20, 19,  6, 17,  5, 15],
        [11,  5,  7, 16,  4,  6, 11,  6, 10, 18, 14,  3, 13, 15,  1,  9, 19, 10, 20,  8],
        [11, 19, 20, 15,  3, 16,  9, 17,  2, 11, 10, 12,  4, 16, 18, 15,  2,  6,  9,  1],
        [10,  4, 15,  6,  7,  5, 13,  7, 18, 17,  2, 14, 14,  9, 18, 10,  3,  2,  1, 20],
        [ 7, 17, 11, 12, 20,  4, 14, 13, 16,  5,  5, 13, 11,  1, 10,  5, 12,  2,  3, 17],
        [ 9,  9, 13, 14, 13,  7, 17,  4,  1, 10, 19, 11, 15,  8, 12, 17, 18,  3,  6, 16],
        [ 6, 20, 11, 17,  8,  7, 15,  9, 12, 10,  3, 19, 15,  4, 14,  1,  5,  4,  2, 18],
        [ 5, 18, 16, 12, 14, 17, 18, 18, 18, 19, 13,  9, 13, 20, 12,  1,  2, 15,  8, 13],
    ]

    # Method to use: "True" for brute force; "False" for smart (CSP with Forward checking/MRV)
    method = False

    # Set a puzzle
    puzzle = puzzle8

    solve_hitori(puzzle, method)
