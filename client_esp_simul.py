import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

mqttBroker ="mqtt.eclipseprojects.io" 

client_name = 'Client_ESP_Simul'

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))

client = mqtt.Client("Temperature_Inside_Getter", transport="websockets")
client.connect(mqttBroker, port=80)

client.loop_start()

client.subscribe("CMD")
client.on_message=on_message

time.sleep(30)
client.loop_stop()
