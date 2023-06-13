import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

x_vals = list(range(1,193,1))
print(x_vals)
X=[100]
y_vals = len(x_vals)*X

index = count()


def animate(i):
    i=0
    while i<=len(x_vals)-1:
        y_vals[i] = y_vals[i]+random.uniform(-10,10)
        i+=1

    plt.cla()

    plt.bar(x_vals, y_vals, label='Channel 1')
    

    plt.legend(loc='upper left')
    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()