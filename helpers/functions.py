
def find_first_substring_index(s: str, sub: str) -> int | None:
    try:
        return s.index(sub)
    except ValueError:
        return None

def find_last_substring_index(s: str, sub: str) -> int | None:
    for start in reversed(range(0, len(s))):
        try:
            return s.index(sub, start)
        except ValueError:
            continue
    return None

def serialize_position(x: int, y: int) -> str:
    return f"{x},{y}"

class Colors:
    RESET = '\033[0m'
    BLACK = '\033[30m'
    WHITE = '\033[97m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    GRAY = '\033[90m'
    DARK_RED = '\033[31m'
    DARK_GREEN = '\033[32m'
    DARK_BLUE = '\033[34m'

def get_color_string(color: str, s: str):
    return f"{color}{s}{Colors.RESET}"

def reduce_color_opacity(color: tuple[int, int, int, int], new_opacity: float) -> tuple[int, int, int, int]:
    return (color[0], color[1], color[2], new_opacity)

def chunk_list(input_list, chunk_size) -> list[list]:
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

def sort_list(original_list, compare: callable) -> list:
    sorted_list = original_list.copy()
    n = len(sorted_list)
    for i in range(n):
        for j in range(0, n-i-1):
            current, next_item = sorted_list[j], sorted_list[j+1]
            if compare(current, next_item) == 1:
                sorted_list[j], sorted_list[j+1] = sorted_list[j+1], sorted_list[j]
    return sorted_list

def test_sort_list():
    original_list = [1, 3, 2, 5, 4]
    def compare(x, y):
        return x > y
    sorted_list = sort_list(original_list, compare=compare)
    assert sorted_list == [1, 2, 3, 4, 5]

def rotate_matrix(matrix):
    transposed_matrix = list(map(list, zip(*matrix)))
    rotated_matrix = [row[::-1] for row in transposed_matrix]
    return rotated_matrix
