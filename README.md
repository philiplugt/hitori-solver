
# Building a solver for Hitori

Task to create a brute force and intelligent (forward checking/minimum remaining values) 
solver for [Hitori puzzles](https://en.wikipedia.org/wiki/Hitori).

This assignment was originally for an 2013 RIT Artificial Intelligence course.

### Versioning

Successfully tested and run with Python 3.11

Original code is from 2013-01-05, and was updated from 2021-04-11 through 2021-04-16

### How to use

Downloaded the files and run with `python hitori.py`

Within `hitori.py` within `if __name__ == '__main__':` statement you can set `method = True` to use the brute solver, default is the smart solver (`method = False`).

You can use your own puzzle by setting the `puzzle` variable to a list of lists. 

### Details

Hitori is a Japanese puzzle game, which consists of a n-by-n grid of numbers with numbers ranging from 1-n.

The game has three conditions that must be met in order to win:
1. There must be no duplicate numbers in the rows or columns
2. Black values (represented by 0 value) cannot be adjacent (vertically and horizontally) to each other
3. White values (non-black values) must not be isolated (all connected)

This solver implements 2 methods an brute force solver and a smart solver. The brute force solver traverses the entire puzzle and tries each combination to check for a solution. The only optimization to the brute force solver is that it skips cells that are known to be white due to Rule 1. The smart solver uses techniques such as forward checking and minimum remaining values to solve puzzles significantly faster. It labels the entire puzzle board with values, such as `BW`, `B`, `W`, or ` ` (where B is black, and W is white), to keep track of valid values for each cell. Then via a process of elimination, as defined by Hitori's rules, the total number of combinations are reduced. A cell `BW` can still be black or white, while a cell `B` or `W` can *only* be black or *only* be white. As a result, cells that have been labelled ` ` are empty and can never be valid. Therefore when the solver encounters a ` ` that search traversal is ended, because it cannot contain a solution. The solver then proceeds on with the next (still) valid puzzle state. The solver repeats these steps until a solution if found, or all puzzle states have been exhausted and no solution has been found.