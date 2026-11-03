import sys
import subprocess
import random as rand

# reads a sudoku from file
# columns are separated by |, lines by newlines
# Example of a 4x4 sudoku:
# |1| | | |
# | | | |3|
# | | |2| |
# | |2| | |
# spaces and empty lines are ignored
def sudoku_read(filename):
    myfile = open(filename, 'r')
    sudoku = []
    N = 0
    for line in myfile:
        line = line.replace(" ", "")
        if line == "":
            continue
        line = line.split("|")
        if line[0] != '':
            exit("illegal input: every line should start with |\n")
        line = line[1:]
        if line.pop() != '\n':
            exit("illegal input\n")
        if N == 0:
            N = len(line)
            if N != 4 and N != 9 and N != 16 and N != 25:
                exit("illegal input: only size 4, 9, 16 and 25 are supported\n")
        elif N != len(line):
            exit("illegal input: number of columns not invariant\n")
        line = [int(x) if x != '' and int(x) >= 0 and int(x) <= N else 0 for x in line]
        sudoku += [line]
    return sudoku
        
#print sudoku on stdout
def sudoku_print(myfile, sudoku):
    if sudoku == []:
        myfile.write("impossible sudoku\n")
    N = len(sudoku)
    for line in sudoku:
        myfile.write("|")
        for number in line:
            if N > 9 and number < 10:
                myfile.write(" ")
            myfile.write(" " if number == 0 else str(number))
            myfile.write("|")
        myfile.write("\n")



# here you are encouraged to define your own functions !
from pysat.solvers import Glucose3

VARIABLE_COUNT = 0
def getNewVariable():
    global VARIABLE_COUNT
    VARIABLE_COUNT += 1
    return VARIABLE_COUNT

# CONSTRAINT For SUDOKU
# 1. Each box has 1 number
def one_number_for_each_box(solver, variables, size, N):
    # 1.1. Each box has AT LEAST 1 number
    # => p(i,j,k)
    for i in range(size):
        for j in range(size):
            solver.add_clause(variables[i][j])

    # 1.2. Each box has AT MOST 1 number
    # => not( p[i][j][k1] /\ p[i][j][k2] )
    # => not p[i][j][k1] \/ not p[i][j][k2]
    for i in range(size):
        for j in range(size):
            for k1 in range(N):
                for k2 in range(k1+1, N):
                    solver.add_clause([-variables[i][j][k1], -variables[i][j][k2]])

    return

# 2. Box at the same row, column cannot have the same number
def different_number_for_box_at_same_row_column(solver, variables, size, N):
    # 2.1. Box at the same row cannot have the same number
    # not( p[i][j1][k] /\ p[i][j2][k] )
    # => not p[i][j1][k] \/ not p[i][j2][k]
    for i in range(size):
        for j1 in range(size):
            for j2 in range(j1+1,size):
                for k in range(N):
                    solver.add_clause([-variables[i][j1][k], -variables[i][j2][k]])

    # 2.2. Box at the same column cannot have the same number
    # not( p[i1][j][k] /\ p[i2][j][k] )
    # => not p[i1][j][k] \/ not p[i2][j][k]
    for i1 in range(size):
        for i2 in range(i1+1, size):
            for j in range(size):
                for k in range(N):
                    solver.add_clause([-variables[i1][j][k], -variables[i2][j][k]])

    return

# 3. Box in same square cannot have the same number
def different_number_for_box_in_same_square(solver, variables, size, k):
    s = int(size ** 0.5)  # square side: 2 for 4x4, 3 for 9x9, 4 for 16x16, 5 for 25x25

    for bi in range(s):          # which block row
        for bj in range(s):      # which block column
            # all cells of this square
            cells = [(bi * s + di, bj * s + dj) for di in range(s) for dj in range(s)]
            # print(cells)

            for a in range(len(cells)):
                for b in range(a + 1, len(cells)):
                    i1, j1 = cells[a]
                    i2, j2 = cells[b]
                    for n in range(k):
                        solver.add_clause([-variables[i1][j1][n], -variables[i2][j2][n]])

    return


def decode(model, variables, size, N):
    true_vars = set(v for v in model if v > 0)
    grid = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            for k in range(N):
                if variables[i][j][k] in true_vars:
                    grid[i][j] = k + 1
    return grid


from enum import Enum
class Mode(Enum):
    SOLVE = 1
    UNIQUE = 2
    CREATE = 3
    CREATEMIN = 4
    CREATEFAIR = 5
    CREATESPARSE = 6
    CREATEHARD = 7

