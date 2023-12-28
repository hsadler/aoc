import sys
sys.path.append('..')

from helpers import functions

class Point:
    x: int
    y: int
    val: str
    color: str = functions.Colors.WHITE
    def __init__(self, x: int, y: int, val: str):
        self.x = x
        self.y = y
        self.val = val
    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.val})"

class Grid:
    grid: dict[str, Point]  = {}
    @classmethod
    def build(cls):
        grid = cls()
        with open("input.txt", "r") as f:
            lines = f.readlines()
            for y, l in enumerate(lines):
                for x, c in enumerate(l):
                    p = Point(x, y, c)
                    grid.add(p)
        return grid
    def add(self, p: Point):
        self.grid[functions.serialize_position(p.x, p.y)] = p
    def get_points(self) -> list[Point]:
        return list(self.grid.values())
    def get(self, x: int, y: int) -> Point | None:
        return self.grid.get(functions.serialize_position(x, y))
    def get_neighbor(self, p: Point, direction: str) -> Point | None:
        if direction == "up":
            return self.get(p.x, p.y - 1)
        elif direction == "down":
            return self.get(p.x, p.y + 1)
        elif direction == "left":
            return self.get(p.x - 1, p.y)
        elif direction == "right":
            return self.get(p.x + 1, p.y)
        else:
            raise Exception(f"Invalid direction: {direction}")
    def get_neighbors(self, p: Point) -> list[Point]:
        neighbors = []
        for x in range(p.x - 1, p.x + 2):
            for y in range(p.y - 1, p.y + 2):
                if x == p.x and y == p.y:
                    continue
                neighbors.append(self.get(x, y))
        return [n for n in neighbors if n is not None]
    def print(self):
        for p in self.get_points():
            print(functions.get_color_string(p.color, p.val), end="")
    def get_first_int_points(self) -> list[Point]:
        def point_is_first_int(p: Point) -> bool:
            left_neighbor = self.get_neighbor(p, "left")
            return p.val.isdigit() \
                and (left_neighbor is None or not left_neighbor.val.isdigit())
        return [p for p in self.get_points() if point_is_first_int(p)]
    def get_number_points_from_point(self, p: Point) -> list[Point]:
        points = [p]
        curr_point = p
        while True:
            curr_point = self.get_neighbor(curr_point, "right")
            if curr_point is None:
                break
            if curr_point.val.isdigit():
                points.append(curr_point)
            else:
                break
        curr_point = p
        while True:
            curr_point = self.get_neighbor(curr_point, "left")
            if curr_point is None:
                break
            if curr_point.val.isdigit():
                points.append(curr_point)
            else:
                break
        points.sort(key=lambda p: p.x)
        return points
    @classmethod
    def filter_points(cls, points: list[Point], f: callable) -> list[Point]:
        return [p for p in points if f(p)]

# first problem
if True:
    grid = Grid.build()
    nums_to_sum = []
    for p in grid.get_first_int_points():
        def number_points_are_valid(number_points: list[Point]) -> bool:
            for n in number_points:
                neighbors = grid.get_neighbors(n)
                for nb in neighbors:
                    if nb.val != "." and nb.val != "\n" and not nb.val.isdigit():
                        return True
            # print(f"Invalid number: {number}")
            return False
        number_points = grid.get_number_points_from_point(p)
        number = int("".join([n.val for n in number_points]))
        if number_points_are_valid(number_points):
            for n in number_points:
                n.color = functions.Colors.GREEN
            nums_to_sum.append(number)
        else:
            for n in number_points:
                n.color = functions.Colors.RED
    grid.print()
    print('\n')
    print(sum(nums_to_sum))

# second problem
if True:
    nums_to_sum = []
    grid = Grid.build()
    gears = Grid.filter_points(grid.get_points(), lambda p: p.val == "*")
    for p in gears:
        p.color = functions.Colors.RED
        number_neighbors = Grid.filter_points(grid.get_neighbors(p), lambda n: n.val.isdigit())
        coord_to_number_points = {} # for deduplication
        for n in number_neighbors:
            number_points = grid.get_number_points_from_point(n)
            for np in number_points:
                np.color = functions.Colors.GREEN
            n.color = functions.Colors.YELLOW
            first_number_point = number_points[0]
            coord_to_number_points[functions.serialize_position(first_number_point.x, first_number_point.y)] = number_points
        nums_to_product = []
        for number_points in coord_to_number_points.values():
            number = int("".join([n.val for n in number_points]))
            nums_to_product.append(number)
        if len(nums_to_product) == 2:
            nums_to_sum.append(nums_to_product[0] * nums_to_product[1])            
    grid.print()
    print('\n')
    print(sum(nums_to_sum))