#include <ESP8266WiFi.h>

const char* ssid = "WDIRUSTA";
const char* password =  "USTA8000";
const uint16_t port = 8899;
const char * host = "192.168.30.173";
const char ID = '2';
String data="";
void setup()
{

  Serial.begin(115200);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }

  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());

}

void loop()
{
    WiFiClient client;

    if (!client.connect(host, port)) {

        Serial.println("Connection to host failed");

        delay(1000);
        return;
    }

    //Serial.println("Connected to server successful!");
     if (Serial.available() > 0) {
     data = data+ID+Serial.readString();
     //Serial.print(data);
    client.print(data);
    client.read();
    data="";
     }

    //Serial.println("Disconnecting...");
    client.stop();

    //delay(1000);
}
