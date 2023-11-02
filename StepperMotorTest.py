import RPi.GPIO as GPIO

# import the library
from RpiMotorLib import RpiMotorLib

# define GPIO pins
GPIO_pins = (14, 15, 18) # Microstep Resolution MS1-MS3 -> GPIO Pin
step = 38      # Step -> GPIO Pin
direction = 40       # Direction -> GPIO Pin

# Declare an named instance of class pass GPIO pins numbers
mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")


# call the function, pass the arguments
mymotortest.motor_go(False, "Full" , 200, .01, False, .01)
