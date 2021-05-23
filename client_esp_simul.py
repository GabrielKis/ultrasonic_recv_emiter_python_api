import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

from queue import Queue

mqttBroker ="mqtt.eclipseprojects.io" 

client_name = 'Client_ESP_Simul'
topics_list = [('QTD', 2), ('Waveform', 2)]

cmd_payloads = []
wf_format_payloads = []
wf_send_payloads = []
wf_recv_payloads = []

def on_message(client, userdata, message):
    q.put(message)
    print("{} RECEIVED {} from topic {}".format(client_name, str(message.topic), \
                                            str(message.payload.decode("utf-8"))))
    if message.topic == 'CMD':
        cmd_payloads.append(message.payload.decode("utf-8"))
    elif message.topic == 'Waveform':
        wf_format_payloads.append(message.payload.decode("utf-8"))

def send_data(client_obj):
    client_obj.publish("Ultrasound_send", 'PAYLOAD1')
    print("{} PUBLISH {} to Ultrasound_send".format(str(client_name), 'PAYLOAD1'))
    client_obj.publish("Ultrasound_recv", 'PAYLOAD2')
    print("{} PUBLISH {} to Ultrasound_recv".format(str(client_name), 'PAYLOAD2'))

def receive_data(client_obj):
    client_obj.loop_start()

    client_obj.subscribe(topics_list)
    client_obj.on_message=on_message

    time.sleep(30)
    client_obj.loop_stop()

if __name__ == "__main__":
    q = Queue()
    client_esp = mqtt.Client("Temperature_Inside_Getter", transport="websockets")
    client_esp.connect(mqttBroker, port=80)
    #parse input
    #receive-waveforms
    receive_data(client_esp)
    #send cmd-waveform
    send_data(client_esp)
    client_esp.disconnect()
    #show_data

    print(cmd_payloads)
    print(wf_format_payloads)

    print(q)