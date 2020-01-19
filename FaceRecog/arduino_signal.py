#!/usr/bin/python3

from notifications import bucket, upload_blob, send_to_token_param, send_to_token
import serial, time, os
from faces import who_is_it
import predict
#def who_is_it(filename):
#    return input("Whos there?")

def what_is_in_the_fridge(filename):
    res = predict.main(filename)
    return [x["tagName"] for x in res if x["probability"] > 0.3]

class Item:
    def __init__(self, weight, azure_id):
        self.weight = weight
        self.id = azure_id

    def __eq__(self, other):
        return math.abs(self.weight == other.weight) < 20

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
        self.old_contents = []
        self.new_contents = []
        self.person = ""
        self.door_open = False

    def on_picked_up(self, weight, name):
        if self.person == "":
            print("I don't know who did that")
        item = Item(weight, name)
        if item in self.old_contents:
            self.old_contents.remove(item)
        if item in self.people[self.person].fridge_objects:
            self.people[self.person].fridge_objects.remove(item)
            print(self.person + " picked up a " + name + " that weighed " + str(weight))
        else:
           print("They shouldn't have taken that")
           self.on_intruder_detected(name)

    def on_intruder_detected(self, item_stolen):
       upload_blob(bucket, self.timestr + ".jpg", self.timestr)
       try:
           send_to_token_param(self.person, time.time(), self.timestr, item_stolen)
           print("Detailed notificiation sent")
       except:
           send_to_token()
           print("Notification sent without details")

    def on_put_down(self, weight, name):
        if self.person == "":
            print("I don't know who did that")
        self.people[self.person].fridge_objects.append(Item(weight, name))
        print(self.person + " put a " + name + " down that weighed " + str(weight))
        self.old_contents.append(name)

    def on_door_open(self):
        print("Taking a picture")
        # take a picture
        self.timestr = time.strftime("%H%M%S-%d%m%Y")
        os.system("nohup fswebcam -r 1280x720 " + self.timestr + ".jpg")
        person = who_is_it(self.timestr + ".jpg")
        if person != "":
            self.person = person
            print(self.person + " is at the fridge")
        else:
            print("Somebody is there but I don't know who")
        self.ser.reset_input_buffer()
        time.sleep(5)

    def on_door_close(self):
        print("They went away, pressure is ", self.new_pressure)
        #print("Taking a picture")
        # take a picture
        #self.timestr = time.strftime("%H%M%S-%d%m%Y")
        #os.system("nohup fswebcam -r 1280x720 " + self.timestr + ".jpg")
        #self.ser.reset_input_buffer()
        self.new_contents = what_is_in_the_fridge(self.timestr + ".jpg")
        if self.new_pressure - self.old_pressure > 0 and self.new_contents:
            self.on_put_down(self.new_pressure - self.old_pressure, self.new_contents[0])
        elif self.new_pressure - self.old_pressure < 0:
            self.on_picked_up(self.old_pressure - self.new_pressure, "unknown object")
        else:
            print("They did nothing")
        print("The fridge contains " + " and ".join(self.old_contents))
        #taken_out = [x for x in self.old_contents if x not in self.new_contents]
        #put_in = [x for x in self.new_contents if x not in self.old_contents]
        #for x in taken_out:
        #    self.on_picked_up(0, x)
        #for x in put_in:
        #    self.on_put_down(0, x)
        self.old_pressure = self.new_pressure
        self.person = ""
        #self.old_contents = self.new_contents

    def run(self):
        while True:
            temp = self.ser.readline();
            s = temp.decode("utf-8").strip()
            if len(s.split(",")) != 2:
                continue
            touch, pressure = s.split(",")[0], s.split(",")[1]
            self.new_pressure = int(pressure)
            # print("door: ", "open" if touch == "0" else "closed")
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
