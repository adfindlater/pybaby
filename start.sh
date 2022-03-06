libcamera-vid -t 0 --nopreview 1 --inline --listen -o tcp://0.0.0.0:8080 --width 800 --height 600 --codec mjpeg -q 50 &
python3 -m pybaby.app
