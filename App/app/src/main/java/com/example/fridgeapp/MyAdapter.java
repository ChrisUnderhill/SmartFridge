package com.example.fridgeapp;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.recyclerview.widget.RecyclerView;

import com.firebase.ui.auth.data.model.User;

public class MyAdapter extends ArrayAdapter<NotificationData> {

    private NotificationData[] mArray;
    private Context mContext;

    public MyAdapter(@NonNull Context context, int resource, @NonNull NotificationData[] objects) {
        super(context, resource, objects);
        mArray = objects;
        mContext = context;
    }

    @Override
    public View getView(int pos, View recycledView, ViewGroup parent){
        if (recycledView == null) {
            LayoutInflater vi;
            vi = LayoutInflater.from(mContext);
            recycledView = vi.inflate(R.layout.notificationitem, null);
        }


        NotificationData notification = mArray[pos];

        TextView titleView = recycledView.findViewById(R.id.notificationItemTitle);
        titleView.setText(notification.title);

        TextView bodyView = recycledView.findViewById(R.id.notificationItemBody);
        bodyView.setText(notification.messageBody);

        TextView dateTimeView = recycledView.findViewById(R.id.notificationItemDateTime);
        dateTimeView.setText(notification.datetime.toString());

        ImageView iconView = recycledView.findViewById(R.id.notificationItemIcon);
        iconView.setImageResource(R.drawable.fui_ic_googleg_color_24dp);

        return recycledView;
    }

}