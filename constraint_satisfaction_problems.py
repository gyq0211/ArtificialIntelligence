# Constraint Satisfaction Problems
# Written in Python 2

import sys

# Checks if the given board satisfies the sudoku row condition
def check_rows(board, ignore_zeroes=False):
    for row in board:
        nums = set()
        for col in range(9):
            val = row[col]
            if ignore_zeroes and val == 0:
                continue
            if val in nums or val < 1 or val > 9:
                return False
            nums.add(val)
    return True

# Checks if the given board satisfies the sudoku column condition
def check_columns(board, ignore_zeroes=False):
    for col in range(9):
        # Generate a list representing the column for easy checking
        col_list = [i[col] for i in board]
        nums = set()
        for val in col_list:
            if ignore_zeroes and val == 0:
                continue
            if val in nums or val < 1 or val > 9:
                return False
            nums.add(val)
    return True

# Checks if the given board satisfies the sudoku 3x3 square condition
def check_squares(board, ignore_zeroes=False):
    # Check all rows of 3x3 squares
    for meta_row in range(3):
        # Check each of the 3 3x3 squares on that row
        for meta_col in range(3):
            row = meta_row * 3;
            col = meta_col * 3;
            nums = set()
            # Finally, check the 3x3 square itself
            for i in range(row, row + 3):
                for j in range(col, col + 3):
                    val = board[i][j]
                    if ignore_zeroes and val == 0:
                        continue
                    if val in nums or val < 1 or val > 9:
                        return False
                    nums.add(val)
    return True

# Checks if the given assignments are a valid sudoku solution
def goal_test(assignments):
    board = assignments_to_board(assignments)
    return (check_rows(board) and 
            check_columns(board) and 
            check_squares(board))

# Convert a set of assignments to a 9x9 board for simpler checking.
def assignments_to_board(assignments):
    board = [[0 for i in range(9)] for j in range(9)]
    for ((row, col), value) in assignments.items():
        board[row][col] = value
    return board

# Checks whether the assignments meet all constraints, 
# ignoring unassigned variables
def meets_constraints(assignments):
    board = assignments_to_board(assignments)
    return (check_rows(board, ignore_zeroes=True) and 
            check_columns(board, ignore_zeroes=True) and 
            check_squares(board, ignore_zeroes=True))

# Generate a dictionary of the initial assignments
def initial_assignments(easy=True):
    assignments = {}
    # Generate the easy assignments
    if easy:
        assignments[(0, 0)] = 6
        assignments[(0, 2)] = 8
        assignments[(0, 3)] = 7
        assignments[(0, 5)] = 2
        assignments[(0, 6)] = 1
        assignments[(1, 0)] = 4
        assignments[(1, 4)] = 1
        assignments[(1, 8)] = 2
        assignments[(2, 1)] = 2
        assignments[(2, 2)] = 5
        assignments[(2, 3)] = 4
        assignments[(3, 0)] = 7
        assignments[(3, 2)] = 1
        assignments[(3, 4)] = 8
        assignments[(3, 6)] = 4
        assignments[(3, 8)] = 5
        assignments[(4, 1)] = 8
        assignments[(4, 7)] = 7
        assignments[(5, 0)] = 5
        assignments[(5, 2)] = 9
        assignments[(5, 4)] = 6
        assignments[(5, 6)] = 3
        assignments[(5, 8)] = 1
        assignments[(6, 5)] = 6
        assignments[(6, 6)] = 7
        assignments[(6, 7)] = 5
        assignments[(7, 0)] = 2
        assignments[(7, 4)] = 9
        assignments[(7, 8)] = 8
        assignments[(8, 2)] = 6
        assignments[(8, 3)] = 8
        assignments[(8, 5)] = 5
        assignments[(8, 6)] = 2
        assignments[(8, 8)] = 3
    # Generate the evil assignments
    else:
        assignments[(0, 1)] = 7
        assignments[(0, 4)] = 4
        assignments[(0, 5)] = 2
        assignments[(1, 5)] = 8
        assignments[(1, 6)] = 6
        assignments[(1, 7)] = 1
        assignments[(2, 0)] = 3
        assignments[(2, 1)] = 9
        assignments[(2, 8)] = 7
        assignments[(3, 5)] = 4
        assignments[(3, 8)] = 9
        assignments[(4, 2)] = 3
        assignments[(4, 6)] = 7
        assignments[(5, 0)] = 5
        assignments[(5, 3)] = 1
        assignments[(6, 0)] = 8
        assignments[(6, 7)] = 7
        assignments[(6, 8)] = 6
        assignments[(7, 1)] = 5
        assignments[(7, 2)] = 4
        assignments[(7, 3)] = 8
        assignments[(8, 3)] = 6
        assignments[(8, 4)] = 1
        assignments[(8, 7)] = 5
    return assignments

# Get the next unassigned variable. This requires that there is
# at least one possible unassigned variable.
def get_unassigned_variable(assignments):
    # Find the first variable that hasn't been assigned.
    for i in range(9):
        for j in range(9):
            if (i, j) not in assignments:
                return i, j

# Get the domain for a given variable
def get_domain(row, col, assignments):
    domain = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    board = assignments_to_board(assignments)
    # Remove all elements from the row from the domain
    for val in board[row]:
        if val in domain:
            domain.remove(val)
    # Remove all elements from the column from the domain
    for val in [i[col] for i in board]:
        if val in domain:
            domain.remove(val)
    # Remove all elements from the 3x3 square from the domain
    meta_row = int(row / 3) * 3 
    meta_col = int(col / 3) * 3
    for i in range(meta_row, meta_row + 3):
        for j in range(meta_col, meta_col + 3):
            if board[i][j] in domain:
                domain.remove(board[i][j])

    return domain

# Print a 9x9 sudoku board.
def print_sudoku(board):
    print('---------------------------'),
    for row in range(0, 9):
        print('\n|'),
        for col in range(0, 9):
            if board[row][col] == 0:
                print('-'),
            else:
                print(board[row][col]),
            if col % 3 == 2: 
                print('|'),
        if row % 3 == 2:
            print('\n---------------------------'),
    print('')

# Return a solved solution for the given sudoku board
def solve(easy=True):
    assignments = initial_assignments(easy)
    return recursive_solve(assignments)[1]

# Recursively check assignments until we find a successful one
def recursive_solve(assignments):
    # Check if we have the solution
    if goal_test(assignments):
        return (True, assignments)

    # Get the next variable to assign, and try everything in its domain
    row, col = get_unassigned_variable(assignments)
    for val in get_domain(row, col, assignments):
        assignments[(row, col)] = val
        if not meets_constraints(assignments):
            del assignments[(row, col)]
            continue
        # If constraints are satisfied, continue assigning variables
        result = recursive_solve(assignments)
        if result[0]:
            return result
        del assignments[(row, col)]
    # If we never found a solution, return failure
    return (False, {})

# Run the solver for the easy and evil puzzles
if __name__ == "__main__":
    print("Solving the easy puzzle...")
    print_sudoku(assignments_to_board(solve(easy=True)))

    print("Solving the evil puzzle...")
    print_sudoku(assignments_to_board(solve(easy=False)))
    
