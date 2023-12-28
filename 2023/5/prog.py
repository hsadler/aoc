import sys
sys.path.append('..')

import json
import random
from enum import Enum
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from helpers import functions


class MapName(Enum):
    SEED_TO_SOIL = "seed-to-soil"
    SOIL_TO_FERTILIZER = "soil-to-fertilizer"
    FERTILIZER_TO_WATER = "fertilizer-to-water"
    WATER_TO_LIGHT = "water-to-light"
    LIGHT_TO_TEMPERATURE = "light-to-temperature"
    TEMPERATURE_TO_HUMIDITY = "temperature-to-humidity"
    HUMIDITY_TO_LOCATION = "humidity-to-location"

def parse_int_string(s: str) -> list[int]:
    return [int(x) for x in s.split()]

def parse_seeds(s: str) -> list[int]:
    seeds = []
    ids = s.split(":")[-1].strip().split()
    for id in ids:
        seeds.append(int(id))
    return seeds

# parse
seeds: list[int] = []
map_to_ids: dict[str, list[int]] = {
    MapName.SEED_TO_SOIL.value: [],
    MapName.SOIL_TO_FERTILIZER.value: [],
    MapName.FERTILIZER_TO_WATER.value: [],
    MapName.WATER_TO_LIGHT.value: [],
    MapName.LIGHT_TO_TEMPERATURE.value: [],
    MapName.TEMPERATURE_TO_HUMIDITY.value: [],
    MapName.HUMIDITY_TO_LOCATION.value: []
}
map_order: list[str] = [
    MapName.SEED_TO_SOIL.value,
    MapName.SOIL_TO_FERTILIZER.value,
    MapName.FERTILIZER_TO_WATER.value,
    MapName.WATER_TO_LIGHT.value,
    MapName.LIGHT_TO_TEMPERATURE.value,
    MapName.TEMPERATURE_TO_HUMIDITY.value,
    MapName.HUMIDITY_TO_LOCATION.value
]
def parse_map_ids(lines: list[str]) -> list[list[int]]:
    id_lists: list[list[str]] = []
    for line in lines:
        id_lists.append([int(n) for n in line.split()])
    return id_lists
with open("input.txt", "r") as f:
    contents = f.read()
    parts = contents.split("\n\n")
    for part in parts:
        if part.startswith("seeds:"):
            seeds = parse_seeds(part)
        else:
            lines = part.split("\n")
            raw_map_name = lines[0]
            for mn in map_to_ids.keys():
                if mn in raw_map_name:
                    map_to_ids[mn] = parse_map_ids(lines[1:])
# print(seeds)
# print(json.dumps(map_to_ids, indent=4))

# mapper
def do_mapping(input: int, maps: list[list[int]]) -> tuple[int, list[int]]:
    curr_id = input
    last_map = None
    for i, m in enumerate(maps):
        if curr_id in range(m[1], m[1] + m[2]):
            curr_id += m[0] - m[1]
            last_map = m
            break
    return curr_id, last_map

# test mapping logic
def test_do_mapping():
    inputs = [79, 14, 55, 13]
    expected_outputs = [81, 14, 57, 13]
    maps = [
        [50, 98, 2], 
        [52, 50, 48]
    ]
    for i, input in enumerate(inputs):
        output, _ = do_mapping(input, maps)
        expected_output = expected_outputs[i]
        if output != expected_output:
            raise Exception(f"test_do_mapping failed: {input} -> {output}, expected: {expected_output}")
test_do_mapping()

# map all seeds to resulting values
def proc_seeds(seeds: list[int]) -> dict[int, int]:
    for seed in seeds:
        if seed in seed_to_final_value:
            continue
        # print(f"mapping seed: {seed}")
        curr_id = seed
        for map_name in map_order:
            # print(f"doing mapping for: {map_name}, id: {curr_id}")
            curr_id, _ = do_mapping(curr_id, map_to_ids[map_name])
        seed_to_final_value[seed] = curr_id
        # print(f"final id: {curr_id}")
        # print("----")
    return seed_to_final_value


seed_to_final_value: dict[int, int] = {}
seed_to_final_value = proc_seeds(seeds)
print("seed to final value: ", json.dumps(seed_to_final_value, indent=4))
print("min final value: ", min(seed_to_final_value.values()))

print("----")

@dataclass
class Min:
    val: int
    seed_range_num: int = 0
    last_map: list[int] = None
def proc_seeds_2(seeds: list[int]) -> Min:
    m = Min(float("inf"))
    for seed in seeds:
        curr_id = seed
        for map_name in map_order:
            curr_id, last_map = do_mapping(curr_id, map_to_ids[map_name])
        if curr_id < m.val:
            m.val = curr_id
            m.seed_range_num = 0
            m.last_map = last_map
    print(m.val)
    return m

print("seeds: ", seeds)
min_final = Min(float("inf"))
for i, seed in enumerate(seeds):
    if i % 2 != 0:
        range_num = int(i/2)
        # range 6 was identified as the range with the lowest min final value
        if range_num != 6:
            continue
        start = seeds[i-1]
        delta = seed
        seed_range = range(start, start + delta)
        sample_size = int(0.1 * len(seed_range))
        SAMPLED = False
        if SAMPLED:
            sampled_seed_range = random.sample(seed_range, sample_size)
        else:
            sampled_seed_range = seed_range
        chunked_seed_range = functions.chunk_list(sampled_seed_range, 100000)
        chunk_count = 0
        total_chunks = len(chunked_seed_range)
        THREADED = True
        if THREADED:
            with ThreadPoolExecutor(max_workers=100) as executor:
                result = list(executor.map(proc_seeds_2, chunked_seed_range))
                for m in result:
                    if m.val < min_final.val:
                        min_final = m
        else:
            for seed_chunk in chunked_seed_range:
                chunk_count += 1
                proc_seeds_2(seed_chunk, range_num)
                print(f"chunk {chunk_count}/{total_chunks} done. min: {m.val}. seed range num: {m.seed_range_num}. last map: {m.last_map}.")
print("min final value: ", min_final.val)
