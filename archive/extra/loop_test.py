
from time import perf_counter

# Overly complex method
def number_of_white(puzzle):
    count = len(puzzle) * len(puzzle) # Total possible positions
    for i in range(len(puzzle)):
    	# Whites can have any value except 0, so count 
    	# all 0's and subtract from total possible positions
        count = count - puzzle[i].count(0) 
    return count


# Simple method
def total_white_cells(puzzle):
	count = 0
	for i in puzzle:
		for j in i:
			if j != 0:	
				count = count + 1
	return count

if __name__ == '__main__':
	puzzle = [0, 5, 0, 3, 4], [1, 4, 3, 2, 5], [4, 5, 5, 4, 3], [3, 1, 5, 5, 4], [5, 4, 1, 4, 5]

	# Test complex method
	ts = perf_counter()
	print(number_of_white(puzzle))
	te = perf_counter()
	t1 = te - ts
	print(t1)

	print("")

	# Test simple method
	ts = perf_counter()
	print(total_white_cells(puzzle))
	te = perf_counter()
	t2 = te - ts
	print(te - ts)

	print("")
	print("Simple method takes much less time:")
	print(t2/t1)

	# Conclusion, simple method is a order of magnitude faster