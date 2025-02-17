#include <DHT.h>
#include <ESP8266WiFi.h>
#define DHTPIN 5
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "<WIFI_NAME>";
const char* password = "<PASSWORD>";
const char* ip_to_raspberry = "10.48.80.101"; 
const int port_on_raspberry = 12444;
const char* sensorName = "TemperatureAndHumiditySensor";
float lastSentValue1 = 0, lastSentValue2 = 0;
const float threshold1 = 0.5, threshold2 = 0.5;

WiFiClient client;

void setup() {
  Serial.begin(9600);
  dht.begin();
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting....");
  }
  Serial.println("Connected");

  if(!client.connect(IPAddress(10,48,80,101), port_on_raspberry)){
    Serial.println("Connection failed...");
    delay(5000);
    return;
   }
   Serial.println("Hello from esp");
}




void loop() {
  // Skickar data till Raspberry
  
  float sensor_Value1 = ReadSensor();
  float sensor_Value2 = ReadSensor2();

  // Lägger till <SENSOR= i början och <END> vid slutet
  if (abs(sensor_Value1 - lastSentValue1) >= threshold1 || abs(sensor_Value2 - lastSentValue2) >= threshold2) {
    String message = "<SENSOR=" + String(sensorName) + ">" + String(sensor_Value1) + " : " + String(sensor_Value2) + "<END>";
    client.write(message.c_str());

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
