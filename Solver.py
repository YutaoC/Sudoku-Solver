def sudoku(board):
    """main function to solve the sudoku"""
    if is_complete(board):
        return board

    r, c = find_empty(board)
    for val in range(1, 10):  # try all the possible numbers
        board[r][c] = val
        if valid(board):
            result = sudoku(board)  # continue to the next "step"
            if is_complete(result):  # if the sudoku is completed
                return result
        board[r][c] = 0  # if the number is not valid, set it back to EMPTY
    return board


def is_complete(board):
    """check if the sudoku is completed"""
    return all(all(val is not 0 for val in row) for row in board)


def find_empty(board):
    """find the first blocks that are empty"""
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == 0:
                return i, j  # return the row number and the col number
    return False  # id no empty block, return False


def valid(board):
    """check whether the number is valid"""
    if not row_valid(board):
        return False
    if not col_valid(board):
        return False
    if not cell_valid(board):
        return False
    return True


def row_valid(board):
    """check if the number is valid in its row"""
    for row in board:
        if duplicate(row):  # if contain duplicats
            return False
    return True


def col_valid(board):
    """check if the number is valid in its column"""
    for j in range(len(board[0])):
        if duplicate([board[i][j] for i in range(len(board))]):  # if contain duplicates
            return False
    return True


def cell_valid(board):
    """check if the number is valid in its cell"""
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            block = []
            for h in range(3):
                for k in range(3):
                    block.append(board[i+h][j+k])  # store all the number in a list
            if duplicate(block):
                return False
    return True


def duplicate(lst):
    """check if there is duplicates in the list"""
    c = {}
    for val in lst:
        if val in c and val != 0:
            return True
        c[val] = True
    return False
