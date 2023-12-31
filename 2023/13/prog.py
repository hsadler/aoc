import sys

sys.path.append("../..")
import random
import uuid
import itertools
from dataclasses import dataclass

from helpers import functions, grid

# functions.test_rotate_matrix()
# functions.test_transpose_matrix()

# To summarize your pattern notes, add up the number of columns
# to the left of each vertical line of reflection; to that,
# also add 100 multiplied by the number of rows above each
# horizontal line of reflection.


def print_matrix(matrix: list[list[str]]):
    for row in matrix:
        print(row)


# parse input to get list of grids
grids: list[grid.Grid] = []
INPUT_FILE = "input.txt"
# INPUT_FILE = "test_input.txt"
with open(INPUT_FILE, "r") as f:
    inputs = f.read().split("\n\n")
    for input in inputs:
        matrix: list[list[str]] = []
        lines = input.split("\n")
        for line in lines:
            matrix.append(list(line.strip()))
        # print("input matrix:")
        # print_matrix(matrix)
        g = grid.Grid.build(matrix)
        # print("to matrix:")
        # print_matrix(g.to_matrix())
        for p in g.get_points():
            if p.val == "#":
                p.color = grid.Color.YELLOW
            else:
                p.color = grid.Color.DARK_GREEN
        grids.append(g)
# for g in grids:
#     print(g.to_print_string())


def is_grid_column_a_reflection(g: grid.Grid, column_index: int) -> bool:
    next_column_index = column_index + 1
    offset = 0
    if next_column_index >= g.get_width():
        return False
    while True:
        curr_column = g.get_column(column_index - offset)
        next_column = g.get_column(next_column_index + offset)
        if len(curr_column) == 0 or len(next_column) == 0:
            break
        if [p.val for p in curr_column] != [p.val for p in next_column]:
            return False
        offset += 1
    # print([p.val for p in g.get_column(column_index)])
    return True


def calc_grid_score(g: grid.Grid) -> int:
    reflected_column_index = None
    reflected_row_index = None
    for i in range(g.get_width()):
        if is_grid_column_a_reflection(g, i):
            reflected_column_index = i
            break
    g2 = grid.get_rotated_grid(g)
    g3 = grid.get_rotated_grid(g2)
    g4 = grid.get_rotated_grid(g3)
    for i in range(g4.get_width()):
        if is_grid_column_a_reflection(g4, i):
            # print(i)
            reflected_row_index = i
            break
    # print("grid")
    # print(g.to_print_string())
    # print("rotated grid")
    # print(g4.to_print_string())
    # print("reflected column index:", reflected_column_index)
    # print("reflected row index:", reflected_row_index)
    reflected_column_score = (
        reflected_column_index + 1 if reflected_column_index is not None else 0
    )
    reflected_row_score = (
        reflected_row_index + 1 if reflected_row_index is not None else 0
    )
    score = (reflected_column_score) + 100 * (reflected_row_score)
    return score


scores = []
for g in grids:
    score = calc_grid_score(g)
    scores.append(score)

score_sum = sum(scores)
# print(scores)
print(score_sum)
# assert score_sum == 405
