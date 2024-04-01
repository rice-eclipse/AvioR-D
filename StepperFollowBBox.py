import serial
import time

arduino = serial.Serial(port='COM7', baudrate=115200, timeout=.1)
speed = 500


def StepperFollowBBox(bbox, frame):
    """
    Send Serial communication [stepper number, speed] to Arduino to move stepper to follow bbox
    & Return steppers' positions
    :param bbox: list of ints, representing bbox's parameters [left, top, width, height]
    :param frame: tuple of ints, representing frame's dimensions (width, height)
    :return: tuple of ints, representing stepper's position (stepper0, stepper1)
    """
    top = bbox[0]
    left = bbox[1]
    bot = bbox[0]-bbox[2]
    right = bbox[1]-bbox[3]

    if top == frame[1]:
        array = [0,speed]
        arduino.write(array, len(array))
    if bot == 0:
        array = [0, -speed]
        arduino.write(array, len(array))
    if left == 0:
        array = [1, speed]
        arduino.write(array, len(array))
    if right == frame[0]:
        array = [1, -speed]
        arduino.write(array, len(array))

    stepperPos = arduino.readline()
    return stepperPos