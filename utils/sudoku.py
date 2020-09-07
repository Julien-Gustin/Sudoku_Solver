from utils.utils import Alphabet
import numpy as np
class Grid:
    def __init__(self, grid):
        self.grid = self.__init_grid(grid)
        line = {}
        column = {}
        for i in range(len(self.grid)):
            line[i] = self.grid[i]
            column[Alphabet.get(i)] = self.grid[:, i]

        self.line = line
        self.column = column
        self.assignment = self.setAssignment()


    """ getBox
        @param i: the index of the line (integer)
        @param j: the index of the column (char)
    """
    def getBox(self, i, j):
        ret = []
        j = Alphabet.index(j)
        if i < 3:
            if j < 3:
                for k in range(0, 3):
                    for l in range(0, 3):
                        ret.append(self.grid[k][l])


            elif j >= 3 and j < 6:
                for k in range(0, 3):
                    for l in range(3, 6):
                        ret.append(self.grid[k][l])

            elif j >= 6:
                for k in range(0, 3):
                    for l in range(6, 9):
                        ret.append(self.grid[k][l])

        elif i >= 3 and i < 6:
            if j < 3:
                for k in range(3, 6):
                    for l in range(0, 3):
                        ret.append(self.grid[k][l])

            elif j >= 3 and j < 6:
                for k in range(3, 6):
                    for l in range(3, 6):
                        ret.append(self.grid[k][l])

            elif j >= 6:
                for k in range(3, 6):
                    for l in range(6, 9):
                        ret.append(self.grid[k][l])

        elif i >= 6:
            if j < 3:
                for k in range(6, 9):
                    for l in range(0, 3):
                        ret.append(self.grid[k][l])

            elif j >= 3 and j < 6:
                for k in range(6, 9):
                    for l in range(3, 6):
                        ret.append(self.grid[k][l])

            elif j >= 6:
                for k in range(6, 9):
                    for l in range(6, 9):
                        ret.append(self.grid[k][l])

        return ret

    """ getAt
        @bref: from an index line and index column, return the cell at this pos
        
        @param line: an integer
        @param column: a char
        
        @return: the element at the pos : line, column
    """
    def getAt(self, line, column):
        column = Alphabet.index(column)
        return self.grid[line][column]

    """ getConflict
        @bref: get all conflict cell with 'cell', i.e cell without value from the same line, column or box as form of coord
        
        @param i: the index of the line (integer)
        @param j: the index of the column (char)
        
        @return union: a list of conflict cell
    """
    def getConflict(self, i, j):
        line = [(elem.line, elem.column) for elem in self.line[i] if elem.val == 0]
        column = [(elem.line, elem.column) for elem in self.column[j] if elem.val == 0]
        box = [(elem.line, elem.column) for elem in self.getBox(i, j) if elem.val == 0]

        union = line + column + box
        union = list(set(union))
        union = [self.grid[elem[0]][Alphabet.index(elem[1])] for elem in union]

        return union

    """ setDomain
        @bref: set the domain of the cell at pos(i, j) (j is in alphabet form)
        
        @param i: the line (integer)
        @param j: the column (char)
        
        @return: if error False, otherwise a list of integer
    """
    def setDomain(self, i, j):
        domain = []
        line = [elem.val for elem in self.line[i]]
        column = [elem.val for elem in self.column[j]]
        box = [elem.val for elem in self.getBox(i, j)]

        union = line + column + box

        union = np.unique(union)
        for k in range(0, 10):
            if k not in union:
                domain.append(k)

        if len(domain) == 0:
            print("ERREUR : {} {}".format(i, j))
            return False

        return domain

    """ setAt
        @bref: set at pos(i, j) the value 'val' and modify the domain of cell in conflict 
        
        @param i: the line (integer)
        @param j: the column (char)
        @param val: a integer [0, 10[
        
        @return: ass a list of assignement or False if error
    """
    def setAt(self, i, j, val):
        print("add : {} {} => {}".format(i, j, val))
        self.grid[i][Alphabet.index(j)].setVal(val)

        conflict_cells = self.getConflict(i, j)
        l = []
        for cell in conflict_cells:
            if val in cell.domain:
                l.append(cell)

        ass = self.setAssignment(l)
        if ass is False:
            return False

        return ass

    """ removeAt
        @bref: remove from a pos(i, j) the value which is in

        @param i: the line (integer)
        @param j: the column (char)

        @return: ass a list of assignement or False if error
    """
    def removeAt(self, line, column):
        print("remove : {} {}".format(line, column))
        self.grid[line][Alphabet.index(column)].setVal(0)
        ass = {}

        for cell in self.getConflict(line, column):
            dom = self.setDomain(cell.line, cell.column)
            self.grid[cell.line][Alphabet.index(cell.column)].domain = dom
            ass[cell.line, cell.column] = dom

        return ass


    """ 
        @param l: list of cell:
    """
    def setAssignment(self, l=None):
        ass = {}
        if l is None:
            for line in range(9):
                for j in range(9):
                    if self.grid[line][j].val != 0:
                        ass[line, Alphabet.get(j)] = self.grid[line][j].val

                    else:
                        ass[line, Alphabet.get(j)] = self.setDomain(line, Alphabet.get(j))

        else:
            for cell in l:
                line = cell.line
                column = Alphabet.index(cell.column)
                ret = self.setDomain(line, cell.column)
                if ret is not False:
                    ass[line, cell.column] = ret
                    self.grid[line, column].domain = ret

                else:
                    return False

        return ass

    def __repr__(self):
        alphabet = Alphabet.alphabet[:9]
        i = 0
        var = "  "
        for lettre in alphabet:
            if (i % 3) == 0:
                var += " "
            i += 1
            var += lettre + "  "

        i = 0
        for rows in self.grid:
            if (i % 3) == 0:
                var += "\n"

            var += str(i) + " "
            j = 1
            for cell in rows:
                var += str(cell)
                if (j % 3) == 0:
                     var += " "
                j += 1

            var += "\n"
            i += 1
        return var

    def __init_grid(self, grid):
        alphabet = Alphabet.alphabet[:9]
        i = 0
        while i < len(grid):
            j = 0
            while j < len(grid[i]):
                grid[i][j] = Cell(grid[i][j], i, alphabet[j])
                j += 1
            i += 1

        return np.array(grid)

    # def get_(self, cell):

class Cell:
    def __init__(self, val, line, column):
        self.val = val
        self.line = line
        self.column = column
        if val == 0:
            self.domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        else:
            self.domain = [val]

    def setVal(self, val):
        self.val = val
        self.domain = [val]

    def __repr__(self):
        return "[" + str(self.val) + "]"

