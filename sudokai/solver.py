import os
import pandas as pd


def print_grid(grid):
    for i in range(9):
        row = grid[9*i:9*i+9]
        print("".join(map(str, row)))


def solve(puzzle):

    SQUARES = [
        [0,  1,  2,  9,  10, 11, 18, 19, 20],
        [3,  4,  5,  12, 13, 14, 21, 22, 23],
        [6,  7,  8,  15, 16, 17, 24, 25, 26],
        [27, 28, 29, 36, 37, 38, 45, 46, 47],
        [30, 31, 32, 39, 40, 41, 48, 49, 50],
        [33, 34, 35, 42, 43, 44, 51, 52, 53],
        [54, 55, 56, 63, 64, 65, 72, 73, 74],
        [57, 58, 59, 66, 67, 68, 75, 76, 77],
        [60, 61, 62, 69, 70, 71, 78, 79, 80]
    ]

    grid = list(puzzle)

    def row(i): return list(range(9*i, 9*i+9))
    def col(i): return list(range(i, 81, 9))
    def square(i): 
        for row in SQUARES:
            if i in row:
                return row


    def all_diff(xs):
        s = [0] * 10
        for x in xs:
            value = grid[x]
            if value > 0:
                s[value] += 1
                if s[value] > 1:
                    return False
        return True


    def valid(i): 
        return all_diff(row(i//9)) and all_diff(col(i%9)) and all_diff(square(i))


    def backtrack(k=0):

        if k >= 81:
            return True
        
        if grid[k] > 0:
            return backtrack(k+1)
        
        for i in range(1, 9+1):
            grid[k] = i
            if valid(k):
                if backtrack(k+1):
                    return True
            grid[k] = 0

        return False

    result = backtrack()
    return result, grid

