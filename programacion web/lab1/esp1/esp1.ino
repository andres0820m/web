#include <ESP8266WiFi.h>

const char* ssid = "red 2";
const char* password =  "79966208";
const uint16_t port = 8899;
const char * host = "192.168.10.106";

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

    Serial.println("Connected to server successful!");

    client.print("2,123,123");

    Serial.println("Disconnecting...");
    client.stop();

    delay(1000);
}
