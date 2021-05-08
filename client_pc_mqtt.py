import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

from queue import Queue

mqttBroker ="mqtt.eclipseprojects.io" 
client_name = "Client_PC"

topics_pub_list = [('QTD', 2), ('Waveform', 2)]
topics_sub_list = [('Ultrasound_send', 2), ('Ultrasound_recv', 2)]

def on_message(client, userdata, message):
    q.put(message)
    print("{} RECEIVED {} from topic {}".format(client_name, str(message.topic), \
                                            str(message.payload.decode("utf-8"))))

def send_data(client_obj):
    #client_pc = mqtt.Client(client_name, transport="tcp")

    #randNumber = uniform(20.0, 21.0)
    client_obj.publish("QTD", 5)
    print("{} PUBLISH {} to QTD".format(str(client_name), 5))
    client_obj.publish("Waveform", 'SINE')
    print("{} PUBLISH {} to Waveform".format(str(client_name), 'Sine'))

def receive_data(client_obj):
    receive_data_ctrl = [False, False]

    client_obj.loop_start()

    client_obj.subscribe(topics_sub_list)
    client_obj.on_message=on_message

    # espera ate que os topicos de retorno sejam recebidos
    while not all(receive_data_ctrl):
        if not q.empty():
            msg = q.get()
            if msg.topic == topics_sub_list[0][0]:
                receive_data_ctrl[0] = True
            if msg.topic == topics_sub_list[1][0]:
                receive_data_ctrl[1] = True

    client_obj.loop_stop()

if __name__ == "__main__":
    q = Queue()
    client_pc = mqtt.Client("Client_PC", transport="websockets")
    client_pc.connect(mqttBroker, port=80)
    #parse input
    #send cmd-waveform
    send_data(client_pc)
    #receive-waveforms
    receive_data(client_pc)
    client_pc.disconnect()
    #show_data
