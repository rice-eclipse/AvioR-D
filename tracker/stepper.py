import serial
import time

arduino = serial.Serial(port='COM7', baudrate=115200, timeout=.1)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

while True:
    num = input("Set: ") # Taking input from user
    arduino.write(bytes(num, 'utf-8'))