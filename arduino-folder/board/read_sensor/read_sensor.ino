#include <DHT.h>
#include <ESP8266WiFi.h>
#include <EEPROM.h>
#include <UUID.h>
#define DHTPIN 5
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
const char* ssid = "<NAME>";
const char* password = "<PASSWORD>";
const char* ip_to_raspberry = "<IP-ADDRESS>"; 
const int port_on_raspberry = 12444;
const char* first_sensor = "temperature";
const char* second_sensor = "humidity";
const char* generated_uuid;
float lastSent1 = 0, lastSent2 = 0;
const float threshold1 = 0.5, threshold2 = 0.5;

UUID uuid;
WiFiClient client;
int UUID1_ADDRESS = 0;
int UUID2_ADDRESS = 1;



void write_uuid(int address, const char* uid) {
  for (int i = 0; i < 36; i++) {
    EEPROM.write(UUID1_ADDRESS + i, uid[i]);
  }
  EEPROM.commit();
}



void read_uuid(int address, char* uid) {
  for (int i = 0; i < 36; i++) {
    uid[i] = EEPROM.read(address + i);    
  }
  uid[16] = '\0';
}





void setup() {
  Serial.begin(9600);
  dht.begin();
  EEPROM.begin(512);
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting....");
  }
  Serial.println("Connected");

  if(!client.connect(IPAddress(<IP-ADDRESS>), port_on_raspberry)){
    Serial.println("Connection failed...");
    delay(5000);
    return;
   }
  
   Serial.println("Hello from esp");

   generated_uuid = uuid.toCharArray();
   write_uuid(UUID1_ADDRESS, generated_uuid);
   Serial.println(generated_uuid);
   uuid.generate();
   generated_uuid = "";
   generated_uuid = uuid.toCharArray();
   write_uuid(UUID2_ADDRESS, generated_uuid);
   
   
}




void loop() {
  // Skickar data till Raspberry
  
  float sensor_one = dht.readTemperature();
  float sensor_two = dht.readHumidity();

  char ID1[37];
  char ID2[37];

  read_uuid(UUID1_ADDRESS, ID1);
  read_uuid(UUID2_ADDRESS, ID2);


  // Lägger till <SENSOR= i början och <END> vid slutet
  if (abs(sensor_one - lastSent1) >= threshold1 || abs(sensor_two - lastSent2) >= threshold2) {
    String message = "<SENSOR=" + String(first_sensor) + ";" + "ID=" +  String(ID1) + ">" + String(sensor_one) + "<END>";
    String second_message = "<SENSOR=" + String(second_sensor) + ";" + "ID=" +  String(ID2) + ">" + String(sensor_two) + "<END>";
    
    client.write(message.c_str());
    client.write(second_message.c_str());

    lastSent1 = sensor_one;
    lastSent2 = sensor_two;
    Serial.println("Sent: " + message);
    Serial.println("Sent: " + second_message);
  }
  delay(1000);

  
}
