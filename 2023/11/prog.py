import sys
sys.path.append('../..')
import random
import copy
import uuid
import itertools
from dataclasses import dataclass

from helpers import functions, grid

# parse input
INPUT_FILE = "input.txt"
# INPUT_FILE = "test_input.txt"
matrix: list[list[str]] = []
with open(INPUT_FILE, "r") as f:
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
        # print("row", y)
        temp_matrix.append(chars)
temp_matrix = functions.rotate_matrix(temp_matrix)
expanded_matrix: list[list[str]] = []
for y, chars in enumerate(temp_matrix):
    expanded_matrix.append(chars)
    if "#" not in chars:
        # print("row", y)
        expanded_matrix.append(chars)
expanded_matrix = functions.rotate_matrix(expanded_matrix)
g_expanded = grid.Grid.build(expanded_matrix)

for p in g_expanded.filter_points(g_expanded.get_points(), lambda p: p.val == "."):
    p.color = grid.Color.DARK_RED
for p in g_expanded.filter_points(g_expanded.get_points(), lambda p: p.val == "#"):
    p.color = grid.Color.YELLOW

# color expanded space
for y in range(g_expanded.get_height()):
    chars = [p.val for p in g_expanded.get_row(y)]
    if "#" not in chars:
        for p in g_expanded.get_row(y):
            p.color = grid.Color.GREEN
for x in range(g_expanded.get_width()):
    chars = [p.val for p in g_expanded.get_column(x)]
    if "#" not in chars:
        for p in g_expanded.get_column(x):
            p.color = grid.Color.GREEN

stars = [p for p in g_expanded.get_points() if p.val == "#"]
star_pairs: set[tuple[grid.Point, grid.Point]] = set()
# dedupe permutations
for pairs in itertools.permutations(stars, 2):
    pairs = list(pairs)
    pairs.sort(key=lambda p: p.x)
    pairs.sort(key=lambda p: p.y)
    star_pairs.add(tuple(pairs))

# calc distances between star pairs
star_pair_distances = {}
for star_pair in star_pairs:
    p1, p2 = star_pair
    distance = grid.Grid.manhattan_distance(p1, p2)
    star_pair_distances[star_pair] = distance
total_distance = 0
for star_pair, distance in star_pair_distances.items():
    total_distance += distance

print(total_distance)

# print(g_expanded.get_print_string())
