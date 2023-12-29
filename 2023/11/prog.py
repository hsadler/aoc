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

# print(g.get_print_string())

# expand the space
temp_matrix: list[list[str]] = []
for y in range(g.get_height()):
    row = g.get_row(y)
    chars = [p.val for p in row]
    temp_matrix.append(chars)
    if "#" not in chars:
        print("row", y)
        temp_matrix.append(chars)
temp_matrix = functions.rotate_matrix(temp_matrix)
expanded_matrix: list[list[str]] = []
for y, chars in enumerate(temp_matrix):
    expanded_matrix.append(chars)
    if "#" not in chars:
        print("row", y)
        expanded_matrix.append(chars)
expanded_matrix = functions.rotate_matrix(expanded_matrix)
g_expanded = grid.Grid.build(expanded_matrix)

for p in g_expanded.filter_points(g_expanded.get_points(), lambda p: p.val == "."):
    p.color = grid.Color.DARK_RED
for p in g_expanded.filter_points(g_expanded.get_points(), lambda p: p.val == "#"):
    p.color = grid.Color.YELLOW

print(g_expanded.get_print_string())
