from operator import itemgetter
from utils.utils import Alphabet

""" isComplete
    @bref: verify if all the element of assignement has a matching value
    
    @param assignement: dictionary cell associating to a domain (set of value)
    
    @return bool
"""
def isComplete(assignement):
    for key, val in assignement.items():
        if isinstance(val, list) and key != "inference":
            return False

    return True

""" selectUnassignedVariable
    @bref: select the most usefull variable (cell) from assignement 
    
    @param assignement: dictionary cell associating to a domain (set of value)
    @param csp: is an instance of sudoku
    
    @return orderList, is a list of [legal_value, conflict_cells, cell] sorted in a way that the first as the fewest "legal value"
        and is involved in the largest number of constraints on other unassigned var
"""
def selectUnassignedVariable(csp, assignement):
    unOrdererList = []
    for key, val in assignement.items():
        if isinstance(val, list) and key != "inference":
            line = key[0]
            column = key[1] # lettre
            legal_value = len(val)
            conflict_cells = len(csp.getConflict(line, column))
            unOrdererList.append((legal_value, conflict_cells, csp.getAt(line, column)))

    unOrdererList = sorted(unOrdererList, key=itemgetter(1), reverse=True)
    orderedList  = sorted(unOrdererList, key=itemgetter(0))
    return orderedList[0][2]

""" backtrackingSearch
    @bref: a simple back tracking search
    
    @param assignement: dictionary cell associating to a domain (set of value)
    @param csp: is an instance of sudoku
    
    @return: the solution of the problem
"""
def backtrackingSearch(csp):
    assignment = csp.assignment
    assignment["inference"] = []
    return backtrack(assignment, csp)

""" orderDomainValues
    @bref: return a list of [nb_of_conflicts, domain], ordered by the domain
    
    @param var: the variable, here is a Cell
    @param assignement: dictionary cell associating to a domain (set of value)
    @param csp: is an instance of sudoku
    
    @param orderedList: a list of the domain of var, sorted
"""
def orderDomainValues(var, assignement, csp):
    domain = assignement[var.line, var.column]
    unOrdererList = []
    for nb in domain:
        conflictCells = csp.getConflict(var.line, var.column)
        conflict = 0
        for cell in conflictCells:
            dom_of_cell = assignement[cell.line, cell.column]
            if nb in dom_of_cell:
                conflict += 1

        unOrdererList.append((conflict, nb))

    orderedList = sorted(unOrdererList, key=itemgetter(0))
    return orderedList


""" inference
    @bref: if there are no error return a list with a function and these variable to do the opposite move or False

    @param var: the variable, here is a Cell
    @param assignement: dictionary cell associating to a domain (set of value)
    @param csp: is an instance of sudoku

    @return match, inferences: bool, 
"""
def inference(csp, var, assignment):
    line = var.line
    column = var.column
    val = assignment[line, column]
    del assignment[line, column]

    inferences = lambda : csp.removeAt(line, column)
    # inferences = (csp.removeAt, line, column)
    ass = csp.setAt(line, column, val)

    if ass is not False:
        updateAssignment(assignment, ass)
        return True, inferences

    return False, inferences

""" updateAssignment
    @bref: update assignement using ass
    
    @param assignement: dictionary cell associating to a domain (set of value)
    @param ass: a set of {(line, column), value}
"""
def updateAssignment(assignement, ass):
    for key, val in ass.items():
        assignement[key] = val

""" backtrack
    @bref: the backtrack algorithm

    @param assignement: dictionary cell associating to a domain (set of value)
    @param csp: is an instance of sudoku

    @return False: bool (if an error occur)
            result: dictionary cell associating to a domain (set of value) (if a solution is found)
"""
def backtrack(assignment, csp):
    print(csp)
    if isComplete(assignment):
        return assignment

    var = selectUnassignedVariable(csp, assignment)
    for value in orderDomainValues(var, assignment, csp):
        nb = value[1]
        assignment[var.line, var.column] = nb
        match, inferences = inference(csp, var, assignment)
        assignment["inference"].append(inferences)

        if match is not False:
            result = backtrack(assignment, csp)

            if result is not False:
                return result

        inf = assignment["inference"].pop()
        ass = inf()
        updateAssignment(assignment, ass)

    return False

