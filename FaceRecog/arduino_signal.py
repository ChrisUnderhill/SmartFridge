#!/usr/bin/python3

from notifications import bucket, upload_blob
import serial, time, os
from faces import who_is_it
#def who_is_it(filename):
#    return input("Whos there?")

def what_is_it(filename):
    return "monster"

class Item:
    def __init__(self, weight, azure_id):
        self.weight = weight
        self.id = azure_id

    def __eq__(self, other):
        return self.id == other.id

class Person:
    def __init__(self, name):
       self.name = name
       self.fridge_objects = []

    @property
    def weight_owned(self):
        return sum(item.weight for item in self.fridge_objects)

class Fridge:

    def __init__(self):
        self.people = {n: Person(n) for n in ["", "Simon", "Andreas"]}
        self.ser = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=1)
        self.old_pressure = 0
        self.new_pressure = 0
        self.person = ""
        self.door_open = False

    def on_picked_up(self, weight):
        if self.person == "":
            print("I don't know who did that")
        item = Item(weight, what_is_it(self.timestr))
        if item in self.people[self.person].fridge_objects:
            self.people[self.person].fridge_objects.remove(item)
            print(self.person + " picked something up that weighed " + str(weight))
        else:
           print("They shouldn't have taken that")
           self.on_intruder_detected()

    def on_intruder_detected(self):
       upload_blob(bucket, self.timestr + ".jpg", self.timestr)
       # send the picture somewhere

    def on_put_down(self, weight):
        if self.person == "":
            print("I don't know who did that")
        item = what_is_it(self.timestr)
        self.people[self.person].fridge_objects.append(Item(weight, item))
        print(self.person + " put a " + item + " down that weighed " + str(weight))

    def on_door_open(self):
        print("Taking a picture")
        # take a picture
        self.timestr = time.strftime("%H%M%S-%d%m%Y")
        os.system("nohup fswebcam -r 1280x720 " + self.timestr + ".jpg")
        person = who_is_it(self.timestr + ".jpg")
        if person != "":
            self.person = person
        print(self.person + " is at the fridge")
        self.ser.reset_input_buffer()
        time.sleep(5)

    def on_door_close(self):
        print("They went away, pressure is ", self.new_pressure)
        if self.new_pressure - self.old_pressure > 0:
            self.on_put_down(self.new_pressure - self.old_pressure)
        elif self.new_pressure - self.old_pressure < 0:
            self.on_picked_up(self.old_pressure - self.new_pressure)
        else:
            print("They did nothing")
        self.old_pressure = self.new_pressure
        self.person = ""

    def run(self):
        while True:
            temp = self.ser.readline();
            s = temp.decode("utf-8").strip()
            if len(s.split(",")) != 2:
                continue
            touch, pressure = s.split(",")[0], s.split(",")[1]
            self.new_pressure = int(pressure)
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
