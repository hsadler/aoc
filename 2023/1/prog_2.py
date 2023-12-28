import sys
sys.path.append('..')

from helpers import functions

# read each line
# find all string versions of integers and save their index (ex: "two")
# find all characters that are integers and save their index (ex: "2")
# find and assign the first and last integers found
# compose first and last integers to resulting line value (ex: "2" + "4" -> 24)
# sum all line values

total: int = 0

integer_map: dict[str, int] = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five':5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}

with open('input.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        
        # print(line)
        
        # variable to save all string or integer ocurring integers as a int->index map
        index_to_int: dict[int, int] = {}

        # find all string versions of integers and save their index
        for s_int in integer_map.keys():
            first_found_index = functions.find_first_substring_index(line, s_int)
            if first_found_index is not None:
                index_to_int[first_found_index] = integer_map[s_int]
            last_found_index = functions.find_last_substring_index(line, s_int)
            if last_found_index is not None:
                index_to_int[last_found_index] = integer_map[s_int]
        
        # find all characters that are integers and save their index
        for index, character in enumerate(line):
            if character.isdigit():
                index_to_int[index] = int(character)
        
        # print(index_to_int)

        # find and assign the first and last integers found
        min_index: int = min(index_to_int.keys())
        max_index: int = max(index_to_int.keys())
        first_int: int = index_to_int[min_index]
        last_int: int = index_to_int[max_index]

        # compose first and last integers to resulting line value
        line_value: int = int(str(first_int) + str(last_int))

        # print(f"line value: {line_value}")
    
        total += line_value

print(total)
