from abc import abstractmethod
import cv2
from enum import Enum

from tools import Color


class Frame(Enum):
    MASK = 1, "mask"
    RAW = 0, "raw"

    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, label: str = None):
        self._label_ = label
        self._title_ = label.title()
        self._alt_ = f"video of type {label} from camera."
        self._url_ = f"/video_{label}"

    # this makes sure that the description is read-only
    @property
    def label(self):
        return self._label_

    @property
    def alt(self):
        return self._alt_

    @property
    def title(self):
        return self._title_

    @property
    def url(self):
        return self._url_


class Mask:

    def __init__(self, color, thickness, variant):
        """
        Initialize a mask updater.
        :param color: color as hex string.
        """
        self.color = color
        self.thickness = thickness
        self.variant = variant

    @abstractmethod
    def update_mask(self, mask, boundary_box):
        """
        Update mask.
        :param mask: previous mask or image.
        :param boundary_box: boundary box to draw.
        :return: new mask.
        """
        return self.variant.method(mask, boundary_box, self.color.rgb, self.thickness)


def rect_mask(mask, boundary_box, color, thickness):
    """
    Create a rectangular mask on an image.
    :param mask: previous mask.
    :param boundary_box: rectangle to draw.
    :param color: color of rectangle.
    :param thickness: thickness of rectangle.
    :return:
    """
    top_left = (int(boundary_box[0]), int(boundary_box[1]))
    bottom_right = (int(boundary_box[0] + boundary_box[2]), int(boundary_box[1] + boundary_box[3]))
    return cv2.rectangle(mask, top_left, bottom_right, color, thickness)


def circle_mask(mask, boundary_box, color, thickness):
    """
    Create a circular mask on an image.
    :param mask: previous mask.
    :param boundary_box: rectangle to calculate circle from.
    :param color: color of circle.
    :param thickness: thickness of circle.
    :return:
    """
    center = (int(boundary_box[0] + boundary_box[2] / 2),
              int(boundary_box[1] + boundary_box[3] / 2))
    radius = int((boundary_box[2] + boundary_box[3]) / 3)
    return cv2.circle(mask, center, radius, color, thickness)


class MaskVariant(Enum):
    RECT = "rectangle", rect_mask
    CIRCLE = "circle", circle_mask

    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, method: str = None):
        self._method_ = method

    def __str__(self):
        return self.value

    # this makes sure that the description is read-only
    @property
    def method(self):
        return self._method_


class TrackingConfig:
    def __init__(self, data):
        """
        Tracking configuration.
        :param data: parsed python object from config.json.
        """
        self.color = Color.from_hex(data.tracking_color)
        self.thickness = data.tracking_thickness
        self.model = Model(data.tracker).model
        self.mask_variant = MaskVariant(data.mask_updater)


class Tracking:
    @abstractmethod
    def __init__(self):
        """
        Create tracker. Not initialized.
        """
        pass

    @abstractmethod
    def update(self, image):
        """
        Update tracker.
        :param image: current image in the video.
        :return: boundary box of the object.
        """
        pass

    @abstractmethod
    def clear(self, image, boundary_box):
        """
        Clear or initialize the tracker.
        :param image: image in the video when boundary box was taken.
        :param boundary_box: boundary box over the object. Takes form
        (min x, min y, change in x, change in y)
        :return:
        """
        pass


class Mosse(Tracking):

    def __init__(self):
        self.tracker = cv2.legacy.TrackerMOSSE.create()
        self.updater = lambda x: (True, (0, 0, 0, 0))

    def update(self, image):
        return self.updater(image)

    def clear(self, image, boundary_box):
        self.tracker = cv2.legacy.TrackerMOSSE.create()
        self.tracker.init(image, boundary_box)
        self.updater = lambda im: self.tracker.update(im)


class Empty(Tracking):

    def __init__(self):
        self.boundary_box = None
        self.updater = lambda x: (True, (0, 0, 0, 0))

    def update(self, image):
        return self.updater(image)

    def clear(self, image, boundary_box):
        self.boundary_box = boundary_box
        self.updater = lambda x: (True, self.boundary_box)


class Model(Enum):
    RECT = "none", Empty
    CIRCLE = "mosse", Mosse

    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, model: str = None):
        self._model_ = model

    def __str__(self):
        return self.value

    # this makes sure that the description is read-only
    @property
    def model(self):
        return self._model_
