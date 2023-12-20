
# Python imports
from time import perf_counter
from copy import deepcopy
from collections import deque

# Hitori check imports
from hitori_check import (test_duplicate_number, 
    test_adjacent_black, 
    test_white_connected, 
    valid_black, 
    unique_values, 
    is_duplicate, 
    fc_black, 
    fc_white)


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
        print_start_text(args[0], args[1])
        timer_start = perf_counter()

        func(args[0])

        # Calculate and print time taken
        timer_end = perf_counter()
        time = timer_end - timer_start
        print_end_text(time)
    return inner


# Takes in a puzzle and attempts to solve it using the brute force method
@timeit
def solve_brute(puzzle):
    
    # Initialize start variables
    states = 1
    solution_found = False
    solution = []

    # Initialize puzzle add initial state
    current_state = []
    state_q = deque([deepcopy(puzzle)])

    # Check if initial puzzle state is the solution
    if test_duplicate_number(puzzle) and test_adjacent_black(puzzle) \
            and test_white_connected(puzzle):
        solution_found = True
        solution = puzzle

    # Breadth first search to find first valid solution_found
    while state_q and not solution_found:

        # Check if current state is the answer
        current_state = list(state_q.popleft())  
        if test_duplicate_number(current_state) :
            solution_found = True
            solution = current_state
            break

        # Create board labelling unique values (cells that must be white due to Rule 1)
        uniqueboard = unique_values(current_state)
        for i in range(len(puzzle)):
            for j in range(len(puzzle)):

                # Check value that can be skipped
                if current_state[i][j] != 0 and uniqueboard[i][j] == 0:

                    # Create a new state by turning a cell black
                    new_state = deepcopy(current_state)
                    new_state[i][j] = 0

                    # Check if rules are upheld by new state, if so add to queue
                    if valid_black(new_state, i, j) and test_white_connected(new_state):
                        states = states + 1
                        state_q.append(new_state)

    print_solution(states, solution_found)


# Takes in a puzzle and attemps to solve it using the smart method
@timeit
def solve_smart(puzzle):

    # Initialize start variables
    states = 1
    solution_found = False
    solution = []

    # Depth first search with forward checking and MRV
    x = [1, 0, -1, 0]
    y = [0, -1, 0, 1]
    start_node = [0, 0]
    nodes = [start_node] # Depth first travesal with stack
    # Track if a location has already been visited
    visitboard = [[False for i in puzzle] for j in puzzle]

    # Create a grid to track the domain for each puzzle node
    # Each character represents the remaining domain values for that cell
    # B is for black, and W for white
    domain = [['BW' for i in range(len(puzzle))] for j in range(len(puzzle))]
    # Update black domain to reflect nodes that must be white, due to unique values
    uniqueboard = unique_values(puzzle)
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if uniqueboard[i][j] == 1:
                domain[i][j] = 'W' # If unique, cannot be black, thus 'W'

    # 3D list to keep track of puzzle and domain
    state = [list(deepcopy(puzzle)), domain, visitboard]
    stack = [state]

    # Check if initial puzzle is the solution
    if test_duplicate_number(puzzle) and test_adjacent_black(puzzle) \
            and test_white_connected(puzzle):
        solution_found = True
        solution = puzzle

    # Start depth first search
    while nodes and not solution_found:
        [i, j] = nodes.pop()
        current_state = stack.pop()
        current_state[2][i][j] = True

        for d in current_state[1][i][j]:
            new_puzzle = deepcopy(current_state[0])
            new_domain = deepcopy(current_state[1])
            new_visit = deepcopy(current_state[2])
            new_domain[i][j] = d

            # Forward check based on value of domain d
            if d == 'B':
                new_puzzle[i][j] = 0
                if valid_black(new_puzzle, i, j) and test_white_connected(new_puzzle):
                    states = states + 1 # Each coloring is a new state
                    new_domain = fc_black(new_domain, i, j) # Forward check rule 2
                    # No need for MRV, FC reduces all adjacent domains to 1 or 0 already
                    # There is no gain to be had from sorting domains from 1 to 0
                    for k in range(4): # Size of x, y lists
                        if coord_within_bounds( i+x[k], j+y[k], len(puzzle)) \
                                and not new_visit[i+x[k]][j+y[k]]:
                            nodes.append([i+x[k], j+y[k]])
                            stack.append([new_puzzle, new_domain, new_visit])
            
            if d == 'W':
                states = states + 1 # Each coloring is a new state
                new_domain = fc_white(new_puzzle, new_domain, i, j) # Forward check rule 1
                # MRV: By adding adjacent domains to the stack, first large domains to 
                # be traversed later, then smaller domains to be traversed first.
                for k in range(4): # Size of x, y lists
                    if coord_within_bounds(i+x[k], j+y[k], len(puzzle)) \
                            and not new_visit[i+x[k]][j+y[k]] \
                            and len(new_domain[i+x[k]][j+y[k]]) > 1: 
                        nodes.append([i+x[k], j+y[k]])
                        stack.append([new_puzzle, new_domain, new_visit])
                for k in range(4): # Size of x, y lists
                    if coord_within_bounds(i+x[k], j+y[k], len(puzzle)) \
                            and not new_visit[i+x[k]][j+y[k]] \
                            and len(new_domain[i+x[k]][j+y[k]]) == 1: 
                        nodes.append([i+x[k], j+y[k]])
                        stack.append([new_puzzle, new_domain, new_visit])
                for k in range(4): # Size of x, y lists
                    if coord_within_bounds(i+x[k], j+y[k], len(puzzle)) \
                            and not new_visit[i+x[k]][j+y[k]] \
                            and len(new_domain[i+x[k]][j+y[k]]) < 1: 
                        nodes.append([i+x[k], j+y[k]])
                        stack.append([new_puzzle, new_domain, new_visit])

            if test_duplicate_number(new_puzzle):
                solution_found = True
                solution = new_puzzle

    print_solution(states, solution, solution_found)


