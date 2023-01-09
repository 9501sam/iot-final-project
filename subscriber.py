import paho.mqtt.client as mqtt
import json
from tkinter import *
import os

# https://stackoverflow.com/questions/48798410/using-mqtt-to-update-tkinter-gui

#Get the window and set the size
window = Tk()
window.geometry('640x400')

label = Label(window, text = "hello")
label.pack()

field_ultra = 'field1'
field_temperature = 'field2'
field_humidity = 'field3'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    m_json = json.loads(msg.payload)
    # print("field1="+m_json["field1"])
    temperature_str = m_json[field_temperature]
    label['text'] = temperature_str

username = "DjkSFDAMJCQfAyw1MDwOHjk"
clientId = "DjkSFDAMJCQfAyw1MDwOHjk"
password = "je0+n3TBjZzjwwN6d08ZW5RL"
channelId = "2002997"
broker_address = "mqtt3.thingspeak.com"
port = 1883
topic = "channels/" + channelId + "/subscribe"

client = mqtt.Client(clientId)
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username, password)
client.connect(broker_address, port, 60)
client.loop_start()

window.mainloop()
