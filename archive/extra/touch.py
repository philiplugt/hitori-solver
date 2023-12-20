
# Alternative non-recursive implementation fo the touch() implemented in hitori_check.py
from hitori_check import first_white
from hitori import coord_within_bounds


# Count all white cells touching each other within a group
def white_group_count(puzzle):
    # Initialize necessary variables
    x = [1, 0, -1, 0]
    y = [0, -1, 0, 1]
    count = 0
    start_coord = first_white(puzzle)
    
    # Check if a white cell was found, see first_white()
    if start_coord is None:
        return 0
    else:
        stack = [start_coord] # Depth first travesal with stack

        # Create grid to track travesal visits
        binaryboard = [[False for i in puzzle] for j in puzzle]
        binaryboard[start_coord[0]][start_coord[1]] = True

        while stack:
            [i, j] = stack.pop()
            count = count + 1
            for k in range(4): # Size of x, y lists
                if coord_within_bounds( i+x[k], j+y[k], len(puzzle)) \
                and puzzle[i+x[k]][j+y[k]] != 0 \
                and not binaryboard[i+x[k]][j+y[k]]:
                    stack.append([i+x[k], j+y[k]])
                    binaryboard[i+x[k]][j+y[k]] = True
        return count

