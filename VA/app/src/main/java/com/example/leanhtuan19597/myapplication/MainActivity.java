package com.example.leanhtuan19597.myapplication;

import android.app.Application;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.speech.RecognizerIntent;
import android.support.annotation.NonNull;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.SwitchCompat;
import android.util.Log;
import android.view.ContextMenu;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.Toast;

import com.afollestad.materialdialogs.DialogAction;
import com.afollestad.materialdialogs.MaterialDialog;
import com.android.volley.AuthFailureError;
import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.firebase.database.ChildEventListener;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

import ai.api.AIDataService;
import ai.api.AIServiceException;
import ai.api.android.AIConfiguration;
import ai.api.model.AIRequest;
import ai.api.model.AIResponse;
import ai.api.model.Result;

public class MainActivity extends AppCompatActivity {
    SwitchCompat switchRelay1, switchRelay2, switchRelay3, switchRelay4, switchRelay5, switchRelay6;
    CheckBox cbRelay1, cbRelay2, cbRelay3, cbRelay4, cbRelay5, cbRelay6;
    DatabaseReference mDatabase;
    ProgressDialog pg;
    FloatingActionButton fab;
    RequestQueue queue;
    int count = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if (isOnline()) {
            initControls();
            initEvents();
            queue = Volley.newRequestQueue(MainActivity.this);
        } else {
            new MaterialDialog.Builder(this)
                    .title("Thông báo")
                    .content("Vui lòng bật kết nối mạng !")
                    .negativeText("Đóng")
                    .canceledOnTouchOutside(false)
                    .onPositive(new MaterialDialog.SingleButtonCallback() {
                        @Override
                        public void onClick(@NonNull MaterialDialog dialog, @NonNull DialogAction which) {
                            Toast.makeText(getApplicationContext(), "On", Toast.LENGTH_LONG).show();
                        }
                    })
                    .onNegative(new MaterialDialog.SingleButtonCallback() {
                        @Override
                        public void onClick(@NonNull MaterialDialog dialog, @NonNull DialogAction which) {
                            System.exit(1);
                        }
                    }).show();
        }
    }

    /**/
    public void initControls() {
        switchRelay1 = findViewById(R.id.switchRelay1);
        switchRelay2 = findViewById(R.id.switchRelay2);
        switchRelay3 = findViewById(R.id.switchRelay3);
        switchRelay4 = findViewById(R.id.switchRelay4);
        switchRelay5 = findViewById(R.id.switchRelay5);
        switchRelay6 = findViewById(R.id.switchRelay6);

        cbRelay1 = findViewById(R.id.cbRelay1);
        cbRelay2 = findViewById(R.id.cbRelay2);
        cbRelay3 = findViewById(R.id.cbRelay3);
        cbRelay4 = findViewById(R.id.cbRelay4);
        cbRelay5 = findViewById(R.id.cbRelay5);
        cbRelay6 = findViewById(R.id.cbRelay6);

        mDatabase = FirebaseDatabase.getInstance().getReference();

        pg = new ProgressDialog(MainActivity.this);
        fab = findViewById(R.id.fab);
    }

    public boolean isOnline() {
        ConnectivityManager cm =
                (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo netInfo = cm.getActiveNetworkInfo();
        return netInfo != null && netInfo.isConnectedOrConnecting();
    }

    /**/
    public void initEvents() {
        processing(switchRelay1, cbRelay1, "Relay1");
        processing(switchRelay2, cbRelay2, "Relay2");
        processing(switchRelay3, cbRelay3, "Relay3");
        processing(switchRelay4, cbRelay4, "Relay4");
        processing(switchRelay5, cbRelay5, "Relay5");
        processing(switchRelay6, cbRelay6, "Relay6");

        pg.setMessage("Đang khởi động hệ thống...");
        pg.setCancelable(false);
        pg.show();

        mDatabase.child("MinhTrung").addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                for (DataSnapshot dt : dataSnapshot.getChildren()) {
                    restoreData(dt);
                }
                pg.dismiss();
            }

            @Override
            public void onCancelled(DatabaseError databaseError) {

            }
        });

        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());

                if (intent.resolveActivity(getPackageManager()) != null) {
                    startActivityForResult(intent, 10);
                }
            }
        });
    }

    /**/
    public void restoreData(DataSnapshot dt) {
        String key = dt.getKey();
        Boolean blink = (Boolean) dt.child("Blink").getValue();
        Boolean turnOn = (Boolean) dt.child("TurnOn").getValue();


        if (key.equals("Relay1")) {
            if (turnOn) {
                switchRelay1.setChecked(true);
                cbRelay1.setEnabled(true);
            }

            if (blink) {
                cbRelay1.setChecked(true);
                switchRelay1.setEnabled(false);
            }
        } else if (key.equals("Relay2")) {
            if (turnOn) {
                switchRelay2.setChecked(true);
                cbRelay2.setEnabled(true);
            }

            if (blink) {
                cbRelay2.setChecked(true);
                switchRelay2.setEnabled(false);
            }
        } else if (key.equals("Relay3")) {
            if (turnOn) {
                switchRelay3.setChecked(true);
                cbRelay3.setEnabled(true);
            }

            if (blink) {
                cbRelay3.setChecked(true);
                switchRelay3.setEnabled(false);
            }
        } else if (key.equals("Relay4")) {
            if (turnOn) {
                switchRelay4.setChecked(true);
                cbRelay4.setEnabled(true);
            }

            if (blink) {
                cbRelay4.setChecked(true);
                switchRelay4.setEnabled(false);
            }
        } else if (key.equals("Relay5")) {
            if (turnOn) {
                switchRelay5.setChecked(true);
                cbRelay5.setEnabled(true);
            }

            if (blink) {
                cbRelay5.setChecked(true);
                switchRelay5.setEnabled(false);
            }
        } else if (key.equals("Relay6")) {
            if (turnOn) {
                switchRelay6.setChecked(true);
                cbRelay6.setEnabled(true);
            }

            if (blink) {
                cbRelay6.setChecked(true);
                switchRelay6.setEnabled(false);
            }
        }

    }

    /**/
    public void processing(final SwitchCompat switchRelay, final CheckBox cbRelay, final String relay) {

        switchRelay.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean b) {
                if (b) {
                    cbRelay.setEnabled(true);
                    mDatabase.child("MinhTrung/" + relay + "/TurnOn").setValue(true);
                    // Toast.makeText(getApplicationContext(), "Bat den 1", Toast.LENGTH_LONG).show();
                } else {
                    mDatabase.child("MinhTrung/" + relay + "/TurnOn").setValue(false);
                    cbRelay.setEnabled(false);
                    Toast.makeText(getApplicationContext(), "Tat den 1", Toast.LENGTH_LONG).show();
                }
            }
        });

        cbRelay.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean b) {
                if (b) {
                    switchRelay.setEnabled(false);
                    mDatabase.child("MinhTrung/" + relay + "/Blink").setValue(true);
                    Toast.makeText(getApplicationContext(), "Bat nhap nhay", Toast.LENGTH_LONG).show();
                } else {
                    switchRelay.setEnabled(true);
                    mDatabase.child("MinhTrung/" + relay + "/Blink").setValue(false);
                    Toast.makeText(getApplicationContext(), "Tat nhap nhay", Toast.LENGTH_LONG).show();
                }
            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        return super.onOptionsItemSelected(item);
    }

    public void queryFromAPIAI(String query) {
        /*api ai*/
        final AIConfiguration config = new AIConfiguration("873c83cbf665414a885eebbf5d5bd448",
                AIConfiguration.SupportedLanguages.English,
                AIConfiguration.RecognitionEngine.System);

        final AIDataService aiDataService = new AIDataService(config);

        final AIRequest aiRequest = new AIRequest();
        aiRequest.setQuery(query);

        new AsyncTask<AIRequest, Void, AIResponse>() {
            @Override
            protected AIResponse doInBackground(AIRequest... requests) {
                final AIRequest request = requests[0];
                try {
                    final AIResponse response = aiDataService.request(aiRequest);
                    return response;
                } catch (AIServiceException e) {
                }
                return null;
            }

            @Override
            protected void onPostExecute(AIResponse aiResponse) {
                if (aiResponse != null) {
                    final Result result = aiResponse.getResult();
                    String action = result.getAction().toString();
                    Toast.makeText(getApplicationContext(), action, Toast.LENGTH_LONG).show();

//                    if (action.equals("BatDen1")) {
//                        switchRelay1.setChecked(true);
//                        mDatabase.child("MinhTrung/Relay1/TurnOn").setValue(true);
//                    } else if (action.equals("TatDen1")) {
//                        checkTurnOffBlink(cbRelay1, switchRelay1, "MinhTrung/Relay1/TurnOn");
//                    } else if (action.equals("BatDen2")) {
//                        switchRelay2.setChecked(true);
//                        mDatabase.child("MinhTrung/Relay2/TurnOn").setValue(true);
//                    } else if (action.equals("TatDen2")) {
//                        checkTurnOffBlink(cbRelay2, switchRelay2, "MinhTrung/Relay2/TurnOn");
//
//                    } else if (action.equals("BatDen3")) {
//                        switchRelay3.setChecked(true);
//                        mDatabase.child("MinhTrung/Relay3/TurnOn").setValue(true);
//                    } else if (action.equals("TatDen3")) {
//                        checkTurnOffBlink(cbRelay3, switchRelay3, "MinhTrung/Relay3/TurnOn");
//
//                    } else if (action.equals("BatDen4")) {
//                        switchRelay4.setChecked(true);
//                        mDatabase.child("MinhTrung/Relay4/TurnOn").setValue(true);
//                    } else if (action.equals("TatDen4")) {
//                        checkTurnOffBlink(cbRelay4, switchRelay4, "MinhTrung/Relay4/TurnOn");
//
//                    } else if (action.equals("BatDen5")) {
//                        switchRelay5.setChecked(true);
//                        mDatabase.child("MinhTrung/Relay5/TurnOn").setValue(true);
//                    } else if (action.equals("TatDen5")) {
//                        checkTurnOffBlink(cbRelay5, switchRelay5, "MinhTrung/Relay5/TurnOn");
//
//                    } else if (action.equals("BatDen6")) {
//                        switchRelay6.setChecked(true);
//                        mDatabase.child("MinhTrung/Relay6/TurnOn").setValue(true);
//                    }
//                    //Blink
//                    else if (action.equals("BatNhapNhayDen1")) {
//                        Toast.makeText(getApplicationContext(), "Bat nhap nhay den 1", Toast.LENGTH_LONG).show();
//                    } else if (action.equals("TatNhapNhayDen1")) {
//                        Toast.makeText(getApplicationContext(), "Tat nhap nhay den 1", Toast.LENGTH_LONG).show();
//                    } else if (action.equals("BatNhapNhayDen2")) {
//                        Toast.makeText(getApplicationContext(), "Bat nhap nhay den 2", Toast.LENGTH_LONG).show();
//                    } else if (action.equals("TatNhapNhayDen2")) {
//                        Toast.makeText(getApplicationContext(), "Tat nhap nhay den 2", Toast.LENGTH_LONG).show();
//                    } else if (action.equals("BatNhapNhayDen3")) {
//                        Toast.makeText(getApplicationContext(), "Bat nhap nhay den 3", Toast.LENGTH_LONG).show();
//                    } else if (action.equals("TatNhapNhayDen3")) {
//                        Toast.makeText(getApplicationContext(), "Tat nhap nhay den 3", Toast.LENGTH_LONG).show();
//                    } else {
//                        new MaterialDialog.Builder(MainActivity.this)
//                                .title("Thông báo")
//                                .content("Hệ thống không nhận dạng được giọng nói, vui lòng nói lại!")
//                                .negativeText("Đóng")
//                                .canceledOnTouchOutside(false)
//                                .show();
//                    }
                }
            }
        }.execute(aiRequest);
    }

    /*
    * */
    public void checkTurnOffBlink(CheckBox cb, SwitchCompat switchRelay, String child) {
        if (!cb.isChecked()) {
            switchRelay.setChecked(false);
            mDatabase.child(child).setValue(false);
            return;
        }
        showDialog();
    }

    public void showDialog() {
        new MaterialDialog.Builder(this)
                .title("Thông báo")
                .content("Vui lòng tắt nhấp nháy trước!")
                .negativeText("Đóng")
                .canceledOnTouchOutside(false)
                .show();
    }

    @Override
    protected void onActivityResult(final int requestCode, int resultCode, Intent data) {
        if (requestCode == 10) {
            if (resultCode == RESULT_OK && data != null) {
                count++;
                ArrayList<String> result = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
                final String textRespone = result.get(0).toString();
                Toast.makeText(getApplicationContext(),textRespone, Toast.LENGTH_LONG).show();
               // queryFromAPIAI(textRespone);
//                Toast.makeText(getApplicationContext(), textRespone + " " + count, Toast.LENGTH_LONG).show();
//                String url = "http://192.168.1.12:3000/query";
//
//                JSONObject postparams = new JSONObject();
//                try {
//                    postparams.put("text", textRespone);
//                } catch (JSONException e) {
//                    e.printStackTrace();
//                }
//
//                JsonObjectRequest request = new JsonObjectRequest(
//                        Request.Method.POST, url, postparams,
//                        new Response.Listener<JSONObject>() {
//                            @Override
//                            public void onResponse(JSONObject response) {
//                                Toast.makeText(getApplicationContext(), response.toString(), Toast.LENGTH_LONG).show();
//                            }
//                        },
//                        new Response.ErrorListener() {
//                            @Override
//                            public void onErrorResponse(VolleyError error) {
//                                Toast.makeText(getApplicationContext(), error.toString(), Toast.LENGTH_LONG).show();
//                            }
//                        }) {
//                };
//
//                request.setRetryPolicy(new DefaultRetryPolicy(
//                        0,
//                        DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
//                        DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
//                queue.add(request);
            }
        }
    }
}
