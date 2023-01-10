import paho.mqtt.client as mqtt
import json
from tkinter import *
import os

# https://stackoverflow.com/questions/48798410/using-mqtt-to-update-tkinter-gui

#Get the window and set the size
window = Tk()
window.title('Monitor')
window.geometry('640x400')

label_tem = Label(window, text = "Temperature: ", font=('Arial', 32))
label_hum = Label(window, text = "Humidity: ", font=('Arial', 32))
label_ult = Label(window, text = "Ultra: ", font=('Arial', 32))

label_warn_tem = Label(window, text = "", bg = 'red', font=('Arial', 48))
label_warn_hum = Label(window, text = "", bg = 'red', font=('Arial', 48))
label_warn_ult = Label(window, text = "Warning: Someone is too close!!!", bg = 'red', font=('Arial', 48))

label_tem.pack()
label_hum.pack()
label_ult.pack()

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
    ultra_str = m_json[field_ultra]
    humidity_str = m_json[field_humidity]
    if temperature_str != None:
        t = int(temperature_str) / 100
        label_tem['text'] = 'Temperature: ' + str(t) + '°C'
        if int(temperature_str) > 2500:
            label_warn_tem['text'] = "Warning: Temperature is too high!!!"
            label_warn_tem['bg'] = 'red'
            label_warn_tem.pack()
        elif int(temperature_str) < 1400:
            label_warn_tem['text'] = "Warning: Temperature is too low!!!"
            label_warn_tem['bg'] = 'blue'
            label_warn_tem.pack()
        else:
            label_warn_tem.pack_forget()
    if humidity_str != None:
        h = int(humidity_str) / 100
        label_hum['text'] = 'Humidity: ' + str(h) +'%'
        if int(humidity_str) > 6500:
            label_warn_hum['text'] = "Warning: Humidity is too high!!!"
            label_warn_hum['bg'] = 'red'
            label_warn_hum.pack()
        elif int(humidity_str) < 4500:
            label_warn_hum['text'] = "Warning: Humidity is too low!!!"
            label_warn_hum['bg'] = 'blue'
            label_warn_hum.pack()
        else:
            label_warn_hum.pack_forget()
    if ultra_str != None:
        label_ult['text'] = 'Ultra: ' + ultra_str + 'cm'
        if int(ultra_str) < 500:
            label_warn_ult.pack()
        else:
            label_warn_ult.pack_forget()

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
