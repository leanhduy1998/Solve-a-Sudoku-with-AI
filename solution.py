assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)



row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)



def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def createDiagnalUnitsInPeer():
    diagnal_units_left_to_right = []
    diagnal_units_right_to_left = []
    for line in range(0,5):
            if line < 4:
                diagnal_units_left_to_right.extend(cross(rows[line],cols[line]))
                diagnal_units_right_to_left.extend(cross(rows[line],cols[(len(cols)-1)-line]))
            
                diagnal_units_right_to_left.extend(cross(rows[(len(rows)-1)-line],cols[line]))
                diagnal_units_left_to_right.extend(cross(rows[(len(rows)-1)-line],cols[(len(cols)-1)-line]))
            else:
                diagnal_units_left_to_right.extend(cross(rows[line],cols[line]))
                diagnal_units_right_to_left.extend(cross(rows[line],cols[line]))
    
    for unit in diagnal_units_left_to_right:
        peers[unit].update(diagnal_units_left_to_right)
        peers[unit].remove(unit)
        
    for unit in diagnal_units_right_to_left:
        peers[unit].update(diagnal_units_right_to_left)
        peers[unit].remove(unit)
        
    unitlist.append(diagnal_units_left_to_right)
    unitlist.append(diagnal_units_right_to_left)

def cross(a, b):
    return [s+t for s in a for t in b]

def grid_values(grid):
    assert len(grid) == 81
    
    values = []
    for c in grid :
        if c == '.':
            values.append("123456789")
        else:
            values.append(c)
    
    return dict(zip(boxes,values))

def display(values):
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values


def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        

        
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values



def solve(grid):
    createDiagnalUnitsInPeer()
    gridValues = grid_values(grid)
    gridValues = search(gridValues)
    
    return gridValues
    """
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists."""
    
def naked_twins(values):
    for unitArr in unitlist:
        for x in range(2,8):
            selectedKey = []
            selectedValue = []
            
            for unit in unitArr:    
                if len(values[unit]) == x:
                    selectedKey.append(unit)
                    selectedValue.append(values[unit])
            
            
            checkUnitArr = unitArr.copy()
            deletingkey = []
            
            for key in selectedKey:
                if selectedValue.count(values[key]) == x:
                    testSame = False
                    for sameKey in deletingkey:
                        if values[key] == values[sameKey]:
                            testSame = True
                    
                    if testSame == False:
                        deletingkey.append(key)
                    checkUnitArr.remove(key)
            
            for un in checkUnitArr:
                if len(values[un]) == 1:
                    checkUnitArr.remove(un)
                elif len(values[un]) < x:
                    checkUnitArr.remove(un)
                
            for key in deletingkey:
                for temp in checkUnitArr:
                    for digit in values[key]:
                        if digit in values[temp]:
                            newvalue = values[temp].replace(digit,'')
                            assign_value(values, temp, newvalue)
    return values


def search(values):
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                """
                print("{}: {}", "unit" ,unit)
                print("{}: {}", "dplaces[0]" ,dplaces[0])
                print("{}: {}", "values[dplaces[0]] before" ,values[dplaces[0]])
                values[dplaces[0]] = digit
                print("{}: {}", "values[dplaces[0]] after" ,values[dplaces[0]])
                """

                values[dplaces[0]] = digit

    return values


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
        

 
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
