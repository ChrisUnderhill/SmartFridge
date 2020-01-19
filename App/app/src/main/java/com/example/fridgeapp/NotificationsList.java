package com.example.fridgeapp;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;

import java.util.Date;

public class NotificationsList extends AppCompatActivity {
    private ListView listView;
    private MyAdapter mAdapter;
    private NotificationData[] data;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_notifications_list);
        listView = (ListView) findViewById(R.id.myListView);

        NotificationData data1 = new NotificationData();
        data1.title = "I am a test title thing";
        data1.messageBody = "body";
        data1.datetime = new Date();
        data1.imageLocation = "/data/data/com.example.fridgeapp/files/test.jpg";


        data = new NotificationData[]{data1};

        // specify an adapter (see also next example)
        mAdapter = new MyAdapter(this, R.layout.notificationitem, data);
        listView.setAdapter(mAdapter);

        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Intent intent = new Intent(NotificationsList.this, Notifications.class);
                intent.putExtra("title", data[position].title);
                intent.putExtra("body", data[position].messageBody);
                intent.putExtra("dateTime", data[position].datetime);
                intent.putExtra("imageLocation", data[position].imageLocation);

                startActivity(intent);
            }
        });
    }


}
