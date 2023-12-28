import matplotlib.pyplot as plt
import random

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

plt.plot(x, y)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Matplotlib Example')
plt.show()

while True:
    rand_x = random.choice(x)
    rand_y = random.choice(y)
    plt.scatter(rand_x, rand_y)
    plt.pause(0.2)
