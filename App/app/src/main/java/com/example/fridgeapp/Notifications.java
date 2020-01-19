package com.example.fridgeapp;

import androidx.appcompat.app.AppCompatActivity;

import android.net.Uri;
import android.os.Bundle;
import android.widget.ImageView;
import android.widget.TextView;

public class Notifications extends AppCompatActivity {

    private String imageLocation;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_notifications);

        TextView titleView = findViewById(R.id.detailsTitle);
        titleView.setText(getIntent().getStringExtra("title"));

        TextView bodyView = findViewById(R.id.detailsBody);
        bodyView.setText(getIntent().getStringExtra("body"));

        TextView dateTimeView = findViewById(R.id.detailsDateTime);
        dateTimeView.setText(getIntent().getStringExtra("dateTime"));

        ImageView imageView = findViewById(R.id.detailsImage);
        //imageView.setImageURI(new Uri(getIntent().getStringExtra("imageLocation")));

        //imageLocation = savedInstanceState.getString("imageLocation");
    }
}
