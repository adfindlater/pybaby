from sensor import BMP180
from collections import namedtuple

bmp = BMP180(1, 0x77)
temperature = namedtuple("Temperature", "C F K")


def read_bmp180_sensor(msl=1019.303):
    pressure, temp = bmp.all()
    altitude = pressure.altitude(msl=msl)
    temp = temperature(
        round(temp.C, 1),
        round(temp.F, 1),
        round(temp.K, 1),
    )
    return pressure, temp, altitude
