import paho.mqtt.client as mqtt

username = "Ny4HECE1BwgpCwwfOxsPDSU"
clientId = "Ny4HECE1BwgpCwwfOxsPDSU"
password = "StySmalK9G7Xn2WuualO1MVS"
channelId = "2002997"
broker_address = "mqtt3.thingspeak.com"
port = 1883
topic = "channels/" + channelId + "/publish"

# field1: ultrasonic
# field2: temperature
# field3: humidity
payload = "field2=777"

mqtt_client_id = "OjAzFTQVAg8lDzgTNCwRDh0"
mqtt_username = "OjAzFTQVAg8lDzgTNCwRDh0"
mqtt_password = "6Tuy+aahsfEORwESWK3iqRob"
mqtt_port = 1883
mqtt_topic = "channels/" + channelId + "/publish"

mqttc = mqtt.Client(clientId, protocol=mqtt.MQTTv311)
mqttc.username_pw_set(username, password)
mqttc.connect(broker_address, port)

mqttc.publish(topic, payload)
