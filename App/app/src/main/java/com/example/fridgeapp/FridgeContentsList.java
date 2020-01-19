package com.example.fridgeapp;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Notification;
import android.os.Bundle;
import android.widget.ListView;

public class FridgeContentsList extends AppCompatActivity {
    private ListView listView;
    private MyFridgeContent mFridgCont;
    private NotificationData[] data;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_fridge_contents);
        listView = (ListView) findViewById(R.id.myFridgeContentsView);
        //
        NotificationData data2 = new NotificationData();
        data2.itemName = "milk";
        data2.itemQuantity = 1000;
        data2.inUnits = "ml";
        data = new NotificationData[]{data2};

        // specify an adapter (see also next example)
        mFridgCont = new MyFridgeContent(this, R.layout.fridgecontentsitem, data);
        listView.setAdapter(mFridgCont);


    }

}
