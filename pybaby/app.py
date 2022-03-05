from flask import Flask, Response
from pybaby.models.tcp_camera import TCPCamera
from datetime import datetime
from sensor import BMP180
import cv2
from collections import namedtuple
            
app = Flask(__name__)
cam = TCPCamera()
bmp = BMP180(1, 0x77)

def generate(cam):
    frame = cam.get_frame()
    time_last = cam.last_access
    temp = namedtuple('Temperature', 'C F K')
    image = namedtuple('Image', 'FPS H W C')
    pressure_last, temp_last_0 = bmp.all()  # read both at once
    temp_last = temp(
        round(temp_last_0.C, 1),
        round(temp_last_0.F, 1),
        round(temp_last_0.K, 1),
    )
    datetime_last = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    alt_last = pressure_last.altitude(msl=1019.303)
    fps_last = 1
    n_frames = 1
    image_last = image(fps_last, *frame.shape)
    while True:
        frame = cam.get_frame()

        if (cam.last_access - time_last) > 10.0:
            time_current = cam.last_access
            fps_last = int(float(n_frames) / (time_current - time_last))
            time_last = time_current
            image_last = image(fps_last, *frame.shape)
            pressure_last, temp_last_0 = bmp.all()  # read both at once
            temp_last = temp(
                round(temp_last_0.C, 1),
                round(temp_last_0.F, 1),
                round(temp_last_0.K, 1),
            )
            datetime_last = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            alt_last = pressure_last.altitude(msl=1019.303)
            n_frames = 0

        cv2.putText(frame, f"{datetime_last}", (6,15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, f"{temp_last}", (6,31), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, f"{pressure_last}", (6,47), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, f"Altitude(m={round(alt_last.m, 1)}, ft={round(alt_last.ft, 1)})", (6,63), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, f"{image_last}", (6,81), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        
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
