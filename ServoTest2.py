from time import sleep
import RPi.GPIO as GPIO
import cv2
import numpy as np
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


pan_id = 27
tilt_id = 17
button_id = 2

GPIO.setup(tilt_id, GPIO.OUT) # white => TILT
GPIO.setup(pan_id, GPIO.OUT) # gray ==> PAN
GPIO.setup(button_id, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def setServoAngle(servo, angle):
        #assert angle >=30 and angle <= 150
        pwm = GPIO.PWM(servo, 50)
        pwm.start(8)
        dutyCycle = angle / 18. + 3.
        # magic numbers  18. + 3.
        pwm.ChangeDutyCycle(dutyCycle)
        sleep(0.3)
        pwm.stop()


if __name__ == '__main__':
    angle = 0
    cap = cv2.VideoCapture(0)

    while True:

        # buttonState = GPIO.input(button_id)
        # print(buttonState)
        # if buttonState == False:
        #     print("not pressed")
        #     setServoAngle(pan_id, 0)
        #     setServoAngle(tilt_id, 0)
        # else:
        #     setServoAngle(pan_id, 15)
        #     setServoAngle(tilt_id, 30)
        #     print("pushed")
        # setServoAngle(tilt_id, 30)

        # cv2 from tutorial HERE
        ret, frame = cap.read()
        # Comment / uncomment if camera needs to be flipped based on mount orentation
        #frame = cv2.flip(frame, -1)  # Flip camera vertically
        blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        lower_range = np.array([35, 110, 40], dtype=np.uint8)
        upper_range = np.array([85, 180, 130], dtype=np.uint8)

        # create a mask for image
        mask = cv2.inRange(hsv, lower_range, upper_range)

        # display both the mask and the image side-by-side
        cv2.imshow('mask', mask)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()

