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
    if s == "":
        continue
    #print("s", s)
    touch, pressure = s.split(",")[0], s.split(",")[1]
    new_pressure = int(pressure)
    #print("touch", touch)
    #print("pressure", pressure)
    if touch != "0":
        print("Taking a picture")
    #     # take a picture
    #     timestr = time.strftime("%H%M%S-%d%m%Y")
    #     os.system("fswebcam -r 1280x720 " + timestr + ".jpg")
    #     print(quickstart.who_is_it(timestr + ".jpg"))
    #     ser.reset_input_buffer()
    #     time.sleep(5)
    print(new_pressure)
    if new_pressure - old_pressure > 10:
        on_put_down()
    elif new_pressure - old_pressure < -10:
        on_picked_up()
    old_pressure = new_pressure
    ser.reset_input_buffer()
    time.sleep(0.1)
