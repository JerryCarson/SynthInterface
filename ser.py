import matplotlib.pyplot as plt
import serial  # requires pip install pyserial
import numpy as np

class SerialWrite:
    def __init__(self, com, baud, file):
        self.serial_port = com
        self.baud_rate = baud
        self.read_file_path = file
    def comWrite(self):
        # read_file_path = "input.txt"
        # with serial.Serial(self.serial_port, self.baud_rate, timeout = 0) as ardu: #opens and automatically closes COM port after use
        #     with open(read_file_path, "r") as input_file:
        #         for line in input_file:
        #             ardu.write(line.strip())
        with open(self.read_file_path, "r") as input_file, open("output.txt", "w") as output:
            for line in input_file:
                output.write(line)


# data = np.loadtxt('output.txt')
# y = data[:]
# plt.plot(y)
# plt.ylabel('y')
# plt.show()