import numpy as np

with open("input.txt", "r") as f:
    numbers = [int(n) for n in f.readline().split(",")]
    boards = []
    lines = f.readlines()
    while lines:
        lines.pop(0)
        boards.append([
            np.array([[int(line[i:i + 2]) for line in [lines.pop(0)] for i in range(0, 14, 3)] for j in range(5)]),
            np.zeros((5, 5), dtype=bool)
        ])

def board_won(board):
    return any(np.any(np.all(board[1], axis=axis)) for axis in [0, 1])

def board_score(n, board):
    return n * np.sum(board[0][np.logical_not(board[1])])

def part_1(boards):
    while True:
        n = numbers.pop(0)
        for board in boards:
            board[1] = np.logical_or(board[1], board[0] == n)
            if board_won(board):
                return board_score(n, board)

def part_2(boards):
    while True:
        n = numbers.pop(0)
        for board in boards:
            board[1] = np.logical_or(board[1], board[0] == n)
        if len(boards) == 1 and board_won(boards[0]):
            return board_score(n, boards[0])
        boards = list(filter(lambda board: not board_won(board), boards))


if __name__ == '__main__':
    print("part 1", part_1(boards))
    print("part 2", part_2(boards))