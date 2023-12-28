import sys
sys.path.append('../..')
import random
import copy
import uuid
from dataclasses import dataclass

import pygame

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
for p in g.filter_points(g.get_points(), lambda p: p.val == "S"):
    p.color = grid.Color.YELLOW

# print(g.get_print_string())
# exit()

char_to_valid_directions: dict[str, list[grid.Direction]] = {
    "|": [grid.Direction.DIRECTION_UP, grid.Direction.DIRECTION_DOWN],
    "-": [grid.Direction.DIRECTION_LEFT, grid.Direction.DIRECTION_RIGHT],
    "L": [grid.Direction.DIRECTION_UP, grid.Direction.DIRECTION_RIGHT],
    "J": [grid.Direction.DIRECTION_UP, grid.Direction.DIRECTION_LEFT],
    "7": [grid.Direction.DIRECTION_LEFT, grid.Direction.DIRECTION_DOWN],
    "F": [grid.Direction.DIRECTION_RIGHT, grid.Direction.DIRECTION_DOWN],
    "S": [
        grid.Direction.DIRECTION_UP, grid.Direction.DIRECTION_DOWN, 
        grid.Direction.DIRECTION_LEFT, grid.Direction.DIRECTION_RIGHT
    ],
}

@dataclass
class Location:
    id: uuid.UUID
    point: grid.Point
    distance: int
    previous_location_id: uuid.UUID | None

@dataclass
class Path:
    id: uuid.UUID
    curr_location: Location
    location_id_history: list[uuid.UUID]
    distance: int
    is_terminal: bool = False

start_point = g.filter_points(g.get_points(), lambda p: p.val == "S")[0]
start_location = Location(
    id=uuid.uuid4(),
    point=start_point,
    distance=0,
    previous_location_id=None
)
id_to_location: dict[uuid.UUID, Location] = {
    start_location.id: start_location
}
start_path = Path(
    id=uuid.uuid4(),
    curr_location=start_location,
    location_id_history=[start_location.id],
    distance=0
)
id_to_path: dict[uuid.UUID, Path] = {
    start_path.id: start_path
}
is_traveling: bool = True

def travel(g: grid.Grid, path: Path) -> bool:
    global char_to_valid_directions
    curr_p = path.curr_location.point
    valid_next_point_found: bool = False
    directions: list[grid.Direction] = char_to_valid_directions[curr_p.val]
    random.shuffle(directions)
    direction = directions[0]
    # validate next point
    next_p = g.get_neighbor(curr_p, direction=direction)
    next_p_in_history = False
    # get all locations in history and check against next point
    for location_id in path.location_id_history[:-1]:
        location = id_to_location[location_id]
        if location.point == next_p:
            next_p_in_history = True
            break
    if next_p is not None and not next_p_in_history:
        valid_next_point_found = True
        # create next location and put in lookup table
        next_location = Location(
            id=uuid.uuid4(),
            point=next_p,
            distance=path.distance + 1,
            previous_location_id=path.curr_location.id,
        )
        id_to_location[next_location.id] = next_location
        # set next location color
        next_location.point.color = grid.Color.GREEN
        path.curr_location = next_location
        path.location_id_history.append(next_location.id)
        path.distance += 1
    path.is_terminal = not valid_next_point_found
    return valid_next_point_found

def color_trail(head_locations: list[Location]):
    for l in head_locations:
        if l.previous_location_id is not None:
            loc = id_to_location[l.previous_location_id]
            loc.point.color = grid.Color.BLACK

def reset_grid(g: grid.Grid):
    for p in g.get_points():
        if p.val == ".":
            p.color = grid.Color.DARK_RED
        elif p.val == "S":
            p.color = grid.Color.YELLOW
        else:
            p.color = grid.Color.GRAY

def init_vars():
    global g, id_to_location, id_to_path, is_traveling
    start_point = g.filter_points(g.get_points(), lambda p: p.val == "S")[0]
    start_location = Location(
        id=uuid.uuid4(),
        point=start_point,
        distance=0,
        previous_location_id=None
    )
    id_to_location = {
        start_location.id: start_location
    }
    start_path = Path(
        id=uuid.uuid4(),
        curr_location=start_location,
        location_id_history=[start_location.id],
        distance=0
    )
    id_to_path = {
        start_path.id: start_path
    }
    is_traveling = True

HEADLES = False
if HEADLES:
    while is_traveling:
        is_traveling = False
        paths = list(id_to_path.values())
        print(f"paths: {len(paths)}")
        for path in paths:
            did_travel, new_paths = travel(g=g, path=path)
            if did_travel:
                is_traveling = True
    distances = [p.distance for p in id_to_path.values()]
    print(max(distances))
else:
    # Initialize pygame
    pygame.init()
    # Constants
    POSITION_MULTIPLIER = 6
    POSITION_OFFSET = 50
    WIDTH = g.get_width() * POSITION_MULTIPLIER + (POSITION_OFFSET * 2)
    HEIGHT = g.get_height() * POSITION_MULTIPLIER + (POSITION_OFFSET * 2)
    FPS = 1000
    TICK_DURATION = 1
    # Create a screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AOC 2023 day 10")
    # Create a clock object to control the frame rate
    clock = pygame.time.Clock()
    # Create a list of points
    points: list[tuple[int, int]] = []
    # Main game loop
    last_time = pygame.time.get_ticks()
    running = True
    while running:
        # Exit condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Update points
        current_time = pygame.time.get_ticks()
        if current_time - last_time >= TICK_DURATION and is_traveling:
            is_traveling = False
            paths: list[Path] = []
            terminated_paths: list[Path] = []
            for path in id_to_path.values():
                if not path.is_terminal:
                    paths.append(path)
                else:
                    terminated_paths.append(path)
            print(f"paths: {len(paths)}")
            print(f"terminated_paths: {len(terminated_paths)}")
            for path in paths:
                did_travel = travel(g=g, path=path)
                if did_travel:
                    is_traveling = True
            color_trail(head_locations=[p.curr_location for p in id_to_path.values()])
            last_time = current_time
        else:
            reset_grid(g=g)
            init_vars()
        # Clear the screen
        screen.fill(grid.Color.BLACK.value)
        # Draw the points
        for p in g.get_points():
            # print(f"point color: {p.get_color_as_tuple()}")
            # draw a circle
            pygame.draw.circle(
                screen, 
                p.get_color_as_tuple(), 
                (
                    p.x * POSITION_MULTIPLIER + POSITION_OFFSET, 
                    p.y * POSITION_MULTIPLIER + POSITION_OFFSET
                ), 
                2.8
            )
            # draw a triangle
            # pygame.draw.polygon(
            #     screen,
            #     p.get_color_as_tuple(),
            #     [
            #         (
            #             p.x * POSITION_MULTIPLIER + POSITION_OFFSET,
            #             p.y * POSITION_MULTIPLIER + POSITION_OFFSET - 2
            #         ),
            #         (
            #             p.x * POSITION_MULTIPLIER + POSITION_OFFSET - 2,
            #             p.y * POSITION_MULTIPLIER + POSITION_OFFSET + 2
            #         ),
            #         (
            #             p.x * POSITION_MULTIPLIER + POSITION_OFFSET + 2,
            #             p.y * POSITION_MULTIPLIER + POSITION_OFFSET + 2
            #         )
            #     ]
            # )
        # Update the display
        pygame.display.flip()
        # Cap the frame rate
        clock.tick(FPS)

    # Quit pygame
    pygame.quit()
    sys.exit()
