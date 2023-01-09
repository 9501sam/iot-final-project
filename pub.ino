#include <LWiFi.h>
#include <PubSubClient.h>
#include <Ultrasonic.h>
#include "LDHT.h"

// char ssid[] = "iPhone";
// char password[] = "00000000";
char ssid[] = "Xperia XZ Premium_6ab5";
char password[] = "3c63283b83e8";
char mqtt_server[] = "mqtt3.thingspeak.com";
char pub_topic_ultrasonic[] = "channels/2002997/publish/fields/field1";
char pub_topic_temperature[] = "channels/2002997/publish/fields/field2";
char pub_topic_humidity[] = "channels/2002997/publish/fields/field3";
char client_Id[] = "Ny4HECE1BwgpCwwfOxsPDSU";
char user_name[] = "Ny4HECE1BwgpCwwfOxsPDSU";
char passwd[] = "StySmalK9G7Xn2WuualO1MVS";
int mqtt_port = 1883;

int status = WL_IDLE_STATUS;
WiFiClient client;
PubSubClient upload(client);

#define ULTRASONIC_PIN 3
#define DHTPIN 10          // what pin we're connected to
#define DHTTYPE DHT22     // using DHT11 sensor
Ultrasonic ultrasonic(ULTRASONIC_PIN);
LDHT dht(DHTPIN,DHTTYPE);

void reconnect()
{
    // Loop until we're reconnected
    while (!upload.connected()) {
        Serial.print("Attempting MQTT connection...");
        if (upload.connect(client_Id, user_name, passwd)) {
            Serial.println("connected");

        } else {
            Serial.print("failed, rc=");
            Serial.print(upload.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}

void setup()
{
    Serial.begin(9600);

    while (status != WL_CONNECTED) {
        Serial.print("Attempting to connect to SSID: ");
        Serial.println(ssid);
        // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
        status = WiFi.begin(ssid, password);

    }
    Serial.println("Connected to wifi");
    printWifiStatus();

    // if analog input pin 0 is unconnected, random analog
    // noise will cause the call to randomSeed() to generate
    // different seed numbers each time the sketch runs.
    // randomSeed() will then shuffle the random function.
    randomSeed(analogRead(0));

    upload.setServer(mqtt_server, mqtt_port);
    dht.begin();
    delay(1500);
}

void loop()
{
    if (!upload.connected()) {
        reconnect();
    } else {
        int distance_cm;
        int danger_distance = 50;
        float temperature;
        float humidity;
        long microsec = ultrasonic.timing();
        String payload_distance;
        String payload_temperature;
        String payload_humidity;

        distance_cm = ultrasonic.convert(microsec, Ultrasonic::CM);
        if (dht.read()) {
            temperature = dht.readTemperature();
            humidity = dht.readHumidity();
        }

        payload_distance = String(distance_cm);
        payload_temperature = String((int)(temperature * 100));
        payload_humidity = String((int)(humidity * 100));

        if (distance_cm < danger_distance) {
            if (upload.publish(pub_topic_ultrasonic, payload_distance.c_str()))
                Serial.println("distance => " + payload_distance + " has been sent to " + mqtt_server + ".");
        } else {
            if (upload.publish(pub_topic_temperature, payload_temperature.c_str()))
                Serial.println("temperature => " + payload_temperature + " has been sent to " + mqtt_server + ".");
            delay(12000);
            if (upload.publish(pub_topic_humidity, payload_humidity.c_str()))
                Serial.println("humidity => " + payload_humidity + " has been sent to " + mqtt_server + ".");

        }
        delay(100);
    }

    upload.loop();
    delay(5000);
}

void printWifiStatus()
{
    Serial.print("SSID: ");
    Serial.println(WiFi.SSID());

    // print your WiFi shield's IP address:
    IPAddress ip = WiFi.localIP();
    Serial.print("IP Address: ");
    Serial.println(ip);

    // print the received signal strength:
    long rssi = WiFi.RSSI();
    Serial.print("signal strength (RSSI):");
    Serial.print(rssi);
    Serial.println(" dBm");
}
