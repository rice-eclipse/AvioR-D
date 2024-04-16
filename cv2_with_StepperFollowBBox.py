import cv2
import sys
import serial
import time

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
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
        print(True)
        array = "0"
        print(array)
        arduino.write(array)
    if bot == 0:
        print(True)
        array = "1"
        print(array)
        arduino.write(array)
    if left == 0:
        print(True)
        array = "2"
        print(array)
        arduino.write(array)
    if right == frame[0]:
        print(True)
        array = "3"
        print(array)
        arduino.write(array)

    print(False)
    #stepperPos = arduino.readline()
    #return stepperPos


#intialize tracker
tracker = cv2.legacy.TrackerMOSSE.create()
print(tracker)

#read video
video = cv2.VideoCapture("SpaceX.mp4")
if not video.isOpened():
    print("cannot open video")
    sys.exit()

#read first frame
ok, frame = video.read()
if not ok:
    print("cannot read video")
    sys.exit()

#instantiating boundary box
bbox = cv2.selectROI(frame)

ok = tracker.init(frame, bbox)

fps = int(video.get(cv2.CAP_PROP_FPS))

while True:
    #read to new frame
    ok, frame = video.read()
    if not ok:
        break

    #update tracker
    ok, bbox = tracker.update(frame)

    if ok:
        #drawing new boudnary box
        p1 = (int(bbox[0]),int(bbox[1]))
        p2 = (int(bbox[0]+bbox[2]),int(bbox[1]+bbox[3]))
        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        StepperFollowBBox([int(bbox[0]),int(bbox[1]), int(bbox[2]),int(bbox[3])], (50,50))
    else:
        print("tracking failed")

    cv2.putText(frame, "MOSSE tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255))
    cv2.putText(frame, "FPS " + str(fps), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255))

    #display results
    cv2.imshow("tracking",frame)

    #exit if ESC is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

video.release()
cv2.destroyWindow()