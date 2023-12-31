from dataclasses import dataclass

# Time:        45     98     83     73
# Distance:   295   1734   1278   1210


def problem_1():
    time_to_distance = {45: 295, 98: 1734, 83: 1278, 73: 1210}
    win_list = []
    for time, target_distance in time_to_distance.items():
        # print(f"Time: {time} Target Distance: {target_distance}")
        wins = 0
        for time_held in range(0, time):
            time_going = time - time_held
            speed = time_held
            distance = speed * time_going
            if distance > target_distance:
                wins += 1
                # print(f"Time held: {time_held} Speed: {speed} Distance: {distance}")
        win_list.append(wins)
    product = 1
    for win in win_list:
        product *= win
    print(product)


def problem_2():
    @dataclass
    class Time:
        time: int
        total_time: int
        target_distance: int

        @property
        def distance(self):
            d = self.time * (self.total_time - self.time)
            # print("time", self.time, "distance", d)
            return d

        def __repr__(self):
            return f"time {self.time}, distance from target {self.distance - self.target_distance}"

    total_time = 45988373
    times = list(range(0, total_time))
    target_distance = 295173412781210
    print("target_distance", target_distance)

    # binary search for start of wins
    low_index = 0
    high_index = len(times) - 1
    while low_index <= high_index:
        mid_index = (low_index + high_index) // 2
        curr_sec = times[mid_index]
        curr_time = Time(curr_sec, total_time, target_distance)
        next_sec = times[mid_index + 1]
        next_time = Time(next_sec, total_time, target_distance)
        # print(curr_time.distance - target_distance)
        if (
            curr_time.distance <= target_distance
            and next_time.distance > target_distance
        ):
            print("start of wins found")
            print("current_time", curr_time)
            print("next_time", next_time)
            break  # Target found, return the index
        elif (
            curr_time.distance < target_distance
            and next_time.distance <= target_distance
        ):
            low_index = mid_index + 1  # Target is in the right half
        else:
            high_index = mid_index - 1  # Target is in the left half
    start_of_wins = Time(times[mid_index + 1], total_time, target_distance)

    # binary search for end of wins
    low_index = 0
    high_index = len(times) - 1
    while low_index <= high_index:
        mid_index = (low_index + high_index) // 2
        curr_sec = times[mid_index]
        curr_time = Time(curr_sec, total_time, target_distance)
        next_sec = times[mid_index + 1]
        next_time = Time(next_sec, total_time, target_distance)
        # print(curr_time.distance - target_distance)
        if (
            curr_time.distance > target_distance
            and next_time.distance <= target_distance
        ):
            print("end of wins found")
            print("current_time", curr_time)
            print("next_time", next_time)
            break  # Target found, return the index
        elif (
            curr_time.distance > target_distance
            and next_time.distance > target_distance
        ):
            low_index = mid_index + 1  # Target is in the right half
        else:
            high_index = mid_index - 1  # Target is in the left half
    end_of_wins = Time(times[mid_index], total_time, target_distance)

    print(f"number of wins: {end_of_wins.time - start_of_wins.time}")


problem_1()
print("-------------------")
problem_2()
