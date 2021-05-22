import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

mqttBroker ="mqtt.eclipseprojects.io" 

client_name = "Client_PC"

#client_pc = mqtt.Client(client_name, transport="tcp")
client_pc = mqtt.Client("Client_PC", transport="websockets")
client_pc.connect(mqttBroker, port=80)

for i in range(0,10):
    #randNumber = uniform(20.0, 21.0)
    client_pc.publish("CMD", i)
    print("{} PUBLISH {} to CMD".format(str(client_name), str(i)))
    time.sleep(0.5)

client_pc.disconnect()
