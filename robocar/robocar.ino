//https://console.firebase.google.com/u/0/project/led-blink-wifi/database/led-blink-wifi-default-rtdb/data

#include <ESP8266WiFi.h>
#include "FirebaseESP8266.h"
//#include <Servo.h>
 
int sensor1 = 5;              // D5=GPIO14, the pin that the sensor is atteched to
int sensor2 = 4;              // D4=GPIO2, the pin that the sensor is atteched to
int state = LOW;             // by default, no motion detected
int val1, val2;  

//#define WIFI_SSID "Galaxy M116379"
//#define WIFI_PASSWORD "kvow3925"

#define WIFI_SSID "Vicky"
#define WIFI_PASSWORD "oyevicks"

#define FIREBASE_HOST "************************************"
#define FIREBASE_AUTH "************************************"

FirebaseData firebaseData;

void setup() {
//  Servo1.attach(servoPin); 
  
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }
  
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();
  
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);

  //Set database read timeout to 1 minute (max 15 minutes)
  Firebase.setReadTimeout(firebaseData, 1000 * 60);

  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);
}

void loop() {

 val1 = digitalRead(sensor1);
  val2 = digitalRead(sensor2);
  delay(50); 
  // read sensor value
  if (val1 == HIGH) {           // check if the sensor is HIGH

    if (Firebase.setInt(firebaseData,"/slot1",val1))
    {
      Serial.println("slot1 : 1");
    }
  } 
  else {
    
 if (Firebase.setInt(firebaseData,"/slot1",val1))
    {  
      Serial.println("slot1 : 0");
    }
  }

  // read sensor value
 
  if (val2 == HIGH) {           // check if the sensor is HIGH

    if (Firebase.setInt(firebaseData,"/slot2",val2))
    {
      Serial.println("slot2 : 1");
    }
  } 
  else {
    
 if (Firebase.setInt(firebaseData,"/slot2",val2))
    {  
      Serial.println("slot2 : 0");
    }
  }
     
    delay(100);
}
