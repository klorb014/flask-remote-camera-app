import cv2
from enum import Enum
from exceptions import CameraFeedException, DeviceNameException

class Resolution(Enum):
    DEFAULT = 1
    MEDIUM = 2
    LOW = 3

class Camera:
    def __init__(self, device_name: str):
        try:
            self.device_name = device_name
            self.camera_index = int(device_name[7:])
            self.resolution = Resolution.DEFAULT
            self.rgb = True
            self.is_open = False
            self.feed = None
        except ValueError:
            raise DeviceNameException("Expected syntax: camera-<<index>>")

    def __repr__(self):
        return "Camera(%s, Resolution: %s, RGB: %s)" % (self.device_name, self.resolution, self.rgb)

    def __eq__(self, other):
        if isinstance(other, Camera):
            return self.camera_index == other.camera_index
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return self.camera_index

    def change_feed_resolution(self):
        if self.resolution is not Resolution.DEFAULT:
            if self.resolution is Resolution.MEDIUM:
                self.feed.set(3, 640)
                self.feed.set(4, 480)
            else:
                self.feed.set(3, 256)
                self.feed.set(4, 256)
    
    def open_feed(self):
        if self.feed is None:
            self.feed = cv2.VideoCapture(self.camera_index)
            if self.feed.read()[0]:
                self.is_open = True
                self.change_feed_resolution()
                return True
        else:
            raise CameraFeedException(str(self) + " camera feed is already open")
        return False
    
    def close_feed(self):
        if self.feed is not None:
            self.feed.release()
            self.feed = None
            self.is_open = False
        else:
            raise CameraFeedException(str(self) + " camera feed is already closed")

    def set_resolution(self, resolution: Resolution):
        self.resolution = resolution
    
    def set_colour(self, rgb: bool):
        self.rgb = rgb