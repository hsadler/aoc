# read each line
# pick out the first integer and the last integer and use as a single integer
# OR if a single integer exists, use that twice (ex. 7 -> 77)
# add resulting integers from all lines together and print

total = 0

with open("input.txt", "r") as f:
    lines = f.readlines()
    for l in lines:
        l = l.strip()
        first_int = None
        last_int = None
        # print(l)
        for c in l:
            if c.isdigit():
                if first_int is None:
                    first_int = c
                else:
                    last_int = c
        if last_int is None:
            last_int = first_int
        # print(first_int, last_int)
        line_int = int(first_int + last_int)
        # print(line_int)
        total += line_int

print(total)
