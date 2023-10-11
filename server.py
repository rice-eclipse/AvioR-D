import argparse
import json
import threading
from types import SimpleNamespace

from detection import *
from app import App
from tracking import TrackingConfig, Frame

if __name__ == '__main__':
    # initialize three singleton variables
    output_frames = [None] * len(Frame)
    lock = threading.Lock()
    camera = cv2.VideoCapture(0)

    # terminal arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
                    help="ephemeral port number of the server (1024 to 65535)")
    args = vars(ap.parse_args())

    # load config into python SimpleNamespace object
    with open("config.json") as file:
        config = json.load(file, object_hook=lambda d: SimpleNamespace(**d))

    # start a thread that will perform object tracking
    detection = Detection(camera, lock, output_frames, TrackingConfig(config.website))
    detection.create_worker()

    # start flask app
    app = App(args["ip"], args["port"], detection, config)
    app.start()



