package com.example.fridgeapp;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.Date;

import static java.lang.Float.parseFloat;
import static java.lang.Integer.parseInt;

public class NotificationData {
    public int id;
    public String title, imageLocation, messageBody;
    //public int notificationType;
    public Date datetime;
    //for fridge contents
    public String itemName, inUnits;
    public int itemQuantity;

    public String toCSV(){
        return id + ", " + title + ", " + messageBody + ", " + datetime.getTime() + ", " + imageLocation + ", " + itemName + ", " + itemQuantity + ", " + inUnits + "\n";
    }

    public NotificationData fromCSV(String csv){
        String[] splitty = csv.split(", ");

        this.id = parseInt(splitty[0]);
        this.title = splitty[1];
        this.messageBody = splitty[2];
        this.datetime =  new Date(Long.parseLong(splitty[3]));
        this.imageLocation = splitty[4];
        this.itemName = splitty[5];
        this.itemQuantity = parseInt(splitty[6]);
        this.inUnits = splitty[7];

        return this;

    }
}