# Prints a 2d array for display
def display(x):
    for i in x:
        print("  ", end="")
        print(i)


# Checks to see if coordinate on grid is within bounds
def coord_within_bounds(i, j, size):
    return 0 <= i < size and 0 <= j < size


def print_start_text(puzzle, mode):
    print(f"  Hitori Solver - {mode}")
    print("  Puzzle to solve:")
    print("")
    display(puzzle)
    print("")
    print("  Start solving... (this might take a moment)")


def print_end_text(time):
    print("")
    print(f"  Elapsed time: {str(time)} seconds")
    print("")


def print_filler_text():
    print("")
    print("  ------------")
    print("")


def print_solution(states, solution, solution_found):
    if solution_found:
        print_filler_text()
        print(f"  Solution found! It took {str(states)} iteration(s):")
        print("")
        display(solution)
    else:
        print_filler_text()
        print(f"  No solution found after {str(states)} iteration(s)")


if __name__ == "__main__":

    # Sample puzzles
    puzzle1 = [2, 1], [1, 1] # Simple case, solved if last 1 set to 0
    puzzle2 = [1, 2, 3], [1, 1, 3], [2, 3, 3] # Solvable
    puzzle3 = [1, 2, 3], [2, 2, 3], [1, 1, 3] # Unsolvable
    puzzle4 = [3, 3, 1, 2], [4, 3, 2, 3], [3, 4, 1, 1], [1, 2, 3, 4]
    puzzle5a = [5, 5, 3, 3, 4], [1, 4, 3, 2, 5], [4, 5, 5, 4, 3], [3, 1, 5, 5, 4], [5, 4, 1, 4, 5]
    puzzle5b = [0, 5, 0, 3, 4], [1, 4, 3, 2, 5], [4, 5, 5, 4, 3], [3, 1, 5, 5, 4], [5, 4, 1, 4, 5]
    puzzle6 = [5, 5, 4, 4, 2], [5, 1, 3, 4, 1], [2, 3, 3, 1, 1], [3, 4, 1, 2, 5], [1, 1, 4, 5, 5]
    puzzle6a = [0, 5, 4, 0, 2], [5, 0, 3, 4, 1], [2, 3, 0, 1, 0], [3, 4, 1, 2, 5], [0, 1, 0, 5, 5]
    puzzle7 = [3, 2, 5, 4, 5], [2, 3, 4, 3, 5], [4, 3, 2, 4, 4], [1, 3, 3, 5, 5], [5, 4, 1, 2, 3]

    # Method to use: "True" for brute force; "False" for smart (CSP with Forward checking/MRV)
    method = False

    # Set a puzzle
    puzzle = puzzle6

    solve_hitori(puzzle, method)