import argparse
import time
from time import sleep
import cv2
import numpy as np
import threading
from flask import Response
from flask import Flask
from flask import render_template
import sys

outputFrameMask = None
outputFrameRaw = None
lock = threading.Lock()

# initialize a flask object
app = Flask(__name__, static_folder="static")


@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")


@app.route("/video_feed_mask")
def video_feed_mask():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate_mask_mask(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/video_feed_raw")
def video_feed_raw():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate_mask_raw(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


pan_id = 27
tilt_id = 17
button_id = 2
cap = cv2.VideoCapture(0)





def generate_mask_mask():
    # grab global references to the output frame and lock variables
    global outputFrameMask, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrameMask is None:
                continue

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrameMask)
            # print(flag)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')
        time.sleep(0.04)

def generate_mask_raw():
    # grab global references to the output frame and lock variables
    global outputFrameRaw, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrameRaw is None:
                continue

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrameRaw)
            # print(flag)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')
        time.sleep(0.04)

def detect_motion():
    global outputFrameMask, outputFrameRaw

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

        with lock:
            if frame is not None:
                outputFrameRaw = frame.copy()

        # Comment / uncomment if camera needs to be flipped based on mount orentation
        # frame = cv2.flip(frame, -1)  # Flip camera vertically
        blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        lower_range = np.array([35, 110, 40], dtype=np.uint8)
        upper_range = np.array([85, 180, 130], dtype=np.uint8)
        #
        # # create a mask for image
        mask = cv2.inRange(hsv, lower_range, upper_range)

        # display both the mask and the image side-by-side
        with lock:
            if mask is not None:
                outputFrameMask = mask.copy()

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
    t = threading.Thread(target=detect_motion)
    t.daemon = True
    t.start()

    def run():
        app.run(host=args["ip"], port=args["port"], debug=True,
                threaded=True, use_reloader=False)

    # t2 = threading.Thread(target=run)
    # t2.daemon = True
    # t2.start()
    run()


    angle = 0


