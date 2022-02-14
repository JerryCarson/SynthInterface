import matplotlib.pyplot as plt
import serial #requires pip install pyserial
import numpy  as np

serial_port = 'COM19' #set your COM port value

baud_rate = 9600; #set same as Arduino has
write_to_file_path = "output.txt"

with serial.Serial(serial_port, baud_rate, timeout = 0) as ardu: #opens and automatically closes COM port after use
    with open(write_to_file_path, "w") as output_file: #same for output file

        num = input("Enter a number: ") # Taking input from user
        ardu.write(bytes(num, 'utf-8')) #Input -> COM port
        while True:
            # time.sleep(0.01)
            value = ''
            while (value.find('\n') == -1):
                value += ardu.readline().decode('utf-8')
            value = value.strip()
            if (value == 'END'): 
                break
            print(value) # printing the value
            output_file.write(value + '\n')

data = np.loadtxt('output.txt')
y = data[:]
plt.plot(y)
plt.ylabel('y')
plt.show()