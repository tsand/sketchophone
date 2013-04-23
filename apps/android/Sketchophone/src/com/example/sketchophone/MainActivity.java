package com.example.sketchophone;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;

public class MainActivity extends Activity {
    /**
     * Called when the activity is first created.
     */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        WebView browser = (WebView)findViewById(R.id.browser);
        browser.loadUrl("http://sketchophone.appspot.com"); //Replace google.com with you webapp's URL
    }
}

