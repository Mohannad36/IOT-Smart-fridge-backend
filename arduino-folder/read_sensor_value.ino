#include <DHT.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#define DHTPIN 5
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "";
const char* password = "";
const char* ip_to_raspberry = ""; 
const int port_on_raspberry = 0;
const char* sensorName = "Temperature and Humidity sensor";
float lastSentValue1 = 0, lastSentValue2 = 0;
const float threshold1 = 0.5, threshold2 = 0.5;

WiFiUDP udp;

void setup() {
  Serial.begin(9600);
  dht.begin();
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting....");
  }
  Serial.println("Connected");
}




void loop() {


  // Skickar data till Raspberry
  
  float sensor_Value1 = ReadSensor();
  float sensor_Value2 = ReadSensor2();



  
  // Lägger till <SENSOR= i början och <END> vid slutet
  if (abs(sensor_Value1 - lastSentValue1) >= threshold1 || abs(sensor_Value2 - lastSentValue2) >= threshold2) {
    String message = "<SENSOR=" + String(sensorName) + ">" + String(sensor_Value1) + " : " + String(sensor_Value2) + "<END>";
    udp.beginPacket(ip_to_raspberry, port_on_raspberry);
    udp.write(message.c_str());
    udp.endPacket();

    lastSentValue1 = sensor_Value1;
    lastSentValue2 = sensor_Value2;
    Serial.println("Sent: " + message);
  }
  delay(1000);

  
}



float ReadSensor() {
  return dht.readHumidity();
}



float ReadSensor2() {
  return dht.readTemperature();
}
