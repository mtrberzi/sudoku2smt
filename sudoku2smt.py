#!/usr/bin/python3

## This program converts Sudoku puzzles into a set of SMT formulas
## that can be solved by an SMT solver such as Z3.
## Input is from stdin and consists of 9 lines, each of which has 9 entries.
## Each line of input corresponds to a single row of the Sudoku board.
## Each entry on a given line represents the value in the corresponding
## column of that row, given as an integer between 1 and 9,
## or a marker denoting a blank cell, given as a '.' (period).
## The program writes to standard output a set of SMT formulas
## that together encode the initial state of the puzzle
## and the constraints on a valid solution.
## For example, the following input (without comment signs):
## 5 3 . . 7 . . . .
## 6 . . 1 9 5 . . .
## . 9 8 . . . . 6 .
## 8 . . . 6 . . . 3
## 4 . . 8 . 3 . . 1
## 7 . . . 2 . . . 6
## . 6 . . . . 2 8 .
## . . . 4 1 9 . . 5
## . . . . 8 . . 7 9
##

import sys
import re

regex_one_entry = "\\s*([1-9\\.])\\s*"
regex_one_line = ""
for i in range(9):
    regex_one_line += regex_one_entry

re_line = re.compile(regex_one_line)

def parse_sudoku_line(line):
    match_line = re_line.search(line)
    if match_line:
        entries = []
        for i in range(9):
            entries.append(match_line.group(i + 1))
        return entries
    else:
        raise Exception("Invalid input line '{0}'.".format(line))

initial_grid = [] # initial_grid[row][column] = entry

# Read 9 lines of input
for i in range(9):
    line = sys.stdin.readline()
    grid_line = parse_sudoku_line(line)
    initial_grid.append(grid_line)
pass
