import sys
sys.path.append('..')

import math
from dataclasses import dataclass

from helpers import functions
functions.test_sort_list()

# example node:
# NNN = (TNT, XDJ)

LEFT = "L"
RIGHT = "R"
START_NODE_ID = "AAA"
END_NODE_ID = "ZZZ"

class Node:
    id: str
    left: str
    right: str
    def __init__(self, id: str, left: str, right: str):
        self.id = id
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Node(id={self.id}, left={self.left}, right={self.right})"
    def __str__(self):
        return self.__repr__()

# parse input
nodes: list[Node] = []
directions: list[str] = []
with open("input.txt") as f:
    contents = f.read()
    raw_directions, raw_nodes = contents.split("\n\n")
    directions = list(raw_directions)
    for n in raw_nodes.split("\n"):
        id = n.split(" = ")[0]
        left, right = n.split(" = ")[1].split(", ")
        left = left[1:]
        right = right[:-1]
        nodes.append(Node(id, left, right))

id_to_node = {}
for n in nodes:
    id_to_node[n.id] = n

# part 1
curr_node = id_to_node[START_NODE_ID]
moves_count = 0
while curr_node.id != END_NODE_ID:
    for d in directions:
        # print(f"curr_node: {curr_node}")    
        moves_count += 1
        if d == LEFT:
            curr_node = id_to_node[curr_node.left]
        elif d == RIGHT:
            curr_node = id_to_node[curr_node.right]
        if curr_node.id == END_NODE_ID:
            print(f"found end node {curr_node} in {moves_count} moves")
            break

print('----------------------')

# part 2

# find all start nodes
start_nodes: list[Node] = []
for n in nodes:
    if n.id.endswith("A"):
        start_nodes.append(n)

# find all end nodes
end_nodes: list[Node] = []
for n in nodes:
    if n.id.endswith("Z"):
        end_nodes.append(n)

@dataclass
class HistoryStep():
    node: Node
    moves_count: int
    instruction_index: int
    next_history_step: "HistoryStep" = None
    prev_history_step: "HistoryStep" = None
    def to_dict(self):
        return {
            "node": self.node.id,
            "moves_count": self.moves_count,
            "instruction_index": self.instruction_index,
            "next_history_step": self.next_history_step.node.id if self.next_history_step else None,
            "prev_history_step": self.prev_history_step.node.id if self.prev_history_step else None,
            "is_end": self.node.id.endswith("Z") if self.node else False,
        }

@dataclass
class Ghost():
    start_node: Node
    curr_node: Node
    history: list[HistoryStep]

# build a run history for each ghost
HISTORY_STEP_LIMIT = 100000
ghosts: list[Ghost] = []
# for start_node in start_nodes:
for start_node in start_nodes:
    print(f"building run history for ghost starting at {start_node}")
    ghost = Ghost(start_node=start_node, curr_node=start_node, history=[])
    moves_count = 0
    while moves_count < HISTORY_STEP_LIMIT:
        for i, d in enumerate(directions):
            history_step = HistoryStep(
                node=ghost.curr_node, 
                moves_count=moves_count, 
                instruction_index=i
            )
            if len(ghost.history) > 0:
                ghost.history[-1].next_history_step = history_step
                history_step.prev_history_step = ghost.history[-1]
            ghost.history.append(history_step)
            moves_count += 1
            if d == LEFT:
                ghost.curr_node = id_to_node[ghost.curr_node.left]
            elif d == RIGHT:
                ghost.curr_node = id_to_node[ghost.curr_node.right]
            if moves_count == HISTORY_STEP_LIMIT:
                break
    ghosts.append(ghost)

# find cycle for ghost
def find_cycle(ghost: Ghost) -> list[HistoryStep]:
    for i in range(2, len(ghost.history), 2):
        # print(f"i: {i}")
        histories_to_check = ghost.history[-i:]
        # print(f"len histories_to_check: {len(histories_to_check)}")
        midpoint_index = len(histories_to_check) // 2
        # print(f"midpoint_index: {midpoint_index}")
        first_half = histories_to_check[:midpoint_index]
        second_half = histories_to_check[midpoint_index:]
        if (
            [h.node.id for h in first_half] == [h.node.id for h in second_half]
            and first_half[0].instruction_index == second_half[0].instruction_index
        ):
            return first_half
    raise Exception("no cycle found")

# gather information to predict where end-nodes will be
@dataclass
class GhostInfo():
    ghost_id: str
    cycle_offset: int
    cycle_length: int
    def get_next_cycle_move(self, move: int) -> int:
        return move + self.cycle_length
    def move_is_valid_end(self, move: int) -> bool:
        return move % self.cycle_length == self.cycle_offset
    def to_dict(self):
        return {
            "ghost": self.ghost_id,
            "cycle_offset": self.cycle_offset,
            "cycle_length": self.cycle_length,
        }
ghost_id_to_ghost_info: dict[str, GhostInfo] = {}
# ghost starting at NPA has cycle of length 19631 and offset 19631 and instruction_index 0
# ghost starting at HMA has cycle of length 13771 and offset 27542 and instruction_index 0
# ghost starting at GQA has cycle of length 21389 and offset 21389 and instruction_index 0
# ghost starting at CXA has cycle of length 17287 and offset 17287 and instruction_index 0
# ghost starting at AAA has cycle of length 23147 and offset 23147 and instruction_index 0
# ghost starting at VHA has cycle of length 20803 and offset 20803 and instruction_index 0
ghost_id_to_ghost_info = {
    "NPA": GhostInfo(ghost_id="NPA", cycle_offset=19631, cycle_length=19631),
    "HMA": GhostInfo(ghost_id="HMA", cycle_offset=13771, cycle_length=13771),
    "GQA": GhostInfo(ghost_id="GQA", cycle_offset=21389, cycle_length=21389),
    "CXA": GhostInfo(ghost_id="CXA", cycle_offset=17287, cycle_length=17287),
    "AAA": GhostInfo(ghost_id="AAA", cycle_offset=23147, cycle_length=23147),
    "VHA": GhostInfo(ghost_id="VHA", cycle_offset=20803, cycle_length=20803),
}
if False:
    for g in ghosts:
        cycle = find_cycle(g)
        if cycle:
            end_step_from_cycle = [h for h in cycle if h.node.id.endswith("Z")][0]
            ghost_id_to_ghost_info[g.start_node.id] = GhostInfo(
                ghost_id=g.start_node.id,
                cycle_offset=end_step_from_cycle.moves_count,
                cycle_length=len(cycle)
            )
            print(f"ghost starting at {g.start_node.id} has cycle of length {len(cycle)} and offset {end_step_from_cycle.moves_count} and instruction_index {end_step_from_cycle.instruction_index}")
        else:
            print(f"no cycle found for ghost starting at {g.curr_node}")

lcm = math.lcm(*[gi.cycle_length for gi in ghost_id_to_ghost_info.values()])
print(f"lcm: {lcm}")
