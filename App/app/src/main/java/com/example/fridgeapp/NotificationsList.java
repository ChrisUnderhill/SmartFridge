package com.example.fridgeapp;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Date;
import java.util.LinkedList;

public class NotificationsList extends AppCompatActivity {
    private ListView listView;
    private MyAdapter mAdapter;
    private NotificationData[] dataarray;
    private LinkedList<NotificationData> dataList;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_notifications_list);
        listView = (ListView) findViewById(R.id.myListView);
/*
        NotificationData data1 = new NotificationData();
        data1.title = "I am a test title thing";
        data1.messageBody = "body";
        data1.datetime = new Date(Long.parseLong(remoteMessage.getData().get("time"));
        data1.imageLocation = "/data/data/com.example.fridgeapp/files/test.jpg";
*/
        dataList = new LinkedList<NotificationData>();


        try {
            Path CSVPath = Paths.get(getFilesDir() + "/database.csv");
            File database = new File(CSVPath.toString());
            BufferedReader br = new BufferedReader(new FileReader(database));

            String st;
            while(( st = br.readLine()) != null) {
                dataList.add(new NotificationData().fromCSV(st));
            }

            br.close();
        }
        catch(Exception e){
            Log.e("TAG", "Something gone very very very wrong with file reading from database.");
            Log.e("TAGGINGMYOWNERROR", e.getStackTrace().toString());
            e.printStackTrace();
        }

        Object[] objarr = dataList.toArray();

        dataarray = Arrays.copyOf(objarr, objarr.length, NotificationData[].class);
        // specify an adapter (see also next example)
        mAdapter = new MyAdapter(this, R.layout.notificationitem, dataarray);
        listView.setAdapter(mAdapter);

        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Intent intent = new Intent(NotificationsList.this, Notifications.class);
                intent.putExtra("title", dataarray[position].title);
                intent.putExtra("body", dataarray[position].messageBody);
                intent.putExtra("dateTime", Long.toString(dataarray[position].datetime.getTime()));
                intent.putExtra("imageLocation", dataarray[position].imageLocation);

                startActivity(intent);
            }
        });
    }


}
