import sys

sys.path.append("../..")
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
for p in g.filter_points(g.get_points(), lambda p: p.val == "."):
    p.color = grid.Color.DARK_RED
for p in g.filter_points(g.get_points(), lambda p: p.val == "#"):
    p.color = grid.Color.YELLOW
for y in range(g.get_height()):
    chars = [p.val for p in g.get_row(y)]
    if "#" not in chars:
        for p in g.get_row(y):
            p.color = grid.Color.GREEN
for x in range(g.get_width()):
    chars = [p.val for p in g.get_column(x)]
    if "#" not in chars:
        for p in g.get_column(x):
            p.color = grid.Color.GREEN

# part 1

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

# get star pairs
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

print(g_expanded.to_print_string())
print("part 1: ", total_distance)
print("--------------------")

# part 2

EXPANSION_FACTOR: int = 1000000

# create new grid
g2 = grid.Grid.build(matrix)
for p in g2.get_points():
    if p.val == ".":
        p.color = grid.Color.DARK_RED
    elif p.val == "#":
        p.color = grid.Color.YELLOW

# print(g2.to_print_string())

# get star pairs
stars = [p for p in g2.get_points() if p.val == "#"]
star_pairs: set[tuple[grid.Point, grid.Point]] = set()
# dedupe permutations
for pairs in itertools.permutations(stars, 2):
    pairs = list(pairs)
    pairs.sort(key=lambda p: p.x)
    pairs.sort(key=lambda p: p.y)
    star_pairs.add(tuple(pairs))

# note expansion row and col indices
x_expansion_positions = []
y_expansion_positions = []
for x in range(g2.get_width()):
    col = g2.get_column(x)
    chars = [p.val for p in col]
    if "#" not in chars:
        x_expansion_positions.append(x)
for y in range(g2.get_height()):
    row = g2.get_row(y)
    chars = [p.val for p in row]
    if "#" not in chars:
        y_expansion_positions.append(y)
print("x_expansion_positions", x_expansion_positions)
print("y_expansion_positions", y_expansion_positions)


def get_expansions_count(
    p1: grid.Point, p2: grid.Point, x_expansion_positions, y_expansion_positions
) -> int:
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    min_x = min(x1, x2)
    max_x = max(x1, x2)
    min_y = min(y1, y2)
    max_y = max(y1, y2)
    expansions_count = 0
    for x in x_expansion_positions:
        if x > min_x and x < max_x:
            expansions_count += 1
    for y in y_expansion_positions:
        if y > min_y and y < max_y:
            expansions_count += 1
    return expansions_count


# calculate distances between star pairs
star_pair_distances = {}
for star_pair in star_pairs:
    p1, p2 = star_pair
    expansions_count = get_expansions_count(
        p1, p2, x_expansion_positions, y_expansion_positions
    )
    distance = grid.Grid.manhattan_distance(p1, p2) + expansions_count * (
        EXPANSION_FACTOR - 1
    )
    star_pair_distances[star_pair] = distance

total_distance = 0
for star_pair, distance in star_pair_distances.items():
    total_distance += distance

print(g2.to_print_string())
print("part 2: ", total_distance)
# assert total_distance == 8410
print("--------------------")
