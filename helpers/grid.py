import sys
sys.path.append('..')
from enum import Enum

from helpers import functions

class Direction(Enum):
    DIRECTION_UP = "up"
    DIRECTION_DOWN = "down"
    DIRECTION_LEFT = "left"
    DIRECTION_RIGHT = "right"

class Color(Enum):
    BLACK = (0, 0, 0, 255)
    WHITE = (255, 255, 255, 255)
    RED = (255, 0, 0, 255)
    GREEN = (0, 255, 0, 255)
    BLUE = (0, 0, 255, 255)
    YELLOW = (255, 255, 0, 255)
    MAGENTA = (255, 0, 255, 255)
    CYAN = (0, 255, 255, 255)
    GRAY = (128, 128, 128, 255)
    DARK_RED = (128, 0, 0, 255)
    DARK_GREEN = (0, 128, 0, 255)
    DARK_BLUE = (0, 0, 128, 255)

color_map: dict[Color, str] = {
    Color.BLACK: functions.Colors.BLACK,
    Color.WHITE: functions.Colors.WHITE,
    Color.RED: functions.Colors.RED,
    Color.GREEN: functions.Colors.GREEN,
    Color.BLUE: functions.Colors.BLUE,
    Color.YELLOW: functions.Colors.YELLOW,
    Color.MAGENTA: functions.Colors.MAGENTA,
    Color.CYAN: functions.Colors.CYAN,
    Color.GRAY: functions.Colors.GRAY,
    Color.DARK_RED: functions.Colors.DARK_RED,
    Color.DARK_GREEN: functions.Colors.DARK_GREEN,
    Color.DARK_BLUE: functions.Colors.DARK_BLUE,
}

class Point:
    x: int
    y: int
    val: str
    color: Color = Color.GRAY
    color_opacity: float = 1.0
    def __init__(self, x: int, y: int, val: str):
        self.x = x
        self.y = y
        self.val = val
    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.val}), color={self.get_color_as_tuple()}"
    def get_color_as_tuple(self) -> tuple[int, int, int, int]:
        return (self.color.value[0], self.color.value[1], self.color.value[2], 10)

class Grid:
    grid: dict[str, Point]  = {}
    @classmethod
    def build(cls, matrix: list[list[str]]):
        g = cls()
        for y, l in enumerate(matrix):
            for x, c in enumerate(l):
                p = Point(x, y, c)
                g.grid[functions.serialize_position(p.x, p.y)] = p
        return g
    def get_points(self) -> list[Point]:
        return list(self.grid.values())
    def get_point(self, x: int, y: int) -> Point | None:
        return self.grid.get(functions.serialize_position(x, y))
    def get_neighbor(self, p: Point, direction: Direction) -> Point | None:
        if direction == Direction.DIRECTION_UP:
            return self.get_point(p.x, p.y - 1)
        elif direction == Direction.DIRECTION_DOWN:
            return self.get_point(p.x, p.y + 1)
        elif direction == Direction.DIRECTION_LEFT:
            return self.get_point(p.x - 1, p.y)
        elif direction == Direction.DIRECTION_RIGHT:
            return self.get_point(p.x + 1, p.y)
        else:
            raise Exception(f"Invalid direction: {direction}")
    def get_neighbors(self, p: Point, include_diagonals: bool=False) -> list[Point]:
        neighbors = []
        if include_diagonals:
            for x in range(p.x - 1, p.x + 2):
                for y in range(p.y - 1, p.y + 2):
                    if x == p.x and y == p.y:
                        continue
                    neighbors.append(self.get_point(x, y))
        else:
            for direction in Direction:
                neighbors.append(self.get_neighbor(p, direction))
        return [n for n in neighbors if n is not None]
    def get_width(self) -> int:
        return len([p.x for p in self.get_points() if p.x == 0])
    def get_height(self) -> int:
        return len([p.y for p in self.get_points() if p.y == 0])
    def get_column(self, x: int) -> list[Point]:
        return [p for p in self.get_points() if p.x == x]
    def get_row(self, y: int) -> list[Point]:
        return [p for p in self.get_points() if p.y == y]
    def get_print_string(self) -> str:
        print_strings: list[str] = []
        y_to_row: dict[int, list[Point]] = {}
        for p in self.get_points():
            if p.y not in y_to_row:
                y_to_row[p.y] = []
            y_to_row[p.y].append(p)
        curr_y = 0
        while curr_y in y_to_row:
            row = y_to_row[curr_y]
            row.sort(key=lambda p: p.x)
            for p in row:
                print_strings.append(functions.get_color_string(color_map[p.color], p.val))
            print_strings.append("\n")
            curr_y += 1
        return "".join(print_strings)
    @classmethod
    def filter_points(cls, points: list[Point], f: callable) -> list[Point]:
        return [p for p in points if f(p)]
