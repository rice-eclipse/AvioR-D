import cv2

# create tracker just for fun

# reading video
video = cv2.VideoCapture(0)

# reading first frame
ok, frame = video.read()


# set output video
frame_height, frame_width = frame.shape[:2]


while True:
    # reading new frame
    ok, frame = video.read()

    if not ok:
        print("End of the video")
        break

    cv2.imshow("MOSSE Tracking but without the tracking", frame)

    k = cv2.waitKey(2) & 0xff
    if k == 27:
        break

video.release()
cv2.destroyAllWindows()
