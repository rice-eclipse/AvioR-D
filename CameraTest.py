import cv2
import numpy as np

video = cv2.VideoCapture(0)

# Create MultiTracker object
trackers = cv2.legacy.MultiTracker_create()

while True:
    frame = video.read()[1]
    if frame is None: break
    # frame = cv2.resize(frame,(1090,600))

    ok, boxes = trackers.update(frame)
    print(ok,boxes)
    # loop over the bounding boxes and draw then on the frame
    if not ok:
        bboxes = trackers.getObjects()
        idx = np.where(bboxes.sum(axis= 1) != 0)[0]
        bboxes = bboxes[idx]
        trackers = cv2.legacy.MultiTracker_create()
        for bbox in bboxes:
            trackers.add(tracker,frame,bbox)

    for i,box in enumerate(boxes):
        (x, y, w, h) = [int(v) for v in box]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame,'TRACKING',(x+10,y-3),cv2.FONT_HERSHEY_PLAIN,1.5,(255,255,0),2)

    cv2.imshow('Frame', frame)
    k = cv2.waitKey(1)

    if k == ord("s"):
        # select the bounding box of the object we want to track (make
        # sure you press ENTER or SPACE after selecting the ROI)
        roi = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
        # create a new object tracker for the bounding box and add it
        # to our multi-object tracker
        tracker = cv2.legacy.TrackerMOSSE_create()
        trackers.add(tracker, frame, roi)

    # press q to end
    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()