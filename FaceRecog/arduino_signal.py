#!/usr/bin/python3

import serial, time, os
from faces import who_is_it


class Fridge:

    def __init__(self):
        self.weight_owned_by_people = {n: 0 for n in ["Simon", "Andreas"]}
        self.ser = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=1)
        self.old_pressure = 0
        self.person = ""
        self.door_open = False

    @property
    def weight_in_fridge(self):
        return sum(self.weight_owned_by_people.values())

    def on_picked_up(self, weight):
        if self.person == "":
            print("I don't know who did that")
            return
        self.weight_owned_by_people[self.person] -= weight
        print(self.person + " picked something up that weighed " + str(weight))

    def on_put_down(self, weight):
        if self.person == "":
            print("I don't know who did that")
            return
        self.weight_owned_by_people[self.person] += weight
        print(self.person + " put something down that weighed " + str(weight))

    def on_door_open(self):
        print("Taking a picture")
        # take a picture
        timestr = time.strftime("%H%M%S-%d%m%Y")
        os.system("fswebcam -r 1280x720 " + timestr + ".jpg")
        person = who_is_it(timestr + ".jpg")
        if person != "":
            self.person = person
        print(self.person + " is at the fridge")
        self.ser.reset_input_buffer()
        time.sleep(5)

    def on_door_close(self):
        print("They went away")
        if self.person == "":
            return
        if self.new_pressure - self.old_pressure > 0:
            self.on_put_down(self.new_pressure - self.old_pressure)
        elif self.new_pressure - self.old_pressure < 0:
            self.on_picked_up(self.old_pressure - self.new_pressure)
        self.old_pressure = self.new_pressure
        self.person = ""

    def run(self):
        while True:
            temp = self.ser.readline();
            s = temp.decode("utf-8").strip()
            if len(s.split(",")) != 2:
                continue
            touch, pressure = s.split(",")[0], s.split(",")[1]
            new_pressure = int(pressure)
            # print("touch", touch)
            # print("pressure", pressure)
            if touch == "0":
                if self.person == "":
                    self.door_open = True
                    self.on_door_open()
            else:
                if self.door_open:
                    self.door_open = False
                    self.on_door_close()
            self.ser.reset_input_buffer()
            time.sleep(0.1)


fridge = Fridge()
fridge.run()
