import cv2
from pybaby.models.base_camera import BaseCamera

capture = cv2.VideoCapture("tcp://0.0.0.0:8080")


class TCPCamera(BaseCamera):
    @staticmethod
    def frames():
        while True:
            ret, frame = capture.read()
            yield frame
