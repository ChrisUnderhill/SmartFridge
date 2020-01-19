package com.example.fridgeapp;

import androidx.appcompat.app.AppCompatActivity;

import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import java.io.File;
import java.nio.file.Path;
import java.util.Date;

public class Notifications extends AppCompatActivity {

    private String imageLocation;

    private boolean isBig;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_notifications);

        isBig = false;

        TextView titleView = findViewById(R.id.detailsTitle);
        titleView.setText(getIntent().getStringExtra("title"));

        TextView bodyView = findViewById(R.id.detailsBody);
        bodyView.setText(getIntent().getStringExtra("body"));

        TextView dateTimeView = findViewById(R.id.detailsDateTime);
        Date date = new Date(Long.parseLong(getIntent().getStringExtra("dateTime")));
        dateTimeView.setText(date.toString());

        final ImageView imageView = findViewById(R.id.detailsImage);
        imageView.setImageURI(Uri.fromFile(new File(getIntent().getStringExtra("imageLocation"))));

        imageView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (isBig){
                    imageView.setScaleX(1);
                    imageView.setScaleY(1);
                } else{
                    imageView.setScaleX(2);
                    imageView.setScaleY(2);
                }
                isBig = !isBig;
                imageView.setPivotY(0);

            }
        });

        //imageLocation = savedInstanceState.getString("imageLocation");
    }
}
