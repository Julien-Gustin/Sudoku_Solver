from utils.sudoku import Grid
from utils.backtracking import backtrackingSearch
import json
import os

if __name__ == '__main__':
    print("Choose the input by tipping the number associated to the sample \n \n")

    list = os.listdir('Sample/')
    i = 0
    for sample in list:
        print("{} : {}".format(i, sample))
        i += 1

    number = input("\t => ")

    f = list[int(number)]

    with open("Sample/"+f, 'r') as file:
        grid = json.load(file)

    grid = Grid(grid)
    backtrackingSearch(grid)
    print("Here is the solution for {}".format(f))


