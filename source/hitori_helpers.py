
def display(grid):
    # Find number of digits to determine width for printing
    digits = 0
    for row in grid:
        digits = max(digits, max([len(str(cell)) for cell in row]))

    # Calculate the length of the start and end bars
    start_bar = "─" * (len(grid[0]) * 2 + 1) + "─" * (len(grid[0]) * (digits-1))
    end_bar = "─" * (len(grid[len(grid)-1]) * 2 + 1) + "─" * (len(grid[len(grid)-1]) * (digits-1))
    
    # Print puzzle
    print(f"  ┌{start_bar}┐")
    for i in grid:
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


def print_start_text(puzzle, mode):
    print(f"  Hitori Solver - {mode}")
    print(f"")
    print(f"  Initial puzzle state:")
    print(f"")
    display(puzzle)
    print(f"")
    print(f"  Start solving... (this might take a moment)")


def print_end_text(time):
    print(f"")
    print(f"  Elapsed time: {str(time)} seconds")
    print(f"")


def print_filler_text(width):
    print(f"")
    bars = "-" * (width * 2 + 3)
    print(f"  {bars}")
    print(f"")


def print_solution(states, solution, puzzle_length):
    if solution:
        print_filler_text(len(solution[0]))
        print(f"  Solution found! It took {str(states)} iteration(s):")
        print(f"")
        display(solution)
    else:
        print_filler_text(puzzle_length)
        print(f"  No solution found after {str(states)} iteration(s)")