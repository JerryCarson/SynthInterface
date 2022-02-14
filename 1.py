import matplotlib.pyplot as plt
import serial  # requires pip install pyserial
import numpy as np

serial_port = "COM19"  # set your COM port value

baud_rate = 9600
# set same as Arduino has
read_file_path = "input.txt"

with serial.Serial(serial_port, baud_rate, timeout = 0) as ardu: #opens and automatically closes COM port after use
    with open(read_file_path, "r") as input_file:
        for line in input_file:
            ardu.write(line.strip())

# data = np.loadtxt('output.txt')
# y = data[:]
# plt.plot(y)
# plt.ylabel('y')
# plt.show()
