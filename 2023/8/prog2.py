import math

cycles = [19631, 13771, 21389, 17287, 23147, 20803]
lcm = math.lcm(*cycles)
print(f"lcm: {lcm}")

print(f"doubled lcm: {lcm*2}")

for c in cycles:
    print(f"lcm % c: {lcm % c}")
