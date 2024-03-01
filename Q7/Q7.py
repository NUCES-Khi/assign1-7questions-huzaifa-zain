def is_safe(board, row, col):
    for i in range(row):
        if board[i][col] == 1:
            return False
    i = row
    j = col
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1
    i = row
    j = col
    while i >= 0 and j < len(board):
        if board[i][j] == 1:
            return False
        i -= 1
        j += 1
    return True


def solve_n_queens_util(board, row):
    n = len(board)
    if row == n:
        return True
    for col in range(n):
        if is_safe(board, row, col):
            board[row][col] = 1
            if solve_n_queens_util(board, row + 1):
                return True
            board[row][col] = 0
    return False


def solve_n_queens(n):
    board = [[0] * n for _ in range(n)]
    if not solve_n_queens_util(board, 0):
        print("No solution exists.")
        return None
    return board


def print_board(board):
    for row in board:
        print(" ".join(map(str, row)))


def solve_and_print_n_queens(n):
    solution = solve_n_queens(n)
    if solution:
        print(f"Solution for {n}-Queens:")
        print_board(solution)


n = 8
solve_and_print_n_queens(n)
