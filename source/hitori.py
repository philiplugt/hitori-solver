
# Python imports
from time import perf_counter

# Hitori check imports
from hitori_puzzles import *
from hitori_helpers import (
    print_start_text, 
    print_end_text, 
    print_filler_text, 
    print_solution,
    display
)
from hitori_rules import (
    load_puzzle,
    check_solution,
    domain_complete,
    test_duplicate_number, 
    test_white_connected, 
    black_allowed, 
    unique_white_cells,  
    fc_black, 
    fc_white,
    cell_surrounded,
    copy
)


# Main method of solver
def solve_hitori(puzzle, method=False):
    if method:
        solve_brute(puzzle, 'Brute Force')
    else:
        solve_smart(puzzle, 'Smart')


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
    counter = 0
    nodes = [[0, 0]]
    states = [load_puzzle(puzzle)]

    while nodes:
        i, j = nodes.pop()
        state = states.pop()

        if check_solution(state):
            return counter, state['puzzle']

        if i >= len(state['puzzle']):
            continue

        # If initial domain is "V", then value is already unique, so skip
        if state['domain'][i][j] == 'V':
            states.append(state)
            nodes.append([i, j+1] if j+1 < len(state['puzzle'][i]) else [i+1, 0])
            continue

        # Append white
        white_state = copy(state)
        white_state['domain'][i][j] = 'W'
        counter += 1
        states.append(white_state)
        nodes.append([i, j+1] if j+1 < len(state['puzzle'][i]) else [i+1, 0])
        
        # Append black
        if black_allowed(state, i, j):
            black_state = copy(state)
            black_state['puzzle'][i][j] = 'B'
            black_state['domain'][i][j] = 'B'
            counter += 1

            if not test_white_connected(black_state['domain'], black_state['edges']):
                continue

            states.append(black_state)
            nodes.append([i, j+1] if j+1 < len(state['puzzle'][i]) else [i+1, 0])
    return counter, None


# Takes in a puzzle and attemps to solve it using the smart method
@timeit
def solve_smart(puzzle):
    counter = 0
    nodes = [[0, 0]]
    states = [load_puzzle(puzzle)]

    while nodes:

        i, j = nodes.pop()
        state = states.pop()

        if check_solution(state):
            return counter, state['puzzle']

        if i >= len(state['puzzle']) and j >= len(state['puzzle'][0]):
            continue

        state = cell_surrounded(state, i, j)
        if not state:
            continue
        
        # Go through the remaining values in the domain
        for d in state['domain'][i][j]:

            # If initial domain is white i.e. 'V', then value is already unique, so skip
            if d == 'V':
                states.append(state)
                nodes.append([i, j+1] if j+1 < len(state['puzzle'][i]) else [i+1, 0])
                continue

            # Append white
            if d == 'W':
                white_state = copy(state)
                white_state['domain'][i][j] = 'W'
                counter += 1

                # Forward check for Rule 1
                new_domain_white = fc_white(white_state, i, j)
                if not new_domain_white:
                    continue

                states.append(white_state)
                nodes.append([i, j+1] if j+1 < len(state['puzzle'][i]) else [i+1, 0])

            # Append black
            if d == 'B' and black_allowed(state, i, j):
                black_state = copy(state)
                black_state['puzzle'][i][j] = 'B'
                black_state['domain'][i][j] = 'B'
                counter += 1

                if not test_white_connected(black_state['domain'], black_state['edges']):
                    continue

                # Forward check for Rule 2
                black_state = fc_black(black_state, i, j)
                if not black_state:
                    continue

                states.append(black_state)
                nodes.append([i, j+1] if j+1 < len(state['puzzle'][i]) else [i+1, 0])
    return counter, None


if __name__ == "__main__":

    # Method to use: "True" for brute force; "False" for smart (CSP with Forward checking/MRV)
    method = True

    # Set a puzzle
    puzzle = PUZZLE_10

    solve_hitori(puzzle, method)
