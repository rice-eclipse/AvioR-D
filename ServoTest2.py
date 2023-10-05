import argparse
from time import sleep
import RPi.GPIO as GPIO
import cv2
import numpy as np
import threading
from flask import Response
from flask import Flask
from flask import render_template
import sys

outputFrame = None
lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)


@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pan_id = 27
tilt_id = 17
button_id = 2

GPIO.setup(tilt_id, GPIO.OUT)  # white => TILT
GPIO.setup(pan_id, GPIO.OUT)  # gray ==> PAN
GPIO.setup(button_id, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def setServoAngle(servo, angle):
    # assert angle >=30 and angle <= 150
    pwm = GPIO.PWM(servo, 50)
    pwm.start(8)
    dutyCycle = angle / 18. + 3.
    # magic numbers  18. + 3.
    pwm.ChangeDutyCycle(dutyCycle)
    sleep(0.3)
    pwm.stop()


def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')

def detect_motion():
    global outputFrame

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
        # frame = cv2.flip(frame, -1)  # Flip camera vertically
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_range = np.array([0, 50, 0], dtype=np.uint8)
        upper_range = np.array([0, 255, 255], dtype=np.uint8)

        # create a mask for image
        mask = cv2.inRange(hsv, lower_range, upper_range)

        # display both the mask and the image side-by-side
        with lock:
            outputFrame = frame.copy()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
                    help="ephemeral port number of the server (1024 to 65535)")

    args = vars(ap.parse_args())

    # start a thread that will perform motion detection
    t = threading.Thread(target=detect_motion, args=(
        args["frame_count"],))
    t.daemon = True
    t.start()

    # start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True,
            threaded=True, use_reloader=False)


    angle = 0
    cap = cv2.VideoCapture(0)