OPTIONS = {}
OPTIONS["-s"] = Mode.SOLVE
OPTIONS["-u"] = Mode.UNIQUE
OPTIONS["-c"] = Mode.CREATE
OPTIONS["-cm"] = Mode.CREATEMIN
OPTIONS["-cf"] = Mode.CREATEFAIR
OPTIONS["-ch"] = Mode.CREATESPARSE
OPTIONS["-chf"] = Mode.CREATEHARD

if len(sys.argv) != 3 or not sys.argv[1] in OPTIONS :
    sys.stdout.write("./template.py <operation> <argument>\n")
    sys.stdout.write("     where <operation> can be -s, -u, -c, -cm, -cf, -cs, -ch\n")
    sys.stdout.write("  ./template.py -s <input>.txt: solves the Sudoku in input, whatever its size\n")
    sys.stdout.write("  ./template.py -u <input>.txt: check the uniqueness of solution for Sudoku in input, whatever its size\n")
    sys.stdout.write("  ./template.py -c <size>: creates a Sudoku of appropriate <size>\n")
    sys.stdout.write("  ./template.py -cm <size>: creates a Sudoku of appropriate <size> using only <size>-1 numbers\n")
    sys.stdout.write("  ./template.py -cf <size>: creates a Sudoku of appropriate <size> fairly\n")
    sys.stdout.write("  ./template.py -cs <size>: creates a sparse Sudoku of appropriate <size>\n")
    sys.stdout.write("  ./template.py -ch <size>: creates a hard Sudoku of appropriate <size>\n")
    sys.stdout.write("    <size> is either 4, 9, 16, or 25\n")
    exit("Bad arguments\n")

mode = OPTIONS[sys.argv[1]]
if mode == Mode.SOLVE or mode == Mode.UNIQUE:
    filename = str(sys.argv[2])
    sudoku = sudoku_read(filename)
    size = len(sudoku)

    # your code to solve the sudoku
    print(f'Sudoku shape: {size}x{len(sudoku[0])}', )

    #region Initializing SAT SOLVER
    N = size
    solver = Glucose3()

    # Initializing VARIABLES
    VARIABLES = [[[getNewVariable() for k in range(N)] for j in range(size)] for i in range(size)]
    print(f'NUM VARIABLES: {VARIABLE_COUNT}')
    #endregion

    #region Generate rules for sudoku
    one_number_for_each_box(solver, VARIABLES, size, N)
    result = solver.solve()
    # print('First result: ', result)

    different_number_for_box_at_same_row_column(solver, VARIABLES, size, N)
    result = solver.solve()
    # print('Second result: ', result)

    different_number_for_box_in_same_square(solver, VARIABLES, size, N)
    # result = solver.solve()
    # print('Third result: ', result)
    #endregion

    #region Add constant value from sudoku file into rules
    for i in range(size):
        for j in range(size):
            k = sudoku[i][j]
            if k != 0:
                solver.add_clause([VARIABLES[i][j][k - 1]])
    #endregion

    #region Solving sudoku
    if solver.solve():
        grid = decode(solver.get_model(), VARIABLES, size, N)
        sudoku_print(sys.stdout, grid)
    else:
        sudoku_print(sys.stdout, [])  # "impossible sudoku"
    #endregion

    if sudoku != [] and mode == Mode.UNIQUE:
        
        # your code to determine whether the solution is unique
        # forbid this exact solution: at least one cell must differ
        blocking = [-VARIABLES[i][j][grid[i][j] - 1]
                    for i in range(size) for j in range(size)]
        solver.add_clause(blocking)

        if solver.solve():
            print("The solution is NOT unique. Another solution:")
            grid2 = decode(solver.get_model(), VARIABLES, size, N)
            sudoku_print(sys.stdout, grid2)
        else:
            print("The solution is unique.")
    
elif mode == Mode.CREATE:
    size = int(sys.argv[2])

    # your code to create a sudoku

elif mode == Mode.CREATEMIN:
    size = int(sys.argv[2])

    # your code to create a sudoku with only <size>-1 different numbers
    
elif mode == Mode.CREATEFAIR:
    size = int(sys.argv[2])

    # your code to create a sudoku fairly

elif mode == Mode.CREATESPARSE:
    size = int(sys.argv[2])

    # your code to create a sparse sudoku

elif mode == Mode.CREATEHARD:
    size = int(sys.argv[2])

    # your code to create a hard sudoku