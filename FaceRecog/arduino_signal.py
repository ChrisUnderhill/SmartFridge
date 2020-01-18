#!/usr/bin/python3

import serial, string, time, os, quickstart
from serial import Serial


output = " "
ser = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=1);

def on_picked_up():
    print("You picked something up")

def on_put_down():
    print("You put something down")

old_pressure = 0
while True:
    temp = ser.readline();
    s = temp.decode("utf-8").strip()
    touch, pressure = s.split(",")
    new_pressure = int(pressure)
    if touch != "0":
        # take a picture
        timestr = time.strftime("%H%M%S-%d%m%Y")
        os.system("fswebcam -r 1280x720 " + timestr + ".jpg")
        print(quickstart.who_is_it(timestr + ".jpg"))
        ser.reset_input_buffer()
        time.sleep(5)
    if new_pressure > old_pressure:
        on_put_down()
    elif new_pressure < old_pressure:
        on_picked_up()
