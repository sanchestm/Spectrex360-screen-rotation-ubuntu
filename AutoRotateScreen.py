#!/usr/bin/env python

import subprocess
import time

orientation = ["normal", "inverted", "left", "right"]
statePrev = -1

# Buffer value to increase hysteresis if needed
buffer = 1000000

while True:

    angleX = subprocess.check_output(
             "cat /sys/bus/iio/devices/iio:device*/in_incli_x_raw", shell=True)
    angleY = subprocess.check_output(
             "cat /sys/bus/iio/devices/iio:device*/in_incli_y_raw", shell=True)

    angleX = int(angleX)
    angleY = int(angleY)

    if abs(angleY) > abs(angleX) + buffer:
        if angleY >= 0:
            state = 2
            subprocess.call('/home/thiago/rotatescreenspectre/./portrait.sh')
        else:
            state = 3
            subprocess.call('/home/thiago/rotatescreenspectre/./portraitr.sh')

    if abs(angleY) < abs(angleX) - buffer:
        if angleX >= 0:
            state = 0
            subprocess.call('/home/thiago/rotatescreenspectre/./landscape.sh')
        else:
            state = 1
            subprocess.call('/home/thiago/rotatescreenspectre/./inverted.sh')


    if state != statePrev:
        subprocess.call(["xrandr", "-o", orientation[state]])

    statePrev = state
    time.sleep(1)

