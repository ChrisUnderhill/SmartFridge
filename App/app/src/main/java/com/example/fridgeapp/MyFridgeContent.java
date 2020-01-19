package com.example.fridgeapp;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;

public class MyFridgeContent extends ArrayAdapter<NotificationData>{
    private NotificationData[] mArray;
    private Context mContext;

    public MyFridgeContent(@NonNull Context context, int resource, @NonNull NotificationData[] objects) {
        super(context, resource, objects);
        mArray = objects;
        mContext = context;
    }

    @Override
    public View getView(int pos, View recycledView, ViewGroup parent){
        if(recycledView==null){
            LayoutInflater vi;
            vi=LayoutInflater.from(mContext);
            recycledView=vi.inflate(R.layout.fridgecontentsitem,null);
        }
        NotificationData notification=mArray[pos];

        TextView itemName = recycledView.findViewById(R.id.fridgeItemName);
        itemName.setText(notification.itemName);

        TextView itemQuantity = recycledView.findViewById(R.id.fridgeItemQuantity);
        itemQuantity.setText(String.valueOf(notification.itemQuantity)+" "+notification.inUnits);

        return recycledView;
    }

}

