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
    print(f'Sudoku shape: {size}x{len(sudoku[0])}',)

    if sudoku != [] and mode == Mode.UNIQUE:
        
        # your code to determine whether the solution is unique
        pass
    
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