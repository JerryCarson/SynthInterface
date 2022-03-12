import numpy as np

def sine(app):
    with open("input.txt", "w+") as input:
        for i in range (0, 2*np.pi(), 0.01*np.pi()):
            input.write(np.sin(i))

