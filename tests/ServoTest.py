from time import sleep
import RPi.GPIO as GPIO
import cv2
import numpy as np


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)



pan = 27
tilt = 17

GPIO.setup(tilt, GPIO.OUT) # white => TILT
GPIO.setup(pan, GPIO.OUT) # gray ==> PAN
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def setServoAngle(servo, angle):
	#assert angle >=30 and angle <= 150
	pwm = GPIO.PWM(servo, 50)
	pwm.start(8)
	dutyCycle = angle / 18. + 3.
	pwm.ChangeDutyCycle(dutyCycle)
	sleep(0.3)
	pwm.stop()

if __name__ == '__main__':  
    angle = 0
    while True:
        
        buttonState = GPIO.input(2)
        if buttonState == False:
            print("here")
            setServoAngle(pan, angle)
            setServoAngle(tilt, angle)
            if angle <= 150:
                angle += 10
            else:
                angle -= 10;
        #setServoAngle(tilt, 30)
        #setServoAngle(tilt, 30)
    #if button == GPIO.HIGH:
        #setServoAngle(pan, 15)
        #setServoAngle(tilt, 30)
        #print("pushed")
    
    #setServoAngle(pan, 100)
    #setServoAngle(tilt, 90)    
    GPIO.cleanup()