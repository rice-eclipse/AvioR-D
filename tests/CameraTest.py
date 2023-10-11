import cv2

#tracker = cv2.legacy.TrackerMOSSE.create()
video = cv2.VideoCapture(0)

ok, frame = video.read()
#bbox = cv2.selectROI(frame)
#ok = tracker.init(frame, bbox)

while True:
	ok, frame = video.read()

	cv2.imshow('frame', frame)
	#ok, bbox = tracker.update(frame)
	#if ok:
		#p1 = (int(bbox[0]), int(bbox[1]))
		#p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
		#cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
		#print(True, bbox)
		#cv2.imshow('frame', frame)
	if cv2.waitKey(1) & 0xFF == 27:
		break
video.release()
cv2.destroyAllWindows()
