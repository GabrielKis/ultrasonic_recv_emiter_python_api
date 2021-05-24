import queue
import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

from queue import Queue

#mqttBroker ="mqtt.eclipseprojects.io" 
mqttBroker ="localhost" 

client_name = 'Client_ESP_Simul'
topics_list = [('QTD', 2), ('Waveform', 2)]

def on_message(client, userdata, message):
    q.put(message)
    print("{} RECEIVED {} from topic {}".format(client_name, str(message.topic), \
                                            str(message.payload.decode("utf-8"))))

def send_data(client_obj):
    client_obj.publish("Ultrasound_send", 'PAYLOAD1')
    print("{} PUBLISH {} to Ultrasound_send".format(str(client_name), 'PAYLOAD1'))
    client_obj.publish("Ultrasound_recv", 'PAYLOAD2')
    print("{} PUBLISH {} to Ultrasound_recv".format(str(client_name), 'PAYLOAD2'))

def receive_data(client_obj):
    receive_data_ctrl = [False, False]

    client_obj.loop_start()

    client_obj.subscribe(topics_list)
    client_obj.on_message=on_message

    # espera ate que os topicos de retorno sejam recebidos
    while not all(receive_data_ctrl):
        if not q.empty():
            msg = q.get()
            if msg.topic == 'QTD':
                # salvar mensagem em alguma variavel
                receive_data_ctrl[0] = True
            if msg.topic == 'Waveform':
                receive_data_ctrl[1] = True

    client_obj.loop_stop()

if __name__ == "__main__":
    q = Queue()
    receive_data_ctrl_queue = Queue()
#   client_esp = mqtt.Client("Temperature_Inside_Getter")
    client_esp = mqtt.Client("Temperature_Inside_Getter", transport="websockets")
    client_esp.connect(mqttBroker, port=9001)
    #parse input
    #receive-waveforms
    receive_data(client_esp)
    #send cmd-waveform
    send_data(client_esp)
    client_esp.disconnect()
    #show_data
