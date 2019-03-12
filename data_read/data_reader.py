import serial
import serial.rfc2217
import serial.tools.list_ports
import re
# import matplotlib.pyplot as plt

serialport = serial.Serial(port='/dev/cu.SLAB_USBtoUART', baudrate=9600)

while True:
    command = serialport.readline()
    str_command = str(command)
    parameters = re.findall("\d+\.\d+", str_command)
    print(parameters)
