import cv2
import logging
from camera import Camera, Resolution
from exceptions import InvalidCameraException, CameraClosedException


class CameraController:
    def __init__(self):
        self.MAX_CONCURRENT_FEEDS = 2 
        self.available_cameras = None
        self.open_cameras = []


    def find_available_cameras(self):
        # checks the first 10 indexes.
        index = 0
        cameras = {}
        i = 10
        while i > 0:
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                device_name = "camera-" + str(index)
                cameras[device_name] = Camera(device_name)
                cap.release()
            index += 1
            i -= 1
        logging.info("Available cameras: " + str(cameras))
        self.available_cameras = cameras

    def close_all_feeds(self):
        for camera in self.open_cameras:
            camera = self.open_cameras.pop(0)
            logging.info("Closing " + str(camera))
            camera.close_feed()

    def switch_cameras(self, device_name: str, resolution: Resolution, rgb: bool):
        logging.info("list of open cameras: " + str(self.open_cameras))
        if device_name in self.available_cameras.keys():
            camera = self.available_cameras[device_name]
            if camera in self.open_cameras:
                logging.warning(str(camera) + "is already open")

            else:
                if len(self.open_cameras) == self.MAX_CONCURRENT_FEEDS:
                    old_camera_feed = self.open_cameras.pop(0)
                    logging.info("Closing " + str(old_camera_feed))
                    old_camera_feed.close_feed()

                logging.info("Opening " + str(camera))
                camera.set_resolution(resolution)
                camera.set_colour(rgb)
                camera.open_feed()
                self.open_cameras.append(camera)
            return True
        else:
            raise InvalidCameraException("Selected camera is not in list of available devices")
        

    def open_feed(self, device_name: str):  # generate frame by frame from camera
        logging.info("list of open cameras: " + str(self.open_cameras))
        camera = self.available_cameras[device_name]
        if camera in self.open_cameras:
            while True:
                # Capture frame-by-frame
                success, frame = camera.feed.read()  # read the camera frame
                if not success:
                    logging.warning("failed to read image from camera")
                    break
                else:
                    if not camera.rgb:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
        else:
            raise CameraClosedException(device_name + " not found in list of open cameras")