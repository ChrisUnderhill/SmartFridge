/usr/bin/python3

import serial, string, time, os, quickstart
from serial import Serial


output = " "
ser = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=1);

while True:
    temp = ser.readline();
    if(temp  == b''):
        print("Off")
    else:
        timestr = time.strftime("%H%M%S-%d%m%Y")
        os.system("fswebcam -r 1280x720 " + timestr + ".jpg")
        print(quickstart.who_is_it(timestr + ".jpg"))
        ser.reset_input_buffer()
        time.sleep(5)
