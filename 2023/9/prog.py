import sys
sys.path.append('..')

# example line:
# -1 0 1 10 53 187 518 1233 2660 5388 10524 20246 38935 75343 146509 284568 548473 1044637 1965205 3663693 6812697

lines = []
with open("input.txt") as f:
    for l in f.readlines():
        lines.append([int(n) for n in l.split(" ")])

def get_diffs(line: list[int]):
    diffs = []
    for i in range(len(line) - 1):
        diffs.append(line[i+1] - line[i])
    return diffs

def get_list_string(l: list[int]):
    return ",".join([str(n) for n in l])

def get_history_string(history: list[list[int]]):
    return "\n".join([get_list_string(l) for l in history])

line_to_history: dict[str, list[list[int]]] = {}
for l in lines:
    # print(f"orig: {get_list_string(l)}")
    history = []
    curr = l
    history.append(curr)
    while any([l!=0 for l in curr]):
        curr = get_diffs(curr)
        history.append(curr)
        # print(get_list_string(curr))
    line_to_history[get_list_string(l)] = history

# for k, v in line_to_history.items():
#     print(get_history_string(v))

# part 1

DIRECTION_FORWARD = "forward"
DIRECTION_BACKWARD = "backward"
def extrapolate_next_values_in_direction(history: list[list[int]], direction: str):
    history.reverse()
    if direction == DIRECTION_FORWARD:
        for i, l in enumerate(history):
            if i == 0:
                l.append(0)
            elif i == 1:
                l.append(l[-1])
            else:
                l.append(l[-1] + history[i-1][-1])
    elif direction == DIRECTION_BACKWARD:
        for i, l in enumerate(history):
            if i == 0:
                l.append(0)
            elif i == 1:
                l.append(l[-1])
            else:
                l.insert(0, l[0] - history[i-1][0])
    else:
        raise Exception("Invalid direction")
    history.reverse()

for l in line_to_history.values():
    extrapolate_next_values_in_direction(l, direction=DIRECTION_FORWARD)

# for k, v in line_to_history.items():
#     print(get_history_string(v))

history_sums: list[int] = []
for history in line_to_history.values():
    history_sums.append(history[0][-1])
print(sum(history_sums))

print("------")

# part 2

for k, v in line_to_history.items():
    print(get_history_string(v))

for l in line_to_history.values():
    extrapolate_next_values_in_direction(l, direction=DIRECTION_BACKWARD)

for k, v in line_to_history.items():
    print(get_history_string(v))

history_sums: list[int] = []
for history in line_to_history.values():
    history_sums.append(history[0][0])
print(sum(history_sums))
