import numpy as np
from scipy import signal

def sine(app):
    with open("input.txt", "w+") as input:
        a = np.linspace(0, 2*np.pi, 100)
        for i in range (0, 100):
            input.write(str(np.sin(a[i])))
            input.write("\n")

def square(app):
    with open("input.txt", "w+") as input:
        t = np.linspace(0, 1, 100, endpoint=False)
        a = signal.square(2 * np.pi * 1 * t)
        for i in range (0, 100):
            input.write(str(a[i]))
            input.write("\n")
