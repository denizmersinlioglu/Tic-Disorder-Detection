import serial, re
from collections import deque


class SerialPlot:
    # constr
    def __init__(self, strPort, maxLen):
        # open serial port
        self.ser = serial.Serial(port=strPort, baudrate=9600)

        self.accel_x = deque([0.0] * maxLen)
        self.accel_y = deque([0.0] * maxLen)
        self.accel_z = deque([0.0] * maxLen)
        self.gyro_x = deque([0.0] * maxLen)
        self.gyro_y = deque([0.0] * maxLen)
        self.gyro_z = deque([0.0] * maxLen)
        self.maxLen = maxLen

    # add to buffer
    def addToBuf(self, buf, val):
        if len(buf) < self.maxLen:
            buf.append(val)
        else:
            buf.pop()
            buf.appendleft(val)

    # add data
    def add(self, data):
        assert (len(data) == 6)
        self.addToBuf(self.accel_x, data[0])
        self.addToBuf(self.accel_y, data[1])
        self.addToBuf(self.accel_z, data[2])
        self.addToBuf(self.gyro_x, data[3])
        self.addToBuf(self.gyro_y, data[4])
        self.addToBuf(self.gyro_z, data[5])

    # update plot
    def update(self, frameNum, a0, a1, a2, a3, a4, a5):
        try:
            line = self.ser.readline()
            data_str = re.findall(r"[-+]?\d*\.\d+|\d+", str(line))
            data = [float(val) for val in data_str]
            if (len(data) == 6):
                self.add(data)
                a0.set_data(range(self.maxLen), self.accel_x)
                a1.set_data(range(self.maxLen), self.accel_y)
                a2.set_data(range(self.maxLen), self.accel_z)
                a3.set_data(range(self.maxLen), self.gyro_x)
                a4.set_data(range(self.maxLen), self.gyro_y)
                a5.set_data(range(self.maxLen), self.gyro_z)
            else:
                print("Update doesn't used")
        except KeyboardInterrupt:
            print('exiting')

        return a0,

    # clean up
    def close(self):
        # close serial
        self.ser.flush()
        self.ser.close()
