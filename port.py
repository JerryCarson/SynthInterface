import matplotlib.pyplot as plt
import serial  # requires pip install pyserial
import numpy as np


class SerialWrite:
    def __init__(self, com, baud, file, app):
        self.serial_port = com
        self.baud_rate = baud
        self.bytesize = serial.EIGHTBITS
        self.read_file_path = file
        self.app = app

    def comWrite(self):
        read_file_path = "input.txt"
        # with serial.Serial(self.serial_port, self.baud_rate, self.bytesize, timeout = 0) as ardu: #opens and automatically closes COM port after use
        #     ardu.write(bytes((32768>>8)&0b11111111))
        #     ardu.write(bytes(32768&0b11111111))
        #     with open(read_file_path, "r") as input_file:
        #         for line in input_file:
        #             ardu.write(bytes(int(line.strip())))
        #     ardu.write(bytes((31744>>8)&0b11111111))
        #     ardu.write(bytes(31744&0b11111111))
        with open(self.read_file_path, "r") as input, open(
            "output.txt", "w"
        ) as output:
            for line in input:
                output.write(line)

    def comWriteField(self):
        with open("output.txt", "w+") as output:
            for line in self.app.getTextArea("t1"):
                output.write(line)
