import threading

import cv2

from tools import Color
from tracking import Frame, MaskVariant, Mask
import time


class Detection:
    def __init__(self, cam, lock, output_frames, tracking_config):
        """
        Create detection system.
        :param cam: singleton camera.
        :param lock: singleton lock.
        :param output_frames: singleton output frames list.
        :param tracking_config: tracking configuration from TrackingConfig.
        """
        self.boundary_box = None
        self.cam = cam
        self.lock = lock
        self.output_frames = output_frames
        self.tracker = tracking_config.model()
        self.mask_updater = Mask(tracking_config.color,
                                 tracking_config.thickness,
                                 MaskVariant(tracking_config.mask_variant))
        self.cam_lock = False

    def set_tracking_display(self, display):
        """
        Set tracking display from string.
        :param display: string that is a value of MaskVariant.
        :return:
        """
        self.mask_updater.variant = MaskVariant(display)

    def set_tracking_color(self, color):
        """
        Set tracking color.
        :param color: color as hex string.
        :return:
        """
        self.mask_updater.color = Color.from_hex(color)

    def set_tracking_thickness(self, thickness):
        """
        Set tracking thickness.
        :param thickness: integer as tracking thickness.
        :return:
        """
        self.mask_updater.thickness = thickness

    def create_worker(self):
        """
        Create motion tracking worker on a thread.
        :return:
        """
        t = threading.Thread(target=self._update_motion_tracking)
        t.daemon = True
        t.start()

    def _update_motion_tracking(self):
        """
        Infinite motion tracking process loop.
        :return:
        """

        while True:
            ret, frame = self.cam.read()

            with self.lock:
                if (frame is not None) and (not self.cam_lock):
                    self.output_frames[Frame.RAW.value] = frame.copy()

            # Comment / uncomment if camera needs to be flipped based on mount orentation
            # frame = cv2.flip(frame, -1)  # Flip camera vertically
            # blurred = cv2.GaussianBlur(frame, (5, 5), 0)
            # hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            # #
            # # # create a mask for image
            # mask = cv2.inRange(hsv, lower_range, upper_range)
            mask = frame.copy()

            if self.boundary_box is not None:
                _, tracking_box = self.tracker.update(frame)
                mask = self.mask_updater.update_mask(mask, tracking_box)

            # display both the mask and the image side-by-side
            with self.lock:
                if (mask is not None) and (not self.cam_lock):
                    self.output_frames[Frame.MASK.value] = mask.copy()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def set_boundary_box(self, bbox):
        """
        Set boundary box of the detection.
        :param bbox: boundary box in form [min x, min y, delta x, delta y]
        :return:
        """
        shape = self.output_frames[Frame.RAW.value].shape
        self.boundary_box = [int(bbox[0] * shape[1]), max(int(bbox[1] * shape[0]), 2),
                             int(bbox[2] * shape[1]), max(int(bbox[3] * shape[0]), 2)]
        self.tracker.clear(self.output_frames[Frame.RAW.value], self.boundary_box)

    def generate(self, frame_type):
        """
        Flask generating method for a frame type.
        :param frame_type: type of frame in form Frame
        :return:
        """
        print(frame_type.value)

        # loop over frames from the output stream
        while True:
            # wait until the lock is acquired
            with self.lock:
                # check if the output frame is available, otherwise skip the iteration of the loop
                if self.output_frames[frame_type.value] is None:
                    continue

                # encode the frame in JPEG format
                (flag, encodedImage) = cv2.imencode(".jpg", self.output_frames[frame_type.value])
                # print(frame_type.value)

                # ensure the frame was successfully encoded
                if not flag:
                    continue

            # yield the output frame in the byte format
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(encodedImage) + b'\r\n')
            time.sleep(0.04)
