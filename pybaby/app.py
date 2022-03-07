from flask import Flask, Response
from pybaby.models.tcp_camera import TCPCamera
from pybaby.utils import measure_fps
from pybaby.sensors.dht11_temp_module import read_dht11_sensor
from pybaby.sensors.bmp180_pressure_module import read_bmp180_sensor
from pybaby.sensors.daoki_sound_module import DaokiSoundSensor
from datetime import datetime
from collections import namedtuple
import cv2


app = Flask(__name__)
cam = TCPCamera()
sound = DaokiSoundSensor()


def generate(cam):
    frame = cam.get_frame()
    fps = 1
    n_frames = 1

    # image_data = image(fps, *frame.shape)    
    # time_last = cam.last_access
    # pressure, temp, alt = read_bmp180_sensor()
    # humidity = read_dht11_sensor()
    # datetime_now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    # has_sound = False

    time_last = 0
    n_frames = 0

    while True:
        frame = cam.get_frame()

        if (cam.last_access - time_last) > 2.5:
            image_data, time_last = measure_fps(cam.last_access, time_last, n_frames, *frame.shape)
            pressure, temp, alt = read_bmp180_sensor()
            humidity = read_dht11_sensor()
            has_sound = sound.poll()
            datetime_now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")            
            n_frames = 0

        cv2.putText(frame, f"PyBaby v1.0.0 {datetime_now}", (6,15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, f"{temp}", (6,31), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, f"{pressure}", (6,47), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, f"Altitude(m={round(alt.m, 1)}, ft={round(alt.ft, 1)})", (6,63), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, f"{image_data}", (6,81), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, f"{humidity}", (6,98), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        if has_sound:
            cv2.putText(frame, f"SOUND DETECTED", (6, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)
        
        (flag, encodedImage) = cv2.imencode(".jpg", frame)

        yield (
            b"--frame\r\n" +
            b"Content-Type: image/jpeg\r\n\r\n"
            + bytearray(encodedImage)
            + b"\r\n"
        )

        n_frames += 1

@app.route("/")
def video_feed():
    return Response(
        generate(cam), mimetype="multipart/x-mixed-replace; boundary=frame"
    )

if __name__ == "__main__":
    app.run(port=5001, host="0.0.0.0", threaded=True, use_reloader=False)
