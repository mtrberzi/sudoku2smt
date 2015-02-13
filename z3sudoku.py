#!/usr/bin/python

## This program uses the Z3 SMT solver to find solutions to Soduko puzzles.
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
import z3

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
variables_grid = []
s = z3.Solver()

# Helper functions to generate SMT2 expressions

def entry(row,col):
    return "x%d%d" % (row, col)

def declare_variable(row, col):
    return z3.Int(entry(row,col))

def declare_entry(row,col):
    v = variables_grid[row][col]
    initial_entry = initial_grid[row][col]
    if initial_entry == ".":
        s.add(v >= 1)
        s.add(v <= 9)
    else:
        e = int(initial_entry)
        s.add(v == e)

def constrain_row(row):
    for i in range(9):
        for j in range(i+1, 9):
            e1 = variables_grid[row][i]
            e2 = variables_grid[row][j]
            s.add(e1 != e2)

def constrain_column(col):
    for i in range(9):
        for j in range(i+1, 9):
            e1 = variables_grid[i][col]
            e2 = variables_grid[j][col]
            s.add(e1 != e2)

def constrain_subgrid(x, y):
    xmin = 3*x
    xmax = 3*x + 2
    ymin = 3*y
    ymax = 3*y + 2
    for i1 in range(xmin, xmax+1):
        for j1 in range(ymin, ymax+1):
            for i2 in range(xmin, xmax+1):
                for j2 in range(ymin, ymax+1):
                    if i1 != i2 or j1 != j2:
                       e1 = variables_grid[i1][j1]
                       e2 = variables_grid[i2][j2]
                       s.add(e1 != e2)
    
## Entry point.

# Read 9 lines of input
for i in range(9):
    line = sys.stdin.readline()
    grid_line = parse_sudoku_line(line)
    initial_grid.append(grid_line)

for row in range(9):
    line = []
    for col in range(9):
        line.append(declare_variable(row, col))
    variables_grid.append(line)

# Declare all constants for grid entries
for row in range(9):
    for col in range(9):
        declare_entry(row, col)

# Constrain all rows
for row in range(9):
    constrain_row(row)

# Constrain all columns
for col in range(9):
    constrain_column(col)

# Constrain all 3x3 subgrids
for x in range(3):
    for y in range(3):
        constrain_subgrid(x, y)
        
# finally
if s.check():
    m = s.model()
    for row in range(9):
        for col in range(9):
            v = variables_grid[row][col]
            sys.stdout.write(str(m[v]) + " ")
        sys.stdout.write("\n")
else:
    print("no solution")

