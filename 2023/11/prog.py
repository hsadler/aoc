import sys
sys.path.append('../..')
import random
import copy
import uuid
from dataclasses import dataclass

from helpers import functions, grid

# parse input
matrix: list[list[str]] = []
with open("input.txt", "r") as f:
    lines = f.read().split("\n")
    for line in lines:
        matrix.append(list(line.strip()))
g = grid.Grid.build(matrix)

for p in g.filter_points(g.get_points(), lambda p: p.val == "."):
    p.color = grid.Color.DARK_RED
for p in g.filter_points(g.get_points(), lambda p: p.val == "#"):
    p.color = grid.Color.YELLOW

expanded_matrix: list[list[str]] = []
for row in matrix:
    expanded_row: list[str] = []
    for col in row:
        expanded_row.append(col)
        expanded_row.append(col)
    expanded_matrix.append(expanded_row)
    expanded_matrix.append(expanded_row)

g_expanded = grid.Grid.build(expanded_matrix)
print(g_expanded.get_print_string())
